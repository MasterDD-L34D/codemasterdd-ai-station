# ADR-0046 — Board agenti come livello di coordinamento della flotta: ratifica, restringi o rinvia

> *TL;DR: la Board agenti e' nata per coordinare un solo progetto. Oggi coordina di fatto la flotta (benchmark, hardware, Ollama, PR di questo repo, lavori schedulati di un altro progetto). Funziona cioe' da bus di messaggi cross-repo, la cosa che lo spec orchestratore aveva rinviato al Gate B, ed e' cresciuta fuori da quel gate e fuori da AGENTIC_OS.md. Il Gate B e' obsoleto nella sostanza; la lettura fedele della sua definizione da' 6 repo, sotto la soglia. Raccomandazione: RINVIA ora; RATIFICA quando le prove di uscita della Fase 1 saranno verificate e STATUS_MULTI_REPO.md sara' aggiornato. Decide Eduardo.*

- Status: **Proposed** (2026-11-12, cancello del progetto "Board di flotta", fase 1)
- Data: 2026-11-12
- Decisore: Eduardo Scarpelli
- Deciders: solo-dev (single-user workstation)
- Autore draft: Claude (subagent adr-drafter, worktree isolato su Lenovo). Un design
  self-made e' un'ipotesi ad alto errore (SDMG). Prima revisione dopo review severa
  (verdetto "correggere e rivedere", fix round 1).
- Amends (solo se l'esito e' RATIFICA): il Gate B in `docs/governance/ESCALATION_GATES.md`
  viene annotato come riaperto e deciso da questo ADR. Lo spec orchestratore cross-repo non
  viene emendato: e' gia' superato.
- Protocolli applicati: refresh-verify con Currency Gate (ADR-0026 P1), Gate B contato dal
  file e non a memoria, sezione dei risultati negativi.
- Privacy: questo repo e' PUBBLICO. La Board e' descritta per funzione: nessun nome di repo
  privato, nessun indirizzo, nessun percorso utente, nessun dettaglio operativo che non sia
  gia' pubblico.

## Context and Problem Statement

La Board agenti e' un file markdown in Git, nel repo privato del progetto in cui e' nata.
Ha un writer atomico, un lock, lease advisory e la redazione dei segreti, e quattro sezioni:
Presenze, Lavori, Messaggi, Decisioni. Un ponte (bridge) la usa per passare lavoro agli
agenti. Era pensata per un solo progetto; oggi ci passano anche lavori di flotta. Casa,
schema e igiene sono rimasti quelli di un progetto solo.

Questo ADR risponde a una sola domanda: la Board e' il livello di coordinamento della flotta
(e va ratificata e adattata), va ristretta, o la decisione va rinviata? Il codice della Board
vive altrove e qui non si decide nulla su di esso.

### Situazione attuale (misurata il 2026-11-12)

**Provenienza dei numeri**: vengono dalla sezione 2 dello spec di design "Board di flotta
v2". Lo spec non e' in git in questo repo, per privacy, e i numeri si possono verificare solo
con accesso al repo privato. Qui sono riportati, non rimisurati.

| Fatto | Misura |
|---|---|
| File board vivo | 190 KB, un solo `.md`, in un checkout condiviso sul Ryzen |
| Peso per sezione | Messaggi 127 KB (67% del file), Lavori 39 KB, Presenze 21 KB, resto 5 KB. Le sezioni sommano a 192 KB contro 190 KB del file: le due misure sono state prese in modo diverso |
| Checkout che ospita lo stato vivo | fermo su un ramo feature, 272 commit dietro `main` e 30 avanti; ospita anche altro stato vivo |
| Board su `main` del repo d'origine | 13 KB (fossile) |
| Codice Board su `main` | 32 file sorgente, circa 7.450 righe, 30 file di test |
| Percorso della board | in parte nella configurazione, in parte scritto nel codice in piu' punti |
| Scrittori del file vivo | almeno 3: la release installata; il writer vecchio del checkout (usato via SSH; -457 righe nette rispetto a `main`); un terzo scrittore schedulato (task oggi disabilitato) |
| Messaggi | 206: 121 open, 85 done. Open per tipo: info 60, result 21, review 16, request 12, handoff 12 |
| Open che chiedono azione | 40: eta' mediana 1,1 giorni, massima 16,4; 14 oltre i 7 giorni |
| Lavori | 91: review 43, unverified 27, blocked 12, done 6, attivi 2, handoff 1 |
| Presenze | 131: chiuse 116, attive 8, in pausa 7 |
| Campo progetto | assente |
| Accesso da Lenovo | solo SSH, con un comando composto a mano |

