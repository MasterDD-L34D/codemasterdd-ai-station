# Multi-AI Routing — NotebookLM -> ChatGPT -> Claude Code

## Principio guida
Usa sempre questa regola:

**Fonte complessa -> Comprensione -> Compressione -> Decisione -> Esecuzione -> Compact**

Non mandare subito tutto nello strumento più forte.
Prima scegli chi deve fare cosa.

## Ruoli consigliati per strumento
### NotebookLM
Usalo per:
- grandi set di fonti
- PDF, documentazione, slide, articoli, note e fonti eterogenee
- capire velocemente un corpus documentale
- fare chat grounded sulle fonti
- generare overview, briefing e materiali di studio

Non usarlo come strumento principale per:
- refactoring del repo
- architettura di codice in-session sul progetto
- implementazione modulo per modulo

### Claude Code
Usalo per:
- leggere il repo
- fare repo map e audit
- ricostruzione first principles del core tecnico
- scrivere moduli, test e piani di migrazione

### ChatGPT / libreria operativa
Usalo per:
- orchestrare il workflow
- trasformare materiali sparsi in sistema
- progettare moduli, prompt, piani, backlog e documenti
- integrare risultati provenienti da altri strumenti
- consolidare compact, decision log, prompt library e reference

### Modelli economici / locali / mini
Usali per:
- compressione preliminare di PDF o trascrizioni
- classificazione
- pulizia testo
- deduplicazione
- passaggi ad alto volume ma bassa profondità

## Workflow consigliato con NotebookLM
1. raccogli le fonti
2. caricale o centralizzale in NotebookLM
3. usa NotebookLM per ottenere:
   - overview del corpus
   - domande/risposte grounded
   - nodi concettuali
   - sintesi per tema
4. esporta o copia la sintesi densa
5. porta la sintesi nella libreria operativa
6. usa ChatGPT o Claude Code per trasformarla in design, piano o implementazione

## Routing consigliato per un repo game
### Caso A — Hai tantissima documentazione sparsa
Usa:
- NotebookLM per comprendere corpus e fonti
- ChatGPT per trasformare la comprensione in struttura operativa
- Claude Code per agire sul repo

### Caso B — Hai già capito il gioco ma il repo è il problema
Usa:
- ChatGPT per definire prompt e workflow
- Claude Code per repo map, audit, migration plan, coding

NotebookLM qui è opzionale.

### Caso C — Devi riallineare gioco, documentazione e codice
Usa:
- NotebookLM per ricostruire la conoscenza dispersa
- ChatGPT per sintetizzare contraddizioni, decisioni e piano
- Claude Code per implementare la nuova architettura minima

## Cosa chiedere a NotebookLM
### Panorama iniziale
```text
Leggi tutte queste fonti come se dovessi spiegare il progetto a un nuovo collaboratore.
Dimmi:
1. qual è il tema centrale
2. quali concetti ricorrono di più
3. quali contraddizioni emergono
4. quali decisioni sembrano implicite ma non formalizzate
5. cosa manca per trasformare tutto in un brief operativo
```

### Sintesi densa del corpus
```text
Riassumi questo notebook in forma densa e operativa.
Preserva:
- decisioni
- definizioni
- concetti chiave
- vincoli
- dubbi aperti
- elementi ripetuti che sembrano strutturali

Rimuovi:
- ripetizioni ridondanti
- esempi marginali
- riempitivi
- dettagli non utili a pianificazione o implementazione
```

### Contraddizioni e conflitti
```text
Analizza le fonti e dimmi:
1. dove due documenti o note sembrano dire cose incompatibili
2. quali concetti cambiano significato tra una fonte e l’altra
3. quali parti sembrano obsolete
4. quali elementi dovrebbero essere decisi ufficialmente
```

### Brief per il coding
```text
Partendo dalle fonti, crea un brief per un engineer che deve lavorare sul repo.
Includi:
1. obiettivo del sistema
2. vincoli hard
3. componenti che sembrano core
4. domande ancora aperte
5. rischi di implementazione
```

## Prompt ponte — da NotebookLM a ChatGPT
```text
Ho usato NotebookLM per analizzare un corpus di fonti.
Qui sotto trovi la sintesi risultante.

Agisci come Project Architect + Archivist + PM.

Voglio:
1. separare reference, decisioni, vincoli, idee e problemi aperti
2. trasformare il materiale in brief, backlog e decision log
3. evidenziare le contraddizioni da risolvere
4. dirmi quale modulo della libreria usare subito dopo

Sintesi:
[incolla qui l’output di NotebookLM]
```

