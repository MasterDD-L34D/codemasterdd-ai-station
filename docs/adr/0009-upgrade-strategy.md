# ADR 0009 - Strategia di Evoluzione dello Stack AI Locale per il 2026-2027

## Status
Proposed

## Data
2023-04-21

## Decisore
Eduardo Scarpelli

## Tipo decisione
Strategia di evoluzione del stack AI locale

## Contesto
Il documento descrive la strategia di evoluzione dello stack AI locale per il 2026-2027, basata sui findings presenti nel file `docs\research\ai-stack-evolution-2026.md`.

## Opzioni analizzate
1. **Upgrade da Qwen 2.5 Coder a Qwen3-Coder-Next**
   - **Qwen3-Coder-Next** è un modello MoE con 80B parametri totali, 3B attivi in inference.
   - **Performance**: State-of-the-art su Agentic Coding, Browser-Use e Tool-Use.
   - **Benchmark**: SWE-Bench Verified, SWE-Bench Pro, Terminal-Bench 2.0.

2. **Upgrade hardware se Qwen3 MoE non fit su RTX 5060 8GB**
   - **Hardware options**:
     - RTX 5060 Ti 16GB: upgrade consumer, ~+8GB headroom.
     - Mac mini M4 Pro 48GB: unified memory, scala a modelli 30B+ comodamente.

3. **Conferma Aider continuity**
   - **Aider** è un repository attivo con 39K GitHub stars e 4.1M installs.
   - **Updates 2026**: support aggiunto per Gemini 2.5 pro/flash, OpenAI o1-pro / o3-pro con thinking tokens.

## Decisione
La decisione prevede di:
1. **Upgrade da Qwen 2.5 Coder a Qwen3-Coder-Next** se il benchmark verificato lo consente.
2. **Upgrade hardware** su RTX 5060 Ti 16GB o Mac mini M4 Pro 48GB se Qwen3 MoE non fit su RTX 5060 8GB.
3. **Confermare Aider continuity** per mantenere la continuità del workflow.

## Implicazioni
- **Qwen3-Coder-Next**: Migrazione a un modello più efficiente e di qualità superiore.
- **Hardware upgrade**: Possibilità di scalare al 30B+ parametri con hardware aggiornato.
- **Aider continuity**: Mantenimento del workflow CLI agentic senza interruzioni.

## Follow-up
1. Verifica il benchmark per Qwen3-Coder-Next.
2. Valutazione dell'hardware RTX 5060 Ti 16GB e Mac mini M4 Pro 48GB.
3. Conferma la continuità di Aider.

## Riferimenti
- [docs\research\ai-stack-evolution-2026.md](docs\research\ai-stack-evolution-2026.md)
