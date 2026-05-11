# CLAUDE.md — CodeMasterDD AI Station

## Ruolo workstation
Dev workstation AI agentic **PRINCIPALE** per Eduardo Scarpelli.
Questa macchina è autosufficiente per tutti i workflow dev e AI locali.
Target: piattaforma AI sovereign con zero subscription fisse post-maggio 2026.

## Roadmap strategica (realistica — aggiornata 2026-04-23 post ADR-0013+0014)
- **19/04/2026**: ✅ setup Lenovo completato, infrastructure ready
- **20-21/04**: ✅ Ollama + Qwen 7B/14B, ADR-0004/0007/0008 findings
- **22/04**: ✅ migrazione Evo-Tactics + Synesthesia, RAM upgrade 64GB (ADR-0012), API keys cloud (ADR-0013 Accepted)
- **22-23/04 notte**: ✅ quality bench + 4 wrapper cloud + 6 dogfood Fase 6 inaugurati
- **Fino al 19/05**: Claude Max attivo, Fase 6 tracking compresso (ADR-0014 Accepted) — target n≥20 dogfood + privacy validation + cost tracking <$20/mese
- **20/05/2026 (approx, allineato Claude Max expiration)**: Fase 6 closure → **ADR-0015 budget decision finale**
- **Post 20/05**: operatività target **full-sovereign $0-50/anno** via:
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

## Ecosistema device (aggiornato 2026-05-10 post LAN discovery + Ryzen capability reveal)

Fleet Eduardo on-LAN 192.168.1.0/24 (4 PC totali, 2 di Eduardo + 2 di moglie):

- **CodeMasterDD** (Lenovo LOQ Tower 17IAX10, 192.168.1.121): workstation primaria AI agentic
- **DESKTOP-T77TMKT** (192.168.1.222) -- **Ryzen 9600X desktop EDUARDO** (rivelato 2026-05-10 NON in dismissione): MSI MS-7E26 mobo, **RTX 4070 SUPER 12GB VRAM** (+50% vs Lenovo 8GB), 31GB RAM, Windows 11 build 26200, OpenSSH server 9.5 attivo. **Capability tier**: 14B Q4 full-GPU + 22B Q4 split + Codestral 22B + SDXL/Flux. AI stack inizialmente assente (Ollama/Python/Aider non installati al 2026-05-10), install pending.
- **DESKTOP-B9L203E** (192.168.1.37) -- secondary desktop **moglie**: Windows DESKTOP-XXX hostname, MAC Samsung OUI 2C:F0:5D, capability TBD, OpenSSH non attivo (install pending Eduardo direct)
- **LAPTOP-D73A8DIE** (192.168.1.130) -- laptop **moglie**: Windows LAPTOP-XXX hostname, MAC A0:A4:C5, capability TBD, OpenSSH non attivo (install pending Eduardo direct)

**Drift fix 2026-05-10**: claim originale "Ryzen 9600X desktop: PC appoggio corrente, dismissione graduale" e' OBSOLETO. Ryzen ha 4070 SUPER 12GB > Lenovo 5060 8GB per modelli 14B-22B. Ryzen e' **secondary inference active** + complementary tier capability, NOT phase-out.

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
- **Storage primario**: `C:\Users\edusc\.config\api-keys\keys.env` (ACL: solo `CODEMASTERDD\edusc:(F)`, inheritance disabilitata)
- **Backup locale**: `C:\dev\codemasterdd-ai-station\backup\api-keys-2026-04-22.env` (gitignored via `backup/*`, ACL identiche)
- **Config Aider globale**: `C:\Users\edusc\.aider.conf.yml` contiene `env-file:` → auto-load in ogni sessione Aider (via LiteLLM)
- **Provider attivi** (free-tier):
  - **Groq** (`GROQ_API_KEY`) — LPU inference veloce, tier free 6000 tok/min, candidato tier 3 prioritario. Model examples: `groq/llama-3.3-70b-versatile`, `groq/qwen-2.5-coder-32b`
  - **Cerebras** (`CEREBRAS_API_KEY`) — WSE inference massima velocità, tier free generoso. Model examples: `cerebras/llama3.3-70b`
  - **Google Gemini** (`GEMINI_API_KEY` per Aider/LiteLLM; `GOOGLE_GENERATIVE_AI_API_KEY` per OpenCode native Google provider — dual-name necessario, vedi ADR-0022 follow-up) — 60 req/min free. Model examples: `gemini/gemini-2.5-flash` (`gemini-2.0-flash-exp` deprecated v1beta 404)
  - **OpenAI** (`OPENAI_API_KEY`) — pay-per-use (no free tier generoso). Model examples: `gpt-4o`, `gpt-4o-mini`
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

## Stack da installare questa settimana
_(completato il 2026-04-19 — vedi "Stack installato")_

