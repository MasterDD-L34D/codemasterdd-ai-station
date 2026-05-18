# Evo-Tactics — Guida Ecosistema (basi reali, file-cited)

> Guida operativa per continuare il progetto. Costruita 2026-05-18 da audit
> diretto dei 7 repo (gh API + clone locali). Ogni file citato e' verificato
> presente al momento dell'audit. Repo daily-ship (Game/Godot/Game-Database)
> evolvono in ~2gg: i path strutturali restano stabili, gli HEAD/PR no --
> ri-verifica con `gh` prima di azioni puntuali.

> **Portabilita'**: i path assoluti in questa guida sono della workstation
> Lenovo `CODEMASTERDD` (Eduardo). Su altre macchine (split Ryzen/Lenovo)
> vedi codemasterdd `CLAUDE.md` device map. Riferimenti repo-relativi dove
> possibile; path macchina = appendice operativa, non canonici.

---

## Indice

**Questo file (GUIDE)** = mappa 7-repo + front-matter condiviso canonico.
Design (ispirazioni/stile/contenuti) = file companion **[DESIGN_DIGEST](EVO_TACTICS_DESIGN_DIGEST.md)**.

- **Front matter**: Autorita' & fonte verita' | Stato & attivita' | Testing/Licensing/Ownership | Numeri canonici | Glossario
- **0** Mappa mentale corretta
- **1-7** Repo deep-dive: Game (1) | Game-Godot-v2 (2) | Game-Database (3) | evo-tactics-refs-meta (4) | evo-swarm/Dafne (5) | vault (6) | codemasterdd (7)
- **8** Data flow cross-repo *(sintetico; dettaglio = DIGEST 12.3)*
- **9** Come continuare -- workflow concreti
- **10** Ordine lettura nuova sessione
- **11-12** -> [DESIGN_DIGEST.md](EVO_TACTICS_DESIGN_DIGEST.md): 11 Ispirazioni/Fonti/Stato · 12 Stile distillato + design-doc + pipeline contenuti
- **Coda** Doc improvement backlog (harsh-review status)

---

## Autorita' & fonte verita' (canonico -- risolve ambiguita' sez. 6/9/11/12)

Modello unico (precedenza decrescente). vault e Game NON sono entrambi
"fonte verita'" allo stesso modo:

| Cosa | Autorita' | Dove | Nota |
|------|-----------|------|------|
| Verita' meccanica/numerica/schema | **A2** | **Game** `data/core/*`, `packs/.../data/*`, `packages/contracts/schemas/*` | YAML/schema vince su ogni doc descrittivo |
| Scope prodotto / freeze | **A3** | **Game** `docs/core/90-FINAL-DESIGN-FREEZE.md` | Vince su roadmap/planning |
| Boundary architetturale | **A1** | **Game** `docs/hubs/*`, `docs/combat/round-loop.md`, `docs/adr/*` | Vince su freeze se boundary contraddetto |
| Inventory/governance doc | **A0** | **Game** `docs/governance/`, `docs_registry.json` | Path/status/ownership |
| Modo operativo agent | **A4** | `CLAUDE.md`, `.claude/*`, `SAFE_CHANGES.md` | "how" non "what" |
| Contesto/intento/ricerca | **A5** | museum cards, Canvas, playtest notes | Informa, non governa |

**vault `Spaces/Dev/Evo-Tactics/` = layer A5/narrativo + shadow copy
read-only di reference**, NON canonical per meccanica/scope. Quando sez.
6/9/10 dicono "fonte verita' = vault" intendono *design narrative + ricerca
+ ADR storici*; la verita' runtime/shipping vive in **Game** (A0-A3). In
conflitto: **Game A2 YAML > A3 freeze > A1 ADR**; vault perde. (Sez. 11
usava "A1-A3" in modo generico -- la gerarchia precisa e' A0-A5 sopra,
fonte Game `docs/planning/EVO_FINAL_DESIGN_SOURCE_AUTHORITY_MAP.md`.)

---

## Stato & attivita' (verificato 2026-05-18, volatile)

> Repo daily-ship: HEAD/PR/sprint driftano in ~2gg. Tabella = snapshot
> 2026-05-18; ri-verifica `gh` prima di azioni puntuali.

| Repo | Visibilita' | Attivita' (as-of 2026-05-18) | Privacy / cloud | Playable |
|------|-------------|------------------------------|-----------------|----------|
| Game (Vue3) | PUBLIC | VIVO daily-ship | cloud-OK (whitelisted) | backend sim + web 2D legacy |
| Game-Godot-v2 | PRIVATE | VIVO daily-ship | cloud-OK (whitelisted) | client; evo-tactics.com tunnel (vedi sotto) |
| Game-Database | PUBLIC (no LICENSE) | Attivo (pipeline multi-AI) | cloud-OK; **no clone Lenovo** | n/a (CMS) |
| evo-tactics-refs-meta | PRIVATE | IDLE (push 2026-04-29) | sovereign-default | n/a (asset) |
| evo-swarm (Dafne) | PRIVATE | IDLE da ~2026-05-08 | sovereign | n/a (orchestratore) |
| vault | PRIVATE | attivo | **sovereign-only** (aider-cloud=ABORT) | n/a (KB) |
| codemasterdd | PRIVATE | attivo (SPRINT_02) | cloud-OK (whitelisted) | n/a (policy) |

