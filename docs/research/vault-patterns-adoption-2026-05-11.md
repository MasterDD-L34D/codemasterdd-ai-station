# Vault-shared pattern adoption research (2026-05-11)

<!--
Cherry-pick policy applicata: pull-when-needed, audit-then-replay.
Source: vault-shared sibling-peer (C:/dev/vault-shared/, Karpathy LLM-wiki).
NO clone vault files, NO commit hash citato (drift risk repo Eduardo-driven).
Boundary: sovereign-only sibling-peer disjoint scope (memory project_vault_shared.md).
Audit-then-replay 2026-05-11 (AA01 task aa01-002-vault-integration-readonly).
-->

> **Scope**: read-only deep dive vault-shared (sibling-peer), identificazione 5 pattern strutturali/metodologici, decisione adopt/skip/defer per ognuno con rationale documented.
>
> **Status**: Research complete 2026-05-11. Apertura PR atomiche derivate (ADR + agent template) opzionale — Eduardo decide.
>
> **Generated via**: AA01 workspace `2026-05-aa01-002-2026-05-11-vault-integration-readonly/DRAFT/` (00-04). Questo doc è sintesi destinata codemasterdd repo, DRAFT integrali conservati in AA01.

---

## TL;DR

5 pattern identificati in vault-shared (7/7 production agents milestone parziale: 6/7 actually production + 1/7 hold draft per `evo-tactics-design-watcher` TASK-007 in flight). Decisioni:

| Pattern | Decision | Rationale |
|---------|----------|-----------|
| A1 routing per-task granular | **SKIP** | Vault multi-format workload != codemasterdd dev-coding workload, mapping forzato = over-engineering |
| A2 3-step Quality Gate methodology | **SKIP** (revised post-autoresearch) | ADR-0018 già definisce 3-gate identico (pubblicato 2026-04-24, convergenza), duplicate avoid |
| A3 A/B benchmark twin (claude vs sovereign) | **DEFER** | Re-evaluate post-Max scenario reale + sub-agent specifico mostra frizione |
| B Agent template strutturale (Edge case + Quality Gate body sections) | **EXPAND ADOPT** | 2 file: `SMOKE_TEST_TEMPLATE.md` (chiude gap ADR-0018 esistente) + `SUB_AGENT_TEMPLATE.md` (scaffolding nuovo agent) |
| C `smoke_metric` frontmatter | **SKIP (frontmatter), inglobato in B (body)** | Drift osservato in vault stesso (production folder + status: draft frontmatter not synced) |

Output finale Phase 5 opzionali (PR atomiche post questa research doc):
1. `.claude/agents/SMOKE_TEST_TEMPLATE.md` (Pattern B Part 1, chiude gap ADR-0018 esistente file mai creato)
2. `.claude/agents/SUB_AGENT_TEMPLATE.md` (Pattern B Part 2, scaffolding nuovo agent)

**NOTE autoresearch revised**: ADR-0026 sub-agent-quality-gate scartato post multi-source synthesis. ADR-0018 (2026-04-24) già definisce 3-gate protocol identico al Quality Gate vault. Vedi sezione 9 sotto.

---

## 1. Findings preliminari

### 1.1 Path drift llm-routing.json

- Memory codemasterdd `project_vault_shared.md` cita `vault-shared/llm-routing.json`
- Path reale: `C:/dev/vault-shared/Extras/config/llm-routing.json`
- **Action**: aggiornare memory durante consolidation (fatto, vedi sezione 7)

### 1.2 Stack overlap concreto verificato

`Extras/config/llm-routing.json` schema v1.0 Ollama endpoint:
```
"endpoint": "http://192.168.1.121:11434"
```

`192.168.1.121` = IP Lenovo CodeMasterDD nel fleet codemasterdd (CLAUDE.md fleet section). Vault USA Ollama runtime DI codemasterdd.

