# D2b -- Goal-Drift Monitor -- Design (GATED, design-only)

> **Status (2026-06-23):** design-only -- not approved for build (SDMG-gated); not built as of 2026-06-23

> Status: DESIGN-ONLY HYPOTHESIS. **NOT approved for build.**
> Gate: Protocol 7 (SDMG). Build requires harsh-reviewer falsification + 2-week empirical (SDMG-gate landed 2026-05-20; not before ~2026-06-03) + new evidence. See cross-repo-goals spec section 6.
> Author: Claude Code hub (Ryzen). Refs: ADR-0026 P5/P7, L-066, HSGF rejection 2026-05-20, GOALS.md.

## 1. Purpose

Read-only signal: flag when a repo's recent activity drifts from its declared **Short** goal. NOT auto-coordination, NOT auto-trigger -- a human-facing alert only. This is the safest first increment toward the "agents coordinate work" intent, staying inside the DO-NOT (no auto-trigger predicates, P7 step 6).

## 2. What it is NOT (boundary)

- NOT auto-spawning work (that = HSGF F-FULL, RETHINK-FUNDAMENTAL rejected 2026-05-20).
- NOT writing goals back into repos.
- NOT deciding priorities. Decider stays human.
- Output = a report a human reads. Zero side effects on repos.

## 3. Design

### Input
- `codemasterdd/GOALS.md` Snapshot (declared Short per repo).
- Each repo's `## Goals (S/M/L)` canonical section (now merged in all 5 repos).
- Recent activity per repo: last N merged PRs + open PRs (titles) + recent commit subjects (via `gh pr list` + `git log`).

### Logic (drift heuristic -- read-only)
For each repo:
1. Extract declared Short goal keywords (e.g. Game Short = "M1 Sistema", "hardcore band").
2. Extract recent activity themes (PR/commit titles, last ~10).
3. Alignment check: do recent themes reference the Short-goal keywords?
   - **ALIGNED**: recent work matches declared Short.
   - **DRIFT**: recent work on a different theme than declared Short (neither wrong nor right -- just flagged for human: "is the goal stale, or is the work off-track?").
   - **STALE-GOAL**: Short goal references closed/merged items (e.g. PR already merged) -> goal needs refresh.

### Output (markdown report, read-only)
```
## Goal-drift check YYYY-MM-DD
| Repo | Declared Short | Recent activity | Verdict |
|------|----------------|-----------------|---------|
| Game | M1 Sistema + band | M1 route #2364, band #2365 | ALIGNED |
| Database | schema versioning Phase A | ... | ALIGNED / DRIFT / STALE-GOAL |
```
Plus: "Action: human decides -- refresh goal OR re-focus work. No auto-action taken."

### Mechanism (candidate)
- Extend `repo-health-auditor` agent with a "drift mode" (it already aggregates GOALS.md + PR themes -- read-only, same pattern). Invoked on demand by Eduardo, or scheduled read-only.
- NO new daemon, NO auto-trigger. On-demand or cron-read-only-report.

## 4. Falsification plan (for the gate, when it opens ~06-03)

Hypotheses to falsify via harsh-reviewer:
- H1: the keyword-match heuristic produces useful ALIGNED/DRIFT signal, not noise. (Risk: shallow keyword match = false drift/false-align. Same family as L-069 "shallow signal".)
- H2: the report adds value over just reading GOALS.md + STATUS manually. (Risk: redundant ceremony.)
- H3: read-only stays read-only -- no scope-creep toward auto-trigger. (Risk: incremental drift into HSGF.)
- New-evidence test: did this session's manual multi-session coordination actually suffer from goal-drift that a monitor would have caught? (If no real drift occurred, the monitor solves a non-problem -> DEFER.)

Pre-commit stance (P7): "if harsh-reviewer rejects, adopt non-defend."

## 5. Gate checklist (Protocol 7, ALL required before build)

- [ ] 2-week SDMG empirical elapsed (~2026-06-03+).
- [ ] harsh-reviewer falsification PASS (H1-H3 + new-evidence).
- [ ] Anti-accretion: is this the Nth amendment on a defective base? (HSGF was rejected -- is D2b genuinely narrower, or F-FULL in disguise? Must be demonstrably read-only.)
- [ ] Narrow adoption: read-only report only, action human.
- [ ] NO auto-trigger predicates.

## 6. Decision

DESIGN PARKED. Re-open at ~2026-06-03 (post 2-week + hub-shape re-eval, open-action #4) with harsh-reviewer. Until then: GOALS.md (D1) is the active coordination layer; drift-checking done manually by repo-health-auditor on-demand.
