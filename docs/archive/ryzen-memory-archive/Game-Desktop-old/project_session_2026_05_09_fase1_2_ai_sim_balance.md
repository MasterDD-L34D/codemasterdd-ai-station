---
name: Session 2026-05-09 FASE 1+2 AI sim + balance signal end-to-end
description: 9 PR shipped Day 4-5 — B-NEW-14 unblock combat phone, FASE 1 AI harness, FASE 2 batch runner + N=162 balance signal, K3 prod fix +36.5pp WR, K4 sticky negative result
type: project
originSessionId: c1bf26d8-f7b0-422c-8073-fa8e4ea45db8
---

# Session 2026-05-09 — FASE 1+2 AI sim + balance signal

9 PR cumulative shipped Game/ + 1 Godot v2 main. Backend AI infra + sim harness + balance discovery + K3 production fix + K4 negative result. End-to-end balance signal arc: 53.5% → 95% → 90% production state.

## PR shipped (9 Game/ + 1 Godot v2)

| PR | Squash | Coverage |
|---|---|---|
| #2140 | merged | B-NEW-14 backend WS world_confirm action handler |
| Godot v2 7b92724 | direct main | B-NEW-14 phone Conferma mondo CTA + B-NEW-7 v2 timeout 60s+retry + WS register |
| #2141 | `480d1b53` | FASE 1 AI-driven sim harness T1.1 (player AI) + T1.2 (telemetry JSONL) |
| #2142 | `ee1304e3` | FASE 2 batch runner T2.1 + N=30 baseline (3-profile aggregate) |
| #2143 | `9b8d02fe` | balance-illuminator agent RCA + N=162 confirm |
| #2144 | `28e3ebc6` | sistema_decision JSONL telemetry per RCA aggressive timeout |
| #2145 | `488f9c46` | H1 validation oscillation root cause confirmed |
| #2146 | `623136f9` | **K3 production fix** aggressive use_utility_brain false (+36.5pp WR) |
| #2147 | `736b5782` | K4 Approach A stickiness term implementation + sweep N=40 negative result |

## Balance signal arc

| Stage | aggressive WR | Notes |
|---|---:|---|
| Pre-fix N=43 baseline | 53.5% | utility ON, oscillation timeout 47% |
| K3 ablation utility OFF | 95% | +41.5pp |
| K3 prod validation N=20 | **90%** (production state) | timeout 0%, defeat 2 |
| K4 sticky 0.15 | 55% | -30pp insufficient |
| K4 sticky 0.30 | 60% | -25pp insufficient |

**Counterintuitive RCA**: aggressive profile (utility ON + retreat 0.15 + kite 0 + utility brain) UNDERPERFORMS vs balanced/cautious. Cause: bidirectional kite oscillation between 2 Sistema units alternating UTILITY_AI ↔ REGOLA_001 rule paths producing 1-tile up/down loops with net zero displacement.

## Discoveries

1. **B-NEW-14 unblocks combat phone-only**: backend WS `world_confirm` handler + Godot phone CTA "Conferma mondo (host)" let single-player smoke reach combat phase end-to-end. Previously stuck MODE_WORLD_VOTE post-vote.

2. **B-NEW-7 v2 (60s + retry-on-timeout)**: friend cold-start tunnel ~16s observed. 30s insufficient; 60s + 1 silent retry covers cold-start jitter.

3. **AI sim infra scalable**: `tests/smoke/ai-driven-sim.js` + `tools/sim/batch-ai-runner.js` ready for N=100+ parallel runs. Per-worker isolated subdir → race-free concurrency. JSONL ingest via `playtest-analyzer` agent.

4. **balance-illuminator agent calibration mode WORKS**: invoked with batch CSV + RCA delivered 281-line analysis with 3 knob proposals + SPRT plan + MAP-Elites grid sketch. Agent shipped `docs/research/2026-05-09-aggressive-profile-calibration.md` autonomous.

5. **K4 Approach A stickiness FAILS**: additive bonus 0.15-0.30 cannot dominate weighted sum (Distance/TargetHealth/SelfHealth 0.4-0.8 each). Score gradient too steep. Approach B commit-window OR Approach C softmax temperature deferred next cycle.

## Production state

- `aggressive` profile: `use_utility_brain: false` (K3 fix #2146 maintained)
- `aggressive_no_util`: ablation reproduction profile (preserved)
- `aggressive_with_stickiness` (sticky 0.15): negative sweep, preserved for retest
- `aggressive_sticky_30`: negative sweep, preserved
- `balanced` + `cautious`: utility OFF (unchanged)
- Sim harness + batch runner shipped + tested live tunnel x4 sessions

## Files toccati

Game/:
- `apps/backend/services/network/wsSession.js` (world_confirm handler)
- `apps/backend/services/ai/utilityBrain.js` (stickiness branch + selectAction wiring)
- `apps/backend/services/ai/declareSistemaIntents.js` (per-profile stickiness merge)
- `apps/backend/services/ai/sistemaTurnRunner.js` (last_action + last_move_direction tracking)
- `packs/evo_tactics_pack/data/balance/ai_profiles.yaml` (K3 flip + 2 sweep profiles)
- `tests/smoke/ai-driven-sim.js` (FASE 1 harness + sistema_decision capture)
- `tools/sim/batch-ai-runner.js` (FASE 2 parallel runner)
- `docs/research/2026-05-09-*.md` × 4 (RCA + H1 + K3 + K4)
- `docs/playtest/2026-05-09-fase1-ai-driven-sim-harness.md`
- `docs/playtest/2026-05-09-fase2-batch-ai-runner.md`

Godot v2:
- `scripts/phone/phone_composer_view.gd` (Conferma mondo CTA)
- `scripts/net/lobby_api.gd` + `companion_api.gd` + `coop_api.gd` (timeout 60s + retry)
- `scripts/net/coop_ws_peer.gd` (world_confirm_accepted handler register)

## Resume triggers

> _"esegui K4 Approach B commit-window — declareSistemaIntents.js anti-flip guard"_

> _"esegui K4 Approach C softmax temperature — selectAction stochastic"_

> _"esegui MAP-Elites K4 grid — sticky × commit × softmax behavior cells"_

> _"esegui FASE 5 nightly cron + Slack alert on regression"_

> _"esegui FASE 1 T1.3 browser sync spectator — Chrome MCP screenshots per phase"_

## Refs

- `docs/research/2026-05-09-aggressive-profile-calibration.md` (balance-illuminator agent RCA, 281 LOC)
- `docs/research/2026-05-09-aggressive-h1-validation-oscillation.md` (H1 confirm)
- `docs/research/2026-05-09-k3-fix-shipped-k4-audit.md` (K3 fix + K4 audit proposal)
- `docs/research/2026-05-09-k4-stickiness-implementation.md` (K4 implementation + sweep negative)
- Live batch dirs: `C:/tmp/ai-sim-runs/batch-2026-05-09T*` × 5 (~165 JSONL files cumulative)