Lo spec dichiara due cose non misurate: quanti riferimenti al vecchio percorso contiene la
release installata, e perche' 43 lavori sono fermi in `review` (le righe Lavori non hanno
data).

Stato funzionale dichiarato altrove: ADR-0045 riporta, dal 2026-11-02, che "la Board non
funziona ancora". Secondo quel testo e' un registro, non un'esecuzione.

### Input / trigger

1. Lo spec di design "Board di flotta v2" (approvazione registrata nell'intestazione dello
   spec, 2026-11-12; lo spec e' fuori da git, quindi verificabile solo con accesso al repo
   privato) fa di questo ADR il
   **cancello**: la Fase 2 (forma) esiste solo con esito RATIFICA.
2. La Board usata cross-progetto **funziona di fatto da bus di messaggi**, cioe' proprio la
   cosa che lo spec orchestratore cross-repo aveva rinviato ("NO event/message bus" fino al
   Gate B).
3. AGENTIC_OS.md non cita la Board: e' un livello ombra.

### Currency Gate delle autorita' citate

| Documento | Ultimo commit | Stato dichiarato nel file | Peso in questo ADR |
|---|---|---|---|
| Spec orchestratore cross-repo `docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md` | 2026-06-23 | header "superseded -- evolved into unified-fleet-governor"; corpo "Draft V3", confidenza 55% | **Non e' un vincolo certo**: superato e mai uscito da Draft. Il Gate B nasce qui e sopravvive solo perche' ESCALATION_GATES.md lo riprende |
| `docs/governance/ESCALATION_GATES.md` | 2026-06-04 | "checkpoint, NOT prescription" | Fonte operativa del Gate B |
| Spec governor di flotta `docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md` | 2026-06-23 | "shipped-partial -- R0/R1 live + weekly reconcile scheduled"; corpo "DRAFT v2" | Vincolo per R0 e per il principio anti-circolarita' (sez. 4). Vecchio di 5 mesi |
| Spec console Agentic OS `docs/superpowers/specs/2026-07-12-agentic-os-console-design.md` | 2026-07-13 | "MVP IMPLEMENTED (2026-07-13)" | Vincolo: la console legge la tabella dei layer di AGENTIC_OS.md |
| Spec fleet-tools MCP `docs/superpowers/specs/2026-05-29-fleet-tools-mcp-design.md` | 2026-06-23 | "shipped -- apps/fleet-tools-mcp live" | Serve solo per `cross_check` (reviewer di un'altra famiglia di modelli). Nessuna sovrapposizione funzionale con la Board |
| [STATUS_MULTI_REPO.md](../../STATUS_MULTI_REPO.md) | 2026-07-13 | "Ultimo refresh 2026-06-30" + delta fino al 2026-07-13 | Unica fonte ammessa per contare il Gate B. **Fermo da 4 mesi** |
| Spec di design Board di flotta v2 (2026-11-12) | nessuno: fuori da git per privacy | intestazione "v2 APPROVATA da Eduardo in chat il 2026-11-12": approvazione registrata nell'intestazione dello spec, verificabile solo con accesso al repo privato | Fonte dei numeri. Prove di uscita della Fase 1 **non ancora eseguite** |

### Gate B: conteggio dal file

Definizione operativa (ESCALATION_GATES.md, Gate B): "repo count >=7 (codemasterdd + Game +
Godot-v2 + Dafne + vault + Synesthesia + >=1 NEW = 7+) OR client production work attivo".

Tabella "Snapshot 1-riga per repo" di STATUS_MULTI_REPO.md, contata riga per riga:
**12 righe**.

