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

### REF-EXT-05 (M14 BOOKMARK 2026-05-12, refreshed 2026-05-12 sera)
- **Codice**: EXT-05
- **Titolo**: `dair-ai/Prompt-Engineering-Guide` (74479 stars MIT 2026-05-12)
- **URL**: https://github.com/dair-ai/Prompt-Engineering-Guide + hosted https://www.promptingguide.ai/
- **Funzione**: reference canonical Prompt Engineering + LLM techniques + RAG + AI agents + context engineering. Lookup-only navigator post-screening.
- **Stato**: BOOKMARK + Vault Card live (`Cards/m14-claude-resources-wave-2026-05-12/dair-ai-prompt-engineering-guide.md`).
- **Uso consigliato**: consultare per pattern prompt + few-shot + chain-of-thought + RAG quando emerge gap specifico. Sezione "AI Agents" complementare a ADR-0018 + ADR-0026.
- **Note**: M14 Wave 2026-05-12 task #9 EXECUTED 2026-05-12 sera (vault Card creation sotto Eduardo authorization "voglio fare 3 e 4"). License MIT empirical re-verify L-2026-05-007 pattern. Refresh stars 74448 -> 74479 (+31 in 1 day).

### REF-EXT-07 (M14 BOOKMARK 2026-05-12 sera)
- **Codice**: EXT-07
- **Titolo**: `shanraisshan/claude-code-best-practice` (52602 stars MIT 2026-05-12)
- **URL**: https://github.com/shanraisshan/claude-code-best-practice
- **Funzione**: cross-pattern reference Claude Code features comprehensive (Subagents + Commands + Skills + Hooks + MCP + Plugins + Memory + Orchestration). Cherry-pick on-demand quando emerge gap codemasterdd-side.
- **Stato**: BOOKMARK + Vault Card live (`Cards/m14-claude-resources-wave-2026-05-12/shanraisshan-best-practice-cross-pattern.md`)
- **Cross-pattern review**: 8 pattern reference candidate identified (Orchestration Command->Agent->Skill + Routines + Power-ups + Auto/Fast Mode + Git Worktrees + Plugin marketplaces + Memory 4-layer + Ultrareview). DEFER formal ADR adoption fino SPRINT_02+ Three Strikes trigger.
- **Note**: M14 Wave 2026-05-12 task #2 EXECUTED 2026-05-12 sera. License MIT empirical re-verify.

### REF-EXT-08 (M14 AUDIT-ONLY 2026-05-12 sera)
- **Codice**: EXT-08
- **Titolo**: `hesreallyhim/awesome-claude-code` (43498 stars NOASSERTION 2026-05-12)
- **URL**: https://github.com/hesreallyhim/awesome-claude-code
- **Funzione**: awesome-list canonica community-curated per Claude Code. Refresh status check post-Apr 22 entries.
- **Stato**: AUDIT-ONLY (NOASSERTION license = no clear rights, default copyright). Vault Card live (`Cards/m14-claude-resources-wave-2026-05-12/hesreallyhim-awesome-claude-code-refresh.md`)
- **Uso consigliato**: NO clone NO derivative. Refresh scan periodic vs `docs/reference/subagents-skills-candidates.md` per identify entries post-Apr 22 non-catalogate. Same pattern come #5 Karpathy AUDIT-ONLY (L-2026-05-007 + L-008).
- **Note**: M14 Wave 2026-05-12 task #6 EXECUTED 2026-05-12 sera.

### REF-EXT-09 (M14 BOOKMARK trigger-conditional 2026-05-12 sera)
- **Codice**: EXT-09
- **Titolo**: `VoltAgent/awesome-design-md` (76314 stars MIT 2026-05-12)
- **URL**: https://github.com/VoltAgent/awesome-design-md
- **Funzione**: awesome-list DESIGN.md curated index (brand systems Linear/Vercel/Stripe/etc.). Reference per UX/brand standards.
- **Stato**: BOOKMARK trigger-conditional. Vault Card live (`Cards/m14-claude-resources-wave-2026-05-12/voltagent-awesome-design-md-bookmark.md`)
- **Trigger condition**: Synesthesia M5 BACKLOG riattivata (UI work post-esame UniUPO ~ago 2026) OR Game-Godot-v2 UX phase (post Path A canonical closure)
- **Note**: M14 Wave 2026-05-12 task #12 EXECUTED 2026-05-12 sera. NO clone disk fino a trigger.

