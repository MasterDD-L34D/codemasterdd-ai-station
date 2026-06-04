---
name: Repo content audit 2026-05-05 (pre-cutover Phase A)
description: Static scan + triage results for Game/ + Game-Godot-v2 pre-cutover audit session. Phase 1+3 complete, Phase 2 pending.
type: project
originSessionId: a517688b-57fc-43f3-91c7-b62b8a5a7121
---
## Session outcome 2026-05-05 — Phase 1 static scan + Phase 3 triage

Phase 1 (3-agent parallel static scan) + Phase 3 (triage + cleanup PRs) executed. Phase 2 (live runtime probe) pending.

**Report canonical**: `docs/reports/2026-05-05-repo-audit-static-scan.md`

**Why:** Pre-cutover Phase A (ADR-2026-05-05 Scenario 3 STAGED canary) requires lean, intentional repo state. Handoff doc shipped prior session: `docs/planning/2026-05-05-repo-content-audit-handoff.md`.

**How to apply:** Next session — check PRs merged, then optionally Phase 2 runtime probe, then Phase 3 remaining tickets (conviction wire + buff_stat handler).

---

## Key findings

### Game/ backend — orphan services

- `aiPersonalityLoader.js` (121 LOC) — **deleted**. Zero runtime callers (test-only).
- `sistemaActor.js` — **deleted**. Zero runtime callers.
- `tests/services/aiPersonalityLoader.test.js` — **deleted** (test for deleted service).

### Game/ data — species biome_affinity (10 species fixed)

`biomeResonance.js:isPerfectMatch()` requires exact canonical biome slug. 10/15 species had generic habitat slugs → could never achieve Risonanza Perfetta.

**Fixed** (canonical biome ID per species biology):
- anguis_magnetica: `acquatico_costiero` → `atollo_obsidiana`
- chemnotela_toxica: `terrestre_forestale` → `foresta_acida`
- elastovaranus_hydrus: `terrestre_pianeggiante` → `pianura_salina_iperarida`
- gulogluteus_scutiger: `terrestre_roccioso` → `canyons_risonanti`
- perfusuas_pedes: `sotterraneo` → `caverna`
- proteus_plasma: `acquatico_dolce` → `palude`
- rupicapra_sensoria: `terrestre_montano` → `caldera_glaciale`
- soniptera_resonans: `terrestre_forestale` → `canopia_ionica`
- terracetus_ambulator: `terrestre_pianeggiante` → `steppe_algoritmiche`
- umbra_alaris: `terrestre_umido` → `dorsale_termale_tropicale`

### Game/ Gate 5 violations — 4 total (3 exempt, 1 TODO)

| Surface | Verdict | Note |
|---|---|---|
| `enneaEffects.js` | EXEMPT | Surface = vcScoring telemetry + debrief badge |
| `meta/eventChainScripting.js` | EXEMPT | Narrative infra deferred M18+ |
| `routes/speciesWiki.js` | EXEMPT | Dev-tooling surface, no player wiki |
| `routes/conviction.js` | **TODO** TKT-GATE5-CONVICTION | FE wire or deprecate (~4h) |

### Game-Godot-v2 — stub deleted

- `scripts/ai/stubs/sistema_turn_runner.gd` — **deleted** (Tier 3 abandon). SistemaIntents + RoundOrchestrator on Node side cover all functionality.

### YAML orphans — 51 ancestor traits with `buff_stat` kind

`active_effects.yaml` has 51 ancestor traits with `effect.kind: buff_stat` but `traitEffects.js` + `passiveStatusApplier.gd` have NO handler for this kind. 

**Note:** `legame_di_branco` / `spirito_combattivo` / `pack_tactics` were initially flagged as null stubs but are LIVE via `beastBondReaction.js` (different schema: `triggers_on_ally_attack` top-level key).

**Ticket**: TKT-TRAITS-ANCESTOR-BUFF-STAT (~3h: add `buff_stat` handler in `passiveStatusApplier.js`)

### services/rules/ Python engine

Pre-condition for Phase 3 removal: `tools/py/simulate_balance.py` must be ported or deleted.
**Ticket**: TKT-RULES-SIMULATE-BALANCE (~1h verify/port/delete)

---

## PRs opened (not yet merged)

| PR | Repo | Title | Status |
|---|---|---|---|
| #2058 | Game/ | fix(audit): pre-cutover cleanup 2026-05-05 | Open, awaiting merge |
| #177 | Game-Godot-v2 | fix(ai): drop sistema_turn_runner stub (Tier 3 abandon) | Open, awaiting merge |

Both require master-dd approval.

---

## Open tickets post-audit

| Ticket | Effort | Priority |
|---|---|---|
| TKT-GATE5-CONVICTION | ~4h | P1 (wire conviction voting FE or deprecate route+service) |
| TKT-TRAITS-ANCESTOR-BUFF-STAT | ~3h | P1 (buff_stat handler = 51 ancestor traits activated) |
| TKT-RULES-SIMULATE-BALANCE | ~1h | P2 (prerequisite for services/rules/ Phase 3 deletion) |

---

## Phase 2 runtime probe (pending)

Boot `deploy-quick.sh`, curl all routes, check trait fire log. Not blocking cutover but recommended before Phase A trigger.