8/8 modelli routing vault sono presenti su Lenovo Ollama:
- qwen3-coder:30b, qwen2.5-coder:7b, mistral:latest, qwen3.5:latest, qwen3:8b, nomic-embed-text:latest, deepseek-r1:14b (riferimento llm-routing.json)

Sibling-peer stack overlap confermato concretamente. Adoption pattern A1 sarebbe applicabile, ma decisione SKIP per cost-benefit (workload divergente, vedi sez 3.1).

### 1.3 Gap "production folder" vs "status: draft" frontmatter

7 agent in `production/agents/` MA tutti hanno frontmatter `status: draft`.

Cross-reference DIFF.md UPDATE 2026-05-10 documenta:
- 6/7 PRODUCTION promotion completata (passed Step 3 Tuning)
- 1/7 HOLD DRAFT (`evo-tactics-design-watcher`, TASK-007 in flight)

Frontmatter status field NOT synced con folder state per 6 agent. Memory codemasterdd cita "7/7 PRODUCTION milestone hit 2026-05-10" — accuracy parziale (folder location yes, status frontmatter no, 1/7 in flight).

**Implicazione adoption**: pattern C `smoke_metric` in frontmatter è UNSAFE (sync drift osservato in vault stesso). Adottare in body section (pattern B), NON in frontmatter.

---

## 2. Quality Gate workflow formalized (vault § Quality Gate)

3-step gate override globale (vault CLAUDE.md riga 62-88):

### Step 1 -- Smoke Test
Fixture concreta + output minimo + time + idempotency-tested.

Esempio canonical: `pathfinder-pdf-indexer` frontmatter
```
smoke_metric: 'Pregen-Bard.pdf 3pg / 31.7s / 14391 chars md / idempotency-tested'
```

### Step 2 -- Research
≥3 edge case formal in `docs/research/<component>-<date>.md` con frontmatter `quality_gate_step: 2`.

Edge case canonici: file corrotto/encoding, Ollama endpoint unreachable, vault 10k+ note perf, conflitti frontmatter, permessi filesystem Windows, path UTF-16 BOM/emoji.

### Step 3 -- Tuning
Metrica before/after, target dichiarato. Esempi: ingestor PDF 100pg <2min, linter scan <30s per 1000 note, dispatcher throughput task/min + claude_cost=0.

### Promotion workflow

```
wip/agents/<name>  → Step 1 Smoke pass
  ↓
draft/agents/<name>  → Step 2 Research + Step 3 Tuning pass
  ↓
production/agents/<name>  -- live (passed all 3 gates)
```

Regola hard: **mai skip step**.

---

## 3. Pattern adoption decisions con rationale

### 3.1 Pattern A1 -- SKIP routing per-task granular

**Source vault**: `Extras/config/llm-routing.json` schema v1.0 + DIFF routing decision matrix (15 task-type mappati).

**Codemasterdd current**: CLAUDE.md tier routing class-based (cosmetic/behavior-critical/strategic) + constraint-count ADR-0016 (2nd dim) + OpenCode tier ADR-0022.

**Gap workload**:
- Vault = multi-format (PDF batch indexing, vault embed obsidian, tagging massive, atomization research, summary bulk)
- Codemasterdd = coding-dev (Edit/Write/Read/Bash/Grep su repo)
- Task-types vault NON mappabili 1:1 a codemasterdd

**Decision**: SKIP. Adottare addendum per-task-type granular = adopt task ontology che non serve, over-engineering NO benefit.

**Trade-off accettato**: codemasterdd class-based stays. Se in futuro workload codemasterdd diventa multi-format (integration vault stessa via shared task), revisita.

### 3.2 Pattern A2 -- SKIP 3-step Quality Gate methodology (revised post-autoresearch)

**Source vault**: CLAUDE.md § Quality Gate (override globale, 3-step gate, mai skip).

