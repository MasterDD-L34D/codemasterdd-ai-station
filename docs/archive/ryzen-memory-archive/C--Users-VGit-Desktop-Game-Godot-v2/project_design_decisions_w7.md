---
name: W7-Ferrospora design decisions (master-dd 2026-05-04)
description: 7 design decisioni master-dd su AI personalità + selection model + profile assignment per Sprint W7-Ferrospora caller-wire integration + AI sprint future
type: project
originSessionId: 6299d943-a1b3-410f-9e20-19b5971732e3
---
Master-dd ha sbloccato 3 decision-point post Ferrospora SEQUENCE FULL CLOSURE 5/5 (#147/#148/#152/#155/#156) + caller-wire #1 BattleFeedAdapter (#158).

## A — AI personalità (Beehave plan #133)

- **A1-b**: **9 personalità totali** = 3 base (aggressive/cautious/opportunist) × 3 ruoli (skirmisher/tank/support). Esempi: `aggressive_skirmisher`, `cautious_tank`, `opportunist_support`.
- **A2-a**: **Code-first authoring** — Beehave tree built programmatically in GDScript (no editor visuale .tres). Veloce per debug, no plugin learning curve.
- **A3-b**: **Naming narrativo** — nodi behavior tree usano labels umane, es. `panic_when_wounded` (NOT `bb_low_hp_retreat`), `seek_weakest_target`, `protect_ally_under_threat`.
- **A4-b**: **Random a spawn** — encounter spawner pesca personalità random dal pool, non hardcoded per file unità. Più varietà tra partite.

## B — Selection model in combat

- **B1-a**: **XCOM/FFT sticky click** — click su Unit attiva selezione persistente. UnitInfoPanel mostra HP/CT/traits/status finché player clicca altra Unit o cella vuota. Forecast panel mostra preview pre-AttackAction. Combat lento ma informativo, party-based RPG feel.

## C — Assegnazione AI personalità a nemici

- **C1-b**: **Per-encounter** — encounter YAML specifica `ai_profile_pool: [aggressive_skirmisher, cautious_tank, opportunist_support]`. Spawner pesca random dal pool per ogni SISTEMA spawned (consistent con A4-b). Encounter design ricco, varietà cross-encounter.

## How to apply

**Sprint priorità 1 — caller-wire #2-#4 (B1-a sticky)**:
- UnitSelectionState bus singleton (selected_unit_id + signal selection_changed)
- UnitInfoPanelAdapter (listen bus → bind_unit)
- ForecastPanelAdapter (pre-AttackAction preview pop-up)
- BoardOverlayAdapter (move/attack range tile rendering)
- Unit.clicked signal + Main wire bus emit + HudView mount

**Sprint priorità 2 — Beehave authoring (A1-b + A2-a + A3-b + A4-b)**:
- Update doc plan #133 con 9-personality scope + code-first + narrative naming + random-spawn assignment
- Build 9 Beehave trees code-first (3 personality root × 3 role overlay)
- Tree node labels narrativi (panic_when_wounded, seek_weakest_target, hold_position_under_fire, etc.)
- Random spawn picker hooks encounter spawner

**Sprint priorità 3 — AI loaders caller-wire (C1-b per-encounter)**:
- Encounter YAML schema extension: `ai_profile_pool: [profile_id_1, profile_id_2, ...]`
- ETL update: encounter loader parses ai_profile_pool field
- Spawner: pesca random profile_id da pool per ogni spawn
- SisPolicy / UtilityBrain consume profile via AiProfilesLoader.get(profile_id) + AiPersonalityLoader.get(personality_id)
- Unit gets ai_profile_id field (runtime-assigned, not in YAML data)

## Why

**B1-a sticky** sblocca subito 3 PR concreti che migliorano UX combat (visible upgrade per master-dd playtest). A+C dipendono da playtest delle personalità — meglio fare prima B per testare combat clarity, poi A per AI variety, poi C per encounter richness.

**A1-b 9 personalità** sceglie variety over simplicity: 3 base bastano per playtest minimo ma 9 dà vero range tactical (skirmisher fast vs tank stoico vs support buff).

**A2-a code-first** evita plugin Beehave editor learning curve + permette debug rapido tramite GDScript breakpoints.

**A3-b narrative naming** allinea naming con design vision diegetic (creature non sono "bot" — hanno comportamenti emergenti che parlano in linguaggio umano).

**A4-b + C1-b combo** = encounter authoring ricco: ogni encounter è un palcoscenico tactical unico. Random pick consistent (seeded) per replay-ability.
