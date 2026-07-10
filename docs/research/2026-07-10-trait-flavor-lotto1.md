# Trait flavor -- Fase 1: template di voce, routing, lotto 1 (10 tratti)

- data: 2026-07-10 -- macchina: Ryzen (`DESKTOP-T77TMKT`)
- stato: **da curare da Eduardo**. Nessun testo committato.
- artefatti: `results/*.json` (5 arm), `scores_final.json`, `confirm.json`, `blind.md`,
  log `Extras/ollama-runs/2026-07-10-trait-flavor-eval.log`

> NB: questo doc contiene il **payload dati** (testo che finira' nei JSON i18n), quindi
> le voci dei tratti hanno accenti reali. La regola ASCII-first vale per la prosa `.md`,
> non per il testo di gioco -- confermato da `data/i18n/it/common.json`, UTF-8 con accenti,
> zero mojibake (verificato byte-level: 0 U+FFFD).

---

## 1. Correzioni alla ground-truth di partenza

Tre premesse del brief non reggono alla verifica. Contano tutte e tre.

**1. Il backing non e' `data/i18n/{it,en}` -- oggi e' `locales/it/traits.json`, e non e' vuoto.**
Esiste, e' tracciato in git, contiene **263 entry**. Lo scrive `scripts/sync_trait_locales.py`;
lo schema e' `config/i18n/trait_locales.schema.json`. `data/i18n/` contiene solo `common.json`.

**2. La copertura del 263/309 e' illusoria: oltre meta' e' boilerplate clonato.**

| campo | valori presenti | valori unici | in cluster duplicati |
| --- | --- | --- | --- |
| mutazione_indotta | 237 | 119 | 131 |
| uso_funzione | 237 | 125 | 122 |
| spinta_selettiva | 237 | 117 | 131 |
| debolezza | 182 | 70 | 122 |

Le frasi piu' frequenti compaiono **14 volte identiche** su tratti diversi
(`"Ottimizza scatti direzionali e transizioni rapide fra livelli verticali."`,
`"Suscettibile a disturbi elettromagnetici e saturazione sensoriale."`).
121 campi iniziano in minuscolo (frase troncata). Il testo autorato reale e' ~119 stringhe, non 237.

Gap effettivo vs 309 tratti: `label` 46, `mutazione_indotta`/`uso_funzione`/`spinta_selettiva` 72
ciascuno, `debolezza` 127. **EN: zero** (`locales/en/` non esiste).

**3. Il gioco oggi non parla per segnaposto: non parla affatto.**
Nessun runtime risolve `i18n:traits.*`. Il backend (`traitRepository.js:81`) usa il prefisso
solo per estrarre l'id via regex; `traitStyleGuide.js` lo valida come convenzione di naming.
`locales/it/traits.json` ha **zero lettori**. Godot non consuma prosa dei tratti.
Lo conferma la spec: *"Backend: nessun loader i18n reale (il prefisso `i18n:traits.*` e'
convenzione di naming, non runtime)"* -- `docs/design/evo-tactics-localization-i18n.md`.

> Conseguenza operativa: **310 voci curate, da sole, non fanno parlare il gioco.**
> Serve anche un PR di wiring (~10 righe) che importi il bundle in `apps/play/src/i18n.js`.
> Il contenuto resta il collo di bottiglia, ma il wiring va schedulato o il lavoro resta invisibile.

### Conflitto di SoT da dirimere (non l'ho deciso io)

`ADR-2026-06-08` (QA3) ratifica **`data/i18n` = sorgente unica, nessun secondo key-space**.
Ma `sync_trait_locales.py` + `tools/migrations/traits_styleguide_migration.py` scrivono in
`locales/`. Sono due key-space. Il validator `tools/py/validate_i18n_parity.py` fa glob su
`data/i18n/<locale>/*.json`: un file `data/i18n/{it,en}/traits.json` **entrerebbe nel gate
`npm run i18n:check` senza scrivere una riga di codice**. Vedi Domanda 2.

---

## 1-bis. CORREZIONE POST-REVIEW (dopo Codex su PR Game #3247)

