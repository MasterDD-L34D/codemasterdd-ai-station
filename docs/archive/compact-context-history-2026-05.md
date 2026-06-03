# COMPACT_CONTEXT history -- 2026-05 session log (archived)

## origin: COMPACT_CONTEXT.md, archived 2026-06-03 context-files reorg Fase 2
## (verbatim historical session-log block extracted from COMPACT_CONTEXT.md; superseded by the lean current snapshot in that file)

## Cosa e' gia' stato fatto

### Sessione 2026-05-12 mattina (worktree+branch cleanup metodologico + drift fix v20->v21)

#### Pattern strategico
Cleanup operativo post marathon 11/5+12/5 PR #48+#49. Eduardo richiesta esplicita rimozione worktree+branch residui via comandi suggeriti (3 worktree + 3 branch). Applicato Protocol 1 refresh-verify + Protocol 2 autoresearch multi-source per ogni candidato (merged-status / superseded-content / filesystem-orphan classification).

#### Cleanup eseguito (sequenza)
- **Tentativi iniziali bloccati** da 13 sessioni Claude orfane (PID 11/5 16:03-21:24) lock-holding worktree dirs Windows. Eduardo kill manuale post escalation.
- **6 branch claude/* eliminati**:
  - `claude/funny-dirac-82131b` (merged PR #48)
  - `claude/closure-2026-05-12-aa01-integration` (merged PR #49)
  - `claude/optimistic-shannon-26ff0e` (merged PR #39)
  - `claude/closure-ritual-2026-05-11` (1 commit superseded: COMPACT v19 -> v20 post #48, integration plan IDENTICO in main, JOURNAL absorbed)
  - `claude/journal-compact-v18-housekeeping` (4 commit superseded: fix h12 hook PRESENTE in main via PR #41 squash-merge `32838b4`, v18 housekeeping superseded da v20)
  - `claude/goofy-noether-e8a08e` (3 commit obsoleti: branch 3117 righe IN MENO di main, contenuti tutti riimplementati in PR #38+#39+altri successivi)
- **3 worktree rimosse** via `git worktree remove`: `funny-dirac-82131b`, `optimistic-shannon-26ff0e`, `goofy-noether-e8a08e`
- **5 dir filesystem orfane** (0 items, residui post-cleanup parziale precedente) rimosse: `distracted-colden-c50d3a`, `hardcore-keller-72c77e`, `hungry-haibt-4a83aa`, `magical-villani-f2af96`, `recursing-mirzakhani-da8bb3`

#### Drift identificati nel refresh + fix in questa PR
1. **COMPACT v20 lag 1 PR**: HEAD `f3fdc92` (post #48) -> reale `30e94ee` (post #49). Fix: aggiornato.
2. **Coda PR claim "1 nuova PR closure pending push"**: era PR #49, ora mergeata. Fix: aggiornato a "VUOTA post-merge #49".
3. **Hyperspace Phase 1 ancora in "deferred opportunistic"**: contraddittorio con ADR-0025 ABANDONED definitivo (D-017 99% confidence empirical trial). Fix: rimosso da deferred.
4. **Worktree `funny-dirac-82131b` citata come "orphan post-merge"**: rimossa in questa sessione. Fix: aggiornato a `practical-kowalevski-1f7c9e` synced.
5. **Residui pre-Max**: 8gg -> 7gg.

#### Stato finale repo
- Worktrees: solo `main` + `practical-kowalevski-1f7c9e` (corrente)
- Branch claude/*: solo `practical-kowalevski-1f7c9e` (corrente)
- `.claude/worktrees/`: dir pulita (no orfane filesystem-only)
- `.git/worktrees/` internal: solo entry corrente

#### Branch state
1 commit ahead di main su `claude/practical-kowalevski-1f7c9e` (questo PR drift fix v20 -> v21).

### Sessione 2026-05-11 sera (closure ritual: merge batch + cleanup + integration plan)

#### Pattern strategico
Continuazione marathon 11/5 dopo PR #41 v18 housekeeping merged. Triage open PR + Eduardo "si confermo" auth bulk merge + post-merge cleanup orphan branches via Issue #46 + plan formalization next session integration.

#### Merge batch 5 PR codemasterdd (sequenza ordinata)
- **PR #43** squash `6165905`: pytest base dogfood-ui 18 tests
- **PR #44 auto-closed**: base branch deleted via #43 `--delete-branch` -> GitHub auto-close. **Rescue cherry-pick**: nuovo branch + commit `589279d` (sparklines) -> **PR #45** squash `6cd79c8`. Audit comment su #44 con redirect.
- **PR #40** squash `f437480`: governance fleet Ryzen RTX 4070 SUPER 12GB scoperto + LAN 4 device + AA01 task 002
- **PR #41** squash `32838b4`: housekeeping v18 + OD-007 + hook fix
- Sandbox guard rail 1 volta: force-push `--force-with-lease` denied -> fallback nuovo branch (sandbox-friendly path)

#### Issue #46 cleanup (Eduardo creato da Ryzen sandbox)
- Verify pre-delete: 9 branches associate con PR merged (single edge `claude/dogfood-ui-charts` PR #44 closed-not-merged ma work cherry-picked in #45)
- Bulk delete sandbox flow: 1st attempt denied per "precise user intent naming targets" -> enumerated chat + Eduardo "si" -> 2nd attempt 9/9 OK
- `git fetch --prune` cleanup 9 tracking ref
- **Structural toggle**: `gh api -X PATCH ... -F delete_branch_on_merge=true` confermato. Future merge auto-pulizia attiva
- Issue #46 chiusa con audit comment

#### Integration plan formalization next session
- Auto-analisi: 3 pattern worked + 3 friction + 1 meta-pattern
- Plan 3 obiettivi sequenziati: AA01 hub orchestrante + Vault read-only sibling-peer + Hyperspace Phase 1 privacy audit
- Sequencing 3 sessioni (~1.5h + 2h + 3h), dipendenza esplicita Hyperspace -> Vault lessons
- Risk flag Claude Max 8gg residui (Hyperspace audit ideally entro 19/05)
- Plan committed: `docs/plans/integration-aa01-vault-hyperspace-2026-05.md`

#### Branch state
1 commit ahead di main su `claude/closure-ritual-2026-05-11` (questo PR plan + JOURNAL + COMPACT v19).

### Sessione 2026-05-10 mid-morning (SPRINT_02 T3+T4 + governance refresh #35-#39 + vault-shared integration)

#### Pattern strategico
Continuazione marathon 10/5 oltre PR #34 (v17 housekeeping). 5 PR mergeati 04:25 -> 11:26 CEST coprendo: SPRINT_02 pre-validation T3 (stack hot-restart 2nd pass) + T4 (cleanup PR esterni triage) + dogfood-ui regression fix + 3 governance refresh (status / backlog / open_decisions drift sync) + AA01-driven integration di 4 repo identificati autonomamente (vault-shared + toolkit + autoresearch + hyperspace).

#### PR #35 mergeato (`0da13ff`): SPRINT_02 pre-validation T3+T4 + dogfood-ui regression fix
- **T3 hot-restart 2nd pass PASS**: `docker compose up -d` 11.7s wallclock (target <60s), LiteLLM + Langfuse 200 OK, **38 trace preservati post 13gg+ downtime** (volume codemasterdd-postgres-data integrity), dogfood-ui up
- **Regression detection**: POST `/api/entries` 500 ValueError -- `apps/dogfood-ui/db.py:56` `valid_stacks` desync con `app.py:184-196` `VALID_STACKS` (commit `6924482` initial scaffold vs `8c70728` smoke sovereign extension)
- **Fix path A direct**: db.py:56 valid_stacks aggiornato sync con app.py (5 -> 12 righe set). Re-POST {"id":13,"status":"created"}. Field name desync residuo (`retries`/`retry_count` + `tokens_in`/`tokens_sent`) lasciato T2 organic SPRINT_02
- **T4 cleanup PR esterni triage**: 4 PR target gia' triagati 7/5 (Game-Database #97 closed-stale + #105 + compass-marketplace #10 + evo-swarm #61 mergeati). SPRINT_02 status header aggiornato
- **Runbook nuovo** `docs/runbook/adr-0017-hot-restart.md` (127 righe): 5 edge cases documentati (PowerShell IPv6 quirk + LiteLLM 172.18.0.1 health-check + trace count preservation + dogfood-ui regression + field name desync)
- Cleanup git: 4 branch local stale deleted + worktree prune

#### PR #36 mergeato (`ee1edea`): STATUS_MULTI_REPO refresh post 7-10/5 cross-repo
Verify HEAD origin/main empirico via `gh` API (drift mitigation pattern PR #11 caso-studio). Updates: codemasterdd HEAD `a71d653` -> `0da13ff`; Game (Vue3) `7dd18ad` post #2159 BASELINE_WR fix 30 PR mergeati 7-10/5 stream K4/FASE 5/AI sim/skiv; Game-Godot-v2 215 -> ~230 PR (+15); Dafne `9255b4b` Atto 2 day 14+; AA01 2 task PROPOSED storici archived 9/5. Status-phase-a chiarito (PR Game #2138/#2139 GIA' MERGED al 9/5, memory v14 stale). Sprint Impronta narrative corretto.

#### PR #37 mergeato (`e24c070`): BACKLOG H9 drift sync (1 riga)
Sync `[ ]` a `[x]` H9. Bench mixed-workload gia' eseguito 9/5 (commits `cbdf2ed` + `11cac69`) ma BACKLOG checkbox dimenticato. Drift fix.

#### PR #38 mergeato (`516d9a8`): OD-003 closure + drift fix a3+a4
- A3 OD-003 closure: Cerebras 8B cosmetic default + Groq 70B behavior default (opzione 1 formalizzata, gia' implicita in MODEL_ROUTING)
- A4 drift fix: STATUS_MULTI_REPO rimossa entry stale "Decisione 004 da scrivere"
- A2 honest skip: dogfood cosmetic gap n=7->n>=10 NON forzato (working rule "niente forzatura quota")

#### PR #39 mergeato (`3735d32`): vault-shared sibling-peer + 3 reference repo (autoresearch + hyperspace + toolkit)
AA01-driven autonomous task `2026-05-aa01-001-two-repos-analysis-integration` (preset research-long, phase 1-5 standard + Phase 4 harsh-reviewer REWORK verdict 2 BLOCKING + 2 SIGNIFICANT + 1 MINOR fixati).

**Integrazione vault-shared** (MasterDD-L34D/vault):
- Sibling-peer monitored, sovereign-only (NON whitelisted privacy guard rail)
- 7/7 production agents milestone 2026-05-10 (Quality Gate workflow smoke->draft->production 3-gate)
- Stack overlap codemasterdd: Ollama LAN + Qwen + deepseek-r1 + Claude variants
- Privacy validato spot-check empirico (academic UniUPO + IP curated GDR + design notes Dev)
- Hook globali compat VALIDATED (empty commit test PASS, reverted)
- LLM routing matrix v1.0 -> research input MODEL_ROUTING.md (no commit hash drift risk)
- Boundary: NO write-path codemasterdd-side, sibling-peer disjoint scope

**Reference repo** (REFERENCE_INDEX entries):
- awesome-claude-code-toolkit (rohitg00 OSS Apache 2.0): pull-when-needed cherry-pick, audit-then-replay, attribution header, NO bulk import
- Autoresearch (multi-candidate eval): top fit 199-biotechnologies/autoresearch-cli (any AI coding agent) + alternative Karpathy/autoresearch MIT, deferred SPRINT_03+ overnight research
- Hyperspace Pods (strategic Mac mini scenario alternative): libp2p v3 + GossipSub + Kademlia DHT, RTX 5060 8GB qualifies, AUDIT REQUIRED PRE-install (P2P data flow + Pod trust mesh)

File codemasterdd-side: STATUS_MULTI_REPO (+98) + CLAUDE.md (+36) + MODEL_ROUTING (+23) + REFERENCE_INDEX (+45) + 4 memory file nuovi (project_vault_shared + reference_external_toolkits + reference_autoresearch_tools + reference_hyperspace_pods) + project_multi_repo_overview update + MEMORY.md +4.

#### Branch state
1 commit ahead di main su `claude/journal-compact-v18-housekeeping` (questo PR JOURNAL + COMPACT v18).

### Sessione 2026-05-09 sera tardi -> 2026-05-10 mattina (housekeeping + AA01 + H11 + H7)

#### Pattern strategico
Continuazione marathon 9/5 oltre commit `cb248d5` v16. Sequenza esplicita Eduardo: "facciamo tutti i pending" -> "lancia tu lo script" -> "passa a h11" -> "facciamo i caveat mancanti" -> "3+2". 4 PR addizionali oltre i 5 commit base, cambio data 9/5 -> 10/5 durante sessione.

#### PR #31 mergeato (`ae3ca88`): cascata M9-M10 squash
- Squash merge 5 commit: M9 task-classify + M8 smoke-hooks + M7 backup-keys + M10 bench-cloud-free + JOURNAL/COMPACT v16
- Smoke wrapper 3/3 PASS post-install in `~/.local/bin/`

#### PR #32 mergeato (`8cf4994`): install-schtasks setup
- Sandbox bloccato schtasks direct via Auto Mode (Unauthorized Persistence policy) -> mitigation `scripts/setup/install-schtasks.ps1` ~145 righe idempotente (default install + `-Verify` + `-Uninstall`)
- Eduardo auth esplicita -> 2 schtasks installati: ApiKeysBackup daily 03:00 + HookIntegritySmoke weekly Sunday 09:00

#### PR #33 mergeato (`9ec352c`): H11 closure superseded by reality
- Reality check: PR Game #2138 + #2139 status-phase-a GIA' MERGED (memory v14 stale)
- AA01 audit workspace: 2 task PROPOSED 25/04 stale one-shot reactive (eventi 26/04 passati 13gg)
- Action: archive entrambi `--status=TIMEOUT`, workspace 0 attivi, INDEX.md 3 entries cumulative

#### AA01 caveat completati (out-of-repo, no commit codemasterdd)
- `tests/smoke.sh` MANCANTE -> creato (~140 righe), 6/6 PASS lifecycle end-to-end (capture->classify->promote->propose->archive REJECT con self-cleanup)
- 2 fix iter: `set -e` rimosso interferiva classify.sh stderr, find pattern `*smoke-${TS}*` sed strip leading underscore
- Bootstrap audit-replay: idempotente (deps 3/3 OK + profile.yml + .gitkeep + struttura PASS)
- Side-finding: `just` NON installato, fallback `bash scripts/<cmd>.sh` validato OK
- Memory `project_aa01_studio.md` aggiornata: stato post-audit + caveat operativi + workflow task tipico

#### Housekeeping 10/5 mattina (3+2 bundle)
- H7 scaffolding: `logs/claude-api-spend-2026-05.md` (gitignored via `logs/*`) con header + template entry + aggregati cumulative + ADR-0023 reference
- Cleanup 3 branch local stale: `claude/recursing-mirzakhani-da8bb3` + `claude/install-schtasks-setup` + `claude/h11-aa01-closure` deleted local (mergeati squash + remote deleted)
- JOURNAL extension entry + COMPACT v16 -> v17 (questo PR)

#### Branch state
1 commit ahead di main su `claude/h7-scaffolding-housekeeping`, pending push + PR.

### Sessione 2026-05-09 sera (M7-M10 deferred SPRINT_02 cascata 4-task pre-Max)

#### Pattern strategico
Eduardo opzione 3 = opportunistic SPRINT_02 deferred. 4 voci M7/M8/M9/M10 in cascata ordine lean-rischio crescente.

#### M9 task-classify tooling (~25min, commit `c74966c`)
`scripts/task-classify.ps1` (~210 righe). Decision tree CLAUDE.md "Trigger delega in-session" + ADR-0008/0016/0022. Mode interactive 5-6 domande + parametric `-Quiet`. Smoke 9/9 PASS coprenti tutte branche tier (cosmetic locale/cloud/cerebras + behavior locale/groq/borderline-4 + multi-step opencode + cosmetic-subdir-self-ref mitigation + strategic + 5+constraint short-circuit). Install Eduardo manual `~/.local/bin/`.

#### M8 hook integrity smoke test (~40min, commit `912b91a`)
`scripts/smoke-test-hooks.ps1` (~210 righe). 12 test cases: commit-msg ADR-0011 (5) + silent-corruption ADR-0008 (3) + silent-fail Python ADR-0020 (4). Pattern 1 scratch repo per test in `$env:TEMP/hook-smoke-$PID/`. Smoke 12/12 PASS. Schedule weekly Sunday 09:00. 2 fix iter: PS5.1 native `2>&1` ErrorRecord + 1-repo-per-test isolation.

#### M7 backup-api-keys daily rotation (~30min, commit `bb78999`)
`scripts/backup-api-keys.ps1` (~160 righe). Daily snapshot keys.env -> `backup/api-keys/api-keys-YYYY-MM-DD.env` (gitignored). Encryption opt-in DPAPI `-Encrypt`. Idempotent intra-giorno + rotation 30gg + ACL strict best-effort + integrity check round-trip. Smoke 3/3 PASS. Schedule daily 03:00. Recovery DPAPI snippet documentata.

#### M10 bench OpenCode cloud free (~1h, commit `fe94dbe`)
`scripts/bench-opencode-cloud-free.ps1` + `docs/research/bench-opencode-cloud-free-2026-05-09.md`. Esecuzione effettiva n=3 conclusivo (T2/T5 file-attached skipped per yargs `--file` greedy). **ADR-0022 CONFIRMED**: T1 groq/llama-3.3-70b TPM 12k vs richiesto 49698 BLOCKED -2.7x..-4.1x; T4 cerebras/llama3.1-8b ctx 8192 vs 12228 BLOCKED -1.5x; T3 groq/qwen-2.5-coder-32b DECOMMISSIONED. Discovery: nessun `--max-tokens` CLI esposto OpenCode (ipotesi M10 invalidata). Side-action: `~/.config/opencode/opencode.json` refresh rimosso `qwen-2.5-coder-32b` (out-of-repo). 2 fix iter: PS5.1 Start-Process `+` array + opencode TUI hang Start-Process -> bypass bash inline `timeout 90` diretto.

#### Effort cascata
4 task = ~2h45min (vs stima medium 4-6h). Pattern lean-hyperactive 4° giornata consecutiva confermato.

#### Branch state
4 commit ahead di main su `claude/recursing-mirzakhani-da8bb3`, pending push + PR Eduardo auth esplicita.

### Sessione 2026-05-09 mattino-mezzogiorno (routine + harsh review + 6 H-tasks)

#### Mattino (PR #22 + PR #23 + memory consolidation)
- PR #22: STATUS_MULTI_REPO refresh 9/5 (4 punti accuracy)
- PR #23: Tier 1 cleanup pending (DECISIONS_LOG + MODEL_ROUTING + ADR-0009 status)
- Memory consolidation skill: 6 file out-of-repo refresh post drift -15gg

#### Mezzogiorno (PR #24-#29 + harsh review + 6 H-tasks)
- Harsh review flow chart via harsh-reviewer agent: 2 BLOCKING + 3 SIGNIFICANT + 4 choke + 5 errori + 7 edge cases + 5 process smells
- 6 questions Eduardo BLOCKING vibecoded + risposte 1A 2A 3B 4A 5A+ 6A
- PR #24: harsh review report + ADR-0023 + ADR-0024 + BACKLOG H7-H12 + Decisione 007
- PR #25 H7: ADR-0023 integration CLAUDE.md + MODEL_ROUTING
- PR #26 H9: bench mixed-workload + batched + MAX=2 (3 bench, drift docs corretto, contrarian MAX=2)
- PR #27 H8 BLOCKING: privacy guard rail tecnico (4 wrapper + whitelist, 2/2 smoke PASS)
- PR #28 H10: ADR early-acceptance flag (ADR-0010 addendum + retroactive ADR-0021/0022)
- PR #29 H12: stop hook automatico (2 PowerShell + .claude/settings.json + 3/3 smoke)

#### Effort lean-hyperactive
8 PR mergeati in 4-5h, effort reale tipicamente <50% stime (es. H8 1h vs 1gg, H10 30min vs 2-3h).

#### Trigger calendarizzati post-merge
- 2026-05-19: Claude Max expiration (10gg residui)
- 2026-05-20+: SPRINT_02 prima sessione full-sovereign
- 2026-06-07: ratification check ADR-0021
- 2026-06-09: ratification check ADR-0022

### Sessione 2026-05-08 sera -> 9/5 notte (transition attiva sovereign + ADR-0022 OpenCode routing Accepted)

#### Pattern strategico
"non ci conviene incominciare a usare opencode e infra prima che claude max finisca?" -- transition ATTIVA con safety net Claude Max invece di stop passivo + cold-cutover.

#### Setup transition
- OpenCode v1.14.41 installato (npm global, dopo Path 1 PowerShell installer 404 + sandbox bloccato `irm | iex` per missing auth -> fallback npm safer)
- Config `~/.config/opencode/opencode.json` 5 provider mappati a tier ADR-0008
- Stack ADR-0017 active mode: docker compose up -d -> 4 endpoint UP (LiteLLM/Langfuse/Postgres/dogfood-ui), T3 SPRINT_02 hot-restart anticipato + passato

#### Smoke test (entries #16-#24)
9 smoke validation tool-use compat. Findings critici:
1. **Qwen 2.5 Coder family** (7B/14B Q2) NON tool-use OpenCode-compat (raw JSON in stdout)
2. **Cloud free 8B-70B** tutti rate-limited TPM o context vs OpenCode default 50k token
3. **Solo Ollama qwen3-coder:30b MoE** viable per OpenCode default sovereign
4. Discovery: env var Gemini differisce tra tool (`GEMINI_API_KEY` Aider vs `GOOGLE_GENERATIVE_AI_API_KEY` OpenCode)

#### Dogfood OpenCode reali (entries #25-#26)
- #25 (PR #17): docstring `empty_stats()` stats.py -- PASS 1st-try, +1/-0
- #26 (PR #18): docstring `_auth_header()` langfuse_client.py -- PASS 1st-try, +1/-0, indentazione classe preservata

PASS rate Ollama 30B MoE OpenCode: **3/3** (smoke + 2 edit reali).

#### ADR-0022 ciclo completo
- PR #15: Proposed (199 righe MADR, 4 opzioni, decision tree)
- PR #16: addendum cloud findings (status invariato Proposed)
- PR #19: ratification Proposed -> Accepted (post 2/2 dogfood reali)
- PR #20: integrazione tier OpenCode in CLAUDE.md + MODEL_ROUTING.md (dual-name Gemini, decision tree, scenario routing)

### Sessione 2026-05-08 sera (pattern auto-skip skiv-monitor + drift cleanup piani strategici)

#### PR #12 -- pattern auto-skip skiv-monitor cron 4h
Triage chat-only PR #2117 Game (8/5 02:45 UTC, automation `github-actions[bot]` workflow `skiv-monitor.yml` cron 4h). Diff +229/-212, 4 file in safe-list `data/derived/skiv_monitor/` + `docs/skiv/MONITOR.md`. Pattern coerente, merge-ready POV codemasterdd. Decisione: pattern auto-skip esplicito documentato in STATUS_MULTI_REPO (4 edit minimali). PR #12 mergeato `6ec8681` 11:06 UTC. Nessun PR-specifico tracking futuro (cambia ogni 4h).

#### PR #13 -- drift cleanup ROADMAP + BACKLOG + OPEN_DECISIONS
Esposizione "stato e ripresa" ha rivelato drift accumulato ~14gg dietro nel ROADMAP (mai refreshato da PR #11). Refresh chirurgico 7 punti drift:
- ROADMAP (4): Fase 6 IN PROGRESS 40% -> CLOSED 7/5; Fase 7 BLOCKED -> CLOSED 7/5; Fase 8 PLANNED -> PLANNING transition window 11gg + 7 task SPRINT_02 mappati; Calendario sintetico 23/04 -> 8/5 con milestone reali Fase 6+7 closed
- BACKLOG (2): U5 ADR-0017 ratification "if completati" -> DONE Accepted 7/5 anticipato; "Primo sprint consigliato" SPRINT_01 -> Sprint corrente SPRINT_02 planning (T1+T4 anticipated DONE)
- OPEN_DECISIONS (2): OD-001 dettaglio "Proposed 24/04" -> "Accepted 7/5" + soft-override 5 rationale; **OD-002 cp1252 closure formale** (n=15 cumulative senza retry loop naturale, soglia ADR-0014 raggiunta, M3 PowerShell wrapper deferred reactive)

Scope chirurgico: nessun file core toccato (JOURNAL/COMPACT/DECISIONS_LOG/CLAUDE/AGENTS/ADR/SPRINT preservati). PR #13 mergeato `f8a4bb3` 11:20 UTC.

### Sessione 2026-05-08 mattino (audit coerenza doc + governance refresh)

#### Audit coerenza doc + scope cross-repo
Reality-check 6 governance file vs stato reale post 7/5 sera + 8/5 mattina. Drift identificati:
- COMPACT v11: HEAD `39f97da` claim vs reale `5828909` (mergiate PR #4-#10)
- STATUS Game-Godot-v2: 211 PR vs reale 215 (+4 post 7/5 sera)
- STATUS Game: "0 PR open" vs reale 1 (PR #2108 swarm-distillation Claude Code session 7/5 22:19 UTC)
- STATUS Game: claim "in pieno corso" 7/5 vs reale pausa Sprint Impronta dal 26/04 (~12gg, drift accuracy preesistente perpetuato in v1 refresh, fixato in v2)
- STATUS Dafne: HEAD `1e14253` vs reale `a87da39` (+5 commit: 4 il 7/5 sera + 1 il 8/5 00:29 CET)
- STATUS Dafne open items: OD-002+OD-003+OD-006 chiusi vs status precedente "open"

Cross-repo positives confermati: JOURNAL 7/5 entry completa, DECISIONS_LOG ha Decisione 004+005, ADR coerenti, BACKLOG H-items chiusi correttamente, OPEN_DECISIONS OD-001+OD-006 chiusi, AGENTS.md aderente ADR-0021.

#### Governance refresh chirurgico (questa sessione)
Branch dedicato `claude/governance-refresh-2026-05-08`:
- STATUS_MULTI_REPO: refresh date 8/5, sezioni Game/Dafne/Game-Godot-v2 aggiornate, header tabella, scheduled checkpoint riga aggiunta
- COMPACT v11 -> v12 (questo file)
- CLAUDE.md sezione Game-Godot-v2 PR count cosmetic fix (211 -> 215) + sezione Game pausa Sprint Impronta corretta + Stack installato +1 riga "modelli aggiuntivi"

Nessun file core toccato (JOURNAL/DECISIONS_LOG/ADR/BACKLOG/OPEN_DECISIONS/SPRINT_02/AGENTS.md preservati).

#### Pre-Max checklist tecnica (locale read-only, eseguita questa sessione)
Verifica wrapper sovereign + API keys + stack hot-restart-ready in vista 19/05 expiration:
- 6 wrapper aider-* presenti in `C:/Users/edusc/.local/bin/` (cosmetic, refactor, groq, cerebras, gemini, openai) + aider-log + aider.exe v0.86.2
- API keys `~/.config/api-keys/keys.env` 609 bytes presente; Aider config global `~/.aider.conf.yml` 235 bytes presente
- Aider 0.86.2, promptfoo 0.121.7 (vs latest 0.121.10, lag minor), 16 modelli Ollama presenti
- Docker compose `infra/docker-compose.yaml` config validation OK (`docker compose config --quiet` exit 0)
- Drift trovato: CLAUDE.md "Stack installato" Ollama documentava 8 modelli, reali 16. +1 riga "modelli aggiuntivi" added.

Esito: sovereign stack pronto per 19/05 transition. Nessun blocker tecnico.

#### Triage operativo PR #2108 Game (chat-only delivery)
PR #2108 Game (docs research distillation run #5 evo-swarm). Analisi codemasterdd:
- Safety: docs-only additive (1 file nuovo +211/-0), no edit `data/core/`, gate ratifica preservato (5 open questions per game-side review)
- CI: governance + paths-filter SUCCESS, altri SKIPPED (atteso docs-only)
- Branch: `claude/swarm-distillation-2026-05-08` -> Claude Code session, NON Dafne automation
- Conflitti: nessuno, mergeable
- Pattern coerente vs altri `docs/research/2026-04-25-skiv-*.md` esistenti

Raccomandazione: **merge-ready** dal POV codemasterdd. Decisione merge resta Game-side per ownership boundary CLAUDE.md ("monitora solo"). Tentato `gh pr comment 2108` -> sandbox correttamente bloccato (External System Write su repo non-codemasterdd richiede auth esplicita, non coperta da Auto Mode generico). Lezione salvata in `feedback_external_repo_action_boundary.md`.

### Sessione 2026-05-07 (resume + Codex + Fase 6 closure)

#### Triage PR cross-repo
5 PR open su 5 repo. Identificato branch `codex/structural-reset` su codemasterdd (no PR aperto, push 1° maggio) come priorita' sopra tutti gli altri PR.

#### Review sistematica `codex/structural-reset`
43 file +3690/-2186, premessa "transplanted/paths missing". Verifica empirica: tutti 9 path target esistono fisicamente. Codex operava da Codex Cloud sandbox.
Classificazione: 36 REJECT + 4 ADAPT-concept + 0 ACCEPT. Branch REJECTED in toto.

#### Cherry-pick ADR-0021
ADR-0021 "Multi-client instruction files" Accepted (MADR format). AGENTS.md ~70 righe come preamble Codex anti-confusion. CLAUDE.md +10 righe (encoding policy + pointer multi-client). PR #2 mergeato.

#### Cleanup `codex/structural-reset`
PR #3 [REJECTED] formal aperto e chiuso (audit trail). Delete remote ref con conferma esplicita Eduardo.

#### Fase 6 closure anticipata
Dataset n=12 fermo dal 24/04. Decisione: closure anticipata vs target sett.4 originale per evitare dogfood sintetici (anti-pattern ADR-0014).

- **ADR-0015** (Proposed -> Accepted): Scenario A full-sovereign $0-50/anno confermato. Soft-override esteso n>=12 con 5 rationale additivi. Claude Pro NOT acquired, scenario B declassato definitivamente.
- **ADR-0017** (Validated live + Proposed -> Accepted): 5/5 criteri ratification PASS. Stack scaffold opt-in (Docker Desktop manual start).

#### Governance refresh
JOURNAL entry +87 righe (questa sessione). COMPACT v11 (questo file). STATUS_MULTI_REPO refresh + DECISIONS_LOG entry pending in corso branch.

### Pre-sessione corrente
- 14 ADR + ADR-0020 silent-fail Python (Accepted 25/04). 21 ADR totali post-ADR-0021.
- 4 guard rail commit cross-agent + tracking ccusage + dogfood log.
- Quality bench framework (75 test, 100% pass@1).
- 11 file governance root-level + 4 aggiuntivi.
- Framework `Archivio_Libreria_Operativa_Progetti/` integrato.
- 12 dogfood Fase 6 cumulative al 24/04 (cosmetic 93%, behavior 70-80%, corruption 0).
