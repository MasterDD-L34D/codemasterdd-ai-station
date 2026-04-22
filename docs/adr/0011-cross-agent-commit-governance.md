# ADR-0011 — Cross-agent commit message governance

> *TL;DR: il primo dogfood Aider (2026-04-22) ha scoperto che `commit-guard.js` PreToolUse protegge solo commit fatti via Claude Code; Aider (e qualsiasi agent esterno) bypassa il gate. Inoltre i wrapper `aider-*.cmd` non impongono lingua/format del commit message. Scelto **1A + 2C**: aggiunto `commit-msg` git hook globale (defense-in-depth con PreToolUse esistente) + `--commit-prompt` nei wrapper. Smoke test PASS.*

- **Status**: Accepted
- **Data**: 2026-04-22
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)

## Context and Problem Statement

Il primo dogfood Aider in-session (task cosmetic JSDoc su `scripts/hooks/commit-guard.js`, delegato a Qwen 7B + whole) ha prodotto esito empirico success (22s, 1.8k/632 tokens, zero corruption) **ma** ha esposto 2 gap non previsti dalla "guard rail chain" documentata in `CLAUDE.md`:

### Gap 1 — commit-guard.js bypass
Il commit originale generato da Aider aveva subject:
> `feat: Aggiungo JSDoc comments al file \`scripts/hooks/commit-guard.js\` per documentare il hook e le sue funzionalità.`

che viola **4/4** regole del commit-guard:
- italiano (convention CLAUDE.md: commit in inglese)
- 117 chars (max 72)
- "Aggiungo" maiuscolo (must lowercase)
- trailing period (not allowed)

**Root cause**: `commit-guard.js` è registrato come `PreToolUse` hook di Claude Code sulla tool `Bash`. Attivato solo quando **Claude Code** chiama `git commit` via Bash. Aider chiama `git commit` come subprocess Python proprio → il layer 1 della guard rail chain non vede mai il tentativo.

Il gap non è specifico di Aider: qualsiasi agent CLI esterno (git manuale, script, futuri agent MCP, hook Husky che committa auto) ha la stessa caratteristica.

### Gap 2 — Wrapper `aider-*.cmd` senza commit-prompt
I wrapper `aider-cosmetic.cmd` e `aider-refactor.cmd` configurano `--model` e `--edit-format` ma non passano istruzioni sul formato del commit message generato da Aider. Qwen 7B default alla lingua del prompt utente (italiano nella nostra interazione → commit italiano) e produce message descrittivi lunghi.

## Decision Drivers

- **Cross-agent coverage**: la guard rail chain deve proteggere contro commit malformati indipendentemente dall'agent che li origina
- **Layering**: preferire gate al layer più appropriato (git-native hook > applicazione-specifica)
- **YAGNI minimalism** (ADR-0005): non introdurre machinery ridondante
- **Sovereign transition**: post-Max l'uso di Aider aumenterà → costo del gap cresce
- **Existing infra**: già c'è un git-level hook globale (`~/.local/share/git-hooks/pre-commit` per silent-corruption) che dimostra la fattibilità del pattern git-hook-globale

## Considered Options — Gap 1 (bypass)

### Opzione 1A — Duplicare logica commit-guard nel git hook globale
Aggiungere un file `commit-msg` in `~/.local/share/git-hooks/` con stessa logica Conventional Commits. Mantiene anche il `PreToolUse` Claude Code per feedback immediato.

**Pro**: massima copertura (tutti gli agent + git manuale). Mantiene feedback-loop veloce in Claude Code (fail-fast pre-exec).  
**Contro**: duplicazione regex/errori in 2 file (drift risk). Richiede sync manuale se cambiano regole.

### Opzione 1B — Convertire interamente a `commit-msg` git hook globale, rimuovere PreToolUse
Unico gate a livello git, applicato uniformemente.

**Pro**: fonte unica di verità, zero drift, copertura totale. Allineato al pattern già usato per silent-corruption.  
**Contro**: feedback più tardivo (commit-msg gira dopo che user ha dato il messaggio, non prima). Claude Code perde gate locale al Bash.

### Opzione 1C — Status quo + documentazione gap
Accettare la limitazione, documentare in CLAUDE.md "commit-guard applicato solo a Claude Code", richiedere user vigilance su commit Aider.

