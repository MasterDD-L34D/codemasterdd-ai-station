---
name: project-p4-storytelling-cascade-2026-05-20
description: P4 storytelling sprint Cronaca + Custode voice + Named L3 + Bond L4 cascade 7 PR sera 2026-05-20. DF L2+L3+L4 flipped engine + surface + voice. Audit-driven verdict converged from 3 parallel agents.
metadata:
  node_type: memory
  type: project
  originSessionId: 7c08f071-f7f8-4cf0-a16b-fcd6aba717fa
---

P4 storytelling sprint sera 2026-05-20 = 7 PR cascade chiusura wave DF L2/L3/L4 ❌→✅ end-to-end. Master-dd verdict "merge historical + audit profondo + procedi criterio + usa tool" → audit 3 agent paralleli (repo-archaeologist + evo-tactics-domain-specialist + narrative-design-illuminator) convergono su Cronaca MVP recommendation → 7 PR ship.

**Wave PR ledger:**

| PR | Topic | Main SHA | DF Level |
|----|---|---|---|
| #284 | design-conformance gap report (historical merge) | `a19e8dd` | meta |
| #313 | Eval A FULL CLOSURE (WASM async resolved) | `0008441` | infra |
| #314 | Cronaca event_log Phase 1 engine | `28248d5` | L2 engine |
| #315 | Cronaca DebriefView Phase 1.5a surface | `afad47b` | L2 surface |
| #316 | Custode voice Phase 1.5b GDTracery | `8f2aacf` | L2 atmosphere |
| #317 | Named Mutations Phase 2 L3 Wildermyth | `190e050` | L3 |
| #318 | Bond Engine Phase 3 L4 XCOM | `4bd3a45` | L4 |

**Engine assembled post-cascade:**
- `CampaignState.event_log` Cronaca append-only Rimworld/DF Legends pattern (500 FIFO cap)
- `CampaignState.event_log_snapshot` DebriefState deep-copy snapshot (per-PG 200 cap)
- `CampaignState.bond_pairs` D2-B JSON cross-session bond persistence
- `CronacaPanel` TabContainer + filter chips (Tutti/Significant/Lineage) + per-PG cards
- `CronacaTextRenderer` (Phase 1.5a placeholder, unused post 1.5b but preserved)
- `CustodeVoiceEngine` GDTracery wrapper Italian 25+ template variants
- `LineagePropagator._pool_meta` parallel store inherited_from + biome_origin
- `BondEngine` pair_key normalized + process_encounter + apply_to_campaign threshold
- `CombatLifecycleHook._on_session_ended` enriched: flush → lineage emit → bond emit → bind → clear

**Cronaca v1.1 schema fully populated:**
- `ts, actor_id, action_class, target_id, encounter_id, biome_id, outcome, damage_dealt, status_applied, mutation_trigger, lineage_event, display_name`
- Schema reservations (mutation_trigger + lineage_event) honored via Phase 2/3 emit

**CustodeVoice routing precedence (final):**
1. lineage_event in {mutation_propagated, mutation_inherited, bond_formed} → body_lineage_*/body_bond_formed
2. status_applied != "" → body_status
3. outcome match → body_attack_*
4. fallback → body_fallback

**Audit converged recommendation 2026-05-20 = ship reality:**
- Cronaca MVP first (no master-dd checkpoint, multiplier on 4 engines already LIVE)
- Skip ADR-2026-05-18 Sistema-learning Phase 4 (gated)
- Skip asset W7 (external commission)
- Sequencing: Cronaca → Named → Bond proved 100% (each subsequent reads previous data)

**Workflow superpowers cascade pattern:**
- using-superpowers (intro)
- brainstorming (1 critical question per phase scope)
- writing-plans (bite-sized TDD 3-7 tasks)
- subagent-driven-development (fresh implementer per task + 2-stage review for foundational, single review for incremental)
- ~25-30 subagent dispatches total wave, 100% APPROVED post-spec-fix

**Anti-pattern guards enforced:**
- #8 ADOPT-shallow → GDTracery G2 smoke isolated PASS 7/7 BEFORE adoption (test_tracery_g2_smoke.gd)
- #83 P1 (Codex) ledger.clear AFTER ALL flush/emit/bind operations
- #10 LOC cap pre-merge stack check (debrief_view 290 / combat_lifecycle_hook 430 / cronaca_panel 189 — well under 1000)
- DRY/YAGNI: pair_key lex normalize avoids duplicate counters

**DF coverage delta:**
| Level | Pre 2026-05-20 sera | Post #318 |
|---|:--:|:--:|
| L0 sim | ✅ | ✅ |
| L1 identity | ✅ engine | ✅ + Custode voice + named heirloom |
| L2 mondo-ricorda | ❌ | ✅ engine + surface + atmosphere + lineage + bond events |
| L3 named-mut | ❌ | ✅ Wildermyth |
| L4 bond | ❌ | ✅ XCOM cross-battle |
| L5 losing-fun | ✅ | ✅ |

**Sample player payoff visible:**
- "skiv_7 ha trafitto anguis_3 — 14 danni inflitti nelle terre di Savana durante S4-T23."
- "skiv_3 ha lasciato Scaglie Rigenerative al lignaggio della Savana durante S1-T20."
- "Il Custode ha visto: skiv_3 riconosce skiv_5 come fratello del lignaggio durante S3-T18."

**GUT cumulative delta:** ~2510 pre-session → 2603 pass post-#318 (+93 tests / +120+ asserts, zero regression).

**Deferred queue post-cascade:**
- Phase 3.5 AI behavior modifier (SisPolicy intent_weight bond defense bias) + BattleFeed bond defense trigger + bond_broken on death — tocca RoundOrchestrator combat path
- Phase 4 ADR-2026-05-18 Sistema-learning L2 — gated master-dd verdict A/B/C
- Phase 5/2.5 inherit-side Cronaca emit (mutation_inherited) — requires CombatSession unit spawn hook
- Codex automated review iter su 5 PRs Cronaca chain
- User visual smoke deploy iOS Safari via Cloudflare tunnel `evo-tactics.com`

**Lesson codified:**
1. Audit BEFORE next sprint quando suspected scope creep — 3 agent paralleli converging verdict beats 1 deep agent
2. Phase-incremental shipping (1.5a/1.5b/2a/2b/2c/3a/3b/3c) lower risk than bundle PR
3. Engine LIVE / Surface DEAD anti-pattern catchable via Gate-5 audit (P2/P3/P4 surface flips post Cronaca consumer)
4. Cronaca = "world remembers" pattern is MULTIPLIER for L3/L4 — build first
5. GDTracery + G2 smoke gate viable adoption when external dep needed (Italian grammar variation impossible pure-GDScript at 12+ rule scale without library)

Related: [[feedback-chrome-mcp-visual-loop]] [[feedback-godot-wasm-recurring-callback]] [[project-pr-284-cascade-closure]] [[feedback-loc-sum-check]] [[feedback-peer-review-blocker-pattern]]
