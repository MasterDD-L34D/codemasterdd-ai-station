# Design spec — Cross-repo orchestrator evolution (Opt 1.5)

**Date**: 2026-05-13
**Status**: Draft REWORK post harsh-review (3 P0 + 6 P1 + 3 P2 findings integrated)
**Cross-ref**: ADR-0021 (multi-client pattern) + ADR-0026 (cognitive protocols) + L-012 (vault sibling-peer write under explicit auth)
**Methodology applied**: Protocol 6 brainstorming (superpowers skill) + Protocol 3 Archon 7-step First Principles + Protocol 5 harsh-reviewer subagent (post-draft adversarial)
**Confidence**: 70% (downgraded from aspirational 75%, post harsh-review P0.3 meta-recursion finding + post 3/3 P0 + 5/6 P1 + 3/3 P2 integration). PENDING P1.1 Eduardo input for final calibration.

## Methodology bias disclosure (post P0.3 fix)

**This spec applies the methodology it preserves** (Protocol 6 brainstorming + Protocol 3 Archon for designing a system that itself preserves Protocol 6 + 3 + adds Protocol 1 dashboard reinforcement). L-2026-05-016 explicitly warned against same-PR self-application as cherry-picking inflato. The 75% confidence claim was methodology-laundered.

Mitigations applied:
- Protocol 5 harsh-reviewer adversarial read invoked (output in commit history + spec body P0-P2 findings integrated). Counter-balance to meta-recursive self-validation.
- This spec does NOT count toward Protocol 6 n>=2 instance counter (anti-pattern L-016 caught).
- Falsifier: 30gg post-Max missed-coordination empirical tracking (Component 3) — independent of methodology preserved.

## Context

Eduardo richiesta 2026-05-13 sera-tardi: "siamo solidi come hub osservatore, non come orchestratore attivo. Facciamo il punto 1 [Re-design boundary cross-repo] per partire".

### Trigger acquisiti (3/4 selected via AskUserQuestion)

| Trigger | Selected | Implicazione |
|---------|----------|--------------|
| Visibility gap concreto | YES | **CLAIM ASSERTED ma NON-VERIFIED**: Eduardo ha selezionato l'opzione MA spec non documenta incident specifico (P1.1 harsh-review finding). Trigger rest su unverified self-report. See "Empirical trigger evidence" section sotto. |
| Post-Max anxiety | NO | NON è capability-anticipating fear. Esclude solution-looking-for-problem framing. |
| Coordination overhead percepito | YES | Eduardo single-bottleneck pain concreto. Pattern Eduardo media bidirezionale tutti i cross-repo flow. |
| Strategic alignment lungo termine | YES | Scaling 4 active monitored → 6-8 repo in 2-3 anni hypotetico. Forward-looking. |

### Empirical trigger evidence (PENDING Eduardo input)

**Status**: P1.1 harsh-review flag. Spec come scritto rest su trigger asserted ma non documented.

Pre-Accepted status richiede Eduardo:
- [ ] **Opzione A**: nominare 1-2 incident concrete missed-coordination ultimi 30gg con (data + scope + cost minuti). Cita qui inline.
- [ ] **Opzione B**: ammettere no concrete incident yet + rescope spec a "preventive instrumentation only" (drop Component 2+3 a gates, mantain Component 1 dashboard solo)

Senza una delle due, spec rimane Draft.

### Archon 7-step output

**RESTATE**: gestire 6 repo non-self come ecosistema coordinato post-Max (6gg residui Opus 4.7 al 2026-05-13), mantenendo zero subscription target $0-50/anno + governance interna autonoma 4 active monitored (Game Vue3 / Game-Godot-v2 / Dafne evo-swarm / AA01) + 1 sibling-peer (vault-shared) + 1 dormant (Synesthesia).