**Pro**: zero effort.  
**Contro**: policy failure inaccettabile per convention repo; la regola Conventional Commits perde enforcement.

## Considered Options — Gap 2 (wrapper commit-prompt)

### Opzione 2A — Aggiungere `--commit-prompt` ai wrapper
Modificare `aider-cosmetic.cmd` e `aider-refactor.cmd`:
```
aider --model ollama/qwen2.5-coder:7b --edit-format whole ^
  --commit-prompt "Commit message MUST be in English, Conventional Commits format (type: description), subject <=72 chars, lowercase description, no trailing period." ^
  %*
```

**Pro**: fix direct, compat Aider nativo (flag `--commit-prompt` supportato v0.86+).  
**Contro**: prompt instruction-following non è garantito — Qwen 7B può ignorare/interpretare male. Richiede verifica empirica.

### Opzione 2B — Lasciare al gate (Opzione 1A/1B) di bloccare commit malformati, Aider farà retry internally
Aider ha feature di retry su hook failure: se il `commit-msg` git hook respinge, Aider può rigenerare message. Non richiede modifica wrapper.

**Pro**: separation of concerns — wrapper resta minimale, enforcement unificato nel gate.  
**Contro**: cicli retry costano token; se Qwen ripete stesso pattern → loop infinito (safe-fail dopo N reflections, default 3).

### Opzione 2C — Opzioni 2A + 2B combinati
Commit-prompt **guida** la generazione + gate **enforce** a valle. Prompt riduce probabilità di fail, gate garantisce correctness.

**Pro**: defense-in-depth. Minor token waste su retry.  
**Contro**: più superficie da mantenere.

## Decision Outcome

**Scelto 1A + 2C** (2026-04-22, stessa sessione del discovery).

### Gap 1 — Opzione 1A (duplicate)
Creato `~/.local/share/git-hooks/commit-msg` (bash, 1668 bytes) con stessa logica di `scripts/hooks/commit-guard.js`:
- Conventional Commits regex: `^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?!?:\s.+`
- Subject <=72 chars
- No trailing period
- Lowercase description first char

Skip automatico per commit auto-generati (`Merge*`, `Revert*`, `fixup!*`, `squash!*`, commenti `#*`).

Il PreToolUse `scripts/hooks/commit-guard.js` **resta attivo** come fail-fast gate in sessione Claude Code. Il nuovo `commit-msg` copre Aider, manual git, script, futuri agent.

**Drift risk mitigation**: per ora regex duplicata testualmente in 2 file. Se il drift diventa problema concreto, refactor futuro estraendo in file JSON condiviso (non YAGNI oggi).

### Gap 2 — Opzione 2C (combined)
Aggiunto `--commit-prompt` a `C:\Users\edusc\.local\bin\aider-cosmetic.cmd` e `aider-refactor.cmd`:
> `"Commit message MUST be in English, Conventional Commits format (type: short description), subject line <=72 chars total, lowercase description, no trailing period. Example: 'docs: add JSDoc to hook validation blocks'."`

Esempio diverso per cosmetic vs refactor (seed corretto per il tipo di task).

### Smoke test gate (2026-04-22 12:10)
3 scenari testati in repo /tmp/hook-smoketest isolato:
| Scenario | Message | Expected | Exit |
|----------|---------|----------|------|
| Non-conforme | "Aggiungo cose al file che fanno delle cose molto molto belle." | block 3 errors | 1 ✅ |
| Conforme | "feat: add f.txt smoke test" | pass | 0 ✅ |
| Merge | "Merge branch 'foo' into main" | skip | 0 ✅ |

Errori rilevati TEST 1: regex non-match + trailing period + Description uppercase. **Length check non triggerato** (62<=72), corretto.

## Addendum — Gap 3 scoperto post-implementation (2026-04-22 17:04)

Il secondo dogfood Aider (batch PS1 comment-based help) ha esposto che l'implementation 1A+2C **non era sufficiente**:

- Qwen 7B ha **ignorato** `--commit-prompt` generando come subject un chunk di codice PowerShell (~172 chars)
- Il `commit-msg` git hook **non è stato chiamato**: commit 47c6403 passato con subject illeggibile

