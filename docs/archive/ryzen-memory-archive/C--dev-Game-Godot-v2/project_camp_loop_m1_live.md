---
name: project-camp-loop-m1-live
description: Campaign-loop arc — M1 Sistema persistent-learning write-path is LIVE end-to-end in co-op (kill→delta→fold→upsert on real run.id) + TV DebriefView mounted; telegraph READ surface gated on CAMP-3c (not yet done).
metadata: 
  node_type: memory
  type: project
  originSessionId: 20c560cf-9e4c-416c-a419-e0a1881db0cc
---

Session 2026-05-21/22 shipped the campaign-loop arc that makes M1 Sistema learning actually accumulate (it was built-but-unwired before — only the abandoned web-v1 `session.js /end` wrote SistemaState, never called by the Godot/co-op flow). 9 PR merged.

## What's LIVE (write path)
Combat is **client-side** (Godot RoundOrchestrator; server only relays in co-op — session.js d20 is legacy/unwired). End-to-end accumulation:
`combat_session` lethal hit → `ev.is_kill` → `combat_lifecycle_hook` Cronaca `outcome="kill"` → `SistemaObservations.from_snapshot` slim-delta `{roster, kills}` (kill = outcome==kill & actor∈pg_ids & target∉pg_ids) → `MainCoopCombatEnd.notify_host` POST `/coop/combat/end` w/ `sistema_observations` → `coopOrchestrator.endCombat` → `foldObservations(prior, obs)` → `sistemaStateStore.upsert(run.id, units_observed)` + threat.
- `run.id` = `run_${crypto.randomUUID()}` (collision-safe #2374; was millisecond — now the persistence key). Threaded lobby `start_run` response → `WorldSetupState.run_id` → `CampaignState.campaign_id` via `MainCampaign.apply_run_id` (combat) + `MainSistema.install_with_run_id` (brief).
- M1 defensive overlay reaches Utility-AI Sistema too (#2376 — `aggressive: use_utility_brain:true` in `packs/evo_tactics_pack/data/balance/ai_profiles.yaml`; `selectAiPolicyUtility` now gets `persistent_high_threat` → +0.2 retreat bonus).
- **TV DebriefView mounted** (CAMP-3b #347): `MainDebrief.mount` on `_on_debrief_ready` → debrief screen + Cronaca per-PG render (kills "ha abbattuto" via PR-B0 + lineage + bond + M1 echo). Decoupled from echo network (#348): mount-first + `refresh_after_echo`.

## PR ledger
GGv2: #342 (mirror) #343 (arch map) #345 (CAMP-1+2 client) #346 (uid) #347 (CAMP-3b) #348 (decouple). Game/: #2371 (CAMP-2 server) #2374 (run.id) #2376 (utility-AI passthrough). (M1 sub-proj-1 #2363 prior session.)

## Remaining (gated)
- **Game/ #2377 OPEN** — M1 sistema-memory chip in debrief (Gate-5 surface), review+merge.
- **CAMP-3c loop re-entry** (NOT done) — debrief continue → next encounter → re-loop. This is what makes the **telegraph fire** (reads sistema-state at the 2nd brief) + defines "what after continue" (currently dismiss → neutral end). Design-heavy: next-encounter semantics on the local-driven TV + co-op next_macro walks a server-side in-memory scenarioStack (NOT the Descent campaign engine — see arch map #343).
- **Migration 0010+0011 apply** at next deploy (idempotent `prisma migrate deploy`). Until then SistemaState/godot-v2 reads return empty.
- **Tuning playtest #2** — HIGH_THREAT_KILLS=3, retreat +0.2 (utility)/+20% (legacy), attrition — all v0, no balance claim (anti-pattern #14/#15).

## Refs
Handoff `docs/godot-v2/handoff-2026-05-22-camp-loop-m1-live.md`. Arch decision-map `docs/superpowers/specs/2026-05-21-campaign-loop-architecture-design.md` (#343, O1-O5 + roadmap CAMP-1..6). CAMP-3b spec `docs/superpowers/specs/2026-05-21-camp3b-tv-debrief-mount-design.md`.

Related: [[feedback-verify-scope-packs]] [[feedback-parallel-chip-overlap]] [[project-m1-subproj2-godot-mirror]] [[project-session-closure-2026-05-21-m1m2]]
