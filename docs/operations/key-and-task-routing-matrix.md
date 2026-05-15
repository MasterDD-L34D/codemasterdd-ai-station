# Key Inventory + Task Routing Matrix

**Scope**: documento operativo unico per gestione API keys + dispatching task across tool ecosystem (REST + interactive web UIs + local sovereign).

**Aggiornato**: 2026-05-15 (post audit Eduardo "come gestiamo tutte le key e i compiti come li smistiamo").

**Authoritative source for**: routing decisions consolidata da CLAUDE.md + ADR-0013 + ADR-0022 + ADR-0023 + ADR-0030. In caso conflitto, questo doc + ADR successivi prevalgono.

---

## 1. Inventario API keys (`~/.config/api-keys/keys.env`)

ACL hardened: `CODEMASTERDD\edusc:(F) + NT AUTHORITY\SYSTEM:(F)`, inheritance disabled. Mai in repo, mai in registry, mai in commit.

| Key name | Provider | Tier | Costo | Tool consumer | Status |
|---|---|---|---|---|---|
| `GROQ_API_KEY` | Groq (LPU cloud) | 3 free | $0 (TPM 300K post-Tier1) | aider-groq-bypass, OpenCode `groq` provider | Attivo |
| `CEREBRAS_API_KEY` | Cerebras (WSE cloud) | 3 free | $0 (733 tok/s, ctx 8K cap) | aider-cerebras, OpenCode `cerebras` provider | Attivo |
| `GEMINI_API_KEY` | Google AI Studio | 3 free | $0 (60 req/min) | aider-gemini, Gemini CLI standalone, Aider LiteLLM | Attivo |
| `GOOGLE_GENERATIVE_AI_API_KEY` | Google AI Studio | 3 free | $0 | OpenCode native `google` provider (dual-name necessario) | Attivo (added 2026-05-15) |
| `OPENAI_API_KEY` | OpenAI | 4 paid | $5/mese cap consigliato | aider-openai, OpenCode `openai` provider | Attivo |
| `ANTHROPIC_API_KEY` | Anthropic | 0 strategic | $10-20/mese cap (ADR-0023) | Pay-per-use post-Max on-demand | Dormant durante Max |
| `TAVILY_API_KEY` | Tavily (search) | utility | $0 free tier | **Dafne swarm only** (Flask backend) | Isolato dal dispatcher codemasterdd |
| `HUGGINGFACE_API_KEY` | HuggingFace Inference Providers | 3 free | $0 (100K credit/mese) | `aider-hf` wrapper + OpenCode `huggingface` provider | **Setup pending Eduardo signup** (vedi sezione 6.4) |

**Gap fixati 2026-05-15**:
- ✅ Added `GOOGLE_GENERATIVE_AI_API_KEY` (dual-name OpenCode native google provider auth)
- ✅ Updated `opencode.json` google models: `gemini-2.0-flash-exp` (deprecato 404) → `gemini-2.5-flash` + `gemini-2.5-pro`
- ✅ Smoke test C OpenCode google provider: **PASS** (output "6" risposta a "3+3?")
- ✅ Added `huggingface` provider entry to `opencode.json` (baseURL router.huggingface.co, models DeepSeek-R1 + GPT-OSS 120B + Qwen Coder 32B) — env var pending
- ✅ Installed `notebooklm-py` 0.4.1 CLI + `notebooklm-mcp-cli` 0.6.9 (entrambi via uv tool / pip user) — auth pending Eduardo
- ✅ Created `~/.local/bin/aider-hf.cmd` wrapper (default DeepSeek R1, security-hardened temp env-file pattern)

**Gap pending (non bloccanti)**:
- ⏸️ `OPENROUTER_API_KEY` (Hybrid A1 emergency overflow Pro 5h rate-limit) — Eduardo manual signup quando senti il bisogno
- ⏸️ `HUGGINGFACE_API_KEY` — Eduardo signup huggingface.co + token (vedi sezione 6.4 step-by-step)
- ⏸️ NotebookLM auth — Eduardo `notebooklm login` (browser OAuth interactive, vedi sezione 6.5)
- ⏸️ Claude Code MCP server config notebooklm-mcp — Eduardo aggiunge a `~/.claude.json` projects.<repo>.mcpServers (richiede CC restart)

---

## 2. Tool ecosystem completo

3 categorie distinte basate su auth method e integrazione tecnica.

### 2.1 REST tools (auth via API key, integrazione programmatica)

