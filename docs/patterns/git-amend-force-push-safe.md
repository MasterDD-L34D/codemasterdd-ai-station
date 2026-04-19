# Pattern: Git amend + force-push safe

**Data formalizzazione**: 2026-04-20
**Scopo**: documentare pattern sicuro per amend + force-push
**Applicato**: sessione 20/04 quando ho integrato Ollama in commit esistente

## Executive summary

**`git commit --amend` + `git push --force-with-lease`** è il pattern
sicuro per correggere l'ultimo commit già pushato.

**`--force-with-lease` è superiore a `--force` nudo** perché fallisce
elegantemente se il remote è cambiato sotto i piedi (protezione contro
sovrascrittura lavoro altrui).

## Il problema

**Scenario tipico**:

1. Ho committato `feat: install dev stack (node, python, vscode)`
2. Ho fatto `git push origin main` → commit su GitHub come `087442c`
3. Dopo, ho installato Ollama come bonus (stesso "arco" dev stack)
4. Voglio **includere Ollama nel commit precedente**, non fare commit separato

**Perché includere, non separare**:
- Ollama è parte dello stesso cambio logico (dev stack)
- Storia git più pulita con commit semanticamente coerenti
- `feat: install dev stack + ollama` è ancora atomico

### Opzioni considerate

**A)** Nuovo commit separato (storia "sporca" con 5 commit stasera)
**B)** Amend + force-push (storia pulita ma richiede riscrittura)

Ho scelto **B**. Vediamo come farlo safe.

## La soluzione: amend + force-with-lease

### Step 1: amend commit locale

```bash
# Modifica file (CLAUDE.md, JOURNAL.md con Ollama info)
# ...

# Stage changes
git add CLAUDE.md JOURNAL.md

# Amend: modifica l'ultimo commit includendo nuove modifiche
git commit --amend --no-edit
# --no-edit: mantiene messaggio originale

# Se volessi cambiare anche il messaggio:
# git commit --amend -m "new message"
```

**Risultato**: il commit ha nuovo SHA (es. `0059d45`) che sostituisce `087442c`.

### Step 2: verifica locale

```bash
git log --oneline -5
```

Output:
```
0059d45 feat: install complete dev stack (node, python, vscode, ollama)
e8c372c chore: gitignore Claude Code local settings
eb425d1 docs: rename workstation label to CodeMasterDD
9de5254 chore: initial project structure
```

Nota: `087442c` non esiste più localmente. È stato sostituito da `0059d45`.

### Step 3: force-push safe

**NO** `git push --force` (pericoloso).
**SÌ** `git push --force-with-lease=branch:expected_sha`.

```bash
git push --force-with-lease=main:087442c origin main
```

**Semantica**:
- `--force-with-lease=main:087442c`: "push force solo se `origin/main` è esattamente `087442c`"
- Se qualcun altro ha pushato dopo il mio `087442c`, il lease fallisce
- Fallimento = abort sicuro (no sovrascrittura lavoro altrui)

**Output successo**:
```
+ 087442c...0059d45 main -> main (forced update)
```

Il `+` indica force-push. La transizione `087442c → 0059d45` è la riscrittura storia.

**Output fallimento** (scenario ipotetico):
```
! [rejected]        main -> main (stale info)
error: failed to push some refs to '...'
hint: Updates were rejected because the tip of your current branch is behind
```

In questo caso: **investiga cosa è cambiato su remote**, poi decidi.

## Varianti di force-with-lease

### Form base (shorthand)

```bash
git push --force-with-lease origin main
```

**Comportamento**: Git auto-detect expected SHA dall'ultimo `git fetch`.
**Rischio**: se hai fatto fetch dopo che qualcuno ha pushato, il tuo
"expected" potrebbe già includere il loro lavoro. Meno safe.

### Form explicita (raccomandato)

```bash
git push --force-with-lease=main:087442c origin main
```

**Comportamento**: specifichi esplicitamente il SHA che TI aspetti su remote.
**Rischio**: zero - solo push se quel SHA esatto è ancora tip del branch remoto.

**Mio pattern**: **SEMPRE form esplicita** quando ricordo il SHA.

### Form "cautious"

```bash
# Prima verifica cosa c'è remote
git fetch origin
git log origin/main --oneline -1
# Confronta con il tuo "expected SHA"

# Se match, procedi
git push --force-with-lease=main:$(git rev-parse origin/main) origin main
```

Più pedante ma ultra-safe per repo critici.

## Quando NON usare amend + force-push

### 1. Commit già parte di PR review

Se qualcuno sta reviewing il tuo commit `087442c` e tu lo rimpiazzi con `0059d45`,
la review si spezza (link al vecchio SHA non esiste più).

**Alternative**: commit fixup separato.

### 2. Branch collaborativo

Se altri hanno già basato lavoro sul tuo commit (branched da `087442c`),
force-push rompe i loro branch.

**Mio caso**: repo solo-dev, zero rischio.

### 3. Commit molto vecchio (>2-3 commit back)

Amend modifica solo HEAD. Per commit più vecchi, serve **interactive rebase**.

```bash
git rebase -i HEAD~5
# editor interattivo per riorganizzare/amendare commit specifici
```

**Per commit vecchi + push già fatto**: valuta se vale rework storia, spesso meglio commit fix separato.

### 4. Quando non ti serve riscrivere

Se il commit è "buono così", **lascialo**. La storia git **deve essere
immutable**, not "perfect". Il principio è: "stesso cambio logico, stesso commit".
Se aggiungi cose logicamente separate, fai nuovo commit.

## Il reasoning dietro la mia scelta

### Caso concreto 20/04/2026