**Questo doc, come scritto sotto, indica la fonte sbagliata del canone.** La review Codex sul PR ha
trovato che `zampe_a_molla` prometteva al giocatore un "balzo di riposizionamento" mentre il motore
concede `+1 danno da posizione sopraelevata con MoS >= 5`. Non era un caso isolato.

Gerarchia reale delle fonti, in ordine, per scrivere `uso_funzione`:

1. **Il modulo dedicato** `apps/backend/services/combat/<trait>.js` -- 12 dei 38 tratti autorati ne
   hanno uno, e spesso fa **di piu'** dello yaml (`membrane_osmotiche` cura anche 1 a fine round se
   adiacente ad acqua o palude; `tessuti_adattivi` ha un cap di 2 canali adattati insieme).
2. **`data/core/traits/active_effects.yaml`** (428 voci: `trigger` + `effect`) -- la regola meccanica.
3. **`data/core/traits/glossary.json`** -- **solo fallback**. E' metadata descrittivo, non canone:
   l'header di `active_effects.yaml` lo dichiara esplicitamente.

Costo dell'errore: **21 tratti su 38, 68 campi**. Due (`zampe_a_molla`, `legame_di_branco`) sarebbero
arrivati al giocatore su una schermata di *scelta*. Lo yaml ha anche incoerenze interne:
`mente_lucida.description_it` dice `MoS >= 3`, `trigger.min_mos` dice `5` -- vince il trigger.

**Regola dura aggiunta al template**: una `debolezza` non puo' asserire una meccanica che il motore non
implementa. L'ho violata due volte per fare colore (`eco_sismico`: "la zona rivela chi l'ha creata" --
la sorgente e' *immune*; `spore_paniche`: "gli alleati respirano il panico" -- e' *single-target*).
Nessuno dei gate automatici della sez. 5 lo intercetta: serve la lettura del motore.

Le tabelle del lotto 1 in sez. 4 riportano il testo **pre-correzione**. Il testo corretto e definitivo
e' in `data/i18n/{it,en}/traits.json` su PR Game #3247.

---

## 2. Il template di voce

Il brief chiedeva "2-3 frasi flavor + 1 riga effetto". Lo schema reale
(`traitStyleGuide.js:6`, `I18N_FIELDS`) ha gia' quattro campi che *sono* quel template:

| campo | funzione narrativa | forma |
| --- | --- | --- |
| `mutazione_indotta` | cosa il corpo ha cambiato | 1 frase, soggetto = struttura anatomica concreta, presente indicativo |
| `spinta_selettiva` | la pressione che l'ha selezionato | 1 frase, nomina il bioma in prosa (mai in `snake_case`) |
| `uso_funzione` | **l'effetto in chiaro** | 1 riga, verbo attivo, numeri del canone riportati **alla lettera** |
| `debolezza` | il costo | 1 riga, una **contromossa reale**, non una tassa di manutenzione |

Regole dure (sono anche i gate automatici, sez. 5): 8-24 parole per frase; iniziale maiuscola,
punto finale; vietate le formule `"permette alle squadre"`, `"ottimizza le operazioni"`,
`"garantire continuita'"`; mai identificatori `snake_case` nella prosa; mai iniziare ripetendo
il nome del tratto; nessuna frase riciclata fra tratti; EN = traduzione idiomatica, non calco.

`debolezza` e' il campo che separa il testo vero dal riempitivo. "Richiede manutenzione costante"
non e' una debolezza: e' rumore. "Non protegge da nulla che colpisca a distanza" lo e'.

---

## 3. Routing sovereign -- pipeline 2-stage, esito

**Stage 1 -- llmfit shortlist (HW-fit).** Authority: `LOCAL-LLM-STANDARD.md` + `ryzen-llm-fit.json`.
Dense <=14B in-VRAM -> Ryzen; MoE/grandi/offload -> Lenovo. Esclusi a priori i `*-coder*`
(task sbagliato) e i reasoning `deepseek-r1*`/`qwen3.6` (lo standard li marca flaky su
structured-output; qwen3.6 "hung 13min"). Shortlist: `gemma3:12b`, `qwen3:8b`, `mistral` (Ryzen),
`qwen2.5:32b-instruct` (Lenovo). Baseline: Claude, autorata **alla cieca prima** di vedere i locali.

