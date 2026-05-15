# ADR-0017 — UI + observability stack per CodeMasterDD AI Station

> *TL;DR: codemasterdd-ai-station oggi è "infrastructure-as-code" puro (ADR-0001/0002) senza UI né dashboard — tier routing via wrapper `.cmd`, tracking tramite log markdown, quality bench via JSON raw. Eduardo ha richiesto UI + feature per renderlo "sistema di verifica e coding principale". Research interna (4 repo monitorati) ha mappato lo stack comune (Express/Flask + vanilla JS + Ollama + Aider), research esterna ha identificato 3 tool MIT/Apache che coprono il 90% del gap: **LiteLLM Proxy + Admin UI** (routing unificato + virtual keys + cost dashboard), **Langfuse self-hosted** (observability + tracing + evals), **promptfoo** (bench runner con web viewer). Bonus: **Aider `--browser`** (già installato) per GUI dev-loop immediata. Decisione: adottare stack 3-layer docker-compose + mini-app Flask custom per tracking dogfood Fase 6. Scope codemasterdd evolve da "pure infrastructure-as-code" a "infrastructure-as-code + observability self-hosted + UI glue minimale". Target install ~4h in 4 step phased. Zero subscription ricorrenti preservato.*

- **Status**: **Accepted** (2026-05-07 -- 5/5 criteri ratification PASS, vedi sezione "Closure verdict 2026-05-07" sotto). Originalmente Validated live 2026-04-24 + formal closure pending sett.4.
- **Data**: 2026-04-24 (Proposed + Validated live) -- 2026-05-07 (Accepted)
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev

## Context and Problem Statement

### Situazione attuale

codemasterdd-ai-station funge da policy hub per l'ecosistema (4 repo: questo + Game + Synesthesia + evo-swarm). Operativamente offre:

- **Tier routing AI**: 6 wrapper `.cmd` in `~/.local/bin/` (aider-cosmetic/refactor/groq/cerebras/gemini/openai). CLI-only, scelta tier manuale, nessuna UI.
- **Tracking Fase 6**: log markdown `logs/aider-delegation-YYYY-MM.md` (gitignored). Aggiornamento manuale, nessuna visualizzazione aggregata.
- **Cost monitoring**: `ccusage` per Claude Max (CLI), cloud API spend manually aggregated da entry log. Nessuna dashboard live.
- **Quality bench**: script PowerShell `scripts/quality-bench/run-bench.ps1` + JSON raw in `scripts/quality-bench/results/`. Nessun viewer, correlation dogfood↔bench fatta manualmente (M4 closed recentemente).

### Input Eduardo (2026-04-24 auto-mode)

> "forse un UI e altre feature (cerca online scarica i repo e includili) per CodeMaster che cmq rimane il nostro sistema di verifica e coding principale" + "1 tutto 2 tutto 3 ce ne sono molti citati già nei nostri progetti da monitorare potremmo partire da quelli valutarli e poi fare una tua research aggiuntiva"

Scope allargato: UI (dashboard + tier router + Aider wrapper + bench viewer) + feature aggiuntive. Preferenza: ripartire dai tool già citati nei 4 repo + research esterna.

### Gap diagnosi

| Area | Gap attuale | Impatto |
|------|-------------|---------|
| Routing UI | zero — 6 wrapper `.cmd` hardcoded | switching tier richiede ricordare sintassi CLI; no budget enforcement runtime |
| Observability | log markdown grezzi | no trend analysis, no regression detection automatica, no cost alarm live |
| Cost tracking | aggregazione manuale | rischio drift su Fase 7 sovereign ($20/mese cloud budget ADR-0014) |
| Bench visualization | JSON raw | correlation dogfood↔bench è manual, pain-point M4 |
| Interactive dev-loop | CLI-only | no visual feedback su aider session live, no history browsing UI |

## Research — inventario interno + esterno

### Stack comune già presente nei nostri 4 repo

Scanning effettuato 2026-04-24 su:

