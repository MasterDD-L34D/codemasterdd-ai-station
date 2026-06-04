# codemasterdd-ai-station -- first-principles audit (2026-05-28)

> **Method**: `FIRST_PRINCIPLES_INFRA_CHECKLIST.md` (root, prodotto stesso giorno chiudendo OD-005). Dogfood-su-se-stesso post 4-hardening + cross-fleet deploy + governance cleanup. Run rapido sezioni 1/3/4/7/8/9/10 (saltati 2/5/6 less-applicabili a infra meta-audit).
> **Trigger**: Eduardo "punto A repo-wide first-principles pass". Punto naturale post accretion sostanziale 2026-05-28 (~25 commit + 3 PR Game + nuovo deploy system 3-layer + privacy guard + mirror task).
> **Scope**: codemasterdd-ai-station inventory + categorize (core / supporto / opzionale / cerimoniale) + actionable cut list. NON esegue cuts (audit-only, Eduardo decide).

## 1. Verita fondamentali (repo invarianti, non slogan)

1. **"Build on existing work, never recreate"** (Ibrahim 2026 + Microsoft Multi-Agent Ref Arch + ARCHON D-007). Cardine deployato 2026-05-28 sera come L3 directive STRONG-PURE -> ogni session futura riceve l'istruzione.
2. **"Decisioni architetturali = ADR; operative = DECISIONS_LOG Decisione NNN; ambigue = OPEN_DECISIONS"**. Schema ibrido ratificato empirico (10 Decisioni + 34 ADR + 8 OD coesistono pulite -- vedi OD-004 closure).
3. **"Cross-PC reproducibility via canonical-in-codemasterdd + deploy-script-on-target"**. Canonical sta in git; deploy in `~/.claude/` o equivalente; pull+script su entrambi PC produce stato identico (testato live agent-scanner deploy 2026-05-28: skill discoverable in skill-list immediato post-Apply).

Verifica assiomi: tutti e 3 hanno evidenza empirica recente (questa sessione stessa per verita 1 + 3; OD-004 closure per verita 2).

## 2. Triade fondamentale del repo

- **mission**: dev workstation AI agentic principale Eduardo (Lenovo CodeMasterDD) + governance infra-as-code per fleet 2-PC (Lenovo+Ryzen). NON contiene codice progetti reali (Game/Synesthesia/Dafne separate repos).
- **scope**: tooling (wrapper aider/opencode 6+ wrapper) + governance (ADR/CLAUDE.md/DECISIONS_LOG/OPEN_DECISIONS/BACKLOG) + observability (stack ADR-0017 LiteLLM+Langfuse, currently DOWN) + cross-repo coordination (STATUS_MULTI_REPO + memory) + sub-agent quality (.claude/agents 21 sub-agent + meta) + skill+directive cross-fleet (.claude/global-skills/ + global-claude-md-fragments/, 2026-05-28 sera nuovo).
- **constraint dominante** (post-pivot 2026-05-18): **sovereign-first philosophy invariata + ~Hybrid A1 ratificato ADR-0030** ($240-600/anno target, Pro $20/mo + Meridian + OpenCode + Gemini-CLI-free + OpenRouter-overflow). NO zero-subscription-absolute (numero $0-50 morto).

Punti deboli rilevati:
- Triade scope **rischio bloat**: 6+ sub-system (tooling / governance / observability stack / cross-repo / sub-agents / cross-fleet skill+directive) crescono indipendentemente. Sez 8 sotto identifica candidati congelamento.
- constraint dominante post-pivot lascia ambigua la **necessita' LiteLLM+Langfuse stack** (ADR-0017 strategic-tier-emerged pre-pivot; Hybrid A1 routing primario Pro+Meridian, non LiteLLM proxy).

## 3. Inventory + Test di cancellazione (per categoria)

### 3.1 Root governance files (20)

