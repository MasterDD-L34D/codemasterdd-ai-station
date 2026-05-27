---
name: project-adr-2026-05-18-sistema-learning-briefing
description: ADR-2026-05-18 Sistema persistent-state learning L2 — master-dd verdict A/B/C briefing pre-decision. Cross-stack Game/-side. Cronaca event_log feed ready. Engine pre-reqs MISSING. Audit 2026-05-20 recommended B pilot.
metadata:
  node_type: memory
  type: project
  originSessionId: 7c08f071-f7f8-4cf0-a16b-fcd6aba717fa
---

ADR `C:/dev/Game/docs/adr/ADR-2026-05-18-sistema-persistent-state-learning.md` — DRAFT, no code, master-dd verdict pending.

**Audit verdict 2026-05-20**: Option B pilot recommended (3-4h). Option A full = 9h with HIGH balance risk (4 interacting FSMs cascade). Option C defer = 0h passive Cronaca accumulation.

## ADR scope quick-recap

Sistema (enemy AI) cross-session persistent learning — Sistema impara tattiche giocatore tra encounter + contra-strategie. DF L2 maximum differentiator. 4 buckets proposed:
1. **units_observed**: kills_vs_sistema + sightings per unit_id
2. **tactics_observed**: player tactic types (flanking / focus_fire / spread) per encounter
3. **factions**: morale + bounty cascade by faction
4. **strategic_phase**: FSM 1..5 escalation

## Engine ground-truth (verified 2026-05-20 audit)

### Game/-side MISSING

- `/end` route hook in `apps/backend/routes/session.js` post-`scoreSession()` — NEEDED for accumulator call
- `apps/backend/services/ai/sistemaStateAccumulator.js` — NEEDED (~80 LOC for B pilot)
- Prisma `SistemaState` model + migration — NEEDED (1 JSONB col for B, multi-col for A)
- `apps/backend/services/campaign/campaignLoader.js` injection of `session.sistema_state_persistent` — NEEDED at combat start
- `apps/backend/services/ai/declareSistemaIntents.js` optional `persistent_tactics` arg — NEEDED for A only

### Cronaca signals sufficient B (verified Phase 1 + 1.5 ship)

- `outcome: "kill"` / `wound_permanent` — CronacaPanel `_is_significant` line 129
- `damage_dealt` integer — line 133
- `status_applied` string — line 131
- `mutation_trigger` / `lineage_event` — lines 140-141
- `actor_id` / `target_id` per event — line 107

**Tactics bucket gap** (Option A only): `tactics_observed` requires NEW `session.events` emit shape — not in current Cronaca v1.1.

## 3 Options decision matrix

| | **A — Full** | **B — Pilot (Recommended)** | **C — Defer** |
|---|:--:|:--:|:--:|
| Scope | 4 buckets cascade | units_observed + threat only | passive Cronaca accumulation |
| Effort cross-stack | ~9h | **~3-4h** | 0h |
| Prisma | New `SistemaState` multi-col model + migration | Lighter 1-2 JSONB col | None |
| Seams missing pre-req | All 4 (route hook, accumulator, loader, declareSistemaIntents arg) | Same 4 lighter footprint | None |
| Balance risk | HIGH (4 FSM cascade interact: morale × phase × bounty × counter-tactic) | LOW (single counter bounded effect) | NONE |
| Determinism replay | snapshot+seed required, non-trivial | Same risk bounded to 1 counter | N/A |
| Playtest pre-req | YES required (multi-cycle) | YES (single cycle) | NO (passive collection) |
| Blocks anything? | Non-blocking M1 (ADR §Scope: "observational") | Same | Same |
| Master-dd checkpoint | YES (high risk) | YES (B pilot also gated 🟡) | NO |

## Recommended verdict: B pilot

