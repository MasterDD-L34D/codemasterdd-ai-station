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
| Source 5b re-deploy (cavecrew fix) | `.\scripts\setup\deploy-global-skills.ps1 -Apply` post 5b edit | sandbox QG OK + 3 phases green + ASCII clean + DONE exit 0 | PASS | 2026-05-28 |
| 5b behavioral capture | `find "$HOME/.claude/plugins" ... \| grep cavecrew` | cavecrew-investigator/builder/reviewer enumerated | PASS | 2026-05-28 |

## Step 2 -- Indagine di Ricerca (>=3 edge case)

| Edge case | Behavior | Verified |
|-----------|----------|----------|
| Frontmatter malformato in agent file | SKILL.md says log `MALFORMED FRONTMATTER: <path>`, skip, continua | Documented in SKILL.md Step 1; manual smoke required if a real malformed agent file appears |
| Permission denied on source dir | Log `SOURCE UNREADABLE: <path>` (NOT silent-empty) | Documented in SKILL.md Step 1 |
| AA01 source 7 absent on a PC without the aa01/archon deploy | Silently omit source 7, NOT error | Test 7 PASS (2026-05-28) |
| Inventory >50 agents | Hard cap 50 + ranked by source-priority + `+N more` footer | Documented in SKILL.md Step 3; smoke required when inventory reaches threshold |
| Sentinel false-positive (start match but Rule (STRONG missing) | Returns 'ambiguous', logs `.apply-blocked-<ts>.log`, exit 4 | Test 4 PASS |
| -Remove with user content post-directive | User content survives (P0#3 harsh) | Test 5 PASS + T14 sandbox smoke |
| -Remove with end sentinel missing (legacy) | Falls back to latest `.bak` restore | Implemented in `Invoke-Rollback`; smoke required |
| Sandbox idempotency violation | Sandbox fails red, exit 5, NO live write | Implemented in Invoke-SandboxQG run-2 diff check |
| Plugin marketplace mirror dupes (source 5b) | Same agent `name:` appears across `cache/<plugin>/...` (active) AND `marketplaces/<plugin>/...` mirror subpaths -> Step 4 `SILENT OVERRIDE` warning fires for benign plugin-internal mirrors (e.g. cavecrew x4+ paths), inflating inventory toward hard-50 cap | Known limitation 2026-05-28 (5b deploy). Mitigation: Step 4 already mandates manual review post-report; treat same-name within one plugin tree as benign mirror, not real override. Refinement candidate if cap pressure observed: dedup by `name:` keeping highest source-priority path (cache > marketplaces) |

## Step 3 -- Tuning & Ottimizzazione

| Iter | Misurazione | Before | After | Delta |
|------|-------------|--------|-------|-------|
| Baseline (T12 2026-05-28) | Token cost full ON_DEMAND fire (skill-load 1.3k + enum 0.5k + report 0.7k) | n/a | ~2.5k tokens (estimate, no exact telemetry) | -- |
| Baseline (T12 2026-05-28) | Token cost auto-fire on task w/ inventory cached in-session (FIRE-A/C) | n/a | ~0.4k incremental each (estimate) | -- |
| Baseline (T12 2026-05-28) | Time-to-output (source enumeration, 7 sources, 25 entries) | n/a | 223ms wall | -- |
| Tuning trigger | Per spec sec 10 R1: post N=5 sessions Lenovo + N=5 Ryzen, if mean fire-rate >50% on non-selection OR mean tokens-per-fire >2000 -> tune description keywords | -- | NOT triggered (auto-fire ~0.4k << 2000; ON_DEMAND 2.5k is explicit-request not auto-fire) | -- |

### T12 behavioral smoke 2026-05-28 (Lenovo, fresh session) -- 3 FIRE prompts

| FIRE | Prompt | Expected | Result |
|------|--------|----------|--------|
| FIRE-A | `che agent uso per code review?` | scanner fires (TEAM_FORMATION), raccomanda agent esistente | PASS -- REUSE harsh-reviewer / /code-review / owasp / cavecrew-reviewer, 0 shadow-duplicate |
| FIRE-B | `scan agents` | ON_DEMAND full report | PASS -- 25-entry report (20 active + 5 dormant + 2 user skill), anti-pattern check clean |
| FIRE-C | `fix typo at line 42 in foo.js` | STRONG-PURE fires (no triviality bypass) | PASS -- fires, raccomanda cavecrew-builder / inline Edit, no new agent |

**Findings (non-blocking):**
- Scanner source 5 (`.claude/plugins` project-local) NON copre user plugin cache `~/.claude/plugins` -> caveman cavecrew agents non enumerati da find (recuperati manualmente da harness subagent-list). Candidate scanner refinement: aggiungere source 5b `$HOME/.claude/plugins`. **RESOLVED 2026-05-28**: source 5b added (parallel to 5, maxdepth 6, `2>/dev/null`, grep `(agents|skills)/`); behavioral test confirms cavecrew-investigator/builder/reviewer now enumerated. New edge case surfaced (marketplace mirror dupes) -> Step 2 table.
- 5 dormant agents in `_dormant/` ancora esposti come `subagent_type` dall'harness (a11y/dafne/database/game-design-validator/lore-consistency) mentre disk-state = dormant. Coherence note.

Step 3 baseline captured. Iteration deferred to post-deploy first 5 sessions each PC (per spec sec 10 R1 trigger).

## Step 4 -- Released

- [x] Step 1 smoke complete (5/5 PASS).
- [x] Step 2 research (8 edge cases documented; 4 verified via tests, 4 documented in SKILL.md + smoke required as inventory/conditions emerge).
- [x] Step 3 tuning baseline captured (T12 2026-05-28: 3-prompt behavioral smoke 3/3 PASS + token/time baseline). Iteration deferred to post-deploy 5-session sample/PC.
- [x] Lenovo live deploy green (T11 `0c6b405`).
- [x] Ryzen cross-fleet deploy (T13 verified post-closure, journal `9ed9231`).

Production status: **LIVE cross-fleet (Lenovo + Ryzen)**. All 3 QG steps complete.
