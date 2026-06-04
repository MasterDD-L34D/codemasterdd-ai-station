---
name: calibration-toolkit-2026-05-21
description: Full calibration methodology toolkit + L-069/070/071/072/073 cluster. Both hardcore scenarios P6 primary in-band. 7 PRs merged session 2026-05-20/21.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f821c00b-6bc9-4eec-bacc-b012fef82617
---

# Calibration toolkit + lessons cluster (session 2026-05-20/21)

## Toolkit shipped to main (all `tools/py/`)

| Tool | Method | Key flags |
|------|--------|-----------|
| `calibrate_parallel.py` | C — 4-shard parallel 4x | `--scenario --n --shards 4 --base-port 3341`; `start_shard(curves_path)` staging-aware |
| `calibrate_sprt.py` | B — Wilson CI95 early-stop | stops when CI entirely above/below/inside band |
| `calibrate_optuna.py` | A — Bayesian TPE | `--parallel` (per-trial 4x) `--n-per-trial 40` (L-073 ratify-grade) staging-writer |
| `calibrate_map_elites.py` | D — QD real evaluator | `--stub-eval` (synthetic) OR real (N=40 default, ~17h full) |
| `calibrate_drift_verify.py` | N=10 probe -> N=40 ratify | `--prior-baseline <wr%>` L-072 inversion guard (AWAY -> abort exit 7) |
| `check_trait_mirror_consistency.py` | Engine-LIVE-Surface-DEAD validator | trait_mechanics.yaml vs active_effects.yaml mirror |

## scenario_overrides infra (data/core/balance/damage_curves.yaml)

Per-scenario knob layer (Hades Pact + ITB pattern). Resolvers in
`apps/backend/services/balance/damageCurves.js`:
- `boss_hp_multiplier` -> applyScenarioBossHpOverride (build-time, hardcoreScenario.js)
- `turn_limit_defeat_override` -> getTurnLimitDefeat(scenarioId) (sessionRoundBridge.js)
- `enemy_count_modifier` -> applyScenarioEnemyCountModifier (build-time)
- `enemy_damage_multiplier_override` -> applyEnemyDamageMultiplier(scenarioId) REPLACES class (session.js /start, needs encounter.id in payload)

Backend env `DAMAGE_CURVES_PATH` overrides default path -> staging-writer
(calibration tools write candidate to damage_curves.staging.yaml, production untouched).

## Lessons cluster (calibration-rigor, CLAUDE.md anti-pattern #14-18)

- **#14 L-069** N=10 lucky-sample false in-band — N=10 CI95 +/-30pp; never pillar upgrade from N=10 alone if CI spans band ceiling. N=40 ratify gate.
- **#15 L-070** Multi-knob sequential overshoot — iter3 (WR 0->85%) + iter4 (15->47.5%) + 3A (60->70% inverted). Single-knob bisection safer; multi-knob needs Bayesian joint-effect.
- **#16 L-071** LOBBY_WS_PORT collision multi-shard — `LOBBY_WS_ENABLED=false` per shard (else 426 Upgrade Required).
- **#17 L-073** Optimizer-on-noise — optimizer objective N MUST be >= ratify threshold (N=40). Optuna N=20-objective converged to noise (best N=20 WR 15% -> N=40 ratify 30% OOB).
- **#18 L-072** Direction-test N=10 probe pre-N=40 — knob direction non-obvious -> N=10 probe FIRST, compare vs PRIOR baseline (not target band). TOWARD=escalate, AWAY=reverse delta. Auto-enforced in calibrate_drift_verify.py `--prior-baseline`.

## Pillar P6 state (main, post 7 PRs)

| Scenario | Knob | WR (N=40) | Status |
|----------|------|-----------|--------|
| hardcore_06 | boss_hp_multiplier 0.65 | 15% | primary in-band; secondary defeat 85% RED — structural blocker, design call OD-032 |
| hardcore_07 | enemy_damage_multiplier_override 2.1 | 45% | in-band |

## hardcore_06 secondary band: RESOLVED A+C 2026-05-21 (OD-032, PR #2365)

Master-dd verdict A+C. SHIPPED PR #2365:
- **A**: damage_curves.yaml hardcore band revised to engine reality — defeat
  [0.40,0.55]->[0.75,0.85], timeout [0.15,0.25]->[0.00,0.05], WR [0.15,0.25] kept.
  Evidence prod config N=40: WR 25/def 75/to 0 (pooled N=72 ~21/78/0). Original
  band was design-target incompatible with own turn_limit_defeat=25 (M7 kills
  timeout). NO production knob change (boss_hp 0.65 + M7 timer stay).
- **C**: enemy_damage_multiplier_override knob wired hc06 (batch encounter.id +
  Optuna knob_space + multi-band objective). Capability only (timer-off ALT path).
- **Bug fixed**: batch client ignored DAMAGE_CURVES_PATH env (no-op staging knobs).
  Now env-aware + passed to batch subprocess in optuna/parallel.
- **Side-finding (spawned task)**: backend hangs after ~7 sessions/process during
  batch (3 runs stalled at 7/shard, both timer regimes). Workaround: 8 shards x 5.
- **ALT not shipped (master-dd)**: timeout-middle band needs M7 revert + stalemate
  tune (fragile, iter7=67% timeout). enemy_damage knob ready if pursued.

### Original investigation (why blocked, kept for context)
Secondary band (defeat 40-55, timeout 15-25) **structurally unreachable** with
current knobs. Do NOT relaunch Optuna expecting the original band.

