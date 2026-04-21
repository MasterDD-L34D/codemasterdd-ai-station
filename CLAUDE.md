# CLAUDE.md — CodeMasterDD AI Station

## Ruolo workstation
Dev workstation AI agentic **PRINCIPALE** per Eduardo Scarpelli.
Questa macchina è autosufficiente per tutti i workflow dev e AI locali.
Target: piattaforma AI sovereign con zero subscription fisse post-maggio 2026.

## Roadmap strategica (realistica)
- **Oggi (19/04/2026)**: setup Lenovo completato, infrastructure ready
- **Settimana corrente**: Ollama + primo modello locale (Qwen 2.5 Coder 7B)
- **Settimana prossima**: migrazione progetti da Ryzen (Evo-Tactics + Synesthesia)
- **Fino al 19/05**: uso intensivo Claude Max (Opus 4.7) + benchmark parallelo Ollama
- **Post Claude Max (da 20/05)**:
  - Primary: Ollama locale + Claude Code (senza OAuth Max)
  - Fallback: OpenRouter pay-per-use per task critici
  - Zero subscription ricorrenti

## Estensioni future (opzionali, non pianificate)
- Mac mini M4 Pro 48GB come **upgrade AI inference** se/quando budget permette
  - Aggiungerebbe capacità modelli 30B+ Ollama
  - **NON è dependency** del piano: Lenovo funziona pienamente da solo

## Hardware (definitivo)
- **CodeMasterDD** (Lenovo LOQ Tower 17IAX10, desktop)
  - Intel Core Ultra 7 255HX (24 core Arrow Lake HX, 2.40 GHz base)
  - NVIDIA RTX 5060 8GB VRAM (Blackwell sm_120, CUDA 13.2)
  - 16GB DDR5
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
  - `OLLAMA_CONTEXT_LENGTH=8192` (ridotto da 16384 il 2026-04-20: +36% speed su 14B Q2 liberando KV cache da CPU spill. Override per-request `num_ctx: 16384` per task multi-file.)

## Ecosistema device
- **CodeMasterDD** (Lenovo LOQ Tower 17IAX10): workstation primaria AI agentic
- **Ryzen 9600X desktop**: PC appoggio corrente, dismissione graduale quando CodeMasterDD ha tutto

## Configurazione sicurezza applicata (19/04/2026)
- BitLocker: triplo layer disabilitato
- OneDrive: account scollegato, sync bloccato
- Bloatware rimosso (21 pacchetti)
- Account: eduscarpelli@gmail.com (con Claude Max attivo)

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
- Aider 0.86.2 (installato 2026-04-20 via `python -m pip install aider-install && aider-install`, binary `C:\Users\edusc\.local\bin\aider.exe`) — **client agentic consigliato per workflow sovereign**
- VSCode Cline extension `saoudrizwan.claude-dev` v3.79.0 (installata 2026-04-20) — **NOT viable come agentic con Qwen 7B**, vedi `docs/adr/0006-cline-qwen-viability.md`

## Stack da installare questa settimana
_(completato il 2026-04-19 — vedi "Stack installato")_

## Stack da installare settimana prossima (quando migriamo progetti)
- Dipendenze specifiche progetti (da Evo-Tactics e Synesthesia)
- Eventuali MCP server (filesystem, github) se emergono bisogni reali

## Progetti target (migrazione settimana prossima)
- **Evo-Tactics**: co-op tactical game d20, monorepo Node+Python
  - GitHub: `github.com/MasterDD-L34D/Game`
  - Path Lenovo: `C:\dev\Game`
  - Stack: Node 22 + Python 3.10, xstate@5, inkjs, Vue3 bundle
  - Compat runtime: useremo Node 24 a livello di sistema; installeremo nvm-windows solo se emergono incompatibilità
  - 710+ test

- **Synesthesia**: web app esame UniUPO
  - GitHub: `github.com/MasterDD-L34D/synesthesia`
  - Path Lenovo: `C:\dev\synesthesia`
  - Stack: Node 20 ESM, Express, EJS, SQLite, Passport
  - Status: MVP funzionante

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
  - Multi-file refactor / debug strategico → OpenRouter pay-per-use (Sonnet/Opus) o Claude Pro come backbone
  - **⚠️ DEPRECATO**: Aider + 14B Q2 + `whole` — silent-corruption deterministico su task "edit single file" semplici, vedi ADR-0008
  - Riferimenti decisionali: `docs/adr/0007-aider-qwen-quantization-findings.md` + `docs/adr/0008-aider-whole-format-silent-corruption.md`

- **Safety protocol per Aider** (valido sempre):
  - `git diff HEAD~1` post-edit prima di pushare: commit message generati dall'LLM riflettono l'intent, non necessariamente il diff reale
  - Evitare `--yes-always` in repo con working tree sporco
  - Per task behavior-critical considerare `--no-auto-commits`
  - Guard rail pre-commit globale attivo (`git config --global core.hooksPath C:/Users/edusc/.local/share/git-hooks`) che blocca commit con silent corruption pattern — bypass con `git commit --no-verify`, non raccomandato

- **Wrapper CLI per delegazione** (in PATH Windows, eseguibili da cmd.exe):
  - `aider-cosmetic <file>` → 7B + whole (JSDoc, docstrings, rename, lint-fix)
  - `aider-refactor <file>` → 14B Q2 + diff + no-auto-commits (refactor, bug fix, logic change)

- **Delegation protocol Claude Code → Aider**: vedi `docs/patterns/delegation-to-aider.md` — decision tree classification, formato handoff, review loop, tracking fail rate per Fase 6

## Aggiornamento JOURNAL
A fine sessione significativa, aggiungere entry in JOURNAL.md:
- Data YYYY-MM-DD
- Sezioni: Completato | Da fare | Note