| File | Categoria | "Se lo tolgo cosa si rompe?" | Azione |
|------|-----------|------------------------------|--------|
| `CLAUDE.md` (387 righe, ~daily edit) | **core** | autorita' progetto-specifica + ordine lettura session. Senza: ogni session perde context. | TIENI |
| `PROJECT_BRIEF.md` (last 2026-04-23) | supporto utile | scope+mission statement. Eduardo non lo rilegge spesso. Senza: drift mission risk basso. | TIENI (low-cost) |
| `COMPACT_CONTEXT.md` (2026-05-16) | core | snapshot stato corrente per nuova session. Senza: ogni session ricomincia da CLAUDE.md only. | TIENI |
| `DECISIONS_LOG.md` (2026-05-28) | **core** | ADR index + Decisione NNN operative. Senza: tracciabilita' decisioni persa. | TIENI |
| `OPEN_DECISIONS.md` (2026-05-28) | **core** | decisioni aperte/ambigue. Senza: dimentichi cosa pende. | TIENI |
| `BACKLOG.md` (2026-05-28) | core | task pending + Sprint scope. Senza: drift task. | TIENI |
| `STATUS_MULTI_REPO.md` (2026-05-28) | **core** | dashboard cross-repo. Senza: stato fleet opaco. | TIENI |
| `GOALS.md` (2026-05-22) | supporto utile | direzione S/M/L. Senza: ogni decisione missing-anchor. | TIENI |
| `JOURNAL.md` (2026-05-28) | **core** | session log + storia. Senza: archeologia decisioni rotta. | TIENI |
| `MODEL_ROUTING.md` (2026-05-22) | core | matrice routing. Senza: ogni delega ridiscute setup. | TIENI |
| `ROADMAP.md` (2026-05-08) | supporto utile | timeline strategica. Lettura sparsa. Senza: drift roadmap latent. | TIENI |
| `SPRINT_02.md` (2026-05-13) | core (in-flight) | sprint corrente. Senza: scope sprint perso. | TIENI |
| `SPRINT_01.md` (2026-04-24, CLOSED) | cerimoniale | sprint chiuso. Storia. | **CONGELA**: move to `docs/sprints/_closed/` |
| `MASTER_PROMPT.md` (2026-05-07) | opzionale | meta-prompt orchestrator. Quanto usato? | TIENI (low-cost reference) |
| `PROMPT_LIBRARY.md` (2026-05-15) | opzionale | template prompt. Quanto usato? | TIENI (low-cost reference) |
| `REFERENCE_INDEX.md` (2026-05-16) | core | mappa risorse esterne. Senza: discovery loss. | TIENI |
| `FIRST_PRINCIPLES_INFRA_CHECKLIST.md` (2026-05-28, nuovo) | supporto utile | questo audit la usa. Senza: questo audit non esiste. | TIENI |
| `AGENTS.md` (2026-05-07) | core multi-client | entry-point per Codex/altri client. ADR-0021. | TIENI |
| `README.md` (2026-05-15) | core | repo entry-point esterno. | TIENI |
| `final-research-and-snippets-2026-04-21-v3.md` (root, untracked age) | **cerimoniale** | source material esterno gia' triato. BACKLOG dead-weight (line 157). Senza: nulla rompe. | **TAGLIA** o move a `docs/archive/` |

**Findings root**: 1 taglio sicuro (`final-research-...v3.md` dead-weight) + 1 congelamento (`SPRINT_01.md` move to closed subdir). 18 file restanti core/supporto.

### 3.2 ADR (34 file)

Tracciati 4 SUPERSEDED esplicito (0001 / 0015 / 0023 / 0032).

| ADR | Stato | Azione |
|-----|-------|--------|
| 0001 sovereign AI strategy | SUPERSEDED-by-0030 (Hybrid A1) | **CONGELA** in `docs/adr/_superseded/` |
| 0006 cline-qwen-viability | Frozen post-cline-drop | **CONGELA** in `docs/adr/_superseded/` |
| 0015 fase7-budget full-sovereign | SUPERSEDED-by-0030 | **CONGELA** |
| 0023 strategic-tier post-Max API on-demand | SUPERSEDED-by-0030 | **CONGELA** |
| 0032 jules-pr-governance-active-model | SUPERSEDED-by-0033 | **CONGELA** |
| 0002 codemasterdd-naming | Frozen reference | TIENI in main dir (lookup ancora) |
| Altri ADR 0003-0034 Accepted/Proposed | core/supporto | TIENI |

