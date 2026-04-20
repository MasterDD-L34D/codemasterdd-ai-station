# Aider delegation log — template

**Scopo**: tracciare ogni delegazione Claude Code → Aider locale per costruire il dataset decisionale Fase 6 (post-19/05 evaluation, ADR-0008 follow-up).

**Come usare**:
1. Copiare questo file in `logs/aider-delegation-YYYY-MM.md` a inizio mese (il path `logs/` è gitignored tranne `.gitkeep`, quindi il file istanza resta locale).
2. Compilare una riga per ogni delegazione durante la sessione (anche fallite o interrotte).
3. A fine mese fare aggregati: fail rate per classe task, top failure modes, token savings stimati.
4. ADR-0008 follow-up prevede review mensile durante il periodo 2026-05-20 → 2026-08-20.

## Schema tabella

| Data/ora | Task (1 riga) | Classe | Stack | Esito | Retry | Tokens sent/recv | Durata | Commit/note |
|----------|---------------|--------|-------|-------|-------|------------------|--------|-------------|
| YYYY-MM-DD HH:MM | Descrizione breve | cosmetic / behavior / strategic | 7B-whole / 14B-diff / claude | success / safe-fail / hook-block / corruption / error | 0 / 1 / 2 / 3+ | N / M | Ns | hash, errore o note |

### Valori ammessi

**Classe**:
- `cosmetic` — JSDoc, docstrings, rename, lint-fix, type annotations
- `behavior` — refactor, bug fix, logic change minimale, API signature
- `strategic` — multi-file, debug architetturale, design decisions (eseguite direttamente da Claude Code, NO delega — tracciate solo per ratio)

**Stack**:
- `7B-whole` — qwen2.5-coder:7b + `--edit-format whole` (default cosmetic)
- `14B-diff` — qwen2.5-coder:14b-instruct-q2_K + `--edit-format diff` + `--no-auto-commits` (default behavior)
- `claude` — eseguito direttamente da Claude Code (strategic o override)
- `other` — altro stack sperimentale (documentare in note)

**Esito**:
- `success` — edit applicato, diff corretto, task risolto
- `safe-fail` — Aider respinto input (es. missing filename), no edit, file intatto
- `hook-block` — pre-commit hook ha intercettato silent corruption pattern
- `corruption` — silent corruption passata al hook (BUG CRITICO → aprire issue / ADR revision)
- `error` — crash llama runner irrecuperabile, Ollama non risponde, timeout, etc.

**Retry**: numero di reflection retry di Aider (0 = first-try success, 1-3 = reflection recovery, >3 = stop)

## Esempio compilato

| Data/ora | Task | Classe | Stack | Esito | Retry | Tokens s/r | Durata | Commit/note |
|----------|------|--------|-------|-------|-------|------------|--------|-------------|
| 2026-05-21 09:12 | JSDoc su user.controller | cosmetic | 7B-whole | success | 0 | 1.4k/680 | 14s | `abc1234`, auto-translate commit msg in italiano |
| 2026-05-21 10:05 | Extract validateEmail in utils | behavior | 14B-diff | safe-fail | 3 | 3.2k/110 | 45s | Qwen filename missing anche dopo retry, re-prompt con "use exact filename path" → success 2° invocazione |
| 2026-05-21 10:30 | (re-prompt) | behavior | 14B-diff | success | 1 | 3.5k/320 | 28s | `def5678`, manual commit |
| 2026-05-21 14:20 | Refactor db pool multi-file | strategic | claude | success | — | — | — | cross-file, eseguito direttamente |
| 2026-05-22 08:45 | Rename `usr` → `user` | cosmetic | 7B-whole | hook-block | 0 | 900/50 | 8s | hook detected: file content = `"user.js"`, reset, re-prompt con file path esplicito → success |

## Aggregati mensili (sezione da compilare a fine mese)

### Statistiche raw
- Delegations totali: N
- Success: N (X%)
- Safe-fail: N (X%)
- Hook-block: N (X%)
- Corruption: N (dovrebbe essere 0; se >0 → BUG)
- Error: N (X%)

### Per classe
- Cosmetic: N totali, X% success, Y% hook-block
- Behavior: N totali, X% success, Y% safe-fail (retry count medio)
- Strategic: N ratio vs delegati

### Token savings stimati
- Tasks delegati: N
- Token/task stimato se eseguito direttamente: T1
- Token/task orchestrazione effettivo: T2
- Savings totali mese: (T1 - T2) × N ≈ Z token
- In percentuale su session totale: X%

### Trigger decisioni
- Se `corruption > 0`: apri issue, ADR-0008 revision, rivedi hook pattern
- Se `safe-fail` su behavior > 40%: valutare prompt-engineering più esplicito o downgrade a 7B + manual review
- Se cosmetic success > 90% e behavior safe-fail < 25%: scenario full-sovereign viable, skip Claude Pro
- Se mix complessivo con success < 50%: stack sovereign non maturo, Claude Pro mandatory

## Pattern da tenere d'occhio

- **Auto-translate commit** (Qwen ↔ italiano): cosmetic, ma se diventa consistent potrebbe indicare contamination di chat history
- **Reflection retry 14B Q2 su diff**: positivo pattern, se ricorrente alza la stima viability di 14B Q2 oltre ADR-0008
- **Llama runner termination**: se frequency aumenta, indagare RAM/VRAM pressure o aggiornare Ollama
- **CRLF warnings**: se diventano noise, valutare `.gitattributes`

## Riferimenti

- Delegation protocol: `docs/patterns/delegation-to-aider.md`
- ADR-0008 follow-up metrics: `docs/adr/0008-aider-whole-format-silent-corruption.md` sezione "Metriche da tracciare post-19/05"
