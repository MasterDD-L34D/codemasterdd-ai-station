# CodeMasterDD AI Station — Archivio documentazione

Archivio della memoria progettuale e decisionale del setup workstation
AI sovereign del 18-20 aprile 2026.

## Filosofia di questo archivio

Questo non è un wiki, non è documentazione "pulita" a posteriori.
È un **codex vivente**: registro narrativo di decisioni prese, errori evitati,
pattern identificati, ricerche svolte. Scritto in tempo reale durante
il setup, senza sanitizzazione post-hoc.

Obiettivo: **me stesso del passato è gentile con me stesso del futuro**.

## Struttura

```
docs/
├── sessions/           # Narrative sessioni operative (journal esteso)
├── adr/                # Architecture Decision Records (34)
├── research/           # Ricerche svolte durante le decisioni
├── patterns/           # Pattern operativi emersi (riutilizzabili)
├── lessons-learned/    # Cosa ho imparato dai trauma/successi
├── reference/          # Cheatsheet tecnici pronto-uso
├── runbook/            # Runbook operativi (setup, deploy, recovery)
├── operations/         # Matrici operative (key routing, task routing)
├── reviews/            # Processi di review (harsh review flow)
├── strategy/           # Strategie di esecuzione (parallel execution)
├── plans/              # Piani di integrazione
├── cross-repo/         # Coordinamento cross-repo (PR, escalation)
├── agent-smoke-tests/  # Smoke test per agent AI
├── aa01-handoff/       # Handoff AA01 (workspace personale)
├── jules/              # Jules capabilities master
├── jules-batch/        # Jules batch records
└── superpowers/        # Design specs e implementation plans
```

## Cronologia temporale

- **17/04/2026**: disastro Victus (BitLocker + KB5083769)
- **18/04/2026**: negoziazione Euronics, sostituzione → Lenovo LOQ Tower
- **19/04/2026** (notte): sessione di hardening sistema, Claude Code install
- **19/04/2026** (sera): GitHub setup, dev stack, Ollama bonus

## Come leggere

### Se sei io stesso tra 6 mesi e cerco "come avevo fatto X"
→ `reference/commands-cheatsheet-windows.md`

### Se sei io stesso tra 1 anno e cerco "perché avevo deciso Y"
→ `adr/`

### Se sei io stesso in futuro trauma e cerco "come resisti"
→ `lessons-learned/victus-trauma-postmortem.md`

### Se sei persona esterna che vuole capire il progetto
→ leggi in quest'ordine:
1. `sessions/2026-04-19-sessione-notturna.md` (il trauma e la recovery)
2. `sessions/2026-04-19-sessione-serale.md` (il setup completo)
3. `adr/0001-sovereign-ai-strategy.md` (perché questo progetto esiste)
4. `lessons-learned/capire-prima-fare-dopo.md` (il metodo)

## Meta

**Autore**: Eduardo Scarpelli (MasterDD-L34D / @eduscarpelli)
**Collaboratore AI**: Claude (Opus 4.7, con compaction esplicita)
**Licenza**: uso personale. Riuso permesso con attribuzione.
**Lingua**: italiano esteso. Alcuni termini tecnici restano in inglese.

## Note sui file

- Tutti i file sono `.md` standard compatibile GitHub + VS Code preview
- Dimensioni variabili (da 200 a 8.000+ parole per file)
- Conteggio totale archivio (2026-05-24): ~171.000 parole
- I subdirectory aggiuntivi riflettono l'espansione del repository

## File count (2026-05-24)

```
sessions/            7 file
adr/                34 file
research/           21 file
patterns/            7 file
lessons-learned/     3 file
reference/           5 file
runbook/             7 file
operations/          1 file
reviews/             1 file
strategy/            1 file
plans/               1 file
cross-repo/          5 file
agent-smoke-tests/   9 file
aa01-handoff/        2 file
jules/               1 file
jules-batch/         2 file
superpowers/plans/   4 file
superpowers/specs/   8 file
README.md            1 file (questo)
TOTALE             119 file
```
