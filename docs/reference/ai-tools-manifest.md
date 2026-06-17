# AI Tools & Models Manifest -- CodeMasterDD AI Station

<!-- Vista unica "quale AI, quale licenza, per cosa" del fleet. Consolida info
     sparse in stack-installed.md + MODEL_ROUTING.md + hardware-and-models.md + ADR.
     On-demand reference. ASCII-first (ADR-0021). Creato 2026-06-17 (gap-audit G1,
     report AI-gamedev-standards; sweep multi-source 6-reader). Scope: HUB + POINTER
     (dettaglio dev-tool hub + pointer ai provenance per-repo gia' esistenti).
     NON e' un consumer AI-STANDARDS.md (no bias/watermark: il fleet non shippa
     contenuto creativo generato -- vedi sez. 7). -->

## 0. Scope

DEV-TIME, hub-centric. Elenca gli strumenti/modelli AI usati per SVILUPPARE il
software del fleet. Il dettaglio esaustivo per-repo (vault eng-graph, Game asset,
Dafne swarm) resta nei provenance doc nativi -- qui solo pointer (sez. 8).

NON descrive AI dentro i giochi prodotti: ASSENTE by design (sez. 7).

Authority decisioni: ADR-0001 (sovereign), ADR-0013 (cloud-free), ADR-0023 (API
cap), ADR-0029 (BYOK / no-OpenRouter-primary), ADR-0030 (Hybrid A1), ADR-0036
(orchestration + fleet-tools). Ruoli operativi: `MODEL_ROUTING.md` + `ORCHESTRATION.md`.
Versioni live: `docs/reference/stack-installed.md`. Modelli locali: `hardware-and-models.md`.

## 1. Coding assistants (dev-time)

| Tool | Licenza | Accesso | Ruolo |
|------|---------|---------|-------|
| Claude Code (Opus) | Proprietary (Anthropic) | OAuth Max -> post-Max Pro/API | tier 0 strategic (multi-file, ADR, debug-arch) |
| Aider 0.86.2 | Apache-2.0 | local + 8 wrapper (sez. 3) | daily-driver edit 1-file (tier 1-2) |
| OpenCode (+opencode-with-claude v1.6.11) | MIT (wrapper: unknown) | npm global | multi-step agentic tool-use (ADR-0022) |
| Meridian (bridge OpenCode<->Pro) | unknown -- not stated | via opencode-with-claude | Pro bridge Hybrid A1 (ADR-0030) |
| Cline ext v3.79.0 | Apache-2.0 | VS Code | EVALUATED non-viable Qwen 7B (ADR-0006), dormant |

## 2. Modelli LLM locali (Ollama 0.30.8 -- runtime MIT)

Licenze verificate via `ollama show <model> --modelfile` 2026-06-17 dove possibile.

| Modello | Licenza | Macchina | Ruolo |
|---------|---------|----------|-------|
| qwen2.5-coder:7b | Apache-2.0 | Lenovo/Ryzen | cosmetic (114 tok/s) |
| qwen2.5-coder:14b-q2_K | Apache-2.0 | Lenovo (Ryzen q4) | behavior default |
| qwen2.5-coder:14b-q3_K_M | Apache-2.0 | Lenovo | reference (hallucination-prone) |
| qwen2.5-coder:32b | Apache-2.0 | Lenovo | reference dense (scartato, 3.65 tok/s) |
| qwen3-coder:30b MoE | Apache-2.0 | Lenovo (RAM-rich) | escalation + OpenCode default |
| deepseek-r1:8b | MIT | Lenovo (full-VRAM) | reasoning/debug |
| deepseek-r1:14b | MIT | Lenovo | reasoning scale-up |
| deepseek-coder-v2:16b MoE | DeepSeek License (commercial OK) | **Ryzen-only** | speed-first non-constraint (non su Lenovo) |
| gemma4:latest (8B) | Apache-2.0 (modelfile-embedded) | Lenovo | multimodal (OCR/audio/vision) |
| mistral:latest | Apache-2.0 | Lenovo | small-instruct sovereign |
| phi4:14b | MIT | Lenovo | esplorazione |
| qwen3:8b | Apache-2.0 | Lenovo/Ryzen | Dafne+vault query/fallback |
| qwen3.5 / qwen3.6 | Apache-2.0 | Lenovo | esplorazione |
| qwen2.5:32b-instruct | Apache-2.0 | Lenovo | non-coder reference |
| gpt-oss:120b | Apache-2.0 | reference-only (OOM 63GB) | future RAM upgrade |
| nomic-embed-text | Apache-2.0 | entrambe | embedding (Dafne H5 gate) |
| snowflake-arctic-embed2:568m | unknown -- not stated | Ryzen | embedding vault eng-graph (1024d) |

