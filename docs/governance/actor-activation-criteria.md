---
id: actor-activation-criteria
title: Actor activation criteria -- autonomy earn-path for the unified governor
type: control-plane
status: active
created: 2026-06-01
owner: master-dd
language: en
tags: [cross-repo, orchestration, autonomy, sdmg, adr-0036, gate]
---

# Actor activation criteria -- autonomy earn-path

> **Scope**: the single mechanical checklist that decides WHEN the unified governor
> (the `cross-repo-dashboard` promoted to an active observe->classify->act loop) is
> allowed to climb each autonomy rung. Authority: ADR-0036 "Ratify scope split"
> (revised 2026-06-01). Design: `docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md`.
>
> **Invariant (SDMG, Cognitive Protocol 7)**: no rung is climbed on judgment -- only on
> the mechanical conditions below + an external harsh-reviewer falsification of THAT
> specific increment. The decider is ground-truth (a human acted / a PR was not
> reverted), never the actor's own classifier. ASCII-first (ADR-0021).

## 1. The rungs

| Rung | What the actor may do | Default |
|------|-----------------------|---------|
| R0 | OBSERVE: ingest island signals, persist, render a read-only consolidated pane; write the advisory log (sec 4) | active once Fase 1 ships |
| R1 | CLASSIFY + open a branch+PR / emit a drift escalation. A PR is inert until a HUMAN merges it. | OFF until unlocked (sec 2) |
| R2 | ACT: auto-merge the LOWEST-risk reversible class ONLY (journal/doc reconciles) | OFF until unlocked (sec 3) |
| R3+ | wider auto-merge classes | OFF; each needs its own ADR |
| -- | irreversible/destructive, outward-facing, account-credential, external-comms, ADR-class architecture, "what NOT to build" | HUMAN irreducible -- never automated |

## 2. R0 -> R1 unlock (open-PR / escalate)

Climb to R1 only when ALL hold:

- [ ] Fase 1 (R0) shipped + CI green + its tests cover every ingestor adapter.
- [ ] harsh-reviewer reviewed the CLASSIFIER design and the verdict is SURVIVE (or
      SURVIVE-WITH-CHANGES, changes adopted).
- [ ] **Off-ramp passed (the honest experiment)**: in the first 4 weeks of R0,
      Eduardo ACTED on **>= 3** surfaced signals (see sec 5 for what "acted" means).
      If < 3, reading B was right (pain below threshold) -> STOP at observability; do
      NOT build the classifier/actor. (N=3 set by Eduardo 2026-06-01.)
- [ ] R1 ships behind its own PR + its own ADR (Fase 2).

> **Off-ramp WAIVED 2026-06-02 by Eduardo.** The 4wk/>=3 acted-on condition was not met
> (R0 shipped same day as R1 build).  R1 triggers on a heuristic (error OR worsened-delta).
> Waiver is intentional and recorded here per SDMG step 1 (honesty preamble).  Off-ramp
> counting still runs: acted-on>=3 gates R2 normally; the waiver does NOT propagate.
> Authority: spec docs/superpowers/specs/2026-06-02-governor-fase2-r1-classifier-actor.md.

R1 is reversible by construction (a PR is inert until merged), so it is the rung at
which auto-merge evidence may accrue WITHOUT ever enabling auto-merge first.

## 3. R1 -> R2 unlock (gated auto-merge, lowest-risk class only)

Climb to R2 only when ALL hold (granted by a dedicated R2 ADR, never by this file alone):

- [ ] **>= 4 distinct CLEAN R1 cycles** (sec 6 definition) on the journal/doc-reconcile
      class, across **>= 2 repos**, over **>= 2 weeks**.
- [ ] Zero bad-merge / drop incidents in that window (any reset the counter).
- [ ] harsh-reviewer FALSIFIES the auto-merge increment specifically and the verdict is
      SURVIVE (changes adopted) -- not a generic re-review.
- [ ] Revert path PROVEN on a throwaway: a merged auto-PR can be reverted cleanly.
- [ ] A different-FAMILY judge is wired into the gate (fleet-tools `cross_check`,
      Gemini/Groq) OR the R2 ADR explicitly drops "different-model judge" from the
      mitigation list and relies on reversibility + class-restriction + drop-check +
      CI-watchlist. (Rationale: the harsh-reviewer is itself Claude = partial
      monoculture -- ADR-0036 / ORCHESTRATION sec 7.)
- [ ] A CI-watchlist (file <-> essential-test) exists for the auto-merge class so an
      anti-#10 drop goes CI-red.
- [ ] `.claude/settings.json` is amended to add the narrow auto-merge permission for the
      one class only (today the ceiling is `git push origin claude/*`, no merge).

