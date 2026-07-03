# Reference Addendum -- Trigger naturali / lore-driven / emergenti per campagna + tratti/evoluzione (Evo-Tactics)

> Addendum a `docs/research/2026-07-03-big-map-tactical-design-reference-evo-tactics.md` (decisione D7: famiglie di obiettivi + richiesta owner di trigger naturali/lore-driven per campagna e tratti). Documento di RIFERIMENTO, non un piano. Le formule e i mapping sono ipotesi ad alto errore (SDMG / quality-gate): richiedono falsificazione esterna + batch-sim N-sample prima di governare la progressione.

---

## 1. TL;DR

Sei giochi indipendenti (Wildermyth, RimWorld, Darkest Dungeon, Crusader Kings 3, Battle Brothers, Dwarf Fortress) convergono su una tesi unica: **non si scrivono gli obiettivi -- si scrive un piccolo set di VARIABILI DI STATO + un resolver che legge quello stato e FA PARTIRE contenuto quando soglie/azioni vengono colpite.** La "quest" e una lettura emergente della simulazione, non un nodo scriptato.

Due paradigmi di innesco dominano, e sono complementari:

1. **On-Action hook (CK3)** -- la simulazione emette gia eventi di dominio (nascita, morte, kill, mutazione, biome-entered); il contenuto si AGGANCIA con gate di trigger a basso costo. Nuovo contenuto = aggiungi un listener, mai toccare la sim.
2. **Budget/pressure resolver (RimWorld)** -- uno scalare di "minaccia" e calcolato dallo stato del mondo (ricchezza/pop/tempo-dall-ultimo) e SPESO su una tabella pesata di incidenti.

Il significato nasce da **tre moltiplicatori** stratificati sopra:

- **Persona-fit** -- il trigger legge i tratti dell'attore, quindi lo stesso evento atterra diverso (CK3 `stress_impact`, DD affliction-history).
- **Persistence** -- gli esiti riscrivono irreversibilmente il personaggio/mondo e diventano INPUT di trigger futuri (Wildermyth benda/figlio, DD quirks).
- **Pacing** -- un layer di ritmo che garantisce valli di recupero (RimWorld on/off, Wildermyth anni-di-pace tra capitoli).

**Per Evo-Tactics nello specifico:** modella lo STATO ECOLOGICO del bioma (densita predatore/preda, deplezione risorse, stagione, contaminazione) come sorgente-budget stile RimWorld; emetti on-action su CREATURA/EVOLUZIONE (mutation-gained, trait-expressed, apex-killed, biome-entered) come superficie-hook stile CK3; e lascia che **gli obiettivi delle combat-map e gli sblocchi di tratti siano LETTURE di quello stato** invece di "kill N" scriptati. Il map generator emette gia dati deterministici seed-based: estendi la STESSA pipeline di stato perche emetta anche l'obiettivo, cosi mappa + goal sono un'unica lettura coerente.

Sul lato tratti, il pattern real-game piu forte e **"evoluzione-come-record-condizionale"** (Pokemon, Niche, Caves of Qud, SMT): un tratto scatta quando una condizione leggibile in-fiction e soddisfatta -- esposto a un bioma, sopravvissuto a una pressione, eseguito un comportamento-firma, raggiunta una soglia di relazione/lore -- NON quando un contatore raggiunge un numero. Regola anti-grind unificante dalla letteratura roguelite: i migliori sblocchi **cambiano l'albero decisionale, non alzano la capacita**.

---

## 2. Tabella trigger-pattern (gioco -> trigger naturale/lore -> innesto Evo-Tactics)

