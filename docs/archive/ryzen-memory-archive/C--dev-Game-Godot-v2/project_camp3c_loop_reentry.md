# CAMP-3c — TV loop re-entry (PR #350)

**Date**: 2026-05-22 · branch `feat/camp3c-loop-reentry` · base main `b97b905`

## Shipped
Closes the campaign loop on TV. Debrief **continue** re-enters the SAME encounter via the scenario-brief phase → `MainSistema.install_with_run_id` re-reads `units_observed[run.id]` → M1 telegraph renders on the 2nd+ loop (the payoff of the CAMP-1+2+3 chain). **retire** = end run (unchanged dismiss).

3 surfaces:
- `MainCombatSetup.teardown(host)` — idempotent combat-scene teardown (orchestrator/hook/ambition/vfx + `_units_container` children + `units_by_id.clear()`), first line of `_setup_combat_phase`. Fixes unit double-spawn + tracker orphans on re-entry + latent boot-recreate gap. Co-located with creation (Archon-fusion verdict over "separate MainLoop helper"). main.gd 1000→996 LOC.
- `MainDebrief.reenter(host)` — free DebriefView (queue_free, runs in signal callback) + dialogue overlay → `_on_world_setup_confirmed(_initial_world_state)`. null world_state → dismiss fallback. continue→reenter, retire→dismiss.
- `MainAtlas.install` — detach prior `AtlasPulseAdapter` on atlas reuse (holistic-review followup; was leaking one `skiv_pulse_fired` handler per loop).

## Scope / gated
- Same-encounter re-loop, **TV/solo only**. Co-op phone-sync (`next_macro` broadcast + composer follow) = CAMP-3c-coop followup (NOT done).
- Telegraph RENDER still gated on **migration 0010/0011 applied at deploy** — until then `/sistema-state` read empty (loop works, telegraph dark). Manual loop smoke = same gate.
- CAMP-4 (Descent engine `/campaign/advance`) + CAMP-5 (content variety) + CAMP-6 still ahead.

## Method / quality
brainstorm (Archon ensemble: 2 blind evaluators risk-lens A vs arch-lens B → critic fusion = B refined by ownership boundaries) → writing-plans → subagent-driven (2-stage per-unit review) → holistic (opus, verdict SHIP-WITH-FOLLOWUPS, the followup landed). GUT 2797 pass / 0 fail / 5 pending (pre-existing) / 2 orphans (pre-existing). +10 net tests. gdlint clean.

## Also this session
- Game/ **#2377 MERGED** (M1 sistema-memory debrief chip backend; wording "Il Sistema ti ricorda" approved by master-dd at merge — a parallel chip had pre-claimed approval in-code, surfaced + confirmed before merge).
- Duplicate handoff commit dropped via rebase onto origin/main (already merged as #349).

## Post-PR codex P2 (addressed, 0e0e8e1)
`_promotion_panel` binds `combat_lifecycle_hook.promotion_evaluations_ready`; the hook is recreated each loop but `MainCombatPanels.mount_promotion` early-returns on a still-valid panel WITHOUT re-wiring → reused panel stayed bound to the freed hook → loop 2+ promotions never reached UI. Fix: `teardown` also frees `_promotion_panel` → mount rebuilds + rewires.
**Generalizable trap** (holistic opus review MISSED it — claimed "reused panels idempotent"): a mount/attach helper that early-returns on existing is NOT safe when its dependency (signal source) is recreated per loop. Either free the consumer in teardown (chosen) OR make the helper disconnect-old+reconnect. Check every reused node connected to a per-loop-recreated hook/orchestrator. (Note: emitter/HUD are REUSED not recreated, so their connections survive — only hook-bound + orchestrator-bound consumers break.)

## Supersedes
`project_camp_loop_m1_live.md` blockers: #2377 open → MERGED; CAMP-3c "not done" → PR #350.