**Findings ADR**: 5 candidati `_superseded/` subdir (riduce visible 34 → 29). Lookup intentionale via `git log` o esplicito `grep -r SUPERSEDED docs/adr/`. Non perdita storia.

### 3.3 Sub-agents (.claude/agents/, 21 + 4 meta = 25 file)

Last-touch signal (most 2026-04-24 batch creation, mai modificati = mai usati o stabili):

**CORE high-fire-rate** (used N volte questa sessione + multi-week pattern):
- `harsh-reviewer` ✅ used multiple times (3-4 dispatch session 2026-05-28).
- `sot-drift-verifier` ✅ used 2026-05-28 (primo uso reale NO-DRIFT epigenome verdict).
- `delegation-classifier` ✅ + `repo-health-auditor` ✅ + `compact-conversation` ✅ + `harsh-reviewer` ✅ (used in cluster Apr/May).

**Supporto utile** (specialist trigger-on-demand, basso fire rate ma utili quando emerge):
- `owasp-security-auditor`, `privacy-policy-enforcer`, `adr-drafter`, `bench-reporter`, `cost-monitor`, `dogfood-analyst`, `repo-health-auditor`, `swarm-cycle-analyzer`.

**Game cluster** (Evo-Tactics specialist):
- `game-balance-auditor` ✅ (used Apr/May n=2), `jules-pr-triager` ✅ (Jules cluster maggio), `godot-engine-specialist` (low fire), `game-systems-designer` 🟡 draft (no smoke), `game-design-validator` 🟡 draft, `lore-consistency-checker` 🟡 draft.

**Dormant / never-fired (5+ settimane, frozen 2026-04-24)**:
- `a11y-wcag-reviewer` 🟡 draft — Synesthesia dormant fino UniUPO; no fire previsto.
- `database-schema-designer` 🟡 draft — rare specialty.
- `dafne-proposal-triager` 🟡 draft — Dafne swarm Eduardo-mediated, by-pass naturale.
- `lore-consistency-checker` 🟡 draft — Game lore Eduardo-direct, dormant.
- `game-design-validator` 🟡 draft — first-principles delegabile a skill `superpowers:first-principles-game` o questo audit stesso.

**Azione**: i 5 draft never-fired potrebbero congelati in `.claude/agents/_dormant/`. Recovery semplice (rename). Riduce visible 21 sub-agent → 16. CANDIDATE NON URGENT.

### 3.4 Scripts (~30 file)

**Core daily**:
- `hooks/*` (commit-guard, journal-drift-check, session-start-marker, tddguard-seed) → cardine.
- `wrappers/*` (aider-cosmetic / aider-refactor / aider-groq-bypass / aider-cerebras / aider-gemini / aider-openai installati via install-wrappers.ps1) → daily delegation routing.
- `setup/deploy-global-skills.ps1` (nuovo 2026-05-28) + `setup/install-privacy-guard.ps1` + `setup/install-wrappers.ps1` → setup-reproducible.
- `backup/mirror-repos.ps1` + `backup/copy-mirror-to-external.ps1` (nuovo 2026-05-28) + `backup-api-keys.ps1` → backup chain.

**One-time setup scripts** (executed once during initial PC bootstrap):
- `bitlocker-hard-disable.ps1` (eseguito 2026-04-19).
- `disconnect-onedrive.ps1` (eseguito 2026-04-19).
- `godot-install-ryzen.ps1` (one-time per PC).

**Azione**: move questi 3 a `scripts/_one-time/` con README "executed once, kept for reference / re-run su nuovo PC fleet". Riduce visible.

**Bench / quality** (run-when-needed):
- `bench-cloud.ps1`, `bench-ollama.ps1`, `bench-mixed-workload/run-bench.ps1`, `bench-opencode-cloud-free.ps1` → eseguibili ad-hoc per re-bench. Tieni.
- `quality-bench/load-problems.js` + `playwright-monitor-regression.py` + `run-bench.ps1` → stack ADR-0017 promptfoo. Vedi 3.6.