- **codemasterdd-ai-station**: Aider 0.86.2 + Ollama 0.21.0 + LiteLLM implicito (env-file) + Claude Code 2.1.116 + GitHub CLI
- **Game (Evo-Tactics)**: Express 4.19 + Prisma 6.2 + xstate@5.30 + inkjs@2.4 + React@18.3 (solo tools/ts) + Vite@5.4 + Playwright@1.48 + prom-client@15
- **Dafne swarm**: Flask + Flask-CORS + Ollama urllib client + **dashboard.html vanilla JS + CSS inline 1200px responsive** (pattern direttamente copiabile)
- **Synesthesia**: Express 4.18 + EJS 3.1 + Passport 0.7 + SQLite3 + Playwright

### Pattern identità cross-repo

- **Backend web**: Express (2/4) + Flask (1/4). Nessun FastAPI. **Flask pattern Dafne → più semplice per mini-app Python in codemasterdd**.
- **UI frontend**: Vanilla JS + HTML (2/4 dashboard-style). Zero SPA obbligatorio. **Dafne dashboard.html riutilizzabile come template**.
- **Test e2e**: Playwright (2/4). Possibile riuso per smoke test UI.
- **Local LLM**: Ollama (2/4, codemasterdd + Dafne). Già consolidato via ADR-0004.
- **LLM routing**: **LiteLLM implicito via Aider env-file** ma nessun proxy centralizzato (Dafne decide modello in codice imperativo).

### Research esterna — short-list candidate

Criteri: licenza MIT/Apache 2.0, offline-capable, dev attivo 2025-2026, Windows-compatible (nativo o Docker-on-Windows OK), supporto LiteLLM preferito.

#### Categoria A — Observability/tracing

| Tool | Licenza | Stars | Fit | Note |
|------|---------|------:|-----|------|
| **Langfuse** | MIT | ~14k | ✅ Top | Integra LiteLLM nativamente. Docker Compose 5-min. Tracing + evals + prompt mgmt + cost tracking per-model/tag. |
| **OpenLLMetry (Traceloop)** | Apache 2.0 | ~7k | ✅ Collector | SDK OpenTelemetry, da abbinare a backend (Langfuse funziona). |
| Helicone | Apache 2.0 | ~5k | 🟡 Secondary | Proxy-style più semplice ma meno feature. |
| Phoenix (Arize) | **Elastic v2** | ~9k | ⚠️ Source-available non OSI. | No showstopper per uso interno, viola spirito sovereign puro. |

#### Categoria B — LLM tier routing / gateway

| Tool | Licenza | Stars | Fit | Note |
|------|---------|------:|-----|------|
| **LiteLLM Proxy + Admin UI** | MIT | ~18k | ✅✅ Top | Già dependency implicita. Virtual keys + budget per-key + spend dashboard per-model/tag + aggiunta modelli runtime senza redeploy. **Unifica i 6 wrapper `.cmd` dietro un singolo endpoint OpenAI-compat**. |
| Open WebUI | BSD-3 (verify recente) | ~90k | 🟡 Complement | UI chat/playground, non routing puro. Complementare, non sostituto. |
| LocalAI | MIT | ~30k | ❌ Duplica Ollama | Skip, non aggiunge valore. |

#### Categoria C — Aider UI / alternative agentic con GUI

| Tool | Licenza | Stars | Fit | Note |
|------|---------|------:|-----|------|
| **Aider Browser UI** (`aider --browser`) | Apache 2.0 | (incluso in Aider ~39k) | ✅ Quick-win | Zero install aggiuntivo (Aider già 0.86.2). Streamlit-based. Preserva tier routing CLI esistente. |
| Continue.dev | Apache 2.0 | ~30k | 🟡 Alt sovereign | Ollama first-class, config JSON come Aider. Semi-agentic (meno autonomo di Aider). |
| Cline | Apache 2.0 | ~40k | ❌ Already eval | ADR-0006 ha già documentato non-viability con Qwen 7B. |
| OpenHands | MIT | ~68k | ❌ Windows pain | Richiede WSL+Docker. Viola "Windows-native zero-overhead". |

#### Categoria D — Bench runner + viewer

