# Design spec — Cross-repo orchestrator evolution (Opt 1.5)

**Date**: 2026-05-13
**Status**: Draft (post brainstorming skill + Archon 7-step)
**Cross-ref**: ADR-0021 (multi-client) + ADR-0024 (cross-repo dependency) + ADR-0026 (cognitive protocols) + L-012 (vault sibling-peer write under explicit auth)
**Methodology applied**: Protocol 6 brainstorming (superpowers skill) + Protocol 3 Archon 7-step First Principles (high-stakes architectural)
**Confidence**: 75% (post trigger acquisition, ECE-adjusted)

## Context

Eduardo richiesta 2026-05-13 sera-tardi: "siamo solidi come hub osservatore, non come orchestratore attivo. Facciamo il punto 1 [Re-design boundary cross-repo] per partire".

### Trigger acquisiti (3/4 selected via AskUserQuestion)

| Trigger | Selected | Implicazione |
|---------|----------|--------------|
| Visibility gap concreto | YES | Failure incident reale ultimi 30gg (grep manuale cross-repo). Action-required. |
| Post-Max anxiety | NO | NON è capability-anticipating fear. Esclude solution-looking-for-problem framing. |
| Coordination overhead percepito | YES | Eduardo single-bottleneck pain concreto. Pattern Eduardo media bidirezionale tutti i cross-repo flow. |
| Strategic alignment lungo termine | YES | Scaling 5→7-10 repo in 2-3 anni hypotetico. Forward-looking. |

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
        [6 repos read]           [4 repos PR + 1 L-012] [tracking logs]
        Game / Godot / Dafne     Game / Godot /         logs/escalation-
        AA01 / vault / synes     Dafne / AA01           gates-YYYY-MM.md
        (read-only all)          + vault via L-012
                                 (Synesthesia skipped)
```

## Components

### Component 1 — Dashboard live aggregator

**Scope**: Flask extension di `apps/dogfood-ui/` (riuso ADR-0017 Accepted infrastructure, NO new container).

**Source pull** (5min cron + manual trigger):
- gh API: PR open / issue / commit recent per **6 repo** (Game / Godot-v2 / Dafne / AA01 / vault / Synesthesia — all read-only)
- Healthcheck endpoints: Flask dogfood-ui `/api/health` + Dafne `:5000/health` + Ollama `:11434/api/tags`
- Git log local: HEAD + divergence vs origin/main per 6 repo
- Memory indexes: MEMORY.md cross-session + AA01 archive INDEX.md
- Doc snapshots: STATUS_MULTI_REPO.md + COMPACT_CONTEXT.md last update timestamp

**Cache layer**: SQLite-backed (riuso `dogfood.sqlite` file), nuova tabella `cross_repo_state` (key, value JSON, fetched_at, ttl_sec). TTL 5min per gh API + 1min per local git/healthcheck.

**View**:
- Summary page `/cross-repo`: 6 repo card layout (Game / Godot-v2 / Dafne / AA01 / vault / Synesthesia) con (PR open count / HEAD short / divergence ↑↓ / last commit author + date / hook chain status / privacy class / dormant flag se applicable)
- Drill-down `/cross-repo/<repo>`: detail per-repo (last 10 commit / PR list / open decisions / health endpoints status)
- Stale flag visivo se source last-update >72h

**Endpoint API**: `/api/cross-repo/state` returns JSON dump (per integration futura es. claude-mem worker).

**Implementation effort**: ~2 settimane (1 design SQL schema + Flask routes; 1 build + smoke test)

### Component 2 — Proactive contributor channel

**Scope**: write-via-PR pattern L-012 (vault sibling-peer auth) **esteso** a 4 repo (Game / Godot-v2 / Dafne / AA01).

**Workflow**:
1. codemasterdd identifica cross-repo issue durante uso normale (vedi tipi sotto)
2. Apre PR su repo target con body descrittivo (issue + proposed change + reference codemasterdd ADR/policy)
3. Governance interna repo decide accept / reject / amend via standard review
4. Outcome tracking in `logs/cross-repo-pr-YYYY-MM.md` (gitignored)

**Tipi PR cross-repo** (definizioni esplicite):
- **policy-alignment**: codemasterdd ADR Accepted / convention CLAUDE.md changes che impatta repo target (es. encoding policy ADR-0021 propagation, hook chain pattern update)
- **ADR-cross-ref**: nuovo ADR codemasterdd cita repo target ma quel repo ha CLAUDE.md/AGENTS.md proprio non aggiornato (es. ADR-0024 cross-repo dependency)
- **drift-fix**: discovery state diverge tra codemasterdd memory / STATUS / doc e reality del repo target (es. claim "Ryzen AHEAD" PR #69 narrative drift case study)
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
[gh API 6 repo]──────────────────────────────┐
[healthcheck Flask:5050]                     │
[healthcheck Dafne:5000]                     │
[healthcheck Ollama:11434] ──────────────────┼──> [Flask aggregator] ──> [SQLite cache] ──> [HTML /cross-repo view]
[git log local 6 repo]                       │     (apps/dogfood-ui)     (dogfood.sqlite)         │
[MEMORY.md indexes codemasterdd]             │                                                    │
[AA01 archive/INDEX.md]                      │                                                    └──> [JSON API /api/cross-repo/state]
[STATUS_MULTI_REPO.md timestamp]             │
[COMPACT_CONTEXT.md timestamp] ──────────────┘
```

