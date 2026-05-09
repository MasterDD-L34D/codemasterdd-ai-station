# Harsh review — Flow chart operativo CodeMasterDD AI Station

**Data**: 2026-05-09 mattino
**Reviewer**: harsh-reviewer agent + analisi complementare Claude Code session
**Trigger**: Eduardo ha richiesto analisi affondo del flow chart per identificare vulnerabilità, choke points, errori, inesattezze
**Scope**: flow chart 7-section che descrive workflow operativo "se tutti i piani vengono seguiti"
**Output**: report harsh + 6 scelte strategiche presi da Eduardo + 6 task derivate per BACKLOG

## Verdetto top-level

> **REWORK richiesto pre-19/05**. 2 buchi BLOCKING + 1 SIGNIFICANT empirico. Non ship as-is. Costo fix stimato 3-4 giornate, fattibile in transition window 10gg residui.

---

## Vulnerabilità BLOCKING (2)

### V1. Tier 0 strategic post-19/05 e' un buco nero non risolto

**Citation**: ADR-0008 dichiara strategic NON delegabile. Sezione 2 step 4 del flow: "5+ strict constraint -> ritorno a Claude direct (cloud 70B degrada 20%)". Ma:

- Post-19/05: Claude Max scaduto, Pro NON acquisito, "API key occasional" mai formalizzata in ADR
- Multi-file refactor / debug strategico: chi lo fa? OpenCode 30B su multi-file NON validato (n=2 dogfood single-file)
- ADR-0015 Scenario A dichiara "full-sovereign" ma NON copre strategic tier -- e' wishful thinking gap

**Severity**: blocca operativita' post-19/05. Window 10gg per fixare.

**Risoluzione (Eduardo 9/5)**: **Scelta 1A** -- Claude API on-demand con budget cap mensile $10-20/mese, tracciato in ccusage. Quando emerge task strategic complesso, autorizzo spend per quella sessione e poi torno a sovereign. Trigger ADR-0023.

### V2. Privacy boundary cloud bypass-friendly

**Citation**: CLAUDE.md "verificare caso-per-caso" per Synesthesia/Game/clienti. Problemi:

- Classificazione manuale per-task. **Zero guard rail tecnico**.
- `aider-groq` su `Synesthesia/controllers/auth.js` non viene bloccato da niente -- solo memoria Eduardo o Claude in-session
- Repo cliente whitelist: NON esiste. Pattern "verificare caso-per-caso" = drift inevitabile
- Pre-commit hook blocca silent-corruption + bare except, **NON blocca** "questo file editato da provider cloud"
- Audit retroattivo: `logs/aider-delegation` gitignored + manualmente aggiornato

**Severity**: 1 leak = ADR-0001 sovereign principle violato. Reputational/contractual se repo cliente.

**Risoluzione (Eduardo 9/5)**: **Scelta 2A** -- Wrapper enforcement automatico. Gli script `aider-groq`/`-cerebras`/`-gemini`/`-openai` controllano repo + leggono whitelist + abort se non zona OK. Tooling fa il guardiano. Task BACKLOG H8.

---

## Vulnerabilita' SIGNIFICANT (3)

### V3. Sample size empirici sotto threshold per claim "Accepted"

- **ADR-0022** Accepted con n=3 OpenCode PASS. n=3 e' statisticamente nullo
- **Fase 6 closure** n=15 dogfood "0 corruption": survival bias enorme (task selezionati da Eduardo in working tree controllato != varianza reale 6+ mesi)
- **Fail rate 8.3% cumulativo**: denominator? Smoke read-only contano? Tooling-bug noti esclusi ma threshold flessibile
- **ADR-0021** Accepted dopo "conferma uso reale Game-Godot-v2 governance autosufficiente" -- n=1 ricognizione passiva

**Pattern**: ADR Accepted troppo presto. Risk: future contraddizioni -> cascade Superseded.

**Risoluzione (Eduardo 9/5)**: **Scelta 3B** -- Tieni n=3-5 ma flag "early-acceptance" sullo status. ADR-0022 diventa "Accepted (early, n=3, ratification check fra 30gg)". Trasparente e revisionabile. Task BACKLOG H10 (status workflow update).

### V4. Single-point-of-failure non mitigati

- **Ollama daemon down** (Windows update / driver / CUDA): tier 1-2 offline, cloud free OK ma privacy gate blocca repo sensibili. **Synesthesia controllers offline = stop work**
- **`~/.config/api-keys/keys.env`** corrotto/cancellato: aider cloud + opencode cloud entrambi giu'. Backup `backup/api-keys-2026-04-22.env` e' di **17 giorni fa**. Stale se chiavi rotate
- **Hook globale corrotto silenzioso**: regex Conventional Commits troppo permissiva = junk accettato cross-repo. Detection retroattiva non documentata
- **LiteLLM/Langfuse stack**: opt-in. Se dogfood active mode + Postgres problemi = tracking perso. Recovery procedure?

