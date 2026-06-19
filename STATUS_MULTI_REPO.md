# STATUS_MULTI_REPO — Dashboard operativa cross-repo

<!-- GOVERNOR-SYNC:signals BEGIN -->
| source | severity | summary | produced_at | ref |
| --- | --- | --- | --- | --- |
| archon-learnings | info | 36 ARCHON lessons, latest L-2026-05-038 | 2026-05 | https://api.github.com/repos/MasterDD-L34D/vault/contents/Vault-ops-remote/claude-global/aa01-system/learnings |
| evo-swarm-digest | info | 0 cycles, 20 coverage gaps | 2026-05-27 | https://api.github.com/repos/MasterDD-L34D/evo-swarm/contents/docs/exports/EXPORT-FOR-GAME-REPO-2026-05-27.md?ref=main |
| game-governance-drift | warning | 0 errors, 362 warnings (362 total) | 2026-06-10T23:03:01+00:00 | https://raw.githubusercontent.com/MasterDD-L34D/Game/main/reports/docs/governance_drift_report.json |
| game-sot-drift | ok | 0 open SoT drift candidate(s) |  | https://api.github.com/repos/MasterDD-L34D/Game/issues?labels=sot-drift-candidate&state=open |
| jules-digest | ok | jules digest 2026-06-11: 0 awaiting | 2026-06-11 | https://api.github.com/repos/MasterDD-L34D/codemasterdd-ai-station/contents/docs/jules-batch/2026-06-11-digest.md?ref=main |
| vault-coherence | ok | coherence report present 2026-06-11 | 2026-06-11 | https://api.github.com/repos/MasterDD-L34D/vault/contents/Extras/lint-reports/coherence-2026-06-11.md?ref=main |
| vault-eng-graph | (masked: time-derived) | eng-graph MOC: 5 repos indexed, last_verified 2026-05-31 | 2026-05-31 | https://api.github.com/repos/MasterDD-L34D/vault/contents/Atlas/engineering-moc.md |
| vault-gap | warning | gap report 2026-06-11: 3/5 summary metrics nonzero | 2026-06-11 | https://api.github.com/repos/MasterDD-L34D/vault/contents/Extras/lint-reports/gap-2026-06-11.md?ref=main |
| vault-whatsmissing | warning | whatsmissing report 2026-05-22: 3/5 summary metrics nonzero | 2026-05-22 | https://api.github.com/repos/MasterDD-L34D/vault/contents/Extras/lint-reports/whatsmissing-2026-05-22.md?ref=main |

_Auto-synced governor signal snapshot; human prose elsewhere is authoritative. Time-derived severities are masked (ADR-0039 amendment P1)._
<!-- GOVERNOR-SYNC:signals END -->

> Direction layer: vedi [`GOALS.md`](GOALS.md) per goal cross-repo Short/Mid/Long.
>
> Vista consolidata progetti. Aggiornare quando cambia stato significativo o al massimo settimanalmente.
>
> ⚠️ **Insight strutturale 2026-05-16 (reconcile 43% stale)**: HEAD/PR puntuali in §Snapshot/§per-repo **NON sono git-truth** — repo daily-ship (Game/Godot) li rendono stale in ~2gg. NON ri-hardcodare HEAD qui (rot garantito); usa `gh pr list` + `git log` per stato corrente. Le sezioni per-repo = contesto operativo narrativo dato (last-verified), NON asserzione fresca.
>
> **Governance ownership**: questo repo (codemasterdd) è policy hub, non esegue codice altri progetti. Le azioni specifiche vivono nei rispettivi repo.
>
> Riferimenti deep: CLAUDE.md sezione "Progetti monitorati" (descrittivo), memory `project_multi_repo_overview.md` (architetturale), questo file (operativo). Audit storici + session-log May 2026 archiviati in [`docs/archive/status-multi-repo-history-2026-05.md`](docs/archive/status-multi-repo-history-2026-05.md) (Ecosystem-audit 15-repo + Reconcile OD-038 + DF Integration + ADR retrospective + D-sequence + multi-session orchestration).

**Ultimo refresh**: **2026-06-19** (ground-truth audit repo-health-auditor, gh-api verified tutti i repo; riconciliati ~9gg di daily-ship vs snapshot 06-10). _Dettaglio JOURNAL 2026-06-19._ NB: la **Snapshot 1-riga** sotto e' fresca 06-19; le sezioni per-repo narrative restano contesto datato 06-10 (last-verified per-sezione).

