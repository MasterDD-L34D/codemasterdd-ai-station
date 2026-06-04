---
name: project-m1-subproj2-godot-mirror
description: "M1 sub-project 2 (Godot Sistema-memory client mirror) shipped to PR — mechanism complete + tested, but BOTH player surfaces not yet reachable in current main.gd wiring (documented follow-up boundaries)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c85420b-b594-4f97-bda3-689f09a4ba69
---

M1 sub-project 2 = Godot v2 read-only client mirror of the server Sistema persistent-learning state (sub-proj 1 = Game/ #2363). Built 2026-05-21 via superpowers full chain (brainstorm → writing-plans → subagent-driven-development 8 tasks, per-task two-stage review + final holistic review) on PC VGit (Ryzen).

## Shipped to PR (NOT yet merged as of 2026-05-21)
- **Game/ [#2364](https://github.com/MasterDD-L34D/Game/pull/2364)** — `GET /api/campaign/sistema-state?campaign_id=` read-only route (thin read over existing `sistemaStateStore`, empty-safe). Branch `claude/m1-sistema-state-route` (built in Game/ worktree off origin/main, coordinate pattern — local Game/ checkout was dirty on hc07).
- **GGv2 [#342](https://github.com/MasterDD-L34D/Game-Godot-v2/pull/342)** — `SistemaApi` (CampaignApi clone) + `SistemaMemory` (pure presenter, filters server `threat_level`, never recomputes) + `body_sistema_remembers` Custode template + ScenarioBriefView telegraph (PRIMARY) + DebriefState/Cronaca echo (SECONDARY). Branch `claude/m1-godot-mirror-2026-05-21`. `main.gd` held 999 LOC via `MainSistema` helper extraction (mirrors `main_seasonal`).

Master-dd surface verdict: "1+2 ponderato" — pre-combat telegraph primary (new build) + post-combat Cronaca echo secondary (light, reuses L2 pipeline).

## Non-obvious: BOTH surfaces mechanism-complete but NOT player-reachable yet
Same "engine LIVE / surface-wiring deferred" boundary as M2 Phase C/D. Documented in spec §11. Future wiring follow-up:
1. **Telegraph** — `_campaign_state` (carries campaign_id) is populated in `_setup_combat_phase`, AFTER `ScenarioBriefView` boots in `_on_world_setup_confirmed`. So `cid` is empty at brief time → telegraph stays hidden. Needs campaign scope established before the brief phase. (Offline tutorial flow may have no campaign at all.)
2. **Echo** — `apply_debrief_echo` correctly folds events into `_last_debrief_state.event_log_snapshot`, but NO TV `DebriefView` is mounted in main.gd's live combat flow (only `PhoneDebriefView`, which doesn't consume `event_log_snapshot`/Cronaca). Events render nowhere on TV today. Needs a TV `DebriefView`/`CronacaPanel` mounted post-combat.
3. Both gated on data anyway: server returns empty `units_observed` until Game/ migration `0011_sistema_state` is applied at deploy → hidden is correct back-compat until then.
4. Notes for the TV-DebriefView wirer (spec §11): echo lands in `encounter`+`pg_ids` only, NOT `per_pg` (so it shows in CronacaPanel "Encounter corrente" tab, not "Storia completa"); `biome_id`/`ts` passed empty → generic "Luogo Sconosciuto" render — thread real biome/ts for flavor.

## Verify-not-trust catch (holistic review)
The PRIMARY-telegraph reachability gap was NOT in the spec (spec §5.5 assumed campaign_id available at brief). Ground-truth of main.gd phase ordering revealed it — same class as the M1 sub-proj-1 ADR-seam corrections. Per-commit reviews passed (code correct); only the cross-task holistic review + reading `_on_world_setup_confirmed` vs `_setup_combat_phase` ordering surfaced it.

Related: [[project-session-closure-2026-05-21-m1m2]] [[feedback-godot-new-classname-editor-scan]] [[feedback-gdformat-tests-ci]]
