# Dungeon Alchemist come reference di design + scope generatore mappe-scontro (Evo-Tactics / Godot-v2)

Data: 2026-07-02 -- Autore: Claude (Opus 4.8), sessione Stream-2 "mappe Evo-Tactics"
Macchina: Ryzen DESKTOP-T77TMKT (dove Eduardo possiede Dungeon Alchemist su Steam)
Stato: **FASE 1 -- report + proposta scope. HARD-GATE: nessun codice prima di OK Eduardo + brainstorming Fase 2.**

---

## TL;DR

- **Dungeon Alchemist (DA)** genera mappe belle con 4 leve: (1) generazione room/paint-based con
  auto-fill coerente di muri/pavimento, (2) auto-popolamento semantico di props per tema/biome, (3)
  re-roll stocastico ma coerente (1 click), (4) scena 3D con lighting real-time + terreno vivo animato.
- **CORREZIONE metodo (ricerca pubblica 2026-07-02)**: DA NON usa Wave Function Collapse nel prodotto
  finale (mia inferenza Fase-1 dall'osservazione era imprecisa). Iter reale: WFC -> abbandonato (fallisce
  su oggetti multi-tile + relazioni non-adiacenti) -> deep-learning/data-mining -> abbandonato (troppi
  pochi esempi di training) -> **shipped = algoritmo custom a regole di interior-design** (estrae dati
  comportamentali da stanze-esempio hand-crafted, piazza oggetti soddisfacendo vincoli logici +
  randomness). Dettaglio in sezione "Metodo reale di DA + technique register".
- **Osservato dal vivo** (non da doc): disegnato un "Dungeon Cell" (Crypt) trascinando un rettangolo ->
  DA ha auto-generato muri, pavimento in pietra, 2 torce con luce dinamica, e props a tema (ruota,
  branda); il re-roll ha ri-randomizzato SOLO i props mantenendo struttura+luci -> pattern chiave.
- **Vincolo duro rispettato**: DA = SW Unity proprietario. Estratti solo PATTERN di design, zero
  codice/asset. Target = Godot 4.x (Game-Godot-v2), NON Unity.
- **Ground-truth Godot-v2 (da subagent godot-engine-specialist, read-only)**: il combat oggi e' una
  **TileMap 2D flat top-down** (griglia quadrata, 16px, zoom 2x), terreno dipinto proceduralmente
  `(x+y)%5` su UN SOLO tileset (`arid_ground`), `terrain_features` **scritte a mano** (2-3 celle per
  mappa). Meccaniche elevation/cover/hazard/move-cost ESISTONO; line-of-sight e biome-theming visivo
  ASSENTI; **nessun procgen tattico esiste (greenfield)**.
