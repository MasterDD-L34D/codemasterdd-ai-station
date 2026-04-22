# ADR-0011 — Cross-agent commit message governance

> *TL;DR: il primo dogfood Aider (2026-04-23) ha scoperto che `commit-guard.js` PreToolUse protegge solo commit fatti via Claude Code; Aider (e qualsiasi agent esterno) bypassa il gate. Inoltre i wrapper `aider-*.cmd` non impongono lingua/format del commit message. Questo ADR documenta i 2 gap e presenta opzioni; decision **deferred** in attesa di valutazione Eduardo.*

- **Status**: Proposed
- **Data**: 2026-04-23
- **Decisore**: Eduardo Scarpelli (pending)
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

**Deferred**. Raccomandazione per valutazione futura:

- **Gap 1**: tendere verso **Opzione 1A** (duplicate). Ragione principale: il feedback veloce di PreToolUse resta prezioso in sessione Claude Code; aggiungere `commit-msg` git hook copre il resto senza rimuovere valore esistente. Il drift risk è mitigabile con shared source (es. estrarre regex in file JSON condiviso sourced da entrambi hook).
- **Gap 2**: tendere verso **Opzione 2C** (combined). Il costo di 1 flag `--commit-prompt` nei wrapper è trascurabile; pair con gate è robusto.

Decision non presa oggi perché:
1. È un problema emerso durante dogfood, non era pianificato
2. La sessione 2026-04-23 è focalizzata su raccolta dati empirici Fase 6, non refactoring guard-rail
3. L'utente potrebbe preferire scelte diverse (es. 1B puro se valuta il drift risk maggiore del feedback-loss)

## Consequences

Fino a risoluzione:
- **Commit via Aider continuano a bypassare commit-guard**: richiede review manuale subject + amend post-commit se non conforme
- **Pattern operativo temporaneo**: dopo ogni delega Aider, `git log -1 --format="%s"` + eventuale `git commit --amend -m "..."` prima di push

Benchmark cost di questa ADR-0011 stessa: `git log -1 --format="%s" | awk '{print length}'` come verifica veloce, oppure attivare il futuro `commit-msg` hook per enforcement uniforme.

## Follow-up

- [ ] User review ADR-0011, scelta opzioni
- [ ] Se scelto 1A: creare `~/.local/share/git-hooks/commit-msg` con logica regex estratta da `scripts/hooks/commit-guard.js`
- [ ] Se scelto 2C: update `aider-cosmetic.cmd` + `aider-refactor.cmd` con flag `--commit-prompt`
- [ ] Aggiornare CLAUDE.md sezione "Guard rail chain" con nuovo layer git-level
- [ ] Aggiornare `logs/aider-delegation-2026-04.md` quando findings risolti

## Riferimenti

- Log dogfood: `logs/aider-delegation-2026-04.md` entry 2026-04-23 11:58
- Hook attuale: `scripts/hooks/commit-guard.js` (PreToolUse Claude Code)
- Git hook globale esistente: `~/.local/share/git-hooks/pre-commit` (silent-corruption)
- Aider `--commit-prompt` docs: https://aider.chat/docs/config/options.html#--commit-prompt-prompt
- Wrapper: `C:\Users\edusc\.local\bin\aider-cosmetic.cmd`, `aider-refactor.cmd`
- ADR-0008 (delega baseline): `docs/adr/0008-aider-whole-format-silent-corruption.md`
- ADR-0010 (format policy MADR): `docs/adr/0010-madr-format-adoption-and-skill-policy.md`
