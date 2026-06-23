# Spec -- journal-land cross-fleet (kill recurring journal-branch drift)

> **Status (2026-06-23):** shipped -- journal-land.ps1 live (CLAUDE.md helper)

Date: 2026-05-29
Status: Design (pending Eduardo review)
Scope repo: codemasterdd-ai-station (own repo, branch+PR, auto-merge per ORCHESTRATION.md sec 5)
Governs: both fleet PCs (Lenovo .10 + Ryzen .11)
ASCII-first (ADR-0021).

## 1. Problem (root cause, evidence-backed)

Symptom (observed 3x in the 2026-05-29 session): Ryzen (`DESKTOP-T77TMKT`, .11) keeps
ending up on per-session JOURNAL branches on codemasterdd -- `chore/journal-coop-ws-surface-2026-05-29`,
`docs/journal-task8-2026-05-29` -- each carrying a `docs(journal): ...` commit. They never
merge; content is manually recovered to main each session (PR #214 + later edits). Pulling
main while HEAD is on such a branch creates stray `ort` merge commits and diverges fleet HEADs.

Investigation (systematic-debugging Phase 1, SSH read-only to Ryzen + local reads):

- **Ryzen reflog** reproduces the mechanism 3x: `checkout main -> chore/journal-* (or docs/journal-*)`,
  `commit docs(journal): ...`, then `git pull origin main` WHILE ON THE BRANCH = `Merge made by
  the 'ort' strategy` (the stray merge), then `checkout ... -> main`, commit stranded.
- **Branch prefix divergence**: Lenovo sessions use `claude/*` (matches the `git push origin
  claude/*` standing allow-rule -> push -> PR -> merge). Ryzen sessions use `chore/journal-*` /
  `docs/journal-*` -> prefix does NOT match the allow-rule -> autonomous session will not push.
- **Ryzen gh token INVALID** (`gh auth status`: "The token in default is invalid") -> cannot
  `gh pr create` regardless.
- **Ryzen push capability is HEALTHY**: origin = `git@github.com:...` (SSH), and
  `ssh -T git@github.com` -> "Hi MasterDD-L34D! You've successfully authenticated". So Ryzen
  CAN `git push` via its SSH key; only `gh` (PR creation) is broken.

Ruled OUT with evidence: rogue hook (3 hooks read = `journal-drift-check.ps1` / `session-start-marker.ps1`
/ `tddguard-seed-instructions.ps1` are all check/seed-only, zero git mutation); scheduled task
(`Get-ScheduledTask` filter for journal/git/drift/... = empty); Ryzen-local settings override
(`.claude` dir has only `settings.json` = the committed file; no `settings.local.json`, no extra hooks).

**Root cause (single):** Ryzen journals codemasterdd work onto commit-type-prefixed branches that
miss the `claude/*` push allow-rule; the dead gh token blocks PR creation; so the journal commit
never reaches origin and must be manually recovered every session. Compounded by `git pull` run
on the feature branch (stray merges). It is a branch-naming + completion convention defect, NOT a
hook/cron/settings problem. Push itself works (SSH).

## 2. Decision

**Approach 1 (approved): fix the originating workflow.** A canonical landing helper
`scripts/fleet/journal-land.ps1` + a doctrine convention. Prevents stranding at the SOURCE
(content always reaches origin via a pushable `claude/*` branch), no credential fix required.

Rejected:
- **Doc-only convention** -- anti-pattern #12 (doc-only policy self-violates; this bug IS a
  vague-doc failure). Convention alone would re-fail.
- **cross-fleet-drift-monitor cron** (detect stranded branches -> auto-PR) -- anti-pattern #11+#13
  (cron + SSH cross-shell scan + PR-bot = more failure surface than the manual recovery it
  replaces). It mops up after the fact and does not prevent the stray-merge. Only justified if
  Ryzen could not push -- but it can (SSH). Solving a problem we can prevent.

## 3. Architecture

Two units, one clear purpose each:

1. **`scripts/fleet/journal-land.ps1`** -- deterministic git landing. Does NOT edit JOURNAL.md
   content (newest-first insert needs session judgment); it lands an already-made edit.