## Prompt ponte — da NotebookLM a Claude Code
```text
Questa sintesi proviene da NotebookLM ed è basata sulle fonti del progetto.

Trasformala in un brief tecnico per Claude Code.
Voglio:
1. obiettivo core del sistema
2. vincoli hard
3. ipotesi da validare
4. componenti presumibilmente core
5. domande bloccanti prima del refactor

Sintesi:
[incolla qui]
```

## Pacchetto operativo per repo game
### Checklist — cosa mettere in NotebookLM
Sorgenti prioritarie:
- game design notes
- brief del progetto
- descrizioni del core loop
- documenti sulla singola partita o round flow
- note su unità, abilità, AI, economy, UX di partita
- screenshot annotati o raccolte di riferimenti
- design bible
- backlog o TODO di design
- estratti di conversazioni lunghe che contengono decisioni reali

Sorgenti da evitare nel primo passaggio:
- dump enormi di codice senza contesto
- asset binari non leggibili
- materiale puramente visuale senza legenda
- backlog vecchi non verificati

### Cartella di staging consigliata
```text
NotebookLM_Staging/
- 01_Project_Brief
- 02_Game_Design_Core
- 03_Round_and_Combat
- 04_Systems_and_Economy
- 05_UX_and_Player_Experience
- 06_Backlog_and_Decisions
- 07_Screenshots_and_References
- 08_Old_or_Conflicting_Material
```

### Prompt starter per NotebookLM — Repo Game Corpus
#### 1. Spiegami il progetto
```text
Leggi tutte queste fonti come se dovessi spiegare il progetto a un nuovo collaboratore che dovrà lavorare al gioco e al suo repository.

Dimmi:
1. qual è il fantasy del giocatore
2. qual è il core loop del gioco
3. quali sistemi sembrano davvero centrali
4. quali decisioni sembrano già prese
5. quali punti sono ancora vaghi, incoerenti o contraddittori
6. cosa dovrei chiarire prima di toccare il repo
```

#### 2. Unità minima di partita
```text
Partendo da queste fonti, dimmi qual è l’unità minima di esperienza che il gioco deve far funzionare bene.

Voglio capire:
1. cos’è una singola partita o encounter in questo progetto
2. quali input minimi servono
3. quali stati del match devono esistere
4. quali trasformazioni devono avvenire durante un round
5. quali output o feedback il giocatore deve vedere chiaramente
```

#### 3. Contraddizioni importanti
```text
Trova le contraddizioni più importanti in queste fonti.

Per ciascuna dimmi:
1. quali fonti sono in conflitto
2. su quale sistema o concetto litigano
3. quale versione sembra più aggiornata o più coerente
4. quale decisione andrebbe formalizzata nel decision log
```

#### 4. Materiali per il coding
```text
Trasforma questo corpus in un brief per un engineer che dovrà ricostruire il repo game.

Includi:
1. obiettivo core del gioco
2. sistemi minimi da far funzionare
3. vincoli hard impliciti o espliciti
4. aree dove il codice dovrebbe essere testabile e separato dalla UI
5. punti ancora ambigui da non dare per scontati
```

#### 5. Sintesi finale export-ready
```text
Crea una sintesi densa, pronta da esportare verso un altro strumento AI.

Preserva:
- verità fondamentali del gioco
- sistemi principali
- vincoli
- decisioni prese
- dubbi aperti
- priorità implicite

Rimuovi:
- ripetizioni
- esempi marginali
- dettagli non operativi
- formulazioni troppo narrative

Output come brief strutturato, non come testo promozionale.
```

## Output attesi da NotebookLM prima di passare oltre
1. una spiegazione chiara del progetto
2. una definizione dell’unità minima di partita
3. una lista delle contraddizioni principali
4. un brief per engineer
5. una sintesi densa esportabile

## Prompt ponte — da NotebookLM a ChatGPT
### Ponte base — da sintesi a sistema operativo
```text
Questa sintesi viene da NotebookLM ed è basata sulle fonti del progetto game.

Agisci come Project Architect + PM + Archivist.

Voglio:
1. separare reference, decisioni, vincoli, idee ancora aperte e problemi
2. identificare cosa deve entrare in PROJECT_BRIEF, DECISIONS_LOG e BACKLOG
3. costruire una struttura operativa per lavorare sul repo game
4. dirmi quale modulo della libreria usare subito dopo

Sintesi:
[incolla qui]
```