### Root cause (Aider 0.86.2)
Dal source `aider/repo.py:278`:
```python
if not self.git_commit_verify:
    cmd.append("--no-verify")
```
E `aider/args.py:494`:
```python
"--git-commit-verify", action=argparse.BooleanOptionalAction, default=False,
help="Enable/disable git pre-commit hooks with --no-verify (default: False)"
```

**Aider di default passa `--no-verify` a git commit → bypass TUTTI i git hooks** (commit-msg, pre-commit, post-commit). Non documentato esplicitamente nei wrapper.

### Fix applicato same-session
Aggiunto `--git-commit-verify` (forma positive, disabilita `--no-verify`) a entrambi i wrapper:
- `C:\Users\edusc\.local\bin\aider-cosmetic.cmd`
- `C:\Users\edusc\.local\bin\aider-refactor.cmd`

Ora Aider rispetta i git hooks → `commit-msg` globale applicato come da design opzione 1A.

### Validazione pendente
Questo Addendum è basato su **source code analysis** + **empirical observation Gap 3 manifestation** (dogfood #2). **Re-test empirico post-fix pendente**: prossimo dogfood deve mostrare `commit-msg hook block` quando Qwen genera subject non-conforme, con Aider retry automatico interno.

### Lesson architetturale
La "guard rail chain" deve essere **enforced by default**, non configurabile via flag agent-specifici. Aider è un design case notevole: il default `--no-verify` è documentato come feature (evitare conflitti pre-commit formatters noisy) ma confligge con il design hub-and-spoke di questa workstation dove i hook globali sono **fonte di verità** (vedi ADR-0008 silent-corruption enforcement).

**Estensione regola CLAUDE.md**: per qualsiasi futuro agent CLI integrato, verificare se applica `--no-verify` di default e correggere nel wrapper.

## Consequences

### Guard rail chain aggiornata
```
1. Claude Code PreToolUse  commit-guard.js        (solo Claude Code Bash → fail-fast)
2. git commit-msg globale  commit-msg              (tutti gli agent → cross-agent enforcement)  ← NEW
3. git pre-commit globale  pre-commit              (silent-corruption ADR-0008)
4. Husky repo-local        .husky/pre-commit       (solo Evo-Tactics, skip-worktree wrapper)
```

### Nessun amend manuale richiesto
Dopo fix 2C il wrapper Aider produce commit message conformi in inglese; 1A blocca residui se prompt ignorato da Qwen. Pattern operativo temporaneo deprecato.

### Token cost trascurabile
`--commit-prompt` ~40 token aggiuntivi per invocazione Aider. Retry cycles evitati se Qwen segue il prompt = savings netto.

## Follow-up

- [x] Creare `~/.local/share/git-hooks/commit-msg`
- [x] Update wrapper `aider-cosmetic.cmd` + `aider-refactor.cmd`
- [x] Smoke test 3 scenari PASS
- [x] Aggiornare CLAUDE.md sezione guard rail chain
- [x] Gap 3 scoperto + fix `--git-commit-verify` applicato ai wrapper (addendum 2026-04-22 17:04)
- [ ] Re-test dogfood post-Gap 3 fix: verificare che `commit-msg` hook ora blocca commit Qwen non-conformi
- [ ] Se Qwen ignora `--commit-prompt` ripetutamente (>30% retry): aumentare specificità prompt o valutare model switch
- [ ] Se emerge drift regex (divergenza commit-guard.js vs commit-msg): refactor con shared JSON source
- [ ] Considerare upgrade commit-prompt con esempi negativi ("NEVER include code blocks or diffs in commit message")

## Riferimenti

- Log dogfood: `logs/aider-delegation-2026-04.md` entry 2026-04-22 11:58
- Hook attuale: `scripts/hooks/commit-guard.js` (PreToolUse Claude Code)
- Git hook globale esistente: `~/.local/share/git-hooks/pre-commit` (silent-corruption)
- Aider `--commit-prompt` docs: https://aider.chat/docs/config/options.html#--commit-prompt-prompt
- Wrapper: `C:\Users\edusc\.local\bin\aider-cosmetic.cmd`, `aider-refactor.cmd`
- ADR-0008 (delega baseline): `docs/adr/0008-aider-whole-format-silent-corruption.md`
- ADR-0010 (format policy MADR): `docs/adr/0010-madr-format-adoption-and-skill-policy.md`
