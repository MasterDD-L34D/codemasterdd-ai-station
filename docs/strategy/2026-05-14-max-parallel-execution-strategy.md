# Strategy — Max parallel execution 5gg residui (2026-05-14)

**Date**: 2026-05-14 sera
**Status**: Active execution
**Trigger**: Eduardo statement "abbiamo un'infrastruttura con dashboard ma non è completa non ci permette ancora di smistare il lavoro come volevamo e i vari sprint sono ancora ingiustamente delegati a un futuro che può essere benissimo ora affiancato al max"

## Honest reframe — methodology was over-conservative

### Bias identified

PR #87 + PR #88 + SPRINT_02 plan + W0 pre-flight applied **L-016 anti-aspirational + Gate E gating + sovereign-first defaults** in modo TROPPO restrittivo. Pattern observed:

- Component 1 dashboard build: gated to Gate E 30gg post-Max → Eduardo "userei ogni giorno anche ora" articulation invalida (L-019 promoted)
- SPRINT_02 T8/T9/T10: calendarizzato 5/20-6/19 per "sovereign-tier empirical validation" → ma NON c'è ragione tecnica di aspettare. Max disponibile NOW + Max-worthy multi-source synthesis = higher quality output rispetto a sovereign tier limit.
- Cross-repo PR Component 2: gated to "first 3 PR pattern-validation" SPRINT_02 → empirical validation possibile NOW con Max + Eduardo authorization

### Reality post-screenshot Max usage

| Capacity | Usage | Headroom |
|----------|-------|----------|
| 5h limit | 7% | 93% |
| Settimanale tutti modelli | 75% | 25% × 2gg reset |
| Solo Sonnet | 3% | 97% |
| Context window | 75% | 25% session |

**Max is RESOURCE, NOT scarce-preserve**. Sfruttare massivamente fintanto disponibile.

## New strategy — affianca Max + sovereign parallel

### Tier routing NEW (override SPRINT_02 plan)

| Task class | Tier | Rationale |
|-----------|------|-----------|
| Multi-file synthesis cross-repo | **Max NOW** | Opus 4.7 quality multi-file unbeaten sovereign tier |
| ADR draft + research doc | **Max NOW** | Heavy synthesis Max-worthy |
| Architectural design | **Max NOW** | Strategic decisions need Opus capability |
| Methodology analysis (T9) | **Max NOW** | Cross-source cite + pattern detection |
| Quality Gate Three Strikes (T10) | **Max NOW** | Empirical scan multi-source |
| Component 1 v0.3 features | **Max NOW** | Daily-use feedback loop critical, Max ship faster |
| Cosmetic edits (rename, JSDoc) | Sovereign Aider 7B | post-Max viable |
| Behavior single-file refactor | Sovereign Aider 14B Q2 | post-Max viable |
| Cross-repo PR drafting | **Max + Eduardo auth** | First-3-PR pattern validation Max-quality output |
| Routine task delegation | OpenCode 30B | post-Max viable |

### Parallel execution plan 5gg residui (5/14-5/19)

**Day 0 (oggi sera) — Started**:
- ✅ Component 2+3 shipped
- ✅ Dashboard v0.2 shipped
- ✅ Docker stack live
- ✅ Console flash fix
- → Strategy doc (this) + execute Max-tier work

**Day 1-5 (15/5 - 19/5) — Max-tier ship list**:

1. **Component 1 v0.3 daily-use features** (Eduardo informed by 1-day usage):
   - Filter / search repos by name/state
   - Drill-down per-repo detail view (full PR list + commits + decisions)
   - PR velocity chart (commits/week last 4 weeks)
   - JOURNAL recent entry preview header
   - Recent cross-repo activity feed
   - **Effort**: ~4-6h Max
   - **When**: tomorrow after Eduardo 1-day-use real feedback

2. **T9 methodology empirical analysis** (Max-worthy synthesis):
   - Cite count P1-P6 deep analysis cumulative (current baseline P1=19 P2=13 P3=12 P4=8 P5=5 P6=2)
   - Gap identification: which protocols under-utilized? over-applied?
   - ADR-0026 amendments concrete (P5 + P6 n>=3 threshold validation)
   - Quality Gate ADR-0028 Three Strikes empirical scan (vault MODEL_ROUTING adoption pattern)
   - **Output**: research doc `docs/research/methodology-effectiveness-2026-05-14.md` + eventual ADR amendments
   - **Effort**: ~3-4h Max
   - **When**: shipping today/tomorrow

