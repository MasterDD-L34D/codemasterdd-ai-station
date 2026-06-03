# Jules suggestions snapshot 2026-06-03 (READ-ONLY; Start = Eduardo)

> **BASELINE, not a live sweep.** No Claude-connected browser was available this
> session (`list_connected_browsers` -> `[]`), so this carries the last-known
> inventory from the sec-9 finding (`docs/jules/JULES-CAPABILITIES-MASTER.md`,
> live sweep 2026-06-02) -- NOT fresh 2026-06-03 data. Refresh via
> `docs/runbook/jules-suggestions-snapshot.md` once Eduardo's Chrome is connected.
> Verdicts are ADVISORY stubs for a human/triage pass. Start / edit+submit /
> close / toggle = Eduardo (SDMG R6). Source: jules.google per-repo (no API).

## Enabled repos (4): suggestions surface

### Game-Database
- **[Security]** Unvalidated headers
  - VERDICT-STUB: **likely-resolved-verify** -- CWE-290 role-spoof / header trust
    fixed + merged (PR #170, authContext-authoritative). Ground-truth before acting.
- **[Security]** Missing rate-limit
  - VERDICT-STUB: **likely-resolved-verify** -- mutation-scoped rate-limit merged
    (PR #169). Confirm the suggestion is stale on next live sweep.

### codemasterdd-ai-station
- **[Security]** "API Secret Exposure to Frontend"
  - VERDICT-STUB: **triage** -- no known PR; verify independently (could be a
    false-positive on a public config or a real leak). Ground-truth the cited file.

### Game
- **[Code Health]** Unused imports (os / sys)
  - VERDICT-STUB: **likely-resolved-verify** -- a cleanup pass removed 11 unused
    imports (PR #267); confirm scope overlap, drop if covered.
- **[Code Health]** Duplication `flint_status_stdlib.py`
  - VERDICT-STUB: **drop** -- the apparent duplication is a DELIBERATE stdlib-only
    fallback; a prior Jules dedup of it would have broken CI (design-intent catch,
    memory `feedback_jules_autonomous_loop_2026_06_02`). Do NOT dedup.

### Game-Godot-v2
- (no sample captured in the sec-9 baseline; enumerate on the next live sweep.)

## Repos OFF / not-configured
- **OFF (3 configured):** compass-marketplace, evo-swarm, evo-tactics-refs-meta.
- **Not-configured (4 in selector):** Gpt, Item-generator, LeaD, Master-DD-Pathfinder-GPT.

## Triage notes
- **edit-before-Start**: the generic "Start" template is a "Code Health Improvement
  Task" boilerplate WITHOUT our anti-#10 / anti-S5 constraints. For any high-signal
  suggestion that survives triage, Eduardo uses "edit" to paste the guard-rail
  (zero-behavior, single-file, minimal-diff/no-rewrite, grep-before-remove, lock-test
  CI-green) THEN Starts -- so the suggestion inherits the scoped-prompt discipline.
- **Mechanics (beta):** opt-in per repo, cap <=5, refresh every few days, PRO plan
  Gemini 3.1 Pro, daily session limit 0/100. Categories: Cleanup / Performance /
  Security / Code Health / Testing. Expanded chevron = DESCRIPTION + LOCATION
  (file:line) + RATIONALE + CODE CONTEXT (e.g. duplication via AST hashing cross-file).
