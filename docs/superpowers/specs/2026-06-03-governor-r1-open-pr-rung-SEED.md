# SEED — Governor R1->open-PR rung (brainstorm -> spec -> build, NEXT session)

> **This is a SEED / kickoff brief, NOT a spec.** A fresh session reads this to start the
> brainstorming flow for the missing earn-path rung, without re-deriving the 2026-06-03 marathon.
> Created 2026-06-03. Non-doctrine (design brief; defines no rules). ASCII-first (ADR-0021).

## Why this exists

Eduardo wants to reduce his hand-merge load on routine governance/doc PRs. Session 2026-06-03
established -- after **two** merge-authority grant attempts were KILLED by SDMG harsh-reviewer
falsification (a 15s-timer auto-merge, then a self-repo-non-doctrine standing grant) -- that the
**only sanctioned route** to merge autonomy is the governor **earn-path** (ADR-0037 dec.4), NOT a
fiat/timer/standing grant. The earn-path's missing piece is the **R1->open-PR rung**. This seed
kicks off its design.

## Goal

Build the rung that makes the unified governor open **actual reconcile PRs** (journal/doc-reconcile
class) instead of only GitHub issues. Human-merged CLEAN PR-cycles then accrue toward R2 (gated
auto-merge of that one class), per `actor-activation-criteria.md` sec 3 + sec 6.

## The blocker (precise)

R1 currently ships as **issue-escalation** (scope A, 2026-06-02): it opens/updates a GitHub ISSUE,
not a PR. Per `actor-activation-criteria.md` sec 6 addendum, issues are "seen" (acknowledged), NOT
clean-PR-cycles -> **0 R2 evidence accrues -> R2 is unreachable** (ADR-0037 dec.4: "the R1->open-PR
rung that would emit the required >=4 clean PR-cycles does not yet exist"). Close that gap.

## Read FIRST (ground-truth)

- `docs/cross-repo/actor-activation-criteria.md` -- R0/R1/R2 rungs; sec 2 (R0->R1 unlock); **sec 3
  (R1->R2 unlock conditions)**; **sec 6 (CLEAN R1 cycle = PR human-merged + no-revert-7d +
  no-same-line-followup-7d)**; sec 4 (severed self-licking loop -- only human acted-on counts);
  sec 5 (what "acted-on" means).
- `docs/adr/0037-merge-autonomy-model.md` (dec.4 = earn-path is the only route, currently
  unreachable; dec.3 external=Eduardo-explicit). `docs/adr/0038-doctrine-carveout-completion.md`
  (what the governor must NEVER auto-merge -- the doctrine carve-out, globs + catch-all).
  `docs/adr/0036-unified-orchestration-doctrine.md`.
- `docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md` +
  `docs/superpowers/specs/2026-06-02-governor-fase2-r1-classifier-actor.md` (the governor design +
  the shipped R1 classifier/actor that currently does issues).
- memory `feedback_external_repo_action_boundary` (v2/v3/v4 = the 2 killed grants + the boundary +
  why the earn-path is the only route).

## Design questions to brainstorm (the rung)

1. **Class scope**: confirm journal/doc-reconcile ONLY (lowest-risk reversible). Define precisely
   what qualifies (e.g. SoT-drift reconciles, stale doc-pointer fixes, journal lands, status
   refreshes). R3+ wider classes = separate ADRs later. MUST exclude every ADR-0038 doctrine file.
2. **Generation**: how does the governor PRODUCE the reconcile fix (the PR content), not just flag
   it? Can it reuse existing tooling (`sot-drift-verifier` agent, `journal-land.ps1`, the
   `cross-repo-dashboard`)? Where does the diff come from?
3. **Safety during earn**: R1 invariant = the PR is inert until a HUMAN merges. So during the earn
   window, **Eduardo merges** each reconcile PR; the clean-cycle counter (sec 6) is mechanical
   (git history), never self-assessed. No self-licking (sec 4).
4. **Evidence accrual**: R2 needs >=4 clean cycles / >=2 repos / >=2 weeks / zero bad-merge. Which
   2+ repos? Is the reconcile cadence enough to produce that in reasonable time?
5. **The R2 ADR (later, separate)**: after >=4 clean cycles, a dedicated R2 ADR -- harsh-reviewer
   FALSIFIED specifically -- grants gated auto-merge of THAT class only, plus: the narrow
   `.claude/settings.json` merge permission, a CI-watchlist (file<->essential-test, anti-#10), and
   a different-FAMILY judge (fleet-tools `cross_check`/Gemini/Groq) or an explicit drop of that
   mitigation. (harsh-reviewer is Claude = partial monoculture.)

## Method (next session)

1. `superpowers:brainstorming` skill -> explore context -> 2-3 approaches + tradeoffs -> design.
2. -> spec in `docs/superpowers/specs/YYYY-MM-DD-governor-r1-open-pr-rung-design.md`.
3. -> `superpowers:writing-plans` -> build (the rung ships behind its OWN PR + its own ADR, per
   actor-criteria sec 2/3).
4. SDMG (Protocol 7): harsh-reviewer FALSIFIES the rung increment specifically before acceptance.

## Anti-patterns -- do NOT (hard-learned 2026-06-03)

- Do NOT propose fiat / timer / standing auto-merge. KILLED twice this session (self-licensing).
  The rung only OPENS PRs; auto-merge (R2) is EARNED later via clean cycles + its own ADR.
- Do NOT let the governor's own output count toward its own promotion (self-licking; sec 4). Only
  HUMAN acted-on / human-merged-clean-PR counts. The decider is ground-truth, never the classifier.
- Do NOT touch doctrine files (ADR-0038 carve-out) in the auto-class, EVER.
- Do NOT mistake "issue escalation" for a clean PR-cycle (sec 6 addendum).

## State at handoff (2026-06-03)

- Context-files reorg Fasi 1-6 COMPLETE (6 CLAUDE.md <200 + root governance + memory 37->34 +
  agents + baseline-policy + Ryzen parity-deploy + `scripts/fleet/sync-claude-global.ps1`).
- ADR-0038 (doctrine carve-out completion) MERGED (#286). ADR-0039 (auto-merge grant) KILLED, not
  submitted.
- Merge model now: per-call classifier = self-repo non-doctrine; doctrine (ADR-0038 set) + external
  = Eduardo-explicit; standing autonomy = ONLY via this earn-path.
- origin/main HEAD at seed time: post-#286.