| Tool | Licenza | Stars | Fit | Note |
|------|---------|------:|-----|------|
| **promptfoo** | MIT | ~11k | ✅ Top | CLI + web viewer built-in. YAML configs. LiteLLM-compat (chiama endpoint OpenAI-compat → LiteLLM Proxy + Ollama). A/B testing + LLM-as-judge + cost tracking. |
| Inspect AI (UK AISI) | MIT | ~5k | 🟡 Overkill | Eval framework production-grade. Curva apprendimento ripida. Giustificato solo se n dogfood >50. |
| DeepEval | Apache 2.0 | ~5k | 🟡 Framework-only | Viewer best-in-class SaaS (Confident AI), framework OSS CLI-only. |
| OpenAI evals | MIT | — | ❌ Sunset | Low commit velocity 2025-2026. Skip. |

#### Warning licenza

- **Phoenix ELv2**: source-available, non OSI-approved. OK uso interno ma rilassa principio sovereign.
- **Open WebUI**: verificare se licenza recente è cambiata (storicamente MIT → potrebbe aver migrato a BSD-3 o altra).
- **Nessun AGPL/GPL contaminante** tra i candidate top → scope conforme a ADR-0010 skill policy.

## Options

### Opzione A — Stack 3-layer docker-compose self-hosted ✅ RACCOMANDATA

Adottare:

1. **LiteLLM Proxy + Admin UI** (Docker) — centralizza routing tier 1-4, sostituisce wrapper `.cmd` con virtual keys + endpoint OpenAI-compat unificato
2. **Langfuse self-hosted** (Docker Compose) — observability layer, riceve traces da LiteLLM Proxy, sostituisce markdown log strutturato
3. **promptfoo** (`npm i -g`) — bench runner con web viewer, punta a LiteLLM Proxy come endpoint unificato
4. **Aider `--browser`** (già installato) — GUI dev-loop immediata, preserva tier routing
5. **Mini-app Flask custom** (~200 righe Python, copy pattern Dafne) — dogfood tracker UI che legge da Langfuse API + scrive entry classificate, sostituisce editing manuale `logs/aider-delegation-YYYY-MM.md`

**Architettura**:
```
┌─────────────────────────────────────────────┐
│  Utente (browser + CLI)                     │
└──────────┬────────────────┬─────────────────┘
           │                │
   ┌───────▼──────┐  ┌──────▼───────┐
   │ Dogfood UI   │  │ Aider        │
   │ (Flask mini) │  │ --browser    │
   │ :8080        │  │ :8501        │
   └───────┬──────┘  └──────┬───────┘
           │                │
   ┌───────▼────────────────▼───────┐
   │ LiteLLM Proxy + Admin UI       │
   │ :4000 (OpenAI-compat + virtual │
   │   keys + budget + spend)       │
   └──────┬────────────────┬────────┘
          │                │
   ┌──────▼──────┐  ┌──────▼──────────────┐
   │ Ollama      │  │ Cloud free tier +   │
   │ :11434      │  │ paid (Groq/Cereb/  │
   │ (local tier)│  │  Gemini/OpenAI)     │
   └─────────────┘  └─────────────────────┘
          │                │
          └────────┬───────┘
                   │
   ┌───────────────▼──────────────┐
   │ Langfuse (tracing + evals)   │
   │ :3000 + postgres :5432       │
   └──────────────┬───────────────┘
                  │
   ┌──────────────▼───────────────┐
   │ promptfoo viewer :15500       │
   │ (bench results consume        │
   │  LiteLLM + Langfuse datasets) │
   └───────────────────────────────┘
```

**Scope repo evolution**:

- `CLAUDE.md` sezione "Scopo repository" evolve: `"infrastructure-as-code della workstation Lenovo"` → `"infrastructure-as-code + observability self-hosted + UI glue minimale"`
- Nuova directory `infra/` per docker-compose + config files
- Nuova directory `apps/dogfood-ui/` per mini-app Flask custom (solo codice custom residuale)
- **NON** si scarica source code dei tool OSS (docker images pre-built gestiscono tutto)
- **NON** si mescola codice altri progetti (Game/Synesthesia/Dafne restano separati — codemasterdd resta policy hub)

