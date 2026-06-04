---
name: PR #2144 sistema_decision JSONL telemetry
description: PR #2144 merged 2026-05-09 12:15 UTC squash 28e3ebc6. Plumbs Sistema AI decisions per-round per-unit into JSONL via new kind sistema_decision in tests/smoke/ai-driven-sim.js. RCA validation pending tunnel.
type: project
originSessionId: 1269e0a9-b712-4d99-9523-d88159719a21
---
# PR #2144 — sistema_decision JSONL telemetry for RCA aggressive timeout

**Squash**: `28e3ebc6` merged main 2026-05-09 12:15 UTC via auto-merge L3 (7 safety gate verdi).

## Diff scope

- `apps/backend/services/ai/declareSistemaIntents.js`: plumb `policy.score` + `policy.breakdown` (utility brain) into `decisions[]` for attack + move push.
- `tests/smoke/ai-driven-sim.js`: new `logSistemaDecisions(round, body)` extracts `round_decisions` (already returned by `handleTurnEndViaRound` line 1630 sessionRoundBridge.js — no new endpoint) at all 3 `/turn/end` call sites. Aggregate report adds intent + rule distribution.

54 insertions / 3 deletions. Zero forbidden paths. AI suite 383/383 verde.

## RCA hypothesis distinguishability

- **H1** utility picks retreat instead attack (scoring) → `intent="retreat"` + `breakdown[]` per-consideration
- **H2** stepTowards null / cornered (pathfinding) → `intent="skip"` + `reason="cannot approach"` / `"cannot retreat — cornered"`
- **H3** threat ctx null in harness (injection) → `rule` field shows `UTILITY_AI` vs `REGOLA_001`

## Pending live validation

N=99 RCA run blocked this session: no tunnel alive + main repo had uncommitted `apps/backend/services/network/wsSession.js` change (don't disturb in-progress work) + worktree lacks `node_modules`.

## Next session resume trigger

> _"resume RCA aggressive timeout PR #2144 validation: TUNNEL=https://<host>.trycloudflare.com AI_SIM_PROFILE=aggressive AI_SIM_RUNS=99 node tests/smoke/ai-driven-sim.js → jq 'select(.kind==\"sistema_decision\" and .intent==\"retreat\")' run-*.jsonl → confirm H1 vs H2 vs H3"_

## Cross-ref

- RCA doc: `docs/research/2026-05-09-aggressive-profile-calibration.md`
- N=162 baseline: aggressive 53.5% WR vs balanced 100% (Fisher p<0.0001)
- Last-enemy kiting stalemate: 4/4 timeouts at round 40 with `enemies=1`, `kite_buffer=0` + `retreat_hp_pct=0.15` → Sistema kites at range=2 indefinitely
