# AI Stack Evolution — State of the Art 2026

Research snapshot (2026-04-21) per supportare ADR-0009 decision su trigger upgrade stack.

## Qwen3-Coder-Next (released Feb 2026)

- **Architecture**: MoE (Mixture of Experts), 80B total parameters, **3B active** at inference
- **Context**: 256K tokens native, 1M con estrapolazione Yarn
- **Performance**: State-of-the-art open model su Agentic Coding, Agentic Browser-Use, Agentic Tool-Use — comparabile a Claude Sonnet 4
- **Benchmark**: SWE-Bench Verified, SWE-Bench Pro, SWE-Bench Multilingual, Terminal-Bench 2.0, Aider — match o supera MoE più grandi con 10-20x active params
- **Training**: large corpus di executable tasks + reinforcement learning per planning, tool calls, recovery da runtime failures long-horizon
- **License**: open weight
- **Varianti**: Qwen3-Coder-480B-A35B-Instruct (480B/35B active, flagship), Qwen3-Coder-30B-A3B-Instruct, Qwen3-Coder-Next (80B/3B, sweet spot local)
- **Source**: https://github.com/QwenLM/Qwen3-Coder, https://huggingface.co/Qwen/Qwen3-Coder-Next, blog ufficiale https://qwenlm.github.io/blog/qwen3-coder/

## VRAM footprint MoE vs dense

Per modelli MoE, la VRAM richiesta a inference dipende principalmente da:
1. **Active params** (quelli effettivamente computati per token)
2. **KV cache** (context length dependent)
3. Weights totali vanno caricati in RAM/VRAM ma sparsamente attivati

Per Qwen3-Coder-Next (80B/3B attivi):
- Weights totali in Q4: ~40 GB (non cap in 8GB VRAM)
- Ma se Ollama/llama.cpp supporta MoE offloading, solo expert attivi in VRAM → footprint effettivo ~3-5 GB
- **Implica**: on RTX 5060 8GB potenzialmente viable, da confermare post supporto Ollama

Hardware upgrade options (da valutare se Qwen3 MoE non fit):
- RTX 5060 Ti 16GB: upgrade consumer, ~+8GB headroom
- Mac mini M4 Pro 48GB: unified memory, scala a modelli 30B+ comodamente
- Status quo 5060 8GB: OK per dense 7-14B Q2

## Aider (Status 2026)

- **Attività**: repo attivo, 39K GitHub stars, 4.1M installs, 15B tokens/settimana processati
- **Updates 2026**: support aggiunto per Gemini 2.5 pro/flash, OpenAI o1-pro / o3-pro con thinking tokens
- **Architettura**: git-native CLI, diff-first review loop, multi-edit-format
- **Niche**: "seasoned Git-native pair programmer with steep preference curve but unmatched diff-first review loop"
- **Market position vs competitor 2026**: ancora top-tier per workflow CLI agentic, ma emergono alternative (OpenCode, Continue.dev, Roo Code)
- **Source**: https://github.com/Aider-AI/aider/releases

## OpenCode — alternativa client valutata 2026-04-21

OpenCode (117k GitHub stars) valutato come alternativa ad Aider. Decisione: **mantenere Aider**. Tre motivi:

1. **Windows-nativo**: Aider gira nativo, OpenCode raccomanda WSL → overhead setup non giustificato
2. **Diff-first review loop** allineato al workflow sovereign consolidato (ADR-0008)
3. **Claude Code-compatibilità di OpenCode**: legge nativamente `CLAUDE.md`, `.claude/skills/*`, con fallback `AGENTS.md` → `CLAUDE.md`. Portabilità del codex a costo zero se un giorno serve switchare

Implicazione sovereign: il codex `CLAUDE.md` + `.claude/` è client-portabile by design.

Trigger re-valutazione = ADR-0009 T3 (Aider >6 mesi senza commit upstream, o breakthrough concorrente senza migration cost).

Sources: https://opencode.ai/docs/rules/, https://opencode.ai/docs/skills/

## OpenRouter — rate limits e pool fallback (2026-04-21)

