# Evo-Tactics — Guida Ecosistema (basi reali, file-cited)

> Guida operativa per continuare il progetto. Costruita 2026-05-18 da audit
> diretto dei 7 repo (gh API + clone locali). Ogni file citato e' verificato
> presente al momento dell'audit. Repo daily-ship (Game/Godot/Game-Database)
> evolvono in ~2gg: i path strutturali restano stabili, gli HEAD/PR no --
> ri-verifica con `gh` prima di azioni puntuali.

---

## 0. Mappa mentale corretta

La mappa iniziale aveva 3 etichette imprecise. Versione verificata:

```
codemasterdd-ai-station   policy + infra + ADR (rulebook workstation, NO codice gioco)
evo-swarm (Dafne)         orchestratore agenti AI runtime (governa specialist -> content)
        | produce content
Game (Vue3)               simulation core + gameplay loop + backend Express VIVO
Game-Godot-v2             shell visuale + UX, client Godot 4.x VIVO (frontend canonical futuro)
Game-Database             taxonomy CMS (trait/biome/specie/ecosistemi) -> feed Game Vue3
evo-tactics-refs-meta     pipeline asset reference (3D/2D/SFX, rebuildable, no binari)
vault                     knowledge base Obsidian sovereign (fonte verita' design + ricerca)
```

Correzioni chiave vs mappa iniziale:
- **Game NON e' archivio morto.** E' il core simulation + backend Express,
  attivo in parallelo a Godot-v2 (parallel-run port phase). Piano: Godot-v2
  diventa frontend canonical e Vue3 -> archive, ma decisione futura non ancora
  eseguita codebase-wide.
- **Coordinatore = evo-swarm (Dafne), NON codemasterdd.** codemasterdd e'
  infrastruttura + regole + ADR; non esegue agenti runtime.
- **Game-Database alimenta Game Vue3**, non Godot direttamente.

---

## 1. Game (Evo-Tactics Vue3) — simulation core + backend

| Campo | Valore |
|-------|--------|
| Remote | `github.com/MasterDD-L34D/Game` (PUBLIC) |
| Path locale | `C:\dev\Game` |
| Stack | Node 22 (compat Node 24) + Python 3.10, Express, Vue3, xstate@5, inkjs |
| Ruolo | Simulation engine d20 + backend API + dataset canonical + gameplay loop |
| Stato | VIVO, daily-ship (~200 PR / 14gg in cluster recenti) |

### Struttura directory

| Dir | Contenuto |
|-----|-----------|
| `apps/backend/` | Express API (port 3334) + WS (3341) -- Idea Engine, session orchestration |
| `apps/play/` | Frontend Vue3 (Vite, port 5180) -- secondario, render 2D legacy |
| `apps/mission-console/`, `apps/trait-editor/`, `apps/analytics/` | Tooling UI |
| `services/` | Microservizi: triSorgente (bridge d20), generation, ai, difficulty, replay, party, narrative, eventsScheduler |
| `packages/contracts/` | Schemi AJV + tipi TS condivisi (seam cross-stack) |
| `engine/` | `tri_sorgente_worker.py` -- worker Python regole d20 |
| `data/core/` | Dataset canonical YAML: species, biomes, traits, mating, difficulty, i18n |
| `packs/evo_tactics_pack/` | Pack ecosistema v1.7 self-contained (sorgente per Game-Database import) |
| `docs/core/` | Game design docs (GDD, regole, sistema tattico) |
| `docs/adr/` | ADR architetturali game-side (date-named, es. ADR-2026-05-05) |

### File piu' importanti

| File | Scopo |
|------|-------|
| `README.md` | Mappa monorepo, policy playtest-first, commit style |
| `CLAUDE.md` | Guardrail agent: caveman, verify-before-claim, museum-first, encoding |
| `package.json` | Workspace + 50+ script root (dev:stack, test:stack, start:api) |
| `apps/backend/index.js` | Entry: Express :3334, WS :3341, integrazione Game-Database :3333, Prisma |
| `apps/backend/services/combat/` | ~30 file: archetipi, mutazioni, biome modifier, sinergie, morale, elevazione (core tattico d20) |
| `apps/backend/routes/session.js` | Orchestrazione sessione co-op (~1967 LOC, sorgente port Godot) |
| `services/triSorgente/bridge.js` | Bridge Node <-> worker Python d20 (`engine/tri_sorgente_worker.py`) |
| `apps/play/src/main.js` | Frontend Vue3: phase-coordinator, render engine, pannelli UI |
| `docs/core/00-GDD_MASTER.md` | Game Design Document canonical (visione, pilastri, d20, specie, biomi) |
| `docs/core/90-FINAL-DESIGN-FREEZE.md` | Scope shipping + vincoli architetturali (A3 canonical) |
| `docs/core/10-SISTEMA_TATTICO.md` + `11-REGOLE_D20_TV.md` | Layer tattico + sistema d20 |
| `docs/adr/ADR-2026-05-05-cutover-godot-v2-fase-3-formal.md` | Decisione cutover Godot primario / web v1 fallback |

### Build & run

```bash
npm ci                    # install root + workspace
npm run prepare           # husky hooks
npm run dev:stack         # backend + frontend Vite
npm run start:api         # solo backend :3334
npm run play:dev          # solo frontend Vue3 :5180
npm run test:stack        # suite cross-stack (~150 AI test + 196 Python)
```

### Integrazione cross-repo

- **-> Game-Godot-v2**: backend condiviso. Godot consuma via HTTPClient + WS,
  zero duplicazione logica. README dichiara primary frontend = Godot v2 phone HTML5.
- **<- Game-Database**: trait glossary via `GET ${GAME_DATABASE_URL}/api/traits/glossary`
  se `GAME_DATABASE_ENABLED=true` (ADR-2026-04-14 Alt B), altrimenti fallback locale.
- **<- evo-swarm (Dafne)**: Dafne scrive content in `agents/` / `.ai/` + draft issue.
- **<- evo-tactics-refs-meta**: asset finali entrano in `assets/` via output-staging.

---

## 2. Game-Godot-v2 — client visuale Godot (frontend canonical futuro)

| Campo | Valore |
|-------|--------|
| Remote | `github.com/MasterDD-L34D/Game-Godot-v2` (PRIVATE) |
| Path locale | `C:\dev\Game-Godot-v2` (clone 2026-05-07) |
| Stack | Godot 4.6.2 LTS, GDScript, GUT test framework |
| Ruolo | Shell visuale + UX + esperienza native engine. NO Node/Vue/Python |
| Stato | VIVO, daily-ship (~282 PR cumulative). Deploy prod evo-tactics.com |

### Struttura

| Item | Path | Dettaglio |
|------|------|-----------|
| Config progetto | `project.godot` | Godot 4.6.2, forward_plus, viewport mobile 480x854 |
| Main scene | `scenes/PhoneComposerBoot.tscn` | Boot -> `scenes/phone/PhoneComposer.tscn` |
| Scene core | `scenes/Main.tscn`, `Unit.tscn`, `HudView.tscn`, `CTBarHud.tscn` | Combat/HUD/Unit runtime |
| Script | `scripts/session/`, `scripts/combat/`, `scripts/ai/`, `scripts/net/` | Logica gioco |
| Dati | `data/lifecycle/`, `data/species/`, `data/biomes/`, `data/traits/` | Resource JSON/YAML |
| Test | `tests/unit/` | 429 test GUT (~1499 assert, ~56s headless) |
| Addons | `addons/` | gut, phantom_camera, beehave (AI tree), dialogue_manager, AsepriteWizard, ldtk_importer |
| Docs | `docs/godot-v2/` | architecture, sprint, deploy, deferred-roadmap |

