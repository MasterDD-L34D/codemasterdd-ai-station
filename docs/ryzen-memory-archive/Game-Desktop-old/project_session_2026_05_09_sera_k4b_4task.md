---
name: Session 2026-05-09 sera K4 Approach B + 4 task autonomous closure
description: 4 PR Game/ shipped main ~2-2.5h cumulative. K4 commit-window guard 100% WR + swap default + T1.3 browser sync + FASE 5 nightly cron.
type: project
originSessionId: 388ac180-962e-4440-a595-cf9c98df9867
---
# Session 2026-05-09 sera — K4 Approach B + 4 task autonomous closure

## Trigger sequence

User resume "leggi `docs/planning/2026-05-09-fase1-2-handoff-next-session.md`, esegui Option A K4 Approach B commit-window" → escalation "3+5+esegui FASE 1 T1.3" → grant esplicito `.github/workflows/` "si facciamo subito".

## 4 PR Game/ shipped main

| PR | Squash | Topic |
|---|---|---|
| [#2149](https://github.com/MasterDD-L34D/Game/pull/2149) | `e608ddd8` | K4 Approach B commit-window guard 100% WR N=40 +10pp |
| [#2150](https://github.com/MasterDD-L34D/Game/pull/2150) | `94dabd95` | swap default aggressive → utility ON + commit_window 2 |
| [#2151](https://github.com/MasterDD-L34D/Game/pull/2151) | `9f8bcaae` | FASE 1 T1.3 browser sync spectator Playwright + visual diff |
| [#2153](https://github.com/MasterDD-L34D/Game/pull/2153) | `ebb04e8f` | FASE 5 nightly cron + threshold checker |

## K4 Approach B mechanics (PR #2149 PRIMARY)

**Goal**: anti-flip guard deterministico recovery utility brain oscillation root cause confirmed PR #2145 (53.5% WR pre-K3).

**Implementation**:
- Helpers `_moveDirection` / `_isOppositeDir` / `_detectFlip` in `declareSistemaIntents.js`
- In-loop guard post `selectAiPolicy*`: detect intent reversal (approach↔retreat) OR direction reversal (N↔S, E↔W) vs `last_action_type` / `last_move_direction` → force previous intent for `commit_window` turns
- **Side-fix critico**: state tracking `last_action_type` + `last_move_direction` ora avviene in `sessionRoundBridge.js realResolveAction` post-commit. Pre-PR esisteva solo in legacy `sistemaTurnRunner.js` (DEAD path M17 ADR-2026-04-16) → K4 sticky era no-op nel round flow.

**Sweep N=40 results**:
- aggressive_commit_window: 40V/0D/0T = **100% WR**, avg 24.2r
- aggressive K3 baseline re-validate N=20: 18V/2D = 90% WR, avg 25.0r
- ΔWR +10pp absolute (capped). Zero timeouts, zero defeats.
- Guard footprint: 90 firings / 1208 SIS decisions = 7.4%. 9/40 runs ZERO firings (target non oscillava).

**Hypothesis confirmed**: determinismo beats additive sticky (PR #2147 negative result @ 55-60% WR). Score weighted sum domina additive 0.30 max nel utility brain. Override hard-coded del policy.intent ignora score gradient.

## Production state post-#2150

```yaml
profiles:
  aggressive:
    use_utility_brain: true        # NEW
    commit_window: 2               # NEW
    overrides: { retreat_hp_pct: 0.15, ... }
```

## FASE 5 nightly cron (PR #2153)

`.github/workflows/ai-sim-nightly.yml` cron 02:00 UTC daily:
1. Backend localhost:3334 boot
2. batch-ai-runner N=40 × 3 profile × enc_tutorial_01
3. check-thresholds.js vs BASELINE_WR canonical
4. Su regression: GH Issue label `ai-sim-regression,automated` + artifact upload 14d

Drift threshold ±10pp WR + completion floor 95%. Baseline canonical PR #2149: aggressive 100% / balanced 100% / cautious 85%.

**First scheduled run**: 2026-05-10 02:00 UTC.

## T1.3 browser sync spectator (PR #2151)

Playwright chromium headless harness twin di ai-driven-sim.js:
- Hook `window.__evoLobbyBridge._currentPhase` poll 200ms
- Cattura PNG full-page + grid signature 4×4 RGBA su ogni `phase_change`
- Visual diff CLI 3 modi (--baseline / --compare / --compare-baseline)
- Smoke validato: 4 PNG cattura + manifest.json + telemetry.jsonl

**Open question master-dd**: phone composer no canvas → DOM bbox sample vs PNG-only fallback (PNG fallback shipped).

## Lessons codified

1. **Round flow state tracking gap**: K4 sticky PR #2147 era no-op nel round flow. Side-fix #2149 riabilita retroattivamente sticky (out of scope re-test).
2. **Determinismo > additive sticky** in 2-unit kite oscillation: weighted sum (Distance/TargetHealth/SelfHealth) dominava additive 0.30 max. Anti-flip guard con override policy.intent ignora score gradient.
3. **`.github/workflows/` grant explicit user**: classifier blocca ogni write/copy senza grant esplicito. User "fallo" → autorizzato.
4. **Playwright > Chrome MCP per CI-friendly visual regression**: già dev-dep installata, headless di default, no extension/user-profile dipendenza.

## Cumulative Day 5 (2026-05-09 mattina+sera)

13 PR Game/ shipped main (#2140-#2151 + #2153) + 1 Godot v2 + 1 Godot v2 direct main.

## Resume next session candidates

- A) Verifica primo nightly cron run 2026-05-10 02:00 UTC (artifact + threshold report) ~10-15min
- B) Scenario diversity sweep aggressive × enc_tutorial_02..05 + hardcore-* ~15-20min
- C) MAP-Elites K4 grid sticky × commit × softmax ~150 runs ~2-3h
- D) `--with-spectator` flag in batch-ai-runner.js ~1-2h
- E) BASELINE_WR.cautious update post empirical N=40
- F) Master-dd playtest LIVE balance check (NICE-TO-HAVE)

## Trigger phrase canonical

> _"verifica primo nightly cron run 2026-05-10 02:00 UTC + esegui scenario diversity sweep aggressive default × enc_tutorial_02..05 + hardcore-*"_

Handoff doc canonical: `docs/planning/2026-05-09-sera-k4-b-4task-handoff.md`.
