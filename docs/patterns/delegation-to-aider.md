# Delegation protocol: Claude Code hub → Aider locale

**Stato**: attivo dal 2026-04-21 (follow-up ADR-0008, revisione hub-first)
**Obiettivo**: ridurre consumo token Claude Code delegando codegen a Qwen locale, **mantenendo l'utente in una singola interfaccia (Claude Code)**
**Prerequisiti**: Aider 0.86.2 installato, `OLLAMA_API_BASE=http://localhost:11434` persistito, guard rail hook pre-commit globale attivo (ADR-0008 safety protocol)

## Architettura hub

```
User → Claude Code (chat qui)
         ↓
       Bash/PowerShell invocation
         ↓
       aider --message → Qwen (locale, sovereign)
         ↓
       git commit (o review manuale se --no-auto-commits)
         ↓
       Guard rail hook (pre-commit ADR-0008)
         ↓
       Claude Code legge git diff → riporta
         ↑
User
```

**Principio**: user dialoga solo con Claude Code. Claude Code invoca Aider via tool bash/PowerShell, non interattivo (`--message`). Output parsed dal tool result, user vede solo il summary.

## Quando delegare vs eseguire direttamente (Claude Code)

Decision tree applicato dall'orchestratore (me) prima di ogni task codegen:

1. **Task tocca codice da modificare?**
   - No (query, explain, discuss, plan) → eseguo direttamente
   - Sì → step 2

2. **Task richiede ragionamento cross-file o multi-step strategico?**
   - Sì (refactor multi-file, debug architetturale, design decisions) → eseguo direttamente (capability non-sostituibile)
   - No → step 3

3. **Task è cosmetic o behavior-critical?**
   - **Cosmetic** (JSDoc, docstrings, rename variabile, lint-fix, type annotations che non cambiano runtime) → delego a stack **7B + whole**
   - **Behavior-critical** (refactor funzione, bug fix, logic change minimale, API signature change) → delego a stack **14B Q2 + diff + no-auto-commits**

### Borderline
- Task che sembra cosmetic ma include logica di validazione → behavior-critical (precauzionale)
- Task con più di 3 file → strategico, eseguo direttamente
- Task con constraint "do not change logic" esplicito → resta cosmetic se tocca solo nomi/commenti

## Invocation pattern canonico (hub, bash da Claude Code)

### Cosmetic
```bash
aider --model ollama/qwen2.5-coder:7b \
      --edit-format whole \
      --yes-always --no-pretty --no-stream --no-show-release-notes \
      --message "<prompt task>" \
      <file1> [file2 ...]
```

### Behavior-critical
```bash
aider --model ollama/qwen2.5-coder:14b-instruct-q2_K \
      --edit-format diff \
      --no-auto-commits \
      --yes-always --no-pretty --no-stream --no-show-release-notes \
      --message "<prompt task>" \
      <file1> [file2 ...]
```

**Flag rationale**:
- `--yes-always`: skip conferme interattive (necessario per bash non-TTY)
- `--no-pretty`: output plain ASCII, no ANSI escape (parsable)
- `--no-stream`: output atomico (semplifica parsing tool result)
- `--no-show-release-notes`: riduce rumore output
- `--no-auto-commits` (solo refactor): forza review manuale post-edit, previene sigillamento corruption

**Output post-invocazione da leggere**:
- Behavior-critical: `git status -s` + `git diff` → se OK, committo io manualmente; se KO, `git reset` e re-prompting
- Cosmetic: `git show HEAD --stat` + prime righe file con `head` → verifica quick corruption check; Aider ha auto-committato, hook ha già filtrato silent corruption

## Fallback: user direct invocation (opzionale, non default)

Se in qualche situazione vuoi bypassare il hub (es. sessione senza Claude Code attiva):

```cmd
REM Da cmd.exe
aider-cosmetic <file>    :: wrapper per 7B + whole
aider-refactor <file>    :: wrapper per 14B Q2 + diff + no-auto-commits
```

