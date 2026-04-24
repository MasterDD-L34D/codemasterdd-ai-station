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
| 0015 | Fase 7 budget decision full-sovereign | **Proposed** | 2026-04-24 | Opzione A $0-50/anno + deroga criterio #3 (Synesthesia dormant fino agosto) |
| 0016 | Constraint-count routing dimension | **Proposed** | 2026-04-24 | 2D matrix classe + constraint-count; 5+ strict → manual Claude Code |
| 0017 | UI + observability stack | **Proposed** (4/5 criteri live validated 2026-04-24) | 2026-04-24 | LiteLLM Proxy + Langfuse + promptfoo + Aider browser + Flask mini-app custom |
| 0018 | Agent readiness protocol (3-gate smoke+research+tuning) | **Accepted** | 2026-04-24 | Ogni agent `draft` fino passaggio gate. 3/18 ready, 15/18 draft retroactive |

### In review (Proposed, awaiting Accepted trigger)
- **ADR-0015** — Fase 7 budget decision full-sovereign. Trigger Accepted: review settimana 4 (~2026-05-17) con verifica criteri #2 reliability + #4 cost confermati + no fail rate regression. Input 2026-04-24: Synesthesia dormant fino agosto 2026 → criterio #3 derogato.
- **ADR-0016** — Constraint-count routing dimension. Trigger Accepted: n≥3 data points addizionali (constraint=4 explicit LOCAL, 2-transform LOCAL, 5-strict LOCAL). Update 2026-04-24: +1 data point (#12 constraint=4 parity-based, partial) → constraint specificity identificata come sub-dimensione.
- **ADR-0017** — UI + observability stack. Trigger Accepted: step 0-4 rollout phased completato senza blocker entro Sprint 02 (~2026-05-17). Scope codemasterdd evolve "infrastructure-as-code" → "infrastructure-as-code + observability self-hosted + UI glue minimale".

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