### Ponte audit — da sintesi a mappa dei rischi
```text
Partendo da questa sintesi di NotebookLM, crea una mappa dei rischi del progetto.

Voglio:
1. rischi di design
2. rischi di architettura
3. rischi di scope
4. punti non decisi che possono compromettere il refactor
5. priorità assolute da chiarire prima di toccare il core del repo

Sintesi:
[incolla qui]
```

### Ponte archivio — da sintesi a documenti di progetto
```text
Trasforma questa sintesi in 4 sezioni pronte da archiviare:
1. Project Brief
2. Compact Context
3. Decision Log provvisorio
4. Backlog iniziale

Mantieni il testo denso, chiaro e riusabile fuori contesto.

Sintesi:
[incolla qui]
```

## Output attesi da ChatGPT prima di Claude Code
- `PROJECT_BRIEF` pulito
- primo `COMPACT_CONTEXT`
- bozza di `DECISIONS_LOG`
- `BACKLOG` iniziale
- brief tecnico specifico per il repo
- elenco di contraddizioni ancora aperte
- vincoli hard esplicitati

## Prompt ponte — da ChatGPT a Claude Code
### Brief tecnico verso Claude Code
```text
Ti passo il brief tecnico consolidato del progetto game.

Agisci come Principal Engineer e Systems Architect.

Prima leggi questo brief come fonte di verità operativa del progetto.
Poi analizza il repo rispettando questi vincoli e questi obiettivi.
Infine dimmi:
1. dove il repo attuale supporta bene il core del gioco
2. dove lo tradisce
3. quale primo modulo o confine architetturale va stabilizzato

Brief:
[incolla brief tecnico]
```

### Brief tecnico + first principles reconstruction
```text
Userai il brief seguente come contesto fondamentale del progetto.
Non assumere che il repo attuale sia corretto.

Dopo aver letto il brief, applica un’analisi first principles del repository:
- verità fondamentali del gioco
- verità fondamentali del sistema
- verità fondamentali del repo
- architettura minima ricostruita
- strategia di migrazione migliore
- primo modulo atomico da implementare

Brief:
[incolla brief]
```

### Brief tecnico + repo map iniziale
```text
Leggi questo brief e poi crea una repo map orientata al gameplay core.

Non voglio solo la struttura cartelle.
Voglio sapere:
1. dove dovrebbe vivere la simulazione pura
2. dove dovrebbe stare l’orchestrazione
3. dove stanno UI, adapter e tooling
4. dove il repo attuale mescola livelli che andrebbero separati

Brief:
[incolla brief]
```

## Sequenza ideale completa — Repo Game Multi-AI
1. Raccolta in `00_Inbox`
2. Staging per NotebookLM
3. NotebookLM
4. ChatGPT
5. Claude Code
6. Ritorno alla libreria
7. Compact finale

## Protocollo di ritorno nella libreria
### In `DECISIONS_LOG`
- strategia di migrazione scelta
- componenti che saranno considerati core
- componenti da deprecare o congelare

### In `BACKLOG`
- step 1 del migration plan
- task del primo sprint tecnico
- rischi da monitorare

### In `COMPACT_CONTEXT`
- cosa è stato capito del repo
- cosa è stato deciso
- qual è il prossimo modulo da toccare

### In `REFERENCE_INDEX`
- link o riferimento al report Claude Code
- classificazione come audit, design ricostruito o migration plan

## Checklist veloce — se il workflow si è bloccato
1. sto usando NotebookLM per capire qualcosa che in realtà è già chiaro?
2. sto mandando a Claude Code documentazione ancora troppo grezza?
3. sto saltando il passaggio di consolidamento in ChatGPT?
4. manca un vincolo hard esplicitato?
5. stiamo discutendo architettura senza aver fissato l’unità minima di partita?

## Regola finale
Questo pacchetto funziona bene solo se il passaggio tra strumenti produce sempre un oggetto più chiaro del precedente.

Deve succedere questo:
- le fonti diventano comprensione
- la comprensione diventa struttura
- la struttura diventa brief tecnico
- il brief tecnico diventa piano di ricostruzione
- il piano di ricostruzione diventa sprint reale