**Codemasterdd current re-verificato**: ADR-0018 (agent-readiness-protocol, Accepted 2026-04-24) definisce **3-gate identico**:
- Gate 1 Smoke test live (required) -- corrisponde Step 1 Smoke vault
- Gate 2 Ricerca validation (required, sources/licenses/framework) -- corrisponde Step 2 Research vault
- Gate 3 Tuning iterativo (required) -- corrisponde Step 3 Tuning vault

**Convergenza temporale**: ADR-0018 pubblicato 2026-04-24, vault Quality Gate stesso periodo (vault created 2026-04-24, milestone 2026-05-10). Convergenza pattern indipendente.

**Decision REVISED post autoresearch**: **SKIP** (NOT TENTATIVE ADOPT). Crear nuovo ADR-0026 sarebbe duplicate di ADR-0018, increases governance bloat senza benefit.

**Differenza sottile NOT actioned**: vault Step 2 Research = "≥3 edge case formal in docs/research/<comp>-<date>.md". ADR-0018 Gate 2 = sources/licenses/framework validation. Scope diverso.

**Reactivation trigger**: se gap edge-case formalization in ADR-0018 emerge concreto durante futuro smoke test (Gate 2 sources/license insufficient per qualitative review) → proporre ADR-0018 addendum con `≥3 edge case formal` come 5° item Gate 2 (NON nuovo ADR).

**Pattern strutturale ancora valorizzato in Pattern B** (sezione 3.4): Edge case section + smoke test fixture body block dal vault sono adottati come template, NOT come governance separato.

### 3.3 Pattern A3 -- DEFER A/B benchmark twin

**Source vault**: 2 coppie A/B implementate:
- `dispatcher-claude` <-> `ollama-dispatcher`
- `ingestor-claude` <-> `vault-ingestor`

DIFF.md formal benchmark con 5-category metric + routing decision matrix update + edge case formalization.

**Cost setup**: alto (2 variant implementation + benchmark fixture + DIFF doc methodology + run/compare cycle).

**Benefit**: data-driven post-Max migration decisions, validate sovereign tier vs strategic tier per sub-agent specifico.

**Gap codemasterdd**: 18 sub-agent `.claude/agents/` tutti claude-driven, NO local-llm variants.

**Decision**: DEFER. Pre-condition adoption = 1 sub-agent specifico mostra effective frizione (cost ricorrente, quality requirement degradabile) post-Max → trigger setup A/B per QUEL sub-agent.

**Reactivation criteria** (in research doc per future reference):
- Sub-agent invocato ≥N volte/mese post-Max con cost >threshold
- Sovereign tier validation needed empirico per sub-agent specifico
- Re-evaluate post-Max window 2026-05-20+ durante SPRINT_02 T5 (sovereign validation reale)

### 3.4 Pattern B -- EXPAND ADOPT (revised post-autoresearch)

**Source vault**: 7/7 agent seguono pattern strutturale comune (DRAFT 02 § 1):
- `## Ruolo` (1 line scope)
- `## Input` (spec)
- `## Processo` (numbered steps ≤7)
- `## Output` (path + template)
- `## Edge case (research TODO)` (5-7 formal)
- `## Quality Gate -- Step 1 smoke test` (fixture + expected + target + status in body)

**Gap codemasterdd identificato + GAP ESISTENTE da chiudere**:
- 18 sub-agent `.claude/agents/` variable structure, NO formal Edge case + smoke test sections
- **ADR-0018 (riga 175+202-208) promette `.claude/agents/SMOKE_TEST_TEMPLATE.md` con prompt prescriptive per ogni tipo agent + output validation checklist + tuning iteration pattern**
- **File MAI creato** (gap ~17gg, 2026-04-24 → 2026-05-11)

**Decision REVISED EXPAND**: crear 2 file (NON 1):
1. `.claude/agents/SMOKE_TEST_TEMPLATE.md` (PR atomic, chiude gap ADR-0018 + structure vault-informed)
2. `.claude/agents/SUB_AGENT_TEMPLATE.md` (PR atomic, scaffolding nuovo agent body)

