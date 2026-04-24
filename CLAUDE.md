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
- Mac mini M4 Pro 48GB come **upgrade AI inference** se/quando budget permette
  - Aggiungerebbe capacità modelli 30B+ Ollama
  - **NON è dependency** del piano: Lenovo funziona pienamente da solo

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
- Velocità **misurate** (sustained eval, prompt DoublyLinkedList Python):

| Modello | Tok/s | GPU offload | Uso consigliato |
|---------|-------|-------------|-----------------|
| Qwen 2.5 Coder 7B Q4_K_M | **114** | 100% | query one-shot, create, read/explain |
| Qwen 2.5 Coder 14B Q3_K_M | 10.8 | 62% | sconsigliato (hallucination su constraint) |
| Qwen 2.5 Coder 14B **Q2_K** | **18.7** | 73% | **agentic edit (sweet spot + faithful)** |

- Stack agentic sovereign consigliato: **Aider + Qwen 14B Q2_K** — vedi `docs/adr/0007-aider-qwen-quantization-findings.md`
- Env vars Ollama applicate (User scope, persistenti) — config rationale: `docs/adr/0004-ollama-rtx5060-config.md` + `docs/adr/0007-aider-qwen-quantization-findings.md`
  - `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_KEEP_ALIVE=30m`
  - `OLLAMA_CONTEXT_LENGTH=8192` (ridotto da 16384 il 2026-04-20 su 16GB RAM: +36% speed su 14B Q2 liberando KV cache da CPU spill. Override per-request `num_ctx: 16384` per task multi-file. **Post upgrade 64GB 2026-04-22: il razionale originale è decaduto — rivalidare bench empirico prima di riportare default a 16384**, vedi `docs/adr/0012-ram-upgrade-64gb-impact.md`.)
- **Nuova capacità post 2026-04-22 (64GB RAM)**: modelli 30B+ non più RAM-bound; qwen3-coder:30b tier 2 non più borderline; Qwen 2.5 Coder 32B Q4 (~19-20GB) diventa candidato benchmarkable; 14B Q3_K_M potrebbe tornare competitivo con ctx più alto. Tutti i valori tok/s in tabella rimangono **validi** (misurati pre-upgrade, ma non RAM-bound) — rebench opzionale solo per scoprire se ctx più largo cambia la decision matrix.

## Ecosistema device
- **CodeMasterDD** (Lenovo LOQ Tower 17IAX10): workstation primaria AI agentic
- **Ryzen 9600X desktop**: PC appoggio corrente, dismissione graduale quando CodeMasterDD ha tutto

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
  - **Google Gemini** (`GEMINI_API_KEY`) — 60 req/min free. Model examples: `gemini/gemini-2.0-flash-exp`
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
- Aider 0.86.2 (installato 2026-04-20 via `python -m pip install aider-install && aider-install`, binary `C:\Users\edusc\.local\bin\aider.exe`) — **client agentic consigliato per workflow sovereign**
- VSCode Cline extension `saoudrizwan.claude-dev` v3.79.0 (installata 2026-04-20) — **NOT viable come agentic con Qwen 7B**, vedi `docs/adr/0006-cline-qwen-viability.md`

## Stack da installare questa settimana
_(completato il 2026-04-19 — vedi "Stack installato")_

## Stack da installare settimana prossima (quando migriamo progetti)
- Dipendenze specifiche progetti (da Evo-Tactics e Synesthesia)
- Eventuali MCP server (filesystem, github) se emergono bisogni reali

## Progetti monitorati (status 2026-04-24)

- **Evo-Tactics** — co-op tactical game d20, monorepo Node+Python
  - GitHub: `github.com/MasterDD-L34D/Game`
  - Path Lenovo: `C:\dev\Game`
  - Stack: Node 22 + Python 3.10, xstate@5, inkjs, Vue3 bundle
  - Compat runtime: Node 24 system-level (validato n=710+ test)
  - **Integration 2026-04-24**: repo target dello swarm Dafne (vedi sotto). Branch `swarm/register-agents-2026-04-24` contiene 2 agent registrati (gameplay-prototyper, combat-engineer) + runtime state sync. PR pending su GitHub UI.
  - **File chiave toccati da swarm**: `agents/agents_index.json` (registry 11 agent), `agents/*.md` + `.ai/*/PROFILE.md` (definizioni), `docs/flint-status.json` (monitor telemetria), `data/flow-shell/atlas-snapshot.json`

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

### Relazioni inter-repo