**DECOMPOSE** in primitivi irriducibili:
- P1: chi possiede write-path su un repo è chi decide cosa è "controllo" (Conway's law)
- P2: costo cognitivo policy aligned cresce con N repo × frequenza changes
- P3: modifica boundary cross-repo è costosa-da-reverse (richiede consenso governance interna 4 repo + ADR amendment cross-repo)
- P4: post-Max NO Opus 4.7 multi-file synthesis → tier capability gap per orchestration strategic
- P5: Eduardo è single human coordinator, bandwidth limitato

**CHALLENGE — falsifier check**:
- Empirical check (BACKLOG + JOURNAL + STATUS_MULTI_REPO): governance interna autosufficiente NON sta fallendo
- Game-Godot-v2 215+ PR auto-gestiti zero codemasterdd intervention
- Vault 7/7 PRODUCTION milestone hit autonomously
- Dafne Atto 2 day 14+ stabile
- AA01 16 lessons cumulative + 0 inbox/workspace

→ Opt 3 (write-direct) e Opt 4 (mesh-bus) PIENI sono **prematuri** senza failure trigger. Cost asimmetrico.

**RECONSTRUCT da primitivi**: Opt 1.5 (Read-active dashboard + Write-via-PR opportunistic + Strategic escalation gates) emerge come reconstruction stabile da P1-P5. Soddisfa trigger #1 + #3 al 100%, trigger #4 parzialmente via escalation gates.

**RED-TEAM pre-mortem 12 mesi**:
- Opt 3 fail scenario: Conway's law uccide ADR amendment cross-repo. Eduardo abbandona dopo 2-3 mesi.
- Opt 4 fail scenario: Bootstrap 4-8 settimane consuma budget Pro reactivated. Synesthesia incompatibile mixed privacy.
- Opt 1.5 fail scenario: underpowered per ≥2 use case strategic → pivot a Opt 3/Opt 4 dopo 90gg empirical con trigger documentato.

Asymmetric cost: Opt 1.5 fallisce con "underpowered + reversible pivot" (cheap). Opt 3/Opt 4 falliscono con "overpowered + Conway's law violation" (expensive).

**CALIBRATE**:
- Verdetto: **Opt 1.5 baseline con escalation gates espliciti**
- Confidenza: 75% (ECE-adjusted)
- Assunti portanti rimasti: (1) governance interna continua funzionare post-Max, (2) Eduardo bandwidth per dashboard build pre-Max sufficiente, (3) sovereign tier sufficient per Read-active + Write-via-PR singoli
- Falsificatore: 30gg post-Max tracking missed-coordination events

**CM-1 anti-position bias**: testato ordine Opt3→Opt4 vs Opt4→Opt3, verdetto cambiava con ordine → entrambi unstable in isolamento. Opt 1.5 emerge stabile da primitivi.

## Decisione

**codemasterdd evolve da policy-hub + osservatore → policy-hub + read-active aggregator + proactive contributor**.

Boundary cross-repo cross-repo **PRESERVED**: governance interna autonoma di Game / Godot-v2 / Dafne / vault / AA01 invariata. Synesthesia dormant invariato.

Cambio è del **ruolo codemasterdd**, NON dei repo monitored. Nessun ADR amendment cross-repo richiesto.

## Architecture

```
                              ┌─────────────────────────┐
                              │   codemasterdd          │
                              │   (policy-hub +         │
                              │    read-active +        │
                              │    proactive contrib)   │
                              └──────────┬──────────────┘
                                         │
                ┌────────────────────────┼────────────────────────┐
                │                        │                        │
                ▼                        ▼                        ▼
        [Read-active layer]    [Write-via-PR layer]    [Escalation gates]
                │                        │                        │
                ▼                        ▼                        ▼
    ┌───────────────────┐    ┌───────────────────┐    ┌──────────────────┐
    │ Flask aggregator  │    │ PR drafting       │    │ Gate A (Opt 3)   │
    │ apps/dogfood-ui/  │    │ via Aider/Claude  │    │ Gate B (Opt 4)   │
    │ +sqlite cache     │    │ on whitelist      │    │ Gate C enhanced  │
    └───────────────────┘    └───────────────────┘    └──────────────────┘
                │                        │                        │
                ▼                        ▼                        ▼
        [6 sources read]         [3 repos PR + 1 L-012] [tracking logs]
        Game / Godot / Dafne     Game / Godot / Dafne   logs/escalation-
        AA01 / vault / synes     + vault via L-012      gates-YYYY-MM.md
        (read-only all)          (AA01 = filesystem-
                                  direct NON-git)
                                 (Synesthesia skipped)
```

## Components

### Component 1 — Dashboard live aggregator

**Scope**: Flask extension di `apps/dogfood-ui/` (riuso ADR-0017 Accepted infrastructure).

**P1.5 prerequisite acknowledged**: dogfood-ui è **scaffold opt-in (DOWN)** in STATUS_MULTI_REPO.md current state. Pre-Component 1 build serve **promote dogfood-ui da scaffold opt-in a always-on** (system service / scheduled task), ALTRIMENTI alternative path: **build Component 1 come standalone Flask app `apps/cross-repo-dashboard/`** per evitare coupling con app unmaintained. Decisione (alternative A vs B) in writing-plans phase. Effort estimate aggiornato sotto.

**Source pull** (5min cron + manual trigger):
- gh API: PR open / issue / commit recent per **5 git repo** (Game / Godot-v2 / Dafne / vault / Synesthesia — read-only). AA01 NON-git: lettura via filesystem `inbox/` + `workspace/` + `archive/INDEX.md` + `learnings/` direct.
- Healthcheck endpoints: Flask dogfood-ui `:8080/api/health` (port verified app.py:9) + Dafne `:5000/health` + Ollama `:11434/api/tags`
- Git log local: HEAD + divergence vs origin/main per 5 git repo (AA01 excluded)
- Memory indexes: codemasterdd-only MEMORY.md auto-memory (`C:\Users\edusc\.claude\projects\C--dev-codemasterdd-ai-station\memory\` — NO altro repo ha auto-memory equivalente) + AA01 `archive/INDEX.md`
- Doc snapshots: STATUS_MULTI_REPO.md + COMPACT_CONTEXT.md last update timestamp

**gh API rate budget** (P1.3 fix, 6 sources × cron 5min):
- Authenticated quota: 5000 req/hr
- Naive estimate: 5 repos × 4 endpoints (PR list / issue list / commit recent / healthcheck) × 12 cron/hr = 240 req/hr baseline (~5% quota)
- Pagination policy: **max-1-page deep** (per-page=30 default, no full-history walk). Game-Godot-v2 ha 249+ PR mergeati ma solo `state=open` interrogato, NON history walk.
- Cache key strategy: `<repo>:<endpoint>:<page>` SQLite key, TTL 5min gh API + 1min local healthcheck
- Degraded mode: se quota >70% consumed → drop source priority: (1) Synesthesia (dormant), (2) full commit history detail, (3) issue list. PR list + HEAD divergence sempre top-priority.

**Cache layer**: SQLite-backed (riuso `dogfood.sqlite` file), nuova tabella `cross_repo_state` (key, value JSON, fetched_at, ttl_sec). TTL 5min per gh API + 1min per local git/healthcheck.

**View**:
- Summary page `/cross-repo`: 6 source card layout (5 git repo: Game / Godot-v2 / Dafne / vault / Synesthesia + 1 NON-git: AA01) con (PR open count [N/A AA01] / HEAD short [N/A AA01] / divergence ↑↓ [N/A AA01] / last activity timestamp / hook chain status / privacy class / dormant flag se applicable / non-git flag AA01)
- Drill-down `/cross-repo/<source>`: detail per source — git repo: last 10 commit / PR list / open decisions / health endpoints status. AA01: archive INDEX summary / inbox count / workspace active count / lessons cumulative count.
- Stale flag visivo se source last-update >72h

**Endpoint API**: `/api/cross-repo/state` returns JSON dump (per integration futura es. claude-mem worker).

**Implementation effort**: ~2 settimane (1 design SQL schema + Flask routes; 1 build + smoke test)

### Component 2 — Proactive contributor channel

**Scope**: write-via-PR pattern L-012 (vault sibling-peer auth) **esteso** a **3 git repo** (Game / Godot-v2 / Dafne) + 1 sibling-peer (vault via L-012 per-task auth). **AA01 ESCLUSO** (P0.2 harsh-review): NON-git workspace (`C:/Users/edusc/aa01/` senza `.git`), PR pattern fundamentally inapplicable. Alternative contribution channel AA01 = **filesystem-direct via lesson promotion + inbox capture lifecycle** (workflow esistente AA01 mantained, codemasterdd NON scrive direct su AA01 — Eduardo media via personal workflow).

**Workflow**:
1. codemasterdd identifica cross-repo issue durante uso normale (vedi tipi sotto)
2. Apre PR su repo target con body descrittivo (issue + proposed change + reference codemasterdd ADR/policy)
3. Governance interna repo decide accept / reject / amend via standard review
4. Outcome tracking in `logs/cross-repo-pr-YYYY-MM.md` (gitignored)

**Tipi PR cross-repo** (definizioni esplicite):
- **policy-alignment**: codemasterdd ADR Accepted / convention CLAUDE.md changes che impatta repo target (es. encoding policy ADR-0021 propagation, hook chain pattern update)
- **ADR-cross-ref**: nuovo ADR codemasterdd cita repo target ma quel repo ha CLAUDE.md/AGENTS.md proprio non aggiornato (es. addendum ADR-0024 Vue3 archive timeline propagation a Game)
- **drift-fix**: discovery state diverge tra codemasterdd memory / STATUS / doc e reality del repo target (es. hypothetical: vault `Extras/config/llm-routing.json` hardcoded IP `.121` mentre reality post-DHCP reservation è `.10` → drift-fix PR a vault. Esempio reale già eseguito via L-012 pattern 2026-05-13 notte). **NOTA**: il caso ADR-0027 / Ryzen PR #69 narrative drift era correzione INTERNA codemasterdd memory, NON cross-repo PR — escluso da questa categoria (P2.3 fix).
- **docs**: typo / link fix / cross-reference broken
- **governance-suggestion**: pattern noto codemasterdd applicable ma non yet adopted da repo target (es. cognitive protocol P1 Refresh-verify proposal). **Soft-suggestion only**, governance interna repo decide.

**Privacy guard rail**: Component 2 usa wrapper Aider esistenti (cloud free privacy-whitelisted o local tier 1-2 sovereign). Drafting PR via cloud wrapper su repo non-whitelisted BLOCKED automaticamente (es. Synesthesia controllers/ sovereign-only). Component 2 NON tocca Synesthesia in fase iniziale (dormant + privacy mixed) — Synesthesia rientra solo post reactivation esame UniUPO + privacy class re-evaluation.

**NO direct push**: write boundary cross-repo PRESERVED via PR review obbligatorio.

**Tracking template** (`logs/cross-repo-pr-2026-05.md`):
```
| Date | Repo target | PR # | Type | Outcome | Effort | Notes |
|------|-------------|------|------|---------|--------|-------|
```

Type: policy-alignment / ADR-cross-ref / drift-fix / docs / governance-suggestion.
Outcome: accepted / rejected / amended / pending.

**Implementation effort**: ~3gg (workflow doc + tracking template + first 3 PR empirici)

### Component 3 — Strategic escalation gates

Criteri **pre-definiti** per evoluzione paradigm SE failure trigger empirico emerge.

| Gate | Trigger condition | Empirical measure | Escalation path |
|------|-------------------|-------------------|-----------------|
| A | >2 missed-coordination events / settimana × 4 settimane consecutive | counter `logs/escalation-gates-YYYY-MM.md` field `missed_coord_weekly` | Re-evaluate Opt 3 write-direct via ADR amendment cross-repo |
| B | repo count ≥7 OR client production work attivo | STATUS_MULTI_REPO.md count + JOURNAL entries client work | Re-evaluate Opt 4 mesh-bus design (Dafne extension cross-repo) |
| C | Eduardo bandwidth coordinator <50% available (es. lavoro full-time esterno) | qualitative self-report mensile | Opt 1.5 enhanced via Dafne specialist routing automatic |

**Definition "missed-coordination event"**:
- Eduardo o agent in sessione ha dovuto fare grep manuale cross-repo >3 location per stato
- Cross-repo policy drift discovered DOPO causing rework (>30min)
- Two-way communication needed cross-repo per decisione singola che ha richiesto >2 round trip

**Tracking template** (`logs/escalation-gates-2026-MM.md`):
```
| Week start | Missed-coord events | Repo count | Bandwidth qualitative | Gate triggered? |
|------------|---------------------|------------|----------------------|-----------------|
```

**Implementation effort**: ~1gg (criteri ADR-like doc + tracking template)

## Data flow

```
[gh API 5 git repo]──────────────────────────┐
[healthcheck Flask:8080/api/health]          │
[healthcheck Dafne:5000/health]              │
[healthcheck Ollama:11434/api/tags] ─────────┼──> [Flask aggregator] ──> [SQLite cache] ──> [HTML /cross-repo view]
[git log local 5 git repo]                   │     (apps/dogfood-ui      (dogfood.sqlite          │
[codemasterdd MEMORY.md auto-memory]         │      OR new app)           cross_repo_state)       │
[AA01 filesystem direct: inbox+workspace+    │                                                    │
       archive/INDEX.md+learnings/]          │                                                    └──> [JSON API /api/cross-repo/state]
[STATUS_MULTI_REPO.md timestamp]             │
[COMPACT_CONTEXT.md timestamp] ──────────────┘
```

Nota: MEMORY.md è user-local codemasterdd-only (`C:\Users\edusc\.claude\projects\C--dev-codemasterdd-ai-station\memory\`). Altri repo non hanno equivalente. AA01 = filesystem-direct read (non gh API, è NON-git).

Refresh policy: cron 5min + manual `Refresh` button. Source con last-update >72h flagged visually.

## Error handling

- **gh API rate limit (HTTP 403/429)**: retry exp.backoff + jitter, max 3 attempts; fallback cache 24h con "stale" badge
- **Repo unreachable (git fetch fail)**: degraded display + alert banner "unable to fetch <repo>"
- **Healthcheck endpoint down**: badge "stale" su drill-down + last-success timestamp
- **Memory file stale (>72h since last update)**: warning flag amber, Protocol 1 Refresh-verify reminder banner
- **Privacy violation attempt** (Component 2 drafting PR su repo non-whitelisted): blocked at wrapper level + logged in `logs/privacy-violations-YYYY-MM.md`

## Testing

**Component 1 dashboard**:
- Smoke pattern esistente `apps/dogfood-ui/test_*` riuso
- New tests: `test_cross_repo_aggregator.py` (3 cases: fresh fetch / cache hit / stale flag)
- Manual smoke per source × 2 settimane → automated weekly post-stabilization

**Component 2 PR pattern**:
- Pre-deploy: dry-run draft PR su 1 repo (Game o AA01) con explicit `--dry-run` flag
- First 3 PR reali: explicit Eduardo confirmation each (CLASSE D scelta-valore esterno repo)
- Post-3rd PR: outcome tracking automatico, pattern audit cumulative monthly

**Component 3 escalation gates**:
- Tracking template smoke: 1 settimana empirica, verify counter increments + zero double-count

## Integration con sistema esistente

| Sub-system | Integration |
|------------|-------------|
| 6 cognitive protocols | P1 Refresh-verify **rinforzato** (dashboard pre-action invece di grep cross-repo). P4 AA01 workspace invariato. P5/P6 invariati. |
| 18 sub-agent | `repo-health-auditor` sub-agent (markdown prompt, NON callable backend service) genera STATUS_MULTI_REPO.md **on-demand** quando Eduardo invoca; dashboard legge file timestamp + parsa sezioni. NO live coupling Flask -> sub-agent. (P2.2 fix) |
| ADR-0017 stack | Dashboard è **extension** di `apps/dogfood-ui/` (Flask+SQLite). NO new container. Langfuse trace opzionale per observability JSON API. |
| Privacy guard rail H8 ADR-0023 | 4 wrapper cloud invariati. Component 2 PR drafting rispetta whitelist runtime check. |
| Hook chain 5-layer | Invariata. Component 2 PR passa attraverso commit-msg + pre-commit + commit-guard standard. |
| Plugin ecosystem | claude-mem auto cross-session memory. superpowers brainstorming/writing-plans applicato per questo spec (case study Protocol 6 + 3). |
| MODEL_ROUTING | Component 2 PR drafting tier routing invariato (Aider cosmetic/refactor/cloud + OpenCode multi-step) |

## Effort + timeline (P1.2 fix: decoupled from pre-Max deadline for Component 2)

| Item | Effort revised | Timing | Constraint / Dependency |
|------|----------------|--------|------------------------|
| Component 1 dashboard (alternative A: extension dogfood-ui) | ~3 settimane (~1 promote dogfood-ui to always-on + 1 design + 1 build) | SPRINT_02 T1-T2 amended scope, post-Max | dogfood-ui currently DOWN, needs promotion |
| Component 1 dashboard (alternative B: standalone app) | ~2.5 settimane (~0.5 scaffold + 1 design + 1 build) | SPRINT_02 T1-T2 amended scope, post-Max | NO coupling con dogfood-ui unmaintained |
| Component 2 PR workflow + tracking template | ~1gg (workflow doc + tracking template + dry-run protocol) | Pre-Max (6gg residui) ✅ | Small scope, doc-only |
| Component 2 "first 3 PR accepted by external governance" | ~variable | **DEFERRED a SPRINT_02** (external governance approval time NON-controllable) | Gate empirico: ≥1 PR accepted by external governance prima di claim pattern validated |
| Component 3 escalation gates | ~1gg (criteri + template + smoke test 1 settimana) | Pre-Max ✅ | Small scope |

**Critical path pre-Max revised**: Component 2 workflow-doc-only + Component 3 buildable pre-Max (~2gg). Component 1 + Component 2 empirical PR validation in SPRINT_02 (20/05+).

**P1.2 explicit acknowledgement**: "first 3 PR empirici" pre-Max claim originale era aspirational. External governance (Game-Godot-v2 215+ PR auto-gestiti governance interna autosufficiente) ha decision time non-controllable. New gate: pattern validated SOLO post ≥1 PR accepted by external governance in SPRINT_02, NOT pre-Max.

## YAGNI exclusions (cosa NON include) — P2.1 fix: rilevanti, no obvious

- ❌ NO write-direct cross-repo (Opt 3 deferred via Gate A)
- ❌ NO event/message bus (Opt 4 deferred via Gate B)
- ❌ NO real-time websocket (cron 5min sufficient per use case attuale)
- ❌ NO ML / anomaly detection (premature, no failure pattern yet)
- ❌ NO authentication / authorization (single-user trust, sovereign workstation. Out-of-scope reverse proxy auth via Tailscale o equivalent se mai cross-LAN exposed)
- ❌ NO audit log retention policy (logs/ gitignored cresce unbounded, accettabile per ora — review se >1GB single log)
- ❌ NO data export/import format stability (SQLite schema = internal, no contract esterno)
- ❌ NO graceful SQLite schema migration framework (single dev: ALTER TABLE su demand, no migration tool come Alembic. Accettabile sotto 5 schema changes/anno)
- ❌ NO notification push (cron + manual review sufficient)

## Reversibility analysis (P1.4 fix: graduated, no hand-wave)

| Component | Reversibility | Effort to remove |
|-----------|---------------|------------------|
| Component 1 dashboard | 100% reversible | ~30min (remove Flask route + drop SQLite table cross_repo_state) |
| Component 2 PR pattern (≤2 PR accepted by external governance) | **Full reversibility** | ~10min stop drafting + governance interna doesn't yet cite codemasterdd patterns |
| Component 2 PR pattern (3-4 PR accepted) | **Graduated reversibility — soft lock-in begin** | ~1-2h: stop drafting + audit target repo CLAUDE.md/AGENTS.md per cross-references created + coordinated cleanup PR su target repo per rimuovere refs |
| Component 2 PR pattern (≥5 PR accepted with reference adoption) | **Soft lock-in confirmed** | Days+: ADR amendment cross-repo per ritirare codemasterdd pattern adoption from target repo governance. Comparable cost a Opt 3 ADR amendment (NOT 100% reversible) |
| Component 3 escalation gates | 100% reversible | ~5min (delete tracking files, no decision impact pending) |

**Gate D — Reversibility threshold** (P1.4 fix):
- Trigger: ≥5 PR cumulative accepted by external governance WITH cross-reference adoption (target repo CLAUDE.md/AGENTS.md cita codemasterdd pattern)
- Action: PAUSE Component 2 + audit lock-in scope cross-repo + ADR formale per ritiro coordinato OR continuation explicit

**Asymmetric advantage vs Opt 3/Opt 4 (revised)**:
- Opt 3 richiederebbe ADR amendment cross-repo upfront (high cost day 1, irreversibile soft after governance internal consent obtained)
- Opt 4 richiederebbe Dafne expansion (high cost month 1, irreversibile mid-term)
- Opt 1.5 ha **graduated cost curve**: cheap day 1 (≤2 PR), graduated growth (3-4 PR), eventual Gate D trigger (≥5 PR)
- **Honest comparison**: Opt 1.5 lock-in cost LAGGED vs Opt 3 UPFRONT, NOT absent. Per ≤2 PR accepted Opt 1.5 wins. Per ≥5 PR accepted converge toward Opt 3 cost.

## Open questions

1. **Component 1 source priority**: se gh API rate limit hit, quale source degrada per primo? (Proposta default: synesthesia drop first dato dormant)
2. **Component 2 PR template**: standardizzare body PR cross-repo con conventional sections (issue / proposed change / ADR ref / privacy class)?
3. **Component 3 missed-coord events**: chi marca un evento? Eduardo manual? Agent auto-detect (es. grep cross-repo count >3 location)?

Aperte per writing-plans phase. Non bloccano spec approval.

## Next steps

1. ✅ Brainstorming skill applied + design approved Eduardo "Approve as-is"
2. → (this) spec doc committed to `docs/superpowers/specs/`
3. → spec self-review (inline)
4. → Eduardo reviews spec
5. → invoke `superpowers:writing-plans` skill per implementation plan dettagliato

## Harsh review findings integrated (Protocol 5 ADR-0026 addendum)

Harsh-reviewer subagent invoked 2026-05-13 post-Draft. Verdict: **REWORK** (confidence 80%). Findings integrated questa revisione:

| Priority | Finding ID | Status | Where fixed in spec |
|----------|------------|--------|---------------------|
| P0 | P0.1 ADR-0024 mis-cite hallucinated | FIXED | Header cross-ref + References section (rimosso ADR-0024 cross-repo dep claim, era hallucinated. ADR-0024 reale = Vue3 archive Godot timeline) |
| P0 | P0.2 AA01 NOT git, PR pattern inapplicable | FIXED | Component 2 scope ridotto a 3 git repo + vault L-012 + AA01 filesystem-direct alternative channel |
| P0 | P0.3 Methodology meta-recursion self-validating | FIXED | New "Methodology bias disclosure" section + confidence downgraded 75% -> 65% + falsifier explicit |
| P1 | P1.1 Visibility gap concreto not documented | PENDING Eduardo | New "Empirical trigger evidence" section richiede Eduardo input pre-Accepted |
| P1 | P1.2 Effort 6gg pre-Max unrealistic | FIXED | Component 2 decoupled da pre-Max deadline, "first 3 PR" → SPRINT_02 gated |
| P1 | P1.3 gh API rate budget not computed | FIXED | New "gh API rate budget" table + cache key strategy + max-1-page deep policy |
| P1 | P1.4 Reversibility 100% Component 2 hand-wave | FIXED | New "graduated reversibility" table + Gate D trigger ≥5 PR threshold |
| P1 | P1.5 dogfood-ui scaffold opt-in DOWN | FIXED | P1.5 prerequisite acknowledged + alternative A (promote dogfood-ui always-on) vs B (standalone app) decision in writing-plans |
| P1 | P1.6 Port inconsistency 5050 vs 8080 | FIXED | All port references aggiornati a 8080 (verified app.py:9) |
| P2 | P2.1 YAGNI list inflated | FIXED | Replaced "NO mobile UI" / "NO multi-tenant" con NO auth / NO audit retention / NO data export / NO schema migration framework |
| P2 | P2.2 repo-health-auditor "backend" misleading | FIXED | Integration table clarifies sub-agent generates STATUS_MULTI_REPO.md on-demand, NO live coupling |
| P2 | P2.3 Drift-fix example Ryzen PR #69 internal not cross-repo | FIXED | Replaced example con hypothetical vault llm-routing.json drift-fix |

**Net**: 3/3 P0 fixed + 5/6 P1 fixed (P1.1 PENDING Eduardo input) + 3/3 P2 fixed. Confidence post-rework: 70% (up da 65% post P0+P1+P2 integration MA still below original aspirational 75%).

## References

- Brainstorming skill: `superpowers:brainstorming` (Protocol 6 ADR-0026 addendum 2026-05-13)
- Archon protocol: `~/aa01/archon/system/ARCHON_v2_SYSTEM.md` (Protocol 3 ADR-0026)
- Harsh-reviewer skill: `superpowers:requesting-code-review` (Protocol 5 ADR-0026 addendum 2026-05-13)
- ADR-0017: stack scaffolding (apps/dogfood-ui foundation)
- ADR-0021: multi-client pattern (boundary preservation)
- ADR-0023: privacy guard rail H8 (whitelist runtime check)
- ADR-0024: Vue3 archive + Godot v2 canonical timeline (CORRECTLY cited post P0.1 fix; NOT cross-repo dependency tracking)
- ADR-0026: cognitive workflow protocols (P1-P6)
- ADR-0027: cross-PC clone architecture (Ryzen vs Lenovo lineage)
- L-002: Hyperspace audit cycle anti-pattern
- L-012: vault sibling-peer write under explicit auth (Component 2 pattern source)
- L-016: cognitive protocols measurement anti-aspirational (Component 3 measurement discipline + P0.3 meta-recursion warning source)
