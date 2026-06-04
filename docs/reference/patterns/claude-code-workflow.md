# Pattern: Claude Code workflow consolidato

**Data formalizzazione**: 2026-04-20
**Basato su**: 2 sessioni operative intense (19/04 notturna + 20/04 serale)
**Scopo**: documentare pattern di interazione con Claude Code che funzionano per me

## Executive summary

Dopo il trauma Victus e 2 sessioni intense con Claude Code, ho consolidato
un **workflow specifico** che bilancia velocità e sicurezza.

**Pattern core**:
1. Un comando alla volta
2. Approvazione esplicita "1 Yes" manuale
3. MAI "2 Yes always" automatico
4. Diff review prima di modifiche file
5. Verifica output dopo ogni step
6. Commit atomici semanticamente coerenti
7. Journaling in tempo reale

## I 7 principi del mio workflow con Claude Code

### 1. Un comando alla volta

**Anti-pattern**: Claude propone 5 comandi "eseguiamo tutti in sequenza?"
**Mio pattern**: "esegui solo il primo, fammi vedere output, poi continua"

**Motivazione**:
- Ogni comando può avere output inaspettato
- Un errore al 3° comando può corrompere gli effetti dei primi 2
- Investigare errore post-batch è più complesso

**Eccezioni accettabili**:
- Serie di `git status` / `ls` (pure read, no side effect)
- File reads multipli in sequenza (pre-analysis)

**Esempio real**:
Quando Claude voleva fare BitLocker off + registry edit + service disable
tutto insieme, ho detto "no, prima solo `manage-bde -off C:`, aspettiamo
decrittazione, poi registry, poi service". Rallentato di 25 min ma
zero rischio.

### 2. Approvazione esplicita "1 Yes" manuale

**Default Claude Code**: ogni azione di scrittura/modifica richiede approvazione utente.

**3 opzioni tipiche**:
1. **Yes** (singola operazione)
2. **Yes, and don't ask again for {similar actions}** (permesso durativo)
3. **No, and tell Claude what to do differently** (rifiuto + redirect)

**Mia scelta consistente**: **1** (Yes singola).

**Motivazione**:
- "Yes always" rimuove l'ultima linea di difesa
- Pochi secondi di attrito per ogni step sono l'investimento giusto
- Ogni volta che approvo, rileggo cosa sto approvando

**Effetto collaterale positivo**: mi sono allenato a leggere veloce e
accuratamente cosa Claude sta per fare. Skill di "code review real-time".

### 3. MAI "2 Yes always" automatico

**Casi tipici dove Claude lo propone**:
- "Execute bash commands" (che già approvo singolarmente)
- "Read files without asking" (che già sono read-only)
- "Modify files matching pattern X"

**Perché rifiuto sempre**:
- "always" copre anche edge case che non ho previsto
- Context può cambiare, scope può slittare
- Preferisco attrito micro ogni volta a potenziale catastrofe

**Scenario ipotetico dannoso**:
- Ho approvato "modify .md files always"
- Claude decide di riscrivere JOURNAL.md intero
- Perdo storia settimane di decisioni

Questa sequenza è irreversibile se approvo "always" senza attenzione.

### 4. Diff review prima di modifiche file

**Claude Code mostra diff colorato** prima di applicare edit:
- Verde: righe da aggiungere
- Rosso: righe da rimuovere
- Contesto circostante

**Mio processo**:
1. Leggo diff completo (non sommario AI)
2. Verifico che cambi solo quello che mi aspetto
3. Controllo che non alteri sezioni non menzionate
4. Approva o reject

**Tempo medio**: 15-30 secondi per diff semplice, 1-2 min per complesso.

**Benefit**: zero surprise edits. Zero rework per "Claude ha cambiato troppo".

### 5. Verifica output dopo ogni step

**Pattern**:
```
Comando X → Output Y → Leggi attentamente Y → Decidi next step
```

**Anti-pattern**:
```
Comando X → "ok procedi" → Comando Y → "ok procedi" → ...
```

**Cosa cerco nell'output**:
- Error messages (anche "warning" deserve attention)
- Version numbers (allineati con expected?)
- Paths (stanno dove mi aspetto?)
- Performance indicators (tempo, size)
- Unexpected behaviors (Claude stesso che nota cose strane)

**Real example**:
Quando ho lanciato `winget install OpenJS.NodeJS.LTS`, output ha mostrato
**Node 24.15.0** invece di Node 22. Se avessi detto "ok procedi" veloce,
avrei perso questa informazione cruciale per ADR-0003.

### 6. Commit atomici semanticamente coerenti

**Pattern**: un commit = un cambio logico.

**Buoni esempi** (commit fatti):
- `9de5254 chore: initial project structure`
- `eb425d1 docs: rename workstation label to CodeMasterDD`
- `e8c372c chore: gitignore Claude Code local settings`
- `0059d45 feat: install complete dev stack (node, python, vscode, ollama)`

