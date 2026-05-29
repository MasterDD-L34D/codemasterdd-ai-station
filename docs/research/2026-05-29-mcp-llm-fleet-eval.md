# MCP llm-fleet -- SDMG falsification eval (2026-05-29)

> SDMG (ADR-0026 Protocol 7 + anti-pattern #8) gate for a self-designed tool before build.
> Verdict: **NO-GO (REJECT).** Adopt-not-defend (pre-committed). Build NOT done.

## Proposal (hypothesis)

Lightweight custom MCP server "llm-fleet": stdio, ~100 lines, reads `keys.env`, exposes one
tool `llm_call(provider, model, prompt, [max_tokens])` over OpenAI-compatible endpoints
(Groq/Cerebras/OpenAI/HF/GitHub Models) + Gemini, to make cloud keys first-class tools.
Confirmed by Eduardo as a doctrine component "gated SDMG" (i.e. could be rejected by gate).

## Executed experiments

1. **Call-path smoke (PASS):** direct Groq REST (`/openai/v1/chat/completions`,
   `llama-3.3-70b-versatile`, GROQ_API_KEY) returned `FLEET_OK`. Proves the multi-provider
   call path already works via plain REST/Bash -- no MCP needed to reach the keys.
2. **External falsification (different-model judge, harsh-reviewer subagent):** ground-truth
   verified (wrappers exist, keys.env present, OD-009 shipped yesterday, ADR-0036 anti-scope
   written yesterday). Verdict **NO-GO**, fails 5/5 axes.

## harsh-reviewer findings (NO-GO)

- **No caller (blocking):** every routing-tree cell is better served by another spoke --
  sovereign/cheap -> local Ollama; cloud-OK edit -> aider-* (a raw completion blob cannot
  edit a file); async -> Jules; strategic/synthesis -> inline-Opus, which is MORE capable
  than every model `llm_call` would reach (Opus calling Groq-70b = capability downgrade +
  latency tax). The residual intersection is near-empty and already served by
  `aider-groq-bypass` / curl. Gold-plating.
- **LiteLLM-redux (blocking):** multi-provider key-fanout + endpoint normalization IS the
  overhead category decommissioned 24h ago (OD-009); contradicts ADR-0036 sec 8 anti-scope.
- **Net failure surface (significant):** new always-on stdio process + a 7th invocation
  path (which is canonical? drift) + MCP schema coupling, for ~zero functional gain over
  the proven REST/wrapper path. Anti-pattern #11 (helper adds more failure surface than the
  task).
- **Drift owner = solo, forever (significant):** 6 endpoints' model names/APIs drift (we
  already have dead refs: gemini-2.0-flash-exp 404, Cerebras-70b paid-only, aider-groq
  removed); a registered native tool that breaks is worse than a wrapper that simply is not
  invoked.
- **Secret-residency regression (minor):** a long-lived MCP holds all 10 keys resident the
  whole session vs current per-invocation sourcing (aider-groq-bypass deliberately keeps
  keys out of argv, CWE-214). Broader/longer-lived surface for zero gain.

## Decision

**NO-GO.** Do not build. The cloud keys' value is realized through the EDIT wrappers
(aider-*), Jules (async), and local Ollama -- not a raw-completion tool, because the hub
(Opus 4.8) is more capable than the callable cloud models. The discoverability concern
("keys not visible as tools") is addressed by ORCHESTRATION.md sec 7 (invocation table +
adoption rule), NOT by a tool with an empty caller-set.

**Re-open only at n>=2 concrete logged call-sites** where a wrapper/REST genuinely blocked
a needed raw cloud completion -- and then the narrowest form is a curl snippet in a runbook,
not a process.

## CORRECTION (2026-05-29, Eduardo reframe -- human overrule of an over-narrow gate)

The eval above evaluated ONE framing: a general completion-routing MCP (`llm_call` to
weaker cloud models for normal tasks). That framing is correctly **REJECTED** -- it stands.
But Eduardo clarified the actual intent: the cloud keys are used **WITH** Opus, not as
competitors -- for cross-check / diverse-POV inside multi-agent steps, deferrable sub-tasks,
and **services Opus lacks**. This defeats the harsh-reviewer's "no caller" axis for a
DIFFERENT, scoped design:

- **Services (no hub equivalent):** Tavily web search; OpenAI image generation. The
  "hub is more capable" argument does not apply -- Opus cannot generate images or run
  Tavily. Clear callers.
- **Non-Claude cross-check judge:** Gemini/Groq as a DIFFERENT-model-family verifier for
  high-stakes. This is the doctrine's own anti-monoculture mandate -- and note the
  harsh-reviewer is itself a Claude subagent (same family = partial monoculture), which is
  exactly why it under-weighted the diverse-POV value. A non-Claude second opinion is
  strictly better for catching shared blind spots.

**Corrected verdict:** general completion-routing MCP = **REJECT** (gold-plating, stands).
A **scoped fleet-tools MCP = GO** -- `tavily_search` + `openai_image` + `cross_check(model,
prompt)`, keys.env, used inside multi-agent steps. NOT cost-routing, NOT LiteLLM-redux. The
build goes through its own SDMG-minimal spec/plan (where the scoped design is itself
falsified before code). Lesson: an automated gate run by a same-family judge can be
over-aggressive on diversity value; the human decider is the correct overrule for that
exact blind spot.

## Methodology note

This is the SDMG gate working as designed: self-designed tool = hypothesis -> executed
experiment (smoke) + external falsification (different-model judge) -> REJECT -> adopt, not
defend. Negative finding = positive methodology value (a gold-plated always-on process
avoided the day after deciding to build it). 4th logged SDMG invocation; adoption rate and
the ADOPT-without-experiment health signal stay green.
