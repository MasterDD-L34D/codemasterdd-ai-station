# STATUS_MULTI_REPO — Dashboard operativa cross-repo

> Vista consolidata dei 4 progetti attivi. Aggiornare quando cambia stato significativo o al massimo settimanalmente.
>
> **Governance ownership**: questo repo (codemasterdd) è policy hub, non esegue codice altri progetti. Le azioni specifiche vivono nei rispettivi repo.
>
> Riferimenti deep: CLAUDE.md sezione "Progetti monitorati" (descrittivo), memory `project_multi_repo_overview.md` (architetturale), questo file (operativo).

**Ultimo refresh**: 2026-04-24 auto-mode post-ADR-0015

---

## Snapshot 1-riga per repo

| Repo | Status | Next action | Deadline/trigger | Blocker |
|------|--------|-------------|------------------|---------|
| **codemasterdd-ai-station** | Fase 6 60%, on-track | Review sett.4 + ADR-0015 ratification | ~2026-05-17 | Nessuno bloccante |
| **Synesthesia** | Dormant | Riattiva pre-esame UniUPO | ~agosto 2026 | Nessuno (dormant intenzionale) |
| **Game (Evo-Tactics)** | Q-001 review active + swarm staging `aa82d67f` | Continuazione Q-001 follow-up branch plan | No fixed | Pending PR branch `swarm/register-agents-2026-04-24` |
| **Dafne swarm (evo-swarm)** | Atto 1 day-3/10, server Flask UP idle :5000 | DAY-5 Scout/Solver/Builder family task | 2026-04-26 | Nessuno |

---

## 1. codemasterdd-ai-station (policy hub)