**Risoluzione**: deferred SPRINT_02 T7 review (ADR addendum reactive se trigger emerge). Mitigation parziale: bench mixed-workload (4A) cattura swap overhead Ollama; rotazione keys backup automation deferred.

### V5. Trust boundary inconsistency interno vs esterno

- External repo (Game/Godot/Dafne/AA01): auth esplicita Eduardo per merge/close ✅
- **Interno codemasterdd**: Claude Edit/Write/commit/push autonomo (SAFE_CHANGES limits)
- **Inconsistency**: codemasterdd e' policy hub. Edit qui (CLAUDE.md routing matrix, `scripts/hooks/`) ha effetto cross-repo via hook globali. Commit autonomo Claude codemasterdd puo' alterare comportamento commit Game/Godot. **Write esterno indirect mascherato da interno**.

**Risoluzione**: deferred. Pattern da emergere prima di formalizzare. Monitoring opportunistic: in next session, segnalare a Eduardo se task tocca CLAUDE.md "Convenzioni operative" / `scripts/hooks/` / MODEL_ROUTING -> conferma esplicita richiesta.

---

## Choke points QUANTIFICATI

### C1. RTX 5060 8GB VRAM -- sustainability under continuous workflow

- 30B MoE 23.3 tok/s @ ctx 8192. Sessione agentic OpenCode 5-10 round-trip = 2-5 min/task. **30 task/giorno = 1-2.5h solo inference**
- `OLLAMA_MAX_LOADED_MODELS=1`: swap continuo se workflow alterna 7B/14B/30B. Ogni swap ~10-20s. **20 task misti = 5-10min swap overhead**
- **Throughput effettivo MAI benchmarked in mixed-workload realistic**

**Risoluzione (Eduardo 9/5)**: **Scelta 4A** -- 1 giornata bench mixed-workload pre-19/05. Task BACKLOG H9.

### C2. Cognitive overhead decision tree -- ~24 path

- 6 tier x privacy x constraint = decision per ogni Edit/Write
- 22 ADR da tenere in testa anche solo come "esiste, devo verificare"
- **14 caveat/exception nel CLAUDE.md decision matrix**
- Decision fatigue reale, dimenticanze inevitabili

**Risoluzione**: deferred. Tooling `task-classify <file>` candidate post-bench (4A insight).

### C3. JOURNAL/COMPACT/memory drift inevitable

- "Sessione significativa" trigger soft. Claude Code stop senza prompt automatico
- 18 memory file. Refresh manuale = drift cumulativo
- **Stima miss-rate 30-40% in 10gg high-intensity**

**Risoluzione (Eduardo 9/5)**: **Scelta 6A** -- Stop hook automatico. Task BACKLOG H12.

### C4. Bus factor 1 (mia aggiunta)

- Tutto context vive in (a) memory files (b) repo docs (c) **head di Eduardo**
- Eduardo malato 2 settimane -> ricostruzione stato senza human in the loop?
- 5 progetti monitorati ma 1 solo manutentore

**Risoluzione**: parziale via memory consolidation 9/5 + project_session_resumption refresh con paste-ready opener. Bus factor structural.

---

## Errori logici / Inesattezze

| # | Claim | Realta' |
|---|-------|---------|
| E1 | "5 progetti monitorati" | 1 hub + 1 paused + 1 dormant + 2 read-only governance autosufficiente. Effective monitoring = 2 |
| E2 | ADR Accepted con n=3 | Status workflow violato. Risolto da Scelta 3B (early-acceptance flag) |
| E3 | "Cloud free 70B sempre rate-limited per OpenCode" | Universal claim su default request 50k. Per task piccoli (<5k) Groq 70B funzionerebbe. Tier perso senza indagine |
| E4 | Synesthesia criterio #3 "deroga ADR-0015" | NON documentato in ADR-0015. Vive solo in memory file. Debt non tracked formalmente |
| E5 | Token-rate cherry-picking | Tutti @ ctx 8192/16384. Workflow agentic reali 32k+. Numbers non scalano linearmente. Decision matrix usa numeri ottimisti |

**Risoluzione**: E1 e' nominale (accettato), E2 risolto, E3+E5 risolti da bench (4A), E4 da formalizzare in ADR-0015 addendum (deferred SPRINT_02 T6 privacy preview).

---

## Edge cases prioritizzati

