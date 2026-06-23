# Design spec V4 — Component 1 cross-repo dashboard MVP

> **Status (2026-06-23):** superseded -- shipped v0.2->v0.3->dogfood-ui #196, then dogfood-ui decommissioned (OD-009 / ADR-0030)

**Date**: 2026-05-14
**Status**: BUILD AUTHORIZED (trigger #1 verified empirical, methodology re-evaluation post Eduardo daily-use confirmation)
**Cross-ref**: Spec V3 cross-repo orchestrator (PR #87) + archived pre-design (PR #88, `docs/research/component-1-design-options-archived-2026-05-13.md`)
**Confidence**: 70% (mid-high: trigger verified, scope compressed pre-Max, MVP-first)

## Critical methodology re-evaluation (HONEST)

**Previous conclusions (now invalidated)**:
- PR #87 Archon ciclo 2: "trigger #1 unverified, Eduardo self-falsification"
- PR #88 harsh-reviewer P0.1: "pre-design META anti-pattern L-016"

**Why previous was wrong**:
- Both assumed `Eduardo couldn't articulate session 13/5 late = no incident exists`
- Reality 14/5: Eduardo articulates concrete daily-use case: *"userei ogni giorno anche ora"*
- Distinguishing criterion missing: **session-decision-fatigue articulation ≠ permanent trigger absence**

**Lesson candidate L-2026-05-019** (in promotion):
- Pattern: trigger validation deve avere window > single-session decision fatigue
- Anti-pattern: "user-couldn't-articulate-in-session" treated as "trigger-unverified-permanently"
- Mitigation: post-decision check-in window (24-48h) per ratify methodology conclusion before locking-in

## Trigger #1 evidence (NEW empirical, 2026-05-14)

Eduardo statement (verbatim): *"ma io ho bisogno della component 1 la userei ogni giorno anzi anche ora"*

Interpretation:
- "ogni giorno" = daily usage frequency claim
- "anche ora" = pain felt RIGHT NOW (pre-Max, with Opus available)
- Implies: current manual grep + STATUS_MULTI_REPO refresh + multiple `gh pr list` invocations = insufficient

**Trigger #1 status**: VERIFIED empirical (Eduardo self-report concrete + daily frequency + immediate pain).

ROI recalculation:
- Original estimate: ~1/wk usage → break-even 20-33 anni → NEGATIVE
- Updated estimate: ~5/wk usage (daily) → 50min/wk × 50 weeks = 42h/anno saved
- Build effort MVP 2-3gg = ~20-30h
- Break-even: <1 anno → POSITIVE

## MVP scope (compressed 5gg pre-Max window)

### Build target
- **Alt B standalone** (`apps/cross-repo-dashboard/`) — NO coupling con dogfood-ui scaffold opt-in DOWN
- **Port 8081** — avoid 8080 dogfood-ui
- **Flask + Jinja2** — minimal stack, Python 3.12 (installed)
- **In-memory cache dict** — NO SQLite MVP (defer to v1.1 if needed)
- **No auth** — single-user trust, localhost only

### Sources MVP (minimal, expand post-MVP)
| Source | MVP | v1.1+ |
|--------|-----|-------|
| gh API PR list 5 git repos (state=open) | ✅ MVP | refresh |
| gh API commits recent 5 repos | ✅ MVP | refresh |
| gh API issues open 5 repos | ⏸️ v1.1 | post-MVP |
| Healthcheck endpoints (Flask:8080/Dafne:5000/Ollama:11434) | ⏸️ v1.1 | post-MVP |
| Git log local divergence vs origin/main | ⏸️ v1.1 | post-MVP |
| Memory MEMORY.md (codemasterdd) | ⏸️ v1.2 | post-MVP |
| AA01 filesystem (inbox/workspace/archive) | ⏸️ v1.2 | post-MVP |
| STATUS_MULTI_REPO.md timestamp | ⏸️ v1.2 | post-MVP |

**MVP = 2 source endpoints × 5 repos = 10 gh API calls × on-refresh**.

### Views MVP
- **`/` Summary page**: 5 repo cards (PR open count + last commit info + manual refresh button)
- **`/api/state`**: JSON dump for future integration
- **NO drill-down** MVP (v1.1+)
- **NO filtering** MVP

### Refresh strategy MVP
- Manual button → triggers gh API calls + updates cache
- Cache TTL: 5 minutes (auto-refresh if stale)
- NO cron MVP (defer cron + schtask install to v1.1)

### Error handling MVP
- gh API rate limit (HTTP 403/429): show stale badge + error text
- Repo unreachable: show error badge
- NO retry exp.backoff (defer)

## File structure MVP

```
apps/cross-repo-dashboard/
├── app.py              # Flask app + routes + gh API calls
├── templates/
│   └── index.html      # Summary view 5 repo cards
├── static/
│   └── style.css       # Minimal CSS
├── requirements.txt    # flask, requests
└── README.md           # How to run
```

## Effort estimate compressed

| Day | Target | Effort |
|-----|--------|--------|
| Day 1 (oggi 5/14) | Scaffold + Flask app + gh API integration single repo working | ~3-4h |
| Day 2 (5/15) | 5 repos aggregation + HTML view + manual refresh | ~3-4h |
| Day 3 (5/16) | Polish + smoke + Eduardo first daily use | ~2-3h |
| Buffer (5/17-5/19) | Bug fix + iteration based Eduardo feedback | ~variable |

**Total core MVP: 8-11h cumulative, 3 days elapsed**.

## Post-MVP iteration (post-Max)

**NOT in this PR**:
- v1.1: add healthcheck sources + git log divergence + drill-down + cron auto-refresh
- v1.2: add memory MEMORY.md + AA01 filesystem + STATUS doc timestamps
- v1.3: schtask cron auto-refresh + improve UI

**Iteration informed by**: Eduardo real daily-use feedback (W1-W4 SPRINT_02 dogfood T8 substitution — Component 1 IS now T8-equivalent for "plugin-like" empirical observation).

## SPRINT_02 plan amendment

Original SPRINT_02 plan (PR #88) had Component 1 GATED Gate E. Amendment 2026-05-14:
- ✅ Gate E gating REMOVED — trigger #1 verified empirical, methodology over-applied
- ✅ Component 1 MVP build pre-Max (Days 1-3)
- ✅ Post-Max iteration informed by Eduardo daily-use real feedback
- ✅ Gate E counter still useful: tracks Eduardo missed-coordination events that MVP fails to address → informs v1.1+ priority

## YAGNI exclusions MVP

- ❌ NO auth (localhost only)
- ❌ NO SQLite cache (in-memory dict sufficient MVP)
- ❌ NO real-time WebSocket (manual refresh acceptable)
- ❌ NO mobile responsive (workstation desktop only)
- ❌ NO drill-down per-repo (summary view enough MVP)
- ❌ NO export/import format
- ❌ NO graceful schema migration
- ❌ NO multi-user

## Reversibility

100% reversible: `rm -rf apps/cross-repo-dashboard/` + revert PR. Build effort ~8-11h. If Eduardo finds MVP underdelivers daily-use need → iterate based on concrete feedback (NOT speculation).

## Honest disclosure (methodology rationale)

**Why this spec violates "no anticipatory build" Archon ciclo 2 conclusion**:
- Archon ciclo 2 conclusion was correct GIVEN information at session 13/5 late night
- New information 2026-05-14 (Eduardo daily-use articulation) invalidates the "trigger unverified" assumption
- Methodology framework MUST update on new evidence (Strato 7 Layer 2 CLASSE A: nuova informazione fattuale → aggiorno liberamente)

**Why MVP and not full Alt A/B**:
- 5gg pre-Max insufficient for full build (Alt A 3.5-4w, Alt B 2.5w)
- MVP gets Eduardo using TODAY (immediate value)
- Real usage post-MVP informs v1.1+ priority (NOT speculation)
- Failure mode: MVP underdelivers → iterate fast post-Max with concrete feedback (lower waste than full anticipatory build)

## References

- Spec V3 cross-repo orchestrator (PR #87)
- Archived pre-design (`docs/research/component-1-design-options-archived-2026-05-13.md`) — content useful AFTER MVP shipped (alternative design options)
- L-2026-05-016 anti-aspirational measurement (warning source, methodology framework)
- L-2026-05-019 (in promotion) — trigger validation window > single-session decision fatigue
- ADR-0017 stack scaffolding (NOT used MVP, standalone Alt B chosen)
- ADR-0023 strategic tier post-Max (NO Opus dependency MVP — Flask straightforward, sovereign tier can iterate post-Max)
- ADR-0026 cognitive workflow protocols (applied + re-evaluated per L-019)
