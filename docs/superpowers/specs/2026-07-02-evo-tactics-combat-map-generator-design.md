# Design spec -- Generatore procedurale di mappe-scontro (Evo-Tactics)

Data: 2026-07-02 (verdetto loop 2026-07-03) -- Stato: **DEFERRED**. Loop avversariale Round 1: premessa
OFF ("resa" = binario VISIVO, non procgen; Eduardo ha scelto fork A "mappe brutte da guardare"). NON
passare a implementation-plan. Riprendere SOLO come riframe-B (map-diversity per batch-sim), applicando
le correzioni fattuali in sez. 12. Vedi verdetto completo in sez. 12.
Reference di design: Dungeon Alchemist (solo pattern, no codice/asset) --
`docs/research/2026-07-02-dungeon-alchemist-design-patterns-map-generator.md`.

---

## 1. Contesto e obiettivo

Eduardo teme la RESA delle mappe di scontro di Evo-Tactics e vuole un generatore. Oggi le mappe tattiche
sono `terrain_features` SCRITTE A MANO (2-3 celle per board), zero procgen, e la resa visiva e' un gap
noto (solo `arid_ground` wired lato Godot). Obiettivo: un generatore che produca mappe-scontro tattiche
**valide, varie e bilanciate** in modo procedurale, innestandosi sul contratto e sul combat esistenti.

Non e' un clone di Dungeon Alchemist: DA e' un tool VTT 3D per dungeon-dressing; Evo-Tactics vuole
griglie TATTICHE 2D dove cover/elevation/hazard/LOS sono MECCANICHE, non decorazione. Di DA prendiamo
il *modello di generazione* (area/bioma semantica -> auto-fill coerente -> seed -> validazione), non la
tecnologia.

## 2. Decisioni bloccate (Fase 2)

| Asse | Scelta | Razionale |
| --- | --- | --- |
| Cosa e' | **Sistema runtime (data-layer)** | Genera mappa per scontro, seed-based; massima rigiocabilita'/varieta' sim. |
| Dove vive | **Backend Game (Node)** | E' lo STESSO codice della batch-sim -> parita' balance sim-vs-gioco; testabile headless. |
| LOS | **Dentro il primo scope** | Ma de-riscato: `getLineOfSight` esiste gia' nel backend (unwired). |
| Algoritmo | **Rule-based constraint placement** | Metodo reale di DA; vincoli tattici facili da imporre; il piu' testabile headless. |
| Schema output | **Emetti l'unione** (superset backend+Godot) | Entrambi i consumatori accettano; riconciliazione schema = cleanup separato. |
| Cover-wiring | **Fuori dal primo scope** | Il generatore EMETTE `defense_mod`; consumarlo nel combat = feature a se' (oggi non-wired). |

## 3. Vincoli e non-scope

