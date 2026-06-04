---
name: Curated external repos for Evo-Tactics
description: Tiered list of GitHub repos to study for tactical combat, AI, session engine, balance, narrative, tooling — with concrete extraction targets per repo
type: reference
---

# External Repo Reference Map (curated 2026-04-16)

4 priority tiers ranked by direct impact on Evo-Tactics architecture. 37 repo totali.

---

## Tier 0 — Analisi immediata (coding agent)

| Repo | Stars | Da estrarre per Evo-Tactics |
|---|---|---|
| [boardgame.io](https://github.com/boardgameio/boardgame.io) | 12.3k | Round flow, state authority, phases, AI bots, deterministic simulation, event log — match architetturale diretto col session engine |
| [xstate](https://github.com/statelyai/xstate) | 27.5k | Statecharts + actor model per round orchestrator, workflow UI, flussi multi-step. Già analizzato in sprint 019 |
| [wesnoth](https://github.com/wesnoth/wesnoth) | 5.6k | Separazione gameplay/contenuti/bilanciamento, telemetria partita, longevità progetto turn-based |
| [awesome-game-design](https://github.com/Roobyx/awesome-game-design) | — | Hub GDD pubblici, template, postmortem — benchmark per copertura design doc (loop, AI, economy, fail states) |
| [GDDMarkdownTemplate](https://github.com/LazyHatGuy/GDDMarkdownTemplate) | — | Matrice audit GDD: overview, gameplay, progressione, combat, economy, AI, technical — confronto con docs/core/ |
| [playwright](https://github.com/microsoft/playwright) | 68k | Già in uso. E2E, tracing, codegen, test isolation — investimento qualità su console e flow UI |

## Tier 1 — Architettura tattica / engine patterns

| Repo | Stars | Da estrarre |
|---|---|---|
| [OpenRA](https://github.com/OpenRA/OpenRA) | 15k | Content pipeline, modding, data-driven design, boundary engine/content — reverse-engineering patterns |
| [colyseus](https://github.com/colyseus/colyseus) | 6.8k | Node.js session authoritative, state sync, serializer — fit per co-op vs Sistema quando multiplayer diventa priorità |
| [open_spiel](https://github.com/google-deepmind/open_spiel) | 5.1k | MCTS + game theory + simulazione — balance testing d20, fairness analysis |
| [godot](https://github.com/godotengine/godot) | 93k | Organizzazione tooling, demo, docs, export multi-piattaforma — riferimento organizzativo |
| [bevy](https://github.com/bevyengine/bevy) | 37k | ECS data-oriented, modularità sistemi — concetti applicabili anche su Node/Python |
| [MonoGame](https://github.com/MonoGame/MonoGame) | 11.8k | Sample, loop, organizzazione cross-platform — riferimento classico framework |

## Tier 2 — Narrativa, dialoghi, content authoring

| Repo | Stars | Da estrarre |
|---|---|---|
| [ink](https://github.com/inkle/ink) | 4.2k | Narrazione ramificata, eventi testuali, briefing/debrief, scelte — se Evo-Tactics aggiunge narrative layer |
| [YarnSpinner](https://github.com/YarnSpinnerTool/YarnSpinner) | 2.4k | Dialoghi interattivi, formato semplice per writer, integrazione gioco |
| [Arrow](https://github.com/mhgolkar/Arrow) | 1.5k | Authoring narrativo visuale, nonlinear storytelling, export HTML, VCS-friendly |

## Tier 3 — Documentazione, DSL, pipeline AI, grid/pathfinding

| Repo | Stars | Da estrarre |
|---|---|---|
| [mermaid](https://github.com/mermaid-js/mermaid) | 74k | Docs-as-code: flowchart, sequence, state diagram per workflow esistenti |
| [langium](https://github.com/eclipse-langium/langium) | 1.8k | DSL builder: parser, code generator, LSP — se config/encounter template evolvono in linguaggio di dominio |
| [game-design-doc-generator](https://github.com/potnoodledev/game-design-doc-generator) | — | Genera GDD JSON da descrizione — bozze rapide moduli/encounter pack |
| [yuka](https://github.com/Mugen87/yuka) | 1.3k | Game AI JS: steering, goal-driven agents, fuzzy logic — applicabile a Sistema AI |
| [easystarjs](https://github.com/prettymuchbryce/easystarjs) | 1.9k | A* async JS per griglia — drop-in pathfinding |
| [AncientBeast](https://github.com/FreezingMoon/AncientBeast) | 1.8k | Tactical combat creatures su hex — reference combattimento tattico |
| [rpg_tactical_fantasy_game](https://github.com/Grimmys/rpg_tactical_fantasy_game) | 503 | Tactical RPG Python — comparabile a rules engine d20 |
| [libtcod](https://github.com/libtcod/libtcod) | 1.2k | FOV + pathfinding Python — applicabile a griglia tattica |
| [GOApy](https://github.com/jameswilliamknight/GOApy) | 50 | GOAP Python — usabile nel resolver AI Sistema |
| [gdx-ai](https://github.com/libgdx/gdx-ai) | 1.3k | Formation + behavior trees — reference per AI tattica |
| [rlcard](https://github.com/datamllab/rlcard) | 3.4k | RL framework strategy games — balance/fairness testing |
| [aitoolkit](https://github.com/lgrammel/aitoolkit) | 517 | FSM + BT + utility AI + GOAP — toolkit completo AI gamedev |
| [utility-ai](https://github.com/pschroeder89/utility-ai) | 19 | Utility AI Node.js — drop-in per decision-making Sistema |
| [godot-tactical-rpg](https://github.com/GDQuest/godot-tactical-rpg) | 891 | FFT-style reference — movement, grid, turn flow |
| [von-grid](https://github.com/vonWolfeworthy/von-grid) | 393 | Hex grid renderer — reference visualizzazione griglia |
| [HexGridUtilities](https://github.com/mkiael/HexGridUtilities) | 148 | Hex FOV + pathfinding — reference griglia esagonale |
| [pathfinding (Rust)](https://github.com/samueltardieu/pathfinding) | 1.1k | High-perf pathfinding — benchmark algoritmi |
| [LockstepEngine](https://github.com/JiepengTan/LockstepEngine) | 947 | Deterministic multiplayer — reference sync deterministico |
| [ReGoap](https://github.com/luxkun/ReGoap) | 1.1k | GOAP C# — reference architettura goal-oriented AI |
| [awesome-game-engine-dev](https://github.com/stevinz/awesome-game-engine-dev) | 1.3k | Engine dev resources — meta-lista strumenti engine |
| [magictools](https://github.com/ellisonleao/magictools) | 16.5k | Meta-risorsa massiva gamedev — coprire gap strumenti |
| [awesome-game-ai](https://github.com/datamllab/awesome-game-ai) | 953 | Multi-agent RL, imperfect info — reference AI avanzata |
| [ai-game-devtools](https://github.com/simoninithomas/ai-game-devtools) | 1.1k | AI tools tracker — panoramica strumenti AI gamedev |
| [2DGD_F0TH](https://github.com/2DGD-F0TH/2DGD_F0TH) | 450 | Ebook 500+ pagine game dev — reference teoria completa |