Scope diverso:
- SMOKE_TEST_TEMPLATE = check-list per validate agent ESISTENTI (run smoke + report)
- SUB_AGENT_TEMPLATE = scaffold body per CREARE nuovo agent

Structural vault contributo: Edge case + Quality Gate body sections inglobate in entrambi.

`SUB_AGENT_TEMPLATE.md` (nuovo file scaffolding):

```markdown
---
name: <slug-agent>
description: <1-2 line + trigger phrases>
tools: <list>
model: sonnet|opus|haiku
---

# <agent-name>

## Ruolo
<1 line scope>

## Processo
1. ...
(max 7 steps consigliato, non enforced)

## Output
<path + structure template>

## Edge case (research TODO)
- ...
(target >=3, ispirato vault Quality Gate Step 2)

## Quality Gate -- Step 1 smoke test
Input: <fixture concrete>
Expected: <output osservabile>
Target: <perf or correctness criterion>
Status: [ ] not run
```

**Attribution header** in commento HTML inizio file (cherry-pick policy compliance).

**NO retroactive update 18 sub-agent existing** (over-touch risk). Template applies a future sub-agent.

### 3.5 Pattern C -- SKIP frontmatter, inglobato in B body

**Source vault**: pathfinder-pdf-indexer `smoke_metric: '3pg / 31.7s / 14391 chars md / idempotency-tested'` in frontmatter.

**Drift findings critico** (sez 1.3): vault stesso mostra frontmatter status hard to maintain (7 agent production folder + status: draft frontmatter not synced).

**Decision**: SKIP frontmatter approach. Pattern inglobato in B body block (`## Quality Gate -- Step 1 smoke test`) — smoke fixture + status checkbox in body, NOT frontmatter.

Status frontmatter codemasterdd resta NULL (Claude Code convention). Status tracking gestito in `.claude/agents/README.md` matrix (ADR-0018) = single source of truth.

---

## 4. Output finale -- PR atomiche derivate (revised post-autoresearch)

3 PR atomiche post questa research doc:
1. **Questo file** `docs/research/vault-patterns-adoption-2026-05-11.md` (mandatory output, foundation, include sezione 9 autoresearch finding)
2. **`.claude/agents/SMOKE_TEST_TEMPLATE.md`** (Pattern B Part 1, chiude gap ADR-0018 file mai creato)
3. **`.claude/agents/SUB_AGENT_TEMPLATE.md`** (Pattern B Part 2, scaffolding nuovo agent body structure)

NON commit insieme: ogni PR atomic, mantenere review surface focused.

PR 2 e 3 possono essere adoptate selettivamente (es. solo SMOKE_TEST se SUB_AGENT è over-engineering per scope corrente).

---

## 5. Constraint compliance verified

- [x] NO write su vault-shared (read-only access only durante research)
- [x] NO clone agent files (catalog by head + frontmatter only, pattern decision based)
- [x] NO referenziare commit hash vault (no hash citato in questo doc né in DRAFT)
- [x] NO bulk import (5 pattern selettivi + 2 ADOPT + 2 DEFER/SKIP + 1 SKIP-inglobato)
- [x] Attribution header (cherry-pick policy compliance, HTML comment top file)
- [x] Privacy guard rail H8 N/A (no delegation cloud invoke durante research)

---

## 6. Reactivation triggers per defer/skip patterns

- **A1 routing per-task granular**: trigger se codemasterdd workload diventa multi-format (es. integration vault stessa via shared task)
- **A3 A/B benchmark twin**: trigger se sub-agent specifico mostra effective frizione post-Max (cost ricorrente >threshold, quality requirement degradabile testato empirico)

---

## 7. Memory + governance updates riferiti

- `project_vault_shared.md` (memory codemasterdd): aggiornare con
  - Path llm-routing.json corretto (`Extras/config/llm-routing.json`)
  - Stato 6/7 PRODUCTION + 1/7 HOLD DRAFT (vs claim "7/7 milestone")
  - Pattern adoption findings sintetici