**Playable status**: `evo-tactics.com` = Cloudflare Named Tunnel verso
`localhost:3334` (NON hosting cloud persistente -- live solo se backend
Game gira + tunnel up sulla workstation). NON e' una release pubblica
stabile. M6 Release Candidate "no Master DD approval" (sez. 12.2/11.8):
nessun build shippato approvato. Playtest = tabletop-guided M1 (2026-04-17)
+ target 50 playtest M6 futuro. Pillar status tabella sez. 11.1 datata
**2026-04-20** (~4 settimane fa, NON ri-verificata -- trattare come storica).

**Testing/CI** (sparso nel doc, sintesi): Game ~150 AI test + 196 Python
(`npm run test:stack`) | Game-Godot-v2 429 GUT (~56s headless) + CI
gdformat/gdlint | Game-Database Vitest + Playwright E2E + 3 GitHub Action |
codemasterdd governance-lint + promptfoo. Nessun repo ha CI cross-repo
unificata.

**Licensing**: Game/Game-Godot-v2 implicito (no LICENSE esplicito citato).
**Game-Database = PUBLIC senza LICENSE = copyright strict de-facto**
(rischio legale se open-source atteso; decisione MIT/Apache deferred
Eduardo). Asset: 100% CC0/PD/Sonniss (sez. 11.6/12.1).

**Ownership / approval**: progetto single-dev Eduardo Scarpelli
("Master DD" = Eduardo nei doc design = autorita' approvazione finale
gate M0-M6 + merge PR + Q-001 decision). Nessun team.

---

## Numeri canonici (con fonte -- SSoT, non ri-citare altrove)

> Anti-drift (#16/#18): questi numeri vivono QUI. Altre sezioni/DIGEST
> rimandano qui invece di re-asserire. Volatili -> verifica fonte.

| Fatto | Valore | Fonte autoritativa |
|-------|--------|--------------------|
| Trait ETL Godot | 458 | Game `data/core/traits/active_effects.yaml` -> Godot `data/traits/active_effects.json` |
| Specie lifecycle Godot | 15 | Game `data/core/species/*_lifecycle.yaml` -> Godot `data/lifecycle/lifecycles.json` |
| Specie canonical totali | 84 | vault `00E-NAMING_STYLEGUIDE.md` §Modello |
| Job archetipi | 7 | vault `core/20-SPECIE_E_PARTI.md` |
| Biomi | 9 shipping + 11 deferred | vault `41-ART-DIRECTION.md` §Palette matrix |
| Museum card | ~45 (~31 con gioco esterno) | Game `docs/museum/MUSEUM.md` (indice) |
| ADR vault game-design | ~39-44 date-named | vault `Spaces/Dev/Evo-Tactics/adr/` (count approssimato, vedi registry) |
| ADR codemasterdd | 33 numerati (0001-0033) | codemasterdd `docs/adr/` |
| Test Game | ~150 AI + 196 Python | Game `npm run test:stack` |
| Test Godot | 429 GUT (~1499 assert) | Game-Godot-v2 `tests/unit/` |

ADR count = approssimato (repo daily-ship); fonte ground-truth =
`docs_registry.json` / `gh api`. Non trattare come esatto.

---

## Glossario acronimi

| Sigla | Espansione | 1-line |
|-------|-----------|--------|
| d20 | dado 20 facce | core resolver tiro vs CD |
| MoS | Margin of Success | ogni +5 sopra CD = +1 step danno (cap 6) |
| AP | Action Points | budget azioni/turno (2 + reazioni) |
| PT | Punti Tattici (PT spend) | risorsa tattica (perforazione/spinta), cap tuning |
| PP | Punti Potere / combo meter | +hit/+kill/+assist -> sblocca ability |
| SG | Stress / burst per-unit | risorsa stress combat |
| PE | Punti Evoluzione | currency run (costo evoluzione forma ~8) |
| PI | Punti Identita' / pacchetti | currency pack/job unlock |
| Seed | currency meta | output mating/legacy |
| VC | Vettori Comportamentali | metriche aggro/risk/cohesion/setup/explore/tilt |
| MBTI | profilo 4-assi E/N/T/P | 16 forme, reveal diegetico (telemetria ludica) |
| Ennea | Enneagramma | temi personalita' secondari (modulo non-core) |
| NPG | NPC Generator (Director) | genera gruppi spawn per bioma |
| QBN | Quality-Based Narrative | engine narrativo (briefing/debrief) |
| DoD | Definition of Done | gate Godot (prettier+governance+test+smoke) |
| ETL | Extract-Transform-Load | Game YAML -> Godot JSON (`tools/etl/*.py`) |
| FD-ID | Final-Design ID | task backlog freeze (es. FD-006/050) |
| OD | Open Decision | decisione pendente (es. OD-001/013) |
| CAP | Capability (Sprint Impronta) | capability AA01 Game (CAP-11..15) |
| TKT | Ticket sprint | unita' lavoro (es. TKT-P2 Brigandine) |
| EA | Early Access | modello release (EA -> Premium 1.0) |
| A0-A5 | Authority levels | gerarchia fonte verita' (vedi sopra) |
| M0-M6 | Milestone freeze | Baseline->RC (vedi 11.8/12.2) |
| Bundle A/B/C | gruppi feature deferred | scheduling indie-cluster (sez. 11.2D) |
| D4/D5 | decision/writer gate | bottleneck narrativo/scope (sez. 11.2D) |

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

## 6. vault — knowledge base sovereign (design narrative + ricerca)

| Campo | Valore |
|-------|--------|
| Remote | `github.com/MasterDD-L34D/vault` (PRIVATE) |
| Path | `C:\dev\vault-shared` (clone downstream; origin Ryzen `C:\Users\VGit\Vault`) |
| Stack | Obsidian ACCESS + Karpathy LLM-wiki + Ollama LAN + 7 production agent |
| Ruolo | Knowledge base + archivio ricerca + design narrative (layer A5/shadow -- canonical runtime/scope = Game, vedi front-matter "Autorita'") |
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

**Il design narrative + ricerca + ADR storici di Evo-Tactics vivono QUI**
(`Spaces/Dev/Evo-Tactics/`): visione, pilastri, ricerca, glossario design.
**MA** la verita' canonical runtime/scope (meccanica A2 / freeze A3 /
boundary A1) e' in **Game** -- vedi front-matter "Autorita'". vault =
layer A5 + shadow reference: ottimo per *capire il perche'*, non
autoritativo per *cosa shippa*. In conflitto vault perde vs Game A0-A3.

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

