# Big-map tactical design reference -- Evo-Tactics verso mappe "Descent-style" biome-survival

Data: 2026-07-03 -- Autore: Claude (Opus 4.8), sessione "mappe grandi Evo-Tactics"
Tipo: DESIGN-REFERENCE (sintesi ricerca cross-source). NON e' un implementation-plan.
Stato: reference doc. Le decisioni di scope/architettura restano gated a Eduardo (sez. 6).

Reference di ground-truth repo:
- `docs/research/2026-07-02-dungeon-alchemist-design-patterns-map-generator.md` (stato combat Godot-v2 + technique register)
- `docs/superpowers/specs/2026-07-02-evo-tactics-combat-map-generator-design.md` (spec generatore, DEFERRED, correzioni fattuali sez. 12)

Intento di design del proprietario (verbatim, da onorare):
> "le mappe devono essere grandi, stile Descent -- hazard da affrontare, punti da controllare,
> wave di nemici da tenere sotto controllo, il tutto mentre si esplora e si cerca di sopravvivere al bioma."

Movimento (verbatim):
> "la spesa per il movimento e' la stessa per ogni creatura ma cambia il risultato in quadretti a
> seconda delle sue mutazioni/trait e altri fattori" (costo azione fisso -> quadretti variabili per build evolutiva).

---

## 1. TL;DR

- **"Grande" non e' una virtu', e' un costo.** Il contro-esempio load-bearing e' Into the Breach: griglia 8x8
  hand-authored, scelta APPOSTA perche' mappe grandi/procgen generano dead-space non-divertente e informazione
  illeggibile. La regola per Evo-Tactics: **ogni quadretto in piu' va guadagnato** con un reveal-beat, un tick di
  clock, o una decisione-hazard. Altrimenti rimpicciolisci.
- **La tensione su mappa grande = tre sistemi a strati, NON "mappa piu' grande + piu' nemici":**
  (1) **REVEAL/PRESSIONE** -- la mappa entra a bocconi (room/sector-gated reveal a la Descent/Gloomhaven; pod-activation
  a la XCOM); ogni reveal e' simultaneamente spawn + hazard + objective drop, cosi' il fronte di esplorazione E'
  sempre il fronte di minaccia.
  (2) **CLOCK/OBJECTIVE** -- un orologio crescente (Doom / threat-per-round / hazard-front che avanza) tassa il
  temporeggiare, cosi' la mappa grande diventa una corsa e non un invito a fare turtle.
  (3) **TERRAIN-AS-MECHANIC** -- ogni hazard ha un VERBO distinto (nega-entrata / punisci-la-sosta / rallenta /
  blocca-LOS / isola), scalato col livello, cosi' il terreno impone routing ogni turno invece di essere chip-damage ignorabile.
- **Il layer mancante oggi in Evo-Tactics** (da ground-truth Godot-v2 + backend Game, sez. 3): LOS **ASSENTE**;
  `terrain_features` **scritte a mano e scarse** (2-3 celle); `waves[].spawn_points` consumati da `ReinforcementSpawner`
  ma **NON accoppiati all'esplorazione**; nessun procgen tattico; nessun clock di sopravvivenza. Il "survive the biome"
  oggi e' una stringa `objective` + un `hazard` narrativo per-encounter, non un sistema spaziale.
