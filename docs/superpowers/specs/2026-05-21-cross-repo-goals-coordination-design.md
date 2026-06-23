# Cross-Repo Goals + Coordination -- Design Spec

> **Status (2026-06-23):** shipped -- goals layer live (GOALS.md); auto-orchestration D2c rejected

> Status: DRAFT (brainstorming output 2026-05-21, awaiting Eduardo review)
> Author: Claude Code (hub session, Ryzen)
> Method: superpowers brainstorming -> writing-plans (D1); D2 gated via harsh-reviewer
> Refs: STATUS_MULTI_REPO.md, ROADMAP.md, ADR-0026 Protocol 6/7, L-066, HSGF rejection 2026-05-20

## 1. Problem

Each repo self-governs (own CLAUDE.md / BACKLOG / ROADMAP / hot.md). codemasterdd is the monitoring hub (STATUS_MULTI_REPO.md = state dashboard). But there is **no unified Short / Mid / Long goal layer** across repos. Result: each session infers direction ad hoc; cross-repo features (e.g. M1 Sistema spanning Game + Godot) lack a shared declared goal; coordination is reactive, not direction-driven.

Goal: a goals layer that (a) every session/agent reads for shared direction, (b) respects each repo's self-governance, (c) enables future agent-assisted coordination -- WITHOUT building auto-trigger orchestration (the previously-rejected HSGF F-FULL).

## 2. Scope split (decided)

- **D1 -- Goals A+B (this spec, safe, build now)**: canonical per-repo S/M/L + hub synthesis. Read-only reference. No automation.
- **D2 -- Auto-coordination (separate, GATED)**: design-only hypothesis; MUST pass harsh-reviewer falsification (Protocol 7 step 3) + the 2-week empirical gate before any build. NOT in this implementation. See section 6.

## 3. D1 Design -- A+B hybrid

### 3a. Canonical (B): per-repo `## Goals (S/M/L)`

Each repo owns its goals inside its existing governance file (no new files where avoidable):

| Repo | Goals home (canonical) |
|------|------------------------|
| Game | `BACKLOG.md` new top section `## Goals (S/M/L)` (PROJECT_BRIEF = identity, stays) |
| Game-Godot-v2 | own `CLAUDE.md` new `## Goals (S/M/L)` section |
| Game-Database | own `CLAUDE.md` new `## Goals (S/M/L)` section |
| vault | `docs/decisions/` or `hot.md` `## Goals (S/M/L)` |
| evo-swarm | `ROADMAP.md` refresh + `## Goals (S/M/L)` |
| codemasterdd | `ROADMAP.md` already has phases; add `## Goals (S/M/L)` cross-cut |

Self-gov respected: codemasterdd does NOT overwrite repo internals; per-repo goals authored repo-side (branch+PR where codemasterdd has write-path, else flagged for repo owner).

### 3b. Hub synthesis (A): `codemasterdd/GOALS.md`

Read-only mirror table. Single glance for any session. Format:

```
| Repo | Short (sprint, weeks) | Mid (epic, 1-2mo) | Long (vision, 3-6mo) | Cross-dep |
```

Plus a `## Cross-cutting initiatives` section (e.g. M1 Sistema = Game backend + Godot client) with explicit ordering constraints (drift-seams).

### 3c. Horizon definitions

- **Short**: current sprint, weeks. Concrete, in-flight or next.
- **Mid**: epic, 1-2 months. Named workstream.
- **Long**: vision, 3-6 months. Directional, from PROJECT_BRIEF / vision docs.

## 4. D1 Draft content (FOR REVIEW -- Eduardo refines)

Derived from PR-analysis 2026-05-21 + PROJECT_BRIEF/ROADMAP reads. First-pass hypothesis, not authoritative.