### REF-EXT-06 (M11 INSTALLED 2026-05-12)
- **Codice**: EXT-06
- **Titolo**: `obra/superpowers` v5.1.0 (186664 stars MIT 2026-05-12)
- **URL**: https://github.com/obra/superpowers (via marketplace `anthropics/claude-plugins-official`)
- **Funzione**: 14 skills methodology framework auto-trigger Claude Code (brainstorming + writing-plans + executing-plans + subagent-driven-development + dispatching-parallel-agents + TDD + systematic-debugging + verification-before-completion + using-git-worktrees + reviews + writing-skills)
- **Stato**: **INSTALLED 2026-05-12** scope user (`~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/`). Effective ALL future Claude Code sessions Eduardo.
- **Uso consigliato**: methodology layer additivo. Skill auto-trigger cross-session. Monitor 1 settimana behavior impact (Eduardo direct).
- **Note**: M11 SHIP via Archon Protocol 3 CALIBRATE + falsifying experiment 5/5 PASS (PR #59). Lesson L-2026-05-008 methodology promote learnings/.

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

---

## EXT — External Claude Code Catalogs (added 2026-05-10)

### REF-EXT01
- **Codice**: EXT-01
- **Titolo**: `awesome-claude-code-toolkit` (rohitg00 community OSS Apache 2.0)
- **Path locale**: `C:/dev/scratch/awesome-claude-code-toolkit/`
- **Remote**: `github.com/rohitg00/awesome-claude-code-toolkit.git`
- **License**: Apache 2.0 (attribution required per file imported)
- **Funzione**: catalog community per cherry-pick selettivo agents/skills/hooks/rules/mcp-configs/templates
- **Stato**: live (cloned per evaluation), pull-when-needed reference
- **Inventario**: 135 agents (10 cat) + 35+ skills (38 dirs) + 42 commands + 20 hooks + 15 rules + 7 templates + 14 MCP configs + 176+ plugins
- **Uso consigliato**: NO bulk import. Cherry-pick on-demand quando un task reale richiede skill specifica. Audit-then-replay obbligatorio (read full file prima adopt). Lock commit hash al momento dell'import effettivo (NON pre-emptive).
- **Anti-pattern**: bulk import speculativo (YAGNI ADR-0005), continuous sync upstream, blind import (supply-chain vector).
- **Skill candidate per codemasterdd** (top-tier match, da validate fit empirico): claude-memory-kit / mcp-development / continuous-learning / docker-best-practices / accessibility-wcag / python-best-practices / git-advanced.
- **Note**: integrato 2026-05-10 via AA01 task `2026-05-aa01-001-two-repos-analysis-integratio` research-long preset. Memory `reference_external_toolkits.md` per cherry-pick policy completa.

### REF-EXT02
- **Codice**: EXT-02
- **Titolo**: Autoresearch tools (multi-candidate)
- **Funzione**: autonomous AI experiment loop / research agents -- candidate per overnight research workflow + dogfood expansion SPRINT_03+
- **Stato**: research-only (NO clone), strategic candidate evaluation
- **Top candidate**: [`199-biotechnologies/autoresearch-cli`](https://github.com/199-biotechnologies/autoresearch-cli) -- "any AI coding agent" integration -> direct fit Aider/OpenCode/Claude Code codemasterdd stack
- **Alternative (Karpathy pattern coerente vault-shared)**: [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch) MIT, single-GPU PyTorch + uv, modifies train.py iteratively (5min/iter, val_bpb metric), tested H100 (RTX 5060 8GB potenzialmente sotto-spec per full training, ma orchestrazione pattern valuable)
- **Other candidates**: AutoResearch/autora (theorist+experimentalist agents), aiming-lab/AutoResearchClaw (idea-to-paper end-to-end), openags/Auto-Research (UI-driven generalist scientist)
- **Use case codemasterdd**: deferred SPRINT_03+ quando emerge use case concreto (overnight autonomous research / dogfood expansion). NO install pre-emptive (YAGNI ADR-0005).
- **Privacy**: tools generic, no Eduardo source code -> cloud OK irrelevante
- **Note**: integrato 2026-05-10 scope extension AA01 task 001. Memory `reference_autoresearch_tools.md` per evaluation completa.

### REF-EXT03
- **Codice**: EXT-03
- **Titolo**: [Hyperspace Pods](https://hyperspace.sh/) -- Private AI Compute Clusters
- **Funzione**: P2P decentralized AI cluster: pool laptops/desktops in shared inference network (no cloud, no central server). Allineamento sovereign-first codemasterdd.
- **Stato**: strategic research candidate (research-only fase 1, pre-audit privacy)
- **Stack**: libp2p v3 + GossipSub + Kademlia DHT + Circuit Relay v2 + Yamux + Noise encryption
- **License**: open source CLI + network + SDK (Pi component MIT). Web app + Thor backend source-available.
- **CLI install**: `curl -fsSL https://download.hyper.space/api/install | bash` (Linux/macOS) / `curl ... | powershell -` (Windows admin)
- **Hardware**: VRAM 4GB minimum (GTX 1650) -- RTX 5060 8GB QUALIFIES. CPU-only relay/embedding mode supportato.
- **Capabilities** (9): Inference / Embedding / Storage / Memory / Relay / Validation / Orchestration / Caching / Proxy
- **Strategic relevance codemasterdd**: roadmap menziona "Mac mini M4 Pro 48GB" come future inference upgrade (CLAUDE.md "Estensioni future"). Pods abilita scenario *senza* infrastruttura proprietaria: Eduardo pool Lenovo + (futuro) Mac mini + altri device family/friends in shared cluster.
- **Use case codemasterdd**: REFERENCE only fase 1. Install opportunistic SE/QUANDO Mac mini entra device fleet OR scenario distributed inference emerge post-Max sovereign expansion.
- **Privacy gate**: P2P inference -- **AUDIT REQUIRED PRIMA install** (user query data flow + Pod trust mesh model + LAN model sharing). NO install pre-audit.
- **Note**: integrato 2026-05-10 scope extension AA01 task 001. Memory `reference_hyperspace_pods.md` per detail strategico + ADR addendum trigger.
