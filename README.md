# CodeMasterDD AI Workstation

**Infrastructure-as-code** del desktop CodeMasterDD dedicato allo sviluppo AI agentic.

Questa è la workstation **primaria e autosufficiente** di Eduardo Scarpelli: tutti i workflow di sviluppo e i modelli AI locali girano qui, senza dipendenze da altri device.

## Scopo del repository
- Setup e configurazione ripetibile della workstation
- Procedure di manutenzione e backup
- Documentazione decisioni architetturali (ADR)
- Knowledge base personale e log sessioni significative

> **Nota**: questo repo non contiene codice di progetti reali. Quelli vivono in repository separati (Evo-Tactics, Synesthesia, ecc.).

## Hardware (classe, dettagli specifici nel private fleet store)
- **CPU**: Intel Core Ultra 7 255HX class (24 core Arrow Lake HX)
- **GPU**: NVIDIA RTX 5060 8GB VRAM (Blackwell sm_120, CUDA 13.2)
- **RAM**: 64GB DDR5-5600 dual channel (upgrade 2026-04-22, vedi ADR-0012)
- **Storage**: SSD 1TB NVMe
- **OS**: Windows 11 Home 25H2 (build 26200)

## Stack attivo (aggiornato 2026-06-17)
- **Claude Code 2.1.179** -- agente CLI di sviluppo (OAuth Claude Max ~fino 2026-06-17)
- **Git 2.53.0.windows.3** + **GitHub CLI 2.90.0**
- **NVIDIA Driver 595.95 + CUDA 13.2**
- **Node.js** via nvm-windows: **22.22.3** attivo (Game-canonical -- engines `>=22 <23` + AI-playtest calibration runtime-sensitive) + **24.15.0** disponibile (ADR-0003); switch per-progetto
- **Python 3.12.10**
- **VS Code 1.120.0**
- **Ollama 0.30.8** con modelli locali tier-based (cosmetic 7B / behavior 14B Q2 / escalation qwen3-coder:30b MoE / reasoning deepseek-r1 / multimodal gemma4)
- **Aider 0.86.2** con wrapper CLI (`aider-cosmetic`, `aider-refactor`, `aider-groq-bypass`, `aider-cerebras`, `aider-gemini`, `aider-openai`)
- **Cloud tier 3** (free tier): Groq llama-3.3-70b + Cerebras llama-3.1-8b + Gemini 2.5 Flash + OpenAI gpt-4o-mini

## Roadmap sintetica (aggiornata post ADR-0014)
- **19/04**: ✅ setup base completato
- **20-22/04**: ✅ Ollama + Qwen stack + migrazione progetti + bench + RAM upgrade
- **22-23/04**: ✅ tier 3 cloud stack + quality bench + Fase 6 inaugurata
- **Fino 19/05 (Claude Max expiration)**: Fase 6 CLOSED 2026-05-07 (n=12 con soft-override esteso, ADR-0015 Accepted)
- **~20/05/2026**: ADR-0015 Accepted 2026-05-07: scenario A full-sovereign confermato

Per i dettagli operativi e le convenzioni di lavoro con Claude Code, vedi [CLAUDE.md](./CLAUDE.md). Per storia decisionale completa, `docs/adr/` (43 ADR: 0001-0043).

## Governance & navigazione

File governance root-level (schema framework archivio adottato 2026-04-23):

- [PROJECT_BRIEF.md](./PROJECT_BRIEF.md) — scopo, obiettivo di successo, vincoli
- [COMPACT_CONTEXT.md](./COMPACT_CONTEXT.md) — snapshot stato corrente (aggiornato fine sessione)
- [DECISIONS_LOG.md](./DECISIONS_LOG.md) — indice ADR strategici + decisioni operative
- [BACKLOG.md](./BACKLOG.md) — backlog prioritizzato + primo sprint consigliato
- [OPEN_DECISIONS.md](./OPEN_DECISIONS.md) — decisioni aperte non bloccanti
- [docs/archive/ROADMAP.md](./docs/archive/ROADMAP.md) — ARCHIVED (fasi 1-8 storiche; direzione live = GOALS.md)
- [docs/archive/SPRINT_01.md](./docs/archive/SPRINT_01.md) — ARCHIVED (sprint chiuso 2026-04-24)
- [docs/archive/SPRINT_02.md](./docs/archive/SPRINT_02.md) — ARCHIVED (finestra 2026-05-20..06-19 spent)
- [MASTER_PROMPT.md](./MASTER_PROMPT.md) — prompt apertura portabile
- [REFERENCE_INDEX.md](./REFERENCE_INDEX.md) — indice navigabile docs/reference/patterns/research
- [PROMPT_LIBRARY.md](./PROMPT_LIBRARY.md) — prompt riutilizzabili progetto-specifici
- [MODEL_ROUTING.md](./MODEL_ROUTING.md) — routing strategico strumenti/modelli

Framework universale multi-progetto: `Archivio_Libreria_Operativa_Progetti/` (libreria, template, workflow, regole meta Claude Code).

## Licenza

Repo pubblico per backstop di piattaforma e trasparenza -- NON un template da riusare.
Tutti i diritti riservati: nessuna licenza di riuso/ridistribuzione concessa (assenza di
file LICENSE = all-rights-reserved di default). Il codice dei progetti reali vive in repo
separati.

## Autore
Eduardo Scarpelli - `<email-redacted>` - GitHub: [@MasterDD-L34D](https://github.com/MasterDD-L34D)

## Data creazione
19 aprile 2026

Ultimo refresh stack: 2026-06-17.