| Priority | Scenario | Impact | Risoluzione |
|----------|----------|--------|-------------|
| **HIGH** | Eduardo offline + Ollama daemon down | Stop totale | Deferred reactive (no fallback documented) |
| **HIGH** | Game pivot Vue3->Godot definitivo pre-settembre | Monitoring/hook/pipeline cambia | **Scelta 5A**: ADR-0024 soft-deadline 2026-09-30 + AA01 attivazione su Ondata 1+2 (Eduardo direct action) |
| **HIGH** | AA01 silent driver "muore" | NON git-tracked, recovery? | Deferred reactive (Eduardo standalone) |
| **MED** | Qwen3-Coder-Next rilascia DURANTE 9-19/05 | Conflitto priorita' OpenCode validation | Deferred reactive (trigger ADR-0009 T1) |
| **MED** | Hook globale corrotto silenzioso | Detection settimanale non documentata | Deferred SPRINT_02 (smoke test settimanale candidate) |
| **MED** | Game-Godot-v2 governance autosufficiente diverge | Codemasterdd assumption | Monitoring passivo |
| **LOW** | Synesthesia riattiva pre-agosto | Privacy validation on-demand | Deferred reactive |

---

## Process smells (mia aggiunta)

1. **"Lean honest execution"** memory documentata MA self-policing rule, non trigger empirico
2. **BACKLOG vs SPRINT_02 source-of-truth**: drift se update uno e non l'altro
3. **Pace alta sostenibile?** 10 PR mergeati 8/5 + 5+ PR 9/5 mattino. Test resilienza non fatto
4. **Manual cleanup branch locali**: 9 branch stale eliminati 9/5 -- pattern ricorrente, automate?
5. **Auto Mode + sandbox guard**: blocchi context-dipendenti, workaround per-volta

**Risoluzione**: deferred opportunistic. Smell 4 candidate post-19/05 hook.

---

## Cose che funzionano (no flattery, evidence)

- ADR practice solid: 22 ADR formalizzati, status workflow, addendum tracking. Best-in-class solo-dev
- Hook chain layered (commit-msg + pre-commit Layer 1+2 + Claude Code PreToolUse) robust per silent-corruption
- Wrapper CLI Aider buona astrazione: complexity buried, surface API semplice
- Multi-client AGENTS.md pattern intelligente, validated da uso reale Game-Godot-v2
- MEMORY.md index 18 entries organized, NON soup

---

## Decisione 007 -- Risposte 6 questions BLOCKING (Eduardo 2026-05-09)

| Q | Scelta | Action item |
|---|--------|-------------|
| 1 | A -- Claude API on-demand $10-20/mese | ADR-0023 (H7) |
| 2 | A -- Wrapper enforcement automatico | Privacy guard rail (H8) |
| 3 | B -- Early-acceptance flag | Status workflow update (H10) |
| 4 | A -- Bench mixed-workload pre-19/05 | Bench session (H9) |
| 5 | A+ -- Soft-deadline 2026-09-30 + AA01 attivazione Ondata 1+2 | ADR-0024 + AA01 trigger (H11) |
| 6 | A -- Stop hook automatico | settings.json hook (H12) |

---

## 3 Next actions (priority alta)

| # | Action | Effort | Resolve |
|---|--------|--------|---------|
| 1 | **ADR-0023**: Strategic tier post-Max fallback policy. Budget cap mensile API $10-20 + threshold escalation + criteria reactivation Pro condizionale | 2-3h | V1 BLOCKING |
| 2 | **Privacy guard rail tecnico**: wrapper script aider-* runtime check + whitelist `~/.config/aider-privacy-whitelist.txt` | 1gg | V2 BLOCKING |
| 3 | **Bench mixed-workload**: 10-20 task realistici alternati tier 1/2/2.5. Misura swap overhead + throughput effettivo | 1gg con Claude Max ancora attivo | C1 + V3 sample size |

**Costo totale**: 3-4 giornate. Window: 10gg residui. **Fattibile**.

---

## Riferimenti

- ADR-0001 (sovereign strategy) -- vincolo strategico
- ADR-0008 (silent-corruption + tier routing backbone) -- strategic NON delegabile
- ADR-0015 (Fase 7 budget Scenario A) -- da emendare per coprire scenario API on-demand
- ADR-0017 (UI + observability) -- stack scaffold opt-in, possibile attivazione mixed-workload bench
- ADR-0022 (OpenCode tool-use) -- early-acceptance candidate (n=3)
- `feedback_lean_honest_execution.md` -- self-policing rule
- `feedback_external_repo_action_boundary.md` -- inconsistency interno vs esterno trust
- BACKLOG H7-H12 nuovi task derivati
- Decisione 007 in DECISIONS_LOG (questa sessione)
