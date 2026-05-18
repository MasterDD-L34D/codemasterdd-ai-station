# Evo-Tactics — Design Digest (ispirazioni, stile, contenuti)

> Companion di [EVO_TACTICS_ECOSYSTEM_GUIDE.md](EVO_TACTICS_ECOSYSTEM_GUIDE.md).
> Split 2026-05-18 (harsh-review #13). La **GUIDE** = mappa 7-repo + front-matter
> condiviso (Autorita' / Stato / Glossario / Numeri canonici). Questo **DIGEST**
> = ispirazioni design + stile distillato + sistema design/contenuti.
> Autorita', glossario sigle, privacy/stato: vedi GUIDE front-matter (canonico,
> non duplicato qui). Repo daily-ship: ri-verifica `gh` prima azioni puntuali.

---

## 11. Ispirazioni, Fonti & Stato Design (catalogo completo)

> Ricostruzione 2026-05-18 da audit cross-source esaustivo (6 explore agent,
> Protocol 2 autoresearch): lettura di TUTTE le ~45 museum card + grep vault
> completo. Documento unico e completo -- non sommario. Le decisioni di design
> vivono in due layer indipendenti che si corroborano:
>
> - **(A) Game museum cards** -- `Game/docs/museum/cards/` (Dublin Core,
>   alternative + ROI + reuse path, ~45 card, indice `docs/museum/MUSEUM.md`)
> - **(B) vault pillars** -- `vault/Spaces/Dev/Evo-Tactics/core/` (design
>   narrative + ricerca; vedi front-matter "Autorita'": canonical
>   runtime/scope = Game A0-A3, vault = A5/shadow reference)
>
> Weighting: internal>external, empirical>doc, multi-source-converge >
> single-signal. Dove un'ispirazione appare in entrambi i layer = alta
> confidenza. Autorita' in caso di divergenza: vault `core/` (freeze A3)
> vince per scope shipping; museum = catalogo alternative + ROI.

### 11.1 I 6 pilastri di design <-> ispirazione ancora

Ogni pilastro (vault `core/02-PILASTRI.md`) e' ancorato a un'ispirazione
precisa. Stato pilastri 2026-04-20: 0/6 verde, 6/6 giallo (revisione onesta
post-playtest M1; pre-playtest era 5/6 verde -- NON regressione, realta'
testata).

| Pilastro | Nome | Ispirazione ancora | Stato |
|----------|------|--------------------|-------|
| P1 | Tattica leggibile | **Final Fantasy Tactics** + Into the Breach | 🟡 d20+MoS funziona, notazione AP ambigua (friction #1-2) |
| P2 | Evoluzione emergente | **Spore** (concetto) via Wesnoth + AI War (meccanica) | 🟡 mating non testato M1, persistence M10, runtime M12+ |
| P3 | Identita Specie x Job | FFT job cross-inheritance | 🟡 specie differenziate, job ability costs unclear (friction #4) |
| P4 | Temperamenti giocati | **Disco Elysium** (reveal diegetico MBTI/Ennea) | 🟡 VC tracking off in M1, solo T_F full |
| P5 | Co-op vs Sistema | **AI War** + NS2 Strategist + Frozen Synapse | 🟡 focus-fire live, "Sistema troppo passivo" |
| P6 | Fairness | Hades Heat + Monster Train Pact + AI War Progress | 🟡 d20 trasparente, scaling curves canonical |

### 11.2 Catalogo completo ispirazioni positive

Legenda stato: **SHIPPED** = implementato | **IN-DESIGN** = deciso/ADR ma
non shippato | **DEFERRED** = post-playtest/post-EA | **MUSEUM** = curated,
preservato ma non shippato (alternativa o forgotten).

#### A. Pillar-tier / architetturale (ancore dei pilastri)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte (file) | Stato |
|-----------------|-----------------|------------------------|--------------|-------|
| **Final Fantasy Tactics** (1997) | CT bar charge-time, Wait action, facing crit (rear+50%/side+25%), JP cross-job inheritance | Adotta legibilita' temporale (init + action_speed + wait) RIFIUTA crit Zodiac opaco. Wait shipped PR#1896. CT bar+facing 3-zone ~8h. JP cross-job M14+ | museum `combat-fft-ct-bar-wait-facing-crit.md` (4/5); vault `core/02-PILASTRI.md`,`10-SISTEMA_TATTICO.md` | SHIPPED (wait) + DEFERRED (CT/facing) |
| **Spore** (2008) | Part-pack assembly, ability auto-derivata da parti, mutazione morfologica runtime | RIFIUTA sandbox real-time; 6-pattern stack: slot morfologia, ability auto-derive, DNA budget, visual swap obbligatorio, ereditarieta' generazionale, part-bingo. Path moderato ~21h chiude P2 | museum `spore-part-pack-runtime-stack.md` (5/5); vault `core/20-SPECIE_E_PARTI.md`,`00-SOURCE-OF-TRUTH.md` §20 | IN-DESIGN (engine mating shipped, runtime M12+) |
| **Disco Elysium** (2019) | Thought Cabinet slots, voce interna 4-MBTI assi, skill-check passive->active popup, reveal diegetico MBTI color-coded | MBTI tag debrief shipped PR#1897. Thought Cabinet UI ~8h (P0 residuo). Voce interna ~10h. "Fonte calore" per P4 (pilastro piu' freddo) | museum `narrative-disco-thought-cabinet-diegetic.md` (5/5); vault `core/02-PILASTRI.md` P4 | SHIPPED (MBTI debrief) + DEFERRED (Cabinet/voce) |
| **AI War** (2009) | Antagonista data-driven persistente (Sistema), pack-unlock progression (no power-creep grind), progress meter chosen-escalation, multi-profile narrative voice | Pattern A Sistema-centric Fase 1. aiProgressMeter.js shipped #1898. `ai_profiles.yaml` narrative_voice per tier. 4-8 player co-op vs AI | vault `core/00F-ART_AUDIO_BUSINESS.md` §4.1,`00-SOURCE-OF-TRUTH.md`; museum `economy-hades-multi-currency-pact-menu.md` §convergenza | SHIPPED (progress meter, Fase 1) + IN-DESIGN (co-op net M11) |
| **Into the Breach** (2018) | Telegraph rule (tutto visibile pre-commit), push/pull arrows, kill-probability badge, zero RNG nascosto | "Sacrifice cool for clarity, every time". Threat tile overlay shipped PR#1884. Push/pull+kill badge ~3h. Determinismo = zero RNG post-decisione. Hand-curate maps ~10h | museum `ui-itb-telegraph-deterministic.md` (4/5); vault `core/41-ART-DIRECTION.md` | SHIPPED (threat overlay) + DEFERRED (arrows/badge) |
| **Hades** (2020) | Multi-currency split (PE-run vs Shards-meta), Pact menu opt-in difficulty, Codex tematico, gradual reveal | 3-currency split (PE-run/Shards-meta/PI-pack) ~6h. Pact Shards 0-5 ~5h. Cap a 3 currency (Hades 7 = overkill). Codex panel ~20h | museum `economy-hades-multi-currency-pact-menu.md` (5/5) | DEFERRED (post-playtest) |
| **Monster Train** (2020) | Pact Shards opt-in scaling componibile (modifier additivo, NON preset monolitico) | Pact Shards opt-in N-tier, reward tradeoff trasparente. Convergenza 4-source (Hades+MonsterTrain+AIWar+XCOM LW2) | museum `economy-hades-multi-currency-pact-menu.md` (5/5, row Monster Train) | DEFERRED (post-playtest) |
| **Tactics Ogre: Reborn** (2022) | HP floating bar sopra sprite, charm/recruit boss via dialogue, auto-battle button, class-change altare, WORLD rewind | HUD canonical: HP floating refactor ~5-7h, AP pip shipped PR#1901, charm recruit ~8h, auto-battle ~3h | museum `combat-tactics-ogre-hp-floating-charm.md` (5/5); vault `core/44-HUD-LAYOUT-REFERENCES.md` | SHIPPED (HP/AP) + DEFERRED (charm/auto/WORLD) |

#### B. Creature & narrativa (museum cards)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte | Stato |
|-----------------|-----------------|------------------------|-------|-------|
| **Wildermyth** (2021) | Battle-scar permanent (cicatrice=sprite change), ritratto stratificato, aging cross-session, choice->flag permanente, narrativa storylet | battle-scar registry ~12h, portrait layered ~15h, aging ~10h, choice flag ~4h. Convergenza 3-source (Wildermyth+SporeS4+VoidlingP6) | museum `creature-wildermyth-battle-scar-portrait.md` (4/5); vault `core/41-ART-DIRECTION.md` | IN-DESIGN (silhouette-per-specie canonical) |
| **Triangle Strategy** (2022) | MBTI Transfer Plan: 3 proposte concrete P4-closure -- (A) phased reveal Disco-style, (B) dialogue color codes diegetic, (C) recruit gating by MBTI threshold | 3 proposte mai citate in BACKLOG/OD = dimenticate. Map: vcScoring.js + formSessionStore.js + mbti_forms.yaml. **Solo museum, NON vault** | museum `personality-triangle-strategy-transfer.md` (M-2026-04-25-009, 5/5) | MUSEUM (FORGOTTEN, 5/5 high-ROI) |

#### C. Combat & UI quick-win (museum cards)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte | Stato |
|-----------------|-----------------|------------------------|-------|-------|
| **Cogmind** (2015) | Tooltip stratificati base+expand-on-hover, trade-off espliciti per componente | trait cost_ap -> multi-cost ~4-6h. Gold standard "identita = equip + trade-off espliciti" (P2+P3) | museum `ui-cogmind-tooltip-stratificati-quick-win.md` (4/5) | MUSEUM (quick-win ready) |

#### D. Indie research cluster (museum M-2026-04-27-019..031)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte | Stato |
|-----------------|-----------------|------------------------|-------|-------|
| **The Banner Saga** (2014) | Caravan supply attrition cross-mission ("3 giorni cibo, 47 bocche") + permadeath autentico opt-in | campaignResourceTracker.js ~6h minimal. Permadeath party.yaml preset ~4h | museum `indie-banner-saga-caravan-attrition.md` + `indie-banner-saga-permadeath-optin.md` (4/5) | DEFERRED (post-playtest) |
| **Cobalt Core** (2023) | Position-conditional ability bonus (posizione = prerequisito ability) | abilityExecutor.js position_condition tag -> +2 se flanking. Ripple ~15h post-Bundle A | museum `indie-cobalt-core-position-bonus.md` (4/5) | DEFERRED (post-Bundle A) |
| **Backpack Hero** (2023) | Spatial inventory adjacency (Tetris-griglia, posizione crea bonus) | 2+ trait stesso organ_system -> bonus passivo. form_pack_bias.yaml live, layer post-S6 | museum `indie-backpack-hero-spatial-inventory.md` (3/5) | DEFERRED (post-S6) |
| **Astrea: Six-Sided Oracles** (2023) | Dadi contaminati/puri = character sheet visibile (pool dadi tangibile) | VC axes come dadi facce contaminate/pure. Defer fino OD-013 MBTI surface verdict | museum `indie-astrea-dice-purification.md` (3/5) | DEFERRED (OD-013) |
| **Citizen Sleeper** (2022) | Fatigue drift cross-encounter (corpo si degrada -> modifica VC axis) | fatigue accumulator store + ink rest events. Post-Bundle C | museum `indie-citizen-sleeper-fatigue-drift.md` (3/5) | DEFERRED (post-Bundle C) |
| **Slay the Princess** (2023) | 12-knot branching state memory ("il gioco sa come ho giocato") | narrativeRoutes.js debrief knot per mbti_group. Writer D4 bottleneck (55 ink unit, 8h) | museum `indie-slay-princess-branching-state.md` (3/5) | DEFERRED (D4 writer) |
| **Pentiment** (2022) | Job voice + confessionals (job player colora comunicazione) | job-variant briefing ink (35+ stitch x 7 job). Writer D4 bottleneck | museum `indie-pentiment-job-voice-confessionals.md` (3/5) | DEFERRED (D4 writer) |
| **Inscryption** (2021) | Camera reveal meta-frame escalating (Sistema rivela dati progressive come "dossier intercettato") | objectiveEvaluator.js esposto post-MVP. TKT-09 prereq. Dossier tracker 3-consecutive | museum `indie-inscryption-camera-reveal-meta.md` (2/5) | DEFERRED (post-MVP) |
| **1000xRESIST** (2024) | Memory layered POV (briefing cita "volta scorsa Sistema ha usato fianco destro") | previousBiomeLoss store + conditional ink knot ~5h. Post-Bundle B | museum `indie-1000xresist-memory-layered-pov.md` (3/5) | DEFERRED (post-Bundle B) |
| **Loop Hero** (2021) | Minimap campaign visual emergence (hex 5x5 illumina post-scenario, grigio = attesa) | briefing hex_revealed array 1-3/scenario. Decisione D5 pending (diegetic vs HUD) ~6-9h | museum `indie-loop-hero-minimap-visual-emergence.md` (3/5) | DEFERRED (D5) |
| **Cocoon** (2023) | Biome rules layer (1-2 regole tattiche uniche/bioma, combinano in transition) | biome_rules.yaml ext, biomeSpawnBias rework ~7h post-P3 | museum `indie-cocoon-biome-rules-layer.md` (3/5) | DEFERRED (post-P3) |
| **Tunic** (2022) | Manual-as-puzzle diegetic knowledge (codex sbloccabile, lingua gliffica deduci) | subset decipher Codex ADOPT ~5h. Broader scope post-MVP UX | museum `indie-tunic-manual-puzzle-broader.md` (2/5) | DEFERRED / partial ADOPT |

#### E. Core/GDD narrative & system tier (vault canonical)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte | Stato |
|-----------------|-----------------|------------------------|-------|-------|
| **Wesnoth** (GPL) | Campaign dialogue inline, leader named = unita giocabile, `{QUANTITY}` scaling (Easy 0.7x/Norm 1.0x/Hard 1.3x). **Validatore pattern P2** (evoluzione = advancement tree, NON sim) | Pattern citato (no code-clone) per campaign + difficulty scaling Fase 2 | vault `00-SOURCE-OF-TRUTH.md` §15.4-15.5; `00F` §4.4 | Research-validated, narrative Fase 2 |
| **Descent: Road to Legend** (FFG board) | Overlord plot-card rhythm, struttura campagna multi-hero, quest branching win/loss, campaign book + "dadi Descent-like" su spese PT/PP | Pattern B "Overlord + Custodi named" Fase 2 post-EA: `data/core/custodi.yaml` + campaign book. Dice metaphor TV in `11-REGOLE_D20_TV.md` | vault `core/00F-ART_AUDIO_BUSINESS.md` §4.3-4.4; `core/11-REGOLE_D20_TV.md` | DEFERRED (narrative Fase 2) + SHIPPED (dice metaphor) |
| **Fire Emblem** | Square grid tactics, positioning depth (ref comparativo scelta grid) | Hex preferito su square (ADR-2026-04-16), pattern FE noto | vault `00-SOURCE-OF-TRUTH.md` §14.1 | Design-known |
| **AncientBeast** (GPL) | Hex 16x9 grid, multi-tile creature, coord axial/cube, pathfinding+FOV/LOS | **DECISO**: hex axial adottato | vault `00-SOURCE-OF-TRUTH.md` §14.1-14.3; **ADR-2026-04-16-grid-type-hex-axial** | IN-DESIGN (ADR DECIDED) |
| **Don't Starve** | Silhouette forte + palette limitata (16-24 col/biome), creature iconiche | Silhouette language (P3 job-to-shape), 32x32 sprite, indexed PNG | vault `41-ART-DIRECTION.md` §Implementazione | IN-DESIGN (art-direction APPROVED) |
| **Slay the Spire** (2017) | Mood UI scuro TV-first, intent preview info-on-entity, loop economici scarsita'-driven | Mood canonical post ADR-2026-04-18. Economia non-gacha. Convergenza UI Telegraph | vault `core/41-ART-DIRECTION.md`; Game `docs/planning/2026-04-20-design-audit-consolidated.md` | IN-DESIGN (art-direction decisa) |
| **Wargroove** (2019) | Pixel-art moderno (no 8-bit, no 3D), clarity combat, palette vivida | Pixel-art ortho, palette matrix 9 biomi x 4-color, Aseprite pipeline. Reference moodboard ufficiale | vault `core/41-ART-DIRECTION.md`,`00F` §2.4 | IN-DESIGN (reference, no ADR esplicito) |
| **OpenRA** (GPL) | Mission briefing + campaign scripting Lua, objective narrativi | encounter YAML schema `narrative.briefing_ink` field | vault `00-SOURCE-OF-TRUTH.md` §15.2; `00F` §4.4 | Schema-integrated |
| **FFT: War of the Lions** (2007) | Named companion dialogue + generic recruit, acted scenes, isometric legibility | Fase 2: 2-4 Custodi named + generic "Wolf-03" slot. Campaign arc intro->acts->climax | vault `00F` §4.4; `00-SOURCE-OF-TRUTH.md` audience | DEFERRED (narrative Fase 2) |
| **Ink / inkle** (engine) | Multi-speaker knot dialogue, branching variable state | narrativeEngine.js (inkjs) + ai_profiles.yaml narrative_voice | vault `00F` §4.2,§4.4 | **IMPLEMENTED** (Fase 1 minimal) |
| **80 Days / Sorcery** (inkle) | Gold standard Ink multi-speaker, no-VO emphasis | Validazione pattern Ink (creature silent, Sistema narra) | vault `00F` §4.4 | Reference-validated |

> **Nota d20/TTRPG**: il progetto usa la regola d20 + Margin-of-Success
> (ADR-2026-04-13) senza accreditare Pathfinder/D&D 5e per nome. Ispirazione
> meccanica, non sistema citato.

### 11.3 Pattern di convergenza (multi-source = principio hard)

Dove >=3 fonti indipendenti convergono = principio di design non negoziabile:

1. **UI Telegraph** (7-source: Slay the Spire + ITB + Tactics Ogre + FFT CT bar
   + Cogmind + Battle Brothers ATB + Halfway) -> "info attaccata all'entita',
   mai nascosta". Hybrid overlay (Tactics Ogre base + Dead Space tint additivo).
2. **Cambio visibile permanente** (3-source: Wildermyth + Spore S4 + Voidling
   Pattern 6) -> ogni cambio meccanico significativo HA conseguenza visiva (P3+P4).
3. **Difficolta' opt-in componibile** (4-source: Hades Heat + Monster Train Pact
   + AI War Progress + XCOM Long War 2) -> scaling player-controlled, NON preset (P6).
4. **Visibilita' co-op** (3-source: Frozen Synapse replay + ITB telegraph + NS2
   Strategist atlas) -> reveal simultaneo post-decisione = sblocco planning (P5).

### 11.4 Anti-reference (cosa NON vogliamo essere)

Fonte: vault `41-ART-DIRECTION.md` §Direzione sintetica + `00F-ART_AUDIO_BUSINESS.md`
§1.2,§4.5. Decisioni esplicite di rifiuto:

| Anti-reference | Perche' rifiutato |
|----------------|-------------------|
| Disney cartoon | No cute -- creature bio-plausibili, body-horror trait |
| Pokemon-style cute | Incompatibile PEGI 16 + creature mature |
| Full-3D realistico | Budget indie, TV pixel clarity > fidelity |
| Anime shonen | Taglio adulto, no narrativa serializzata |
| Military sci-fi polished | Contro tono bio-plausibile + autonomia creature |
| Descent puro (Heroes fissi) | Named heroes contraddicono creature modulari (creature != player) |
| Pattern C (Player-named Commander) | Ownership si ma caratterizzazione generica, anchor narrativo debole |
| Pattern D (Ramza-light FFT single-POV) | Single protagonist contraddice co-op ownership, costo lineare alto |

### 11.5 Museum -- alternative scartate/parcheggiate preservate

Game `docs/museum/` (museum-first protocol): ~101 artifact, ~45 curator card
Dublin Core (31 con citazione gioco esterno, 14 worldgen/genetics interni),
3 gallerie, 9 inventory. Indice: `docs/museum/MUSEUM.md`.

| Card | Cos'era | Perche' scartato/parcheggiato |
|------|---------|-------------------------------|
| Promotions-orphan (3/5) | Job rank advancement (JP inheritance FFT) | Complessita' FFT-specifica, scope creep. JP cross-job deferred M14+ |
| MBTI Gates Ghost (4/5) | Modal unlock gate MBTI early | Opaco -> sostituito da Disco color-coded debrief. Recuperabile via git |
| Magnetic Rift Resonance (4/5) | Swarm trait T2 biome-resonance oscillator | Simulazione real-time troppo costosa -> trait cost + biome memory |
| Sentience Tiers v1.0 (5/5) | Interocezione T0-T6 + 22 Self-Control trigger | Non integrato ma high-ROI. Skiv Sprint C unblock (290/297 trait live) |
| Worldgen 4-level stack (5/5) | Bioma->Ecosistema->Foodweb->Network | Infra completa MA zero runtime consumption. Revive ~3-6h quick win |
| Enneagramma Registry (5/5) | 16 hook stub Ennea effect injection | Non integrato, ready-to-wire. 93 LOC orphan ~3h |
| Voidling Bound 6 Patterns (4/5) | Genetics: rarity-gate, path-lock, Apex terminal, visual_swap | Pattern 6 (visual swap) non integrato, P0 gap |
| Triangle Strategy Transfer (5/5) | 3 proposte P4-closure A/B/C | Dimenticato, mai in BACKLOG/OD. Cross-validate quando Thought Cabinet wiring |
| Mating Engine D1+D2 (5/5) | 1053 LOC engine + 7 REST, zero frontend | **REVIVED 2026-04-27**: PR#1876/1879/1911 shipped. OD-001 era disinfo |

### 11.6 Asset provenance: creature(Skiv)/biomi/audio refs

> Dedup (#5): direzione visiva canonica (stile target, 3 modi visivi,
> palette/token, audio identity, a11y) vive in **12.1** -- non duplicata
> qui. Questa sezione = SOLO provenance/refs asset (cosa scaricato, da
> dove, licenza). Token/identita' -> 12.1.

**Archetipo Skiv -- asset refs** (`evo-tactics-refs-meta/SKIV_REFS_EXTRACTED.md`).
NB: "Skiv" = archetipo/shorthand player-facing, NON specie letterale (vedi
12.1 naming); qui = label sotto cui sono organizzati i ref asset:
- 3D anatomia: Quaternius Animal Pack Vol.2 Wolf + Red Fox (CC0, rig posing),
  wolf-skiv-ref (Blender rigged + 3dwolf FBX PBR color/normal/rough/spec)
- 2D sprite: HF OGA-CC0 Desert Kit Wild Animals (Fox/Wolf 36-40px, Wolf Howl
  16fr = "calling pack" diretto per lore Skiv), DENZI cat 32x32 (12 variant)
- Concept: Surt CC0 pack 175+ file (100 color + 26 doodle + silhouette_pack +
  monster concept), HF "creature and cub sketch" 21MB PNG+PSD (anatomia +
  relazione madre/cucciolo), Kenney Monster Builder, PhyloPic 581 SVG
- Skiv design = **lavoro originale** ground su questi ref, no artista attribuito

**Biomi**: Africa Savanna Pack v1.0 493 file DAE (habitat Skiv, scale creature
vs env, sun-angle warm), CAVE_PACK_PRO 272 file (burrow secondario), 3D Nature
Pack 160 + Desert Arena 53, HF Desert Kit tileset (Cactus/Palm/Sand 32-8px,
quicksand animato GIF, Hermit Sand 5-sprite burrow), ambientCG PBR sand 20
material seamless 1K, Kenney roguelike-caves.

**Audio**: Sonniss 6691 file royalty-free perpetual (Paw Trot = "Skiv soft paw
trot diretto", Deep Breather idle pitch -2 semitoni, Alien Creature Growl
sweep, AMB Wind-Gusty desert, ATMO Eerie Cave loop) + HF OGA-CC0 creature SFX
811 (80-CC0-creature roar, Monster RPG 2, Baby Animals cub, cat purr).
**`vocal/sand-spell.flac` = DIRECT FIT Skiv echolocation/sand-magic SFX**.
Pipeline Audacity documentata: idle (Deep Breather trim 3s + pitch -2 +
22050Hz mono), roar (roar_01.ogg + Punch Whoosh layered), echolocation
(sand-spell trim 800ms + EQ high-pass 2kHz + reverb tail). Kenney UI/impact +
FreePD orchestral 1237 MP3.

**Licensing**: 100% license-clean (`evo-tactics-refs-meta/HANDOFF.md`,
MANIFEST.json indicizza 32136 file). ~8080 CC0 + 6691 Sonniss perpetual +
~1240 PD reference-only. Zero CC-BY-SA viral. Zero Tier B/C (DMCA: GTA/CoD/
Pokemon banditi esplicitamente). 4 path workflow:
1. **Path 1**: Kenney/CC0 base + modify Aseprite + CREDITS.md entry
2. **Path 2**: AI gen (Retro Diffusion ToS enterprise indemnified) 10 variant
   -> pick 1-3 -> polish -> CREDITS "AI generated, human-edited"
3. **Path 3**: ref + redraw fresh (studia, chiudi file, canvas blank, redraw)
   -> CREDITS "original work, inspired by [era]"
4. **Path 4**: licensed SFX -> Audacity edit/layer -> CREDITS source
Local ref folder PRIVATO (mai synced). Shipping solo da `Game/assets/` +
CREDITS.md provenance.

### 11.7 Fonti & ricerca disponibili (indice)

| Fonte | Path | Contenuto |
|-------|------|-----------|
| Museum index | Game `docs/museum/MUSEUM.md` | ~45 card + 3 gallerie + 9 inventory + relevance table |
| Pilastri canonical | vault `Spaces/Dev/Evo-Tactics/core/02-PILASTRI.md` | 6 pilastri + ancora ispirazione |
| Source of Truth | vault `core/00-SOURCE-OF-TRUTH.md` | §14 grid, §15 campaign/encounter, §20-23 evoluzione |
| Art direction | vault `core/41-ART-DIRECTION.md` + `00F-ART_AUDIO_BUSINESS.md` | Reference + anti-reference + audio + business |
| HUD layout | vault `core/44-HUD-LAYOUT-REFERENCES.md` | HP floating + AP pip ref |
| Design freeze | Game `docs/core/90-FINAL-DESIGN-FREEZE.md` (A3) | Scope shipping locked |
| Roadmap index | Game `docs/planning/EVO_FINAL_DESIGN_ROADMAPS_INDEX.md` | M0-M6 + FD-ID backlog |
| Combat canon | Game `docs/combat/combat-canon.md` + `round-loop.md` | d20 + status + economy frozen |
| Design audit | Game `docs/planning/2026-04-20-design-audit-consolidated.md` + `pilastri-reality-audit.md` | Pillar audit post-M1 |
| ADR game-design | vault `Spaces/Dev/Evo-Tactics/adr/` (39) + Game `docs/adr/` (date-named) | Decisioni architetturali |
| Design watcher | vault `production/agents/evo-tactics-design-watcher.md` | Agent flag contraddizioni |
| Asset refs | `evo-tactics-refs-meta/` (SKIV_REFS, CATALOG, CC0_SOURCES, HANDOFF) | Provenance asset 100% classificata |
| Art Godot | Game-Godot-v2 `docs/godot-v2/visual-screen-bible.md` + `visual-design-research.md` | Bibbia visiva 3-modi |
| External repos | vault `memory/reference_external_repos.md` | Repo tracciati Fase 2 (non letto in audit) |

### 11.8 A che punto siamo (roadmap M0-M6)

Fase: **Final Design Freeze** (scope locked 2026-04-20). Critical path:
Combat -> Balance -> Content -> UX -> Meta -> RC. Ogni gate blocca il
successivo + richiede approvazione Master DD.

| Fase | Nome | Stato | Dettaglio |
|------|------|-------|-----------|
| M0 | Baseline & Governance | ~completo | Freeze pubblicato, docs registry, owner matrix pending (FD-006) |
| M1 | Combat Freeze | **IN CORSO** | Resolver Python deprecato/killed 2026-05-05 (ADR-2026-04-19), Node canonical, contracts 23/23, 237 Python test archiviati, 6 azioni + 6 status + economy PT/PP/SG frozen. Gate: validator+smoke CI |
| M2 | Balance & Progression | Attesa M1 | trait audit 33/33 done; economia PE/PI/Seed non frozen (FD-050-058) |
| M3 | Content Slice | Attesa M2 | 4 specie (Dune Stalker/Sand Burrower/Echo Wing/Rust Scavenger) + 6 job + 3 biomi (Desert/Cavern/Badlands); mission slice incompleta (FD-060-068) |
| M4 | UX/HUD/Telemetry | Parziale | HUD Wave 2-7 shipped (PT/PP/SG, AP, status, biome bonus, warning); debrief spec pending (FD-080-087) |
| M5 | Meta & Cross-Repo | Attesa M4 | Form Evolution Engine Phase A-D done (🟢 cand P2, Prisma persistence); Recruit/Trust + Nest/Mating slice pending |
| M6 | Release Candidate | Attesa M5 | Target 50 playtest; validator/smoke/snapshot pending; no Master DD approval |

**Deferred / cut espliciti** (con motivazione):
- XP Cipher: parked redundant (ADR-2026-04-17; coperto da job/mating/VC economy)
- Tabletop DM mode: killed digital-only (ADR-2026-04-19; "1 gioco online no master")
- Genetics mating complesse: M5 slice minima (genealogy/multi-gen deferred post-freeze)
- Game-Database HTTP runtime: out-of-scope freeze (solo Game->DB import unidirezionale)
- Enneagram deep tuning: modulo secondario (ADR-2026-04-23; non asse design core)
- Burnout/sentiment detection + Rust CLI rewrite: won't (RESEARCH_TODO W3/W6, no perf problem)

### 11.9 Gap, contraddizioni & autorita' cross-layer (onesto, no fabbricazione)

1. **Spore ibrido**: vault dice "Spore-like" poi chiarisce "NON sandbox,
   pattern = Wesnoth advancement tree + AI War pack-unlock". Nome ref corretto,
   adozione meccanica ibrida (concetto non meccanica diretta).
2. **FFT grid-agnostic**: ADR-2026-04-16 accetta hex-axial citando FFT, ma
   pathfinding/FOV non implementati (TV-first shared-screen). Borrow UX FFT
   senza richiederne complessita' grid. Accettabile MVP.
3. **Iso vs ortho RISOLTO**: intento "2.5D iso" vs codice ortho (Camera2D
   zoom 2.0, no shear). Verdetto 2026-05-16: codice canonical, art-direction
   ora ortho. Asset pipeline zero-cost ri-allineata.
4. **Narrative Fase A vs B**: Fase A Sistema-centric (AI War) defer named-hero
   (Descent Road to Legend) a Fase B post-EA. Rischio se community chiede
   narrativa prima del trigger story-mode workstream.
5. **Audio senza ancora-gioco**: unico pilastro senza ispirazione-gioco
   nominata (solo source pack Sonniss/HF/Kenney). Accettabile (low-pri pre-MVP).
6. **Moodboard visivo pending**: palette matrix 9 biomi canonical ma esempi
   visivi moodboard ancora da produrre.
7. **Discrepanza cross-layer (sapere quando si wira)**:
   - Triangle Strategy = **museum-only** (5/5 FORGOTTEN), NON in vault
   - Don't Starve / AncientBeast / Fire Emblem / OpenRA / Wesnoth / Ink =
     **vault core**, framing diverso o assenti in museum
   - Stessa ispirazione (es. FFT) ha framing leggermente diverso nei 2 layer:
     non contraddizione, complementare. Museum = catalogo alternative + ROI +
     reuse-path; vault `core/` = decisione canonical (autorita' A1-A3, freeze
     A3 vince per scope shipping). Verificare coerenza prima di wire meccanica.

**Negative results** (cercati esplicitamente, CONFERMATI assenti): Darkest
Dungeon, XCOM core series (solo "Long War 2" come analog convergenza P6),
Pikmin, Pokemon (solo anti-reference, mai positivo), Monster Hunter, Battle
Brothers (citato solo in pattern Telegraph 7-source, no card), Halfway (idem),
Resident Evil, nessun "Descent: Journeys" board game (solo Road to Legend).

**Conteggio finale**: ~31 titoli unici citati positivamente (8 pillar-tier +
1 creature museum + 1 quick-win + 11 indie-cluster + 10 core/GDD narrative+
system) + 8 anti-reference esplicite + ~14 museum card senza gioco esterno
(worldgen/genetics interni). Scope audit: museum index + grep vault,
2026-05-18 -- NON garanzia di completezza esaustiva.

---

## 12. Stile distillato & sistema design/contenuti

> Ricostruzione 2026-05-18 da audit cross-source (3 explore agent paralleli,
> Protocol 2). Fonti: vault `core/` (canonical), Game-Godot-v2 impl
> (`tokens.gd`, `cinzel.tres`, `visual-screen-bible.md`), Game `docs/`,
> Game-Database. File-cited, gap dichiarati, no fabbricazione.

### 12.1 Stile distillato (fingerprint)

#### Identita & naming

| Dimensione | Valore canonical | Fonte |
|------------|------------------|-------|
| Nome progetto | **Evo-Tactics** -- co-op tactical RPG, 4-8 player vs antagonista. PEGI 16. Early Access -> Premium (no F2P) | vault `00F-ART_AUDIO_BUSINESS.md` §1 |
| Antagonista | **Sistema** (mai chiamato "AI" -- entita' diegetica persistente) | vault `00F` §4.1; `visual-screen-bible.md` |
| "Skiv" | **NON una specie letterale**: archetipo/shorthand player-facing EN. Es. "Dune Skiver" = `Arenavolux sagittalis` (IT primary "Predatore delle Dune"). Etimologia non dichiarata | vault `00E-NAMING_STYLEGUIDE.md` |
| Naming specie | Code: Genus latinizzato Title Case 4-18char + epithet lowercase semantico. Player-facing: 2-3 parole, IT primary + EN alt. 84 specie canonical, 7 job, 4 archetipi | vault `00E §Regole formali` |
| Naming biomi | kebab/snake ASCII descrittivo (`ferrous-badlands`, `caverna_sotterranea`). 9 shipping + 11 deferred. 6 class enum (arid/subterranean/wetland/upland/canopy/littoral) | vault `00E` + `41-ART-DIRECTION.md` |
| Bias fonetico | Apex/Threat -> cluster duri (k,t,x); Keystone/Support -> sonoranti (m,n,l). Bias non regola | vault `00E §Regole formali` |

#### Narrativa & tono

- **Pattern A Sistema-centric** (attivo): Sistema = unico attore narrativo,
  parla al player via Ink (5-8 knot/tier). Creature = **mute, anonime**
  ("Wolf-03"), identita' emerge da trait+MBTI+comportamento.
- **Tono modulato** per `sistema_pressure`: Calm -> Tense -> Apex
  (`ai_profiles.yaml` campo `narrative_voice` opzionale).
- **PEGI 16**: body-horror trait (denti seghettati, bleeding, fracture),
  status mentali (panic/rage), antagonista distopico.
- **Fase B post-EA** (deferred): hybrid Overlord (Sistema) + 2-4 Custodi
  named (Descent-inspired). Non implementato.
- Fonte: vault `00F` §4 + `02-PILASTRI.md` P5 + `visual-screen-bible.md` Screen 3.

#### Tipografia / font

Stack canonical (vault `42-STYLE-GUIDE-UI.md §Typography`):
```
--font-ui:   'Inter', 'Noto Sans', system-ui, sans-serif
--font-mono: 'JetBrains Mono', 'Consolas', monospace
```
Scale TV-first (1080p @ 3m): xs 14 / s 16 / m 20 (default) / l 24 / xl 32 /
xxl 48 / hero 72 px. **Min 16px legibile, NO weight <400** (illeggibile TV).

Godot impl (`Game-Godot-v2 tokens.gd`): FONT_LABEL 12 / BODY 14 / H3 18 /
H2 20 / H1 28 / DISPLAY 36 / HERO 56. Theme resource `cinzel.tres`
(variant label/button/progressbar). **Nota onesta**: nessun .ttf "Cinzel"
nel repo -- system font fallback; "Cinzel" = intento estetico serif
rinascimentale, non font caricato. Scale Godot px != scale CSS (due
sistemi, riconciliare se si unifica).

#### Palette canonica

**Funzionali universali** (10, vault `41-ART-DIRECTION.md`):
Player `#4a8ad4` | Sistema `#d44a4a` | NPC recruit `#e8c040` | Selection
`#f0f0f4` | AoE `#d44a4a80` | Path preview `#40d4a8` | Buff `#4ad488` |
Debuff `#d4884a` | Crit flash `#f0d040` | Heal flash `#88d444`.

**Surface dark** (vault `42-STYLE-GUIDE-UI.md`): bg-primary `#030912` /
surface-soft `#0a1420` / elevated `#142030` / text-primary `#f2f8ff`
(17.8:1) / text-secondary rgba(242,248,255,.7).

**Biome matrix 9 shipping** (vault `41-ART-DIRECTION.md §Palette matrix`,
dominante/accent/mood): savana ocra `#b8935a` | caverna basalt `#3d3d42`
cyan-bio | foresta_acida poison `#5a7a3a` | foresta_miceliale fungal
`#6b4a7a` | rovine_planari stone `#5e5a52` | frattura_abissale deep-blue
`#0d1e3d` | reef teal `#1e6a7a` | abisso_vulcanico lava `#c83a1e` |
steppe_algoritmiche steel `#6a6e78`. (11 biomi extended deferred post-MVP).

**Ferrospora UI shell** (vault `42-STYLE-GUIDE-UI.md §Ferrospora tokens`,
sampled 2026-05-16): teal `#3acde5` | mycelium `#cd52d2` | bronze-gold
`#eedbae` | ground `#070707` | frame-gold `#f5e1aa`. **Finding**: sigil
action-dock attack/defend/ritual = AI art painterly-gradient, NON flat
token (no hex canonical -- design decision aperta, non valore nascosto).

#### UI identity

- **3 modi visivi** (`visual-screen-bible.md §Screen grammar`):
  World-forming (void vivo, beat ritual 500-900ms) / Tactical (grid pulita,
  overlay alto-contrasto, feedback 80-350ms) / Memory (battlefield dim,
  portrait/voce, reveal 400-900ms).
- **HUD hierarchy** (`41-ART-DIRECTION.md`): L1 Unit+HP (center, always) >
  L2 grid+cover > L3 intents (overlay planning) > L4 HUD AP/PT/status
  (edge) > L5 log (lateral) > L6 minimap (corner toggle).
- **Motion** (`tokens.gd`): pulse .08 / quick .18 / normal .3 /
  transition .5 / slow .7 / ritual .9.
- **TV safe-zone**: padding >=5% viewport (>=54px @1080p), zero UI critica
  outer 5%. Target MVP TV-1080p; 4K integer 2x.
- **Pixel art**: 32x32 tile MVP, upscaling integer-only 2x/3x/4x.

#### Audio identity

SFX-only, **creature silent** (no VO -- comunicano via comportamento),
Sistema narra via Ink (tono Calm/Tense/Apex). Mix default Music 70% /
SFX 100% / Master 80%. MVP prototype freesound.org; post-EA asset pack
commerciale. **Status DRAFT** (ADR-2026-04-18-audio-direction-placeholder,
`creature-sfx-spec.md` draft, pitch convention TBD). Fonte: vault `00F` §3.

#### Accessibility (gate canonical, vault `41-ART-DIRECTION.md`)

Contrast body >=4.5:1 (WCAG AA), large >=3:1, critical >=7:1 (AAA target).
Colorblind mode (shape+color), high-contrast (2px border, 90% opaque bg),
3 scale font, screen-reader parity.

### 12.2 Sistema design-doc & autorita

**Stack autorita A0-A5** (Game `docs/planning/EVO_FINAL_DESIGN_SOURCE_AUTHORITY_MAP.md`).
Nota: la sez. 11 citava genericamente "A1-A3 freeze"; la gerarchia precisa e':

| Liv | Autorita | Governa | Precedenza |
|-----|----------|---------|------------|
| **A0** | `docs/governance/*`, `docs_registry.json` | Path file, frontmatter, status, canonical-vs-storico | Vince su planning + convenzioni locali |
| **A1** | `docs/hubs/*`, `docs/combat/round-loop.md`, `docs/adr/*` | Boundary architetturali, contratti, runtime scope | Vince su freeze se boundary contraddetto; non override data |
| **A2** | `data/core/*`, `packs/.../data/*`, `packages/contracts/schemas/*` | Verita' meccanica/numerica/schema, validazione, tuning | Vince su doc descrittivi |
| **A3** | `docs/core/90-FINAL-DESIGN-FREEZE.md` | Sintesi prodotto, scope shipping, priorita' | Vince su roadmap/planning |
| **A4** | `AGENTS.md`, `.claude/*`, `CLAUDE.md`, `SAFE_CHANGES.md` | Modo operativo agent, DoD, guardrail | Governa "how" non "what" |
| **A5** | Canvas, appendici, playtest notes, research backlog | Contesto, intento, baseline | Solo informa; perde vs A0-A4 |

Principio: *governance colleziona, ADR delimita, YAML prova, freeze decide
prodotto, agent-doc esegue, storico ispira ma non governa.*

**Serie core numerata** (`docs/core/NN-*.md`, Game canonical + vault shadow).
Indice essenziale (A0 registry):

| Doc | Scopo |
|-----|-------|
| 00-GDD_MASTER / 00-SOURCE-OF-TRUTH | Master index + sorgente unificata (vision+loop+ecosystem) |
| 00B/00C/00D/00E/00F | Promotion matrix / where-to-use / engines-as-features / **naming styleguide** / art-audio-business |
| 01-VISIONE / 02-PILASTRI / 03-LOOP | Vision + 6 pilastri + session loop |
| 10-SISTEMA_TATTICO / 11-REGOLE_D20_TV | Combat ruleset d20/AP/MoS/PT-PP-SG + TV rulebook |
| 15-LEVEL_DESIGN / 17-SCREEN_FLOW | Map/encounter + UX flow |
| 20-SPECIE_E_PARTI / 22-FORME_BASE_16 / 24-TELEMETRIA_VC | Specie/morph-slot + 16 forme MBTI + VC scoring |
| 25-REGOLE_SBLOCCO_PE / 26-ECONOMY / 27-MATING_NIDO / 28-NPC_BIOMI_SPAWN | Unlock PE/PI + economy + mating/nido + Director/spawn |
| 30-UI_TV_IDENTITA / 40-ROADMAP / 41-ART-DIRECTION / 42-STYLE-GUIDE-UI / 43-ASSET-SOURCING / 44-HUD-LAYOUT | UI TV + roadmap + arte + style-guide + asset sourcing + HUD ref |
| 51-ONBOARDING-60S | First-match 60s UX |
| **90-FINAL-DESIGN-FREEZE** | **A3 supreme** -- scope shipping, freeze, validation gates |

**Governance machinery (A0)** -- `Spaces/Dev/Evo-Tactics/governance/` +
Game `docs/governance/`:
- `docs_registry.json` -- SSoT inventory (path/title/status/owner/workstream/
  last_verified), CI gate ogni doc -> entry
- `docs_metadata.schema.json` -- JSON Schema frontmatter (status/workstream/
  language enum), linter CI
- `workstream_matrix.json` -- 7-8 workstream (flow/atlas/backend/dataset-pack/
  ops-qa/combat/cross-cutting/incoming), owner + exit-criteria
- `GLOSSARY.md` -- vocabolario canonico IT+EN
- `Q-001-DECISIONS-LOG.md` -- tracker approvazioni Tier1/2/3 + outcome+commit
- `QUARANTINE.md` / `legacy_index_mapping.md` / `master_realign_plan.md` --
  doc deprecati / mapping storico->active / piano migrazione

**Decision recording** -- 3 convenzioni ADR coesistono:
- vault `adr/ADR-YYYY-MM-DD-<slug>.md` (~44, date-named, immutabile)
- Game `docs/adr/` (date-named, sync con vault, cross-ref in freeze/hubs)
- codemasterdd `docs/adr/NNNN-*.md` (numerati, infra non game-design)
- Museum-first: `docs/museum/cards/` cattura intento/alternative (A5)

**Godot DoD/safe-change gate** (`Game-Godot-v2 .claude/`):
- `SAFE_CHANGES.md`: 🟢 safe (doc, refactor <50LOC, test, component) /
  🟡 checkpoint (round flow, initiative, VC, schema, endpoint, scope-cut) /
  🔴 hard-gate (`.github/workflows`, `migrations/`, `packages/contracts/`,
  `services/generation/`, `.env`)
- `TASK_PROTOCOL.md`: 7-fase (orient->min-read->map->analysis->plan->
  execute->DoD-verify); DoD = prettier + governance + AI test + smoke
- Godot rispetta canon Game via reference (no duplicazione file)

**Consistency**: CI governance gate (`tools/check_docs_governance.py`:
registry completeness + frontmatter + stale + orphan) + design-watcher
agent (drift freeze/ADR/YAML/schema -> Q-001) + dual-track canonical/storico
+ frontmatter lifecycle (status enum + review_cycle_days).

### 12.3 Pipeline generazione & gestione contenuti

#### Dove vive il content (canonical + formato)

| Content | Sorgente canonical | Formato | Validato da | ETL target Godot |
|---------|--------------------|---------|-------------|-------------------|
| Specie lifecycle | Game `data/core/species/*_lifecycle.yaml` | YAML v1.7 | `validate_species_v1_7.py` | `data/lifecycle/lifecycles.json` (15 specie) |
| Trait | Game `data/core/traits/active_effects.yaml` | YAML (+JSON catalog derivato) | foodweb/trophic validators | `data/traits/active_effects.json` (458) |
| Biomi | Game `data/core/biomes.yaml` | YAML | `validate_bioma_v1_1.py` | `data/biomes/biomes.json` |
| Foodweb | Game `packs/.../data/foodwebs/*.yaml` | YAML | `validate_foodweb_v1_0.py` | (no auto-export) |
| NPG/Director | Game `packs/.../data/npg/*.json` | JSON | schema | (se serve) |
| Taxonomy CMS | Game-Database `server/prisma/schema.prisma` | Prisma->PostgreSQL | AJV (import-taxonomy) | sync via import script |
| Swarm artifact | Dafne `camel-agents/artifacts/*.json` | JSON (coherence+payload+confidence) | review manuale | -> Game (0 auto-integrated) |

#### Generazione

- **Director / NPG** (Game `docs/core/28-NPC_BIOMI_SPAWN.md` +
  `apps/mission-console/src/state/generator/`): da biome context -> NPC
  group (power_range, group_size, role_weights), consuma `trophic_roles.yaml`,
  valida vs `species.yaml` global_rules.
- **Dafne specialists** (swarm): trait/biome/species/lore curator generano
  artifact JSON con `confidence` 0-1 (>=0.9 auto-integrabile / 0.5-0.9
  review / <0.5 reject) + `coherence_check` (deve referenziare file esistenti).
- **AI narrative** (Game `apps/backend/services/narrative/`):
  briefingVariations / enneaVoice / innerVoice / mbtiInsights / qbnEngine
  (Ink-based). Personality synth Enneagram+MBTI da `tools/py/modules/personality/`.

#### Gestione / authoring

- **Game-Database dashboard** (`apps/dashboard/src/features/`): CRUD React
  trait/specie/biome (slug auto, dataType, range, synergies, conflicts).
  E2E `e2e/traits.crud.spec.ts`. Storage Prisma->PostgreSQL + AuditLog.
- **Trait scheda operativa** (`README_HOWTO_AUTHOR_TRAIT.md` +
  `docs/traits_scheda_operativa.md`): definisci slug+dataType, ref
  `trait_reference.json` per label condivise.
- **Validation gate** (Game `packs/evo_tactics_pack/`):
  foodweb.py (edge predation/scavenging/detritus) + trophic_roles.py
  (keystone/dominant/engineer/...) + schema validators per versione +
  `validate_package.py` (all-in-one -> `out/validation/*.json`).
  No playtest valido finche' Balancer pass (placeholder 0 -> verificato).

#### Flusso cross-repo content

```
[Authoring] Game-Database dashboard CRUD  --\
                                             > Prisma/PostgreSQL (canonical CMS)
[Authoring] Game data/core/*.yaml  --------/        |
                                                    | import-taxonomy.js
                                                    v
   Game-Database  --(npm run evo:import --repo Game)--> Postgres + AuditLog
        ^                                                    |
        | legge packs/evo_tactics_pack/docs/catalog/         |
        |                                                    v
   Game data/core/ (YAML A2 truth)  <-- runtime fallback OR GET /api/traits/glossary
        |
        | tools/etl/*.py (lifecycle/species/biome/ai_profiles yaml->json)
        v
   Game-Godot-v2 data/*.json  --> GDScript loader scripts/data/*.gd --> runtime
```

- **Game-DB <- Game** (build-time, `import-taxonomy.js`): legge
  `packs/evo_tactics_pack/docs/catalog/` (species/trait/biome/ecosystem),
  AJV validate, batch 50, upsert by slug -> Postgres + AuditLog.
- **Game-DB -> Game** (runtime opt-in): `GET /api/traits/glossary`,
  `GAME_DATABASE_ENABLED=true`.
- **Game -> Godot** (ETL per sprint, `Game-Godot-v2 tools/etl/*.py`):
  `lifecycle_yaml_to_json.py` (15 specie: anguis_magnetica, dune_stalker,
  leviatano_risonante, ...), `species/biome/ai_profiles_yaml_to_json.py`.
  Output JSON -> GDScript loader `scripts/data/lifecycle_catalog.gd`.

#### Gap & step manuali (dichiarati)

1. **Swarm artifact integration**: 223+ generati, **0 auto-integrati**
   (review Eduardo manuale, copia in target_files, commit). No re-validate
   post-merge.
2. **Godot ETL manuale per sprint**: no CI continuo, dev lancia
   `python tools/etl/*.py` dopo update content Game.
3. **Game-DB <-> Game one-way**: import legge Game->Prisma; no reverse
   sync Prisma->file. Authoring dashboard ma file restano in catalog.
4. **Trait dual-source**: `active_effects.yaml` (canonical) +
   `catalog/trait_*.json` (derivato). No SSoT unico -- validare entrambi.
5. **Cross-biome trait inheritance non documentato**:
   `global-trait-keeper.yaml` + per-biome keeper, merge strategy unclear.
