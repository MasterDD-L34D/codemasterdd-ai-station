# CLAUDE_OPERATING_RULES

Queste sono le regole operative canoniche per Claude Code dentro questo progetto.

## 1. Priorità delle fonti

Tratta queste fonti di verità in quest'ordine:

1. Decisioni esplicite nei file canonici del progetto
2. Brief di progetto e compact context aggiornato
3. Regole della libreria operativa e checklist validate
4. Stato reale del repository
5. Inferenza ragionevole
6. Domande aperte

Se due fonti confliggono:
- non scegliere in silenzio
- descrivi il conflitto
- proponi la riconciliazione migliore
- registra il punto in `OPEN_DECISIONS.md` o `DECISIONS_LOG.md`

## 2. Obiettivo primario

Non ottimizzare il repo per eleganza astratta.
Ottimizzalo per:
- chiarezza del gioco
- testabilità del core
- separazione dei livelli
- velocità di iterazione
- migrazione reale e sicura

## 3. Livelli da non mescolare

Mantieni distinti:
- verità del gioco
- verità del sistema
- verità del repo

E mantieni distinti anche:
- simulation core
- orchestration
- adapters/infrastructure
- presentation/UI
- tooling/debug

## 4. File prima della chat

La tua uscita principale deve essere **file scritti nel progetto**, non spiegazioni lunghe in chat.

Usa la chat solo per:
- dire in che fase sei
- dire quali file hai creato o aggiornato
- segnalare decisioni veramente bloccanti

## 5. Quando puoi decidere da solo

Puoi decidere autonomamente se:
- la scelta è locale e reversibile
- la scelta non cambia il gameplay core
- la scelta migliora chiarezza o testabilità senza cambiare la visione
- il rischio è basso e il valore è alto
- la decisione è coerente con i file canonici

## 6. Quando devi fermarti

Devi fermarti e registrare una decisione aperta se:
- cambia il fantasy del giocatore
- cambia il core loop o il round flow
- modifica priorità di prodotto o scope strategico
- rimuove un sistema potenzialmente centrale ma ambiguo
- impone un compromesso pesante tra semplicità, profondità e leggibilità

## 7. Regola anti-cerimonia

Se una parte del repo:
- non sostiene una verità del gioco
- non sostiene una verità del sistema
- non sostiene un vincolo hard
- non migliora test, debug o iterazione

allora è candidata a:
- taglio
- congelamento
- rinvio
- isolamento

## 8. Regola di scrittura

Ogni file che crei deve essere:
- leggibile fuori contesto
- denso, non prolisso
- esplicito su cosa è certo e cosa è inferito
- utile per la sessione successiva

## 9. Regola di chiusura sessione

A fine sessione aggiorna sempre:
- `COMPACT_CONTEXT.md`
- `BACKLOG.md`
- `DECISIONS_LOG.md` se sono state prese decisioni
- `OPEN_DECISIONS.md` se restano ambiguità

## 10. Definizione di successo

Una sessione è riuscita se lascia il progetto:
- più comprensibile
- più testabile
- meglio documentato
- con il prossimo passo più chiaro di prima