### File piu' importanti

| File | Scopo |
|------|-------|
| `project.godot` | Config engine (versione locked, no drift) |
| `CLAUDE.md` | Guardrail sprint, DoD 4-gate, regola 50-LOC, museum/vault reference |
| `AGENTS.md` | Status sprint + topologia sibling repo + workflow cross-repo (per Codex) |
| `.claude/SAFE_CHANGES.md` | Decision tree gate safe/yellow/red (docs/refactor/gameplay/schema) |
| `.claude/TASK_PROTOCOL.md` | Protocollo 7-fase esecuzione task (orient->map->plan->execute->verify) |
| `scripts/session/round_orchestrator.gd` | Resolver d20, dispatch azione, ciclo DOT, status apply (core loop) |
| `scripts/combat/d20_resolver.gd` | Hit/miss/damage + Margin-of-Success + resist (port bit-exact da session.js) |
| `scripts/ai/vc_scoring.gd` | 20+ metriche raw + aggregati + inferenza MBTI/Enneagramma (AI engine) |
| `scripts/session/mating_trigger.gd` | Predicato lifecycle<->breeding + enrichment specie figlio |
| `data/lifecycle/lifecycles.json` | 15 specie, fasi lifecycle (hatchling->juvenile->mature->apex->legacy) |
| `docs/godot-v2/architecture/combat-resolver.md` | Spec port logica d20 da session.js |
| `docs/godot-v2/architecture/net-stack.md` | Spec HTTP + WS, endpoint, JWT, CORS, target latenza |
| `docs/godot-v2/visual-screen-bible.md` | Bibbia visiva 3-modi (World/Tactical/Memory) |

### Run & test

```bash
godot --path .                                    # apre progetto (Godot 4.6.2)
# main scene: res://scenes/PhoneComposerBoot.tscn
godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://tests/unit -gexit   # 429 test ~56s
```

### Deploy produzione

| Item | Valore |
|------|--------|
| Tunnel | Cloudflare Named Tunnel `evo-tactics-prod` |
| Dominio | `evo-tactics.com` (Cloudflare Registrar ~$10/anno) |
| Route | `evo-tactics.com *` -> `http://localhost:3334` (REST + WS condivisi) |
| Token | `~/.cloudflared/evo-tactics-prod.token` (chmod 600, MAI commit) |
| Script | `tools/deploy/named-tunnel.sh` (backend Game/ prima, poi tunnel) |
| Checklist | `docs/godot-v2/deploy-master-dd-checklist.md` |
| Requisito backend | `LOBBY_WS_SHARED: "true"` in docker-compose.yml Game/ |

### Integrazione

Backend NON duplicato: Godot consuma `Game/` Express via HTTPClient + WS.
Workflow port: edita spec/dataset su `Game/` (canonical) -> sync a Godot
quando si porta (Sprint ETL). Telemetry gate CI: `test_biome_focus_telemetry_export.gd`
rigenera `data/derived/atlas-telemetry/biome-focus.jsonl` (CI fail se drift).

---

## 3. Game-Database — taxonomy CMS

| Campo | Valore |
|-------|--------|
| Remote | `github.com/MasterDD-L34D/Game-Database` (PUBLIC, no LICENSE) |
| Path | Ryzen `C:\Users\VGit\Documents\GitHub\Game-Database` (no clone Lenovo) |
| Stack | Express 4 + Prisma 5 + PostgreSQL 16 + React 18 (MUI + TanStack + Vite) |
| Ruolo | Glossario canonical trait/biome/specie/ecosistemi -> feed Game Vue3 |
| Stato | Attivo, pipeline multi-AI (Jules + Codex + Claude Code) |

### Struttura

- **Backend**: `server/` -- `server/index.js` (HTTP :3333), `server/app.js` (factory Express)
- **Schema**: `server/prisma/schema.prisma` (PostgreSQL 16, 10 model)
- **Route**: `server/routes/` (9 moduli REST CRUD + junction)
- **Import**: `server/scripts/evo-import.js` + `server/scripts/ingest/import-taxonomy.js`
- **Frontend**: `apps/dashboard/` (React + Vite :5174)

### File piu' importanti

| File | Scopo |
|------|-------|
| `server/prisma/schema.prisma` | 10 model: Trait, Biome, Species, Ecosystem + 4 junction + Record + AuditLog |
| `server/index.js` | Entry server Express (default 0.0.0.0:3333) |
| `server/app.js` | Factory Express: CORS, basicAuth, user context, route binding |
| `server/scripts/ingest/import-taxonomy.js` | Core ingest: legge pack Game, valida, upsert by slug in Postgres |
| `server/scripts/evo-import.js` | CLI wrapper import (dev:setup + delega import-taxonomy) |
| `server/schemas/glossary.schema.json` | Contratto shape glossary (mirror Game packages/contracts) |
| `CLAUDE.md` | Overview, topologia sibling, port dev, endpoint integrazione |
| `WORKSPACE_MAP.md` | Layout workspace + bootstrap + smoke + data flow |
| `README.md` | Quick-start Docker/npm, matrice test, CI, LAN mode |

### Data model (Prisma)

- **Master**: `Trait` (dataType BOOLEAN/NUMERIC/CATEGORICAL/TEXT, tier, family),
  `Biome` (parentId gerarchia, climateTags, hazard), `Species` (tassonomia
  kingdom..epithet, trophicRole, playableUnit, morphotype), `Ecosystem` (region, climate)
- **Junction**: `SpeciesTrait`, `SpeciesBiome` (presence: resident/migrant/endemic),
  `EcosystemBiome`, `EcosystemSpecies` (role: keystone/dominant/engineer/invasive)
- **Aux**: `Record` (generico, stato Attivo/Bozza/Archiviato), `AuditLog` (CREATE/UPDATE/DELETE)

### Run

```bash
docker compose up -d db                       # Postgres 16 host :5433
npm run dev:setup                             # prisma generate + migrate + seed
npm run dev                                   # Express :3333
npm run evo:import -- --repo <PATH_TO_GAME>   # import idempotent by slug
npm run prisma:studio                         # browser DB :5555
# frontend: cd apps/dashboard && npm run dev  # :5174
```

### Integrazione con Game

- **Build-time** (default): `npm run evo:import -- --repo <Game>` legge
  `packs/evo_tactics_pack/docs/catalog/` (trait_glossary.json, *.ecosystem.yaml,
  *.biome.yaml), upsert by slug.
- **Runtime HTTP** (opt-in): `GET /api/traits/glossary` (no auth). Game backend
  setta `GAME_DATABASE_ENABLED=true` per fetch HTTP invece di fallback locale.
- Topologia canonical: `Game/docs/adr/ADR-2026-04-14-game-database-topology.md`.

---

## 4. evo-tactics-refs-meta — pipeline asset reference

| Campo | Valore |
|-------|--------|
| Remote | `github.com/MasterDD-L34D/evo-tactics-refs-meta` (PRIVATE) |
| Path | remote-only (no clone Lenovo) |
| Stack | Python (download tooling) + manifest JSON + URL lists |
| Ruolo | Meta-backup asset reference (3D/2D/concept/SFX), NO binari, rebuildable |
| Stato | Idle (push 2026-04-29), layer asset legittimo |

### File piu' importanti