**Codemasterdd state**: HEAD main `f15387e` (docs(journal): rfc4 s3 closed NO-GO, #398). 0 PR open. 84 PR merged 06-10->06-19. **Claude Max SCADUTO ~2026-06-17 -> post-Max routing ADR-0023 attivo** (`logs/claude-api-spend-2026-06.md` presente, spend ~$0 giugno). Stack ADR-0017 DOWN (scaffold opt-in, expected). Last-verified: 2026-06-19.

---

## Snapshot 1-riga per repo

| Repo | Status | Next action | Deadline/trigger | Blocker |
|------|--------|-------------|------------------|---------|
| **codemasterdd-ai-station** | HEAD `f15387e` (2026-06-19, #398). 84 PR merged 06-10->06-19. 0 PR open. **Claude Max SCADUTO ~2026-06-17** -> post-Max routing ADR-0023 attivo; spend ~$0 giugno. Stack ADR-0017 DOWN (scaffold opt-in). Sub-agent ecosystem 16+5 stabile. | SDMG quarterly review ~2026-08-01; aggiorna spend log mensile | 2026-08-01 | Nessuno |
| **Synesthesia** | Dormant, HEAD `05f8a92` (invariato, verificato 06-10) | Riattiva pre-esame UniUPO | ~agosto 2026 | Nessuno (dormant intenzionale) |
| **Game (Evo-Tactics)** | HEAD `9df35b8` (2026-06-19, #2877). ~166 PR merged 06-10->06-19 (daily-ship). **RFC#4 CHIUSO** (S1 traits / S2 fidelity-shadow + biome/eco import-only / S3 NO-GO ADR-2026-06-19). **Taxonomy+calib arc DONE** (#2832/#2837/#2850/#2853/#2857/#2862/#2863/#2868/#2872/#2876; validate-datasets 0 warn). **PE_ratio PR2/PR2b DONE** (#2867/#2869; finding: signal marginale). SPEC-K K-05 quorum #2871. 1 PR open: #2765 DRAFT weekly-drift. | Decisione PE_ratio (ratify band o alt-source -> flip P4/P5); prod-auto-restart residue (chip task_3ce69e8d) | -- | Nessuno |
| **Game-Godot-v2** | HEAD `b6e7afd` (2026-06-19, #508). ~43 PR merged 06-10->06-19. **Ferrospora UI art-pass v2 DONE** + **style-LoRA v1 DONE** (step2000, P0-P5, bf16). **SPEC-K K-05 phone/TV client #507**. 2 PR open: #509 (Ferrospora ornate twin-socket ForecastPanel frame) + #510 (K-05 AI co-op playtest PASS docs). Owner-paused at finish+wire ForecastPanel. | Merge #509/#510 (Eduardo); finish+wire ForecastPanel (pattern #489) | -- | Nessuno |
| **Dafne swarm (evo-swarm)** | HEAD `f14d2e7` (2026-06-19, #126). **REACTIVATED** (era IDLE dal 05-28): 3 commit oggi -- entity-grounding pre-emit gate Lever-1 #124 + trait-source union #125 + trait field-value canonical_refs #126; suite 471 green. Swarm RUNTIME ancora PARKED (gate validato offline). 0 PR open. | Decisione Eduardo: spec Lever-2/Lever-3 o PARK esplicito runtime | -- | Flask :5000 non verificato (non blocker se parked) |
| **AA01 (Archon Atelier 01)** | v1.0.0 silent-driver mode. **21 archive entries + 38 lessons** (L-001..L-040+, conteggio file 06-10). Workspace 0 attivi. | Continua driver mode + nuovo task quando emerge. | nessuna | nessuno bloccante |
| **vault-shared (Vault Knowledge Mgmt)** | HEAD `ed0e26c` (2026-06-19, gap-capture PASS-4). 48 PR merged 06-10->06-19. **ADR-2026-06-03 asset-pipeline ratificato 06-18**. Backstop daily autonomo. 7 WARN carry-forward (W-2 Claude-Max-urgency RESOLVED). 0 PR open. Privacy: sovereign-only. | Nessun triage pendente; 7 WARN = candidato next Short se vuoi | -- | Nessuno |
| **Game-Database** (Ryzen `C:\dev\Game-Database`, Lenovo clone present) | HEAD `4e97841` (2026-06-19, #230). 33 PR merged 06-10->06-19. **RFC#4 S2 chiuso** (#226/#227) + **S3 stamp DONE** (#230, pointer Game ADR-2026-06-19). 0 PR open. Jules-maintained + Eduardo RFC stamps. | Monitor (Jules/Eduardo-driven) | -- | Nessuno |
| **claude-supermemory-local** (Ryzen-only) | Claude-Supermemory MCP local instance (persistent context tooling). Auxiliary. | Informational, no action | -- | Nessuno |
| **compass-marketplace** (Ryzen-only) | Compass plugin marketplace -- direction-first audit/kickoff lens per Claude Code. Auxiliary. | Informational, no action | -- | Nessuno |
| **Master-DD-Pathfinder-GPT** (Ryzen-only) | Pathfinder 1E Master DD GPT core repo (API + Prompt Kit), external GPT backing. Personal PF1e. | Informational, no action | -- | Nessuno |
| **torneo-cremesi-site** (Ryzen-only) | Static site PF1e Torneo Cremesi (ABP+EITR ON, localStorage). Personal campaign site. | Informational, no action | -- | Nessuno |

### Stack ADR-0017 runtime — DECOMMISSIONED reference

Stack `Accepted` ma in modalita' **scaffold opt-in** (containers down per default, hot-restartable). Note storiche: hot-restart ~12s wallclock validato 2026-05-10, 38 trace Langfuse preservati post 13gg downtime, DB persistence cross-restart OK. Procedure: `docs/runbook/adr-0017-hot-restart.md`.

| Componente | Port | Status runtime | Note |
|------------|-----:|:--------------:|------|
| LiteLLM Proxy | 4000 | scaffold opt-in (DOWN) | v1.82.6, hot-restartable |
| Langfuse | 3000 | scaffold opt-in (DOWN) | trace persistiti Postgres |
| Postgres | 5432 | scaffold opt-in (DOWN) | Persistence cross-restart |
| dogfood-ui Flask | 8080 | scaffold opt-in (DOWN) | v0.2.0, FLASK_SECRET required post #96 |
| promptfoo CLI | -- | installed v0.121.7 | Eval on-demand via CLI |
| Dafne swarm (esterna) | 5000 | gestito repo Dafne separato | Vedi §Dafne sotto |

---

## codemasterdd-ai-station (policy hub)

**Path**: `C:\dev\codemasterdd-ai-station\` -- **Remote**: [MasterDD-L34D/codemasterdd-ai-station](https://github.com/MasterDD-L34D/codemasterdd-ai-station) -- **Privacy**: public

**Status**: Fase 6 CLOSED 2026-05-07 (ADR-0015 + ADR-0017 Accepted, scenario A full-sovereign). SPRINT_02 chiuso e archiviato in `docs/archive/` (no SPRINT_03 aperto). Stack ADR-0017 scaffold opt-in (DOWN default, hot-restart <60s). Claude Max fino ~2026-06-17 (scadenza vicina -> post-Max routing ADR-0023).
**Last-verified**: 2026-06-10.
**Decisioni pendenti**:
- ADR-0016 (Proposed) awaiting n>=3 data points addizionali.
- **ADR-0036 -- Unified Orchestration Doctrine: Accepted (spine) 2026-06-01 + Deferred (auto-merge rung)**. `ORCHESTRATION.md` single cross-executor routing authority. Consolida ADR-0013/0022/0023/0030/0034/0035.
- **ADR-0037 -- merge-autonomy model: Accepted 2026-06-03** (jules-dispatch fail-closed wrapper #290).
- **ADR-0038 (doctrine carveout completion) + ADR-0039 (R1 open-PR reconcile rung, built #295): Accepted 2026-06-11** (Eduardo, dossier ratifica + amendment: 0038 4 testuali + sec-7 sync; 0039 P1 clock-free rescope -- STATUS-leg cycles non contano per R2 fino a fix clock-leak -- + 3 annotazioni R2).
**Sub-agent ecosystem**: 16 agent attivi + 5 dormant (`.claude/agents/`, scan 06-10) coprono 4 repo + cross-cutting. Dettaglio: [.claude/agents/README.md](.claude/agents/README.md), fonti in `SOURCES.md`.

---

## Synesthesia

**Path**: `C:\dev\synesthesia\` -- **Remote**: [MasterDD-L34D/synesthesia](https://github.com/MasterDD-L34D/synesthesia) -- **Privacy**: sovereign-only (controllers/ sensitive; views/public cloud OK)
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

## Game (Evo-Tactics Vue3)

**Path**: `C:\dev\Game\` (Lenovo synced primary + Ryzen STALE sandbox) -- **Remote**: [MasterDD-L34D/Game](https://github.com/MasterDD-L34D/Game) -- **Privacy**: public (cloud-whitelisted)
**Status**: repo daily-ship attivissimo (multi-track), ~297 PR merged 05-28->06-10. HEAD main `55adfb4` (2026-06-10, #2722). **OD-058 wound cutover SHIPPED flip-ON**: D1 overcharge probe #2713 -> D2 read-apply flag-gated #2714 -> D3 write-trigger flip ON #2720 + vcSnapshot coop server-side ledger replay #2722; follow-up trait mirror/prettier #2717/#2718/#2719. ER6 StressWave flag-gated OFF #2712; SPEC-I fork ER6/ER7 ratificato + flip active #2705; trait electric channel #2715. Coop stream: SPEC-P PA3 biomeChip, branco, name-emergence, identity M-2. Governance vive nel Game repo (`docs/governance/`); codemasterdd monitora, non dirige.
**Last-verified**: 2026-06-10.
**Open**: PR #2723 (ER7 biome population tick BUILT flag-gated, non-draft) + PR #2683 (DRAFT mission-console auto-build dist). Chiusi 06-08/06-10: Gate-5 #2716, tracker OD-058-build #2531, weekly-drift #2512. (Nota: #2385 era un PR, MERGED 05-29 -- la riga precedente "DRAFT still open" era confusione PR/issue.)
**Lane**: Game = Ryzen; da Lenovo NO push (fold-race L3). Lenovo clone behind 15 + file tmp non tracciati.
**Blocker**: nessuno.
**Next (codemasterdd-side)**: monitor Eduardo+AA01-driven progression; triage #2723/#2683 (lane Ryzen). NON gestire capability/design interni.
**Detail-pointer**: Game `docs/governance/` + memory `project_game_wave3_hub.md` + `project_multi_repo_overview.md`. Audit findings storici (boss enrage, XP curve) + Sprint-Impronta CAP-11..15 in archive history.

---

## Dafne swarm (evo-swarm)

**Path**: `C:\Users\edusc\Dafne\workspace\swarm\` (Lenovo) + `C:\dev\evo-swarm` (Ryzen clone) -- **Remote**: [MasterDD-L34D/evo-swarm](https://github.com/MasterDD-L34D/evo-swarm) -- **Privacy**: sovereign (orchestratore AI custom)
**Status**: **REACTIVATED 2026-06-19** (era IDLE dal 05-28) -- origin/main HEAD `f14d2e7` (#126); 3 commit oggi: entity-grounding pre-emit gate Lever-1 #124 + trait-source union #125 + trait field-value canonical_refs #126 (suite 471 green). Swarm RUNTIME ancora PARKED (gate validato OFFLINE, non triggera reattivazione). Process persistence ADR-0019 (`START-SWARM-PERSISTENT.ps1`). Chat Dafne endpoint `:5000/dafne` (fallback chain qwen3:8b -> groq 70B -> cerebras 8B -> gemini flash). Flask :5000 non verificato (not blocker unless workflow resumes). Lever-2/Lever-3 = spec future.
**Last-verified**: 2026-06-19.
**Open**: 0 PR. OD-004 dashboard usage deferred; OD-005 Tavily degraded.
**Blocker**: nessuno hard.
**Next**: decisione Eduardo resume-vs-PARK esplicito (vedi GOALS.md PROPOSTE). Handoff invariato: Dafne propone -> Eduardo approva via POST -> H5 gate -> Game agents/ write.
**Detail-pointer**: repo swarm governance (5 file root-level) + memory `reference_dafne_swarm.md` + `project_dafne_persona.md`.

---

## Game-Godot-v2 (Evo-Tactics Godot 4.x port, pivot 2026-04-29)

**Path**: `C:\dev\Game-Godot-v2\` (cloned 2026-05-07) -- **Remote**: [MasterDD-L34D/Game-Godot-v2](https://github.com/MasterDD-L34D/Game-Godot-v2) -- **Privacy**: public (cloud-whitelisted)
**Status**: daily-ship attivo, 105 PR merged 05-28->06-10 (465 cumulative). HEAD `dc88167` = **#465 AI playtest item-3 co-op PASS + host driver riusabile** (2026-06-10). Sprint corrente: co-op + Form Pulse (item-3 identity surfaces #463, creature_named broadcast #464) + phone chronicle M-7 Memory-mode MVP #452 + AI playtest ladder; genetics Fase-2 conclusa; stream #2679 (Form Pulse axis contract) chiuso 06-10. Stack Godot 4.x GDScript (GUT; no Node/Vue/Python). Governance interna autosufficiente (proprio CLAUDE.md con caveman mode + AGENTS.md per Codex + SAFE_CHANGES/TASK_PROTOCOL); codemasterdd monitora soltanto. Hook globali applicati via `core.hooksPath` user-level.
**Last-verified**: 2026-06-10.
**Open**: 0 PR open.
**Blocker**: nessuno post-clone.
**Next (codemasterdd-side)**: monitor `gh pr list`. NON gestire GDScript/scene files (Eduardo-driven). Relazione con Game: Game = backend/sim/canon + balance authority (server cross-stack, preservato by design, Game ADR-2026-05-05 sez.6.3); Godot v2 = frontend canonico (cutover Phase A 2026-05-07 + Phase B web-archive 2026-05-14). NO archive repo-wide Game. Dettaglio: codemasterdd ADR-0024 (reconciled 2026-06-08).
**Detail-pointer**: repo CLAUDE.md + memory `project_multi_repo_overview.md`.

---

## vault-shared (sibling-peer Eduardo)

**Path**: `C:\dev\vault\` (Lenovo clone downstream + Ryzen origin) -- **Remote**: [MasterDD-L34D/vault](https://github.com/MasterDD-L34D/vault) -- **Privacy**: **sovereign-only** (NON in aider-privacy-whitelist; aider-cloud su file vault = ABORT)
**Status**: sibling-peer disjoint scope (knowledge management Karpathy LLM-wiki ACCESS + 7 production agents on content). HEAD `2074956` (2026-06-10, gap-capture backstop daily). 40+ PR merged 05-28->06-10: eng-graph SSE/HTTP daemon #243, cloud gpt-4o-mini OD-059 #241, OD-058 D1-D5 verdicts ratified #234, d20 SoT reconcile (ability executor SHIPPED) #254. Stack overlap: Ollama LAN (stesso daemon) + qwen2.5-coder + deepseek-r1 + Claude variants + LLM routing matrix v1.0. Hook globali compatibili (validated 2026-05-10).
**Last-verified**: 2026-06-10.
**Open**: 0 PR (serie DRAFT #180/#181/#190 MERGED + #201 CLOSED il 2026-05-29).
**Blocker**: nessuno.
**Boundary**: codemasterdd PUÒ branch+PR push, MAI direct-main/merge. Eduardo media il merge-gate (oversight SPOF intenzionale su personal workflow). Cross-reference one-way: vault llm-routing matrix -> potential MODEL_ROUTING.md addendum codemasterdd.
**Next**: nessun triage pendente (backstop daily autonomo). Lint-WARN residui (coherence WARN 1 + gap 3/5 nonzero, signals 06-03) = candidato next Short (GOALS.md PROPOSTE).
**Detail-pointer**: memory `project_vault_shared.md`. Privacy rationale (academic integrity UniUPO + curated narrative IP + cross-project strategic + prompt library) in archive/CLAUDE.md.

---

## Ryzen-only sibling repos (minimal monitoring)

5 repo attivi presenti solo su Ryzen `C:\dev\` (consolidati 2026-05-21), tracking minimo informational (snapshot on-demand, no piano operativo cross-repo). **Privacy**: tutti default SOVEREIGN in whitelist Aider Ryzen finche no classificazione per-repo. Trigger ADR addendum se uno cambia scope strategico.

| Repo | Status | Privacy |
|------|--------|---------|
| **claude-supermemory-local** | Active dev. Local SDK replacement Supermemory cloud. | sovereign |
| **compass-marketplace** | Active dev (compass plugin marketplace, direction-first lens Claude Code). | sovereign |
| **Game-Database** | **Active monitored** -- Taxonomy CMS Evo-Tactics (Prisma + PG + Express + React MUI + Vite). Upstream content provider per Game via `npm run evo:import` + HTTP runtime API (`GAME_DATABASE_ENABLED=true`). 12 PR merged 05-28->06-10 (Jules code-health: CWE-290 #170, rate-limit #169, JSDoc/test/docs). Has own CLAUDE.md (multi-client ADR-0021) + WORKSPACE_MAP.md. PUBLIC, no LICENSE. Jules aggressive-maintenance source. Lenovo clone behind 3 (verificato 2026-06-10). Boundary: auth esplicita Eduardo per review/merge/close (sibling Evo-Tactics family). | public, cloud-OK |
| **Master-DD-Pathfinder-GPT** | Active Codex. Pathfinder GPT campaign tooling. | sovereign |
| **torneo-cremesi-site** | Low-activity static site PF1e Torneo (main `016496e` PR #9, Ott-2025). | sovereign |

**Dormant repos** (silent-driver autonomous, no monitoring): Gpt, Item-generator, LeaD, pathfinder-1e-homebrew.
**Cross-repo handoff** verso codemasterdd: nessuno attuale. compass-marketplace + claude-supermemory-local potrebbero trigger plugin ecosystem dogfood (SPRINT_02 T8) se Eduardo decide installation.
**Detail-pointer**: memory `project_multi_repo_overview.md`; Game-Database audit dettagliato + reconcile OD-038 in archive history.

---

## evo-tactics-refs-meta (asset pipeline Evo-Tactics, remote-only minimal monitoring)

**Path**: nessun clone (remote-only, scope-monitorable da gh API) -- **Remote**: [MasterDD-L34D/evo-tactics-refs-meta](https://github.com/MasterDD-L34D/evo-tactics-refs-meta) -- **Privacy**: PRIVATE, sovereign-default (NON cloud-whitelisted finche no clone locale)
**Status**: meta-backup pipeline asset reference (3D/2D/concept art, SFX, SKIV creature refs). NO binari versionati -- rebuildable via `robust_download.py` + `urls-*.txt` + `gen_manifest.py`. Conformita CC0/PD/Sonniss (provenance `CC0_SOURCES.md`). Connessione gioco: asset finali -> `C:\dev\Game\assets\` via output-staging. Idle (last push 2026-04-29), layer asset legittimo non daily-ship.
**Last-verified**: 2026-05-18.
**Blocker**: nessuno.
**Trigger scope-up**: Eduardo riprende lavoro asset attivo o clona Lenovo-side.
**Detail-pointer**: `docs/EVO_TACTICS_ECOSYSTEM_GUIDE.md` sezione 4.

---

## Scheduled checkpoints (future)

> Checkpoint storici DONE (struck-through) archiviati in [`docs/archive/status-multi-repo-history-2026-05.md`](docs/archive/status-multi-repo-history-2026-05.md).

| Data | Evento | Progetto | Azione |
|------|--------|----------|--------|
| ~~**~2026-06-17**~~ **DONE 06-19** | **Claude Max scaduto ~06-17** -> post-Max routing ADR-0023 ATTIVO | codemasterdd | Eseguito: budget cap $10-20/mese + tracking `logs/claude-api-spend-2026-06.md` (presente, spend ~$0 finora) |
| **~giugno-agosto 2026** | Synesthesia riattivazione | Synesthesia | Privacy validation 2/3 + esame prep |
| **~2026-08-01** | **SDMG-gate quarterly review** (codemasterdd PR #194 narrow-pick 2-week empirical period -> 3 month review) | codemasterdd | Trigger: adoption rate < 30% qualifying decisions OR ADOPT-rate without executed experiment > 0 -> ADR-0026 amendment B/C |
| ~~trigger-based~~ | ~~**ADR-0038 + ADR-0039 ratify**~~ **DONE 2026-06-11**: entrambi Accepted con amendment (0038: 4 testuali + actor-criteria sec-7 sync; 0039: P1 clock-free rescope + annotazioni R2 b-d). Dossier `docs/research/adr-0038-0039-ratify-dossier-2026-06.md`. Residui chiusi same-day: clock-leak P1-1 FIXED (#333, mask severity time-derived nel render STATUS) + primo run post-fix (reconcile PR cdd #336 + vault #258, merge Eduardo-only) | codemasterdd | **Cadenza rung decisa (Eduardo 2026-06-11): run manuale settimanale** (`py -m governor.reconcile`, token env Eduardo; ingest prima del run) durante l'earn window R2; no cron (ADR-0039 dec.8). Non-run prolungato = segnale off-ramp letto onestamente (annotazione R2-d) |

---

## Regola di ingaggio

**Quando apri sessione cold**: leggi CLAUDE.md + COMPACT_CONTEXT.md + questo file (in quest'ordine) → avrai vista operativa completa.

**Quando cambia stato di un repo**: aggiorna la riga corrispondente in questo file (+ ADR/BACKLOG/JOURNAL del repo specifico se necessario).

**Quando emerge decisione multi-repo**: ADR dedicato in codemasterdd `docs/adr/` con scope esplicito cross-repo.