**Stage 2 -- task-eval sul prompt reale, 10 tratti campione** (mix di 8 categorie, tier T1/T2/T3;
5 MANCANTE, 2 BOILERPLATE, 3 UNICO). Gate oggettivi, prima **falsificati** su fixture con
difetti piantati a mano (6/6 rilevati) -- senza quella prova il gate non era una decisione ma un'opinione.

| arm | n | DIFETTI | schema ok | campi inventati | numeri persi | numeri inventati | boilerplate vietato | err rete | lat med | stima 309 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **claude** | 10 | **0** | 10/10 | 0 | 0 | 0 | 0 | 0 | -- | -- |
| gemma3:12b | 10 | 7 | 10/10 | 0 | 6 | 1 | 0 | 0 | 10.1s | ~52 min |
| qwen3:8b | 10 | 7 | 8/10 | 2 | 3 | 1 | 0 | 0 | 3.4s | ~18 min |
| mistral | 10 | 12 | 7/10 | 7 | 4 | 0 | 1 | 0 | 4.0s | ~21 min |
| qwen2.5:32b (Lenovo) | 6 | 3 | 6/6 | 0 | 3 | 0 | 0 | 4 | 59.7s | ~5 h |

Letture, in ordine di peso:

- **Il difetto dei locali non e' la prosa: e' il contratto col dato.** Perdono o inventano i numeri
  canonici. `gemma3:12b` ha scritto per `criostasi_adattiva`: *"Riduce i danni subiti del 50% fino
  all'inizio del turno successivo"* -- una meccanica di combattimento che **il canone non autorizza**.
- `mistral` inventa chiavi (`debolezza_en_2`, `effetto_durata_it`) e riproduce l'esatto boilerplate
  che stiamo cercando di uccidere (*"Permette alle squadre di anticipare..."*). Fuori.
- `qwen2.5:32b` su Lenovo gira 75% CPU / 25% GPU (RAM-offload, come predetto da llmfit), 4 timeout
  di rete, ~5 ore per 309. Fuori per costo, non per qualita'.

**Anti lucky-sample (N=3 sui 4 tratti con meccanica, 12 campioni per cella) + 1 iterazione di tuning.**
Ipotesi: la perdita di numeri e' un difetto di *prompt*, non un tetto di capacita'. Il prompt indurito
elenca i valori canonici come vincolo esplicito.

| arm / prompt | voci perfette | numeri persi | numeri inventati |
| --- | --- | --- | --- |
| gemma3:12b / base | 1/12 | 15 | 0 |
| gemma3:12b / **indurito** | 8/12 | 5 | 0 |
| qwen3:8b / base | 7/12 | 8 | 1 |
| qwen3:8b / **indurito** | **12/12** | **0** | **0** |

Delta misurato: `qwen3:8b` passa da 7/12 a **12/12** voci canon-perfette. **La mia prima lettura
("i locali non tengono i numeri") era sbagliata**: i numeri sono recuperabili col prompt.

**Falsificazione esterna (blind A/B/C, `harsh-reviewer`, etichette anonime).**
Concorda coi gate su tutto cio' che i gate misurano, e trova quello che i gate non vedono:

- Claude (SISTEMA-1): *"pubblicabile cosi' com'e'"*, zero violazioni di canone.
- gemma3 (SISTEMA-2): *"da rifare integralmente... prosa gradevole, meccaniche sbagliate: e' il caso
  peggiore per un file di dati di gioco"*. Due volte ha messo **una debolezza dentro `uso_funzione`**
  (schema valido, significato no). Su `spore_paniche` ha **invertito il tratto** da offensivo a difensivo.