| File | Scopo |
|------|-------|
| `README.md` | Tier policy + confini legali (CC0 safe, Tier B/C banditi) |
| `HANDOFF.md` | Handoff workspace, tool installati |
| `SKIV_REFS_EXTRACTED.md` | Registry asset direct-use creatura Skiv (wolf 3D, biome, concept) |
| `CATALOG.md` + `CATALOG_skiv.json` | Picks curati da dataset HF OGA-CC0 |
| `CC0_SOURCES.md` | Log provenance licenze |
| `robust_download.py` | Downloader atomico (retry backoff, zip-validate, 3 worker) |
| `gen_manifest.py` | Catalogazione post-download (schema builder) |
| `urls-*.txt` | Manifest sorgenti: 3d-art, hf-2d-art, hf-concept-art, hf-sound-effect, sonniss-gdc |
| `STATUS.md` / `WORKSPACE.md` | Stato workspace + folder map + quick-start |

### Workflow rebuild asset

```
urls-*.txt  ->  robust_download.py  ->  references/  ->  gen_manifest.py (catalog)
                                                       ->  output-staging  ->  C:\dev\Game\assets\
```

Nessun binario versionato (repo leggero, rebuildable). Conformita' licenze:
solo CC0/Public Domain/Sonniss royalty-free, zero estrazioni Tier B/C.

---

## 5. evo-swarm (Dafne) — orchestratore agenti AI

| Campo | Valore |
|-------|--------|
| Remote | `github.com/MasterDD-L34D/evo-swarm` (PRIVATE) |
| Path | `C:\Users\edusc\Dafne\workspace\swarm` (git separato, NON in C:\dev) |
| Stack | Python 3.12 + Flask + Ollama (qwen3:8b governance) + CAMEL framework |
| Ruolo | Coordinatrice + memory keeper che governa specialist -> content per Game |
| Stato | Stable post-dashboard sprint (Atto 2). Idle da ~2026-05-08 |

Dafne non e' solo scheduler: e' persona deliberata (INFP, SOUL.md + IDENTITY.md)
che governa agenti Scout/Solver/Builder/Specialist via CAMEL.

### File piu' importanti

| File | Scopo |
|------|-------|
| `camel-agents/api_server.py` | Flask app :5000, health, workflow approve-agent |
| `camel-agents/orchestrator.py` | Loading agent, integrazione Game repo, dispatch Ollama |
| `camel-agents/dafne.py` | Logica governance Dafne, creazione agent, flint watch |
| `agents/Dafne/IDENTITY.md` | Persona Dafne, valori, red line |
| `agents/Scout/IDENTITY.md` | Persona Scout (ricercatore) |
| `docs/pipeline-swarm-to-game.md` | Spec pipeline artifact, gate integrazione, soglie confidence |
| `START-SWARM.ps1` | Launch script (env setup + api_server + swarm_loop) |
| `swarm-to-game-export.py` | Export artifact filtrati -> Game repo target_files + draft issue |

### Endpoint principali (dashboard `http://localhost:5000`)

- `/api/status` -- orchestrator + Ollama health
- `/api/health` -- composito (Ollama/Game-repo/telemetry/escalation)
- `/api/dafne/status` -- stato Dafne + approval pending
- `/api/dafne/approve-agent` -- approvazione manuale specialist (POST, H5 gate)
- `/dafne` -- chat personale Dafne (persistence `workspace/memory/dialoghi/`)

### Avvio

```powershell
cd C:\Users\edusc\Dafne\workspace\swarm
.\START-SWARM.ps1            # -> dashboard http://localhost:5000
```

### Workflow content -> Game

Dafne propone agent -> Eduardo approva via `POST /api/dafne/approve-agent`
-> H5 gate (similarity check anti-duplicato) -> scrittura Game `.ai/` +
`agents_index.json` + `docs/exports/EXPORT-FOR-GAME-REPO-*.md` + draft issue.
NO auto-merge: review Eduardo manuale.

---

## 6. vault — knowledge base sovereign (fonte verita')

| Campo | Valore |
|-------|--------|
| Remote | `github.com/MasterDD-L34D/vault` (PRIVATE) |
| Path | `C:\dev\vault-shared` (clone downstream; origin Ryzen `C:\Users\VGit\Vault`) |
| Stack | Obsidian ACCESS + Karpathy LLM-wiki + Ollama LAN + 7 production agent |
| Ruolo | Knowledge base + archivio ricerca. Fonte verita' design Evo-Tactics |
| Privacy | **sovereign-only** (NON in aider-privacy-whitelist, aider-cloud = ABORT) |

### Struttura (pattern ACCESS)

- `Atlas/` -- MOC, indici tematici
- `Cards/` -- note atomiche evergreen (1 idea = 1 file)
- `Sources/raw/` -- PDF/web clip immutabili
- `Spaces/` -- progetti: **Dev/Evo-Tactics**, Synesthesia, UniUPO, GDR, GPT-Prompts
- `Extras/config/` -- `llm-routing.json` (matrice routing v1.0)
- `production/agents/` -- 7 agent live

### File / dir piu' importanti

| Path | Scopo |
|------|-------|
| `README.md` + `CLAUDE.md` | Operating rules, Quality Gate 3-step, frontmatter schema |
| `Extras/config/llm-routing.json` | Matrice routing v1.0 (Claude reasoning / Ollama bulk / embeddings) |
| `production/agents/evo-tactics-design-watcher.md` | Agent watcher design Evo-Tactics |
| `Spaces/Dev/Evo-Tactics/core/` | Design canonical: 01-VISIONE, 02-PILASTRI, 10-SISTEMA_TATTICO, 20-SPECIE_E_PARTI, 90-FINAL-DESIGN-FREEZE |
| `Spaces/Dev/Evo-Tactics/adr/` | 39 ADR architetturali game-design (dal 2026-04-13) |
| `Spaces/Dev/Evo-Tactics/governance/` | docs_registry.json (SSoT), GLOSSARY.md, workstream_matrix.json |
| `docs/research/` | ~22 doc Quality Gate Step 2 (es. evo-tactics-design-watcher) |

**Il design canonical di Evo-Tactics vive QUI** (`Spaces/Dev/Evo-Tactics/`),
non nei repo codice. I repo Game/Godot implementano; vault e' la fonte verita'
di visione, pilastri, ADR di game-design, glossario.

---

## 7. codemasterdd-ai-station — policy + infrastruttura

| Campo | Valore |
|-------|--------|
| Remote | `github.com/MasterDD-L34D/codemasterdd-ai-station` (PRIVATE) |
| Path | `C:\dev\codemasterdd-ai-station` |
| Ruolo | Policy hub + ADR + dashboard + infra. **ZERO codice gioco** |
| Stato | Fase 6+7 CLOSED, SPRINT_02 attack mode |

NON e' il coordinatore runtime (quello e' Dafne). E' il rulebook: hardware,
tier routing modelli, ADR decisioni, monitoring cross-repo.

### File piu' importanti

| File | Scopo |
|------|-------|
| `CLAUDE.md` | Operating rules autoritative: hardware, tier routing, convenzioni, protocolli cognitivi |
| `PROJECT_BRIEF.md` | Scope: sostituire Claude Max con stack sovereign $0-50/anno |
| `STATUS_MULTI_REPO.md` | Dashboard operativa cross-repo (15 repo monitored) |
| `MODEL_ROUTING.md` | Why strategico routing modelli (vs CLAUDE.md = how) |
| `DECISIONS_LOG.md` / `OPEN_DECISIONS.md` / `BACKLOG.md` / `ROADMAP.md` | Governance append-only + pending + backlog + fasi |
| `docs/adr/` | 33 ADR numerati (0001-0033) |
| `.claude/agents/` | 18 sub-agent (5 core + 4 Game + 2 Dafne + 3 quality + 2 DB + 2 meta) |
| `apps/cross-repo-dashboard/` | Dashboard daily-use (port 8081) |
| `infra/` | Docker stack ADR-0017 (LiteLLM :4000, Langfuse :3000, Postgres :5432) |

