# [ARCHIVED PRE-DECISION] Component 1 dashboard — design options exploration

> **CRITICAL — DO NOT CONSULT during Gate E W4 audit** (per ADR-0026 + L-2026-05-016 anti-pattern bias risk).
>
> **Status**: ARCHIVED 2026-05-13 sera-tardi-ultra-3 post harsh-reviewer P0.1 finding (PR #88 v1 was META-anti-pattern L-016).
>
> **Original status**: Pre-design spec, confidence 40% (anticipatory + gate-dependent + Eduardo CLASSE D scelta-valore explicit).
>
> **Why archived**: pre-design's existence would bias Gate E empirical audit (Eduardo anchoring on Alt A vs B framing pre-decision). Honest disclosure section in original was insufficient mitigation — file existence itself anchors the decision.
>
> **What stays useful**: Alt A vs B tradeoff matrix as input AFTER Gate E PASS decision, NOT before.

## Triple-warning header

1. ❌ **DO NOT** read this file during Gate E logging discipline 4-week window (5/20 → 6/19)
2. ❌ **DO NOT** read this file during Week 4 harsh-reviewer audit (~6/14)
3. ✅ **ONLY** consult AFTER Gate E threshold decision finalized (PASS/MINIMAL/FALSIFIED) as design-options input for post-decision execution

## What was originally proposed (trimmed to essentials)

Component 1 = read-active dashboard aggregator for cross-repo coordination state. Originally spec V3 cross-repo orchestrator (Opt 1.5 REDUCED) gated this build to Gate E threshold ≥5 events/wk × 4 weeks empirical.

### Alternative A vs B tradeoff matrix (KEEP — useful post-Gate-E)

| Criterion | Alternative A (extension dogfood-ui) | Alternative B (standalone) |
|-----------|-------------------------------------|---------------------------|
| Effort total | ~3w + 0.5-1w prereq (dogfood-ui scaffold opt-in DOWN currently — promote to always-on prerequisite) = **3.5-4w realistic** | ~2.5w |
| Coupling risk | High (depends on dogfood-ui maintenance) | Low (independent app) |
| Container count | 1 (riuso) | 2 (new container) |
| Port conflicts | None (8080 already used) | New port (8081 proposed) |
| Maintenance overhead | Shared with dogfood-ui (currently DOWN) | Independent lifecycle |
| Future Component 2/3 integration | Easier (shared infrastructure) | Requires bridge layer |

**Honest revision post P1.5 harsh-review**: Alt A pre-req cost (`promote dogfood-ui always-on`, ~0.5-1w) was hidden in original v1; matrix now shows real 3.5-4w vs 2.5w → **Alt B has stronger advantage than original matrix implied**.

### Gate E threshold-dependent decision tree (KEEP — operational)

| Gate E outcome | Component 1 action |
|----------------|-------------------|
| ≥5 events/wk (BUILD full) | Eduardo Alt A vs B explicit decision; design from scratch OR re-consult this archive |
| 2-<5 events/wk (BUILD MINIMAL) | Alt A reduced scope OR Alt B minimal |
| <2 events/wk (FALSIFIED) | NOT BUILT. Update STATUS_MULTI_REPO trigger #1 empirically falsified. Close spec V3 follow-up. |

## What was trimmed from original v1 (prescriptive sections that bias audit)

**Removed sections** (intentionally — these were prescriptive AND would bias W4 Gate E audit):
- ❌ Data model SQLite schema (`CREATE TABLE cross_repo_state ...`) — pre-decision, not needed
- ❌ Source aggregation budget table (10 sources × cron × TTL) — same
- ❌ View design HTML layout details — same
- ❌ JSON API endpoint shape — same
- ❌ Error handling tiers — same
- ❌ Testing patterns — same

These details belong in the **actual Component 1 build spec** (written AFTER Gate E PASS decision, NOT before).

## Falsifier for "pre-design saved 30-50% effort" (P1.4 fix)

Original v1 claimed "IF Gate E PASS, design ready saves SPRINT_02 30-50% effort". Harsh-reviewer P1.4: no falsifier defined.

**Honest falsifier**: this archive contains ~5% of full Component 1 design (Alt A vs B matrix + decision tree only, post-archival trim). If Gate E PASSes and Eduardo's full Component 1 spec takes ~3.5-4w (Alt A) or ~2.5w (Alt B), this archive provided **<5% savings** vs designing fresh. The 30-50% claim was inflated.

**Audit post-SPRINT_02**: if Component 1 ships, measure actual savings vs estimated-from-scratch baseline. Threshold for "pre-design valeva l'effort": ≥20% effort reduction. <20% = pre-design was wrong call (effort lost).

## Lesson captured (in promotion as L-2026-05-018)

**Pattern**: META-anti-pattern recurrence — same session that ratifies anti-pattern lesson (L-016 PR #87 ciclo 2 self-falsification) immediately violates it with pre-empirical artefact (PR #88 v1 Component 1 spec).

**Mitigation applied** (PR #88 v2):
- Conversion spec → archived research doc with hard DO NOT CONSULT header
- Trim of prescriptive sections (kept only Alt A vs B matrix + decision tree)
- Plan file restructured as DELTA over SPRINT_02.md

**Future trigger**: SPRINT_02 W4 audit (Week 4 ~6/14) must include explicit check "did Eduardo consult any archived pre-design during 4-week window? If yes, contamination flag in audit".

## Methodology re-statement

PR #87 spec V3 ratified L-016 anti-aspirational. The Component 1 pre-design (originally proposed v1) violated that exact lesson. Honest disclosure insufficient. Action taken: archive + trim + WARN.

Post-Gate-E decision (PASS/MINIMAL/FALSIFIED), if Component 1 build is justified empirically, the actual design spec should be written fresh OR consult this archive AFTER decision made, NOT before.

## References

- Spec V3 cross-repo orchestrator (PR #87 merged `3e580e2`)
- ADR-0017 stack scaffolding (apps/dogfood-ui foundation reference for Alt A)
- ADR-0026 cognitive workflow protocols (P5 harsh-reviewer caught this anti-pattern)
- L-2026-05-016 cognitive protocols measurement anti-aspirational (the violated lesson)
- L-2026-05-018 (in promotion) — META anti-pattern recurrence same-session
- Component 3 escalation gates Gate E threshold definition (`docs/governance/ESCALATION_GATES.md`)
- PR #88 v1 (rewrite as v2 includes this archive) — recovery action chosen REWORK to MERGE