| Tool | Binary | Auth | Routing tier |
|---|---|---|---|
| **Claude Code desktop** | Claude Code app | OAuth Max/Pro/OS keychain | Strategic + hub session |
| **Aider wrappers** | `~/.local/bin/aider-*` (6) | env vars from keys.env | Single-file edit (tier 1-4) |
| **OpenCode** | `~/AppData/Roaming/npm/opencode.cmd` | env vars from keys.env + Meridian plugin per Pro | Multi-step agentic (tier 1-4) |
| **Gemini CLI** | `~/AppData/Roaming/npm/gemini.ps1` | `GEMINI_API_KEY` env var | Long-context analysis (1M ctx) |
| **Ollama API** | localhost:11434 | none (sovereign local) | Tier 1-2 local |
| **Claude API direct** | curl/requests | `ANTHROPIC_API_KEY` env var | Tier 0 strategic post-Max (dormant) |

### 2.2 Interactive web UIs (auth via browser, dispatching manual)

Nessuna integrazione programmatica diretta. Si usano via browser. Eduardo dispatcha manualmente quando il task ha caratteristiche adatte.

| Tool | Auth | Use case primario | Quando preferirlo |
|---|---|---|---|
| **ChatGPT.com** | OAuth ChatGPT subscription | Conversational + brainstorming + one-shot complex | Esplorazione tema senza file context, persona-driven |
| **OpenAI Codex Cloud** | OAuth ChatGPT subscription | Sandboxed parallel agent su Game (multi-client ADR-0021) | Task isolabili in sandbox, async parallel work |
| **NotebookLM** | OAuth Google | Source-grounded research synthesis (audio overviews, citation tracking) | Analisi documenti lunghi multi-source con grounding citations |
| **Manus** | Manus subscription | Autonomous task execution end-to-end (300 credits/day free, $20/mo standard) | Task delegabili full-autonomous (es. ricerca + report + presentation) |

**Important**: questi tool **non hanno API integration** con codemasterdd dispatcher. Sono "Tier interactive" — Eduardo decide manualmente quando aprire il browser invece di delegare a tool REST. La frase "smistiamo" si applica anche qui, ma il dispatching è cognitivo non automatizzato.

**NotebookLM API status (verified 2026-05-15)**: Enterprise alpha via Vertex AI esiste ma è pre-GA + enterprise-only. Public API ancora **non disponibile**. Unofficial wrappers (teng-lin/notebooklm-py, nblm-rs) esistono ma ToS gray area + breakage risk — **non adottare**.

**Manus API status (verified 2026-05-15)**: nessuna API tier pubblica documentata. Solo web-agent platform. Pricing free 300 credits/giorno + Standard $20/mese 4000 credits.

### 2.3 Local sovereign (Ollama, zero key)

| Model | Tier | Use case | Speed |
|---|---|---|---|
| `qwen2.5-coder:7b` Q4_K_M | 1 | Query one-shot + cosmetic edit | 114 tok/s |
| `qwen2.5-coder:14b-instruct-q2_K` | 2 | Behavior-critical edit (sweet spot) | 18.7 tok/s isolato / 17.6 mixed |
| `qwen3-coder:30b` MoE A3B | 2 escalation | OpenCode default + R1 anti-pattern | 23.3 tok/s @ 8K ctx |
| `deepseek-r1:8b` | reasoning | Logic debug + chain-of-thought | 74.57 tok/s full GPU |
| `gemma4:latest` | multimodal | Vision/audio/screenshot OCR | 39.26 tok/s |
| `nomic-embed-text` | embedding | Dafne H5 gate (utility) | n/a |

Modelli aggiuntivi installati (qwen3, qwen3.5, qwen3.6, qwen2.5:32b, phi4, deepseek-r1:14b, mistral) **non in tier routing primario** — bench coverage opzionale post-Max.

---

## 3. Routing matrix unificata

3 layer decisionali concentrici da applicare in ordine.

### Layer 1 — Privacy (enforcement automatico ADR-0019 H8)

Pre-domanda obbligatoria: **il file/repo è sovereign-only o cloud-OK?**

```
git rev-parse --show-toplevel → check ~/.config/aider-privacy-whitelist.txt
├── Whitelisted (codemasterdd, Game public, Game-Godot-v2 public)
│   → tutti i tier disponibili
└── NOT whitelisted (Synesthesia controllers/, repo cliente futuri)
    → ABORT cloud, solo local Ollama
```

Wrapper Aider cloud (`aider-groq-bypass` / `aider-cerebras` / `aider-gemini` / `aider-openai`) enforced via git rev-parse check. Bypass deliberato: aggiungi temporaneamente alla whitelist, ripristina post-task. **Anti-pattern**: commentare il check inline (perde guard rail).

### Layer 2 — Task class

