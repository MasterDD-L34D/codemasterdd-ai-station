# QUALITY -- agent-scanner LITE skill

> Quality Gate evidence per CLAUDE.md (`Quality Gate -- Release Standard`).

## Step 1 -- Smoke Test

| Check | Command | Expected | Result | Date |
|-------|---------|----------|--------|------|
| 19 unit tests pass | `.\scripts\setup\deploy-global-skills.Tests.ps1` | `Results: 19 passed, 0 failed`, exit 0 | PASS | 2026-05-28 |
| Sandbox QG green | `.\scripts\setup\deploy-global-skills.ps1 -Apply` (throwaway USERPROFILE) | `[sandbox OK]` printed | PASS | 2026-05-28 (T8 + T9 + T11) |
| Live `-Apply` Lenovo | `.\scripts\setup\deploy-global-skills.ps1 -Apply` (real) | All 3 phases green + `DONE` | PASS (commit 0c6b405) | 2026-05-28 |
| Idempotency live | 2nd `-Apply` | hash pre == hash post | PASS | 2026-05-28 (T11 Step 4) |
| -Remove rollback sandbox | -Apply then -Remove against throwaway | bounded strip, user content preserved | PASS (T14) | 2026-05-28 |

## Step 2 -- Indagine di Ricerca (>=3 edge case)

| Edge case | Behavior | Verified |
|-----------|----------|----------|
| Frontmatter malformato in agent file | SKILL.md says log `MALFORMED FRONTMATTER: <path>`, skip, continua | Documented in SKILL.md Step 1; manual smoke required if a real malformed agent file appears |
| Permission denied on source dir | Log `SOURCE UNREADABLE: <path>` (NOT silent-empty) | Documented in SKILL.md Step 1 |
| AA01 source 7 absent on non-Lenovo PC | Silently omit source 7, NOT error | Test 7 PASS (2026-05-28) |
| Inventory >50 agents | Hard cap 50 + ranked by source-priority + `+N more` footer | Documented in SKILL.md Step 3; smoke required when inventory reaches threshold |
| Sentinel false-positive (start match but Rule (STRONG missing) | Returns 'ambiguous', logs `.apply-blocked-<ts>.log`, exit 4 | Test 4 PASS |
| -Remove with user content post-directive | User content survives (P0#3 harsh) | Test 5 PASS + T14 sandbox smoke |
| -Remove with end sentinel missing (legacy) | Falls back to latest `.bak` restore | Implemented in `Invoke-Rollback`; smoke required |
| Sandbox idempotency violation | Sandbox fails red, exit 5, NO live write | Implemented in Invoke-SandboxQG run-2 diff check |

## Step 3 -- Tuning & Ottimizzazione

| Iter | Misurazione | Before | After | Delta |
|------|-------------|--------|-------|-------|
| Baseline | Token cost per invocation (T12 plan: behavioral smoke 3-prompt) | pending | pending | pending |
| Baseline | Time-to-output | pending | pending | pending |
| Tuning trigger | Per spec sec 10 R1: post N=5 sessions Lenovo + N=5 Ryzen, if mean fire-rate >50% on non-selection OR mean tokens-per-fire >2000 -> tune description keywords | -- | -- | -- |

Iteration deferred until baseline data captured (T12 behavioral smoke + post-deploy first 5 sessions each PC).

## Step 4 -- Released

- [x] Step 1 smoke complete (5/5 PASS).
- [x] Step 2 research (8 edge cases documented; 4 verified via tests, 4 documented in SKILL.md + smoke required as inventory/conditions emerge).
- [ ] Step 3 tuning -- pending baseline capture (T12 plan).
- [x] Lenovo live deploy green (T11 `0c6b405`).
- [ ] Ryzen cross-fleet deploy (T13 plan: Eduardo-direct).

Production status: **LIVE on Lenovo**. Cross-fleet mirror (Ryzen) pending Eduardo execution of T13.