3 blockers:
1. **turn_limit binary, not split-control**: MAX_ROUNDS=40 + detect_outcome
   force-defeat at turn>=limit means any limit <=40 catches all unresolved games
   before round 40 -> timeout=0% for ALL of [25,40]. Timeout only unlocks at
   limit >=41 (= disabled). No partial conversion -> can't finely hit timeout 15-25%.
2. **Disabling timer spikes WR**: probe turn_limit=41 + boss_hp 0.65 -> 5/6 victory
   (turns 23-38). WR looked 15% only because turn-25 force-defeat cut off games the
   party would win. Timer-off needs boss_hp >> [0.50,1.00] to suppress WR. 1 effective
   continuous knob (boss_hp) vs 3 band constraints -> likely infeasible.
3. **No-op bug**: batch CLIENT ignores DAMAGE_CURVES_PATH env (hardcoded prod,
   batch_calibrate_hardcore06.py:21). load_turn_limit_defeat/override-parser read
   prod -> Optuna turn_limit_defeat_override knob was a SILENT NO-OP (client always
   used prod=25, only boss_hp varied). Optuna objective was also WR-only (ignored
   defeat/timeout bands).

Master-dd verdict needed (OPEN_DECISIONS OD-032): A) revise canonical band to
match engine reality, B) raise MAX_ROUNDS for partial-conversion control, or
C) add independent split knob (enemy_damage like hc07). Prereq for B/C: fix
no-op bug (client env-aware path + pass env to batch subprocess) + multi-band
Optuna objective. User chose "Hold — design call" 2026-05-21, no run, no ship.

WR primary stays in-band (boss_hp 0.65 = WR 15% N=40). This is SECONDARY band only.

## hardcore_07 secondary band: ANALYZED -> healthy, verdict C (leave as-is) 2026-05-21

Mirror of hc06 secondary analysis. hc07 = INVERSE of hc06:
- N=40 (edm 2.1): WR 35% (in-band 30-50), defeat **0%**, timeout **65%**, rounds ~14/15.
- hc07 = mission-timer "pod rush" (MAX_ROUNDS=15 + real mission_timer). detect_outcome:
  timer_expired -> timeout. Losses are TIMEOUTS (ran out of time), party never wiped
  (defeat 0% even at edm 2.1 = scenario can't fully wipe party; not a bug, by design).
- hc07 has NO canonical defeat/timeout band (uses tool-level WR "30-50%" only, NOT class
  hardcore bands). WR in-band = balanced.
- VERDICT C (master-dd 2026-05-21): leave as-is. WR-only band sufficient; timeout is the
  designed loss for a beat-the-clock scenario; zero unfair wipes. NO mechanic change, NO
  band codification. Do NOT re-investigate — hc07 healthy.
- Both hardcore P6 scenarios now closed: hc06 (defeat-dominated, band revised OD-032) +
  hc07 (timeout-dominated, healthy as-is). Inverse loss profiles, both WR in-band.

## PRs merged session 2026-05-20/21

#2354 (scenario_overrides + α P0 trio) / #2355 (Codex audit) / #2357 (MAP-Elites
real) / #2358 (staging-writer #2356) / #2359 (hc07 edm 2.1) / #2360 (L-072
auto-enforce) / #2361 (Optuna parallel-internal). Issue #2356 resolved.

## L-074 — calibration host MUST be 127.0.0.1, never "localhost" (Windows IPv6 stall)

Symptom reported as: backend "hangs" after ~7 sessions/shard during batch
calibration; /api/health 200 but /round/execute "never returns"; deterministic at
~7; workaround 8 shards x 5.

ROOT CAUSE (empirically isolated 2026-05-21, NOT the backend): the calibration
clients used `http://localhost:{port}`. Backend binds IPv4 (`0.0.0.0`). On Windows
`localhost` resolves IPv6 `::1` first, and Python `urllib` has no Happy-Eyeballs
→ it stalls ~2s per request before falling back to 127.0.0.1. Measured: urllib to
`localhost` = **2.04s/call** vs `127.0.0.1` = **0.001s/call**. A run does ~28 calls
(tutorial + start + ~25 round/execute + end) → ~56s/run of pure connect-stall while
the backend sits idle (CPU ~0.25s/run, RSS flat). N=10 batch: ~560s via localhost
→ **7s via 127.0.0.1** (~80x). The "hang at 7" = slowness (+ likely urllib 30s
timeout/_retry on a worse box) misread as a hang; backend never accumulated anything.

FALSIFIED red herring: `appendEvent`→`persistEvents` rewrites the FULL session.events
array per event (O(n^2) ~20MB writes/session). Looked guilty (I/O-bound, low CPU) but
A/B with per-event persist disabled changed nothing (222s vs 216s) — the localhost
stall dominated. persistEvents is a real latent micro-inefficiency, NOT this bug.

FIX (PR pending): default all calibration host strings to `127.0.0.1` —
calibrate_parallel/optuna shard-host construction + DEFAULT_HOST/`--host` defaults in
batch_calibrate_hardcore06/07 + calibrate_sprt/map_elites/drift_verify. curl was a
poor diagnostic here (does Happy-Eyeballs → only 0.2s); reproduce client stalls with
the SAME client (urllib), and always bind-vs-resolve check (IPv4 server + name host).

LESSON: for any local HTTP harness on the Windows fleet, use 127.0.0.1 not localhost.
Generalizes L-071 (env/port footguns). Verified: calibrate_parallel hc06 N=8 = 4.0s.

## Method C empirical 4x (repeated)

iter4 hc06 642.7s, 3A hc07 359.6s, edm22/edm21 ~360s each — all N=40 4x vs serial.
Optuna parallel-internal: per-trial 24min -> 6min.
