# ADR-0037 — Merge-autonomy model (standing vs Eduardo-explicit)

> Status: **Accepted** — 2026-06-03 (G1; Proposed + ratified same day by Eduardo, explicit "fai la ratifica").
> Survived an SDMG harsh-reviewer falsification (verdict: SURVIVE-WITH-CHANGES;
> all blocking + significant findings adopted pre-write -- see "Falsification").
> Extends ADR-0036 (ORCHESTRATION doctrine) + `docs/cross-repo/actor-activation-criteria.md`
> (the governor earn-path). ASCII-first body (ADR-0021).
> **Accepted**: the decisions below are binding doctrine. The doctrine-file carve-out
> (decision 2) is reflected in actor-criteria sec 7 (this PR) + ORCHESTRATION sec 5/6 (follow-up).

## TL;DR

Decide what merge autonomy is STANDING (no per-action human prompt) vs Eduardo-explicit.
Answer: **almost nothing is standing.** External-repo merge stays Eduardo-explicit
indefinitely; the only sanctioned path to ever change that is the existing governor
R0->R1->R2 earn-path -- which is **currently unreachable** and out of scope here.
Governance-doctrine files are Eduardo-only-merge **regardless of repo** (a hub must not
merge its own rule-book). A fiat scoped standing-grant (Option B) is rejected. Net: this
ADR LOCKS OUT shortcuts more than it enables autonomy -- which is the SDMG-correct result.

## Context

- The goal (`docs/goals/2026-06-03-jules-autonomy-gaps.md`, G1) asks for a decided
  merge-autonomy model, gated by SDMG (Cognitive Protocol 7): NO fiat standing-grant; the
  chosen option must survive an external harsh-reviewer falsification before this ADR.
- Today: external-repo merge (Game, Game-Godot-v2, Game-Database) = Eduardo per-PR
  explicit grant (ADR-0035 hard-constraint 4). The governor autonomy ladder
  (R0 observe -> R1 classify/escalate -> R2 auto-merge) is default-OFF and earn-gated
  (ORCHESTRATION sec 5 + actor-activation-criteria.md).
