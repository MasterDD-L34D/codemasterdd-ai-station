# ARCHON Agent Scanner -- cross-fleet deploy design

> **Status (2026-06-23):** shipped -- OD-007 3-layer deploy + agent-scanner skill live

- **Status**: Approved (design) 2026-05-28 -- pending implementation plan
- **Owner**: Eduardo
- **Brainstorm**: questa sessione (superpowers:brainstorming, Protocol 6)
- **Problema**: chiusura OD-007 ("AA01 capability registry / scan automatico?") aveva applicato un fix L1 parziale (link in `aa01/AGENTS.md` DRILL-DOWN). Eduardo ha segnalato il gap: discovery-by-link != semantic auto-trigger cross-fleet. Per "reazione automatica" del modello su OGNI sessione Claude Code (qualsiasi PC, qualsiasi progetto) serve un deploy global, non un link interno AA01.

## 1. Contesto & problema

### 1.1 Lo stato pre-design

- ARCHON v2 dentro AA01 ha gia' built l'Agent Scanner skill: `aa01/archon/skills/agent-scanner/SKILL.md` + `aa01/archon/templates/agent_registry.yaml` + decisione `D-007` (overlap 70% threshold) + 4 trigger mandatori (BOOTSTRAP / TEAM_FORMATION / DELTA / ON_DEMAND).
- L'asset esiste ma NON e' discoverable dal Claude Code skill loader: vive in un path interno ARCHON (`aa01/archon/skills/...`), non in `~/.claude/skills/` o `.claude/skills/`.
- Conseguenza: il modello in sessione non vede mai la skill nel session-start skill-list -> nessun auto-trigger semantic -> il bias "scelgo l'agent che ricordo" persiste anche su Eduardo + agent ARCHON-aware.
- Discovery gap, NON feature gap. La feature esiste, manca il deploy.

### 1.2 Anti-pattern famiglia

- Anti-pattern #19 ("stale tracker / shipped work non riconciliata"): la versione meta = "asset shipped ma non discoverable" = stesso effetto pratico.
- Anti-pattern Shadow Duplication (Ibrahim 2026, Microsoft Multi-Agent Reference Architecture): se la skill non e' visible, il modello ricrea agent paralleli ("creo planner-v2 quando planner funziona").
- L1 only (link in AGENTS.md AA01 drill-down) cattura solo sessioni AA01-context che leggono drill-down. Cross-fleet auto-trigger richiede L2 (skill in `~/.claude/skills/`) + L3 (directive in `~/.claude/CLAUDE.md`).

## 2. Goals & non-goals

### Goals

- G1: skill `agent-scanner` discoverable dal Claude Code skill loader su OGNI sessione (Lenovo + Ryzen + futuri PC), qualsiasi progetto.
- G2: directive in `~/.claude/CLAUDE.md` che istruisce il modello a INVOCARE scanner PRIMA di selezione subagent/skill/agent (STRONG calibration, no bypass via memoria episodica, eccezione minima esplicita).
- G3: deploy cross-PC riproducibile via `git pull codemasterdd` + script idempotente, no manual edit dei file user-global.
- G4: zero modifica della FULL ARCHON skill in AA01 (preserve canonical ARCHON ownership).
- G5: rollback completo via `-Remove` (skill dir + CLAUDE.md section + bak restore).

### Non-goals

