# Research — Methodology framework empirical effectiveness 2026-05-14

**Date**: 2026-05-14 sera-tardi-ultra-2
**Source-of-truth**: JOURNAL.md cite counts + lessons promoted + ADR-0028 Three Strikes scan
**Trigger**: T9 SPRINT_02 task brought forward to pre-Max parallel execution (strategy doc 2026-05-14)

## Executive summary

| Question | Finding |
|----------|---------|
| Protocol 1-6 over-applied or under-applied? | P1 dominant (19x), P5+P6 NEW threshold met (6x + 2x) but P6 limited samples |
| ADR-0026 P5+P6 n>=3 threshold status | **P5 met (6 cite + 3+ invocations); P6 unmet (2 cite + 1-2 invocations)** |
| ADR-0028 Three Strikes empirical state | **0/3 strikes empirical** — stays Proposed |
| Lessons cross-session value | 19 cumulative L-001..L-020 (3 new today: L-018+L-019+L-020) |
| Methodology amendments needed? | YES: L-016 scope refinement + Gate E counter-as-build-trigger reframe |

## Cite count Protocol 1-6 (JOURNAL.md cumulative)

| Protocol | Cite count | Threshold n>=3? | Trend vs 2026-05-14 mattina baseline |
|----------|------------|-----------------|--------------------------------------|
| P1 Refresh-verify | 19 | YES (well above) | +0 (stable, most-used) |
| P2 Autoresearch | 13 | YES | +0 |
| P3 Archon 7-step | 12 | YES | +0 |
| P4 AA01 workspace | 8 | YES | +0 |
| P5 harsh-reviewer | 6 | YES (just over threshold post today's 2x invocations) | +1 (NEW today: Protocol 5 cumulative this session reference) |
| P6 brainstorming | 2 | **NO** (under threshold, NEEDS 1 more cite) | +0 |

### Distribution observation

P1 dominates 36% of cite (most heavily used). P5 + P6 only 16% combined despite being formalized 1 day ago (2026-05-13 addendum). **Pattern**: newly-added protocols take time to integrate organically into JOURNAL narrative.

P6 brainstorming has 2 cite but **empirical invocations 1-2x this session** (Protocol 6 design generative). Real usage > documented mentions — possibly under-cited in JOURNAL drafts.

## P5/P6 n>=3 instances Accepted threshold (ADR-0026 addendum)

### P5 harsh-reviewer status: **READY for Accepted ratification**

Empirical invocations cumulative:
1. PR #87 spec V3 ciclo 2 harsh-review post-Draft (3 P0 + 6 P1 + 3 P2 findings)
2. PR #88 v1 -> v2 harsh-review (3 P0 + 5/6 P1 + 3 P2 → REWORK verdict)
3. PR #91 v0.2 post-build harsh-review (4 P0 + 5 P1 + 12 acknowledge)
4. PR #88 final harsh-review post v3 archive (5 P0 + 6 P1 + 6 P2)
5. Today's end-to-end verifica-con-metodo (4 P0 + 5 P1 + 12 ack)

**N=5 invocations across multiple PRs cumulative session 2026-05-13/14**. Threshold n>=3 met **empirically genuine** (NOT same-PR self-application per L-016 mitigation).

**Action**: ratify ADR-0026 P5 Accepted (drop "Option C non-mandatory" status, formalize as standard pattern for cluster >=3 PR + governance-critical files).

### P6 brainstorming status: **UNDER threshold**

Empirical invocations:
1. PR #87 spec V3 design (Eduardo "Riavvio Archon ciclo 2" partly P6-mediated)
2. PR #88 spec V4 Component 1 MVP (4 categorie ABCD AskUserQuestion = P6-style structured options)
3. Strategy doc 2026-05-14 (this session, partial P6 brainstorming options presentation)

**N=2-3 invocations** (boundary). Counter: harsh-reviewer P0.1 PR #88 noted "PR #88 v1 IS L-016 anti-pattern" - meaning P6 may be over-applied when triggered by Eduardo direct "what should I do" question (over-structured option presentation).

**Action**: keep P6 status quo (Option C non-mandatory). Re-evaluate post +2 invocations cross-session.

## ADR-0028 Three Strikes empirical scan

Source-of-truth: `docs/research/` + `logs/aider-delegation-*.md` + JOURNAL.md + BACKLOG.md

### Strike 1 — Regress reale tier promotion ad-hoc

**Search**: regress + ad-hoc + tier promotion mentions

**Result**: **0 hits** empirici. No tier ad-hoc promotion regress documented in delegation logs.

**Verdict**: NOT FIRED.

### Strike 2 — Successful manual Quality Gate 3-step application

**Search**: Smoke + Research + Tuning fixture on tier candidate

**Result**: 3 research docs found mentioning these terms BUT inspection needed for actual 3-step application:
- `adr-0026-effectiveness-reflexive-audit-2026-05-12.md`: methodology reflexive audit, NOT tier promotion fixture
- `hook-chain-effectiveness-smoke-2026-05-12.md`: hook chain smoke, NOT tier promotion
- `model-routing-quality-gate-cross-pattern-2026-05-12.md`: research doc that PROPOSED the Quality Gate methodology, NOT application of it

**Verdict**: NOT FIRED (research-doc-as-input vs application-of-3-step).

### Strike 3 — Emergent tier promote request

**Search**: tier promote + model rotation + wrapper variant requests

**Result**: BACKLOG mentions Three Strikes ADR-0028 status (Proposed) but no empirical PROMOTE REQUEST emergent in real workflow.

**Verdict**: NOT FIRED.

### Net Three Strikes verdict

**0/3 strikes fired empirical**. ADR-0028 status remains **Proposed**. No ratification trigger active.

**Action**: ADR-0028 stays Proposed. Re-scan post SPRINT_02 end-of-window (~6/19). Document this scan as input.

## Methodology amendments concrete (ADR-0026 candidates)

### Amendment 1: P5 harsh-reviewer Accepted formalization

Current status: ADR-0026 addendum Option C non-mandatory.
Proposed: **Accepted** status given n=5 empirical invocations cross-PR genuine (not self-PR cherry-pick).
Required: ADR-0026 amendment commit + JOURNAL entry. **Action**: ship now.

### Amendment 2: L-016 anti-aspirational scope clarification

Current scope: anti-aspirational policing applies to "introduce framework + same-PR self-apply".
Proposed clarification: **DOES NOT apply when**:
- User articulates concrete daily-use case (L-019 reference)
- Capability resource is available AND has expiration deadline
- Multi-source synthesis benefits from higher-tier model
- Eduardo CLASSE D scelta-valore explicit override

Reference: today's strategy doc + L-019 promoted.
**Action**: amend L-016 lesson file inline + cross-link L-019 + strategy doc.

### Amendment 3: Gate E counter framing

Current framing (PR #87 spec V3): Gate E counter as BUILD-blocker for Component 1.
Reality post Component 1 MVP shipped (PR #91 c2cb816): Component 1 EXISTS. Counter NOT build-blocker.

Proposed framing: **Gate E counter as FEEDBACK METRIC** — measures how much pain Eduardo feels for missed-coordination events. Informs:
- Whether v0.3+ iteration priorities are right
- Whether dashboard adoption succeeds (low events post-build = success)
- Whether scope expansion (Opt 3/Opt 4) is justified eventually

**Action**: amend Component 3 ESCALATION_GATES.md with reframe Gate E thresholds (still ≥5 vs 2-<5 vs <2 but interpretation = feedback NOT block).

## Lessons cumulative state

```
~/aa01/learnings/
├── L-2026-04-001 (one-shot reactive pattern)
├── L-2026-05-002..L-2026-05-016 (15 lessons cluster 12-13/5)
├── L-2026-05-018 META anti-pattern recurrence (NEW 14/5)
├── L-2026-05-019 trigger validation window (NEW 14/5)
└── L-2026-05-020 Docker orphan socket cleanup (NEW 14/5)
```

Total: 18 files (gap L-017 = intentional skip — was claimed pre-promotion but never created).

**Quality observation**: 3 new lessons today are CONCRETE empirical (not aspirational claims). Pattern improvement vs L-016 risk.

## Cross-reference recommendations

| Output | File | Status |
|--------|------|--------|
| ADR-0026 amendment P5 Accepted | `docs/adr/0026-cognitive-workflow-protocols.md` (add amendment section) | TODO ship |
| L-016 scope clarification | `~/aa01/learnings/L-2026-05-016-*.md` (inline amend) | TODO ship |
| ESCALATION_GATES.md Gate E reframe | `docs/cross-repo/ESCALATION_GATES.md` (amend) | DONE |
| Strategy doc reference | `docs/strategy/2026-05-14-max-parallel-execution-strategy.md` | DONE |

## Net assessment

Methodology framework empirical:
- **5/6 protocols (P1-P5) well-integrated** with cite >= threshold + organic invocations
- **P6 brainstorming under-tested** — may need more empirical cycles before Accepted
- **ADR-0028 Three Strikes** = methodology NOT YET justified empirical; stays Proposed
- **3 lessons promoted concrete today** = healthy lesson capture cycle restored

**Confidence**: 80%. Cite count is one signal (NOT comprehensive). Organic invocation count is another (counted manually). Gap: no automated effectiveness measurement = future enhancement candidate post-Max.

## References

- ADR-0026 cognitive workflow protocols (P1-P6 + addendum)
- ADR-0028 Tier promotion Quality Gate methodology (Proposed, Three Strikes ratification trigger)
- L-2026-05-016 anti-aspirational measurement
- L-2026-05-018 META anti-pattern recurrence
- L-2026-05-019 trigger validation window
- Strategy doc 2026-05-14 max parallel execution