**Vincoli:**
- Output = shape `EncounterDefinition` esatto -> Godot e sim lo consumano INVARIATO (zero rottura contratto).
- Deterministico: stesso `{biome_id, grid, seed, params}` -> stessa mappa (riproducibile per batch-sim).
- Zero nuove dipendenze prod senza approvazione (PRNG seeded = inline, no npm dep).
- ASCII-first nei doc; Conventional Commits; commit trailer ADR-0011 (`Coding-Agent` + `Trace-Id`).
- Direzione visiva target = Ferrospora biopunk (teal #3acde5); asset tile biome = pipeline gia' validata
  (dipendenza S1/S2, NON in questo scope: il generatore emette DATI corretti anche senza tile finali).

**Non-scope (esplicito, YAGNI):**
- Scena 3D, lighting real-time, arredo interni, export-immagine VTT (roba da DA, off-target).
- Cover-wiring nel combat (`defense_mod` consumato) -- emesso ma non consumato.
- Riconciliazione completa schema backend<->Godot (flaggata, follow-up).
- Objective-aware layout (capture-point degli schemi waves) -- stretch futuro.
- Autoraggio manuale/tool-designer UI -- scelto "runtime", non "designer".

## 4. Architettura (unita')

Tutte in `apps/backend/services/mapgen/` (confermato dallo scan backend: co-abita con `worldgen/`
ecologia, zero overlap). Ogni unita' = uno scopo, interfaccia netta, testabile in isolamento.

### 4.1 `BiomeRuleset` (data-driven, no logica)
Per ogni `biome_id`: palette `terrain_type`, pesi feature (densita' cover/hazard/elevation), lista
`los_blocker_types`, regole spawn (min-clearance, min-separation). Vive come blocco `gen_rules` esteso
in `data/biomes/biomes.json` (fonte UNICA condivisa backend+Godot -> niente drift dei tipi-blocker).
Interfaccia: `getRuleset(biomeId) -> ruleset`.

### 4.2 `MapGenerator` (funzione pura, seeded)
`generateMap({ biome_id, grid_w, grid_h, seed, params }) -> EncounterDefinition-shape`.
`params` = override opzionali (es. moltiplicatori densita' cover/hazard, difficolta', numero spawn);
default presi da `BiomeRuleset` se assenti. PRNG seeded inline (nessuna dep). Pipeline a stadi (ognuno funzione pura testabile):
- **a. base terrain fill** -- `terrain_type` per cella dal bioma. (Autotiling dei bordi = concern
  di RENDER lato Godot via plugin Better Terrain; il backend emette solo il dato per-cella.)
- **b. elevation pass** -- opzionale per bioma (dislivelli +/- come oggi consumati da elevation-damage).
- **c. feature placement** -- cover/ostacoli/hazard via regole pesate + **Poisson-disk** (distribuzione
  sparsa non-degenere, no cluster).
- **d. LOS-blocker placement** -- terreno alto (rocce/vegetazione densa/nuovi tipi) con intento tattico.
- **e. spawn zones** -- `player_spawn` + `spawn_points` nemici; enforce clearance + separazione.
- **f. validation pass** (vedi sez. 7) -- se invalida, **reject + reroll** con seed successivo (cap N
  tentativi, poi fail-esplicito loggato, mai silent-degrade).

### 4.3 `ContractAdapter`
Serializza l'output nello schema `EncounterDefinition` esatto (groups/waves). Punto d'innesto:
`/api/session/start` accetta gia' un param `terrainFeatures` (combat-adapter.js:92-103) ed
`encounterLoader.js` puo' essere esteso per caricare generato + hand-authored.

### 4.4 `LosCheck` (wiring meccanica, 2 impl per parita')
- **Backend**: collega l'esistente `getLineOfSight(from, to, blocksLosFn)` (`hexGrid.js:175`, oggi 0
  chiamanti) con predicato `terrainBlocksLos(type)` (tipi da `BiomeRuleset.los_blocker_types`). Slot:
  in `resolveAttack` pre-danno (tiro a distanza bloccato se LOS ostruita) e/o in `pickInRangeTarget`
  (filtra bersagli LOS-clear). **CAVEAT**: `getLineOfSight` sta in `hexGrid.js` ma il combat e' a
  griglia QUADRATA -> primo task = verificare/adattare l'algoritmo interno al square-grid (Bresenham);
  la firma resta invariata.
- **Godot (parita')**: LOS oggi ASSENTE nel runtime combat. Portare lo STESSO check + STESSO predicato
  in GDScript, leggendo gli stessi `los_blocker_types` da `biomes.json`. Cosi' sim e gioco reale
  bloccano gli stessi tiri.

## 5. Data flow

```
biomes.json (gen_rules) --> BiomeRuleset
                                 |
{biome_id,grid,seed,params} --> MapGenerator --(pipeline a-f)--> map-shape --> ContractAdapter
                                                                                     |
                                              EncounterDefinition JSON <-------------+
                                                     |                    |
                                       backend combat (resolveAttack,     Godot runtime (main.gd,
                                       moveCost, LosCheck)                 TileMap, LosCheck-GDScript)
```
Seed unico -> stessa mappa in entrambi -> parita'.

## 6. Schema `terrain_features` (unione) + divergenza

Divergenza reale rilevata tra i due consumatori:
- Backend consuma: `{x, y, type, defense_mod}` (`defense_mod` DICHIARATO ma NON usato dal resolver).
- Godot consuma: `{x, y, type, terrain_type, elevation, defense_mod}`.

**Decisione**: il generatore emette il **superset**:
`{x, y, type, terrain_type, elevation, defense_mod, los_blocker(bool)}`.
Entrambi ignorano i campi che non usano -> nessuna rottura. La riconciliazione (schema unico condiviso)
e' un **follow-up** loggato, non blocca il primo scope.

## 7. Validazione tattica (il cuore della qualita')

Il `validation pass` (stadio f) e' cio' che rende le mappe GIOCABILI, non solo "riempite". Regole
(config-driven, banda tarabile per bioma):
- **Reachability**: flood-fill da ogni spawn -> nessuna cella-obiettivo/spawn isolata da terreno
  invalicabile.
- **Spawn separation**: distanza min tra `player_spawn` e `spawn_points` nemici (no adiacenza degenere).
- **Spawn clearance**: celle spawn e immediato intorno prive di hazard/blocker.
- **Cover balance**: densita' cover entro banda [min,max] per bioma; distribuzione non tutta-da-un-lato.
- **Hazard density**: entro banda; nessun choke obbligato-su-hazard tra spawn e nemici.
- **LOS non-degenere**: nessuno spawn totalmente sight-blocked; esistono almeno K linee di tiro aperte.
Falliti > N reroll -> **fail esplicito** (log + errore), mai emettere mappa invalida.

## 8. Testing e Definition of Done (Quality Gate 3-step)

Casa test: `tests/services/mapgen/*.test.js` (`node --test`, gia' globbato da `run-test-api.cjs`).

- **Step 1 Smoke (happy-path verificabile)**: `generateMap` per >=1 bioma -> output conforme schema
  (assert campi + bounds x/y in griglia) + validation-pass verde. Determinismo: stesso seed -> output
  byte-identico (assert su 2 run).
- **Step 2 Ricerca (>=3 edge case)**: griglia minima (es. 3x3) vs grande (12x12); bioma con densita'
  hazard alta; seed che forza reroll (validazione fallisce e ri-genera); grid senza spawn definiti;
  bioma senza `gen_rules` (fallback). Comportamenti inattesi flaggati.
- **Step 3 Tuning (>=1 iterazione + delta)**: metrica di qualita' mappa (es. % reachability, spread
  cover, aperture-LOS) prima/dopo una taratura dei pesi bioma; report delta.
- **DoD**: test/build verdi (output mostrato), zero TODO/stub/placeholder nel modulo, LOS wired e
  testato (backend), parita' Godot portata + test GDScript, doc/commit aggiornati, no self-merge che
  salta review-gate. `QUALITY.md` con i 3 step + evidenze prima di production.
- **Test parita'**: un test che genera con seed S e verifica che backend-LosCheck e Godot-LosCheck
  diano lo stesso verdetto su un set di coppie (from,to) -> anti-drift.

## 9. Rischi / caveat / open items

- **R1 `getLineOfSight` su square-grid**: e' in `hexGrid.js` -> verificare che regga la griglia quadrata
  o adattare l'algoritmo interno (task 1 del blocco LOS). Firma invariata.
- **R2 Parita' 2-impl**: LOS + blocker in Node E GDScript = doppia manutenzione. Mitigazione: predicato
  e tipi-blocker da fonte-dato unica (`biomes.json`) + test-parita' anti-drift.
- **R3 Schema divergence**: emettiamo superset ora; riconciliazione = follow-up (non dimenticare -> issue).
- **R4 Resa visiva**: tile biome (S1/S2 asset) non pronti -> il generatore e' corretto sui DATI ma la
  resa finale dipende da asset fuori-scope. D-combat resta PAUSED (compatibile: siamo data-layer).
- **R5 SDMG**: questa architettura e' self-designed = ipotesi. Pre-implementazione: harsh-reviewer sullo
  spec (governance-critical) prima del merge del plan.
- **R6 defense_mod placeholder**: cover non-wired anche nel backend; se un domani si vuole cover-mechanic,
  e' feature separata (il generatore la emette gia').

## 10. Metodi applicati (governance, espliciti)

| Metodo | Dove |
| --- | --- |
| Refresh-verify (ADR-0026 #1) | Ground-truth via 2 subagent read-only (Godot combat + Game backend), non da memoria. |
| Agent-scanner STRONG-PURE | Pre-subagent; riuso godot-engine-specialist + Explore; zero nuovi agent. |
| Autoresearch multi-source | DA live + ricerca pubblica (devlog/technique) + 2 codebase probe. |
| Ground-truth > surface | Corretta l'inferenza "DA usa WFC" (falso); LOS scoperto half-existing. |
| Brainstorming skill (ADR-0026 #6) | Questo spec = output del flusso brainstorming (3 approcci + forcelle strutturate). |
| SDMG (ADR-0026 #7) | Spec = ipotesi -> harsh-reviewer pre-merge plan (R5). |
| Quality Gate 3-step | Mappato in sez. 8 (Smoke/Ricerca/Tuning + QUALITY.md). |
| Boundary repo | Il codice vive in `C:\dev\Game` (backend) + `Game-Godot-v2` (Godot): branch+PR, merge = Eduardo. |

## 11. Riferimenti

- Report DA + technique register: `docs/research/2026-07-02-dungeon-alchemist-design-patterns-map-generator.md`
- Godot-v2 combat (specialist): `scripts/main.gd:487-492`, `scripts/data/encounter_definition.gd`,
  `resources/tilesets/*.tres`, `data/encounters/encounters.json`.
- Backend combat (Explore): `apps/backend/routes/sessionHelpers.js:270` (resolveAttack),
  `apps/backend/services/combat/moveCost.js`, `apps/backend/services/grid/hexGrid.js:175`
  (getLineOfSight, unwired), `schemas/evo/encounter.schema.json`, `apps/backend/services/worldgen/`
  (ecologia, no overlap), `tests/services/mapgen/` (casa test proposta).
- Tecniche (open-source): `mxgmn/WaveFunctionCollapse` (MIT), `boristhebrave/DeBroglie` (MIT),
  `Portponky/better-terrain` (Unlicense), Poisson-disk (Bridson 2007).
- Memory: `project_godot_first_playable`, `project_godot_visual_asset_pipeline`.

## 12. Verdetto loop avversariale (Round 1, 2026-07-02/03) -- SPEC DEFERRED

Loop di confutazione, 3 subagent con lenti diverse: `harsh-reviewer` (solidita'/governance) +
`game-design-validator` (first-principles sulla premessa) + `general-purpose` (ground-truth vs codice).

**PREMESSA (game-design-validator, ratificata da Eduardo):** "resa" = problema visivo/render + curatela
tattica, NON data-layout. Il generatore tocca solo la data-layer -> per costruzione non muove la resa.
Eduardo ha confermato fork A ("mappe brutte da guardare"). -> **Generatore DEFERRED.** Vero primo passo
= binario visivo (wire 5 tileset biome rotti + 3-4 mappe curate su Ferrospora + fix 3 difetti visivi
combat), allineato a `project_godot_visual_asset_pipeline` S0-S3 + GGv2 #387. Riframe-B (map-diversity
per batch-sim) resta disponibile ma separato dalla resa: allora taglia LOS + superset, sotto
balance-authority, rinomina.

**LOS (harsh + ground-truth, verificato su codice) -- CUT dal primo scope:**
- `getLineOfSight` (`hexGrid.js:175`) e' HEX-native (cube coords `q,r`, `hexDistance`, `cubeRound`) ->
  su griglia quadrata e' un PORT di algoritmo, non "wiring, firma invariata".
- `resolveAttack(actor,target,rng)` (`sessionHelpers.js:270`) non ha geometria -> LOS non calcolabile
  li' senza allargare la firma (rompe "zero rottura contratto").
- LOS gia' testato (`tests/ai/hexGrid.test.js:123-136`) + SoT-green (primitiva esiste, mecc. non wired).
- Godot NO LOS; parita' = cross-repo, nessuna CI unica -> drift-trap.
- Fork square-vs-hex mai risolto (backend ha SIA griglia ortogonale SIA modulo hex).

**Correzioni fattuali (da applicare SE lo spec viene ripreso -- il primo Explore aveva dato fatti errati,
corretti da harsh + ground-truth):**
1. Seam: `tools/sim/combat-adapter.js` (SIM harness, NON `apps/backend/tools/...`); route reale =
   `session.js:2482-2490`; shape = `encounter.grid.terrain_features` (no param top-level; mutex con
   `scenarioId`).
2. Backend runtime legge solo `{x,y,type}` (`moveCost.terrainAtFromFeatures`); `defense_mod` dichiarato
   in schema ma letto da ZERO codice backend.
3. "Backend manca elevation" = FALSO: backend HA elevation unit-level, wired in hit
   (`elevationModifier.js`, `session.js:652`) + danno (`computePositionalDamage`). Gap reale: elevation
   non e' campo terrain su nessun lato; nulla deriva `unit.elevation` dalla griglia.
4. Cover asimmetrico: Godot GIA' consuma terrain `defense_mod` come cover (`terrain_reactions.gd:59-60`);
   non-wired SOLO backend.
5. RNG: esiste gia' `services/combat/pseudoRng.js` (mulberry32, 0 dep) -> riusare, non PRNG nuovo.
   Combat prod gira UNSEEDED -> determinismo solo se `seed` inviato (batch-sim si', live-play no).
6. Backend terrain-glue MANCANTE: `computeTerrainModifier`/`getDefenderAdvantage` leggono
   `unit.terrain_type/elevation` ma nulla li popola dalla griglia (`session.js:586` "TBD") -> un
   generatore che emette terrain-array NON attiva cover/elevation backend.
7. Validation/reroll: soglie da rendere numeriche (min/max/K); definire N + feasibility pre-check
   (griglie piccole 3x3 possono essere infeasible -> reject-loop); parita' = golden-vector fixture +
   DDA integer-only, non "live equivalence".

**Cosa RESTA valido:** disciplina non-scope, `BiomeRuleset` data-driven da fonte unica, determinismo
come requisito, la meta' generatore-di-DATI-terreno e' vicina a shippable. La META' LOS era su 3 fatti
sbagliati.
