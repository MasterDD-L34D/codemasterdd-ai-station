---
name: Sprint P closed state (as of 2026-04-30)
description: Sprint P fully shipped (P.onset → P.4 closed) — Sprint Q next
type: project
originSessionId: 585dba96-6d14-4988-ab48-b6cb8dcaf004
---
Sprint P (trait + lifecycle + mating port) status:

- ✅ P.onset (PR #30) — TraitEffect Resource + TraitCatalog + sample 8 trait + YAML preprocessor.
- ✅ P.1 (PR #31) — Full 458 trait ETL via `tools/etl/yaml_to_json.py` → `data/traits/active_effects.json` (339KB).
- ✅ P.x (PR #32) — TraitEffect alt schema `triggers_on_ally_attack` (3 traits: legame_di_branco, spirito_combattivo, pack_tactics) + BeastBondReaction `check_reactions_with_catalog` overload.
- ✅ P.2 (PR #33) — D20Resolver trait integration: `resolve_attack(..., catalog, actor_traits, target_traits, context)` → `AttackResult.{triggered_traits, status_applies, damage_trait_delta}` → `RoundOrchestrator` applies status via `apply_status` mapper. 3 codex P1 fixes bundled.
- ✅ P.3 (PR #34) — LifecycleStage + SpeciesLifecycle + LifecycleCatalog (mirror TraitCatalog pattern) + 15 species ETL via `tools/etl/lifecycle_yaml_to_json.py` → `data/lifecycle/lifecycles.json` (35KB). Canonical phase chain hatchling → juvenile → mature → apex → legacy (terminal).
- ✅ P.4 (PR #37) — MatingTrigger ↔ LifecycleCatalog integration. `set_lifecycle_catalog()` injection enriches child preview with `species_id_canonical`, `evolution_path`, `starting_stage="hatchling"`, `biome_affinity`, `inheritable_phase_fields` (alias `inheritable_phase_traits` deprecated since P.4.1) from highest parent phase. Backward compat preserved.
- ✅ P.4.1 (direct push `0427d68`) — vertical slice bridge: docs state truth + player-driven AttackAction (explicit `target_id` required, no auto-target) + DOT cleanup via `combat_session.apply_damage` helper + MatingTrigger field rename + action bar minima (HudView Attack/Move/Defend/Trait buttons).
- ✅ Regression fix (PR #38) — 4 P.2/P.3 trait integration tests updated to pass explicit `target_id: "b"` (P.4.1 strict validation broke legacy auto-target); main.gd `_first_free_adjacent_cell` probe helper for HUD MOVE (was hitting Pulverator block).
- ✅ Drift sync (PR #39) — CLAUDE.md PR count 32→39 + GUT 439→451 + sprint narrative.

**Sprint P CLOSED.** Sprint Q next (encounter + biome ETL + GUT parity audit ≥250/384).

**Why:** Fase 3 cutover phase per plan v3 — Sprint P unlocked Q (encounter+data ETL+test parity audit) which is gating dataset prep for the rest of the port.

**How to apply:** When user asks resume Sprint Q, read `Game/docs/planning/2026-04-29-master-execution-plan-v3.md §Sprint Q` for full effort breakdown. Encounter YAML in `Game/data/encounters/` + `Game/docs/planning/encounters/` (14 files). ETL pattern mirrors P.3 lifecycle batch script.

Repo HEAD post-P.4 + P.4.1 audit + fix: `3f45b42`. 40 PR shipped main #1-#39 + P.4.1 direct push.
