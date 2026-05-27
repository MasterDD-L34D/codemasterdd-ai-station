---
name: project-pr-284-cascade-closure
description: PR
metadata: 
  node_type: memory
  type: project
  originSessionId: 7c08f071-f7f8-4cf0-a16b-fcd6aba717fa
---

PR #284 addendum-2 cascade CLOSED 2026-05-20 via 11 merged PR. Single session execution: spec → ultrareview → integrate → P0 → P1 → P2 → hotfix → final cascade.

**Why:** Eduardo failure points (a/b/c/d/e) on phone/TV bible-conformance audit (DRAFT spec #284). Master-dd authorized "procedi" then "pronto" then "procedi" then "procedi sempre con aiuto tool" sequence executing gate-4 P0+P1+P2 autonomous.

**How to apply:** When resuming session post 2026-05-20 cascade:

- main HEAD `b15933f` Merge #296. 11 PR merged total.
- PR #284 SPEC remains **DRAFT** (living doc). Master-dd decides close vs merge.
- **P2-5 deferred**: remove phone create-room post master-dd TV-canonical-in-prod manual smoke confirm.
- **P1-3 re-evaluation deferred**: re-introduce `OS.is_debug_build()` gate on host buttons (`_install_host_start_button_if_needed` + `_install_host_world_confirm_button_if_needed`) once master-dd validates TV `phase_change` reliably drives in prod release. Currently reverted to text-rename only (drop `(host)` suffix).
- **Visual smoke iOS Safari pending master-dd**: verify biome-tint visible + conn indicator render + radar fade-in tween + composer transition fade + neighbor stagger + CompanionPicker fallback rendering.

**Cascade PR ledger:**
| Wave | PR | Topic | SHA |
|---|---|---|---|
| Spec | #284 | addendum-2 verification | `606a216` (DRAFT) |
| P0 | #287 | build_web.sh BOTH modes | `b287ce1` |
| P0 | #288 | deploy-quick.sh TV pipeline | `cedcd65` |
| P0 | #289 | phone theme + StatusLabel gate | `5ca1bfc` |
| P1 | #290 | TV LobbyView CompanionPanel | `d523b9f` |
| P1 | #292 | phone composer biome-reactive bg | `c2eb460` |
| Hotfix | #293 | LOC cap overflow | `830b5d4` |
| P1 | #291 | phone lobby redesign (rebased ×2) | `6965782` |
| P2 | #294 | RadarPolygon fade-in tween | `61761c6` |
| P2 | #295 | composer transition system | `e640045` |
| P2 | #296 | world reveal stagger + CompanionPicker wire | `b15933f` |

**Helper modules introduced (extraction pattern):**
- `scripts/phone/composer_biome_tint.gd` (62 LOC, PR #292)
- `scripts/phone/composer_transition_runner.gd` (55 LOC, PR #295)
- `scripts/ui/canvas_transition.gd` (69 LOC, PR #295)
- `scripts/ui/companion_resolver.gd` (43 LOC, PR #296)
- `scripts/ui/world_reveal_motion.gd` (41 LOC, PR #296)

**Already-shipped discoveries (saved rework):**
- P1-4 RoomCodeLabel `label_hero` — W-Tokens-Phase-2 (PR #290 minimal CompanionPanel-only)
- P0-3 sub-task 4 Express `/` mount — `app.js:433` static publicDir pre-existing (cross-repo work eliminated)
- P2-4 phone lobby identity-first — B-NEW-10 fix 2026-05-09 + #291 RoomCodeDisplay (branch discarded)

**BLOCKERS caught pre-merge:**
- #289 `_set_status` default semantic-inversion (peer review) → fix commit `dce8d6f`
- #292 P1-3 gate + tween lambda guard (peer review) → fix commit `6548e73`

Related: [[feedback-loc-sum-check]] [[feedback-peer-review-blocker-pattern]]
