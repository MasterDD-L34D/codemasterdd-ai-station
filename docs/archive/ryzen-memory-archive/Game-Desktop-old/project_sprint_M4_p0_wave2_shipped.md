---
name: Sprint M4 P0 Wave 2 + Wave 3 shipped
description: PR #1607 Wave 2 HUD + PR #1608 Wave 3 fix stack. 9 fix totali da 2 user playtest iter. Checkpoint sessione 2026-04-18/19.
type: project
originSessionId: bacbe4b9-9e50-4dd9-9a8a-c21fcdd04a8a
---
Stack branch: `feat/play-sprint-a-p0-hud-v2` (#1606) → `feat/play-sprint-a-p0-wave2-hud` (#1607) → `feat/play-sprint-a-p0-wave3-fx-range` (#1608).

**Why:** 2 user playtest iter iterative su enc_tutorial_01. Wave 2 shipped 6 HUD fix, run2 ha scoperto 5 gap UX critici (3 P0 NON HUD-cosmetic ma meccaniche-feedback core). Wave 3 ship 3/4 P0 in PR #1608.

**How to apply:** Prossima sessione → (a) verifica CI #1606+#1607+#1608 pass, (b) user playtest run3 port 5180 post merge #1608, (c) cattura eval set JSONL v0.3 (TKT-WAVE4-01 first), (d) merge chain quando approved.

## Wave 2 fix (PR #1607, commit bac64f5e +582/-7)

| # | Fix | File | Status |
|---|---|---|:-:|
| W2.1 | Help panel overlay + auto-open first run | `helpPanel.js` (new 136 LOC) | ✅ verified run2 |
| W2.2 | Fullscreen toggle header ⛶ | `main.js` +30 | ✅ |
| W2.3 | flashUnit + attackRay anim | `anim.js` +81 | ⚠️ wire incompleto (vedi W3.2/W3.3) |
| W2.4 | Job colors 7 classi | `ui.js`+`style.css`+`render.js` | ✅ |
| W2.5 | Hover tooltip | `main.js` buildUnitTooltip | ✅ stub intent |
| W2.6 | Safe zone no-op | — | — |

## Wave 3 fix (PR #1608, commit 01917041 + face8913, +86/-23)

Post user playtest run2 (sessione `a724991e…`, enc_tutorial_01 win), user segnala 5 gap:

| # | Gap user verbatim | Fix Wave 3 |
|---|---|:-:|
| 1 | "ancora round non sono simultanei" | **W3.1** `useRoundFlow` default ON, opt-out 'sequential' |
| 2 | "attacchi non mostrano effetti visivi né numerici" | **W3.2** commit-round handler wire `processIaActions(player+ia actions)` |
| 3 | "non mi indicano cosa è successo" | **W3.3** stessa W3.2 (damage popup via pushPopup) |
| 4 | "mouse non animato" | ⏸️ SKIP (P2, Wave 4 backlog) |
| 5 | "no casele attacare/muoversi quando selezioni" | **W3.5** `drawRangeOverlay` (move Manhattan ≤AP blu, attack Chebyshev ≤range rosso) |

### W3.2/W3.3 root cause found

`publicSessionView` (sessionHelpers.js:203) expose `log_events_count` ma **NOT `events[]`**. Frontend `processNewEvents` leggeva `newWorld.events = undefined` → flashUnit/attackRay/pushPopup MAI chiamati in simultaneous flow. Legacy flow funzionava via `ia_actions` in `/turn/end` response.

Fix frontend-side (minimal change): wire `processIaActions([...player_actions, ...ia_actions])` in commit-round handler. Shape compatibile (stessa bucket struct in `buildUnifiedRoundResolver`).

## Residual gap / follow-up

1. **Fix #4 mouse cursor anim** — Wave 4 backlog. CSS `cursor: crosshair` su canvas + hover pulse.
2. **Eval set Flint v0.3 capture** — **TKT-WAVE4-01 blocker** per prossimo playtest. JSONL auto-capture via `/api/session/log-decision` endpoint nuovo.
3. **Backend `publicSessionView` expose `events[]` tail** — robustness alternative a player_actions wire. Backlog Wave 5.
4. **Tooltip intent real** da `threat_preview` payload quando ADR-2026-04-18 Plan-Reveal implementato.
5. **PR stack rebase chain** — se #1606 merge first, #1607 + #1608 auto-rebase. Ricorda pattern §13 feedback_claude_workflow_consolidated.md.
6. **Governance drift unrelated** — `reports/docs/governance_drift_report.json` modified non staged (noise).

## Verify Wave 3

Browser test session `a724991e…` post unit select p_scout:
- `movePx = 57100` (~14 move-range tiles tinted blu)
- `attackPx = 3048` (~2 enemy cells Chebyshev ≤ range 2 tinted rosso)
- localStorage flag `simultaneous` default ON

## Baseline test status

- Node AI 197/197 · Python rules 196/196 · Session engine 309/309 (baseline pre-sessione)
- **Wave 3 NO automated test added** — render.js drawRangeOverlay pure function, main.js wire trivial. Verificato via browser pixel diff.
- Test totali ~710+ unchanged

## Next session handoff

1. `gh pr view 1606 --json statusCheckRollup` verifica CI base branch
2. `gh pr view 1607 --json statusCheckRollup` verifica CI Wave 2
3. `gh pr view 1608 --json statusCheckRollup` verifica CI Wave 3
4. Se tutti pass + user disponibile → user playtest run3 port 5180 post-merge
5. Implementa TKT-WAVE4-01 eval set JSONL capture PRIMA di run3
6. Fix #4 mouse cursor anim (Wave 4 CSS-only, S effort)

## Server running state

- `play` port 5180 serverId `e00c339e-068f-487b-92d8-2b68b3fdddef`
- `backend` port 3334 serverId `c1700de3-b2f0-49b2-b109-7cc1a71091d7`
- Entrambi live dal 2026-04-18, uptime >24h

## Cross-ref

- [docs/playtest/2026-04-18-M4-user-playtest-enc_tutorial_01.md](../../../Desktop/Game/docs/playtest/2026-04-18-M4-user-playtest-enc_tutorial_01.md) — run1 Wave 2 baseline
- [docs/playtest/2026-04-19-M4-run2-ux-gaps.md](../../../Desktop/Game/docs/playtest/2026-04-19-M4-run2-ux-gaps.md) — run2 + Wave 3 fix