ADR rilevanti ecosistema: ADR-0001 (sovereign strategy), ADR-0013 (cloud free
tier), ADR-0021 (multi-client governance), ADR-0023 (Claude API post-Max),
ADR-0026 (cognitive protocols), ADR-0027 (refresh-verify).

---

## 8. Data flow cross-repo

```
                          vault (fonte verita' design)
                                |  visione + pilastri + ADR game-design
                                v
   evo-tactics-refs-meta   Game-Database              evo-swarm (Dafne)
   (asset pipeline)        (taxonomy CMS)              (agenti AI)
        |                       |                          |
   assets/ staging         npm run evo:import          .ai/ + draft issue
        |                  OR GET /api/traits/glossary      |
        v                       v                          v
   +-------------------------------------------------------------+
   |                    Game (Vue3) -- simulation core            |
   |   apps/backend Express :3334 + WS :3341 + d20 worker Python   |
   +-------------------------------------------------------------+
                                |  HTTPClient + WS (no logica dup)
                                v
                  Game-Godot-v2 -- client visuale
                  deploy -> evo-tactics.com (Cloudflare tunnel)

   codemasterdd-ai-station: governance/ADR/monitoring (osserva tutto, scrive nulla nei game repo)
```

Punti integrazione verificati (file-cited):
- Game `apps/backend/index.js` -- documenta WS :3341 + Game-DB :3333
- Game-Database `server/scripts/ingest/import-taxonomy.js` -- legge `packs/evo_tactics_pack/`
- Godot consuma backend via `scripts/net/` (HTTPClient/WebSocketClient)
- Dafne `swarm-to-game-export.py` -- scrive Game `docs/exports/`
- ADR-2026-04-14 (Game) -- topologia Game-Database
- ADR-2026-05-05 (Game) -- cutover Godot v2 primario

---

## 9. Come continuare il progetto — workflow concreti

### Modificare game-design (visione/pilastri/regole)
1. Fonte verita' = vault `Spaces/Dev/Evo-Tactics/core/` + `adr/`
2. Decisione architetturale -> nuovo ADR in vault `Spaces/Dev/Evo-Tactics/adr/`
3. Implementazione -> repo Game (logica) e/o Godot (UX)

### Aggiungere/modificare trait, specie, biomi
1. Editare in Game-Database (dashboard React :5174 o seed)
2. `npm run evo:import` per sync, OR runtime `GAME_DATABASE_ENABLED=true`
3. Verifica contratto `server/schemas/glossary.schema.json`

### Lavorare sulla simulazione / combat d20
- Logica canonical: Game `apps/backend/services/combat/` + `routes/session.js`
- Worker regole: Game `engine/tri_sorgente_worker.py` via `services/triSorgente/bridge.js`
- Test: `npm run test:stack`

### Lavorare su UX / visuale
- Game-Godot-v2 `scripts/` + `scenes/`. Leggere PRIMA `.claude/SAFE_CHANGES.md`
  + `.claude/TASK_PROTOCOL.md` + `CLAUDE.md` (regola 50-LOC)
- Test: GUT headless `tests/unit/`
- Deploy: `tools/deploy/named-tunnel.sh` -> evo-tactics.com

### Asset 3D/2D/SFX
- evo-tactics-refs-meta: `urls-*.txt` -> `robust_download.py` -> staging -> Game `assets/`

### Generare content via agenti AI
- Dafne: `START-SWARM.ps1` -> propone -> `POST /api/dafne/approve-agent` -> Game

### Decisioni infra / modelli / budget
- codemasterdd `docs/adr/` + `OPEN_DECISIONS.md`. NON tocca codice gioco.

---

## 10. Ordine di lettura raccomandato (nuova sessione)

1. Questo file -- mappa ecosistema
2. vault `Spaces/Dev/Evo-Tactics/core/01-VISIONE.md` + `02-PILASTRI.md` -- cosa e' il gioco
3. Repo target: `CLAUDE.md` (Game o Godot) -- guardrail operativi
4. Game `docs/core/00-GDD_MASTER.md` -- design master
5. codemasterdd `STATUS_MULTI_REPO.md` -- stato cross-repo corrente
6. ADR rilevanti al task (vault game-design / Game date-named / codemasterdd numerati)

> Repo daily-ship: ri-verifica HEAD/PR con `gh pr list -R MasterDD-L34D/<repo>`
> prima di azioni puntuali. I path strutturali in questa guida sono stabili.

---

## 11. Ispirazioni, Fonti & Stato Design (catalogo completo)

> Ricostruzione 2026-05-18 da audit cross-source esaustivo (6 explore agent,
> Protocol 2 autoresearch): lettura di TUTTE le ~45 museum card + grep vault
> completo. Documento unico e completo -- non sommario. Le decisioni di design
> vivono in due layer indipendenti che si corroborano:
>
> - **(A) Game museum cards** -- `Game/docs/museum/cards/` (Dublin Core,
>   alternative + ROI + reuse path, ~45 card, indice `docs/museum/MUSEUM.md`)
> - **(B) vault pillars** -- `vault/Spaces/Dev/Evo-Tactics/core/` (fonte
>   verita' canonical, autorita' A1-A3, freeze A3)
>
> Weighting: internal>external, empirical>doc, multi-source-converge >
> single-signal. Dove un'ispirazione appare in entrambi i layer = alta
> confidenza. Autorita' in caso di divergenza: vault `core/` (freeze A3)
> vince per scope shipping; museum = catalogo alternative + ROI.

### 11.1 I 6 pilastri di design <-> ispirazione ancora

Ogni pilastro (vault `core/02-PILASTRI.md`) e' ancorato a un'ispirazione
precisa. Stato pilastri 2026-04-20: 0/6 verde, 6/6 giallo (revisione onesta
post-playtest M1; pre-playtest era 5/6 verde -- NON regressione, realta'
testata).

