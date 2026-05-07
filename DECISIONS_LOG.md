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
| 0009 | Upgrade trigger framework | Proposed (T2 materialized by 0012) | 2026-04-21 | Framework trigger hardware/cloud |
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
| 0021 | Multi-client instruction files (AGENTS.md + Codex anti-confusion) | **Accepted** | 2026-05-07 | AGENTS.md preamble Codex sandbox-aware + CLAUDE.md autoritativo + encoding ASCII-first nuovi doc. PR #2 mergeato. Trigger: branch `codex/structural-reset` REJECTED per false-premise sandbox-confusion. |

### In review (Proposed, awaiting Accepted trigger)
- **ADR-0016** -- Constraint-count routing dimension. Trigger Accepted: n>=3 data points addizionali (constraint=4 explicit LOCAL, 2-transform LOCAL, 5-strict LOCAL). Update 2026-04-24: +1 data point (#12 constraint=4 parity-based, partial). Stato 2026-05-07: dataset Fase 6 closed a n=12, ulteriori data points emergeranno organicamente in SPRINT_02 post-Max.

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
