# Design spec — Component 1 dashboard (PRE-DESIGN gated Gate E)

**Date**: 2026-05-13 sera-tardi-ultra-3
**Status**: PRE-DESIGN (anticipatory, gated Gate E threshold ≥5 events/wk × 4 weeks)
**Cross-ref**: Spec V3 cross-repo orchestrator (PR #87 merged commit `3e580e2`) + ADR-0017 stack scaffolding + ADR-0026 cognitive protocols
**Confidence**: **40%** (lower-than-Component-2+3 honest: anticipatory intervention pre-empirical-validation)

## Honest disclosure (anti-pattern acknowledgment)

**Eduardo CLASSE D scelta-valore explicit**: chose to pre-design Component 1 despite Archon ciclo 2 self-falsification of trigger #1 (visibility gap unverified). This violates L-2026-05-016 anti-aspirational principle.

**Risks accepted**:
1. Gate E may falsify Component 1 entirely (<2 events/wk threshold) → 1-2h pre-design effort lost
2. Gate E may BUILD MINIMAL scope (2-<5 events/wk) → design oversized for needs, partial rework
3. Gate E may BUILD full (≥5 events/wk) → pre-design valuable, saves SPRINT_02 effort 30-50%

**Counter-balance rationale Eduardo**:
- Pre-Max 5gg residui = bandwidth available NOW
- Opus 4.7 quality currently available, post-Max sovereign tier capability lower
- IF Gate E PASS, design ready saves cognitive overhead post-Max

**Confidence trail Component 1 pre-design** (separate from Component 2+3 trail):
- Component 2+3 final confidence: 65% (post all rounds review)
- Component 1 pre-design confidence: 40% (anticipatory + gate-dependent + alternative A vs B unresolved)

## Decision context

Component 1 = read-active dashboard aggregator. Spec V3 cross-repo orchestrator (Opt 1.5 REDUCED) ha 2 alternative design paths:

| Alternative | Approach | Effort | Risk |
|-------------|----------|--------|------|
| A | Extension `apps/dogfood-ui/` Flask (riuso ADR-0017 infrastructure) | ~3 settimane (1 promote dogfood-ui always-on + 1 design + 1 build) | dogfood-ui scaffold opt-in DOWN currently — needs promotion + maintenance |
| B | Standalone Flask app `apps/cross-repo-dashboard/` | ~2.5 settimane (0.5 scaffold + 1 design + 1 build) | NO coupling unmaintained app, MA new container/process to manage |

Decision Alternative A vs B → **DEFERRED to Gate E result**. Pre-design copre 80% comune (data model + sources + view templates); 20% alternative-specific (deployment + Flask coupling).

## Architecture (shared A+B)

```
[gh API 5 git repo] ─────────────────────┐
[healthcheck 4 endpoints]                │
[git log local 5 repo]                   │
[codemasterdd MEMORY.md] ────────────────┼──> [Flask aggregator] ──> [SQLite cache] ──> [/cross-repo HTML view]
[AA01 filesystem direct]                 │     (A: dogfood-ui ext   (dogfood.sqlite       │
[STATUS_MULTI_REPO.md timestamp]         │     OR B: standalone)     OR new DB file)      │
[COMPACT_CONTEXT.md timestamp] ──────────┘                                                 └──> [/api/cross-repo/state JSON]
```

Alternative A: shares `dogfood.sqlite` (new table `cross_repo_state`) + Flask routes added to `apps/dogfood-ui/app.py` (currently 322 lines)
Alternative B: new `apps/cross-repo-dashboard/app.py` + new `apps/cross-repo-dashboard/data/cross_repo.sqlite`

## Data model SQLite (shared)

```sql
CREATE TABLE cross_repo_state (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  repo_name TEXT NOT NULL,                 -- Game / Game-Godot-v2 / Dafne / vault / Synesthesia / AA01
  source_type TEXT NOT NULL,               -- gh-api / healthcheck / git-log-local / memory / filesystem
  endpoint TEXT NOT NULL,                  -- specific endpoint per source_type (es. 'pulls?state=open')
  payload_json TEXT NOT NULL,              -- response cached, JSON serialized
  fetched_at TEXT NOT NULL,                -- ISO 8601 timestamp
  ttl_sec INTEGER NOT NULL,                -- cache TTL (300 for gh API, 60 for local)
  is_stale_flag INTEGER DEFAULT 0,         -- 1 if fetched_at + ttl_sec exceeded
  fetch_error TEXT                         -- non-null if last fetch failed
);

CREATE INDEX idx_repo_source ON cross_repo_state(repo_name, source_type);
CREATE INDEX idx_fetched_at ON cross_repo_state(fetched_at);
```

## Source aggregation budget

Per `P1.3 fix` spec V3 (PR #87): gh API rate budget verified.

| Source | Endpoint | Cron | Req/hr | Cache TTL |
|--------|----------|------|--------|-----------|
| gh API 5 git repo × PR list (state=open, page 1) | `/repos/:owner/:repo/pulls?state=open&per_page=30` | 5min | 60 | 300s |
| gh API 5 git repo × commit recent | `/repos/:owner/:repo/commits?per_page=10` | 5min | 60 | 300s |
| gh API 5 git repo × issue open | `/repos/:owner/:repo/issues?state=open&per_page=30` | 5min | 60 | 300s |
| Healthcheck Flask dogfood-ui (alt A) OR new app (alt B) | `:8080/api/health` (alt A) / `:8081/api/health` (alt B) | 1min | - | 60s |
| Healthcheck Dafne | `:5000/health` | 1min | - | 60s |
| Healthcheck Ollama | `:11434/api/tags` | 1min | - | 60s |
| Git log local 5 repo | `git log -1 --format=...` | 5min | - | 60s |
| Filesystem AA01 | `ls inbox/ + workspace/ + cat archive/INDEX.md` | 5min | - | 60s |
| Memory indexes | `cat MEMORY.md` | 30min | - | 1800s |
| Doc snapshots | `stat STATUS_MULTI_REPO.md + COMPACT_CONTEXT.md` | 5min | - | 300s |

**Total gh API: 180 req/hr authenticated** (well within 5000/hr quota). Synesthesia drop-first if budget >70%.

## View design (HTML + JSON)

### Summary page `/cross-repo`

Card layout 6 source. Each card:
- Header: repo name + privacy class badge (sovereign-only / mixed / cloud-OK) + dormant flag (Synesthesia) + non-git flag (AA01)
- Metrics: PR open count / HEAD short / divergence ↑↓ / last commit date+author
- Status: hook chain status + last source fetch + stale flag
- Action: link to drill-down `/cross-repo/<repo>`

Sort default: most recent activity desc. Filter: privacy class / has open PR / stale flag.

### Drill-down `/cross-repo/<repo>`

Per-repo detail:
- Last 10 commit (oneline + author + date)
- PR list (open) with title + author + state
- Open decisions (parse `OPEN_DECISIONS.md` if exists)
- Health endpoints status
- Source fetch log last 10

### JSON API `/api/cross-repo/state`

```json
{
  "timestamp": "2026-05-20T09:00:00Z",
  "sources": {
    "Game": { "pr_open_count": 3, "head_short": "1abcd23", "divergence_up": 0, "divergence_down": 5, "last_commit_date": "2026-05-18", "last_commit_author": "Eduardo Scarpelli", "fetch_status": "ok", "is_stale": false },
    "Game-Godot-v2": { ... },
    "Dafne": { ... },
    "vault": { ... },
    "Synesthesia": { "pr_open_count": 0, "is_dormant": true, ... },
    "AA01": { "is_non_git": true, "inbox_count": 0, "workspace_active": 0, "archive_count": 15, "lessons_count": 16, ... }
  }
}
```

## Error handling

Tier 1 (degraded mode, no abort):
- gh API rate limit (HTTP 403/429): retry exp.backoff jitter max 3 attempts → fallback cache 24h with stale badge
- Repo unreachable (git fetch fail): degraded display + alert banner "unable to fetch <repo>"
- Healthcheck endpoint down: badge "stale" su drill-down + last-success timestamp
- Memory file stale (>72h): warning flag amber, Protocol 1 reminder banner

Tier 2 (hard fail, abort):
- SQLite cache DB unwritable: log + return 503 (degraded mode incompatible)
- Privacy violation attempt (cloud LLM access to Synesthesia controllers/): blocked + log

## Testing

Pattern Plan from spec V3 carryover + add:
- Unit test `test_cross_repo_aggregator.py` (3 cases: fresh fetch / cache hit / stale flag)
- Integration test `test_dashboard_routes.py` (route 200 + JSON schema validation)
- Smoke manual 2 weeks → automated weekly cron

## Decision matrix Alternative A vs B (post-Gate-E)

| Criterion | Alternative A (extension dogfood-ui) | Alternative B (standalone) |
|-----------|-------------------------------------|---------------------------|
| Effort total | ~3 settimane | ~2.5 settimane |
| Coupling risk | High (depends on dogfood-ui maintenance) | Low (independent app) |
| Container count | 1 (riuso) | 2 (new container) |
| Port conflicts | None (8080 already used by dogfood-ui) | New port (8081 proposed) |
| Maintenance overhead | Shared with dogfood-ui (which is scaffold opt-in DOWN) | Independent lifecycle |
| Pre-promotion dogfood-ui? | YES required | NO required |
| Future Component 2/3 integration | Easier (shared infrastructure) | Requires bridge layer |

**Decision deferred to Gate E PASS event + Eduardo authorization**. Pre-design covers shared 80%; alternative-specific 20% scaffolding post-Gate-E.

## Reversibility analysis (Component 1 only)

| Outcome Gate E | Component 1 action | Reversibility |
|----------------|--------------------|---------------|
| ≥5 events/wk (BUILD full) | Alternative A o B implementation | Full revert ~30min remove route + drop table |
| 2-<5 events/wk (BUILD MINIMAL) | Alternative A solo, view layout reduced | Full revert ~30min |
| <2 events/wk (NOT BUILT) | Pre-design archived `docs/research/component-1-pre-design-archived.md` | N/A (never built, only paper exists) |

Pre-design itself = 100% reversible (delete spec file + commit message). Effort lost = 1-2h.

## Open questions (post-Gate-E)

1. **Alternative A vs B**: deferred per design matrix
2. **Authentication**: single-user trust assumed (codemasterdd LOCAL only). Should dashboard be reachable via Tailscale LAN (Lenovo + Ryzen)? Future P1.
3. **Frontend tech**: pure HTML+CSS+vanilla JS (consistente con dogfood-ui style) vs add lightweight framework (Vue/Alpine.js)? Default vanilla per simplicity.
4. **Realtime updates**: cron 5min sufficient OR WebSocket push needed? YAGNI cron default.

## YAGNI exclusions (Component 1 specific)

- ❌ NO multi-tenant (single Eduardo user)
- ❌ NO authentication (single-user trust, LOCAL only — Tailscale future P1 if needed)
- ❌ NO real-time WebSocket (cron 5min sufficient)
- ❌ NO ML anomaly detection (premature)
- ❌ NO mobile-responsive layout (workstation Lenovo + Ryzen desktops only)
- ❌ NO export/import format stability
- ❌ NO i18n (Italian Eduardo only)

## Gate E threshold-dependent next steps

**IF Gate E PASS ≥5 events/wk**:
1. Eduardo Alternative A vs B explicit decision (~5min)
2. Subagent-Driven implementation 11-15 tasks (~2-3 settimane elapsed)
3. PR + review + merge

**IF Gate E 2-<5 events/wk (MINIMAL)**:
1. Alternative A only (no decision needed)
2. Reduced view (summary page only, NO drill-down) + reduced source list (drop Synesthesia + AA01 filesystem)
3. ~1.5 settimane elapsed

**IF Gate E <2 events/wk (FALSIFIED)**:
1. Archive pre-design → `docs/research/component-1-pre-design-archived-2026-MM-DD.md`
2. Update STATUS_MULTI_REPO: trigger #1 empirically falsified
3. Close spec V3 follow-up

## References

- Spec V3 cross-repo orchestrator (PR #87 merged `3e580e2`)
- ADR-0017 stack scaffolding (apps/dogfood-ui foundation)
- ADR-0026 cognitive workflow protocols (P1-P6)
- L-2026-05-016 cognitive protocols measurement anti-aspirational (warning source: pre-design IS the anti-pattern Eduardo accepted explicitly)
- Component 3 escalation gates Gate E threshold definition
