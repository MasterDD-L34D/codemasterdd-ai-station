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
- Modelli fino a **7-8B** a piena quality (Qwen 2.5 Coder, Qwen 3 8B, DeepSeek 7B)
- Modelli fino a **14B** con quantizzazione Q4 aggressiva (performance ridotta)
- Velocità attesa Qwen 2.5 Coder 7B: ~40-55 tok/s (da validare con benchmark reale)

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
- Claude Code 2.1.114 (OAuth Claude Max, Opus 4.7)
- NVIDIA Driver 595.79 + CUDA 13.2

## Stack da installare questa settimana
- Node.js 22 LTS
- Python 3.10+
- VS Code
- Ollama 0.21+ + Qwen 2.5 Coder 7B
- GitHub CLI (gh)

## Stack da installare settimana prossima (quando migriamo progetti)
- Dipendenze specifiche progetti (da Evo-Tactics e Synesthesia)
- Eventuali MCP server (filesystem, github) se emergono bisogni reali

## Progetti target (migrazione settimana prossima)
- **Evo-Tactics**: co-op tactical game d20, monorepo Node+Python
  - GitHub: `github.com/MasterDD-L34D/Game`
  - Path Lenovo: `C:\dev\Game`
  - Stack: Node 22 + Python 3.10, xstate@5, inkjs, Vue3 bundle
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
- **Post Max**:
  - Task routine → Ollama Qwen 2.5 Coder 7B
  - Task complessi → OpenRouter pay-per-use (Claude Sonnet, GPT)
  - Task veloci → Ollama Qwen 3 8B

## Aggiornamento JOURNAL
A fine sessione significativa, aggiungere entry in JOURNAL.md:
- Data YYYY-MM-DD
- Sezioni: Completato | Da fare | Note