- **Ground-truth (load-bearing, settings.json):** `.claude/settings.json` grants NO merge
  permission of any kind -- the allow-ceiling is `git push origin claude/*`. There is no
  `gh pr merge` allow-rule. Therefore "the hub already self-merges codemasterdd PRs" is NOT
  a standing settings.json grant: each merge this session (#271/#272/#273) was
  **classifier-judged per-call** (the auto-mode classifier permitted a well-formed,
  CI-green, review-gated self-repo merge), or Eduardo-executed. That is a real gate, not a
  standing allow-rule -- the distinction is the whole point.
- R2 evidence today: clean human-merged PR-cycles = 0; acted-on = 0. R1 shipped as
  issue-escalation only, which accrues ZERO clean PR-cycles BY DESIGN (actor-criteria
  sec 8). Nothing is earned.

## Decision

1. **Self-repo (codemasterdd) merge is classifier-judged, NOT standing.** This ADR does
   NOT grant prompt-free self-merge. The auto-mode classifier remains the per-call gate for
   hub self-repo merges (CI green + Codex-auto-review-or-substitute + ground-truth triage;
   governance-critical files additionally require the harsh-reviewer external-perspective
   pass, Protocol 5). settings.json is unchanged (no merge allow-rule added).

2. **Governance-doctrine files = Eduardo-only-merge, REGARDLESS of repo.** A hub that can
   merge edits to its own rule-book can loosen the very gate meant to stop it (a
   self-licensing loop CI/Codex/same-family-harsh-reviewer do not close). This aligns with
   ORCHESTRATION sec 5's irreducible-human residue ("ADR-class architecture, what NOT to
   build"). The carve-out set:
   `ORCHESTRATION.md`, `docs/adr/**`, `docs/cross-repo/actor-activation-criteria.md`,
   authoritative `CLAUDE.md`, `.claude/settings.json`, `~/.config/aider-privacy-whitelist.txt`.
   Edits to these are proposed by the hub (branch + PR) and **merged by Eduardo only**.

3. **External-repo merge (Game / Game-Godot-v2 / Game-Database) = Eduardo-explicit.** Today
   and indefinitely, until earned per (4). Unchanged from ADR-0035.

4. **The only sanctioned path to standing external-merge = the governor R0->R1->R2
   earn-path** (actor-criteria), R2 granted solely by its own dedicated R2 ADR after the
   mechanical conditions. **Honest status: this path is currently UNREACHABLE** -- R1 is
   issue-only (0 PR-cycles by design) and the R1->open-PR rung that would emit the required
   >=4 clean PR-cycles **does not yet exist** (no ADR/spec defines it; out of scope here).
   So standing external-merge is a FUTURE-ADR matter; until that rung is defined AND R2
   earns, external-merge stays Eduardo-explicit. This is a **principled hold** (correct for
   irreversible-class external merge), not an accidental stall -- "Eduardo-explicit possibly
   for a long time" is the intended, honest outcome, not a bug to route around.

5. **Reject Option B (scoped fiat standing-grant now)** for external repos: it would grant
   standing BEFORE the >=4-clean-cycle evidence exists -- the exact fiat-grant SDMG forbids
   (grant-before-evidence). The earn-path is the evidence mechanism; you cannot skip to its
   conclusion.

## Options considered

- **A (CHOSEN) -- Earn-path is the sole vehicle + doctrine-file carve-out + honest
  unreachability.** Consolidates onto the one already-falsified autonomy model (no second
  track), forecloses fiat grants, and adds the governance-doctrine Eduardo-only constraint.
  More than status-quo because it NAMES and GATES the only path and locks the doctrine-file
  hole. Tradeoff: standing external-merge is far off / currently unreachable -- accepted as
  the honest, safe state.
- **B -- Scoped standing-grant now (lowest-risk reversible class, full gate-stack +
  revert-proven).** Rejected for external repos on the grant-before-evidence ground (5). It
  would also fork a second merge-autonomy track parallel to governor R2 (accretion). Note:
  a self-repo-non-doctrine variant of B is moot -- self-repo merge is already
  classifier-judged (1), and doctrine files are carved out (2), so there is no remaining
  self-repo class that needs a standing grant.
- **C -- Status quo per-batch explicit (no change).** The safe baseline, but silent on the
  path and the doctrine-file hole. A (chosen) keeps C's safety while adding the foreclosure
  of fiat shortcuts and the doctrine-file carve-out -- strictly more decided than C.

## Consequences

**Positive:** one merge-autonomy model (no parallel tracks); fiat shortcuts foreclosed; the
self-licensing rule-book hole closed; the earn-path's real (unreachable) status stated
honestly so no future session mistakes it for a live runway; G1 linked to G4 (the governor
ladder is the merge-autonomy vehicle -- progressing G4 is the only way to progress
standing-merge).

**Negative / accepted:** standing external-merge does not arrive from this ADR (by design);
it requires a future R1->open-PR rung ADR + R2 earning. Routine external-repo merges remain
Eduardo labor until then. That cost is accepted as correct for irreversible-class actions.

**Disclosure (this session, honest):** #271 (which edited ORCHESTRATION.md, a doctrine file)
was self-merged this session via classifier-permitted `gh pr merge`, BEFORE this ADR's
carve-out (2) existed. It was gate-TIGHTENING (made `:create` per-instance, tightened the
Codex sub-gate), harsh-reviewer-reviewed pre-commit, and is revertible. It is left standing
but flagged here; going forward (2) makes doctrine-file merges Eduardo-only. This ADR's own
PR is therefore the FIRST the hub does NOT self-merge -- it is left for Eduardo, demonstrating
the rule it proposes.

**Ratified (Eduardo, 2026-06-03, explicit "fai la ratifica"):** flipped to Accepted; the
doctrine-file carve-out (2) added to actor-criteria sec 7 + the sec-8 acted-on count
reconciled (0->1) in this same PR; the ORCHESTRATION sec 5/6 pointer is a follow-up (it lives
on origin/main ahead of this branch).

## Falsification (SDMG Protocol 7, 2026-06-03)

External harsh-reviewer falsification PRE-write. Verdict **SURVIVE-WITH-CHANGES**; adopted:
- **P0.1** -- the original "self-repo merge is STANDING" clause was factually false vs
  settings.json (no merge grant). Re-founded as classifier-judged (decision 1).
- **P0.2** -- standing self-merge of doctrine files = self-licensing loop. Added the
  Eduardo-only doctrine-file carve-out (decision 2).
- **P1.1** -- trimmed the Option-B rejection to the grant-before-evidence ground for
  external repos (decision 5); dropped weaker padding.
- **P1.2** -- stated the earn-path's current unreachability honestly (decision 4).
- **P2.2** -- dropped the transient "cross_check down today" runtime reason from the durable
  rationale (it belongs in the session log, not the doctrine).

## References

- ADR-0036 (ORCHESTRATION doctrine), ADR-0035 (Jules external-repo merge = Eduardo-explicit),
  ADR-0026 (Cognitive Protocols, incl. Protocol 7 SDMG).
- `docs/cross-repo/actor-activation-criteria.md` (R0/R1/R2 earn-path; sec 8 = unreachable today).
- `ORCHESTRATION.md` sec 5 (autonomy ladder + irreducible residue) + sec 6 (standing perms).
- `docs/goals/2026-06-03-jules-autonomy-gaps.md` (G1 + G4).

## Addendum 2026-06-03 -- `jules-dispatch` wrapper BUILT (path-to-standing prerequisite met; standing STILL deferred)

The fail-closed `jules-dispatch` wrapper named in the `:create` path-to-standing clause now
EXISTS: `scripts/fleet/jules-dispatch.ps1` (+ `jules-dispatch.Tests.ps1`, 52 unit asserts).

- **What was built.** A 5-gate fail-closed stack: repo-whitelist -> ASCII-lint (native
  byte-check) -> scoped-template-lint (+ a `-Target`<->task-file consistency check) -> dedup
  vs ACTIVE sessions -> dispatch (REST `POST /v1alpha/sessions`) + audit-log
  (`logs/jules-dispatch-YYYY-MM.md`, gitignored). Dedup = option A: title+prompt target-token
  match over sessions in a NON-terminal state (denylist {COMPLETED, FAILED, CANCELLED, ARCHIVED};
  unknown/null -> active, fail-closed), boundary-precise matcher, conservative-abort on
  uncertainty, `-Force` (known-overlap override) and `-ForceBlind` (cannot-verify override) as
  distinct flags that NEVER bypass gates 1-3.
- **Dispatch-SOURCE decided.** Human-authored scoped tasks from real repo needs (Eduardo,
  2026-06-03) -- the SAFE source. This closes the harsh-reviewer "attacker-influenced auto-feed"
  risk that was a blocker to making `:create` standing.
- **Disciplined path.** Spec (`docs/superpowers/specs/2026-06-03-jules-dispatch-wrapper-design.md`)
  -> harsh-reviewer FALSIFICATION (SDMG Protocol 7; verdict SURVIVE-WITH-CHANGES; 3 P0 + 4 P1
  adopted, verified against the LIVE Jules API not just docs) -> TDD (RED/GREEN) -> QG
  (`docs/research/jules-dispatch-wrapper-2026-06-03.md`: Smoke + 7 research edges + 1 tuning
  iteration with before/after).

**SDMG boundary (load-bearing -- this addendum does NOT loosen any gate).** Building/running the
wrapper is the PREREQUISITE + the ENFORCEMENT MECHANISM, NOT the grant. `:create` stays
**NOT-standing / per-instance**: a human runs the wrapper manually each dispatch (the wrapper
just makes each manual dispatch SAFE). "Standing" = removing the per-action human prompt by
allow-listing the wrapper in `.claude/settings.json` -- a SEPARATE autonomization that needs its
own decision + its own harsh-reviewer gate (un-globbable scope + dispatch-time harms remain the
open questions). Until that separate gate is passed, settings.json is unchanged (no `:create`
allow-rule). External-repo MERGE is untouched by this addendum (decision 3: Eduardo-explicit).

**Merge of THIS addendum.** It edits `docs/adr/**`, a governance-doctrine file -> Eduardo-only
merge (decision 2). Shipped as its own branch + PR, NOT self-merged by the hub.
