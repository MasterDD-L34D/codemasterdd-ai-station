# CodeMasterDD AI Station — Archivio documentazione

Archivio della memoria progettuale e decisionale del setup workstation
AI sovereign del 18-20 aprile 2026.

## Filosofia di questo archivio

Questo non e' un wiki, non e' documentazione "pulita" a posteriori.
E' un **codex vivente**: registro narrativo di decisioni prese, errori evitati,
pattern identificati, ricerche svolte. Scritto in tempo reale durante
il setup, senza sanitizzazione post-hoc.

Obiettivo: **me stesso del passato e' gentile con me stesso del futuro**.

## Struttura (riorganizzata 2026-06-04 -- vedi PR chore/docs-reorg)

Ogni directory top-level ha un proprio `README.md` indice.

```
docs/
+-- adr/            # Architecture Decision Records (authoritative, ~39)
+-- archive/        # Frozen: ryzen-memory-archive, aa01-handoff, plans, snapshot storici
+-- governance/     # Cross-repo: PR workflow, escalation gates, review flow, execution board
+-- handoffs/       # Session handoff + continuity logs (ex sessions/)
+-- jules-batch/    # Jules digest cron output (automation sink ATTIVO, non archiviare)
+-- reference/      # Cheatsheet + patterns/ + lessons/ (reference stabile)
+-- research/       # Ricerche esplorative datate
+-- runbook/        # Playbook operativi + routing matrix
+-- superpowers/    # Agent capabilities: specs/, plans/, tests/, jules/
```

Note sul riassetto 2026-06-04:
- `sessions/` -> `handoffs/` (rename).
- `patterns/` + `strategy/` -> `reference/patterns/`; `lessons-learned/` -> `reference/lessons/`.
- `cross-repo/` + `reviews/` -> `governance/`.
- `agent-smoke-tests/` -> `superpowers/tests/`; `jules/` + `goals/` -> `superpowers/jules/`.
- `operations/` -> `runbook/` (flat); `ryzen-memory-archive/` + `aa01-handoff/` + `plans/` -> `archive/`.
- `jules-batch/` resta top-level: e' lo sink del cron digest (scritto da `scripts/jules-daily-digest.ps1`, letto dal governor).

## Cronologia temporale

- **17/04/2026**: disastro Victus (BitLocker + KB5083769)
- **18/04/2026**: negoziazione Euronics, sostituzione -> Lenovo LOQ Tower
- **19/04/2026** (notte): sessione di hardening sistema, Claude Code install
- **19/04/2026** (sera): GitHub setup, dev stack, Ollama bonus

## Come leggere

### Se sei io stesso tra 6 mesi e cerco "come avevo fatto X"
-> `reference/commands-cheatsheet-windows.md`

### Se sei io stesso tra 1 anno e cerco "perche' avevo deciso Y"
-> `adr/`

### Se sei io stesso in futuro trauma e cerco "come resisti"
-> `reference/lessons/victus-trauma-postmortem.md`

### Se sei persona esterna che vuole capire il progetto
-> leggi in quest'ordine:
1. `handoffs/2026-04-19-sessione-notturna.md` (il trauma e la recovery)
2. `handoffs/2026-04-19-sessione-serale.md` (il setup completo)
3. `adr/0001-sovereign-ai-strategy.md` (perche' questo progetto esiste)
4. `reference/lessons/capire-prima-fare-dopo.md` (il metodo)

## Meta

**Autore**: Eduardo Scarpelli (MasterDD-L34D / @eduscarpelli)
**Collaboratore AI**: Claude (con compaction esplicita)
**Licenza**: uso personale. Riuso permesso con attribuzione.
**Lingua**: italiano esteso. Alcuni termini tecnici restano in inglese.

## Note sui file

- Tutti i file sono `.md` standard compatibile GitHub + VS Code preview
- Dimensioni variabili (da 200 a 8.000+ parole per file)
- I subdirectory riflettono l'espansione del repository nel tempo
