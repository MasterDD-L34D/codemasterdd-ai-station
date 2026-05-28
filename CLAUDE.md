# CLAUDE.md — CodeMasterDD AI Station

## Ruolo workstation
Dev workstation AI agentic **PRINCIPALE** per Eduardo Scarpelli.
Questa macchina è autosufficiente per tutti i workflow dev e AI locali.
Target: piattaforma AI sovereign-first (locale-prioritario, no-lock-in, multi-provider). ⚠️ **PIVOT ACCETTATO 2026-05-18 (ADR-0030, Decisione 009)**: il target "zero subscription / $0-50/anno absolute" e' **SUPERSEDED** -> **Hybrid A1** (Pro $20/mo + Meridian + OpenCode + Gemini-CLI-free + OpenRouter-overflow, ~$240-600/anno). Filosofia sovereign-first invariata; il numero $0-50 e' morto. Vedi ADR-0030.

## Roadmap strategica (realistica — aggiornata 2026-04-23 post ADR-0013+0014)
- **19/04/2026**: ✅ setup Lenovo completato, infrastructure ready
- **20-21/04**: ✅ Ollama + Qwen 7B/14B, ADR-0004/0007/0008 findings
- **22/04**: ✅ migrazione Evo-Tactics + Synesthesia, RAM upgrade 64GB (ADR-0012), API keys cloud (ADR-0013 Accepted)
- **22-23/04 notte**: ✅ quality bench + 4 wrapper cloud + 6 dogfood Fase 6 inaugurati
- **Fino al 19/05**: Claude Max attivo, Fase 6 tracking compresso (ADR-0014 Accepted) — target n≥20 dogfood + privacy validation + cost tracking <$20/mese
- **20/05/2026 (approx, allineato Claude Max expiration)**: Fase 6 closure → **ADR-0015 budget decision finale**
- ⚠️ **AGGIORNAMENTO 2026-05-18 (premessa-drift corretta)**: deadline reale era ~**17/05** (non 19/20). Eduardo ha **ri-acquistato Claude Max +1 mese** (~17/05 → ~17/06/2026). Le righe "Fino al 19/05" / "20/05 closure / Post 20/05 sovereign" sopra sono **storiche, NON la deadline corrente**. Deadline sovereign-transition reale = **~17/06/2026**. Urgenza esistenziale OFF, scope sovereign INVARIATO (long-term). Dettaglio: ADR-0023 §Addendum 2026-05-18 + DECISIONS_LOG.
- **Post ~17/06 (deadline aggiornata)**: ~~full-sovereign $0-50/anno~~ → **Hybrid A1 ~$240-600/anno (ADR-0030 Accepted, pivot Decisione 009)**. Stack tier sotto resta valido come *layer locale-first*, ma orchestration/reasoning = Pro+Meridian, non free-tier-only:
  - Tier 1-2 locale: Qwen Coder 7B/14B/30B MoE (Ollama, RTX 5060)
  - Tier 3 cloud free: Groq llama-70B + Cerebras llama-8B
  - Tier 4 cloud paid (emergency only): OpenAI gpt-4o-mini
  - **Zero subscription ricorrenti** (abbandono Claude Max + no Claude Pro richiesto)

## Estensioni future (opzionali, non pianificate)
- **Mac mini M4 Pro 48GB** come **upgrade AI inference** se/quando budget permette
  - Aggiungerebbe capacità modelli 30B+ Ollama
  - **NON è dependency** del piano: Lenovo funziona pienamente da solo
- **Hyperspace Pods** (P2P AI Compute Clusters via libp2p) come **alternativa Mac mini scenario** (added 2026-05-10)
  - Pool device (Lenovo + futuro Mac mini + family/friends) in private cluster condiviso, NO infrastruttura proprietaria
  - Distributed inference + model sharing LAN ~1Gbps, NO cloud, NO central server (allineamento sovereign-first ADR-0015)
  - Hardware compatible: RTX 5060 8GB qualifies (VRAM 4GB minimum). License open (Pi MIT)
  - **Status**: REFERENCE only fase 1. Audit privacy P2P required PRE-install. Trigger evaluation: Mac mini scenario / VRAM 8GB constraint sentito / device pooling family-friends interest emerge
  - Dettaglio: REFERENCE_INDEX EXT-03 + memory `reference_hyperspace_pods.md`

## Hardware (definitivo)
- **CodeMasterDD** (Lenovo LOQ Tower 17IAX10, desktop)
  - Intel Core Ultra 7 255HX (24 core Arrow Lake HX, 2.40 GHz base)
  - NVIDIA RTX 5060 8GB VRAM (Blackwell sm_120, CUDA 13.2)
  - **64GB DDR5-5600** (2×32GB Micron CT32G56C46S5.C16D, dual channel ChannelA+ChannelB DIMM1) — upgrade 2026-04-22 da 16GB originali, vedi `docs/adr/0012-ram-upgrade-64gb-impact.md`
  - SSD 1TB Micron NVMe (~877 GB liberi post-cleanup bloatware)
- OS: Windows 11 Home 25H2 (build 26200, no KB5083769)

## Capacità AI locali (Lenovo da solo)
- Modelli **full-GPU** su 8 GB VRAM: fino a 7-8B a quality piena (Qwen 2.5 Coder 7B, Qwen 3 8B, DeepSeek 7B)
- Modelli **14B**: entrano parzialmente (60-75% GPU + CPU spill 25-40%) — usabili ma throughput ridotto
- Velocità **misurate** (sustained eval, prompt DoublyLinkedList Python isolated single-task):

| Modello | Tok/s isolato | GPU offload | Uso consigliato |
|---------|--------------|-------------|-----------------|
| Qwen 2.5 Coder 7B Q4_K_M | 114 | 100% | query one-shot, create, read/explain |
| Qwen 2.5 Coder 14B Q3_K_M | 10.8 | 62% | sconsigliato (hallucination su constraint) |
| Qwen 2.5 Coder 14B **Q2_K** | 18.7 | 73% | **agentic edit (sweet spot + faithful)** |

- Velocità **mixed-workload** (bench H9 2026-05-09, n=4 per tier, 11 swap forced, vedi `docs/research/bench-mixed-workload-2026-05-09.md`):

| Modello | Tok/s isolato | Tok/s mixed (n=4) | Drift | Note workflow misto |
|---------|--------------|------------------|-------|---------------------|
| Qwen 2.5 Coder 7B Q4_K_M | 114 | **100.75** | -12% | Realistic per workflow continuo |
| Qwen 2.5 Coder 14B Q2_K | 18.7-25 | **17.62** | **-30% vs 25 doc** | Sweet spot ma drift significativo |
| qwen3-coder:30b MoE A3B | 23 | **32.98** | **+43% upside** | **Discovery positiva**: superiore a doc precedente, ora competitive con 14B Q2 in throughput + capability superiore |

**Swap overhead** (workflow alternato 7B/14B/30B): **3047ms/swap × 11 swap = 33.5s su 79.2s totale = 42.3%** del workflow misto.

**Mitigation quantificata** (bench batched 2026-05-09): se task per stesso modello vengono raggruppati prima di switch (run [4×7B → 4×14B Q2 → 4×30B]), workflow time scende a **49.9s (saving 37%)** con solo 2 swap. Throughput per-modello invariato. Raccomandazione: **quando possibile, batch task per modello** (es. tutti i cosmetic 7B prima, poi tutti behavior 14B Q2, poi escalation 30B MoE).

- Stack agentic sovereign consigliato: **Aider + Qwen 14B Q2_K** — vedi `docs/adr/0007-aider-qwen-quantization-findings.md`
- Env vars Ollama applicate (User scope, persistenti) — config rationale: `docs/adr/0004-ollama-rtx5060-config.md` + `docs/adr/0007-aider-qwen-quantization-findings.md`
  - `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_KEEP_ALIVE=30m`
  - `OLLAMA_CONTEXT_LENGTH=8192` (ridotto da 16384 il 2026-04-20 su 16GB RAM: +36% speed su 14B Q2 liberando KV cache da CPU spill. Override per-request `num_ctx: 16384` per task multi-file. **Post upgrade 64GB 2026-04-22: il razionale originale è decaduto — rivalidare bench empirico prima di riportare default a 16384**, vedi `docs/adr/0012-ram-upgrade-64gb-impact.md`.)
- **Nuova capacità post 2026-04-22 (64GB RAM)**: modelli 30B+ non più RAM-bound; qwen3-coder:30b tier 2 non più borderline; Qwen 2.5 Coder 32B Q4 (~19-20GB) diventa candidato benchmarkable; 14B Q3_K_M potrebbe tornare competitivo con ctx più alto. Tutti i valori tok/s in tabella rimangono **validi** (misurati pre-upgrade, ma non RAM-bound) — rebench opzionale solo per scoprire se ctx più largo cambia la decision matrix.

## Ecosistema device (aggiornato 2026-05-12 post IP + username + AI stack drift fix; base 2026-05-10 LAN discovery + Ryzen capability reveal)

Fleet Eduardo on-LAN 192.168.1.0/24 (4 PC totali, 2 di Eduardo + 2 di moglie):