Ogni commit ha **uno scope chiaro**. Non "misto" (5 tipi di cambi insieme).

**Message convention**:
- Type prefix: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `style:`, `test:`
- Scope opzionale: `feat(auth): ...`
- Imperative mood: "add X" non "added X"
- Lower case (tranne nomi propri)
- <72 caratteri subject, dettagli in body

**Claude Code attribution** (policy canonica ADR-0011 Addendum 2026-05-17, opzione C):
per i commit che Claude genera, trailer metadata (MAI `Co-Authored-By:` — vietato):
```
Coding-Agent: claude-opus-4.7
Trace-Id: <uuidv7>
```

**Motivazione**: attribution onesto trace-able, co-author-noise GitHub rimosso.
Enforcement 2-layer (commit-guard.js sempre-attivo + global commit-msg). Vedi
`docs/adr/0011-cross-agent-commit-governance.md` §Addendum 2026-05-17.
in git log.

### 7. Journaling in tempo reale

**Pattern**: JOURNAL.md aggiornato mentre faccio, non dopo.

**Formato**:
```markdown
## Sessione 2026-MM-DD (ora)

### Contesto
[stato mentale, energia, obiettivo]

### Cosa ho fatto
[sequenza operazioni con motivazione]

### Problemi incontrati
[errori, sorprese]

### Decisioni prese
[con rationale]

### Stato finale
[riepilogo]
```

**Durante sessione**: aggiungo sezioni a JOURNAL.md in tempo reale.
**Mai "lo aggiorno dopo"** (perché dopo = mai, o sintesi povera).

## Micro-pattern di interazione

### Come chiedo a Claude di fare

**Anti-pattern**: "fai X"
**Mio pattern**: "voglio Y risultato, propongo X approach, verifica e dimmi se hai
alternative migliori, poi esegui 1 step alla volta con approvazione"

**Esempio reale**:
> "Voglio push del repo su GitHub come privato.
> Approach: gh repo create con flag appropriate.
> Verifica: proprio gh è installato, chiedi a me di aprire PS fresca se serve,
> o usa path assoluto come workaround.
> Dopo creazione: verifica visibile come private, description italiana."

### Come Claude risponde (pattern consolidato)

Claude ha interiorizzato il pattern:
1. Propone approach
2. Identifica potenziali issue (PATH stantio, ecc.)
3. Esegue 1 comando
4. Commenta output
5. Chiede "procedo con X next?"

### Come rifiuto una proposta

**Esempio concreto**: quando Claude ha proposto Z.ai come subscription alternative:

**Mia risposta**:
> "No. Non l'ho mai chiesto. Viola filosofia sovereign. Rimuovi dal piano.
> Spiega perché l'hai proposto per la prossima volta evitare pattern simile."

**Benefit**: corregge bias di Claude real-time. Previene drift.

### Come correggo errori di interpretazione

**Esempio**: Claude pensava Mac mini fosse dependency del piano.

**Mia risposta**:
> "Chiarimento: Mac mini è ESTENSIONE OPZIONALE FUTURA, NON dependency.
> Lenovo deve funzionare AUTOSUFFICIENTE da oggi.
> Mac mini arriverà SE e QUANDO budget permette, non è certo.
> Aggiorna CLAUDE.md con questa distinzione."

**Benefit**: propaga correzione in documentazione, non solo in chat.

## Anti-pattern che ho evitato

### 1. "Trust the AI fully"

**Anti**: "Claude sa meglio, eseguo cieco".
**Pattern mio**: "Claude propone, io valuto, decido".

### 2. "Multi-task in session"

**Anti**: "lanciamo install in background mentre configuriamo altro".
**Pattern mio**: "una cosa alla volta, lineare".

### 3. "Skip documentation"

**Anti**: "ora faccio, documento dopo".
**Pattern mio**: "documento mentre faccio, anche se rallenta".

### 4. "Generic prompt"

**Anti**: "aiutami con setup".
**Pattern mio**: specifico, scope-bound, con vincoli espliciti.

### 5. "Accept first solution"

**Anti**: "Claude propone X, ok facciamo X".
**Pattern mio**: "Claude propone X, ci sono Y, Z alternativas? Trade-off?".

## Claude Code vs Web Chat (distinzione)

**Web Chat (Claude.ai)**:
- Pensiero strategico, planning
- Research con web_search
- Thinking partner per decisioni
- Documentazione outline

**Claude Code (terminal)**:
- Execution concreta
- File operations
- Bash commands
- Commit + git
- Edit tecnici precisi

**Pattern mio**: uso **entrambi** in complementarità.
- Web chat: pianifico sessione + ricerche
- Claude Code: eseguo

Passa contesto da web chat a Claude Code via file (markdown plans) o copy-paste dei punti chiave.

