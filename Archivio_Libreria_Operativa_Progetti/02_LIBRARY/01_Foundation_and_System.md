# Foundation and System

## Scopo
Questa libreria serve a:
- evitare di ripartire da zero a ogni progetto
- mantenere contesto, decisioni e output in ordine
- distinguere tra strategia, esecuzione, revisione e archivio
- usare prompt e ruoli stabili invece di richieste improvvisate
- comprimere il contesto senza perdere le decisioni importanti

## Regola madre
Usa sempre questa sequenza:

**Reference -> Adattamento -> Workflow -> Output -> Compact -> Archivio**

Non copiare un prompt a caso.
Prima scegli il tipo di progetto.
Poi scegli il modulo.
Poi scegli il prompt più adatto.
Poi lo adatti al contesto.
Infine salvi il risultato e aggiorni la memoria del progetto.

## Principi guida
1. Prima il sistema, poi il task
2. Un progetto = una memoria organizzata
3. Un prompt madre batte 100 prompt casuali
4. Il contesto va compresso regolarmente
5. I ruoli vanno separati
6. Ogni output deve essere riutilizzabile

## Struttura universale definitiva
```text
00_Inbox
01_Project_Brief
02_Objectives_and_Scope
03_Research
04_Strategy
05_Execution
06_Assets
07_Reviews_and_QA
08_Decisions
09_Backlog
10_Deliverables
90_AI_Output
95_Reference_Library
99_Templates
```

## File base da creare sempre
- `PROJECT_BRIEF.md`
- `COMPACT_CONTEXT.md`
- `DECISIONS_LOG.md`
- `BACKLOG.md`
- `MASTER_PROMPT.md`
- `REFERENCE_INDEX.md`
- `PROMPT_LIBRARY.md`

## Prompt madre definitivo
```text
Agisci come supporto operativo per questo progetto.

Prima di rispondere:
1. identifica l’obiettivo reale
2. separa fatti, ipotesi, problemi e priorità
3. non mescolare strategia e output finale se non richiesto
4. proponi una struttura ordinata
5. evidenzia blocchi, rischi, dipendenze e prossimi passi

Contesto progetto:
[incolla brief o compact context]

Tipo di progetto:
[software / game design / ricerca / brand / scrittura / business / studio / altro]

Modalità attiva:
[STRATEGY MODE / PM MODE / EXECUTION MODE / REVIEW MODE / AUDIT MODE / CREATIVE MODE / RESEARCH MODE / SYSTEMS MODE]

Ruolo attivo:
[Project Architect / Research Analyst / Builder / Reviewer / QA Auditor / Brand Strategist / Systems Designer / Writer / Tech Lead / Product Designer]

Output richiesto:
[analisi / piano / checklist / documento / template / prompt / revisione / backlog / decision log / report / handoff]

Vincoli:
- sii concreto
- non duplicare
- mantieni coerenza col contesto
- se mancano dati, esplicita cosa manca
- distingui chiaramente tra certo, probabile e ipotetico

Formato di output:
1. Sintesi
2. Struttura operativa
3. Rischi o punti deboli
4. Prossimi passi
```

## Mappa decisionale: quale prompt usare
### Se devi capire il progetto
Usa:
- `/INTAKE`
- `/STRUCTURE`
- Project Architect

### Se devi decidere una direzione
Usa:
- `/DECIDE`
- STRATEGY MODE
- Research Analyst o Systems Designer

### Se devi costruire davvero qualcosa
Usa:
- `/BUILD`
- EXECUTION MODE
- Builder o Tech Lead o Writer

### Se devi migliorare qualcosa che esiste già
Usa:
- `/REVIEW`
- REVIEW MODE
- Reviewer

### Se devi trovare problemi nascosti
Usa:
- `/AUDIT`
- AUDIT MODE
- QA Auditor o Security Auditor

### Se devi chiudere bene una sessione
Usa:
- `/COMPACT`
- Archivist

## Comandi rapidi definitivi
- `/INTAKE`
- `/STRUCTURE`
- `/PLAN`
- `/BUILD`
- `/REVIEW`
- `/AUDIT`
- `/DECIDE`
- `/BACKLOG`
- `/HANDOFF`
- `/COMPACT`
- `/FORMAT AS`
- `/COMPARE`
- `/MULTI-PERSPECTIVE`
- `/SWOT`

## Sistema di qualità per scegliere un prompt
Prima di usare un prompt, controlla:
1. Serve davvero a questo progetto?
2. È universale o richiede adattamento?
3. È un prompt sorgente o già un prompt operativo?
4. Mi serve strategia, esecuzione o audit?
5. Sto cercando chiarezza o profondità?
6. Devo produrre un file o solo pensare meglio?

Se non sai quale usare, parti sempre da:
- Project Architect
- `/INTAKE`
- `/STRUCTURE`

## Rituali operativi di sessione
### Apertura sessione
1. leggi `COMPACT_CONTEXT.md`
2. dichiara l’obiettivo della sessione
3. scegli modalità + ruolo

### Chiusura sessione
1. aggiorna `COMPACT_CONTEXT.md`
2. aggiorna `DECISIONS_LOG.md`
3. aggiorna `BACKLOG.md`
4. scrivi la prossima azione singola più utile

## Versione ultra-rapida da usare subito
```text
Voglio avviare o rimettere in ordine un progetto.

Agisci come Project Architect + PM + Archivist.

1. chiarisci l’obiettivo reale
2. separa caos, materiali, vincoli e priorità
3. crea una struttura di lavoro riusabile
4. genera backlog e prossimi passi
5. indica il modulo e il prompt migliore da usare subito dopo

Materiale:
[incolla tutto]
```
