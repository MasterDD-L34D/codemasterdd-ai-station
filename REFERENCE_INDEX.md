# REFERENCE_INDEX

> Compilato dal template `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/REFERENCE_INDEX.md`.
>
> Indice navigabile delle reference attive del progetto. Popolato con asset realmente consultabili.

## Come leggere questo indice

Ogni entry ha: codice univoco, titolo, categoria, funzione (perché esiste), stato del testo (live/frozen/deprecated), uso consigliato (quando consultare), modulo collegato (dove si integra), note.

Categorie attive:
- **ADR** — decision record architetturali
- **PAT** — pattern operativo riusabile
- **RES** — research report / bench scientifico
- **LES** — lesson learned
- **REF** — reference esterno catalogato
- **SES** — log sessione
- **GOV** — file governance root-level
- **LOG** — log operativi
- **ARC** — archivio framework universale

---

## GOV — Governance root-level (entry point operativi)

### REF-G01
- **Codice**: GOV-01
- **Titolo**: CLAUDE.md
- **Categoria**: GOV
- **Funzione**: convenzioni autoritative progetto-specifiche per Claude Code (stack, hardware, tier routing, trigger delega, safety protocol)
- **Stato**: live, aggiornato 2026-04-23 post ADR-0012/13/14
- **Uso consigliato**: consultare SEMPRE inizio sessione; single-source convenzioni operative progetto
- **Modulo collegato**: regole meta-universali in `Archivio_.../07_.../CLAUDE_OPERATING_RULES.md`
- **Note**: ~16KB, autoritativo. Non sostituisce regole 07 ma le coabita (CLAUDE.md progetto-specific, 07 meta-universali).

### REF-G02
- **Codice**: GOV-02
- **Titolo**: PROJECT_BRIEF.md + COMPACT_CONTEXT.md
- **Categoria**: GOV
- **Funzione**: snapshot denso progetto per onboarding rapido (umano o agente)
- **Stato**: live v2 (post-integrazione archivio 2026-04-23)
- **Uso consigliato**: Fase 1 Task Execution Protocol — lettura minima obbligatoria
- **Modulo collegato**: schema template `04_BOOTSTRAP_KIT`

### REF-G03
- **Codice**: GOV-03
- **Titolo**: DECISIONS_LOG.md + OPEN_DECISIONS.md
- **Categoria**: GOV
- **Funzione**: indice ADR strategici + decisioni operative granulari + decisioni aperte non bloccanti
- **Stato**: live
- **Uso consigliato**: quando conflict tra fonti o decisione incerta (CLAUDE_OPERATING_RULES regola 1)

### REF-G04
- **Codice**: GOV-04
- **Titolo**: BACKLOG.md + ROADMAP.md + SPRINT_01.md
- **Categoria**: GOV
- **Funzione**: backlog prioritizzato + fasi long-term + sprint attivo
- **Stato**: live, SPRINT_01 attivo 2026-04-23 → 2026-05-06
- **Uso consigliato**: Fase 2 Task Execution Protocol — mappa task corrente

### REF-G05
- **Codice**: GOV-05
- **Titolo**: MASTER_PROMPT.md + PROMPT_LIBRARY.md + MODEL_ROUTING.md + REFERENCE_INDEX.md (questo)
- **Categoria**: GOV
- **Funzione**: prompt compilato portabilità + prompt riutilizzabili + routing modelli + indice reference
- **Stato**: live (creati 2026-04-23)
- **Uso consigliato**: quando portare progetto fuori contesto Claude Code nativa, o dubbi routing modello

---

## ADR — Architecture Decision Records

Indice completo in `DECISIONS_LOG.md`. Path: `docs/adr/NNNN-topic.md`.

### Critici (hub pattern / backbone strategico)
- **ADR-0001** — Sovereign AI strategy (target budget, fasi)
- **ADR-0008** — Aider whole format silent-corruption (**hub pattern** tier routing)
- **ADR-0010** — MADR format + skill policy
- **ADR-0011** — Cross-agent commit governance
- **ADR-0013** — Tier 3 cloud free providers
- **ADR-0014** — Fase 6 timeline compression

### Operativi correnti (stack)
- **ADR-0004** — Ollama RTX 5060 config
- **ADR-0007** — Aider + Qwen quantization (partially superseded)
- **ADR-0012** — RAM 64GB upgrade impact

### Superseded / reference only
- ADR-0002/0003/0005/0006/0009 — decisioni chiuse a complessità bassa o framework in attesa di trigger

---

## PAT — Pattern operativi

### REF-P01
- **Codice**: PAT-01
- **Titolo**: `docs/patterns/delegation-to-aider.md`
- **Funzione**: decision tree classificazione task cosmetic/behavior/strategic + formato handoff + review loop
- **Stato**: live, **backbone** trigger delega in-session (CLAUDE.md)
- **Uso consigliato**: prima di ogni Edit/Write su file esistente

### REF-P02
- **Codice**: PAT-02
- **Titolo**: `docs/patterns/aider-delegation-log-template.md`
- **Funzione**: schema colonne log dogfood (mensile)
- **Uso consigliato**: entry in `logs/aider-delegation-YYYY-MM.md`

