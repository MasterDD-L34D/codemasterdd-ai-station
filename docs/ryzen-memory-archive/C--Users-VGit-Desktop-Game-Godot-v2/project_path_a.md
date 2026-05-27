---
name: Path A — parallel W (world creation) + Q (encounter ETL)
description: Sprint roadmap post-Sprint P. W0-W7 world creation flow + Sprint Q.1-Q.2 encounter+biome ETL run in parallel. Custode naming locked.
type: project
originSessionId: 585dba96-6d14-4988-ab48-b6cb8dcaf004
---
Post-Sprint P (closed at HEAD `1172819`), user pushed strategic plan
`docs/godot-v2/integrated-world-companion-plan.md` introducing world
creation flow (Lobby → Form Pulse → World Setup → Scenario Brief →
Combat). Decision (2026-04-30): execute Path A — parallel W0-W7 +
Sprint Q.1-Q.2 ETL.

**Why:** V3 doctrine says worldgen = pressure conditions, not tactical
map. Combat data depth (encounter parity ≥250/384) still needed but
orthogonal to world creation flow. Sample-JSON-first approach lets
W2/W3 UI advance without backend wire (Game/ Express endpoints port
deferred to W4).

**How to apply:** When user resumes, Path A status is canonical:
- W0 ✅ (PR #40) — 4 strategic docs (1387 LOC)
- W1 ✅ (PR #41) — `WorldSetupState` Resource + sample JSON + 17 tests
- Q.1 ✅ (PR #42) — `EncounterCatalog` + `EncounterDefinition` + 14 encounter ETL (dual-schema) + 19 tests
- W2 ✅ (PR #44) — `WorldSetupHostView.tscn` TV scene + `CompanionPanel.tscn` consume sample JSON, no backend wire + 15 tests
- Q.2 ✅ (PR #45) — `BiomeCatalog` + `BiomeDefinition` + 20 biome ETL (+ 7 alias merges) + 22 tests + parity audit gate ≥250/384 → 524/524 (137%)
- **Sprint Q CLOSED**
- W3 ✅ (PR #47) — `ScenarioBriefView` + Main `boot_phase` switch (manual chain world_setup → scenario_brief → combat from sample JSON, HUD restore, backward compat default=combat preserved) + 14 tests
- **Audit cycle ✅** (PR #49-#52, post-W3 thorough check):
  - PR #49 codex P2 backlog (4 fixes: vote_tally aggregate, difficulty_bucket groups mapping, null bind propagate, alias shadow guard) + 10 regression tests
  - PR #50 comprehensive visual pass (cinzel theme StyleBox upgrade, ColorRect bg per visual mode, PressureMeter ProgressBar, BiomePalette 21 class colors, Custode silhouette tint, ScenarioBriefView hierarchy + QuoteFrame, Tween fade-in 500-600ms ritual reveals) + 18 visual tests
  - PR #51 AGENTS.md committed + .gitignore .claude/worktrees/
  - PR #52 W3.5 4 missing scenes (LobbyView §1, FormPulseHostView §2 with 5-axis aggregate ProgressBar rows, DebriefView §7 + DebriefState Resource, LegacyMemoryView §8) + 28 tests — bible §1/§2/§7/§8 gap closed
- **Sessione 2026-05-01 18 PR (#55-#72)** — Path A bible coverage CHIUSA TV+Phone:
  - PR #55 W4 wire (CoopApi async + LoadingOverlay + ErrorBanner + 4 view inject)
  - PR #56 P1 hygiene (4 StyleBox .tres + BiomePalette.id_to_class consolidator)
  - PR #57 W4.5 TV (WorldSeedRevealView Bible §3)
  - PR #58 W-Tokens-Phase-2 (Theme type variations cinzel.tres)
  - PR #59 retrofit (WorldSeedRevealView token migration)
  - PR #60 doc sync audit
  - PR #61 preflight (4 master-dd Q resolved + W6 cert decision auth-tunnel)
  - PR #62 W5-Godot (CompanionArchetypePool + CompanionPicker + 3 multi-biome samples atollo/caverna/foresta)
  - PR #63 P-x-lineage (LineagePropagator port — Spore S5 plumbing)
  - PR #64 W4.5.1 (BiomeAdjacency + multi-biome cards)
  - PR #65 W6 onset (CoopWsPeer scaffold)
  - PR #66 W6 phone (composer + lobby_join + world_vote)
  - PR #67 W6 lobby-api (LobbyApi HTTP refactor)
  - PR #68 W6 phone-reveal (Bible §3 phone resonance)
  - PR #69 W6 phone-combat (Bible §6 intent submit)
  - PR #70 W6 phone-debrief (Bible §7 lineage choice)
  - PR #71 W6 ws-reconnect (auto-reconnect backoff)
  - PR #72 docs final sync
  - PR #73 verify cycle (3 audit agents, doc + memory updates, no code drift found)
  - PR #74 W6 deploy ops (HTML5 build script + phone-mode boot + Cloudflare Tunnel deploy doc)
  - PR #75 W7-radar Bible §2 (5-axis Polygon2D replacing ProgressBar fallback)
  - **Cross-repo Game/#2028 W5-bb backend services MERGED** (4 services + worldEnricher facade + coopOrchestrator extension + routes/coop.js rich payload + 57 tests Game/-side)
  - PR #76-#78 doc sync + lineage integration follow-up
  - PR #79 W7-phone-form-pulse (4 MBTI axis sliders TF/NS/EI/JP, sums to 1.0, composer integration)
  - PR #80 W7-character-creation TV §0 (CharacterCreationHostView + main.gd phase machine LOBBY → CHARACTER_CREATION → FORM_PULSE)
  - PR #81 W7-phone-character-creation §0 (name + species + job pick, MODE_CHARACTER_CREATION composer dispatch)
- **Bible coverage matrix**: §0+§1+§2+§3+§4+§6+§7 TV+Phone shipped; §5/§8 TV-only by design. §0 chiusura: TV CharacterCreationHostView (PR #80) + Phone PhoneCharacterCreationView (PR #81). §2 con full radar polygon (W7 PR #75). Phone phase chain: lobby → character_creation → form_pulse → world_seed_reveal → world_setup → combat → debrief.
- **1+2+3 sequence completata** (master-dd request 2026-05-01): (1) W5-bb cross-repo Game/ services ✅ MERGED, (2) W6 deploy ops ✅ MERGED (manual master-dd ops documented), (3) W7-radar ✅ MERGED.
- **Cross-repo bridge end-to-end**: Godot v2 phone composer LobbyJoin → CoopApi.confirm_world() ↔ Game/ Express POST /api/coop/world/confirm → rich payload {world, ermes, aliena_summary_it, custode} → Godot WorldSetupState.from_dict.
- **GUT 882/882** (2408 asserts, post PR #81 +13 phone §0 tests).
- **Cross-repo Game/ tag** `web-v1-final` pushed (commit 91876ac0 pivot anchor).
- **Next session opzioni master-dd**: (a) **Master-dd manual deploy** — Cloudflare Tunnel run + DNS records + Game/ backend startup + phone real-device smoke test; (b) **Asset-driven W7 follow-ups** — Wildermyth portraits + companion sprite art (Skiv canonical + biome variants) + tactical vs ritual theme variation + audio cues — designer sprint or art commission; (c) **Codex backlog review** — wait codex P1/P2 reviews su recent PR e bundle se rilevanti.

**Naming lock (canonical, do not negotiate):**
- `Custode` = generic companion system name (Italian, diegetic narrator/guide)
- `Skiv` = canonical/prototype instance only
- All Godot class names use `custode` (avoid `Companion` placeholder)

**Companion runtime sample shape** (from `data/world_setup/sample_world_setup.json`):
```
custode: {
  display_name: "Vrak",
  species_id: "dune_stalker",
  voice_it: "Il vento porta fame.",
  biome_origin_id: "savana"
}
```

**Encounter ETL dual-schema** — `EncounterDefinition.schema` discriminates:
- `groups` schema (Game/data/encounters/, 4 YAML): id/label/difficulty/groups[]
- `waves` schema (Game/docs/planning/encounters/, 10 YAML): encounter_id/waves[]/conditions

`list_groups()` / `list_waves()` accessors return empty for the wrong
schema. `difficulty_bucket()` heuristic maps both schemas to
tutorial/standard/elite/hardcore.

Repo HEAD post sessione 2026-05-01 1+2+3 sequence close: `00f4147`. 75+ PR shipped main #1-#75 + P.4.1 direct push. Cross-repo Game/#2028 W5-bb MERGED `54d7bce2`.

**Visual pillar canonical** (post audit cycle): `resources/themes/cinzel.tres` upgraded with full StyleBoxFlat for PanelContainer + Button × 5 states + ProgressBar. `scripts/ui/biome_palette.gd` is canonical color source — 21 biome class → Color + pressure → green/amber/red tint. Custode silhouette tints by biome_origin via `BiomePalette`. All Path A scenes (W1+W2+W3+W3.5 = 6 scenes) consistent: cinzel theme + ColorRect dark void bg + ✦ glyphs primary buttons + unique_name_in_owner labels. Tween fade-in via `main.gd::_fade_in_view(view, duration)` 500-600ms on phase transitions.

**Test pattern stabilized**: scene tests prefer `%UniqueName` get_node syntax (robust to layout changes vs hierarchy paths). Adopted across 15 path conversions in PR #50.

**Catalog pattern fully established**: TraitCatalog (P.onset/P.1) → LifecycleCatalog (P.3) → EncounterCatalog (Q.1) → BiomeCatalog (Q.2) → WorldSetupState (W1). All RefCounted/Resource pairs follow same `load_from_json_file` / `from_dict` / `get_X` / `has` / `all_ids` API.

**ETL pattern**: `tools/etl/<thing>_yaml_to_json.py` script per dataset. Args: `--in <yaml>` (single) OR `--in-dir <dir>` (batch). Output: `data/<thing>/<thing>.json`. Optional `--aliases` merge for legacy slug compat (introduced Q.2).

**Sessione 2026-05-03 deploy smoke** (master-dd real-device iPhone Safari): Cloudflare Quick Tunnel demo PASS end-to-end. WS handshake + JWT auth + lobby join verified ("Connesso come Chiara (player)"). 33 PR Godot v2 sessione 2026-05-01/03 (#85-#117) + 9 PR cross-repo Game/ (#2028-#2036). Sprint R complete + Sprint R codex bundle + Cloudflare deploy fix chain (#108-#117): automation scripts + WebOriginResolver auto-detect + readiness regex + viewport 480x854 + virtual keyboard window.prompt() bridge + URL build + /ws path. GUT 1065/1065. Session artifacts archived in `docs/godot-v2/deploy-smoke-2026-05-03/SESSION-SUMMARY.md`.

**Sessione 2026-05-03/04 deploy-FU bundle** (3 pure-code follow-ups closing Cloudflare deploy smoke friction items, all MERGED): **Game/ PR #2037 dotenv autoload** (`apps/backend/index.js` calls `require('dotenv').config({path: <repo-root>/.env})` before `./app` — eliminates `$env:AUTH_SECRET` PowerShell workaround. dotenv ^16.6.1 backend dep. +3 tests). **Godot v2 PR #120 ?room= URL auto-fill** (WebOriginResolver `read_url_query(key)` + pure `parse_query` helper. PhoneLobbyJoinView `_ready` reads `?room=` (fallback `?code=`) on web → `apply_room_code_from_url(raw)`. Deep-link from REST create. +14 GUT). **Godot v2 PR #121 in-app Crea stanza** (PhoneLobbyJoinView `%CreateButton` → LobbyApi.create_room. Validation split _validate_join vs _validate_create. ValidationLabel hint flicker fix. Test split per gdlint max-public-methods=20: test_phone_lobby_join_view.gd 15 + test_phone_lobby_join_view_create.gd 8. +8 GUT). FU3 rebased onto FU2 pre-merge for clean conflict resolution. GUT **1087/1087** (2766 asserts) post-merge.

**Sessione 2026-05-04 codex+polish bundle** (3 PR closing codex automated review backlog deploy chain + minor polish, all MERGED): **Godot v2 PR #123 codex bundle** (2 P1 + 4 P2: `_parse_port` defensive helper no silent `int("")=0` + `_on_create_pressed` post-fill `_refresh_validation` retry path + mobile_keyboard touch-only no-double-prompt + matchMedia coarse-pointer gate desktop regression closed + deploy-quick.sh trap `$rc` preserved + build_web.sh viewport regex fail-fast. +7 GUT new test_mobile_keyboard_helper.gd file). **Game/ PR #2038 dotenv non-override test** (explicit precedence: pre-set process.env → load .env → CLI value wins. +1 test, 4/4). **Godot v2 PR #124 polish bundle** (parse_query `+` → space decode RFC 1738 / WHATWG parity JS URLSearchParams + deploy-quickstart curl one-liner PowerShell + Bash + jq → phone deep-link URL. +1 GUT test). GUT **1095/1095** (2786 asserts) post-merge. 20 codex findings shipped lifetime. Pure-code rimanenti zero. Master-dd next: asset-driven W7 (designer sprint) | Sprint Q encounter ETL extension | Sprint S cutover checklist.

**Sessione 2026-05-04 W7.x pure-code heavy bundle** (13 PR shipped 2026-05-04, 12 merged + 1 closed redundant, MERGED). Master-dd chip "plan + execute heavier pure-code pending" + autonomous merges:

- PR #126 Sprint R `auth_expired` re-mint wire (PhoneComposer ↔ LobbyApi ↔ CoopWsPeer) +7 GUT
- PR #127 LineagePropagator caller wire via WorldSetupState.campaign + LineageCampaignSpec helper +19 GUT
- PR #128 click-to-target AttackAction (replaces P.4.1 demo bridge) + Unit.set_target_highlight +11 GUT
- PR #129 ObjectiveEvaluator (4 types: elimination/survival/capture_point/escort) + ReinforcementSpawner (waves) +28 GUT
- PR #130 BiomeModifiers + BiomeResonance + TerrainReactions full impl (3 stub→full migrations) +32 GUT
- PR #131 closed redundant (subsumed by #134 audit fix bundle)
- PR #132 EncounterRuntime aggregator + Main combat phase wire (stacked #129+#130, audit fix Bug A/B/C inline)
- PR #133 Beehave AI tactical tree authoring plan-only (4 master-dd checkpoints, awaits C1)
- PR #134 post-merge audit fix bundle: #128 defensive Variant iter on _first_live_unit_id + _is_cell_occupied (freed Unit crash) + #129 ReinforcementSpawner cumulative spawn_idx for unique ids (same-species diff-tier collision) +3 GUT
- PR #135 doc audit cleanup: integrated-world-companion-plan + sprint-r-plan drift fix
- PR #136 BiomeResonance per-attack wire (SISTEMA atk += biome.mod_biome via _combat_specs_from_tutorial reorder) +3 GUT
- PR #137 TimeOfDayModifier full impl (4 phases dawn/day/dusk/night + diurnal/nocturnal split + i18n labels) +12 GUT
- PR #138 SgTracker full impl (Sistema Gravity stresswave accumulator + threshold events, consumes biome.stresswave config) +17 GUT
- PR #139 final doc sync chore

Combat stubs registry **14 → 9** (5 ported W7.x: BiomeModifiers / BiomeResonance / TerrainReactions / TimeOfDayModifier / SgTracker). GUT 1095 → 1255+ (3018+ asserts). Sprint R closed end-to-end (R.0-R.5 + codex bundle + auth_expired caller wire). Stale local branches cleaned post-merge.

Audit cycle (in-session post-merge bug detection on #128/#129 → #134; on #130/#132 → #132 inline audit fix): both yielded real bugs caught + fixed with test coverage. Pattern memorized: aggressive post-merge audit catches drift between stubs.

Stubs rimanenti (9): 5 combat (ArchetypePassives, SenseReveal, SynergyDetector, TelepathicReveal, PassiveStatusApplier) + 4 AI (AiPersonalityLoader, AiProfilesLoader, AiProgressMeter, SistemaTurnRunner). Each blocked by data ETL or design dependency.

Master-dd checkpoint pendenti: **Beehave plan #133 C1 greenlight** (scope 3 trees vs +archetype overlay, naming, authoring code-first vs editor) — only doc-driven gate. Pure-code ulteriori options (without master-dd input): pursue 5 remaining combat stubs with available data, OR codex review polling on #126-#138 PR backlog.

**Sessione 2026-05-04 coordinated 3-phase chip** (audit + unblock + ship, 5 PR shipped open for review):

Phase 1 — codex review polling PR #126-#141 (15 recent PR Godot v2): **0 codex inline findings** (all reviews 👍 reaction equivalent only, top-level "no findings" markers via `chatgpt-codex-connector`). Codex bundle PR NOT needed.

Phase 2 — combat stub unblock check (5 stubs): **4 UNBLOCKED + 1 BLOCKED**.
- ArchetypePassives ✅ pure helpers, 5 passive_token strings, no data dep — ship
- PassiveStatusApplier ✅ pure, requires TraitCatalog (Sprint P shipped) — ship
- SenseReveal ✅ pure helpers, hardcoded `sensori_geomagnetici` trait id, no catalog dep — ship
- TelepathicReveal ✅ pure, status-driven, no catalog dep — ship
- SynergyDetector ❌ BLOCKED — requires `species.yaml` `catalog.synergies` + `species[].default_parts` ETL (not present Godot side)

Phase 3 — AI stub unblock check (4 stubs): **1 UNBLOCKED + 1 SUBSUMED + 2 BLOCKED**.
- AiProgressMeter ✅ pure, mirrors PRESSURE_TIERS table, `session.sistema_pressure` read — ship
- SistemaTurnRunner 🟢 SUBSUMED — covered by SistemaIntents O.3 + RoundOrchestrator O.1 (registry comment), no flip needed
- AiPersonalityLoader ❌ BLOCKED — requires `data/core/ai/ai_profiles_extended.yaml` ETL
- AiProfilesLoader ❌ BLOCKED — requires `packs/.../ai_profiles.yaml` ETL

Phase 4 — 5 PR shipped (open, NO auto-merge default per memory `feedback_codex_reviews` — `feat` requires master-dd review):
- PR #142 feat(combat): full impl SenseReveal — +14 GUT, 1266/1266
- PR #143 feat(combat): full impl TelepathicReveal — +15 GUT, 1266/1266
- PR #144 feat(ai): full impl AiProgressMeter — +16 GUT, 1267/1267
- PR #145 feat(combat): full impl ArchetypePassives — +21 GUT split across 2 files (gdlint max-public-methods=20: test_archetype_passives.gd 16 + test_archetype_passives_alpha.gd 5), 1273/1273
- PR #146 feat(combat): full impl PassiveStatusApplier — +15 GUT, 1267/1267

Each PR independently branched off origin/main → minor sequential conflicts on `stubs_registry.gd` count line + `test_stubs_registry.gd` count + match branches expected on merge. Each PR self-contained with local Godot 4.6.2 GUT pre-flight green + gdformat + gdlint clean.

Stub registry delta (when all 5 land): 9 → 4 (1 combat blocked SynergyDetector + 1 AI subsumed SistemaTurnRunner + 2 AI blocked AiPersonalityLoader/AiProfilesLoader).

Master-dd checkpoints pendenti post-chip: (1) Review/merge PR #142-#146 sequenziale, (2) Beehave plan #133 C1 greenlight unchanged, (3) Asset-driven W7 (designer sprint), (4) SynergyDetector blocked → species.yaml ETL unlock pre-flip, (5) AiPersonalityLoader/AiProfilesLoader blocked → ai_profiles*.yaml ETL unlock pre-flip.

**Sessione 2026-05-04 follow-up "1+2"** (master-dd request: merge sequenziale + ETL sprint):

Phase 1 — merge PR #142-#146: master-dd merged ALL 5 sequenziale via GitHub UI con conflict resolution inline (registry count line). Final main HEAD landed at registry count 4 (SynergyDetector + AiPersonalityLoader + AiProfilesLoader + SistemaTurnRunner). Bonus PR #147 art(ui) Ferrospora landed alongside.

Phase 2 — ETL sprint unlocking 3 blocked stubs (3 PR shipped, all open for review):

- **PR #149** `feat(combat): SynergyDetector full impl + species ETL + SynergyCatalog`. Stack: `tools/etl/species_yaml_to_json.py` → `data/species/species.json` (1 synergy + 15 species) + `scripts/data/synergy_catalog.gd` Resource + `scripts/combat/synergy_detector.gd` full impl. +21 GUT (test_synergy_catalog.gd 7 + test_synergy_detector.gd 14). Suite 1352/1352.
- **PR #151** `feat(ai): AiPersonalityLoader full impl + personalities ETL + AiPersonalityCatalog`. Stack: `tools/etl/ai_personalities_yaml_to_json.py` → `data/ai/ai_personalities.json` (3 personalities aggressive_bloodthirsty/cautious_defensive/opportunist_flexible) + `scripts/data/ai_personality_catalog.gd` Resource + `scripts/ai/ai_personality_loader.gd` static facade. +15 GUT. Suite 1346/1346.
- **PR #153** `feat(ai): AiProfilesLoader full impl + profiles ETL + AiProfilesCatalog`. Stack: `tools/etl/ai_profiles_yaml_to_json.py` → `data/ai/ai_profiles.json` (3 profiles + sistema_resource_model invariant) + `scripts/data/ai_profiles_catalog.gd` Resource + `scripts/ai/ai_profiles_loader.gd` static facade. +16 GUT. Suite 1347/1347.

ETL pattern triplicated proven: `tools/etl/<thing>_yaml_to_json.py` → `data/<thing>/<thing>.json` → `scripts/data/<thing>_catalog.gd` Resource → `scripts/ai/<thing>_loader.gd` static facade (or domain-specific scripts/combat/ for non-AI).

Stub registry final state when all 3 land: **9 → 1 (SistemaTurnRunner SUBSUMED only)**. Registry comment doc-only — no flip needed. Pure-code zero blocked.

Sample lifetime stub flips delta this session: 9 active → 1 doc-only. 5 PR (master-dd merged) + 3 PR (open for review) = 8 PR total shipped this chip.

Master-dd checkpoint pendenti post-1+2: (1) Review/merge PR #149/#151/#153 sequenziale (same 1-line conflict pattern stubs_registry), (2) Beehave plan #133 C1 greenlight unchanged, (3) Asset-driven W7 designer sprint unchanged, (4) Caller wires for new services (SynergyDetector hook su attack resolution + AiPersonalityLoader/AiProfilesLoader hook su Sistema turn runner — caller integration deferred until master-dd direzione).

**Sessione 2026-05-04 follow-up "controlla main + parallelo"**:

State check post master-dd merge: #149 SynergyDetector MERGED. #151 AiPersonalityLoader + #153 AiProfilesLoader OPEN. Bonus master-dd ship: PR #147/#148/#152 Ferrospora UI sigil pass landed alongside.

Parallel actions:
1. **Rebased + force-pushed** #151 + #153 onto current main (1-line conflict on stubs_registry count + match block — both branches were branched off pre-#149-merge with count expecting 4→3, current main is at 3 so resolution = both flips land → count 3→2). Pure mechanical resolve.
2. **Spawned 2 parallel Explore agents** for caller-wire research:
   - Agent A: SynergyDetector wire — identified CombatSession.resolve_attack_action (lines 90-145) + RoundOrchestrator._resolve_end_turn (line 156-160) + Main._build_encounter_runtime catalog load. Estimated ~28 LOC pure-code wire fits 50-line guardrail.
   - Agent B: AI loaders wire — identified SisPolicy hardcoded thresholds (LOW_HP_RETREAT_THRESHOLD line 22 / KITE_BUFFER line 23 / DEFAULT_ATTACK_RANGE line 20) + UtilityBrain.score_action accepts weights param. Outstanding design decisions: profile selection mechanism (per-unit / per-encounter / difficulty mapping). Master-dd checkpoint required.
3. **Shipped PR #154** `feat(combat): wire SynergyDetector into CombatSession + RoundOrchestrator`. Implementation:
   - CombatSession +48 LOC: `_synergy_catalog` + `_synergy_session` Dict state container + `set_synergy_catalog` + `get_synergy_session_state` + augmented `resolve_attack_action` (detect post-D20 + fold bonus_damage on hit + record_synergy_fire post-damage + telemetry `synergy_bonus`/`synergies` fields)
   - RoundOrchestrator +15 LOC: `synergy_catalog` + `set_synergy_catalog` + start_session inject + reset_round_synergy_tracker call in `_resolve_end_turn`
   - Main +8 LOC: SynergyCatalog.load_from_json_file + inject pre-start_session
   - +13 GUT tests (test_combat_session_synergy_wire 7 + test_round_orchestrator_synergy_reset 4 + 2 helper tests)
   - Suite 1366/1366 pass (3191 asserts).
4. **Deferred AI loaders wire** until: (a) PR #151 + #153 merge (compile dep), (b) master-dd design call on profile assignment mechanism.

8 PR shipped lifetime this chip ("1+2" + "controlla main parallel"): 5 merged (#142-#146 by master-dd) + 3 open ETL+flip (#149 already merged + #151 + #153 rebased) + 1 open caller wire (#154). Stub registry final state when all rebased PRs land: **2 stubs remaining** (AiProfilesLoader if #151 lands first, OR vice versa — both will resolve to 0 AI stubs + 0 combat stubs except SistemaTurnRunner subsumed).

Pure-code rimanenti dopo all-merge: AI loaders caller wire (2 PR planned: SisPolicy threshold override from AiProfilesLoader.overrides, UtilityBrain weights from AiPersonalityLoader.intent_weights). Blocker: master-dd design call su profile assignment mechanism prima implementazione.

**Sessione 2026-05-04 final closure** (chip 100% + Ferrospora UI Art Pass v1 FULL CLOSURE 5/5):

Finalizzato batch merge sequenziale tutti i PR aperti (rebase + force-with-lease su conflitti stubs_registry/test_stubs_registry pattern noto): #143/#144/#145/#146/#149/#151/#153/#154 chip + #148/#152/#155/#156 Ferrospora. Ogni rebase: drop entry stub + aggiorna count line + cleanup match cases. Lifetime force-push usato 4× (#144/#145/#146/#153) — guardrail Git Destructive richiede explicit auth ogni volta.

**Ferrospora UI Art Pass v1 SEQUENCE FULL CLOSURE** (5/5 PR merged):
- PR #147 art(ui) v1 assets/docs/tools (109 file: 90 PNG + 17 doc + 4 tool + GitHub helpers + .gitignore artifacts/ferrospora_*/* preserve README pattern)
- PR #148 feat(ui) ActionButtonSigil component (~30 LOC TextureButton wrapper auto-load 4-state textures, 6 GUT)
- PR #152 feat(ui) HudView text→sigil swap (SIGIL_ACTION_MAP attack/defend/move/spore/wait → AttackAction/DefendAction/MoveAction/UseTraitAction/EndTurnAction; signal contract `action_selected(action_type)` PRESERVED; defensive ritual no-op; +9 LOC nette hud.gd)
- PR #155 feat(ui) ActionDock shell (~30 LOC Control + 5-socket HBox + actiondock_v2_runtime_1200.png frame; signal action_pressed re-emit; 6 GUT)
- PR #156 feat(ui) panels bundle (UnitInfoPanel + ForecastPanel + BoardOverlay + BattleFeed; 4 component scaffold standalone <50 LOC each + 24 GUT; live wire deferred caller PR future)

**Stub registry FINAL STATE**: 14 → 1 (only SistemaTurnRunner SUBSUMED by design — comment-only, no flip needed). Chip 100% closure su tutti gli stub flippabili.

**Sessione totale 2026-05-04**: **17 PR mergiati** (cleanup #140/#141 + 8 chip stub flips #142-#146/#149/#151/#153 + chip wire #154 + 5 Ferrospora #147/#148/#152/#155/#156 + 3 codex/lint inline fix). GUT post-#156: ~1390/1390 (~3260 asserts).

**Constraint check Ferrospora**: tutti rispettati end-to-end (NO RoundOrchestrator modify in visual PR — solo PR #154 chip combat wire legittimo; NO RitualAction creato — asset pool in PR #147 ma nessuna code surface; HudView `action_selected(action_type: String)` signal PRESERVED PR #152; UnitInfoPanel naming NOT SelectedUnitPanel; wait→EndTurnAction mapping wired SIGIL_ACTION_MAP).

**Codex lifetime stats**: 0 codex inline findings su #126-#156 (chatgpt-codex-connector "no findings" markers solo). Phase 1 chip codex bundle skipped — no actionable items.

**Master-dd checkpoint pendenti post-final-closure**:
1. **Ferrospora caller wire integration sprint** (future): live data binding RoundOrchestrator/CombatSession/TileMap → 4 panels (UnitInfoPanel.bind_unit on selection / ForecastPanel.set_forecast pre-AttackAction / BoardOverlay overlays per move/attack range / BattleFeed.push_event on action_resolved). Effort ~5-8 LOC wire per panel + caller refactor in main.gd.
2. **Beehave plan #133 C1 greenlight** invariato (scope 3 trees vs +archetype overlay, naming, authoring code-first vs editor) — solo doc-driven gate.
3. **AI loaders caller wire** (2 PR planned post #151+#153 merge): SisPolicy threshold override from AiProfilesLoader.overrides + UtilityBrain weights from AiPersonalityLoader.intent_weights. Blocker: master-dd design call su profile assignment mechanism (per-unit / per-encounter / difficulty mapping).
4. **Asset W7 designer sprint** invariato (Wildermyth portraits + companion sprite art Skiv canonical + biome variants + audio cues — external commission).
5. **Cloudflare prod deploy** invariato (named tunnel + DNS records + dominio — master-dd manual ops).

**Sessione 2026-05-04 caller-wire end-to-end closure** (+5 PR post-Ferrospora full closure):

Master-dd 2026-05-04 ha sbloccato 7 design decision (project_design_decisions_w7.md): A1-b 9 personalità (3×3 ruoli) / A2-a code-first / A3-b narrative naming / A4-b random spawn / B1-a XCOM sticky / C1-b per-encounter profile pool. Sprint priorità 1 (B1-a sticky) eseguito interamente.

- **PR #158** BattleFeedAdapter (caller-wire #1) — listens action_resolved → BattleFeed.push_event con format actor→target:RESULT(N HP) + severity damage/status. FakeOrchestrator inner class pattern + 9 GUT.
- **PR #159** UnitSelectionState bus + UnitInfoPanelAdapter (caller-wire #2) — bus single source truth, selection_changed signal idempotent, get_selected_data copy defensive. Adapter listen → bind_unit/clear. 14 GUT (7+7).
- **PR #160** ForecastPanelAdapter (caller-wire #3) — listen forecast_updated payload → ForecastPanel.set_forecast + opt-in clear_on_signal hook (auto-clear post action_resolved). 9 GUT.
- **PR #161** BoardOverlayAdapter (caller-wire #4) — listen overlay_requested(cells: Array[Dict]) → batch clear_all + set_overlay per cella. Unknown modes silently ignored (ritual locked). 9 GUT.
- **PR #162** Caller integration #5 (FINAL wire) — Unit.clicked signal LMB-only emit + Main bus instantiate + Unit factory loop wires u.clicked.connect → bus.select + dead unit clears bus + ESC clears bus + HudView.attach_combat_panels(bus, orchestrator) idempotent + UnitInfoPanel + BattleFeed mounted in HudView.tscn (anchor preset 9 left + 11 right). +200 LOC, ~16 GUT (4 unit_clicked + 7 hud_combat_panels + 5 main_selection_bus_wire).

Caller-wire pipeline LIVE end-to-end: 2/4 adapters wired in HudView (UnitInfoPanel + BattleFeed). ForecastPanel + BoardOverlay components esistono ma DEFERRED — no emitter source (richiede sprint dedicato d20 forecast computation + move/attack range query).

GUT post-#162: ~1455/1455 (~3400+ asserts). Sessione 2026-05-04 second wave totale: 23 PR mergiati (cleanup 2 + chip 9 + Ferrospora 5 + docs sync 1 + caller-wire components 4 + caller integration 1 + lint inline 3).

**Risultato visibile gioco** (verificabile con `godot run scenes/Main.tscn`):
- Click XCOM sticky su Unit → UnitInfoPanel mostra HP/CT/traits/status
- Click altra Unit → switch selezione + re-bind panel
- ESC → clear selezione + cancel targeting mode
- Unit muore mentre selezionata → auto-clear panel
- Combat azione (attack/defend/move) → BattleFeed entry "actor → target: RESULT (N HP)" con severity tint

**Master-dd checkpoint pendenti post caller-wire end-to-end**:
1. Sprint A Beehave authoring (A1-b 9 trees code-first narrative random-spawn) — ~3-5 PR
2. Sprint C AI loaders caller-wire C1-b per-encounter — ~2 PR (encounter YAML schema extension `ai_profile_pool` + spawner random pick + SisPolicy threshold override + UtilityBrain weights)
3. Forecast/BoardOverlay emitter source — sprint dedicato (d20 forecast + range query)
4. Asset W7 designer sprint (Wildermyth portraits + sprite art Skiv biome variants + audio cues)
5. Cloudflare prod deploy (named tunnel + DNS records)

**Sessione 2026-05-04 Sprint A + Sprint C coordinated bundle** (PR #164 single feature branch with 5 sequential commits, OPEN for review):

Sprint priorità 2+3 closure pure-code. Master-dd 2026-05-04 design decisions (A1-b 9 personalità / A2-a code-first / A3-b narrative naming / A4-b random spawn / C1-b per-encounter pool) eseguite end-to-end senza scene-tree dependency.

**Architectural choice**: pure RefCounted `TacticalNode` decision tree mirrors Beehave SUCCESS/FAILURE/RUNNING semantics WITHOUT requiring Beehave plugin scene-tree binding. Plugin Beehave installed (Sprint M.1) but reserved as future swap point — pure-code factories deterministic + offline-testable + no autoload dependency. If master-dd later requires real Beehave nodes (visual debug overlay), factory output can be re-wrapped.

Branch `sprint-a-c-coordinated`, PR #164 (5 commits):

**Sprint A — Beehave personality factories** (3 commits):
- **Sprint A.1**: PersonalityTreeFactory abstract + 3 personality factories (aggressive 0.15 panic + range 2 charge / cautious 0.45 panic + counter melee 1 + hold default / opportunist 0.30 panic + protect ally + flank). 8 narrative-named leaves: panic_when_wounded / enemy_in_attack_range / ally_under_threat / seek_weakest_target / flee_to_cover / protect_ally_under_threat / hold_position_under_fire / coordinate_flank. Composites: SequenceNode (fail-fast) + SelectorNode (succeed-fast). Reuses SisPolicy.step_toward/step_away. +33 GUT (test_tactical_node 8 + test_tactical_leaves 15 + test_personality_factories 10).
- **Sprint A.2**: 3 role overlays (skirmisher kite_after_strike HP>0.5 + adjacent → flee / tank stoic_guard HP>0.7 + ally<0.6 → protect / support screen_for_squishies ally<0.4 → protect). New leaf HpAbove (PanicWhenWounded inverse). BeehavePersonalityRegistry combiner: list_profile_ids() → 9 canonical, build(profile_id) → tree (null on unknown), parse_profile_id() greedy personality prefix. +18 GUT (test_role_overlays 8 + test_beehave_personality_registry 10) — all 9 build combinations verified.
- **Sprint A.3**: BeehaveRandomPicker — pick_from_pool(rng) raw + pick_valid_from_pool(rng) registry-filtered + sample_distribution diagnostic. Replay-stable with seeded RandomNumberGenerator. +10 GUT (empty/null/single/deterministic-seed/filter/all-unknown/distribution/replay-stable/integration-with-registry).

**Sprint C — Caller wire** (2 commits):
- **Sprint C.1**: EncounterDefinition.list_ai_profile_pool() → Array[String]. ETL untouched (verbatim YAML→JSON pass-through). Defensive coercion via str() (Godot 4 strict-typed Array iteration: String() constructor errors on String input — bug found+fixed during dev). +5 GUT back-compat (absent / array / waves schema / invalid type / mixed types).
- **Sprint C.2**: ReinforcementSpawner.set_profile_pool(pool, rng) — when group ai_profile is empty, picks via BeehaveRandomPicker.pick_valid_from_pool. Legacy per-group ai_profile preserved (back-compat). Unit.ai_profile_id @export field, setup() reads spec.ai_profile or spec.ai_profile_id. EncounterRuntime.setup forwards encounter pool with seed = hash(encounter_id) for replay stability. Main._instantiate_reinforcement propagates ai_profile through Unit.setup. +9 GUT (test_reinforcement_spawner_pool 5 + test_unit_ai_profile_id 3 + 1 helper).

**Test totale**: +75 GUT new tests. Full suite **1553/1553 pass** (3447 asserts) — zero regression across 159 scripts.

**gdformat + gdlint clean** all sprint files (50-line guardrail respected per file, max-public-methods=20).

**Constraint check coordinated bundle**:
- NO RoundOrchestrator modify (zero touch)
- NO HudView signal contract change
- NO Beehave plugin actor binding (pure RefCounted offline-testable)
- Cross-repo Game/ untouched (canonical YAML can adopt ai_profile_pool field incrementally with zero Godot v2 deploy)
- Encounter back-compat: 14 existing encounters unchanged → empty pool → SisPolicy archetype path preserved

**Wire chain end-to-end**:
encounter YAML `ai_profile_pool: [...]` → ETL passthrough → EncounterDefinition.list_ai_profile_pool() → EncounterRuntime.setup() → ReinforcementSpawner.set_profile_pool() → spawn-time random pick → spec.ai_profile → Unit.setup → Unit.ai_profile_id → (future caller PR) BeehavePersonalityRegistry.build → tree.tick → ActionIntent.

**Pure-code rimanente zero**. Beehave tree dispatch into SistemaIntents action resolution (replace SisPolicy when ai_profile_id non-empty) deferred per master-dd review post-merge — that wire requires direzione su ActionIntent → CombatSession dispatch shim.

**Master-dd checkpoint pendenti post Sprint A+C bundle**:
1. Review/merge PR #164 (or split into 5 separate PR if preferred — requires branch rework)
2. Beehave tree → SistemaIntents wire decision (parallel-run with SisPolicy / sunset SisPolicy / Beehave-only when profile_id set) — **PARTIAL PROCEEDED** with default [A]+[X]+[P] (parallel-run, dispatcher facade, IntentToAction shim) shipped come Sprint AC.4+AC.5 in PR #164
3. Forecast/BoardOverlay emitter source sprint invariato
4. Asset W7 designer sprint invariato
5. Cloudflare prod deploy invariato

**Sprint AC.4+AC.5 dispatch wire** (master-dd 2026-05-04 default proceed [A]+[X]+[P], pushed nello stesso PR #164 sequential commit `3d7aa21`):

Pure-code parallel-run dispatch facade — RoundOrchestrator zero-touch, SisPolicy preserved come fallback. Choice rationale:
- **[A] dispatcher facade NOT inject** — instead of patching RoundOrchestrator, ship `SistemaAiDispatcher.next_action_for(actor, allies, enemies, grid_size)` standalone. Caller (Main combat phase) invokes externally → returns RoundOrchestrator-compatible action dict. Inversione di controllo: orchestrator stays generic, AI logic isolated.
- **[X] parallel-run** — dispatcher branches: profile_id non-empty + canonical → Beehave tree; else (or unknown profile) → SisPolicy fallback. Both paths normalized through IntentToAction.translate. Back-compat permanente.
- **[P] IntentToAction shim** — pure RefCounted translator. 7 kind→action_type mappings: attack/approach/retreat/defend/defend_ally/idle/<unknown>. Preserves TacticalNode offline-testability.

Files Sprint AC.4+AC.5:
- `scripts/ai/intent_to_action.gd` — translator helper
- `scripts/ai/sistema_ai_dispatcher.gd` — facade with Beehave + SisPolicy fallback
- `tests/unit/test_intent_to_action.gd` — 9 tests (5 mappings + edge cases)
- `tests/unit/test_sistema_ai_dispatcher.gd` — 7 tests (empty / fallback / Beehave / unknown profile defensive)
- `tests/unit/test_beehave_dispatch_e2e.gd` — 4 tests (encounter pool → spawner → dispatcher → RoundOrchestrator → HP delta observed; legacy fallback path; end-turn safe; unknown profile defensive)

Wire chain LIVE end-to-end (verified by test_encounter_pool_drives_sistema_attack_resolution): encounter ai_profile_pool: ["aggressive_skirmisher", "aggressive_tank"] → ETL → list_ai_profile_pool → ReinforcementSpawner.set_profile_pool seed=12345 → BeehaveRandomPicker → spec.ai_profile → CombatSession.add_unit preserves field → SistemaAiDispatcher → BeehavePersonalityRegistry.build → TacticalNode.tick → IntentToAction → AttackAction → CombatSession.resolve_attack_action → PG HP 10 → 4 (damage 6 with fixed_d20=20).

GUT regression full suite **1573/1573 pass** (3483 asserts, 162 scripts, 36s). Zero regression.

PR #164 final state: 6 sequential commits (Sprint A.1+A.2+A.3+C.1+C.2+AC.4+AC.5). +95 GUT new tests cumulative. Master-dd next: **review/merge PR #164** + decide caller wire site in Main combat phase (currently dispatcher uncalled — Main combat flow lacks SISTEMA turn tick, parallel-run safe to land first then add caller).

Resume trigger update: caller-wire pipeline LIVE component-level (UnitInfoPanel + BattleFeed); AI dispatch pipeline LIVE module-level (dispatcher + shim + e2e); Main caller integration (per-turn invoke) **deferred** pending master-dd direzione su SISTEMA turn site.

**Sessione 2026-05-05 autonoma extension Sprint AC.6-18** (15 sub-sprint shipped post-Sprint A+C #164, master-dd "procedi continua autonomia" mode):

| PR | Sprint | Topic | GUT |
|----|--------|-------|----:|
| #171 | AC.6 (empty squash bug) | caller wire empty merge | n/a |
| #172 | AC.6+7 RECOVERY | Main.try_dispatch + advance_sistema_phase + SistemaPhaseRunner extraction | +12 |
| #173 | AC.8 | ForecastService + RangeQuery + CombatEmitter | +25 |
| #174 | AC.9 | CombatEmitter caller wire Main combat phase | +5 |
| #175 | AC.10 | HudView mount ForecastPanel + BoardOverlay (UI visible) | +8 |
| #176 | AC.11 | ForecastService status_odds via TraitCatalog | +5 |
| #178 | AC.12 | auto-advance SISTEMA phase post PG EndTurn (opt-in flag) | +8 |
| #179 | AC.13 | codex bundle 7 findings (#172/#174/#175/#176) | +9 |
| #180 | AC.14 | AI loaders override consumption (dispatch-time, SisPolicy path) | +6 |
| #181 | AC.15 | Beehave factory parameterization (override injection) | +7 |
| #182 | AC.16 | multi-trait status_odds probabilistic union | +3 |
| #183 | AC.17 | AiPersonalityLoader intent_weights helpers | +8 |
| #184 | AC.18 | codex bundle 2 P2 findings (#182/#183) | +4 (3 updated) |

**Pipeline AI dispatch + Forecast/Overlay LIVE end-to-end visible in-game**:

```
encounter ai_profile_pool → ETL → spawner pool pick + ai_profile_id Unit field
  → SistemaAiDispatcher.next_action_for (resolves overrides via _resolve_profile_overrides)
      ├─ Beehave: BeehavePersonalityRegistry.build(profile_id, overrides) → factory.build_tree(overrides)
      │   → tree.tick(blackboard) → ActionIntent
      └─ SisPolicy fallback: select_action(actor, target, grid, overrides)
      → IntentToAction.translate (7 kind→action mappings)
  → RoundOrchestrator.resolve_action → CombatSession.resolve_attack_action

[Forecast/Overlay UX]
PG attack-target click → CombatEmitter.emit_attack_range + emit_forecast
  → BoardOverlay (Node2D layer) renders attack-range cells
  → ForecastPanel (HudView) shows hit% + damage band + status_odds
PG action_resolved → clear_overlay + ForecastPanel.visible=false
PG EndTurnAction (opt-in flag) → advance_sistema_phase XCOM-style enemy turn

[Auto-trigger SISTEMA phase]
Main.auto_advance_sistema_after_pg_turn @export bool default false
  → on PG turn_ended event: SistemaPhaseRunner.maybe_auto_advance_after_pg_turn
  → faction filter rejects SISTEMA (no cascade)

[Status odds split aggregation]
ForecastService deterministic min_mos=0 traits → max() (same hit event)
gated min_mos>0 traits → union P=1-prod(1-P_i) (independent events)
combined det+gated → final union (independent paths)
```

**GUT main HEAD `3ada773` post-AC.18**: **1719/1719 pass** (3786 asserts, 178 scripts).

**Architectural extractions** (max-file-lines guardrail):
- `scripts/session/sistema_phase_runner.gd` — SISTEMA dispatch + phase loop + auto-advance helper (AC.6+7+12)
- `scripts/session/combat_emitter_caller.gd` — emitter forwarding helpers (AC.9+10)
- `scripts/combat/forecast_service.gd` — d20 forecast + status_odds (AC.8+11+16+18)
- `scripts/combat/range_query.gd` — Manhattan reachable cells (AC.8 + W+H per AC.13)
- `scripts/ui/combat_emitter.gd` — forecast_updated + overlay_requested signal Node (AC.8)

**Override consumption complete** (mirror SisPolicy + Beehave):
- AiProfilesLoader.load_profile.overrides → SisPolicy.select_action thresholds (AC.14)
- AiProfilesLoader.load_profile.overrides → Beehave factory.build_tree params (AC.15)
- AiPersonalityLoader.intent_weights_for / intent_weight helpers (AC.17, AC.18 bare-id fix)
- Resolution: profile_id direct → personality-prefix fallback (aggressive_skirmisher → aggressive)

**Codex review lifetime sessione AC.6-18**:
- AC.13 fixed 7 findings (2 P1 + 5 P2): SistemaPhaseRunner winner-stop, GRID_H clamp, exit_targeting clear, ForecastService context propagation + min_mos
- AC.18 fixed 2 P2 findings: det vs gated split aggregation, bare personality id prefix fallback
- 9 codex findings closed total

**Master-dd checkpoint pendenti post-AC.18**:
1. Asset W7 designer sprint (Wildermyth portraits + sprite art) — external commission
2. Cloudflare prod deploy (named tunnel + DNS records) — manual ops
3. UtilityBrain caller wire dispatcher (action enumeration upgrade required)
4. CLAUDE.md sprint context resume trigger sync (this file = current source-of-truth)

**Pure-code rimanenti zero** — all autonomous-shippable items closed end-to-end. Future sprints require master-dd design call OR external asset commission OR architectural redesign.
