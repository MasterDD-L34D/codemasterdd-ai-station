# TASK_EXECUTION_PROTOCOL

Questo protocollo definisce l'ordine standard con cui Claude Code deve lavorare.

## Sequenza base obbligatoria

### Fase 0 — Orientamento
- trova root del repo
- trova root dell'archivio operativo
- identifica i file canonici
- identifica eventuali duplicati o file stale

### Fase 1 — Lettura minima obbligatoria
Leggi almeno:
- `PROJECT_BRIEF.md`
- `COMPACT_CONTEXT.md`
- `DECISIONS_LOG.md`
- `BACKLOG.md`
- `MODEL_ROUTING.md`
- `FIRST_PRINCIPLES_GAME_CHECKLIST.md`

Se mancano, segnalalo e crea una versione iniziale se il task lo richiede.

### Fase 2 — Mappa del task
Per ogni task, chiarisci:
- obiettivo reale
- livello coinvolto: game / system / repo
- file e moduli toccati
- rischio del cambiamento
- test o verifiche necessarie

### Fase 3 — Analisi
Analizza prima di cambiare.
Domande minime:
- cosa regge davvero questo pezzo?
- quale vincolo supporta?
- è simulation, orchestration, adapter o presentation?
- il cambiamento è locale o propaga?
- esiste già un punto migliore in cui intervenire?

### Fase 4 — Piano minimo
Scrivi sempre un micro-piano prima di toccare codice o file critici.
Formato minimo:
1. cosa cambio
2. perché lo cambio
3. cosa non tocco
4. come verifico

### Fase 5 — Esecuzione
Applica solo il cambiamento necessario.
Evita refactor ad ampio raggio nella stessa run se non esiste scaffolding di migrazione.

### Fase 6 — Verifica
Verifica almeno uno dei seguenti:
- test automatici
- analisi statica
- build minima
- controllo manuale ragionato
- coerenza con i file canonici

### Fase 7 — Aggiornamento memoria
Aggiorna i file di stato:
- `COMPACT_CONTEXT.md`
- `BACKLOG.md`
- `DECISIONS_LOG.md`
- `OPEN_DECISIONS.md`

## Protocollo speciale per task di refactor

1. mappa il confine del refactor
2. identifica se tocca gameplay assumptions
3. se sì, apri decisione o checkpoint
4. crea o aggiorna un report di refactor
5. esegui solo il primo boundary ad alto leverage

## Protocollo speciale per task di design-repo

Se il task riguarda il gioco e il repo insieme:
1. estrai game truths
2. estrai system truths
3. controlla se il repo le serve o le tradisce
4. poi modifica il repo

## Protocollo speciale per sprint

Per avviare uno sprint:
1. conferma obiettivo sprint
2. conferma file attesi
3. conferma definition of done
4. spezza in task piccoli
5. esegui un task alla volta
6. aggiorna backlog e compact a fine task importante