- qwen3 (SISTEMA-3): *"da rifare le meccaniche, riscrivere le debolezze"*. Collasso in template
  (`"Predatori che X: serviva Y"` su 6 voci su 10), debolezze-tassa ripetute
  (*"richiede rinnovo / pulizia / rifornimenti"*), errori d'accordo (*"in un stato"*), e biologia
  inventata (*"cellule ematopoietiche"* per un effetto emolitico).

**Verdetto.** Il prompt indurito ripara i **numeri**. Non ripara campo-sbagliato, tratto-invertito,
debolezza-generica, collasso sintattico: difetti semantici che nessun gate automatico intercetta e
che su un file di dati costano piu' della prosa mediocre. Per l'**authoring** -> Claude.
Per i locali resta una lane onesta e misurabile: **QA a costo zero** (rigenerare e diffare contro il
testo curato per stanare le voci a rischio) e, eventualmente, primo-draft su tratti **senza numeri
canonici** con revisione obbligatoria. Vedi Domanda 3.

---

## 4. Lotto 1 -- 10 tratti da curare

Testo autorato da Claude, alla cieca, prima di vedere gli output locali.
Zero difetti sui gate, zero violazioni di canone al blind review.

### aculei_velenosi
`fisiologico` / Fisiologico/Morfologia / tier T1 / stato precedente: **MANCANTE**

| campo | IT | EN |
| --- | --- | --- |
| label | Aculei Velenosi | Venomous Spines |
| mutazione_indotta | Le setole dorsali si sono fatte cave, innestate su sacche che distillano tossine emolitiche. | Dorsal bristles have turned hollow, grafted onto sacs that distil hemolytic toxins. |
| spinta_selettiva | Contro predatori troppo grandi per essere respinti, restava solo rendere costoso il morso. | Against predators too large to repel, only making the bite costly remained. |
| uso_funzione | Chi attacca in mischia si ferisce sugli aculei e sanguina a lungo. | Melee attackers wound themselves on the spines and bleed at length. |
| debolezza | Non protegge da nulla che colpisca a distanza: la punizione richiede contatto. | It guards against nothing that strikes from afar: the punishment needs contact. |

> **Nota meccanica** -- nessun numero canonico.  
> canone: Aculei rivestiti di tossine emolitiche che inducono sanguinamento prolungato al contatto.

### ali_ioniche
`locomotorio` / Locomotorio/Mobilità / tier T1 / stato precedente: **BOILERPLATE(x14)**

| campo | IT | EN |
| --- | --- | --- |
| label | Ali Ioniche | Ionic Wings |
| mutazione_indotta | Le membrane alari accumulano carica lungo nervature metalliche e la scaricano in micro-impulsi. | Wing membranes gather charge along metallic veins and release it in micro-pulses. |
| spinta_selettiva | Nella canopia ionica l'aria è già elettrica: chi sa spenderla si muove per primo. | In the ionic canopy the air is already electric: whoever can spend it moves first. |
| uso_funzione | Concede scatti direzionali improvvisi e cambi di quota rapidi in esplorazione. | Grants sudden directional dashes and rapid altitude changes while scouting. |
| debolezza | Ogni scatto svuota la carica; senza aria ionizzata le ali restano membrane inerti. | Each dash drains the charge; without ionised air the wings are inert membranes. |

> **Nota meccanica** -- nessun numero canonico.  
> canone: Membrane propulsive che rilasciano micro-scariche per scatti controllati.

### antenne_flusso_mareale
`offensivo` / Offensivo/Assalto / tier T1 / stato precedente: **BOILERPLATE(x13)**

| campo | IT | EN |
| --- | --- | --- |
| label | Antenne di Flusso Mareale | Tidal-Flow Antennae |
| mutazione_indotta | Le antenne si sono sintonizzate sul ritmo delle maree, immagazzinando l'onda nei condotti muscolari. | The antennae tuned themselves to the tide's rhythm, storing the surge in muscular ducts. |
| spinta_selettiva | Nella laguna bioreattiva colpire fuori tempo significa colpire l'acqua e nient'altro. | In the bioreactive lagoon, striking off-beat means striking water and nothing else. |
| uso_funzione | Scarica l'energia accumulata in un colpo singolo che apre le difese avversarie. | Discharges the stored energy into a single blow that cracks enemy defences. |
| debolezza | L'onda va rilasciata: trattenuta troppo a lungo, si scarica sul portatore. | The surge must be released: held too long, it discharges into its bearer. |

