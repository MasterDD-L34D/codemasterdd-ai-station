---
name: Cross-stack port wave 2026-05-11 (9 PR shipped session)
description: Sessione auto-mode 9 PR cross-stack port Game/ → Godot v2 — pillar P2+P6 flip 🟡→⚪, 3-layer profilo psicologico LIVE, +130 GUT
type: project
originSessionId: c77e9715-286a-45d7-9987-55a73d50a206
---
## State after auto-mode session 2026-05-11 sera

9 PR shipped + merged:
- #221 TKT-PRESSURE-TIER-ENCOUNTER (vault ADR P0)
- #223 JobCardPanel design call + pillar-status correction
- #224 TKT-M14-A elevation+terrain modifier (P1)
- #225 TKT-P6 rewind buffer (P6 anti-frustration)
- #226 TKT-M15 promotion engine (P3 FFT ladder)
- #227 TKT-M14-B Phase A Conviction (P4 3-axis)
- #228 TKT-P2 Brigandine Phase A seasonal (P2)
- #229 TKT-P2 Phase B content+catalog (P2)
- #230 TKT-M14-B Phase B Conviction dialogue 5 branches (P4)

**Why**: master-dd green-lit auto-mode → "dobbiamo farle tutte 5" → continuous cross-stack port pipeline. Game/ side aveva shipped 8 ticket 2026-05-11 (PR #2242-#2253), zero ported Godot v2 pre-wave. Post-wave 8/8 ported.

**How to apply**:

1. **Cross-stack pattern proven**: pure engine + tests + catalog Resource + doc.md per ogni ticket. 1-2h per port. Caller wire deferred per scope guardrail + master-dd schema gate.

2. **Resume trigger** (CLAUDE.md sprint context aggiornato):
   > "Cross-stack engine + content layer wave 2026-05-11 CLOSED — 9 PR shipped, 8/8 Game/ tickets ported, 3-layer profilo psicologico LIVE..."

3. **Next session candidati**:
   - Playtest #2 userland validation (docs/playtest/2026-05-11-playtest-2-plan.md)
   - Caller wire sprints post master-dd schema decisions
   - JobCardPanel UX (PR #223 design call)
   - DialogueBranchView UI scene + button binding (post Conviction Phase B)
   - DebriefView PromotionPanel (post M15 caller wire decision)

**Pillar status post-wave**:
- P1 Tattica ⚪ + M14-A engine
- P2 Evoluzione ⚪ (flip 🟡→⚪) + seasonal engine + content
- P3 Identità ⚪ + promotion engine
- P4 Temperamenti ⚪ + Conviction 3-axis + dialogue branches (3-layer psicologico FULL: MBTI+Ennea+Conviction)
- P5 Co-op ⚪ unchanged
- P6 Fairness ⚪ (flip 🟡→⚪) + pressure_tier_floor + rewind buffer

**Tests cumulati**: +130 new GUT tests local pass. Wave compresa #221 +24 / #224 +15 / #225 +14 / #226 +17 / #227 +18 / #228 +16 / #229 +13 / #230 +13.

**Doc ledger canonical**: `docs/godot-v2/sprint-cross-stack-port-wave-2026-05-11.md`.