```
codemasterdd-ai-station (policy + infrastruttura)
       │
       ├─── Evo-Tactics (C:\dev\Game)
       │         ↑
       │         │ swarm produce → integra manualmente
       │         │
       └─── Dafne swarm (C:\Users\edusc\Dafne\workspace\swarm)
                 ↑
                 │ governance + pilastri + metriche empirical
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

## Struttura repository
```
lenovo-ai-station/
├── scripts/       # setup, maintenance, backup scripts
├── docs/          # documentazione tecnica, procedure, ADR
├── logs/          # log esecuzione (gitignored)
├── backup/        # backup config, registry (gitignored)
├── README.md
├── JOURNAL.md
├── CLAUDE.md
└── .gitignore
```

## Scopo repository
`lenovo-ai-station` è **infrastructure-as-code** della workstation Lenovo:
- Gestione setup, manutenzione, backup
- Procedure ripetibili
- Documentazione decisioni architetturali
- Knowledge base personale
- Log sessioni significative

**NON contiene codice di progetti reali** (vivono in repo separati).

## Priorità modelli AI
- **Durante Claude Max (fino 19/05/2026)**: Opus 4.7 per tutto
- **Post Max** — task-routing (vedi ADR-0008 per rationale completo):
  - Query one-shot → `ollama run qwen2.5-coder:7b` (114 tok/s)
  - Read/explain + CREATE single file → Aider + Qwen 7B + `whole`
  - **Cosmetic edit** (JSDoc, docstrings, rename, lint-fix) → **Aider + Qwen 7B + `whole`** (format compatibile, faithfulness non critica)
  - **Behavior-critical edit** (refactor, bug fix, logic change) → **Aider + Qwen 14B Q2_K + `--edit-format diff`** (safe failure; ~20-40% retry manuale ma zero silent-corruption)
  - **Behavior-critical escalation** (quando 14B Q2 safe-fails, es. task R1-type 1-line value change) → **Aider + qwen3-coder:30b + diff** (MoE 30B-A3B, tier 2 fallback prima di Claude Pro; speed 2× slower + RAM tight ma risolve anti-pattern — vedi ADR-0009 addendum)
  - Multi-file refactor / debug strategico → OpenRouter pay-per-use (Sonnet/Opus) o Claude Pro come backbone
  - **⚠️ DEPRECATO**: Aider + 14B Q2 + `whole` — silent-corruption deterministico su task "edit single file" semplici, vedi ADR-0008
  - Riferimenti decisionali: `docs/adr/0007-aider-qwen-quantization-findings.md` + `docs/adr/0008-aider-whole-format-silent-corruption.md`
  - **Seconda dimensione routing (in review)**: `docs/adr/0016-constraint-count-routing-dimension.md` (Proposed 2026-04-24). Estende matrice classe-based con **constraint-count**: 1 qualsiasi tier / 2-3 additive+preserve → 14B Q2 local o 70B cloud / 2 fix+transform → downgrade 14B Q2 (7B skippa transform) / **5+ strict → manual Claude Code**. Consultare per task con ≥3 constraint espliciti nel prompt. Status Accepted trigger: n≥3 data points addizionali.

- **Safety protocol per Aider** (valido sempre):
  - `git diff HEAD~1` post-edit prima di pushare: commit message generati dall'LLM riflettono l'intent, non necessariamente il diff reale
  - Evitare `--yes-always` in repo con working tree sporco
  - Per task behavior-critical considerare `--no-auto-commits`
  - Guard rail chain (`git config --global core.hooksPath C:/Users/edusc/.local/share/git-hooks`):
    1. `commit-msg` globale — valida Conventional Commits cross-agent (tutti gli agent inclusi Aider). ADR-0011.
    2. `pre-commit` globale — blocca silent-corruption pattern (ADR-0008).
    3. Husky repo-local (solo Evo-Tactics) — skip-worktree wrapper.
    4. Claude Code PreToolUse `scripts/hooks/commit-guard.js` — fail-fast in sessione Claude Code (duplicato di 1 per feedback veloce).
  - Bypass guard rail con `git commit --no-verify`, non raccomandato

- **Wrapper CLI per delegazione** (in `C:\Users\edusc\.local\bin\`, eseguibili da cmd.exe):
  - **Locali (tier 1-2 sovereign)**:
    - `aider-cosmetic <file>` → 7B + whole (JSDoc, docstrings, rename, lint-fix) — 114 tok/s
    - `aider-refactor <file>` → 14B Q2 + diff + no-auto-commits (refactor, bug fix, logic change) — 25 tok/s
  - **Cloud (tier 3-4, aggiunti 2026-04-23 combo F+D, vedi ADR-0013)**:
    - `aider-groq <file>` → groq/llama-3.3-70b-versatile + diff + no-auto-commits — 630 tok/s free tier
    - `aider-cerebras <file>` → cerebras/llama3.1-8b + diff + no-auto-commits — 733 tok/s free tier
    - `aider-gemini <file>` → gemini/gemini-2.5-flash + diff + no-auto-commits (attenzione thinking budget)
    - `aider-openai <file>` → openai/gpt-4o-mini + diff + no-auto-commits — **paid, monitorare ccusage**
  - **Privacy guard rail**: cloud OK solo su repo non-sensitive (`codemasterdd-ai-station` sì, Evo-Tactics/Synesthesia verificare caso-per-caso, repo cliente MAI). Vedi `docs/patterns/delegation-to-aider.md` Extension tier 3 cloud.

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
4. `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/CLAUDE_OPERATING_RULES.md` — regole meta
5. `BACKLOG.md` + `OPEN_DECISIONS.md` — cosa è aperto ora
6. ADR rilevanti se il task tocca topic noto
