# GOALS -- Cross-Repo Direction (S/M/L)

> Read-only hub synthesis. Canonical goals live per-repo (each repo's `## Goals (S/M/L)`).
> Refreshed by repo-health-auditor agent. Horizons: Short=sprint(weeks) / Mid=epic(1-2mo) / Long=vision(3-6mo).
> Last refresh: 2026-05-21. Source: docs/superpowers/specs/2026-05-21-cross-repo-goals-coordination-design.md

## Snapshot

| Repo | Short | Mid | Long | Cross-dep |
|------|-------|-----|------|-----------|
| Game (Vue3) | Close M1 Sistema (route #2364 + pilot #2363); hardcore band revision (#2365) | M1 full Game<->Godot; trait completeness | Co-op tactical shippable, TV+phones Jackbox, ~60min, "how you play shapes what you become" | M1 (backend) |
| Game-Godot-v2 | M1 Sistema Godot client (#342); Bond 3.5d residue | M2 generational succession prod; Bond depth | Canonical frontend (Vue3 archive); full systems shippable | M1 (client) |
| Game-Database | Fase 3 schema versioning Phase A (#154); DB hygiene (#155 GIN, slug) | Versioning complete (revertable taxonomy); audit-UI mature | Robust versioned auditable content backend (evo:import) | feeds Game |
| vault | Pathfinder corpus ingest + bloat triage | KB coverage; 7/7 agents stable | Complete personal/project knowledge layer, agent-queryable | -- |
| evo-swarm (Dafne) | dafne/portability-fix | Integrable game content low-manual-validation | Trusted AI content-orchestration meta-layer at scale | feeds Game |
| codemasterdd | This goals layer; whisper SDMG empirical | Sovereign stack maturity (ADR-0030 Hybrid A1); coordination tooling (gated) | Self-sufficient sovereign AI dev station + ecosystem governance | hub |

## Cross-cutting initiatives

- **M1 "Sistema"** (persistent cross-session AI learning). Spans Game backend (route sistema-state #2364 + pilot #2363) + Godot client/mirror (#342, spec #340). **Ordering constraint:** merge Game backend route BEFORE Godot client (avoid client-on-missing-route, drift-seam L-066).

## Notes

- D2 auto-coordination = gated (harsh-reviewer + 2-week SDMG + new-evidence). See spec section 6. This file is READ-ONLY direction, no auto-trigger.