| Class | Caratteristiche | Tool primario | Fallback |
|---|---|---|---|
| **Strategic** | Multi-file ≥3, synthesis cross-source, ADR draft, debug architetturale, constraint ≥5 strict | Claude Code (durante Max) / Codex Cloud (parallel agent) | Manual su Claude API post-Max |
| **Multi-step agentic** | Tool orchestration (Read+Edit+Bash+ListFiles), multi-file refactor con coord | OpenCode (`ollama/qwen3-coder:30b`) | Claude Code direct |
| **Behavior single-file** | Bug fix, logic change, refactor su 1 file | `aider-refactor` (Qwen 14B Q2 local) | `aider-cerebras` (Llama 70B cloud free) |
| **Behavior escalation** | 14B safe-fails (anti-pattern R1, 1-line value change) | `aider-groq-bypass` (Llama 70B Groq 30s) | `aider-cerebras` |
| **Cosmetic single-file** | JSDoc, docstrings, rename, lint-fix | `aider-cosmetic` (Qwen 7B local) | `aider-refactor` se file in subdir + docstring self-ref (caveat L-007) |
| **Q&A read/explain one-shot** | Domanda diretta, no edit | `ollama run qwen2.5-coder:7b` | Gemini CLI free se ctx >100K |
| **Long-context analysis** | >100K token (multi-file synthesis read-only) | Gemini CLI (1M ctx free tier) | Claude Code (200K) |
| **Reasoning + debug logica** | Chain-of-thought, problemi logici | `ollama run deepseek-r1:8b` | Claude Code Opus durante Max |
| **Multimodal** | Screenshot OCR, vision, audio | `ollama run gemma4` | Gemini Pro vision (free tier) |
| **Dafne swarm content** | Lore, traits, balance, narrative gen | Swarm internal (Flask + Tavily) | Eduardo approve via `/api/dafne/approve-agent` |
| **Web research** | Multi-source synthesis | WebSearch + WebFetch (Claude Code native) | Tavily via Dafne (deferred) |
| **Brainstorming + esplorazione conversazionale** | Persona-driven, no file context | ChatGPT.com web UI | Manus web UI (autonomous) |
| **Sandboxed parallel work** | Task isolabili async su Game | Codex Cloud web UI | n/a |
| **Source-grounded multi-doc research** | Document analysis con citation tracking | NotebookLM CLI/MCP programmatic (post auth) | Gemini CLI 1M ctx (alt) |
| **Reasoning-heavy task** (DeepSeek R1 class) | Logic-heavy, math, complex debug | `aider-hf` (DeepSeek R1 via HF) | ollama deepseek-r1:8b local |
| **Specialty model need** (vision/audio/embed) | Task richiede modello non-mainstream | HF Inference Providers (300+ models proxy) | Gemini Pro vision / OpenAI |
| **Autonomous end-to-end task** | Ricerca + report + delivery senza intervento | Manus web UI (300 credits/day free) | Codex Cloud parallel |

### Layer 3 — Constraint count (ADR-0016 second dimension)

Conta vincoli espliciti nel prompt:

| # constraints | Routing |
|---|---|
| 1 generico | Qualsiasi tier sopra |
| 2-3 additivi+preserve | 14B Q2 local OR 70B cloud free |
| 2 fix+transform | Downgrade 14B (7B skippa transform) |
| ≥5 strict | Manual Claude Code (no delega) |

---

## 4. Workflow handoff cross-tool

### 4.1 Pattern Hub-and-spoke (default operativo)

```
Claude Code (hub session)
├── Classify task (privacy + class + constraint)
├── Decide: do direct OR delegate?
├── If delegate:
│   ├── Aider single-file → run wrapper, verify diff post
│   ├── OpenCode multi-step → run with model + verify output
│   ├── Ollama direct → run + capture output
│   └── Gemini CLI long-ctx → run with API key + capture
└── Synthesize results back in hub session
```

### 4.2 Pattern Web-UI dispatching (interactive tools)

```
Eduardo cognitive dispatch (not automated):
├── Task brainstorming + esplorazione → open ChatGPT.com tab
├── Task sandbox async su Game → open Codex Cloud tab
├── Task long-doc grounded research → open NotebookLM tab
├── Task autonomous full-stack → open Manus tab
└── Cross-pollination: copy-paste verso Claude Code hub per integration
```

**Caveat**: web UI tier NON entra nel dispatcher automatico. Eduardo decide manualmente quando il task ha caratteristiche adatte (es. ricerca con audio overview → NotebookLM, brainstorming free-form senza file → ChatGPT, autonomous report → Manus).

---

## 5. Hybrid A1 post-Max (ADR-0030, attivo 2026-05-19+)

