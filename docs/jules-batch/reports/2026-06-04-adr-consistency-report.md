# ADR + Decision-Log Consistency Report

## 1. ADR Inventory Table
| Num  | Short Title                         | Status     | Summary                                            |
|------|-------------------------------------|------------|----------------------------------------------------|
| 0001 | ADR 0001 -- Sovereign AI Strategy   | Superseded | post Claude Max (scadenza 19/05/2026), transizi... |
| 0002 | ADR 0002 -- Naming: CodeMasterDD... | Accepted   | rename repo da `lenovo-ai-station` a `codemaste... |
| 0003 | ADR 0003 -- Node.js: versione 24... | Accepted   | accetto Node 24 (Active LTS dal 28/10/2025, win... |
| 0004 | ADR 0004 -- Ollama config per RT... | Accepted   | Ollama configurato con `OLLAMA_FLASH_ATTENTION=... |
| 0005 | ADR 0005 -- YAGNI e approccio mi... | Accepted   | formalizzo YAGNI come principio trasversale del... |
| 0006 | ADR 0006 -- Cline + Qwen 7B viab... | Accepted   | Cline + Qwen 7B NON viable come sostituto Claud... |
| 0007 | ADR 0007 -- Aider + Qwen quantiz... | Superseded | Aider 0.86.2 + Qwen 14B Q2_K adottato come stac... |
| 0008 | ADR 0008 -- Silent corruption Ai... | Accepted   | scoperto silent-corruption deterministico con A... |
| 0009 | ADR 0009 -- Strategia evoluzione... | Accepted   | upgrade stack AI locale guidato da trigger espl... |
| 0010 | ADR-0010 -- Adozione MADR format... | Accepted   | da ADR-0010 in poi uso formato MADR bare-minima... |
| 0011 | ADR-0011 -- Cross-agent commit m... | Accepted   | il primo dogfood Aider (2026-04-22) ha scoperto... |
| 0012 | ADR-0012 -- Upgrade RAM 1664 GB... | Accepted   | upgrade hardware 232GB DDR5-5600 dual channel ... |
| 0013 | ADR-0013 -- Tier 3 cloud escalat... | Accepted   | acquisite 4 API keys gratuite o a basso costo (... |
| 0014 | ADR-0014 -- Fase 6 timeline comp... | Accepted   | ADR-0001 definiva Fase 6 tracking come "3 mesi ... |
| 0015 | ADR-0015 -- Fase 7 budget decisi... | Superseded | Fase 6 ha chiuso 3/4 criteri ADR-0014 PASS (qua... |
| 0016 | ADR-0016 -- Constraint-count as ... | Proposed   | La matrice routing modelli di ADR-0008 (hub pat... |
| 0017 | ADR-0017 -- UI + observability s... | Superseded | codemasterdd-ai-station oggi e' "infrastructure-... |
| 0018 | ADR-0018 -- Agent readiness prot... | Accepted   | Sessione 2026-04-24 ha creato 13 nuovi agent in... |
| 0019 | ADR-0019 -- Persistenza processo... | Accepted   | Il server Dafne (`START-SWARM.ps1`) muore 2 in... |
| 0020 | ADR-0020 -- Silent-fail Python g... | Accepted   | il `/insights` audit (2026-04-25, Evo-Tactics r... |
| 0021 | ADR-0021 -- Multi-client instruc... | Accepted   | la review del branch `codex/structural-reset` (... |
| 0022 | ADR-0022 -- OpenCode tool-use mo... | Accepted   | smoke test 2026-05-08 (n=5 entries #16-#20) ha ... |
| 0023 | ADR-0023 -- Strategic tier post-... | Superseded | post-19/05/2026 Claude Max OAuth scade. Strateg... |
| 0024 | ADR-0024 -- Vue3 Game archive + ... | Proposed   | Game-Godot-v2 (port pivot 2026-04-29) ha 215+ P... |
| 0025 | ADR-0025 -- Hyperspace Pods priv... | Accepted   | Hyperspace Pods (P2P AI Compute Clusters via li... |
| 0026 | ADR-0026 -- Cognitive workflow p... | Accepted   | Formalize integration di 3 cognitive workflow p... |
| 0027 | ADR-0027 -- Cross-PC clone archi... | Accepted   | **Accepted** -- empirical evidence-driven, 2026-... |
| 0028 | ADR-0028 -- Tier promotion metho... | Proposed   | **Proposed** 2026-05-13 notte tarda -- auto-mode... |
| 0029 | ADR-0029 -- OpenRouter eval decl... | Proposed   | **Context**: harsh-reviewer (PR #80+#81 cluster... |
| 0030 | ADR-0030 -- Post-Max orchestrati... | Accepted   | Eduardo realization 2026-05-15 mattina: soverei... |
| 0031 | ADR-0031 -- ChatGPT Business wor... | Proposed   | Esportare l'intero workspace ChatGPT Business "... |
| 0032 | ADR-0032 -- Jules-PR governance:... | Superseded | Riconcilia una divergenza cross-sessione non fo... |
| 0033 | ADR-0033 -- Jules governance: ow... | Accepted   | Supersede ADR-0032. Risoluzione dopo Archon 7-s... |
| 0034 | ADR-0034 -- Jules autonomous-man... | Proposed   | Eduardo (master-dd, sole decider) ha dato manda... |
| 0035 | ADR-0035 -- Jules-from-CLI proac... | Accepted   | Add **proactive Jules task dispatch from the CL... |
| 0036 | ADR-0036 -- Unified Orchestratio... | Accepted   | Adopt one hub-and-spoke orchestrator-worker doc... |
| 0037 | ADR-0037 -- Merge-autonomy model... | Accepted   | Decide what merge autonomy is STANDING (no per-... |
| 0038 | ADR-0038 -- Doctrine carve-out c... | Proposed   | ADR-0037 decision 2 made "governance-doctrine f... |
| 0039 | ADR-0039 -- R1 open-PR reconcile... | Proposed   | ADR-0037 dec.4 made standing external-merge rea... |

## 2. Supersede / Status Problems
- (a) ADR-0034 says it supersedes ADR-0033 decision 2,
  but ADR-0033 is NOT marked superseded.
  ADR-0034: `Questo SUPERSEDE ADR-0033 (2) "esterni read-only"`
  ADR-0033: `- **Status**: **Accepted** (2026-05-17)`
- (c) None found.

## 3. Direct Contradictions
- **ADR-0033 vs ADR-0034 (Autonomy on external repos)**
  - ADR-0033: `repo ESTERNI... SOLO triage read-only...`
  - ADR-0034: `Claude gestisce L'INTERO processo... in autonomia`

## 4. Decision-log Alignment
- (a) Decisions in log with no backing ADR: None found.
- (b) Open decisions that should be closed: None found.
  All items are marked CLOSED in OPEN_DECISIONS.md.
- (c) Accepted ADRs not reflected in DECISIONS_LOG.md:
  - ADR-0011: `- **Status**: Accepted`
  - ADR-0012: `- **Status**: Accepted`
  - ADR-0013: `- **Status**: **Accepted** (2026-04-23 02:05 ...`
  - ADR-0018: `- **Status**: **Accepted** (2026-04-24 ...`
  - ADR-0019: `- **Status**: **Accepted** (2026-04-24 ...`
  - ADR-0020: `- **Status**: Accepted`
  - ADR-0025: `- **Status**: **Accepted** (2026-05-12 ...`
  - ADR-0026: `- **Status**: **Accepted** (2026-05-12 ...`
  - ADR-0037: `> Status: **Accepted** -- 2026-06-03 ...`

## 5. Cross-reference Integrity
- `docs/adr/0024-vue3-archive-godot-canonical-timeline.md` ->
  Bad reference `ADR-2026` (mentions Game ADR-2026-05-05).

## 6. Severity Summary
| Finding | Severity | Description |
|---------|----------|-------------|
| ADR-0033/0034 Contradiction | High | Autonomy conflicts. |
| ADR-0033 not marked Super. | High | 0034 supersedes 0033. |
| Missing from Log | Medium | 9 Accepted ADRs not logged. |
| Bad cross-ref in ADR-0024 | Low | Non-existent ADR-2026. |