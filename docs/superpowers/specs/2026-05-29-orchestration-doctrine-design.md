# Design spec -- Unified Orchestration Doctrine (multi-LLM + Jules + Opus 4.8, cross-repo)

> **Status (2026-06-23):** shipped -- ADR-0036 Accepted 2026-06-01 + ORCHESTRATION.md live

> Status: DESIGN (brainstorming output, pending user review -> writing-plans).
> Date: 2026-05-29. Author: Claude Code hub (Opus 4.8), Lenovo.
> Approach chosen: **A -- Streamline/unify** (evidence-driven; reject heavy frameworks).

## Problem

Coordination capability across LLMs/agents is rich but FRAGMENTED: a sovereign-only
local-fleet routing doctrine (`MODEL_ROUTING.md` + llmfit) plus scattered cloud ADRs
(0013/0022/0023/0030), a key-and-task-routing matrix, 8 Aider/OpenCode wrappers, and a
just-ratified Jules dispatch routine (ADR-0035). No single authority answers "for task X,
which executor, at what autonomy, verified how." Goal: ONE doctrine, evidence-grounded,
for coordinating future work across all repos -- adopt/streamline/expand on evidence.

## Research basis (multi-source, 2026-05-29)

Direct web fetch (the deep-research workflow's fetch layer failed; sources fetched
directly + triangulated). Convergent findings:

- **Orchestrator-worker (supervisor) is the dominant pattern**; Router for simple
  classification (best fit for solo hub-and-spoke); Swarm = high-throughput/low-
  predictability (avoid solo). (lushbinary, Anthropic)
- **Multi-agent beats single-agent ~90% on breadth-first research but costs ~15x tokens
  and is a POOR fit for shared-context / interdependent work like most coding.**
  (Anthropic multi-agent-research-system)
- **The bottleneck is VERIFICATION, not generation.** Independent judge with a DIFFERENT
  model (anti-monoculture: same model = same blind spots), rules-based gates, schema
  validation. (Osmani, Redis, Claude Agent SDK)
- **Failure-mode distribution:** specification 41.77% (vague prompts) > coordination
  36.94% > verification-gaps 21.30%. Fix #1 = scoped explicit contracts. (augmentcode)
- **Routing:** smallest model that reliably completes; <=3 tiers for debuggability;
  ~70-80% local cap; pin versions; fallback chains; ~88% cost reduction routing ~70%
  local. (Hannecke, Ollama+LiteLLM)
- **Async coding agents:** delegate well-defined + acceptance-criteria + scoped;
  inline for exploratory; treat agent PRs like junior-dev submissions; never direct-to-
  main without review; scoped permissions. (Tembo, Osmani)
- **Heavy frameworks (LangGraph/CrewAI/AutoGen/claude-flow) add coordination overhead
  that frequently UNDERperforms single-agent for solo-dev; more failure surface than
  value.** -> NOT adopted.

**Key insight:** our existing practices already embody the evidence-based best practices
(ADR-0035 scoped prompt = fix #1; R3-bis + harsh-reviewer = different-model verification;
llmfit/MODEL_ROUTING = tiered routing; SDMG = living-spec discipline). The gap is
FRAGMENTATION + discoverability, not capability. Hence streamline-unify, not expand.

## Deliverable shape (anti-fragmentation)

ONE authority: **`ORCHESTRATION.md`** (repo root) = doctrine + decision-tree + autonomy
ladder + verification gate + spoke invocation layer. Backed by **ADR-0036** (records the
decision + supersedes/links the fragments). `MODEL_ROUTING.md` stays as local-fleet detail
(linked, not duplicated); the key-matrix + ADR-0013/0022/0023/0030/0034/0035 become
referenced spokes. Net: -1 fragmentation, single entry point.

## 1. Core model -- hub-and-spoke orchestrator-worker

**Hub orchestrator = Claude Code / Opus 4.8** (keeps judgment + verification; never
delegates the decision). Five executor spokes:

1. **Inline-Opus (hub)** -- strategic, multi-file, synthesis, architecture, and ALL
   verification. The hub does not delegate the verdict.
2. **Local fleet** (Ollama / llmfit, Ryzen + Lenovo) -- sovereign, cheap, scoped
   (cosmetic/behavior edits, batch, tagging). Invocation: `ollama run` / aider-cosmetic /
   aider-refactor / OpenCode local / REST `:11434`.
3. **Cloud keys** -- when local insufficient AND repo cloud-OK AND privacy-guard passes.
   Invocation: `aider-groq-bypass` / `aider-cerebras` / `aider-gemini` / `aider-openai` /
   `aider-hf` / `aider-github-models` (Bash wrappers), OpenCode, or direct REST with keys
   sourced from `~/.config/api-keys/keys.env`.
4. **Jules async** (ADR-0035) -- well-defined + acceptance-criteria + scoped chores on
   whitelisted repos, parallelizable, ASCII-clean target files. Invocation: `jules remote
   new/list/pull` + REST `jules.googleapis.com/v1alpha`.
5. **In-session subagents** (Agent tool: harsh-reviewer, Explore, godot-specialist, etc.)
   + **Workflow tool** (deterministic fan-out, opt-in only).

## 2. Spoke invocation layer + adoption (closes the discoverability gap)

The cloud/Jules/local spokes are NOT native or MCP tools -- they are invoked via **Bash**
(wrappers `.cmd` / CLIs / direct REST with keys.env). Capability is proven (Jules driven
end-to-end via CLI+REST 2026-05-29). The risk is the orchestrator FORGETTING a spoke and
defaulting to inline-Opus (the adoption gap). Mitigations (doc-only, no new tooling --
evidence: avoid gold-plating; wrappers already work):

- The decision-tree below lists EACH spoke with its exact one-line invocation.
- **Adoption rule:** prefer the cheapest-sufficient spoke before inline-Opus; inline-Opus
  is for judgment/synthesis/verification, not for work a cheaper spoke can verifiably do.
- 10 keys present: ANTHROPIC, CEREBRAS, GEMINI, GITHUB_MODELS, GOOGLE_GENERATIVE_AI, GROQ,
  HUGGINGFACE, JULES, OPENAI, TAVILY.