Nota: MEMORY.md è specifico di codemasterdd (user-local `C:\Users\edusc\.claude\projects\C--dev-codemasterdd-ai-station\memory\`). Altri repo non hanno MEMORY.md auto-memory. Source "MEMORY.md indexes" si riferisce solo a codemasterdd.

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
| 18 sub-agent | `repo-health-auditor` agent definition esistente diventa **backend** per dashboard view aggregation. `dogfood-analyst` invariato. |
| ADR-0017 stack | Dashboard è **extension** di `apps/dogfood-ui/` (Flask+SQLite). NO new container. Langfuse trace opzionale per observability JSON API. |
| Privacy guard rail H8 ADR-0023 | 4 wrapper cloud invariati. Component 2 PR drafting rispetta whitelist runtime check. |
| Hook chain 5-layer | Invariata. Component 2 PR passa attraverso commit-msg + pre-commit + commit-guard standard. |
| Plugin ecosystem | claude-mem auto cross-session memory. superpowers brainstorming/writing-plans applicato per questo spec (case study Protocol 6 + 3). |
| MODEL_ROUTING | Component 2 PR drafting tier routing invariato (Aider cosmetic/refactor/cloud + OpenCode multi-step) |

## Effort + timeline

| Item | Effort | Timing | Constraint |
|------|--------|--------|------------|
| Component 1 dashboard | ~2 settimane (1 design + 1 build) | SPRINT_02 T1-T2 amended scope, post-Max | NO blocker, sovereign tier sufficient |
| Component 2 PR pattern | ~3gg (workflow + tracking + first 3 PR) | Pre-Max (6gg residui) ✅ | Small scope, doable now |
| Component 3 escalation gates | ~1gg (criteri + template) | Pre-Max ✅ | Small scope |

**Critical path pre-Max**: Component 2 + 3 buildable nei 6gg residui. Component 1 in SPRINT_02 (20/05+).

## YAGNI exclusions (cosa NON include)

- ❌ NO write-direct cross-repo (Opt 3 deferred via Gate A)
- ❌ NO event/message bus (Opt 4 deferred via Gate B)
- ❌ NO real-time websocket (cron 5min sufficient per use case attuale)
- ❌ NO ML / anomaly detection (premature, no failure pattern yet)
- ❌ NO multi-tenant (single Eduardo user)
- ❌ NO mobile UI (Eduardo workstation Lenovo + optionally Ryzen)
- ❌ NO notification push (cron + manual review sufficient)

## Reversibility analysis

| Component | Reversibility | Effort to remove |
|-----------|---------------|------------------|
| Component 1 dashboard | 100% reversible | ~30min (remove Flask route + drop SQLite table) |
| Component 2 PR pattern | 100% reversible | ~10min (stop drafting PR, governance interna assorbe pattern naturally) |
| Component 3 escalation gates | 100% reversible | ~5min (delete tracking files, no decision impact pending) |

**Asymmetric advantage vs Opt 3/Opt 4**: Opt 3 richiederebbe ADR amendment cross-repo (governance internal consent = irreversibile soft). Opt 4 richiederebbe Dafne expansion (mesi di setup, irreversibile mid-term).

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

## References

- Brainstorming skill: `superpowers:brainstorming` (Protocol 6 ADR-0026 addendum 2026-05-13)
- Archon protocol: `~/aa01/archon/system/ARCHON_v2_SYSTEM.md` (Protocol 3 ADR-0026)
- ADR-0017: stack scaffolding (apps/dogfood-ui foundation)
- ADR-0021: multi-client pattern (boundary preservation)
- ADR-0023: privacy guard rail H8 (whitelist runtime check)
- ADR-0024: cross-repo dependency tracking
- ADR-0026: cognitive workflow protocols (P1-P6)
- ADR-0027: cross-PC clone architecture (Ryzen vs Lenovo lineage)
- L-002: Hyperspace audit cycle anti-pattern
- L-012: vault sibling-peer write under explicit auth (Component 2 pattern source)
- L-016: cognitive protocols measurement anti-aspirational (Component 3 measurement discipline)
