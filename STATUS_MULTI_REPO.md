# STATUS_MULTI_REPO — Dashboard operativa cross-repo

> Direction layer: vedi [`GOALS.md`](GOALS.md) per goal cross-repo Short/Mid/Long.
>
> Vista consolidata progetti. Aggiornare quando cambia stato significativo o al massimo settimanalmente.
>
> ⚠️ **Insight strutturale 2026-05-16 (reconcile 43% stale)**: HEAD/PR puntuali in §Snapshot/§1-7 **NON sono git-truth** — repo daily-ship (Game/Godot) li rendono stale in ~2gg. **Stato verificato = §Ecosystem-audit 15-repo** (git-truth, ri-derivato da audit). §1-7 = contesto operativo narrativo. NON ri-hardcodare HEAD qui (rot garantito); aggiorna §Ecosystem-audit con audit fresco.
>
> **Governance ownership**: questo repo (codemasterdd) è policy hub, non esegue codice altri progetti. Le azioni specifiche vivono nei rispettivi repo.
>
> Riferimenti deep: CLAUDE.md sezione "Progetti monitorati" (descrittivo), memory `project_multi_repo_overview.md` (architetturale), questo file (operativo), vault `docs/decisions/ecosystem-state-audit-2026-05-16.md` (audit git fresco 15-repo 2026-05-16: 14/15 sani+synced, evidenza cross-stack esterna — ✅ **RATIFICATO master-dd 2026-05-16, integrato §Ecosystem audit 15-repo sotto**).

**Ultimo refresh**: **2026-05-14 sera-tardi-ultra-3** (post Component 1 cross-repo Dashboard v0.3 daily-use features ship + Docker stack ADR-0017 LIVE + claude-mem disabled + 4 lessons promoted L-018/019/020/021 + Max parallel strategy doc + T9 methodology empirical + Cross-repo PR scan NEGATIVE finding).

