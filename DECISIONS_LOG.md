# DECISIONS_LOG

> Schema ibrido: il progetto usa ADR MADR come source-of-truth per decisioni strategiche. Questo file è **indice** degli ADR + sezione aggiuntiva per decisioni operative minori (non-ADR).
>
> Coesistenza con template archivio `04_BOOTSTRAP_KIT/DECISIONS_LOG.md` (formato "Decisione NNN"): le decisioni granulari non-ADR seguono quel formato; le strategiche restano in ADR separati (più ricchi, più navigabili).

## ADR index (strategiche)

| # | Topic | Status | Data | Decisione operativa derivata |
|--:|-------|--------|------|------------------------------|
| 0001 | Sovereign AI strategy | Accepted (timeline parzialmente superata da 0014) | 2026-04-20 | Target $0-50/anno; Fasi 1-3 strategiche invariate |
| 0002 | Workstation naming CodeMasterDD | Accepted | 2026-04-19 | Label "Lenovo AI Station" → "CodeMasterDD AI Station" |
| 0003 | Node 24 vs 22 | Accepted | 2026-04-19 | Node 24 LTS vanilla, `nvm-windows` deferred YAGNI |
| 0004 | Ollama RTX 5060 config | Accepted (partial, `num_ctx` superseded da 0012) | 2026-04-20 | FA=1, KV q8_0, MAX_LOADED=1, ctx 8192 default |
| 0005 | YAGNI minimalism approach | Accepted | 2026-04-20 | No pre-config, no abstraction anticipate |
| 0006 | Cline + Qwen 7B viability | Accepted (NOT viable agentic) | 2026-04-20 | Scartato Cline, fallback Aider |
| 0007 | Aider + Qwen quantization | Partially Superseded (whole deprecated by 0008) | 2026-04-20 | 14B Q2_K sweet spot behavior |
| 0008 | Aider whole format silent-corruption | Accepted (hub pattern backbone) | 2026-04-21 | Whole deprecated behavior-critical → tier routing |
| 0009 | Upgrade trigger framework | **Accepted 2026-05-09** (partial T2 materialized by 0012; T1/T3 reference) | 2026-04-21 (P) -> 2026-05-09 (A) | Framework trigger hardware/cloud/client. T2 RAM upgrade DONE. T1 Qwen3-Coder-Next + T3 client alternative continuano come reference. ADR-0022 OpenCode T3-adjacent (coexist, non sostituisce Aider). |
| 0010 | MADR format + skill policy | Accepted | 2026-04-22 | MADR da 0010 in poi; skill install richiede preview + ADR |
| 0011 | Cross-agent commit governance | Accepted (validated) | 2026-04-22 | commit-msg hook globale + wrapper verify |
| 0012 | RAM 64GB upgrade impact | Accepted + Validated | 2026-04-22 | qwen3:30b +31% speed tier 2 stabile |
| 0013 | Tier 3 cloud free providers | Accepted (75 test + OK user) | 2026-04-23 | Groq/Cerebras tier 3 primary; OpenAI/Gemini capability-max |
| 0014 | Fase 6 timeline compression | Accepted (OK user) | 2026-04-23 | 3 mesi → ~4 settimane; chiusura ~20/05 |
| 0015 | Fase 7 budget decision full-sovereign | **Accepted 2026-05-07** | 2026-04-24 (P) -> 2026-05-07 (A) | Opzione A $0-50/anno confermato + deroga criterio #3 (Synesthesia dormant) + soft-override esteso n>=12 |
| 0016 | Constraint-count routing dimension | **Proposed** | 2026-04-24 | 2D matrix classe + constraint-count; 5+ strict → manual Claude Code |
| 0017 | UI + observability stack | **Accepted 2026-05-07** (5/5 criteri PASS) | 2026-04-24 (P) -> 2026-05-07 (A) | LiteLLM Proxy + Langfuse + promptfoo + Aider browser + Flask mini-app, scaffold opt-in post-closure |
| 0018 | Agent readiness protocol (3-gate smoke+research+tuning) | **Accepted** | 2026-04-24 | Ogni agent `draft` fino passaggio gate. 11/18 ready dopo batch P0+P1, 7/18 draft |
| 0019 | Dafne process persistence (3 opzioni A/B/C) | **Accepted** | 2026-04-24 | Opzione A wrapper PS auto-restart (committato Dafne repo `c638098`), B Task Scheduler post-Fase 6, C Docker deferred |
| 0020 | Silent-fail Python guardrail (extension pre-commit) | **Accepted** | 2026-04-25 | Pre-commit hook globale Layer 2: bare `except:` + `except: pass` one-liner blocked. Bypass: `# silent-ok`. PR #1 mergeato. |
| 0021 | Multi-client instruction files (AGENTS.md + Codex anti-confusion) | **Accepted (early, n=1, ratification check 2026-06-07)** | 2026-05-07 | AGENTS.md preamble Codex sandbox-aware + CLAUDE.md autoritativo + encoding ASCII-first nuovi doc. PR #2 mergeato. Trigger: branch `codex/structural-reset` REJECTED per false-premise sandbox-confusion. Status flip Accepted (early) 2026-05-09 via ADR-0010 addendum. |
| 0022 | OpenCode tool-use model routing (tier dedicato vs Aider) | **Accepted (early, n=3, ratification check 2026-06-09)** | 2026-05-08 (P) -> 2026-05-09 (A early) | Tier OpenCode-specifico distinto da Aider tier ADR-0008. Default `ollama/qwen3-coder:30b` MoE A3B (3/3 PASS empirico). NON usare con OpenCode: Qwen 2.5 Coder family (raw JSON tool call) + cloud free 8B-70B (rate-limited TPM/context). PR #15 Proposed + #16 addendum cloud + #19 Accepted + #20 integrazione CLAUDE.md+MODEL_ROUTING. Status flip Accepted (early) 2026-05-09 via ADR-0010 addendum. |
| 0023 | Strategic tier post-Max API on-demand budget cap | **Proposed 2026-05-09** | 2026-05-09 | Claude API pay-per-use $10-20/mese cap. Strategic NON-delegabile (ADR-0008) + Pro NOT acquisito (ADR-0015 Scenario A) -> fallback formalizzato. Trigger reactivation Pro: utilizzo >$20/mese 2 mesi consecutivi. ccusage tracking. Risolve V1 BLOCKING harsh review 9/5. |
| 0024 | Vue3 archive + Godot v2 canonical timeline | **Proposed 2026-05-09** | 2026-05-09 | Soft-deadline archive Vue3 entro 2026-09-30 (4 mesi). Review trimestrale 2026-08-01. Trigger archive: 60gg silenzio commit Vue3 main OR feature parity Godot v2 dichiarata Eduardo. AA01 attivazione esplicita Sprint Impronta Ondata 1+2 (Eduardo direct H11). Risolve edge case HIGH harsh review 9/5. |
| 0025 | Hyperspace Pods privacy assessment (NO-GO empirico) | **Accepted 2026-05-12** (auto-ratified) | 2026-05-11 | NO-GO definitivo: 3 finding architetturali non-config-fixable (auto-update FORCED + Ollama auto-expose + pulse voting). pktmon 120149 pkt/3min TUTTE pubbliche. Pivot: llama.cpp RPC LAN-only. |
| 0026 | Cognitive workflow protocols (6 protocol P1-P6) | **Accepted** | 2026-05-13 | P1 Refresh-verify + P2 Autoresearch + P3 Archon 7-step + P4 AA01 audit trail + P5 harsh-reviewer + P6 brainstorming skill. Combined methodology + anti-aspirational measurement. |
| 0027 | Cross-PC clone architecture Lenovo+Ryzen | **Accepted (early 2026-05-13)** | 2026-05-13 | Fleet 4 PC LAN: Lenovo `.10` agentic hub + Ryzen `.11` inference secondary 4070S 12GB. DHCP reservation permanent TIM HUB. SSH key-based auth. |
| 0028 | Tier promotion quality gate methodology | **Accepted** | 2026-05-13 | 3-gate (smoke->draft->production) per vault agent + wrapper promotion. Anti-aspirational: n>=1 empirical PASS required. |
| 0029 | OpenRouter eval declined sovereign-first BYOK | **Proposed 2026-05-13** | 2026-05-13 | Decline OpenRouter: free tier Groq 70B NON incluso + SPOF cloud + BYOK negate simplification. Mantieni 6-wrapper direct. Trigger reactivation: >$5/mese x2 mesi OR >8 wrapper. |
| 0030 | ChatGPT Business workspace recovery + classification pipeline | **Proposed 2026-05-14** | 2026-05-14 | brianjlacy/export-chatgpt MIT (unico con Projects traversal Business verificato) + BERTopic + nomic-embed-text + Qwen 14B Q2 100% sovereign. Staging vault Sources/raw/, promozione Eduardo-direct. Ratification: bulk export PASS + classify.py smoke PASS. |

