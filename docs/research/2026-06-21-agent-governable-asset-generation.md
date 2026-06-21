---
title: Agent-governable asset generation (ComfyUI vs manual ChatGPT-Pro)
date: 2026-06-21
status: research (A5 -- informs, does not govern)
author: claude-opus-4.8 (owner-requested tech-scout, Lenovo)
method: /last30days engine (Reddit/HN/GitHub) + targeted WebSearch + GitHub repo recon
layer: A5
related:
  - Game-Godot-v2 docs/research/2026-06-03-asset-generation-pipeline.md (prior, image-method scout)
  - Game-Godot-v2 docs/superpowers/specs/2026-06-21-shared-llm-routing-contract-resolution.md (the local LLM router seam)
  - Game-Godot-v2 docs/superpowers/specs/2026-06-21-evo-content-mcp-creature-lore-design.md (lore content-gen, parallel build)
  - raw dump: ~/Documents/Last30Days/agent-governable-automated-game-asset-generation-comfyui-mcp-local-diffusion-raw-v3.md
---

# Agent-governable asset generation -- research (2026-06-21)

## TL;DR / verdict

The de-facto "manual ChatGPT-Pro image step" is the OUTLIER, not the standard. The
validated 2026 path for asset generation an AI agent can drive end-to-end, zero-cost,
locally, is **ComfyUI** (graph engine) controlled via its `/prompt` REST API or an MCP
server. It is programmable, local, free, deterministic (seed/sampler/CFG/model-locked),
and its workflows are JSON committable to git -- the workflow-as-code + manifest discipline
our own content-gen standard already prescribes. A manual browser step is the un-governable
bottleneck; this replaces it.

## The question

Owner challenge (2026-06-21): for a content-gen INFRA, why default to manual ChatGPT-Pro
when automatic, non-manual, agent/LLM-governable means surely exist? Is there validated
prior art? Answer: yes, abundantly, and it is the indie 2026 default.

## Findings (validated, GitHub + community, last-30-days)

### ComfyUI is the agent-governable substrate
- `comfyanonymous/ComfyUI` -- 118K stars; "most powerful and modular diffusion GUI, API
  and backend". Local + free.
- The `/prompt` endpoint IS the seam: the canvas serializes the graph to JSON and POSTs it;
  ANY HTTP client can submit it. "Anything you can build visually, you can submit
  programmatically." (Runflow ComfyUI API guide; 9elements.)
- Reproducibility = lock seed, size, sampler, steps, CFG, model version, LoRA weights,
  post-processing. A workflow is git-versionable code: dev -> staging -> prod.

### Agent-driven, unattended, is demonstrated (not hypothetical)
- Livestream demo (per Runflow): Claude Code controlling a local ComfyUI over REST --
  queuing prompts, downloading missing LoRAs, batch generations, self-diagnosing a broken
  node with NO human in the loop. Queue 1000 variations overnight.

### Validated game-asset repos (agent-first)
- `mor-o/comfyui-2d-character-pipeline` (33 stars, Python, updated 2026-06-21) -- single
  character image -> layered, separately-tintable 2D sprite sheets; "harness-driven,
  designed to be run fully automatically by an AI agent such as Claude Code or Cursor";
  workflows shipped in `/prompt` API format. THE reference for our exact need.
- `mattwilliamson/comfyui-ai-gamedev` -- Hunyuan3D 2.1 image->3D asset nodes + an Ollama
  prompt-extender node (a LOCAL LLM inside the graph -- the router shows up here too).

### MCP-native seams (6+ servers; one is a Claude Code plugin)
- `artokun/comfyui-mcp` (167 stars, TypeScript) -- Claude Code plugin + MCP server, 88
  tools, 14 AI skills (Flux/WAN/LTX/Qwen), live graph editing from a Claude session.
- `shawnrushefsky/comfyui-mcp`, `joenorton/comfyui-mcp-server`, `alecc08/comfyui-mcp`,
  `IO-AtelierTech/comfyui-mcp`, `ericwanghp/ComfyUI_MCP` -- bridges natural language ->
  workflow params over the REST API.
- `ComfyGPT` + `AIDC-AI/ComfyUI-Copilot` -- self-optimizing multi-agent systems that AUTHOR
  the workflow itself from a task description.
- `SaladTechnologies/comfyui-api` -- horizontal scale; sync or async outputs (overnight batch).

### Provenance is now a legal deadline
- C2PA content-credentials = tamper-evident signed manifest recording AI-gen status +
  generation metadata (TianPan, Numonic, eyesift). A programmatic pipeline can stamp C2PA
  per asset; a manual export cannot cleanly.
- EU AI Act Article 50 (effective 2026-08-02) REQUIRES machine-readable provenance manifests
  for AI content -- "metadata-first" / provenance as a first-class pipeline concern.

## Recommendation (for the asset-content-gen spec)

Agent -> ComfyUI local (`/prompt` API or `artokun/comfyui-mcp`) -> deterministic images +
C2PA provenance per asset, with the SHARED local LLM router (`pick()`) composing the
design-grounded prompts. End-to-end agent-governed, zero-cost (runs on the fleet: Ryzen
RTX 4070S 12GB / Lenovo RTX 5060 8GB), workflows-as-code, manifest/queue -> validate ->
gated-promote. This is NOT "ChatGPT-Pro + prompt"; it is a ComfyUI agent pipeline.

## Caveat (load-bearing, consistent with 2026-06-03 research)

Raw diffusion output does NOT hold cross-evolution creature identity alone -- needs
ControlNet silhouette-lock and, for a stable roster across stages, the 3D-to-pixel path
(Blender ortho / Hunyuan3D). The human-authorship cleanup layer remains (zero-cost/legal
policy) but becomes a REVIEW-GATE over generated output, not manual generation.

## Reuse / recall

- Raw evidence: the last30days file in `related` above.
- This supersedes the implicit "manual ChatGPT-Pro is the path" assumption in
  `FERROSPORA_IMAGE_PIPELINE_DECISION_GUIDE.md` -- flag for that doc's owner.
- Next step (owner-chosen): evidence-first SPIKE of `mor-o/comfyui-2d-character-pipeline`
  on the fleet to validate the Ferrospora creature look before writing the spec.
