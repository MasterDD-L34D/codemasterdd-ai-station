---
title: Handoff -- content-gen infra + asset-pipeline spike
date: 2026-06-21
doc_status: active
workstream: cross-cutting (Game-Godot-v2 + codemasterdd hub + evo-content-mcp)
language: it
source_of_truth: false
---

# Handoff -- content-gen infra + asset-pipeline -- 2026-06-21

## TL;DR

- Ferrospora UI arc CHIUSO: 8 PR su main (Game-Godot-v2). Vedi tabella.
- Content-gen "router/genfleet" mio = **KILLED** dal gate SDMG (harsh-reviewer):
  shadow-duplicate della spec **evo-content-mcp gia approvata** (parallel chip). Niente
  router duplicato; il chip possiede router + lore.
- Coordinamento col chip = **file-based, durevole** (sopravvive al reset): vedi "Coord".
- Ricerca asset-gen salvata + recallable (hub KNOWLEDGE_MAP A5). Scelto path asset =
  **opzione 2 (SDXL+LoRA static via ComfyUI /prompt)**; opzione 1 (mor-o animati) =
  reminder feasible-ma-lento.
- **NEXT #1 = lo SPIKE opzione-2** (recipe sotto, cold-runnable). Owner ha gia
  autorizzato la variante localhost.

## PR mergiati (Game-Godot-v2, questa sessione)

| PR | Scope | Note |
| --- | --- | --- |
| #517 | ActionDock curated frame + measure-place + responsive | dock alignment FIX |
| #519 | DOCK-ALIGNMENT-SOLUTION.md + tool measure_socket_centers / cut_flat_bg | |
| #520 | ForecastPanel visual-first (valori grandi + gauge + pip) | |
| #521 | .uid sidecar drift (chip) | |
| #522 | UnitInfoPanel visual-first (gauge HP/CT + pip) | |
| #523 | BattleFeed righe ring-per-evento | |
| #525 | BoardOverlay outline cavi (readable over terrain) | |
| #526 | spore/ritual overlay + CATEGORY-COLORS.md (canon spore=viola/ritual=verde) | |

## Coord chip evo-content-mcp (DUREVOLE -- leggi questi, non serve il contesto)

- Shared routing contract: Game-Godot-v2 `docs/superpowers/specs/2026-06-21-shared-llm-routing-contract.md` (branch docs/evo-content-mcp-creature-lore-spec).
- Mia risoluzione: Game-Godot-v2 `docs/.../2026-06-21-shared-llm-routing-contract-resolution.md` (branch `docs/coord-routing-resolution-asset-gen`, commit b9c0260).
- Spec canonica content-gen: Game-Godot-v2 `docs/.../2026-06-21-evo-content-mcp-creature-lore-design.md` (approved, commit 6ad2682). Possiede MCP + lore + `pick()` router.
- Contratto chiave: UN solo `pick(task_class)->(host,ollama_tag)`, pubblicato da evo-content-mcp; io consumo. Source = `LOCAL-LLM-STANDARD.md` matrix + `/api/tags` preflight (NON le JSON llmfit = HF-ids). Le mie asset task_class = nessuna attiva ora (`prompt_compose`/`manifest_*` riservate).
- Mia spec genfleet superseded: hub branch `claude/content-gen-fleet-sharding-spec` (record del KILL, non buildare).

## Ricerca salvata (recallable hub)

- `docs/research/2026-06-21-agent-governable-asset-generation.md` (branch `claude/research-agent-asset-gen`, commit e4d251f) -- ComfyUI /prompt + MCP + repo validati + C2PA/EU-AI-Act + **specs fleet verificate + feasibility opzione-1**. Registrato in `docs/KNOWLEDGE_MAP.md` A5.
- Raw: `~/Documents/Last30Days/agent-governable-automated-game-asset-generation-comfyui-mcp-local-diffusion-raw-v3.md`.

## NEXT ENTRY POINT #1 -- SPIKE opzione-2 (cold-runnable)

Obiettivo: provare il seam agent-governable ComfyUI `/prompt` + Ferrospora-LoRA su Ryzen, 1 ritratto creatura statico. Owner: variante **localhost** (no `--listen`), driver gira su Ryzen.

Pezzi verificati su Ryzen (.11, DESKTOP-T77TMKT, SSH Vgit@192.168.1.11):
- ComfyUI portable: `C:\AI\ferrospora-spike\ComfyUI_windows_portable` (down ora).
- Checkpoint: `...\ComfyUI\models\checkpoints\sd_xl_base_1.0.safetensors` (6.5GB) PRESENT.
- LoRA: `C:\AI\ferrospora-lora-dataset\ferrospora_style_v1_ADOPTED.safetensors` (va copiata in `...\ComfyUI\models\loras\`).

Recipe (cross-PC mutation = gated; owner ha autorizzato la variante localhost):
1. SSH Ryzen: `Copy-Item` LoRA -> `ComfyUI\models\loras\`.
2. SSH Ryzen: lancia ComfyUI detached **localhost only** -- `python_embeded\python.exe -s ComfyUI\main.py --port 8188` (WorkingDirectory il portable, WindowStyle Hidden, redirect log a `C:\AI\comfyui-spike.log`).
3. Poll Ryzen `127.0.0.1:8188/api/tags` (o /system_stats) finche up (~30-90s model scan).
4. Workflow API-JSON minimale (SOLO nodi core): CheckpointLoaderSimple(sd_xl_base_1.0) -> LoraLoader(ferrospora_style_v1_ADOPTED, strength ~0.8) -> 2x CLIPTextEncode (pos = prompt creatura Ferrospora teal/spore; neg) -> EmptyLatentImage(1024x1024) -> KSampler(euler_a, ~28 steps, cfg 7) -> VAEDecode -> SaveImage. Pattern driver = mor-o (`C:\dev\_spike-comfyui\drivers\*` clonato; urllib POST /prompt, poll /history).
5. Pull l'immagine da Ryzen `...\ComfyUI\output\` a Lenovo, valuta look Ferrospora.
6. Cleanup: kill ComfyUI Ryzen a fine spike.
Caveat: raw diffusion non tiene coerenza cross-evoluzione da solo -> per roster servira ControlNet silhouette-lock (futuro). Lo spike valida solo il SEAM + lo stile, non la coerenza.

## Cleanup pendente (worktrees / cloni)

- Hub worktree `C:/dev/_wt-hub-research` (branch claude/research-agent-asset-gen) -- rimuovi a fine (branch su remote = record).
- Hub branch record: `claude/content-gen-fleet-sharding-spec` (superseded), `claude/research-agent-asset-gen` (research+reminder).
- Game branch record: `docs/coord-routing-resolution-asset-gen` (b9c0260).
- Clone spike: `C:/dev/_spike-comfyui` (mor-o repo, per il driver-pattern).
- NOTA: il game shared tree `C:/dev/Game-Godot-v2` e sul branch del PARALLEL session (`docs/evo-content-mcp-creature-lore-spec`) -- NON toccare il suo HEAD.

## Memory candidates (chiedi conferma prima di salvare)

- feedback: "before designing infra, check existing hub specs (agent-scanner) -- genfleet KILL was a shadow-duplicate the SDMG harsh-reviewer caught; the spec was the session-start branch".
- project: "asset-gen path = ComfyUI /prompt + Ferrospora-LoRA (opt-2 static); mor-o animated (opt-1) deferred-feasible; fleet 8GB/63GB Lenovo + 12GB/31GB Ryzen, pipeline-split".
- reference: "Ryzen ComfyUI spike install paths + sd_xl_base + LoRA locations (recipe above)".