## 3. Provider cloud (BYOK -- keys in `~/.config/api-keys/keys.env`, ACL-locked, mai in repo)

9 provider. Wrapper aider in `scripts/wrappers/` (repo-tracked) + `~/.local/bin/`.
Ogni wrapper applica privacy guard-rail H8 (whitelist check) + key-handling hardened
(temp env-file, non argv; CWE-214). Platform = proprietary; sotto la licenza-MODELLO servito.

| Provider | Wrapper | Modello servito (licenza) | Tier | Note |
|----------|---------|----|------|------|
| Groq | aider-groq-bypass | llama-3.3-70b (Llama 3.3 Community) | free 6k tok/min | LPU speed |
| Cerebras | aider-cerebras | llama-3.1-8b (Llama 3.1 Community) | free 8k ctx | cosmetic fast |
| Gemini API | aider-gemini | gemini-2.5-flash | free-key 60 req/min | OAuth-free RITIRATO 2026-06-18 |
| OpenAI API | aider-openai | gpt-4o-mini, gpt-image-1 | paid | ccusage monitor; image via fleet-tools |
| Anthropic API | -- (Claude Code) | Claude (Opus/Sonnet/Haiku) | paid | cap $10-20/mo (ADR-0023) |
| GitHub Models | aider-github-models | gpt-4o (+ mini/Llama-3.3-70B/Mistral-Large/Phi-3.5) | free 150 req/day | endpoint Azure, fine-grained PAT |
| HuggingFace Inference | aider-hf | DeepSeek-R1:fastest (+ gpt-oss-120b/Qwen2.5-Coder-32B) | free | router OpenAI-compat, :fastest/:cheapest |
| Tavily | -- (fleet-tools MCP) | web search (no LLM) | free | sez. 4 |
| OpenRouter | -- (optional) | 290+ modelli | pending/emergency | DECLINED-primary (ADR-0029), 0% markup BYOK |

## 4. fleet-tools MCP (codemasterdd `apps/fleet-tools-mcp/`)

Server MCP scoped (stdio, registrato in `.mcp.json`), ratificato ADR-0036 Decision 5
(SDMG gate: general llm_call REJECTED gold-plating; scoped fleet-tools ACCEPTED).
Dipende da `@modelcontextprotocol/sdk` v1.12.0. Keys lette per-call, mai resident-session.

| Tool | Servizio | Uso |
|------|----------|-----|
| tavily_search | Tavily API | web search + answer-extraction (multi-agent) |
| openai_image | OpenAI gpt-image-1 | image gen (quality=medium hardcoded, ~$0.04-0.07/img) |
| cross_check | non-Claude model | diverse-POV verification (anti-monoculture) |

## 5. AI tooling / plugin (dev-time)

**Tool standalone:**

| Tool | Licenza | Ruolo |
|------|---------|-------|
| promptfoo | MIT | quality-bench HumanEval-style (QG Step-1) |
| faster-whisper / CTranslate2 | MIT | transcription audio sovereign (GPU CUDA, large-v3) |
| repomix v1.14.0 | MIT | repo-pack AI-ingestible per handoff |
| notebooklm-py 0.4.1 / -mcp-cli 0.6.9 | MIT (wrapper non-uff., ToS gray) | NotebookLM programmatic (auth pending) |
| Gemini CLI v0.42.0 | Proprietary (Google) | cloud-free query (path API-key; OAuth retire 2026-06-18), **dormant** |
| Bun v1.3.13 | MIT | runtime JS (pre-req claude-mem) |
| Playwright v1.59.0 | Apache-2.0 | browser automation (NotebookLM OAuth + bench regression) |