3. **Cross-repo PR opportunistic empirical** (Component 2 first-3-PR pattern validation):
   - Scan 4 target repos (Game / Godot-v2 / Dafne / vault) for concrete drift / policy-alignment / docs candidates
   - Open 1-2 real PR via dry-run-pr.ps1 (Eduardo authorization each)
   - Outcome tracking in `logs/cross-repo-pr-2026-05.md`
   - **Output**: 1-2 real PR opened + empirical validation Component 2 workflow
   - **Effort**: ~2-3h Max + Eduardo
   - **When**: tomorrow opportunistic post-scan

4. **Dogfood-ui slow latency root-cause fix** (defer-eligible):
   - Profile `/api/health` endpoint internal checks
   - Cache N seconds or async background
   - **Effort**: ~30min-1h Max
   - **When**: opportunistic

5. **Lesson L-021+ capture** if new patterns emerge from above work
   - Cross-pattern adoption pattern (post Three Strikes scan)
   - Cross-repo PR empirical (post first PR outcome)
   - **Effort**: ~30min per lesson

### What stays sovereign post-Max (5/20+)

- Daily ops use (dashboard daily-use, gh CLI checks)
- Cosmetic edits via Aider wrappers (7B/14B)
- OpenCode multi-step routine tasks
- Logging discipline Gate E (Eduardo manual)
- Bug fixes singular-file behavior changes

## Revised SPRINT_02 framing

**Original** (PR #88): T8 plugin observation + T9 methodology effectiveness + T10 Three Strikes — all GATED post-Max.

**Revised** (this strategy): T8 + T9 + T10 ATTACKED NOW with Max, **post-Max becomes**:
- Continuous use + observation passive
- Cost tracking primo-mese empirical
- Gate E logging discipline (only thing genuinely needs sovereign empirical)
- Component 1 v0.4+ iteration informed by accumulated feedback

**Sprint window**: still 5/20-6/19 calendar, but **NOT work-boundary**. Sprint = "first sovereign month review", NOT "wait for it".

## Methodology amendments captured

### L-016 anti-aspirational policing revised

NEW criterion (post L-019 + this strategy):
- Anti-aspirational applies to **pure speculation without articulated need**
- DOES NOT apply when:
  - User articulates concrete daily-use case (L-019)
  - Capability resource is available AND has expiration deadline (Max 19/5)
  - Multi-source synthesis benefits from higher-tier model
  - Eduardo explicitly overrides via CLASSE D scelta-valore in his domain

### Gate E counter still valid

Gate E counter for Component 1 build trigger was correct discipline IF Component 1 build cost > Max-tier capability advantage. **Reality**: Component 1 SHIPPED day-1 with Max (8-11h actual). Future iterations informed by use. Gate E counter STILL useful as feedback metric (events/wk = how much pain Eduardo feels) but NOT as build-blocker since infrastructure already exists.

### Cross-repo PR pattern validation

Component 2 first-3-PR validation was scheduled SPRINT_02 W2-W3. **Revised**: attempt now empirically with Max + Eduardo authorization. Faster pattern-validate signal than waiting calendar.

## Risk acknowledgments

1. **Max overrun**: 75% settimanale → could hit limit before 5/19 if heavy parallel work. Mitigation: monitor Settimanale gauge, downshift to Sonnet if needed (3% Sonnet utilization = headroom).
2. **Console window flashing fixed** but other subprocess sites (Component 2 scripts, install-shortcut) NOT in dashboard. Eduardo can ignore brief flashes from manual script invocations (rare events).
3. **Anti-pattern recurrence**: this strategy IS itself a methodology decision NOW. If proves over-aggressive in retrospect, capture as L-022 + amend.

## Confidence

**80%**. Bias was identified honest. Max capability is real. Eduardo articulated explicit override. Work items are concrete + scoped.

## Execute sequence (starting NOW)

1. Commit + push this strategy doc
2. Start Max-tier work #1: T9 methodology empirical analysis (deeper synthesis, immediate)
3. Then #3 Cross-repo PR opportunistic (Eduardo auth at PR drafting time)
4. Then #1 Component 1 v0.3 features (Eduardo daily-use feedback first)
5. #4 dogfood-ui root-cause + #5 lessons captured opportunistically

## References

- L-2026-05-019 trigger validation window > single-session decision fatigue (companion lesson invalidating prior over-conservative bias)
- L-2026-05-016 anti-aspirational measurement (still valid, scope revised)
- ADR-0023 strategic tier post-Max API on-demand (post-Max budget cap, NOT pre-Max scarcity)
- PR #88 SPRINT_02 detailed plan (SUPERSEDED by this strategy doc)
- Eduardo statement 2026-05-14 sera "i piani fino ora sono tutti troppo conservativi" + screenshot Max usage 75%/2gg
