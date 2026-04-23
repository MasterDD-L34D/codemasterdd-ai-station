# CHANGE_BUDGET

Questo documento limita quanto Claude Code può cambiare in una singola run senza controllo umano.

## Obiettivo

Evitare:
- refactor troppo larghi
- cascata di effetti non controllati
- perdita di contesto
- “big bang rewrites” mascherati da pulizia

## Budget standard per una singola run

### Documentazione
Consentito:
- più file docs
- più report
- più checklist
- aggiornamento bootstrap kit

### Codice
Per default, in una run Claude dovrebbe restare dentro uno di questi envelope:

#### Envelope A — basso rischio
- 1 modulo o boundary principale
- fino a 3-5 file di codice toccati
- test locali aggiunti o aggiornati
- nessun cambio a gameplay assumptions

#### Envelope B — medio rischio con scaffolding
- 1 sistema + 1 adapter collegato
- fino a 6-10 file
- piano di migrazione già scritto
- test o verifica chiara
- nessun cambio non documentato a verità del gioco

#### Envelope C — alto rischio
Non consentito senza checkpoint umano.
Esempi:
- riscrittura del core
- migrazione multipla di moduli
- nuove astrazioni architetturali ampie
- cambi di stato/flow che toccano più sistemi insieme

## Budget per tipo di task

### Repo map / audit
- nessun limite pratico: può leggere molto
- deve scrivere report sintetici e riusabili

### First principles reconstruction
- può produrre analisi e piani larghi
- non può eseguire larghi refactor solo perché li ha progettati

### Sprint execution
- un task ad alto leverage alla volta
- meglio finire un boundary bene che toccarne cinque male

## Regola di stop

Se durante una run emerge che per finire bene il task servirebbe:
- toccare molti moduli
- cambiare assunzioni di gioco
- fare riscrittura larga

allora Claude deve:
1. fermare l'esecuzione pratica
2. scrivere il nuovo confine del problema
3. aggiornare backlog/migration plan
4. proporre il checkpoint successivo

## Budget ideale per Evo-style repo game

Per un repo game in ricostruzione, il miglior default è:
- 1 boundary architetturale per run
- 1 step di migrazione per run
- 1 update dei file di memoria per run

Questo massimizza continuità e minimizza caos.