### Game (Evo-Tactics Vue3)
- **Short**: close M1 Sistema persistent cross-session learning (route #2364 + pilot #2363); finalize hardcore band revision (#2365 OD-032).
- **Mid**: M1 Sistema full (game/AI remembers across sessions) wired Game<->Godot; trait system completeness (post-A4 ionico/termico).
- **Long**: shippable co-op tactical loop -- 4-8 friends, TV + phones (Jackbox model), ~60min runs, "how you play shapes what you become" (frozen vision 2026-04-18).

### Game-Godot-v2
- **Short**: M1 Sistema Godot client/mirror (#342); finish Bond Phase 3.5d residue.
- **Mid**: M2 generational succession (lifecycle attrition + true-death) production; Bond system depth.
- **Long**: Godot = canonical frontend (Vue3 archive long-term); full gameplay systems (bond, succession, sistema) shippable.

### Game-Database
- **Short**: Fase 3 schema versioning Phase A (#154 TaxonomyVersion/snapshots) + DB hygiene (GIN indexes #155, slug constraints).
- **Mid**: complete schema versioning (revertable taxonomy changes) + curator audit-UI maturity (Fase 2 done).
- **Long**: robust canonical content backend -- versioned, auditable taxonomy provider feeding Game via evo:import.

### vault
- **Short**: pathfinder corpus ingest (478 md) + bloat triage (done partial).
- **Mid**: knowledge-base coverage (corpora ingested, agents at 7/7 production stable).
- **Long**: Karpathy LLM-wiki = complete personal/project knowledge layer, agent-queryable.

### evo-swarm (Dafne)
- **Short**: `dafne/portability-fix` (cross-PC portability).
- **Mid**: swarm produces integrable game content (trait/biome/lore) with confidence, low manual validation.
- **Long**: trusted AI content-orchestration meta-layer feeding Game design space at scale.

### codemasterdd
- **Short**: cross-repo goals layer (this); whisper stack SDMG empirical period.
- **Mid**: sovereign stack maturity (Hybrid A1 ADR-0030); coordination tooling (gated).
- **Long**: self-sufficient sovereign-first AI dev station + governance authority for ecosystem.

### Cross-cutting
- **M1 Sistema** (Game backend route <-> Godot client). Ordering: merge Game backend before Godot client (avoid client-on-missing-route). Active now.

## 5. D1 Architecture / data flow

- Per-repo goals = source of truth (self-governed).
- `GOALS.md` hub = synthesis, refreshed by repo-health-auditor agent (read-only aggregation, like STATUS_MULTI_REPO refresh). No write-back to repos.
- Agents read GOALS.md + repo goals for shared direction (context input). Action stays human/session-decided = Protocol 7 narrow-adoption (read-only flag).

## 6. D2 -- Auto-coordination (GATED, design-only, NOT built here)

Hypothesis space to explore SEPARATELY, bound to falsification:
- Option D2a: agent-assisted (agent reads goals+STATUS, PROPOSES next-action per repo, human approves). No auto-spawn.
- Option D2b: scheduled goal-drift monitor (read-only flag: "repo X drifting from declared Short goal").
- Option D2c (REJECTED zone): auto-spawn/orchestrate work cross-repo = HSGF F-FULL.

Gate (Protocol 7, mandatory before ANY build):
1. Design = hypothesis, not decision.
2. harsh-reviewer falsification PRE-build ("if rejects, adopt non-defend").
3. 2-week empirical gate (SDMG-gate landed 2026-05-20; not before ~2026-06-03).
4. New evidence required (HSGF was RETHINK-FUNDAMENTAL rejected). This session's multi-session coordination (text/audio/img split, M1 cross-repo, L-066 managed) = candidate evidence, to be assessed by harsh-reviewer.
5. Narrow adoption only: read-only / propose-approve, NEVER auto-trigger predicates (P7 step 6).

## 7. Testing / validation (D1)

- GOALS.md renders + links valid.
- Per-repo goal sections parse (no broken markdown).
- Each S/M/L horizon non-empty + concrete per repo.
- Cross-dep (M1) ordering stated.
- Eduardo review = acceptance gate for goal CONTENT (the draft in section 4 is hypothesis).

## 8. Out of scope

- Any automation / auto-trigger (D2 gated).
- Overwriting repo-internal governance.
- New tooling beyond GOALS.md + repo sections + existing repo-health-auditor refresh.