Cambio del componente "hub session" da Claude Code Max OAuth a OpenCode + Meridian bridge + Claude Pro $20/mo:

```
PRE 19/05:                          POST 19/05 (Hybrid A1):
Claude Code (Max OAuth)        →    OpenCode TUI (orchestratore)
+ Ollama local                       + Meridian → Claude Pro (sub-agent dispatch)
+ wrappers Aider                     + Gemini CLI free (1M ctx)
+ Codex Cloud (parallel)             + Ollama local (preserved)
                                     + wrappers Aider (preserved)
                                     + (Optional) OpenRouter overflow
                                     + Codex Cloud (preserved)
                                     + ChatGPT.com / NotebookLM / Manus (preserved web UI)
```

Routing matrix Layer 2 sopra **resta valida** post-19/05 — cambia solo il hub orchestratore.

Validation criteria 1 mese empirical (19/5 → 19/6):
- Cost actual ≤$50/mese
- Daily orchestration feasibility PASS
- Methodology cite count ≥80% baseline (vs Claude Code Max attuale)
- Sub-agent dispatch viability ≥2 invocazioni per session significativa

---

## 6. Potential additions (decision deferred)

### 6.1 HuggingFace Inference Providers (tier 3 unified proxy) — **INTEGRATED 2026-05-15**

**Cosa è**: HF Inference Providers è un unified proxy OpenAI-compatible che dà accesso a **300+ modelli** distributed across 18+ providers (Cerebras, Groq, Together, Fal, Replicate, SambaNova, Fireworks, ecc.) tramite **single token**. Drop-in replacement OpenAI API.

**Endpoint**: `https://router.huggingface.co/v1`
**Auth**: `HF_TOKEN` Bearer (header) o env var.

**Use case unici vs Groq/Cerebras diretti**:
- **DeepSeek R1**: reasoning specialty, NON in Groq/Cerebras free
- **GPT-OSS 120B**: open weights 120B (qualità simile Claude Haiku, gratuito)
- **Qwen 2.5 Coder 32B** specialty coder via API
- **FLUX.1**: image generation (text→image)
- **Embeddings**: SOTA models (NV-Embed, BGE, etc.)
- **VLM** (vision): GLM-4V, Llama Vision 90B
- **Speech-to-text**: Whisper variants

**Provider selection policy** (model suffix):
- `:fastest` (default) → highest throughput across providers
- `:cheapest` → lowest $/tok across providers
- `:preferred` → user-configured preference order
- `:<provider-name>` → force specific provider (es. `:sambanova`)

**Free tier 2026** (verified): 100K monthly credits, modello size limit ~10B params nominally (but proxy to upstream provider relaxes this — DeepSeek R1 + GPT-OSS 120B accessibili gratis via routing).

#### Setup step-by-step (Eduardo manual, ~3 minuti)

```powershell
# 1. Signup https://huggingface.co (Google/GitHub OAuth o email)
# 2. Generate fine-grained token:
#    https://huggingface.co/settings/tokens/new?ownUserPermissions=inference.serverless.write&tokenType=fineGrained
#    Permission: "Make calls to Inference Providers"
# 3. Append to keys.env:
Add-Content "$env:USERPROFILE\.config\api-keys\keys.env" -Value "HUGGINGFACE_API_KEY=hf_..."
# 4. Test wrapper:
cd C:\dev\codemasterdd-ai-station   # repo whitelisted
aider-hf <file>                      # default DeepSeek R1
# 5. Test OpenCode integration:
opencode run --model "huggingface/deepseek-ai/DeepSeek-R1:fastest" "Spiegami questo file"
```

#### Pre-built integration (already installed 2026-05-15)

- **Aider wrapper** `~/.local/bin/aider-hf.cmd` — default model `deepseek-ai/DeepSeek-R1:fastest`, security-hardened (temp env-file NTFS-protected, key NOT in argv), privacy guard rail H8 attivo, diff format + no-auto-commits + git-commit-verify
- **OpenCode provider** `huggingface` entry in `~/.config/opencode/opencode.json` — baseURL + 3 models pre-mapped (DeepSeek R1 reasoning, GPT-OSS 120B general, Qwen 2.5 Coder 32B specialty)
- **OpenAI-compatible** drop-in: ogni altro tool che supporta OpenAI SDK puntando a `https://router.huggingface.co/v1` con `HF_TOKEN` come API key funziona out-of-the-box

### 6.2 NotebookLM CLI + MCP — **INTEGRATED 2026-05-15**