### In review (Proposed, awaiting Accepted trigger)
- **ADR-0016** -- Constraint-count routing dimension. Trigger Accepted: n>=3 data points addizionali (constraint=4 explicit LOCAL, 2-transform LOCAL, 5-strict LOCAL). Update 2026-04-24: +1 data point (#12 constraint=4 parity-based, partial). Stato 2026-05-09: dataset Fase 6 closed a n=12 + smoke OpenCode 9 + dogfood OpenCode 2 = ulteriori data points emergeranno organicamente in SPRINT_02 post-Max.

### Accepted 2026-05-09 (transition active sovereign)
- **ADR-0022** -- OpenCode tool-use model routing. Tier dedicato OpenCode distinto da Aider. Validato n=11 entries (9 smoke + 2 dogfood reali #25-#26 PASS 1st-try) con Ollama qwen3-coder:30b MoE A3B come default sovereign. Cloud free non viable (rate-limited). Qwen 2.5 Coder family non tool-use OpenCode-compat.

### Proposed 2026-05-09 (post-harsh-review fixes)
- **ADR-0023** -- Strategic tier post-Max Claude API on-demand budget cap. Risoluzione V1 BLOCKING harsh review (strategic tier post-19/05 buco nero). Budget cap $10-20/mese tracciato ccusage. Trigger reactivation Pro >$20/mese 2 mesi consecutivi.
- **ADR-0024** -- Vue3 Game archive + Godot v2 canonical timeline 2026-09-30. Risoluzione edge case HIGH "Game pivot Vue3->Godot definitivo pre-settembre". Soft-deadline 4 mesi + review trimestrale + trigger 60gg silenzio. AA01 attivazione esplicita Ondata 1+2 (Eduardo direct H11).

### Accepted 2026-05-07 (closure batch Fase 6)
- **ADR-0015** -- Closure anticipata vs target sett.4 originale. Soft-override esteso n>=12 con 5 rationale: trigger ADR-0008 confermato, behavior 5/3 superato, fail rate strict 8.3%, zero silent-corruption, anti-pattern dogfood sintetici.
- **ADR-0017** -- 5/5 criteri ratification PASS (LiteLLM + Langfuse + promptfoo + dogfood-ui + maintenance budget). Stack scaffold opt-in (Docker Desktop manual start), persistence DB preservata, hot-restartable in <60s.

### Note coerenza
- **0007 vs 0008**: 0008 depreca whole solo per behavior-critical; cosmetic+whole resta valido (faithfulness non critica).
- **0001 timeline**: superseded da 0014 sul timing, rationale tecnico invariato.
- **0009 T2**: non formalmente triggerato (upgrade 0012 opportunistic, documentato).

---

## Decisioni non-ADR (operative minori)

Formato granulare per decisioni che non meritano ADR (reversibili, locali, non vision-sensitive).

### Decisione 001 — Adozione schema framework archivio per governance files
- **Data**: 2026-04-23
- **Titolo**: Schema `04_BOOTSTRAP_KIT` adottato per i 7 file governance root-level
- **Decisione presa**: i file `PROJECT_BRIEF`/`COMPACT_CONTEXT`/`DECISIONS_LOG`/`BACKLOG`/`OPEN_DECISIONS` seguono lo schema template archivio. Aggiunti 4 file mancanti (`MASTER_PROMPT`/`REFERENCE_INDEX`/`PROMPT_LIBRARY`/`MODEL_ROUTING`) compilati col contenuto reale del progetto. Skipped `FIRST_PRINCIPLES_GAME_CHECKLIST` (N/A, non è game repo).
- **Perché**: archivio è framework multi-progetto prescrittivo importato 2026-04-23; non adottarlo avrebbe creato drift tra template e realtà. Adozione schema preserva riusabilità cross-progetto.
- **Alternative considerate**:
  - Ignorare archivio, mantenere schema custom dei miei file → rigetto per drift.
  - Riscrittura totale seguendo template vuoti → rigetto per perdita contenuto ricco.
  - Merge ibrido (schema archivio + contenuto progetto) → scelta.
- **Conseguenze**: leggibilità cross-progetto ↑; 30 min lavoro + 11 file aggiornati/creati; zero codice toccato.
- **Azioni derivate**: pointer aggiunti in `CLAUDE.md` e `README.md` all'archivio; memory refresh pending.

### Decisione 002 — `FIRST_PRINCIPLES_GAME_CHECKLIST.md` non applicabile
- **Data**: 2026-04-23
- **Titolo**: Skip `FIRST_PRINCIPLES_GAME_CHECKLIST` per natura del repo
- **Decisione presa**: NON creare file al root. Documentato come N/A qui.
- **Perché**: framework archivio ha bias game-repo (esplicito nel `CLAUDE_CODE_MASTER_ORCHESTRATOR.prompt.md` "a game repository"). Questo repo è **infrastructure-as-code**, non un gioco. Game truths/system truths/round flow → N/A.
- **Alternative considerate**:
  - Creare file vuoto "not applicable" come placeholder → rigetto (cerimonia inutile).
  - Creare versione adattata "First principles infrastructure checklist" → rimandato, nessun trigger.
- **Conseguenze**: zero.
- **Azioni derivate**: nessuna. Se in futuro emerge bisogno analogo → ADR dedicato.

### Decisione 003 — Regole Operating Package 07_ non clonate al root
- **Data**: 2026-04-23
- **Titolo**: Regole 07_CLAUDE_CODE_OPERATING_PACKAGE restano nell'archivio, non duplicate
- **Decisione presa**: NON copio `CLAUDE_OPERATING_RULES.md`, `TASK_EXECUTION_PROTOCOL.md`, `SAFE_CHANGES_ONLY.md`, `CHANGE_BUDGET.md` al root. Aggiungo pointer nel `CLAUDE.md` con statement di adozione.
- **Perché**: evita drift. `CLAUDE.md` è progetto-specifico (stack, hardware, convenzioni); le regole 07 sono meta-universali. Manterle in archivio single-source, referenziate, evita manutenzione duplicata.
- **Alternative considerate**:
  - Clonare al root → rigetto per drift potenziale.
  - Merge integrale in `CLAUDE.md` → rigetto per bloat; `CLAUDE.md` già 16KB.
  - Pointer+adozione esplicita → scelta.
- **Conseguenze**: Claude Code future sessions devono leggere archivio per regole operative meta. Lista fonti di verità (CLAUDE_OPERATING_RULES #1) estesa.
- **Azioni derivate**: edit `CLAUDE.md` per pointer + statement adozione.

### Decisione 004 -- Codex `/structural-reset` REJECTED per false-premise sandbox-confusion
- **Data**: 2026-05-07
- **Titolo**: Branch `codex/structural-reset` (Codex Cloud, 2026-05-01) REJECTED in toto, cherry-pick 3/4 concept astratti via ADR-0021
- **Decisione presa**: branch chiuso (PR #3 [REJECTED] formal + delete remote ref). Cherry-pick: AGENTS.md + encoding policy + pointer multi-client. Deferred: `config/machine-profile.example.yaml` (riprendere se entra Mac mini come device secondario).
- **Perche'**: branch contiene 43 file +3690/-2186 basati su premessa "transplanted checkout, all paths missing". Verifica empirica 2026-05-07 sul PC corretto: tutti 9 path target (Game/Synesthesia/Dafne/AA01/wrapper aider/api keys/dogfood log/SQLite/promptfoo) esistono fisicamente. Codex Cloud sandbox confondeva "non vedo path Windows assoluti" con "non esistono". Mergeare in toto avrebbe cancellato CLAUDE.md -312, MODEL_ROUTING.md -359, STATUS_MULTI_REPO.md -247.
- **Alternative considerate**:
  - Merge full -> rigetto (perderemmo governance reale per stato dormant falso)
  - Cherry-pick selettivo concept ADAPT -> scelta (3 di 4)
  - Close veloce senza cherry-pick -> rigetto (perderemmo concept utili emersi)
- **Conseguenze**: ADR-0021 Accepted, AGENTS.md attivo come instruction file Codex, encoding policy ASCII-first nuovi doc. Pattern Codex Cloud confusion documentato come caso-studio.
- **Azioni derivate**: ADR-0021 mergeato (PR #2). Branch deleted da origin. Mitigation strutturale anti-ricorrenza in AGENTS.md preamble.

### Decisione 008 -- Claude Max ri-acquistato +1mo, deadline-drift corretta (2026-05-18)
- **Data**: 2026-05-18
- **Decisione presa**: Eduardo ha ri-acquistato Claude Max per +1 mese. Deadline reale era ~17/05 (non 19/20: premessa-drift nel doc strategico fondante). Nuova deadline sovereign-transition = ~17/06/2026. Urgenza esistenziale OFF, scope sovereign INVARIATO.
- **Perche'**: rilassare il cronometro, non la rotta. Il mese aggiuntivo = finestra per validazione empirica sovereign-tier + decision-review profonda (uso produttivo capacita' Opus, no limit-anxiety).
- **Conseguenze**: ADR-0023 resta Proposed (no periodo post-Max reale ancora); trigger/date shiftano +1mo. CLAUDE.md roadmap §AGGIORNAMENTO 2026-05-18 + "Priorita' modelli AI" date corrette. ADR-0023 §Addendum 2026-05-18.
- **Classe-errore**: drift doc-vs-reality (deadline-fantasma), stessa famiglia Triangle/Sentience caught 2026-05-18. Lezione: date strategiche = re-verify, non ereditare.
- **Azioni derivate**: CLAUDE.md + ADR-0023 addendum + questo entry. NO flip ADR-0023 status. Programma decision-review (A2 PILLAR reconcile -> B1 ADR-retrospective -> B2 compass) prosegue, deadline-pressure rimossa.

### Decisione 007 -- Risposte 6 questions BLOCKING harsh review (2026-05-09)
- **Data**: 2026-05-09 mattino
- **Titolo**: Eduardo ha risposto alle 6 questions BLOCKING/SIGNIFICANT/MEDIUM identificate da harsh review flow chart 2026-05-09 (`docs/reviews/flow-chart-harsh-review-2026-05-09.md`)
- **Decisione presa**: 6 scelte ratificate, 6 task derivate (BACKLOG H7-H12), 2 ADR scaffold (ADR-0023 + ADR-0024 Proposed):

| Q | Domanda | Scelta | Action item |
|---|---------|--------|-------------|
| 1 | Strategic tier post-19/05 chi lo fa? | A -- Claude API on-demand $10-20/mese cap | ADR-0023 Proposed (H7) |
| 2 | Privacy guard rail tecnico? | A -- Wrapper enforcement automatico | Task H8 (1gg pre-19/05) |
| 3 | ADR Accepted threshold? | B -- Early-acceptance flag | Task H10 (status workflow update) |
| 4 | Bench mixed-workload pre-Max? | A -- 1 giornata dedicato | Task H9 (9-15/5 preferibile 9-10/5) |
| 5 | Vue3 -> Godot archive timing? | A+ -- Soft-deadline 2026-09-30 + AA01 attivazione Ondata 1+2 | ADR-0024 Proposed + Task H11 (Eduardo direct) |
| 6 | Memory drift mitigation? | A -- Stop hook automatico | Task H12 (settings.json hook) |

- **Perche'**: harsh review identificato 2 BLOCKING (V1 strategic tier + V2 privacy bypass) + 1 SIGNIFICANT (V3 sample size) + 4 choke points + edge cases. Senza decisioni esplicite, transition window 10gg pre-Max chiude con vulnerabilita' note. Decisioni Eduardo direzionano fix in 3-4 giornate fattibili nel window.
- **Alternative considerate**: per ogni Q opzioni B/C/D presentate harsh-reviewer mode. Eduardo ha scelto A in 5/6 (B in 3 con motivazione "trasparenza pura").
- **Conseguenze**: ADR-0023 + ADR-0024 Proposed (questo PR scaffold). 6 task BACKLOG H7-H12. 4 task M7-M10 deferred SPRINT_02 / opportunistic. Report harsh review salvato `docs/reviews/flow-chart-harsh-review-2026-05-09.md`.
- **Azioni derivate**: questo PR (1) salva report + crea ADR-0023 + ADR-0024 scaffold + aggiorna BACKLOG H7-H12 + DECISIONS_LOG. (2) Eduardo direct: H11 attivazione AA01 standalone. (3) Sessioni successive: H7-H10 + H12 fix prima 19/05.

### Decisione 006 -- Transition active sovereign 8-9/5 (validation pre-Max expiration)
- **Data**: 2026-05-08 sera -> 2026-05-09 notte
- **Titolo**: Adozione transition attiva (vs cold-cutover 19/05) per validare end-to-end stack sovereign con safety net Claude Max
- **Decisione presa**: invece di stop passivo + switch sovereign il 19/05 senza fallback, **attivare ora (8-9/5) lo stack sovereign completo** (OpenCode + Ollama 30B MoE + stack ADR-0017 active mode) per scoprire findings critici PRIMA che Claude Max scompaia.
- **Perche'**: 11gg residui sono finestra naturale per validation con safety net. Cold-cutover senza test reale e' rischio inutile (hardcoded gap stack scoperti il 20/05 senza fallback = blocker). Pattern lean: ogni minuto investito ora vale 10 minuti post-Max in trouble-shooting.
- **Alternative considerate**:
  - Stop passivo + cold-cutover 19/05 -> rigetto (rischio hardcoded gaps non scoperti)
  - Skip OpenCode + restare Aider only -> rigetto (limita esplorazione tool-use agentic alternative)
  - Migrazione completa OpenCode + abbandonare Aider -> rigetto (perdita 12 dogfood Aider validati)
  - Transition attiva con OpenCode + Ollama + stack ADR-0017 active mode -> scelta (ADR-0022 + dogfood #25 + #26 emergono naturalmente)
- **Conseguenze**: 4 findings critici scoperti (Qwen 2.5 Coder non tool-use OpenCode-compat / cloud free 8B-70B rate-limited / Qwen3 30B MoE viable / env var Gemini differisce). ADR-0022 ratificato Accepted in stessa giornata grazie a 2 dogfood reali. Tier routing OpenCode-specifico documentato in CLAUDE.md + MODEL_ROUTING.md. T3 SPRINT_02 hot-restart anticipato + passato.
- **Azioni derivate**: ADR-0022 Proposed (PR #15) -> Accepted (PR #19). 12 PR mergeati 8-9/5. Stack ADR-0017 down a chiusura sessione (volumes preservati per restart futuro). 10gg residui pre-Max ora con confidence empirica end-to-end.

### Decisione 005 -- Fase 6 closure anticipata 2026-05-07
- **Data**: 2026-05-07
- **Titolo**: Fase 6 closed con ADR-0015 + ADR-0017 entrambi Accepted, anticipato vs target sett.4 originale (~2026-05-17)
- **Decisione presa**: closure anticipata di 10 giorni rispetto al target ADR-0015 originale per riconoscere realta' empirica (dataset fermo a n=12 dal 24/04, focus shiftato a Game Sprint Impronta + Dafne Atto 2 + AA01).
- **Perche'**: forzare n>=15 in 12 giorni residui (07/05 -> 19/05) richiederebbe dogfood sintetici, anti-pattern documentato in ADR-0014 ("data per decidere, non collect data"). Trigger ADR-0008 "FULL-SOVEREIGN VIABLE" gia' confermato empiricamente al dogfood #12. Behavior-critical 5/3 superato (167%). Fail rate 8.3% << threshold 30%. Decision support gia' raggiunto.
- **Alternative considerate**:
  - Push aggressivo n=12 -> n>=15 in 12 giorni con task sintetici -> rigetto (anti-pattern)
  - Extension Fase 6 di 1-2 settimane (scenario C ADR-0015) -> rigetto (costo bridge stack senza valore aggiunto)
  - Mantenere status Proposed fino sett.4 -> rigetto (statusquo per status quo, ADR-0014 anti-hoarding)
  - Closure anticipata con soft-override esteso e rationale documentato -> scelta
- **Conseguenze**: scenario A full-sovereign $0-50/anno operativo da 19/05. Window 12 giorni ora orientata a smoke test sovereign opzionale + SPRINT_02 abbozzo + cleanup PR esterni. Privacy validation Synesthesia (criterio #3) retroattiva post-agosto.
- **Azioni derivate**: ADR-0015 status flip (Proposed -> Accepted). ADR-0017 status flip (Validated live + Proposed -> Accepted, 5/5 criteri PASS). JOURNAL entry +87 righe. COMPACT v11. STATUS_MULTI_REPO refresh.
