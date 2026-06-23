# SPEC -- `jules-dispatch.ps1` fail-closed wrapper (design, pre-build)

> **Status (2026-06-23):** shipped -- jules-dispatch.ps1 fail-closed live (ADR-0035)

> Status: DRAFT for harsh-reviewer FALSIFICATION (SDMG Protocol 7, adopt-not-defend).
> Authority: ADR-0037 (path-to-standing clause) + ADR-0035 (Jules dispatch hard-constraints
> + REST `:create` schema) + goal `docs/superpowers/jules/2026-06-03-jules-dispatch-wrapper.md`.
> ASCII-first body (ADR-0021). This is the artifact the harsh-reviewer attacks BEFORE any code.

## 1. Purpose + boundary

Build `scripts/fleet/jules-dispatch.ps1`: a fail-closed wrapper that takes a Jules task WE
authored (human-authored scoped task -- the safe dispatch source decided by Eduardo 2026-06-03)
and dispatches it via REST `POST /v1alpha/sessions` ONLY if every safety gate passes.

SDMG boundary (load-bearing): building this wrapper does NOT make `:create` standing.
"Standing" = allow-listing the wrapper in `.claude/settings.json` (removes the per-action human
prompt) -- a SEPARATE autonomization needing its own harsh-reviewer gate. Until then `:create`
stays per-instance: a human runs this wrapper manually each time. The wrapper is the
*prerequisite + enforcement mechanism*, not the grant. External-repo MERGE stays
Eduardo-explicit (ADR-0037 decision 3), unchanged.

## 2. Input contract

```
jules-dispatch.ps1 -Repo <owner/repo> -TaskFile <scoped-prompt.md> -Target <id> [-Title <t>] [-Force] [-DryRun]
```

- `-Repo` (required): `owner/repo`. Checked against the whitelist (gate 1).
- `-TaskFile` (required): path to a markdown scoped-strict prompt (ADR-0035 template). Its
  CONTENT becomes the dispatch `prompt`.
- `-Target` (required): the identifier(s) dedup checks -- a path and/or function name
  (e.g. `scripts/fleet/foo.ps1` or `Get-Bar` or `scripts/fleet/foo.ps1::Get-Bar`).
- `-Title` (optional): session title; default derived from `-Target` + date.
- `-Force` (optional): human override of the DEDUP gate ONLY (gate 4). Does NOT bypass
  gates 1-3 (whitelist / ASCII / template) -- those are hard safety, never force-overridable.
- `-DryRun` (optional): run all gates + build the exact REST body + show it + write a
  DRYRUN audit-log line, but do NOT POST. The verifiable happy-path for QG Step-1 without
  creating a real cloud session.

## 3. Gate-stack (fail-closed -- abort on FIRST failure, non-zero exit)

| # | Gate | Pass condition | On fail | Force-overridable? |
|---|------|----------------|---------|--------------------|
| 1 | Repo whitelist | `-Repo` in {Game, Game-Godot-v2, codemasterdd-ai-station, Game-Database} | ABORT | NO |
| 2 | ASCII-lint task-file | task-file has zero bytes > 0x7F | ABORT | NO |
| 3 | Scoped-template lint | task-file contains the 4 load-bearing markers (below) | ABORT | NO |
| 4 | Dedup vs ACTIVE | `-Target` does not overlap any active session on `-Repo` | ABORT | YES (-Force) |
| 5 | Dispatch + audit | POST succeeds -> append audit-log line | propagate error | n/a |

Gate 1 is FIRST (cheapest + the sovereign-leak guard: a non-whitelisted repo must never reach
the network). Gate 2/3 are local file checks. Gate 4 is the only one that touches the network
before dispatch (the GET enumerate).

### Gate 2 -- ASCII-lint (native byte-check, not perl)

