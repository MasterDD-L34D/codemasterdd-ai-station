# GOAL -- Close the Jules-collaboration autonomy gaps (2026-06-03)

> Self-contained handoff for a fresh session (`/goal`). Cold-start: read this + the
> pointers at the bottom; the prior session already ground-truthed the state below.
> Authority: ADR-0035 (+2026-06-03 addendum) · ORCHESTRATION.md (ADR-0036) ·
> `docs/superpowers/jules/JULES-CAPABILITIES-MASTER.md` §9 · memory `project_jules_collaboration_state`,
> `feedback_jules_autonomous_loop_2026_06_02`, `feedback_codex_clean_verdict_reaction`.

## State (ground-truthed 2026-06-03, do not re-discover)

The Jules **operational loop works** end-to-end: dispatch (`POST /v1alpha/sessions`,
`x-goog-api-key`, NO OAuth, runs on Ryzen) -> monitor (`/activities`) -> ground-truth
triage (extract `gitPatch`; COMPLETED+no-PR = S3 sandbox-stale, work trapped not empty)
-> recover/sovereign-extract -> PR -> merge (with explicit grant). Demonstrated: 6 PRs
merged in one session (#170/#169/#2577/#171/#2581), 2 S3-trapped recovered, sessions
archived. Standing-allow (no prompt, ORCHESTRATION §6): read-ops, `remote list/pull`,
`:archive`, `:sendMessage`. Queue currently clean (0 AWAITING, 0 open Jules PRs).

What is NOT yet autonomous / automated = the 6 gaps below. None blocking; each is a step
from "works on-demand" to "runs by itself".

## Work items (prioritized)

### G6 -- formalize `:create` (dispatch) in standing-list  [quick, doc]
- **Problem**: dispatch (`POST /sessions`) was adopted as a tier (ADR-0035) and demoed,
  but ORCHESTRATION §6 standing-allow lists only `:archive`/`:sendMessage`, not `:create`.
  Gray-zone (works, but not formally standing).
- **Action**: amend §6 -- add Jules `:create` to standing-allow **scoped to the ADR-0035
  hard-constraints** (scoped-prompt template + ASCII-clean target + whitelisted repo +
  mandatory ground-truth triage). OR explicitly keep it per-instance and say why.
- **Accept**: §6 names `:create` with its constraint or its gate, no ambiguity.

### G5 -- formalize Codex-unavailable -> harsh-reviewer substitute  [quick, doc]
- **Problem**: Codex auto-review can hit a usage cap (happened 2026-06-03 on #2581) ->
  external-review sub-gate can't run. Handled ad-hoc with a harsh-reviewer substitute.
- **Action**: amend ORCHESTRATION §5 Codex sub-gate: "Codex confirmed-unavailable
  (usage-limit comment ground-truthed, NOT a poll-miss) -> SUBSTITUTE harsh-reviewer
  (document it in the merge), do NOT skip/self-waive." (Already in memory
  `feedback_codex_clean_verdict_reaction` addendum -- promote to ORCHESTRATION.)
- **Accept**: §5 documents the substitution + the discriminators vs the #258 anti-pattern.

### G3 -- install the Jules daily-digest cron on the active PC  [concrete, build]
- **Problem**: `scripts/jules-daily-digest.ps1` exists but the scheduled task
  `jules-daily-digest` is NOT registered on Ryzen (last digest 2026-05-29). The
  enumerate-sessions feed that surfaces triage is not automatic here.
- **Action**: register the daily task on the active PC (Ryzen now). Read-only: GET Jules
  API + gh + writes `docs/jules-batch/<day>-digest.md`. Verify the script still matches
  the current API (it predates the 2026-06-02 findings). Decide cross-fleet ownership
  (Ryzen vs Lenovo vs both) and document.
- **Accept**: digest runs daily, produces a fresh digest file. **QG Step-1**: run
  `-Apply` in a throwaway/sandbox target first (anti-pattern #9), verify the artifact +
  encoding (anti-pattern #12 ASCII), not just the log.

### G2 -- programmatic suggestions feed (browser read-only)  [build]
- **Problem**: Jules proactive suggestions have NO API (404, verified); readable ONLY via
  the browser. So the suggestion->triage loop is not automatable end-to-end.
- **Action**: build a repeatable **read-only** Claude-in-Chrome snapshot: for each
  suggestions-enabled repo (opt-in, 3-5 cap), navigate jules.google, read the per-repo
  suggestions (title + category + expand for LOCATION), write
  `docs/jules-batch/suggestions-<date>.md` (inventory + verdict-stub). The §9 finding
  proved reading works (navigate + get_page_text/screenshot). **Start stays Eduardo**
  (generative, SDMG R6) -- this feed only READS + drafts verdicts for a human/triage pass.
- **Accept**: one command/flow produces a suggestions inventory file; the per-repo sweep
  is documented (dropdown switch + expand + get_page_text caveats: SPA fragments on nav,
  use screenshot to read).

### G1 -- merge-autonomy model (PRIMARY, ADR-class)  [decide, gated]
- **Problem**: external-repo merge is **per-explicit-grant** ("ti autorizzo merge"), not
  standing. The auto-merge rung (R2) is default-OFF / not earned (ORCHESTRATION §5).
- **Action**: DECIDE the merge-autonomy model -- but this is ADR-class autonomization of a
  self-designed gate, so **SDMG applies (do NOT grant standing-merge by fiat = the rejected
  pattern)**. Run: (1) `brainstorming` skill -> options, e.g. (A) earn-path only
  (R0->R1->R2, slow+correct), (B) scoped standing-grant for the lowest-risk reversible
  class (docs/JSDoc/recovered-clean-tests) behind the full gate-stack + revert-proven,
  (C) status-quo per-batch; (2) `harsh-reviewer` falsification of the chosen option
  PRE-commit ("if it rejects, adopt not defend"); (3) write/amend the ADR.
- **Accept**: an ADR (amend 0036 or new) defining what merge-autonomy is standing vs
  explicit, that SURVIVED harsh-reviewer. Linked to G4.

### G4 -- progress the governor autonomy ladder R0 -> R1  [longer-term]
- **Problem**: the unified governor (observe->classify->act) ladder is default-OFF; R0 not
  shipped; acted-on signals 1/3 toward the R0->R1 off-ramp. This is the principled,
  earn-based path to autonomous merge (so it underpins G1).
- **Action**: ship R0 (observe pane + the crons) + accumulate acted-on signals (>=3 / 4
  weeks per `docs/governance/actor-activation-criteria.md`); R1 (open-PR, human-merge)
  unlocks behind its own ADR. Jules-PR-cycles are one of the signals it acts on.
- **Accept**: R0 shipped + CI-green + off-ramp tracking started. (Mid-horizon, not 1
  session.)

## Suggested execution order

1. **G6 + G5** (quick ORCHESTRATION doc amendments -- ~30min, one PR).
2. **G3** (digest cron on Ryzen -- concrete, QG Step-1 sandbox-Apply).
3. **G2** (suggestions read-only feed -- build, Claude-in-Chrome).
4. **G1** (merge-autonomy ADR -- brainstorming + harsh-reviewer, gated; DO NOT fiat).
5. **G4** (governor R0->R1 -- mid-horizon, links G1; track, don't rush).

## Method (mandatory)
- P1 refresh-verify before each item (state may have moved). P2 autoresearch (ground-truth
  > heuristic). **SDMG (Protocol 7) for G1 + any autonomization** -- brainstorm + external
  harsh-reviewer falsification PRE-commit, adopt-not-defend. External-repo MERGE stays
  Eduardo-explicit until G1 changes it. Suggestions Start stays Eduardo (SDMG R6).
  No fiat standing-grants.

## Pointers
- `ORCHESTRATION.md` §5 (ladder) + §6 (standing perms) · `docs/adr/0035-*.md` (+addendum)
  · `docs/adr/0036-*.md` · `docs/superpowers/jules/JULES-CAPABILITIES-MASTER.md` §9
  · `docs/governance/actor-activation-criteria.md` (R0/R1/R2 earn-path)
  · `docs/jules-batch/2026-06-02-hardened-prompts.md` (prompt templates + verdicts)
  · memory `project_jules_collaboration_state`, `feedback_jules_autonomous_loop_2026_06_02`,
  `feedback_codex_clean_verdict_reaction`.
- Capability recap: keys in `~/.config/api-keys/keys.env` (JULES_API_KEY). Dispatch JSON via
  `curl --data @-` (Windows curl can't read MSYS /tmp; pipe+heredoc collide on stdin).
