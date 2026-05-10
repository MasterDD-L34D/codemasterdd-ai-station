# COMPACT_CONTEXT

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/COMPACT_CONTEXT.md`.
>
> Aggiornare in rituale chiusura sessione (CLAUDE_OPERATING_RULES.md #9).

## Progetto
- **Nome**: CodeMasterDD AI Station
- **Versione del compact**: v17 (sessione 2026-05-09 sera tardi -> 10/5 mattina: housekeeping + AA01 audit + H11 closure + H7 scaffold. Cumulative 7-10/5: 24 PR mergeati.)
- **Data ultimo aggiornamento**: 2026-05-10 mattina

## Stato attuale
- **Barra globale ~99%** (invariata da v16): Fase 6 + Fase 7 CLOSED. ADR-0022 + ADR-0023 + ADR-0024. **Window pre-19/05 chiusa anticipata su tutti i task pre-Max**: 8 PR 9/5 mattino-mezzogiorno (H7-H12) + 4 PR 9/5 sera-tardi/10/5 (#30 v15 final + #31 cascata M9-M10 + #32 install-schtasks + #33 H11 closure superseded). Privacy guard rail tecnico attivo. Stop hook deployed (atteso prima activation prossima session). Tooling task-classify/smoke-hooks/backup-keys/bench-cloud-free installato globale + scheduled daily/weekly. AA01 lifecycle smoke 6/6 PASS, workspace pulito. Niente piu' BLOCKING tecnico. 9gg residui pre-Max al 10/5.
- HEAD origin/main `9ec352c` (post merge PR #31-#33 in giornata 9/5 sera-tardi -> 10/5). **Worktree corrente `recursing-mirzakhani-da8bb3` su nuovo branch `claude/h7-scaffolding-housekeeping`** (1 commit ahead per H7+JOURNAL+COMPACT v17 housekeeping bundle, pending push + PR).
- **Stack ADR-0017 ACTIVE MODE 8/5 sera**: LiteLLM:4000 + Langfuse:3000 + Postgres + dogfood-ui:8080 UP. T3 SPRINT_02 hot-restart validation anticipato + passato (<60s endpoint health, persistence preservata). Da spegnere `docker compose down` a chiusura sessione.
- **OpenCode v1.14.41** (npm global) installato 8/5 sera. Config `~/.config/opencode/opencode.json` con 5 provider mappati. Default `ollama/qwen3-coder:30b` (tier 1 sovereign, ADR-0022 Accepted).
- **Agent ecosystem ADR-0018**: 12/18 ready, 6/18 draft trigger-gated. Status invariato dal 24/04.
- **Codex `/structural-reset` REJECTED + chiuso + delete remote**: branch difensivo Codex Cloud sandbox-confusion (assunzione "transplanted, paths missing" smentita empiricamente, 9/9 path target presenti). Cherry-pick astratto: ADR-0021 + AGENTS.md + encoding policy.
- **PR pulito 7/5 -> 9/5 notte**: 7/5 (10 PR #1-#10 governance/Codex/closure/sprint/smoke/godot/aider/master_prompt) + 8/5 mattino-sera (10 PR #11-#20: governance refresh #11, skiv pattern #12, drift cleanup #13, journal/compact #14, ADR-0022 Proposed #15 + addendum #16 + dogfood #17 + #18 + Accepted #19 + tier integration #20). **20 PR mergeati cumulativi 7-9/5**. Coda PR codemasterdd vuota.
- **Pattern automation auto-skip**: workflow Game-side `auto/skiv-monitor-update` cron 4h riconosciuto (PR #12). codemasterdd NON traccia PR-specifico ne' valuta merge (Game-side deterministico).
- **ADR-0022 OpenCode tool-use routing Accepted**: tier OpenCode-specifico distinto da Aider. Default `ollama/qwen3-coder:30b` MoE A3B (3/3 PASS). Cloud free non viable (rate-limited). Qwen 2.5 Coder family non tool-use OpenCode-compat.

### Gap operativo 25/04 -> 07/05 (non-stagnation)

Eduardo ha lavorato attivamente in altri repo (silent driver mode):
- **Game**: Sprint Impronta Ondata 1, 8+ commit clusterati 25-26/04, branches `aa01/cap-11..15` (telemetry + onboarding v2 + imprint phase V2). HEAD `5f42757a` (26/04 12:53 CET). **Pausa Sprint Impronta dal 26/04 (~12gg)**. PR #2108 Claude Code session swarm-distillation aperto 7/5 sera (non triagato).
- **Dafne swarm**: Atto 2 day 11+ -> day 12+, 10 commit cumulative (5 al 7/5 mattina + **4 nuovi 7/5 sera che chiudono OD-002+OD-003+OD-006** + 1 nuovo 8/5 00:29 PR #71 lock fix). HEAD `a87da39`. Decision debt cleanup massiccio.
- **Game-Godot-v2**: 215 PR mergeati totali (+4 dal 7/5 sera). Path A canonical CHIUSO end-to-end 7/5.
- **AA01**: silent driver del Sprint Impronta Game, capability-by-capability. 2 task PROPOSED del 25/04 (#001 voice-test + #002 day-5-post-session-ritual) restano in workspace.
- **codemasterdd**: dataset Fase 6 fermo a n=12 dal 24/04 -- shift naturale di focus quando policy hub ha completato il ciclo (trigger ADR-0008 confermato a #12).

## Obiettivo di questa fase

**Transition window 08/05 -> 19/05** (11 giorni residui Claude Max):
- Smoke test 3 wrapper sovereign empirico -- gia' eseguito PR #6 in giornata 7/5 (T1 SPRINT_02 anticipato)
- SPRINT_02 abbozzo -- gia' eseguito PR #5 in giornata 7/5
- Cleanup PR esterni opportunistico -- **TUTTI completati 7/5**: Game-Database #97 closed-stale, #105 merged, compass-marketplace #10 merged, evo-swarm #61 merged
- Triage opzionale: PR #2108 Game (swarm-distillation routine 7/5 sera, governance interna Game decide)
- 8/5: governance refresh post 7/5 sera (questa sessione) -- STATUS_MULTI_REPO + COMPACT v12
- 19/05: disattivazione Claude Max, transizione a wrapper sovereign + Ollama

## Cosa e' gia' stato fatto

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

## Decisioni prese

### ADR strategici (24 totali, indice in DECISIONS_LOG)
- **ADR-0008** Hub pattern tier routing (cosmetic/behavior/escalation)
- **ADR-0011** Commit governance cross-agent
- **ADR-0012** RAM 64GB upgrade
- **ADR-0013** Tier 3 cloud free providers
- **ADR-0014** Fase 6 compressa
- **ADR-0015** Fase 7 budget full-sovereign + deroga #3 Synesthesia -- **Accepted 2026-05-07**
- **ADR-0016** Constraint-count routing -- Proposed (n>=3 data points trigger pending)
- **ADR-0017** UI + observability stack -- **Accepted 2026-05-07** (5/5 criteri PASS)
- **ADR-0018** Agent readiness protocol 3-gate -- Accepted 2026-04-24
- **ADR-0019** Dafne process persistence -- Accepted 2026-04-24
- **ADR-0020** Silent-fail Python guardrail -- Accepted 2026-04-25 (PR #1 mergeato)
- **ADR-0021** Multi-client instruction files (AGENTS.md + Codex anti-confusion) -- **Accepted 2026-05-07** (PR #2 mergeato)
- **ADR-0022** OpenCode tool-use model routing (tier OpenCode distinto da Aider) -- **Accepted (early, n=3, ratification check 2026-06-09)** (PR #15 Proposed + #19 Accepted + #28 retroactive flag)
- **ADR-0023** Strategic tier post-Max API on-demand budget cap -- **Proposed 2026-05-09** (Eduardo scelta 1A, $10-20/mese cap + trigger reactivation Pro)
- **ADR-0024** Vue3 archive + Godot v2 canonical timeline 2026-09-30 -- **Proposed 2026-05-09** (Eduardo scelta 5A+, soft-deadline + AA01 attivazione H11)

### Decisioni non-ADR (operative minori, in DECISIONS_LOG)
- **001** Adozione schema framework archivio
- **002** `FIRST_PRINCIPLES_GAME_CHECKLIST` N/A per questo repo
- **003** Regole 07_OPERATING_PACKAGE pointer + adozione (no clone root)
- **004** (pending entry) Codex `/structural-reset` REJECTED 2026-05-07

## Vincoli hard
- RTX 5060 8 GB VRAM -> ctx tuning obbligato modelli >7B
- Windows cp1252 bug Aider -> fix deployato + 9 dogfood consecutivi senza retry loop naturale (n=15 trigger raggiunto -- gap closure not bloccante)
- **Deadline fissa 2026-05-19** (Claude Max expiration). Fase 6 closure anticipata a 2026-05-07.
- Privacy per-repo rigorosa (Synesthesia mixed dormant fino ago 2026)
- No `--force` su main, no `--no-verify`, Conventional Commits enforced

## Problemi aperti

- **P3** Privacy validation Synesthesia 1/3. Retroattivo a riattivazione ~ago 2026 (deroga ADR-0015 documentata).
- **P6** Qwen 7B commit-prompt 0% compliance (auto-retry post-hook funziona empirically).
- **P7** Cloud 70B degrada a 20% compliance su behavior-critical con >=5 strict semantic constraint (dogfood #7).

P1, P2 chiusi tramite ADR-0015 closure (P1 behavior-critical n>=5 superato; P2 cp1252 monitoring chiuso a soglia).

## File / output importanti
- Governance root-level (12, +AGENTS.md): `PROJECT_BRIEF`, `COMPACT_CONTEXT` (questo), `DECISIONS_LOG`, `BACKLOG`, `OPEN_DECISIONS`, `ROADMAP`, `SPRINT_01`, `MASTER_PROMPT`, `REFERENCE_INDEX`, `PROMPT_LIBRARY`, `MODEL_ROUTING`, `AGENTS.md` (nuovo per multi-client)
- Convenzioni: `CLAUDE.md` (autoritativo) + `AGENTS.md` (Codex preamble) + `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/*` (meta-rules)
- Diario: `JOURNAL.md` (entry 2026-05-07 +87 righe)
- Decision history: `docs/adr/` (21 file, ultimi ADR-0015 e ADR-0017 e ADR-0020 e ADR-0021 Accepted)
- Operational log: `logs/aider-delegation-2026-04.md` (12 dogfood, fermo dal 24/04)
- Framework archivio: `Archivio_Libreria_Operativa_Progetti/`

## Prossimi 3 passi

1. **Eduardo direct (azioni standalone, residuo unico)**:
   - **H7 setup ANTHROPIC_API_KEY** in `~/.config/api-keys/keys.env` (~5min via Anthropic Console) -- pre-19/05 priority. Scaffold log `logs/claude-api-spend-2026-05.md` gia' pronto (gitignored).
   - ~~H11 AA01 attivazione~~ DONE 9/5 sera (superseded by reality, 2 task stale archived TIMEOUT)
2. **Calendarizzati passive** (no immediate action):
   - 2026-05-19 Claude Max expiration (10gg residui, stack pronto)
   - 2026-05-20+ SPRINT_02 prima sessione Fase 8 sovereign (T1+T3+T4 anticipated DONE; restano T2 dogfood organico + T5 cost tracking + T7 review)
   - 2026-06-07 ratification check ADR-0021
   - 2026-06-09 ratification check ADR-0022
3. **Deferred SPRINT_02 / opportunistic post-19/05**:
   - ~~M7 backup automation API keys~~ DONE 9/5 sera
   - ~~M8 hook integrity smoke test settimanale~~ DONE 9/5 sera
   - ~~M9 task-classify tooling~~ DONE 9/5 sera
   - ~~M10 OpenCode + cloud free token-trim test~~ DONE 9/5 sera (n=3 conclusivo, ADR-0022 confirmed)
   - **L6 (NEW da M10)** OpenCode plugin custom o tool-set trim per cloud free viable -- solo se gpt-4o-mini emergency budget eccessivo
   - T7 review fine sprint MAX=2 re-eval se workflow evolve 2-tier dominant

Side-tasks gia' DONE 7/5 -> 9/5 sera:
- 7/5: ADR-0015 + ADR-0017 Accepted (PR #4), SPRINT_02 abbozzo (PR #5), smoke sovereign T1 (PR #6), Game-Godot-v2 governance (PR #7+#8), pattern aider wrong-target (PR #9), master_prompt handoff (PR #10), 4 PR esterni triagati
- 8/5 mattino: governance refresh post 7/5 (PR #11)
- 8/5 sera: pattern auto-skip skiv (PR #12), drift cleanup ROADMAP+BACKLOG+OPEN_DECISIONS (PR #13), JOURNAL+COMPACT v13 (PR #14)
- **9/5 notte (transition attiva)**: ADR-0022 Proposed (PR #15) + addendum cloud (PR #16) + dogfood OpenCode #25 (PR #17) + #26 (PR #18) + ADR-0022 Accepted (PR #19) + tier OpenCode in CLAUDE.md+MODEL_ROUTING (PR #20) + COMPACT v14 + JOURNAL append
- 9/5 mattino-mezzogiorno: STATUS+memory (PR #22-#23), 6 H-tasks (PR #24-#29)
- **9/5 sera**: M9 task-classify (commit `c74966c`), M8 smoke-hooks (`912b91a`), M7 backup-keys (`bb78999`), M10 bench cloud free (`fe94dbe`) -- 4 commit branch worktree pendenti PR

Cumulativo: **21 PR mergeati cumulative + 4 commit branch ahead** 7-9/5. Branch `claude/recursing-mirzakhani-da8bb3` pending push + PR Eduardo.

## Next session restart: cosa leggere per ripartire

Ordine raccomandato:
1. `CLAUDE.md` -- convenzioni progetto autoritative
2. Questo file (`COMPACT_CONTEXT.md`) -- snapshot stato corrente
3. `AGENTS.md` SE sessione e' Codex/OpenCode/sandbox-based -- preamble anti-confusion
4. `STATUS_MULTI_REPO.md` -- dashboard cross-repo (Game Sprint Impronta, Dafne Atto 2)
5. `BACKLOG.md` + `OPEN_DECISIONS.md` -- cosa e' aperto
6. `SPRINT_01.md` (close imminente) o `SPRINT_02.md` (quando creato)
7. ADR rilevanti se task tocca topic noto

Memory auto-caricata via `~/.claude/projects/.../memory/MEMORY.md`.