> **Addendum 2026-06-17 (Rule-of-Two precondition, recorded for the R2 ADR).** Per the
> "Agents Rule of Two" (Meta, 2025-10-31, ai.meta.com/blog/practical-ai-agent-security): an
> agent should hold no more than two of [A] untrusted input, [B] secret / private-data access,
> [C] state-change / external-comms. Granting STANDING auto-merge to the governor while a
> session also reads untrusted PR-content [A] AND holds keys.env [B] AND can merge [C] puts all
> three live at once. So an R2 precondition (to be ratified IN the R2 ADR, not by this file
> alone) is session-isolation: the auto-merge actor runs with NO keys.env in context, OR merges
> only on a clean/separate context. This makes explicit a constraint ADR-0037 + sec 1
> (irreducible residue) already imply; by itself it climbs no rung.

## 4. Advisory vs gate -- the severed self-licking loop (load-bearing)

A harsh-reviewer falsification (2026-06-01, P0.3) killed the v1 idea of the actor
auto-logging its own classifier verdicts into the metric that licenses its own
expansion (a self-licking ice cream cone). Two SEPARATE signals replace it:

- **`auto-observed-signals` log = ADVISORY ONLY.** The ingestor/classifier MAY record a
  detected signal-needing-action here to inform Eduardo. This log is **EXCLUDED from
  every unlock condition above.** It never votes for the actor's own promotion.
- **`acted-on` count = the gate input.** The only metric that gates R1/R2/Fase-4 is how
  many surfaced signals a HUMAN acted on (sec 5). The actor cannot manufacture a human
  action, so it cannot license itself.

Rule: any future change that lets the actor's own output feed an unlock condition is a
self-licking regression -- reject it.

## 5. What "acted on a signal" means (the gate metric)

A surfaced signal counts as "acted on" when, after the pane/advisory surfaced it,
Eduardo did one of: merged a PR addressing it; pushed a commit/branch fixing the drift
it named; recorded a decision (OD / ADR / JOURNAL) resolving it; or archived it as
deliberately-wont-fix. Passive viewing does NOT count.  Closing or reading a governor-attention issue is
"seen" (acknowledged), NOT "acted-on" -- only acting on the underlying signal (a fix,
OD/ADR, or deliberately-wont-fix) counts.  Counting is manual + auditable (git log / OD /
JOURNAL cross-ref) -- never inferred by the actor.

## 6. Definition of a CLEAN R1 cycle (mechanical, not self-assessed)

A clean R1 cycle = a PR opened by the actor that is:

