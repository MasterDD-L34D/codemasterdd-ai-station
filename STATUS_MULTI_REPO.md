# STATUS_MULTI_REPO — Dashboard operativa cross-repo

> Vista consolidata dei 4 progetti attivi. Aggiornare quando cambia stato significativo o al massimo settimanalmente.
>
> **Governance ownership**: questo repo (codemasterdd) è policy hub, non esegue codice altri progetti. Le azioni specifiche vivono nei rispettivi repo.
>
> Riferimenti deep: CLAUDE.md sezione "Progetti monitorati" (descrittivo), memory `project_multi_repo_overview.md` (architetturale), questo file (operativo).

**Ultimo refresh**: 2026-05-12 sera (post cluster Bundle 1+2+3 12/5 sera + residual auto-ratification ADR-0025+0026: codemasterdd HEAD `1be6c5b` post PR #65 cumulative **47 PR 7-12/5** + **3 plugins installed** ecosystem MAJOR upgrade (compass + superpowers v5.1.0 + claude-mem v13.2.0 + 4 marketplaces + Bun v1.3.13 + repomix v1.14.0) + **5 research docs Bundle 2+3** + 2 lessons promoted (L-010 reflexive methodology audit + L-011 applicative optimization audit) + ADR-0025/0026 ratified Accepted; Game HEAD `36c9822` post PR #2258 200 PR last 14d sprint; Game-Godot-v2 HEAD `a765e4e` post PR #249 +34 PR dal 7/5 (+2 codemasterdd-authored #248+#249 TKT-P2 Phase D complete); Dafne stable HEAD `9255b4b` post PR #102 8/5 14:39 4gg inattivita'; **vault-shared HEAD `2007a8a2` 12/5 7/7 PRODUCTION milestone hit** + frontmatter drift 7/7 identificato + handoff doc Eduardo-direct `docs/aa01-handoff/2026-05-12-vault-frontmatter-drift-handoff.md`).

---

## Snapshot 1-riga per repo

| Repo | Status | Next action | Deadline/trigger | Blocker |
|------|--------|-------------|------------------|---------|
| **codemasterdd-ai-station** | **Fase 6+7 CLOSED**. HEAD `1be6c5b` post PR #65 12/5 sera (**47 PR mergeati 7-12/5 cumulative**: pre-cluster #11-#62 + cluster 12/5 sera #63 Bundle 1 hygiene + #64 Bundle 2 methodological + #65 Bundle 3 applicative). **Plugin ecosystem MAJOR upgrade**: 3 plugins (compass v0.4.3 + superpowers v5.1.0 + claude-mem v13.2.0) + 4 marketplaces + Bun v1.3.13 + repomix v1.14.0. **ADR-0025+0026 ratified Accepted** auto 12/5 sera. **11 lessons** AA01 cumulative (L-001 + L-002..L-011). 12/18 agent ready (3 grandfathered + 6 dormant workflow-driven). | SPRINT_02 prima sessione 20/05+ (T1+T3+T4 anticipated DONE, restano T2/T5/T7) | 2026-05-19 (Claude Max expiration, **7gg residui**) | Nessuno bloccante. H7 ANTHROPIC_API_KEY pending Eduardo direct (Anthropic Console ~5min, browser-direct) |
| **Synesthesia** | Dormant, HEAD `05f8a92` (invariato) | Riattiva pre-esame UniUPO | ~agosto 2026 | Nessuno (dormant intenzionale) |
| **Game (Evo-Tactics Vue3)** | **HEAD `36c9822` post PR #2258 11/5** (200 PR last 14d sprint multi-track). Local checkout `C:/dev/Game` reset --hard origin/main 2026-05-12 (Path A confirmed post Protocol 1+2 investigation: 27 commit AA01 CAP-* Sprint Impronta MAI shipped a origin -> safe abandon via 13 backup branches `aa01/cap-*` + stash safety net 295 file WIP refactor). PR open: solo #2257 skiv-monitor (auto-skip pattern). **OD-023 APERTA 2026-05-12** (Phase B execution date verdict, Path C+Path A 34/35). | Continue monitoring (Eduardo-driven). NO codemasterdd action proattiva. **Phase B Day 7 formal closure scheduled 2026-05-14 mattina UTC** (sub-event ADR-0024 codemasterdd addendum PR #55). | **2026-05-14** Phase B closure | Nessuno (governance interna Game autonoma) |
| **Game-Godot-v2** | **249 PR mergeati cumulative** (+34 PR dal 7/5, +2 questa sessione codemasterdd-authored: #248 Main SeasonalService wire + #249 Phone MODE_ORGANIZATION). HEAD origin/main `a765e4e` PR #249. Local checkout pulled fast-forward post-merge. Path A canonical CHIUSO + Sprint AC bundle closed. Hook globali applicati. Governance interna autosufficiente. **TKT-P2 Brigandine Phase D cross-stack chain COMPLETE 2026-05-12**: backend (Game #2251+2252+2253) -> Godot HTTP client (#245) -> TV season label (#245) -> Main caller wire (#248) -> Phone organization mode (#249). | Continue port (Eduardo-driven). Deferred follow-up GUT integration tests test_main_seasonal_wire.gd + test_phone_composer_organization.gd (~55 LOC totali, NON blocking). | No fixed | Nessuno |
| **Dafne swarm (evo-swarm)** | **Stable post-dashboard sprint**, HEAD origin/main `9255b4b` post PR #102 (fase 8 evaluation A/B + PII redaction, 8/5 14:39 UTC). **20 PR cascata 8/5** (PR #83-#102 dashboard fase 0-8 + Tier 4 fix x3 + orchestrator CO-02 + compass anchor fix). **4gg inattivita' post 8/5** (no commit dal 8/5). 0 PR open. Atto 2 status post-sprint indeterminate (probabilmente concluded post dashboard fase 8). | Continue (Eduardo-driven), pull locale se workflow Dafne riprende | No fixed | Nessuno |
| **AA01 (Archon Atelier 01)** | v1.0.0 silent-driver mode. Counter 12/5 sera post Bundle 1+2+3: **14 archive entries + 11 lessons cumulative**. Bundle 2 SHIP + Bundle 3 SHIP questa sessione (2 task addizionali). 11 lessons cross-session `learnings/`: L-2026-04-001 + L-2026-05-002..L-2026-05-011 (+L-010 reflexive methodology audit + L-011 applicative optimization audit promoted 12/5 sera). Workspace 0 attivi. Inbox cleanup 12/5 pomeriggio. | Continua driver mode + nuovo task quando emerge. OD-007 Three Strikes counter: frizione tool-selection NON osservata. | nessuna | nessuno bloccante |
| **vault-shared (Vault Knowledge Mgmt)** | **Sibling-peer Eduardo, monitored. 7/7 production agents milestone hit 2026-05-12** (HEAD `2007a8a2` "feat(milestone) 7/7 agents PRODUCTION + bulk ingest 100/100"). **Frontmatter drift 7/7 identificato** spot-check empirical 12/5 sera: production/agents/*.md status: draft non-synced (drift 100%). LLM routing matrix v1.0 path `Extras/config/llm-routing.json`. Stack overlap codemasterdd: Ollama LAN + qwen2.5-coder family + deepseek-r1 + Claude variants. Privacy: sovereign-only (NOT cloud whitelist). Hook globali compat VALIDATED. **Pattern D ADOPT codemasterdd 2026-05-12** (governance-lint.ps1 PR #51, audit-then-replay NO clone). **V3 cross-pattern adoption Quality Gate**: research doc Bundle 2 12/5 sera, DEFER fino SPRINT_02+. | Continue (Eduardo-driven). **Handoff doc Eduardo-direct** `docs/aa01-handoff/2026-05-12-vault-frontmatter-drift-handoff.md` (frontmatter fix + CLAUDE.md drift + README discoverability, 30-45min one-shot). NO write-path codemasterdd-side. | No fixed | Nessuno (sibling-peer disjoint scope) |

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

**HEAD origin/main 2026-05-12 mattina**: `36c9822 chore(phase-b): Day 5/8 OOA audit + Path C handoff preserve (#2258)` -- **repo ATTIVISSIMO**: **200 PR mergeati last 14d**, NON pausa. Sprint multi-track scope ampliato post 26/04 con Phase B + Brigandine + Conviction + trait-editor Vue3 rebuild.

**Open PR al 12/5**:
- **#2257** `claude/skiv-monitor` auto-update stato + feed creatura (cron 4h automation, pattern auto-skip codemasterdd-side invariato)

**Cascata 11/5 sera (27 PR mergeati in ~13h, #2228-#2258)**:
- **TKT-M14 Conviction system 3 phases** (#2248 A combat + #2249 B narrative + #2250 C api endpoints close AC3)
- **TKT-P2 Brigandine seasonal campaign 3 phases** (#2251 A engine + #2252 B yaml content + #2253 C api endpoints 6+10 tests)
- **TKT-C1 trait-editor Vue3 rebuild** (#2243 AngularJS->Vue3 4/5 surface + #2247 FE editor view full close C1 ADR-2026-05-10)
- **TKT-M14-A elevation + terrain** (#2246 P1 Tattica)
- **TKT-M15 CT bar audit + promotion engine** (#2242 4.5/5 acceptance + 17 test) + **TKT-M15-FE** UI promotion accept/defer (#2245)
- **TKT-P6 rewind safety valve** (#2241 3-snapshot buffer + #2244 P6-FE rewind HUD)
- **TKT-C4 mutation forbidden paths** (#2239 12/12 kinds Phase 6 complete)
- **TKT-B1 V6 UI TV dashboard polish** (#2240 proactive 4 scoped edits)
- **TKT-C6 Game Balance & Economy Tuning skill** (#2238 install-doc canonical)
- **species_expansion schema canonical migration** (#2237 morph_slots -> trait_plan, ADR-2026-05-11 ACCEPTED + #2230 ADR Proposed earlier in day)
- **Phase B governance** (#2229 Day 4 monitor + #2232 Day 5 grace iter4 + #2256 Day 7 closure pre-stage + #2258 Day 5/8 OOA audit + Path C handoff)
- **master-dd verdict batch 11 decisioni ACCEPT** (#2234)
- **2 T3 species ship** (#2235 tempestarius_psionicus + magmocardium_furens close trait residue)
- **TKT-P2 species Phase A engine** (#2251)
- **dist auto-build mission-console** (#2221 source-driven)
- **ennea dedup duration tie-break fix** (#2255 Lealista buff wins over Coordinatore)
- **closure docs COMPACT v38->v39->v40** + memory save 2026-05-11 (#2233 + #2254)
- **fix tests baseline-drift service** (#2227 restore 6 failures)
- **docs p4 Thought Cabinet round-mode adoption** (#2226 Sprint 6 +14gg)
- **chore governance weekly drift audit** (#2228 11/5)

### Piano operativo

Governance del Game vive **nel Game repo stesso** (`docs/governance/`). codemasterdd non dirige, **monitora**.

- **Sprint Impronta narrative SUPERSEDED 2026-05-12**: HEAD locale invariato 26/04, ma origin/main ha pivotato a scope ampliato Phase B + Brigandine + Conviction + trait-editor Vue3 rebuild + master-dd verdict batch. CAP-11..15 attivita' clusterata 25-26/04 driven by AA01 silent driver mode resta storia originaria, ora multi-track post-Impronta:
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

**Status 2026-05-12 pomeriggio**: **249 PR mergeati cumulative** (+34 PR dal 7/5 sera, cluster 30 PR mergeati 11/5 sera 16:36-22:51 UTC #218-#247 + **2 PR questa sessione codemasterdd-authored**: #248 Main SeasonalService caller wire + #249 Phone composer MODE_ORGANIZATION). 0 PR open. HEAD origin/main `a765e4e feat(phone): tkt-p2 phase d phone composer organization mode (#249)`.

**TKT-P2 Brigandine Phase D cross-stack chain COMPLETE 2026-05-12**:
| Component | Source | Status |
|-----------|--------|--------|
| Game backend Phase A engine | Game PR #2251 | ✅ |
| Game backend Phase B YAML content | Game PR #2252 | ✅ |
| Game backend Phase C 6 REST endpoints | Game PR #2253 | ✅ |
| Godot CampaignApi HTTP client | Godot PR #245 | ✅ |
| Godot HudView TV-side season label | Godot PR #245 | ✅ |
| Godot SeasonalPanel + SeasonalService | pre-existing | ✅ |
| Godot Main.gd SeasonalService caller wire | Godot PR #248 | ✅ NEW |
| Godot Phone composer MODE_ORGANIZATION | Godot PR #249 | ✅ NEW |

Discovery scope: claim Game COMPACT v40 "TKT-P2 Phase D UI Godot v2 phone composer ~3h" era stale -- 95% Phase D infra GIA' ESISTENTE Godot-v2 pre-questa sessione. Solo Main wire (+32 LOC) + Phone organization (+19 LOC) MANCAVANO. Effort reale ~1h vs claim 3h.

PR mergeati 11/5 sera (campione highlights, dettaglio Game-side):
- **#247** sprint-context checkpoint execution wave 12/5 closure (9 PR shipped)
- **#246** C1 Playwright playtest agent combat 5R + phone airplane reconnect
- **#245** C2 P2 Phase C+D bundle CampaignApi + HudView season indicator
- Cluster #218-#244 (vari): wave execution multi-track parallel

Milestone: **Path A canonical CHIUSO end-to-end** + Sprint AC bundle 15 sub-sprint (#171-#185, AC.6-AC.18) + W3.5 4 nuove scene + W4 wire CoopApi+LoadingOverlay+ErrorBanner. Post 7/5: wave execution attivissimo 11/5 sera con 30+ PR mergeati cluster.

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

## 6. vault-shared (sibling-peer Eduardo)

**Path**: `C:\dev\vault-shared\`
**Remote**: [MasterDD-L34D/vault](https://github.com/MasterDD-L34D/vault)

### Relazione con codemasterdd

Sibling-peer disjoint scope:
- codemasterdd = infrastructure-as-code + governance + 4 progetti monitored + AA01
- vault-shared = knowledge management content (Karpathy LLM-wiki ACCESS) + 7 production agents on content
- Disjoint: NO bidirectional dependency, NO write-path codemasterdd-side, NO formal monitoring SLA
- Cross-reference one-way: vault llm-routing matrix v1.0 -> potential research input MODEL_ROUTING.md addendum codemasterdd
- Eduardo media tutti i flow

### Stack overlap codemasterdd

- Ollama LAN (stesso daemon Lenovo) + qwen2.5-coder family + deepseek-r1 + Claude variants
- 7 production agent (vault-linter, ingestor-claude, dispatcher-claude, ollama-dispatcher, pathfinder-pdf-indexer, vault-ingestor, evo-tactics-design-watcher)
- LLM routing matrix v1.0 (vault-shared/llm-routing.json) basata su bench A/B claude vs ollama (methodology Quality Gate Step 2 con split metrics + keep_alive + retries + output validation)
- Quality Gate workflow (smoke -> draft -> production 3-gate) -- pattern transferibile

### Privacy

**Sovereign-only**: NON in `~/.config/aider-privacy-whitelist.txt`. Aider-cloud su file vault = ABORT.

Rationale (validato spot-check empirico 2026-05-10):
1. Academic integrity: `Spaces/UniUPO/` + `Spaces/Dev/Synesthesia/` (DEPLOY, FEEDBACK_FORM, SCREENSHOT_GUIDE) -- esame UniUPO in corso
2. Curated narrative IP: `Spaces/GDR/HaoJin` (Pathfinder Torneo, Obsidian Foundry Pack v0.2.8) + Valdombra + Pathfinder + CharacterForge
3. Cross-project strategic info: `Spaces/Dev/Evo-Tactics` + `Flint` design notes
4. Prompt library asset: `Spaces/GPT-Prompts/Master-DD v1-v6` + Dispatcher + VTT
5. Owner principle: vault CLAUDE.md riga 1-3 dichiara "Vault personale Eduardo Scarpelli"

Note: claim originale "Spaces/Personal/" da CLAUDE.md vault NON ESISTE empirically (drift documentazione vault-internal). Verdict sovereign-only invariato per altre 4 ragioni.

### Hook globali

Compatible VALIDATED 2026-05-10 (empty commit test PASS, reverted post-test per boundary respect). Vault `core.hooksPath` = `C:/Users/edusc/.local/share/git-hooks` (codemasterdd hook globali ATTIVI). Pattern emoji-leading description ("feat(milestone): 🎯 ...") compatibile con regex commit-msg.

### Boundary

Codemasterdd NON scrive su vault-shared. Vault-shared self-governs. Eduardo media bidirezionale via personal workflow.

### SPOF accepted risk

Vault-shared workflow richiede Eduardo per ogni promote/tune/quality-gate -- intentional SPOF su personal workflow. Mitigation = backup + recovery, NON delegation.

### Update 2026-05-12 (Pattern D ADOPT + drift verifications)

- **HEAD reale verificato**: `054cad6 feat(pc-scan): inventory + Downloads bulk ingest + atomize` (11/5 15:44 UTC). 8 commit cluster 11/5 (PC scan + hybrid search qmd+FTS5+Smart Connections + Ollama local fallback chain mistral+qwen3:8b + canonical decision matrix optimal-hybrid-pattern + post-session tune Global+Vault CLAUDE.md + AGENT_PROTOCOL).
- **Pattern D ADOPT codemasterdd 2026-05-12**: vault `production/agents/vault-linter.md` concept transfer -> `scripts/governance-lint.ps1` (PR #51 merge `0350be5`, audit-then-replay PowerShell-native, NO clone). 3 check MVP (COMPACT HEAD sync + Coda PR claim + JOURNAL stale). Smoke 3/3 ALL-CLEAR self-applied. Future expansion Three Strikes SPRINT_03+. Cross-pattern reference one-way preserved.
- **Status drift findings**: 7/7 vault agent `status: draft` frontmatter ma in `production/agents/` (memory codemasterdd valid via "location = ground truth" interpretation, caveat noted L-2026-05-005).
- **No bidirectional dependency**: codemasterdd governance-lint NON conosce vault concept name nei file di codice (solo nel commit message + research doc + lesson). Replay clean separation.

---

## Scheduled checkpoints

| Data | Evento | Progetto | Azione |
|------|--------|----------|--------|
| ~~2026-04-26~~ | Day-5 Dafne swarm | evo-swarm | DONE -- Atto 1 chiuso post Day-5 successo |
| ~~2026-04-30~~ | H4 cost snapshot fine-mese | codemasterdd | DONE -- gia' fatto mid-sprint 24/04 |
| ~~2026-05-07~~ | Fase 6 closure (anticipata vs sett.4 originale) | codemasterdd | DONE -- ADR-0015 + ADR-0017 Accepted |
| ~~2026-05-08~~ | Governance refresh (drift fix STATUS + COMPACT v12) | codemasterdd | DONE -- branch governance-refresh-2026-05-08 |
| ~~2026-05-12~~ | Cross-repo triage chat-only + STATUS drift fix major (Game 200 PR 14d + Godot-v2 +32 + Dafne stable + vault HEAD update) | codemasterdd | DONE -- PR #53 |
| ~~2026-05-12~~ | ADR-0024 addendum "Sub-events timeline" + scope disjoint clarification (Game OD-023 cross-repo) | codemasterdd | DONE -- PR #55 |
| ~~2026-05-12~~ | TKT-P2 Brigandine Phase D cross-stack chain COMPLETE (Godot PR #248 Main wire + PR #249 Phone organization mode) + Game pull Path A reset (post Protocol 1+2 investigation) | Game-Godot-v2 + Game | DONE -- questa session |
| **2026-05-14** | **Phase B Day 7 formal closure** (Game ADR-2026-05-05 §13.4 cascade actions: web-v1-final tag + apps/play/ archive + README banner) | Game (Vue3) | Eduardo direct. **Sub-event di** ADR-0024 codemasterdd (NON archive Vue3 codebase-wide). Canonical execution checklist gia' preparato in Game `docs/planning/2026-05-14-phase-b-cutover-canonical-execution.md`. |
| **2026-05-19** | Claude Max expiration | codemasterdd | **7gg residui al 12/5 mattina**. Transizione sovereign (wrapper + Ollama). H7 ANTHROPIC_API_KEY MISSING (Eduardo direct ~5min). |
| **2026-05-20+** | SPRINT_02 prima sessione | codemasterdd | Scenario A operativo, smoke test sovereign confermato |
| **~giugno-agosto 2026** | Synesthesia riattivazione | Synesthesia | Privacy validation 2/3 + esame prep |

---

## Regola di ingaggio

**Quando apri sessione cold**: leggi CLAUDE.md + COMPACT_CONTEXT.md + questo file (in quest'ordine) → avrai vista operativa completa.

**Quando cambia stato di un repo**: aggiorna la riga corrispondente in questo file (+ ADR/BACKLOG/JOURNAL del repo specifico se necessario).

**Quando emerge decisione multi-repo**: ADR dedicato in codemasterdd `docs/adr/` con scope esplicito cross-repo.