## 11-12 -> Design Digest (file separato)

Ispirazioni design (catalogo ~31 titoli + anti-reference + museum) e
stile distillato (naming/font/palette/UI/audio + autorita' design-doc +
pipeline contenuti) vivono nel companion:

**[EVO_TACTICS_DESIGN_DIGEST.md](EVO_TACTICS_DESIGN_DIGEST.md)** -- sez. 11 + 12.

Front-matter condiviso (Autorita' / Stato / Glossario / Numeri canonici)
resta QUI ed e' canonico per entrambi i file.

---

## Coda -- Doc improvement backlog (harsh-review 2026-05-18)

Harsh-review esterno (18 finding). **Risolti in questa revisione** (P0+P1
cheap): #1 contraddizione autorita' (front-matter "Autorita'" unico) ·
#2 TOC (Indice) · #3/#4/#12 staleness (tabella "Stato & attivita'"
datata + playable status + pillar flagged storico) · #6 Skiv archetipo
vs creatura (11.6 wording fix + cross-ref) · #8 glossario · #9 privacy
per-repo · #10 testing/licensing/ownership (front-matter) · #11
portabilita' (nota header) · #14 doppio `---` rimosso · #15 false
precision "tutte le card lette" -> scope honest.

**Risolti in 2a revisione 2026-05-18 (Eduardo ha approvato i deferred):**
- **#13** P2 SPLIT FATTO: GUIDE (0-10 repo map + front-matter canonico) +
  companion [DESIGN_DIGEST.md](EVO_TACTICS_DESIGN_DIGEST.md) (11-12)
- **#5** P1 dedup 11.6/12.1: 11.6 = provenance/refs asset, 12.1 = token
  canonici; prosa "3 modi/palette/audio" duplicata rimossa da 11.6 -> xref 12.1
- **#7** P1 doppio data-flow: §8 GUIDE = sintetico; DIGEST 12.3 = dettaglio;
  Indice + intestazioni segnalano il rimando (no merge -- ruoli distinti voluti)
- **#16/#18** numeri: tabella "Numeri canonici" SSoT in front-matter;
  altrove si rimanda li'
- **#17** forward-ref: Glossario copre Bundle/D4-D5/OD/TKT; scheduling
  dettagliato resta in Game `docs/planning/` (volatile, non duplicato)

Verdetto harsh pre-fix: REWORK. Post 2 revisioni: tutti i finding
P0/P1/P2 risolti o documentati-mitigati -> **SHIP**.

---

> Documento completo. Fonti file-cited verificate 2026-05-18. Path strutturali
> stabili; HEAD/PR/sprint-status volatili -- ri-verifica vault `core/` + Game
> `docs/planning/` + `gh pr list` prima di azioni puntuali.
