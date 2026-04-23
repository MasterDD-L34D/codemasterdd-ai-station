# REPO_AUTONOMY_READINESS_CHECKLIST

Questa checklist misura quanto il progetto è pronto per essere lavorato in semi-autonomia da Claude Code.

## A. Verità canoniche del progetto
- [ ] Esiste un `PROJECT_BRIEF.md` utile e non vuoto
- [ ] Esiste un `COMPACT_CONTEXT.md` aggiornato
- [ ] Esiste un `DECISIONS_LOG.md` con decisioni vere
- [ ] Esiste un `BACKLOG.md` prioritizzato
- [ ] Esiste un `OPEN_DECISIONS.md` o template pronto

## B. Leggibilità del repo
- [ ] Esiste una repo map iniziale
- [ ] I moduli principali hanno responsabilità distinguibili
- [ ] La simulazione non è completamente fusa con la UI
- [ ] I punti di ingresso sono identificabili
- [ ] Esiste almeno una strategia minima di test o verifica

## C. Prontezza operativa
- [ ] Esistono regole operative per Claude Code
- [ ] Esiste un protocollo di esecuzione task
- [ ] Esistono regole su safe changes
- [ ] Esiste un change budget
- [ ] Esiste un prompt orchestratore usabile

## D. Prontezza first principles
- [ ] Le verità del gioco sono state almeno abbozzate
- [ ] Le verità del sistema sono almeno abbozzate
- [ ] Le verità del repo sono almeno abbozzate
- [ ] Esiste una checklist first-principles compilabile
- [ ] Esiste una strategia di migrazione o almeno un'ipotesi forte

## E. Routing strumenti
- [ ] Esiste un `MODEL_ROUTING.md`
- [ ] È chiaro quando usare NotebookLM, ChatGPT, Claude Code
- [ ] È chiaro quando usare locale vs cloud
- [ ] Esistono regole anti-caos per non duplicare lavoro tra tool

## Interpretazione

### 0-9 spunte
Il progetto non è ancora operabile bene da Claude Code. Serve Sprint 00.

### 10-17 spunte
Claude Code può aiutare bene, ma serve ancora guardrail forte.

### 18-24 spunte
Il progetto è vicino a una semi-autonomia reale.

### 25+ spunte
Claude Code può lavorare molto bene con supervisione minima e checkpoint intelligenti.