| Pilastro | Nome | Ispirazione ancora | Stato |
|----------|------|--------------------|-------|
| P1 | Tattica leggibile | **Final Fantasy Tactics** + Into the Breach | 🟡 d20+MoS funziona, notazione AP ambigua (friction #1-2) |
| P2 | Evoluzione emergente | **Spore** (concetto) via Wesnoth + AI War (meccanica) | 🟡 mating non testato M1, persistence M10, runtime M12+ |
| P3 | Identita Specie x Job | FFT job cross-inheritance | 🟡 specie differenziate, job ability costs unclear (friction #4) |
| P4 | Temperamenti giocati | **Disco Elysium** (reveal diegetico MBTI/Ennea) | 🟡 VC tracking off in M1, solo T_F full |
| P5 | Co-op vs Sistema | **AI War** + NS2 Strategist + Frozen Synapse | 🟡 focus-fire live, "Sistema troppo passivo" |
| P6 | Fairness | Hades Heat + Monster Train Pact + AI War Progress | 🟡 d20 trasparente, scaling curves canonical |

### 11.2 Catalogo completo ispirazioni positive

Legenda stato: **SHIPPED** = implementato | **IN-DESIGN** = deciso/ADR ma
non shippato | **DEFERRED** = post-playtest/post-EA | **MUSEUM** = curated,
preservato ma non shippato (alternativa o forgotten).

#### A. Pillar-tier / architetturale (ancore dei pilastri)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte (file) | Stato |
|-----------------|-----------------|------------------------|--------------|-------|
| **Final Fantasy Tactics** (1997) | CT bar charge-time, Wait action, facing crit (rear+50%/side+25%), JP cross-job inheritance | Adotta legibilita' temporale (init + action_speed + wait) RIFIUTA crit Zodiac opaco. Wait shipped PR#1896. CT bar+facing 3-zone ~8h. JP cross-job M14+ | museum `combat-fft-ct-bar-wait-facing-crit.md` (4/5); vault `core/02-PILASTRI.md`,`10-SISTEMA_TATTICO.md` | SHIPPED (wait) + DEFERRED (CT/facing) |
| **Spore** (2008) | Part-pack assembly, ability auto-derivata da parti, mutazione morfologica runtime | RIFIUTA sandbox real-time; 6-pattern stack: slot morfologia, ability auto-derive, DNA budget, visual swap obbligatorio, ereditarieta' generazionale, part-bingo. Path moderato ~21h chiude P2 | museum `spore-part-pack-runtime-stack.md` (5/5); vault `core/20-SPECIE_E_PARTI.md`,`00-SOURCE-OF-TRUTH.md` §20 | IN-DESIGN (engine mating shipped, runtime M12+) |
| **Disco Elysium** (2019) | Thought Cabinet slots, voce interna 4-MBTI assi, skill-check passive->active popup, reveal diegetico MBTI color-coded | MBTI tag debrief shipped PR#1897. Thought Cabinet UI ~8h (P0 residuo). Voce interna ~10h. "Fonte calore" per P4 (pilastro piu' freddo) | museum `narrative-disco-thought-cabinet-diegetic.md` (5/5); vault `core/02-PILASTRI.md` P4 | SHIPPED (MBTI debrief) + DEFERRED (Cabinet/voce) |
| **AI War** (2009) | Antagonista data-driven persistente (Sistema), pack-unlock progression (no power-creep grind), progress meter chosen-escalation, multi-profile narrative voice | Pattern A Sistema-centric Fase 1. aiProgressMeter.js shipped #1898. `ai_profiles.yaml` narrative_voice per tier. 4-8 player co-op vs AI | vault `core/00F-ART_AUDIO_BUSINESS.md` §4.1,`00-SOURCE-OF-TRUTH.md`; museum `economy-hades-multi-currency-pact-menu.md` §convergenza | SHIPPED (progress meter, Fase 1) + IN-DESIGN (co-op net M11) |
| **Into the Breach** (2018) | Telegraph rule (tutto visibile pre-commit), push/pull arrows, kill-probability badge, zero RNG nascosto | "Sacrifice cool for clarity, every time". Threat tile overlay shipped PR#1884. Push/pull+kill badge ~3h. Determinismo = zero RNG post-decisione. Hand-curate maps ~10h | museum `ui-itb-telegraph-deterministic.md` (4/5); vault `core/41-ART-DIRECTION.md` | SHIPPED (threat overlay) + DEFERRED (arrows/badge) |
| **Hades** (2020) | Multi-currency split (PE-run vs Shards-meta), Pact menu opt-in difficulty, Codex tematico, gradual reveal | 3-currency split (PE-run/Shards-meta/PI-pack) ~6h. Pact Shards 0-5 ~5h. Cap a 3 currency (Hades 7 = overkill). Codex panel ~20h | museum `economy-hades-multi-currency-pact-menu.md` (5/5) | DEFERRED (post-playtest) |
| **Monster Train** (2020) | Pact Shards opt-in scaling componibile (modifier additivo, NON preset monolitico) | Pact Shards opt-in N-tier, reward tradeoff trasparente. Convergenza 4-source (Hades+MonsterTrain+AIWar+XCOM LW2) | museum `economy-hades-multi-currency-pact-menu.md` (5/5, row Monster Train) | DEFERRED (post-playtest) |
| **Tactics Ogre: Reborn** (2022) | HP floating bar sopra sprite, charm/recruit boss via dialogue, auto-battle button, class-change altare, WORLD rewind | HUD canonical: HP floating refactor ~5-7h, AP pip shipped PR#1901, charm recruit ~8h, auto-battle ~3h | museum `combat-tactics-ogre-hp-floating-charm.md` (5/5); vault `core/44-HUD-LAYOUT-REFERENCES.md` | SHIPPED (HP/AP) + DEFERRED (charm/auto/WORLD) |

#### B. Creature & narrativa (museum cards)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte | Stato |
|-----------------|-----------------|------------------------|-------|-------|
| **Wildermyth** (2021) | Battle-scar permanent (cicatrice=sprite change), ritratto stratificato, aging cross-session, choice->flag permanente, narrativa storylet | battle-scar registry ~12h, portrait layered ~15h, aging ~10h, choice flag ~4h. Convergenza 3-source (Wildermyth+SporeS4+VoidlingP6) | museum `creature-wildermyth-battle-scar-portrait.md` (4/5); vault `core/41-ART-DIRECTION.md` | IN-DESIGN (silhouette-per-specie canonical) |
| **Triangle Strategy** (2022) | MBTI Transfer Plan: 3 proposte concrete P4-closure -- (A) phased reveal Disco-style, (B) dialogue color codes diegetic, (C) recruit gating by MBTI threshold | 3 proposte mai citate in BACKLOG/OD = dimenticate. Map: vcScoring.js + formSessionStore.js + mbti_forms.yaml. **Solo museum, NON vault** | museum `personality-triangle-strategy-transfer.md` (M-2026-04-25-009, 5/5) | MUSEUM (FORGOTTEN, 5/5 high-ROI) |

#### C. Combat & UI quick-win (museum cards)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte | Stato |
|-----------------|-----------------|------------------------|-------|-------|
| **Cogmind** (2015) | Tooltip stratificati base+expand-on-hover, trade-off espliciti per componente | trait cost_ap -> multi-cost ~4-6h. Gold standard "identita = equip + trade-off espliciti" (P2+P3) | museum `ui-cogmind-tooltip-stratificati-quick-win.md` (4/5) | MUSEUM (quick-win ready) |

#### D. Indie research cluster (museum M-2026-04-27-019..031)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte | Stato |
|-----------------|-----------------|------------------------|-------|-------|
| **The Banner Saga** (2014) | Caravan supply attrition cross-mission ("3 giorni cibo, 47 bocche") + permadeath autentico opt-in | campaignResourceTracker.js ~6h minimal. Permadeath party.yaml preset ~4h | museum `indie-banner-saga-caravan-attrition.md` + `indie-banner-saga-permadeath-optin.md` (4/5) | DEFERRED (post-playtest) |
| **Cobalt Core** (2023) | Position-conditional ability bonus (posizione = prerequisito ability) | abilityExecutor.js position_condition tag -> +2 se flanking. Ripple ~15h post-Bundle A | museum `indie-cobalt-core-position-bonus.md` (4/5) | DEFERRED (post-Bundle A) |
| **Backpack Hero** (2023) | Spatial inventory adjacency (Tetris-griglia, posizione crea bonus) | 2+ trait stesso organ_system -> bonus passivo. form_pack_bias.yaml live, layer post-S6 | museum `indie-backpack-hero-spatial-inventory.md` (3/5) | DEFERRED (post-S6) |
| **Astrea: Six-Sided Oracles** (2023) | Dadi contaminati/puri = character sheet visibile (pool dadi tangibile) | VC axes come dadi facce contaminate/pure. Defer fino OD-013 MBTI surface verdict | museum `indie-astrea-dice-purification.md` (3/5) | DEFERRED (OD-013) |
| **Citizen Sleeper** (2022) | Fatigue drift cross-encounter (corpo si degrada -> modifica VC axis) | fatigue accumulator store + ink rest events. Post-Bundle C | museum `indie-citizen-sleeper-fatigue-drift.md` (3/5) | DEFERRED (post-Bundle C) |
| **Slay the Princess** (2023) | 12-knot branching state memory ("il gioco sa come ho giocato") | narrativeRoutes.js debrief knot per mbti_group. Writer D4 bottleneck (55 ink unit, 8h) | museum `indie-slay-princess-branching-state.md` (3/5) | DEFERRED (D4 writer) |
| **Pentiment** (2022) | Job voice + confessionals (job player colora comunicazione) | job-variant briefing ink (35+ stitch x 7 job). Writer D4 bottleneck | museum `indie-pentiment-job-voice-confessionals.md` (3/5) | DEFERRED (D4 writer) |
| **Inscryption** (2021) | Camera reveal meta-frame escalating (Sistema rivela dati progressive come "dossier intercettato") | objectiveEvaluator.js esposto post-MVP. TKT-09 prereq. Dossier tracker 3-consecutive | museum `indie-inscryption-camera-reveal-meta.md` (2/5) | DEFERRED (post-MVP) |
| **1000xRESIST** (2024) | Memory layered POV (briefing cita "volta scorsa Sistema ha usato fianco destro") | previousBiomeLoss store + conditional ink knot ~5h. Post-Bundle B | museum `indie-1000xresist-memory-layered-pov.md` (3/5) | DEFERRED (post-Bundle B) |
| **Loop Hero** (2021) | Minimap campaign visual emergence (hex 5x5 illumina post-scenario, grigio = attesa) | briefing hex_revealed array 1-3/scenario. Decisione D5 pending (diegetic vs HUD) ~6-9h | museum `indie-loop-hero-minimap-visual-emergence.md` (3/5) | DEFERRED (D5) |
| **Cocoon** (2023) | Biome rules layer (1-2 regole tattiche uniche/bioma, combinano in transition) | biome_rules.yaml ext, biomeSpawnBias rework ~7h post-P3 | museum `indie-cocoon-biome-rules-layer.md` (3/5) | DEFERRED (post-P3) |
| **Tunic** (2022) | Manual-as-puzzle diegetic knowledge (codex sbloccabile, lingua gliffica deduci) | subset decipher Codex ADOPT ~5h. Broader scope post-MVP UX | museum `indie-tunic-manual-puzzle-broader.md` (2/5) | DEFERRED / partial ADOPT |

#### E. Core/GDD narrative & system tier (vault canonical)

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte | Stato |
|-----------------|-----------------|------------------------|-------|-------|
| **Wesnoth** (GPL) | Campaign dialogue inline, leader named = unita giocabile, `{QUANTITY}` scaling (Easy 0.7x/Norm 1.0x/Hard 1.3x). **Validatore pattern P2** (evoluzione = advancement tree, NON sim) | Pattern citato (no code-clone) per campaign + difficulty scaling Fase 2 | vault `00-SOURCE-OF-TRUTH.md` §15.4-15.5; `00F` §4.4 | Research-validated, narrative Fase 2 |
| **Descent: Road to Legend** (FFG board) | Overlord plot-card rhythm, struttura campagna multi-hero, quest branching win/loss, campaign book + "dadi Descent-like" su spese PT/PP | Pattern B "Overlord + Custodi named" Fase 2 post-EA: `data/core/custodi.yaml` + campaign book. Dice metaphor TV in `11-REGOLE_D20_TV.md` | vault `core/00F-ART_AUDIO_BUSINESS.md` §4.3-4.4; `core/11-REGOLE_D20_TV.md` | DEFERRED (narrative Fase 2) + SHIPPED (dice metaphor) |
| **Fire Emblem** | Square grid tactics, positioning depth (ref comparativo scelta grid) | Hex preferito su square (ADR-2026-04-16), pattern FE noto | vault `00-SOURCE-OF-TRUTH.md` §14.1 | Design-known |
| **AncientBeast** (GPL) | Hex 16x9 grid, multi-tile creature, coord axial/cube, pathfinding+FOV/LOS | **DECISO**: hex axial adottato | vault `00-SOURCE-OF-TRUTH.md` §14.1-14.3; **ADR-2026-04-16-grid-type-hex-axial** | IN-DESIGN (ADR DECIDED) |
| **Don't Starve** | Silhouette forte + palette limitata (16-24 col/biome), creature iconiche | Silhouette language (P3 job-to-shape), 32x32 sprite, indexed PNG | vault `41-ART-DIRECTION.md` §Implementazione | IN-DESIGN (art-direction APPROVED) |
| **Slay the Spire** (2017) | Mood UI scuro TV-first, intent preview info-on-entity, loop economici scarsita'-driven | Mood canonical post ADR-2026-04-18. Economia non-gacha. Convergenza UI Telegraph | vault `core/41-ART-DIRECTION.md`; Game `docs/planning/2026-04-20-design-audit-consolidated.md` | IN-DESIGN (art-direction decisa) |
| **Wargroove** (2019) | Pixel-art moderno (no 8-bit, no 3D), clarity combat, palette vivida | Pixel-art ortho, palette matrix 9 biomi x 4-color, Aseprite pipeline. Reference moodboard ufficiale | vault `core/41-ART-DIRECTION.md`,`00F` §2.4 | IN-DESIGN (reference, no ADR esplicito) |
| **OpenRA** (GPL) | Mission briefing + campaign scripting Lua, objective narrativi | encounter YAML schema `narrative.briefing_ink` field | vault `00-SOURCE-OF-TRUTH.md` §15.2; `00F` §4.4 | Schema-integrated |
| **FFT: War of the Lions** (2007) | Named companion dialogue + generic recruit, acted scenes, isometric legibility | Fase 2: 2-4 Custodi named + generic "Wolf-03" slot. Campaign arc intro->acts->climax | vault `00F` §4.4; `00-SOURCE-OF-TRUTH.md` audience | DEFERRED (narrative Fase 2) |
| **Ink / inkle** (engine) | Multi-speaker knot dialogue, branching variable state | narrativeEngine.js (inkjs) + ai_profiles.yaml narrative_voice | vault `00F` §4.2,§4.4 | **IMPLEMENTED** (Fase 1 minimal) |
| **80 Days / Sorcery** (inkle) | Gold standard Ink multi-speaker, no-VO emphasis | Validazione pattern Ink (creature silent, Sistema narra) | vault `00F` §4.4 | Reference-validated |

> **Nota d20/TTRPG**: il progetto usa la regola d20 + Margin-of-Success
> (ADR-2026-04-13) senza accreditare Pathfinder/D&D 5e per nome. Ispirazione
> meccanica, non sistema citato.

### 11.3 Pattern di convergenza (multi-source = principio hard)

Dove >=3 fonti indipendenti convergono = principio di design non negoziabile:

1. **UI Telegraph** (7-source: Slay the Spire + ITB + Tactics Ogre + FFT CT bar
   + Cogmind + Battle Brothers ATB + Halfway) -> "info attaccata all'entita',
   mai nascosta". Hybrid overlay (Tactics Ogre base + Dead Space tint additivo).
2. **Cambio visibile permanente** (3-source: Wildermyth + Spore S4 + Voidling
   Pattern 6) -> ogni cambio meccanico significativo HA conseguenza visiva (P3+P4).
3. **Difficolta' opt-in componibile** (4-source: Hades Heat + Monster Train Pact
   + AI War Progress + XCOM Long War 2) -> scaling player-controlled, NON preset (P6).
4. **Visibilita' co-op** (3-source: Frozen Synapse replay + ITB telegraph + NS2
   Strategist atlas) -> reveal simultaneo post-decisione = sblocco planning (P5).

