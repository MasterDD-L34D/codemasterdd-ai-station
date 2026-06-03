# STATUS_MULTI_REPO — Dashboard operativa cross-repo

> Direction layer: vedi [`GOALS.md`](GOALS.md) per goal cross-repo Short/Mid/Long.
>
> Vista consolidata progetti. Aggiornare quando cambia stato significativo o al massimo settimanalmente.
>
> ⚠️ **Insight strutturale 2026-05-16 (reconcile 43% stale)**: HEAD/PR puntuali in §Snapshot/§per-repo **NON sono git-truth** — repo daily-ship (Game/Godot) li rendono stale in ~2gg. NON ri-hardcodare HEAD qui (rot garantito); usa `gh pr list` + `git log` per stato corrente. Le sezioni per-repo = contesto operativo narrativo dato (last-verified), NON asserzione fresca.
>
> **Governance ownership**: questo repo (codemasterdd) è policy hub, non esegue codice altri progetti. Le azioni specifiche vivono nei rispettivi repo.
>
> Riferimenti deep: CLAUDE.md sezione "Progetti monitorati" (descrittivo), memory `project_multi_repo_overview.md` (architetturale), questo file (operativo). Audit storici + session-log May 2026 archiviati in [`docs/archive/status-multi-repo-history-2026-05.md`](docs/archive/status-multi-repo-history-2026-05.md) (Ecosystem-audit 15-repo + Reconcile OD-038 + DF Integration + ADR retrospective + D-sequence + multi-session orchestration).

**Ultimo refresh**: **2026-05-28 (notte)** (ALIENA diagnostic A->D pipeline + tribes+telemetry phone cross-repo, 14 PR session). _Dettaglio JOURNAL 2026-05-28 (notte)._

**Codemasterdd state**: HEAD main `4b40321` (docs(agent): repo-health-auditor refreshes GOALS.md). 0 PR open. Stack ADR-0017 DOWN (scaffold opt-in, all services down). Ollama UP 16 models. Last-verified: 2026-05-28.

---

## Snapshot 1-riga per repo