| Gioco | Trigger naturale / lore / emergente | Innesto su Evo-Tactics (campagna / tratti / obiettivi) |
|---|---|---|
| **Crusader Kings 3** | On-Action architecture: il codice emette azioni di dominio (`on_birth_child`, `on_death`, `on_title_gain`) + pulse periodici; il contenuto si aggancia con `trigger{}` / `weight_multiplier{}`; `stress_impact` lega la scelta-opzione ai tratti dell'attore | **Event bus della sim**: emetti `mutation_gained`, `trait_expressed`, `apex_predator_killed`, `biome_entered`, `creature_starved`, `contamination_crossed_threshold`. Obiettivi/lore/unlock si REGISTRANO come listener economici con gate. Nuovo contenuto = nuovo listener, la sim non cambia |
| **RimWorld** | AI Storyteller come resolver a BUDGET: raid points da wealth+pop+animali+edifici, modulati da adaptation-factor (morti/ferite recenti) e tempo-dall-ultima-minaccia, spesi su tabella pesata; la personalita dello storyteller = curva di pacing (Cassandra crescente / Phoebe 8-on-8-off / Randy caos) | **ecology_pressure budget**: `f(party_evolution_level, biome_resource_depletion, predator_density, turns_since_last_event, recent_deaths as damper)` speso su tabella pesata di encounter-seed/obiettivi. wealth->raid mappa su evolution-power->biome-response: il bioma "nota" un party forte ed escala. Wrappa in un pacing governor con intervalli-di-pace |
| **Darkest Dungeon** | Stress come scalare-trigger emergente (crit, curio, interazioni party -> 100 -> affliction check); **Affliction History** = persistenza per-eroe (lo stesso eroe si rompe allo stesso modo); quirks alimentano il metagame di citta. Fonte canonica di PITFALL (RNG punitivo, roster-grind, time-disrespect) | Tratti/reazioni che leggono la storia della creatura: la stessa "predator ambush" atterra come `evade` per una stealth-mutation, come `hunt-back` per un aggression-trait (e NON cacciare costa instinct-stress). Ogni write-back persistente deve gatare/pesare almeno un trigger futuro |
| **Wildermyth** | "String of pearls" modulare: beat autorati con slot riempiti da tratti/relazioni/storia del party, incastrati proceduralmente tra ancore-di-capitolo bloccate; gli esiti riscrivono permanentemente (benda, figlio, trasformazione) | **Pearls per lore/story beat**: TEMPLATE di beat autorati con slot riempiti da creature/tratti/cicatrici/relazioni reali del party, tra ancore-di-capitolo; gli esiti scrivono tratti persistenti che gatano beat futuri. Qualita autoriale + varieta combinatoria |
| **Battle Brothers** | Ambitions: obiettivi a medio termine OFFERTI da un pool filtrato per company+world state (e per cio che hai gia fatto); scalano da tutorial a storico; ignorarli decade il morale = accountability senza questline scriptata. Crisi late-game = buildup a due fasi (warning-sign) poi payoff | **Offered-objective pool**: offri 2-3 obiettivi filtrati per stato-mondo/party/evoluzione per intervallo, il party co-op sceglie il thread; decadi party-cohesion se ignorati. **Two-phase telegraph** su eventi ad alto rischio (avvistamenti/spore-spread poi payoff) |
| **Dwarf Fortress** | Substrato sistemico piu profondo: 500+ bisogni/skill/memorie per agente + ecologia (tier di fauna, megabestie attratte dalla prosperita della fortezza) + Legends mode; le storie emergono dall'interdipendenza sistemica, la prosperita stessa e il trigger che attrae minacce | **Prosperity-as-threat**: un party molto evoluto/di successo ATTRAE apex-encounter e biome-response come una fortezza ricca attrae draghi -- l'escalation e leggibile come conseguenza della crescita, non come difficolta arbitraria |
| **Pokemon** | Evoluzione condizionale: friendship>=220, time-of-day, oggetti-bioma (Moss Rock->Leafeon, Ice Rock->Glaceon, campo-magnetico->Magnezone), meteo (Sliggoo->Goodra sotto pioggia), held-item, mossa-conosciuta, comportamento-in-battaglia (Farfetch'd 3 crit), danno-subito (Basculin recoil) | **Biome-exposure / hazard-survival / signature-behavior**: combatti 3 map in swamp-tossico -> offerta poison-resistance; sopravvivi un combat su tile-lava/spore -> heat-callus; colpisci ripetutamente da concealment -> ambush-mutation. Il bioma / hazard / comportamento E il trigger, non un kill-counter |
| **Caves of Qud** | Mutation points + Unstable Genome (destabilizzazione -> draw 3-choose-1) + sorgenti-mutageno world-object (gamma moth, sparking baetyl, nectar injector, glowsphere) | **World-object mutagen**: piazza tile `Ferrospora bloom` / relic-antico su certe map; finire un fight adiacente triggera un mutation-draw. Raro, spaziale, discovery-gated -> sembra un ritrovamento, non un chore. **Post-map "evolution altar"**: 3-choose-1 dal pool che il tuo play ha sbloccato, gli altri bruciati |
| **Shin Megami Tensei / Nocturne** | Evoluzione demone gated su learn-all-skills + delta-livello (a volte defeat-boss-form); persona-mutation post-Rank-8; ultimate-persona P5R via Confidant maxato | **Mastery-completion gate (limitato)**: una creatura evolve solo dopo aver ESPRESSO tutti i suoi tratti tier-corrente in combat reale almeno una volta -- checklist finita che pacinga la crescita senza numero farmabile. Keystone-branch gated su story-beat (defeat biome-apex) |
| **Slay the Spire** | Reliquie a tier per SORGENTE-come-contesto: Boss-relic dai boss, Event-relic SOLO da certi esiti-evento, Shop, Elite; gate run-to-run (Neow boss-swap richiede milestone di run precedente) | **Lore-gated trait tree**: rami-keystone di mutazione esistono SOLO come esito di eventi narrativi, mai da grinding generico. La campagna resta l'autorita di pacing, non l'XP |
| **Noita** | Perk agli altari Holy Mountain (3-choose-1, gli altri svaniscono, reroll raddoppia) + interazioni emergenti perk x wand x elemento | **Draw-from-pool at safe-node**: al checkpoint map/campagna, 3-choose-1 dal pool sbloccabile; prenderne uno brucia gli altri. Scarsita + tradeoff rende ogni pick significativa |
| **Hades / Hades II** | Keepsake relationship-gated: regala Nectar a un NPC -> ricevi il keepsake; rank-up completando encounter mentre equipaggiato; keepsake speciali gated dietro story-completion | **Relationship/bond trigger co-op-native**: due creature di due giocatori che si proteggono ripetutamente sbloccano un tratto paired/symbiote. Trasforma il layer sociale co-op in sorgente-tratto meccanica unica al genere |
| **Niche** | Population-genetics reale: mutation-menu 1 gene/generazione al 50% ereditarieta, wanderer/rogue-male come gene-flow, selezione naturale clima/predatore tra biomi | **Gene-flow via rescue/recruit**: recuperare/reclutare una creatura selvatica inietta il suo tratto nel breedable-pool co-op. Esplorazione ed esiti non-letali diventano un verbo di acquisizione-tratto di prima classe |
| **Enter the Gungeon** | Lo sblocco AGGIUNGE l'item al POOL di drop invece di concederlo (discovery-gated, non garantito) | **Unlock-expands-pool**: battere l'apex di un bioma la prima volta aggiunge in permanenza la sua signature-mutation al draw-pool -- devi comunque incontrarla, resta una scoperta |

---

## 3. Stato-ecologia + comportamento + esiti-sopravvivenza -> SEED di obiettivi e beat (non quest autorate)

### 3.1 Il principio: l'obiettivo e una lettura, non un nodo

Il map generator gia emette dati deterministici seed-based (biome_id + seed). Il salto e **estendere la stessa pipeline di stato perche l'obiettivo sia derivato dalle stesse variabili ecologiche**, non appeso a mano. Cosi mappa e goal sono un'unica lettura coerente dello stato, e sono deterministici per seed.

### 3.2 Le variabili di stato ecologico (sorgente-budget stile RimWorld)

Modella per-bioma (valori continui 0-1 salvo dove indicato):

- `predator_density`, `prey_density`
- `resource_depletion` (deplezione risorse locali)
- `contamination` (carico spore/Ferrospora)
- `season` (categoriale) + eventuale `season_phase`
- derivati di party: `party_evolution_level`, `turns_since_last_event`, `recent_deaths` (damper adattivo)

### 3.3 State-threshold seeding (obiettivi come letture di bande che si attraversano)

Gli obiettivi sono READ di variabili continue che attraversano bande, non nodi autorati. Esempi di mapping (illustrativi, da falsificare):

- `prey_density < 0.2` -> auto-seed "famine migration": raggiungi l'abbeveratoio prima dell'apex
- `contamination > 0.6` -> compare "purge the spore-node"
- `predator_density` alto + `party_evolution_level` alto -> "apex incursion" (prosperity-as-threat)
- `season == die-off` -> "out-survive the bloom" / escort-migration

### 3.4 Ecology-pressure budget (analogo raid-points)

Calcola uno scalare e SPENDILO su una tabella pesata di encounter-seed/obiettivi:

```
ecology_pressure = f( party_evolution_level,
                      biome_resource_depletion,
                      predator_density,
                      turns_since_last_event )
                   dampened_by recent_deaths          # adaptation-factor
```

Il mapping wealth->raid di RimWorld (interpolazione: ~14k wealth -> 0 pt, 400k -> 2400 pt, 1M -> cap 4200 pt, piu contributi da pop/animali/edifici al 50% e adaptation-factor su morti/ferite recenti) e il riferimento strutturale diretto: **evolution-power sostituisce wealth**, il bioma "risponde" a un party forte. Wrappa nel pacing governor (sotto).

### 3.5 Pacing / rhythm layer (valli obbligatorie)

Avvolgi ogni firing in un governor di ritmo che garantisce finestre di recupero e time-skip inter-capitolo (RimWorld on/off cycles + Wildermyth anni-di-pace). Le valli sono DOVE i write-back persistenti (invecchiamento, ritiro, prole, consolidamento-mutazione) vengono narrati. Pressione senza valli = grind (il fallimento di DD).

### 3.6 Two-phase telegraph

Eventi ad alto rischio (apex incursion, spore bloom, die-off stagionale) sparano prima una fase WARNING-SIGN economica (piu avvistamenti-predatore, eventi spore-spread, shift meteo) e poi il payoff. Il telegrafo converte "spike casuale" in "una storia che ho visto arrivare" -- e questo e gran parte di cio che fa sembrare autorata l'emergenza (Battle Brothers ha risolto le crisi late-game esattamente cosi).

### 3.7 Lore/story beat come pearls

Beat autorati come TEMPLATE con slot riempiti da creature/tratti/cicatrici/relazioni reali del party, incastrati tra ancore-di-capitolo bloccate; gli esiti scrivono tratti persistenti che gatano beat futuri (Wildermyth). Mantiene qualita autoriale con varieta combinatoria; la campagna resta l'autorita di pacing.

---

## 4. Sblocchi tratto/evoluzione guidati da cosa e successo nel play + guardrail anti-grind

### 4.1 Tre layer di trigger (naturale / lore / emergente)

**A. Naturali / ecologici** (adatta la creatura alla nicchia):

- **Biome-exposure mutation** -- tratto dopo N encounter sopravvissuti IN un bioma (Pokemon location-evo: Moss Rock->Leafeon; Niche selezione clima). *Evo:* 3 map in swamp-tossico -> offerta poison-resistance.
- **Environmental-hazard survival** (behavior-scored) -- il tratto scatta dal SOPRAVVIVERE a una pressione, usando il danno/effetto stesso come condizione (Basculin >=294 HP da recoil; Sliggoo->Goodra solo mentre piove). *Evo:* sopravvivi un combat intero stando su tile lava/spore -> heat-callus.
- **Feeding / prey-diet** -- cosa la creatura ha consumato plasma cosa diventa (Qud nectar injectors). *Evo:* un carnivoro che finisce N apex-prey sblocca un ramo predatorio; una dieta scavenger un ramo diverso -- la dieta e un fork di play-style, non un numero.

**B. Lore / relazionali** (gatano sblocchi di campagna):

- **World-object mutagen** (discovery) -- interagire con una sorgente rara destabilizza il genoma e OFFRE una scelta (Qud gamma moth/baetyl; Unstable Genome 3-choose-1). *Evo:* tile Ferrospora bloom; finire un fight adiacente -> mutation-draw.
- **Relationship / bond threshold** -- un tratto sblocca quando un bond attraversa una soglia raggiunta col play (Pokemon friendship>=220; Hades gift-Nectar poi rank-up-equipped; P5R Confidant maxato). *Evo:* due creature co-op che si proteggono a vicenda -> tratto paired/symbiote.
- **Story-beat / campaign-gate** -- mutazioni/obiettivi esistono SOLO come esito di eventi narrativi (Slay the Spire Event-relic; Hades keepsake story-gated; SMT defeat-boss-form). *Evo:* un ramo-keystone e bloccato fino al beat in cui affronti l'apex del bioma.

**C. Emergenti / sistemici:**

- **Signature-behavior / play-style record** -- il gioco osserva COME hai combattuto e sblocca il tratto corrispondente (flanking, difesa-alleato, mai-ritirata; Farfetch'd crit-streak). *Evo:* colpisci ripetutamente da concealment lungo la campagna -> ambush-mutation. Il trigger e un'identita dimostrata, quindi lo sblocco sembra guadagnato-dal-personaggio.

### 4.2 Selezione e scarsita

- **Draw-from-pool at safe-node** -- post-map "evolution altar": 3-choose-1 dal pool che il play ha sbloccato, gli altri bruciati (Noita Holy Mountain; Qud M-menu; StS boss-relic). Da al layer d20-tattico un beat di trait-selection pulito e ricco di tradeoff.
- **Unlock-expands-pool, not-grants** -- completare un obiettivo aggiunge il tratto al POOL possibile, non lo concede (Enter the Gungeon; StS Neow). La scoperta resta scoperta.
- **Mastery-completion gate (limitato)** -- evolvi solo dopo aver espresso tutti i tratti tier-corrente in combat reale almeno una volta (SMT learn-all-skills): checklist finita e leggibile, non barra-XP farmabile.
- **Gene-flow / immigration** -- nuovi geni entrano via creature selvatiche reclutate, non via shop (Niche wanderer/rogue-male). Esplorazione e mercy diventano il verbo di acquisizione-tratto.

### 4.3 Guardrail anti-grind (regole dure)

1. **No counter-with-a-skin.** Rietichettare "kill 20" come "assorbi 20 spore" e ancora grind se il numero e open-ended e any-map. Il trigger dev'essere una CONDIZIONE limitata o un FORK di play-style, non un tally.
2. **Counter-retirement.** Alla prima soddisfazione, aggiungi il tratto al POOL e ferma quello specifico trigger (Enter-the-Gungeon / StS). One-shot, discovery-gated -- se la stessa azione continua a pagare, i giocatori ottimizzano via il divertimento.
3. **Leggibilita.** Condizioni oscure (Pokemon "hold-item-di-notte-conoscendo-una-mossa") richiedono una wiki. I trigger in-fiction devono essere scopribili e suggeriti in-world (codex / ecology-tooltip), o leggono come RNG arbitrario.
4. **Agency obbligatoria.** Ogni trigger emergente ha bisogno di una leva-giocatore leggibile (mutazione/posizionamento/prep che sposta le odds), o e uno schiaffo-di-dado (il fallimento core di DD: affliction-recovery ~30-40% reject-gated leggeva come punizione arbitraria).
5. **Non-RNG puro** (cautela Rogue Legacy). Gli eredi ricevono tratti casuali scollegati dal parent: ottimo per varieta forzata, SBAGLIATO come sistema "guadagnato-da-cosa-hai-fatto". Serve causa->effetto leggibile dal giocatore.
6. **Bond qualitativi, non contatori.** Se la soglia-friendship e "cammina N passi", ricollassa in un counter. Lega i bond a eventi qualitativi distinti (salvato-da-morte, kill-condivisa) cosi ogni incremento e una memoria.
7. **No obsolescenza.** Progetta i trigger cosi che ogni nuova adattazione apra un nuovo PATH invece di dominare i vecchi (roguelite: non lasciare che il livello-10 renda inutile tutto prima del livello-8).
8. **Persistenza non-cosmetica.** Ogni write-back persistente deve gatare o pesare almeno un trigger futuro. Benda/cicatrice/quirk solo-flavor -> i giocatori imparano a ignorarli.
9. **No mandatory-trigger tax.** Se un trigger lore e l'UNICA via a un tratto necessario, mancare il beat softlocka una build. Fornisci un fallback draw (Noita reroll / Qud Unstable-Genome) cosi i trigger lore/emergenti sono la via FLAVORFUL, non un single-point-of-failure.
10. **Over-simulating trap** (Spore/Thrive). Un sim di pressione-ambientale pienamente emergente e difficile da autorare, leggere, e mantenere sotto controllo narrativo. Per un RPG a campagna, preferisci trigger conditional-record (Pokemon/Qud/SMT: if->then leggibile) alle selection-sim open-ended -- mantiene l'autorialita del pacing e della lore al designer.

---

## 5. Accoppiamento con i sistemi della descent-map (control-point / wave / hazard / survival-clock) + i 6 pilastri

> I sistemi della descent-map e le famiglie di obiettivi (D7) sono definiti nel documento base. Qui: come i trigger naturali/emergenti si innestano SUGLI STESSI sistemi, cosi che un solo pipeline di stato guidi mappa, obiettivo E tratto.

### 5.1 Innesto per sistema-mappa

- **Control-point** -> letti come nodi ecologici: un control-point puo essere un `spore-node` la cui `contamination` locale, se attraversa soglia, seed-a l'obiettivo "purge" ED e la sorgente-mutageno world-object (Qud). Tenere != tenere astratto: tenerlo scarica contamination e diventa un trigger di feeding/exposure.
- **Wave** -> non spawn arbitrari ma SPESA del `ecology_pressure` budget su tabella pesata (RimWorld). Il ritmo delle wave e il pacing governor; prosperity-as-threat modula intensita da `party_evolution_level`.
- **Hazard (tile)** -> doppia funzione: pressione tattica in-fight E condizione-trigger di hazard-survival (sopravvivere un combat su tile lava/spore -> heat-callus). L'hazard che il layout emette e lo stesso che il trigger legge.
- **Survival-clock** -> e il `turns_since_last_event` reso diegetico: piu regge il clock, piu il budget matura -> two-phase telegraph (warning-sign) prima del payoff-apex. Il clock e anche la valle-di-pacing quando si azzera (recovery window).

### 5.2 Un solo pipeline, tre output

```
STATO ECOLOGICO (per-bioma, seed-deterministico)
        |
        +--> MAP LAYOUT       (gia esistente: biome_id + seed)
        +--> OBJECTIVE        (nuovo: read delle stesse bande/soglie)
        +--> TRAIT-TRIGGER    (nuovo: on-action su exposure/hazard/feeding/behavior)
```

Mappa, obiettivo e trigger-tratto derivano dallo STESSO stato: coerenza garantita, determinismo per seed preservato, nuovo contenuto = nuovo listener.

### 5.3 Aggancio ai 6 pilastri (dal doc base)

I sei pilastri non sono ridefiniti qui; l'addendum indica **su quale pilastro ciascun pattern spinge**, come lente di verifica in review:

- **Tattica / posizionamento** <- hazard-survival trigger + control-point-come-nodo-ecologico (la leva-agency della regola anti-grind #4 vive qui).
- **Evoluzione / identita creatura** <- signature-behavior + biome-exposure + feeding (la creatura "diventa cio che ha fatto").
- **Co-op** <- relationship/bond trigger (paired/symbiote) + offered-objective pool condiviso.
- **Progressione / campagna** <- lore-gated trait tree + pearls + pacing governor con valli.
- **Leggibilita / fairness** <- two-phase telegraph + guardrail #3/#4 (scopribilita + agency).
- **Rigiocabilita / emergenza** <- ecology-pressure budget + prosperity-as-threat + draw-from-pool.

> Nota di verifica: prima di far governare la progressione a `ecology_pressure` o a qualsiasi formula-budget, applicare il quality-gate del progetto (smoke happy-path + >=3 edge case + >=1 tuning con delta) e il guardrail SDMG (falsificazione esterna: harsh-reviewer + batch-sim N-sample sul balance-loop reale, NON N=10). La formula e ipotesi, non decisione.

---

## 6. Domande di design aperte per l'owner

1. **Granularita dello stato ecologico**: quante variabili per-bioma sono il minimo che genera obiettivi leggibili senza diventare un sim Thrive-like ingovernabile? (pitfall #10). Partire da 4-5 (predator/prey/depletion/contamination/season) o meno?
2. **Determinismo vs live-state**: gli obiettivi seed-derivati devono restare 100% deterministici per seed (allineati al map generator), o lo stato ecologico deve MUTARE live durante la campagna (control-point tenuti scaricano contamination)? Il secondo rompe la pura riproducibilita per-seed.
3. **Autorita di pacing**: la campagna (pearls/chapter-anchor, Wildermyth) o il budget-resolver (RimWorld) e l'autorita primaria di ritmo? Convivono, ma chi vince in conflitto?
4. **Scala del roster persistente**: quanto piccolo dev'essere il roster co-op perche l'attaccamento sopravviva (evitare il roster-grind di DD)? La persistenza (cicatrici/mutazioni) ha valore solo se non churni unita usa-e-getta.
5. **Co-op e trigger relazionali**: i paired/symbiote-trait sono cross-player (creatura-di-A protegge creatura-di-B) o intra-roster? Il primo e piu unico al genere ma piu difficile da bilanciare in drop/leave co-op.
6. **Fallback anti-softlock**: quale draw-di-fallback (Noita reroll / Qud Unstable-Genome) copre i tratti keystone lore-gated, perche mancare un beat non softlocchi una build (guardrail #9)? Serve un pool-di-riserva sempre-accessibile?
7. **Telegrafo vs sorpresa**: two-phase telegraph su TUTTI gli eventi high-stakes, o mantenere una minoranza di sorprese non-telegrafate per tensione? (il telegrafo totale puo azzerare la paura dell'ignoto).
8. **Verbo di acquisizione-tratto primario**: il gene-flow via rescue/recruit (Niche) e un verbo di prima classe accanto al combat, o secondario? Impatta se esiti non-letali sono meccanicamente premiati.

---

## 7. Fonti (URL reali)

**Pattern campagna / obiettivi emergenti:**

- Wildermyth modular storytelling -- https://cjleo.com/blog/the-power-of-wildermyths-modular-storytelling-in-game-design/
- Darkest Dungeon affliction system (deep dive) -- https://www.gamedeveloper.com/design/game-design-deep-dive-i-darkest-dungeon-s-i-affliction-system
- Darkest Dungeon critique (RNG punitivo / grind / time-disrespect) -- https://thegemsbok.com/art-reviews-and-articles/darkest-dungeon-red-hook-critique-mechanics-design/
- CK3 dev diary 30 -- event scripting (MTTH -> on_action, stress_impact) -- https://forum.paradoxplaza.com/forum/threads/crusader-kings-3-dev-diary-30-event-scripting.1397140/
- CK3 event modding (on_action architecture, trigger/weight_multiplier, trait-gating) -- https://ck3.paradoxwikis.com/Event_modding
- Battle Brothers -- Ambitions (dev blog 89) -- https://battlebrothersgame.com/dev-blog-89-ambitions/
- Battle Brothers -- Late-Game Crises (dev blog 92, two-phase) -- http://battlebrothersgame.com/dev-blog-92-late-game-crises/
- RimWorld AI Storytellers (pacing curves) -- https://rimworldwiki.com/wiki/AI_Storytellers
- RimWorld Raid points (wealth interpolation + adaptation-factor) -- https://rimworldwiki.com/wiki/Raid_points
- Dwarf Fortress (agent sim, ecology, prosperity->megabeasts, Legends) -- https://en.wikipedia.org/wiki/Dwarf_Fortress
- Emergent gameplay principles -- https://gamedesignskills.com/game-design/emergent-gameplay/
- Emergent systems / ecology-shift quest seeding -- https://daydreamsoft.com/blog/emergent-gameplay-designing-systems-that-create-their-own-stories

**Pattern tratti / evoluzione condizionale:**

- Caves of Qud -- Mutations -- https://wiki.cavesofqud.com/wiki/Mutations
- Caves of Qud -- Unstable Genome -- https://wiki.cavesofqud.com/wiki/Unstable_Genome
- Caves of Qud -- Mutating -- https://wiki.cavesofqud.com/wiki/Mutating
- Caves of Qud -- mutation overhaul devlog -- https://freeholdgames.itch.io/cavesofqud/devlog/182472/mutation-overhaul-our-biggest-mutation-rebalance-ever
- Pokemon -- Methods of Evolution -- https://bulbapedia.bulbagarden.net/wiki/Methods_of_Evolution
- Pokemon -- Friendship Evolution -- https://bulbapedia.bulbagarden.net/wiki/Friendship_Evolution
- SMT -- Evolution (fandom) -- https://megamitensei.fandom.com/wiki/Evolution
- SMT -- Evolution (megatenwiki) -- https://megatenwiki.com/wiki/Evolution
- SMT -- Fusion -- https://megamitensei.fandom.com/wiki/Fusion
- SMT III Nocturne -- demon evolution guide -- https://samurai-gamers.com/shin-megami-tensei-iii-nocturne-hd-remaster/demon-evolution-guide/
- Slay the Spire -- Relics (fandom) -- https://slay-the-spire.fandom.com/wiki/Relics
- Slay the Spire -- Relics (wiki.gg) -- https://slaythespire.wiki.gg/wiki/Relics
- Noita -- Perks -- https://noita.wiki.gg/wiki/Perks
- Noita -- Holy Mountain -- https://noita.fandom.com/wiki/Holy_Mountain
- Hades -- Keepsakes -- https://hades.fandom.com/wiki/Keepsakes
- Rogue Legacy -- Traits (cautionary) -- https://roguelegacy.wiki.gg/wiki/Traits
- Rogue Legacy 2 -- Traits -- https://rogue-legacy-2.fandom.com/wiki/Traits
- Niche -- Mutations -- https://niche.fandom.com/wiki/Mutations
- Niche -- Genes -- https://niche.fandom.com/wiki/Genes
- Niche (Steam) -- https://store.steampowered.com/app/440650/Niche__a_genetics_survival_game/

**Meta-progressione / anti-grind (letteratura roguelite):**

- Roguelite meta-progression design -- https://bugnet.io/blog/how-to-design-a-roguelite-meta-progression
- Agency in roguelikes (make-or-break) -- https://thom.ee/blog/what-makes-or-breaks-agency-in-roguelikes/
- Roguelite progression respecting player time -- https://gamerant.com/roguelites-best-progression-systems-respect-your-free-time/
- Spore (scoping realismo del sim) -- https://en.wikipedia.org/wiki/Spore_(2008_video_game)
- Species: Artificial Life (real evolution) -- https://www.indiegogo.com/en/projects/jamieschumacher/species-artificial-life-real-evolution

---

*Verifica-fonti: alcune pagine (RimWorld Raid_points 403 su fetch diretto, CK3 dev-diary browser-check, gamedesignskills 403) sono state corroborate via wiki-mirror + search-snippet; la formula raid-points e i valori di interpolazione vanno riconfermati sulla wiki live prima di usarli come baseline numerica.*