### 11.4 Anti-reference (cosa NON vogliamo essere)

Fonte: vault `41-ART-DIRECTION.md` §Direzione sintetica + `00F-ART_AUDIO_BUSINESS.md`
§1.2,§4.5. Decisioni esplicite di rifiuto:

| Anti-reference | Perche' rifiutato |
|----------------|-------------------|
| Disney cartoon | No cute -- creature bio-plausibili, body-horror trait |
| Pokemon-style cute | Incompatibile PEGI 16 + creature mature |
| Full-3D realistico | Budget indie, TV pixel clarity > fidelity |
| Anime shonen | Taglio adulto, no narrativa serializzata |
| Military sci-fi polished | Contro tono bio-plausibile + autonomia creature |
| Descent puro (Heroes fissi) | Named heroes contraddicono creature modulari (creature != player) |
| Pattern C (Player-named Commander) | Ownership si ma caratterizzazione generica, anchor narrativo debole |
| Pattern D (Ramza-light FFT single-POV) | Single protagonist contraddice co-op ownership, costo lineare alto |

### 11.5 Museum -- alternative scartate/parcheggiate preservate

Game `docs/museum/` (museum-first protocol): ~101 artifact, ~45 curator card
Dublin Core (31 con citazione gioco esterno, 14 worldgen/genetics interni),
3 gallerie, 9 inventory. Indice: `docs/museum/MUSEUM.md`.

