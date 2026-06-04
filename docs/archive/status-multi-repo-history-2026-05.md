# STATUS_MULTI_REPO — History archive (May 2026)

> Point-in-time audit + session-log sections extracted verbatim from `STATUS_MULTI_REPO.md` (slim 2026-06-03). These are historical snapshots; for current state see the live dashboard + per-repo CLAUDE.md.

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
| AA01 / Gpt | tracciati | AA01 no-.git *(corretto 2026-06-01: vendored nel vault git da PR #72 il 2026-05-17, post-snapshot)*; Gpt repo vuoto | 🔒N-A |

**No loss-risk** ovunque (branch autoritativi synced; Game/Godot root-detached = cosmetico già documentato sopra). Drift = §1-7 ~2gg dietro su repo daily-ship (Game/Godot) + torneo §7 entry mai-vera (PR#18/SHA dangling — da correggere a parte, dominio §7). Raccomandazione: §1-7 HEAD-narrativi non affidabili come git-truth → usare QUESTO blocco §Ecosystem-audit per stato verificato; §1-7 per contesto operativo.

> **Correzione stale-pointer (2026-06-01)**: la riga "AA01 no-.git" sopra era vera al 2026-05-16, ma e' **superata**. ARCHON v2 + AA01 sono ora **vendored nel git del vault** a `Vault-ops-remote/claude-global/aa01-system/archon/` (landato via codemasterdd PR #72 = vault commit `275f8bc5f`, 2026-05-17) e **presenti su Ryzen**. NON e' piu' "Lenovo-only / NON-git / filesystem-direct"; il tier FULL di agent-scanner si attiva dove `aa01/archon/` e' detected (Ryzen incl.). Ref: vault `docs/research/2026-06-01-autogovernance-ecosystem-map.md` (Sez. 2 + Correzioni #1).

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

## Scheduled checkpoints — done (struck-through rows, archived)

| Data | Evento | Progetto | Azione |
|------|--------|----------|--------|
| ~~2026-04-26~~ | Day-5 Dafne swarm | evo-swarm | DONE -- Atto 1 chiuso post Day-5 successo |
| ~~2026-04-30~~ | H4 cost snapshot fine-mese | codemasterdd | DONE -- gia' fatto mid-sprint 24/04 |
| ~~2026-05-07~~ | Fase 6 closure (anticipata vs sett.4 originale) | codemasterdd | DONE -- ADR-0015 + ADR-0017 Accepted |
| ~~2026-05-08~~ | Governance refresh (drift fix STATUS + COMPACT v12) | codemasterdd | DONE -- branch governance-refresh-2026-05-08 |
| ~~2026-05-12~~ | Cross-repo triage chat-only + STATUS drift fix major (Game 200 PR 14d + Godot-v2 +32 + Dafne stable + vault HEAD update) | codemasterdd | DONE -- PR #53 |
| ~~2026-05-12~~ | ADR-0024 addendum "Sub-events timeline" + scope disjoint clarification (Game OD-023 cross-repo) | codemasterdd | DONE -- PR #55 |
| ~~2026-05-12~~ | TKT-P2 Brigandine Phase D cross-stack chain COMPLETE (Godot PR #248 Main wire + PR #249 Phone organization mode) + Game pull Path A reset (post Protocol 1+2 investigation) | Game-Godot-v2 + Game | DONE -- questa session |
| ~~2026-05-20~~ | **D-sequence closure** (browser-agentic-loop OD-051+OD-052+OD-053 -> 9 PR merged; 5 L-DRAFT-A..E promossi vault L-2026-05-034..038 PR #139; Anti-Pattern Catalogue #10-#13 PR #140; canonical CLAUDE.md propagated Ryzen, Lenovo PENDING) | vault + codemasterdd | DONE 2026-05-20. Dettaglio: `docs/handoffs/2026-05-19-continuity-handoff.md` §LESSONS-PROMOTED 2026-05-20 |
| ~~2026-05-20/21~~ | **Harsh-review + narrow-pick** (HSGF F-FULL fusion design proposed -> harsh-reviewer RETHINK-FUNDAMENTAL verdict -> pivot Protocol 7 narrow-adoption. Shipped: vault #141 supermemory canonical fix + vault #142 PC identity mechanism + codemasterdd #193 parallel-session collision resolve + codemasterdd #194 sdmg-gate narrow-pick. ~$0.40 harsh-reviewer cost saved ~127h F-FULL waste) | vault + codemasterdd | DONE 2026-05-21. Dettaglio: `docs/handoffs/2026-05-20-evening-harsh-narrow-pick.md` |

---

## 2026-05-19 evening + 2026-05-20 EVENING UPDATE — multi-session orchestration

> Tight delta summary. Per-row refresh sopra (rows 1-N) = follow-up se serve.
> Full context: `docs/handoffs/2026-05-19-continuity-handoff.md` §EVENING UPDATE.

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
- Mutex via `docs/handoffs/2026-05-19-continuity-handoff.md` append-only stamps ("OWNING X branch Y") — used by parallel-coop session
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
- D-sequence pattern reusable: anti-creep gate + harsh-review per phase + autoresearch for blocking Q's. Document as `docs/reference/patterns/multi-phase-d-sequence.md` if applied again.

### Status post-D-sequence cross-repo (open PR snapshot 13:00)

- codemasterdd: 0 open PR (clean)
- Game: 0 open PR
- Game-Database: 2 open (Jules #118 docs spec, #122 feat audit) + issue #123 just opened
- Game-Godot-v2: 1 open (#314 feat cronaca TKT-P4)
- vault: 1 open (#133 coherence-backstop from another session)

Coordinator-lane: clean. Parallel-session work distinct branch-names, no collision detected per monitor iter-4.

---

## Ecosystem audit 2026-05-22 -- git-verified (repo-health-auditor, Ryzen session)

Session context: DESKTOP-T77TMKT / VGit, Ryzen. All services (Ollama/Flask/LiteLLM/Langfuse/dogfood-ui) DOWN from this machine -- they are Lenovo-side, expected. Audit source: direct git -C per-repo + gh pr list.

| Repo | Branch | HEAD | ahead/behind | Working tree | Open PRs | Last commit | Drift vs prior |
|------|--------|------|--------------|--------------|----------|-------------|----------------|
| codemasterdd-ai-station | main | `59ccb98` | 0/0 | clean | 0 | 2026-05-21 | None -- governance hub nominal |
| evo-swarm | main | `4c37100` | 0/0 | clean | 1 (#116 OPEN) | 2026-05-22 | **PR #116 new** (Option A born-ready) + 61 remote branches deleted |
| Game (Vue3) | feat/m1-sistema-memory-debrief-surface | `04f78342` | 3 ahead | clean | 0 | 2026-05-22 | Branch advanced; 3 ahead-main not yet PR'd |
| Game-Godot-v2 | claude/handoff-2026-05-22 | `3fcdc7f6` | 2 ahead | clean | 0 | 2026-05-22 | Handoff branch 2-ahead (CAMP-3c design staged) |
| Game-Database | main | `223fe05` | 0/0 | clean | 0 | 2026-05-22 | Phase B2 schema versioning landed; clean |
| vault (Ryzen) | main | `dcc7a167` | 4 ahead | untracked .claude/ | 2 (#163 OPEN, #164 DRAFT) | 2026-05-21 | 4 commits not pushed; PRs need Eduardo triage |
| vault-shared | N/A | N/A | N/A | absent on Ryzen | -- | -- | Path C:/dev/vault-shared does not exist Ryzen-side (Lenovo clone only, expected) |
| synesthesia | main | `05f8a92` | 0/0 | clean | 0 | 2026-04-16 | Dormant confirmed, no change since April |

### Needs-attention (2026-05-22)

1. **evo-swarm PR #116** -- `dafne/option-a-born-ready`: Option A born-ready artifact enrichment. Behavior-critical, left open by design. Eduardo merge required. Branch is remote-published, only active remote branch besides main (post-cleanup).
2. **Game (Vue3) 3 commits ahead main** -- branch `feat/m1-sistema-memory-debrief-surface` not PR'd yet. Commits: M1 sistema-memory chip (Gate-5 surface) + docs. PR or integrate when M1 milestone closes.
3. **vault 4 ahead + PRs #163/#164** -- #163 OD-056 ratify is OPEN (non-draft), Eduardo review/merge. #164 coherence-backstop is DRAFT. 4 local commits not yet pushed to remote.
4. **Game-Godot-v2 2 ahead** -- handoff doc + CAMP-3c design on staging branch. Likely intentional (Eduardo-driven next session). No blocker, low urgency.
5. **evo-swarm local branches** -- 13 local-only branches (dafne/portability-*, mid-*, claude/goals-section, fix/*) not on remote. Normal feature staging but worth pruning after Option A decision.

### Services (Lenovo-side -- not checkable from Ryzen)
All :11434/:5000/:4000/:3000/:8080 returned 000 (connection refused). Expected: this session runs on Ryzen. Verify Lenovo-side when needed.