| # | Riga | Stato nella riga | Conta nella lettura fedele? |
|---|---|---|---|
| 1 | codemasterdd-ai-station | attivo (hub) | si' |
| 2 | Synesthesia | dormant intenzionale | si' (elencato nella definizione) |
| 3 | Game (Evo-Tactics) | attivo | si' |
| 4 | Game-Godot-v2 | attivo | si' |
| 5 | Dafne swarm (evo-swarm) | remote ARCHIVED+PRIVATE dal 2026-06-22 | no (archiviato) |
| 6 | AA01 | attivo, non-git | no (non e' un repo git) |
| 7 | vault-shared | attivo | si' |
| 8 | Game-Database | attivo | si' |
| 9-12 | 4 righe Ryzen-only informative | "Informational, no action" | no |

Fuori dalla tabella c'e' una sezione remote-only idle, non contata.

Passano dalla Board ma **non compaiono** nel file: il repo privato in cui la Board e' nata,
un repo privato dedicato allo specchio (Fase 1) e almeno un altro repo privato coordinato
via Board. Lo spec dice di contare dal file e non a memoria, quindi non sono contati.

Lavoro cliente attivo: nessuna evidenza nei file letti. CLAUDE.md cita "repo cliente" solo
come classe di privacy.

**Letture:**

- **Lettura fedele alla definizione: 6** (codemasterdd, Synesthesia, Game, Game-Godot-v2,
  vault, Game-Database). E' sotto la soglia. Senza Synesthesia, che e' dormant, sarebbero 5.
- **Lettura debole: 12**, contando anche le righe "Informational, no action". Supera la
  soglia solo perche' conta repo che il file stesso dichiara senza azione. Non regge da sola.

**Il Gate B e' obsoleto nella sostanza.** L'azione che il gate attivava era "re-evaluate
Opt 4 (Dafne swarm extension cross-repo)", e lo swarm e' archiviato dal 2026-06-22. Il
gate misurava un proxy, il numero di repo, per una domanda che oggi si pone in un altro
modo: serve un bus di coordinamento fra agenti, visto che ne esiste gia' uno? Questo ADR
propone di decidere **nel merito**, usando il conteggio solo come contesto.

Comunque si legga il conteggio, vale ESCALATION_GATES.md: "This document is checkpoint, NOT
prescription". Un gate superato riapre la decisione, ma **non autorizza nulla**. Il gate
inoltre non si puo' chiudere con nessuna lettura finche' STATUS_MULTI_REPO.md non viene
aggiornato: il file e' vecchio di 4 mesi e non vede i repo che la Board coordina.

### Domande a cui il cancello deve rispondere (spec di design sez. 6.2)

1. Il Gate B e' soddisfatto? Risposta sopra: no nella lettura fedele, e comunque obsoleto e
   non chiudibile prima del refresh.
2. La Board sostituisce, alimenta o duplica il pannello R0 del governor e la console?
3. Due archivi di coordinamento (markdown della Board, SQLite del governor): dov'e' il
   confine?
4. Esito: RATIFICA, RESTRINGI o RINVIA?
5. La Board va citata in AGENTIC_OS.md in ogni caso: fatto in questo stesso cambio, con una
   nota fuori dalla tabella dei layer.

### Cosa fanno oggi R0 e la console (letto nel codice)

- **Pannello R0 del governor** (`apps/cross-repo-dashboard/governor/`). Legge i file di
  segnale che le isole hanno gia' committato (Game, vault, ARCHON, digest Jules) e li
  normalizza in SQLite (tabella `signals`, deduplicata per hash). Registra in `acted_on` le
  azioni di Eduardo, l'unica misura che autorizza nuovi rung. Tiene un log `auto_observed`
  **solo consultivo**, escluso da ogni gate. E' report-only e la Board non e' una sua
  sorgente. Il blocco GOVERNOR-SYNC copia questi segnali in STATUS_MULTI_REPO.md, che e' un
  file **pubblico**.
- **Console Agentic OS** (`/os`). Mostra la tabella dei layer di AGENTIC_OS.md con uno stato
  vivo per layer e lancia azioni tier-0 e tier-1 al click. Non conosce la Board.
- **Board**. Contiene lo stato vivo scritto dagli agenti: chi e' presente, chi tiene un
  lease, chi chiede cosa a chi. Ne' R0 ne' la console hanno questo dato.

Oggi la Board **non sostituisce** R0 ne' la console, e **non le alimenta**. **Duplica in
parte** R0 su un solo dolore, "lo stato si cerca in tanti posti" (spec governor, dolore 4).
Ma le domande sono diverse: R0 risponde a "cosa riportano le isole", la Board a "chi sta
facendo cosa adesso".

C'e' un terzo archivio con un nome simile, da tenere distinto:
[EXECUTION-BOARD.md](../governance/EXECUTION-BOARD.md). E' un control-plane cross-repo
pubblico, con `last_verified` 2026-05-16 e una regione auto-sync scritta da
`playtest2-board-sync`. Non e' la Board agenti e nessuna opzione lo tocca.

### Posizione rispetto ad ADR-0036 decisione 6

ADR-0036 decisione 6 vieta i framework di orchestrazione pesanti e i gateway LLM. ADR-0045
la legge cosi': le fonti "vietano il coordinamento fra LLM in un runtime" e non vietano i
worktree. La domanda e' se la Board, con il ponte che passa lavoro agli agenti, ricada nel
divieto. L'argomento vale nei due sensi e qui non viene chiuso.

- **Non ricade**: la Board non e' un framework ne' un runtime. E' un file in Git, con writer
  e parser in libreria standard, leggibile senza tool. Nessun processo resta in ascolto e
  non c'e' coordinamento LLM-LLM in memoria condivisa: ogni agente legge e scrive righe, e
  lo stato autoritativo resta versionato. ADR-0045 (regola 3 della checklist) presuppone gia'
  che "la Board e la coda restano in Git" e la tratta come archivio, non come runtime.
- **Ricade, o ci si avvicina**: la sezione Messaggi (67% del file) e' un canale di
  messaggi fra agenti, e la checklist di ADR-0045 (punto 2) esclude proprio "un canale di
  messaggi fra agenti" dentro un'app ammessa. Il ponte che passa lavoro agli agenti e' la
  parte di orchestrazione; se gira in modo persistente, e' un runtime di coordinamento fra
  LLM con il file come bus. La prova citata da ADR-0036 ("multi-agent e' un POOR fit per
  lavoro a contesto condiviso") parla della funzione, non della forma: un bus in markdown
  resta un bus.

**Fatto decisivo, non verificato**: il ponte della Board gira come processo persistente
oppure solo su richiesta? Questo draft non l'ha verificato e i documenti letti non lo dicono.
Se e' persistente pesa l'argomento "ricade"; se parte solo su richiesta, a ogni passaggio di
lavoro, pesa l'argomento "non ricade". La verifica va fatta sul codice e sulla configurazione
nel repo d'origine prima di chiudere la domanda.

Se l'esito e' RATIFICA, questa domanda va chiusa nello stesso atto. Le strade sono due: un
emendamento esplicito a ADR-0036 decisione 6, nel modo usato da ADR-0045, oppure una
dichiarazione motivata che la Board ne resta fuori. Questo ADR non la chiude.

## Options

### Opzione A -- RATIFICA: la Board e' il bus di coordinamento della flotta e la Fase 2 parte

La Board diventa il livello di coordinamento della flotta per lo stato vivo fra agenti. La
Fase 2 dello spec parte con **una sola release** del codice Board:

- i messaggi `info` e `result` scadono;
- un comando `archive` sposta solo le righe terminali piu' vecchie di 14 giorni, e'
  idempotente e ha un dry-run;
- il campo `progetto` diventa obbligatorio sulle righe nuove;
- i 40 messaggi che chiedono azione passano un triage: propone un agente, decide Eduardo.

**Pro**:
- Mette per iscritto cio' che succede gia': il bus esiste ed e' in uso.
- Il campo `progetto` darebbe una misura del meta-lavoro per riga, piu' fine della misura
  sui commit gia' esistente (vedi Opzione B).
- La board viva scenderebbe da 190 KB a circa 80 KB dopo l'archivio. E' una stima ricavata
  dai byte per sezione, non una misura: il dry-run la confermerebbe o la correggerebbe.
- Non aggiunge componenti: stesso file, stesso writer, stessa casa.

**Contro**:
- Oggi le precondizioni non ci sono: la Fase 1 non ha passato le prove di uscita, e ADR-0045
  riporta che la Board "non funziona ancora".
- Il meta-lavoro e' gia' sopra il tetto. ADR-0045 ha misurato 60 commit su 178 in 30 giorni
  con board, coda o handoff nel messaggio. La Fase 2 ci aggiunge una release, fino a 4
  packet e 8 tentativi.
- Fino alla Fase 3 restano due versioni del writer e tre scrittori.
- La domanda su ADR-0036 decisione 6 va chiusa prima (vedi sopra).
- Privacy: anche agenti cloud leggono la Board. Un bus di flotta tocca lavori su repo
  sovereign-only (vault, Synesthesia). La regola "mai contenuto sovrano in board" (spec,
  sez. 5) diventa piu' importante, e **nessun controllo la fa rispettare**.

**Cost**:
- 1 release del codice Board (PR, merge, nuova release installata);
- al massimo 4 packet e 8 tentativi;
- decisioni di Eduardo su TTL (proposta: 72 ore) e valori di budget;
- dipendenza dai crediti Codex: nessun dispatch sotto il 20% di quota.

**Rischio**: meta-lavoro oltre il tetto; bus che continua a crescere; contenuto privato in un
file pubblico, se un segnale della Board arriva fin li'.

**Pannello R0**: la Board potrebbe diventare una **sorgente in sola lettura** di R0, con
quattro limiti:
- solo conteggi, senza testo libero e senza nomi di repo;
- esclusa dal blocco pubblico GOVERNOR-SYNC;
- mai scritta dal governor;
- i suoi messaggi non contano mai come `acted_on`. Vale lo stesso principio
  anti-circolarita' della spec governor (sez. 4): un attore non produce le prove che lo
  autorizzano.

L'aggancio sarebbe una PR separata, non decisa qui.

**Console**: la nota "livelli ombra" in AGENTIC_OS.md sparirebbe. Un'eventuale riga nella
tabella dei layer richiederebbe di emendare ADR-0044, che definisce la mappa a 7 layer.

### Opzione B -- RESTRINGI: la Board torna ai soli lavori multi-agente, senza campo progetto

La Board resta, ma solo per coordinare agenti che lavorano insieme: presenze, lease,
handoff. I segnali di flotta (stato dei benchmark, hardware, Ollama) escono dalla Board e
vanno su R0, nel JOURNAL o nelle PR. Nessuna Fase 2.

**Pro**:
- Rispetta il rinvio del bus deciso nello spec orchestratore.
- Nessuna release e nessun packet: il meta-lavoro aggiunto e' minimo.
- Meno lavori di flotta in un file letto da agenti cloud: la superficie privacy si riduce.
- Il tetto resta misurabile anche senza campo `progetto`, con la misura di ADR-0045: una
  regex sui messaggi di commit, 60 su 178 in 30 giorni. E' piu' grossolana (conta commit,
  non lavori; la finestra include il picco di costruzione della Board v2) ma esiste gia'.

**Contro**:
- Il confine "multi-agente" e' sfumato: il lease su Ollama fra due macchine e' gia'
  coordinamento multi-agente di flotta. La regola resterebbe solo testuale, senza
  enforcement, e il bus ricrescerebbe in silenzio.
- Non c'e' un altro posto per lo stato vivo fra agenti: R0 e' report-only, la console e'
  una porta per l'umano, EXECUTION-BOARD.md e' fermo da maggio.
- I 190 KB e i 14 messaggi oltre i 7 giorni restano: niente archivio, niente scadenza.

**Cost**: una modifica alle istruzioni degli agenti nel repo d'origine, fuori da questo repo
(branch + PR, merge di Eduardo).

**Rischio**: la regola viene ignorata e il file cresce senza archivio.

**Pannello R0**: invariato, la Board non e' una sorgente. **Console**: la nota resta,
riformulata come "livello di progetto, non di flotta".

**Verdict**: secondaria. Ha senso se Eduardo vuole il costo minimo e accetta la misura di
meta-lavoro gia' esistente.

### Opzione C -- RINVIA: resta la Fase 1, nessuna decisione sul ruolo

Lo specchio orario della Fase 1 resta, per la sicurezza dello stato. Niente Fase 2, niente
restrizione. Si rivaluta quando scatta un trigger scritto.

**Pro**:
- Nessun meta-lavoro aggiuntivo.
- Lascia il tempo per le due cose che oggi mancano: le prove di uscita della Fase 1 e il
  refresh di STATUS_MULTI_REPO.md.

**Contro**:
- Il livello ombra resta ombra: la Board continua a crescere fuori da ogni gate.
- Il debito cresce: 14 messaggi oltre i 7 giorni, 43 lavori in `review`, file da 190 KB
  senza archivio.

**Cost**: zero.

**Rischio**: la decisione viene presa per inerzia, e la Board diventa il bus senza ADR. Per
limitarlo servono un trigger di revisione e una nota in AGENTIC_OS.md.

**Pannello R0**: invariato. **Console**: la nota resta "ombra, da ratificare".

## Confine fra i due archivi di coordinamento

Vale in ogni esito.

| | Board agenti (markdown in Git) | Governor (SQLite locale) |
|---|---|---|
| Chi scrive | gli agenti, tramite il writer atomico | solo l'ingest del governor (single-writer, WAL), piu' Eduardo per `acted_on` |
| Cosa contiene | lo stato vivo del coordinamento: presenze, lease, lavori, messaggi e decisioni fra agenti | una copia normalizzata dei segnali gia' committati dalle isole, piu' le azioni di Eduardo |
| Autorita' | autoritativa per lo stato vivo | derivata per i segnali; autoritativa solo per `acted_on` |
| Visibilita' | repo privato | `governor.db` e' locale, ma il blocco GOVERNOR-SYNC finisce in un file **pubblico** |

Regole proposte:

1. Nessun dato e' autoritativo in entrambi gli archivi.
2. Il governor puo' leggere la Board (solo conteggi) ma non la scrive mai.
3. Niente della Board entra in `acted_on`, e nessun conteggio della Board vota per
   l'autonomia del governor.
4. Niente della Board arriva in un file pubblico: niente testo e niente nomi di repo
   privati, ne' nel blocco GOVERNOR-SYNC ne' nelle PR del rung di reconcile R1 (ADR-0039).
5. EXECUTION-BOARD.md resta un terzo archivio, separato, e non viene fuso con gli altri due.

## Decision

**Raccomandazione: RINVIA ora (Opzione C); RATIFICA (Opzione A) quando X e Y saranno
soddisfatte.** Decide Eduardo.

- **X -- prove di uscita della Fase 1 verificate da un reviewer indipendente.** Le prove
  sono quelle dello spec, sez. 6.1:
  - il commit remoto dello specchio e' piu' recente di un'ora rispetto all'ultima modifica
    della board;
  - il ripristino e' stato provato una volta, con lo stesso numero di righe per sezione;
  - con il remoto irraggiungibile, lo script fallisce in modo visibile (controllo negativo).

  Alla data di questo draft le prove **non sono state eseguite**. Il reviewer non e' il
  coordinatore. Sono possibili due scelte:
  1. un modello di un'altra famiglia, tramite lo strumento `cross_check` del server MCP di
     flotta gia' esistente (`apps/fleet-tools-mcp`);
  2. il reviewer severo, in una sessione che non ha partecipato al progetto.
- **Y -- STATUS_MULTI_REPO.md aggiornato**, con i repo coordinati dalla Board dentro (descritti
  per funzione se privati), e decisione di Eduardo **nel merito** sul bus. Vista
  l'obsolescenza del Gate B, il conteggio non decide da solo. Chiudere il gate con la
  lettura debole prima del refresh non e' ammesso.
- Va chiusa anche la domanda su ADR-0036 decisione 6, nello stesso atto della RATIFICA.

Perche' non RATIFICA subito: le due precondizioni oggi non ci sono, e ADR-0045 riporta che la
Board "non funziona ancora". Ratificare come bus di flotta un componente che il suo stesso
perimetro dichiara non funzionante vorrebbe dire ratificare l'uso, non la funzione.

Perche' non RESTRINGI come primo passo: introduce una regola senza enforcement. **Doppio
standard dichiarato**: anche la regola di privacy sotto RATIFICA ("mai contenuto sovrano in
board") non ha enforcement. L'argomento "regola senza enforcement" quindi non distingue le
due opzioni. Le distinguono il costo (RESTRINGI e' quasi gratis) e l'assenza di un posto
alternativo per lo stato vivo fra agenti (sfavorevole a RESTRINGI). RESTRINGI resta
un'opzione legittima se Eduardo da' piu' peso al costo.

**Clausola di arresto (vale se si arriva a RATIFICA).** Le righe Lavori non hanno data,
quindi "lavori nuovi in 7 giorni" non si puo' calcolare sulla board. La misura si sposta sui
diff git dello specchio orario:

- la chiave e' l'ID del lavoro (prima colonna della riga Lavori), non il testo della riga:
  un lavoro e' "nuovo nel giorno D" se il suo ID compare per la prima volta in un commit
  dello specchio con data D. Un cambio di stato o di testo su un ID gia' visto non conta come
  lavoro nuovo;
- il commit di migrazione che introduce il campo `progetto` e' escluso dal conteggio;
- la finestra di 7 giorni comincia con il primo commit dello specchio successivo
  all'installazione della release che introduce il campo;
- la quota e' il rapporto fra ID nuovi con `progetto = board` e ID nuovi totali nella
  finestra;
- `board` deve comparire nell'elenco progetti;
- il calcolo e' riproducibile da chiunque abbia accesso in sola lettura al repo dati.

Soglia: oltre il 10% la Fase 2 si ferma e questo ADR va rivisto verso RESTRINGI. Il calcolo
lo fa il reviewer, non il coordinatore. Il 10% e' il valore proposto dallo spec, non
misurato.

Fatto collegato: il criterio di uscita di ADR-0045 misura collisioni e tocchi manuali dalla
storia git del file board. Le collisioni usano il lease "ricavato dalla storia git"; i tocchi
manuali si misurano "sui commit senza trailer `Coding-Agent`". Finora quella storia non
esisteva con continuita', perche' lo stato vivo stava non committato in un checkout. Lo
specchio la fornirebbe con granularita' oraria. E' un beneficio della Fase 1 per ADR-0045,
indipendente dall'esito di questo ADR.

Pilastri: RINVIA e RATIFICA rispettano sovereign-first e no-lock-in (file in Git, nessun
servizio nuovo, libreria standard). La RATIFICA va contro il rinvio del bus deciso nello spec
orchestratore; lo spec pero' e' superato e il suo gate obsoleto, ed e' per questo che si
decide nel merito.

### Implementation plan

Con RINVIA (subito):
- Step 1 -- nota "Livelli ombra" in AGENTIC_OS.md (fatta in questo cambio).
- Step 2 -- prove di uscita della Fase 1 e verifica del reviewer indipendente (proposta:
  circa 1 ora, stima non misurata).
- Step 3 -- refresh di STATUS_MULTI_REPO.md, senza nomi di repo privati.

Con RATIFICA (dopo X e Y; tutto fuori da questo repo salvo dove indicato):
- Step 4 -- chiudere la domanda su ADR-0036 decisione 6 (emendamento o dichiarazione).
- Step 5 -- Fase 2, una sola release nel repo d'origine: TTL, `archive`, campo `progetto`,
  `migrate --dry-run`. Codex via Board, review di kimi-native e del reviewer severo prima
  del merge, merge di Eduardo.
- Step 6 -- triage dei 40 messaggi che chiedono azione: propone un agente, decide Eduardo.
- Step 7 (separato, opzionale) -- la Board come sorgente R0 solo-conteggi, esclusa dal blocco
  pubblico. PR propria in questo repo, con un controllo negativo: un nome di repo privato nel
  segnale deve far fallire il test.
- Step 8 -- il Gate B in ESCALATION_GATES.md annotato come deciso da questo ADR. E' un file
  di dottrina: lo puo' mergiare solo Eduardo (ADR-0040).

### Consequences

#### Positive

- Il livello ombra ha un nome, una nota in AGENTIC_OS.md e un'autorita' scritta, anche se
  solo Proposed.
- Il confine fra Board, governor ed EXECUTION-BOARD.md e' esplicito.
- Il Gate B obsoleto viene chiamato col suo nome, invece di essere chiuso con un conteggio.

#### Negative

- Con RINVIA il bus continua a esistere senza ratifica per un tempo non definito.
- La domanda su ADR-0036 decisione 6 resta aperta.
- La Board resta un file condiviso letto da agenti cloud: il limite di privacy e' noto e non
  risolto.

### Mitigations

- Trigger di revisione scritti (Notes).
- Con RATIFICA, clausola di arresto sui diff dello specchio, calcolata dal reviewer.
- Una sola release; una seconda vuol dire stop e nuovo OK di Eduardo (spec, sez. 8).
- Rollback della Fase 2: se il dry-run non coincide con il reale, la release non si installa.
  Che il parser nuovo legga anche lo schema v2 e' una proposta dello spec, da verificare con
  un test prima del merge.

## Risultati negativi / cosa la Fase 1 non risolve

Sono scritti qui perche' nessuna opzione li cancella.

- **Due versioni del writer, tre scrittori.** Lo specchio copia il file, ma non cambia chi lo
  scrive. Chi entra via SSH usa ancora il writer vecchio (-457 righe nette rispetto a
  `main`). La Fase 1 consegna solo un inventario di quale writer usare. Il problema si
  risolverebbe solo con la Fase 3 (spostamento, con il file congelato sul posto), che non e'
  progettata e richiede una nuova approvazione.
- **Checkout fermo.** Lo stato vivo resta in un checkout condiviso, su un ramo molto indietro
  rispetto a `main`, che ospita anche altro stato vivo. Un cambio di ramo o un reset li'
  cancellerebbe stato vivo. Lo specchio dovrebbe limitare la perdita a un'ora, ma finche' le
  prove di uscita non passano non e' verificato. In ogni caso non toglie il rischio.
- **Percorso scritto nel codice** in piu' punti: la Fase 1 non lo cambia.
- **43 lavori fermi in `review`**: senza data sulle righe Lavori il collo di bottiglia non si
  puo' misurare. E' un buco dichiarato, non un obiettivo. I diff dello specchio darebbero una
  data di comparsa solo alle righe future.
- **Accesso da Lenovo**: lo spec propone la lettura con `git pull` dallo specchio, non ancora
  verificata. Per scrivere resterebbe comunque SSH.
- **Privacy della Board**: nessun controllo impedisce che nel file finisca contenuto sovrano.
- **Gate B non contabile in modo pulito** finche' STATUS_MULTI_REPO.md non viene aggiornato,
  e comunque obsoleto nella sostanza.

## Related

- **ADR-0036** -- dottrina di orchestrazione, decisione 6. Vedi la sezione dedicata: la
  posizione della Board resta aperta.
- **ADR-0045** (Proposed) -- cockpit di worktree. Regola 3: la Board resta in Git come
  archivio autoritativo dei task. Checklist punto 2: nessun canale di messaggi fra agenti
  dentro un'app. Criterio di uscita: storia git del file board. Fonti di due misure usate
  qui: 60 commit di meta-lavoro su 178 e "la Board non funziona ancora".
- **ADR-0039** -- rung R1 di reconcile, che scrive PR su file pubblici: per questo esiste la
  regola 4 del confine.
- **ADR-0040** -- i file di dottrina (`docs/governance/**`, `docs/adr/**`) li mergia solo
  Eduardo.
- **ADR-0044** -- Agentic OS come composizione; mappa a 7 layer. La Board compare in una nota
  separata, non come ottavo layer.
- Spec governor di flotta (2026-06-01), sez. 4: separazione fra log consultivo e `acted_on`.
- Spec console Agentic OS (2026-07-12): legge la tabella dei layer.
- Spec fleet-tools MCP (2026-05-29): `cross_check` come reviewer indipendente.
- ESCALATION_GATES.md: definizione e lettura dei gate ("checkpoint, NOT prescription").
- BACKLOG.md: X4 (Gate E) chiuso il 2026-06-11; il Gate B non risulta mai valutato.

## Notes

- Perche' ora: lo spec della Board di flotta mette questo ADR come cancello. Senza esito la
  Fase 2 non si scrive.
- Target Accepted: la firma di Eduardo, dopo la review severa. Con esito RINVIA lo stato
  resta Proposed fino a uno dei trigger sotto.
- Trigger di revisione (valori proposti, non misurati):
  1. prove di uscita della Fase 1 verificate e STATUS_MULTI_REPO.md aggiornato (cioe' X e Y);
  2. board viva oltre 250 KB;
  3. piu' di 20 messaggi che chiedono azione oltre i 7 giorni;
  4. un secondo incidente di stato perso nel checkout condiviso.
- Questo draft non aggiorna DECISIONS_LOG.md, docs/adr/README.md, COMPACT_CONTEXT.md ne'
  BACKLOG.md: sono fuori dal perimetro del task e vanno fatti al commit.
