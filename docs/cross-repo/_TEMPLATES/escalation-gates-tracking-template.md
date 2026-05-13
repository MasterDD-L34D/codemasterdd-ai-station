# Escalation gates tracking template

Template per `logs/escalation-gates-YYYY-MM.md` (gitignored).

## Gate E status

- Empirical window: 5/20 -> 6/19 (4 weeks)
- Current week: <fill in week start date>
- Current count: <events>
- Avg events/wk this month: <calc>
- Threshold met? <yes/no/not-yet>

## Per-week summary

| Week start | Events count | Severity avg (1-5) | Total cost (min) | Gate E threshold (>=5)? | Anti-pattern flags |
|------------|--------------|--------------------|-----------------|-------------------------|---------------------|
| 2026-05-20 | 0 | - | 0 | - | - |
| 2026-05-27 | 0 | - | 0 | - | - |
| 2026-06-03 | 0 | - | 0 | - | - |
| 2026-06-10 | 0 | - | 0 | - | - |

## Gate A status (Opt 3 trigger)

- Current count high-severity events: <count>
- 4-week consecutive trigger met? <yes/no>

## Gate B status (Opt 4 trigger)

- Current repo count monitored: 6 (Game / Godot-v2 / Dafne / vault / Synesthesia / AA01)
- >=7 trigger? NO
- Client work active? NO

## Gate C status (bandwidth)

- Eduardo bandwidth self-report monthly: <yes if applicable>

## Gate D status (Component 2 reversibility)

- Cumulative PR opened: 0
- Cumulative PR accepted: 0
- Cross-reference adoption count: 0
- >=5 with adoption trigger? NO

## Week 4 audit checklist (harsh-reviewer subagent invocato)

- [ ] Logging discipline consistency check (no gap weeks)
- [ ] Severity tag distribution sanity (NOT all =1, NOT all =5)
- [ ] Cost minutes documentation present (NOT all = 0)
- [ ] Aggregate count plausibility vs JOURNAL cross-reference
- [ ] Gate E decision: BUILD full / BUILD MINIMAL / DEFER

Audit invoked via Claude Code:
> Spawn harsh-reviewer subagent. Read logs/coord-events-YYYY-MM.md + logs/escalation-gates-YYYY-MM.md.
> Verify: logging discipline + severity distribution + cost documentation + plausibility + Gate E threshold met.
> Output: P0/P1/P2 findings if drift detected + Gate E decision recommendation.

Cost stimato: ~$0.30 (~85K tokens). Sotto cap ADR-0023.