> **Nota meccanica** -- nessun numero canonico.  
> canone: Antenne Flusso Mareale permette alle squadre di canalizzare energia cinetica o elementale in colpi mirati all'interno di laguna bioreattiva.

### corteccia_memetica
`difensivo` / Difensivo/Protezione / tier T2 / stato precedente: **MANCANTE**

| campo | IT | EN |
| --- | --- | --- |
| label | Corteccia Memetica | Memetic Bark |
| mutazione_indotta | La corteccia registra ogni colpo pesante come una cicatrice che gli alleati sanno leggere. | The bark records every heavy blow as a scar that allies know how to read. |
| spinta_selettiva | Nei boschi antichi sopravvive chi trasforma la propria ferita in avvertimento condiviso. | In ancient woods, survival belongs to those who turn their wound into a shared warning. |
| uso_funzione | Subito un colpo da 3 danni o più indurisce (danno -2) e concede +1 attacco agli alleati entro 3. | After taking a hit of 3 damage or more it hardens (damage -2) and grants allies within 3 a +1 attack. |
| debolezza | Serve essere feriti sul serio: contro il logoramento leggero la corteccia non si sveglia mai. | It needs a real wound: against light attrition the bark never wakes. |

> **Nota meccanica** -- numeri canonici ['1', '2', '3'] -> riportati in uso_funzione.  
> canone: Corteccia memetica (treant): quando subisce un colpo pesante (>= 3 danni) la corteccia si indurisce (riduzione danno 2 sui colpi successivi) e la f...

### eco_sismico
`sensoriale` / Sensoriale/Percezione / tier T2 / stato precedente: **MANCANTE**

| campo | IT | EN |
| --- | --- | --- |
| label | Eco Sismico | Seismic Echo |
| mutazione_indotta | Placche cutanee percepiscono la vibrazione del suolo e la restituiscono amplificata. | Cutaneous plates sense the ground's tremor and return it amplified. |
| spinta_selettiva | Sotto la roccia la vista non serve: conta solo chi sente arrivare il peso. | Under the rock, sight is useless: all that counts is feeling the weight approach. |
| uso_funzione | Un impulso marca il terreno come zona risonante per 2 round. | A single pulse marks the ground as a resonant zone for 2 rounds. |
| debolezza | L'eco non distingue amico da nemico: la zona rivela anche chi l'ha creata. | The echo tells no friend from foe: the zone reveals its own maker too. |

> **Nota meccanica** -- numeri canonici ['2'] -> riportati in uso_funzione.  
> canone: Eco sismico (banshee): un impulso marca il terreno come `zona_risonante` (2 round).

### spore_paniche
`strategia` / Comportamentale/Istinto / tier T2 / stato precedente: **MANCANTE**

| campo | IT | EN |
| --- | --- | --- |
| label | Spore Paniche | Panic Spores |
| mutazione_indotta | Sacche sporali maturano sotto la pelle e si aprono al primo segnale di minaccia. | Sporal sacs ripen beneath the skin and burst at the first sign of threat. |
| spinta_selettiva | Non serve uccidere il predatore: basta convincerlo che il branco è già perduto. | There is no need to kill the predator, only to convince it the pack is already lost. |
| uso_funzione | Le spore neurotossiche inducono allucinazioni e mettono in fuga: 3 turni di panico. | Neurotoxic spores induce hallucinations and rout the target: 3 turns of panic. |
| debolezza | La nube non sceglie i polmoni: gli alleati vicini respirano lo stesso terrore. | The cloud does not choose its lungs: nearby allies breathe the same terror. |

> **Nota meccanica** -- numeri canonici ['3'] -> riportati in uso_funzione.  
> canone: Rilascio di spore neurotossiche che inducono allucinazioni terrifiche e fuga (3 turni di panic).