**Path**: `C:\dev\codemasterdd-ai-station\`
**Remote**: [MasterDD-L34D/codemasterdd-ai-station](https://github.com/MasterDD-L34D/codemasterdd-ai-station)

### Piano operativo

- **Fino 2026-05-17** (review settimana 4):
  - Opportunistic dogfood verso n=20 (attuale 12). Non hard-target.
  - H2 cosmetic gap 3 (opportunistic batch)
  - H3 cp1252 monitoring fino n=15 trigger
  - **ADR-0017 rollout phased U0-U4** (UI + observability stack): Aider browser → LiteLLM Proxy → Langfuse → promptfoo → dogfood-ui Flask mini-app. Target ~4h cumulative.

- **2026-05-17** checkpoint:
  - Verifica criterio #2 reliability + #4 cost
  - **ADR-0015 → Accepted** se no regressioni
  - Prep SPRINT_02 post-Max

- **2026-05-19**: Claude Max expiration. Transizione a sovereign tier routing (wrapper cloud + Ollama).

- **Post agosto**: completare M5 Synesthesia privacy (2/3 rimanenti), ADR-0014 criterio #3 retroattivamente PASS.

### Decisioni pendenti
- ADR-0015 (Proposed) ratification
- ADR-0016 (Proposed) awaiting n≥3 data points addizionali
- ADR-0017 (Proposed) UI + observability stack — **scaffolding completato 2026-04-24 auto-mode**, test live pending (U0-U4-test), ratification ~2026-05-17

### Sub-agent ecosystem (`.claude/agents/`)

**18 agent registrati** coprono 4 repo + cross-cutting. Fonti tracciate in `SOURCES.md`:
- 5 core codemasterdd (dogfood/bench/cost/repo-health/adr)
- 4 Game/Evo-Tactics (balance/systems-design/validator/lore)
- 2 Dafne swarm (cycle-analyzer/proposal-triager)
- 3 quality (owasp-security/a11y-wcag/harsh-reviewer)
- 2 DB+privacy (schema-designer/policy-enforcer)
- 2 meta (delegation-classifier/compact-conversation)

Invocabili via Agent tool con `subagent_type: <name>`. Dettaglio: [.claude/agents/README.md](.claude/agents/README.md).

### Stack ADR-0017 — status scaffolding

| Componente | Path | Status code | Status runtime |
|------------|------|:-----------:|:--------------:|
| LiteLLM Proxy config | `infra/litellm/config.yaml` | ✅ validated | ⏸️ not started |
| Langfuse docker setup | `infra/docker-compose.yml` | ✅ validated | ⏸️ not started |
| Postgres init | `infra/postgres/init-multiple-dbs.sh` | ✅ ready | ⏸️ not started |
| promptfoo config | `scripts/quality-bench/promptfoo.config.yaml` | ✅ validated | ⏸️ not installed (npm) |
| dogfood-ui Flask | `apps/dogfood-ui/` | ✅ Python AST OK | ⏸️ not installed (pip) |
| Sub-agents | `.claude/agents/*.md` | ✅ 5 agent registered | ✅ invocabili via Agent tool |

Comando avvio stack completo (quando Eduardo pronto):

```bash
# 1. Setup secrets
cd infra && cp .env.example .env
# (genera NEXTAUTH_SECRET + SALT con openssl rand -base64 32)

# 2. Start docker stack
docker compose up -d

# 3. Start dogfood-ui Python
cd ../apps/dogfood-ui
pip install -r requirements.txt
python app.py

# 4. Install promptfoo globale
npm i -g promptfoo
```

---

## 2. Synesthesia

**Path**: `C:\dev\synesthesia\`
**Remote**: [MasterDD-L34D/synesthesia](https://github.com/MasterDD-L34D/synesthesia)
**Ultima attività tracciata**: `05f8a92 Batch D complete: /about page, image zoom lightbox, notification system`

### Piano operativo

- **Stato**: **DORMANT** fino a ridosso esame UniUPO.
- **Deadline esame**: agosto 2026 (data esatta da confermare).
- **Nessuna azione routinaria richiesta** nel frattempo.
- **Riattivazione attesa**: giugno-luglio 2026 (finale preparazione esame).
- **Priorità 1 a riattivazione**:
  1. Completare M5 privacy validation (≥2 sessioni enforcement classifier: views/ cloud OK, controllers/ sovereign-only)
  2. Task reali normali (bug/feature pre-esame)

### Blocker
Nessuno. La dormancy è status operativo intenzionale, non scope-drop.

### Handoff point
Dormant → Attivo: Eduardo segnala riattivazione → codemasterdd riprende tracking criterio ADR-0014 #3 retroattivo.

---

## 3. Game (Evo-Tactics)

**Path**: `C:\dev\Game\`
**Remote**: [MasterDD-L34D/Game](https://github.com/MasterDD-L34D/Game)
**HEAD**: `aa82d67f feat(swarm): first integration staging — magnetic_rift_resonance trait (#1720)`

### Piano operativo

Governance del Game vive **nel Game repo stesso** (`docs/governance/`). codemasterdd non dirige, **monitora**.

- **Q-001 Decisions Log** (docs/governance/Q-001-decisions-log.md, last_verified 2026-04-17):
  - 11 follow-up branch pianificati (feat/utility-ai-flip, feat/tri-sorgente-bridge, feat/difficulty-*, feat/replay-*, feat/i18n-*, feat/colyseus-boilerplate, feat/a11y-ui, feat/sfx-curation)
  - Stato: review active; merge plan in progress
  - **Ownership**: Eduardo direct su Game, non delegabile a codemasterdd workflow

- **Branch swarm pending**: `swarm/register-agents-2026-04-24` contiene registrazione gameplay-prototyper + combat-engineer. PR pending (mergiata come #1718 nel log HEAD? da verificare). Se non già mergiata, PR manuale.

- **Integration swarm → Game**: pipeline documentata in `docs/pipeline-swarm-to-game.md` (nel Game). Prossimo artifact atteso dopo day-5 Dafne (2026-04-26).

### Blocker visto da codemasterdd
- Nessuno hard. Dipendenze cross-repo: Dafne swarm → Game (write access). Validata live 2026-04-24 (magnetic_rift_resonance trait integrata via #1720).

### Next action visto da codemasterdd
- **Monitorare**: Q-001 follow-up branch progression (Eduardo-driven)
- **Supportare**: pipeline swarm → Game se emergono issue integration
- **Non gestire direttamente**: Q-001 decisions, feat/ branches

### Cross-repo handoff points
- Swarm produce → Game integra: workflow già validato end-to-end (2026-04-24)
- codemasterdd policy → Game adotta: hook commit-msg globale applicato, Conventional Commits enforced, Aider wrapper fruibili anche qui

---

## 4. Dafne swarm (evo-swarm)

**Path**: `C:\Users\edusc\Dafne\workspace\swarm\`
**Remote**: [MasterDD-L34D/evo-swarm](https://github.com/MasterDD-L34D/evo-swarm)

### Piano operativo (Atto 1 day-3/10 in corso)

- **Live status 2026-04-24** (via dogfood-ui proxy + Dafne `/api/status`):
  - Server :5000 UP, HTTP 200, Ollama `qwen3:8b` online, Game repo accessible
  - **52 cicli totali, 0 reject**, 463 artifacts generati
  - **Agent performance**: 3 Specialisti (balancer, lore-designer, species-curator) + 5 Esperti (archivist, asset-prep, biome-ecosystem-curator, dev-tooling, trait-curator) + 3 Apprendisti (biome-gameplay-integrator, combat-engineer, gameplay-prototyper)
  - **Dafne intervention #6**: active, Flint drift detected (gameplay ratio 10% < 20% threshold), last directive: prioritizzare 2 meccaniche giocabili testabili
  - HEAD Dafne: `fb6f5c4` (fix no-cache headers dashboard)
- **Monitoring integrato**: `apps/dogfood-ui` ha panel `/dafne` che proxy verso `:5000` + endpoint `/api/dafne/snapshot` JSON aggregato. Avvia con `python apps/dogfood-ui/app.py`, apri `http://localhost:8080/dafne`.
- **⚠️ Process persistence issue** (tracked 2026-04-24): Dafne server muore dopo ~10-30min senza causa evidente quando launched via `Start-Process -Minimized`. Workaround: usa `START-DAFNE-PERSISTENT.ps1` (auto-restart + log rotation, vedi `docs/reference/dafne-persistence.md`). Per always-on, Task Scheduler opzione 2.
- **Prossimo milestone**: **DAY-5 2026-04-26** — primo task famiglia coordinatori (Solver/Scout/Builder) + Dafne orchestra. Brief già scritto in `DAY-5-BRIEF.md`. Durata stimata 2h.
- **Scope DAY-5**:
  - Consolidare decisione "drift manifest vs reality" da opzione C provvisoria a canonica
  - Test pattern handoff CO-01 (SWARM-CONTROLS v1.0)
  - Output: decisione pubblicata in DECISIONS_LOG swarm + lezione in MEMORY-SHARED.md
- **Server Flask**: UP idle localhost:5000, avviabile/restartabile con `START-SWARM.ps1`
- **Dafne governance dopo DAY-5**: Atto 1 day-5→10 con primi task famiglia applicati a proposte reali. Pilastro 2 attualmente 🟡 (da 🔴 post-H5/H7/H8 integration).

### Open items (OD- tracked in swarm repo)
- **OD-003 Groq key 403** (non bloccante)
- **OD-004 dashboard usage** (observation 1 settimana post day-5)
- **OD-005 Tavily API** (web search degraded)

### Blocker
- Nessuno hard. Server idle consuma RAM/CPU trascurabile.

### Handoff cross-repo
- Dafne propone → Eduardo approva via POST → H5 gate → Game agents/ write
- codemasterdd policy → Dafne segue (API keys centralizzati, Ollama config, commit hook)

---

## Scheduled checkpoints

| Data | Evento | Progetto | Azione |
|------|--------|----------|--------|
| **2026-04-26** | Day-5 Dafne swarm | evo-swarm | Task famiglia + decisione opzione C |
| **2026-04-30** | H4 cost snapshot fine-mese | codemasterdd | Refresh aggregati (già fatto mid-sprint 24/04, finale opzionale) |
| **2026-05-17** | Review settimana 4 | codemasterdd | Verifica criteri ADR-0014 #2/#4 + ADR-0015 Accepted |
| **2026-05-19** | Claude Max expiration | codemasterdd | Transizione sovereign |
| **~2026-05-20** | Fase 6 closure | codemasterdd | ADR-0015 Accepted, transizione Fase 7 |
| **~giugno-agosto 2026** | Synesthesia riattivazione | Synesthesia | M5 privacy + esame prep |

---

## Regola di ingaggio

**Quando apri sessione cold**: leggi CLAUDE.md + COMPACT_CONTEXT.md + questo file (in quest'ordine) → avrai vista operativa completa.

**Quando cambia stato di un repo**: aggiorna la riga corrispondente in questo file (+ ADR/BACKLOG/JOURNAL del repo specifico se necessario).

**Quando emerge decisione multi-repo**: ADR dedicato in codemasterdd `docs/adr/` con scope esplicito cross-repo.