2. **Doctrine** -- ORCHESTRATION.md + CLAUDE.md tell sessions WHEN/HOW to journal and to use the
   helper. The helper is the enforcement that makes the convention stick (anti-pattern #12 fix).

Data flow:
```
session edits JOURNAL.md (newest-first, after the --- divider)
   -> journal-land.ps1 -Subject "docs(journal): <desc>"
      -> git fetch origin main
      -> git stash push -- <paths>            (carry the edit off main)
      -> git switch -c claude/journal-<host>-<date> origin/main   (clean base; no divergence)
      -> git stash pop                        (re-apply edit; conflict -> abort+recover)
      -> git add <paths> ; git commit -F <tmp> (subject + ADR-0011 trailers; ASCII no-BOM)
      -> git push -u origin <branch>          (SSH; works on BOTH PCs today)
      -> gh authed? create PR [+ auto-merge --squash --delete-branch]
                    : print "pushed; PR pending (open from hub / fix gh)"  (Ryzen path)
      -> git switch <original-branch>         (return; other working changes untouched)
```

Why `claude/journal-<host>-<date>`: `claude/*` matches the existing push allow-rule (sec 6
ORCHESTRATION) -> frictionless push, no settings change. `<host>` = sanitized `$env:COMPUTERNAME`
(disambiguates Lenovo vs Ryzen same-day). Collision (2nd journal same host+day) -> append
`-<HHmmss>`.

Why base on `origin/main` (fetch + stash): the journal PR contains ONLY the journal change on top
of latest origin -- never carries Ryzen's local-main divergence into the PR, and never produces a
stray merge.

## 4. Helper interface

`scripts/fleet/journal-land.ps1`

| Param | Type | Default | Purpose |
|-------|------|---------|---------|
| `-Subject` | string (required) | -- | Conventional-commit subject, e.g. `docs(journal): coop-WS surface 3 PR`. Validated: matches `^(feat|fix|docs|...)(\(scope\))?!?: .+`, <=72 chars, no trailing period, lowercase after type. Fail-fast with a clear message (mirrors commit-guard so we never hit a hook block). |
| `-Path` | string[] | `@('JOURNAL.md')` | Files to include. Lets a session land COMPACT_CONTEXT.md / memory in the same journal PR. |
| `-NoMerge` | switch | (off) | Create PR only, skip auto-merge. Default behavior = create PR + `gh pr merge --auto --squash --delete-branch` (JOURNAL append = docs class = AUTO-MERGE per autonomy ladder sec 5). |
| `-DryRun` | switch | (off) | Print the planned branch + actions; no mutation. |

Behavior contract:
- Verifies it is running in the codemasterdd repo (origin url contains `codemasterdd-ai-station`)
  -> refuse otherwise (safety).
- If `-Path` files have no changes -> exit 0, "nothing to journal" (idempotent, not an error).
- gh-unauthed (Ryzen): push still happens; exits 0 with "branch pushed to origin, PR pending".
  Content is on origin = NOT stranded. This is the key win -- the dead gh token is a non-blocker.
- Any git step gated on `$LASTEXITCODE` only, with `$ErrorActionPreference='Continue'`
  (anti-pattern L-040: native git writes to stderr on success; must not be read as failure).
- On mid-sequence failure: best-effort return to the original branch; the commit (if made) stays
  on the pushed branch (nothing lost); print recovery guidance.
- Commit via `-F <tempfile>` (NOT `-m`): tempfile holds subject + blank + trailers
  (`Coding-Agent: claude-opus-4.8`, `Trace-Id: <uuid>` -- uuidv7 via a small inline generator
  [unix-ms prefix + random, ~8 lines] to satisfy ADR-0011; the hooks do not enforce the trailer,
  so a v4 `[guid]::NewGuid()` is an acceptable fallback if the generator misbehaves). Written ASCII no-BOM via
  `[IO.File]::WriteAllText` (anti-pattern #12: never `Set-Content -Encoding utf8` = BOM). `-F`
  also bypasses commit-guard.js `-m` regex; global commit-msg hook still validates the subject.

## 5. Doctrine edits

- **ORCHESTRATION.md** -- new short subsection "Journal / handoff landing (cross-fleet)": journal
  codemasterdd via `scripts/fleet/journal-land.ps1`; branch `claude/journal-<host>-<date>`;
  NEVER `git pull` on a feature branch (`git pull --ff-only` on main only). Governs both PCs.
- **CLAUDE.md** "## Aggiornamento JOURNAL" -- expand from "add an entry" to: add the entry
  (newest-first, after the `---`), then land via `journal-land.ps1 -Subject "docs(journal): <desc>"`.
  Never journal on `chore/`/`docs/`-prefixed branches; never pull on a feature branch.
- **.claude/settings.json** -- no change: `git push origin claude/*` already covers
  `claude/journal-*`.

## 6. Error handling + edge cases

- Branch already exists (same host+date) -> append `-<HHmmss>`.
- `git stash pop` conflict (concurrent JOURNAL.md edit on origin since base) -> abort: keep stash,
  return to original branch, print "resolve manually / re-run after pull --ff-only". Rare.
- Working tree has non-journal dirty files -> only `-Path` files are stashed/committed; others are
  left in place. Recommend (doctrine) running with a tree clean except journal/governance files.
- `gh pr merge --auto` unsupported (repo auto-merge / protection not enabled) -> fall back to
  leaving the PR open with a one-line notice; never hard-fail the landing.

## 7. Testing (Quality Gate Step 1)

Anti-pattern #9: validate the `-Apply` write path, not only `-DryRun`.
1. `-DryRun` preview -> prints planned branch + steps, zero mutation.
2. Live run on Lenovo landing a real entry (this session's fix = legitimate dogfood content):
   verify branch created FROM origin/main, commit subject conventional + trailers present + ASCII
   no-BOM, pushed to origin, PR created + auto-merged (squash, branch deleted), returned to the
   original branch, working tree clean. Document before/after.
3. Negative: run with no JOURNAL.md change -> "nothing to journal", exit 0, no branch.

## 8. Verification gate (ORCHESTRATION sec 4 + Protocol 5)

Different-model judge before merge: adversarial review of the helper (cross-shell / PS5.1
footguns, both-PC correctness, anti-pattern #9/#11/#12/#13 compliance, autonomy-ladder fit) via
parallel subagents (Workflow) and/or `harsh-reviewer`. P0 findings block; P1 fix-or-defer; P2 ack.

## 9. Out of scope (YAGNI)

- **Ryzen gh re-auth** -- documented as an optional manual enhancement (`gh auth login -h github.com`
  on Ryzen) that upgrades Ryzen to full self-service PR+auto-merge. HUMAN-irreducible (credential,
  autonomy ladder sec 5). NOT implemented here; the helper already degrades gracefully without it.
- **Broader Ryzen local-main divergence** (non-journal unpushable commits / bundle sync) -- a
  separate fleet-sync topic; this fix only stops journal stranding + the stray-merge cause.
- No monitor/cron, no GitHub Action, no heavy machinery (ORCHESTRATION sec 8 anti-scope).

## 10. Success criteria

- A journal entry made on EITHER PC reaches origin/main via a `claude/journal-*` PR with no manual
  content recovery and no stray merge commit.
- Helper runs identically on Lenovo + Ryzen (PowerShell + git + SSH push); Ryzen degrades to
  push-only without losing content.
- cross-fleet-reproducibility pillar (Compass) no longer flags journal-branch drift.

## 11. Revision 2026-05-29 -- worktree isolation (supersedes the sec 3/6 mechanics)

The first shipped helper (stash + `git switch -c` in the SHARED working tree) was exercised
live and failed; a bug hunt of the on-main version found three real defects. The originating
incident: a session ran the helper while the shared clone's HEAD was on a CONCURRENT session's
branch -- the helper switched HEAD away from it.

Defects (in the stash+switch design):
- **B (shared-clone HEAD switch, significant):** `git stash push` + `git switch -c <branch>` mutate
  the shared working tree's HEAD. On a clone shared by concurrent Claude Code sessions, this yanks
  HEAD out from under another session. Root cause of the originating incident.
- **#3 (wrong-stash drop, significant):** `git stash drop` / `pop` with no ref operate on
  `stash@{0}` = the NEWEST stash = possibly a concurrent session's stash, not `journal-land-temp`.
- **C (delete-branch false negative, minor):** `gh pr merge --delete-branch` ran while the journal
  branch was still checked out -> local delete fails -> gh returns non-zero -> the script printed
  "auto-merge not enabled" even though the merge succeeded.

Fix (the SDMG fix-the-base, not another amendment): **do all branch/commit/push work in a
THROWAWAY git worktree based on freshly-fetched origin/main; never run `git switch` in the shared
tree.** Revised data flow:
```
session edits JOURNAL.md (newest-first, after the --- divider)
   -> journal-land.ps1 -Subject "docs(journal): <desc>"
      -> git fetch origin main
      -> git stash push -u -m <UNIQUE-TAG> -- <paths>   (carry edit off the SHARED tree)
      -> resolve OUR stash by tag (git stash list) -> $stashRef   (never stash@{0})  [fixes #3]
      -> git worktree add -b claude/journal-<host>-<date> <TEMP> origin/main  [fixes B: no switch]
      -> git -C <TEMP> stash apply $stashRef        (apply edit in the worktree; conflict -> abort+restore)
      -> hash-compare each path vs pre-stash hash   (silent 3-way detect; abort unless -AcceptMerge)
      -> git stash drop $stashRef                   (by ref)  [fixes #3]
      -> git -C <TEMP> add/commit -F <tmp> ; git -C <TEMP> push -u origin <branch>
      -> git worktree remove --force <TEMP>         (free the branch BEFORE gh)  [fixes C]
      -> gh authed? create PR [+ auto-merge --squash --delete-branch] : push-only notice (Ryzen)
      -> git branch -D <branch>                     (shared HEAD was NEVER switched -> no return needed)
```
The safety contract (origin/main base, hash-based silent-merge detection + `-AcceptMerge`,
exit-code-checked recovery, ASCII-no-BOM `-F` commit, gh-graceful Ryzen path, conventional-subject
fail-fast) is preserved unchanged. The helper interface (sec 4) is unchanged. Verified by a live
dogfood land + a different-model `harsh-reviewer` pass (SDMG external falsification, Protocol 7).