Rate limits reali (fonte https://openrouter.ai/docs/api/reference/limits):

- **No crediti acquistati**: 50 richieste/giorno **totali** (aggregato su tutti i modelli `:free`, non per-modello), 20 req/min
- **Con ≥$10 crediti one-time**: 1000 richieste/giorno totali, 20 req/min. Soglia $10 è permanente — la quota alta resta anche se balance scende sotto

Caveat operativi:
- **Failed requests count verso quota**: 429, provider throttling upstream, timeout Cloudflare — tutti consumano quota. Retry storm esaurisce quota rapidamente
- **Provider throttling upstream**: singoli modelli possono throttle in peak hours indipendentemente da quota personale
- **Volatilità free tier**: modelli `:free` possono uscire dal tier senza preavviso → pool fallback esteso richiesto

### Scenari budget aggiornati

| Scenario | Costo | Viable per |
|----------|-------|------------|
| Solo Ollama locale (stack attuale) | €0/mese | Cosmetic + refactor + escalation tier 2 (validato Fase 4) |
| Ollama + OpenRouter free no-credit | €0 + 50 req/day | Troppo stretto per uso agentico serio |
| Ollama + OpenRouter con $10 one-time | **$10 + €0-5/mese** | Tier 2 reale come fallback opportunistico |
| Ollama + OpenRouter paid saltuari | €5-20/mese | Task frontier non gestibili localmente |

### Trigger condizionali riattivazione (non raccomandazione attiva)

1. Fase 6 rivela fail rate Aider+Ollama >30% non risolvibile con reflection retry o switch modello locale → bridge OpenRouter finché T2 hardware non attiva
2. Trigger T1 ADR-0009 fallisce (MoE non fit, performance insufficiente) + T2 non giustificabile → gap-filler temporaneo
3. Scenario offline-impossibile singolo: task frontier raro, no voglia di Claude Pro fisso

Sources: https://openrouter.ai/docs/api/reference/limits, https://openrouter.ai/collections/free-models

## Ollama / llama.cpp ecosystem

- Ollama continua supporto multi-model
- MoE support in llama.cpp upstream (aggiungere verifica per Qwen3 specifico quando pianifichiamo upgrade)
- Verificare `ollama.com/library/qwen3-coder` al momento decisione

## Implicazioni per stack CodeMasterDD

Stack corrente (post-ADR-0008):
- Qwen 2.5 Coder 7B Q4_K_M (cosmetic) — 114 tok/s
- Qwen 2.5 Coder 14B Q2_K (behavior-critical) — 18.7 tok/s base, 25.5 con ctx 8192
- Aider 0.86.2
- RTX 5060 8GB + Ollama 0.21.0

Potenziale upgrade (2026-2027):
- **Qwen 2.5 → Qwen3-Coder-Next**: MoE efficiency + agentic quality jump vs 14B Q2 dense
- **Aider continuity**: nessun trigger a switchare, stay
- **Hardware**: stay finché MoE footprint fit, altrimenti 5060 Ti 16GB o Mac mini

Trigger candidates per upgrade modello:
1. Ollama official support Qwen3-Coder-Next con benchmark verificato
2. ADR-0008 fail rate dati Fase 6 > 30% → stack insufficiente, upgrade necessario
3. Emergenza task blocker non gestibile da 14B Q2 (es. multi-file refactor complesso)

## Framework "5 Levels of Agentic Software" (Agno, marzo 2026)

Modello mentale progressivo per roadmap agent: **L1** stateless+tool → **L2** session+knowledge → **L3** self-learning (agentic memory) → **L4** multi-agent teams → **L5** production runtime. Regola d'oro: ogni livello aggiunge complessità pagabile solo quando il precedente è al suo limite (allineato ADR-0005 YAGNI).

Posizionamento attuale CodeMasterDD: **L2 sofisticato con routing deterministico custom** (hub Claude Code → dual-stack Aider + tier 2 qwen3:30b). Non giustificato salto a L3/L4 con evidenza empirica n=5+ di ADR-0008. Framework utile come linguaggio comune in futuri ADR di roadmap.

Source: https://www.agno.com/blog/the-5-levels-of-agentic-software-a-progressive-framework-for-building-reliable-ai-agents

## Sources citate

- https://github.com/QwenLM/Qwen3-Coder
- https://huggingface.co/Qwen/Qwen3-Coder-Next
- https://qwenlm.github.io/blog/qwen3-coder/
- https://www.marktechpost.com/2026/02/03/qwen-team-releases-qwen3-coder-next-an-open-weight-language-model-designed-specifically-for-coding-agents-and-local-development/
- https://github.com/Aider-AI/aider/releases
- https://www.opensourceaireview.com/blog/best-open-source-ai-coding-agents-in-2026-ranked-by-developers
- https://www.faros.ai/blog/best-ai-coding-agents-2026