**Situazione**:
- Commit `feat: install dev stack (node, python, vscode)` già pushato
- Ollama installato dopo
- Ollama = parte logica dello stesso arco ("dev stack")

**Perché amend**:
- Mantengo commit atomico per "stack completo"
- Storia git più leggibile
- Co-Author Claude citation corretta in un commit, non in due

**Perché accettabile**:
- Repo solo-dev, nessun altro ha clonato/basato lavoro
- Commit ancora "fresco" (pushato 1 ora prima)
- Motivazione chiara (non vanity)

## Template comandi pronti

### Template 1: amend simple (stesso messaggio)

```bash
# 1. Modifica file
# 2. Stage
git add <files>

# 3. Amend
git commit --amend --no-edit

# 4. Force-push safe
git push --force-with-lease=main:$(git log -1 --skip=1 --format=%H) origin main
```

**Nota**: `$(git log -1 --skip=1 --format=%H)` prende il SHA **precedente** a HEAD (quello che era su remote prima dell'amend).

### Template 2: amend con new message

```bash
# 1. Modifica file
# 2. Stage
git add <files>

# 3. Amend con nuovo messaggio
git commit --amend -m "feat: nuovo messaggio più accurato"

# 4. Force-push
git push --force-with-lease=main:<OLD_SHA> origin main
```

### Template 3: amend solo messaggio (no file changes)

```bash
git commit --amend -m "fix: corretto typo nel messaggio"
git push --force-with-lease=main:<OLD_SHA> origin main
```

## Risk mitigation checklist

**Prima di force-push**:

- [ ] Il commit è mio (non base di lavoro altrui)?
- [ ] Il repo è mio (no collaborazione attiva)?
- [ ] Ho il SHA vecchio a portata di mano per --force-with-lease?
- [ ] Sto usando `=branch:SHA` format (non shorthand)?
- [ ] Ho dietro git log locale di recent commits (per debug se fallisce)?

Se tutti YES → procedi.

## Alternative a force-push

### Reverse approach: revert + new commit

Invece di riscrivere storia:

```bash
# Crea commit che annulla precedente
git revert 087442c

# Poi commit nuovo con modifiche
git add <files>
git commit -m "feat: install dev stack + ollama (reintroduce + expand)"

# Push normale (no force)
git push origin main
```

**Pro**: storia immutable, zero rischio force-push
**Contro**: storia "rumorosa" con revert + re-introduce

**Quando usare**: repo condivisi, o quando preferisci audit trail visibile.

### Cherry-pick + branch manipulation

Per scenari complessi, branch aux + cherry-pick.
**Mio caso**: overkill. Stick with amend.

## Meta-learning

### Perché force-with-lease è "kind"

`--force` nudo: "sovrascrivi qualsiasi cosa sia su remote".
`--force-with-lease`: "sovrascrivi solo se remote è come mi aspetto".

Quest'ultimo è **gentile con gli altri** (inclusi i miei futuri self
che lavorassero da altro PC).

### Il trade-off storia vs evidence

**Storia pulita (amend + force)**:
- Più leggibile
- Commit atomici
- Richiede disciplina

**Storia evidente (revert + new)**:
- Più rumorosa
- Ma zero rischio
- Audit trail visibile

**Scelta mia**: amend finché repo è solo-mio. Se diventa collaborativo,
switch a revert approach.

### Git commit è "immutable"... until it isn't

**Principio Git**: storia è immutable.
**Realtà**: amend, rebase, reset **riscrivono** storia locale.
**Regola**: riscrittura di commit **già pushati** richiede cautela extra.

**Il tuo repo privato di infrastructure?** riscrittura OK con disciplina.
**Il codice di produzione condiviso con team?** NEVER force-push.

### Il SHA come "indirizzo stabile"

Ogni commit ha un SHA hash univoco (es. `087442c`). Finché commit esiste
in almeno una reflog/branch, il SHA funziona.

**Dopo amend**: il vecchio SHA (087442c) esiste ancora in **reflog locale**
per ~30 giorni. Questo significa:
- Puoi recuperare con `git reflog` + `git checkout 087442c`
- Anche dopo force-push, il commit vecchio esiste fino a GC

**Safety net nascosta**: tuo mistake è recuperabile 30 giorni.

## Troubleshooting

### Error: "stale info"

```
! [rejected]        main -> main (stale info)
```

**Cause**:
- Qualcun altro ha pushato su remote dopo il tuo ultimo fetch
- Il lease fallisce correttamente

**Fix**:
1. `git fetch origin`
2. `git log origin/main --oneline -5` per vedere cosa è cambiato
3. Decidi: merge loro cambi, o abort force-push

### Error: "non-fast-forward"

```
! [rejected]        main -> main (non-fast-forward)
```

**Cause**: standard rejection perché history diverge.
**Fix**: è quello che force-push è per (quando intenzionale).

### Perdo commit vecchio dopo amend

```bash
# Recover via reflog
git reflog
# Cerca il vecchio SHA nell'output (087442c...)

# Checkout o cherry-pick
git cherry-pick 087442c
# O reset hard
git reset --hard 087442c
```

**Tempo disponibile**: ~30 giorni prima di garbage collection Git.

## Fonti

- Pro Git book cap. 7 "Rewriting History": https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History
- GitHub blog on --force-with-lease: https://blog.github.com/2015-06-09-no-force-with-lease/
- Atlassian tutorial: https://www.atlassian.com/git/tutorials/rewriting-history

## Follow-up

### Da praticare

- Uso consistente di `--force-with-lease=main:SHA` explicit form
- Template comandi in `docs/reference/commands-cheatsheet-windows.md`

### Da evitare

- MAI `git push --force` senza lease
- MAI amend su commit >5 in back (usa interactive rebase)
- MAI force-push su branch shared