| Card | Cos'era | Perche' scartato/parcheggiato |
|------|---------|-------------------------------|
| Promotions-orphan (3/5) | Job rank advancement (JP inheritance FFT) | Complessita' FFT-specifica, scope creep. JP cross-job deferred M14+ |
| MBTI Gates Ghost (4/5) | Modal unlock gate MBTI early | Opaco -> sostituito da Disco color-coded debrief. Recuperabile via git |
| Magnetic Rift Resonance (4/5) | Swarm trait T2 biome-resonance oscillator | Simulazione real-time troppo costosa -> trait cost + biome memory |
| Sentience Tiers v1.0 (5/5) | Interocezione T0-T6 + 22 Self-Control trigger | Non integrato ma high-ROI. Skiv Sprint C unblock (290/297 trait live) |
| Worldgen 4-level stack (5/5) | Bioma->Ecosistema->Foodweb->Network | Infra completa MA zero runtime consumption. Revive ~3-6h quick win |
| Enneagramma Registry (5/5) | 16 hook stub Ennea effect injection | Non integrato, ready-to-wire. 93 LOC orphan ~3h |
| Voidling Bound 6 Patterns (4/5) | Genetics: rarity-gate, path-lock, Apex terminal, visual_swap | Pattern 6 (visual swap) non integrato, P0 gap |
| Triangle Strategy Transfer (5/5) | 3 proposte P4-closure A/B/C | Dimenticato, mai in BACKLOG/OD. Cross-validate quando Thought Cabinet wiring |
| Mating Engine D1+D2 (5/5) | 1053 LOC engine + 7 REST, zero frontend | **REVIVED 2026-04-27**: PR#1876/1879/1911 shipped. OD-001 era disinfo |

### 11.6 Direzione artistica + creature + biomi + audio

**Stile target**: "readable biopunk tactical diorama" -- NO parchment fantasy,
NO cute pixel, NO sci-fi sterile. Fonte: Game-Godot-v2
`docs/godot-v2/visual-screen-bible.md` + `visual-design-research.md`.

3 modi visivi:
- **World-forming**: void vivo, biome color signal, beat ritual 500-900ms
- **Tactical**: grid pulita, overlay alto-contrasto cyan/amber/red/white
  shape-coded, feedback 80-350ms
- **Memory**: battlefield dim, portrait/voce forte, reveal ordinato 400-900ms

Palette 4-layer: biome base (low sat) + unit identity (outline team + tint
specie) + tactical overlay (cyan/amber/red/white) + ritual overlay (deep ink,
warm bone text).

**Creatura Skiv** (refs in `evo-tactics-refs-meta/SKIV_REFS_EXTRACTED.md`):
- 3D anatomia: Quaternius Animal Pack Vol.2 Wolf + Red Fox (CC0, rig posing),
  wolf-skiv-ref (Blender rigged + 3dwolf FBX PBR color/normal/rough/spec)
- 2D sprite: HF OGA-CC0 Desert Kit Wild Animals (Fox/Wolf 36-40px, Wolf Howl
  16fr = "calling pack" diretto per lore Skiv), DENZI cat 32x32 (12 variant)
- Concept: Surt CC0 pack 175+ file (100 color + 26 doodle + silhouette_pack +
  monster concept), HF "creature and cub sketch" 21MB PNG+PSD (anatomia +
  relazione madre/cucciolo), Kenney Monster Builder, PhyloPic 581 SVG
- Skiv design = **lavoro originale** ground su questi ref, no artista attribuito

**Biomi**: Africa Savanna Pack v1.0 493 file DAE (habitat Skiv, scale creature
vs env, sun-angle warm), CAVE_PACK_PRO 272 file (burrow secondario), 3D Nature
Pack 160 + Desert Arena 53, HF Desert Kit tileset (Cactus/Palm/Sand 32-8px,
quicksand animato GIF, Hermit Sand 5-sprite burrow), ambientCG PBR sand 20
material seamless 1K, Kenney roguelike-caves.

**Audio**: Sonniss 6691 file royalty-free perpetual (Paw Trot = "Skiv soft paw
trot diretto", Deep Breather idle pitch -2 semitoni, Alien Creature Growl
sweep, AMB Wind-Gusty desert, ATMO Eerie Cave loop) + HF OGA-CC0 creature SFX
811 (80-CC0-creature roar, Monster RPG 2, Baby Animals cub, cat purr).
**`vocal/sand-spell.flac` = DIRECT FIT Skiv echolocation/sand-magic SFX**.
Pipeline Audacity documentata: idle (Deep Breather trim 3s + pitch -2 +
22050Hz mono), roar (roar_01.ogg + Punch Whoosh layered), echolocation
(sand-spell trim 800ms + EQ high-pass 2kHz + reverb tail). Kenney UI/impact +
FreePD orchestral 1237 MP3.

**Licensing**: 100% license-clean (`evo-tactics-refs-meta/HANDOFF.md`,
MANIFEST.json indicizza 32136 file). ~8080 CC0 + 6691 Sonniss perpetual +
~1240 PD reference-only. Zero CC-BY-SA viral. Zero Tier B/C (DMCA: GTA/CoD/
Pokemon banditi esplicitamente). 4 path workflow:
1. **Path 1**: Kenney/CC0 base + modify Aseprite + CREDITS.md entry
2. **Path 2**: AI gen (Retro Diffusion ToS enterprise indemnified) 10 variant
   -> pick 1-3 -> polish -> CREDITS "AI generated, human-edited"
3. **Path 3**: ref + redraw fresh (studia, chiudi file, canvas blank, redraw)
   -> CREDITS "original work, inspired by [era]"
4. **Path 4**: licensed SFX -> Audacity edit/layer -> CREDITS source
Local ref folder PRIVATO (mai synced). Shipping solo da `Game/assets/` +
CREDITS.md provenance.

### 11.7 Fonti & ricerca disponibili (indice)