Entrambi in `C:\Users\edusc\.local\bin\` (PATH Windows).

## Review loop (automatico, applicato dal hub)

Dopo ogni invocazione Aider, check automatici nell'ordine:

| Check | Tool | Esito positivo | Esito negativo → azione |
|-------|------|----------------|--------------------------|
| Exit code Aider | bash `$?` | 0 | ≠0: leggi output, riporta errore |
| File corruption | `head -n 5 <file>` | contiene codice | contiene solo filename → ⚠️ hook avrebbe dovuto bloccare, documenta bug |
| Commit hash | `git log -1 --oneline` | nuovo hash (se auto-commit) | stesso hash: Aider ha fallito silently |
| Diff sanity | `git diff HEAD~1 --stat` | insertions/deletions sensate vs task | deletions anomale: rollback proposto |
| Hook output | stderr bash | silent | "Aider silent-corruption detected" → blocked, retry con prompt diverso |

## Tracking fail rate (Fase 6 evaluation)

Template log in `docs/patterns/aider-delegation-log-template.md`, istanze mensili in `logs/aider-delegation-YYYY-MM.md` (gitignored).

Compilare **ad ogni delegazione** (righa per task):
- Data/ora
- Classificazione (cosmetic / behavior-critical / strategic)
- Stack usato
- Esito (success / safe fail / corruption / hook-blocked)
- Retry count (Aider reflection)
- Tokens sent/received (Aider riporta in output)
- Durata wall-clock
- Note

Dati aggregati mensilmente → decisione budget post-19/08.

## Scenari risolti

### Scenario 1 — Cosmetic semplice (hub)
User: "aggiungi JSDoc a tutte le funzioni di `utils/helpers.js`"
→ Classifico: cosmetic, single file
→ Invoco 7B + whole via bash `--message`
→ Parso output: Aider commit hash + diff stat
→ Verifico `head -5` + `git show --stat`
→ Riporto: "Done, commit abc1234, +45/-0 insertions"

### Scenario 2 — Refactor minimale (hub)
User: "cambia `divide()` per ritornare null invece di throw su b=0"
→ Classifico: behavior-critical
→ Invoco 14B Q2 + diff + no-auto-commits
→ Se Aider self-correct via reflection → edit applicato, working tree dirty
→ Verifico `git diff` → se OK, `git commit` manuale con message
→ Se diff sbagliato, `git reset`, propongo re-delega con prompt più specifico

### Scenario 3 — Query strategica
User: "come organizzo i middleware Express in questa app?"
→ Eseguo io, nessuna delega.

### Scenario 4 — Multi-file refactor
User: "rinomina `usr` in `user` in tutti i 4 file del modulo"
→ Classifico: strategico per scope (4 file), eseguo io con Edit+Grep

## Ottimizzazioni token (findings 2026-04-21)

**Onestà empirica**: su task piccoli (file <50 righe, cambi <5 linee) il break-even è marginale — l'overhead di leggere output Aider può eguagliare il savings del non generare codice. Il hub vince nettamente su:
- File grandi (200+ righe): codegen lineare vs orchestrazione costante
- Task ripetitivi simili: pattern invocation riusato
- Refactor complessi: ragionamento codegen alto su Qwen, non su Claude Code

**Minimizzazioni applicabili**:
- `--no-pretty --no-stream`: riduce size output Aider
- `tail -N` o `head -N` su output Aider per prendere solo righe informative
- Non re-leggere file post-edit: `git diff HEAD~1 --stat` sufficiente per verifica
- Per task cosmetic riusciti, skip reading diff pieno (hook + stat bastano)

## Limitazioni note

- **Reflection retry**: Aider diff format ha self-correction su format errors — 14B Q2 può recuperare al 2° tentativo (finding 2026-04-21 dogfood: refactor fffcbda recuperato). Non garantito sempre, ma pattern frequente.
- **CRLF warning**: Git Windows mostra warning "CRLF will be replaced by LF" su file editati da Aider (Aider scrive LF). Cosmetic, non impatto funzionale. Eventualmente `.gitattributes` per normalizzare.
- **Auto-translate commit message**: Qwen a volte auto-traduce il commit message in italiano anche con prompt inglese. Cosmetic issue, lascio.
- **Llama runner termination**: ricorrente durante fase commit-message generation di Aider (auto-commit). Aider retry esponenziale recupera di solito in 1-3 secondi.
- **Guard rail hook** protegge il 99% casi ma non garantisce zero danno. `git diff HEAD~1` post-commit sempre consigliato come seconda linea di difesa.
- **Output Aider verboso** su --message può costare più token in input a Claude Code che risparmiato in codegen, su task piccoli. Usare `tail`/`head` per estrarre solo info rilevanti.

## Riferimenti

- ADR-0007 — benchmark e paradox quantization: `docs/adr/0007-aider-qwen-quantization-findings.md`
- ADR-0008 — silent corruption + dual-stack decision: `docs/adr/0008-aider-whole-format-silent-corruption.md`
- Wrapper fallback (cmd.exe): `C:\Users\edusc\.local\bin\aider-cosmetic.cmd`, `C:\Users\edusc\.local\bin\aider-refactor.cmd`
- Hook guard rail: `C:\Users\edusc\.local\share\git-hooks\pre-commit` (attivato via `git config --global core.hooksPath`)
- Log template: `docs/patterns/aider-delegation-log-template.md`
