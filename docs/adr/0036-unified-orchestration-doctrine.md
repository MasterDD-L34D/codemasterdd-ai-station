# ADR-0036 — Unified Orchestration Doctrine (multi-LLM + Jules + Opus 4.8)

> Status: **Accepted (spine)** + **Deferred (auto-merge rung)** -- revised 2026-06-01 (orig Proposed 2026-05-29). The doctrine spine (hub-and-spoke, 5 spokes, routing tree, mandatory verification gate, ladder-as-classification) is ratified on already-practiced evidence. The auto-merge rung is deferred to a future R2 ADR via the earn-path in `docs/governance/actor-activation-criteria.md`. A harsh-reviewer falsification (2026-06-01) corrected the original trigger framing (not "circular" but SDMG-incompatible). See "Ratify scope split".
> Supersedes-as-routing-authority (consolidates, does not deprecate): ADR-0013, 0022, 0023, 0030, 0034, 0035. Reframes: MODEL_ROUTING.md as local-fleet detail.
> Operational authority: `ORCHESTRATION.md` (root). This ADR = the why; ORCHESTRATION.md = the which-executor-and-autonomy; CLAUDE.md = the how.

## TL;DR

Adopt one hub-and-spoke orchestrator-worker doctrine for all repos. **Hub = Claude Code /
Opus 4.8** (keeps judgment + verification). **5 executor spokes**: inline-Opus, local
Ollama fleet, cloud-key LLMs, Jules async coding agent, in-session subagents/Workflow.
Route by capability x cost x privacy x async-fit (cheapest-sufficient-first, <=3 tiers).
**Mandatory verification gate** with a DIFFERENT-model judge (anti-monoculture). **Autonomy
ladder**: auto-merge low-risk + external-merge-auto (CI + Codex-auto-review-resolved + fix
+ judge); irreducible human residue for irreversible/outward-facing/architecture. **NOTE (revised 2026-06-01): the auto-merge rung is DEFERRED -- only the spine is ratified now; auto-merge is granted later via the earn-path (see "Ratify scope split").** Tooling: a general
completion-routing MCP was **SDMG-REJECTED** (no caller; gateway-redux), but a **scoped
fleet-tools MCP = GO** -- services Opus lacks (Tavily search, OpenAI image-gen) + a
non-Claude cross-check judge (anti-monoculture), used WITH Opus, not as competitors.
Explicit anti-scope: no LangGraph/CrewAI/AutoGen/LiteLLM-redux.

## Context

Coordination capability is rich but FRAGMENTED: `MODEL_ROUTING.md` + llmfit cover only the
local sovereign fleet; the cloud + async layer is scattered across ADR-0013 (cloud-free
tiers), 0022 (OpenCode tool-use), 0023 (strategic Claude API), 0030 (Hybrid A1 post-Max),
0034 (Jules managed-owner), 0035 (Jules CLI dispatch), plus a key-and-task-routing matrix
and 8 Aider/OpenCode wrappers. No single artifact answers "for task X: which executor, at
what autonomy, verified how." OD-009 (2026-05-29) decommissioned the LiteLLM+Langfuse stack
as solo-dev admin overhead -- so the unified layer must be lightweight, not a gateway.

Evidence basis (multi-source web research 2026-05-29, see References): orchestrator-worker
is the dominant pattern; verification (not generation) is the bottleneck; a different-model
judge breaks monoculture blind spots; specification failures (vague prompts) are the #1
multi-agent failure mode; routing should use the smallest sufficient model with <=3 tiers;
async coding agents are delegated junior-devs (scoped, acceptance-criteria, never
direct-to-main); heavy frameworks add more failure surface than value for a solo dev.

## Decision

Establish the doctrine operationalized in `ORCHESTRATION.md`:

1. **Hub-and-spoke orchestrator-worker.** Opus 4.8 hub coordinates; never delegates the
   verdict. Five spokes with explicit invocation paths (inline; `ollama`/aider-* wrappers;
   cloud-key wrappers/REST; `jules` CLI+REST; Agent tool + Workflow tool).
2. **Routing decision-tree** by capability x cost x privacy x async-fit. Cost ladder:
   inline-judgment > local-first > free-cloud > paid-cloud. Adoption rule:
   cheapest-sufficient spoke before inline-Opus. <=3 effective tiers for debuggability.
3. **Mandatory verification gate** for every non-inline output: CI + ground-truth triage
   (diff vs origin, ASCII, scope, tests) + DIFFERENT-model judge (harsh-reviewer) for
   high-stakes + schema/scope validation. Codifies R3-bis (ADR-0034) + ADR-0035
   ground-truth triage + SDMG (ADR-0026 Protocol 7).
4. **Autonomy ladder** (automate the gate, do not delete it): auto-merge low-risk +
   reversible; **external-repo merge AUTO** iff CI green + Codex auto-review resolved
   (wait -> evaluate every comment -> fix real / dismiss nit-with-rationale -> re-CI) +
   different-model judge OK; irreducible human residue = irreversible/destructive,
   outward-facing, account-credential, external-comms, ADR-class architecture,
   low-automated-confidence. Standing allow-rules for verified-safe action classes.
