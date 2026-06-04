# RESUME ENTRY — Consolidated repo roadmap (2026-05-22)

**Doc**: `docs/superpowers/plans/2026-05-22-repo-roadmap-consolidated.md` (PR #351). **Start any campaign-loop / M1 / M2 resume here** — it's the single ground-truthed source (the 7 individual plans in `docs/superpowers/plans/` are all SHIPPED; their checkboxes lag reality per anti-pattern #19).

## DONE (main, verified 2026-05-22)
P4 L2/L3/L4 (#284→#337) · M1 pilot (Game/ #2363) · M1 Godot mirror (#342/#2364) · M2 succession **engine** (#339, NOT Main-wired) · CAMP-1/2 (#345/#2371/#2374/#2376) · CAMP-3a/3b (#347/#348) · CAMP-3c loop re-entry (#350) · M1 debrief chip (#2377) · migrations 0010/0011/0012 applied + species seed fixed (#2378). Full server loop + telegraph RENDER smoked (native screenshot).

## REMAINING (sequenced, R1 = next pickup)
- **R1 M2 Phase C** — wire `succession/attrition/lethality_engine.gd` (exist, NOT in main.gd/main_combat_setup.gd) into next-encounter roster build. Descendant inherits via `LineagePropagator.inherit_from_lineage`. **Unblocked by CAMP-3c. Highest value.**
- **R2 M2 Phase D** — player succession UI + fallen Custode pool + auto-succession toggle.
- **R3 CAMP-4** — coop `next_macro` → `/campaign/advance` (Descent def-chain), retire in-memory `scenarioStack` (`coopOrchestrator.advanceScenarioOrEnd`).
- **R4 CAMP-5** — per-encounter content/units loader (today always `tutorial_01`).
- **R5 CAMP-6** — boot-into-world-setup (run from formation, not tutorial) + §8 Legacy Memory.
- **R6 CAMP-3c-coop** — phone-sync on loop re-entry (TV ignores WS phase_change; host doesn't broadcast next_macro on continue).
- **R7 ADR-2026-05-18 Option A** — M1 full-ML factions/FSM (gated vs shipped Opt-B pilot).

## Gated / non-code
Tuning playtest #2 (HIGH_THREAT_KILLS=3 / retreat +0.2/+20% / attrition — v0, no balance claim, anti-pattern #14/#15) · `unit_progressions` schema drift Game/ (separate followup migration) · Cloudflare prod + iOS device smoke · asset W7 · real multi-device co-op smoke.