- `STATUS_MULTI_REPO.md` sezione 6: aggiornare stesso state
- ADR-0026 (se creato): linkato qui come pattern A2 outcome

---

## 8. Provenance

- AA01 workspace task: `2026-05-aa01-002-2026-05-11-vault-integration-readonly`
- DRAFT integrali: `C:/Users/edusc/aa01/workspace/2026-05-aa01-002-*/DRAFT/00-04-*.md`
- Decision audit log: `C:/Users/edusc/aa01/workspace/2026-05-aa01-002-*/decisions.md` (D-001 Phase 5 pivot)
- Plan integration: `docs/archive/plans/integration-aa01-vault-hyperspace-2026-05.md` Obiettivo 2 (completion)
- Session: 2026-05-11, 8gg residui pre-Claude Max 19/05
- Tier strategic: Claude Max attivo (cross-source synthesis 5 pattern decisions = Tier 0 ADR-0023 applicable)

---

## 9. Autoresearch revised decisions (multi-source synthesis post Eduardo "auto modo + archon aa01 + autoresearch core")

### Methodology applicata

Memory `feedback_autoresearch_default.md` enforce multi-source > 1 + parallel + synthesis (NON one-shot README) per decisioni significative. Pre-Phase 5 implementation, applicato 4-source synthesis:

1. **Vault CLAUDE.md** § Quality Gate (3-step: Smoke + Research + Tuning)
2. **Codemasterdd ADR-0018** agent-readiness-protocol (3-gate: Smoke + Ricerca + Tuning, pubblicato 2026-04-24)
3. **`.claude/agents/README.md`** status matrix + cita link `SMOKE_TEST_TEMPLATE.md`
4. **Filesystem check codemasterdd**: `SMOKE_TEST_TEMPLATE.md` **NON ESISTE** (gap 17gg)

### Finding 1 -- Pattern A2 REDUNDANT (decision pivot)

ADR-0018 (2026-04-24) ha già 3-gate identico al Quality Gate vault (vault created stessa data, milestone 2026-05-10). Convergenza temporale + scope similare = **duplicate avoid**.

**Originale**: TENTATIVE ADOPT → crear ADR-0026 sub-agent-quality-gate
**Revised**: **SKIP** → no nuovo ADR (governance bloat avoid)

**Differenza sottile NOT actioned**: vault Step 2 = "≥3 edge case formal in docs/research/", ADR-0018 Gate 2 = sources/licenses/framework validation. Reactivation trigger: addendum ADR-0018 se gap edge-case formal emerge concreto (NON nuovo ADR).

### Finding 2 -- Pattern B EXPAND scope (chiude gap esistente)

ADR-0018 (riga 175+202-208) promette `.claude/agents/SMOKE_TEST_TEMPLATE.md` con prompt prescriptive + output validation checklist + tuning iteration pattern. **File mai creato** (gap ~17gg 2026-04-24 → 2026-05-11).

Vault pattern strutturale informa COME chiudere il gap:
- Body sections: `## Ruolo` / `## Input` / `## Processo` (≤7) / `## Output` / `## Edge case` / `## Quality Gate Step 1 smoke test`
- Smoke test block in body (NOT frontmatter, evita sync drift osservato in vault stesso)

**Originale**: ADOPT → 1 file SUB_AGENT_TEMPLATE.md
**Revised**: **EXPAND ADOPT** → 2 file:
- `SMOKE_TEST_TEMPLATE.md` (PR atomic 2, chiude gap esistente ADR-0018)
- `SUB_AGENT_TEMPLATE.md` (PR atomic 3, scaffolding nuovo agent)

### Validation enforcement

Memory `feedback_autoresearch_default.md` 8-step checklist: 8/8 compliant (vedi DRAFT 04 sez 6 per breakdown). Case-study positivo: ~30min autoresearch ha salvato creazione ADR-0026 duplicato + identificato gap esistente da chiudere = double-win efficiency + correttezza.