### nodi_micorrizici_oracolari
`simbiotico` / Simbiotico/Nervoso / tier T3 / stato precedente: **UNICO**

| campo | IT | EN |
| --- | --- | --- |
| label | Nodi Micorrizici Oracolari | Oracular Mycorrhizal Nodes |
| mutazione_indotta | Radici dermiche si innestano nella rete fungina e ne leggono in anticipo i segnali chimici. | Dermal roots graft into the fungal network and read its chemical signals in advance. |
| spinta_selettiva | Nelle reti micorriziche il bosco sa prima di te: conviene ascoltarlo. | In the mycorrhizal networks the forest knows before you do: better to listen. |
| uso_funzione | Anticipa le minacce e trasmette letture tattiche alla squadra prima del contatto. | Anticipates threats and relays tactical reads to the squad before contact. |
| debolezza | Recisa la rete, i presagi tacciono e resta solo disorientamento. | Sever the network and the omens fall silent, leaving only disorientation. |

> **Nota meccanica** -- nessun numero canonico.  
> canone: Nodi micorrizici che anticipano minacce tramite segnali fungini.

### criostasi_adattiva
`metabolico` / Metabolico/Difensivo / tier T1 / stato precedente: **UNICO**

| campo | IT | EN |
| --- | --- | --- |
| label | Criostasi Adattiva | Adaptive Cryostasis |
| mutazione_indotta | Il sangue si carica di enzimi crioprotettivi che fermano il metabolismo senza spezzare i tessuti. | The blood loads with cryoprotective enzymes that halt metabolism without shattering tissue. |
| spinta_selettiva | Chi non sa attraversare l'inverno deve saperlo dormire. | Those who cannot cross the winter must learn to sleep through it. |
| uso_funzione | Sospende il metabolismo per sopravvivere a stagioni estreme e carestie prolungate. | Suspends metabolism to survive extreme seasons and prolonged famine. |
| debolezza | Nel sonno il corpo non filtra nulla: ogni veleno lavora indisturbato. | Asleep, the body filters nothing: every poison works undisturbed. |

> **Nota meccanica** -- nessun numero canonico.  
> canone: Metabolismo sospeso che sopravvive a stagioni estreme prolungate.

### ghiandole_mnemoniche
`frattura_abissale_sinaptica` / Supporto/Copia / tier T2 / stato precedente: **UNICO**

| campo | IT | EN |
| --- | --- | --- |
| label | Ghiandole Mnemoniche | Mnemonic Glands |
| mutazione_indotta | Ghiandole sinaptiche condensano gli stati alterati in secrezioni che li conservano attenuati. | Synaptic glands condense altered states into secretions that keep them attenuated. |
| spinta_selettiva | Nella frattura sinaptica ogni potenziamento svanisce: sopravvive chi ne serba una copia. | In the synaptic fracture every boon fades: those who keep a copy survive. |
| uso_funzione | Conserva una copia indebolita di un potenziamento e la ridistribuisce più tardi. | Stores a weakened copy of a buff and redistributes it later. |
| debolezza | La copia è sempre più povera dell'originale e occupa la ghiandola finché non viene spesa. | The copy is always poorer than the original, and occupies the gland until spent. |

> **Nota meccanica** -- nessun numero canonico.  
> canone: Secrezioni che trattengono copie attenuate di buff.

### voce_imperiosa
`strategia` / Comportamentale/Istinto / tier T1 / stato precedente: **MANCANTE**

| campo | IT | EN |
| --- | --- | --- |
| label | Voce Imperiosa | Imperious Voice |
| mutazione_indotta | Le corde vocali si sono ispessite in una camera che risuona sotto la soglia dell'udito. | The vocal cords thickened into a chamber that resonates below the threshold of hearing. |
| spinta_selettiva | In un branco l'ordine di fuga arriva prima del predatore: chi lo pronuncia comanda. | In a pack the order to flee arrives before the predator: whoever speaks it commands. |
| uso_funzione | In mischia la voce spezza la volontà del bersaglio: 2 turni di panico. | In melee the voice breaks the target's will: 2 turns of panic. |
| debolezza | Vale solo a portata di voce e non tocca chi non ha volontà da spezzare. | It works only within earshot, and never touches what has no will to break. |