**Cross-repo / Sprint-time**:
- `cross-repo/install-gate-e-reminder.ps1` → Gate E pattern post-Max (Hybrid A1 ridimensiona; valutare). MAYBE archive se Gate E reactivation deferred.
- `cross-repo/coord-event-log.ps1` + `cross-repo/dry-run-pr.ps1` → orchestrator spec V3.

**Migration**:
- `migrate-log-to-sqlite.py` → eseguito una volta (post Fase 6). Move a `_one-time/`.

### 3.5 Docs (84+ file in subdir)

- `docs/research/` (24): rolling audit. Alcuni post-decisione stale. Manual archive opzionale.
- `docs/runbook/` (8): operative current. KEEP.
- `docs/handoffs/` (10): handoff storici frozen. KEEP read-only.
- `docs/superpowers/specs+plans/` (16): brainstorm artifacts recent. KEEP.
- `docs/reference/patterns/` (7): operational patterns. KEEP.
- `docs/superpowers/tests/` (9): smoke logs per ADR-0018. KEEP.
- `docs/archive/ryzen-memory-archive/` (10): preservato 2026-05-27 (139 file memory Ryzen). KEEP (knowledge irrecoverable altrove).

**Findings**: 84+ doc surface alta, ma ognuna ha provenance + purpose chiari. NO cuts raccomandati a parte forse review research/ stale (richiede file-by-file pass, deferrabile).

### 3.6 Stack ADR-0017 (LiteLLM + Langfuse + Postgres + dogfood-ui)

Ground-truth 2026-05-28: **docker daemon NOT running** -> stack containers DOWN. Per ADR-0017 stack e' "opt-in hot-restart" + ADR-0030 Hybrid A1 routing primario = Pro+Meridian+OpenCode+Gemini-CLI, NON LiteLLM proxy.

