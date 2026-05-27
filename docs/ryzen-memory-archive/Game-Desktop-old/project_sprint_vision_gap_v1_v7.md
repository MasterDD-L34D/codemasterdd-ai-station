---
name: Vision Gap Sprint V1-V7 — 2026-04-26 autonomous
description: PR #1726 chiude 6 vision gap (V1 onboarding + V2 tri-sorgente + V4 PI pacchetti + V5 SG earn + V7 biome spawn + telemetry). 411/411 test verdi. Branch feat/p5-vision-gaps.
type: project
originSessionId: 92951e3c-9b9e-4632-a45a-5ea07cf9ded7
---
# Vision Gap Sprint V1-V7 — 2026-04-26 autonomous

**PR**: [#1726](https://github.com/MasterDD-L34D/Game/pull/1726) · **Branch**: `feat/p5-vision-gaps` · **Commits**: 3 (V1+V5+telemetry, V2+V4+V7, wire)

## Contesto

Audit post-M20 co-op shipping rileva 7 verità promesse in `docs/core/` con zero runtime. Sprint chiude 6/7 in 1 sessione autonomous (~12h work).

## Gap chiusi

| Gap | File source | Effort | Status |
| --- | --- | :-: | :-: |
| V1 Onboarding 60s Phase B | `51-ONBOARDING-60S.md` | ~2h | ✅ |
| V2 Tri-Sorgente reward API | `00-GDD_MASTER.md §8` + `tri-sorgente/overview.md` | ~8h | ✅ |
| V4 PI-Pacchetti 16×3 | `22-FORME_BASE_16.md` + `PI-Pacchetti-Forme.md` | ~4h | ✅ |
| V5 SG earn formula Opzione C | `26-ECONOMY_CANONICAL.md Q52` | ~3h | ✅ |
| V7 Biome-aware spawn bias | `28-NPC_BIOMI_SPAWN.md` | ~5h | ✅ |
| Telemetry endpoint | — (new) | ~2h | ✅ |
| V3 Mating/Nido slice | `27-MATING_NIDO.md` | ~20h | ⏸ deferred post-MVP |
| V6 UI TV dashboard identità | `30-UI_TV_IDENTITA.md` | ~6h | ⏸ deferred polish |

## File chiave creati

- `apps/backend/services/combat/sgTracker.js` — V5 pure module
- `apps/backend/services/combat/biomeSpawnBias.js` — V7 pure module
- `apps/backend/services/rewards/rewardOffer.js` + `rewardPoolLoader.js` + `skipFragmentStore.js`
- `apps/backend/services/forms/formPackRecommender.js`
- `apps/backend/routes/rewards.js` — `/offer /skip /fragments`
- `apps/play/src/onboardingPanel.js` + `.css` — Disco Elysium 3-stage overlay
- `data/core/rewards/reward_pool_mvp.yaml` — 15 carte seed
- `data/core/forms/form_pack_bias.yaml` — 16 MBTI × 3 pack canonical
- `docs/adr/ADR-2026-04-26-sg-earn-mixed.md`
- `docs/planning/2026-04-26-vision-gap-sprint-handoff.md`

## Wire runtime completi

- V5 sgTracker.accumulate in `session.js:363` damage step (main attack path)
- V7 biomeSpawnBias in `reinforcementSpawner.pickPoolEntry` optional hook

## Wire runtime completato (PR #1727 follow-up)

PR [#1727](https://github.com/MasterDD-L34D/Game/pull/1727) branch `feat/p5-vision-gap-followup` chiude tutto il residuo wire autonomous:

- V5 `applySgEarn` helper in abilityExecutor.js, wired 7 ability dmg sites (move_attack, attack_move, multi_attack post-adjustment, attack_push, ranged_attack post-adjustment, drain_attack, execution_attack post-adjustment) + surge_aoe AoE loop
- V5 lifecycle: `sgTracker.resetEncounter` su `/start`, helper `sgBeginTurnAll` dopo ogni `session.turn += 1` (4 siti: advanceThroughAiTurns + action early-end + 2 round-bridge flows)
- V1 onboardingPanel già wired PR #1726 in main.js:998-1048 (host + campaign_id gate)
- V2 rewardOffer trigger in phaseCoordinator su phase=debrief via `bridge.getCampaignSummary()`
- V4 formPackRecommender in characterCreation fetch `/api/forms/:id/packs` su form select, render top-3 bias_forma + bias_job + universal

## Residuo userland only

- TKT-M11B-06 playtest live 4p ngrok (non-automatizzabile) → chiude P5 🟢

## Test baseline

411/411 aggregate · 307 AI + 90 new + 14 regression

## Pattern applicato (da archivio)

- **Feature Cancellation Test**: classifica gap per truth-violation severity
- **Technical Task Breaker**: sottoproblemi + ordine dipendenze
- **First Principles Filter**: ogni gap aumenta chiarezza/agency/interazione
- Source: `Archivio_Libreria_Operativa_Progetti/02_LIBRARY/02_Modules_Starter_Packs_and_Best_Of.md`

## Lessons

- Branch sync: `git stash -u` + checkout new branch da main quando locale diverge ma commits coincidono
- Docs governance: `doc_status` enum strict: active/draft/review_needed/legacy_active/generated/historical_ref/superseded (NO "complete"/"accepted")
- Windows test flake EADDRINUSE bulk runs — pre-existing, non regressione
- V2 Python bridge legacy → Node-native coerente con M6-#4 kill-Python direction