### REF-P03
- **Codice**: PAT-03
- **Titolo**: `docs/patterns/git-amend-force-push-safe.md`
- **Funzione**: protocollo safe git amend/force-push (raro, autorizzazione esplicita)

### REF-P04
- **Codice**: PAT-04
- **Titolo**: `docs/patterns/claude-code-workflow.md` + `docs/patterns/prompt-engineering-italiano.md`
- **Funzione**: convenzioni Claude Code specifiche + italiano prompt patterns

---

## RES — Research / Bench

### REF-R01
- **Codice**: RES-01
- **Titolo**: `docs/research/bench-post-ram-upgrade-2026-04-22.md`
- **Funzione**: bench empirico Ollama post-upgrade 64GB (8 run, metodologia + decisioni ADR-0012 addendum)
- **Stato**: authoritative per speed tok/s modelli locali

### REF-R02
- **Codice**: RES-02
- **Titolo**: `docs/research/quality-bench-2026-04-23.md`
- **Funzione**: quality bench HumanEval-style + hard problems (75 test, 100% pass@1, discriminant findings)
- **Stato**: authoritative per quality parity locale/cloud

### REF-R03
- **Codice**: RES-03
- **Titolo**: `docs/research/ai-stack-evolution-2026.md` + `docs/research/mcp-servers-priorities.md` + `docs/research/claude-max-limits-2026.md` + `docs/research/rtx5060-ollama-benchmarks.md`
- **Funzione**: research longitudinale stack AI, MCP servers, limits Max, GPU Blackwell

---

## LES — Lessons learned

### REF-L01
- **Codice**: LES-01
- **Titolo**: `docs/lessons-learned/victus-trauma-postmortem.md`
- **Funzione**: post-mortem incidente BitLocker+OneDrive (driver filosofia sovereign ADR-0001)

### REF-L02
- **Codice**: LES-02
- **Titolo**: `docs/lessons-learned/capire-prima-fare-dopo.md`
- **Funzione**: meta-lesson su analisi-prima-di-execution

### REF-L03
- **Codice**: LES-03
- **Titolo**: `docs/lessons-learned/ai-as-thinking-partner.md`
- **Funzione**: rubber duck meta-pattern per future sessioni

---

## REF — Reference esterne

### REF-E01
- **Codice**: REF-01
- **Titolo**: `docs/reference/commands-cheatsheet-windows.md`
- **Funzione**: cheatsheet comandi operativi Windows/PowerShell

### REF-E02
- **Codice**: REF-02
- **Titolo**: `docs/reference/agno-ollama-snippets.md`
- **Funzione**: snippet Agno framework (Pattern 2 corretto post-audit)

### REF-E03
- **Codice**: REF-03
- **Titolo**: `docs/reference/subagents-skills-candidates.md`
- **Funzione**: catalogo curato subagent/skill/tool candidates
- **Stato**: dormiente (nessun install pianificato; audit periodico L5)

### REF-E04
- **Codice**: REF-04
- **Titolo**: `docs/reference/agentshield-scan-2026-04-22.md`
- **Funzione**: baseline AgentShield scan

---

## SES — Sessioni log

- `docs/sessions/2026-04-19-sessione-notturna.md`
- `docs/sessions/2026-04-19-sessione-serale.md`

**Stato**: frozen. Storiche, low re-read value.

---

## LOG — Log operativi

### REF-LO01
- **Codice**: LOG-01
- **Titolo**: `logs/aider-delegation-2026-04.md`
- **Funzione**: tracking dogfood Fase 6 (schema PAT-02)
- **Stato**: live, in scrittura continua

### REF-LO02
- **Codice**: LOG-02
- **Titolo**: `JOURNAL.md`
- **Funzione**: diario cronologico sessioni significative
- **Stato**: live, append a fine sessione per convenzione CLAUDE.md

---

## ARC — Archivio framework universale

### REF-A01
- **Codice**: ARC-01
- **Titolo**: `Archivio_Libreria_Operativa_Progetti/`
- **Funzione**: framework operativo multi-progetto (imported 2026-04-23): bootstrap kit + pacchetto Claude Code operating + libreria + template + workflow + reference
- **Stato**: live, adottato schema per governance root-level
- **Uso consigliato**: consultare quando si apre nuovo progetto o quando serve template/workflow generico; leggere `00_START_HERE.md` → `01_MASTER_INDEX.md`
- **Moduli principali**: `02_LIBRARY/` (manuale sistema), `04_BOOTSTRAP_KIT/` (template schema), `05_TEMPLATE_REALI_PROMPTATI/` (9 prompt template), `06_WORKFLOWS_AND_CHECKLISTS/` (workflow), `07_CLAUDE_CODE_OPERATING_PACKAGE/` (regole meta Claude Code)
- **Note**: framework è game-biased. Adattato: `FIRST_PRINCIPLES_GAME_CHECKLIST` N/A per questo repo (Decisione 002 DECISIONS_LOG).

---

## Materiale esterno retained

### REF-X01
- **Codice**: X-01
- **Titolo**: `final-research-and-snippets-2026-04-21-v3.md` (root)
- **Funzione**: source material esterno triato (sessione claude.ai browser 2026-04-21)
- **Stato**: frozen. Retained per audit trail.
- **Uso consigliato**: non re-leggere senza motivo specifico. Contenuto utile già integrato in docs/.