- (a) MERGED BY A HUMAN (Eduardo), AND
- (b) NOT reverted within 7 days, AND
- (c) has NO follow-up fix commit touching the SAME lines within 7 days
      (the anti-pattern #10 bot-rewrite-drop check).

A cycle failing (b) or (c) is a FAILED cycle and resets the clean-cycle counter for that
class. "Clean" is decided by these mechanical facts (git history), never by the hub's
judgment that a verdict "looked plausible".

> **Addendum 2026-06-02 (R1 shipped as issue-escalation, scope A).** The SHIPPED R1
> opens/updates a GitHub ISSUE, not a PR (sec 8). This does NOT redefine the clean R1 cycle
> above; it clarifies that issue escalations are a DIFFERENT artifact that must NOT be
> counted as R2 evidence (Codex P1/P2 on PR #260, adopted):
> - The "clean R1 cycle" above stays **PR-based and unchanged** (human-merged PR, no revert,
>   no same-line follow-up) on the **journal/doc-reconcile class** (sec 3). It is the R2
>   auto-merge evidence metric.
> - **Issue escalations are NOT PRs and DO NOT count as clean R1 cycles / R2 evidence.** The
>   shipped issue-only R1 accrues ZERO R2 clean-cycles BY DESIGN. The R2 counter can advance
>   only once R1 is extended to OPEN PRs (a future rung defined by the R2 ADR), and even then
>   only on the journal/doc-reconcile class -- never on arbitrary signals (e.g. eng-graph
>   staleness or a lint warning). Counting issue escalations toward R2 would strip the field
>   evidence (human-merged reconcile PRs, no revert/drop) the auto-merge gate exists to require.
> - What the issue-R1 DOES feed is the **acted-on metric** (sec 5): when Eduardo acts on the
>   underlying signal an escalation named (a fix / OD / ADR / deliberately-wont-fix), that
>   increments acted-on. Per sec 2 + sec 4, acted-on>=3 IS a NECESSARY R2 input (and also
>   gates Fase-2 expansion) -- so issue escalations DO advance that precondition. But
>   acted-on is necessary-NOT-sufficient for R2: the R2 unlock ALSO requires >= 4 clean
>   PR-cycles (sec 3) on the journal/doc-reconcile class, which the issue-only R1 does not
>   produce. R2 needs BOTH; issue escalations can satisfy the acted-on input, NEVER the
>   clean-PR-cycle condition. Closing/reading the issue is NOT acted-on.
>
> Net: a silent governor (steady warnings, nothing worsening) accrues zero acted-on AND zero
> clean PR-cycles. Issue escalations can advance acted-on (an R2 input + the Fase-2 gate) but
> NEVER the clean-PR-cycle R2 condition. Both at 0 today is the honest off-ramp signal.

## 7. Per-increment discipline (every climb)

- SDMG step 3 (FALSIFY) before the climb: harsh-reviewer on the specific increment;
  pre-commit "if rejected, I adopt -- I do not defend".
- TDD for the code that implements the rung; CI green.
- ADR + commit policy-C (`Coding-Agent:` + `Trace-Id:` uuidv7, NO `Co-Authored-By`).
- The climb lands as its own 1 PR (no big-bang). Eduardo merges (human-irreducible).
- If a bad merge ever lands: revert + downgrade that class to human-gated + amend
  ADR-0036 + record the lesson.
- **Governance-doctrine files = Eduardo-only-merge, regardless of repo** (ADR-0037
  decision 2 as completed by ADR-0038, Accepted 2026-06-11; sec synced at ratify):
  - GLOBS: `docs/adr/**`, `docs/governance/**` (incl. this file), repo `.claude/**`,
    `Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/**`, plus the
    `~/.claude/` governance subpaths (explicit positive list in ADR-0038;
    `~/.claude/agents/**` is prospective -- the live agents dir is the repo-level
    `.claude/agents/**`).
  - NAMED root rule/decision files: `CLAUDE.md` (authoritative, any level), `AGENTS.md`,
    `ORCHESTRATION.md`, `GOALS.md`, `DECISIONS_LOG.md`, `OPEN_DECISIONS.md`; plus
    `~/.config/aider-privacy-whitelist.txt`.
  - CATCH-ALL (content-based, ADR-0038): ANY file whose content defines rules/gates/
    decisions/charters the hub operates under is doctrine pending classification -- when in
    doubt, treat as doctrine + ask Eduardo. Human-review-enforced: no path-classifier can
    evaluate content (ADR-0039 dec.2).

  The hub proposes (branch + PR) but NEVER
  merges its own rule-book -- a hub that can loosen its own gate voids the gate.

## 8. Current state (2026-06-02 -- R1 built)

- Rung live: **R0 shipped** (Fase 1a PR #243; Fase 1b PR #244; Fase 1c PR #245).
  **R1 built 2026-06-02** (Fase 2, branch claude/governor-fase2-r1, off-ramp waived per sec 2).
- Auto-merge: **OFF**. `.claude/settings.json` ceiling = `git push origin claude/*`.
- Autonomy ceiling after R1 ship: classify + open/update ONE GitHub issue (label
  governor-attention, codemasterdd only).  Human closes.  No PR, no merge, no branch.
- Next gate to evaluate: R0 off-ramp acted-on count (sec 2). acted-on (sec 5) is an R2 INPUT
  (sec 2/4) AND the Fase-2-expansion gate -- issue escalations can advance it. The SEPARATE
  R2 condition, >= 4 clean PR-cycles (sec 3/6), stays 0 under the issue-only R1 BY DESIGN
  (issues are not PR-cycles); R2 needs BOTH, so issue-R1 alone never unlocks R2.
- **Live state 2026-06-02 (post the 3 non-gated PRs #256/#257/#258).** R0 = **8 signal
  sources** (added archon-learnings #257 + eng-graph staleness #258; R1 actor token-hardened
  #256). R1 has escalated **0 times** to date: the 5 standing `warning` signals are STEADY
  (no error, no worsened-delta), so the actor is silent BY DESIGN. Hence clean-R1-cycles = 0
  AND acted-on = 0; the off-ramp window is just opening. The next real decision point is
  whether R1 ever fires on a genuine regression and whether Eduardo acts on it (sec 6
  addendum) -- NOT more building. R2/Fase-4 remain hard-gated; the "complete the governor"
  grant (2026-06-02) explicitly did not override these gates.

> **Update 2026-06-03.** First **acted-on = 1** (per #261): a governor-surfaced signal
> Eduardo acted on -- Game issue #2477 closed as no-drift (deliberately-wont-fix, sec 5).
> Off-ramp now **1/3**. clean-R1-PR-cycles still **0** (R1 issue-only, by design -- sec 6
> addendum). R2/Fase-4 stay hard-gated. (Supersedes the "acted-on = 0" snapshot above.)

> **Update 2026-06-03 (R1 open-PR rung BUILT -- ADR-0039).** The R1->open-PR reconcile rung is
> BUILT: deterministic, clock-free reconcile actors that OPEN (never merge) one branch+PR per
> drifted doc -- the PR variant the issue-only R1 lacked, added ALONGSIDE it (the issue actor
> `act.py:run_r1` is UNCHANGED; both coexist). Two legs: codemasterdd `STATUS_MULTI_REPO.md` +
> vault `Atlas/lint-status.md` (new governor-owned doc, Eduardo OK; clock-free, content-based
> severity). **Human-merge-only during the earn (sec 6): a clean R1 cycle is HUMAN-merged, so the
> hub must NOT self-merge reconcile-class PRs; vault PRs are Eduardo-only (sibling-peer).** The
> rung OPENS PRs only -- auto-merge (R2) stays **OFF**; `.claude/settings.json` ceiling UNCHANGED.
> The merge-block is code (a negative test on the REAL builder) + the human-merge-only invariant +
> the settings ceiling -- codemasterdd has NO branch protection (free-tier 403), so there is NO
> platform backstop (the R2 ADR must weigh this). [Update 2026-06-17: branch-protection ADDED when
> the repo went public -- enforce_admins + force-push/deletion blocked, but NO required-PR, so it
> blocks history-rewrite/force-push NOT merge-review = NOT a merge backstop; the human-merge invariant
> + negative test remain load-bearing.] Clean-cycle accounting stays EXTERNAL (read-only
> `reconcile_cycles_report.py`, never in the actor -- sec 4). **clean-R1-PR-cycles still 0** until
> the FIRST reconcile PR is human-merged AND survives the 7-day no-revert / no-same-line-followup
> windows (sec 6); cadence is change-triggered, so the rung is SILENT when nothing drifts (silence
> = the off-ramp signal, not a stall). The ">= 4 across >= 2 repos" distribution is DEFERRED to
> the R2 ADR (two real legs now exist; not pre-decided). R2/Fase-4 stay hard-gated. Authority:
> ADR-0039 + spec/plan 2026-06-03.

> **Update 2026-06-28 (STATUS-leg clock-leak FIXED -> exclusion LIFTED + first post-fix cycle in
> flight).** The STATUS-leg clock-leak that ADR-0039 dec.1 used to disqualify codemasterdd-leg
> PR-cycles from R2 was FIXED by #333 (render mask, 2026-06-11) and the exclusion is now LIFTED
> by ADR-0039 Addendum 2026-06-28 (PR #422, MERGED 64d8384): **STATUS-leg STEADY-STATE PR-cycles
> now COUNT toward R2** alongside vault-leg (bootstrap #296/#252 still excluded -- annotation (b)).
> First post-fix reconcile run (2026-06-28, manual `python -m governor.reconcile`, both legs
> drifted on real content): opened codemasterdd **#424** (STATUS_MULTI_REPO.md, region-only, CI
> green, the masked vault-eng-graph row stayed STABLE while real signals drifted = the #333 fix
> validated live) + vault **#261** (Atlas/lint-status.md, region-only). **Both OPEN, pending
> Eduardo human-merge** (sec 6 / ADR-0039 dec.3: a clean R1 cycle is human-merged; the hub does
> NOT self-merge reconcile-class PRs). **clean-R1-PR-cycles still 0** until #424/#261 are
> human-merged AND survive the 7-day no-revert / no-same-line windows; once they do this is the
> 1st post-fix steady-state cycle across 2 repos (need >= 4 across >= 2 repos for R2). Finding:
> vault `Atlas/lint-status.md` carries 13 pre-existing trailing NUL bytes (binary, from the #260
> creation) faithfully preserved by `get_file` -> a de-NUL + builder-sanitize follow-up is tracked
> (does not block this cycle). R2/Fase-4 stay hard-gated.
>
> **Correction (same session): #424 does NOT count as a clean cycle.** #424 (STATUS) was
> human-merged carrying a buggy `vault-coherence = ok` (a parser miss: the multi-pass coherence
> report records "N WARN (W-1..)" / "**0 BLOCK**" which `parse_vault_report` did not read -- Codex
> P2 on #261). The parser was fixed (#428, MERGED -- WARN count form anchored to the `(W-`
> enumeration; SDMG harsh-review SURVIVE-WITH-CHANGES) and re-reconcile opened **#426** to correct
> the same `vault-coherence` line on main (ok -> warning). Because #426 is a same-line follow-up
> to #424 within 7 days, **#424 FAILS the clean-cycle test (sec 6(c))** and does not count. The
> STATUS leg still counts going forward; the leg's FIRST clean cycle will be the next
> correction-free reconcile (#426 + #261, then steady-state). Honest mechanics, not a loss.
