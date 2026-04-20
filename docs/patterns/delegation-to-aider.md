# Delegation protocol: Claude Code → Aider locale

**Stato**: attivo dal 2026-04-21 (follow-up ADR-0008)
**Obiettivo**: ridurre consumo token Claude Code delegando task appropriati al dual-stack Aider locale
**Prerequisiti**: Aider 0.86.2 installato, wrapper `aider-cosmetic` + `aider-refactor` in PATH, guard rail hook pre-commit globale attivo (ADR-0008 safety protocol)

## Quando delegare vs eseguire

### Classificazione task (decision tree)

1. **Task tocca codice da modificare?**
   - No (query, explain, discuss, plan) → **io eseguo** (Claude Code)
   - Sì → step 2

2. **Task richiede ragionamento cross-file o multi-step strategico?**
   - Sì (refactor multi-file, debug architetturale, design decisions) → **io eseguo** (capability non-sostituibile dal locale)
   - No → step 3

3. **Task è cosmetic o behavior-critical?**
   - **Cosmetic** (JSDoc, docstrings, rename variabile, lint-fix, type annotations che non cambiano runtime) → **delego a `aider-cosmetic`** (Qwen 7B + whole)
   - **Behavior-critical** (refactor funzione, bug fix, logic change minimale, API signature change) → **delego a `aider-refactor`** (Qwen 14B Q2 + diff, `--no-auto-commits`)

### Borderline: quando non sono sicuro
- Task che sembra cosmetic ma include logica di validazione → behavior-critical (precauzionale)
- Task con più di 3 file → probabilmente strategico, io eseguo
- Task con constraint "do not change logic" esplicito → resta cosmetic se i nomi/commenti sono l'unico target; diventa behavior-critical se tocca anche parametri/return

## Come formato l'handoff

Quando delego, al posto di eseguire l'edit, **produco un blocco ready-to-paste** in questo formato:

```
[DELEGATE cosmetic | file: path/to/file.ext]

Apri cmd.exe, cd nel repo, poi:

    aider-cosmetic path/to/file.ext

Al prompt Aider digita:

    <prompt target in linguaggio naturale>

Poi `/exit`. Riporta:
- Diff finale (git diff HEAD~1 se auto-commit, o git diff se --no-auto-commits)
- Eventuali retry llama runner / errori format
- Tempo percepito
```

Per `aider-refactor` stessa struttura, ma con safety warning:

```
[DELEGATE behavior-critical | file: path/to/file.ext]

⚠️ --no-auto-commits attivo: dopo l'edit fai tu `git diff` + `git commit` manuale.

Apri cmd.exe, cd nel repo, poi:

    aider-refactor path/to/file.ext

Al prompt Aider digita:

    <prompt target in linguaggio naturale>

Dopo l'edit:
- `/diff` (dentro Aider) per rivedere
- Se ok: `/exit`, poi `git diff` + `git commit -m "..."`
- Se ko: `/undo` dentro Aider, riprova con prompt più specifico
```

## Workflow utente atteso

1. Legge handoff in chat
2. Esegue in cmd.exe (finestra separata, sessione persistente consigliata)
3. Quando Aider ha finito o fallito, torna in Claude Code e incolla:
   - Output Aider (anche parziale)
   - `git diff` se applicabile
   - Qualsiasi anomalia notata

4. Io riprendo analizzando l'output. Se:
   - Success pulito → loggo esito per tracking fail rate (item 5 roadmap) e procedo
   - Fail safe (no edit / respinto) → riprompto con instruction più chiara, rilancio l'handoff
   - Silent corruption sospetta (hook dovrebbe averlo bloccato; se no, bug da documentare) → immediate reset, analisi, eventuale ADR

## Review loop — cosa controllo quando torna output

