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

## Sources citate

- https://github.com/QwenLM/Qwen3-Coder
- https://huggingface.co/Qwen/Qwen3-Coder-Next
- https://qwenlm.github.io/blog/qwen3-coder/
- https://www.marktechpost.com/2026/02/03/qwen-team-releases-qwen3-coder-next-an-open-weight-language-model-designed-specifically-for-coding-agents-and-local-development/
- https://github.com/Aider-AI/aider/releases
- https://www.opensourceaireview.com/blog/best-open-source-ai-coding-agents-in-2026-ranked-by-developers
- https://www.faros.ai/blog/best-ai-coding-agents-2026
