---
name: Sprint plan v3 canonical reference
description: Where to find authoritative sprint specs + sub-step roadmap
type: reference
originSessionId: 585dba96-6d14-4988-ab48-b6cb8dcaf004
---
Canonical sprint plan v3 path: `C:/Users/VGit/Desktop/Game/docs/planning/2026-04-29-master-execution-plan-v3.md` (sibling repo Game/, read-only).

Live sprint progress + sub-step roadmap on Godot side: `C:/Users/VGit/Desktop/Game-Godot-v2/docs/godot-v2/sprint-p-onset.md` (Sprint P) + similar per-sprint onset docs (sprint-o-onset.md etc).

Sprint sequence (Fase 3 cutover):
- M Bootstrap → N Vertical slice MVP → O session engine port → **P trait+lifecycle+mating** → Q encounter+ETL+test parity → R co-op WS → S cutover.

Sprint P sub-steps:
- P.onset — TraitEffect + TraitCatalog + sample 8 trait + YAML preprocessor (~3-4h) ✅
- P.1 — Full 458 trait ETL (~2-3g) ✅
- P.x — TraitEffect alt schema `triggers_on_ally_attack` + BeastBondReaction (~0.5g) ✅
- P.2 — D20Resolver trait integration (~2-3g) ✅
- P.3 — Lifecycle Resource + 15 species port (~2-3g) ✅
- P.4 — Lifecycle ↔ MatingTrigger integration (~1-2g) ✅

Sprint P CLOSED. Sprint Q next: encounter + biome ETL + GUT parity audit ≥250/384 critical port (~1.5-2 sett).