**Cosa è**: Eduardo già usa NotebookLM web UI (notebooklm.google.com) per source-grounded research. Ora integration programmatica via:
- **`notebooklm-py` 0.4.1** ⭐ 13.2k stars — Python library + CLI con personal Google OAuth via Playwright
- **`notebooklm-mcp-cli` 0.6.9** ⭐ 4.4k stars — MCP server per Claude Code / OpenCode integration

#### Capacità unlocked vs web UI

Operazioni che la CLI/MCP espongono OLTRE web UI:
- `notebooklm create "My Notes"` — create notebook programmatic
- `notebooklm source add` — add source PDF/URL/text via CLI
- `notebooklm ask "..."` — query corrente notebook
- `notebooklm generate audio|video|quiz|flashcards|slide-deck|infographic|mind-map|data-table` — generate artifact via API
- `notebooklm download all` — bulk export artifacts
- `notebooklm profile list` — multi-account switching
- `notebooklm share status` — share state programmatico

#### Pre-built integration (status verified 2026-05-15)

- **`nlm.exe` + `notebooklm-mcp.exe` 0.6.9** → `~/.local/bin/` (via `uv tool install`) — **REAL su host**, persistent
- ~~`notebooklm.exe` 0.4.1 via pip --user~~ — **PHANTOM**: Claude Code Bash overlay filesystem ha installato in `AppData/Roaming/Python/` ma path non visibile a host. Re-install richiesto da Eduardo terminal se vuoi CLI: `pip install --user notebooklm-py[browser]`
- ~~Playwright chromium 1217/1223 in `AppData/Local/ms-playwright/`~~ — **PHANTOM**, stesso pattern. Re-install richiesto da Eduardo terminal: `playwright install chromium`

**Raccomandazione pragmatica**: usare `nlm` MCP server (real) + NotebookLM web UI per browsing manuale. Skip notebooklm-py CLI install fino a quando emergono use case che richiedano programmatic generate/download artifacts.

#### Setup auth (Eduardo manual, ~2 minuti)

**Default path (Chromium bundled Playwright)**:
```powershell
notebooklm login
```

**KNOWN ISSUE 2026-05-15**: Playwright bundled chromium-1217/1223 fallisce con `BrowserType.launch_persistent_context: spawn UNKNOWN` + Win32 SxS error "Impossibile avviare l'applicazione: configurazione modalità affiancata non corretta". VC++ Redistributable 2015-2022 GIÀ INSTALLATO (msvcp140.dll + vcruntime140_1.dll presenti) — root cause SxS diverso, deeper Windows-specific. Skip default chromium path.

**Workaround msedge (RACCOMANDATO)**:
```powershell
notebooklm login --browser msedge
# Si apre Edge - fai login Google personale - autorizza
# Torna in PowerShell - premi ENTER
notebooklm auth check --test
notebooklm list
```

**Failed workaround Chrome cookies** (rookiepy):
```powershell
pip install --user "notebooklm-py[cookies]"
notebooklm login --browser-cookies chrome
# FAIL 2026-05-15: "Could not decrypt chrome cookies"
# DPAPI Windows encryption blocca rookiepy
```

**Smoke post-auth**:
```powershell
notebooklm use <notebook-id-partial>
notebooklm ask "Riassumi in 3 punti"
```

Auth persists 2-4 settimane con auto-refresh token.

#### Claude Code MCP integration (Eduardo manual, richiede CC restart)

Add to `~/.claude.json` projects.<repo>.mcpServers:

```json
{
  "projects": {
    "C:/dev/codemasterdd-ai-station": {
      "mcpServers": {
        "notebooklm": {
          "command": "notebooklm-mcp",
          "args": ["--transport", "stdio"]
        }
      }
    }
  }
}
```

Poi `/mcp` in Claude Code session per reconnect. Dopo: hai tools `notebooklm_*` disponibili in sessione (ask, create, list, generate, etc.).

#### OpenCode MCP integration

Add to `~/.config/opencode/opencode.json` mcp field:

```json
{
  "mcp": {
    "notebooklm": {
      "type": "local",
      "command": ["notebooklm-mcp", "--transport", "stdio"],
      "enabled": true
    }
  }
}
```

#### ToS + breakage risk

⚠️ **Unofficial library**, usa undocumented Google API. Google potrebbe cambiare auth flow → tool break. Mitigation:
- Versione pinned 0.4.1 (current)
- Fallback web UI sempre disponibile
- Maintenance attiva: 13.2k stars + multiple releases monthly (basso rischio abbandonment)
- Auth via personal Google account, NON enterprise — niente impatto data residency

**Verdict**: integration concreta + reversibile. Se Google rompe l'API: `pip uninstall notebooklm-py` + ritorno a web UI. Costo adozione minimo.