**Codemasterdd state**: HEAD main `6dc0bed` (console flash defensive fix) + branch `claude/max-parallel-execution-2026-05-14` commit `dfa7f59` post 5 commits Max-tier (strategy + T9 + dogfood-ui cache + JOURNAL + v0.3 features). Cumulative **57+ PR mergeati 7-14/5** + 5 PR open today (#87 #88 #89 #90 #91 merged #92 open). Plugin ecosystem: 3 plugins, claude-mem disabled 14/5 sera per upstream issue #19012 (console flash bug closed-not-planned). **21 lessons** AA01 cumulative (L-001..L-021, 4 new today). **15+ ADR** (P5 harsh-reviewer ratified Accepted 14/5 amendment).

**Cross-repo state** ⚠️ *snapshot storico 14/5 — HEAD sotto NON git-truth (reconcile 2026-05-16: Game→`84e8c448`, Godot→`afaa656`, vault→`7285cb74`). Stato verificato → §Ecosystem-audit 15-repo*: (storico) Game HEAD `36c9822d` Phase B Day 5/8; Game-Godot-v2 `1d9ce3b`/origin `a765e4e`; Dafne stable `9255b4b`; vault `1abaa743`.

**Cross-repo PR scan finding 14/5**: ZERO drift candidates emersi. Tutti 4 target repos (Game/Godot/Dafne/vault) governance interna autosufficiente CONFIRMED — 0 CLAUDE.md mentions di codemasterdd patterns. Component 2 first-3-PR validation NON ha organic emergence. Empirical insight: cross-repo PR pattern usable ONLY se drift specific emerge naturalmente, NON scan-driven.

---

## Snapshot 1-riga per repo

| Repo | Status | Next action | Deadline/trigger | Blocker |
|------|--------|-------------|------------------|---------|
| **codemasterdd-ai-station** | **Fase 6+7 CLOSED + SPRINT_02 ATTACK MODE 14/5**. HEAD main `6dc0bed` + branch PR #92 `dfa7f59` Max-tier work. **57+ PR mergeati 7-14/5 cumulative** + 1 PR open #92 (5 commits Max parallel strategy + T9 methodology + dogfood-ui cache + JOURNAL + v0.3 features). **Component 1 Dashboard v0.3 LIVE** (apps/cross-repo-dashboard/, port 8081, daily-use features: filter/JOURNAL preview/drill-down/velocity/activity feed). **Docker stack ADR-0017 LIVE 3/3** (LiteLLM + Langfuse + Postgres + dogfood-ui). **claude-mem DISABLED 14/5** post upstream issue #19012 console flash bug. **21 lessons cumulative** L-001..L-021 (4 new today: L-018/019/020/021). **ADR-0026 P5 ACCEPTED ratified** 14/5 amendment empirical. | SPRINT_02 attack mode parallel Max+sovereign **NOW** (T8/T9/T10 shipped 14/5 NOT 5/20+) | 2026-05-19 (Claude Max expiration, **5gg residui**) | Nessuno bloccante. Eduardo restart CC quando convenient -> verify zero claude-mem flashes |
| **Synesthesia** | Dormant, HEAD `05f8a92` (invariato) | Riattiva pre-esame UniUPO | ~agosto 2026 | Nessuno (dormant intenzionale) |
| **Game (Evo-Tactics Vue3)** | ⚠️ HEAD/PR → **§Ecosystem-audit git-truth** (reconcile 2026-05-16: `84e8c448` #2280 Phase-4D; il claim storico sotto era `36c9822` Phase-B Day5/8, ~22 commit dietro — repo daily-ship). Contesto narrativo (storico, non git-truth): Local checkout `C:/dev/Game` reset --hard origin/main 2026-05-12 (Path A confirmed post Protocol 1+2 investigation: 27 commit AA01 CAP-* Sprint Impronta MAI shipped a origin -> safe abandon via 13 backup branches `aa01/cap-*` + stash safety net 295 file WIP refactor). PR open: solo #2257 skiv-monitor (auto-skip pattern). **OD-023 APERTA 2026-05-12** (Phase B execution date verdict, Path C+Path A 34/35). | Continue monitoring (Eduardo-driven). NO codemasterdd action proattiva. **Phase B Day 7 formal closure scheduled 2026-05-14 mattina UTC** (sub-event ADR-0024 codemasterdd addendum PR #55). | **2026-05-14** Phase B closure | Nessuno (governance interna Game autonoma) |
| **Game-Godot-v2** | ⚠️ HEAD/PR → **§Ecosystem-audit git-truth** (reconcile 2026-05-16: `afaa656` #282, +33 PR oltre il claim storico `a765e4e` #249 — repo daily-ship). Contesto narrativo (storico): 249 PR cumulative @ #249, #248 Main SeasonalService wire + #249 Phone MODE_ORGANIZATION. Local checkout pulled fast-forward post-merge. Path A canonical CHIUSO + Sprint AC bundle closed. Hook globali applicati. Governance interna autosufficiente. **TKT-P2 Brigandine Phase D cross-stack chain COMPLETE 2026-05-12**: backend (Game #2251+2252+2253) -> Godot HTTP client (#245) -> TV season label (#245) -> Main caller wire (#248) -> Phone organization mode (#249). | Continue port (Eduardo-driven). Deferred follow-up GUT integration tests test_main_seasonal_wire.gd + test_phone_composer_organization.gd (~55 LOC totali, NON blocking). | No fixed | Nessuno |
| **Dafne swarm (evo-swarm)** | **Stable post-dashboard sprint**, HEAD origin/main `9255b4b` post PR #102 (fase 8 evaluation A/B + PII redaction, 8/5 14:39 UTC). **20 PR cascata 8/5** (PR #83-#102 dashboard fase 0-8 + Tier 4 fix x3 + orchestrator CO-02 + compass anchor fix). **4gg inattivita' post 8/5** (no commit dal 8/5). 0 PR open. Atto 2 status post-sprint indeterminate (probabilmente concluded post dashboard fase 8). | Continue (Eduardo-driven), pull locale se workflow Dafne riprende | No fixed | Nessuno |
| **AA01 (Archon Atelier 01)** | v1.0.0 silent-driver mode. Counter 12/5 sera post Bundle 1+2+3: **14 archive entries + 11 lessons cumulative**. Bundle 2 SHIP + Bundle 3 SHIP questa sessione (2 task addizionali). 11 lessons cross-session `learnings/`: L-2026-04-001 + L-2026-05-002..L-2026-05-011 (+L-010 reflexive methodology audit + L-011 applicative optimization audit promoted 12/5 sera). Workspace 0 attivi. Inbox cleanup 12/5 pomeriggio. | Continua driver mode + nuovo task quando emerge. OD-007 Three Strikes counter: frizione tool-selection NON osservata. | nessuna | nessuno bloccante |
| **vault-shared (Vault Knowledge Mgmt)** | **Sibling-peer Eduardo, monitored. 7/7 production agents milestone hit 2026-05-12** (HEAD `2007a8a2` "feat(milestone) 7/7 agents PRODUCTION + bulk ingest 100/100"). **Frontmatter drift 7/7 identificato** spot-check empirical 12/5 sera: production/agents/*.md status: draft non-synced (drift 100%). LLM routing matrix v1.0 path `Extras/config/llm-routing.json`. Stack overlap codemasterdd: Ollama LAN + qwen2.5-coder family + deepseek-r1 + Claude variants. Privacy: sovereign-only (NOT cloud whitelist). Hook globali compat VALIDATED. **Pattern D ADOPT codemasterdd 2026-05-12** (governance-lint.ps1 PR #51, audit-then-replay NO clone). **V3 cross-pattern adoption Quality Gate**: research doc Bundle 2 12/5 sera, DEFER fino SPRINT_02+. **ChatGPT Business recovery 2026-05-14..16**: 1361 conv + 132 projects + 83 memory + 2.15GB assets recovered (Business workspace, complementary OD-032 personal/deferred). 67 topic / 30,764 cards promossi Spaces `_imported-2026-05-14/` (gitignored bulk). **OD-033 doc superseded -> rappresentazione vault segue flusso OD-038** (Eduardo-mediated; guard rail PII-exfiltration impedisce push vault codemasterdd-side). Tooling/governance codemasterdd-side: **PR #118 MERGEABLE/CLEAN**. | Continue (Eduardo-driven). **Handoff doc Eduardo-direct** `docs/aa01-handoff/2026-05-12-vault-frontmatter-drift-handoff.md` (frontmatter fix + CLAUDE.md drift + README discoverability, 30-45min one-shot). Vault recovery staging: Eduardo-mediated via OD-038. NO write-path codemasterdd-side. | No fixed | Nessuno (sibling-peer disjoint scope) |
| **Game-Database** (Ryzen `C:\dev\Game-Database`) | Taxonomy CMS Evo-Tactics (upstream content provider, Express+Prisma+PG). Jules/Claude active: PR #145 MERGED + #146 open 2026-05-21. Dettaglio: CLAUDE.md Progetti monitorati. | Monitor (Eduardo-driven) | No fixed | Nessuno |
| **claude-supermemory-local** (Ryzen-only) | Claude-Supermemory MCP local instance (persistent context tooling). Auxiliary. | Informational, no action | -- | Nessuno |
| **compass-marketplace** (Ryzen-only) | Compass plugin marketplace -- direction-first audit/kickoff lens per Claude Code. Auxiliary. | Informational, no action | -- | Nessuno |
| **Master-DD-Pathfinder-GPT** (Ryzen-only) | Pathfinder 1E Master DD GPT core repo (API + Prompt Kit), external GPT backing. Personal PF1e. | Informational, no action | -- | Nessuno |
| **torneo-cremesi-site** (Ryzen-only) | Static site PF1e Torneo Cremesi (ABP+EITR ON, localStorage). Personal campaign site. | Informational, no action | -- | Nessuno |

### Stack ADR-0017 runtime (aggiornato 2026-05-13 post Phase 2 cross-PC + T1 SPRINT_02 cluster)

Stack `Accepted` con **T3 SPRINT_02 hot-restart 2nd pass 10/5 mattina PASS**: `docker compose up -d` ~12s wallclock + endpoint LiteLLM/Langfuse 200 OK (via curl 127.0.0.1, NO localhost — vedi runbook PowerShell IPv6 quirk) + **38 trace Langfuse preservati** post 13gg+ downtime (target 7+, no DB corruption). **Regressione `dogfood-ui` VALID_STACKS desync** trovata + fixata path A direct (PR #35 `8722212`). Stack DOWN 10/5 fine sessione (cleanup volumes preservati). Default mode resta **scaffold opt-in** (Docker Desktop non auto-start). Hot-restartable in <60s. DB persistence Postgres+SQLite preservata cross-restart + 38 Langfuse traces persistiti. Procedure complete in `docs/runbook/adr-0017-hot-restart.md` (NEW 10/5 con 5 edge cases documentati).

| Componente | Port | Status code | Status runtime 2026-05-08 | Note |
|------------|-----:|:-----------:|:-------------------------:|------|
| LiteLLM Proxy | 4000 | Accepted | scaffold opt-in (DOWN) | Validated 2026-04-24, hot-restartable. v1.82.6 |
| Langfuse | 3000 | Accepted | scaffold opt-in (DOWN) | 7+ trace persistiti Postgres preservati. v2.95.11 |
| Postgres | 5432 | Accepted | scaffold opt-in (DOWN) | Persistence preservata cross-restart |
| dogfood-ui Flask | 8080 | Accepted | scaffold opt-in (DOWN) | v0.2.0, 11 route, side-effect SQLite path worktree noto |
| promptfoo CLI | -- | Accepted | installed v0.121.7 | Smoke 4/4 pass commit `327d078`. Eval on-demand via CLI |
| Cross-repo coordination (Component 2+3) | -- | Accepted | DOC + scripts merged main (#87+#88) | Gate E empirical 30gg post-Max 5/20 -> 6/19 |
| SPRINT_02 ACTIVE W0 pre-flight | -- | Active | 4-week window 5/20 -> 6/19 (W0 = 5/14 today) | Plan delta + Component 1 archived `docs/research/` |
| Component 1 Dashboard v0.3 | 8081 | Active | Running pythonw tray.pyw background | 5 features + drill-down route |
| Stack ADR-0017 LIVE | 3000/4000/5432/8080 | Active | Docker compose up 14/5 sera | 3 containers + dogfood-ui Python standalone |
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
# Post PR #96 (security): FLASK_SECRET required (app fail-fast se unset).
# Setup .env (vedi apps/dogfood-ui/.env.example) o exportare inline:
cd ../apps/dogfood-ui
$env:FLASK_SECRET = "dev-only-replace-in-prod-$(Get-Random)"
python app.py  # :8080
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

## 7. Ryzen-only sibling repos (minimal monitoring, added 2026-05-13 notte via ADR-0027 Q3 outcome)

5 repo attivi NON presenti su Lenovo `C:\dev\`, presenti solo su Ryzen `Desktop\repos\`. Tracking minimo informational: status snapshot, no piano operativo cross-repo dedicato. Trigger ADR addendum se uno cambia scope strategico.

| Repo | Branch HEAD | Status | Note |
|------|-------------|--------|------|
| **claude-supermemory-local** | main `a72152b` | Active dev | Local SDK replacement Supermemory cloud; Eduardo lavoro recente |
| **compass-marketplace** | `fix/marketplace-schema-source-string` `5943ffa` | Active dev | v0.4.3 fix in flight (compass plugin marketplace) |
| **Game-Database** | origin/main `3be942c` (#114) | **Active, burst-landed** | **Taxonomy CMS Evo-Tactics** (Prisma + PG + Express + React MUI + Vite). Sibling Game (HTTP API integration ADR-2026-04-14). ~~7 PR Jules OPEN 2026-05-15~~ → **STALE-corretto 2026-05-16: burst #107-114 LANDED (security timing-fix, perf, test, refactor), 0 PR open ora, synced 0/0**. Has own CLAUDE.md (multi-client pattern ADR-0021). PUBLIC, no LICENSE. Reconcile OD-038 2026-05-16 (vault `cross-stack-state-delta-2026-05-16.md` §Game-Database): backlog `docs/operativo/ROADMAP.md` ~50% stale, OPEN-REALE = I1 standard-error-response-backend (Now-pri). |
| **Master-DD-Pathfinder-GPT** | `codex-fix-pr-542-follow-up-regressions-clean` `5bd2ccb` | Active Codex | Pathfinder GPT campaign tooling (Codex branch flight) |
| **torneo-cremesi-site** | main `016496e` PR #9 (2025-10-23) | Low-activity | Static site Pathfinder Torneo. *Corretto 2026-05-16: claim precedente "`43eda85` PR#18" era quasi-fabbricato — quella SHA = dangling object MAI su main; PR#18 inesistente. Reconcile OD-038.* |

**Privacy classification**: 9 Ryzen-only repos (4 dormant + 5 above) default SOVEREIGN nel whitelist Aider Ryzen (`~/.config/aider-privacy-whitelist.txt` riga commento Q3-update). Add explicit whitelist quando privacy classification per-repo done (SPRINT_02 opportunistic).

**Dormant repos** (silent-driver autonomous, no monitoring): Gpt, Item-generator, LeaD, pathfinder-1e-homebrew.

**Cross-repo handoff** verso codemasterdd: nessuno attuale. compass-marketplace e claude-supermemory-local potrebbero trigger plugin ecosystem dogfood (SPRINT_02 T8) se Eduardo decide installation.

### Game-Database audit dettagliato (2026-05-15 sera, post Jules API ground truth discovery L-025)

Game-Database e' emerso da audit Jules REST API come repo **attivamente lavorato** dal pipeline multi-AI (Jules + Codex + Claude Code), NON minimal monitoring come precedente classificazione. Promozione scope giustificata:

**Identita repo**:
- Path Ryzen: `C:\Users\VGit\Documents\GitHub\Game-Database\`
- Path Lenovo: nessun clone (Ryzen-only checkout, ma scope-monitorable da remote)
- Remote: `github.com/MasterDD-L34D/Game-Database` (PUBLIC, no LICENSE -- de-facto copyright strict, candidate per MIT/Apache se Eduardo planning open-source)
- Created 2025-11-07, default branch main, attivo May 2026
- Stack: Express 4 + Prisma 5 + PostgreSQL 16 + React (MUI + TanStack Table + i18n + Vite)
- Has own `CLAUDE.md` (multi-client governance autosufficiente, ADR-0021 ratificato)
- Has `WORKSPACE_MAP.md` (cross-stack referenza Game)

**Ruolo ecosystem**:
- **Taxonomy CMS** canonical per Evo-Tactics (trait + species + biome + ecosystem)
- Upstream content provider per **Game** (Vue3) via:
  - Build-time import: `npm run evo:import -- --repo C:/Users/VGit/Documents/GitHub/Game` (idempotent upsert by slug)
  - Runtime HTTP: opt-in `GAME_DATABASE_ENABLED=true` flag su Game backend (HTTP Alt B di ADR-2026-04-14 game-side)
- Frontend dashboard standalone: React CRUD su localhost:5174 + API server localhost:3333 + Postgres localhost:5433 (port distinct da Game 5432 evita conflict)

**Attivita multi-AI 2026-05-15** (via Jules REST API `GET /sessions`):
- 7 sessioni cumulative cross-day (Game-Database e' il repo con piu' sessioni Jules dell'ecosystem)
- 7 PR OPEN today con pattern Jules-signature `*-{14-22 digit}`:
  - #107 [security] basicAuth timing attack fix
  - #108 optimize DELETE response
  - #109 tests DELETE species
  - #110 biome import taxonomy slug pre-fetch
  - #111 ecosystem update pagination refetch optimize
  - #112 refactor normalizeId to shared utility (COMPLETED Jules session)
  - #113 PUT tests ecosystems API
- Pattern emerge: Jules sta sistematicamente migliorando coverage test (3 PR test) + perf (2 PR optimize) + security (1 PR) + code health (1 PR refactor) -- multi-stream improvement automatic.

**Cross-PC sync status**:
- HEAD main `91f5468` PR #105 (snapshot 2026-05-15 sera): ancora pre-cluster Jules-PR-questa-mattina. 7 PR open in attesa merge -> main ahead of HEAD via 7+ commits potenziale.
- Push frequency aggressive (last push 2026-05-15 12:39 UTC = same day).

**Cosa cambia per codemasterdd-side monitoring**:
- Da "Ryzen-only sibling, minimal monitoring" -> **attivo monitored ecosystem**, scope simile a Game (Vue3): cross-repo content dependency + Eduardo lavoro ricorrente.
- Quando PR Jules vengono mergiate -> codemasterdd review opportunistico. **Boundary update post PR #100 merge**: Game-Database e' ORA in CLAUDE.md "Progetti monitorati" sezione, MA `feedback_external_repo_action_boundary` memory rule persiste (sibling Evo-Tactics family). Auth esplicita Eduardo per review/merge/close mantenuta per coerenza con Game / Game-Godot-v2. "Monitored" (scope-tracked) e "external boundary" (action-level safety) sono ortogonali.
- Privacy: PUBLIC, cloud-OK come Game/Game-Godot-v2. Future clone locale opzionale -> aggiungere a `~/.config/aider-privacy-whitelist.txt`. Pending fino actual clone.

**Decisioni differite**:
- Aggiunta formale a CLAUDE.md "Progetti monitorati" sezione: DONE in stesso commit (vedi paragrafo Game-Database).
- LICENSE add (no LICENSE current): defer Eduardo decisione strategica (MIT vs Apache vs proprietary).
- Clone locale codemasterdd: defer, scope expansion Ryzen-led OK.

---

## 7b. evo-tactics-refs-meta (asset pipeline Evo-Tactics, remote-only minimal monitoring)

**Remote**: [MasterDD-L34D/evo-tactics-refs-meta](https://github.com/MasterDD-L34D/evo-tactics-refs-meta) (PRIVATE)
**Path**: nessun clone (remote-only, scope-monitorable da gh API)
**Aggiunto a monitoring**: 2026-05-18 (gap reale nella mappa ecosistema -- Eduardo conferma)

### Identita

- **Ruolo**: meta-backup pipeline asset reference (3D/2D/concept art, SFX, SKIV creature refs) per Evo-Tactics. NO binari versionati -- rebuildable via `robust_download.py` + `urls-*.txt` + `gen_manifest.py`.
- **Conformita licenze**: solo CC0/Public Domain/Sonniss royalty-free, zero estrazioni Tier B/C (provenance in `CC0_SOURCES.md`).
- **Connessione gioco**: asset finali -> `C:\dev\Game\assets\` via output-staging.
- **Stato**: idle (last push 2026-04-29). Layer asset legittimo ma non daily-ship.

### File chiave

| File | Scopo |
|------|-------|
| `README.md` | Tier policy + confini legali |
| `SKIV_REFS_EXTRACTED.md` | Registry asset direct-use creatura Skiv |
| `robust_download.py` + `urls-*.txt` | Pipeline rebuild deterministico |
| `gen_manifest.py` + `MANIFEST.json` | Catalogazione post-download |
| `HANDOFF.md` / `WORKSPACE.md` / `STATUS.md` | Handoff + folder map + stato |

### Monitoring tier

Minimal informational, scope simile §7 (Ryzen-only): snapshot on-demand, no piano operativo cross-repo. Privacy: PRIVATE, sovereign-default (NON cloud-whitelisted finche no clone locale). Trigger scope-up: se Eduardo riprende lavoro asset attivo o clona Lenovo-side. Dettaglio: `docs/EVO_TACTICS_ECOSYSTEM_GUIDE.md` sezione 4.

---

## Ecosystem audit 15-repo — git-verified (RATIFICATO master-dd 2026-05-16)

Reactivation gate `EXTERNAL_REPOS.md` #6 (intento master-dd) + #7 (evidenza fresca) soddisfatti. Snapshot **git-ground-truth 2026-05-16** (branch/dirty/sync/detached verificati diretti). Supera gli HEAD sparsi/stale nelle sezioni §1-7 come *snapshot verità-git*; le §1-7 restano dettaglio operativo mantenuto (NON riscritte — additive per design, lezione PR #116 no-clobber).

Fonte completa (matrice per-repo + raccomandazioni): vault `docs/decisions/ecosystem-state-audit-2026-05-16.md`.

- **15 repo totali** (5 core + 10 scoperti). **14/15 git-sani + GitHub-synced.**
- Drift reale al momento audit: `torneo-cremesi-site` (20-behind) → **risolto** (ff-pull 2026-05-16, ora 0/0).
- `Game` root dir = DETACHED 5d27fc50 (cosmetico; lavoro nei worktree, main-wt synced 0/0 — documentato, lasciare).
- `Game-Godot-v2` main-wt: ff-pull 2026-05-16 → 0/0. `.uid/.import` tracked (policy commit, PR #282).
- `codemasterdd` (questo): policy-hub, governance riattivata da questo blocco.
- Pattern: riconciliazione stale-doc applicabile **solo su drift dimostrato**, non default (provato 5× void blind-pick).
- Hygiene minori (opzionali, non-blocking): Godot-v2 `*.uid` gitignore-policy (project decision), `.vs/` torneo junk.

Regola: questo blocco = verità-git snapshot puntuale; ri-verificare con audit fresco prima di trattarlo come corrente (no hand-edit da memoria). Le §1-7 = stato operativo ricco continuativo.

### Reconcile dashboard §1-7 (OD-038 5-step, 2026-05-16) — staleness 43%

Falsify di TUTTI i claim §Snapshot/§1-7 vs git reale (vault `cross-stack-state-delta-2026-05-16.md` §Dashboard-reconcile dettaglio). **Staleness 6/14 ≈ 43%**. §1-7 = narrativa mantenuta (NON riscritta — additive-only, #116); questo flag = layer git-truth.

| Repo | Claim §1-7 | Reale 2026-05-16 | Verdetto |
|---|---|---|---|
| codemasterdd self | "1 PR open #92", `6dc0bed` | **16 PR open**, `b447b58` (#133) | ⚠️STALE |
| Game | `36c9822` "Phase B Day5/8" | `84e8c448` #2280 Phase-4D | ❌WRONG (arco Phase-B/4D non-doc) |
| Game-Godot-v2 | `a765e4e` #249 | `afaa656` #282 (+33 PR) | ❌WRONG |
| **torneo-cremesi-site (§7)** | "main `43eda85` PR#18" | main `016496e` **PR#9** Ott-2025; `43eda85` = SHA dangling MAI su main | ❌WRONG (claim quasi-fabbricato, non solo stale) |
| vault-shared | `1abaa743`/`054cad6` | `7285cb74` #31 synced | ⚠️STALE (sano) |
| compass-marketplace | "v0.4.3 in-flight `5943ffa`" | landed origin `#10 57d4267`; branch locale dietro | ⚠️STALE (no-loss) |
| Synesthesia/Dafne/supermemory/Master-DD-PF/Item-gen/LeaD/pathfinder-1e/Game-DB | come dichiarato | confermato git | ✅ACCURATE |
| AA01 / Gpt | tracciati | AA01 no-.git; Gpt repo vuoto | 🔒N-A |

**No loss-risk** ovunque (branch autoritativi synced; Game/Godot root-detached = cosmetico già documentato sopra). Drift = §1-7 ~2gg dietro su repo daily-ship (Game/Godot) + torneo §7 entry mai-vera (PR#18/SHA dangling — da correggere a parte, dominio §7). Raccomandazione: §1-7 HEAD-narrativi non affidabili come git-truth → usare QUESTO blocco §Ecosystem-audit per stato verificato; §1-7 per contesto operativo.

---

## DF Integration (Dwarf-Fortress-style levels) status — 2026-05-18

Eduardo claude.ai session ha prodotto 3 doc DF-integration (RECONCILIATION-MASTER, PHASE-PLAN-COMPLETE, RESCUE-FORGOTTEN-HIGH-ROI + mappa HTML).

- **Fase 0 file-placement**: ✅ filed via PR (no direct-main, no merge — Eduardo media):
  - vault A5 [PR #94](https://github.com/MasterDD-L34D/vault/pull/94): RECONCILIATION + PHASE-PLAN + HTML map → `Spaces/Dev/Evo-Tactics/core/`
  - Game [PR #2326](https://github.com/MasterDD-L34D/Game/pull/2326): RESCUE doc → `docs/planning/`
- **Rescue governance mutation (Q-001 + TKT-RESCUE-001..004 + "rescue in corso")**: ❌ **NON applicato — premessa falsificata da ground-truth Game 2026-05-18**:
  - Triangle Strategy Proposal A (MBTI phased reveal) **GIÀ SHIPPED 2026-04-25** (`apps/backend/services/mbtiSurface.js` ~140 LOC, 12/12 test, BACKLOG OD-013, card M-2026-04-25-009 reuse_path eseguito)
  - Sentience tier backfill **SHIPPED PR #1808** (OD-008, ALL 45 species, 25/04) — NB BACKLOG L23 cita erroneamente #2262 (Envelope-B bundle scollegato), upstream-wrong Eduardo-side
  - `docs/research/triangle-strategy-transfer-plan.md` esiste dal 25/04 (65KB)
- **Stato reale**: NON "rescue in corso". Pattern L-025/L-030/anti-pattern #8 (snapshot stale claude.ai vs Game ground-truth daily-ship).

### Re-scope ground-truth verificato (gh api origin/main, 2026-05-18)

| Item plan | Claim plan | Ground-truth | Evidenza | Verdetto |
|-----------|-----------|--------------|----------|----------|
| Triangle Strategy **Proposal A** | rescue ROI 5/5 ~6h | **SHIPPED 2026-04-26** | `apps/backend/services/mbtiSurface.js`, 12/12 test, OD-013 Path A, PR #1848 | **DROP — fatto** |
| Triangle Strategy **Proposal B** | proposta ~4h | **SHIPPED 2026-04-26** | `data/core/personality/mbti_axis_palette.yaml` + `mbtiPalette.js` + 26/26 test, OD-013 Path B | **DROP — fatto** |
| Triangle Strategy **Proposal C** (recruit gating) | ~5h post-recruit | **OPEN ma gated** | OD-013 "Proposal C deferred a OD-001 Path A"; no recruit-gate service | KEEP (gated OD-001/M-007) |
| Sentience tier backfill | rescue ~3h | **SHIPPED PR #1808** | OD-008 "sentience_tier backfill ALL 45 species" merged 2026-04-25 (BACKLOG L23 #2262 = upstream-wrong, Envelope-B bundle) | **DROP — fatto** |
| Sentience A4-residue 30 species | — | **PENDING gated** | BACKLOG "A4-residue 30 species heuristic PENDING gated master-dd" | KEEP (master-dd verdict) |
| Sistema intelligence S7/S8 | nuovo state-machine | **PARTIAL** | `services/ai/sistemaTurnRunner.js` + `declareSistemaIntents.js` esistono; no standalone state-machine/persistence | KEEP (formalizzazione, engine c'è) |
| A6 starter_bioma frontend label | — | **PARTIAL ~30 LOC** | BACKLOG A6 backend ✅, frontend label gap | KEEP (low-lift) |
| S2 eventlog / S3 population-tick / S4-S6 identity / S9-S10 chronicle | "rescue/orphan esistente" | **greenfield non-costruito** | nessun `services/eventlog|worldstate/population_tick|identity|chronicle` | RE-FRAME: feature nuove normali, NON "rescue", competono in BACKLOG |

**Errore-chiave premessa**: i doc framing "FORGOTTEN/orphan/rescue high-ROI 5/5". Realtà: Triangle A+B = già shipped; Sentience-backfill = shipped; il resto = greenfield ordinario (non orphan da rescuare). I doc restano validi come ragionamento L0-L5 + modello identità, NON come task-source.

### Genuinely-open azionabile (ranked, post ground-truth)

1. **Triangle Proposal C** recruit-gating MBTI — gated OD-001/M-007 (no action finché mating closure)
2. **Sistema S7 state-machine formalization** — audit DONE 2026-05-18. Gap: `sistemaTurnRunner.js`+`declareSistemaIntents.js` stateless cross-session, no Prisma Sistema model. **ADR DRAFT filed [Game PR #2328](https://github.com/MasterDD-L34D/Game/pull/2328)** (Option A full ~9h / B pilot ~3-4h / C defer). Verdict master-dd pending — NO code finche' deciso
3. **A4-residue 30-species heuristic** — PENDING gated master-dd verdict (decisione Eduardo prima)
4. **A6 frontend label** starter_bioma — ~30 LOC UI, low-lift standalone ship
5. Greenfield DF (eventlog/population-tick/identity/chronicle) — SE voluti: ticket BACKLOG normali, gate GREEN/YELLOW, NON priorità "rescue"

### Consolidamento governance (2026-05-18, opzione 2)

- **GAME-ANALYSIS-COMPLETE.md** (4° doc A5) analizzato: formato migliore (per-game cosa-prendi/NO/integra + anti-ref + ROI) ma **ripete premessa falsificata** (Triangle A+B "RESCUE" = shipped; greenfield travestito "IN-DESIGN"). Verdetto: NON filing standalone (sprawl 4-doc) → contenuto **corretto** assorbito in umbrella ADR.
- **Umbrella ADR DRAFT** [Game PR #2330](https://github.com/MasterDD-L34D/Game/pull/2330) `ADR-2026-05-18-df-levels-integration-direction.md`: afferma intento DF reale+governato, decision-matrix ground-truth-corretta (5 fix), supersede 3 A5 sparsi → reasoning-archive, linka figlio #2328. **Verdetto master-dd pending** (A full / B core-only / C reject).
- Artefatti finali: umbrella ADR #2330 = governance DF · #2328 = sub-decisione Sistema S7 · DESIGN_DIGEST = catalogo player/ref · PLAYER-VISION #2329 = player-facing · RECONCILIATION/PHASE-PLAN/GAME-ANALYSIS = A5 reasoning non-governante.

**Next Eduardo**: nessun "Sprint S1". Triage 1-4 sopra. Game #2326/#2328/#2329/#2330 + vault #94 MERGED 2026-05-18. codemasterdd #160/#162/#163 MERGED. Verdetti chiave: umbrella #2330 (A/B/C) + figlio #2328 (Sistema S7 A/B/C). Greenfield DF = roadmap M2+ ordinaria, non rescue.

### First-principles verdict DF (game-design-validator, 2026-05-18)

Ipotesi B/B falsificata da evidenza freeze-doc. Verdetto:
- **#2330 umbrella DF -> C** (reject come governance artifact). `90-FINAL-DESIGN-FREEZE` §21.3/§4.2 ha gia' tagliato L2-L5; §18.2 barra Director narrativo. L0-L1 = gia' P2/P4. Prova-eliminazione: rimuovi ADR -> nessun pilastro/vision/loop fallisce = cerimonia.
- **#2328 Sistema S7 -> C/defer no pilot**. Gate P5 = playtest co-op live (TKT-M11B-06), zero codice. Persistenza su core M1 non-frozen per debolezza mai-osservata = ottimizza-prima-di-misurare.
- **Mossa max-leverage**: chiudi M1 -> playtest co-op live -> ri-deriva da evidenza. Nessun codice DF prima.
- **Cut permanente**: DF L0-L5 meta-framework governance; L2 persistence; L5 "losing is fun" build-goal; Sistema full-A; framing "rescue".

### PILLAR data-integrity (A2 reconcile — RISOLTO 2026-05-18)

Drift "6/6 yellow post-M1" = **FALSO, zero fonte canonical** (fabbricazione explore-agent propagata in DESIGN_DIGEST, corretta PR #163). Ground-truth Game: `PILLAR-LIVE-STATUS.md` (SOT, 2026-05-06) + `02-PILASTRI` snapshot concordano = **5/6 🟢 + 1/6 🟡 (P3). Demo-ready confirmed.** Pillar health single-voice. C/C verdict regge su freeze-evidence indipendente.

---

## ADR retrospective 2026-05-18 (B1 decision-review, harsh-reviewer)

Audit 34 ADR. **17 HELD / 8 DRIFTED / 3 FALSIFIED / 6 STALE-STATUS**.

**Malattia**: NON premise-drift (sintomo) ma **assenza owner status-lifecycle** — check-date/trigger scritti come se scrivere=eseguire. Cascade Max-deadline (0014/15/23) non-owned. Decision-leak (0030 Proposed mentre stack tratta Pro installato-fatto). DECISIONS_LOG index desync (ferma 0030, omette 0031-0033).

**⚠️ Direction-finding (risposta "stiamo andando giusti?")**: obiettivo fondante **sovereign-$0-50 (ADR-0001) de-facto MORTO** via **ADR-0030 (15/05, Pro $20/mese "Hybrid A1")**. ADR-0015 auto-emendato 15/05 "$0-50 VIOLATO". Notizia "Max +1mese" = parte realta' Pro-acquisita, NON isolata. Corpus (0001/0015/0023) encoda ancora goal morto. **Deriva piu' grossa del DF.**

**Meta**: PR #161/#162/#163/#164 (correzioni sessione) erano UNVERIFIABLE dall'agent perche' non-merged = prova vivente malattia "autored-not-closed". Loop chiuso (consolidate PR + merge).

**Top-3 azioni Eduardo**: (1) ADR-0023 supersede/rewrite (premessa morta da 0030); (2) DECISIONS_LOG index reconcile (rigenera da headers, omette 0031-0033); (3) ADR-0030 ratify Proposed->Accepted ($ gia' eseguito).

**Process-fix max-leverage proposto**: `STATUS-CHECK: YYYY-MM-DD | trigger | default-if-elapsed` machine-greppable per ADR non-finale + cron settimanale grep check scadute (infra cron esiste). Uccide 6 STALE-STATUS + forza collisioni 0023/0030. Pending Eduardo.

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
| ~~2026-05-20~~ | **D-sequence closure** (browser-agentic-loop OD-051+OD-052+OD-053 -> 9 PR merged; 5 L-DRAFT-A..E promossi vault L-2026-05-034..038 PR #139; Anti-Pattern Catalogue #10-#13 PR #140; canonical CLAUDE.md propagated Ryzen, Lenovo PENDING) | vault + codemasterdd | DONE 2026-05-20. Dettaglio: `docs/sessions/2026-05-19-continuity-handoff.md` §LESSONS-PROMOTED 2026-05-20 |
| ~~2026-05-20/21~~ | **Harsh-review + narrow-pick** (HSGF F-FULL fusion design proposed -> harsh-reviewer RETHINK-FUNDAMENTAL verdict -> pivot Protocol 7 narrow-adoption. Shipped: vault #141 supermemory canonical fix + vault #142 PC identity mechanism + codemasterdd #193 parallel-session collision resolve + codemasterdd #194 sdmg-gate narrow-pick. ~$0.40 harsh-reviewer cost saved ~127h F-FULL waste) | vault + codemasterdd | DONE 2026-05-21. Dettaglio: `docs/sessions/2026-05-20-evening-harsh-narrow-pick.md` |
| **~giugno-agosto 2026** | Synesthesia riattivazione | Synesthesia | Privacy validation 2/3 + esame prep |
| **~2026-08-01** | **SDMG-gate quarterly review** (codemasterdd PR #194 narrow-pick 2-week empirical period -> 3 month review) | codemasterdd | Trigger: adoption rate < 30% qualifying decisions OR ADOPT-rate without executed experiment > 0 -> ADR-0026 amendment B/C |

---

## Regola di ingaggio

**Quando apri sessione cold**: leggi CLAUDE.md + COMPACT_CONTEXT.md + questo file (in quest'ordine) → avrai vista operativa completa.

**Quando cambia stato di un repo**: aggiorna la riga corrispondente in questo file (+ ADR/BACKLOG/JOURNAL del repo specifico se necessario).

**Quando emerge decisione multi-repo**: ADR dedicato in codemasterdd `docs/adr/` con scope esplicito cross-repo.

---

## 2026-05-19 evening + 2026-05-20 EVENING UPDATE — multi-session orchestration

> Tight delta summary. Per-row refresh sopra (rows 1-N) = follow-up se serve.
> Full context: `docs/sessions/2026-05-19-continuity-handoff.md` §EVENING UPDATE.

### Closed today end-to-end
- **OD-050 tdd-guard C-raffinato** RESOLVED full chain: codemasterdd PR#178/#180/#181/#182/#183/#184/#185 + vault PR#126/#127/#128/#129/#130/#131/#132 + Task-5 deploy-Apply 2-PC (Ryzen+Lenovo) + static-assert parity tdd-guard@tdd-guard=false + LIVE TRIGGER Ryzen PASS (hot.md edit no-block). Lenovo trust-by-parity (precedent hook_userprofile_fix). `task5-deploy-verify.ps1` helper deprecated (over-engineered fragile); runbook `docs/runbook/tddguard-task5-cross-pc-verify.md` = via affidabile.
- **OD-049 §4.5** (21 Vault-ops scripts -> vault SoT path-portable) MERGED vault main earlier.
- **Game (Vue3)**: 7 PR shipped today across multiple parallel sessions:
  - `#2316` (Jules test optimize) + `#2318` (Jules tooltip fix) + `#2321` (W8O-2 race fix — me)
  - `#2327` (Jules ack — note: dropped W8O-2 + its regression test, requiring re-fix)
  - `#2334` (A6 starter_bioma frontend — parallel-A6 Eduardo Desktop) + `#2335` (coop-tests gap-fill — parallel-coop) + `#2336` (W8O-2 RESTORE + regression test — me)
  - Regression-class observed: Jules-bot rewrites can silently drop substantive fixes if test not in CI-guard. PR#2336 body recommends watchlist.

### Active threads (open-ended)
- **Game-Godot-v2** = 🔴 ZONA-HOT subagent orchestrator: branch `claude/p2-4-phone-lobby-identity-first-2026-05-20`, 4 worktree LOCKED (`agent-a*`), PR#284 DRAFT (gate-1 Eduardo `/ultrareview` deferred), recent merges #291/#292/#293/#298/#299 (P0-3/P1/P2 remediation lineage from #284 spec).
- **Game (Vue3) parallel sessions**: at least 3 spawned by Eduardo Desktop today (A6 frontend / coop-tests / disc-race-roledemands-v2). Branch-prefix convention `claude/parallel-*` working.
- **vault** = clean main 7fb5ded82 -> 57f54cea3 (post-#132 OD-050 RESOLVED). PR #133 DRAFT (coherence-backstop sibling sessione, doc-only).

### Pending owner
| Item | Owner | Note |
|---|---|---|
| `/ultrareview` PR#284 (gate-1 Godot remediation chain) | Eduardo | when ready, no-rush, post-approval umbrella |
| Cleanup Ryzen scheduled-task (continuity-handoff §39) | Eduardo | post-playtest optional |
| W8O-2 CI-watchlist (prevenire future Jules silent-drop) | follow-up | low-pri, considered post-#2336 |
| Game-Database parallel-#2 cleanup (`server/tests`+`AGENTS.md`+`.claude/` untracked) | TBD | paste-block on-offer in handoff |

### Multi-session orchestration pattern (proven today)
- Branch-prefix `claude/parallel-<scope>-<date>` = visibility on who-does-what
- Mutex via `docs/sessions/2026-05-19-continuity-handoff.md` append-only stamps ("OWNING X branch Y") — used by parallel-coop session
- Repo-split: coordinator (this Ryzen Bash) owns governance/meta-cross-repo; parallels own ONE repo each; subagent-orchestrator (Godot) self-contained in `.claude/worktrees/agent-*` LOCKED
- Pre-merge `harsh-reviewer` subagent on governance-critical/cluster PRs (Protocol-5)
- Pull-before-touch, push-after-commit on shared docs
- Background `repo-health-auditor` snapshot per drift/collision detection


---

## D-SEQUENCE 2026-05-20 — browser-agentic-loop E to A to B end-to-end

Single afternoon session, ~$0.40 total spend, all three phases empirically validated + adopted NARROW.

### Phase summary

| Phase | OD | PR(s) merged | Adoption |
|---|---|---|---|
| E Playwright-direct | OD-051 RESOLVED-FE1-PASS | vault #134 + codemasterdd #190 | scripts/quality-bench/playwright-monitor-regression.py |
| A Chrome MCP interactive-codev | OD-052 RESOLVED-FE2-CAPABILITY-PASS-SPEC-DRIFT | vault #135 | empirical pattern documented (5 spec-drifts as lessons) |
| B browser-use exploratory | OD-053 RESOLVED-FE3-PASS | vault #136 + #137 + #138 | 4-step throwaway-venv recipe, NOT permanent |

### Cross-repo touch

- codemasterdd: PR #189 dashboard /monitor route wire + PR #190 Playwright regression script (both MERGED)
- vault: 5 PR merged (#134 OD-051, #135 OD-052, #136 OD-053 DRAFT-v1, #137 OD-053 v3 Q1-Q4 answers, #138 OD-053 RESOLVED-FE3-PASS)
- Game-Database: issue #123 opened (a11y mixed Italian/English aria-labels, P2 from OD-053 FE3 T2 finding #4)

### Cron monitor durable promoted

Session-only cron `e8e94a27`+`af96f168` (CronCreate) replaced by `mcp__scheduled-tasks__cross-repo-drift-monitor` (cross-session durable). File: `C:/Users/VGit/.claude/scheduled-tasks/cross-repo-drift-monitor/SKILL.md`. Schedule `7,37 * * * *` (off-minute). 7-day auto-expire.

Empirical confirmation: iter-2 (12:12), iter-3 (12:18), iter-4 (12:42) fired during D-sequence execution, JSONL feed at `logs/monitor-feed.jsonl` (gitignored) populated correctly, dashboard `/monitor` renders.

### Outstanding from D-sequence

- Venv left at `C:/Users/VGit/AppData/Local/Temp/browser-use-fe3-venv` (classifier denied rm-rf scope-escalation, Eduardo manual cleanup)
- 5 L-DRAFT-F..J lessons in continuity-handoff for promotion to canonical L-2026-05-NNN next session
- D-sequence pattern reusable: anti-creep gate + harsh-review per phase + autoresearch for blocking Q's. Document as `docs/patterns/multi-phase-d-sequence.md` if applied again.

### Status post-D-sequence cross-repo (open PR snapshot 13:00)

- codemasterdd: 0 open PR (clean)
- Game: 0 open PR
- Game-Database: 2 open (Jules #118 docs spec, #122 feat audit) + issue #123 just opened
- Game-Godot-v2: 1 open (#314 feat cronaca TKT-P4)
- vault: 1 open (#133 coherence-backstop from another session)

Coordinator-lane: clean. Parallel-session work distinct branch-names, no collision detected per monitor iter-4.