**Test di cancellazione**: se NON tengo lo stack:
- dogfood-ui (Flask) → unused se docker down. Cosa traccia? Per-task entries che vivono ANCHE in `logs/aider-delegation-*.md` (markdown source-of-truth gia' richiamato). Redundant?
- LiteLLM proxy → routing centralizzato verso provider. MA Hybrid A1 routing post-pivot = Pro (Meridian via opencode-with-claude), Gemini-CLI direct, Cerebras/Groq via wrapper aider-* (NON via LiteLLM). LiteLLM rimasto rilevante per: virtual key budget enforcement promptfoo eval (`U3-test` $5 budget 30d). Marginal value attuale.
- Langfuse → osservabilita' traces LiteLLM. Se LiteLLM marginale, Langfuse anch'esso.
- Postgres → backing per Langfuse + LiteLLM. Se sopra marginale, idem.

**Verdetto provvisorio**: stack ADR-0017 e' **cerimoniale al 70-80% post-pivot ADR-0030**. ADR-0017 Accepted 2026-05-07 (pre-pivot ADR-0030). Valutare con metodo specifico (potrebbe diventare separato OD-009 "stack ADR-0017 post-Hybrid-A1 review").

**Azione**: NON cuts ora (decisione ADR-class). RAISE come OPEN_DECISIONS o ADR-0017 amendment "stack opt-in marginale post-ADR-0030, mantain hot-restart capability ma deemphasize default observability path".

### 3.7 Archivio_Libreria_Operativa_Progetti (7 sub-dirs framework)

Used as reference library. Templates (FIRST_PRINCIPLES_GAME_CHECKLIST = source per INFRA-CHECKLIST appena prodotta; OPEN_DECISIONS.template; CHANGE_BUDGET; TASK_EXECUTION_PROTOCOL; ecc).

**Test cancellazione**: senza Archivio, perdo:
- Template per future progetti (multi-progetto framework imported 2026-04-23).
- Master orchestrator prompt + safe-changes rules + repo-autonomy-readiness checklist.

**Verdetto**: TIENI (reference library, low daily-cost, alto valore se Eduardo apre nuovo repo).

## 7. Rational Design (comportamento desiderato vs attuale)

**Desiderato**:
- Session-start = <=3 doc letti (CLAUDE.md + COMPACT_CONTEXT.md + STATUS_MULTI_REPO.md) per orientarsi rapidamente.
- Delega task = identifico tier (cosmetic/behavior/strategic + constraint-count) -> wrapper aider giusto -> commit con trailer ADR-0011.
- Decisione architectural = ADR draft via `adr-drafter` agent + harsh-reviewer + Eduardo Accept.
- Cross-fleet feature = canonical in codemasterdd + deploy script -> entrambi PC stato identico.

**Attuale problematico**:
- 84+ docs in `docs/` subdir + 34 ADR + 20 root MD + 21 sub-agent + 30 script = **surface alta** per chi rilegge dopo 6 mesi. Discovery non-banale.
- Stack ADR-0017 cerimoniale post-pivot (down, marginal value, ma scaffold + ADR-0017 Accepted lo rendono "permanente" in lettura).
- 5 sub-agent draft never-fired in 5 settimane = surface accumulata.
- 5 ADR SUPERSEDED in cima alla lista = lookup confusion latente (mitigato da SUPERSEDED marker ma cost).

## 9. Decisione finale (strategia post-audit)

**NON refactor profondo**. Repo e' funzionale + ben-strutturato. Cerimony candidates sono il 5-10% del totale, non il 30%+.

**Strategia consigliata**: **freeze-in-place via subdir conventions**, NON delete. Operazioni:

1. **Move 5 ADR SUPERSEDED -> `docs/adr/_superseded/`**. Cross-link da indice. Lookup via `grep -r SUPERSEDED docs/adr/`.
2. **Move `SPRINT_01.md` -> `docs/sprints/_closed/SPRINT_01.md`**. Reference link da `BACKLOG.md`.
3. **Delete o archive `final-research-and-snippets-2026-04-21-v3.md`** (dead-weight per BACKLOG line 157).
4. **Move 3 one-time scripts -> `scripts/_one-time/`** (bitlocker-hard-disable, disconnect-onedrive, godot-install-ryzen, migrate-log-to-sqlite). README spiega "executed once per PC, retained for new-PC bootstrap re-use".
5. **OPEN OD-009 "Stack ADR-0017 post-Hybrid-A1 review"** -- evaluate se LiteLLM+Langfuse stack ha valore attuale o e' cerimony 70-80%. Tradeoff: hot-restart capability vs disk/memory residual + ADR-0017 status semantica.
6. **Considerare** (NON urgent): move 5 sub-agent draft never-fired -> `.claude/agents/_dormant/`. Trigger reactivation: 1° fire del tipo. Riduce visible 21 -> 16.

**Primo step a piu alto leverage e rischio controllato** = (1) ADR SUPERSEDED move (5 file rename, 5min, zero rischio funzionale, riduce confusion lookup).

**NON toccare**:
- ADR Accepted vivi (governance livelina).
- Sub-agent ready (12/21 con smoke validato per ADR-0018).
- Stack ADR-0017 codice/config (decisione amount via OD-009 separata).
- Archivio framework (reference low-cost).

## 10. Gate finale

- [x] So cosa deve fare davvero il repo (mission: dev workstation AI + governance infra-as-code fleet).
- [x] So cosa deve fare davvero il workflow operativo (delega tier-based + ADR governance + cross-fleet reproducibility).
- [x] So cosa deve fare davvero la triade (mission + scope multi-system + constraint Hybrid A1 sovereign-philosophy).
- [x] Sto valutando per migliorare experience operativa / discovery / lookup -- NON eleganza estetica.
- [x] Il primo step e' leggibile (ADR SUPERSEDED move = 5min) + motivato (riduce confusion lookup, zero rischio).

**Tutti 5 ✅ -> proceed**.

## Reference

- Checklist source: `FIRST_PRINCIPLES_INFRA_CHECKLIST.md` (root, prodotta 2026-05-28 chiudendo OD-005).
- Pattern coerente con OD-007 first-principles application: `docs/research/2026-05-28-od-007-first-principles-application.md`.
- ADR pivot ADR-0030 Hybrid A1 Accepted 2026-05-18 = chiave per "post-pivot" reading di ADR-0017 stack.
- BACKLOG dead-weight section (line 153-160) = lista pre-esistente di candidates frozen.