## Stack da installare settimana prossima (quando migriamo progetti)
- Dipendenze specifiche progetti (da Evo-Tactics e Synesthesia)
- Eventuali MCP server (filesystem, github) se emergono bisogni reali

## Progetti monitorati (status 2026-05-08)

- **Evo-Tactics (Game)** — co-op tactical game d20, monorepo Node+Python (Vue3 bundle)
  - GitHub: `github.com/MasterDD-L34D/Game`
  - Path Lenovo: `C:\dev\Game`
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

- **Synesthesia** — web app esame UniUPO
  - GitHub: `github.com/MasterDD-L34D/synesthesia`
  - Path Lenovo: `C:\dev\synesthesia`
  - Stack: Node 20 ESM, Express, EJS, SQLite, Passport
  - Status: MVP funzionante
  - Privacy policy per-repo: `controllers/`/`routes/`/`middlewares/` sovereign-only; `views/`/`public/` cloud OK

- **Dafne swarm (evo-swarm)** — orchestratore AI agentic per Evo-Tactics, multi-agent sistema custom
  - GitHub: `github.com/MasterDD-L34D/evo-swarm`
  - Path Lenovo: `C:\Users\edusc\Dafne\workspace\swarm` (repo git separato, NOT in `C:\dev\`)
  - Home Dafne: `C:\Users\edusc\Dafne\` (start-dafne.cmd + agent/ config + desktop shortcut)
  - Stack: Python 3.12 + Flask + Ollama (qwen3:8b governance + nomic-embed-text per H5 gate)
  - Status 2026-04-24 notte: Atto 1 day-3/10. Server Flask UP idle su `:5000` per day-5 (26/04). 20 commit pushati. 11 agent runtime. Pilastro 2 evoluzione 🔴→🟡 (6 lezioni empirical).
  - **Scopo**: coordinatrice + memory keeper che governa specialist (lore-designer, trait-curator, balancer, ecc.) per produrre content integrabile in repo `Game`.
  - **Integration col Game repo**: scrive su `C:\dev\Game\agents/` quando Eduardo approva nuovi agent via `POST /api/dafne/approve-agent`. H5 gate autonomous blocca pattern loop.
  - **Governance framework-archivio adottato**: 5 file root-level (PROJECT_BRIEF, DECISIONS_LOG, BACKLOG, OPEN_DECISIONS, MODEL_ROUTING) + mapping selettivo. Decisione 006 in DECISIONS_LOG swarm.
  - **Open items**: OD-003 Groq key 403, OD-004 dashboard usage, OD-005 Tavily (tutti non bloccanti). BACKLOG L7 CAMEL integration deferred a Atto 2.
  - **Avvio**: `cd C:\Users\edusc\Dafne\workspace\swarm && .\START-SWARM.ps1` → dashboard `http://localhost:5000`
  - **Dettaglio completo**: memoria `reference_dafne_swarm.md` + `CAMEL-INTEGRATION.md` nel repo swarm

- **Vault (vault-shared)** — knowledge management LLM-wiki personale Eduardo, **sibling-peer monitored** (added 2026-05-10)
  - GitHub: `github.com/MasterDD-L34D/vault`
  - Path Lenovo: `C:\dev\vault-shared\`
  - Stack: Karpathy LLM-wiki + ACCESS structure (Atlas/Cards/Sources/Spaces) + 7 production agent (Quality Gate workflow smoke->draft->production 3-gate) + Ollama LAN (Qwen + deepseek-r1) + Claude variants
  - Status 2026-05-10: **7/7 PRODUCTION milestone hit** (vault-linter v2 nested-YAML FP 0%, design-watcher v2 deepseek-r1 recall +33pp, ollama-dispatcher v1 -91% wall claim methodology TBR). 15+ commit 30gg. LLM routing matrix v1.0 (commit reference path stabile `vault-shared/llm-routing.json`, NO hash citato per drift risk).
  - **Privacy**: sovereign-only (NON in `~/.config/aider-privacy-whitelist.txt`). Contiene UniUPO esame + GDR campagne curated + GPT-Prompts library + Dev/Synesthesia academic + Dev/Evo-Tactics design notes.
  - **Relazione codemasterdd**: sibling-peer disjoint scope. NO write-path bidirezionale. Cross-pattern reference one-way: vault llm-routing matrix v1.0 -> potential MODEL_ROUTING.md addendum (methodology Quality Gate Step 2 con split metrics + keep_alive + retries + output validation).
  - **Hook globali**: compat VALIDATED 2026-05-10 (empty commit test PASS, reverted post-test). Vault `core.hooksPath` punta a `C:/Users/edusc/.local/share/git-hooks`.
  - **Boundary**: codemasterdd NON scrive su vault-shared. Vault-shared self-governs. Eduardo media bidirezionale via personal workflow. SPOF accepted risk documentato.
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

**Sibling-peer disjoint** (sovereign-only, NO write-path bidirezionale, cross-reference one-way):

```
vault-shared (C:\dev\vault-shared)
       │ Knowledge management LLM-wiki Karpathy + 7 production agents
       │ Stack overlap: Ollama LAN + Qwen + deepseek-r1 + Claude variants
       │ Cross-pattern reference one-way -> codemasterdd MODEL_ROUTING addendum
       │ Privacy: sovereign-only (UniUPO + GDR + GPT-Prompts + Dev notes)
       │ Hook globali: compatibili (validated 2026-05-10)
       │ Boundary: NO write-path codemasterdd-side
       │ Eduardo media tutti i flow
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
- **Durante Claude Max (fino 19/05/2026)**: Opus 4.7 per tutto
- **Tier 0 strategic post-Max (2026-05-20+)** — ADR-0023 Proposed 2026-05-09:
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

- **Wrapper CLI per delegazione** (in `C:\Users\edusc\.local\bin\`, eseguibili da cmd.exe):
  - **Aider locali (tier 1-2 sovereign)**:
    - `aider-cosmetic <file>` → 7B + whole (JSDoc, docstrings, rename, lint-fix) — 114 tok/s
    - `aider-refactor <file>` → 14B Q2 + diff + no-auto-commits (refactor, bug fix, logic change) — 25 tok/s
  - **Aider cloud (tier 3-4, aggiunti 2026-04-23 combo F+D, vedi ADR-0013)**:
    - `aider-groq <file>` → groq/llama-3.3-70b-versatile + diff + no-auto-commits — 630 tok/s free tier
    - `aider-cerebras <file>` → cerebras/llama3.1-8b + diff + no-auto-commits — 733 tok/s free tier
    - `aider-gemini <file>` → gemini/gemini-2.5-flash + diff + no-auto-commits (attenzione thinking budget)
    - `aider-openai <file>` → openai/gpt-4o-mini + diff + no-auto-commits — **paid, monitorare ccusage**
  - **OpenCode (tier multi-step agentic, ADR-0022 Accepted 2026-05-09)**: in `C:\Users\edusc\AppData\Roaming\npm\opencode.ps1` (npm global v1.14.41):
    - `opencode run --model "ollama/qwen3-coder:30b" "<task>"` → tier 1 sovereign default (MoE A3B tool-use native)
    - Config: `~/.config/opencode/opencode.json` (5 provider mappati, env vars from `~/.config/api-keys/keys.env`)
    - **NON usare** Qwen 2.5 Coder family con OpenCode (raw JSON tool call non eseguito)
    - **NON viable** cloud free 8B-70B (rate-limited TPM o context vs request ~50k)
  - **Privacy guard rail tecnico (H8 ADR-0023, Accepted 2026-05-09)**:
    - Wrapper cloud (`aider-groq` / `aider-cerebras` / `aider-gemini` / `aider-openai`) controllano automaticamente repo via `git rev-parse --show-toplevel` + whitelist `~/.config/aider-privacy-whitelist.txt`. Se repo non whitelisted → ABORT con error, no source code inviato a cloud.
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

## Cognitive workflow protocols (ADR-0026)

Per audit / eval / decision / pivot significativo, applicare 4 cognitive workflow protocols (triple anchor: ADR-0026 + memory + questa sezione). Vedi `docs/adr/0026-cognitive-workflow-protocols.md` per dettaglio + caso studio + anti-pattern.

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

### Combined methodology (lesson L-2026-05-002 + L-2026-05-003)

```
[Trigger: audit / eval / decision significativa]
  → Protocol 1 Refresh-verify state interno (OBBLIGATORIO)
  → Protocol 4 AA01 workspace audit trail (start)
  → Protocol 2 Autoresearch multi-source (NECESSARY ma INSUFFICIENT)
  → [Decision high-stakes irreversibile?]
        ├── SI → Protocol 3 Archon 7-step + CALIBRATE falsifying experiment
        └── NO → empirical trial breve per architectural validation
  → Output: ADR Proposed / research doc / lesson / archive AA01 SHIP
```

**Reference completo**: ADR-0026 + lesson L-2026-05-002 (Hyperspace audit cycle 3 anti-pattern + 4 pattern positive) + lesson L-2026-05-003 (cross-repo pattern adoption cross-check governance interna).

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
4. `.claude/agents/README.md` — 18 sub-agent disponibili (game/dafne/quality/security/db/meta) + invocation pattern + status matrix (ready vs draft per ADR-0018)
5. `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/CLAUDE_OPERATING_RULES.md` — regole meta
6. `BACKLOG.md` + `OPEN_DECISIONS.md` — cosa è aperto ora
7. ADR rilevanti se il task tocca topic noto

**Per agent multi-client** (Codex Cloud, OpenCode, agent web-based o sandbox-confined): leggere prima `AGENTS.md` (preamble anti-confusion sandbox + path map + encoding policy) — ADR-0021. CLAUDE.md resta autoritativo per dettaglio operativo.
