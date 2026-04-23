# SAFE_CHANGES_ONLY

Questo documento definisce cosa Claude Code può cambiare senza approvazione esplicita.

## Cambiamenti normalmente consentiti

### Documentazione operativa
Claude può creare o aggiornare:
- brief
- compact context
- decision log
- backlog
- repo map
- migration plan
- sprint docs
- audit tecnici
- checklist operative

### Struttura di supporto
Claude può:
- aggiungere cartelle docs/reports/plans/sprints se mancanti
- normalizzare file di supporto
- creare file canonici mancanti
- aggiungere template e indici

### Refactor locali a basso rischio
Claude può:
- estrarre funzioni pure
- separare confini simulation/UI su un boundary locale
- migliorare naming locale se non rompe contratti
- aggiungere test attorno a logica core esistente
- isolare stato o logica deterministic-friendly

### Sicurezza e manutenzione
Claude può:
- rimuovere codice morto chiaramente non referenziato
- aggiungere commenti strutturali o docstring utili
- creare baseline test o smoke checks
- documentare debito tecnico

## Cambiamenti che richiedono checkpoint umano

### Gameplay core
- cambiare round flow
- cambiare initiative/reaction logic
- cambiare win/loss conditions
- cambiare informazioni visibili ai giocatori
- cambiare struttura delle decisioni interessanti

### Architettura a rischio alto
- spostare molti moduli contemporaneamente
- introdurre nuovi layer astratti non giustificati
- riscrivere core systems senza piano di migrazione
- cancellare sistemi ancora ambigui ma forse centrali

### Product / scope
- cambiare priorità di roadmap
- tagliare feature centrali senza decisione registrata
- trasformare un prototipo in direzione diversa dalla visione corrente

## Regola pratica

Se una modifica è:
- locale
- reversibile
- testabile
- coerente con i file canonici
- ad alto leverage

allora è di solito safe.

Se è:
- ampia
- irreversibile
- poco testabile
- vision-sensitive
- con effetti di secondo ordine

allora non è safe senza gate.

## Azione in caso di dubbio

Non fermarti subito.
Fai così:
1. documenta l'ambiguità
2. proponi default migliore
3. continua su parti non bloccate
4. apri `OPEN_DECISIONS.md`