## Subagents: quando e come

**Status attuale** (20/04/2026): **0 subagents**.

**Criterio per creare subagent**:
- Pattern ripetuto >10 volte
- Context stabile (non cambia per task)
- Input/output ben definiti
- Beneficio quantificabile (es. velocità, consistency)

**Esempi futuri probabili**:
- `rules-engineer` per Evo-Tactics (d20 mechanics consistency)
- `passport-auth` per Synesthesia (auth flow review)
- `italian-docs` per scrittura doc bilingue

**YAGNI fino a pattern emerga**: no subagent proattivo.

## Performance pattern (per sessioni produttive)

### Inizio sessione

```
1. Apri Claude Code nel giusto directory
2. Leggi CLAUDE.md (refresh contesto)
3. Leggi JOURNAL.md ultima entry (cosa era stato fatto)
4. Scrivi obiettivo sessione (anche solo mentalmente)
5. Start: "Oggi voglio fare X. Partiamo da Y."
```

### Durante sessione

```
1. Un task alla volta
2. Approvazione esplicita
3. Verifica output
4. Update JOURNAL.md in tempo reale
5. Commit atomico quando cambio conceptual è completo
```

### Fine sessione

```
1. Commit finale (anche WIP "wip: sessione XX pending Y tomorrow")
2. Update JOURNAL.md con bilancio
3. Se push: git push origin main
4. Exit Claude Code cleanly
```

## Context management

### CLAUDE.md pattern

File progetto-root con:
- Stack installato (reale, corrente)
- Stack pianificato (prossimi passi)
- Principi guida
- Comandi frequenti
- Decisioni chiave

**Aggiornare CLAUDE.md regolarmente** è investimento:
- Nuove sessioni Claude Code partono con context giusto
- Riduce prompt engineering ripetitivo

### /compact strategy

Se sessione diventa lunga (>30 interazioni):
- `/compact` (se Claude Code lo supporta) per comprimere storia
- O start nuova sessione con riferimento a JOURNAL.md entry

**Evito** sessioni infinite (hanno degrado di qualità per context bloat).

### File ignore

`.claudeignore` per escludere file ingombranti:
- `node_modules/`
- `venv/`, `__pycache__/`
- Large binaries, dataset
- Secret files (se presenti)

Per ora zero `.claudeignore` (setup minimal), ma pattern da ricordare.

## Claude Max vs future (Ollama, OpenRouter)

**Ora**: Claude Code con Opus 4.7 via Claude Max.

**Post-maggio**: Claude Code con API key propria (pay-per-use) + Ollama via Cline.

**Workflow cambierà?**
- Pattern core (un comando alla volta, approvazione) invariati
- Consumption consapevolezza aumenterà (paying per token)
- Modello locale Ollama = zero costo, zero friction per task routine

## Meta-learning

### Pattern emerso: "lavoro seduto"

**Osservazione**: i miei migliori risultati con Claude Code arrivano
quando sono **seduto comodo, concentrato, no multitasking**.

**Al contrario**: sessioni "veloci" con mind-wandering producono
più errori/rework.

**Policy personale**: se non posso essere concentrato 30+ minuti,
meglio rimandare sessione Claude Code.

### Pattern emerso: "Claude come thinking partner"

**Claude non è oracle**. Claude è:
- Rubber duck advanced
- Proposal generator
- Sintax helper
- Documentation co-author

**Decisioni strategiche**: sempre mie.
**Micro-implementation**: spesso Claude helping.

### Pattern emerso: "correggi reale-time"

Quando Claude drift (Z.ai, Mac mini dependency), **correggo subito**, non "dopo".

Correzione real-time:
- Evita propagazione errore in docs
- Recalibra Claude per resto della sessione
- Rinforza pattern corretto

### Quantificazione beneficio workflow

**Sessioni prima del trauma Victus** (ricordate):
- Errori: frequenti
- Rework: 30-40%
- Satisfaction: media
- Debito tecnico: alto

**Sessioni post-trauma con pattern**:
- Errori: 0 in 2 sessioni (10+ ore lavoro)
- Rework: 1 intenzionale (rename repo)
- Satisfaction: alta
- Debito tecnico: zero (ADR aggiornati)

**Rate**: più lento in step-by-step, ma **velocità netta maggiore** perché
zero rework.

## Fonti

- Claude Code docs: https://docs.claude.com/en/docs/claude-code
- Community best practices: https://github.com/anthropics/claude-code
- GitHub discussions various sessions

## Follow-up

### Da affinare

- Pattern per sessioni >4 ore (context management)
- Pattern per task molto ripetitivi (subagent valutazione)
- Pattern per multi-progetto session (switch context)

### Da documentare in futuro

- Tooling: quale MCP effettivamente installo (se/quando)
- Metriche: tempo medio per task tipo X
- Error patterns: quali errori ricorrono