5. **Spoke invocation = Bash today; one SCOPED fleet-tools MCP = GO (build via own spec).**
   The SDMG gate (eval: `docs/research/2026-05-29-mcp-llm-fleet-eval.md`) separated two
   designs: (i) a general completion-routing MCP (`llm_call` to weaker cloud models for
   normal tasks) -- **REJECTED** (no caller -- hub more capable; cloud-OK work = edits ->
   aider-*; LiteLLM-gateway-redux per OD-009). (ii) a **fleet-tools MCP -- GO**: services
   the hub lacks (Tavily `tavily_search`, OpenAI `openai_image`) + a non-Claude
   `cross_check(model, prompt)` judge (DIFFERENT-model-family verification = true
   anti-monoculture; the harsh-reviewer is itself Claude). These are used WITH Opus inside
   multi-agent steps (cross-check, diverse-POV, deferrable, missing-capability), have real
   doctrine-aligned callers, and are NOT cost-routing. Keys from keys.env. Build is
   SDMG-minimal via its own spec/plan. Bash wrappers + Jules CLI + Ollama REST remain for
   their existing edit/dispatch roles.
6. **Anti-scope**: no heavy orchestration framework; no Docker/proxy/observability stack
   for the tooling layer.

## Options considered

- **A -- Streamline/unify (CHOSEN).** One authority + decision-tree + autonomy ladder +
  lightweight MCP. Codifies what evidence + our own practice already validate. Lowest
  failure surface.
- **B -- A + heavier tooling** (LiteLLM proxy / dispatch service). Rejected: OD-009
  decommissioned exactly this as overhead; gold-plating.
- **C -- Adopt a heavy framework** (LangGraph/CrewAI/AutoGen/claude-flow). Rejected:
  evidence shows coordination overhead frequently underperforms single-agent for solo-dev;
  more failure surface than value.
- **D -- Status quo (stay fragmented).** Rejected: no single entry point; the orchestrator
  forgets spokes and defaults to inline-Opus (adoption gap).

## Supersession map

| Artifact | Disposition under ADR-0036 |
|----------|----------------------------|
| ADR-0013 (cloud-free tiers) | Routing surface consolidated; remains Accepted as cloud-tier detail |
| ADR-0022 (OpenCode tool-use) | Consolidated; remains Accepted as multi-step-agentic detail |
| ADR-0023 (strategic Claude API) | Consolidated; remains Accepted as paid-tier-0 detail |
| ADR-0030 (Hybrid A1 post-Max) | Consolidated; remains Accepted as subscription-stack detail |
| ADR-0034 (Jules managed-owner) | Consolidated; remains Accepted as Jules-governance detail (R3-bis lives in the verification gate) |
| ADR-0035 (Jules CLI dispatch) | Consolidated; remains Accepted as async-spoke routine detail |
| MODEL_ROUTING.md | Reframed as the LOCAL-FLEET detail under ORCHESTRATION.md |

Individual ADRs keep Accepted status; the cross-executor entry point is ORCHESTRATION.md.

## Consequences

**Positive:** single routing/orchestration entry point; evidence-based autonomy that
removes prompt friction where safe; cloud keys become first-class tools (closes the
discoverability/adoption gap); doctrine governs both fleet PCs.

**Negative / risk:** full-rollout external-merge-auto is the most aggressive step
(anti-pattern #10 bot-rewrite-drop was a real incident). Load-bearing mitigations:
different-model judge (not self-judge), Codex auto-review resolution, CI, and
**reversibility** (git revert / branch+PR) -- which is precisely why auto-MERGE is
permitted at full rollout while irreversible actions stay human-gated.

## Ratify scope split (revised 2026-06-01)

A harsh-reviewer falsification (SDMG Cognitive Protocol 7, step 3) found the original
single "Ratify trigger" both mis-framed and over-scoped. Corrected:

**Ratified now (spine, Accepted):** hub-and-spoke, the 5 executor spokes, the routing
decision-tree, the mandatory verification gate, and the autonomy ladder AS A
CLASSIFICATION TAXONOMY. These are already-practiced and evidence-backed (two crons --
vault coherence-pass report-only + codemasterdd playtest2-board-sync PR-only -- already
run the lower rungs clean).

**Deferred (auto-merge rung):** the original trigger ("observe >=1 clean
external-merge-auto cycle per repo, then ratify") is not circular but is
SDMG-INCOMPATIBLE: it asks you to RUN auto-merge to GENERATE its own ratify-evidence,
which Protocol 7 (no autonomize-before-falsify) and anti-pattern #10 (bot-rewrite-drop,
a real incident) forbid. Replacement: a rung-by-rung earn-path where evidence accrues at
a lower, REVERSIBLE rung (R1 = open-PR, human-merges) first. Auto-merge (R2) is granted
only by a dedicated future ADR after the mechanical conditions in
`docs/governance/actor-activation-criteria.md` are met (>=4 clean R1 cycles across >=2
repos over >=2 weeks + harsh-reviewer falsifies the increment + revert proven +
different-family judge). If a bad merge ever lands, revert + downgrade that class to
human-gated + amend.

This doctrine is operationalized by the unified governor (the cross-repo-dashboard
promoted to an active observe->classify->act loop); design + phased rollout:
`docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md`.

## References

- `docs/superpowers/specs/2026-05-29-orchestration-doctrine-design.md` (design + research appendix)
- Web research 2026-05-29: Anthropic multi-agent-research-system + Claude Agent SDK; A.
  Osmani "code agent orchestra"; Tembo "background coding agents"; augmentcode + Redis
  "why multi-agent LLM systems fail"; Hannecke "LLM routing Ollama+LiteLLM"; lushbinary
  "orchestration patterns".
- OD-009 (LiteLLM/Langfuse decommission), ADR-0026 (cognitive protocols / SDMG), anti-pattern catalogue #8/#10/#12.
- `docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md` (unified governor design + phased rollout, harsh-reviewer-falsified 2026-06-01).
- `docs/governance/actor-activation-criteria.md` (autonomy-rung earn-path + mechanical clean-cycle + off-ramp decision rule N=3).
