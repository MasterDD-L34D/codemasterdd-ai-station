# STATUS_MULTI_REPO — Dashboard operativa cross-repo

> Vista consolidata dei 4 progetti attivi. Aggiornare quando cambia stato significativo o al massimo settimanalmente.
>
> **Governance ownership**: questo repo (codemasterdd) è policy hub, non esegue codice altri progetti. Le azioni specifiche vivono nei rispettivi repo.
>
> Riferimenti deep: CLAUDE.md sezione "Progetti monitorati" (descrittivo), memory `project_multi_repo_overview.md` (architetturale), questo file (operativo).

**Ultimo refresh**: 2026-05-09 mattino (post transition active sovereign 8/5 sera -> 9/5 notte: 12 PR codemasterdd #11-#21 mergeati, **ADR-0022 OpenCode tool-use Accepted**, OpenCode v1.14.41 installato. Game: PR #2108 mergeato 8/5 11:15 UTC; **NEW 2 PR DRAFT 9/5 mattino**: #2138 + #2139 `feat/status-phase-a-*` possibile Ondata 2 status-effect)

---

## Snapshot 1-riga per repo

| Repo | Status | Next action | Deadline/trigger | Blocker |
|------|--------|-------------|------------------|---------|
| **codemasterdd-ai-station** | **Fase 6+7 CLOSED + ADR-0022 OpenCode tool-use Accepted 9/5**. HEAD `a71d653` post PR #21 (12 PR mergeati 8-9/5: governance refresh + drift cleanup + ADR-0022 ciclo + transition active sovereign). 12/18 agent ready. | SPRINT_02 prima sessione 20/05+ (T1+T3+T4 anticipated DONE) | 2026-05-19 (Claude Max expiration, 10gg residui) | Nessuno bloccante |
| **Synesthesia** | Dormant, HEAD `05f8a92` (invariato) | Riattiva pre-esame UniUPO | ~agosto 2026 | Nessuno (dormant intenzionale) |
| **Game (Evo-Tactics Vue3)** | **Sprint Impronta Ondata 1 in pausa dal 26/04** (HEAD `5f42757a`, ~13gg). PR #2108 swarm-distillation **MERGED 8/5 11:15 UTC**. **NEW 9/5 mattino: 2 PR DRAFT** `feat/status-phase-a-glossary` (#2138, 5 status-effect traits) + `feat/status-phase-a-policy` (#2139, debuff target preference) -- possible Ondata 2 status-effect feature flow. +N PR cron 4h `auto/skiv-monitor-update` auto-skip pattern. | Aspetta PR #2138/#2139 escano DRAFT prima di triage chat-only. Continue Sprint Impronta (Eduardo+AA01 driven). Auto-skip PR cron skiv-monitor. | No fixed | Nessuno (DRAFT non bloccanti, routine PR cron auto-skip) |
| **Game-Godot-v2** | **215 PR mergeati totali** (+4 post 7/5 sera, dettaglio non triagato in codemasterdd), Path A canonical CHIUSO end-to-end. Cloned 2026-05-07 in `C:\dev\Game-Godot-v2\` (20.7 MB). Hook globali applicati. Governance interna autosufficiente | Continue port (Eduardo-driven), supportare cross-repo se serve | No fixed | Nessuno |
| **Dafne swarm (evo-swarm)** | **Atto 2 day 12+ active**, HEAD `a87da39` (4 PR pushati 7/5 sera: #67 anchor split + #68 OD-006 close + #69 tournament survivor fix + #70 OD-002+OD-003 close + 1 PR 8/5 00:29: #71 proposals lock fix). 3 OD storici chiusi. | Continue Atto 2 (Eduardo-driven) | No fixed | Nessuno |
| **AA01 (Archon Atelier 01)** | v1.0.0 silent-driver mode -- ha guidato Sprint Impronta Game (CAP-11..15). 2 task PROPOSED storici del 25/04 (#001 voice-test + #002 day-5-post-session-ritual) ancora in workspace | Continua driver mode + eventuale review 2 PROPOSED | nessuna | nessuno bloccante |

### Stack ADR-0017 runtime (aggiornato 2026-05-09, post transition active 8/5 sera)

Stack `Accepted` con **transition active validata 8/5 sera** (`docker compose up -d` per smoke OpenCode + dogfood reali, T3 SPRINT_02 hot-restart anticipato + passato in <60s). **Stack DOWN 9/5 fine sessione** (cleanup volumes preservati). Default mode resta **scaffold opt-in** (Docker Desktop non auto-start). Hot-restartable in <60s con `cd infra && docker compose up -d`. DB persistence Postgres+SQLite preservata cross-restart + 7+ Langfuse traces persistiti per debug futuro.

| Componente | Port | Status code | Status runtime 2026-05-08 | Note |
|------------|-----:|:-----------:|:-------------------------:|------|
| LiteLLM Proxy | 4000 | Accepted | scaffold opt-in (DOWN) | Validated 2026-04-24, hot-restartable. v1.82.6 |
| Langfuse | 3000 | Accepted | scaffold opt-in (DOWN) | 7+ trace persistiti Postgres preservati. v2.95.11 |
| Postgres | 5432 | Accepted | scaffold opt-in (DOWN) | Persistence preservata cross-restart |
| dogfood-ui Flask | 8080 | Accepted | scaffold opt-in (DOWN) | v0.2.0, 11 route, side-effect SQLite path worktree noto |
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
**HEAD 2026-05-08**: `5f42757a Merge branch 'aa01/cap-15-imprint-phase' into main (CAP-15 phase merge)` (invariato dal 26/04 12:53 CET, pausa Sprint Impronta ~12gg)

**Open PR**:
- **#2108** swarm-distillation run #5 stress mechanics + biomi extreme (branch `claude/swarm-distillation-2026-05-08`, Claude Code session creato 7/5 22:19 UTC). Triagato chat-only 2026-05-08: merge-ready dal POV codemasterdd, decisione Game-side per ownership boundary.
- **PR automation cron 4h** (branch `auto/skiv-monitor-update`, author `github-actions[bot]`): rigenerato ogni ~4h dal workflow `skiv-monitor.yml`. Scope safe-list `data/derived/skiv_monitor/` + `docs/skiv/MONITOR.md`. **Pattern auto-skip**: codemasterdd NON traccia numero PR specifico (cambia continuamente), NON valuta merge (deterministico Game-side). Esempio storico: #2117 (8/5 02:45 UTC) triagato come reference.

### Piano operativo

Governance del Game vive **nel Game repo stesso** (`docs/governance/`). codemasterdd non dirige, **monitora**.

- **Sprint Impronta Ondata 1 in pausa dal 26/04** (driven by AA01 silent driver mode, attivita' clusterata 25-26/04):
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
- **Triagare PR #2108** (low priority, swarm distillation routine output): valutare merge/comment/close in slot dedicato. Non bloccante.
- **Auto-skip PR cron 4h `skiv-monitor`** (`auto/skiv-monitor-update` branch): pattern automation safe-list-confined, no triage codemasterdd-side; decisione merge Game-side deterministica.
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
**HEAD 2026-05-08**: `a87da39 fix(dafne): proposals lock reentrant + reject gameplay-mechanic-designer (#71)` (4 commit 7/5 sera + 1 commit 8/5 00:29 CET)

### Piano operativo (Atto 2 day 12+ active)

- **Atto 2 in piena attivita'**: Atto 1 chiuso post-Day-5 (2026-04-26 successo). 10 commit dal 25/04 (5 fino al 7/5 mattina + 4 nuovi 7/5 sera + 1 nuovo 8/5 00:29):
  - `ae82652` weekly digest 27/04 (PR #61)
  - `cf779ef` weekly digest 27/04 atto 2 routine
  - `abcbc4e` gitignore cycle-log archive + .bak rotation (#63)
  - `88a7954` IDENTITY refresh post day 11 (#64)
  - `1e14253` health flag draft 2026-05-07 (PR #65)
  - `49c1ab8` compass realignment anchor split + OD-006 handoff (#67) -- 7/5 sera
  - `b38904d` close OD-006 outcome A + STATUS slot (#68) -- 7/5 sera
  - `7a0df9d` tournament survivor fallback + keys.env load .bat fix (#69) -- 7/5 sera
  - `53d58d6` close OD-002 + OD-003, defer OD-004 (#70) -- 7/5 sera
  - `a87da39` proposals lock reentrant + reject gameplay-mechanic-designer (#71) -- 8/5 00:29 CET
- **3 OD storici chiusi in 1 sera**: OD-002, OD-003, OD-006 risolti. Decision debt cleanup massiccio.
- **Pilastro 2 evoluzione**: IDENTITY refresh suggerisce day 11+ ha generato apprendimenti meta sull'identita' di Dafne. Anchor split (pillar 3<->4) in #67 documenta evoluzione concreta.
- **Process persistence**: ADR-0019 applicato. Server runnable via `START-SWARM-PERSISTENT.ps1`.
- **Chat personale Dafne**: endpoint `http://localhost:5000/dafne` operativo. Persistence `workspace/memory/dialoghi/YYYY-MM-DD.md`. Fallback chain qwen3:8b local -> groq 70B -> cerebras 8B -> gemini flash.
- **Voice loop**: `dafne_voice.py` pronto, mai testato con mic reale (status invariato dal 25/04).
- **Widget desktop**: `Dafne Widget.lnk` Edge --app mode operativo. Tauri widget scaffoldato non buildato (decision pending).

### Open items (OD- tracked in swarm repo, status post-7/5 sera)
- **OD-002** ~~chiuso 7/5 (PR #70)~~
- **OD-003** ~~Groq key 403 chiuso 7/5 (PR #70)~~
- **OD-004** dashboard usage -- **deferred** (status update PR #70)
- **OD-005** Tavily API (web search degraded) -- status invariato
- **OD-006** ~~outcome A chiuso 7/5 (PR #68)~~

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

**Status 2026-05-08**: **215 PR mergeati totali** (PR #215 ultimo mergeato), 0 open ora. +4 PR oltre il count del 7/5 sera (#212-#215, dettaglio non triagato in codemasterdd -- governance interna autosufficiente).

PR mergeati 7/5 sera (5, ultimi documentati a livello cross-repo):
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
| ~~2026-05-08~~ | Governance refresh (drift fix STATUS + COMPACT v12) | codemasterdd | DONE -- branch governance-refresh-2026-05-08 |
| **2026-05-19** | Claude Max expiration | codemasterdd | Transizione sovereign (wrapper + Ollama) |
| **2026-05-20+** | SPRINT_02 prima sessione | codemasterdd | Scenario A operativo, smoke test sovereign confermato |
| **~giugno-agosto 2026** | Synesthesia riattivazione | Synesthesia | Privacy validation 2/3 + esame prep |

---

## Regola di ingaggio

**Quando apri sessione cold**: leggi CLAUDE.md + COMPACT_CONTEXT.md + questo file (in quest'ordine) → avrai vista operativa completa.

**Quando cambia stato di un repo**: aggiorna la riga corrispondente in questo file (+ ADR/BACKLOG/JOURNAL del repo specifico se necessario).

**Quando emerge decisione multi-repo**: ADR dedicato in codemasterdd `docs/adr/` con scope esplicito cross-repo.
