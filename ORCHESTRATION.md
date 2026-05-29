# ORCHESTRATION.md -- cross-executor orchestration doctrine

> **Single authority** for "which executor for task X, at what autonomy, verified how."
> Why = `docs/adr/0036-unified-orchestration-doctrine.md`. How (operational session rules)
> = `CLAUDE.md`. Local-fleet detail = `MODEL_ROUTING.md`. This file is the entry point.
> ASCII-first (ADR-0021). Governs both fleet PCs (Lenovo .10 + Ryzen .11).

## 1. Purpose + authority

Coordination across LLMs/agents was fragmented (local-fleet doctrine + scattered cloud
ADRs + Jules). This doctrine unifies it: one hub orchestrator, five executor spokes, an
explicit routing tree, a mandatory verification gate, and an autonomy ladder. Consolidates
ADR-0013/0022/0023/0030/0034/0035 (they remain Accepted as detail).

## 2. Core model -- hub-and-spoke

Hub = Claude Code / Opus 4.8. It keeps judgment + verification; it never delegates the
verdict. Five spokes:

| Spoke | Role | Exact invocation |
|-------|------|------------------|
| Inline-Opus (hub) | strategic, multi-file, synthesis, architecture, ALL verification | (this session) |
| Local fleet | sovereign, cheap, scoped edits, batch, tagging | `ollama run <model>` / `aider-cosmetic <f>` / `aider-refactor <f>` / `opencode run --model "ollama/qwen3-coder:30b"` / REST `:11434` |
| Cloud keys | local-insufficient + repo cloud-OK + privacy-guard pass | `aider-groq-bypass`/`aider-cerebras`/`aider-gemini`/`aider-openai`/`aider-hf`/`aider-github-models <f>`; or `llm_call` (MCP llm-fleet once built); keys from `~/.config/api-keys/keys.env` |
| Jules async | well-defined + acceptance-criteria + scoped chore, whitelisted repo, ASCII-clean target, parallelizable | `jules remote new --repo <o/r> --session "<scoped task>"` + REST `jules.googleapis.com/v1alpha` (list/pull/`:archive`/`:sendMessage`) |
| In-session subagents / Workflow | parallel read/review/verify; deterministic fan-out | Agent tool (harsh-reviewer, Explore, godot-engine-specialist, ...) ; Workflow tool (opt-in) |

## 3. Routing decision-tree (capability x cost x privacy x async-fit)

Cost ladder: **inline-judgment > local-first > free-cloud > paid-cloud**. <=3 effective
tiers (debuggability). **Adoption rule: prefer the cheapest-sufficient spoke before
inline-Opus** -- inline-Opus is for judgment/synthesis/verification, not work a verified
cheaper spoke can do.

```
task ->
  exploratory / architecture / synthesis / multi-file / verification?  -> INLINE-OPUS
  scoped edit, sovereign or cheap, single-file?                        -> LOCAL FLEET
  local insufficient + repo cloud-OK + privacy-guard pass?             -> CLOUD KEYS
  well-defined chore + acceptance-criteria + whitelisted + ASCII-clean
       + parallelizable + reviewable async?                            -> JULES ASYNC
  need parallel read/review/verify or deterministic fan-out?           -> SUBAGENTS / WORKFLOW
```

Privacy: sovereign-only repos -> local only; cloud spokes gated by the privacy-guard
whitelist (`~/.config/aider-privacy-whitelist.txt`). ASCII-clean-target rule for Jules:
non-ASCII files are mangled on rewrite (mojibake) -- exclude or byte-verify (ADR-0035).

## 4. Verification gate (MANDATORY -- the bottleneck is verification, not generation)

Every NON-inline executor output passes this before it counts as done:

1. **CI green** (tests / lint / build) where applicable.
2. **Ground-truth triage** -- diff vs origin/main; ASCII check; scope check (single-file /
   named-target / no-logic-on-doc); run tests.
3. **Different-model judge** for high-stakes -- `harsh-reviewer` subagent (anti-monoculture;
   NOT self-judge -- the load-bearing reliability lever).
4. **Schema/scope validation** -- the scoped-prompt contract was honored.

Codifies R3-bis (ADR-0034) + ADR-0035 ground-truth triage + SDMG (ADR-0026 Protocol 7).

## 5. Autonomy ladder (automate the gate; do not delete it)

A human gate is removed ONLY when replaced by an automated gate of reliability >= AND the
action is reversible.

| Class | Gate |
|-------|------|
| Low-risk + automated-gate-green + reversible (docs/JSDoc/Jules-scoped-clean, branch+PR) | **AUTO-MERGE** (no human) |
| **External-repo merge** | **AUTO iff** CI green + Codex auto-review resolved + fixes applied (re-CI green) + different-model judge OK (see Codex sub-gate) |
| Medium + gate-green | auto + notify + easy-revert |
| Low automated-confidence (gate cannot decide) | escalate to human |
| **Irreversible/destructive (force-push main, rm -rf), outward-facing, account-credential, external-comms, ADR-class architecture, "what NOT to build"** | **HUMAN (irreducible)** |

**Codex sub-gate (external-repo merge -- precise).** Codex runs AUTOMATIC PR review on
GitHub and posts comments that MUST be evaluated before proceeding:
1. WAIT for the Codex auto-review to complete (never auto-merge while pending).
2. Evaluate EVERY Codex comment: real issue -> fix; false-positive/nit -> dismiss with a
   one-line rationale. Zero unresolved actionable comments.
3. Re-run CI after fixes; require green.
4. Different-model judge (harsh-reviewer) OK.
5. AUTO-MERGE (squash + delete branch).
(Repos with NO Codex configured: skip 1-2; other gates still apply.)

Rollout: FULL -- all whitelisted repos (Game, Game-Godot-v2, codemasterdd, Game-Database).
Safety net = the gate stack + reversibility (revert). Bad merge -> revert + downgrade that
class to human-gated + amend ADR-0036.

## 6. Standing permission classes

Allow-listed (no per-action prompt; `.claude/settings.json`): read-ops; local git commit;
branch push (non-main); local-LLM dispatch (ollama / aider-* local); `jules remote
list/pull`; Jules `:archive` / `:sendMessage` (ADR-0034 scope). The auto-mode classifier
still gatekeeps; allow-rules only remove prompts on the verified-safe set. NEVER
allow-listed: the irreducible residue in sec 5.

## 7. Spoke invocation layer + adoption

10 keys in `~/.config/api-keys/keys.env` (ANTHROPIC, CEREBRAS, GEMINI, GITHUB_MODELS,
GOOGLE_GENERATIVE_AI, GROQ, HUGGINGFACE, JULES, OPENAI, TAVILY). Cloud/Jules/local spokes
are invoked via Bash (wrappers/CLI/REST) -- they are NOT native tools today. The **MCP
llm-fleet** (when built, SDMG-gated) exposes `llm_call(provider, model, prompt,
[max_tokens])` as a native tool so the keys are first-class. Adoption rule (sec 3): reach
for the cheapest-sufficient spoke; do not default to inline-Opus out of forgetfulness.

## 8. Anti-scope

No heavy orchestration framework (LangGraph/CrewAI/AutoGen/claude-flow) -- evidence: more
failure surface than value for solo-dev. No heavy LLM gateway/proxy (LiteLLM/Bifrost/
Langfuse) -- decommissioned OD-009 as admin overhead. No Docker/observability stack for the
tooling layer. Rationale: `docs/adr/0036-unified-orchestration-doctrine.md`.
