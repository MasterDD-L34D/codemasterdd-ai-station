# Delegation protocol: Claude Code hub → Aider locale

**Stato**: attivo dal 2026-04-21 (follow-up ADR-0008, revisione hub-first)
**Obiettivo**: ridurre consumo token Claude Code delegando codegen a Qwen locale, **mantenendo l'utente in una singola interfaccia (Claude Code)**
**Prerequisiti**:
- Aider 0.86.2 installato
- Guard rail hook pre-commit globale attivo (ADR-0008 safety protocol)
- `OLLAMA_API_BASE` disponibile nel processo aider. Due setup paralleli richiesti:
  - **User PATH Windows** (per cmd.exe/PowerShell): `setx OLLAMA_API_BASE "http://127.0.0.1:11434"` — attivo per nuovi processi shell
  - **`~/.env`** (per bash Claude Code / Git Bash): aider auto-legge `.env` in home + cwd + git root. Contenuto minimo:
    ```
    OLLAMA_API_BASE=http://127.0.0.1:11434
    ```
  - Rationale dual-setup: `setx` non propaga a shell già attive (bash in Claude Code è spawned all'avvio sessione, non rilegge PATH dopo `setx`). `.env` bypass: aider lo legge ad ogni invocazione

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

### Anti-pattern: value-change singola riga su diff format
Finding 2026-04-21 R1 (n=4 behavior-critical): task "cambia default param X da A a B" (singola riga) ha fail rate più alto di refactor strutturali (extract method, rename). Qwen 14B Q2 include troppo context preamble nel SEARCH block → exact-match fallisce → 3 reflection retry exhausted → safe fail.

**Contromisura**: per value-change singola riga preferire:
- **Aider 7B + whole** se il cambio è localizzato e il resto del file non va modificato (Qwen riproduce l'intero file con 1 diff) — rischio drift minimo su cambio semplice
- **Edit diretto da Claude Code** (mio Edit tool) per minimizzare chiamate LLM su task trivial
- Aider 14B Q2 + diff solo su modifiche multiline o strutturali

## Task strategic (non-delegabili) — protocol

Task che classifico "strategic" NON vanno ad Aider. Io (Claude Code) eseguo direttamente via Edit/Write/Read/Grep + mio ragionamento.

**Criteri strategic**:
- Multi-file (>3 file) con dipendenze incrociate
- Debug architetturale (root cause investigation)
- Design decisions (quale pattern usare, quale architettura)
- Refactor che richiede comprensione di business logic emergente
- Qualsiasi task dove l'utente ha chiesto esplicitamente "ragiona con me"

**Cosa cambia vs delegazione**:
- Token consumption: identico a pre-hub (io scrivo il codice)
- No `aider` invocation
- No tracking log (è il mio baseline di uso)
- Review: utente vede il diff nel Claude Code diff UI / Bash tool

**Non compensation attesa**: i task strategic restano "expensive" per design. Il hub riduce token solo sui delegabili; il mix totale dipende dal rapporto cosmetic+refactor vs strategic nel workflow reale.

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

### Helper `aider-log` (auto-compilazione entry)

Script bash in `C:\Users\edusc\.local\bin\aider-log` (PATH, chmod +x) che parsa output Aider e appende riga auto:

```bash
# pattern canonico: pipe Aider output a aider-log con metadata
aider --model <M> --edit-format <F> --yes-always --message "..." <files> 2>&1 | tee /tmp/aider-last.log
aider-log --task "JSDoc on helpers.js" --class cosmetic --stack 7B-whole < /tmp/aider-last.log
```

Parsing automatico:
- Tokens sent/received da "Tokens: X sent, Y received"
- Commit hash da "Commit HASH" (l'ultimo)
- Outcome heuristic: `hook-block` > `safe-fail` > `success` > `error` > `unknown`
- Retry count: occorrenze "Retrying in"

Compilare manualmente solo: `--task`, `--class`, `--stack`. Durata lasciata vuota (può essere aggiunta editando il file post-hoc se serve).

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

### Scenario 4 — Multi-file cosmetic (2-3 file)
User: "aggiungi JSDoc a tutte le funzioni in `demo.js` e `helpers.js`"
→ Classifico: cosmetic multi-file, pattern supportato
→ Invoco `aider --message "..." demo.js helpers.js` (lista file come args)
→ Aider edita entrambi in una singola session + 1 commit unificato
→ Verifico `git show HEAD --stat`: più file in single commit
→ Finding 2026-04-21: testato 2 file JS+JS e JS+Python, 1.1k/916 tokens totali, 25s

### Scenario 5 — Multi-file refactor cross-dipendenze (4+ file)
User: "rinomina `usr` in `user` in tutti i file che lo usano"
→ Classifico: strategico per scope + dipendenze cross-file, eseguo io con Grep + Edit

## Recovery flow — quando Aider fallisce

Quando Aider respinge l'edit o produce output non utile, seguo questo algoritmo:

1. **Read the fail signal**:
   - Safe-fail: "Only 3 reflections allowed, stopping" → Qwen non riesce a produrre format corretto
   - Llama runner terminated: Ollama crash, retry automatico; se >3 volte, restart Ollama
   - Hook blocked: silent corruption intercettata, working tree pulito

2. **Classificazione azione**:
   - **Safe-fail primo tentativo** → re-prompt con istruzioni più esplicite (es. "the SEARCH block must contain ONLY the function body of X, not surrounding code")
   - **Safe-fail secondo tentativo** → escalation: switch a whole format (7B) se il task lo permette, altrimenti eseguo io
   - **Hook blocked** → Qwen output malformato: re-prompt con constraint filename formatting, o escalation
   - **Llama crash ricorrente** → restart Ollama tray (`ollama app.exe`) prima di retry; se persiste, verificare VRAM pressure

3. **Budget retry**: max 2 re-prompt prima di escalare. Non ostinarsi su un task che Qwen non gestisce.

4. **Escalation path**:
   - Prima: io via Edit/Write (token cost higher ma capability garantita)
   - Poi: Claude Pro/OpenRouter (solo per task critici, dopo due fail locali)

## Rollback pattern

Se un edit va male post-commit (auto-commit o manuale) e voglio annullarlo:

| Situazione | Comando | Quando usare |
|-----------|---------|--------------|
| Ultimo commit, non pushato, in locale | `git reset --hard HEAD~1` | Working tree pulito, drop totale |
| Ultimo commit, non pushato, voglio tenere modifiche come uncommitted | `git reset HEAD~1` | Per review manuale prima di re-committare |
| Commit già pushato | `git revert HEAD` | Crea nuovo commit che annulla (safe per main) |
| Working tree uncommitted (--no-auto-commits mode) | `git checkout -- <file>` | Annulla modifiche Aider non ancora staged |

**Pre-operazione distruttiva**: sempre `git status` + `git log --oneline -3` per confermare su quale commit si sta operando.

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
- **CRLF warning** (risolto): `.gitattributes` con `* text=auto eol=lf` in ogni repo elimina il warning. Applicato a `aider-tty-test` e `codemasterdd-ai-station` il 2026-04-21. Per file pre-esistenti un tempo `git add --renormalize .` una volta normalizza tutto lo storico.
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
