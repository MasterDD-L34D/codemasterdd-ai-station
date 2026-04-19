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
- **RAM**: 16GB DDR5
- **Storage**: SSD 1TB Micron NVMe
- **OS**: Windows 11 Home 25H2 (build 26200)

## Stack attivo
- **Claude Code 2.1.114** — agente CLI di sviluppo (OAuth Claude Max, Opus 4.7)
- **Git 2.53.0.windows.3**
- **NVIDIA Driver 595.79 + CUDA 13.2**

## Stack in arrivo
- Node.js 22 LTS, Python 3.10+, VS Code, GitHub CLI
- Ollama + Qwen 2.5 Coder 7B (runtime LLM locale)

## Roadmap sintetica
- **Oggi (19/04/2026)**: setup base completato
- **Settimana corrente**: Ollama + primo modello locale
- **Settimana prossima**: migrazione progetti reali (Evo-Tactics, Synesthesia)
- **Dal 20/05/2026**: zero subscription ricorrenti — Ollama primario + OpenRouter fallback

Per i dettagli operativi e le convenzioni di lavoro con Claude Code, vedi [CLAUDE.md](./CLAUDE.md).

## Autore
Eduardo Scarpelli · `eduscarpelli@gmail.com` · GitHub: [@MasterDD-L34D](https://github.com/MasterDD-L34D)

## Data creazione
19 aprile 2026