> **Nota meccanica** -- numeri canonici ['2'] -> riportati in uso_funzione.  
> canone: Voce risonante che paralizza la volontà dei deboli applicando 2 turni di panic in melee.


---

## 5. Gate di qualita' per i lotti successivi

Ordine di esecuzione: i primi tre sono automatici e bloccanti, l'ultimo e' umano.

1. **Schema** -- `config/i18n/trait_locales.schema.json` valido; chiavi esattamente
   `{label, mutazione_indotta, spinta_selettiva, uso_funzione, debolezza}`; nessun campo extra.
2. **Nessuna chiave orfana** -- ogni `entries.<id>` esiste in `data/traits/**`; ogni tratto con un
   placeholder `i18n:traits.<id>.<campo>` ha la chiave corrispondente. Simmetrico IT/EN.
   Se la destinazione e' `data/i18n/` questo e' **gia'** `npm run i18n:check` (key-parity +
   no-placeholder + completion): gate gratis, zero codice nuovo.
3. **Gate di contenuto** (i controlli di questa sessione, gia' falsificati):
   numeri del canone presenti in `uso_funzione`; nessun numero non presente nel canone;
   nessuna frase riciclata fra tratti del lotto; nessuno `snake_case` in prosa; nessuna formula
   proibita; `IT != EN`; 8-24 parole; maiuscola iniziale + punto finale.
4. **Spot-check umano**: **N=5 voci per lotto** (non a campione libero -- 2 con numeri canonici,
   1 boilerplate sovrascritto, 2 estratte a caso). Si controlla cio' che l'automatico non vede:
   la `debolezza` e' una contromossa vera? `uso_funzione` contiene davvero l'effetto e non un costo?
   il tratto e' rimasto sé stesso?

**Cadenza.** Lotti da **25** (12-13 lotti per 309), raggruppati **per categoria** e non per ordine
alfabetico: le sinergie e i conflitti stanno dentro la categoria, e vedere 25 tratti `sensoriale`
insieme e' l'unico modo di accorgersi che si stanno ripetendo. Un lotto = un PR, testo mai committato
prima della curatela. Checkpoint + log per ogni run > 5 min (gia' attivo:
`Extras/ollama-runs/2026-07-10-trait-flavor-eval.log`).

**Ordine consigliato dei lotti**: prima i **46 tratti senza alcuna entry** (il gioco non ha nulla da
dire su di loro), poi i **127 `debolezza` mancanti**, infine la sovrascrittura dei cluster boilerplate.

---

## 6. Metodi applicati

| protocollo | dove |
| --- | --- |
| `agent-scanner` (BOOTSTRAP) | eseguito a inizio sessione; riuso di `harsh-reviewer`, nessun agent nuovo |
| Refresh-verify PRE-action | ground-truth su `data/traits`, `locales/`, `data/i18n`, glossary, git log, consumer runtime -- ha ribaltato 3 premesse su 3 |
| Currency Gate / ground-truth > report | il claim "il gioco parla per segnaposto" verificato a codice, non dedotto |
| Quality Gate 3-step | smoke (endpoint + 1 call) -> ricerca (5 arm, 9 gate, edge case) -> tuning (prompt indurito, delta 7/12 -> 12/12) |
| N-sample anti lucky-sample | N=3 x 4 tratti x 2 prompt x 2 modelli = 48 campioni sulla claim numerica |
| SDMG | il gate e' un metodo mio -> falsificato su fixture a difetti noti (6/6) prima di usarlo per decidere |
| Falsificazione esterna | `harsh-reviewer` blind A/B/C, etichette anonime |
| Background task policy | checkpoint idempotente per-arm + log persistente in `Extras/ollama-runs/` |
| Boundary repo esterni | `C:\dev\Game` = solo letture. Zero write, zero commit. |
