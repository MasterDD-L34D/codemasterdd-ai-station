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

## 11. Ispirazioni, Fonti & Stato design

> Ricostruzione 2026-05-18 da audit cross-source (4 explore agent paralleli,
> Protocol 2 autoresearch). Due layer di documentazione indipendenti:
> **(A) Game museum cards** (`docs/museum/cards/` -- Dublin Core, alternative
> preservate) e **(B) vault pillars** (`Spaces/Dev/Evo-Tactics/core/` -- fonte
> verita' design). Si corroborano: dove un'ispirazione appare in entrambi e'
> alta confidenza. Weighting: internal>external, empirical>doc. Gap dichiarati
> esplicitamente, no fabbricazione.

### 11.1 I 6 pilastri <-> ispirazione ancora

I pilastri di design (vault `core/02-PILASTRI.md`) sono ciascuno ancorato a
un'ispirazione precisa:

| Pilastro | Nome | Ispirazione ancora | Stato (vault 2026-04-20) |
|----------|------|--------------------|--------------------------|
| P1 | Tattica leggibile | **Final Fantasy Tactics** + Into the Breach | 🟡 (d20+MoS funziona, notazione AP ambigua) |
| P2 | Evoluzione emergente | **Spore** (concetto) via Wesnoth + AI War (meccanica) | 🟡 (mating non testato M1, persistence M10) |
| P3 | Identita Specie x Job | FFT job cross-inheritance | 🟡 (specie differenziate, job ability costs unclear) |
| P4 | Temperamenti giocati | **Disco Elysium** (reveal diegetico MBTI/Ennea) | 🟡 (VC tracking off in M1, T_F full only) |
| P5 | Co-op vs Sistema | **AI War** + NS2 Strategist + Frozen Synapse | 🟡 (focus-fire live, "Sistema troppo passivo") |
| P6 | Fairness | Hades Heat + Monster Train Pact + AI War Progress | 🟡 (d20 trasparente, scaling curves canonical) |

Score: 0/6 verde, 6/6 giallo. Trend: pre-playtest era 5/6 verde -> revisione
onesta post-playtest M1 a 6/6 giallo (NON regressione: realta' testata).

### 11.2 Tabella master ispirazioni

Per ogni gioco/sistema: cosa ci piaceva | come intendiamo farlo | fonte | stato.
Stato legenda: SHIPPED = implementato, IN-DESIGN = deciso ma non shippato,
DEFERRED = post-playtest/post-EA, MUSEUM = preservato ma scartato/parcheggiato.

| Gioco / Sistema | Cosa ci piaceva | Come intendiamo farlo | Fonte (file) | Stato |
|-----------------|-----------------|------------------------|--------------|-------|
| **Final Fantasy Tactics** (1997) | Initiative/CT bar, facing crit (rear+50%/side+25%), positioning, job cross-inheritance | Adotta legibilita' temporale (init + action_speed + wait action) ma RIFIUTA crit Zodiac opaco. Wait shipped PR#1896. CT bar + facing 3-zone ~8h | Game `docs/museum/cards/combat-fft-ct-bar-wait-facing-crit.md` (4/5); vault `core/02-PILASTRI.md`,`10-SISTEMA_TATTICO.md` | SHIPPED (wait) + DEFERRED (CT bar/facing) |
| **Spore** (2008) | Part-pack creature assembly, ability derivata da parti, mutazione morfologica runtime | RIFIUTA sandbox real-time; adotta 6-pattern stack: slot morfologia, ability auto-derive, DNA budget, **visual swap obbligatorio**, ereditarieta' generazionale, part-bingo. Path moderato ~21h chiude P2 | Game `docs/museum/cards/spore-part-pack-runtime-stack.md` (5/5); vault `core/20-SPECIE_E_PARTI.md` | IN-DESIGN (engine mating shipped, evoluzione runtime M12+) |
| **Into the Breach** (2018) | Telegraph rule (tutto visibile pre-commit), push/pull arrows, kill-probability badge, zero RNG nascosto | "Sacrifice cool for clarity, every time". Threat tile overlay shipped PR#1884. Push/pull + kill badge ~3h. Determinismo = zero RNG post-decisione | Game `docs/museum/cards/ui-itb-telegraph-deterministic.md` (4/5); vault `core/41-ART-DIRECTION.md` | SHIPPED (threat overlay) + DEFERRED (arrows/badge) |
| **Disco Elysium** (2019) | Thought Cabinet equip slots, voce interna (assi personalita' -> narrativa), reveal diegetico MBTI color-coded | MBTI tag debrief shipped PR#1897. Thought Cabinet UI ~8h (P0 residuo). Voce interna 4-assi ~10h. Disco = "fonte calore" per pilastro piu' freddo (P4) | Game `docs/museum/cards/narrative-disco-thought-cabinet-diegetic.md` (5/5); vault `core/02-PILASTRI.md` P4 | SHIPPED (MBTI debrief) + DEFERRED (Thought Cabinet/voce) |
| **AI War** (2019) | Multi-player asimmetrico vs antagonista data-driven, pack-unlock progression (no power-creep grind), progress meter chosen-escalation | Pattern A Sistema-centric Fase 1. aiProgressMeter.js shipped #1898. 4-8 player co-op vs AI | vault `core/00F-ART_AUDIO_BUSINESS.md`,`00-SOURCE-OF-TRUTH.md`; Game ADR-2026-04-16-networking | SHIPPED (progress meter) + IN-DESIGN (co-op net M11) |
| **Wildermyth** (2021) | Cambio aspetto permanente visibile (cicatrice = sprite change), narrativa stratificata, lifecycle aging | Battle-scar registry + ritratti stratificati + flag narrativi permanenti. Convergenza con Spore S4 (visual swap obbligatorio, 3-source) | Game `docs/museum/cards/creature-wildermyth-battle-scar-portrait.md` (4/5); vault `core/41-ART-DIRECTION.md` | IN-DESIGN (silhouette-per-specie canonical) |
| **Tactics Ogre: Reborn** (2022) | HP floating bar sopra sprite, AP pip, charm/recruit boss, auto-battle | HUD canonical: HP floating (5/5 in `44-HUD-LAYOUT-REFERENCES.md`), AP pip shipped PR#1901. Charm recruit + auto-battle deferred | Game `docs/museum/cards/combat-tactics-ogre-hp-floating-charm.md` (5/5) | SHIPPED (HP/AP) + DEFERRED (charm/auto-battle) |
| **Hades + Monster Train** (2020) | Multi-currency (tight vs long loop), Pact opt-in difficulty composable (non preset monolitico) | 3-currency split (PE-run/Shards-meta/PI-pack). Pact Shards 0-5 ~5h. Cap a 3 currency (Hades 7 = overkill) | Game `docs/museum/cards/economy-hades-multi-currency-pact-menu.md` (5/5) | DEFERRED (post-playtest) |
| **NS2 + Frozen Synapse** (2012/2011) | NS2 Strategist 5p+ role asimmetrico (1 atlas-overview, 4 tactical); Frozen Synapse replay cinematico round | Frozen Synapse replay ~10-14h (rewatch deterministico TV condiviso). NS2 Strategist 5p+ ~25-30h | Game `docs/museum/cards/coop-ns2-frozen-synapse-replay-asymmetric.md` (4/5) | DEFERRED (M11 base shipped) |
| **Slay the Spire** (2019) | Mood UI scuro TV-first, loop economici scarsita'-driven, pacing turn-based | Mood canonical post ADR-2026-04-18. Economia non-gacha (tri-sorgente) | vault `core/41-ART-DIRECTION.md` | IN-DESIGN (art direction decisa) |
| **Wargroove** (2019) | Pixel-art moderno (no 8-bit retro, no 3D), clarity combat, palette vivida | Pixel-art ortho, palette matrix 9 biomi x 4-color identity | vault `core/41-ART-DIRECTION.md`,`00F-ART_AUDIO_BUSINESS.md` | IN-DESIGN (reference, no ADR esplicito) |
| **Descent: Road to Legend** | Overlord plot-card rhythm, struttura campagna multi-hero, branching win/loss | Pattern B "Overlord + Custodi named" -- narrative Fase B post-EA (Fase A = Sistema-centric AI War) | vault `core/00F-ART_AUDIO_BUSINESS.md` §4.3-4.4 | DEFERRED (narrative Fase B post-EA) |
| **Banner Saga** (2014) | Caravan supply attrition cross-mission, permadeath opt-in | Supply tracker ~6h. Permadeath party.yaml preset ~4h | Game `docs/museum/cards/indie-banner-saga-*.md` (4/5) | DEFERRED (post-playtest) |
| **Cobalt Core** (2024) | Bonus ability position-conditional (blast/push scala con formazione) | abilityExecutor position_condition hook, blast x1.5 formazione | Game `docs/museum/cards/indie-cobalt-core-position-bonus.md` (4/5) | DEFERRED (post-Bundle A) |
| **Citizen Sleeper** (2022) | Fatigue drift cross-encounter (trauma combat -> stato persistente) | VC axes come state modifier persistente | Game `docs/museum/cards/indie-citizen-sleeper-fatigue-drift.md` (3/5) | DEFERRED (post-Bundle C) |

> Nota d20/TTRPG: il progetto usa la regola meccanica d20 + Margin-of-Success
> (ADR-2026-04-13) **senza accreditare** Pathfinder/D&D 5e per nome. Ispirazione
> meccanica, non sistema citato.

### 11.3 Pattern di convergenza (multi-source = alta confidenza)

Dove >=3 fonti indipendenti convergono = principio di design hard:

1. **UI Telegraph** (7-source: StS + ITB + Tactics Ogre + FFT CT bar + Cogmind
   + Battle Brothers + Halfway) -> "info attaccata all'entita', mai nascosta".
   Hybrid overlay (Tactics Ogre base + Dead Space tint additivo).
2. **Cambio visibile permanente** (3-source: Wildermyth + Spore S4 + Voidling
   Pattern 6) -> ogni cambio meccanico significativo HA conseguenza visiva (P3+P4).
3. **Difficolta' opt-in componibile** (4-source: Hades Heat + Monster Train Pact
   + AI War Progress + XCOM Long War) -> scaling player-controlled, NON preset (P6).
4. **Visibilita' co-op** (3-source: Frozen Synapse + ITB + NS2 Strategist) ->
   reveal simultaneo post-decisione = sblocco planning condiviso (P5).

### 11.4 Museum -- alternative scartate/parcheggiate preservate

Game `docs/museum/` (museum-first protocol): ~101 artifact, 34 curator card
Dublin Core, 3 gallerie, 9 inventory. Indice: `docs/museum/MUSEUM.md`.

| Card | Cos'era | Perche' scartato/parcheggiato |
|------|---------|-------------------------------|
| Promotions-orphan (3/5) | Job rank advancement (JP inheritance FFT) | Complessita' FFT-specifica, scope creep. JP cross-job deferred M14+ |
| MBTI Gates Ghost (4/5) | Modal unlock gate MBTI early | Opaco -> sostituito da Disco color-coded debrief. Recuperabile via git |
| Magnetic Rift Resonance (4/5) | Swarm trait T2 biome-resonance oscillator | Simulazione real-time troppo costosa -> trait cost + biome memory |
| Sentience Tiers v1.0 (5/5) | Interocezione T0-T6 + 22 Self-Control trigger | Non integrato ma high-ROI. Skiv Sprint C unblock (290/297 trait live) |
| Worldgen 4-level stack (5/5) | Bioma->Ecosistema->Foodweb->Network | Infra completa MA zero runtime consumption. Revive ~3-6h quick win |
| Enneagramma Registry (5/5) | 16 hook stub Ennea effect injection | Non integrato, ready-to-wire. 93 LOC orphan ~3h |
| Voidling Bound 6 Patterns (4/5) | Genetics: rarity-gate, path-lock, Apex terminal, visual_swap | Pattern 6 non integrato, P0 gap |
| Mating Engine D1+D2 (5/5) | 1053 LOC engine + 7 REST, zero frontend | **REVIVED 2026-04-27**: PR#1876/1879/1911 shipped. OD-001 era disinfo |

### 11.5 Direzione artistica + creature + biomi + audio

**Stile target**: "readable biopunk tactical diorama" -- NO parchment fantasy,
NO cute pixel, NO sci-fi sterile. Fonte: Game-Godot-v2
`docs/godot-v2/visual-screen-bible.md` + `visual-design-research.md`.
3 modi visivi: World-forming (void vivo, beat ritual 500-900ms) / Tactical
(grid pulita, overlay alto-contrasto cyan/amber/red 80-350ms) / Memory
(battlefield dim, portrait/voce forte 400-900ms). Palette 4-layer: biome base
(low sat) + unit identity (outline team + tint specie) + tactical overlay +
ritual overlay (deep ink, warm bone text).

**Creatura Skiv** (refs in `evo-tactics-refs-meta/SKIV_REFS_EXTRACTED.md`):
- 3D anatomia: Quaternius Wolf/Red Fox (CC0, rig posing), wolf-skiv-ref PBR
- 2D sprite: HF OGA-CC0 Desert Kit Wild Animals (Fox/Wolf 36-40px, Wolf Howl
  16fr = "calling pack" diretto per lore Skiv), DENZI cat 32x32
- Concept: Surt CC0 pack 175+ file (silhouette study, mood board), HF "creature
  and cub sketch" (anatomia + relazione madre/cucciolo)
- Skiv design = **lavoro originale** ground-su questi ref, no artista attribuito

**Biomi**: Africa Savanna Pack 493 file DAE (habitat Skiv), CAVE_PACK_PRO 272
file (burrow), HF Desert Kit tileset + Hermit Sand (animazione burrow),
ambientCG PBR sand 20 material.

**Audio**: Sonniss 6691 file royalty-free (Paw Trot = "Skiv soft paw trot
diretto", Deep Breather idle -2 semitoni, Eerie Cave atmo) + HF OGA-CC0
creature SFX 811. **`vocal/sand-spell.flac` = DIRECT FIT Skiv echolocation**.
Pipeline Audacity documentata (idle/roar/echolocation layering).

**Licensing**: 100% license-clean (`evo-tactics-refs-meta/HANDOFF.md`). ~8080
CC0 + 6691 Sonniss perpetual + ~1240 PD. Zero Tier B/C (DMCA: GTA/CoD/Pokemon
banditi esplicitamente). 4 path workflow: CC0+modify / AI-gen indemnified /
ref+redraw-fresh / audio-process. Shipping solo da `Game/assets/` con CREDITS.md.

### 11.6 Fonti & ricerca disponibili

| Fonte | Path | Contenuto |
|-------|------|-----------|
| Museum index | Game `docs/museum/MUSEUM.md` | 34 card + 3 gallerie + 9 inventory |
| Pilastri canonical | vault `Spaces/Dev/Evo-Tactics/core/02-PILASTRI.md` | 6 pilastri + ancora ispirazione |
| Art direction | vault `core/41-ART-DIRECTION.md` + `00F-ART_AUDIO_BUSINESS.md` | Reference visivi + anti-reference |
| Design freeze | Game `docs/core/90-FINAL-DESIGN-FREEZE.md` (A3 authority) | Scope shipping locked |
| Roadmap index | Game `docs/planning/EVO_FINAL_DESIGN_ROADMAPS_INDEX.md` | M0-M6 + FD-ID backlog |
| Combat canon | Game `docs/combat/combat-canon.md` + `round-loop.md` | d20 + status + economy frozen |
| ADR game-design | vault `Spaces/Dev/Evo-Tactics/adr/` (39) + Game `docs/adr/` (date-named) | Decisioni architetturali |
| Design watcher | vault `production/agents/evo-tactics-design-watcher.md` | Agent flag contraddizioni |
| Asset refs | `evo-tactics-refs-meta/` (SKIV_REFS, CATALOG, CC0_SOURCES) | Provenance asset 100% classificata |
| Art Godot | Game-Godot-v2 `docs/godot-v2/visual-screen-bible.md` | Bibbia visiva 3-modi |

### 11.7 A che punto siamo (roadmap M0-M6)

Fase: **Final Design Freeze** (scope locked 2026-04-20). M0 baseline ~completo,
**M1 Combat Freeze in corso**, M2-M6 bloccati dietro gate M1.

| Fase | Nome | Stato |
|------|------|-------|
| M0 | Baseline & Governance | ~completo (freeze pubblicato, owner matrix pending) |
| M1 | Combat Freeze | **IN CORSO** (resolver Python deprecato 2026-05-05, Node canonical, contracts 23/23, 237 Python test archiviati) |
| M2 | Balance & Progression | Attesa M1 (trait audit 33/33 done, economia PE/PI/Seed non frozen) |
| M3 | Content Slice | Attesa M2 (4 specie + 6 job + 3 biomi presenti, mission slice incompleta) |
| M4 | UX/HUD/Telemetry | Parziale (HUD Wave 2-7 shipped, debrief spec pending) |
| M5 | Meta & Cross-Repo | Attesa M4 (Form Evolution Engine Phase A-D done, Recruit/Nest slice pending) |
| M6 | Release Candidate | Attesa M5 (target 50 playtest, no Master DD approval) |

Critical path: Combat -> Balance -> Content -> UX -> Meta -> RC. Ogni gate
blocca il successivo + richiede approvazione Master DD.

**Deferred/cut espliciti**: XP Cipher (parked redundant ADR-2026-04-17),
tabletop DM mode (killed ADR-2026-04-19, digital-only no master), genetics
mating complesse (M5 slice minima), Game-Database HTTP runtime (out-of-scope
freeze), Rust CLI rewrite (won't, no perf problem).

### 11.8 Gap & contraddizioni (dichiarati, no fabbricazione)

1. **Spore "muddied"**: vault dice "Spore-like" poi chiarisce "NON sandbox,
   pattern = Wesnoth + AI War pack-unlock". Nome ref corretto, adozione ibrida.
2. **FFT grid-agnostic**: ADR-2026-04-16 accetta hex-axial citando FFT, ma
   pathfinding/FOV non implementati (TV-first shared-screen). Rischio: borrow
   UX FFT senza richiederne complessita' grid. Accettabile MVP.
3. **Iso vs ortho RISOLTO**: intento "2.5D iso" vs codice ortho (Camera2D zoom
   2.0). Verdetto: codice canonical, art direction ora ortho.
4. **Narrative Fase A vs B**: Fase A Sistema-centric (AI War) defer named-hero
   (Descent) a Fase B post-EA. Rischio se community chiede narrativa prima.
5. **Audio senza ancora esterna**: unico pilastro senza ispirazione-gioco
   nominata (solo source pack). Accettabile (low-pri pre-MVP).
6. **Moodboard visivo pending**: palette matrix 9 biomi canonical ma esempi
   visivi moodboard ancora da produrre.
7. **Due layer doc (museum vs vault)**: framing leggermente diverso per stesse
   ispirazioni (es. FFT). Non contraddizione -- complementari, ma verificare
   coerenza quando si wira una meccanica (museum = alternative, vault = canonical).
