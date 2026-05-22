# GOALS -- Cross-Repo Direction (S/M/L)

> Read-only hub synthesis. Canonical goals live per-repo (each repo's `## Goals (S/M/L)`).
> Refreshed by repo-health-auditor agent. Horizons: Short=sprint(weeks) / Mid=epic(1-2mo) / Long=vision(3-6mo).
> Last refresh: 2026-05-22 (all repos Short set: M1-full flagship for Game/Godot + 4-repo directions -- Game-DB Phase C-Game loop, vault synthesis-verify, evo-swarm integration-loop, codemasterdd Gate-E logging). Sources: docs/superpowers/specs/2026-05-21-cross-repo-goals-coordination-design.md + docs/superpowers/specs/2026-05-22-four-repo-short-directions-design.md

## Snapshot

| Repo | Short | Mid | Long | Cross-dep |
|------|-------|-----|------|-----------|
| Game (Vue3) | **M1-full: validate/playtest live Game<->Godot loop end-to-end** (PR #2384). M1 build CLOSED (#2363/#2364/#2376/#2377/#2365) | trait completeness (post-A4); M1 loop hardening from playtest | Co-op tactical shippable, TV+phones Jackbox, ~60min, "how you play shapes what you become" | M1 (loop) |
| Game-Godot-v2 | **M1-full: validate live loop client side** (render sistema_memory from read route) + finish Bond 3.5d (PR #352) | M2 generational succession prod; Bond depth | Canonical frontend (Vue3 archive); full systems shippable | M1 (loop) |
| Game-Database | **Phase C-Game wiring: close versioning loop** -- Game pins taxonomy version via `?versionId` from `EVO_TAXONOMY_VERSION` (RFC Section 5 item) (PR #165) | versioned reads Biome/Species/Eco; bidi-sync RFC #4 scoping; audit-UI hardening | Robust versioned auditable content backend (evo:import) | feeds Game |
| vault | **Synthesis fidelity-verify** -- verify ~84 draft cards (TBR->verified) + densify cross-refs (PR #176) | KB coverage; 7/7 agents stable (already met) | Complete personal/project knowledge layer, agent-queryable | -- |
| evo-swarm (Dafne) | **Close integration loop** -- 3-5 ready candidates triage->strict-verify->Game PR; ~1->>=10 integrated; born-ready live-validate first (PR #122) | Integrable game content low-manual-validation | Trusted AI content-orchestration meta-layer at scale | feeds Game |
| codemasterdd | **Gate-E evidence-logging** -- SDMG invocation log + Hybrid A1 cost/cite + H7 spend file; feeds ~06-03 hub-shape/D2 gate review (non-gated) | Sovereign stack maturity (ADR-0030 Hybrid A1); coordination tooling (gated) | Self-sufficient sovereign AI dev station + ecosystem governance | hub |

## Cross-cutting initiatives

- **M1 "Sistema"** (persistent cross-session AI learning). **Build CLOSED** -- Game route #2364 + pilot #2363 + passthrough #2376 + orphan-removal #2377; Godot client #342. Ordering constraint satisfied (backend route merged before client). **Now in validation Short** (Game PR #2384 + Godot PR #352): playtest the live Game<->Godot loop end-to-end, single-source read-route render path.
- **Content supply-chain into Game** (2026-05-22 direction theme). Game-Database closes the versioning loop (Game pins a taxonomy version, PR #165) and evo-swarm lands actual content (~1 -> >=10 integrated, PR #122) -- both feed Game and are Eduardo-gated at the Game-repo boundary. vault (synthesis-verify, PR #176) hardens the internal knowledge layer; codemasterdd (Gate-E logging) preps the ~06-03 coordination-gate review.

## Recent completions (2026-05-21 evening)

GOALS-layer first real cycle: chips read their per-repo `## Goals` -> advanced Short autonomously -> PR -> verified -> merged.
- **vault**: pathfinder corpus 477 reference cards + MOC (#155); 38 ChatGPT-export images caption+OCR vision-local (#153); OD-055 atomize-vs-reference principle (#156).
- **evo-swarm**: portability x3 -- OLLAMA_API_BASE knob (#106), home-relative workspace path + test (#107), preflight doctor script (#108).
- **Game/Godot**: M1 Sistema backend route + Godot client merged.
- **codemasterdd**: whisper-local stack (Ryzen + Lenovo, SDMG-gated ADOPT); D1 goals layer; autonomous-next-point protocol SDMG-REJECTED (cross-ref propagated to Game #2375).

**All Short goals set 2026-05-22** (human direction decision, not autonomous): M1-full flagship (Game/Godot) + 4-repo directions (rationale: `docs/superpowers/specs/2026-05-22-four-repo-short-directions-design.md`). Per-repo canonical PRs: #2384 (Game), #352 (Godot), #165 (Game-DB), #176 (vault), #122 (evo-swarm); codemasterdd row is the canonical (hub-and-repo collapse). Setting the next Short remains a human decision.

## Notes

- D2 auto-coordination = gated (harsh-reviewer + 2-week SDMG + new-evidence). See spec section 6. This file is READ-ONLY direction, no auto-trigger.
- SDMG empirical window: started 2026-05-20; hub-shape re-eval + D2 gate open ~2026-06-03. 2 invocations logged (whisper ADOPT, autonomous-next-point REJECT).
