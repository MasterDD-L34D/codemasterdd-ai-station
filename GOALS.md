# GOALS -- Cross-Repo Direction (S/M/L)

> Read-only hub synthesis. Canonical goals live per-repo (each repo's `## Goals (S/M/L)`).
> Refreshed by repo-health-auditor agent. Horizons: Short=sprint(weeks) / Mid=epic(1-2mo) / Long=vision(3-6mo).
> Last refresh: 2026-05-22 (Short re-set: M1-full flagship thread chosen -- Game/Godot Short promoted to live-loop validation; other 4 repos still await direction). Source: docs/superpowers/specs/2026-05-21-cross-repo-goals-coordination-design.md

## Snapshot

| Repo | Short | Mid | Long | Cross-dep |
|------|-------|-----|------|-----------|
| Game (Vue3) | **M1-full: validate/playtest live Game<->Godot loop end-to-end** (PR #2384). M1 build CLOSED (#2363/#2364/#2376/#2377/#2365) | trait completeness (post-A4); M1 loop hardening from playtest | Co-op tactical shippable, TV+phones Jackbox, ~60min, "how you play shapes what you become" | M1 (loop) |
| Game-Godot-v2 | **M1-full: validate live loop client side** (render sistema_memory from read route) + finish Bond 3.5d (PR #352) | M2 generational succession prod; Bond depth | Canonical frontend (Vue3 archive); full systems shippable | M1 (loop) |
| Game-Database | ✅ schema versioning Phase A #154 + GIN #155 MERGED -- Short done. **Next: set new Short** (versioning complete from Mid) | Versioning complete (revertable taxonomy); audit-UI mature | Robust versioned auditable content backend (evo:import) | feeds Game |
| vault | ✅ Pathfinder ingest DONE (#155, 477 cards) + bloat triage (#145). **Next: set new Short** (KB coverage from Mid) | KB coverage; 7/7 agents stable | Complete personal/project knowledge layer, agent-queryable | -- |
| evo-swarm (Dafne) | ✅ portability DONE (#106 OLLAMA_API_BASE, #107 workspace-path+test, #108 preflight doctor). **Next: set new Short** (integrable content from Mid) | Integrable game content low-manual-validation | Trusted AI content-orchestration meta-layer at scale | feeds Game |
| codemasterdd | ✅ GOALS-layer D1 live; whisper adopted (SDMG empirical ~06-03). **Next:** hub-shape re-eval post-2-week | Sovereign stack maturity (ADR-0030 Hybrid A1); coordination tooling (gated) | Self-sufficient sovereign AI dev station + ecosystem governance | hub |

## Cross-cutting initiatives

- **M1 "Sistema"** (persistent cross-session AI learning). **Build CLOSED** -- Game route #2364 + pilot #2363 + passthrough #2376 + orphan-removal #2377; Godot client #342. Ordering constraint satisfied (backend route merged before client). **Now in validation Short** (Game PR #2384 + Godot PR #352): playtest the live Game<->Godot loop end-to-end, single-source read-route render path.

## Recent completions (2026-05-21 evening)

GOALS-layer first real cycle: chips read their per-repo `## Goals` -> advanced Short autonomously -> PR -> verified -> merged.
- **vault**: pathfinder corpus 477 reference cards + MOC (#155); 38 ChatGPT-export images caption+OCR vision-local (#153); OD-055 atomize-vs-reference principle (#156).
- **evo-swarm**: portability x3 -- OLLAMA_API_BASE knob (#106), home-relative workspace path + test (#107), preflight doctor script (#108).
- **Game/Godot**: M1 Sistema backend route + Godot client merged.
- **codemasterdd**: whisper-local stack (Ryzen + Lenovo, SDMG-gated ADOPT); D1 goals layer; autonomous-next-point protocol SDMG-REJECTED (cross-ref propagated to Game #2375).

**Next Short goals = Eduardo to set** (promote from Mid, or new direction). The layer marks Short as done; setting the next Short is a human direction decision (not autonomous).

## Notes

- D2 auto-coordination = gated (harsh-reviewer + 2-week SDMG + new-evidence). See spec section 6. This file is READ-ONLY direction, no auto-trigger.
- SDMG empirical window: started 2026-05-20; hub-shape re-eval + D2 gate open ~2026-06-03. 2 invocations logged (whisper ADOPT, autonomous-next-point REJECT).
