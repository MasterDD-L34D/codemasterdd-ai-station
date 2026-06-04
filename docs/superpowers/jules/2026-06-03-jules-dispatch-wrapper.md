# GOAL -- Build the `jules-dispatch` fail-closed wrapper (task-authored + dedup-vs-active)

> Self-contained handoff for a fresh `/goal`. Cold-start: read this + the pointers at the
> bottom. Authority: **ADR-0037** (merge-autonomy / the wrapper is named there as the
> path-to-standing for `:create`) + **ADR-0035** (Jules dispatch hard-constraints) +
> ORCHESTRATION.md sec 5/6 + memory `project_jules_collaboration_state`,
> `feedback_jules_autonomous_loop_2026_06_02`.

## Why (state, ground-truthed 2026-06-03)

We want to dispatch Jules with tasks **we author from real repo needs** (not Jules's
auto-suggestions), via the proven REST `:create` path -- and crucially **without
overlapping an already-active Jules session** when we route a task.

This is NOT new scope -- ADR-0037 (Accepted 2026-06-03) already named exactly this as the
"path to standing" for `:create`: *"a fail-closed `jules-dispatch` wrapper (repo-whitelist +
perl ASCII-check + scoped-template lint, abort otherwise) allow-listed in place of raw curl,
AND a decided dispatch-SOURCE model"*. Eduardo's ask (2026-06-03) **decides the
dispatch-source**: human-authored tasks from real needs -- which is the SAFE source (it closes
the harsh-reviewer "attacker-influenced auto-feed" risk that blocked making `:create` standing).