| Segnale | Significato | Action |
|---------|-------------|--------|
| Hook pre-commit ha bloccato commit | Silent corruption intercettata → **sistema funzionante**, l'edit era garbage | Reset, retry con prompt diverso o delega a Claude Code |
| `git diff` mostra edit corretto | Success | Loggo, proseguiamo |
| Aider ha detto "Ok." o simili 2-token | Qwen non ha prodotto edit (format fail o capability fail) | Riprompto più specifico, o escalation |
| Llama runner terminated retry >3 | Backend instabile, probabile memory pressure | Suggerisco restart Ollama tray, retry |
| Output Aider mostra JSDoc ma file su disco è corrotto | Bug silent-corruption che il hook non ha intercettato | **Critico**: aggiornare hook pattern, ADR-0008 revision |

## Scenari

### Scenario 1 — Cosmetic semplice
User: "aggiungi JSDoc a tutte le funzioni di `utils/helpers.js`"
→ Io classifico: cosmetic, single file, low risk
→ Handoff `aider-cosmetic utils/helpers.js` con prompt ready
→ User esegue in cmd.exe, paste output
→ Io verifico diff, OK, loggo

### Scenario 2 — Refactor minimale
User: "estrai la logica di validazione email dal controller in `utils/validate-email.js`"
→ Io classifico: behavior-critical (estrazione modifica struttura chiamate)
→ Opzione A: delego `aider-refactor` con diff format (safe fail)
→ Opzione B: eseguo io se cross-file (più di 1 file modificato) o se la signature è delicata
→ Preferenza A se task isolabile, B se complesso

### Scenario 3 — Query strategica
User: "come organizzo i middleware Express in questa app?"
→ Io eseguo. Nessuna delega.

### Scenario 4 — Borderline
User: "rinomina la variabile `usr` in `user` in tutto il file"
→ Cosmetic (rename è cosmetic per definizione), single file
→ `aider-cosmetic` OK. Ma se il file è usato da altri file con `usr` destructured/importato, diventa cross-file → io eseguo o split in due delegazioni

## Tracking fail rate (Fase 6 evaluation)

Per ogni delegazione tenere traccia in `logs/aider-delegation-YYYY-MM.md` (gitignored) con:

| Data | Task | Stack | Esito | Note |
|------|------|-------|-------|------|
| 2026-05-21 | JSDoc su user.controller | cosmetic | success | 12s, 8 JSDoc applicati |
| 2026-05-22 | extract validate-email | refactor | safe fail (no edit) | retry con prompt più esplicito → success |

Dati aggregati mensilmente informeranno decisione budget post-19/08 (3 mesi uso reale).

## Limitazioni note

- Delegazione ha **cognitive overhead**: user deve aprire cmd.exe, fare copy-paste, tornare in Claude Code. Su task banali può essere più lento che far eseguire a me. Il vantaggio è token-savings, non velocità wall-clock.
- Silent corruption hook protegge il 99% casi ma non garantisce zero danno. Sempre `git diff HEAD~1` post-commit come seconda linea di difesa.
- Qwen 14B Q2 + diff ha fail rate alto (stimato 20-40%). Accettare che ~1 su 3 refactor richiede retry manuale.
- Wrapper `aider-cosmetic` e `aider-refactor` funzionano **solo da cmd.exe** (bash ha TTY broken, vedi JOURNAL 2026-04-20). PowerShell probabilmente OK ma non testato sistematicamente.

## Riferimenti

- ADR-0007 — benchmark e paradox quantization: `docs/adr/0007-aider-qwen-quantization-findings.md`
- ADR-0008 — silent corruption + dual-stack decision: `docs/adr/0008-aider-whole-format-silent-corruption.md`
- Wrapper scripts: `C:\Users\edusc\.local\bin\aider-cosmetic.cmd`, `C:\Users\edusc\.local\bin\aider-refactor.cmd`
- Hook guard rail: `C:\Users\edusc\.local\share\git-hooks\pre-commit` (attivato via `git config --global core.hooksPath`)