- NO modifiche al ARCHON v2 system (la FULL skill resta as-is, AA01-internal).
- NO migrate AA01 a struttura Claude-Code-native (AA01 e' NON-git per design).
- NO SessionStart hook custom (over-engineer: la directive in CLAUDE.md + semantic trigger via skill description e' sufficiente).
- NO cross-org skill sharing (IETF agents.txt out of scope).
- NO auto-pull/auto-deploy via git post-merge hook (richiede sessione separata se mai trigger).

## 3. Architettura (two-tier deploy)

### 3.1 Canonical paths

```
codemasterdd-ai-station/                     # git-tracked, cross-PC via pull
  .claude/global-skills/agent-scanner/
    SKILL.md                                 # LITE version (canonical for global)
  .claude/global-claude-md-fragments/
    agent-scanner-directive.md               # L3 directive canonical
  scripts/setup/
    deploy-global-skills.ps1                 # idempotent deploy

aa01/                                        # non-git, AA01-local
  archon/skills/agent-scanner/SKILL.md       # FULL ARCHON (UNCHANGED)
  AGENTS.md                                  # DRILL-DOWN link added 2026-05-28 (L1)

~/.claude/                                   # user-global, per-PC, deployed
  skills/agent-scanner/SKILL.md              # deployed from LITE canonical
  CLAUDE.md                                  # L3 directive section appended
```

### 3.2 Deploy flow

```
codemasterdd canonical
        |
        | scripts/setup/deploy-global-skills.ps1 (idempotent, sandbox-tested)
        v
~/.claude/skills/agent-scanner/SKILL.md  (Claude-Code-discoverable)
~/.claude/CLAUDE.md  (sentinel-merged directive)

Cross-PC: git pull codemasterdd + deploy script -> stesso stato su Ryzen.
```

### 3.3 Decisione canonical-where

- **LITE** -> codemasterdd (git-tracked, cross-PC reproducibility, audit trail).
- **FULL ARCHON** -> AA01-internal (ARCHON ownership intatto).
- **Deploy target** -> `~/.claude/` (per-PC, derivato dal canonical, mai canonical esso stesso).

Non-overlap intenzionale: la LITE non duplica la FULL, sostituisce solo i pezzi cross-project robust (step 1+2 sources/parsing). I pezzi ARCHON-specific (step 3 overlap + step 4 thresholds + step 5 registry write) restano ESCLUSIVI alla FULL.

## 4. LITE skill scope

### 4.1 Steps inclusi/esclusi

| # | Step | LITE | Razionale |
|---|------|:---:|---|
| 1 | Enumeration sources (find agents) | KEEP | Cross-project robust se ogni find ha `2>/dev/null` |
| 2 | Parse frontmatter (name, description, tools, model) | KEEP | Standard Anthropic, agnostico al progetto |
| 3 | Overlap calc vs 7 ruoli universali ARCHON | DROP | I 7 ruoli sono ARCHON-internal; non esistono fuori AA01 |
| 4 | Soglie REUSE_AUTO / REUSE_CONFIRM / COMPLEMENT | DROP | Dipendono da Step 3 |
| 5 | Registry write `.archon/registry/agent_registry.yaml` | DROP | Path ARCHON-specific |

### 4.2 Sorgenti enumerate (LITE)

Priorita' decrescente, tutte graceful-missing (`2>/dev/null`):

1. `.claude/agents/*.md` (PROJECT)
2. `~/.claude/agents/*.md` (USER global)
3. `.claude/skills/*/SKILL.md` (PROJECT skills)
4. `~/.claude/skills/*/SKILL.md` (USER global skills)
5. `.claude/plugins/cache/*/agents/*.md` + `plugins/.../skills/*/SKILL.md` (plugin agents+skills)
6. `AGENTS.md` + `CLAUDE.md` inline mentions (grep estratto)
7. Pointer ARCHON se `aa01/archon/` detected nel CWD o nei parent. **Nota**: AA01 e' Lenovo-edusc-only per design (memory `project_aa01_studio`); sui PC senza AA01 (Ryzen e altri) source-7 e' assente, NON e' un errore -- il report omette il pointer ARCHON e la LITE opera solo sulle sources 1-6.

### 4.3 Output format

Markdown report read-only:

```markdown
## Agent discovery report (scope: <cwd>)

| name | description (truncated 80ch) | source | tools / model |
| --- | --- | --- | --- |
| harsh-reviewer | Tough quality review (code / ADR / plan) | ~/.claude/agents/ | All / opus |
| sot-drift-verifier | Sovereign gated SoT-vs-runtime verdict | .claude/agents/ | Read,Grep,Glob,Bash / inherit |
| ... | ... | ... | ... |

## Next-action hint

Consider REUSING an existing agent above before creating new
(anti-shadow-duplicate, Ibrahim 2026 + Microsoft Multi-Agent Ref Arch).

## ARCHON full version

If `aa01/archon/` detected -> use `aa01/archon/skills/agent-scanner/SKILL.md`
for overlap calc + role mapping + registry persistence.
```

### 4.4 Trigger description (frontmatter LITE)

```yaml
---
name: agent-scanner
description: >
  Use BEFORE selecting/recommending any subagent/skill/agent for a
  non-trivial task. Anti-shadow-duplicate (build on existing work,
  never recreate; Ibrahim 2026 + Microsoft Multi-Agent Ref Arch).
  Triggers: "scan agents", "quali agenti ho", "inventario agenti",
  "riusa agente", "registry", "overlap", "mappa agenti",
  "che agent uso", "serve un agent per X", "team formation".
tools: [Bash, Glob, Grep, Read]
---
```

### 4.5 Constraints

- NO write su disco (read-only).
- NO registry persist.
- NO overlap math.
- Dimensione attesa: ~80-120 righe.
- Reversibile per design (zero side-effect).

## 5. L3 directive (`~/.claude/CLAUDE.md`)

### 5.1 Calibration: STRONG-PURE (no eccezione)

Eduardo decision 2026-05-28 (brainstorm L3-calibration question + harsh-reviewer P0#1 amendment): scanner SEMPRE invoked before any subagent/skill/agent selection. **STRONG-PURE: nessuna eccezione**. La precedente formulazione ("eccezione minima per task meccanici single-file") e' stata rimossa perche' "meccanico" e "selezione agent" sono categorie di model-judgment vaghe, esposte a bypass involontario (es. aider-cosmetic / batch lint-fix / ADR drafting hanno de-facto routing senza prompt esplicito). Rule unica leggibile + bias false-positive accettato (cost ~2-5sec << cost shadow-duplicate).

### 5.2 Posizione nel file target

Nuovo top-level subito DOPO "Anti-Pattern Catalogue" section (adjacency governance -- directive e' mitigazione anti-pattern Shadow-Duplicate).

### 5.3 Contenuto canonical

File: `codemasterdd/.claude/global-claude-md-fragments/agent-scanner-directive.md`.

Contenuto (~35 righe, body ASCII):

```markdown
## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG, no bypass): PRIMA di selezionare, raccomandare o creare un
nuovo subagent / skill / agent specializzato, INVOCA la skill `agent-scanner`
(semantic trigger: "scan agents" / "quali agenti ho" / "che agent uso" /
"riusa agente"). Principio cardine: **build on existing work, never recreate**
(Ibrahim 2026; Microsoft Multi-Agent Reference Architecture).

**Trigger mandatori** (4, mutuati da ARCHON v2 D-007):
- **BOOTSTRAP**: nuova sessione su un progetto -> invoca step-1 prima di altre
  decisioni di routing agent.
- **TEAM_FORMATION**: prima di proporre/creare un nuovo agent specializzato.
- **DELTA**: a inizio sessione, diff vs scan precedente.
- **ON_DEMAND**: comando utente esplicito ("scan agents").

**Sorgenti** (priorita decrescente, vedi SKILL.md):
`.claude/agents/` PROJECT > `~/.claude/agents/` USER > plugin agents >
`~/.claude/skills/` > `.claude/skills/` > `AGENTS.md`/`CLAUDE.md` inline.

**Skill locations** (two-tier):
- **LITE cross-project**: `~/.claude/skills/agent-scanner/SKILL.md` (default
  globale, enumeration + parsing + markdown report read-only).
- **FULL ARCHON** (solo in AA01 context, `aa01/archon/` detected):
  `aa01/archon/skills/agent-scanner/SKILL.md` (aggiunge overlap-calc 7 ruoli
  + REUSE_AUTO/CONFIRM/COMPLEMENT thresholds + registry persistence).

**Anti-pattern bloccati**:
- **Shadow duplication**: creo planner-v2 quando planner funziona (Ibrahim 2026).
- **Silent override**: file con `name:` duplicato sovrascrive precedente senza warning -- scanner lo flagga in report.
- Bias "chi-ho-piu-memoria-recente-vince" su selezione agent.

**STRONG-PURE**: nessuna eccezione. Scanner fires anche su task apparentemente meccanici (typo fix / rename / batch lint) per evitare bypass involontario via "model-judgment di triviality". Cost overhead ~2-5sec/fire accettato come prezzo dell'assenza di ambiguity rule.

**Reference**: OD-007 closure 2026-05-28 + first-principles application
`docs/research/2026-05-28-od-007-first-principles-application.md` +
deploy spec `docs/superpowers/specs/2026-05-28-archon-agent-scanner-
cross-fleet-deploy-design.md`.

<!-- END agent-scanner-directive -->
```

### 5.4 Sentinel markers (start + end, bounded)

Due sentinel separati per merge + rollback safe-bounded:

- **Start sentinel**: heading `## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)` (sufficientemente specifico).
- **Disambiguation**: scan **first non-blank line within next 5 lines after the start sentinel**, anchor regex `^\*\*Rule\*\* \(STRONG`. La canonical fragment ha una blank line tra heading e `**Rule**` -- detector deve skippare blank lines, NON leggere riga N+1 secca (P0#2 harsh-reviewer).
- **End sentinel**: `<!-- END agent-scanner-directive -->` (HTML comment, invisible in rendered MD, univoco).
- **Range bounded**: tutte le operazioni merge / rollback / re-apply usano `[start sentinel ... end sentinel]` come range esplicito. Mai "next `^## ` heading" come terminator (P0#3 harsh-reviewer footgun: user-added content tra directive e prossimo heading verrebbe mangiato dal -Remove).

## 6. Deploy mechanism

### 6.1 Script

Path: `codemasterdd/scripts/setup/deploy-global-skills.ps1`.

Compatibility: PowerShell 5.1 + PowerShell 7.

Invocation modes:

```powershell
.\deploy-global-skills.ps1            # DRY-RUN (default, preview)
.\deploy-global-skills.ps1 -Apply     # write to ~/.claude/
.\deploy-global-skills.ps1 -Remove    # rollback (rm skill dir + remove section)
```

### 6.2 Workflow

In ordine:

1. **Path normalize**: `$repoRoot = (Resolve-Path $PSScriptRoot/../..).Path` (no `..\` residue, anti-pattern #9a).
2. **Sandbox QG Step-1** (mandatory, anti-pattern #9b):
   - Crea `$env:TEMP/deploy-global-skills-sandbox-<guid>/.claude/`.
   - Esegui deploy in sandbox.
   - Verifica artefatto scritto (file present + parse + content + encoding).
   - Re-run 2a volta in sandbox -> diff = none (idempotency).
   - Hard-fail se sandbox red -> NON procede a `~/.claude/` reale.
3. **Skill deploy** (LITE):
   - **Ensure target dir** (P1#5 harsh): `New-Item -ItemType Directory -Force $env:USERPROFILE\.claude\skills` (no-op if existe; necessario su Ryzen fresh / nuovo PC senza Claude Code mai aperto).
   - **Pre-copy drift check** (P1#1 harsh): se `$env:USERPROFILE\.claude\skills\agent-scanner\SKILL.md` esiste, hash-compare contro canonical. Se hash diversi (drift = user edit locale) -> backup `agent-scanner\SKILL.md.bak-<ts>` PRIMA del Copy-Item + log "DRIFT DETECTED, .bak saved".
   - `Copy-Item -Recurse -Force $repoRoot\.claude\global-skills\agent-scanner $env:USERPROFILE\.claude\skills\agent-scanner`.
   - Idempotente: re-run = overwrite from canonical = stesso contenuto (no .bak generato se hash uguale).
4. **CLAUDE.md merge** (sentinel-based bounded, NO blind append):
   - `Copy-Item ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak-<timestamp>` (backup pre-modify).
   - Check **start sentinel** + scan first non-blank within next 5 lines per `^\*\*Rule\*\* \(STRONG` -> se entrambi match -> sentinel valido + SKIP append (idempotent).
   - Se start sentinel match MA disambiguation fail -> warn + abort (exit 4, vedi sec 7.1).
   - Se start sentinel assente -> append fragment content (start sentinel + body + END sentinel `<!-- END agent-scanner-directive -->`).
   - **Encoding**: `[System.IO.File]::ReadAllText/WriteAllText` con `[System.Text.UTF8Encoding]::new($false)` (UTF-8 no-BOM esplicito, evita PS5.1 BOM gotcha).
   - **Line-ending normalization** (P2#1 harsh): on Windows write, normalize content to CRLF prima del WriteAllText (evita mixed-endings se canonical fragment LF + target CLAUDE.md CRLF). Pattern: `$content = $content -replace "(?<!`r)`n", "`r`n"`.
5. **Post-deploy verify**:
   - SKILL.md frontmatter parses (regex match).
   - CLAUDE.md sentinel present (Select-String).
   - ASCII check sul body deployato.
   - Exit 0 verde, 1 se qualcosa fallisce.
6. **Rollback path** (`-Remove`, bounded sentinel-to-end):
   - `Remove-Item -Recurse -Force ~/.claude/skills/agent-scanner`.
   - CLAUDE.md: regex multiline replace bounded **tra start sentinel `## Agent Scanner discipline` e end sentinel `<!-- END agent-scanner-directive -->`** (inclusivi). Pattern: `(?ms)^## Agent Scanner discipline.*?<!-- END agent-scanner-directive -->\r?\n?`. NON usa "next `^## `" come terminator (P0#3 footgun mitigation: user-added content post-directive non viene mangiato).
   - Fallback se end sentinel assente (directive shipped da una versione vecchia pre-P0#3 fix): restore da `.bak` piu' recente + warn user.
   - `.bak` preservato (mai cancellato da -Remove).

### 6.3 Cross-PC flow

```
Lenovo (oggi, post-merge codemasterdd):
  git -C codemasterdd pull origin main
  .\scripts\setup\deploy-global-skills.ps1            # preview
  .\scripts\setup\deploy-global-skills.ps1 -Apply     # write

Ryzen (same flow):
  git -C codemasterdd pull origin main
  .\scripts\setup\deploy-global-skills.ps1 -Apply

Risultato: entrambi i PC ~/.claude/skills/agent-scanner/SKILL.md identical +
~/.claude/CLAUDE.md ha sentinel.
```

### 6.4 Anti-pattern catch list (script implementa difese)

- #9 idempotent-write: sandbox -Apply test obbligatorio pre live.
- #9b encoding: UTF-8 no-BOM esplicito.
- #11 fragile helper: NO nested SSH, NO cross-shell pipe. Script PowerShell puro, locale per PC.
- #12 non-ASCII enforcement: ASCII check post-deploy.
- L-2026-05-040 (PS native-stderr-under-Stop): `$ErrorActionPreference = "Continue"` + check `$LASTEXITCODE` esplicito su native exe.

## 7. Error handling & degradation modes

### 7.1 Deploy-time

| Modo | Detection | Action |
|------|-----------|--------|
| `~/.claude/` permission denied | `Test-Path` + try-write to temp | hard-fail, exit 2 |
| Canonical missing (codemasterdd path broken) | `Test-Path` pre-deploy | hard-fail, exit 3 |
| `~/.claude/CLAUDE.md` non esiste | `Test-Path` | crea nuovo file con solo directive (+ comment auto-created) |
| Sentinel false-positive (start sentinel match ma disambiguation fail) | scan first non-blank within next 5 lines per `^\*\*Rule\*\* \(STRONG`, no match | warn + abort, **exit 4 (distinct da 2/3)** + scrive `~/.claude/.apply-blocked-<ts>.log` con dump CLAUDE.md heading-context circostante. Risoluzione manuale required (P1#4 harsh) |
| Disk full / write fail mid-merge | try/catch su WriteAllText | restore da `.bak` + hard-fail |
| Idempotency violation (2a run diff non-trivial) | sandbox diff check | hard-fail in sandbox, NON procede live |
| `-Apply` non passato (dry-run default) | flag check | output preview + exit 0, NESSUN write |

### 7.2 Runtime (LITE skill in sessione)

| Modo | Detection | Output |
|------|-----------|--------|
| Source dir missing | `find ... 2>/dev/null` | continua con altre, report parziale |
| Permission denied su sorgente | exit code find + file empty | log "SOURCE UNREADABLE: <path>" nel report |
| Frontmatter malformato | YAML parse exception per-file | log "MALFORMED FRONTMATTER: <file>", skip, continua |
| Zero agenti totali | report vuoto | output esplicito "no agents discovered -- baseline: general-purpose only" |
| Inventory >50 agenti (token cost) | count post-enum | **hard cap 50** entries nel report; rank by source-priority order 1-7 (sez 4.2: PROJECT > USER > plugin > skills > AGENTS.md inline > ARCHON); footer "+N more in `<source>`" per le entries droppate. NO keyword-match (rimosso, dipendeva da context model-side non disponibile pre-render report) |
| Skill assente pre-deploy su PC | Claude Code skill loader non la trova | degrade silent a baseline; post-pull reminder mitigation |

### 7.3 Distinzione esplicita

La LITE OUTPUT discrimina "no agents found" (legitimate) vs "enumeration failed" (BROKEN_SCAN flag) -- NO silent-empty. Model instructed a NOT proceed con agent-selection se BROKEN_SCAN.

### 7.4 L3 directive degradation

- **STRONG-PURE applied**: nessuna eccezione attiva. Scanner fires anche su task apparentemente meccanici (no model-judgment di triviality). Cost overhead accettato come prezzo dell'assenza di ambiguity (vedi sec 5.1).
- **Pre-deploy PC fresh**: directive assente, degrade silent a baseline. Mitigazione: workflow `git pull -> deploy.ps1 -Apply` documentato.
- **Skill errore runtime**: report include fallback msg "scanner failed: <err>, manual review `.claude/agents/` + `~/.claude/agents/` raccomandato prima agent-selection".

## 8. Testing / validation strategy

### 8.1 Quality Gate Step 1/2/3 mapping

- **Step 1 Smoke**: test layer 2 (sandbox) + test layer 3 (live -Apply Lenovo).
- **Step 2 Research** (>=3 edge case): test layer 4 (behavioral) + test layer 5 (cross-PC) + test layer 6 (idempotency + rollback) -> 5 edge case coperti.
- **Step 3 Tuning**: test layer 7 (token cost baseline) + iterazione se token cost emerge problematic.

### 8.2 Test layers

1. **Unit / LITE skill body** (pre-deploy):
   - Sintetico: temp dir con 1 `.claude/agents/X.md`, 1 `~/.claude/agents/Y.md`, 1 plugin agent, 1 frontmatter malformato -> verifica report ha 3 valid + 1 MALFORMED, non silent-empty.
   - Reale: enumerazione codemasterdd `.claude/agents/` -> trova 18 agent categorize.

2. **Deploy sandbox QG Step-1** (automated, mandatory pre-live):
   - Script auto-esegue prima di ogni write live.
   - Verifica: file written + frontmatter + ASCII + sentinel + 2a run no-op.
   - Hard-fail in sandbox -> abort live.

3. **Live `-Apply` Lenovo** (gated post-sandbox-green):
   - Eduardo run.
   - Verifica skill esiste + CLAUDE.md sentinel + line count delta +35+/-5 + ASCII + `.bak` timestamp.

4. **Behavioral smoke** (fresh Claude Code session):
   - Prompt "che agent uso per code review?" -> scanner auto-fires.
   - Prompt "scan agents" -> ON_DEMAND fire.
   - Prompt "fix typo line 42" -> scanner NO-fire (eccezione minima).

5. **Cross-fleet Ryzen**:
   - `git pull` + `-Apply`.
   - Diff hash file deployati == Lenovo.
   - Smoke layer 4 replicato su Ryzen.

6. **Negative + reversibility**:
   - 2a `-Apply` = no-op (diff none, live idempotency).
   - `-Remove` -> skill gone + sentinel absent + `.bak` present.
   - Re-Apply post-Remove restora correttamente.

7. **Token cost baseline** (post first real invocation):
   - Capture token-in/token-out + time-to-output.
   - Soglia review: >2000 tok/inv x N sessioni/day = ottimizza.

### 8.3 Deliverable post-test

`QUALITY.md` (o sezione README) in `codemasterdd/.claude/global-skills/agent-scanner/` con 3 step QG spuntati + evidenza (output log + screenshot transcript behavioral smoke).

## 9. Reversibility & rollback

Reversibile completamente via `-Remove`:

- `~/.claude/skills/agent-scanner/` rimossa (zero residuo).
- `~/.claude/CLAUDE.md` section rimossa (regex multiline replace tra sentinel e next `^## `).
- `.bak` timestamp preservato; restore manuale possibile via `cp ~/.claude/CLAUDE.md.bak-<timestamp> ~/.claude/CLAUDE.md`.
- AA01-side L1 (drill-down link) NON toccata da -Remove (e' AA01-internal, fuori scope deploy script).
- Canonical in codemasterdd NON toccata da -Remove (e' source of truth, non target).

## 10. Open questions / risks

### Risks accettati

- **R1: token cost cumulative** -- scanner STRONG-PURE fires su OGNI sessione (no eccezione) = ~2-5sec + ~500-2000 tok per fire. Stima 10 sessioni/day x 2 PC = ~5-20k tok/day extra. **Tuning trigger esplicito** (P1#3 harsh): post N=5 sessioni Lenovo + 5 Ryzen (baseline capture test layer 7), se **mean fire-rate >50% su prompt non-selection** OR **mean tokens-per-fire >2000** -> tune description keywords (riduci semantic surface) + considera plugin packaging (Q1) per gating piu' chirurgico. Misura prima, decidi dopo (anti-L-016 aspirational).
- **R2: false-positive auto-fire** -- prompt che menziona "agent" in senso non-tecnico potrebbe far fire spurio. Mitigation: trigger keywords specifici nel description; con R1 threshold sopra, R2 rientra automaticamente nella misura (false-positive contano nel fire-rate).
- **R3: cross-PC drift se Ryzen non runna `-Apply` post-pull** -- degrade silent. Mitigation: workflow documentato + reminder post-pull (futuro: git hook auto-deploy, Q2).

### Open questions

- Q1: Plugin packaging (Option C nel brainstorm) future-proof se nascono altre skill global. Defer decisione finche' >=3 skill cross-fleet emergono (Three Strikes).
- Q2: SessionStart hook custom per hard-enforce scanner invocation -- over-engineer ora. Riapri solo se evidence di bypass via memoria episodica anche post-L3-STRONG.

## 11. References

- OD-007 entry: `OPEN_DECISIONS.md` (CLOSED-DUPLICATE-CONFIRMED 2026-05-28 pomeriggio).
- First-principles application: `docs/research/2026-05-28-od-007-first-principles-application.md`.
- ARCHON Agent Scanner full design: `aa01/archon/skills/agent-scanner/SKILL.md` + `aa01/research/07-subagents-and-registry/README.md`.
- Decision ARCHON D-007: agent scanner con overlap soglia 70.
- Ibrahim Mohamed (apr 2026) "Build on existing work. Never recreate." -- principio cardine.
- Microsoft Multi-Agent Reference Architecture (2026) -- monitor agent overlap to prevent redundancy.
- L1 already shipped (drill-down link): `aa01/AGENTS.md` DRILL-DOWN section row added 2026-05-28.
- Anti-pattern catalogue: #9 (sandbox QG), #11 (fragile helper), #12 (non-ASCII enforcement), #19 (stale marker family).
- Lessons related: `aa01/learnings/L-2026-05-040-powershell-native-stderr-under-stop-false-fail.md`.

## 12. Self-review notes + harsh-reviewer amendment log

### 12.1 Self-review (pre harsh-reviewer)

- **Placeholder scan**: zero TBD / TODO / FIXME residui post-cleanup.
- **Internal consistency**: section 3 deploy flow + section 6.3 cross-PC flow allineate; section 5.3 directive content + section 6.2 merge logic consistente.
- **Scope**: implementation plan fattibile in singolo plan (stimato 10-15 task post-amendments -> harsh-reviewer ha alzato a 15-18, borderline split-acceptabile).
- **ASCII**: body verified clean (0 non-ASCII chars, `--` non em-dash).

### 12.2 Harsh-reviewer amendments (2026-05-28, post `3feef6a`)

Verdetto harsh: REWORK (small). Applicati i 3 P0 + 5 P1 + 4 P2 + 2 Eduardo opinion-questions answered:

| # | Severita | Issue | Fix applicato |
|---|----------|-------|---------------|
| P0#1 | block | "Eccezione minima" mechanical = model-judgment vago | Eduardo decision: **STRONG-PURE no eccezione** (sec 5.1 + 5.3 + 7.4 riscritti, false-positive bias accettato) |
| P0#2 | block | Sentinel disambiguation legge riga N+1 (blank) | sec 5.4 + 6.2 step 4: scan first non-blank within next 5 lines, regex `^\*\*Rule\*\* \(STRONG` |
| P0#3 | block | -Remove regex "between sentinel and next `^## `" eat user content | sec 5.4 + 5.3 + 6.2 step 6: aggiunto END sentinel `<!-- END agent-scanner-directive -->` + range bounded |
| P1#1 | should | Copy-Item -Force silently overwrites user edits | sec 6.2 step 3: pre-copy hash-compare + `.bak-<ts>` se drift |
| P1#2 | should | Inventory >30 "keyword match" undefined | sec 7.2: hard cap 50 + ranked by source-priority + "+N more" footer (no keyword match) |
| P1#3 | should | R1 threshold aspirational | Eduardo decision: **define now** (sec 10 R1): post N=5+5 baseline, trigger = fire-rate >50% non-selection OR tokens-per-fire >2000 |
| P1#4 | should | Sentinel false-positive silent abort | sec 7.1: exit 4 distinct + `~/.claude/.apply-blocked-<ts>.log` |
| P1#5 | should | Skill dir potentially missing on fresh PC | sec 6.2 step 3: `New-Item -ItemType Directory -Force ~/.claude/skills` pre-Copy |
| P1#6 | should | AA01 detection cross-PC implicit | sec 4.2 source 7: nota esplicita "AA01 Lenovo-only by design, Ryzen source-7 absent non e' errore" |
| P2#1 | nice | CRLF normalize Windows write | sec 6.2 step 4: regex `(?<!\\r)\\n -> \\r\\n` pre WriteAllText |
| P2#4 | nice | "Silent override" anti-pattern undefined | sec 5.3 anti-pattern list: definito inline "file con `name:` duplicato sovrascrive precedente senza warning" |
| P2#3 | nice | Scope claim 10-15 task ottimistico | sec 12.1 aggiornato a 15-18 borderline-split-acceptabile |

3 P0 chiusi + 5 P1 chiusi + 4 P2 chiusi. Spec ora ready per `superpowers:writing-plans`.
