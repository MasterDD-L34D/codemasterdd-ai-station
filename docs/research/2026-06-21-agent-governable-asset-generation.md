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

## Fleet feasibility (verified 2026-06-21) + deferred animated-sprite option (REMINDER)

Verified GPU/RAM: **Lenovo (.10)** RTX 5060 **8GB VRAM + 63.4GB RAM** (RAM-rich);
**Ryzen (.11)** RTX 4070 SUPER **12GB VRAM + 31GB RAM** (VRAM-rich). Opposite profiles
-> pipeline-split (VRAM-dense stage -> Ryzen; offload-heavy stage -> Lenovo's 63GB RAM).

**CHOSEN NOW (option 2 -- light / static):** SDXL + the trained Ferrospora style-LoRA,
driven via ComfyUI `/prompt`, for STATIC creature portraits / UI assets. Fits 12GB
easily; ComfyUI + `ferrospora_style_v1_ADOPTED.safetensors` already present on Ryzen
(`C:\AI\ferrospora-spike\ComfyUI_windows_portable`). **This spike was EXECUTED 2026-06-21
-- see `## SPIKE EXECUTED -- 2026-06-21 (result)` below.**

**REMINDER -- option 1 (mor-o animated-sprite pipeline) IS feasible on this fleet** when
layered animated sprites are actually needed. An earlier "infeasible" call was WRONG: 24GB
is the COMFORTABLE tune, not a floor. The repo is built to run on less:
- two-stage VRAM-eviction (`VRAMUnloadModel` -- the WAN MoE experts never coexist) ->
  real per-stage peak ~10-16GB, not 25GB;
- documented down-path = Q4_K_M GGUF (~15% smaller); do NOT go below Q4 (quality cliff);
- ComfyUI offloads the text encoders to RAM (Ryzen 31GB / Lenovo 63GB).
So W2 (video stage) runs on Ryzen 12GB (single 14B Q4 ~8.5GB + offload), tight/slow; W1
pose-edit (~19GB, the heaviest) runs via aggressive eviction OR Lenovo's 63GB RAM offload.
Real costs = **~80GB model download + slow gen (offload)**, NOT impossibility. Revisit
when the game needs ANIMATED creature sprites; for static portraits it is overkill.

## Reuse / recall

- Raw evidence: the last30days file in `related` above.
- This supersedes the implicit "manual ChatGPT-Pro is the path" assumption in
  `FERROSPORA_IMAGE_PIPELINE_DECISION_GUIDE.md` -- flag for that doc's owner.
- SPIKE DONE 2026-06-21 -- opt-2 seam validated (see `## SPIKE EXECUTED -- 2026-06-21`
  below). Next: write the asset-content-gen spec.

## SPIKE EXECUTED -- 2026-06-21 (result)

**Verdict: SEAM VALIDATED.** Agent-governable ComfyUI `/prompt` API + Ferrospora style-LoRA
on Ryzen RTX 4070S, end-to-end, zero manual ChatGPT-Pro step.

- **Seam**: ComfyUI launched localhost-only on Ryzen (`--port 8188`, no `--listen`); a stdlib
  urllib driver POSTs the API-JSON workflow to `/prompt`, polls `/history`; the output image is
  pulled to Lenovo. Graph = CheckpointLoaderSimple(sd_xl_base_1.0) -> LoraLoader(
  ferrospora_style_v1_ADOPTED @ 0.75) -> 2x CLIPTextEncode -> EmptyLatentImage(1024x1024) ->
  KSampler(euler_a, 28 steps, cfg 7) -> VAEDecode -> SaveImage.
- **Throughput**: ~18s/img on the 4070S.
- **Output**: 1 static creature portrait, end-to-end (artifact: Lenovo
  `C:/dev/_ferro_scratch/ferrospora_spike_00001.png`; driver `C:/dev/_ferro_scratch/ferrospora_driver.py`).
- **KEY finding**: the v1 LoRA is **UI-frame-domain** (trigger `ferrospora ui`, trained on 36 UI
  frames), so creature generation is working **style-bleed**, NOT in-domain fidelity. The Ferrospora
  signature (teal spore-glow gemstones + bronze chitin) transfers recognizably onto a creature, and
  anti-frame negatives beat the 100%-frame training set. For production creature assets: a dedicated
  creature-LoRA gives in-domain fidelity; ControlNet silhouette-lock gives cross-evolution roster
  coherence (consistent with the Caveat above). This spike validates the SEAM + style transfer ONLY.
- **Cleanup**: ComfyUI killed on Ryzen (port 8188 down, verified); Ryzen clean. Driver + ADOPTED LoRA
  kept staged under `C:/AI/` for future runs.
- **Memory**: Game-Godot-v2 auto-memory `ferrospora-asset-gen-seam-validated` (links `ferrospora-lora-v1-trained`).
