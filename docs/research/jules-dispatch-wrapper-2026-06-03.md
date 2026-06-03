# QG -- jules-dispatch.ps1 fail-closed wrapper (2026-06-03)

> Quality Gate evidence (global CLAUDE.md: Smoke -> Research -> Tuning, "Production = QUALITY.md
> con 3 step + evidenze"). Component: `scripts/fleet/jules-dispatch.ps1` + `.Tests.ps1`.
> Spec: `docs/superpowers/specs/2026-06-03-jules-dispatch-wrapper-design.md`. ASCII-first body.

## Build summary

Disciplined path executed: spec -> harsh-reviewer FALSIFICATION (SURVIVE-WITH-CHANGES, 3 P0 + 4
P1 adopted, verified against the LIVE Jules API not just docs) -> TDD (RED/GREEN, tdd-guard
scoped-off with explicit Eduardo authorization, re-enabled at close) -> this QG -> ADR-0037
addendum.

5-gate fail-closed stack: repo-whitelist -> ASCII-lint -> scoped-template-lint (+Target
consistency) -> dedup-vs-active -> dispatch+audit. Dedup = option A (title+prompt target-token
match over ACTIVE sessions, terminal-denylist state model, boundary-precise matcher,
conservative-abort, `-Force`/`-ForceBlind` split).

## Step 1 -- Smoke (happy-path verde + output verificabile)

`-DryRun` happy-path on a whitelisted self-repo. Runs gates 1-4 for real (incl. the LIVE
`GET /sessions` dedup enumerate; 0 active sessions on `codemasterdd-ai-station` at run time ->
gate 4 passes), builds the exact REST body, writes the audit-line. No POST.

```
[PASS] S1 smoke DryRun (gates1-4 pass + body + audit) (exit=0 expect=0; match 'DRYRUN complete'=True)
--- DryRun audit-log tail ---
  2026-06-03T16:24:08.88+02:00 | DRYRUN | codemasterdd-ai-station | scripts/fleet/jules-dispatch.ps1 | (no-session) | (dryrun) | [codemasterdd-ai-station] scripts/fleet/jules-dispatch.ps1 (2026-06-03)
```

Verifiable output: exit 0, `DRYRUN complete`, audit-line appended to the gitignored
`logs/jules-dispatch-2026-06.md`. The dispatch body is printed (ADR-0035 schema: `prompt` +
`title` + `sourceContext.source = sources/github/MasterDD-L34D/codemasterdd-ai-station` +
`githubRepoContext.startingBranch = main`).

## Step 2 -- Research (>=3 edge cases; here 7 covered)

Integration aborts (full-script, real exit codes):

```
[PASS] S2a non-whitelisted repo -> gate1 abort   (exit=1; 'gate1')          # synesthesia (sovereign) refused, BEFORE any file/network
[PASS] S2b non-ASCII task-file -> gate2 abort     (exit=1; 'gate2')          # UTF-8 e-grave byte -> abort (anti-#12)
[PASS] S2c vague prompt -> gate3 abort            (exit=1; 'gate3')          # "improve code health/perf" -> rejected (ADR-0035 #1)
[PASS] S2d Target<->taskfile mismatch -> gate3    (exit=1; 'not named...')   # -Target a file the task does not touch -> abort (P1.3)
```

Unit-proven matcher edges (deterministic, no network -- `jules-dispatch.Tests.ps1`, 52 asserts):

- **(e) dedup false-positive** -- `fetch.js` target vs session text `prefetchData ... fetchAll`
  -> NO overlap (Test 7 + Test 9 boundary lookaround; naive `.Contains` would false-positive).
- **(d) dedup true-overlap MUST abort** -- `Find-ActiveOverlap` over a session fixture: an
  IN_PROGRESS same-source session whose prompt names the target -> overlap returned (Test 10),
  while COMPLETED-only / different-source / distinct-target fixtures return null.
- **state model** -- COMPLETED/FAILED/CANCELLED/ARCHIVED terminal; IN_PROGRESS /
  AWAITING_USER_FEEDBACK / unobserved-PLANNING / null / empty -> ACTIVE (fail-closed) (Test 3).
- **KNOWN residual false-negative (disclosed, NOT pretended-closed)** -- a session that names the
  same target by a SYNONYM (prompt says "the status helper", `-Target` is `flint_status.py`) is
  MISSED (Test 7). Conservative-abort does NOT close this class; it is the honest limit of
  title+prompt token-matching (spec sec 7 #1). Mitigation is partial (scoped-dispatched sessions
  carry the literal path; browser/pre-wrapper sessions may not).
- **(f) the race** -- documented (spec sec 4.5): the gate-4 GET is the last network op before the
  gate-5 POST, so the window is milliseconds; no lock built (over-engineering for manual dispatch).

Full unit run: `52 passed, 0 failed`.

## Step 3 -- Tuning (>=1 iteration + before/after metric)

Overlap-matcher precision knob = the token boundary. Iteration: naive substring -> boundary
lookaround `(?<![A-Za-z0-9_])TOKEN(?![A-Za-z0-9_])` + a generic-token stoplist.

| Case (target `fetch.js`, session text `prefetchData ... fetchAll`) | Naive `.Contains('fetch')` | Boundary matcher |
|--------------------------------------------------------------------|----------------------------|------------------|
| Match? | TRUE (false-positive -- over-blocks) | FALSE (correct -- no over-block) |

Test 9 asserts both ends of this delta. The stoplist (`scripts`, `services`, `api`, `utils`,
...) is the second knob: it drops generic path components so e.g. `scripts/api/utils.ps1` dedups
on the full path, not on the over-matching token `utils` (Test 6). A target that collapses to
all-stop-tokens returns conservative-overlap -> abort (Test 7 "generic-collapse"), forcing a
specific `-Target` -- over-block, never false-allow.

## Not covered here (correctly deferred)

- **Real live POST (gate 5)** -- the actual outward dispatch creating a Jules cloud session.
  Outward-facing + per-instance (NOT standing); offered as an explicit Eduardo-gated action, not
  auto-fired. The DryRun proves everything up to the POST.
- **Live true-overlap end-to-end** -- needs a real active session; deterministically covered by
  Test 10 instead. Can be re-confirmed live after a real dispatch (dispatch X, re-run with an
  X-overlapping target -> expect gate-4 abort).

## Verdict

QG PASS (Smoke + 7 research edges + 1 tuning iteration with before/after). Production-ready as a
PER-INSTANCE manual wrapper. SDMG boundary intact: building/running it does NOT make `:create`
standing (that is a separate settings.json allow-list + its own harsh-reviewer gate).