### 6.3 GitHub Models — **PROPOSED 2026-05-15** (Eduardo decide trigger)

**Cosa è**: servizio nativo GitHub che espone OpenAI/Anthropic/Mistral/Cohere/Llama/Phi models via REST + Azure OpenAI SDK. Auth via personal access token GitHub (Eduardo già `gh auth` come `MasterDD-L34D`).

**Free tier 2026**: ~150 req/giorno GPT-4o + GPT-4o-mini + Llama 3.3 70B + Mistral Large + Phi. Rate-limit giornaliero, no credit card.

**Gap che riempie**: nessun altro free tier attualmente integrato include **gpt-4o reale** (HF ha gpt-oss-120b open weights, NON gpt-4o proprietary). 150 req/giorno = utile per task strategic-light dove vuoi quality OpenAI senza pagare `OPENAI_API_KEY`.

**Setup quando Eduardo decide go**:
```powershell
# 1. https://github.com/settings/tokens?type=beta
#    Fine-grained PAT, owner: MasterDD-L34D, permission: Models read-only
# 2. Append a keys.env:
Add-Content "$env:USERPROFILE\.config\api-keys\keys.env" -Value "GITHUB_MODELS_API_KEY=github_pat_..."
# 3. Smoke test OpenAI-compat:
curl https://models.github.ai/inference/chat/completions `
  -H "Authorization: Bearer github_pat_..." `
  -H "Accept: application/vnd.github+json" `
  -H "X-GitHub-Api-Version: 2022-11-28" `
  -H "Content-Type: application/json" `
  -d '{"model":"openai/gpt-4o-mini","messages":[{"role":"user","content":"3+3?"}]}'
```

**IMPORTANT verified empirical 2026-05-15**:
- Endpoint NEW 2026: `https://models.github.ai/inference` (era `models.inference.ai.azure.com` deprecato)
- Headers obbligatori: `Accept: application/vnd.github+json` + `X-GitHub-Api-Version: 2022-11-28`
- Model namespace: `openai/gpt-4o-mini` (con prefisso provider, era `gpt-4o-mini` solo)
- PAT path corretto: https://github.com/marketplace/models -> Use this model -> "Create Personal Access Token" auto-configura `Models: Read-only` permission corretto. Manual `?type=beta` path facile sbagliare permission scope (caso studio 2026-05-15 primo PAT no_access su tutti modelli)

**Verdict 2026-05-15 (ACCEPTED post smoke end-to-end PASS)**: working tier 3 cloud free, integrato via wrapper aider-github-models + LiteLLM hub. Test PASS: gpt-4o-mini-2024-07-18 risponde via LiteLLM endpoint port 4000 alias `github-gpt4o-mini`.

### 6.4 LiteLLM hub — **AUDIT existing config dormant**

**Stato attuale**: `infra/litellm-config.yaml` referenziato in ADR-0017 (Proposed 2026-04-24). Configurato per Docker stack con Langfuse + Postgres + dogfood-ui.

**Potenziale**: LiteLLM proxy come **single OpenAI endpoint** che routes verso TUTTI i provider (Ollama + Groq + Cerebras + Gemini + HF + Anthropic + GitHub Models). Tools downstream (Aider/OpenCode/scripts) si configurano UNA volta verso LiteLLM, poi switching modello = solo cambio nome.

**Cosa va verificato**:
1. Stack Docker UP/DOWN attualmente?
2. Config current con i 7 keys + nuovi (HF, GitHub Models)?
3. Vale revivere vs abandon?

**Trade-off**:
- **PRO**: single endpoint = simplification dispatcher, cost tracking centralizzato, fallback automatico cross-provider
- **CON**: latency overhead (~10-50ms), single point of failure, complessità Docker

**Verdict 2026-05-15**: audit task SPRINT_02 day 1 — verificare stato + decidere revive vs abandon. Eduardo conferma o no scope SPRINT_02.

### 6.5 Free LLM API reference lists (bookmark only, periodic scan)

Curated lists per scoprire nuovi free tier emergenti senza investigation overhead per provider:

