# 4-Repo Short Direction-Setting -- Design (2026-05-22)

> Brainstorming artifact + GOALS-layer audit trail. Sets the next **Short** goal
> for the 4 repos that had Short done but no direction after the 2026-05-21
> GOALS-layer cycle. Companion to `2026-05-21-cross-repo-goals-coordination-design.md`.

## Context

After the flagship M1-full thread was set (Game + Godot, 2026-05-22, PRs #2384 /
#352), 4 repos remained Short-done / direction-pending: Game-Database, vault,
evo-swarm, codemasterdd. Eduardo asked to read each repo's docs and find a
coherent next Short for each.

## Method

Parallel read-only research (one general-purpose agent per repo): read each
repo's `## Goals (S/M/L)` canonical section + BACKLOG / OPEN_DECISIONS /
recent commits, assess whether the prior Short is truly done, propose 2-3 Short
candidates with tradeoffs + a recommendation. Decisions taken by Eduardo
(per-repo, AskUserQuestion) -- all 4 recommendations approved.

## Cross-cutting theme

3 of 4 chosen Shorts push the **content supply-chain INTO Game**: Game-Database
closes the versioning loop (Game pins a taxonomy version), evo-swarm lands actual
content (~1 -> >=10 integrated PRs). Both touch the Game repo (Eduardo-gated).
vault is internal (verify shipped synthesis). codemasterdd is gate-prep only --
its natural next (D2 auto-coordination) is locked until ~2026-06-03.

## Per-repo decisions

### Game-Database -- Phase C-Game consumer wiring
- **Goals file**: `C:/dev/Game-Database/CLAUDE.md` (`## Goals (S/M/L)`).
- **New Short**: close the versioning loop end-to-end -- Game's `traitRepository`
  passes `?versionId` resolved from `EVO_TAXONOMY_VERSION`, so a Game build pins
  one taxonomy version. The single unchecked RFC Section 5 acceptance item.
- **Why**: DB-side versioning (Phase A+B+C-DB, #154/#158/#160/#161/#163 + UI #164)
  is shipped; this is the only step between "versioned" and "Game actually pins a
  version" -- highest coherence with the content-provider role.
- **Tradeoff**: cross-repo (Game PR + Eduardo sign-off), not pure own-repo.
- **Rejected**: versioned reads for Biome/Species/Ecosystem (own-repo, but YAGNI
  until a consumer needs it) -> demoted to Mid.

### vault -- Synthesis fidelity-verification pass
- **Goals file**: `C:/dev/vault/hot.md` (`## Goals (S/M/L)`).
- **New Short**: verify the ~84 draft synthesis cards (`fidelity_status: TBR`,
  content-gap waves 1-3, #162-#170) against raw sources, flip to `verified`,
  densify cross-refs.
- **Why**: closes the self-eval #1 gap (graph density) and de-risks already-shipped
  work; the synthesis layer (the Karpathy payoff) is shipped but unverified.
  Respects OD-056 ordering -- L3 "what's-missing" loop stays gated last.
- **Tradeoff**: cleanup, not new coverage.
- **Rejected**: promote L1 maintenance cadence (cheap but low-novelty, D4 chose
  manual-trigger anyway); L3 report-only loop (explicitly sequenced last).

### evo-swarm (Dafne) -- Close the integration loop end-to-end
- **Goals file**: `C:/dev/evo-swarm/ROADMAP.md` (`## Goals (S/M/L)`).
- **New Short**: take 3-5 `ready` candidates through triage -> strict-verify ->
  Game PR; move the Mid metric (~1 -> >=10 artifacts landed in `C:/dev/Game` with
  provenance). First step: validate born-ready (#116) on a live run
  (`EVOSWARM_BORN_READY=1`), then flip default ON.
- **Why**: the production + verify infra is now largely built (#111-#116, 470+
  tests); the missing piece is one exercised end-to-end pass turning a candidate
  into a landed PR. This is the single direction that moves the headline Mid metric.
- **Tradeoff**: touches Game (review-gated), slower per item.
- **Rejected**: validate-born-ready-only (folded in as the first step, no
  integration gain alone); strict-verify-gate-only (folded in as the loop's gate).

### codemasterdd -- Gate-E evidence-logging (non-gated)
- **Goals home**: `GOALS.md` hub row IS canonical (no separate per-repo section;
  the planned ROADMAP cross-cut section was never added).
- **New Short**: build the empirical evidence base the ~2026-06-03 hub-shape
  re-eval + D2 gate review will consume -- SDMG invocation log, Hybrid A1
  cost/cite tracking, H7 `logs/claude-api-spend-2026-05.md`.
- **Why**: highest-leverage non-gated work; makes the gate review evidence-driven
  rather than recollection-driven; structurally cannot trigger D2 early (writes
  logs only, never proposes/spawns).
- **Gate caveat**: D2 auto-coordination is GATED till ~2026-06-03 (SDMG 2-week
  window started 2026-05-20, 2 invocations logged). This Short must NOT build D2
  or auto-trigger -- scope strictly to logging.
- **Tradeoff**: partly passive (Direction 1 cost/cite depends on daily usage data).
- **Rejected**: wrapper/observability hardening (concrete but no unifying thread);
  leave-unset-till-06-03 (wastes the 2-week window).

## Apply plan

- **Game-Database / vault / evo-swarm**: edit canonical `## Goals (S/M/L)` Short
  (+ refill Mid where promoted) on a clean branch off origin/main -> commit (AA01
  trailer, ADR-0011) -> push -> PR. **No merge** (self-governed; vault merge =
  Eduardo-only-explicit).
- **codemasterdd**: edit the `GOALS.md` hub row Short directly (own repo, main) +
  bump last-refresh + clear the 4 "Next: set new Short" markers. Commit with this
  spec.
- **Hub mirror**: the 3 content-repo rows in `GOALS.md` updated to mirror the new
  per-repo Short.

## Status

Directions approved by Eduardo 2026-05-22. Spec is the audit trail; the deliverable
is goal-setting (doc edits), so the brainstorming terminal adapts from "writing-plans"
to "apply goals via PRs" -- no code implementation plan needed.