**Claude Code plugins** (`~/.claude/`, stato da `settings.json` 2026-06-17):

| Plugin | Licenza | Stato |
|--------|---------|-------|
| superpowers v5.1.0 (15 skill) | MIT | ACTIVE |
| caveman | MIT | ACTIVE |
| compass v0.4.3 (own, MasterDD-L34D) | MIT | ACTIVE |
| last30days v3.3.2 | MIT | ACTIVE |
| continuous-learning-v2 | vendored anthropic-skills | ACTIVE (hook observe.sh) |
| agent-scanner (own) | -- internal | ACTIVE (anti-shadow-duplicate) |
| claude-mem v13.2.0 | Apache-2.0 | **DORMANT** (settings `=false`) |
| tdd-guard v1.3.0 | MIT | **DORMANT** (settings `=false`) |

**MCP server connessi** (env Claude Code): NotebookLM, fleet-tools (sez. 4),
computer-use, Claude-in-Chrome, visualize, mcp-registry. Anthropic Agent Skills
marketplace = 18 skill (xlsx/docx/pptx/pdf doc-processing + canvas-design/algorithmic-art/
brand-guidelines/mcp-builder/skill-creator/theme-factory + claude-api). Dettaglio
non duplicato qui (env-managed, non repo-config).

## 6. Frameworks AI esterni (orchestration)

| Tool | Licenza | Dove | Ruolo |
|------|---------|------|-------|
| ARCHON v2.0.2 | MIT (`~/aa01/LICENSE`) | AA01 studio | 7-step protocol high-stakes (ADR-0026) |
| A00 v2 | unknown -- not stated | AA01 monitor | audit direzionale autonomo |

## 7. Runtime AI in-game -- ASSENTE BY DESIGN

I giochi del fleet (Evo-Tactics: Game backend + Game-Godot-v2 frontend) **non
contengono reti neurali ne' LLM nel build runtime**. L'AI nemica e' un policy engine
deterministico/euristico (`utilityBrain.js`, Beehave behavior trees, GdPlanningAI GOAP)
-- requisito hard per la riproducibilita' del balance-gate batch-sim (win-rate
convergente su N-ladder richiede determinismo). Nessun ONNX/TensorRT bundled, nessun
DLSS/FSR/XeSS (turn-based 2D, no rendering realtime-3D pressure). Gli LLM di questo
manifest sono TUTTI dev-time.

## 8. AI stack per-repo (POINTER -- provenance nativi)

Dettaglio esaustivo nei doc del repo proprietario; qui solo sintesi + path.

### Game (`C:/dev/Game`) -- AI dev-time LIVE
- **LLM-as-critic balance loop**: `tools/py/llm_critic_loop.py` -> Anthropic
  **claude-haiku-4-5** (3-iter, user-gated, graceful-degrade se SDK assente).
- **ChatGPT sync**: `scripts/chatgpt_sync.py` -> OpenAI **gpt-4o-mini/gpt-4o**
  (cron 05:30 UTC, `.github/workflows/chatgpt_sync.yml`).
- **AI-driven batch-sim** (no-LLM, deterministico): policy engine, vedi
  `docs/process/CANONICAL-AI-PLAYTEST.md`.
- **Asset** (provenance: `CREDITS.md` + `docs/core/43-ASSET-SOURCING.md`):
  Retro Diffusion (active, Premium indemnified) + SDXL+LoRA / Adobe Firefly /
  Flux Pro (dormant) + Libresprite/ImageMagick/upscayl (post-process).
- SDK: anthropic-sdk-python (MIT), openai-python (MIT).