- [cheahjs/free-llm-api-resources](https://github.com/cheahjs/free-llm-api-resources) — community-driven, mirror SourceForge
- [amardeeplakshkar/awesome-free-llm-apis](https://github.com/amardeeplakshkar/awesome-free-llm-apis) — verified March 2026, OpenAI SDK compat, rate limits documented
- [mnfst/awesome-free-llm-apis](https://github.com/mnfst/awesome-free-llm-apis) — "Permanent free" filter strict
- [nherx/free-llm-api-resources](https://github.com/nherx/free-llm-api-resources)
- [O-LLM/Free-LLM](https://github.com/O-LLM/Free-LLM)
- [free-llm.com](https://free-llm.com/) — 45+ providers directory web

**Usage pattern**: scan trimestrale (Eduardo Q-review SPRINT boundary) per identificare provider mainstream emergenti. Quando un provider passa da "list" a "stable" (>=6 mesi uptime + segnali positivi r/LocalLLaMA), valutare integration come tier 3 add-on.

**Esempi candidati DEFER da queste liste 2026-05-15** (non adottati ora, monitorare):
- Cloudflare Workers AI (10K req/giorno free, Llama family) — overlap Groq
- NVIDIA NIM (free credit tier) — niche
- SambaNova (294 TPS) — già copertura Cerebras
- SiliconFlow, Inference.net, Together (via HF) — coverage già HF Inference Providers
- Mistral AI Le Chat (5 req/min) — niche specialty
- Pollinations AI, LLM7.io, Kluster — emerging

### 6.6 Researched + REJECTED 2026-05-15 (ToS/sustainability risk)

Decision applicata via Archon-style enumerate + challenge + falsifying experiment:

| Candidato | Reject rationale | Pattern anti-adoption |
|---|---|---|
| **Puter** ([developer.puter.com](https://developer.puter.com)) | Claim "400+ models GPT/Claude/Gemini, no API keys, no limits" — sustainability red flag. Free unlimited GPT-4/Claude proxy non è economicamente sostenibile → expect breakage o pivot paywall entro 6-12 mesi. Privacy: tutto passa through Puter intermediario sconosciuto. | "Too good to be true" sustainability |
| **CLIProxyAPI** ([router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)) | Wrap Gemini CLI / ChatGPT Codex / Claude Code in REST API multi-tenant. **Viola ToS** di ogni CLI (auth scoped a personal use, NON multi-tenant exposure). | ToS violation cascade |
| **GeminiHydra** | "Unlimited free-tier via multi-key rotation Gemini" richiede multipli account Google = **viola Google ToS** anti-abuse | Multi-account ToS violation |
| **alistaitsacle/free-llm-api-keys** | Repository aggregator di leaked API keys aggiornato 3-5×/giorno. Violation upstream provider ToS + ethical/legal exposure. | Stolen credentials redistribution |
| **fuergaosi233/claude-code-proxy** | Claude Code → OpenAI API proxy: tecnicamente interessante ma use case sovrapposto a Meridian (opencode-with-claude plugin) per Hybrid A1 nostro. Non gap-fill. | Overlap existing solution |

**Pattern comune anti-adoption**: tool che danno "value gratuito non sostenibile" via shortcut tecnico violando ToS upstream. Adoption = breakage rischio alto + ethical issue + legal exposure quando provider giro vite.

**Lesson learned 2026-05-15** (candidate L-2026-05-NNN promo dopo verifica n>=2 pattern): il free tier **sostenibile** è quello dove il provider HA business model che giustifica il free tier:
- Groq vende enterprise capacity → free tier acquisition funnel
- HuggingFace vende premium subscriptions + enterprise → free tier community building
- Google vende GCP/Workspace → free tier developer onboarding
- GitHub vende Enterprise + Copilot → free tier developer engagement

I "gateway che danno gratis senza upstream economics" sono trap. Apply criterio "where does provider's money come from?" PRE-adoption.

### 6.7 OpenRouter (Hybrid A1 emergency overflow)

**Cosa offre**: BYOK pay-per-use con 300+ models, fallback automatico, Claude Sonnet/Haiku/Opus 4 + DeepSeek + Llama + Qwen.

**Quando attivare**: durante 1-month empirical validation Hybrid A1, se Pro 5h rate-limit si manifesta come bottleneck reale (≥2 incidenti per settimana).

**Setup**: signup openrouter.ai + key + append a keys.env + update opencode.json provider (template in setup script).

**Verdict 2026-05-15**: deferred trigger empirical Pro saturation.

### 6.8 Autoresearch tooling (Karpathy + ecosystem)

**Cosa offre**: Karpathy autoresearch (March 2026, 72k stars) — experiment loop tool per ML training optimization. Pi-Autoresearch, Thoth, AutoResearchClaw spawn dall'ecosystem.

**Verdict 2026-05-15**: **DEFERRED indefinitely** — dominio mismatch:
- Karpathy autoresearch = ML training propose-train-evaluate loop, NON multi-source research synthesis
- Quello che noi chiamiamo "Protocol 2 autoresearch" è già coperto da WebSearch + WebFetch + synthesis in Claude Code session
- Adoption cost (install + workflow integration) > benefit incremental
- Re-evaluate SPRINT_03+ se emergono use case ML training optimization concreti

Reference memoria: `reference_autoresearch_tools` (top candidate 199-biotech/autoresearch-cli + Karpathy MIT) — leave dormant.

---

## 7. Anti-pattern catalog (cose da NON fare)

1. **Cloud delega su repo NON whitelisted** — Synesthesia controllers/, repo cliente futuri vanno solo local Ollama. Wrapper guard rail tecnico previene, ma se commenti inline il check perdi protezione.
2. **Aider whole format su 14B Q2 per behavior edit** — silent-corruption deterministico (ADR-0008). Sempre diff format per behavior-critical.
3. **Hardcoded API key in repo OR registry (`setx`)** — keys vanno SOLO in `~/.config/api-keys/keys.env` ACL-hardened.
4. **Qwen 2.5 Coder family con OpenCode `run` mode** — emette JSON raw stringificato, NON eseguito. Sweet spot Aider non si trasferisce. Default OpenCode è `qwen3-coder:30b`.
5. **Strategic task delegato a 7B/14B** — multi-file synthesis + constraint ≥5 strict richiedono tier 0 (Claude Code/API direct), no shortcut economico.
6. **Web UI tier dispatchato programmatic** — ChatGPT/Codex Cloud/NotebookLM/Manus NON hanno API integration codemasterdd-side. Dispatching è cognitivo Eduardo-side, NON automatizzabile.
7. **Adottare unofficial wrapper NotebookLM** — ToS gray area + breakage risk. Se serve programmatic long-doc analysis usa Gemini CLI 1M ctx (sanzionato).

---

## 8. Quick reference cheat-sheet

```
# Q&A one-shot rapido
ollama run qwen2.5-coder:7b "..."

# Cosmetic single file
aider-cosmetic <file>

# Behavior single file (default safer)
aider-refactor <file>

# Behavior escalation (14B fail)
aider-groq-bypass <file>

# Cloud free 70B alternative
aider-cerebras <file>
aider-gemini <file>

# Cloud paid emergency
aider-openai <file>

# Reasoning specialty (DeepSeek R1 via HF, post HF signup)
aider-hf <file>

# Multi-step agentic
opencode run --model "ollama/qwen3-coder:30b" "..."

# HF Inference Provider via OpenCode (post HF signup)
opencode run --model "huggingface/deepseek-ai/DeepSeek-R1:fastest" "..."
opencode run --model "huggingface/openai/gpt-oss-120b:fastest" "..."

# NotebookLM CLI (post `notebooklm login`)
notebooklm list
notebooklm use <notebook-id>
notebooklm ask "..."
notebooklm generate audio

# Long-context analysis (>100K token, 1M free)
$env:GEMINI_API_KEY = (gc ~/.config/api-keys/keys.env | sls "^GEMINI_API_KEY=").Line -replace "^GEMINI_API_KEY="
gemini --prompt "..." 

# Reasoning + debug
ollama run deepseek-r1:8b "..."

# Strategic / hub session
# (in Claude Code o post-Max OpenCode + Meridian + Pro)

# Web UI dispatching (browser, no automation)
# ChatGPT.com / chat.openai.com/codex / notebooklm.google.com / manus.im
```

---

## 9. Riferimenti

**ADR rilevanti** (in ordine di rilevanza):
- ADR-0008 Aider whole format silent-corruption + tier routing rationale
- ADR-0013 Tier 3 cloud free providers (Groq + Cerebras + Gemini)
- ADR-0016 Constraint-count routing dimension (Proposed)
- ADR-0019 H8 privacy guard rail tecnico
- ADR-0022 OpenCode tool-use model routing
- ADR-0023 Strategic tier post-Max API on-demand
- ADR-0030 Hybrid A1 post-Max orchestration

**Memorie operative**:
- `feedback_hub_delegation_pattern.md` — 3-tier Aider routing logic
- `reference_api_keys.md` — keys.env paths + auto-load mechanism
- `reference_autoresearch_tools.md` — autoresearch ecosystem deferred status

**Reference esterni verified 2026-05-15** (autoresearch sezione 6):
- NotebookLM API status: Google Cloud docs Vertex AI Enterprise alpha
- Manus pricing: manus.im/pricing, lindy.ai blog 2026
- HuggingFace pricing: huggingface.co/pricing + docs/inference-providers/pricing
- Karpathy autoresearch: github.com/karpathy/autoresearch (March 2026)

---

**Owner**: Eduardo Scarpelli
**Maintenance**: aggiornare quando aggiungi/rimuovi key oppure cambi tier routing (es. quando Hybrid A1 transitiona da Proposed ad Accepted post-19/05).
