---
name: Schema decisions + wire wave 2026-05-11 (TKT-P6 full closure)
description: 4 PR post-verdict pipeline (vc_scoring fold + tile wire + rewind adapter + Main caller wire) + TKT-P6 full closure
type: project
originSessionId: c77e9715-286a-45d7-9987-55a73d50a206
---
## State after schema-wire wave 2026-05-11

4 PR shipped + merged post cross-stack wave 9 PR:
- #233 Decision 3 vc_scoring conviction_axis fold (3-layer psicologico fully wired)
- #234 Decision 1 tile-wire (EncounterRuntime.get_tile_at + CombatSession elev/terrain modifier inject pre-d20 + post-hit damage)
- #235 Decision 2 RewindSessionAdapter + MainRewind helpers (engine + adapter)
- #236 Decision 2 main.gd budget trim (8 comment blocks compressed -19 LOC) + caller wire (rewind public trigger)

**Why**: master-dd "procedi auto mode 3 punti" green-lit Option A across all 3 schema decisions (recommended verdict per PR #232 doc). Auto-mode pipeline shipped 4 PR post-verdict (4-7h estimated, actual ~3h).

**How to apply**:

1. TKT-P6 FULL CLOSURE pattern: engine module (RewindBuffer #225) → adapter (RewindSessionAdapter #235) → caller helpers static (MainRewind #235) → Main caller wire (PR #236 ensure_buffer + snapshot_pre_action + reset + rewind_last_action public trigger).

2. main.gd budget trim pattern: 8 verbose multi-line comment blocks compressed to 1-line each (~3-5 lines saved each). Apply when near max-file-lines=1000 cap. Examples in #236 diff.

3. Cross-stack wire layering: payload modifier inject pre-resolve (DefenderAdvantage / PseudoRng / ElevationTerrain pattern). Bonuses fold into actor.attack_mod + target.defense_mod local var → resolve → damage_bonus post-hit. Revert N/A (payload local).

4. Wire flow rewind: PG action → snapshot_pre_action push (Sistema skipped via should_snapshot_for_actor PG-gate) → combat end → reset clears buffer + budget restore → Main.rewind_last_action() pops + applies + restores pressure + HUD render via MainRewind.complete_rewind.

**Pending master-dd post-wave**:
- HUD RewindButton scene authoring (mirror Game/ FE #2244)
- Game/-side YAML elevation field 14 encounter (M14-A cross-stack adoption)
- M14-B Phase B DialogueBranchView UI scene
- M15 DebriefView PromotionPanel UX call
- JobCardPanel UX (PR #223 design call)
- Pressure-tier YAML authoring 14 encounter
- P2 Phase C+D REST + HUD
- Playtest #2 schedule window 2026-05-12 → 2026-05-18

**Tests cumulato wave**: +31 (vc_scoring 6 / tile-wire 10 / rewind_adapter 15). Lifetime 2026-05-11: cross-stack 130 + schema-wire 31 = +161 new GUT tests.

**13 PR session totali 2026-05-11**: 9 cross-stack (#221+#223+#224+#225+#226+#227+#228+#229+#230) + 1 closure docs (#231) + 1 schema decisions doc (#232 CLOSED) + 4 wire (#233+#234+#235+#236).