### Game-Godot-v2 (`C:/dev/Game-Godot-v2`) -- pipeline asset assistita
- Provenance: `docs/godot-v2/artstyle/ferrospora/asset_generation_manifest.json`
  + `FERROSPORA_IMAGE_PIPELINE_DECISION_GUIDE.md`.
- ChatGPT Pro (active, image gen manuale) + Codex (orchestration) + Blender 3D
  (active, mesh->pixel deterministico, `tools/art_pipeline/blender3d/`).
- GdPlanningAI (Apache-2.0, GOAP in-engine, NO-LLM). Dormant local-optional:
  ComfyUI (GPL-3.0), Automatic1111 (AGPL-3.0), Open WebUI (MIT). AsepriteWizard (MIT).

### vault (`C:/dev/vault`) -- eng-graph KG stack (sovereign)
- Provenance: `docs/reference/stack-tecnico.md` + `ai-routing-matrix.md` + OD-059.
- Cognee (KG engine) + Kuzu (graph db) + LanceDB/Qdrant (vector) + Arctic-Embed2:568m.
- Query LLM sovereign qwen3:8b; **cognify EXTRACTION cloud-gated** OpenAI gpt-4o-mini
  (data-egress ACCEPTED OD-059). Mistral (bulk summary).
- Ingest: MinerU 3.1.4 + pypdf + pdftotext (Poppler GPL). Cluster: BERTopic + UMAP +
  HDBSCAN. ML libs: transformers (Apache-2.0) + sentence-transformers + torch (BSD).
- Obsidian plugins: Smart-Connections (bge-micro-v2 transformers.js), Copilot,
  Claude-Code-MCP. MCP: FastMCP (eng-graph query daemon).

### Dafne swarm (`~/Dafne/workspace/swarm`) -- orchestratore AI
- nomic-embed-text (H5 semantic-dup gate, 0.75 cosine + Jaccard fallback).
- Fallback chain: Groq -> Cerebras (llama-3.1-8b) -> Gemini (2.0-flash-exp) -> Ollama.
- Stack: Flask + flask-cors + requests + pyyaml.

## 9. Note governance

1. **Game fa chiamate cloud AI live** (claude-haiku via llm_critic_loop, openai via
   chatgpt_sync): rilevante privacy + cost. Entrambe dev-time, BYOK, non runtime-gioco,
   user-gated/cron. Game e' cloud-whitelisted (privacy OK).
2. **Cloud-gated paths espliciti**: vault cognify EXTRACTION -> gpt-4o-mini (OD-059
   data-egress ACCEPTED, query-path resta sovereign). Pattern corretto: gate esplicito,
   non default-cloud.
3. **Privacy guard-rail**: tutti i wrapper cloud abortano se repo non in
   `~/.config/aider-privacy-whitelist.txt`. OpenRouter DECLINED-primary (ADR-0029,
   no model-origin transparency).
4. **Tool generativi VIETATI nel fleet** (provenance asset): Midjourney, DALL-E 3
   (per asset-art; gpt-image-1 OK solo per util dev via fleet-tools), PixelLab.ai.

## 10. Manutenzione + currency

Refresh quando si aggiunge/rimuove tool o modello:
- Versioni -> `stack-installed.md` (`<tool> --version`). Modelli -> `ollama list` + `hardware-and-models.md`.
- Stato plugin -> `~/.claude/settings.json` (campo `<plugin>@<marketplace>` true/false).
- Licenza nuovo OSS -> verifica empirica (gh API license field), pattern L-2026-05-007.
- Aggiorna questa tabella + entry REF-DOC-03 in `REFERENCE_INDEX.md`.

**Currency caveat noti (2026-06-17):**
- `stack-installed.md` riga 21 tratta claude-mem come installato/attivo: in realta'
  `settings.json` lo ha `=false` (DORMANT). Reconcile in stack-installed.md (RECONCILE-1).
- deepseek-coder-v2:16b: presente solo su Ryzen `.11` (licenza non verificabile da Lenovo).
- snowflake-arctic-embed2 / vari tool vault: licenza "unknown -- not stated" (sotto-prioritario,
  vault-scoped; verificare se eng-graph esce da sovereign-only).