- **CodeMasterDD** (Lenovo LOQ Tower 17IAX10, **192.168.1.10** DHCP reservation locked 2026-05-13 notte): workstation primaria AI agentic. IP history: `.121` (2026-05-10) -> `.124` (2026-05-12) -> **`.10`** (2026-05-13 final, drift class killed via TIM HUB DGA4132 AGTHP reservation outside DHCP pool `.100-.200`).
- **DESKTOP-T77TMKT** (**192.168.1.11** DHCP reservation locked 2026-05-13 notte, user **`Vgit`** NON `edusc`) -- **Ryzen 9600X desktop EDUARDO** (rivelato 2026-05-10 NON in dismissione): MSI MS-7E26 mobo, **RTX 4070 SUPER 12GB VRAM** (verified 12282 MiB nvidia-smi 2026-05-12, driver 591.86 + CUDA 13.1), 31GB RAM, Windows 11 Pro build 26200, **OpenSSH server attivo + SSH key-based auth da Lenovo configurata 2026-05-12** (ed25519 in `C:\ProgramData\ssh\administrators_authorized_keys`, Vgit admin). IP history: `.222` (2026-05-10) -> `.225` (2026-05-12) -> **`.11`** (2026-05-13 final, DHCP reservation TIM HUB). Username `Vgit` registrato 2026-05-12. **Capability tier**: 14B Q4 full-GPU + 22B Q4 split + Codestral 22B + SDXL/Flux. **AI stack partially installed 2026-05-12** (Python 3.13.2, Node 24.11.0, Git 2.51.2, VS Code, Ollama 0.23.2 binary present **MA server NON autostart + 0 modelli installati**; aider missing). Disk C: 157GB free.
- **DESKTOP-B9L203E** (192.168.1.37) -- secondary desktop **moglie**: Windows DESKTOP-XXX hostname, MAC Samsung OUI 2C:F0:5D, capability TBD, OpenSSH non attivo (install pending Eduardo direct)
- **LAPTOP-D73A8DIE** (192.168.1.130) -- laptop **moglie**: Windows LAPTOP-XXX hostname, MAC A0:A4:C5, capability TBD, OpenSSH non attivo (install pending Eduardo direct)

**Drift fix 2026-05-10**: claim originale "Ryzen 9600X desktop: PC appoggio corrente, dismissione graduale" e' OBSOLETO. Ryzen ha 4070 SUPER 12GB > Lenovo 5060 8GB per modelli 14B-22B. Ryzen e' **secondary inference active** + complementary tier capability, NOT phase-out.

