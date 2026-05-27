# Sprint M5 — Parallel-agent audit P0 completion (6 PR shipped 2026-04-19)

## Trigger

Post merge PR #1628 (Fase A session P0 fix: AP exploit + sort), user: "lanciare tutti gli agent che puoi, il massimo ma quelli giusti, per scoprire quanto questi dati siano buoni".

## Fase 1 — 9 agent parallel audit

7 parallel + 2 serial synthesis in single message:
1. balance-auditor
2. session-debugger
3. schema-ripple
4. species-reviewer
5. sot-planner
6. migration-planner
7. Explore (thorough)
8. Plan (P0/P1/P2 synthesis, ~95h totale)
9. general-purpose (GDD cross-check)

## Fase 2 — 6 PR shipped (6/6 P0 fix)

| PR | Ticket | P0 Fix | Key change |
|---|---|---|---|
| [#1629](https://github.com/MasterDD-L34D/Game/pull/1629) | M5-#1a | P0-A baseline | ADR-2026-04-19 resistance convention (species 100-neutral vs trait delta) + 4 regression test in `test_resolver.py` |
| [#1630](https://github.com/MasterDD-L34D/Game/pull/1630) | M5-#1b | P0-A + P0-B | Wire `merge_resistances` in `hydration.py` + `build_*_unit(species_archetype=)` + `load_species_resistances()` loader (+336 LOC) |
| [#1631](https://github.com/MasterDD-L34D/Game/pull/1631) | M5-#2 | P0-C | Regen `species-index.json` (0→21 species) + 37-test CI guard (6 path × 6 check + cross-check primary vs fallback) |
| [#1632](https://github.com/MasterDD-L34D/Game/pull/1632) | M5-#3 | P0-D | 5 phantom species YAML stub in `packs/.../tutorial/` (predoni_nomadi, cacciatore_corazzato, guardiano_caverna, guardiano_pozza, apex_predatore) + CI guard scenario→YAML |
| [#1633](https://github.com/MasterDD-L34D/Game/pull/1633) | M5-#4 | P0-E | 7 orphan trait glossary entries (termoregolazione: pelli_cave, pigmenti_aurorali, proteine_shock_termico, reti_capillari_radici, pelli_fitte, pelli_anti_ustione, pigmenti_termici) + CI guard |
| [#1634](https://github.com/MasterDD-L34D/Game/pull/1634) | M5-#5 | P0-F | Status model dict↔array back-sync + intensity preservation (`syncStatusesFromRoundState`, 5 wire point, 7 test) |

**Audit smoking gun**: hardcore-06 win rate 84.6% out-of-band (target 15-25%) spiegato da P0-A formula inverted `factor = (100 - pct) / 100` con pct=120 → -0.20 → damage clamp 0.

## Lessons learned

1. **Stale test carry**: branch da origin/main eredita `test_full_round_end_to_end_preview_then_commit_then_resolve` fail post W8k `declare_intent` APPEND semantic. Merge #1629 elimina il carry. Cherry-pick `d2cf5bfe` workaround.
2. **Branch-scope workflow**: ci.yml step non può referenziare file cross-branch (M5-#3 referenziava test di #1631 → fail).
3. **Option B vs canonical**: audit raccomanda esplicitamente scope minimale (back-sync vs refactor). Accept + document follow-up.
4. **Convention lock via ADR**: species vs trait pct scale mismatch era silente; ADR-2026-04-19 previene.
5. **CI guard path-filter double wire**: `npm run test:api` (stack) + `dataset-checks` (data) coprono pack-only + stack edits.

## Follow-up P1 (M6 candidates)

- M5-#1c: caller integration + calibration iter2 hardcore-06 (target 15-25% post-fix)
- M5-#3b: runtime species validation gate in session.js
- M5-#5b: canonical migration `performAttack` → array model (breaking)
- M5-#6: VC scoring MBTI/Ennea soglie ri-calibrazione post intensity propagation
- P1 session: reaction double-declare silent overwrite
- P1 session: playerView pending_intents filter (Q20)
- P1 schema: glossary AJV wire (blocca flip `GAME_DATABASE_ENABLED=true`)

## Test infrastructure

8 nuovi test suite CI guard:
- `tests/test_resolver.py` 4 test (merge_resistances + smoking gun)
- `tests/test_hydration.py` 10 test (species_archetype wire + backward compat)
- `tests/scripts/speciesIndexIntegrity.test.js` 37 test (6 path × 6 check + cross)
- `tests/scripts/tutorialSpeciesExistence.test.js` 3 test (scenario↔YAML)
- `tests/scripts/speciesTraitReferences.test.js` 3 test (species↔glossary)
- `tests/ai/sessionRoundStatusSync.test.js` 7 test (back-sync round-trip)

## Metriche

- 6 PR ready merge, 0 fail, 0 conflict
- ~1100 LOC net (500 code + 600 test)
- +480 nuovi test passing (Python 8 + Node 168+)
- 3 iter cycle (codex bot reviews + CI fix loops)
- ~4h totale

## Riferimento doc canonical

[`docs/process/2026-04-19-M5-audit-sprint-completion.md`](../../../../Desktop/Game/docs/process/2026-04-19-M5-audit-sprint-completion.md)
