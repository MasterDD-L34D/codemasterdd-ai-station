# Agno Ollama snippets — pattern riusabili senza framework adoption

Estratti dal cookbook Agno [`cookbook/90_models/ollama/chat/`](https://github.com/agno-agi/agno/tree/main/cookbook/90_models/ollama/chat). Valore: pattern Python minimi copia-incollabili per script ad-hoc (morning briefing, agent task ricorrenti, tool use locale) **senza adottare il framework Agno completo**. Allineato a ADR-0005 (YAGNI minimalism).

## Pattern 1 — Agent Ollama con tool use

Fonte: [cookbook/90_models/ollama/chat/tool_use.py](https://github.com/agno-agi/agno/blob/main/cookbook/90_models/ollama/chat/tool_use.py)

**Install one-time**: `pip install agno` (+ eventuali tool deps, es. `pip install duckduckgo-search` per WebSearch)

```python
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.websearch import WebSearchTools

agent = Agent(
    model=Ollama(id="qwen2.5-coder:7b"),  # swap con qualsiasi modello Ollama locale
    tools=[WebSearchTools()],
    markdown=True,
)
agent.print_response("Whats happening in France?", stream=True)
```

**Quando serve**:
- Morning briefing script (meteo/RSS/news via tool Python custom)
- Summarizer con retrieval web per domande puntuali
- Qualsiasi agent che deve combinare LLM + tool locale

**Come adattare**:
- Custom tool: `@tool` decorator su funzione Python qualsiasi, poi `tools=[my_tool]`
- Modello: `id="qwen3-coder:30b"` per task più complessi (tier 2 escalation)

## Pattern 2 — Agent con memoria persistente (skip-per-ora)

Fonte: [cookbook/90_models/ollama/chat/memory.py](https://github.com/agno-agi/agno/blob/main/cookbook/90_models/ollama/chat/memory.py)

Richiede **Postgres + pgvector via container**. Overkill per use case single-user locale.

**Alternativa pragmatica se serve memoria**: sostituire `PostgresDb` → `SqliteDb` (Agno supporta nativo). Oppure scrivere 30 righe con `sqlite3` stdlib senza Agno — decidere caso per caso.

## Quando NON usare Agno

Se lo script è <50 righe e fa 1 chiamata LLM senza tool/memory, `requests.post("http://localhost:11434/api/chat", ...)` diretto è più rapido. Agno ha senso solo quando `Agent + tools + optional memory` batte davvero uno script bare.

## Verdetto

- **Bookmark il cookbook**, non installare framework finché non serve.
- **Pattern 1 è safe to copy** se emerge use case real. ~15 righe, dep `agno` solo (MIT, Python puro).
- **Telemetria Agno**: `export AGNO_TELEMETRY=false` prima di import per disabilitare (allineato sovereign).
