# Autonomous Next-Point Protocol -- Design (REJECTED-HYPOTHESIS)

> **Status (2026-06-23):** rejected -- SDMG falsification 2026-05-21; not integrated

> Status: **REJECTED** 2026-05-21 by harsh-reviewer falsification (SDMG Protocol 7 step 3). NOT integrated. Archived as rejected-hypothesis (same disposition as HSGF F-FULL).
> Verdict rationale: (H5) no empirical problem -- improvised next-point selection worked fine across ~6 go-signals this session, zero failures a protocol would have prevented; (H4) fully redundant with existing Protocol 1 + verification-before-completion + Protocols 5/6/7 + narrow-pick discipline = accretion bloat; (H3) "highest-value" selection = residual heuristic-as-decider (P7 step 6 violation). Meta: premature codification driven by Eduardo's recall gap (thought it existed), not a capability gap.
> Adopted rejection per pre-commit stance ("if harsh-reviewer rejects, adopt non-defend") + L-2026-05-033.
> Cheap alternative (recall-gap fix, NOT a new protocol): one cross-ref line in CLAUDE.md noting open-ended go-signals are handled by existing Protocol 1 + narrow-pick + STOP-on-irreversible/owner-gated/architectural.
> Re-open condition: only with a LOGGED instance of improvised selection going wrong, AND post 2-week SDMG window (~2026-06-03).
> Author: Claude Code hub (Ryzen) 2026-05-21. Class: method (self-designed). Refs: ADR-0026 P1/P7, L-2026-05-033 (SDMG), HSGF rejection 2026-05-20, GOALS.md, anti-pattern #8.

## 1. Problem

Eduardo issues open-ended go-signals ("prossimo punto autonomo", "procedi", "continuiamo") expecting Claude to select + execute the next actionable item WITHOUT a clarifying round-trip. Today this is improvised. He referenced a "CLAUDE.md §Autonomous Next-Point" that does not exist. Hypothesis: a bounded, deterministic protocol for autonomous next-point selection would reduce round-trips while staying inside the DO-NOT guardrails (no auto-trigger, no HSGF fusion).

## 2. Proposed protocol (hypothesis)

### Procedure
1. **Refresh state (Protocol 1)**: read living task-list (TaskList) + GOALS.md + relevant git/PR state. Trust ground-truth, not narrative.
2. **Select next-point** = the highest-value item satisfying ALL:
   - not time-gated (e.g. not "~Aug", not "1-week-stable" unless gate verifiably met by evidence),
   - not delegated to a chip/session still in-flight,
   - not owner-merge-gated (vault merge = Eduardo-only; cross-repo merges = owner),
   - within my lane (codemasterdd hub direct, OR branch+PR on others without stomping active sessions).
3. **Execute** the work. Apply verification-before-completion (evidence before success claims).
4. **Update** task-list + report what was picked + why + outcome.

### STOP-and-ask (do NOT proceed autonomously) when ANY:
- Irreversible action (delete branch/file, merge, force-push, rm).
- Owner-gated (vault merge, anything needing explicit human authorization).
- Ambiguous scope or premise (the open-ended signal maps to >1 plausible point with materially different cost).
- New architectural/design decision (-> route to brainstorming, not autonomous execution).
- Cross-session collision risk (active session on the target working tree -> use worktree+PR or defer).
- No clear non-gated point remains (report "list drained", do not invent scope).

## 3. Anti-drift boundary (DO-NOT alignment)

- **Select from EXISTING list/GOALS only** -- never generate new cross-repo initiatives autonomously.
- **Never auto-trigger work in other repos' sessions** (P7 step 6).
- **Never auto-merge** gated PRs.
- Distinct from HSGF F-FULL (rejected): that AUTO-SPAWNS cross-repo orchestration. This is single-session self-pacing WITHIN already-declared work. If this protocol ever implies spawning/triggering, it has drifted into HSGF -> STOP.

## 4. Falsification questions (for harsh-reviewer)

- H1: Is this genuinely bounded, or a slippery slope into HSGF auto-coordination? (Anti-accretion: is it the rejected thing in disguise?)
- H2: Does the STOP-list actually catch the dangerous cases, or are there gaps (e.g. a "non-gated" item that's actually high-risk)?
- H3: Is "highest-value" a heuristic-as-decider (P7 step 6 violation)? Who decides value -- me (forbidden euristic) or evidence/Eduardo?
- H4: Does codifying this in CLAUDE.md add real value over the status quo (Claude already picks reasonably when told "procedi"), or is it ceremony/accretion?
- H5: New-evidence check -- this session ran ~6 open-ended go-signals; did autonomous selection actually go wrong anywhere a protocol would have prevented? (If it worked fine improvised, the protocol may be solving a non-problem -> DEFER.)

## 5. Integration plan (only if harsh-reviewer CONFIRMS)

- Add concise `## Autonomous Next-Point` section to codemasterdd CLAUDE.md (procedure + STOP-list + anti-drift).
- Log decision via scripts/sdmg/sdmg-gate.sh (class=method).
- If harsh-reviewer REJECTS or CONDITIONAL-with-fundamental-gaps -> do NOT integrate; archive as rejected-hypothesis (like HSGF F-FULL).

## 6. Pre-commit

Per L-2026-05-033: this is a self-designed method. My design = hypothesis with demonstrated high error rate. If the arbiter rejects, I adopt the rejection and do not defend.
