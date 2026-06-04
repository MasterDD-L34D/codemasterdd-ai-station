# Aider delegation log — template

**Scopo**: tracciare ogni delegazione Claude Code → Aider locale per costruire il dataset decisionale Fase 6 (post-19/05 evaluation, ADR-0008 follow-up).

**Come usare**:
1. **Automatico** (raccomandato): usare lo script helper `aider-log` (in `C:\Users\edusc\.local\bin\`):
   ```bash
   aider --model <M> --edit-format <F> --yes-always --message "..." <files> 2>&1 | tee /tmp/aider-last.log
   aider-log --task "short desc" --class cosmetic --stack 7B-whole < /tmp/aider-last.log
   ```
   Crea automaticamente `logs/aider-delegation-YYYY-MM.md` al primo uso del mese. Parsa tokens/commit/outcome/retry dall'output Aider.
2. **Manuale**: copiare questo file in `logs/aider-delegation-YYYY-MM.md` a inizio mese e compilare righe a mano (più lento ma serve se non hai pipe disponibile o vuoi annotazioni libere).
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

### Quality bench ↔ reliability correlation (M4)

Il quality-bench misura **capability su toy problems** (pass@1 deterministic). Il dogfood log misura **reliability su task reali** (constraint-compliance multi-shot). I due dataset sono ortogonali e **devono essere letti insieme** fine-mese per diagnosticare fail modes.

**Reference table** (da aggiornare a ogni nuovo bench run): mappare ciascuno stack a `pass@1_rate` + `bench_source` per context. Formato consigliato:

```markdown
| Stack | pass@1 (quality bench) | Source | Reliability rate (dogfood) |
|-------|------------------------|--------|----------------------------|
| 7B-whole | 100% | quality-bench-2026-04-23.md | (compilato fine mese) |
| 14B-diff | 100% | quality-bench-2026-04-23.md | (compilato fine mese) |
| qwen3-30b-diff | 100% | quality-bench-2026-04-23.md | (compilato fine mese) |
| groq-70b | 100% | quality-bench-2026-04-23.md | (compilato fine mese) |
| cerebras-8b | 100% | quality-bench-2026-04-23.md | (compilato fine mese) |
```

**Diagnostic patterns**:
- `pass@1 = 100% AND reliability < 80%` → fail mode è **constraint-specific**, non capability-gap. Driver per routing matrix adjustment (es. ADR-0016 constraint-count).
- `pass@1 < 50% AND reliability < 50%` → capability-gap reale, considerare upgrade modello (ADR-0009 T1 trigger).
- `pass@1 = 100% AND reliability = 100%` → stack robusto per la classe task osservata; mantenere.
- `pass@1 variance alta across benches` → discriminant power insufficiente, serve hard problem set (L1 backlog).

**Quando aggiornare la reference table**: a ogni nuovo bench eseguito (run-bench.ps1) o quando un nuovo stack è aggiunto al routing (nuovo wrapper).

## Pattern da tenere d'occhio

- **Auto-translate commit** (Qwen ↔ italiano): cosmetic, ma se diventa consistent potrebbe indicare contamination di chat history
- **Reflection retry 14B Q2 su diff**: positivo pattern, se ricorrente alza la stima viability di 14B Q2 oltre ADR-0008
- **Llama runner termination**: se frequency aumenta, indagare RAM/VRAM pressure o aggiornare Ollama
- **CRLF warnings**: se diventano noise, valutare `.gitattributes`

## Riferimenti

- Delegation protocol: `docs/reference/patterns/delegation-to-aider.md`
- ADR-0008 follow-up metrics: `docs/adr/0008-aider-whole-format-silent-corruption.md` sezione "Metriche da tracciare post-19/05"
