# STATUS_MULTI_REPO — Dashboard operativa cross-repo

> Vista consolidata dei 4 progetti attivi. Aggiornare quando cambia stato significativo o al massimo settimanalmente.
>
> **Governance ownership**: questo repo (codemasterdd) è policy hub, non esegue codice altri progetti. Le azioni specifiche vivono nei rispettivi repo.
>
> Riferimenti deep: CLAUDE.md sezione "Progetti monitorati" (descrittivo), memory `project_multi_repo_overview.md` (architetturale), questo file (operativo).

**Ultimo refresh**: 2026-05-07 (post Fase 6 closure ADR-0015 + ADR-0017 Accepted + Codex review + ADR-0021)

---

## Snapshot 1-riga per repo

| Repo | Status | Next action | Deadline/trigger | Blocker |
|------|--------|-------------|------------------|---------|
| **codemasterdd-ai-station** | **Fase 6 CLOSED 2026-05-07** (ADR-0015 + ADR-0017 Accepted), HEAD post PR #2 #4 #5 #6 mergeati, 12/18 agent ready | SPRINT_02 prima sessione 20/05+ | 2026-05-19 (Claude Max expiration) | Nessuno bloccante |
| **Synesthesia** | Dormant, HEAD `05f8a92` (invariato) | Riattiva pre-esame UniUPO | ~agosto 2026 | Nessuno (dormant intenzionale) |
| **Game (Evo-Tactics Vue3)** | **Sprint Impronta Ondata 1 in pieno corso**, HEAD `5f42757a` (CAP-15 imprint phase V2 mergeato), 8+ commit dal 25/04 driven by AA01 capability-by-capability | Continue Sprint Impronta (Eduardo-driven via AA01) | No fixed | Nessuno (lavoro fuori scope codemasterdd) |
| **Game-Godot-v2** | **211 PR mergeati totali**, 5 oggi (#207-#211), Path A canonical CHIUSO end-to-end. **Cloned 2026-05-07 in `C:\dev\Game-Godot-v2\`** (20.7 MB). Hook globali applicati. Governance interna autosufficiente (CLAUDE.md + AGENTS.md propri) | Continue port (Eduardo-driven), supportare cross-repo se serve | No fixed | Nessuno |
| **Dafne swarm (evo-swarm)** | **Atto 2 day 11+ active**, HEAD `1e14253` (health flag draft 07/05 PR #65), 4 commit dal 25/04. ADR-0019 process persistence applicato. | Continue Atto 2 (Eduardo-driven) | No fixed | Nessuno |
| **AA01 (Archon Atelier 01)** | v1.0.0 silent-driver mode -- ha guidato Sprint Impronta Game (CAP-11..15). 2 task PROPOSED storici del 25/04 (#001 voice-test + #002 day-5-post-session-ritual) ancora in workspace | Continua driver mode + eventuale review 2 PROPOSED | nessuna | nessuno bloccante |

### Stack ADR-0017 runtime (aggiornato 2026-05-07, status flip Accepted)

Stack `Accepted` ma in modalita' **scaffold opt-in**: Docker Desktop non auto-start (scelta operativa per non consumare RAM/CPU costante). Hot-restartable in <60s con `cd infra && docker compose up -d`. DB persistence Postgres+SQLite preservata cross-restart.

| Componente | Port | Status code | Status runtime 2026-05-07 | Note |
|------------|-----:|:-----------:|:-------------------------:|------|
| LiteLLM Proxy | 4000 | Accepted | scaffold opt-in (DOWN ora) | Validated 2026-04-24, hot-restartable. v1.82.6 |
| Langfuse | 3000 | Accepted | scaffold opt-in (DOWN ora) | 7+ trace persistiti Postgres preservati. v2.95.11 |
| Postgres | 5432 | Accepted | scaffold opt-in (DOWN ora) | Persistence preservata cross-restart |
| dogfood-ui Flask | 8080 | Accepted | scaffold opt-in (DOWN ora) | v0.2.0, 11 route, side-effect SQLite path worktree noto |
| promptfoo CLI | -- | Accepted | installed v0.121.7 | Smoke 4/4 pass commit `327d078`. Eval on-demand via CLI |
| Dafne swarm (esterna) | 5000 | -- | gestito da repo Dafne separato | Vedi sezione Dafne sotto |

---

## 1. codemasterdd-ai-station (policy hub)

**Path**: `C:\dev\codemasterdd-ai-station\`
**Remote**: [MasterDD-L34D/codemasterdd-ai-station](https://github.com/MasterDD-L34D/codemasterdd-ai-station)

### Piano operativo

- **Fase 6 CLOSED 2026-05-07** (anticipata vs target sett.4):
  - ADR-0015 Accepted (scenario A full-sovereign confermato, soft-override n=12)
  - ADR-0017 Accepted (5/5 criteri ratification PASS, scaffold opt-in)
  - Dataset finale: 12 dogfood, fail rate 8.3%, behavior 5/3 superato, zero silent-corruption

- **Window 07/05 -> 19/05** (12 giorni residui Claude Max):
  - Smoke test sovereign opzionale (3 wrapper aider-cosmetic + aider-refactor + aider-groq) -- validation tecnica
  - SPRINT_02 abbozzo (post-Max scenario A operativo)
  - Cleanup PR esterni opportunistico (#97 + #105 + #10 + #61)

- **2026-05-19**: Claude Max expiration. Transizione a sovereign tier routing (wrapper cloud + Ollama).

- **Post agosto**: completare privacy validation Synesthesia (2/3 rimanenti), ADR-0014 criterio #3 retroattivamente PASS.

### Decisioni pendenti
- ADR-0016 (Proposed) awaiting n>=3 data points addizionali
- Decisione 004 (operativa, da scrivere in DECISIONS_LOG): Codex `/structural-reset` REJECTED 2026-05-07

### Sub-agent ecosystem (`.claude/agents/`)

**18 agent registrati** coprono 4 repo + cross-cutting. Fonti tracciate in `SOURCES.md`:
- 5 core codemasterdd (dogfood/bench/cost/repo-health/adr)
- 4 Game/Evo-Tactics (balance/systems-design/validator/lore)
- 2 Dafne swarm (cycle-analyzer/proposal-triager)
- 3 quality (owasp-security/a11y-wcag/harsh-reviewer)
- 2 DB+privacy (schema-designer/policy-enforcer)
- 2 meta (delegation-classifier/compact-conversation)

Invocabili via Agent tool con `subagent_type: <name>`. Dettaglio: [.claude/agents/README.md](.claude/agents/README.md).

### Stack ADR-0017 -- status post-Accepted (2026-05-07)

Stack `Accepted 2026-05-07` (5/5 criteri PASS) ma in modalita' **scaffold opt-in**: containers down per default, hot-restartable in <60s. Persistence DB preservata.

Hot-restart procedure:

```bash
cd /c/dev/codemasterdd-ai-station/infra
docker compose up -d
# wait ~30s, then verify:
curl http://localhost:4000/health/readiness  # LiteLLM
curl http://localhost:3000/api/public/health  # Langfuse
# dogfood-ui (Python venv esterno):
cd ../apps/dogfood-ui && python app.py  # :8080
```

Tutti i config + image gia' pulled. No re-setup necessario salvo upgrade pianificato.

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
**HEAD 2026-05-07**: `5f42757a Merge branch 'aa01/cap-15-imprint-phase' into main (CAP-15 phase merge)`

### Piano operativo

Governance del Game vive **nel Game repo stesso** (`docs/governance/`). codemasterdd non dirige, **monitora**.

- **Sprint Impronta Ondata 1 in pieno corso** (driven by AA01 silent driver mode, 25/04 -> 07/05):
  - **CAP-11** biome-resolution merge
  - **CAP-12** PlayerRunTelemetry schema + endpoint
  - **CAP-13** imprint-mockup + UX patch anchor "qual e' la mia creatura"
  - **CAP-14** onboarding_v2 schema + `/campaign/start/v2` endpoint
  - **CAP-15** imprint phase V2 (coopOrchestrator phase merge)
  - Pattern branches: `aa01/cap-NN-...` -> merge to main
  - **Ownership**: Eduardo direct su Game (via AA01 capability-by-capability), non delegabile a codemasterdd workflow

- **Q-001 Decisions Log** (docs/governance/Q-001-decisions-log.md): vedi repo Game per status follow-up branch pianificati pre-Sprint-Impronta.

- **Branch swarm**: `swarm/register-agents-2026-04-24` -- da verificare se mergeato durante Sprint Impronta. Pipeline `docs/pipeline-swarm-to-game.md` invariata.

### Blocker visto da codemasterdd
- Nessuno. Sprint Impronta procede senza dipendenze codemasterdd.

### Next action visto da codemasterdd
- **Monitorare**: Sprint Impronta progression (Eduardo+AA01 driven)
- **Non gestire direttamente**: capability CAP-11..CAP-NN, design decisions interni
- **Cross-repo**: hook commit-msg globale + Conventional Commits funzionano automaticamente su Game (no setup repo-specific necessario)

### Audit findings pending (dal game-balance-auditor 2026-04-24, marked ROSSO)

1. **Boss enrage mod 9.0** (vs player mod 2-4) -- gap 4x sopra range giocatore. File target: `C:/dev/Game/data/core/bosses.yaml`
2. **XP curve delta L5->L6: +75** -- +200% sopra mediana progressione. File target: `C:/dev/Game/data/core/xp-curve.yaml`

Da triageare nel BACKLOG repo Game quando Sprint Impronta lascia spazio. Non gestire da codemasterdd (rispetto ownership). Probabilmente il Sprint Impronta tocchera' aree adiacenti -- attendere outcome prima di forzare fix.

### Cross-repo handoff points
- Swarm produce -> Game integra: workflow validato 2026-04-24
- codemasterdd policy -> Game adotta: hook globali applicati, wrapper Aider fruibili

---

## 4. Dafne swarm (evo-swarm)

**Path**: `C:\Users\edusc\Dafne\workspace\swarm\`
**Remote**: [MasterDD-L34D/evo-swarm](https://github.com/MasterDD-L34D/evo-swarm)
**HEAD 2026-05-07**: `1e14253 chore(exports): atto 2 health flag draft 2026-05-07 (#65)`

### Piano operativo (Atto 2 day 11+ active)

- **Atto 2 in piena attivita'**: Atto 1 chiuso post-Day-5 (2026-04-26 successo). 4 commit dal 25/04:
  - `ae82652` weekly digest 27/04 (PR #61 -> origine PR aperto evo-swarm #61)
  - `cf779ef` weekly digest 27/04 atto 2 routine
  - `abcbc4e` gitignore cycle-log archive + .bak rotation (#63)
  - `88a7954` IDENTITY refresh post day 11 (#64)
  - `1e14253` health flag draft 2026-05-07 (PR #65) -- oggi
- **Pilastro 2 evoluzione**: in progresso, IDENTITY refresh suggerisce day 11+ ha generato apprendimenti meta sull'identita' di Dafne. Da audit nel diary se serve detail.
- **Process persistence**: ADR-0019 applicato. Server runnable via `START-SWARM-PERSISTENT.ps1`.
- **Chat personale Dafne**: endpoint `http://localhost:5000/dafne` operativo. Persistence `workspace/memory/dialoghi/YYYY-MM-DD.md`. Fallback chain qwen3:8b local -> groq 70B -> cerebras 8B -> gemini flash.
- **Voice loop**: `dafne_voice.py` pronto, mai testato con mic reale (status invariato dal 25/04).
- **Widget desktop**: `Dafne Widget.lnk` Edge --app mode operativo. Tauri widget scaffoldato non buildato (decision pending).

### Open items (OD- tracked in swarm repo)
- **OD-003** Groq key 403 (non bloccante)
- **OD-004** dashboard usage (observation post-Atto 1)
- **OD-005** Tavily API (web search degraded)

### Blocker
- Nessuno hard. Atto 2 procede stabilmente.

### Handoff cross-repo
- Dafne propone -> Eduardo approva via POST -> H5 gate -> Game agents/ write
- codemasterdd policy -> Dafne segue (API keys centralizzati, Ollama config, commit hook)

---

## 5. Game-Godot-v2 (Evo-Tactics Godot 4.x port, pivot 2026-04-29)

**Path**: `C:\dev\Game-Godot-v2\` (cloned 2026-05-07, 20.7 MB)
**Remote**: [MasterDD-L34D/Game-Godot-v2](https://github.com/MasterDD-L34D/Game-Godot-v2)
**Description**: "Evo-Tactics Godot 4.x port -- pivot 2026-04-29"
**Created**: 2026-04-29
**Last push**: 2026-05-07 sera (active)

### Piano operativo

Repo creato 5 giorni dopo l'inizio del Sprint Impronta Game (Vue3). Pivot strategico: ricostruire shell visuale + UX in engine native (Godot 4.x) mentre Game (Vue3) mantiene Sprint Impronta gameplay logic + telemetria + onboarding.

**Status 2026-05-07 sera**: **211 PR mergeati totali**, 0 open ora.

PR mergeati oggi (5):
- **#207** phone composer handlers (world_tally + world_vote_accepted)
- **#208** GAP-10 AiProgressMeter wire HUD top-strip
- **#209** gdlint debt cleanup CI (fix)
- **#210** GAP-7 PassiveStatusApplier wire main.gd combat setup
- **#211** GAP-5 MissionTimer countdown HUD wire

Milestone: **Path A canonical CHIUSO end-to-end** + Sprint AC bundle 15 sub-sprint (#171-#185, AC.6-AC.18) + W3.5 4 nuove scene + W4 wire CoopApi+LoadingOverlay+ErrorBanner.

**Stack**: Godot 4.x (engine native, GDScript). 200 test file GUT (~1719 test asserts, 178 scripts). addons + scenes + scripts + tests + tools. No Node, no Vue, no Python (radicalmente diverso da Game Vue3).

**Governance interna autosufficiente**: repo ha
- `CLAUDE.md` proprio (con `caveman mode` + Path A status detail + 6 Pilastri)
- `AGENTS.md` proprio per Codex (**multi-client pattern adottato indipendentemente, conferma ADR-0021 con uso reale pre-codemasterdd policy**)
- `.claude/SAFE_CHANGES.md` + `.claude/TASK_PROTOCOL.md` (operating rules locali)

Codemasterdd NON sovrascrive il governance interno -- monitora soltanto.

**Hook globali**: applicati automaticamente via `core.hooksPath = C:/Users/edusc/.local/share/git-hooks` (user-level). Conventional Commits + silent-fail Python Layer 2 ADR-0020 attivi su Game-Godot-v2 senza setup repo-specific. **Open question RISOLTA** dopo clone.

**Relazione con Game (Vue3)**:
- Parallel-run during port phase
- Game (Vue3) = simulation core + gameplay loop + AA01 capability driving (CAP-11..15)
- Godot v2 = visual shell + UX + native engine experience + canonical frontend
- Long-term: Godot v2 frontend canonical, Vue3 archive (decisione futura non ancora ADR)

### Blocker visto da codemasterdd
- Nessuno post-clone. Hook globali applicati, governance interna autosufficiente.

### Next action visto da codemasterdd
- **Monitorare**: PR aperti via `gh pr list --repo MasterDD-L34D/Game-Godot-v2`
- **Non gestire direttamente**: GDScript code, gdlint config, Godot scene files (Eduardo-driven, governance interna)
- **Disponibilita'**: clone locale apre la possibilita' di Aider wrapper su file Godot se serve (es. cosmetic GDScript), ma `aider-cosmetic` Qwen 7B ha pattern wrong-target-file (smoke-1 2026-05-07) -- usare `aider-refactor` se necessario

### Cross-repo handoff points
- Game (Vue3) -> Game-Godot-v2: porting (capability + dati + UX) -- workflow non ancora documentato in pipeline
- codemasterdd policy -> Game-Godot-v2: hook globali applicati (validato), governance interna autonomia preservata

---

## Scheduled checkpoints

| Data | Evento | Progetto | Azione |
|------|--------|----------|--------|
| ~~2026-04-26~~ | Day-5 Dafne swarm | evo-swarm | DONE -- Atto 1 chiuso post Day-5 successo |
| ~~2026-04-30~~ | H4 cost snapshot fine-mese | codemasterdd | DONE -- gia' fatto mid-sprint 24/04 |
| ~~2026-05-07~~ | Fase 6 closure (anticipata vs sett.4 originale) | codemasterdd | DONE -- ADR-0015 + ADR-0017 Accepted |
| **2026-05-19** | Claude Max expiration | codemasterdd | Transizione sovereign (wrapper + Ollama) |
| **2026-05-20+** | SPRINT_02 prima sessione | codemasterdd | Scenario A operativo, smoke test sovereign confermato |
| **~giugno-agosto 2026** | Synesthesia riattivazione | Synesthesia | Privacy validation 2/3 + esame prep |

---

## Regola di ingaggio

**Quando apri sessione cold**: leggi CLAUDE.md + COMPACT_CONTEXT.md + questo file (in quest'ordine) → avrai vista operativa completa.

**Quando cambia stato di un repo**: aggiorna la riga corrispondente in questo file (+ ADR/BACKLOG/JOURNAL del repo specifico se necessario).

**Quando emerge decisione multi-repo**: ADR dedicato in codemasterdd `docs/adr/` con scope esplicito cross-repo.