- **Scope realistico proposto (MVP)**: un generatore che, dato `(biome_id, grid_size, seed, params)`,
  emette una mappa gia' conforme al contratto `EncounterDefinition` esistente (fill tile biome-aware +
  posizionamento `terrain_features` cover/ostacoli/hazard/elevation con regole biome-pesate +
  vincoli tattici). Si innesta sul seam esistente -> TerrainReactions/ElevationModifier/MoveCostField
  continuano a funzionare invariati. **Dipendenza nota**: i tileset biome visivi vanno autorati/wired
  (gap S1/S2 gia' tracciato in project_godot_visual_asset_pipeline).

---

## Metodi applicati (governance codemasterdd, espliciti)

| Metodo / protocollo | Dove applicato in questa sessione |
| --- | --- |
| **Refresh-verify pre-action** (ADR-0026 #1) | Verifica identita macchina (Ryzen confermato); lettura memory `project_godot_first_playable` + `project_godot_visual_asset_pipeline`; ground-truth codice Godot-v2 via subagent (non da memoria 29gg). |
| **Agent-scanner STRONG-PURE** (OD-007) | Invocato PRIMA di ogni subagent. Verdetto build-on-existing: riuso `godot-engine-specialist` (Fase 1), `game-systems-designer` + `game-design-validator` (Fase 2), `harsh-reviewer` (pre-merge). Zero nuovi agent. Flag dup `sot-drift-verifier`. |
| **Autoresearch multi-source** (ADR-0026 #2) | DA osservato DAL VIVO (computer-use, non solo README) + specialist su codice reale + 2 memory. Triangolazione live-app / source-code / memoria. |
| **Ground-truth > surface** (guardrail) | Architettura Godot-v2 letta da file:line reali, non da memory di 29gg (che era su combat come "WIP con difetti"). |
| **SDMG** (ADR-0026 #7) | La proposta di scope qui sotto = ipotesi alto-errore self-designed. NON e' decisione: input per il brainstorming Fase 2 (game-systems-designer + game-design-validator = falsificazione esterna) PRIMA di qualsiasi codice. |
| **Quality Gate 3-step** (global) | Applicabile SOLO in Fase 3 (implementazione). Ora non pertinente (nessun codice). Flaggato per dopo. |
| **Hard-gate** (mandato utente) | Nessun codice, nessun brainstorming Fase 2 finche' Eduardo non da OK su questo report. |

---

## Fase 1a -- Dungeon Alchemist: pattern di design osservati dal vivo

Sessione osservazione: avviato via Steam, editor mappa aperto ("Untitled Map"), disegnata e
re-rollata una stanza reale. Tutto quanto segue e' OSSERVATO, non da documentazione.

### Cosa rende buone le sue mappe (4 leve)

1. **Generazione room/paint-based con auto-fill coerente.**
   Il workflow primario e' "Draw Rooms": trascini un rettangolo (o forma libera cella-per-cella) sulla
   mappa -> l'app riempie automaticamente muri perimetrali, pavimento con transizioni coerenti, e
   apre varchi/porte. L'utente NON piazza singoli tile: definisce un'area semantica, il generatore
   risolve i tile. (Metodo interno: NON WFC nel prodotto finale -- vedi correzione sotto. L'auto-tiling
   dei bordi e' comunque un pattern standard riproducibile con i terrain-set di Godot.)

2. **Auto-popolamento semantico di props per tema/biome.**
   Le stanze sono organizzate in **categorie-tema** (Crypt, Desert, Village, Tavern, Castle, Mansion,
   Skeletal Palace, Abandoned Ruins, Alchemists' Laboratory, Pits...) con sotto-template (Dungeon Cell,
   Burial Chamber, Chapel, Great Hall, Hallway...). Il tema decide sia il tileset sia il SET di props
   pescabili. Disegnata una "Crypt > Dungeon Cell" -> generati automaticamente branda, ruota/carro,
   torce a muro coerenti col tema. Cambiare tema ri-tematizza output+asset.

3. **Re-roll stocastico ma coerente (1 click).**
   Ogni stanza ha un bottone re-roll. Cliccato -> **props ri-randomizzati mantenendo struttura+luci**
   (muri, torce, footprint invariati; arredo diverso: la ruota+branda-gialla sono diventate branda
   scura + detriti sparsi). Pattern chiave: **struttura deterministica, arredo stocastico
   theme-constrained, variazione a costo zero**. Questa e' la ragione per cui le mappe sembrano
   "fatte a mano ma infinite".

4. **Scena 3D con lighting real-time + terreno vivo.**
   NON e' 2D flat. E' una scena 3D con camera ruotabile (pan/zoom/rotate, cambio camera-mode). Le
   torce **proiettano luce dinamica** sul pavimento; muri con altezza e ombre proiettate; props
   volumetrici. La base outdoor e' un **biome forestale** con alberi, formazioni rocciose, cespugli,
   sentiero sterrato, e **animazione della natura** (voce di menu "Disable Nature Animations" ->
   fogliame animato di default). Griglia quadrata sovrapposta, toggle grid.

### Workflow UX di generazione / editing (osservato)

- **Toolbar verticale sinistra** = categorie-tool primarie (Rooms, Terrain, Water, Objects/Furniture,
  Lights, Characters, FX...). Ogni tool apre un pannello contestuale a sinistra.
- **Sotto-modi per tool**: il tool Rooms ha 3 tab (Draw Rooms / Remove Rooms / edit).
- **Toggle a strati (7 checkbox)**: colonna di 7 layer di auto-popolamento (struttura / pavimento /
  props / scaffalature / colonne / decor / natura) -- l'utente accende/spegne COSA il generatore
  riempie. Controllo granulare senza micro-editing.
- **Terrain-aware**: "Normal rooms will flatten the terrain below it" -- le stanze modificano il
  terreno sottostante; il generatore ragiona su un layer di terreno base.
- **Override manuale**: dopo la generazione l'utente puo' piazzare/spostare oggetti manualmente
  (tool Objects). Generazione = punto di partenza, non gabbia.
- **Camera 3D**: pan (click+drag), zoom (scroll), rotate (scroll-wheel premuto). Cambio camera-mode
  (top-down <-> prospettica).
- **Onboarding progressivo**: tooltip step-by-step ("Let's draw a room", "Let's show you around").

### Cosa e' realisticamente riproducibile (per Godot / Evo-Tactics) e cosa NO

| Pattern DA | Riproducibile in Godot-v2? | Note |
| --- | --- | --- |
| Auto-tiling bordi/transizioni su varianti tile | **SI (core)** | Godot ha terrain-sets nativi MA sono lenti/inaffidabili a runtime -> usare plugin **Better Terrain** (Unlicense/public-domain). Oggi Evo-Tactics usa un dither manuale `(x+y)%5`. Upgrade naturale. |
| Auto-popolamento per biome/tema | **SI (core)** | Mappa direttamente su `biome_id` -> regole di weighting per props/features. E' il cuore del valore. |
| Toggle a strati di generazione | **SI (facile)** | Flag booleani nel generatore (genera cover? hazard? elevation? decor?). |
| Re-roll seed-based coerente | **SI (facile+alto valore)** | Seed deterministico -> re-roll = nuovo seed. Perfetto per un backend sim-driven. |
| Posizionamento features (cover/ostacoli/hazard/elevation) | **SI (core)** | Emette nel contratto `terrain_features` gia' esistente. |
| Terreno outdoor a bioma (erba/rocce/alberi/sentieri) | **SI** | E' l'analogia GIUSTA per Evo-Tactics (creature che combattono in biomi), non le stanze-dungeon. |
| Scena 3D + camera ruotabile | **NO (off-target)** | Godot-v2 combat e' 2D flat top-down BY DESIGN. Riprodurre 3D = scope enorme, contro-direzione. |
| Lighting real-time dinamico | **NO / marginale** | Godot ha luci 2D, ma non e' il valore per una griglia tattica; costo alto, ROI basso. |
| Arredo interni dnd-style (furniture sim) | **NO (fuori scope)** | Evo-Tactics = battaglia creature outdoor, non dungeon-dressing da tavolo. |

**Sintesi**: il valore trasferibile di DA NON e' la grafica 3D ne' l'arredo dnd -- e' il **modello di
generazione**: area/biome semantica -> auto-fill coerente -> variazione seed-based -> override
manuale. Quello si mappa 1:1 su un generatore tattico Godot.

---

## Fase 1a-bis -- Metodo reale di DA + technique register (fonti pubbliche, no binari)

Costruito via ricerca mirata su fonti pubbliche (autorizzazione Eduardo a decompilare RIFIUTATA: EULA
DA + copyright vietano reverse-engineering a prescindere dal possesso; osservazione live + doc
pubbliche = sufficienti e pulite; decompilare avrebbe aggiunto rischio-derivazione al repo Game-Godot-v2
public, zero valore).

### Come DA genera davvero (3 iterazioni, da devlog ufficiale)

1. **Wave Function Collapse** -> ABBANDONATO. "WFC non funziona per oggetti multi-tile (letti/tavoli
   grandi) e non considera relazioni tra oggetti non adiacenti."
2. **Deep-learning / data-mining** (partner ML2Grow) -> ABBANDONATO. "Non riusciamo a creare abbastanza
   esempi perche' l'approccio funzioni."
3. **Algoritmo custom a regole di interior-design** -> SHIPPED. Estrae dati comportamentali da stanze
   hand-crafted, poi genera floor-plan che soddisfano regole logiche (prossimita' porte/finestre,
   walkability/accessibilita', relazioni oggetto-oggetto tipo "mantice vicino al camino, comodino
   vicino al letto", allineamento, spazio attorno agli arredi, regole d'angolo) mantenendo randomness.

**Implicazione per noi**: il motore reale di DA e' **constraint-based placement guidato da esempi**,
non WFC ne' ML end-to-end. Per una griglia TATTICA i nostri vincoli (spawn sgombri, reachability,
cover distribuita, densita' hazard) sono PIU' SEMPLICI dell'"interior design realistico" di DA ->
altamente riproducibile con tecniche pubbliche. NON ci serve replicare il loro ML.

### Technique register (open-source / CS pubblica, adattabile legalmente)

| Tecnica | A cosa serve nel generatore | Riferimento pubblico | Licenza |
| --- | --- | --- | --- |
| **Wave Function Collapse** (tiled model) | Fill tile con vincoli di adiacenza; buono per terreno, debole su multi-tile | `mxgmn/WaveFunctionCollapse` (Gumin, reference) | MIT |
| **DeBroglie** (WFC + constraints) | WFC con vincoli extra (path-connectivity, count, bordi) -> risolve i limiti multi-tile/globali di WFC base | `boristhebrave/DeBroglie` + docs | MIT |
| **Constraint-based placement** | Piazzare cover/ostacoli/hazard/spawn sotto regole tattiche (il pattern reale di DA) | letteratura PCG constraint-solving | pubblica |
| **Poisson-disk sampling** | Distribuzione sparsa e uniforme (alberi/rocce/cover senza cluster degeneri) | Bridson 2007 (algoritmo pubblico) | pubblica |
| **BSP / room-partition** | Suddivisione area in sotto-zone (se servono layout a stanze/arene) | roguelike PCG standard | pubblica |
| **Cellular automata** | Grotte/forme organiche (biomi cavernosi/paludosi) | roguelike PCG standard | pubblica |
| **Godot terrain autotiling** | Resa bordi/transizioni tile a runtime | native Godot 4 (LENTO/inaffidabile a runtime) | MIT |
| **Better Terrain (plugin)** | Rimpiazza autotiling nativo: piu' veloce, API runtime usabile | `Portponky/better-terrain`; API `BetterTerrain.set_cells` + `update_terrain_cells` | **Unlicense (public domain)** |

### DA capability catalog (cosa genera, da doc pubbliche)

- Auto-furnish: porte, muri, finestre, illuminazione, arredi, oggetti on-the-fly; libreria di
  "migliaia" di oggetti; tutto sostituibile.
- Biomi/terreni ambientali: montagne, fiumi, caverne, e altro in pochi click. Es. "Badlands" =
  scogliere ripide, gole, mesa, plateau, palette arancio/marrone/tan, vegetazione sparsa (cactus,
  scrub). -> DA modella ELEVATION (cliffs/mesa/plateau) + ACQUA (fiumi) + vegetazione bioma-specifica.
- Formati: stampa (dimensioni carta) o digitale illimitato; export mappa per VTT.

## Fase 1b -- Godot-v2: come gestisce OGGI le mappe di scontro (ground-truth)

Fonte: subagent `godot-engine-specialist`, read-only su `C:\dev\Game-Godot-v2` HEAD `ae5e486`
(2026-07-02), citazioni file:line verificate. Sintesi:

- **Scena**: `scenes/Main.tscn` (`scripts/main.gd`). Board = `GroundTileMap` (TileMap 2D flat).
  Camera2D fissa, zoom 2x. Griglia **quadrata** (no hex). Dim **variabile**: default 8x6, encounter
  override 6x6..10x10 via `EncounterDefinition.grid_width/height` o `grid_size:[w,h]`.
- **Rendering tile**: 100% procedurale in GDScript, `_paint_ground` (`main.gd:487-492`):
  `atlas_x = (x+y) % 5` su UN tileset `arid_ground.tres`. Dither a 5 varianti anti-scacchiera. NON
  autotile/WFC.
- **Difetto magenta/scacchiera**: gia' FIXATO 2026-06-03 (legacy Ansimuz checker -> nuovo
  `arid_ground.png`). **Rischio latente**: 5 altri tileset biome (`savana/caverna/foresta_acida/town/
  tundra.tres`) esistono ma NON referenziati da nessuno script (dead resources); 4 senza coord atlas
  -> renderebbero rotti se wired. Solo `arid_ground` e' reale.
- **Sorgente dati mappa (SEAM)**: NON fetch HTTP a runtime. E' un file JSON locale
  `data/encounters/encounters.json`, prodotto a build-time da ETL su YAML canonici in `C:\dev\Game`.
  Caricato via `EncounterCatalog.load_from_json_file`. Biome da `data/biomes/biomes.json`.
- **Contratto `EncounterDefinition`** (2 schemi coesistenti, normalizzati):
  - `grid`: `{width, height, terrain_features:[{x,y,type,terrain_type,elevation,defense_mod}]}`
  - `biome_id` (string, cross-ref biomes.json)
  - `hazard`: `{description, severity, stress_modifier}` (narrativo, non per-cella)
  - waves: `grid_size:[w,h]`, `objective`, `player_spawn:[[x,y]]`, `waves[].spawn_points`
  - **`terrain_features` sono SCARSE e SCRITTE A MANO** (2-3 celle su board 6x6/10x10). Anche il
    backend le autora a mano (`desertoCaldoHazardScenario.js` = array fisso). **Nessun procgen.**

### Support matrix terreno/biome (have / stub / absent)

| Feature | Stato | Note |
| --- | --- | --- |
| Elevation | HAVE (solo meccanica, non visiva) | `elevation` -> ElevationTerrainModifier (+/-1 attacco). TileMap flat, nessuna resa altezza. |
| Cover / defense_mod | HAVE (meccanica) | TerrainReactions per-tipo + override per-cella. Visivo = solo outline overlay. |
| Hazards (lava/palude) | HAVE | DOT/turno + penalita. Applicati in `_drive_encounter_runtime`. |
| Difficult terrain / move-cost | HAVE (flag OFF default) | MoveCostField Dijkstra per-morfotipo + bypass volo. `MOVE_TERRAIN_COST_ENABLED` env. |
| Line-of-sight blockers | **ABSENT** | Zero LOS nel repo. Range attacco = raggio flat, nessuna occlusione. |
| Biome theming (visivo) | **STUB/ABSENT** | Solo `arid_ground` wired. `_paint_ground` ignora `biome_id`. |
| Biome theming (meccanico) | HAVE | BiomeModifiers da biomes.json (mod attacco/resonance/stresswave). |
| Spawn points (dati) | HAVE | `player_spawn` + `waves[].spawn_points` consumati da ReinforcementSpawner. |
| Procgen tattico | **ABSENT (greenfield)** | Nessun worldgen tattico client o server. Il worldgen backend e' ecologia/food-web, non geometria griglia. |

---

## Divergenza DA vs Evo-Tactics (allineamento vincoli)

- **DA = dungeon-dressing 3D per VTT** (mappe belle da guardare, arredo interni, esportazione immagine).
- **Evo-Tactics = griglia tattica d20 2D per battaglie di creature in biomi** (mappe da GIOCARE, dove
  cover/elevation/hazard/LOS sono MECCANICHE, non decorazione).
- Percio' il generatore Evo-Tactics deve ottimizzare **leggibilita' tattica + bilanciamento** (spawn
  equi, reachability, cover distribuita, hazard non degeneri), non fedelta' fotografica.
- L'analogia giusta di DA non e' la "stanza-cripta" ma il **layer terreno outdoor** (erba + rocce=cover/
  ostacoli + alberi=LOS/cover + cespugli=difficult-terrain + dislivelli), ri-tematizzato per bioma.
- Direzione visiva target = **Ferrospora biopunk** (teal #3acde5), non parchment/fantasy DA. Gli asset
  tile biome vanno dalla pipeline gia' validata (3D->pixel per creature, ComfyUI-2D per tile/UI).

---

## Proposta di scope realistico (PROPOSAL -- input per brainstorming Fase 2, NON decisione)

> SDMG: questa e' un'ipotesi mia, alto-errore. Va falsificata in Fase 2 (game-systems-designer +
> game-design-validator) PRIMA di scrivere codice. Serve solo a dare forma al brainstorming.

**Nome di lavoro**: generatore procedurale di mappe-scontro (Evo-Tactics / Godot-v2).

**Principio**: replicare il *modello di generazione* di DA (area/biome semantica -> auto-fill coerente
-> seed-based -> override), NON la sua tecnologia 3D. Innestarsi sul contratto `EncounterDefinition`
esistente cosi' le meccaniche attuali continuano a girare invariate.

**MVP (scope minimo difendibile)** -- un generatore che, dato input
`{biome_id, grid_size, seed, tactical_params}`, produce un `EncounterDefinition`-shaped output:
1. **Fill tile biome-aware**: sostituisce `(x+y)%5` con selezione tile per bioma + transizioni
   (Godot TileMap terrain-sets/autotile). Richiede tileset biome autorati (dipendenza S1/S2).
2. **Posizionamento `terrain_features`** (cover/ostacoli/hazard/elevation) via **regole biome-pesate**
   + **vincoli tattici**: zone spawn sgombere, reachability garantita (no aree isolate), cover
   distribuita, densita' hazard entro banda.
3. **Determinismo seed-based** -> re-roll a costo zero (come DA), riproducibile per la batch-sim.
4. **Output = contratto esistente** -> TerrainReactions / ElevationModifier / MoveCostField invariati.

**Stretch (da valutare in Fase 2, NON MVP)**:
- Tag LOS blockers (feature oggi ASSENTE -- serve prima un sistema LOS).
- Objective-aware layout (capture-point degli schemi waves).
- "Toggle a strati" stile DA (genera cover/hazard/elevation/decor on-off).

**Fuori scope (esplicito)**: scena 3D, lighting real-time, arredo interni dnd, export-immagine VTT.

**Dove vive il generatore (da decidere in Fase 2)**: 2 opzioni --
(A) **backend Game** (Node, `services/worldgen/`) che emette `terrain_features` nell'ETL encounter ->
coerente con "backend = balance authority", batch-sim-friendly; oppure
(B) **client Godot** (GDScript) a runtime. Trade-off (authority/testabilita' vs iterazione visiva) =
materiale da brainstorming.

**Dipendenze/rischi noti**:
- Tileset biome visivi NON pronti (solo arid_ground). Il generatore puo' emettere DATI corretti anche
  senza tile finali, ma la resa visiva resta gap finche' S1/S2 asset non chiudono.
- D-combat e' PAUSED da Eduardo ("prima asset, su Ferrospora non parchment") -- il generatore e'
  data-layer, quindi compatibile col pause, ma la verifica visiva finale dipende dagli asset.
- LOS assente: se lo stretch LOS entra in scope, e' un sotto-progetto a se'.

---

## Hard-gate + domande aperte per Eduardo

**HARD-GATE attivo**: fermo qui. Nessun codice. Fase 2 (brainstorming skill per scope+design) parte
SOLO dopo tuo OK, con DA come sola reference.

Domande che orientano la Fase 2 (le pongo in chat, structured):
1. Il generatore ti serve come **tool designer** (autori mappe piu' in fretta) o come **sistema
   runtime** (mappe generate a ogni scontro nella sim)? Cambia molto lo scope.
2. Backend Game (data authority, batch-sim) vs client Godot (iterazione visiva): preferenza?
3. LOS (line-of-sight) dentro o fuori dal primo scope? Oggi e' ASSENTE nel combat.

## Fonti / evidenze

- **DA**: osservazione live via computer-use MCP (Ryzen), 2026-07-02: editor mappa, disegno+re-roll
  di una stanza Crypt/Dungeon-Cell, menu View, toolbar. Screenshot in sessione (non persistiti).
- **Godot-v2**: subagent `godot-engine-specialist` read-only su `C:\dev\Game-Godot-v2` HEAD `ae5e486`;
  file chiave `scripts/main.gd:487-492`, `scripts/data/encounter_definition.gd`,
  `resources/tilesets/*.tres`, `data/encounters/encounters.json`, `assets/tiles/ferrospora/PROVENANCE.md`.
- **Memory**: `project_godot_first_playable`, `project_godot_visual_asset_pipeline` (biopunk Ferrospora
  teal #3acde5; pipeline 3D->pixel validata; D-combat paused).
- **Ricerca pubblica** (2026-07-02, WebSearch/WebFetch diretto): DA devlog ufficiale (metodo di
  generazione: WFC->ML->custom interior-design-rules); dungeonalchemist.com (auto-furnish + biomi);
  DA Fandom wiki (biomi, paywall parziale). Technique: `mxgmn/WaveFunctionCollapse` (MIT),
  `boristhebrave/DeBroglie` (MIT), `Portponky/better-terrain` (Unlicense), Godot docs TileSets/TileMaps
  (`set_cells_terrain_connect`), Poisson-disk (Bridson 2007).
- **Vincoli**: DA = SW Unity proprietario, solo pattern-extraction (no clone/decompile/asset). Target
  Godot 4.x, no Unity. Autorizzazione utente a decompilare RIFIUTATA (EULA+copyright > possesso).