The goal doc named `perl -ne 'exit 1 if /[^\x00-\x7F]/'`. We implement the SAME intent
(anti-#12 byte-accurate ASCII, not GNU-only `grep -P`) as a NATIVE PowerShell byte-check:
`[IO.File]::ReadAllBytes($TaskFile)` then fail if any byte `-gt 127`. Rationale: (a) the repo's
own test runner explicitly avoids external deps ("avoid Pester install requirement on fleet");
native removes the perl dependency; (b) byte-level is strictly more accurate than a decoded-char
regex (no encoding-decode ambiguity); (c) it is a PURE function -> unit-testable (gate 2 is the
overlap-matcher's sibling in the test plan). This is a deliberate, surfaced choice, not a silent
deviation.

### Gate 3 -- Scoped-template lint (the 4 markers)

ADR-0035 hard-constraint #1: vague code-health/perf/"improve" prompts are proven defect
generators. The task-file MUST contain ALL of:
1. a named **target file** (a path token: contains `/` and a file extension), AND
2. a **scope bound** clause (one of: `single-file`, `single file`, `named function`,
   `no logic change`, `no behavior change`, `docstring`-only, ...), AND
3. an **ASCII-only clause** (literal `ASCII only` / `ASCII-only`, case-insensitive), AND
4. a **verifiable acceptance** line (a marker like `accept`, `acceptance`, `verify`, `tests pass`).

Missing any -> REJECT with which marker is missing. (This lints OUR authored task-file; it is a
discipline check on the author, not on Jules.)

## 4. Dedup gate (gate 4) -- option A, the load-bearing new safety

### 4.1 Active set  [CORRECTED -- see sec 11 P0.2/P0.3; this is the binding version]

- "ACTIVE" = sessions whose `state` is NOT in the TERMINAL denylist
  {`COMPLETED`, `FAILED`, `CANCELLED`, `ARCHIVED`}. Allowlisting {IN_PROGRESS,
  AWAITING_USER_FEEDBACK} was REJECTED (harsh-reviewer P0.2): the Jules state enum is not
  exhaustively known, so an unobserved in-flight state (PLANNING / QUEUED / PAUSED /
  AWAITING_PLAN_APPROVAL / null / empty) would silently fall out of an allowlist -> false-ALLOW
  (the dangerous direction). The denylist makes any non-terminal-or-unknown state fail-closed to
  ACTIVE = blocked. (Live probe 2026-06-03: 68 sessions, states observed = COMPLETED(67) +
  FAILED(1); both terminal.)
- `GET /v1alpha/sessions?pageSize=100` -> filter ACTIVE AND
  `sourceContext.source -eq "sources/github/MasterDD-L34D/<Repo>"` (owner constant + exact format
  confirmed live; `-Repo` is the BARE repo name -- see sec 11 P0.1).
- **list-GET failure = fail-closed ABORT** ("cannot enumerate active sessions"). We cannot prove
  no-overlap, so we do not dispatch. (`-ForceBlind` -- a SEPARATE flag from `-Force`, sec 11 P1.2
  -- can override as a logged BLIND dispatch; human takes responsibility.)
- **nextPageToken present -> fail-closed ABORT** ("session list paginated, dedup may be
  incomplete"). One-line guard; we do NOT build pagination (P2.2).

### 4.2 Per-session text  [CORRECTED -- the list ALREADY carries prompt; no extra GET]

Live probe 2026-06-03 (harsh-reviewer P0.3b): the list payload carries `.prompt` populated on
EVERY session (promptLen 1767-2661 chars) alongside `.title` / `.state` / `.sourceContext` /
`.name`. The earlier "list may omit prompt" premise was FALSE. So: match the new `-Target`
against `(.title + " " + .prompt)` STRAIGHT FROM the list payload -- no per-session GET, no
title-only-degrade path (both DELETED). This removes N round-trips and the entire sec 7 #3
concern.

### 4.3 The overlap matcher (pure, unit-testable) -- `Test-TargetOverlap`

`Test-TargetOverlap(NewTarget, SessionText) -> bool`

1. **Derive target identifiers** from `NewTarget`:
   - Split on whitespace / `,` / `::` into raw parts.
   - Path-like part (contains `/` `\` or a `*.ext`): add the normalized **full path** (sep->`/`,
     lowercased) as a STRONG identifier; add the **basename stem** (last segment minus one
     trailing extension) if its length >= 3.
   - Symbol-like part (`^[A-Za-z_][A-Za-z0-9_.-]*$`): add it if length >= 3.
   - Drop generic stop-tokens that over-match: {src, lib, app, apps, test, tests, scripts,
     services, main, index, util, utils, core, api, docs, data, get, set, new, run, build}.
     (Tunable stoplist -- QG Step-3 knob.)
   - **If NO identifier survives -> return $true (conservative): a target too generic to
     characterize is treated as an overlap so the run ABORTS** -- forcing the author to pass a
     specific `-Target`. (Over-block, never a false-allow.)
2. **Boundary match** (the precision knob): for each identifier, test
   `(?<![A-Za-z0-9_]) + [regex]::Escape(id) + (?![A-Za-z0-9_])` against the lowercased
   SessionText, case-insensitive. ANY identifier matches -> return $true (OVERLAP).
   - The lookaround `[^A-Za-z0-9_]` boundary is what kills the `fetch`-in-`prefetch`
     false-positive (naive `.Contains` matches it; the boundary does not).
3. No identifier matched -> return $false (no overlap).

### 4.4 Conservative posture + -Force

- A real overlap -> ABORT `"overlaps active session <id> (<title>)"`. `-Force` -> proceed,
  audit-logged as `FORCED-OVERRIDE-OVERLAP <id>`.
- Cannot verify (list-GET failed) -> ABORT `"cannot verify dedup (API error)"`. `-Force` ->
  proceed, audit-logged as `FORCED-BLIND`.
- Rationale: a false-abort costs one skipped dispatch; a false-allow costs duplicate/conflicting
  Jules work (the worse error). Conservative = on uncertainty, abort.

### 4.5 Race caveat (documented, not locked)

A session can change state between the dedup GET and the dispatch POST (window = seconds). We do
NOT build a lock (over-engineering for human-paced manual dispatch). Worst case: a
near-simultaneous duplicate, rare. Documented as a known QG edge.

## 5. Dedup design alternatives considered

- **A (CHOSEN) -- title+prompt target-token match on ACTIVE sessions, boundary-precise,
  conservative-abort.** The only readable overlap signal for IN_PROGRESS sessions (they have no
  gitPatch yet). Precision via boundary lookaround; safety via conservative-abort + stoplist
  over-block. Residual false-negative risk DISCLOSED (sec 7).
- **B -- touched-files (gitPatch) match.** Rejected: IN_PROGRESS sessions expose no gitPatch
  until COMPLETED -- too late for anti-overlap (the whole point is to catch in-flight work).
- **C -- no dedup, rely on human memory.** Rejected: the goal's load-bearing new safety IS the
  anti-overlap; human memory across a 3-5 active-session cap + two machines is exactly what
  fails.

## 6. Dispatch + audit (gate 5)

- Body (ADR-0035 verified schema): `{"prompt": <task-file content>, "title": <title>,
  "sourceContext": {"source": "sources/github/<Repo>", "githubRepoContext": {"startingBranch":
  "main"}}}`. POST via `Invoke-RestMethod` (clean on Windows; the curl `--data @-` note is a
  Lenovo-MSYS workaround, not needed here).
- On success: parse `name: sessions/<id>` + `state`. Append to `logs/jules-dispatch-YYYY-MM.md`
  (gitignored): `<iso-timestamp> | <Repo> | <Target> | <session-id> | <state> | <title> [| FORCED-*]`.
- Audit-log write uses UTF8-no-BOM append.

## 7. Failure modes I am SURFACING (adopt-not-defend -- attack these)

1. **Residual false-negative (the dangerous direction).** If an active session names its target
   differently than `-Target` (e.g. session prompt says "the status helper", `-Target` is
   `flint_status`), no token matches -> the matcher MISSES the overlap -> duplicate dispatch.
   Mitigation is partial: scoped-dispatched sessions (gate 3) DO contain the literal path; but
   sessions started outside this wrapper (Eduardo browser, pre-wrapper) may not. This risk is
   REAL and cannot be eliminated by token-matching alone. Is conservative-abort enough? Is the
   mitigation honest?
2. **Stoplist false-negative.** With two identifiers where the stoplist drops the one that would
   have matched (`-Target "api Get-Foo"`, session is all about `api`, never `Get-Foo`): no match
   -> false-allow. Stoplist trades this for false-positive reduction. Acceptable? Should the
   stoplist only apply when it is NOT the sole identifier (already the case) -- but the two-token
   leak remains.
3. **Title-only degrade.** If every per-session prompt-GET fails, we match titles only. Are
   scoped titles reliable enough, or is this a silent precision drop that should warn?
4. **-Force blast radius.** -Force overrides BOTH "real overlap" and "cannot verify". Is letting
   -Force override the API-failure-abort (blind dispatch) too permissive? Should blind dispatch
   require a separate, louder flag?
5. **Gate-3 lint is keyword-based.** A task-file could contain "ASCII only" in prose without
   actually being scoped (gaming the lint). The lint checks PRESENCE of markers, not semantic
   scope. Author-discipline check, not a hard guarantee. Bypassable by a careless author?
6. **The race (sec 4.5).** Accepted as documented. Is "document, do not lock" the right call for
   a manual human-paced dispatch, or is even a seconds-window duplicate unacceptable?
7. **pageSize=100 ceiling.** If >100 sessions exist, active ones could be on page 2 and missed ->
   false-negative. Do we need pagination, or is the active-set always small enough?

## 8. Test plan (TDD -- lightweight runner, copy deploy-global-skills.Tests.ps1 pattern)

Pure units dot-sourced from the script (cut before the dispatch `param`/main):
- `Test-AsciiClean` (gate 2): ASCII file -> true; file with a 0x80+ byte -> false.
- `Test-ScopedTemplate` (gate 3): full-marker file -> ok; each missing-marker variant -> reject.
- `Test-RepoWhitelisted` (gate 1): each whitelisted -> true; a non-whitelisted -> false.
- `Test-TargetOverlap` (gate 4 core):
  - exact path in session text -> true (overlap).
  - basename stem in session text -> true.
  - function token whole-word -> true.
  - `fetch` vs `prefetch`/`fetchData` -> FALSE (boundary precision -- the tuning case).
  - distinct target, no token in text -> false.
  - generic-only target (all stoplisted) -> true (conservative abort).
  - false-negative fixture (session names target by synonym) -> documents the miss (asserts the
    KNOWN limitation, not a pass we pretend).
- Gate ordering / fail-closed: a harness test that gate 1 fails before gate 2 touches the file,
  etc. (best-effort; the gates are sequential by construction).

## 9. QG (mandatory before "production")

- **Smoke (Step 1)**: `-DryRun` happy-path on a whitelisted repo -> all gates pass -> exact REST
  body shown -> DRYRUN audit-line written. (The TRUE live dispatch is an explicit Eduardo-gated
  action -- outward-facing -- offered separately, not auto-fired.)
- **Research (Step 2, >=3 edges)**: (a) non-whitelisted -> abort; (b) non-ASCII task-file ->
  abort; (c) vague/no-target prompt -> abort (gate 3); (d) dedup TRUE-overlap -> abort;
  (e) dedup false-positive token-collision -> verify NOT over-blocked (boundary); (f) the race
  (documented).
- **Tuning (Step 3)**: tune the overlap-matcher boundary + stoplist using the edge results;
  document before/after (naive-substring false-pos rate vs boundary false-pos rate on a sample
  of active-session titles).
- Evidence -> a `QUALITY.md`-style section (in the QG doc or appended here) with the 3 steps.

## 10. ADR linkage

ADR-0037 addendum (post-build): the wrapper EXISTS; standing-grant explicitly STILL-DEFERRED
(separate gate). The addendum is a `docs/adr/**` doctrine file -> branch + PR, **Eduardo-only
merge** (ADR-0037 decision 2). The hub does NOT self-merge it.

Two-PR split (harsh-reviewer scope residual): the wrapper + this spec + tests + QG go in ONE
branch/PR (non-doctrine, hub-mergeable per ADR-0037 decision 1, classifier-judged). The
ADR-0037 addendum goes in a SEPARATE branch/PR (doctrine, Eduardo-only-merge). The addendum must
NOT ride in on the hub-merged wrapper commit.

## 11. Falsification adopted (harsh-reviewer, 2026-06-03, SDMG Protocol 7) -- BINDING corrections

Verdict: SURVIVE-WITH-CHANGES. All P0 + P1 adopted (verified against LIVE API, not just the
reviewer's doc citations). This section is authoritative where it conflicts with text above.

**P0.1 (adopted)** -- `-Repo` is the BARE repo name {Game | Game-Godot-v2 |
codemasterdd-ai-station | Game-Database}. Owner is the constant `$OWNER = 'MasterDD-L34D'`
(invariant across all 4 -- confirmed live + git remotes). Gate 1 checks the bare name; gate 4
filter + gate 5 body both construct `sources/github/$OWNER/$Repo` from the SAME helper. Unit
test: `-Repo Game` -> `sources/github/MasterDD-L34D/Game`.

**P0.2 (adopted)** -- ACTIVE = complement of TERMINAL denylist {COMPLETED, FAILED, CANCELLED,
ARCHIVED}; unknown/null/empty state -> ACTIVE (fail-closed). See sec 4.1.

**P0.3 (adopted)** -- (a) source filter uses the constructed constant string with `-eq` (exact
format confirmed live). (b) The list carries `.prompt`; per-session GET + degrade path DELETED.
See sec 4.2.

**P1.1 (adopted, no code change)** -- native byte-check ~ perl for our cases (BOM both-reject =
intended; CRLF/NUL/empty equivalent). Native KEPT (no perl dep). Add an explicit non-empty
task-file precondition (gate 3 already rejects empty via missing markers; the explicit length>0
check is clearer + tested).

**P1.2 (adopted)** -- SPLIT the override flags: `-Force` overrides a KNOWN overlap ONLY (gate 4
"real overlap"); `-ForceBlind` is a SEPARATE flag for the cannot-verify case (list-GET fail /
pagination), with a louder audit tag (`FORCED-BLIND`) + a stderr warning
"DISPATCHING WITH NO DEDUP VERIFICATION". Neither overrides gates 1-3.

**P1.3 (adopted)** -- gate-3 <-> `-Target` consistency: at least one `-Target` identifier MUST
appear in the task-file body, else ABORT ("Target <X> not named in task-file -- dedup would check
the wrong file"). Prevents a scoped-on-foo task dispatched with `-Target bar` from dedup-checking
bar. Pure + testable.

**P1.4 (adopted, already designed)** -- a `-Target` that collapses to all-stop-tokens / no
surviving identifier -> `Test-TargetOverlap` returns $true -> conservative ABORT (over-block,
never false-allow). Kept as a fixture.

**P2.1 (NOT changed, per reviewer)** -- the two-token stoplist "leak" (sec 7 #2) is correct
behavior; do not special-case.

**P2.2 (adopted)** -- nextPageToken present -> fail-closed abort (sec 4.1). Not pagination.

**P2.3 (satisfied by structure)** -- the gate-4 GET is the LAST network op before the gate-5
POST; nothing slow sits between them, so the race window is already milliseconds. No separate
re-GET / lock needed.

**Scope/SDMG boundary -- CLEAN** (reviewer found no erosion). Two-PR split adopted (sec 10).

Corrected input contract (supersedes sec 2):
```
jules-dispatch.ps1 -Repo <bare-name> -TaskFile <scoped.md> -Target <id> [-Title <t>] [-Force] [-ForceBlind] [-DryRun]
```