Proven already this session: REST `:create` works (no OAuth, `x-goog-api-key`, Ryzen); the
full dispatch->monitor->S3-extract->ground-truth->PR->merge->archive loop ran 10x
(self-repo #283/#284 merged; Godot GGv2 #398; Game #2590 = 7 tests, CI-green). The wrapper
just CODIFIES + makes that dispatch safe + repeatable.

## The build

A fail-closed wrapper (script `scripts/wrappers/jules-dispatch.ps1` or
`scripts/fleet/jules-dispatch.ps1`) that takes a task WE wrote and dispatches it ONLY if every
gate passes. WE maintain a queue of scoped task-files (from BACKLOG / real needs); the wrapper
enforces safety.

### Input
`jules-dispatch.ps1 -Repo <owner/repo> -TaskFile <scoped-prompt.md> -Target <file-or-function> [-Title <t>] [-Force]`
- `-TaskFile`: a markdown scoped-strict prompt (exact target file(s) + scope bound + "no logic
  change" where applicable + "ASCII only" + verifiable acceptance) -- the ADR-0035 template.
- `-Target`: the identifier the dedup checks (a path and/or function name).

### Gate-stack (fail-closed -- abort on first failure)
1. **Repo whitelist**: `-Repo` in {Game, Game-Godot-v2, codemasterdd-ai-station, Game-Database}.
   Else ABORT (sovereign-only / non-whitelisted never dispatched to cloud).
2. **ASCII-lint** the task-file (`perl -ne 'exit 1 if /[^\x00-\x7F]/'`, NOT grep -P). Anti-#12.
3. **Scoped-template lint**: the task-file MUST contain the load-bearing markers -- a named
   target file, a scope bound (single-file / named-functions), an "ASCII only" clause, and a
   verifiable acceptance line. Vague code-health/perf/"improve" prompts = REJECT (ADR-0035
   hard-constraint #1: proven defect generators).
4. **Dedup vs ACTIVE sessions (the load-bearing new safety)** -- see spec below.
5. **Dispatch** REST `POST /v1alpha/sessions` (scoped prompt + `sourceContext` +
   `startingBranch: main`) + **audit-log** append to `logs/jules-dispatch-YYYY-MM.md`
   (gitignored): timestamp, repo, target, session-id, title.

### Dedup spec (gate 4 -- option A, the recommended design)
- "ACTIVE" = sessions whose state is `IN_PROGRESS` OR `AWAITING_USER_FEEDBACK` (NOT
  COMPLETED/archived). These are the in-flight ones a new task must not duplicate.
- For the target repo: `GET /v1alpha/sessions?pageSize=100` -> filter active + same
  `sourceContext.source`.
- **Overlap test**: compare the new `-Target` (file path + function token) against each active
  session's title + prompt (they name their target). A token/substring match on the target
  identifier => OVERLAP => **ABORT** with `"overlaps active session <id> (<title>)"`.
- **Conservative**: uncertain/partial match => treat as overlap => abort (a false-abort costs
  one skipped dispatch; a false-allow costs duplicate/conflicting Jules work -- the worse error).
- `-Force`: explicit human override when we KNOW it is not a real overlap (logged as forced).
- Why option A (not "touched-files" match): in-progress sessions have NO gitPatch yet -> the
  only readable overlap signal is the target named in the title/prompt. (Touched-files match
  only works post-completion, which is too late for anti-overlap.)
- **Race caveat (QG edge)**: a session can change state between the dedup GET and the dispatch.
  Acceptable (the window is seconds; worst case a near-simultaneous duplicate, rare for
  human-paced authoring). Document it; do NOT over-engineer a lock.

## Quality Gate (mandatory before "production")
- **Smoke (Step 1)**: dispatch ONE real scoped task end-to-end through the wrapper (whitelisted
  repo) -> session created -> recover -> PR. Verify the audit-log entry written.
- **Research (Step 2, >=3 edge cases)**: (a) non-whitelisted repo -> ABORT; (b) non-ASCII
  task-file -> ABORT; (c) vague/no-target prompt -> ABORT (scoped-lint); (d) **dedup
  false-negative** -- dispatch a target that matches an active session -> MUST abort; (e) dedup
  false-positive -- a distinct target that token-collides (e.g. `fetch` substring) -> verify the
  match is tight enough to not over-block (tune the token boundary); (f) the GET-then-dispatch
  race.
- **Tuning (Step 3)**: tune the overlap-matcher precision (target-token boundary) using the edge
  results; document before/after (e.g. false-positive rate on a sample of active-session titles).
- `QUALITY.md` / section with the 3 steps + evidence.

## Disciplined path (this is autonomy-adjacent + ADR-0037-scoped)
1. **brainstorming/spec** -> `docs/superpowers/specs/<date>-jules-dispatch-wrapper-design.md`
   (gate-stack + dedup option A + the 3 alt-options + edge-cases).
2. **harsh-reviewer FALSIFICATION** (pre-build, adopt-not-defend): falsify the dedup logic (can
   it false-allow a duplicate? is the active-state set complete? race?) + the fail-closed gates
   (can any be bypassed?). SDMG Protocol 7 -- this is a self-designed dispatch-safety method.
3. **TDD build** (tdd-guard active; the matcher logic is pure + unit-testable -- test the
   overlap-detector against fixture session-lists; test each gate's abort).
4. **QG** (above).
5. **ADR-0037 addendum**: the wrapper now EXISTS. **Important SDMG boundary**: building the
   wrapper does NOT by itself make `:create` standing. "Standing" = removing the human per-action
   prompt (allow-listing the wrapper in `.claude/settings.json`), which is a SEPARATE
   autonomization that still needs its own decision + harsh-reviewer (the wrapper is the
   *prerequisite* + the *enforcement mechanism*, not the grant). Until then `:create` stays
   per-instance (run the wrapper manually); the wrapper just makes each manual dispatch SAFE.

## Accept
- `jules-dispatch.ps1` exists, fail-closed, all 5 gates + dedup option A, audit-log.
- Survived harsh-reviewer falsification (findings adopted).
- QG 3 steps documented with evidence (incl. the dedup false-pos/neg edge cases).
- ADR-0037 addendum: wrapper built; standing-grant explicitly still-deferred (separate gate).

## Pointers
- `docs/adr/0037-merge-autonomy-model.md` (the path-to-standing clause + decision 2 doctrine carve-out)
- `docs/adr/0035-jules-cli-proactive-dispatch-routine.md` (hard-constraints + REST addendum: the
  exact `:create` body schema + `curl --data @-` / Invoke-RestMethod dispatch)
- `ORCHESTRATION.md` sec 5 (ladder) + sec 6 (`:create` = NOT-standing/per-instance, the rationale)
- `scripts/jules-daily-digest.ps1` + `scripts/fleet/register-jules-digest-task.ps1` (REST GET
  + keys.env pattern to copy) ; `scripts/setup/install-privacy-guard.ps1` (fail-closed wrapper pattern)
- memory `project_jules_collaboration_state` (autonomy map), `feedback_jules_autonomous_loop_2026_06_02`
- Capability recap: `JULES_API_KEY` in `~/.config/api-keys/keys.env`; dispatch JSON via
  PowerShell `Invoke-RestMethod` (clean) OR `curl --data @-` (Windows curl can't read MSYS /tmp).
  Active-state filter values seen live: `IN_PROGRESS`, `AWAITING_USER_FEEDBACK`, `COMPLETED`.