**Pro**:
- Licenze: tutte MIT/Apache 2.0, zero contaminazione
- Cost: $0 (tutti self-hosted + free tier API)
- Install rapido: ~4h total phased (vedi rollout sotto)
- Compatibilità: Docker Desktop Windows OK, tutti tool tested su Windows
- Sovereign: zero subscription, zero cloud paid obbligatorio
- Leverage: unifica 6 wrapper `.cmd` + log manuali + bench JSON sotto un singolo stack

**Contro**:
- Overhead memoria: Langfuse+postgres ~1GB RAM, LiteLLM ~200MB, promptfoo idle 0 (CLI)
- Manutenzione aggiuntiva: 3 servizi docker da aggiornare periodicamente
- Learning curve: ~2-4h setup iniziale, poi maintenance trascurabile

### Opzione B — Minimal: solo Aider `--browser` + quick UI custom

Zero adozione tool esterni. Abilita Aider browser UI + scrivi mini-app Flask tracker custom (tipo Dafne dashboard.html copy).

**Pro**: zero nuove dependency esterne, install <1h, zero docker overhead.
**Contro**: ignora leverage LiteLLM (tier routing resta frammentato), niente tracing strutturato (stessi gap attuali), niente cost enforcement runtime, bench viewer resta manuale.
**Verdict**: sub-optimal long-term. Buono come step 0 se opzione A viene rimandata.

### Opzione C — Full-SaaS (Langfuse Cloud + OpenRouter)

Usa SaaS hosted per observability + SaaS router.

**Pro**: zero self-host maintenance.
**Contro**: viola ADR-0001 "zero subscription", viola ADR-0013 privacy (traces vanno su cloud third-party), lock-in.
**Verdict**: **scartato**. Contraddice pillars sovereign.

### Opzione D — Custom-only (niente tool esterni)

Scrivi dashboard + router + tracing + bench viewer from scratch in Flask/vanilla JS.

**Pro**: full control, zero dependency esterne.
**Contro**: **setup cost enorme** (50-100h vs 4h opzione A), manutenzione continua, zero community, zero feature maturity.
**Verdict**: violates ADR-0005 YAGNI + ADR-0010 skill policy. Scartato.

## Decision

**Opzione A — Stack 3-layer docker-compose + mini-app Flask custom**.

### Rollout phased (4 step, ~4h total)

**Step 0 — Quick win (30 min)**:
- Enable `aider --browser` per capire se basta UI dev-loop
- Zero config aggiuntiva, zero rischio

**Step 1 — LiteLLM Proxy (1h)**:
- `infra/docker-compose.yml` + `infra/litellm/config.yaml`
- Config 6 virtual keys corrispondenti agli attuali wrapper (`cosmetic-7b`, `refactor-14b`, `refactor-30b-moe`, `groq-70b`, `cerebras-8b`, `openai-4o-mini`)
- Budget per-key: `cosmetic/refactor local = $0/mo`, `groq/cerebras = $5/mo`, `openai = $10/mo cap`
- Update `~/.aider.conf.yml` per puntare a `http://localhost:4000` endpoint unificato
- **I wrapper `.cmd` restano come shortcut CLI** (uno riceve `--model <virtual-key>` invece di hardcoded model) → zero break back-compat

**Step 2 — Langfuse observability (1h)**:
- Add `infra/docker-compose.yml` service Langfuse + postgres
- LiteLLM Proxy config: `success_callback: ["langfuse"]`, `langfuse_host: http://localhost:3000`
- Tutti i calls tier 1-4 passano a Langfuse automaticamente
- Dashboard traces + spend per-virtual-key live
- `logs/aider-delegation-YYYY-MM.md` resta come narrative log; dati strutturati vanno in Langfuse (dual-track)

