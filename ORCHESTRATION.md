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
| Cloud keys | local-insufficient + repo cloud-OK + privacy-guard pass | `aider-groq-bypass`/`aider-cerebras`/`aider-gemini`/`aider-openai`/`aider-hf`/`aider-github-models <f>`; fleet-tools MCP (`tavily_search`/`openai_image`/`cross_check`) for services + non-Claude cross-check; keys from `~/.config/api-keys/keys.env` |
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

> **Rung status (revised 2026-06-01, ADR-0036 scope split).** Auto-merge is **default-OFF**;
> the ladder is ratified as a CLASSIFICATION taxonomy, not as live autonomy. Rungs earn up:
> **R0** report-only (live today: the 2 crons) -> **R1** open-PR / escalate, HUMAN merges (the
> next increment) -> **R2** auto-merge for the lowest-risk reversible class ONLY, granted by a
> dedicated ADR after >=4 clean R1 cycles + harsh-reviewer falsifies the increment + revert
> proven + a different-FAMILY judge (the harsh-reviewer is Claude = partial monoculture).
> Mechanical earn-path + clean-cycle definition + off-ramp (N=3): `docs/cross-repo/actor-activation-criteria.md`.
> Operationalized by the unified governor (cross-repo-dashboard promoted to observe->classify->act):
> `docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md`.

**Codex sub-gate (external-repo merge -- precise).** Codex runs AUTOMATIC PR review on
GitHub and posts comments that MUST be evaluated before proceeding:
1. WAIT for the Codex auto-review to complete (never auto-merge while pending).
2. Evaluate EVERY Codex comment: real issue -> fix; false-positive/nit -> dismiss with a
   one-line rationale. Zero unresolved actionable comments.
3. Re-run CI after fixes; require green.
4. Different-model judge (harsh-reviewer) OK.
5. AUTO-MERGE (squash + delete branch).
(Repos with NO Codex configured: skip 1-2; other gates still apply.)

Rollout (revised 2026-06-01): auto-merge (R2) is NOT live -- deferred per the ADR-0036 scope
split until earned via the `actor-activation-criteria.md` earn-path. R0 (report) is the first
rung to activate (when Fase-1 ships); R1 (open-PR, human merges) is the NEXT increment, unlocked
only after the R0 off-ramp passes (>=3 acted-on signals / 4 weeks). When R2 is earned by its own
ADR, the whitelisted repos are Game, Game-Godot-v2, codemasterdd, Game-Database.
Safety net = the gate stack + reversibility (revert). Bad merge -> revert + downgrade that
class to human-gated + amend ADR-0036.

## 6. Standing permission classes

Allow-listed (no per-action prompt; `.claude/settings.json`): read-ops; local git commit;
branch push (non-main); local-LLM dispatch (ollama / aider-* local); `jules remote
list/pull`; Jules `:archive` / `:sendMessage` (ADR-0034 scope). The auto-mode classifier
still gatekeeps; allow-rules only remove prompts on the verified-safe set. NEVER
allow-listed: the irreducible residue in sec 5.

## 6b. Journal / handoff landing (cross-fleet)

Recording session work to `JOURNAL.md` (and `COMPACT_CONTEXT.md` / memory) MUST use
`scripts/fleet/journal-land.ps1` on BOTH PCs. It branches `claude/journal-<host>-<date>`
(matches the `claude/*` push allow-rule, sec 6) from a freshly fetched origin/main, commits,
pushes via SSH (works on Lenovo + Ryzen today), and -- where gh is authed -- opens the PR and
auto-merges (squash); where gh is NOT authed (e.g. Ryzen's dead token) it pushes anyway so the
content reaches origin and the PR is a trivial hub follow-up (content never stranded). Rules:
- NEVER journal on a `chore/`/`docs/`-prefixed local branch -- it misses the push allow-rule and
  strands; the content then needs manual recovery on the hub (the bug this fixes).
- NEVER `git pull` while on a feature branch (`git pull --ff-only` on main only) -- pulling on a
  branch creates stray `ort` merge commits and diverges fleet HEADs.
Root cause + design: `docs/superpowers/specs/2026-05-29-journal-land-cross-fleet-design.md`.

## 7. Spoke invocation layer + adoption

10 keys in `~/.config/api-keys/keys.env` (ANTHROPIC, CEREBRAS, GEMINI, GITHUB_MODELS,
GOOGLE_GENERATIVE_AI, GROQ, HUGGINGFACE, JULES, OPENAI, TAVILY). Cloud/Jules/local spokes
are invoked via Bash (wrappers/CLI/REST). Two distinct tooling questions were separated by
the SDMG gate (eval: `docs/research/2026-05-29-mcp-llm-fleet-eval.md`):

- **General completion-routing MCP (`llm_call` to weaker cloud models for normal tasks) --
  REJECTED.** No caller: the hub Opus 4.8 is more capable than every callable cloud model;
  cloud-OK edits -> aider-*; sovereign-cheap -> Ollama; async -> Jules. That framing was
  LiteLLM-gateway-redux (OD-009 category). Do not build.
- **Fleet-tools (services + cross-check judge) -- GO (scoped; BUILT 2026-05-29, `apps/fleet-tools-mcp/`, registered in `.mcp.json`).**
  The cloud keys are used WITH Opus, not as competitors: (a) **services Opus lacks** --
  Tavily (web search) + OpenAI image generation; (b) **non-Claude cross-check judge** --
  Gemini/Groq as a DIFFERENT-model-family verifier for high-stakes (true anti-monoculture;
  harsh-reviewer alone is Claude = same family = partial monoculture); (c) deferrable /
  diverse-POV sub-tasks inside a multi-agent step. These have real, doctrine-aligned callers
  and are NOT cost-routing. Minimal MCP exposing `tavily_search`, `openai_image`, and
  `cross_check(model, prompt)`; keys from keys.env. SDMG-minimal build via its own spec/plan.

The keys are reached today via Aider edit-wrappers + Jules CLI + Ollama REST (proven).
Adoption rule (sec 3): reach for the cheapest-sufficient spoke; do not default to inline-Opus
out of forgetfulness; for high-stakes verification prefer a non-Claude cross-check.

## 8. Anti-scope

No heavy orchestration framework (LangGraph/CrewAI/AutoGen/claude-flow) -- evidence: more
failure surface than value for solo-dev. No heavy LLM gateway/proxy (LiteLLM/Bifrost/
Langfuse) -- decommissioned OD-009 as admin overhead. No Docker/observability stack for the
tooling layer. Rationale: `docs/adr/0036-unified-orchestration-doctrine.md`.
