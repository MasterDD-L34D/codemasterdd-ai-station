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
