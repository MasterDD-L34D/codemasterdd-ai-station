---
name: Session 2026-05-05 post-cutover cleanup (services/rules removal + aspect_token)
description: 2 PR merged main 2026-05-05 evening — Phase 3 services/rules/ Python rules engine removal + mutation aspect_token render registry expansion. Pre-cutover Phase A debt cleared.
type: project
originSessionId: c749682d-02c9-459e-9bf9-b2449d7daf62
---
# Session 2026-05-05 post-cutover cleanup

**Trigger**: user "ripartiamo, leggi memorie + Godot v2 plans". Auto mode active. 2 PR shipped autonomous.

## PR shipped main

| PR | SHA | Topic |
|---|---|---|
| [#2059](https://github.com/MasterDD-L34D/Game/pull/2059) | `d0c86c60` | services/rules/ Phase 3 removal — delete 8 Python file + 7 test Python + worker bridge spec + tabletop tools + lint patches + ADR/CLAUDE.md/combat hub aggiornati |
| [#2060](https://github.com/MasterDD-L34D/Game/pull/2060) | `5dc65315` | mutation aspect_token 36/36 backfill + render.js ASPECT_TOKEN_OVERLAY 4→36 entry + lint enforcement bilaterale |
| [#2061](https://github.com/MasterDD-L34D/Game/pull/2061) | `d16cd941` | TKT-MUSEUM-SKIV-VOICES — Type 5+7 ennea voice palette (42 line × 7 beat) + enneaVoice.js evaluator + GET /voice endpoint con seed Mulberry32 + telemetry ennea_voice_type_used + 14 unit test |
| [#2062](https://github.com/MasterDD-L34D/Game/pull/2062) | `5595c968` | Ennea voice palette 9/9 extension — 7 nuovi archetype YAML (Riformatore/Coordinatore/Conquistatore/Individualista/Lealista/Cacciatore/Stoico) + 18 unit test (incluso 63 cell coverage matrix). P4 🟡++ → 🟢 candidato |

## Discovery chiave

**Plan pivot**: user proposto bundle 3 ticket (TKT-RULES-SIMULATE-BALANCE + TKT-TRAITS-ANCESTOR-BUFF-STAT + TKT-GATE5-CONVICTION). Verifica git → tutti già live su main via squash PR #2058 (commit `885ce028` "fix(audit): resolve 3 pre-cutover tickets" includeva conviction deprecate + evaluateMovementTraits handler + simulate_balance.py delete). Branch `fix/pre-cutover-audit-cleanup` aveva 5 commit, squash main solo `87ea9ccf`. Pivottato a Phase 3 services/rules/ removal (next-step naturale unblocked).

## ADR closures

- **ADR-2026-04-19** (Kill Python rules engine): PROPOSED → ACCEPTED + Phase 3 closed
- **ADR-2026-04-13** (Rules Engine d20): superseded by ADR-2026-04-19
- **TKT-RULES-PHASE-3-REMOVAL**: BACKLOG closed
- **TKT-MUTATION-P6-VISUAL**: BACKLOG closed (visual_swap_it pre-shipped #711619e7 + aspect_token 2026-05-05)

## Files touched

**Deleted (20)**: services/rules/{__init__,demo_cli,grid,hydration,resolver,round_orchestrator,trait_effects,worker}.py + DEPRECATED.md + generated/trait_types.py + tests/test_{demo_cli,grid,hydration,master_dm_parser,resolver,round_orchestrator,trait_effects}.py + tests/server/rules-bridge.spec.js + tools/py/{master_dm,mark_python_rules_deprecated}.py

**Patched**: tools/py/gen_trait_types.py (drop PY codegen) + tools/py/lint_mutations.py (REQUIRED_FIELDS bilaterale) + apps/play/src/render.js (+32 token entry) + data/core/mutations/mutation_catalog.yaml (36 aspect_token) + packs/evo_tactics_pack/data/balance/{action_speed,trait_mechanics}.yaml (Node consumer comment) + tests/api/contracts-hydration-snapshot.test.js (snapshot frozen note)

**Doc**: CLAUDE.md (3 punti) + docs/hubs/combat.md (Phase 3 closure section + commands Node-only) + docs/adr/{2026-04-13,2026-04-19}-*.md + docs/governance/workstream_matrix.json + BACKLOG.md (2 ticket close)

## Test baseline

- AI tests: 383/383 verde (zero regression)
- Pytest: 735/735 verde post 7 file delete
- npm run format:check: clean
- docs governance --strict: 0 errors
- node --test tests/play/*.test.js: 200/200
- Runtime probe backend: /api/health 200 + POST /api/session/start crea session_id coerente senza Python

## Logica preservata (idea sopravvive senza Python)

| Python rimosso | Node canonical vivo |
|---|---|
| resolver.py (d20 + MoS + damage) | session.js performAttack + combat/resistanceEngine.js |
| round_orchestrator.py | services/roundOrchestrator.js |
| hydration.py + trait_effects.py | services/traitEffects.js + evaluateMovementTraits |
| grid.py | services/ai/hexGrid.js |
| worker.py + demo_cli.py + master_dm.py | morti per design (no tabletop, no bridge) |

## Next session candidati

- **A) TKT-MUSEUM-SKIV-VOICES** (P1 ~6h) — Type 5+7 narrative palette in `data/core/narrative/ennea_voices/{type_5,type_7}.yaml` + selector narrativeEngine.js + telemetry. Pre-req ENNEA-WIRE shipped ✓
- **B) Phone smoke retry B5** (userland master-dd ~30min) — sblocca cutover Fase 3 ADR formal accept
- **C) Sprint Q Godot stub→full** (~6-8h) — Tier 2 BiomeModifiers/BiomeResonance/SynergyDetector full impl
- **D) Phase 2 audit runtime probe** (~1h autonomous) — boot stack curl every route + trait fire log
- **E) Sentience tier 4 species candidate** (T4=0 attualmente, gap OD-008)

**Resume trigger**: _"leggi memory project_session_2026_05_05_post_cutover_cleanup.md, procedi opzione X"_

## Lessons codified

- **Verify before claim done pattern (squash bundling)**: branch può avere N commit ma squash main include solo subset. Sempre `git log --oneline branch ^main` per scoprire commit non ancora portati. Salvato 4h di lavoro evitando duplicate fix.
- **Plan pivot autonomous**: user-proposed bundle scoperto already-shipped via discovery. Pivot a next-step naturale (Phase 3 removal) invece di no-op work. Asciuga dependency chain.
- **Auto regen drift Windows CRLF**: `python tools/py/gen_trait_types.py` produce CRLF/single-quote drift su file generated/. Revert via `git checkout HEAD --` post smoke. Generator works, ma include drift = polluting PR.
- **Render registry pre-emptive expand**: aggiungere aspect_token field senza espandere ASPECT_TOKEN_OVERLAY render.js = engine LIVE surface DEAD anti-pattern. Sempre includere registry expand stesso PR (32 nuove entry glyph+color).
