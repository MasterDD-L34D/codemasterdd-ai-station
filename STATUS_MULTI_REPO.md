# STATUS_MULTI_REPO — Dashboard operativa cross-repo

> Vista consolidata dei 4 progetti attivi. Aggiornare quando cambia stato significativo o al massimo settimanalmente.
>
> **Governance ownership**: questo repo (codemasterdd) è policy hub, non esegue codice altri progetti. Le azioni specifiche vivono nei rispettivi repo.
>
> Riferimenti deep: CLAUDE.md sezione "Progetti monitorati" (descrittivo), memory `project_multi_repo_overview.md` (architetturale), questo file (operativo).

**Ultimo refresh**: 2026-05-10 mattina (post 9/5 sera->10/5 mattina: codemasterdd PR #22-#35 mergeati cumulative 25 PR 7-10/5 + T3+T4 SPRINT_02 pre-validation + cleanup git stale; Game origin/main `7dd18ad` post #2159 BASELINE_WR fix 30 PR mergeati 7-10/5 stream K4/FASE 5/AI sim; Game-Godot-v2 ~230 PR cumulative (+15 post 7/5 sera); Dafne origin/main `9255b4b` PR #102 fase 8 evaluation A/B + PII redaction Atto 2 day 14+).

---

## Snapshot 1-riga per repo

| Repo | Status | Next action | Deadline/trigger | Blocker |
|------|--------|-------------|------------------|---------|
| **codemasterdd-ai-station** | **Fase 6+7 CLOSED**. HEAD `0da13ff` post PR #35 squash-merge 10/5 mattina (25 PR mergeati 7-10/5 cumulative: #11-#21 transition active sovereign + #22-#34 housekeeping + #35 T3+T4 SPRINT_02 pre-validation con dogfood-ui regression fix + runbook hot-restart). 12/18 agent ready. | SPRINT_02 prima sessione 20/05+ (**T1+T3+T4 anticipated DONE**, restano T2/T5/T7) | 2026-05-19 (Claude Max expiration, **9gg residui**) | Nessuno bloccante. H7 ANTHROPIC_API_KEY pending Eduardo direct (Anthropic Console ~5min) |
| **Synesthesia** | Dormant, HEAD `05f8a92` (invariato) | Riattiva pre-esame UniUPO | ~agosto 2026 | Nessuno (dormant intenzionale) |
| **Game (Evo-Tactics Vue3)** | HEAD locale `5f42757a` invariato dal 26/04 (Eduardo non ha pulled), ma **origin/main attivo `7dd18ad` con 30 PR mergeati 7-10/5** stream paralleli: K4 Approach B closure (#2154 9/5), FASE 5 nightly AI sim cron + threshold (#2153/#2155 9/5), BASELINE_WR empirical fix (#2159 10/5), skiv-monitor auto-update (#2152 10/5). Sprint Impronta-specific stato non noto cross-repo (governance interna). 3 PR open al 10/5: #2156 yaml-loader + #2157 registry sync + #2160 tier-s-data-fixes (claude branches, da triagare chat-only se serve). | Triage chat-only PR open se Eduardo richiede. Continue monitoring (no codemasterdd action proattiva) | No fixed | Nessuno (governance interna Game) |
| **Game-Godot-v2** | **~230 PR mergeati cumulative** (+15 PR 7-10/5: #212-#216 + altri). HEAD origin/main `7b92724` (B-NEW-14+15 phone host Conferma mondo CTA fix). Path A canonical CHIUSO end-to-end. Cloned 2026-05-07 in `C:\dev\Game-Godot-v2\`. Hook globali applicati. Governance interna autosufficiente | Continue port (Eduardo-driven), supportare cross-repo se serve | No fixed | Nessuno |
| **Dafne swarm (evo-swarm)** | **Atto 2 day 14+ active**, HEAD origin/main `9255b4b` post PR #102 (fase 8 evaluation A/B + PII redaction, 8/5 16:39 CET). **30 PR mergeati 7-10/5 cumulative** (cleanup decision debt + governance refresh + dashboard fase 8). HEAD locale stale `a87da39` (Eduardo non ha pulled). 0 PR open al 10/5. | Continue Atto 2 (Eduardo-driven), pull locale se Eduardo riprende workflow Dafne | No fixed | Nessuno |
| **AA01 (Archon Atelier 01)** | v1.0.0 silent-driver mode. **2 task PROPOSED storici 25/04 ARCHIVED 9/5 sera** (TIMEOUT one-shot reactive) via H11 closure session, workspace 0 attivi, INDEX.md 3 entries, archive readonly. Smoke test end-to-end PASS 6/6. Memory `project_aa01_studio.md` aggiornata. | Continua driver mode + eventuale nuovo task quando emerge | nessuna | nessuno bloccante |

### Stack ADR-0017 runtime (aggiornato 2026-05-10 post T3 SPRINT_02 hot-restart 2nd pass)

Stack `Accepted` con **T3 SPRINT_02 hot-restart 2nd pass 10/5 mattina PASS**: `docker compose up -d` ~12s wallclock + endpoint LiteLLM/Langfuse 200 OK (via curl 127.0.0.1, NO localhost — vedi runbook PowerShell IPv6 quirk) + **38 trace Langfuse preservati** post 13gg+ downtime (target 7+, no DB corruption). **Regressione `dogfood-ui` VALID_STACKS desync** trovata + fixata path A direct (PR #35 `8722212`). Stack DOWN 10/5 fine sessione (cleanup volumes preservati). Default mode resta **scaffold opt-in** (Docker Desktop non auto-start). Hot-restartable in <60s. DB persistence Postgres+SQLite preservata cross-restart + 38 Langfuse traces persistiti. Procedure complete in `docs/runbook/adr-0017-hot-restart.md` (NEW 10/5 con 5 edge cases documentati).

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

- **Window 07/05 -> 19/05** (**9 giorni residui Claude Max al 10/5 mattina**):
  - Smoke test sovereign DONE 7/5 (3 wrapper aider validati)
  - SPRINT_02 doc completo + T1+T3+T4 anticipated DONE (T1 smoke 7/5 + T3 hot-restart 8/5 + 10/5 retest con regression fix dogfood-ui + T4 cleanup PR esterni gia' triagati 7/5)
  - 25 PR mergeati 7-10/5 (#11-#35 cumulative): governance refresh + ADR-0022 OpenCode tier + transition active sovereign + housekeeping bundle + T3+T4 SPRINT_02 prep
  - **Restano per 20/05+ SPRINT_02**: T2 dogfood organico continuativo, T5 cost tracking primo mese, T7 review fine sprint
  - **Eduardo direct unico residuo**: H7 ANTHROPIC_API_KEY in `~/.config/api-keys/keys.env` via Anthropic Console (~5min, scaffold log gia' pronto in `logs/claude-api-spend-2026-05.md`)

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

### Stack ADR-0017 -- status post-Accepted (2026-05-07, 2nd hot-restart pass 2026-05-10)

Stack `Accepted 2026-05-07` (5/5 criteri PASS) ma in modalita' **scaffold opt-in**: containers down per default, hot-restartable in **~12s wallclock** validato 10/5 (target era <60s). Persistence DB preservata: **38 trace Langfuse preservati** post 13gg+ downtime.

Hot-restart procedure (versione canonical in `docs/runbook/adr-0017-hot-restart.md`):

```bash
cd /c/dev/codemasterdd-ai-station/infra
docker compose up -d
# Atteso: ~12-15s containers + 2-3s Langfuse "Ready"

# IMPORTANTE: usare 127.0.0.1 esplicito su Windows (NO localhost, IPv6 quirk PowerShell)
curl -sf http://127.0.0.1:4000/health/readiness  # LiteLLM 200 OK
curl -sf http://127.0.0.1:3000/api/public/health  # Langfuse 200 OK

# dogfood-ui (Python venv esterno):
cd ../apps/dogfood-ui && python app.py  # :8080
```

Tutti i config + image gia' pulled. No re-setup necessario salvo upgrade pianificato. Edge cases documentati nel runbook (PowerShell IPv6, internal Docker bridge health-check 172.18.0.1, trace count preservation, dogfood-ui regression history).

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
**HEAD locale 2026-04-26**: `5f42757a Merge branch 'aa01/cap-15-imprint-phase' into main (CAP-15 phase merge)` -- invariato dal 26/04 12:53 CET (Eduardo non ha pulled localmente)

**HEAD origin/main 2026-05-10**: `7dd18ad fix(sim): BASELINE_WR.cautious 0.85 -> 0.95 empirical N=40 update (#2159)` -- repo MOLTO attivo: **30 PR mergeati 7-10/5** stream paralleli (K4 Approach B + FASE 5 nightly cron + AI sim threshold + skiv-monitor auto-update). Sprint Impronta-specific stato non noto cross-repo (governance Game-interna).

**Open PR al 10/5**:
- **#2160** `claude/tier-s-data-fixes` (cross-domain audit Tier S+M+L1, 10 ticket gap fixes)
- **#2157** `claude/registry-sync-2026-05-10` (BACKLOG + COMPACT post 10/5 cron P0 + sweep PR)
- **#2156** `claude/sweep-yaml-loader` (opt-in YAML scenario loader per AI sim harness)
- **PR automation cron 4h** (branch `auto/skiv-monitor-update`, author `github-actions[bot]`): pattern auto-skip codemasterdd-side invariato.

**PR mergeati 7-10/5 highlights** (campione, dettaglio non triagato cross-repo per ownership boundary):
- #2159 BASELINE_WR.cautious 0.85->0.95 empirical fix (10/5)
- #2155 CI nightly AI sim split WS port from HTTP TUNNEL (9/5)
- #2154 closure session 9/5 sera K4 Approach B + 4 task autonomous (9/5)
- #2153 FASE 5 nightly cron + threshold checker drift detection (9/5)
- #2152 skiv-monitor auto-update + feed creatura (10/5)
- #2138 + #2139 status-phase-a glossary + policy (gia' MERGED al 9/5 sera tardi -- memory v14 stale indicava DRAFT)

### Piano operativo

Governance del Game vive **nel Game repo stesso** (`docs/governance/`). codemasterdd non dirige, **monitora**.

- **Sprint Impronta Ondata 1 status non noto cross-repo** (HEAD locale invariato 26/04, ma origin/main attivo con stream diversi 7-10/5: K4 Approach B + FASE 5 + AI sim). CAP-11..15 attivita' clusterata 25-26/04 driven by AA01 silent driver mode resta storia:
  - **CAP-11** biome-resolution merge
  - **CAP-12** PlayerRunTelemetry schema + endpoint
  - **CAP-13** imprint-mockup + UX patch anchor "qual e' la mia creatura"
  - **CAP-14** onboarding_v2 schema + `/campaign/start/v2` endpoint
  - **CAP-15** imprint phase V2 (coopOrchestrator phase merge)
  - Pattern branches: `aa01/cap-NN-...` -> merge to main
  - **Ownership**: Eduardo direct su Game (via AA01 capability-by-capability), non delegabile a codemasterdd workflow
- **Status-phase-a feature flow (status-effect)**: PR #2138 + #2139 mergeati al 9/5 sera tardi (memory v14 stale indicava DRAFT, reality MERGED — vedi JOURNAL 2026-05-09 sera tardi -> 10/5 H11 closure)

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
**HEAD locale 2026-05-08**: `a87da39 fix(dafne): proposals lock reentrant + reject gameplay-mechanic-designer (#71)` (Eduardo non ha pulled localmente dal 8/5)

**HEAD origin/main 2026-05-10**: `9255b4b feat(dashboard): fase 8 evaluation A/B + PII redaction (#102)` (8/5 16:39 CET) — **30 PR mergeati 7-10/5 cumulative** (cleanup decision debt + governance refresh + dashboard fase 8 + Atto 2 progressi). 0 PR open al 10/5.

### Piano operativo (Atto 2 day 14+ active)

- **Atto 2 in piena attivita'**: Atto 1 chiuso post-Day-5 (2026-04-26 successo). Cumulative 30 PR mergeati 7-10/5 (incluso fase 8 evaluation A/B + PII redaction in #102). 10 commit dal 25/04 fino al 8/5 00:29 (campione):
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

**Status 2026-05-10**: **~230 PR mergeati cumulative** (PR #216 ultimo documentato + altri post-7/5 fino al 10/5: 15 PR mergeati 7-10/5 totali). 0 PR open al 10/5. HEAD origin/main `7b92724 fix(phone): host Conferma mondo CTA + timeout 60s/retry + WS handler register (B-NEW-14+15+B-NEW-7-v2)`. Dettaglio non triagato in codemasterdd -- governance interna autosufficiente.

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
