---
name: PR #2155 nightly cron P0 fix
description: Nightly AI sim cron broken on first scheduled run; WS port mismatch + bash -e regression-detection bug. Fixed pre-cron 2026-05-10 02:00 UTC.
type: project
originSessionId: eee74a8e-ebbd-4132-9f61-1a9667d8d169
---
# PR #2155 — Nightly AI Sim P0 fix (2026-05-09 sera)

## Context

User canonical resume trigger: _"verifica primo nightly cron run 2026-05-10 02:00 UTC + esegui scenario diversity sweep aggressive default × enc_tutorial_02..05 + hardcore-*"_. Eseguito ~6h pre-prima cron scheduled 2026-05-10 02:00 UTC.

## P0 finding

Manual `workflow_dispatch` smoke prima cron → run [#25609138128](https://github.com/MasterDD-L34D/Game/actions/runs/25609138128) FAIL 0/120 completion. Cron 02:00 UTC sarebbe fallito identico.

### Root cause #1 (P0 ship-blocker)

`tests/smoke/ai-driven-sim.js:53` derivava `WS_URL` da `TUNNEL` env (HTTP base URL) tramite scheme swap `https→wss / http→ws`. Cloudflare tunnel mode collassa HTTP (3334) + lobby WS (3341) sullo stesso hostname → swap funziona dev. CI direct-localhost mode tiene porte separate → worker connetteva `ws://127.0.0.1:3334/ws` su porta HTTP-only → `ws_open` mai resolved → exit ~145ms con `ws_error` (connection refused / unexpected response).

**Fix**: `AI_SIM_WS_URL` override env in worker (default = TUNNEL-derived, backward compat). Workflow passa `ws://127.0.0.1:3341/ws` esplicito.

### Root cause #2 (P1 latent regression-detection bug)

Eval step usava `bash -e` default → `node check-thresholds.js` exit non-zero terminava lo step PRIMA di `STATUS=$?` capture + `GITHUB_OUTPUT` write. `steps.eval.outputs.regression` empty → "Open regression issue" step skippato anche su drift detected. `continue-on-error: true` mascherava il fault step status.

**Fix**: `set +e` esplicito prima del node call.

## Verification

| Run | Config | Outcome |
|-----|--------|---------|
| [#25609138128](https://github.com/MasterDD-L34D/Game/actions/runs/25609138128) | pre-fix N=40 | ❌ 0/120 unknown 145ms |
| [#25609224916](https://github.com/MasterDD-L34D/Game/actions/runs/25609224916) | WS fix N=10 max=15 | ✅ 30/30 completion, ⚠️ WR 0% (max_rounds floor) |
| [#25609294902](https://github.com/MasterDD-L34D/Game/actions/runs/25609294902) | WS fix N=40 max=40 | ✅ **120/120 completion, verdict CLEAN** |

### N=40 final verdict

| Profile | WR | Drift | Completion | Avg rounds |
|---------|---:|------:|-----------:|-----------:|
| aggressive | 92.5% (37/40) | -7.5pp | 100% | 24.2 |
| balanced | 92.5% (37/40) | -7.5pp | 100% | 25.0 |
| cautious | 95.0% (38/40) | +10.0pp | 100% | 24.45 |

Aggressive avg_rounds 24.2 = PR #2149 baseline N=40 exact match (production state preserved).

## PR status

[#2155](https://github.com/MasterDD-L34D/Game/pull/2155) `claude/great-goldberg-6fbf6a` — 2 commit:
- `966e2e67` — WS port fix (worker + workflow)
- `e5ada07d` — set +e regression-detection fix

CI gates verde (governance + paths-filter + site-audit + stack-quality). MERGEABLE.

**Auto-merge L3 ineligible**: tocca `.github/workflows/` (forbidden path per ADR-2026-05-07). Master-dd manual verdict required.

## Scenario diversity sweep — BLOCKED

User chiese sweep × `enc_tutorial_02..05 + hardcore-*`. Reality check rivelato:
- `tests/smoke/ai-driven-sim.js:150-193` usa **synthetic 2-enemy units hardcoded** (enc_tutorial_01-equivalent), NON carica YAML scenario
- Flag `--scenarios` solo stamp telemetry `scenario_id`, NO real diversity
- `enc_tutorial_03/04/05.yaml` **non esistono** in repo (solo 01+02)
- `hardcore-*` programmatic via `apps/backend/services/hardcoreScenario.js`, no YAML

Eseguire sweep ora → 160-240 runs identici tranne RNG label. Zero real diversity signal.

**Path forward verdict needed**:
- A) Skip + surface gap (questa scelta) + harness extension scoping ~3-5h
- B) Pseudo-sweep transparent ~30-45min (label-only diversity, RNG stress)
- C) Single-scenario stress N=160 ~30min (extend N=40 baseline)
- D) Use 7 esistenti YAML scenarios (caverna/escort/frattura/hardcore_reinf/savana/savana_skiv/survival) → stesso problema (harness no carica YAML)

## Lessons codified

1. **CI direct-localhost ≠ tunnel mode**: porte split richiedono override esplicito. PR #2153 (#ebb04e8f nightly cron) shipped senza testare CI mode → P0 caught solo a smoke proxy a T-6h prima first cron.
2. **bash -e + STATUS=$? incompatibili**: `set +e` esplicito mandatory quando si vuole capturare exit code per ramificare GITHUB_OUTPUT logic.
3. **continue-on-error maschera fault**: lo step "passa" anche su exit non-zero, ma successivi `if: steps.X.outputs.Y == 'true'` falliscono silently se output non scritto.
4. **Scenario diversity claim sbagliato in handoff**: il resume trigger user assumeva sweep funzionante, ma harness ha synthetic-only. Surface honest evita fabricated execution.

## Resume trigger

> _"merge PR #2155 (master-dd verdict), verifica primo cron run 2026-05-10 02:00 UTC artifact + threshold pass; poi scenario diversity sweep harness extension verdict A/B/C"_
