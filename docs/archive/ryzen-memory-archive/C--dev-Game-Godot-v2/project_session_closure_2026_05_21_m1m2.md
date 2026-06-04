---
name: project-session-closure-2026-05-21-m1m2
description: Session 2026-05-21 M2 generational succession + M1 Sistema persistent learning BOTH shipped via superpowers full chain. Cross-stack (GGv2
metadata: 
  node_type: memory
  type: project
  originSessionId: 6b508d26-ce2f-4ad4-a74d-82a0d64f6470
---

Session 2026-05-21 cleared 2 gated master-dd items (M1 + M2) from the prior wave's sospeso queue. Both shipped end-to-end via the superpowers chain (brainstorming → writing-plans → subagent-driven-development → finishing-a-development-branch), per-task two-stage review (spec + code-quality) + final holistic review + post-merge codex audit.

## Shipped

| PR | Repo | Topic | SHA |
|---|---|---|---|
| #339 | Game-Godot-v2 | M2 generational succession engine A.0+A+B | `e66666e` MERGED |
| #2363 | Game/ | M1 Sistema persistent learning (ADR-2026-05-18 Opt B pilot) | MERGED |
| #340 | Game-Godot-v2 | M1 spec+plan docs | `9733ee5` MERGED |

## M2 generational succession (DF L1/L3)
Soft-death + attrition end-of-life → succession descendant inherits bloodline mutations via `LineagePropagator.inherit_from_lineage` (FIRST live caller — was dead-code since PR #63). True-death (critical) only in lethal-enabled missions via deterministic `LethalityEngine`. 6 new modules (is_lethal accessor, unit_lifecycle ledger, AttritionEngine, SuccessionEngine, LethalityEngine, CombatLifecycleHook wire). 48 GUT, suite 2729. Phase C/D (Main roster wire + player UI) deferred — engine-complete, not yet player-reachable by design. Museum card M-2026-05-21-001.

## M1 Sistema persistent learning (P5, Option B pilot)
Server-side `SistemaState` Prisma (JSONB units_observed) + accumulator (kills+sightings, threat high@kills≥3) + DI store (stub-safe) + roster-gated +20% retreat overlay + session.js hydrate/accumulate. 24 tests + 551 regression. Migration 0011 apply DEFERRED to deploy. Built in git worktree off Game/ main (hc07 calibration WIP untouched — coordinate pattern; resolved 142-commit drift at merge).

## Lessons reaffirmed
- **Verify-not-trust (anti-pattern #8 family)**: 3 ground-truth passes corrected 6 ADR-2026-05-18 seam claims (scoreSession→buildVcSnapshot; campaignLoader is NOT session factory; campaign_id absent from session; no per-unit threat; no defend action; session.js zero-Prisma). The ADR was a design scaffold, NOT ground truth.
- **Both codex P1s were cross-file integration gaps direct-injection unit tests miss**: M2 #319-pattern (`_succession_units` not reset in `_on_session_ended`, only reset_ledger → reused-hook re-spawn) + M1 (`persistent_high_threat` scanned full history not current alive roster → biased unrelated battles). Pattern: when a unit test injects the downstream input (threatCtx, mock) directly, the upstream flag-derivation path stays untested. Dead-code-guard integration tests + post-merge codex both load-bearing.
- **Worktree coordinate** for dirty sibling repo: `git worktree add .claude/worktrees/<name> main` off clean main lets a new workstream proceed while another's uncommitted WIP sits untouched in the primary checkout. Cleaned up post-merge.
- **gdformat on test files** (feedback_gdformat_tests_ci): CI gdformat-check covers tests too; run on both script+test (caught on #339).

## Roadmap remaining (gated)
- M1 sub-proj 2 Godot v2 mirror — NOW UNBLOCKED (units_observed shape merged)
- ADR Option A (factions + strategic_phase FSM) — separate verdict, HIGH balance risk
- M2 Phase C/D (Main roster instantiation + player succession UI + fallen Custode pool)
- Migration 0011 apply → next Game/ deploy
- Tuning (HIGH_THREAT_KILLS=3 / +20% / attrition weights) → playtest #2

## Resume
Handoff `docs/godot-v2/handoff-2026-05-21-m1m2.md`. Specs/plans `docs/superpowers/{specs,plans}/2026-05-21-*`. Both ADR seams ground-truthed in M1 spec §2 — do NOT re-derive.

Related: [[project-adr-2026-05-18-sistema-learning-briefing]] [[feedback-gdformat-tests-ci]] [[feedback-codex-post-cascade-audit]] [[feedback-queue-pattern-lifecycle]]