| Fonte | Path | Contenuto |
|-------|------|-----------|
| Museum index | Game `docs/museum/MUSEUM.md` | ~45 card + 3 gallerie + 9 inventory + relevance table |
| Pilastri canonical | vault `Spaces/Dev/Evo-Tactics/core/02-PILASTRI.md` | 6 pilastri + ancora ispirazione |
| Source of Truth | vault `core/00-SOURCE-OF-TRUTH.md` | §14 grid, §15 campaign/encounter, §20-23 evoluzione |
| Art direction | vault `core/41-ART-DIRECTION.md` + `00F-ART_AUDIO_BUSINESS.md` | Reference + anti-reference + audio + business |
| HUD layout | vault `core/44-HUD-LAYOUT-REFERENCES.md` | HP floating + AP pip ref |
| Design freeze | Game `docs/core/90-FINAL-DESIGN-FREEZE.md` (A3) | Scope shipping locked |
| Roadmap index | Game `docs/planning/EVO_FINAL_DESIGN_ROADMAPS_INDEX.md` | M0-M6 + FD-ID backlog |
| Combat canon | Game `docs/combat/combat-canon.md` + `round-loop.md` | d20 + status + economy frozen |
| Design audit | Game `docs/planning/2026-04-20-design-audit-consolidated.md` + `pilastri-reality-audit.md` | Pillar audit post-M1 |
| ADR game-design | vault `Spaces/Dev/Evo-Tactics/adr/` (39) + Game `docs/adr/` (date-named) | Decisioni architetturali |
| Design watcher | vault `production/agents/evo-tactics-design-watcher.md` | Agent flag contraddizioni |
| Asset refs | `evo-tactics-refs-meta/` (SKIV_REFS, CATALOG, CC0_SOURCES, HANDOFF) | Provenance asset 100% classificata |
| Art Godot | Game-Godot-v2 `docs/godot-v2/visual-screen-bible.md` + `visual-design-research.md` | Bibbia visiva 3-modi |
| External repos | vault `memory/reference_external_repos.md` | Repo tracciati Fase 2 (non letto in audit) |

### 11.8 A che punto siamo (roadmap M0-M6)

Fase: **Final Design Freeze** (scope locked 2026-04-20). Critical path:
Combat -> Balance -> Content -> UX -> Meta -> RC. Ogni gate blocca il
successivo + richiede approvazione Master DD.

| Fase | Nome | Stato | Dettaglio |
|------|------|-------|-----------|
| M0 | Baseline & Governance | ~completo | Freeze pubblicato, docs registry, owner matrix pending (FD-006) |
| M1 | Combat Freeze | **IN CORSO** | Resolver Python deprecato/killed 2026-05-05 (ADR-2026-04-19), Node canonical, contracts 23/23, 237 Python test archiviati, 6 azioni + 6 status + economy PT/PP/SG frozen. Gate: validator+smoke CI |
| M2 | Balance & Progression | Attesa M1 | trait audit 33/33 done; economia PE/PI/Seed non frozen (FD-050-058) |
| M3 | Content Slice | Attesa M2 | 4 specie (Dune Stalker/Sand Burrower/Echo Wing/Rust Scavenger) + 6 job + 3 biomi (Desert/Cavern/Badlands); mission slice incompleta (FD-060-068) |
| M4 | UX/HUD/Telemetry | Parziale | HUD Wave 2-7 shipped (PT/PP/SG, AP, status, biome bonus, warning); debrief spec pending (FD-080-087) |
| M5 | Meta & Cross-Repo | Attesa M4 | Form Evolution Engine Phase A-D done (🟢 cand P2, Prisma persistence); Recruit/Trust + Nest/Mating slice pending |
| M6 | Release Candidate | Attesa M5 | Target 50 playtest; validator/smoke/snapshot pending; no Master DD approval |

**Deferred / cut espliciti** (con motivazione):
- XP Cipher: parked redundant (ADR-2026-04-17; coperto da job/mating/VC economy)
- Tabletop DM mode: killed digital-only (ADR-2026-04-19; "1 gioco online no master")
- Genetics mating complesse: M5 slice minima (genealogy/multi-gen deferred post-freeze)
- Game-Database HTTP runtime: out-of-scope freeze (solo Game->DB import unidirezionale)
- Enneagram deep tuning: modulo secondario (ADR-2026-04-23; non asse design core)
- Burnout/sentiment detection + Rust CLI rewrite: won't (RESEARCH_TODO W3/W6, no perf problem)

### 11.9 Gap, contraddizioni & autorita' cross-layer (onesto, no fabbricazione)

1. **Spore ibrido**: vault dice "Spore-like" poi chiarisce "NON sandbox,
   pattern = Wesnoth advancement tree + AI War pack-unlock". Nome ref corretto,
   adozione meccanica ibrida (concetto non meccanica diretta).
2. **FFT grid-agnostic**: ADR-2026-04-16 accetta hex-axial citando FFT, ma
   pathfinding/FOV non implementati (TV-first shared-screen). Borrow UX FFT
   senza richiederne complessita' grid. Accettabile MVP.
3. **Iso vs ortho RISOLTO**: intento "2.5D iso" vs codice ortho (Camera2D
   zoom 2.0, no shear). Verdetto 2026-05-16: codice canonical, art-direction
   ora ortho. Asset pipeline zero-cost ri-allineata.
4. **Narrative Fase A vs B**: Fase A Sistema-centric (AI War) defer named-hero
   (Descent Road to Legend) a Fase B post-EA. Rischio se community chiede
   narrativa prima del trigger story-mode workstream.
5. **Audio senza ancora-gioco**: unico pilastro senza ispirazione-gioco
   nominata (solo source pack Sonniss/HF/Kenney). Accettabile (low-pri pre-MVP).
6. **Moodboard visivo pending**: palette matrix 9 biomi canonical ma esempi
   visivi moodboard ancora da produrre.
7. **Discrepanza cross-layer (sapere quando si wira)**:
   - Triangle Strategy = **museum-only** (5/5 FORGOTTEN), NON in vault
   - Don't Starve / AncientBeast / Fire Emblem / OpenRA / Wesnoth / Ink =
     **vault core**, framing diverso o assenti in museum
   - Stessa ispirazione (es. FFT) ha framing leggermente diverso nei 2 layer:
     non contraddizione, complementare. Museum = catalogo alternative + ROI +
     reuse-path; vault `core/` = decisione canonical (autorita' A1-A3, freeze
     A3 vince per scope shipping). Verificare coerenza prima di wire meccanica.

**Negative results** (cercati esplicitamente, CONFERMATI assenti): Darkest
Dungeon, XCOM core series (solo "Long War 2" come analog convergenza P6),
Pikmin, Pokemon (solo anti-reference, mai positivo), Monster Hunter, Battle
Brothers (citato solo in pattern Telegraph 7-source, no card), Halfway (idem),
Resident Evil, nessun "Descent: Journeys" board game (solo Road to Legend).

**Conteggio finale**: ~31 titoli unici citati positivamente (8 pillar-tier +
1 creature museum + 1 quick-win + 11 indie-cluster + 10 core/GDD narrative+
system) + 8 anti-reference esplicite + ~14 museum card senza gioco esterno
(worldgen/genetics interni). Tutte le ~45 museum card lette.

---

> Documento completo. Fonti file-cited verificate 2026-05-18. Path strutturali
> stabili; HEAD/PR/sprint-status volatili -- ri-verifica vault `core/` + Game
> `docs/planning/` + `gh pr list` prima di azioni puntuali.