**Step 3 — promptfoo bench viewer (30 min)**:
- `npm i -g promptfoo` (già in stack Node 24 codemasterdd)
- `scripts/quality-bench/promptfoo-config.yaml` punta a LiteLLM Proxy endpoint
- `npx promptfoo eval && npx promptfoo view` apre viewer locale :15500
- Copre HumanEval/custom prompts, confronta modelli side-by-side, viewer web built-in
- `scripts/quality-bench/run-bench.ps1` resta come alternative CLI-only

**Step 4 — Mini-app dogfood UI custom (1.5h)**:
- `apps/dogfood-ui/` — Flask ~200 righe + HTML vanilla JS (copy pattern Dafne dashboard.html)
- Features:
  - List dogfood entries (legge da Langfuse API)
  - Form "new dogfood" (classe/stack/task/esito) → auto-tag in Langfuse via LiteLLM trace metadata
  - Cumulative stats Fase 6 (fail rate per stack/classe)
  - Correlation viewer dogfood ↔ promptfoo bench results
- Endpoint: `:8080`
- **Scope minimo** — sostituisce editing manuale `logs/aider-delegation-*.md` senza reinventare Langfuse

### Consequences

#### Positive

- **Tier routing unificato**: scelta modello runtime via virtual key, no ricordare sintassi 6 wrapper
- **Cost enforcement**: budget per-key runtime, alarm automatici quando si avvicina threshold
- **Observability strutturata**: ogni call tier 1-4 tracciato, trend analysis + regression detection automatica, no più aggregazione manuale dogfood log
- **Bench correlation**: promptfoo + Langfuse insieme risolvono il pain-point M4 (correlation dogfood↔bench) strutturalmente
- **UI dev-loop**: Aider browser per sessioni interactive, dogfood UI per tracking Fase 6, promptfoo viewer per bench
- **Scalabilità**: futuro aggiunta modello non richiede nuovo wrapper — solo entry in `litellm config.yaml` + virtual key
- **Sovereign preserved**: tutto self-hosted, zero subscription ricorrenti, zero lock-in cloud

#### Negative

- **Memory overhead**: ~1.2 GB RAM per Docker services (Langfuse 1GB + LiteLLM 200MB). Su 64GB RAM disponibili, trascurabile.
- **Docker Desktop dependency**: richiede Docker Desktop Windows attivo. Già installato per altri use case (`C:\Program Files\Docker\Docker\resources\bin` in PATH).
- **Manutenzione quarterly**: 3 servizi Docker da aggiornare (~30 min ogni 3 mesi)
- **Learning curve setup**: ~4h iniziale Eduardo per familiarizzare con LiteLLM config + Langfuse UI + promptfoo YAML

### Mitigations

- **Backup strategy pre-install**: snapshot `.aider.conf.yml` + `~/.config/api-keys/keys.env` prima di modifiche. Se LiteLLM setup rompe Aider tier routing, rollback ripristina pattern `.cmd` puri in <5 min.
- **Gradual rollout**: 4 step sequenziali, ognuno verificato prima del next. Se step 1 LiteLLM fallisce, step 2-4 non partono.
- **Dual-track durante migrazione**: `logs/aider-delegation-YYYY-MM.md` resta attivo in parallelo a Langfuse finché Eduardo non conferma switch full (tipicamente dopo 2 settimane operative).
- **Docker Desktop health**: se Docker Desktop non attivo → stack fallback a wrapper `.cmd` + log markdown (pattern attuale invariato disponibile).

## Related

