# Content-gen fleet-sharding -- design spec (scoped, SDMG-disciplined)

> Status: DRAFT v1 2026-06-21 -- NOT yet falsified. Author: Claude (Opus 4.8) on
> Lenovo (CodeMasterDD). Awaiting harsh-reviewer falsification (SDMG P7 step 3)
> before any build.
> Scope of THIS spec: a NARROW tool to generate bulk game CONTENT (creature
> lore/flavor, asset prompts) over the local Ollama fleet, sharded. NOT a general
> LLM router (SDMG-rejected, ADR-0036 Decision 5). NOT for code (existing tools).
> NOT a gateway (anti-#scope, OD-009).
> ASCII-first body (ADR-0021). Authority chain: ADR-0036 (why -- local fleet =
> spoke via Bash/REST) -> ORCHESTRATION.md (which-executor) -> CLAUDE.md (how).
> Referenced from `Game-Godot-v2` + `Game` via a pointer; canonical here (hub).

## 0. Naming honesty

This is NOT "genfleet the LLM router" (that framing was caught conflicting with the
ADR-0036 Decision-5 rejection of a general completion-routing MCP). What this spec
proposes is a **content-gen sharding driver**: a thin batch executor that fans
templated, design-grounded content prompts across the local Ollama fleet for ONE
narrow heavy use-case. The local fleet stays a spoke invoked via Ollama REST per the
doctrine; this adds no gateway, no autonomy, no cross-repo authority.

## 1. Problem

The game has a large COMBINATORIAL creature space (specie x parti x 16 Forme Base x
mating/Nido -- vault `core/20-SPECIE_E_PARTI` / `22-FORME_BASE_16` / `27-MATING_NIDO`).
Generating lore/flavor/trait-narrative for that space (and asset-prompt batches for the
art pipeline) per-item with the hub (Opus 4.8) is too expensive at scale: thousands of
combos. The local sovereign fleet (Ryzen 12 GB VRAM + Lenovo 63 GB RAM, both running
Ollama) is the right executor for cheap, parallel, private bulk generation -- it is
exactly the "local Ollama fleet" spoke in ADR-0036.

But there is NO content-gen tool over the fleet today. What exists is oriented to CODE
+ GOVERNANCE (see sec 2). So this is a genuine gap, with a real caller.

### 1.1 The real caller (anti "build ahead of need", SDMG step 5)

The caller is concrete, not hypothetical: the procedural creature-lore generator
(spawned as a dedicated chip session, goals A+B) needs to produce lore across the
combinatorial space; the art pipeline needs asset-prompt batches. Build order: the
caller's first content-type drives the first (and only, until evidence) generator.
If the caller does not materialize, this tool is not built (off-ramp).

## 2. Ground-truth (verified 2026-06-21, Lenovo .10) -- build-on, do not recreate

| Asset | Path | Reuse |
|-------|------|-------|
| llmfit HW-fit lists | `C:\Users\edusc\llmfit-lenovo-{chat,coding,general,reasoning}.json` + Ryzen list | shortlist (stage-1 HW) |
| local-fleet routing matrix | `tools/llmfit/LOCAL-LLM-STANDARD.md` (reframed local-fleet detail under ORCHESTRATION.md) | model+machine selection rules |
| Ollama REST | Lenovo `192.168.1.10:11434`, Ryzen `localhost`/`192.168.1.11:11434` | spoke invocation (doctrine) |
| shard pattern | Game `tools/py/calibrate_parallel.py` + the playtest shard-N runs | parallel fan-out, ~2x throughput |
| stage-2 task-eval harness | hub `scripts/llmfit-task-eval.py` | STRUCTURE only (it scores CODE via asserts; content needs a different scorer -- deferred) |
| existing fleet scripts | hub `scripts/fleet/*` (jules-dispatch, journal, sync) | NONE -- governance, not content-gen |
| cloud-services MCP | hub `apps/fleet-tools-mcp` (Tavily/OpenAI-image/cross-check) | NONE -- cloud, not local content-gen |

The genuinely-missing piece = a content-gen DRIVER. Everything else is reused.

## 3. Doctrine fit (why this is allowed, ADR-0036)

- **Not the rejected pattern.** Decision 5 rejected a general `llm_call` completion
  router to weaker CLOUD models ("no caller -- hub more capable; gateway-redux"). This
  is the OPPOSITE: LOCAL models, a SPECIFIC bulk caller the hub is too expensive for,
  no cloud, no gateway, no general `llm_call`.
- **Spoke invocation stays REST/Bash.** The driver calls Ollama REST directly (the
  doctrine's sanctioned spoke path). It does not interpose a routing service.
- **Anti-scope honored:** no LiteLLM/LangGraph/CrewAI; no autonomy ladder; no
  cross-repo authority; no auto-merge. It is a batch script, run by a human/agent.
- **MODEL_ROUTING.md governs the choice;** this tool just APPLIES it programmatically
  for the content task-class (general/chat clean-instruct -- NOT reasoning/think models,
  per the load-bearing S4 caveat).

## 4. Design

A single small Python package `content_gen_fleet/` (location sec 7). Modules, each
single-purpose + isolated + fixture-testable:

| Module | Does | Interface |
|--------|------|-----------|
| `fleet.py` | endpoint registry (Ryzen/Lenovo hosts+HW profile) + `health()` (probe `/api/tags`: up + installed models) | `health() -> {endpoint: {up, models[]}}` |
| `select.py` | apply MODEL_ROUTING + llmfit lists for the CONTENT task-class -> (machine, model). Clean-instruct only; never reasoning/think. | `pick(content_task, health) -> Target(endpoint, model)` |
| `generate.py` | one Ollama REST `/api/generate` call (timeout, retry, JSON-mode opt) | `gen(target, prompt, **opts) -> GenResult(text, model, latency)` |
| `shard.py` | fan a batch of independent items across HEALTHY endpoints, concurrent, model-affinity (pin model per host per run); resumable checkpoint (anti-#background-task) | `run_batch(items, build_prompt, content_task) -> [GenResult]` |
| `validate.py` | per-item output gate: schema/JSON shape + DESIGN-GROUNDING (required canonical fields present, no hallucinated species/parts) -> pass/fail + reason | `check(item, result, grounding) -> Verdict` |
| `cli.py` | `content-gen-fleet health` / `gen-batch <requests.jsonl> --task lore --out <dir>` | -- |

**Data flow (batch):** caller emits `requests.jsonl` (each = {id, template, grounding
context from canonical design data}) -> `shard.run_batch` (select per item with
affinity -> split across healthy endpoints -> concurrent gen -> checkpoint) ->
`validate.check` per item -> accepted items written to the dataset on `Game/`
(canonical); rejected items logged with reason for re-run. Provenance per item
(model, machine, latency, prompt-hash, timestamp) recorded.

**Grounding (the #1 multi-agent failure mode = vague prompts, ADR-0036):** prompts are
TEMPLATES filled from canonical design data (the species/parts/forme/lifecycle YAML on
`Game/`), not free-form. `validate.py` rejects outputs that drop required grounding or
invent non-canonical entities. This is the quality spine, not an afterthought.

## 5. Anti-scope (explicit)

- NO general LLM router / `llm_call` / gateway (ADR-0036 Decision 5, OD-009).
- NO code generation (existing: aider-* wrappers, llmfit-task-eval).
- NO cloud models (existing: fleet-tools-mcp).
- NO autonomy / auto-merge / cross-repo authority (governor spec owns that).
- NO heavy framework (LangGraph/CrewAI/LiteLLM).
- NO stage-2 task-eval scorer for content YET (sec 6 roadmap).

## 6. SDMG gate + phased rollout (no autonomy ahead of evidence)

- **Fase 0 (this spec):** falsifiable design. Gate: harsh-reviewer falsification
  (P7 step 3) + Eduardo approval. No code until SURVIVE verdict.
- **Fase 1 (MVP, narrow adoption):** build the driver for ONE content type only
  (the chip's first: creature lore for a SMALL fixed combo set, e.g. 1 specie x its
  parts), flag/opt-in, results land as a PR to `Game/` (human merges). Produces the
  honest evidence: does fleet content-gen meet the quality bar vs hub-per-item on a
  held-out sample? This Fase-1 sample IS the experiment.
- **Fase 2+ (roadmap, each its own gate):** generalize to the full combinatorial
  space; add a content task-eval scorer (stage-2 analog -- a different-model judge per
  ADR-0036 anti-monoculture, scoring grounding+quality, NOT code-asserts); wire the
  asset-prompt batches. Each earns its own evidence + gate; none ratified now.
- **Off-ramp:** if Fase-1 quality is below bar (local models can't hold the grounding),
  the tool is proven unnecessary -- fall back to hub-per-item for the high-value subset
  + cheaper local only for low-stakes flavor. The build stops; the spec records why.

## 7. Location + testing

- **Tool:** hub `scripts/content-gen/` (next to `scripts/fleet/` + `llmfit-task-eval.py`
  -- the fleet-tooling home). Cross-project; the `Game`/`Game-Godot-v2` repos get a
  one-line pointer doc, not a copy.
- **Spec (this file):** hub `docs/superpowers/specs/` (canonical). Referenced from the
  game repos.
- **Testing:** unit `select.py`/`validate.py`/`shard.py` with fixture llmfit JSON +
  mocked health + a fake gen fn (pure-logic, no network, CI). Integration gated `--live`
  (real Ollama on the fleet, skipped in CI). Quality gate (CLAUDE.md): smoke (gen-batch
  happy path, output verified + grounded) + research (>=3 edge: endpoint down,
  model-missing, structured-vs-reasoning routing, grounding-violation rejected, shard
  with 1 endpoint, resume-from-checkpoint) + Fase-1 held-out quality sample (N>=10,
  direction-probe; N>=40 to ratify, anti lucky-sample) before any generalization.

## 8. Open questions (for harsh-reviewer + Eduardo)

1. Is the Fase-1 caller (chip creature-lore) concrete enough NOW, or do we wait for the
   chip to define its first content-type before any build? (SDMG: prefer wait-for-caller.)
2. Content task-eval scorer (Fase-2): different-model judge (which? a non-local
   cross-check via fleet-tools-mcp `cross_check`?) vs rule-based grounding validators only.
3. Does the tool live on the hub `scripts/` or should the package be installable so the
   chip session + the art pipeline import it cleanly?