**Drift fix 2026-05-17 (chiude A.4#7 runbook)**: SSH ora **bidirezionale WORKING** Ryzen<->Lenovo. Oltre Lenovo->Ryzen (2026-05-12, key in Ryzen admin-file), stabilito **Ryzen->Lenovo 2026-05-17** (keypair `vgit-ryzen-to-lenovo-2026-05-17`: keygen locale Lenovo -> scp privata su Ryzen `C:\Users\Vgit\.ssh\id_ed25519` -> `setup-ssh-inbound.ps1` elevato+UAC su Lenovo; pub in Lenovo `administrators_authorized_keys`). Verificato test-annidato `OK_RYZEN_TO_LENOVO`. Comando: `ssh -i ~/.ssh/id_ed25519 edusc@192.168.1.10`. **SoT-completo**: `docs/runbook/ssh-inbound-fleet-setup.md` (inventario+matrice+gotcha-admin-ACL+script idempotente). SSH = mezzo-coordinamento PRIMARIO NOTO (anti-rot Eduardo-flag 2026-05-18): read-ops=libero, mutating-remote=gated-ma-noto. Wife-PC (.37/.130) SSH-PENDING = stesso script §Riuso-fleet quando-serve.

**Strategic implication fleet-aware**:
- Lenovo: tier 1 cosmetic (7B Q4 full-GPU 114 tok/s) + agentic hub (Aider/OpenCode/Claude Code stack) + 30B MoE Ollama partial
- Ryzen: tier 2 behavior (14B Q4 full-GPU atteso ~30-40 tok/s) + 22B Q4 split + image gen
- DESKTOP-B9L203E + LAPTOP-D73A8DIE: capability TBD, role Pod TBD post onboarding SSH

## Configurazione sicurezza applicata (19/04/2026)
- BitLocker: triplo layer disabilitato
- OneDrive: account scollegato, sync bloccato
- Bloatware rimosso (21 pacchetti)
- Account: eduscarpelli@gmail.com (con Claude Max attivo)

## API keys tier 3 cloud (aggiunto 2026-04-22)
- **Storage primario**: `C:\Users\edusc\.config\api-keys\keys.env` (ACL: `CODEMASTERDD\edusc:(F)` + `NT AUTHORITY\SYSTEM:(F)`, inheritance disabilitata via `icacls /inheritance:r`. SYSTEM kept per Windows backup/AV functionality; Administrators rimosso come escalation vector. Pre 2026-05-12 sera ACL claim "solo edusc" era drift documentazione: inheritance era ENABLED + Administrators inherited; hardening applicato durante H7 setup.)
- **Backup locale**: `C:\dev\codemasterdd-ai-station\backup\api-keys-2026-04-22.env` (gitignored via `backup/*`, ACL identiche)
- **Config Aider globale**: `C:\Users\edusc\.aider.conf.yml` contiene `env-file:` → auto-load in ogni sessione Aider (via LiteLLM)
- **Provider attivi** (free-tier):
  - **Groq** (`GROQ_API_KEY`) — LPU inference veloce, tier free 6000 tok/min, candidato tier 3 prioritario. Model examples: `groq/llama-3.3-70b-versatile`, `groq/qwen-2.5-coder-32b`
  - **Cerebras** (`CEREBRAS_API_KEY`) — WSE inference massima velocità, tier free generoso. Model examples: `cerebras/llama3.3-70b`
  - **Google Gemini** (`GEMINI_API_KEY` per Aider/LiteLLM; `GOOGLE_GENERATIVE_AI_API_KEY` per OpenCode native Google provider — dual-name necessario, vedi ADR-0022 follow-up) — 60 req/min free. Model examples: `gemini/gemini-2.5-flash` (`gemini-2.0-flash-exp` deprecated v1beta 404)
  - **OpenAI** (`OPENAI_API_KEY`) — pay-per-use (no free tier generoso). Model examples: `gpt-4o`, `gpt-4o-mini`
  - **Anthropic** (`ANTHROPIC_API_KEY`) — **tier 0 strategic post-Max** on-demand pay-per-use (ADR-0023). Setup 2026-05-12 sera (smoke test Haiku 4.5 PASS, $0.000044). Budget cap mensile $10-20, trigger reactivation Pro >$20/mese × 2 mesi consecutivi. Tracking: `logs/claude-api-spend-2026-MM.md` (gitignored). Model examples: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`.
- **Uso bash sessions**: `set -a; source ~/.config/api-keys/keys.env; set +a` (non auto-caricato da Claude Code bash)
- **Policy**: keys MAI in repo, MAI in registry (no setx), MAI in commit. Revoca rapida: `Remove-Item keys.env`. Vedi `docs/adr/0013-tier3-cloud-free-providers.md` per decision rationale.

## Stack installato
- Git 2.53.0.windows.3
- Claude Code 2.1.116 (OAuth Claude Max, Opus 4.7)
- NVIDIA Driver 595.79 + CUDA 13.2
- GitHub CLI 2.90.0 (installato 2026-04-19, auth MasterDD-L34D)
- Node.js 24.15.0 LTS + npm 11.12.1 (installato 2026-04-19, Active LTS fino aprile 2029)
- Python 3.12.10 (installato 2026-04-19)
- VS Code 1.116.0 x64 (installato 2026-04-19, commit `560a9dba96f961efea7b1612916f89e5d5d4d679`)
- Ollama 0.21.0 (installato 2026-04-19, servizio Windows auto-start)
- Modelli locali:
  - `qwen2.5-coder:7b` (Q4_K_M, 4.7 GB, digest `dae161e27b0e`, installato 2026-04-19) — **query one-shot, create single file, read/explain**
  - `qwen2.5-coder:14b-instruct-q3_K_M` (7.3 GB, digest `e00d09afd55a`, installato 2026-04-20) — capace ma rischio hallucination su constraint; 10.8 tok/s (CPU spill 38%)
  - `qwen2.5-coder:14b-instruct-q2_K` (5.8 GB, digest `dfeff73b234d`, installato 2026-04-20) — **sweet-spot agentic: 18.7 tok/s, faithful constraint-respect**, vedi `docs/adr/0007-aider-qwen-quantization-findings.md`
  - `qwen3-coder:30b` (Q4_K_M, 18 GB, digest `06c1097efce0`, MoE 30.5B/3B-active, 256K ctx, installato 2026-04-21) — **tier 2 escalation behavior-critical**: 23.3 tok/s @ ctx 8192. Resolve anti-pattern R1 dove 14B Q2 safe-fails. Vedi `docs/adr/0009-upgrade-strategy.md` addendum 2026-04-21. **Nota RAM tight (1.3 GB free) originale RIMOSSA 2026-04-22**: dopo upgrade a 64GB il modello ha ~40GB headroom in caricamento — promosso da tier 2 borderline a tier 2 stabile, vedi `docs/adr/0012-ram-upgrade-64gb-impact.md`
  - `gemma4:latest` (Q4_K_M, 9.6 GB disk / 10 GB loaded, digest `c6eb396dbd59`, 8.0B params, ctx 128K nativo, installato 2026-04-22) — **tier multimodal dedicato**: unico modello locale con vision + audio + tools + thinking (Apache 2.0). Speed: 39.26 tok/s @ ctx 8192 (GPU 32%, CPU spill 68% per overhead multimodal adapter). **NON coder-specialist**: per task coding continuare Qwen (7B/14B Q2/30B MoE). Usare Gemma 4 solo per screenshot/diagram OCR, audio dictation, o dogfood thinking-mode comparativo. Vedi `docs/research/bench-post-ram-upgrade-2026-04-22.md`
  - `deepseek-r1:8b` (Q4_K_M, 5.2 GB disk / 6.0 GB loaded, digest `6995872bfe4c`, 8.2B params, architecture qwen3 + R1 distillation, ctx 128K nativo, installato 2026-04-22) — **tier reasoning locale**: 74.57 tok/s @ ctx 8192 **100% GPU full-fit** (unico 8B locale full-VRAM), 47.46 @ ctx 16384. Thinking mode R1-distilled per chain-of-thought esteso. Usare per task reasoning/debug logica, NON coder-specialist (Qwen domina per coding). Vedi `docs/research/bench-post-ram-upgrade-2026-04-22.md`
  - `gpt-oss:120b` (MXFP4, 65 GB disk, digest `a951a23b46a1`, **116.8B params**, ctx 128K, installato 2026-04-22) — **NON viable locale**: runtime richiede ~70 GB RAM > 63 GB totali. Via Cerebras catalog free tier bloccato (paid-only). Tenuto su disco come reference per future upgrade RAM (96/128 GB) o paid cloud access. Bench non eseguito per safety OOM.
  - `qwen2.5-coder:32b` (Q4_K_M, 19 GB, digest `b92d6a0bd47e`, dense 32B, installato 2026-04-22) — **SCARTATO tier routing**: bench 3.65 tok/s @ ctx 8192 (ADR-0012 addendum), 8.4× più lento di qwen3-coder:30b MoE. Reference only per comparison dense vs MoE.
  - **Modelli aggiuntivi** (installati ~2 settimane fa per esplorazione, non bench-coperti codemasterdd, non in tier routing primario): `qwen3:8b` (5.2 GB, fallback chain Dafne tier 1), `qwen3.5:latest` (6.6 GB), `qwen3.6:latest` (23 GB), `qwen2.5:32b-instruct-q4_K_M` (19 GB, NON coder-specialist), `phi4:14b` (9.1 GB), `deepseek-r1:14b` (9.0 GB, scaling-up della 8b), `mistral:latest` (4.4 GB), `nomic-embed-text:latest` (274 MB, embedding utility). Bench/ADR opzionale post-Max se emergono use case concreti. Verifica presence: `ollama list`.
- Aider 0.86.2 (installato 2026-04-20 via `python -m pip install aider-install && aider-install`, binary `C:\Users\edusc\.local\bin\aider.exe`) — **client agentic consigliato per workflow sovereign**
- VSCode Cline extension `saoudrizwan.claude-dev` v3.79.0 (installata 2026-04-20) — **NOT viable come agentic con Qwen 7B**, vedi `docs/adr/0006-cline-qwen-viability.md`
- **repomix v1.14.0** (installato 2026-05-12 via `npm install -g repomix`, binary `C:\Users\edusc\AppData\Roaming\npm\repomix.cmd`) — **AI-ingestible repo pack** per handoff cross-session. Use case: pack repo subset (`--include "<pattern>"`) in singolo file con metadata (token count + security scan). M13 Wave 2026-05-12 INSTALL DONE post gh API verify (24609 stars MIT 2026-05-11). Smoke test PASS: `docs/sessions/** + docs/aa01-handoff/**` -> 41886 bytes 12.160 tokens "No suspicious files detected".
- **superpowers v5.1.0** plugin Claude Code (installato 2026-05-12 via `claude plugin install superpowers@claude-plugins-official`, cache `C:\Users\edusc\.claude\plugins\cache\claude-plugins-official\superpowers\5.1.0\`) — **agentic skills framework + methodology completa** (14 skills: brainstorming + writing-plans + executing-plans + subagent-driven-development + dispatching-parallel-agents + TDD + systematic-debugging + verification-before-completion + using-git-worktrees + requesting/receiving-code-review + finishing-a-development-branch + writing-skills + using-superpowers). M11 #3 obra/superpowers re-decision DORMANT -> INSTALLED post Archon CALIBRATE 7-step + falsifying experiment 5/5 PASS (install + verify + disable rollback + re-enable + cache structure). Repo 186664 stars MIT 2026-05-12, official Anthropic marketplace `anthropics/claude-plugins-official`. NO conflict identified vs codemasterdd CLAUDE.md autonomous execution + caveman mode + ADR-0026 cognitive workflow protocols (verification-before-completion ALLINEA Protocol 1 refresh-verify).
- **claude-mem v13.2.0** plugin Claude Code (installato 2026-05-12 via `claude plugin install claude-mem@thedotmack`, cache `C:\Users\edusc\.claude\plugins\cache\thedotmack\claude-mem\13.2.0\`) — **persistent memory compression system cross-session** (6 lifecycle hooks: Setup + SessionStart + UserPromptSubmit + PreToolUse + PostToolUse + Stop). Apache-2.0 74880 stars. M12 INSTALLED post Archon CALIBRATE PIVOT (3 blocker auto-resolved): (a) Bun v1.3.13 installed pre-req, (b) hook collision NO conflict empirical (plugin scope vs project scope codemasterdd .claude/settings.json separato, parallel merge SessionStart), (c) privacy SAME-TIER come Claude Code attuale (claude-agent-sdk = official Anthropic SDK, NON new data exposure). Worker service Bun port 37700+(uid%100) + SQLite `~/.claude-mem/` + Chroma vector DB. Reversibility test PASS (disable/enable cycle clean).
- **Bun v1.3.13** (installato 2026-05-12 via `irm bun.sh/install.ps1 | iex`, binary `C:\Users\edusc\.bun\bin\bun.exe`) — runtime JavaScript/TypeScript fast (alternative Node.js). Pre-req per claude-mem worker service. ALL future tools che richiedono Bun engines.
- **opencode-with-claude v1.6.11** plugin OpenCode (installato 2026-05-15 via `npm install -g opencode-with-claude`, registrato in `~/.config/opencode/opencode.json` plugin[] + provider.anthropic baseURL http://127.0.0.1:3456) — **Meridian bridge per Pro subscription Hybrid A1** (ADR-0030). Senza Pro attivo il bridge non auth, ma config preparato. Reversibile via `npm uninstall -g opencode-with-claude` + remove entries opencode.json.
- **Gemini CLI v0.42.0** (installato 2026-05-15 via `npm install -g @google/gemini-cli`, binary `~/AppData/Roaming/npm/gemini.ps1`) — tier 3 cloud free 1M context. Auth via `GEMINI_API_KEY` env var (path API key, no OAuth needed). `GEMINI_CLI_TRUST_WORKSPACE=true` user-scope persistent settato. Quota: 60 req/min via API key path OR 1000 req/day via OAuth path post `gemini auth login` browser interactive.
- **notebooklm-py v0.4.1** (installato 2026-05-15 via `pip install --user notebooklm-py[browser]`, binary `~/AppData/Roaming/Python/Python312/Scripts/notebooklm.exe`) + **notebooklm-mcp-cli v0.6.9** (installato via `uv tool install notebooklm-mcp-cli`, binari `~/.local/bin/nlm.exe` + `notebooklm-mcp.exe`) — **NotebookLM programmatic access** via personal Google OAuth Playwright. Capacità unlocked vs web UI: create/ask/source-add/generate (audio/video/quiz/flashcards/slide-deck/infographic/mind-map/data-table)/download. Auth pending Eduardo `notebooklm login` browser. Unofficial wrapper Apache-compatible (13.2k + 4.4k stars MIT, undocumented Google API ToS gray, mitigation: pin version + web UI fallback always available).
- **Playwright chromium v1.59.0** + **chromium-1217 cached** (`~/AppData/Local/ms-playwright/`) — browser engine richiesto da notebooklm-py per OAuth flow.
- **faster-whisper** (CTranslate2) + **GPU enable** `nvidia-cublas-cu12` + `nvidia-cudnn-cu12` + `nvidia-cuda-nvrtc-cu12` (installati 2026-05-21 via `pip install --user`, Ryzen) — **sovereign-local audio transcription** nello stack (future: voice memo, meeting, video, podcast). Wrapper canonico `scripts/whisper_transcribe.py` (auto-aggiunge nvidia wheel DLL-dir via `os.add_dll_directory` + PATH; GPU CUDA con fallback CPU; `--model large-v3` default IT-multilingue). **QG Step-1 smoke PASS 2026-05-21**: GPU device=cuda 0.5s su .wav reale, lang=it 0.99, output UTF-8 corretto. **GPU gotcha Windows**: CTranslate2 cerca `cublas64_12.dll`/cuDNN su PATH -> i nvidia wheel li forniscono in `site-packages/nvidia/*/bin`, il wrapper li registra a runtime (CUDA toolkit system NON necessario). Uso: `python scripts/whisper_transcribe.py <file|dir> [--model] [--lang it]` -> .txt sidecar. NON usato per ChatGPT-export 2026-05-13 (voce gia trascritta da OpenAI `audio_transcription` nell'export = whisper ridondante li; tool tenuto per audio futuro NON-pre-trascritto).

## Stack da installare questa settimana
_(completato il 2026-04-19 — vedi "Stack installato")_

## Stack da installare settimana prossima (quando migriamo progetti)
- Dipendenze specifiche progetti (da Evo-Tactics e Synesthesia)
- Eventuali MCP server (filesystem, github) se emergono bisogni reali

## Progetti monitorati (status 2026-05-08)

- **Evo-Tactics (Game)** — co-op tactical game d20, monorepo Node+Python (Vue3 bundle)
  - GitHub: `github.com/MasterDD-L34D/Game`
  - Path Lenovo: `C:\dev\Game`
  - **Path Ryzen**: `C:\dev\Game` (consolidato da `C:\Users\VGit\Desktop\Game` via OD-049 2026-05-19; move path-only, git-state invariato, 5 worktree repaired) -- **STALE sandbox** (HEAD `5d27fc50` PR #2139 OLDER, 107 commits BEHIND origin/main, working tree dirty apps/backend/* deletions). Claim originale PR #69 "Ryzen AHEAD" era **narrative drift L-2026-05-002 case-study** corretto via P1 Refresh-verify 2026-05-13 notte (ADR-0027). Origin = canonical de-facto, Lenovo = synced primary client. BACKLOG cleanup candidate (low priority).
  - Stack: Node 22 + Python 3.10, xstate@5, inkjs, Vue3 bundle
  - Compat runtime: Node 24 system-level (validato n=710+ test)
  - **Status 2026-05-08**: **Sprint Impronta Ondata 1 in pausa dal 26/04** (HEAD `5f42757a` invariato 12:53 CET, CAP-15 imprint phase V2). 8+ commit clusterati 25-26/04 driven da AA01 silent-driver mode (CAP-11 biome-resolution, CAP-12 player telemetry, CAP-13 imprint mockup + UX patch, CAP-14 onboarding v2, CAP-15 imprint V2). PR aperto: **#2108 swarm-distillation run #5** (branch `claude/swarm-distillation-2026-05-08`, Claude Code session 7/5 22:19 UTC, da triagare). PR #97 Game-Database CLOSED stale 7/5.
  - **Integration con Dafne swarm**: repo target. Pipeline `docs/pipeline-swarm-to-game.md`. Hook commit-msg globale applicato.

- **Evo-Tactics Godot v2 (Game-Godot-v2)** — Godot 4.x port di Evo-Tactics, **pivot 2026-04-29**
  - GitHub: `github.com/MasterDD-L34D/Game-Godot-v2`
  - Path Lenovo: `C:\dev\Game-Godot-v2\` (cloned 2026-05-07, 20.7 MB)
  - Stack: Godot 4.x (engine native, GDScript), 200 test file GUT (~1719 test asserts), addons + scenes + scripts + tests + tools
  - **Status 2026-05-08**: **215 PR mergeati totali** (+4 dal 7/5 sera, dettaglio non triagato in codemasterdd -- governance interna autosufficiente). 5 PR documentati cross-repo del 7/5 sera: #207 phone composer + #208 AiProgressMeter HUD + #209 gdlint cleanup CI + #210 PassiveStatusApplier + #211 MissionTimer. Path A canonical CHIUSO end-to-end + Sprint AC bundle 15 sub-sprint chiuso. 0 PR open ora.
  - **Governance interna autosufficiente**: repo ha `CLAUDE.md` proprio (con `caveman mode` + Path A status detail) + `AGENTS.md` proprio per Codex (multi-client pattern adottato indipendentemente, **conferma ADR-0021 con uso reale**) + `.claude/SAFE_CHANGES.md` + `.claude/TASK_PROTOCOL.md`. Codemasterdd NON sovrascrive — monitora solo.
  - **Hook globali codemasterdd**: applicati automaticamente via `core.hooksPath` user-level. Conventional Commits + silent-fail Layer 2 ADR-0020 attivi su Game-Godot-v2 senza setup repo-specific.
  - **Relazione con Game (Vue3)**: parallel-run during port phase. Vue3 mantiene Sprint Impronta gameplay (logica + telemetria + onboarding CAP-11..15); Godot v2 ricostruisce shell visuale + UX + canonical engine. Long-term: Godot v2 frontend canonical, Vue3 archive (decisione futura, NON ancora ADR).

- **Game-Database** — Taxonomy CMS per Evo-Tactics (promoted da Ryzen-only minimal monitoring 2026-05-15 sera, post Jules audit L-025)
  - GitHub: `github.com/MasterDD-L34D/Game-Database` (PUBLIC, no LICENSE)
  - Path Ryzen: `C:\dev\Game-Database` (consolidato in C:\dev 2026-05-21; era `C:/Users/VGit/Documents/GitHub/Game-Database/`. Clone attivo Ryzen-side, NON remote-only -- aggiornamento drift-fix path)
  - Path Lenovo: `C:\dev\Game-Database` (clone presente verificato 2026-05-28 sera post pull-pass cross-fleet; +50 commit pulled clean. Claim originale "no clone Lenovo current" era stale, anti-pattern #19 corretto 2026-05-28)
  - Stack: Express 4 + Prisma 5 + PostgreSQL 16 + React (MUI + TanStack Table + i18n + Vite)
  - **Ruolo**: glossary canonical trait/biome/specie/ecosistemi per Evo-Tactics. Upstream content provider per Game (Vue3) via `npm run evo:import` + HTTP runtime API (`GAME_DATABASE_ENABLED=true` flag su Game backend, ADR-2026-04-14 game-side)
  - **Status 2026-05-15 sera**: HEAD main `91f5468` PR #105 + 7 PR Jules OPEN today (#107..#113: 1 security basicAuth + 2 perf optimize + 3 tests coverage + 1 refactor code health) -> Jules e' aggressive maintenance/improvement source su questo repo (7 sessioni cumulative cross-day, il repo con piu' attivita Jules nell'ecosystem)
  - **Governance interna autosufficiente**: ha `CLAUDE.md` proprio (multi-client ADR-0021) + `WORKSPACE_MAP.md`. Codemasterdd NON sovrascrive, monitora soltanto.
  - **Hook globali**: applicati via `core.hooksPath` user-level (Conventional Commits + ADR-0020 silent-fail check) se Eduardo clone locale Lenovo
  - **Privacy**: PUBLIC + cloud-OK come Game / Game-Godot-v2. NON in `~/.config/aider-privacy-whitelist.txt` perche' no clone locale current; aggiungere se cloning futuro
  - **Stack ADR-0021 multi-client pattern**: Jules + Codex Cloud + Claude Code (multi-AI pipeline empirico, L-024 case study)

- **evo-tactics-refs-meta** — pipeline asset reference Evo-Tactics (added monitoring 2026-05-18, gap reale mappa ecosistema)
  - GitHub: `github.com/MasterDD-L34D/evo-tactics-refs-meta` (PRIVATE)
  - Path: nessun clone (remote-only, scope-monitorable da gh API)
  - Stack: Python (download tooling) + manifest JSON + URL lists. NO binari versionati
  - **Ruolo**: meta-backup asset reference (3D/2D/concept art, SFX, SKIV creature refs). Rebuildable via `robust_download.py` + `urls-*.txt` + `gen_manifest.py`. Conformita licenze CC0/PD/Sonniss (provenance `CC0_SOURCES.md`)
  - **Connessione gioco**: asset finali -> `C:\dev\Game\assets\` via output-staging
  - **Status 2026-05-18**: idle (last push 2026-04-29), layer asset legittimo non daily-ship. Minimal informational monitoring (snapshot on-demand, no piano operativo cross-repo)
  - **Privacy**: PRIVATE, sovereign-default (NON cloud-whitelisted finche no clone locale)
  - **Dettaglio completo**: `docs/EVO_TACTICS_ECOSYSTEM_GUIDE.md` sezione 4 + `STATUS_MULTI_REPO.md` §7b

- **Synesthesia** — web app esame UniUPO
  - GitHub: `github.com/MasterDD-L34D/synesthesia`
  - Path Lenovo: `C:\dev\synesthesia` (dormant per Sprint plan UniUPO esame ~ago 2026)
  - **Path Ryzen**: `C:\dev\synesthesia` (consolidato in C:\dev 2026-05-21; era `C:\Users\VGit\Desktop\repos\synesthesia`. HEAD `05f8a92` Batch D /about + image zoom + notification — discovered 2026-05-12). Dormant Sprint-track (UniUPO ago 2026); Ryzen-side personal-work attivo. Coexistence non oxymoronic: dormancy è scope-level codemasterdd governance, NON ban totale Eduardo. Clarify SPRINT_02.
  - Stack: Node 20 ESM, Express, EJS, SQLite, Passport
  - Status: MVP funzionante
  - Privacy policy per-repo: `controllers/`/`routes/`/`middlewares/` sovereign-only; `views/`/`public/` cloud OK

- **Dafne swarm (evo-swarm)** — orchestratore AI agentic per Evo-Tactics, multi-agent sistema custom
  - GitHub: `github.com/MasterDD-L34D/evo-swarm`
  - Path Lenovo: `C:\Users\edusc\Dafne\workspace\swarm` (repo git separato, NOT in `C:\dev\`)
  - Path Ryzen: `C:\dev\evo-swarm` (clone Ryzen-side, verificato 2026-05-21; branch attivo `dafne/portability-fix`)
  - Home Dafne: `C:\Users\edusc\Dafne\` (start-dafne.cmd + agent/ config + desktop shortcut)
  - Stack: Python 3.12 + Flask + Ollama (qwen3:8b governance + nomic-embed-text per H5 gate)
  - Status 2026-04-24 notte: Atto 1 day-3/10. Server Flask UP idle su `:5000` per day-5 (26/04). 20 commit pushati. 11 agent runtime. Pilastro 2 evoluzione 🔴→🟡 (6 lezioni empirical).
  - **Scopo**: coordinatrice + memory keeper che governa specialist (lore-designer, trait-curator, balancer, ecc.) per produrre content integrabile in repo `Game`.
  - **Integration col Game repo**: scrive su `C:\dev\Game\agents/` quando Eduardo approva nuovi agent via `POST /api/dafne/approve-agent`. H5 gate autonomous blocca pattern loop.
  - **Governance framework-archivio adottato**: 5 file root-level (PROJECT_BRIEF, DECISIONS_LOG, BACKLOG, OPEN_DECISIONS, MODEL_ROUTING) + mapping selettivo. Decisione 006 in DECISIONS_LOG swarm.
  - **Open items**: OD-003 Groq key 403, OD-004 dashboard usage, OD-005 Tavily (tutti non bloccanti). BACKLOG L7 CAMEL integration deferred a Atto 2.
  - **Avvio**: `cd C:\Users\edusc\Dafne\workspace\swarm && .\START-SWARM.ps1` → dashboard `http://localhost:5000`
  - **Dettaglio completo**: memoria `reference_dafne_swarm.md` + `CAMEL-INTEGRATION.md` nel repo swarm

- **Vault (vault-shared)** — knowledge management LLM-wiki personale Eduardo, **sibling-peer monitored** (added 2026-05-10; **origin lineage reframe 2026-05-12: Ryzen è la fonte originale, Lenovo è clone downstream**)
  - GitHub: `github.com/MasterDD-L34D/vault`
  - **Origin Ryzen**: `C:\dev\vault` (consolidato in C:\dev 2026-05-21; era `C:\Users\VGit\Vault\`. clone originario, creato Ryzen-side; user Vgit; sync via origin/main)
  - Path Lenovo (clone downstream): `C:\dev\vault\` (rinominato da `C:\dev\vault-shared\` 2026-05-21; backup pre-reconcile `C:\dev\_vault-shared-prereconcile-2026-05-17`)
  - **Vault-ops Python tooling layer** (ingest/normalize/tune scripts + 3 SQLite DBs `qmd.db`/`qmd-v2.db`/`vault-search.db` + venv): **EXISTS ONLY Ryzen-side** in `C:\Users\VGit\Vault-ops\`. NON replicato Lenovo (operational tooling Ryzen-bound).
  - Sync state 2026-05-12 sera: entrambi cloni a HEAD `67c3bb28` (M14 Cards wave), ahead/behind origin `0/0`. Push claim "deferred Eduardo-direct" in memory `project_vault_shared.md` linea 18 era OBSOLETE — push avvenuto, drift fixato 2026-05-12.
  - Stack: Karpathy LLM-wiki + ACCESS structure (Atlas/Cards/Sources/Spaces) + 7 production agent (Quality Gate workflow smoke->draft->production 3-gate) + Ollama LAN (Qwen + deepseek-r1) + Claude variants
  - Status 2026-05-10: **7/7 PRODUCTION milestone hit** (vault-linter v2 nested-YAML FP 0%, design-watcher v2 deepseek-r1 recall +33pp, ollama-dispatcher v1 -91% wall claim methodology TBR). 15+ commit 30gg. LLM routing matrix v1.0 path `Extras/config/llm-routing.json`. **DRIFT CONFIRMED 2026-05-12 sera empirical SSH read-only**: file hardcodes `http://192.168.1.121:11434` (1 occurrence vs reale **`.10`** Lenovo Ollama post DHCP reservation 2026-05-13). Ryzen-side dispatch verso Lenovo Ollama fallirebbe se invocato. Fix vault-side Eduardo-direct (sibling-peer NO-WRITE da codemasterdd) — BACKLOG R5.
  - **Privacy**: sovereign-only (NON in `~/.config/aider-privacy-whitelist.txt`). Contiene UniUPO esame + GDR campagne curated + GPT-Prompts library + Dev/Synesthesia academic + Dev/Evo-Tactics design notes.
  - **Relazione codemasterdd**: sibling-peer disjoint scope. Cross-pattern reference one-way: vault llm-routing matrix v1.0 -> potential MODEL_ROUTING.md addendum (methodology Quality Gate Step 2 con split metrics + keep_alive + retries + output validation).
  - **Hook globali**: compat VALIDATED 2026-05-10 (empty commit test PASS, reverted post-test). Vault `core.hooksPath` punta a `C:/Users/edusc/.local/share/git-hooks`.
  - **Boundary** (amended 2026-05-16 post OD-033): codemasterdd **PUÒ push feature-branch + creare PR** su vault-shared (es. `claude/<topic>` branch). **MAI direct-main push. MAI merge** — Eduardo media il merge via PR review (personal workflow, oversight gate mantenuto). Local commit + branch push + PR-create OK automatici; merge è Eduardo-only. Vault-shared self-governs il merge. Razionale amend: recovery/ingest operations autorizzate (es. OD-033 ChatGPT Business) generano branch+PR innocui+reversibili; il SPOF oversight resta sul merge-gate, non sul branch-push. Pre-amend policy ("codemasterdd NON scrive") era over-strict per casi recovery espliciti.
  - **Dettaglio completo**: memoria `project_vault_shared.md` + sezione 6 in `STATUS_MULTI_REPO.md`

### Relazioni inter-repo

**Monitored ecosystem** (codemasterdd policy + write-path o monitoring SLA):

```
codemasterdd-ai-station (policy + infrastruttura)
       │
       ├─── Evo-Tactics Vue3 (C:\dev\Game) ── Sprint Impronta active (CAP-11..15)
       │         ↑                   │
       │         │ swarm produce     │ AA01 capability driving
       │         │                   ↓
       │         │            ┌── Evo-Tactics Godot v2 (REMOTE-ONLY)
       │         │            │     pivot 2026-04-29, parallel-run port
       │         │            │
       └─── Dafne swarm (C:\Users\edusc\Dafne\workspace\swarm)
                 ↑
                 │ governance + pilastri + metriche empirical
                 │ (Atto 2 day 14+ active)
```

**Sibling-peer disjoint** (sovereign-only, branch+PR write-path OK / merge Eduardo-only, cross-reference one-way):

```
vault-shared (C:\dev\vault)
       │ Knowledge management LLM-wiki Karpathy + 7 production agents
       │ Stack overlap: Ollama LAN + Qwen + deepseek-r1 + Claude variants
       │ Cross-pattern reference one-way -> codemasterdd MODEL_ROUTING addendum
       │ Privacy: sovereign-only (UniUPO + GDR + GPT-Prompts + Dev notes)
       │ Hook globali: compatibili (validated 2026-05-10)
       │ Boundary (amended 2026-05-16): branch+PR push OK codemasterdd, merge Eduardo-only
       │ Eduardo media il MERGE-gate (oversight), non il branch-push
```

### Monitoring cross-repo (sessione 2026-04-24)

Nessuno dei 3 repo ha CI integration. Monitoring manuale:
- Review settimana 2 Fase 6 (codemasterdd): fatto 2026-04-24 anticipata, on-track
- Validation run swarm (6 cicli): 100% success rate, pattern Dafne gated
- Game repo: branch swarm/register-agents-2026-04-24 pending PR
- Evo-Tactics status own: `d319404e` M11 Phase B→TKT-05 close (pre-swarm integration)

## Lingua
- Comunicazione con utente: italiano
- Codice, identifier, commit message: inglese
- Documentazione progetto: italiano

## Convenzioni operative

### Esecuzione comandi
- Un comando alla volta, spiegazione prima
- Approvazione esplicita per azioni non banali
- No operazioni multiple concatenate

### Modifiche file
- Mostrare contenuto prima di creare/modificare
- Preferire Edit a Write per file esistenti

### Git
- Conventional Commits (feat:, fix:, chore:, docs:, refactor:, test:)
- No --force su main, no --no-verify
- Branch principale: main

### Logging e backup
- logs/ (gitignored)
- backup/ per config sensibili (gitignored)
- .env (gitignored, template in .env.example)

### Encoding e charset (ADR-0021)
- Nuovi file `.md` creati da agent (Codex, Aider, Claude Code) → **ASCII-first** per body prose
- Consentiti: emoji status (⚠️ ✅ 🔴), simboli matematici (≥, ≤, →) se semanticamente rilevanti
- **Evitare** in body nuovi doc: em-dash `—`, middot `·`, smart quotes `'` `'` `"` `"` → usare `--`, `|`, `'`, `"`
- **Eccezione convention progetto**: titoli ADR (`# ADR-NNNN — Title`) e header sintetici mantengono em-dash per coerenza con i 20+ ADR esistenti. La policy ASCII si applica al body prose, non al template title.
- File legacy con mojibake (`Ã`, `â€”`): **frozen**, no global rewrite cieco. Fix mirato solo se file attivamente confusing per task corrente.
- Razionale: ridurre artifact cross-tool (Windows shell, Codex Cloud sandbox, Aider whole/diff format)

## Struttura repository (evoluta 2026-04-24 post ADR-0017 scaffolding)
```
codemasterdd-ai-station/
├── scripts/          # setup, maintenance, backup, quality-bench
├── docs/             # documentazione tecnica, procedure, ADR (17+)
├── logs/             # log esecuzione (gitignored)
├── backup/           # backup config, registry (gitignored)
├── infra/            # docker-compose + LiteLLM config + Langfuse (ADR-0017)
├── apps/             # mini-app UI (dogfood-ui Flask) (ADR-0017)
├── .claude/agents/   # 5 sub-agent Claude Code (dogfood-analyst, bench-reporter, cost-monitor, repo-health-auditor, adr-drafter)
├── Archivio_Libreria_Operativa_Progetti/  # framework archivio multi-progetto
├── 11+ file governance root-level (PROJECT_BRIEF, COMPACT_CONTEXT, DECISIONS_LOG, BACKLOG, ...)
├── STATUS_MULTI_REPO.md  # dashboard operativa cross-repo
├── README.md
├── JOURNAL.md
├── CLAUDE.md
└── .gitignore
```

## Scopo repository
`codemasterdd-ai-station` è **infrastructure-as-code + observability stack self-hosted + UI glue minimale** (scope evoluto post ADR-0017 Proposed 2026-04-24):
- Gestione setup, manutenzione, backup
- Procedure ripetibili + config stack osservabilità
- Documentazione decisioni architetturali (17+ ADR)
- Knowledge base personale + dashboard operativa cross-repo
- Log sessioni + tracking strutturato Fase 6 dogfood
- UI glue per tier routing + dogfood tracking + bench viewer (`apps/dogfood-ui/`)

**NON contiene codice di progetti reali Game/Synesthesia** (vivono in repo separati). Le "apps/" root-level sono mini-strumenti operativi per questo repo stesso (dashboard, Aider wrapper, bench viewer), non gioco né prodotto esterno.

## Priorità modelli AI
- **Durante Claude Max (~fino 17/06/2026, ri-acquistato +1mo 2026-05-17 — vedi roadmap AGGIORNAMENTO)**: Opus 4.7 per tutto
- **Tier 0 strategic post-Max (~2026-06-17+, deadline aggiornata)** — ADR-0023 Proposed 2026-05-09 (vedi §Addendum 2026-05-18):
  - Strategic = NON-delegabile (multi-file refactor ≥3 file, debug architetturale, ADR draft, synthesis cross-source, constraint ≥5 strict). Vedi ADR-0008 per rationale.
  - **Default**: Claude API pay-per-use on-demand con budget cap mensile $10-20, tracciato in ccusage. Eduardo autorizza spend esplicitamente per task strategic complesso, poi torna sovereign.
  - **Setup**: `ANTHROPIC_API_KEY` in `~/.config/api-keys/keys.env` (verificare presenza, eventualmente generare via Anthropic Console)
  - **Tracking**: `logs/claude-api-spend-2026-MM.md` (gitignored) entry per sessione (data, task, token, cost, outcome)
  - **Trigger reactivation Pro**: utilizzo cumulative >$20/mese per 2 mesi consecutivi → ratification ADR-0023 addendum revisita Scenario A vs B
  - **Costo stimato**: $5-15/mese in working assumption (1-3 task strategic complessi/mese)
  - Riferimento: `docs/adr/0023-strategic-tier-post-max-api-on-demand.md`
- **Post Max** — task-routing (vedi ADR-0008 per rationale completo):
  - Query one-shot → `ollama run qwen2.5-coder:7b` (114 tok/s)
  - Read/explain + CREATE single file → Aider + Qwen 7B + `whole`
  - **Cosmetic edit** (JSDoc, docstrings, rename, lint-fix) → **Aider + Qwen 7B + `whole`** (format compatibile, faithfulness non critica). **CAVEAT 2026-05-07**: pattern wrong-target-file su file in subdir + docstring self-referenziato (vedi `docs/patterns/aider-wrong-target-file.md`). Mitigation: usare `aider-refactor` (diff format) anche per cosmetic se file in subdir profonde con docstring header che cita filename.
  - **Behavior-critical edit** (refactor, bug fix, logic change) → **Aider + Qwen 14B Q2_K + `--edit-format diff`** (safe failure; ~20-40% retry manuale ma zero silent-corruption). **Default safer anche per cosmetic** se file in subdir + docstring self-ref (vedi caveat sopra).
  - **Behavior-critical escalation** (quando 14B Q2 safe-fails, es. task R1-type 1-line value change) → **Aider + qwen3-coder:30b + diff** (MoE 30B-A3B, tier 2 fallback prima di Claude Pro; speed 2× slower + RAM tight ma risolve anti-pattern — vedi ADR-0009 addendum)
  - Multi-file refactor / debug strategico → **Claude API on-demand** (tier 0 ADR-0023 sopra) o OpenRouter pay-per-use (alternativa)
  - **⚠️ DEPRECATO**: Aider + 14B Q2 + `whole` — silent-corruption deterministico su task "edit single file" semplici, vedi ADR-0008
  - Riferimenti decisionali: `docs/adr/0007-aider-qwen-quantization-findings.md` + `docs/adr/0008-aider-whole-format-silent-corruption.md`
  - **Seconda dimensione routing (in review)**: `docs/adr/0016-constraint-count-routing-dimension.md` (Proposed 2026-04-24). Estende matrice classe-based con **constraint-count**: 1 qualsiasi tier / 2-3 additive+preserve → 14B Q2 local o 70B cloud / 2 fix+transform → downgrade 14B Q2 (7B skippa transform) / **5+ strict → manual Claude Code**. Consultare per task con ≥3 constraint espliciti nel prompt. Status Accepted trigger: n≥3 data points addizionali.

- **OpenCode tier (multi-step agentic, distinto da Aider)** — ADR-0022 Accepted 2026-05-09:
  - **Default sovereign**: `opencode run --model "ollama/qwen3-coder:30b"` — MoE A3B tool-use native, validato 3/3 (smoke read + 2 dogfood edit reali #25-#26 PASS 1st-try)
  - **NON usare con OpenCode**:
    - Qwen 2.5 Coder family (7B + 14B Q2): emette tool call come JSON raw stringificato in stdout (NON eseguito da OpenCode `run`). Sweet spot Aider non si trasferisce.
    - Cloud free tier 8B-70B (Groq llama-3.3-70b TPM 12k / llama-3.1-8b-instant TPM 6k / Cerebras llama3.1-8b context 8k / Cerebras llama3.3-70b paid-only): tutti rate-limited o context-limited vs OpenCode default request ~50k token.
  - **Cloud paid emergency**: `openai/gpt-4o-mini` (tier 4, monitorare ccusage)
  - **Quando usare OpenCode vs Aider**:
    - **Aider** (single-file edit, constraint-respect, faithful diff): cosmetic / behavior-critical su 1 file con vincoli espliciti
    - **OpenCode** (multi-step agentic con tool calls coordinati): task che richiedono Read+Edit+Bash+ListFiles, multi-file refactor con tool orchestration, MCP server integration, GitHub agent
  - Riferimenti decisionali: `docs/adr/0022-opencode-tooluse-model-routing.md` (Accepted) + `logs/aider-delegation-2026-05.md` (gitignored, entries #16-#26)

- **Safety protocol per Aider** (valido sempre):
  - `git diff HEAD~1` post-edit prima di pushare: commit message generati dall'LLM riflettono l'intent, non necessariamente il diff reale
  - Evitare `--yes-always` in repo con working tree sporco
  - Per task behavior-critical considerare `--no-auto-commits`
  - Guard rail chain (`git config --global core.hooksPath C:/Users/edusc/.local/share/git-hooks`):
    1. `commit-msg` globale — valida Conventional Commits cross-agent (tutti gli agent inclusi Aider). ADR-0011.
    2. `pre-commit` globale — blocca silent-corruption pattern (ADR-0008) **+ silent-fail Python patterns** (bare `except:`, silent except+pass; ADR-0020). Bypass marker: `# silent-ok` o `# noqa: silent-fail`.
    3. Husky repo-local (solo Evo-Tactics) — skip-worktree wrapper.
    4. Claude Code PreToolUse `scripts/hooks/commit-guard.js` — fail-fast in sessione Claude Code (duplicato di 1 per feedback veloce).
  - Bypass guard rail con `git commit --no-verify`, non raccomandato

- **Wrapper CLI per delegazione** (canonical repo `scripts/wrappers/`, installed user-side `C:\Users\edusc\.local\bin\` via `scripts/setup/install-wrappers.ps1` idempotente -- harsh-reviewer P1 #4 fix 2026-05-13):
  - **Aider locali (tier 1-2 sovereign)**:
    - `aider-cosmetic <file>` → 7B + **diff** + no-auto-commits (JSDoc, docstrings, rename, lint-fix) — **updated 2026-05-13 T1 SPRINT_02 entry #34**: switched whole→diff per position-precision PASS, added --no-auto-commits parity con aider-refactor
    - `aider-refactor <file>` → 14B Q2 + diff + no-auto-commits (refactor, bug fix, logic change) — 25 tok/s
  - **Aider cloud (tier 3-4, aggiunti 2026-04-23 combo F+D, vedi ADR-0013)**:
    - ~~`aider-groq`~~ **REMOVED 2026-05-13** post T1 #29+#35: LiteLLM-Groq adapter bug streaming hang (Issue #9296+#12660+#4804+#16040). File deleted user-side. Use `aider-groq-bypass` invece
    - `aider-groq-bypass <file>` → openai/llama-3.3-70b-versatile via `--openai-api-base https://api.groq.com/openai/v1` — **VIABLE 2026-05-13 T1 #36 PASS post P0 hardening**: bypass LiteLLM Groq adapter via OpenAI-compatible endpoint, ~30s latency vs 5min stuck (autoresearch L-2026-05-014 pattern). Groq TPM 300K (era 12K free tier, ora 300K post-Tier1). $0 free tier. **Security HARDENED**: GROQ_API_KEY via temp env-file pattern (NTFS-protected, NOT in argv) -- mitigation CWE-214 process arg list exposure (harsh-reviewer P0 #1)
    - `aider-cerebras <file>` → cerebras/llama3.1-8b + diff + no-auto-commits — 733 tok/s free tier — **VIABLE con `--map-tokens 0`** (T1 #31 PASS $0.0004/task)
    - `aider-gemini <file>` → gemini/gemini-2.5-flash + diff + no-auto-commits (attenzione thinking budget) — **VIABLE con `--map-tokens 0`** (T1 #32 PASS $0.008/task ~6min slow)
    - `aider-openai <file>` → openai/gpt-4o-mini + diff + no-auto-commits — **VIABLE post 10 EUR funding 2026-05-13** + Sharing data toggle ON = pool free 2.5M tok per day eligible (gpt-4o-mini in elenco). Hard limit consigliato $5/mese
  - **Aider cloud free Tier 3 add-on (aggiunti 2026-05-15 SPRINT_02 free LLM ecosystem audit, vedi `docs/operations/key-and-task-routing-matrix.md` + L-2026-05-022)**:
    - `aider-hf <file>` → openai/deepseek-ai/DeepSeek-R1:fastest via `--openai-api-base https://router.huggingface.co/v1` — **HuggingFace Inference Providers** unified proxy a 300+ models. Default DeepSeek R1 reasoning specialty. Alt models: openai/gpt-oss-120b, Qwen/Qwen2.5-Coder-32B-Instruct. Free tier 100K credit/mese. Pending Eduardo signup hf.co + token. Security: HUGGINGFACE_API_KEY via temp env-file (CWE-214 mitigation)
    - `aider-github-models <file>` → openai/gpt-4o via `--openai-api-base https://models.inference.ai.azure.com` — **GitHub Models** proprietary GPT-4o 150 req/giorno free. Alt: gpt-4o-mini, Llama-3.3-70B, Mistral-Large. PROPOSED 2026-05-15 pending Eduardo PAT generation (Models read-only). Real gap-fill (no other free tier integra gpt-4o real, solo gpt-oss-120b open weights via HF)
  - **L-2026-05-015 fix Option B applicato 2026-05-13**: tutti i wrapper hanno REM lines con parens rimosse per killare PowerShell `&` invocation pollution pattern. Vedi `~/aa01/learnings/L-2026-05-015-powershell-wrapper-rem-pollution.md` per dettaglio
  - **OpenCode (tier multi-step agentic, ADR-0022 Accepted 2026-05-09)**: in `C:\Users\edusc\AppData\Roaming\npm\opencode.ps1` (npm global v1.14.41):
    - `opencode run --model "ollama/qwen3-coder:30b" "<task>"` → tier 1 sovereign default (MoE A3B tool-use native)
    - Config: `~/.config/opencode/opencode.json` (5 provider mappati, env vars from `~/.config/api-keys/keys.env`)
    - **NON usare** Qwen 2.5 Coder family con OpenCode (raw JSON tool call non eseguito)
    - **NON viable** cloud free 8B-70B (rate-limited TPM o context vs request ~50k)
  - **Privacy guard rail tecnico (H8 ADR-0023, Accepted 2026-05-09)**:
    - Wrapper cloud (`aider-groq-bypass` / `aider-cerebras` / `aider-gemini` / `aider-openai` / `aider-hf` / `aider-github-models`) controllano automaticamente repo via `git rev-parse --show-toplevel` + whitelist `~/.config/aider-privacy-whitelist.txt`. Se repo non whitelisted → ABORT con error, no source code inviato a cloud.
    - **Repo whitelisted (cloud OK)**: codemasterdd-ai-station, Game (public), Game-Godot-v2 (public).
    - **Repo NON whitelisted (sovereign-only enforcement)**: Synesthesia (mixed privacy, controllers/ sensitive), repo cliente futuri.
    - Setup/verify: `scripts/setup/install-privacy-guard.ps1` (idempotente, rilanciabile).
    - Test logica: `scripts/setup/test-privacy-guard.cmd` (verifica whitelist hit/miss).
    - Template wrapper: `scripts/setup/aider-wrapper-template.txt`.
    - Bypass deliberato (es. workflow Synesthesia views/): aggiungere repo a whitelist temporaneamente, ripristinare post-task. Anti-pattern: commentare il check inline (perde guard rail).

- **Delegation protocol Claude Code → Aider**: vedi `docs/patterns/delegation-to-aider.md` — decision tree classification, formato handoff, review loop, tracking fail rate per Fase 6

- **Trigger delega in-session** (SEMPRE attivo, non solo post-Max — aggiunto 2026-04-22):
  - Prima di Edit/Write su file esistente, **classificare il task** e proporre delega se appropriato:
    - **cosmetic** (JSDoc, docstring, rename, lint-fix, typo, 1-liner batch) + working tree clean → proponi `aider-cosmetic <file>` con task short-description, attendi OK utente
    - **behavior-critical** (refactor singolo file, bug fix, logic change) → proponi `aider-refactor <file>`, attendi OK
    - **strategic** (multi-file, synthesis da conversazione, design, debug architetturale, ADR writing) → esegui direttamente senza proposta delega
  - **Task <1 riga meccanica**: skip proposta (overhead > savings)
  - **Batch operazioni simili ≥5**: proponi delega anche se singolarmente sub-threshold — trigger principale per savings
  - **Tracking**: ogni delega effettuata → entry in `logs/aider-delegation-YYYY-MM.md`. Task strategici eseguiti direttamente → tracciati solo se rilevanti per ratio statistica
  - **Anti-pattern**: default inerziale "faccio io direct" senza classification è un miss; ogni Edit/Write senza step di classification contraddice hub pattern ADR-0008

## Cognitive workflow protocols (ADR-0026 + addendum 2026-05-13)

Per audit / eval / decision / pivot significativo, applicare 6 cognitive workflow protocols (triple anchor: ADR-0026 + memory + questa sezione). Vedi `docs/adr/0026-cognitive-workflow-protocols.md` per dettaglio + caso studio + anti-pattern + Protocol 5 + 6 addendum 2026-05-13.

### Protocol 1 -- Refresh-verify state interno (PRE-action OBBLIGATORIO)

Prima di azione significativa, verifica state interno:
- AA01 workspace + decisions logs task correlati (`cd C:/Users/edusc/aa01 && bash scripts/status.sh`)
- Memory recente (`MEMORY.md` index + file rilevanti)
- ADR existing che coprono scope
- Git state + `gh pr list` repo monitored
- Filesystem check file promessi (es. template promessi ADR)

**Trigger**: ogni audit / eval / new ADR / strategic decision.
**Anti-pattern**: ereditare narrative da COMPACT/JOURNAL precedente senza re-verify (caso studio mio error 2026-05-11 ADR-0025 amend).
**Reference**: memory `feedback_governance_refresh_verify`.

### Protocol 2 -- Autoresearch multi-source (per audit / eval / research)

Multi-source parallel investigation + synthesis weighted (NON one-shot README). 8-step checklist in memory `feedback_autoresearch_default`. Weighting: **internal > external**, **empirical > documentation**, recent > old, multiple corroborate > single signal.

**Trigger**: ogni audit / eval / research significativa.
**Anti-pattern**: one-shot README fetch + verdict confidente.

### Protocol 3 -- Archon v2 7-step First Principles (high-stakes)

Per decisioni high-stakes (architectural lock-in irreversibile / pivot / abandonment), applicare Archon protocol: RESTATE + ENUMERATE + DECOMPOSE + CHALLENGE + RECONSTRUCT + RED-TEAM + CALIBRATE (verdict + confidence + falsifying experiment ~30s-5min PRE-commit).

**Trigger**: audit >=3 cicli verdict opposti / architectural irreversibile / "sono sicuro?" introspection.
**Anti-pattern**: skip Archon per decision time-sensitive sub-15min (over-engineered).
**Path AA01**: `C:/Users/edusc/aa01/archon/system/ARCHON_v2_{SYSTEM,BOOTSTRAP}.md`.
**Reference**: memory `reference_archon_protocol`.

### Protocol 4 -- AA01 workspace audit trail (workflow standard)

Per audit / eval / research / pivot >=30min effort + cross-session value, usare AA01 workflow standard:
1. Capture `inbox/<YYYY-MM-DD-slug>.md`
2. `bash scripts/classify.sh inbox/<file>`
3. `bash scripts/promote.sh inbox/<file> <preset>` (preset: research-long / code-sprint / design-iteration / idea-capture / code-long-alpha / code-maintenance)
4. DRAFT → PROPOSED → lesson obbligatoria SHIP
5. Archive `--status=SHIP|REJECT|DORMANT|TIMEOUT`
6. Promote lesson `learnings/L-YYYY-MM-NNN-<slug>.md`

**Trigger**: ogni audit/eval/research >=30min + cross-session value.
**Anti-pattern**: F2 cimitero (archive senza lesson), F3 confused re-opening, F4 inbox-zero theater (auto-promote senza confirm).
**Path AA01**: `C:/Users/edusc/aa01/` (separato codemasterdd, NON-git, disciplina personale).
**Reference**: memory `project_aa01_studio`.

### Protocol 5 -- External-perspective harsh review via subagent (cluster scrutiny) -- addendum 2026-05-13

Per cluster PR >=3 same day touching shared scope OR file security/governance-critical, spawn `harsh-reviewer` subagent PRE-merge:
- Boundary read-only (NO write/edit/commit, solo report markdown)
- Finding format: P0/P1/P2 + descrizione + impact + recommendation + file refs
- Integrate findings PRE-merge: P0 obbligatorio fix, P1 either fix OR documented defer, P2 acknowledge

**Trigger STRONGLY recommended** (Option C non-mandatory):
- Cluster >=3 PR same day con scope overlap OR consecutive
- File security/governance-critical (wrappers, keys, hooks, ACL, CLAUDE.md authoritative)
- Narrative claim "X/Y VIABLE/PASS" senza decomposition default vs mitigation
- Pre-merge ADR-class decision

**Cost**: ~$0.30-0.50/invocazione (~85K tokens). Sotto cap $20/mese ADR-0023.
**Anti-pattern**: skip per cluster doc-only o <2 PR (over-engineered overhead).
**Caso studio**: PR #80+#81 cluster review 2026-05-13 → 8 finding (3 P0 catch CWE-214 real) → PR #82 fix.
**Reference**: agent definition `~/.claude/agents/harsh-reviewer.md` + ADR-0018.

### Protocol 6 -- Brainstorming structured exploration via skill (architectural design) -- addendum 2026-05-13

Per ADR-class architectural decision generative (new sub-system / replace component / strategic platform choice), invoke superpowers `brainstorming` skill flow:
- Explore project context → 2-3 approaches con tradeoff esplicito + recommendation → present design → spec doc → only AFTER approval implementation

**Trigger STRONGLY recommended** (Option C non-mandatory):
- ADR-class decision architectural irreversibile/costoso reverse
- Replace existing component / pattern / wrapper / tooling
- Strategic platform choice (es. OpenRouter eval, framework adoption)

**Anti-pattern**:
- Apply HARD-GATE per task advisory/review (Eduardo "voglio vedere che ci dicono" NON è new feature)
- Apply per task lean <30min implementation (overhead sproporzionato)
- Sequential clarifying questions in auto-mode (confligge con no-questions instruction)

**Complementarity con P3 Archon**: P3 = analytic decompose post-decision. P6 = generative design pre-decision. Combined optimal: brainstorming PRIMA per options + Archon DOPO per stress-test.

**Caso studio**: brainstorming loaded 2026-05-13 pomeriggio per OpenRouter eval → 4 options A/B/C/D → Option C → ADR-0029 scaffold.

### Protocol 7 -- Self-Designed-Method Governance (SDMG) -- addendum 2026-05-17

Quando sto per **integrare in governance durevole** (ADR/agent/policy/memory) o **rendere autonomo** un METODO/processo che ho progettato io (NON azioni one-off): il mio design e' **ipotesi con tasso d'errore alto dimostrato**, non decisione. Gate obbligatorio: (1) design=ipotesi · (2) test empirico read-only (necessario NON sufficiente) · (3) **falsificazione esterna** arbitro `harsh-reviewer` + Archon CALIBRATE, pre-commit "se rigetta adotto non difendo" · (4) **anti-accretion check** -- se e' l'ennesimo emendamento su base con difetto irrisolto -> STOP, fix la base prima · (5) **adozione narrow** read-only/flag, azione resta umano/specialista · (6) **tuning-before-execute**, il decider e' specialista/ground-truth MAI il mio euristico · (7) post-exec validation.

**Trigger**: integrazione governance / autonomizzazione di un metodo self-designed.
**Evidenza**: n=7 auto-correzioni in sessione 2026-05-16/17 (ogni mio output non-falsificato esternamente era errato).
**Anti-pattern**: design->integra->"poi vediamo"; test-positivo=sufficiente; difendere metodo falsificato; accretion su base difettosa; euristico-come-decider; SDMG su fix one-off (over-engineering).
**Complementarita'**: sequenzia P3 (Archon) + P5 (harsh-reviewer) specificamente per metodi self-designed.
**Reference**: `docs/patterns/self-designed-method-governance.md` + L-2026-05-033 + ADR-0033 post-resolution note.

### Combined methodology UPDATED 2026-05-13 (post Protocol 5+6 addendum)

```
[Trigger: audit / eval / decision significativa]
  → Protocol 1 Refresh-verify state interno (OBBLIGATORIO)
  → [Architectural design generative? new sub-system / replace component]
        ├── SI → Protocol 6 brainstorming (3 approaches + tradeoff)
  → [Cluster >=3 PR same day OR file security/governance-critical?]
        ├── SI → Protocol 5 harsh-reviewer subagent PRE-merge (findings P0/P1/P2)
  → Protocol 4 AA01 workspace audit trail (start, se >=30min)
  → Protocol 2 Autoresearch multi-source (NECESSARY ma INSUFFICIENT)
  → [Decision high-stakes irreversibile?]
        ├── SI → Protocol 3 Archon 7-step + CALIBRATE falsifying experiment
        └── NO → empirical trial breve per architectural validation
  → Output: ADR Proposed / research doc / lesson / archive AA01 SHIP
```

### Measurement empirical post-formalization Protocol 5+6 (anti-aspirational mitigation)

Per evitare protocols 5+6 diventino aspirational reactive (stesso pattern P2 autoresearch FIRST n=2 reactive caso L-014+L-015):
- **PR body section "Cognitive protocols applied"** OR commit message footer: campi "harsh-reviewer invoked? Y/N" + "brainstorming skill applied? Y/N"
- **Threshold review ogni 3 mesi** (~SPRINT_03/04 boundary): check field adoption rate. Se <30% trigger application su qualifying tasks → ADR-0026 amendment B (declassify) o C (re-evaluate trigger).
- **Trigger Accepted Protocol 5+6**: n>=2 instances application con valore empirical documented.

**Reference completo**: ADR-0026 + lesson L-2026-05-002 (Hyperspace audit cycle 3 anti-pattern + 4 pattern positive) + lesson L-2026-05-003 (cross-repo pattern adoption cross-check governance interna) + L-2026-05-014 + L-2026-05-015 (autoresearch FIRST + PowerShell wrapper REM pollution).

## Aggiornamento JOURNAL
A fine sessione significativa, aggiungere entry in JOURNAL.md:
- Data YYYY-MM-DD
- Sezioni: Completato | Da fare | Note

## Governance meta-operativa (framework archivio adottato 2026-04-23)

Il repo adotta lo schema governance di `Archivio_Libreria_Operativa_Progetti/` (framework multi-progetto importato 2026-04-23):

- **File root-level governance**: `PROJECT_BRIEF.md`, `COMPACT_CONTEXT.md`, `DECISIONS_LOG.md`, `BACKLOG.md`, `OPEN_DECISIONS.md`, `ROADMAP.md`, `SPRINT_01.md`, `MASTER_PROMPT.md`, `REFERENCE_INDEX.md`, `PROMPT_LIBRARY.md`, `MODEL_ROUTING.md`
- **Meta-regole operative Claude Code**: `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/` (adottate come reference, non clonate al root per evitare drift):
  - `CLAUDE_OPERATING_RULES.md` — priorità fonti, autonomia, file-first, rituali chiusura
  - `TASK_EXECUTION_PROTOCOL.md` — fasi 0-7 per ogni task
  - `SAFE_CHANGES_ONLY.md` — cosa Claude può cambiare senza checkpoint
  - `CHANGE_BUDGET.md` — envelope A/B/C per limitare scope singola run

**Coabitazione**: `CLAUDE.md` (questo file) è **autoritativo progetto-specifico** (stack, hardware, tier routing, convenzioni); le regole 07 sono **meta-universali**. In caso conflitto, CLAUDE.md vince per decisioni progetto; le regole 07 vincono per pattern operativi generici Claude Code. FIRST_PRINCIPLES_GAME_CHECKLIST del framework è N/A (non è game repo, vedi Decisione 002 in `DECISIONS_LOG.md`).

**Ordine di lettura raccomandato per nuove sessioni**:
1. `CLAUDE.md` (questo file) — convenzioni progetto
2. `COMPACT_CONTEXT.md` — snapshot stato corrente
3. `STATUS_MULTI_REPO.md` — dashboard operativa cross-repo (se task coinvolge progetti monitorati)
3b. `GOALS.md` — direzione cross-repo S/M/L (se task tocca pianificazione/priorità)
4. `.claude/agents/README.md` — 18 sub-agent disponibili (game/dafne/quality/security/db/meta) + invocation pattern + status matrix (ready vs draft per ADR-0018)
5. `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/CLAUDE_OPERATING_RULES.md` — regole meta
6. `BACKLOG.md` + `OPEN_DECISIONS.md` — cosa è aperto ora
7. ADR rilevanti se il task tocca topic noto

**Per agent multi-client** (Codex Cloud, OpenCode, agent web-based o sandbox-confined): leggere prima `AGENTS.md` (preamble anti-confusion sandbox + path map + encoding policy) — ADR-0021. CLAUDE.md resta autoritativo per dettaglio operativo.