**Tooling -- MCP "llm-fleet" (decided 2026-05-29, was wrongly deferred).** Build a
lightweight stdio MCP server (~100 lines, Node or Python) that reads `keys.env` and
exposes ONE first-class tool `llm_call(provider, model, prompt, [max_tokens])` covering
the OpenAI-compatible endpoints (Groq, Cerebras, OpenAI, HuggingFace router, GitHub
Models) + Gemini. This closes the discoverability gap directly: the cloud keys become
NATIVE tools in the orchestrator's toolset (today they are Bash-only, invisible to the
user). It is NOT a heavy gateway -- LiteLLM-MCP and Bifrost are explicitly rejected as the
admin-overhead category Eduardo decommissioned 2026-05-29 (OD-009: LiteLLM+Langfuse =
overhead without proportional value for solo-dev). The MCP is stdio (no Docker, no proxy,
no Langfuse), keys stay in keys.env (not in argv). **Build is SDMG-gated** (Protocol 7 +
anti-pattern #8 no shallow-adopt): research the minimal viable shape -> external
falsification (harsh-reviewer + smoke) -> build minimal only if it survives. The Aider
edit-wrappers + Jules CLI + Ollama REST remain for their existing roles; llm-fleet adds
the missing general-completion path.

## 3. Routing decision-tree (capability x cost x privacy x async-fit)

Cost ladder: **inline-judgment > local-first > free-cloud > paid-cloud**. Async-fit:
well-defined + acceptance-criteria + scoped -> Jules; exploratory/interdependent ->
inline. Privacy: sovereign-only repos -> local only (privacy-guard whitelist gates cloud).
<=3 effective tiers for debuggability.

```
task ->
  exploratory / architecture / synthesis / multi-file / verification?  -> INLINE-OPUS
  scoped edit, sovereign or cheap, single-file?                        -> LOCAL FLEET
  local insufficient + repo cloud-OK + privacy-guard pass?             -> CLOUD KEYS
  well-defined chore + acceptance-criteria + whitelisted + ASCII-clean
       + parallelizable + can review async?                            -> JULES ASYNC
  need parallel read/review/verify or deterministic fan-out?           -> SUBAGENTS / WORKFLOW
```

## 4. Verification gate (MANDATORY -- the bottleneck)

Every NON-inline executor output passes an automated gate before it counts as done:

- **CI green** (tests / lint / build) where applicable.
- **Ground-truth triage** -- diff vs origin/main; ASCII check (ADR-0021); scope check
  (single-file / named-target / no-logic-on-doc); run tests.
- **Different-model judge** for high-stakes -- harsh-reviewer (anti-monoculture; NOT
  self-judge -- the load-bearing reliability lever per Redis/Osmani).
- **Schema/scope validation** -- the scoped-prompt contract was honored.

Codifies R3-bis (ADR-0034) + ADR-0035 ground-truth triage + SDMG (Protocol 7).

## 5. Autonomy policy / gate-removal (automate the gate; do not delete it)

Principle: a human gate is removed ONLY when replaced by an automated gate of
reliability >=, AND the action is reversible. Invest in automated verification +
reversibility -> drop more human gates.

| Class | Gate |
|-------|------|
| Low-risk + automated-gate-green + reversible (docs/JSDoc/Jules-scoped-clean, branch+PR) | **AUTO-MERGE** (no human) |
| **External-repo merge** | **AUTO if ALL of: CI green + Codex auto-review resolved + fixes applied (re-CI green) + different-model judge OK** (see Codex sub-gate) |
| Medium + gate-green | auto + notify + easy-revert |
| Low automated-confidence (gate cannot decide) | escalate to human |
| **Irreversible / destructive (force-push main, rm -rf) / outward-facing / account-credential / external-comms / ADR-class architecture / "what NOT to build"** | **HUMAN (irreducible)** |

**Codex sub-gate (external-repo merge -- precise):** Codex runs AUTOMATIC PR review on
GitHub and posts comments that MUST be evaluated before proceeding. Therefore:
1. WAIT for the Codex auto-review to complete (never auto-merge while it is pending).
2. Evaluate EVERY Codex comment: real issue -> fix; false-positive/nit -> dismiss with a
   one-line rationale. Zero unresolved actionable comments.
3. Re-run CI after fixes; require green.
4. Different-model judge (harsh-reviewer) OK.
5. Then AUTO-MERGE (squash + delete branch).
   (Repos with NO Codex configured: skip step 1-2; the other gates still apply.)

**Honest risk note:** external-merge-auto is the most aggressive step. Anti-pattern #10
(bot-rewrite-drop on external repos) was a real incident. The load-bearing mitigations are
the different-model judge (not self-judge), the Codex resolution, CI, and **reversibility
(git revert)** -- which is exactly why auto-MERGE (reversible) is permitted while
force-push-main (irreversible) stays human-gated.

## 6. Standing permission rules (reduce prompt friction)

Verified-safe action classes get `settings.json` allow-rules (no per-action prompt):
read-ops, local commit, branch push (non-main), local-LLM dispatch, Jules
list/pull/archive/sendMessage (ADR-0034 scope). The auto-mode classifier still gatekeeps
risky actions; allow-rules only remove prompts on the verified-safe set. Irreducible
classes (sec 5) are never allow-listed.

## 7. Opus 4.8 angle

Hub orchestration primitives leveraged: subagents (Agent tool), Workflow tool
(deterministic fan-out / opt-in), fast mode, long context, compaction. The 2026-05-29
session is the working proof of the orchestrator pattern (Jules dispatch + triage +
subagent review + workflow research, all hub-coordinated).

## Anti-scope (explicit)

- NO heavy orchestration framework (LangGraph/CrewAI/AutoGen/claude-flow) -- evidence:
  more failure surface than value for solo-dev.
- NO heavy LLM gateway/proxy (LiteLLM, Bifrost, Langfuse) -- decommissioned 2026-05-29
  (OD-009) as solo-dev admin overhead; the MCP llm-fleet is stdio/keys.env only, NOT a
  gateway.
- NO Docker/proxy/observability-stack for the tooling layer.

## Evidence appendix (sources)

- Anthropic, "Building a multi-agent research system" (orchestrator-worker; 90.2%; 15x
  tokens; poor fit for coding/shared-context).
- Claude Agent SDK, "Building agents" (agent loop context->act->verify; subagents isolated
  context; rules-based / visual / LLM-judge verification; compaction).
- A. Osmani, "Code agent orchestra" (verification is the bottleneck; plan-approval + hooks
  + AGENTS.md; WIP 3-5; kill stuck-3-iter; worktrees; one-file-one-owner; delegate scoped
  / retain architecture).
- Tembo, "Background coding agents" (delegate well-defined; inline exploratory; junior-dev
  PR review; never direct-to-main; scoped perms).
- augmentcode, "Why multi-agent LLM systems fail" (spec 41.77% / coord 36.94% / verify
  21.30%; JSON-schema contracts; structured messaging; judge agents; circuit breakers).
- Redis, "Why multi-agent LLM systems fail" (error compounding; conformity bias; MODEL
  MONOCULTURE -> different-model verification; context rot; stale state; single-agent
  baseline first).
- Hannecke, "LLM model routing with Ollama + LiteLLM" (3-tier; latency/semantic/RouteLLM;
  <=3 tiers; pin versions; ~88% cost cut at ~70% local).
- lushbinary, "Multi-agent orchestration patterns" (supervisor/router/pipeline/swarm;
  router best for solo hub-and-spoke).

## Decisions (user-confirmed 2026-05-29)

- **MCP llm-fleet**: BUILD (SDMG-gated), lightweight stdio, keys.env -> native `llm_call`
  tool. NOT a heavy gateway.
- **ADR-0036**: FULL MADR ADR (context/decision/options/consequences + supersession map of
  ADR-0013/0022/0023/0030/0034/0035; MODEL_ROUTING reframed as local-fleet detail).
- **Auto-merge rollout**: FULL -- all whitelisted repos at once (Game, Game-Godot-v2,
  codemasterdd, Game-Database), NOT a pilot. User accepted the higher risk.
  **Risk note (honest):** full rollout of external-merge-auto is the most aggressive step;
  the load-bearing safety net is the automated gate stack (CI + Codex auto-review resolved
  + fixes + different-model judge) plus reversibility (git revert / branch+PR is reversible,
  unlike force-push). If a bad merge lands, the recovery is revert -- which is why
  auto-MERGE is permitted at full rollout while irreversible actions stay human-gated.

## Deliverables (build order, for writing-plans)

1. **ADR-0036** (full) -- the decision record + supersession map.
2. **ORCHESTRATION.md** (root) -- the operational doctrine: core model, decision-tree,
   verification gate, autonomy ladder, spoke invocation layer, adoption rule. MODEL_ROUTING
   linked (not duplicated); fragments referenced.
3. **MCP llm-fleet** -- SDMG-gated build (research -> falsify -> minimal). Register in
   `.mcp.json` / settings so `llm_call` is a native tool.
4. **Autonomy enablement** -- settings.json allow-rules for verified-safe action classes +
   the auto-merge gate procedure (incl. Codex sub-gate) documented + applied across all
   whitelisted repos (full rollout).
5. **Cross-fleet deploy** -- doctrine + allow-rules deploy to Lenovo + Ryzen (this doctrine
   governs both PCs).