| Repo | Status | Next action | Deadline/trigger | Blocker |
|------|--------|-------------|------------------|---------|
| **codemasterdd-ai-station** | HEAD `4b40321` (2026-05-27). SPRINT_02 active. 3 untracked files (2 jules-batch digests + godot-install-ryzen.ps1). 0 PR open. Stack ADR-0017 DOWN (scaffold opt-in, expected). Ollama UP 16 models. | Commit/triage 3 untracked files | -- | Nessuno |
| **Synesthesia** | Dormant, HEAD `05f8a92` (invariato) | Riattiva pre-esame UniUPO | ~agosto 2026 | Nessuno (dormant intenzionale) |
| **Game (Evo-Tactics Vue3)** | HEAD main `05af47e9` (Ryzen synced 2026-05-28). Clean. **Fase-3 epigenome SHIPPED full** (engine #2402 + live loop #2404 + lineage sim #2407 + weight 0.45 #2409 + hardening #2412 + games-index #2405). Suite 1333/0-fail. DRAFT PR #2385 still open (weekly drift, low-pri triage). | Playtest live (L-069, the Nord) + triage #2385 | -- | Nessuno |
| **Game-Godot-v2** | HEAD `bc475bd` local synced. 0 PR open. Daily-ship active: **PR #356 merged today** (genetics_api + offspring-ritual Fase-2 canonical). 356 PR cumulative. Genetics Fase-2 active sprint. | Monitor (Eduardo-driven) | -- | Nessuno |
| **Dafne swarm (evo-swarm)** | Local branch `chore/weekly-digest-2026-05-27` (2 modified files: cycle-log + dafne-proposals.json). Origin/main HEAD `670e309` (2026-05-25). **PR #123 OPEN** (weekly digest 2026-05-27, non-draft -- needs review/merge). Flask :5000 DOWN. Recent: born-ready artifact enrichment + aider worktree coverage. | Triage PR #123 | -- | Flask down (not blocker unless workflow resumes) |
| **AA01 (Archon Atelier 01)** | v1.0.0 silent-driver mode. Counter 12/5 sera post Bundle 1+2+3: **14 archive entries + 11 lessons cumulative**. Workspace 0 attivi. | Continua driver mode + nuovo task quando emerge. | nessuna | nessuno bloccante |
| **vault-shared (Vault Knowledge Mgmt)** | Local `C:/dev/vault` HEAD `9880f4da0` (2026-05-25, obsidian-wiki runbook). Dirty: 1 modified (.gitignore) + 2 untracked. **4 DRAFT PRs open** (#180/181/190/201 coherence-backstop daily series 24-27/5 -- triage needed, likely Eduardo-merge-gate). Privacy: sovereign-only. | Triage 4 open DRAFT PRs (Eduardo-merge-gate) | -- | Nessuno |
| **Game-Database** (Ryzen `C:\dev\Game-Database`, Lenovo clone present) | HEAD `13079e2` (2026-05-25). 0 PR open. **Phase C-Game versioning active**: versioned trait reads API (#163) + version-management UI (#164) + RFC design (#166). Jules/Claude active. | Monitor (Eduardo-driven) | -- | Nessuno |
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

**Status**: Fase 6 CLOSED 2026-05-07 (ADR-0015 + ADR-0017 Accepted, scenario A full-sovereign). SPRINT_02 active (window 5/20 -> 6/19). Stack ADR-0017 scaffold opt-in (DOWN default, hot-restart <60s). Claude Max ri-acquistato fino ~2026-06-17.
**Last-verified**: 2026-05-28.
**Decisioni pendenti**:
- ADR-0016 (Proposed) awaiting n>=3 data points addizionali.
- **ADR-0036 (Proposed 2026-05-29) -- Unified Orchestration Doctrine**: `ORCHESTRATION.md` single cross-executor routing authority (hub Opus 4.8 + 5 spokes; capability/cost/privacy routing; mandatory different-model verification gate; autonomy ladder full rollout). Consolidates ADR-0013/0022/0023/0030/0034/0035; reframes MODEL_ROUTING come local-fleet detail. Scoped fleet-tools MCP (Tavily + OpenAI image + non-Claude cross-check judge) GO -- build pending spec/plan. **Ratify trigger**: >=1 clean external-merge-auto cycle/repo, zero bad-merge, ~2 weeks. Cross-fleet (Lenovo + Ryzen).
**Sub-agent ecosystem**: 18 agent registrati (`.claude/agents/`) coprono 4 repo + cross-cutting. Dettaglio: [.claude/agents/README.md](.claude/agents/README.md), fonti in `SOURCES.md`.

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
**Status**: repo daily-ship attivissimo (multi-track). HEAD main `05af47e9` (Ryzen synced). Fase-3 epigenome SHIPPED full; suite 1333/0-fail. Governance vive nel Game repo (`docs/governance/`); codemasterdd monitora, non dirige.
**Last-verified**: 2026-05-28.
**Open**: DRAFT PR #2385 (weekly drift audit, low-pri triage).
**Blocker**: nessuno.
**Next (codemasterdd-side)**: monitor Eduardo+AA01-driven progression; triage #2385; auto-skip PR cron `skiv-monitor`. NON gestire capability/design interni.
**Detail-pointer**: Game `docs/governance/` + memory `project_game_wave3_hub.md` + `project_multi_repo_overview.md`. Audit findings storici (boss enrage, XP curve) + Sprint-Impronta CAP-11..15 in archive history.

---

## Dafne swarm (evo-swarm)

**Path**: `C:\Users\edusc\Dafne\workspace\swarm\` (Lenovo) + `C:\dev\evo-swarm` (Ryzen clone) -- **Remote**: [MasterDD-L34D/evo-swarm](https://github.com/MasterDD-L34D/evo-swarm) -- **Privacy**: sovereign (orchestratore AI custom)
**Status**: Atto 2 active. Origin/main HEAD `670e309` (2026-05-25). Process persistence ADR-0019 (`START-SWARM-PERSISTENT.ps1`). Chat Dafne endpoint `:5000/dafne` (fallback chain qwen3:8b -> groq 70B -> cerebras 8B -> gemini flash). Flask :5000 DOWN (not blocker unless workflow resumes).
**Last-verified**: 2026-05-27.
**Open**: PR #123 OPEN (weekly digest 2026-05-27, non-draft); OD-004 dashboard usage deferred; OD-005 Tavily degraded.
**Blocker**: nessuno hard.
**Next**: triage PR #123. Handoff: Dafne propone -> Eduardo approva via POST -> H5 gate -> Game agents/ write.
**Detail-pointer**: repo swarm governance (5 file root-level) + memory `reference_dafne_swarm.md` + `project_dafne_persona.md`.

---

## Game-Godot-v2 (Evo-Tactics Godot 4.x port, pivot 2026-04-29)

**Path**: `C:\dev\Game-Godot-v2\` (cloned 2026-05-07) -- **Remote**: [MasterDD-L34D/Game-Godot-v2](https://github.com/MasterDD-L34D/Game-Godot-v2) -- **Privacy**: public (cloud-whitelisted)
**Status**: daily-ship attivo. HEAD `bc475bd` local synced. 356 PR cumulative. Genetics Fase-2 active sprint. Stack Godot 4.x GDScript (200 test file GUT, ~1719 asserts; no Node/Vue/Python). Governance interna autosufficiente (proprio CLAUDE.md con caveman mode + AGENTS.md per Codex + SAFE_CHANGES/TASK_PROTOCOL); codemasterdd monitora soltanto. Hook globali applicati via `core.hooksPath` user-level.
**Last-verified**: 2026-05-27.
**Open**: 0 PR open.
**Blocker**: nessuno post-clone.
**Next (codemasterdd-side)**: monitor `gh pr list`. NON gestire GDScript/scene files (Eduardo-driven). Relazione con Game (Vue3): Vue3 = simulation core + gameplay loop; Godot v2 = visual shell + UX + canonical frontend (long-term Godot canonical, Vue3 archive, decisione futura).
**Detail-pointer**: repo CLAUDE.md + memory `project_multi_repo_overview.md`.

---

## vault-shared (sibling-peer Eduardo)

**Path**: `C:\dev\vault\` (Lenovo clone downstream + Ryzen origin) -- **Remote**: [MasterDD-L34D/vault](https://github.com/MasterDD-L34D/vault) -- **Privacy**: **sovereign-only** (NON in aider-privacy-whitelist; aider-cloud su file vault = ABORT)
**Status**: sibling-peer disjoint scope (knowledge management Karpathy LLM-wiki ACCESS + 7 production agents on content). HEAD `9880f4da0` (2026-05-25). Stack overlap: Ollama LAN (stesso daemon) + qwen2.5-coder + deepseek-r1 + Claude variants + LLM routing matrix v1.0. Hook globali compatibili (validated 2026-05-10).
**Last-verified**: 2026-05-25.
**Open**: 4 DRAFT PRs (#180/181/190/201 coherence-backstop daily series, Eduardo-merge-gate).
**Blocker**: nessuno.
**Boundary**: codemasterdd PUÒ branch+PR push, MAI direct-main/merge. Eduardo media il merge-gate (oversight SPOF intenzionale su personal workflow). Cross-reference one-way: vault llm-routing matrix -> potential MODEL_ROUTING.md addendum codemasterdd.
**Next**: triage 4 DRAFT PRs (Eduardo-merge-gate).
**Detail-pointer**: memory `project_vault_shared.md`. Privacy rationale (academic integrity UniUPO + curated narrative IP + cross-project strategic + prompt library) in archive/CLAUDE.md.

---

## Ryzen-only sibling repos (minimal monitoring)

5 repo attivi presenti solo su Ryzen `C:\dev\` (consolidati 2026-05-21), tracking minimo informational (snapshot on-demand, no piano operativo cross-repo). **Privacy**: tutti default SOVEREIGN in whitelist Aider Ryzen finche no classificazione per-repo. Trigger ADR addendum se uno cambia scope strategico.

| Repo | Status | Privacy |
|------|--------|---------|
| **claude-supermemory-local** | Active dev. Local SDK replacement Supermemory cloud. | sovereign |
| **compass-marketplace** | Active dev (compass plugin marketplace, direction-first lens Claude Code). | sovereign |
| **Game-Database** | **Active monitored** -- Taxonomy CMS Evo-Tactics (Prisma + PG + Express + React MUI + Vite). Upstream content provider per Game (Vue3) via `npm run evo:import` + HTTP runtime API (`GAME_DATABASE_ENABLED=true`). Has own CLAUDE.md (multi-client ADR-0021) + WORKSPACE_MAP.md. PUBLIC, no LICENSE. Jules aggressive-maintenance source. Lenovo clone present (verificato 2026-05-28). Boundary: auth esplicita Eduardo per review/merge/close (sibling Evo-Tactics family). | public, cloud-OK |
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
| **~giugno-agosto 2026** | Synesthesia riattivazione | Synesthesia | Privacy validation 2/3 + esame prep |
| **~2026-08-01** | **SDMG-gate quarterly review** (codemasterdd PR #194 narrow-pick 2-week empirical period -> 3 month review) | codemasterdd | Trigger: adoption rate < 30% qualifying decisions OR ADOPT-rate without executed experiment > 0 -> ADR-0026 amendment B/C |
| **trigger-based** | **ADR-0036 ratify** (Proposed->Accepted, Unified Orchestration Doctrine) | codemasterdd | Trigger: >=1 clean external-merge-auto cycle/repo, zero bad-merge, ~2 weeks |

---

## Regola di ingaggio

**Quando apri sessione cold**: leggi CLAUDE.md + COMPACT_CONTEXT.md + questo file (in quest'ordine) → avrai vista operativa completa.

**Quando cambia stato di un repo**: aggiorna la riga corrispondente in questo file (+ ADR/BACKLOG/JOURNAL del repo specifico se necessario).

**Quando emerge decisione multi-repo**: ADR dedicato in codemasterdd `docs/adr/` con scope esplicito cross-repo.