- **Movimento evolution-coupled** (l'intento del proprietario) ha precedenti solidi e diretti: MOV-come-stat che
  risolve un'azione a costo fisso in N quadretti (Lancer Speed, XCOM Mobility, D:OS1 move-per-AP, Descent Speed-pool),
  con modificatori che SCALANO con l'investimento di build (Caves of Qud Multiple Legs). Si innesta sul `MoveCostField`
  gia' esistente nel backend (sez. 4).
- **Accoppiamento al bilancio (sez. 5, load-bearing).** Il modello `xpBudget` attuale del backend
  (`apps/backend/services/balance/xpBudget.js`) valuta **SOLO gli stat dei nemici** (hp/mod/ap/range/guardia/tier)
  scalati per encounter_class + party_size. **Non ha alcun termine per area di griglia, densita' hazard, control
  point, tipo di objective, ne' waves accoppiate all'esplorazione.** L'audit doc stesso
  (`docs/balance/2026-04-25-encounter-xp-audit.md`) gia' avverte che il modello ignora action-economy, pressure-tier,
  hazard-tiles, AOE. Una mappa "Descent-style" AMPLIFICA esattamente tutte queste variabili non-modellate -> il gate
  xpBudget va esteso oltre l'area, e ogni claim di ri-bilancio va ri-ratificato a N=40 (non N=10, sez. 5).

---

## 2. Reference table -- gioco -> cosa rubare per Evo-Tactics

Ogni riga = un pattern con teeth meccaniche, non "atmosfera". Fonti in sez. 7.

| Gioco | Cosa rubare (verbo concreto) | Innesto su Evo-Tactics |
| --- | --- | --- |
| **Descent 1e** | Spawn nello spazio che gli eroi NON vedono (anche un dead-end appena controllato): la fog-of-war E' il permesso di spawn. | Accoppia spawn ai reveal + LOS: nessun corridoio "pulito e sicuro". Prerequisito = LOS (oggi assente). |
| **Descent 2e** | Tassonomia terreno con verbi distinti (lava/hazard end-turn-defeat, pit isola+blocca-LOS, water 2-move, sludge speed-cap, obstacle blocca-move+LOS, elevation blocca-move-non-LOS, crumbling one-shot); LOS corner-to-corner. | Palette diretta per il generatore di `terrain_features`. Evo-Tactics ha gia' hazard-DOT, elevation +/-1, move-cost, defense_mod; manca la VARIETA' di verbi e la densita'. |
| **Gloomhaven** | Door-tile reveal = piazza overlay + mostri + loot in un solo evento; pressure-plate (occupa-a-fine-turno -> apre porta o spawna); porte chiuse = muri finche' non scatta una condizione; scaling per formula L (livello) + C (n. personaggi). | Il "reveal = encounter" e' il pattern piu' trasferibile. Le formule L+C = template per la difficolta' parametrica (sez. 5). |
| **Frosthaven** | Hazard-terrain damage = `1 + ceil(scenario_level/3)` (hazard che scala col livello, non solo col count); layout nascosto oltre la prima stanza ma roster/terrain-count noti a monte. | Template pronto per lo scaling hazard del biome-clock. "Roster noto, layout nascosto" = utile per co-op leggibile. |
| **Imperial Assault** | THREAT DIAL: +N threat ogni round, SPENDI threat per deployare un gruppo (costo pieno) o rinforzare una figura (costo ridotto) a "green deployment points" fissi. | Modello piu' pulito per una "biome-pressure dial" tunabile dal backend: un knob di escalation invece di wave scriptate. |
| **Massive Darkness** | Door-card reveal spawna mob+loot; mob attivano DUE volte; roaming monster; enemy level = livello dell'eroe piu' alto; Shadow Mode (zone chiare/scure = layer stealth). | Shadow Mode -> layer visibilita' bioma (canopy/spore-fog/giorno-notte). Enemy-level = highest-hero -> difficolta' parametrica. |
| **Maladum** | Doom accumulator: l'intensita' degli eventi cresce piu' i giocatori temporeggiano. | Il "biome survival clock": temporeggiare = punito. |
| **XCOM 2** | Pod activation (gruppi dormienti che si svegliano su avvistamento/colpo); concealment come stealth-minigame; "plot-and-parcel" procgen (macro hand-authored + parcel modulari con contenuto tattico); mission timer. | Pod = i `spawn_points`/waves esistenti riletti come dormienti. Plot-and-parcel valida constraint-placement+validation vs WFC libero. |
| **Into the Breach** | (CONTRO-ESEMPIO) 8x8 hand-authored APPOSTA; intent nemico completamente telegrafato; hazard-tile come kill-verb (spingi il nemico nel fuoco/acqua); objective = difendi-la-cosa-che-e'-il-tuo-vero-HP (la power-grid). | La disciplina anti-dead-space + "telegrafa la minaccia attiva". Objective legato a una meccanica, non "atmosfera sopra". |
| **Gears Tactics** | E-hole: portali di spawn a wave FINITE (3, poi auto-chiudono) sigillabili in anticipo (advance + granata); overwatch-cone come area-denial; kill-reward -> momentum. | Wave-close condition: "survive the biome" da attrito infinito a valvola-di-pressione risolvibile (raggiungi/distruggi il vent). |
| **Darkest Dungeon** | Torch/stress che cala a ogni passo; low-light moltiplica danno/accuracy/ambush. La traversata STESSA e' un hazard crescente. | Il bioma E' il torch-meter: pressione senza countdown gamey. Attrito/provisioning = spina della sopravvivenza. |
| **Battle Brothers** | Zone of Control (lasciare l'ingaggio = colpo gratis) + Overwhelm (essere circondato erode la difesa); morale/rout cascade. | Impedisce kiting infinito E stallo di linea -- i due fallimenti classici della mappa grande. Rout = win-condition non-attritiva. |
| **Divinity: Original Sin 2** | Superfici (fuoco/veleno/olio/acqua/elettrificato) che si DIFFONDONO, si COMBINANO e sono WEAPONIZZABILI: il terreno e' una risorsa contesa da entrambi i lati. | "Bioma come quarta fazione": lo spore-bloom Ferrospora come superficie che si diffonde/combina; trait evolutivi la trasformano da minaccia in TUO terreno. |
| **Lancer / Caves of Qud** | Speed-stat = quadretti per Move (costo azione fisso, risultato variabile); Multiple Legs = move-speed % che scala col LIVELLO della mutazione. | Il modello di movimento richiesto dal proprietario, letteralmente (sez. 4). |

---

## 3. Pattern di struttura per mappe grandi Evo-Tactics (concreto)

Ognuna di queste sezioni collega il pattern al SEAM reale di Evo-Tactics. Ground-truth combat (verificato nei
due doc reference): Godot-v2 = TileMap 2D flat, griglia quadrata, board 6x6..12x12; backend Game = balance
authority, batch-sim headless. Meccaniche esistenti: elevation (+/-1), cover (`defense_mod`, consumato SOLO da
Godot `terrain_reactions.gd`, non dal backend), hazard-DOT, move-cost (Dijkstra per-morfotipo, flag OFF default).
Assenti: LOS, biome-theming visivo, procgen tattico, wave-reveal coupling, clock di sopravvivenza.

### 3.1 Esplorazione / fog-reveal -- l'unita' atomica della mappa

**Pattern universale:** nessuno di questi giochi mostra la mappa grande tutta insieme. La board e' un grafo di
stanze/settori dietro porte/tile chiusi; un settore si "accende" (overlay terreno + mostri + loot piazzati
SIMULTANEAMENTE) solo quando un eroe apre la porta / calpesta il reveal-tile. **Il reveal E' l'encounter.**
Una board 12x12 giocata come campo aperto = uno slog; la stessa board come 5 stanze door-gated = 5 encounter.

**Fog-of-war = permesso di spawn** (Descent 1e): lo spawn avviene DOVE i giocatori non vedono. Combinato col
room-gating, il fronte esplorato e' sempre una superficie di minaccia viva -- niente "corridoio pulito".

**Su Evo-Tactics (concreto):**
- Partiziona un encounter grande in **biome sub-zone** (es. mappa Ferrospora = spore-vent basin -> canopy shelf ->
  corroded ridge) che si rivelano all'ingresso. Ogni reveal droppa `terrain_features` di quel settore +
  `spawn_points` di una wave + l'eventuale objective, in un solo evento.
- Questo **aggiorna direttamente il contratto `waves[].spawn_points` esistente**: oggi le waves sono consumate da
  `ReinforcementSpawner` ma NON accoppiate all'esplorazione. Accoppiale al sector-reveal e le mappe scarse
  hand-authored di oggi diventano una **reveal-sequence**.
- **Pod-activation (XCOM) come variante deterministica** ideale per la batch-sim headless: semina la mappa con
  gruppi dormienti keyati a LOS/prossimita'; i `spawn_points`/waves diventano pod che si svegliano sull'avanzata.
  Zero nuova complessita' AI, testabile con seed.
- **CAVEAT (dallo spec deferred, sez. 12): il primo passo reale della "resa" e' il binario VISIVO** (wire dei 5
  tileset biome rotti + fix difetti visivi), non il procgen. Il reveal-system e' data-layer e convive col pause di
  D-combat, ma la verifica visiva finale dipende dagli asset S1/S2 (`project_godot_visual_asset_pipeline`).

**Trappola della scelta finta** (BGDF design lore): mettere un tile coperto a ogni bordo aperto SEMBRA scelta ma
spesso non lo e' (ogni direzione rivela "il prossimo tile"). O pre-autori la struttura ramificata, o dai peek/scout
abilities cosi' il ramo porta informazione -- altrimenti l'esplorazione e' illusoria e i giocatori lo sentono.

### 3.2 Control point -- struttura interna che vale la pena contendere

**Pattern:** i rinforzi non hanno placement libero -- rientrano ancorati a punti fissi (edge, portali, deployment
token). IA: rinforzi "il piu' vicino possibile a un green deployment point"; Gloomhaven: "nearest empty hex".
Poiche' lo spawn e' ancorato, i giocatori possono spendere azioni per contendere/tenere l'anchor. **Negare
l'anchor = strozzare la wave.** Questo e' cio' che rende i control point meccanicamente reali invece che narrativi.

**Su Evo-Tactics (concreto):**
- Modella le **sorgenti di spawn del bioma (nidi, vent, portali) come token fissi sulla board** che continuano a
  rilasciare creature finche' i giocatori non raggiungono/distruggono/tengono l'anchor.
- Oggi l'`objective` in `EncounterDefinition` e' **solo una stringa narrativa**. Questo pattern la converte in un
  **goal spaziale seizabile** -- co-op friendly (splitta la squadra per tenere piu' anchor).
- **Control-point DECAY (TF2/Hardpoint): un punto che decade quando lo abbandoni** forza la tensione hold-vs-roam:
  su mappa grande non puoi tenere ogni nodo E esplorare -> devi scegliere (splittare la squadra co-op). Questa e'
  la conversazione tattica co-op che il single-player XCOM non ha, e giustifica la dimensione grande.
- Lega i control point ai 6 pillar: nodi biologicamente significativi (mutation pool, biomass well, scent-marker)
  che alimentano la loop di evoluzione/economia quando tenuti -> map-control legato alla progressione core.

### 3.3 Wave/spawn logic -- una push-economy separata dal reveal

**Pattern:** oltre allo spawn-on-reveal, serve una economia di PUSH per le wave continue, disaccoppiata dal reveal.
Il modello piu' pulito e' il **THREAT DIAL** (Imperial Assault): guadagni +N threat ogni round, poi l'AI SPENDE
threat per deployare un gruppo fresco (costo pieno) o rinforzare una figura in un gruppo esistente (piu' economico).
La wave e' un budget crescente e spendibile, tunabile dal designer, non uno script.

**Wave-close condition** (Gears E-hole): i vent emettono wave FINITE ma sigillabili in anticipo. Converte "spawn
infiniti" in una valvola risolvibile -- un objective spaziale che pretende l'avanzata, uccidendo il turtling.

**Point-budget spawn director** (TD wave theory): un manager spende un budget-punti crescente per wave sui tipi
nemico (swarm economico vs elite costoso), scalando la COMPOSIZIONE non l'HP (+20% HP a wave = il fallimento
HP-sponge di Gears Tactics, da EVITARE). Il budget puo' reagire allo stato della squadra (anti-snowball).

**Su Evo-Tactics (concreto):**
- Dai all'encounter un **budget di "biome pressure" per-round** (survival-flavored: il bioma diventa piu' affamato/
  ostile nel tempo). Spendilo per rilasciare la prossima wave agli anchor di spawn del bioma o rinforzare un pack
  esistente. E' il modello IA threat, ed e' esattamente cio' che una **batch-sim balance-authority** vuole: **un
  knob di escalation tunabile** invece di script wave bespoke, gate-abile dalla batch-sim AI-driven.
- **Riusa l'infra esistente come wave-director**: la batch-sim AI-driven E' gia' la balance authority; usala come
  point-budget director (spendi un "ecosystem pressure budget" sui tipi/specie per wave, scala composizione non HP,
  reagisci alla potenza squadra). Riuso, non bolt-on.
- **Wave-close via anchor**: sigillare un vent (control point, sez. 3.2) chiude la sua wave -> "survive the biome"
  da attrito infinito a valvola risolvibile, con win-state diverso dal total-clear.
- **Telegrafa lo spawn 1 turno prima** (emergence tiles a la Into the Breach): marca la cella-di-spawn prima che
  poppi, cosi' la squadra puo' pre-posizionarsi/bloccare/uccidere la cella. Il same-turn un-warned reinforcement e'
  la lamentela #1 di tedio (Fire Emblem forums). Anche in un sim d20 puoi telegrafare l'INTENT + le spawn-tile
  mantenendo to-hit/danno stocastici -- preservi l'identita' d20 uccidendo l'ambush "ingiusto".

### 3.4 Hazard tiles -- tassonomia tipizzata con verbi distinti

**Pattern (gold-standard = Descent 2e):** ogni hazard ha un VERBO diverso, non chip-damage generico.

| Hazard (Descent 2e) | Verbo | Effetto meccanico |
| --- | --- | --- |
| Lava / Hazard | punisci-la-sosta (letale) | 1 dmg all'entrata + SCONFITTA se finisci il turno li' |
| Pit | isola + blocca-LOS | 2 dmg all'entrata, non puoi spendere movimento dentro, LOS solo ad adiacenti |
| Water | rallenta | costa 2 movimento entrare |
| Sludge | speed-cap | +1 move a entrare E cappa la Speed a 1 |
| Obstacle | blocca-move + blocca-LOS | blocca ENTRAMBI |
| Elevation | blocca-move / permette-LOS | blocca movimento ma NON LOS (spari oltre una cengia che non attraversi) |
| Crumbling | one-shot | terreno che si risolve una volta e sparisce |

**Scaling** (Frosthaven): `hazard damage = 1 + ceil(scenario_level/3)` -- l'hazard morde di piu' col livello, cosi'
i party cauti sono puniti dal livello, non solo dal count.

**Superfici attive** (D:OS2 + Into the Breach): gli hazard che si DIFFONDONO/COMBINANO/sono WEAPONIZZABILI (spingi
il nemico nel fuoco, accendi l'olio su cui sta) sono il pattern a leva piu' alta -- il terreno risolve PRIMA degli
attacchi, creando gioco proattivo. Il "moving hazard front" (flood/spore-fire/fog tossica che avanza 1 tile/turno)
e' un soft-timer che restringe l'area sicura senza countdown gamey.

**Su Evo-Tactics (concreto):**
- Evo-Tactics **ha gia' le meccaniche** (hazard-DOT, elevation +/-1, cover `defense_mod`, move-cost field) ma i
  `terrain_features` sono **hand-authored e scarsi (2-3 celle)**. Adotta la tassonomia Descent come **palette del
  generatore**: acid-pool (end-turn severo), pit-analogo (isola + blocca-LOS), sludge-analogo (speed-cap), obstacle
  (blocca move E la LOS assente), elevation (blocca move, permette shoot-over). Piazzali DENSI con vincoli tattici
  (spawn-zone sgombere, reachability garantita, densita' hazard in banda). Questo e' il fill concreto per il gap
  "terrain_features scarse" flaggato nel map-generator doc.
- **Bioma come quarta fazione (keystone):** rendi l'hazard-signature di ogni bioma (spore-bloom Ferrospora, acid
  mire, thermal vent, flood tide) una **superficie attiva che si diffonde/combina** (a la D:OS2). Squadra e nemici
  se la contendono; i trait evolutivi (fire-immune, amphibious, spore-symbiote) la trasformano da minaccia in TUO
  terreno -> le scelte di evoluzione diventano tatticamente leggibili sulla mappa, servendo il pillar "survive the
  biome" + il pillar evoluzione.
- **CAVEAT ground-truth (dallo spec deferred, sez. 12):** il backend runtime legge OGGI solo `{x,y,type}`
  (`moveCost.terrainAtFromFeatures`); `defense_mod` e' dichiarato nello schema ma letto da ZERO codice backend; il
  cover e' consumato SOLO da Godot (`terrain_reactions.gd`). Un generatore che emette terrain-array NON attiva da
  solo cover/elevation lato backend: manca il terrain-glue (`computeTerrainModifier`/`getDefenderAdvantage` leggono
  `unit.terrain_type/elevation` ma nulla li popola dalla griglia). Il wiring hazard/cover backend e' un sotto-task a se'.

### 3.5 Survival pressure / timer -- l'orologio che tassa il temporeggiare

**Pattern:** un clock crescente e' l'antidoto a "mappa grande = lenta, cauta, noiosa". Maladum Doom e IA
threat-per-round rendono il TEMPO il nemico. Darkest Dungeon: la traversata stessa consuma torch + stress; low-light
moltiplica il danno. Into the Breach: survive-N-turns / difendi-le-building. Il turtling e' attivamente tassato.

**Moving hazard front come soft-timer** (modello Evacuation board-game / superfici D:OS2): un hazard-bioma che
avanza 1 tile/turno restringe continuamente l'area sicura -> niente turni morti, niente camping, pressione senza
un countdown punitivo a schermo.

**Su Evo-Tactics (concreto -- questo E' il pillar sopravvivenza):**
- **Il bioma E' il clock.** Ogni N round il bioma-hazard si intensifica (densita' spore su, hazard-damage su, nuovo
  spawn), cosi' "survive the biome" ha teeth e il turtling e' punito. La formula Frosthaven (`1 + ceil(level/3)`) e'
  un template pronto, scalato dalla difficolta' encounter fornita dal sim.
- **Moving hazard front come motore di pacing co-op:** un fronte-bioma che avanza a ogni round forza la squadra
  co-op a muoversi/adattarsi insieme e da' un timer di sopravvivenza naturale e non-gamey che si allinea al fantasy
  "survive the biome" -- senza il countdown esplicito che stona.
- **HEED THE COUNTER-EXAMPLE (Into the Breach / Burgun):** pilota la mappa piu' PICCOLA che supporti
  pod+hazard+objective, prova la densita'-di-decisione-per-tile nella batch-sim, e scala il tile-count solo quando
  ogni tile extra guadagna un reveal-beat, un tick-clock, o una decisione-hazard. Su co-op la leggibilita' e'
  doppiamente critica (piu' giocatori devono parsare una board).

### 3.6 Objective families -- oltre il "kill-all", sui 6 pillar

**Pattern:** "kill all enemies" e' il default; i designer notano esplicitamente che quando l'objective e' altro, la
MAPPA e' costruita apposta per distrarre e depistare. Famiglie: kill-all / kill-specific (boss/named) / escort
(proteggi un ally-token in movimento) / escape (raggiungi un edge, spesso inseguito dagli spawn) / plunder (loot
token, a volte in gara con l'AI) / hold-control (occupa token/plate). I token-objective portano numeri di
attivazione randomizzati (Gloomhaven) -> anche "prendi il loot" ha tensione d'ordine nascosta.

**Su Evo-Tactics (concreto, mappato sui 6 pillar):**
- Ruota: hold-the-nesting-site / escort-una-larva-al-pool-di-evoluzione / extract-biomass-prima-della-marea /
  survive-N-wave-dell'apex-predator / block-the-hive-emergence-tiles. Questo mappa pulito sul fantasy
  creature-evolution-survival e previene "ogni scontro e' defeat-all".
- **Objective in tensione (Into the Breach):** dai 2-3 objective in conflitto (survive-le-wave MENTRE tieni-un-punto
  MENTRE la marea-acida sale), cosi' ogni azione baratta un goal contro un altro -> il turno diventa una decisione.
- **Non-kill objective richiede decoy** (design lore): quando l'objective NON e' kill, il generatore deve piazzare
  hazard/loot esca per depistare -- un requisito concreto per la validation-pass del generatore.

---

## 4. Il modello di movimento trait-driven -- costo fisso, quadretti variabili

Questo e' l'intento verbatim del proprietario: **la spesa d'azione per muoversi e' la stessa per ogni creatura, ma
il risultato in quadretti cambia per mutazioni/trait**. E' un pattern con precedenti solidi e diretti, e si innesta
sul `MoveCostField` gia' esistente.

### 4.1 Il core: MOV-come-stat, azione a costo fisso -> tiles variabili

Una Move-action paga un costo-azione flat e risolve N tiles = lo stat di movimento della creatura. I build
differiscono SENZA cambiare l'action economy. Precedenti:

| Fonte | Meccanica | Nota |
| --- | --- | --- |
| **Lancer** | Speed-stat = tiles per Move; azione Boost; SIZE = footprint | Il modello piu' pulito: uno stat -> N tiles per la stessa azione. |
| **XCOM EU/2** | Mobility -> ~meta'-move (blu, tieni l'azione) vs dash (giallo, consuma il turno per ~2x reach) | Two-tier move: risolve "troppo lontano per agire" senza dare danno gratis. |
| **D:OS1** | Movement = distanza per AP, derivata da Speed (appiattito in D:OS2 per balance) | Precedente + monito: lo scaling per-stat va tarato o rompe il balance. |
| **Descent 2e** | Speed = pool di move-point per move-action; spendi Fatigue per move-point EXTRA fuori dallo slot-azione | Off-action resource: una riserva stamina/adrenalina che converte in tiles. |
| **Caves of Qud** | Multiple Legs = move-speed % che SCALA col livello della mutazione | Il movimento emerge dall'evoluzione, non dallo spendere piu' azioni. |

### 4.2 Come speccarlo per Evo-Tactics

**Cosa modifica i tiles-per-move (proposta di leve, da falsificare in brainstorming -- SDMG):**
- **Base MOV** per morfotipo/specie (lo stat di partenza).
- **Trait/mutazioni con scaling per tier** (Caves of Qud): +MOV per tier investito; long-limbs = +tiles / jump-gaps;
  wings = fly / ignora-terreno; burrow = attraversa-rock; aquatic = swim in biome-water a costo pieno-ridotto.
  Il movimento diventa un ASSE DI BUILD, non un numero piatto.
- **Off-action stamina/adrenalina pool (Descent Fatigue):** converte in tiles extra o un dash, flavor
  biome-survival (riserva metabolica) -> permette lo sprint a un control point a un costo, senza turni morti.
- **Two-tier move (XCOM):** single-move tiene l'azione d20 vs dash che la forfeita per ~2x reach (+ bonus
  evasione/difesa a la XCOM) -> la creatura in ritardo si riposiziona su mappa grande senza il turno morto
  "troppo-lontano-per-agire".

**Interazione col move-cost di terreno gia' esistente (load-bearing):**
- Il backend ha gia' `MoveCostField` (Dijkstra per-morfotipo + bypass volo, flag `MOVE_TERRAIN_COST_ENABLED` OFF di
  default). Il modello trait-driven si innesta cosi': **MOV = budget di move-point; il terreno CONSUMA move-point a
  tassi variabili** (trail = ridotto, rough/hazard = >1, superfici bioma = penalita'), e i trait modificano SIA il
  budget MOV SIA i tassi di consumo (fly/burrow/aquatic = bypass di specifici tipi terreno). Cosi' MOV-variabile e
  terrain-move-cost sono LO STESSO sistema: un pathfinding pesato dove il budget e i pesi sono funzione della build.
- **Effetto sul balance (vedi sez. 5):** MOV-come-tiles-variabili cambia la matematica di REACHABILITY per la
  balance-authority. Reachability e' esattamente cio' che la validation-pass del generatore verifica (flood-fill da
  ogni spawn). Un MOV/mutazione-scaling nuovo tocca reachability, cioe' tocca cosa e' "raggiungibile in K turni",
  cioe' tocca la tensione di ogni objective spaziale. Va ratificato N=40 (sez. 5), non N=10.
- **Auto-resolve dei turni no-choice (Defender's Quest speed-valve):** per la batch-sim, auto-risolvi i turni di
  puro movimento senza scelta (move-to-contact banale) e fai emergere solo i turni-decisione -> non bruci cicli sim
  su traversate triviali.

---

## 5. Accoppiamento a difficolta' / balance -- perche' xpBudget deve contare griglia+hazard+wave+objective, non solo area

Questa e' la sezione load-bearing per il ruolo backend-as-balance-authority. La ground-truth e' verificata sul codice.

### 5.1 Cosa conta OGGI il modello xpBudget (e cosa NON conta)

`apps/backend/services/balance/xpBudget.js` (+ config `data/core/balance/xp_budget.yaml`):
- **Conta**: XP dei nemici da `computeUnitXp` = `hp*2 + mod*8 + ap*6 + range*4 + guardia*5 + tier_bonus`, sommato su
  `waves[].units` + un worst-case del `reinforcement_pool` (`avgPoolXp * max_total_spawns`).
- **Scala per**: `encounter_class` (tutorial..boss, `budget_base` 80..600) x `party_size_modifier` (0.5..1.6).
- **Verdetto**: `ratio = used/budget` -> under / in_band / over / critical_over, con banda `out_of_band_pct` per classe.
- **Wiring**: solo un **warning log** a `/start` (`session.js:2734-2749`), non un gate bloccante.

**Cosa NON ha NESSUN termine (verificato):** area/dimensione griglia; densita' hazard; numero/tipo di control point;
tipo di objective (kill-all vs escort vs hold vs survive); accoppiamento wave-esplorazione; move-cost/reachability;
LOS. **Zero termini spaziali.** Il modello e' puramente "somma potenza nemici scalata per classe+party".

**L'audit doc stesso lo ammette** (`docs/balance/2026-04-25-encounter-xp-audit.md`, lettura-del-verdetto): il modello
e' una "baseline first-pass" che "usa stat aggregate ignorando action economy, pressure tier, hazard tiles,
AOE/bleeding" e "sotto-predice difficulty per scenari avanzati". Le calibrazioni empiriche mostrano delta importanti
(tutorial_02 modello "too_hard" ma winrate ~80%; tutorial_06_hardcore modello "too_easy" ma winrate ~85%).

### 5.2 Perche' la mappa Descent-style ROMPE questo gate

Una mappa "grande + hazard + control point + wave + survival clock" amplifica ESATTAMENTE tutte le variabili che
xpBudget non modella. Concretamente, la difficolta' reale di un encounter Descent-style e' funzione di almeno:
- **Area di griglia + reachability** (MOV-variabile per build): un boss su board 12x12 puo' perdere turni a
  manovrare (l'action-economy che l'audit gia' segnala come sotto-predetta) -> l'area MODIFICA la potenza effettiva.
- **Densita' e verbo hazard**: un choke obbligato-su-lava vale molto piu' XP di 3 celle di chip-damage; il moving
  hazard-front e' un damage-source continuo non-catturato da nessun unit-XP.
- **Numero/decay di control point**: tenere N anchor mentre la wave-pressure sale e' un tax d'azione che scala col
  numero di anchor, non con l'XP nemico.
- **Tipo di objective**: escort/hold/survive-N cambiano radicalmente la difficolta' a parita' di roster (l'objective
  non-kill richiede la mappa costruita per depistare -> difficolta' spaziale, non di roster).
- **Wave accoppiate all'esplorazione + biome-pressure dial**: un budget di pressione crescente = un damage/threat
  source parametrico che oggi il `reinforcement_pool` cattura solo come worst-case flat.

**Conseguenza:** se il gate resta area-blind (o peggio, se qualcuno lo estende con un termine di sola area), sotto-
o sovra-stimera' sistematicamente la difficolta' delle mappe grandi. Il gate va esteso con termini per: banda
densita' hazard, conteggio/decay control-point, moltiplicatore per tipo-objective, e un termine per la biome-pressure
dial (rate di escalation) -- **non** un semplice fattore-area. L'area da sola e' un proxy sbagliato: 12x12 vuoto e'
piu' facile di 8x8 saturo di hazard e vent.

### 5.3 Cross-ref: il task xpBudget gate-drift (C:/dev/Game) e le implicazioni N=10 -> N=40

- **Task/gate**: l'audit xpBudget e' oggi un warning log non-bloccante (`session.js:2734`); il tuning raccomandato
  dall'audit doc (pesare i trait per categoria, aggiungere `pressure_modifier`, modellare action-economy) e' pending
  e non chiuso. Questo e' il "gate-drift" concreto: **il modello di difficolta' e la difficolta' REALE divergono, e
  la redesign Descent-style allarga la divergenza.** Prima di trattare qualsiasi mappa grande come "bilanciata", il
  gate va ri-parametrizzato sui nuovi termini spaziali sopra, ALTRIMENTI il verdetto in_band/over e' rumore.
- **Implicazione N-sample (guardrail globale, non-negoziabile):** ogni claim di ri-bilancio (nuovo termine hazard/
  objective/pressure nel gate, o nuovo scaling MOV/mutazione) e' un upgrade-claim su metrica. Il guardrail:
  **N=10 = direction-probe, N=40 = ratify.** Con mappe grandi la varianza per-run CRESCE (piu' hazard stocastici,
  piu' wave, piu' pathing) -> il CI95 a N=10 spannera' piu' facilmente la banda, quindi un N=10 "verde" NON e'
  ratifica: serve N=40 per chiudere. In pratica: probe a N=10 per direzione, poi ratifica a N=40 sulla batch-sim
  PRIMA di aggiornare `xp_budget.yaml` o i pesi di scaling.
- **SDMG (guardrail):** i nuovi termini del gate (hazard-density weight, objective-type multiplier, pressure-rate)
  sono metodo self-designed = ipotesi alto-errore. Pre-integrazione governance: falsificazione esterna
  (harsh-reviewer + game-design-validator), adozione narrow (flag/warn prima di gate bloccante), decider = specialista
  non euristico. Non promuovere un nuovo termine di gate a "verita'" su una calibrazione self-designed.

---

## 6. Decisioni di design aperte per il proprietario (numerate)

1. **Grande quanto, e con quale substrato?** Per-cella (Descent/Gloomhaven/XCOM) vs zone-based (Massive Darkness:
   muovi zona-a-zona, "spawn nella prossima zona"). Le zone tagliano drasticamente la fiddliness su mappa grande e
   rendono economico ragionare su reveal/spawn -- fallback utile se il per-tile d20 diventa troppo lento nella
   batch-sim. Piloto la mappa piu' piccola che supporta pod+hazard+objective (Into the Breach thesis) o punto subito
   a "grande"?
2. **Reveal-gating: pre-autorato o procedurale?** Struttura ramificata hand-authored (scelte reali, controllo) vs
   generata (varieta' batch-sim, rischio scelta-finta). Data lo spec DEFERRED (fork A "mappe brutte da guardare" +
   binario visivo prima del procgen), il reveal-system entra come data-layer o si aspetta il visivo?
3. **LOS: dentro o fuori dal primo scope?** LOS e' il PREREQUISITO che gli altri pattern assumono (fog=spawn-permit,
   cover, ambush, Shadow Mode). Ground-truth: `getLineOfSight` esiste nel backend ma e' HEX-native (`hexGrid.js:175`)
   e il combat e' a griglia QUADRATA -> e' un PORT di algoritmo (Bresenham), non "wiring firma-invariata"; Godot non
   ha LOS -> parita' cross-repo = drift-trap. Lo scopo come sotto-progetto a se' (raccomandato) o si taglia?
4. **Biome-pressure dial vs wave scriptate?** Il threat-dial (IA) e' un knob singolo tunabile dalla batch-sim; le
   wave scriptate sono piu' autorabili ma bespoke. Quale come modello primario per "wave di nemici da tenere sotto
   controllo"?
5. **Survival clock: moving-hazard-front o escalation-scaling?** Fronte-hazard che avanza (spaziale, leggibile,
   co-op-forzante) vs scaling crescente a la Frosthaven (piu' semplice, meno spettacolare). O entrambi?
6. **Control point: quanti, e con decay?** Il decay forza hold-vs-roam e split co-op ma alza il carico cognitivo su
   mappa grande. Quanti anchor per mappa, e decadono?
7. **Objective families: quali dei 6-pillar per primi?** hold-nest / escort-larva / extract-biomass /
   survive-apex-waves / block-emergence. Quale set entra nel primo taglio, e con quale objective-type-multiplier nel gate?
8. **MOV trait-driven: quali leve nel primo taglio?** Base-MOV + trait-scaling (Caves of Qud) e' il minimo; off-action
   stamina (Descent) e two-tier dash (XCOM) sono additivi. Quali entrano subito e quali sono stretch? (Ricorda: ogni
   leva MOV tocca reachability -> ratifica N=40.)
9. **Estensione del gate xpBudget: warn o block?** I nuovi termini spaziali entrano come warning (come oggi) o come
   gate bloccante? E chi e' il decider della calibrazione (specialista, non euristica -- SDMG)?
10. **Dove vive il tutto: backend Game (authority, batch-sim, testabile headless) o client Godot (iterazione
    visiva)?** Lo spec deferred propendeva backend (parita' sim-vs-gioco); il fork-A visivo di Eduardo spinge prima
    il render Godot. Conferma la sequenza (visivo -> data-layer) o inverti?

---

## 7. Fonti (URL reali)

### Board tactical crawler (big-map structure)
- Descent 1e -- spawn dove gli eroi non vedono: https://tvtropes.org/pmwiki/pmwiki.php/TabletopGame/DescentJourneysInTheDark
- Descent 2e terrain taxonomy: https://descent2e.fandom.com/wiki/Terrain
- Descent 2e line of sight (corner-to-corner): https://descent2e.fandom.com/wiki/Line_of_sight
- Descent 2e overlord card economy: https://descent2e.fandom.com/wiki/Overlord_Card
- Descent 2e secret room (reveal-on-entry): https://descent2e.fandom.com/wiki/Secret_Room
- Descent 2e Fatigue -> move-point off-action: http://www.descentinthedark.com/_f_/fatigue.php
- Gloomhaven special scenario rules (pressure plates, locked doors, spawn nearest hex, L+C scaling): https://www.ultraboardgames.com/gloomhaven/special-scenario-rules.php
- Gloomhaven monster spawning timing: https://rules.dized.com/game/I7lEsCGOS2-zgol-ZRNf3g/6Fg7QjLbS9-8B0d3MpB-lw/tKCRa-gKRFymqzeEKZTNFw/monster-spawning
- Gloomhaven corner-to-corner LOS: https://steamcommunity.com/app/780290/discussions/0/1741134753983139907/
- Frosthaven hazardous terrain + section reveal: https://boardgamegeek.com/thread/3084979
- Imperial Assault threat dial (campaign rules): https://www.ultraboardgames.com/star-wars-imperial-assault/campaign-mode-rules.php
- Massive Darkness roaming monster + door-card reveal + level scaling: https://massive-darkness.fandom.com/wiki/Roaming_Monster
- Massive Darkness Shadow Mode (light/dark tactical layer): https://www.kickstarter.com/projects/cmon/massive-darkness/posts/1605776
- Maladum Doom accumulator (review): https://playerelimination.com/2024/11/11/the-form-of-dungeon-crawling-a-maladum-dungeons-of-enveron-review/

### Video-game tactical (pods, clocks, terrain-as-mechanic)
- Into the Breach (Wikipedia): https://en.wikipedia.org/wiki/Into_the_Breach
- Into the Breach -- reimagining failure (Game Developer): https://www.gamedeveloper.com/design/reimagining-failure-in-strategy-game-design-in-i-into-the-breach-i-
- Into the Breach tiles/environments: https://intothebreach.fandom.com/wiki/Tiles + https://intothebreach.fandom.com/wiki/Environments
- Into the Breach -- dynamic puzzles / small-map thesis: https://blogofarcanesecrets.wordpress.com/2018/03/09/into-the-breach-and-dynamic-puzzles/
- XCOM 2 concealment: https://www.ufopaedia.org/index.php/Concealment_(XCOM2)
- XCOM 2 pod/enemy-intro analysis: http://www.vigaroe.com/2020/05/xcom-2-analysis-general-enemy-intro.html
- XCOM 2 plot-and-parcel procgen (GDC): https://gdcvault.com/play/1025387/Plot-and-Parcel-Procedural-Level
- XCOM 2 plot-and-parcel (coverage): https://gamerant.com/xcom-2-procedural-level-detail/
- Gears Tactics (Wikipedia): https://en.wikipedia.org/wiki/Gears_Tactics
- Gears Tactics E-holes/overwatch tips: https://steamcommunity.com/sharedfiles/filedetails/?id=2650428501
- Darkest Dungeon light meter: https://darkestdungeon.fandom.com/wiki/Light_Meter
- Darkest Dungeon expedition/traversal: https://darkestdungeon.wiki.gg/wiki/Expedition
- Battle Brothers tactical combat mechanics: https://battlebrothersgame.com/tactical-combat-mechanics/
- Battle Brothers combat mechanics (ZoC/Overwhelm/morale): https://battlebrothers.fandom.com/wiki/Combat_Mechanics
- Wildermyth combat mechanics (flanking/destructible terrain): https://wildermyth.com/wiki/Combat_mechanics
- Divinity: Original Sin II surface/environmental combat: https://www.thegamer.com/best-environmental-hazards-weapons-games/

### Movement (fixed-cost -> variable-tiles, evolution-coupled)
- XCOM EU Mobility -> tiles: https://www.ufopaedia.org/index.php/Movement_(EU2012)
- XCOM 2 blue-move vs yellow-sprint: https://www.gamepressure.com/xcom2/movement/za848f
- D:OS1 Speed -> movement distance: https://divinityoriginalsin.wiki.fextralife.com/Speed
- D:OS2 AP design note (flattened per-Speed): https://divinity.fandom.com/wiki/Original_Sin_2_Action_Points
- Lancer rules (Speed = tiles/Move, Boost, SIZE): https://lancer-rules.carrd.co/
- Gloomhaven game rules (per-class Move, Jump/Fly ignore terrain): https://www.ultraboardgames.com/gloomhaven/game-rules.php
- Caves of Qud Multiple Legs (move-speed % scaling con mutation level): https://wiki.cavesofqud.com/wiki/Multiple_Legs
- Freeciv/terrain move-cost model (roads 1/3, rough >1): https://strategygamestudio.com/sgs-rules/maps/terrain-types-and-effects/

### Design theory (pacing, telegraphing, wave-direction, procgen)
- Patatas -- The Dungeon Crawler Recipe (never let players breathe): https://www.gamedeveloper.com/design/the-dungeon-crawler-recipe
- Skeleton Code Machine -- what makes a dungeon crawl good: https://www.skeletoncodemachine.com/p/what-makes-a-dungeon-crawl-good
- BGDF -- fake-choice vs real-choice tile reveal: https://www.bgdf.com/forum/game-creation/design-theory/dungeon-crawler-mechanic
- Keith Burgun -- solving major problems in TB tactical wargames: http://keithburgun.net/solving-some-major-problems-in-turn-based-tactical-wargames/
- Sinister Design -- 12 ways to improve TB RPG combat: https://sinisterdesign.net/12-ways-to-improve-turn-based-rpg-combat-systems/
- Enemy attacks and telegraphing (Game Developer): https://www.gamedeveloper.com/design/enemy-attacks-and-telegraphing
- Cogmind -- roguelike level design (entrance/exit, loops, dead-space): https://www.gridsagegames.com/blog/2019/03/roguelike-level-design-addendum-procedural-layouts/
- Cogmind -- static among procedural (interest-curve pacing): https://www.gridsagegames.com/blog/2019/03/roguelike-level-design-addendum-static-procedural/
- Defender's Quest / Doucet -- FOCUS+THINKING pacing (time control, speed-valve): https://www.fortressofdoors.com/optimizing-tower-defense-for-focus-and-thinking-defenders-quest/
- Wave-spawn design (staggered arrivals, protect-target anchors): https://craftmygame.com/features/wave-spawn
- NEAT wave generation (adaptive point-budget spawn director): https://www.open-access.bcu.ac.uk/13568/1/A_NEAT_Approach_to_Wave_Generation_in_Tower_Defense_Games___IMET.pdf
- Fire Emblem same-turn reinforcements debate (telegraph vs ambush): https://www.neogaf.com/threads/fire-emblem-if-please-intelligent-systems-removes-same-turn-reinforcements.1022797/
- Evacuation board-game (rising-hazard-front pacing model): https://games4sustainability.org/gamepedia/evacuation-board-game/
- The metrics of space -- tactical level design: https://www.gamedeveloper.com/design/the-metrics-of-space-tactical-level-design
- TF2 control point (contest/decay mechanics): https://wiki.teamfortress.com/wiki/Control_Point_(game_mode)

### Ground-truth repo (Evo-Tactics)
- Stato combat Godot-v2 + technique register: `docs/research/2026-07-02-dungeon-alchemist-design-patterns-map-generator.md`
- Spec generatore mappe (DEFERRED + correzioni fattuali sez. 12): `docs/superpowers/specs/2026-07-02-evo-tactics-combat-map-generator-design.md`
- xpBudget engine: `C:/dev/Game/apps/backend/services/balance/xpBudget.js`
- xpBudget config: `C:/dev/Game/data/core/balance/xp_budget.yaml`
- xpBudget audit (ammette hazard/action-economy ignorati): `C:/dev/Game/docs/balance/2026-04-25-encounter-xp-audit.md`
- xpBudget warning-log wiring: `C:/dev/Game/apps/backend/routes/session.js:2734-2749`

---

## 8. Decisioni ratificate (Eduardo, 2026-07-03)

Le 10 decisioni della sez. 6, decise via AskUserQuestion. Definiscono la DIREZIONE dell'arco redesign;
il primo slice implementabile va comunque scopato (brainstorm -> writing-plans) -- non si costruisce
tutto in un colpo.

| # | Decisione | Scelta |
| --- | --- | --- |
| D1 | Substrato + scala | **Per-cella, parti-grande subito** (destinazione big diretta) |
| D2 | Reveal-gating | **Ibrido plot-and-parcel** (macro hand-authored + parcel modulari generati) |
| D3 | LOS | **DENTRO il primo scope** (port getLineOfSight hex->square nel backend + parita' Godot) |
| D4 | Modello wave | **Threat/pressure dial** (Imperial Assault -- knob di escalation tunabile) |
| D5 | Survival clock | **ENTRAMBI** (moving-hazard-front + escalation-scaling Frosthaven) |
| D6 | Control point | **1-2 anchor + DECAY** (hold-vs-roam, split co-op) |
| D7 | Objective families | **Tutte e 4** (survive-apex-waves / hold-control-anchors / extract-biomass / block-emergence) **+ ricerca trigger naturali/lore-driven per campagna+tratti** (addendum dedicato) |
| D8 | MOV trait-driven | **Tutte e 3 le leve** (base-MOV+trait-scaling / off-action stamina / two-tier dash) |
| D9 | Gate xpBudget | **Warn poi promuovi** (staged: warn -> calibra N=40 -> block; SDMG) |
| D10 | Dove vivono i sistemi | **Sequenza: slice VISIVO -> poi sistemi BACKEND** (rispetta fork-A visivo come primo passo, poi sistemi dove devono stare per la parita' sim) |

**Tensione da gestire nel design (flag onesto):** D1 (parti-grande) + D5 (entrambi i clock) + D7 (tutte le
objective) + D8 (tutte le MOV leve) = un primo-cut molto ambizioso, in tensione con la thesis del report
("pilota la mappa piu' piccola che regge, guadagna ogni tile"). La direzione e' ratificata; il **primo
slice** dovra' comunque essere un sottoinsieme coerente e costruibile -- il candidato per sequenza D10 =
(1) slice visivo (tile biome + camera #585 gia' fatta), poi (2) LOS (D3, il prerequisito), poi i sistemi
uno alla volta. Da definire in brainstorm/writing-plans.

**Addendum CONSEGNATO:** ricerca "trigger naturali/lore-driven per campagna + tratti" (da D7) ->
`docs/research/2026-07-03-lore-driven-triggers-campaign-traits.md`. Tesi: modella lo STATO ECOLOGICO
del bioma + resolver che lo legge -> mappa + obiettivo + trigger-tratto = 3 output dello stesso stato;
trait-unlock = conditional-record (exposure/hazard-survival/signature-behavior), non counter; 10 guardrail
anti-grind; 8 domande di design aperte (sez.6 dell'addendum).