**Why**:
1. Cronaca signals cover B fully today (kill + damage fields exist)
2. Option A tactics_observed bucket requires NEW `declareSistemaIntents` emit shape — 2-step dependency vs 1-step for B
3. Balance risk on A non-trivial (4 interacting FSMs explicit per ADR §Risks #5)
4. ~3-4h vs ~9h: B ships faster, validates whether persistent learning actually changes feel BEFORE full investment
5. B is additive upgrade path — A layerable on top if B engaging
6. NO playtest data yet (playtest #2 not executed per CLAUDE.md master-dd queue item #3); shipping A blind = gamble

## Option B concrete next step (if master-dd chooses B)

1. **Prisma model** `SistemaState` — 1 JSONB col `units_observed` only (skip factions/phase)
2. **Service** `apps/backend/services/ai/sistemaStateAccumulator.js` ~80 LOC — reads `session.events`, aggregates `kills_vs_sistema` + `sightings` per unit_id
3. **Route hook** `apps/backend/routes/session.js` `/end` post-`scoreSession()` — calls accumulator, upserts Prisma record
4. **Loader** `apps/backend/services/campaign/campaignLoader.js` — attach `sistema_state.units_observed` to session at load
5. **AI dispatch** `apps/backend/services/ai/declareSistemaIntents.js` — optional arg: if `unit_id` in `high_threat`, bias `defend` weight +20%
6. **Migration** Postgres + 1 integration test
7. **Estimated**: 3-4h, gate 🟡 CHECKPOINT (opt-arg on AI core)
8. **Cross-stack mirror**: D2-C pattern shipped 2026-05-13 — same Game/ → Godot v2 ↔ Postgres mirror

## Option A escalation conditions (if master-dd chose A)

`tactics_observed` bucket requires:
- New emit in `declareSistemaIntents.js` (tactic-type field NOT in current `session.events`)
- 🟡 CHECKPOINT gate per `schema-ripple` agent (tactic propagates to session.events, Prisma, accumulator, dispatcher)
- Pre-flight: schema migration design + 1 playtest cycle to validate signal-noise ratio

## Cronaca cross-stack mirror status

Engine LIVE post Phase 1.5a: `CampaignState.to_payload()` includes `event_log` + `bond_pairs` in serialized dict. `CampaignApi.put_godot_v2_state` (D2-C shipped 2026-05-13) PUT cross-stack. Game/-side Prisma schema for these JSONB cols would extend D2-C pattern to capture full Cronaca dump for offline analysis.

Future ADR-Sistema may consume Cronaca cross-stack dumps as input signal source.

## Decision tree master-dd

```
Playtest #2 executed?
├── NO → Option C (defer) recommended — collect data passive first
└── YES + signal shows persistent learning would change feel
    ├── YES → Option B pilot (3-4h, single counter)
    │         └── validates → Option A full layered on B base later
    └── NO  → Option C (defer indefinitely, P5 stays 🟡)
```

## Risks register

- **ADR Risk #1**: Determinism replay → snapshot+seed required. Mitigated in B (single counter bounded).
- **ADR Risk #2**: Faction morale cascade balance unpredictable. Option A only.
- **ADR Risk #3**: Strategic_phase FSM lock-in vs player escalation pace. Option A only.
- **ADR Risk #4**: `/end` seam finality vs idempotency. Check ADR-2026-04-16 before wiring.
- **ADR Risk #5**: Playtest dependency (1 cycle B / multi cycle A).

## References

- ADR path: `C:/dev/Game/docs/adr/ADR-2026-05-18-sistema-persistent-state-learning.md`
- D2-C cross-stack pattern: PR #253 #254 #2259 #256 (2026-05-13 wave)
- Cronaca engine path: PR #314 (engine), #315 (snapshot), #316 (voice)
- Audit 2026-05-20 sera (balance-illuminator agent) — full ground-truth survey
- CLAUDE.md sprint context PR #323 post-wave

Related: [[project-p4-storytelling-cascade-2026-05-20]] [[feedback-codex-post-cascade-audit]]