- **ADR-0001** — Sovereign AI strategy (scope evolution, ma pillars preservati)
- **ADR-0005** — YAGNI: NON costruire tool custom quando OSS copre 90%+ del use case
- **ADR-0008** — Hub pattern tier routing (LiteLLM Proxy è evoluzione naturale)
- **ADR-0010** — MADR format + skill install preview+ADR requirement (questo ADR formalizza)
- **ADR-0011** — Cross-agent commit governance (commit-msg hook applicato anche a dogfood-ui commits)
- **ADR-0013** — Tier 3 cloud free providers (virtual keys LiteLLM re-configurano per provider)
- **ADR-0014** — Fase 6 timeline compression (criteri reliability e cost beneficiati dall'automazione tracking)
- **ADR-0015** — Fase 7 budget decision full-sovereign (stack osservabilità rafforza trigger validity)

## Notes

### Perché NON scaricare source code dei tool OSS

User ha chiesto "cerca online scarica i repo e includili". Possibili interpretazioni:

1. **Clone sorgenti in codemasterdd**: scartata. Duplica immenso codebase esterno dentro il policy hub (Langfuse da solo è ~50k file), rompe scope repo, introduce maintenance enormous, viola principio "codemasterdd non contiene codice progetti reali".
2. **Pull docker images pre-built** ✅ scelta. Docker Compose riferenzia immagini ufficiali (`langfuse/langfuse:latest`, `ghcr.io/berriai/litellm:main-latest`), upgrade via `docker compose pull`. Config custom in `infra/*.yaml` = infrastructure-as-code puro.
3. **npm/pip install**: ✅ applicato per `promptfoo` (CLI npm) e eventuali Python deps mini-app dogfood-ui.

Scelta 2+3 preserva onestamente scope repo codemasterdd.

### Skip ADR-0010 preview requirement?

ADR-0010 richiede "skill install preview + ADR" prima di adottare nuovi tool. Questo ADR-0017 **è** la preview + ADR combinata, quindi conforme. Adozione effettiva sarà phased in Sprint 02.

### Dipendenza Node 24 / Python 3.12

- promptfoo richiede Node ≥18 → codemasterdd ha Node 24.15.0 ✅
- Mini-app dogfood-ui richiede Python ≥3.10 + Flask → codemasterdd ha Python 3.12.10 ✅
- Docker Desktop Windows richiede Windows 11 ≥24H2 → codemasterdd ha 25H2 ✅

Tutte le dipendenze infrastrutturali già soddisfatte.

### Ratification trigger (metriche concrete) — UPDATE 2026-04-24 validation

Status **Proposed** → **Accepted** richiede **tutti e 5** i seguenti criteri PASS:

1. **LiteLLM Proxy funzionante**: ✅ **VALIDATED 2026-04-24** — chat completion via `ollama-cosmetic-7b` virtual key risponde HTTP 200 con response Ollama (37 prompt / 2 completion tokens test case).
2. **Langfuse riceve traces**: ✅ **VALIDATED 2026-04-24** — 7 traces + 7 observations in Postgres dopo 4 chat completions di smoke test. Callback automatico funzionante.
3. **promptfoo eval OK**: ⏳ **PENDING** — npm install + YAML config pronto, eval su `problems.json` non ancora run.
4. **Dogfood-ui Flask up**: ✅ **VALIDATED 2026-04-24** — `/api/health` mostra `langfuse.configured:true + reachable:true`, entry #1 creata via POST API, Dafne integration via proxy (quando Dafne server UP).
5. **Maintenance budget rispettato**: ⏳ **IN PROGRESS** — setup totale stimato ~3h cumulative (pull images + 2 blocker fix + smoke test). Sotto stima 4h originale ✅.

**3/5 criteri PASS live, 2/5 pending completamento routine**. Setup è stato più rapido dell'atteso grazie alla pre-seeding API keys via env var.

**Soft criteria** (non bloccanti ma tracked):
- Docker Desktop uptime stabile per 7gg post-up
- Zero data loss Langfuse DB
- Nessuna licenza tool cambiata a breaking terms

**Hard blocker** (se qualsiasi emerge, ratification fail + revisione):
- Password mismatch / init script failure (come identificato in harsh review 2026-04-24)
- Langfuse self-host instabile (crash >1/gg)
- LiteLLM config drift tra versioni (breaking change non documentato)
- Performance degrade >20% su Aider workflow (wrapper attuale vs nuovo via proxy)

**Rollback plan**: se uno degli Hard blocker materializza → `docker compose down -v` + ripristina `.aider.conf.yml` pre-stack (backup fatto a Step 1). Tempo rollback target: <10 min.

Target Status Accepted: **~2026-05-17** (coincide con review settimana 4 + ADR-0015 ratification).

## Closure verdict 2026-05-07

Status flip da **Validated live + Proposed** a **Accepted**. Closure anticipata vs target ~2026-05-17 originale. Coerente con closure ADR-0015 stessa data.

### Rating finale 5/5 criteri

| Criterio | Status | Evidenza |
|----------|--------|----------|
| 1. LiteLLM Proxy funzionante | PASS | Validated 2026-04-24, HTTP 200 chat completion via virtual key `ollama-cosmetic-7b` (37/2 token test) |
| 2. Langfuse riceve traces | PASS | Validated 2026-04-24, 7 traces + 7 observations Postgres-persisted, callback automatico OK |
| 3. promptfoo eval OK | PASS | Validated 2026-04-24/25, smoke 4/4 pass via virtual key env var (commit `327d078`) |
| 4. Dogfood-ui Flask up | PASS | Validated 2026-04-24/25, `/api/health`, entry creation via POST API, Dafne integration via proxy. v0.2.0 con 11 route |
| 5. Maintenance budget rispettato | PASS | Setup totale ~3h vs stima 4h (sotto budget 25%) |

### Soft criteria (non bloccanti, status informativo 2026-05-07)

- Docker Desktop uptime: stack e' opt-in (Docker Desktop non auto-start, scelta operativa). Hot-restartable in <60s con `docker compose up -d`. DB persistence (Postgres + SQLite) preservata cross-restart -- 7+ traces ancora persistiti.
- Zero data loss: confermato (Postgres + dogfood SQLite intatti).
- Licenze tool: nessun cambio breaking dal 2026-04-24 (LiteLLM v1.82.6, Langfuse v2.95.11, promptfoo v0.121.7).

### Hard blocker check (2026-05-07)

- Password mismatch / init script failure: NON emerso post 2026-04-24 (fix harsh review applicato + DB ricreato OK).
- Langfuse self-host instabile: NON emerso, container stabile durante 24h+ uptime testato.
- LiteLLM config drift: nessun upgrade involontario.
- Performance degrade Aider: non misurato direttamente, wrapper continuano a girare via `~/.local/bin/aider-*` con `~/.aider.conf.yml` env-file (LiteLLM proxy NOT-in-middle del path Aider, viene usato solo per traces opzionali via callback). Path Aider invariato vs pre-stack.

### Note operative post-Accepted

1. **Stack opt-in**: Docker Desktop non parte automaticamente al boot Windows (decisione operativa per non consumare RAM/CPU costante). Avvio manuale quando si vogliono usare le feature dashboard/tracing/eval. `cd infra && docker compose up -d` (~30s).
2. **Aider workflow**: indipendente dal proxy. Wrapper `aider-cosmetic`/`aider-refactor`/`aider-groq-bypass`/`aider-cerebras`/`aider-gemini`/`aider-openai` continuano a usare `~/.aider.conf.yml` con env-file -> direct provider call. LiteLLM e' opzionale per cost tracking centralizzato. (Update 2026-05-13: `aider-groq` rimosso, sostituito da `aider-groq-bypass` per LiteLLM-Groq adapter bug streaming hang -- vedi CLAUDE.md.)
3. **dogfood-ui** restera' utility tool per dogfood entries futuri. SQLite path locked a `apps/dogfood-ui/data/dogfood.sqlite` (worktree-side-effect noto in COMPACT v10).
4. **Bench viewer**: promptfoo run-on-demand via CLI o web (`promptfoo view`). Eval futuri tracked in `scripts/quality-bench/results/`.

### Action items post-closure

1. SPRINT_02 abbozzo deve includere "stack ADR-0017 hot-restart procedure" come bullet (non re-architecture)
2. Eventuale dogfood post-Max che trigga issue stabilita' (Langfuse drift, Docker break) -> ADR addendum, non riapertura ADR-0017
3. STATUS_MULTI_REPO.md "Stack ADR-0017 runtime" tabella aggiornata: status colonna runtime cambia in "scaffold opt-in" (vs "live" precedente) per riflettere Docker Desktop opt-in pattern

