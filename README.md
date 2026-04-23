# CodeMasterDD AI Workstation

**Infrastructure-as-code** del desktop CodeMasterDD (Lenovo LOQ Tower 17IAX10) dedicato allo sviluppo AI agentic.

Questa è la workstation **primaria e autosufficiente** di Eduardo Scarpelli: tutti i workflow di sviluppo e i modelli AI locali girano qui, senza dipendenze da altri device.

## Scopo del repository
- Setup e configurazione ripetibile della workstation
- Procedure di manutenzione e backup
- Documentazione decisioni architetturali (ADR)
- Knowledge base personale e log sessioni significative

> **Nota**: questo repo non contiene codice di progetti reali. Quelli vivono in repository separati (Evo-Tactics, Synesthesia, ecc.).

## Hardware
- **Modello**: Lenovo LOQ Tower 17IAX10 (desktop)
- **CPU**: Intel Core Ultra 7 255HX (24 core Arrow Lake HX, 2.40 GHz base)
- **GPU**: NVIDIA RTX 5060 8GB VRAM (Blackwell sm_120, CUDA 13.2)
- **RAM**: **64GB DDR5-5600** dual channel (2×32GB Micron CT32G56C46S5.C16D, upgrade 2026-04-22, vedi ADR-0012)
- **Storage**: SSD 1TB Micron NVMe
- **OS**: Windows 11 Home 25H2 (build 26200)

## Stack attivo (aggiornato 2026-04-23)
- **Claude Code 2.1.116** — agente CLI di sviluppo (OAuth Claude Max fino 2026-05-19)
- **Git 2.53.0.windows.3** + **GitHub CLI 2.90.0**
- **NVIDIA Driver 595.79 + CUDA 13.2**
- **Node.js 24.15.0 LTS** + npm 11.12.1
- **Python 3.12.10**
- **VS Code 1.116.0**
- **Ollama 0.21.0** con modelli locali tier-based (cosmetic 7B / behavior 14B Q2 / escalation qwen3:30b MoE / reasoning deepseek-r1 / multimodal gemma4)
- **Aider 0.86.2** con wrapper CLI (`aider-cosmetic`, `aider-refactor`, `aider-groq`, `aider-cerebras`, `aider-gemini`, `aider-openai`)
- **Cloud tier 3** (free tier): Groq llama-3.3-70b (630 tok/s) + Cerebras llama-3.1-8b (733 tok/s) + Gemini 2.5 Flash + OpenAI gpt-4o-mini

## Roadmap sintetica (aggiornata post ADR-0014)
- **19/04**: ✅ setup base completato
- **20-22/04**: ✅ Ollama + Qwen stack + migrazione progetti + bench + RAM upgrade
- **22-23/04**: ✅ tier 3 cloud stack + quality bench + Fase 6 inaugurata
- **Fino 19/05 (Claude Max expiration)**: Fase 6 tracking compresso — target n≥20 dogfood + quality bench continuation
- **~20/05/2026**: ADR-0015 budget decision finale → target **full-sovereign $0-50/anno** (Ollama locale + cloud free-tier, **zero subscription ricorrenti**)

Per i dettagli operativi e le convenzioni di lavoro con Claude Code, vedi [CLAUDE.md](./CLAUDE.md). Per storia decisionale completa, `docs/adr/` (14 ADR).

## Autore
Eduardo Scarpelli · `eduscarpelli@gmail.com` · GitHub: [@MasterDD-L34D](https://github.com/MasterDD-L34D)

## Data creazione
19 aprile 2026
