# MODEL_ROUTING -- Quality Gate cross-pattern adoption research

> **Audit data**: 2026-05-12 sera (Bundle 2 methodological audit V3)
> **Sources**:
> - vault-shared `Extras/config/llm-routing.json` (sibling-peer, read-only spot-check)
> - codemasterdd `MODEL_ROUTING.md` (305 righe corrente)
> - ADR-0007 + ADR-0008 + ADR-0016 + ADR-0022 (routing decisions empirical)
> - Memory `project_vault_shared.md`
> **Scope**: research doc NON committed-decision, valutare candidate adoption Quality Gate methodology per codemasterdd code-edit routing

## TL;DR

Vault Quality Gate methodology (3-step Smoke -> Research -> Tuning) e' applicata content-routing (15 task-type vault). Codemasterdd MODEL_ROUTING ha tier matrix code-edit ma NON Quality Gate formale per validation pre-promote nuovo modello/wrapper in routing.

**Empirical evidence**: ADR-0008 Aider 14B Q2 sweet spot + ADR-0022 OpenCode qwen3:30b sono entrati in routing tramite **ad-hoc dogfood** (n>=1 PASS + manual review), NON tramite Quality Gate formal 3-step.

**Cross-pattern adoption proposal**: MODEL_ROUTING addendum future "Tier promotion methodology" allinea con Quality Gate Step 2 rigor (multi-test + edge case + before/after metric). NON adoption blind, mapping codemasterdd-specific (silent-corruption rate + retry rate + tok/s + constraint-count tolerance).

**Risk** se NON adopted: future tier promotion (es. nuovo model Ollama / nuovo wrapper Aider) ripete ad-hoc validation, possible regression (silent-corruption tipo ADR-0008 ripetibile).

**Mitigation candidate**: ADR-NEW oppure MODEL_ROUTING.md sezione "Tier promotion methodology" formalize 3-step adapted.

## Methodology empirical analysis

### Vault Quality Gate workflow (sibling-peer reference)

**Step 1 SMOKE** (vault):
- Input fixture + expected output + idempotency check
- Lightweight pass-fail per ogni edge case primario
- File location: per-agent script smoke `production/agents/<name>.md` body section

**Step 2 RESEARCH** (vault):
- Multi-edge-case >=3 cases con frontmatter `quality_gate_step: 2`
- Methodology rigorous: split metrics (cold_load_s + inference_s + wall_s) + keep_alive=-1 + retries con exponential backoff + output validation (word count + retry stricter prompt)
- File location: `docs/research/<component>-<date>.md`
- Esempio empirical: 5 research report agents 2026-05-10 (dispatcher, design-watcher, ingestor, pathfinder-pdf-indexer, vault-linter)

**Step 3 TUNING** (vault):
- Metric before/after target empirical (es. ollama-dispatcher v1 -91% wall, vault-ingestor v2 conflict recall 67->100%)
- Folder-move smoke -> draft -> production concretizza promotion
- File location: per-agent script + commit con metric in message

### Codemasterdd code-edit routing (current state)

**Tier promotion pattern empirical** (ADR-0007/0008/0009/0016/0022):

| Step | Cosa fa | Quality Gate equivalente |
|------|---------|--------------------------|
| **Dogfood pre-promote** | n>=1 task reale con classification (cosmetic/behavior) + classe (whole/diff) + outcome (PASS 1st-try / retry / REJECT / silent-corruption) | Step 1 SMOKE (fixture = task reale, output = git diff, idempotency = re-run) |
| **Constraint-count classification** | OD-006 -> ADR-0016 Proposed: 2D matrix (classe x constraint-count). n>=11 dogfood empirical | Step 2 RESEARCH parziale (multi-edge-case + metric empirico) |
| **ADR Proposed -> Accepted ratification** | 30gg post-Proposed default Accept se non-trigger evaluation | Step 3 TUNING parziale (metric assessed post-period, no explicit before/after target) |

**Gap identified**:
1. **NO formal Step 1 fixture**: dogfood task reale e' situational, NON replicable fixture standard
2. **NO Step 2 multi-edge-case explicit**: dogfood n>=11 e' organic, NON forced 3+ edge case per claim
3. **NO Step 3 before/after metric target**: ratification non specifica metric target a priori (es. silent-corruption rate < threshold X)

### Empirical evidence gap impact

**ADR-0008 silent-corruption deterministic discovery (2026-04-22)**:
- Dogfood #4 first reveal silent-corruption Aider 14B Q2 whole format
- Discovery REACTIVE, NON identificata pre-promote 14B in routing
- Se Step 1 SMOKE formal con fixture "edit single file con docstring header self-ref" + diff verification + idempotency check fosse stato applicato pre-promote, silent-corruption sarebbe stata identificata earlier
- **Cost**: 1 dogfood real-task corruption (recovered via git reset, no actual code lost) + ADR-0008 retro-formalization effort

**ADR-0022 OpenCode tool-use discovery (2026-05-09)**:
- Bench n=3 PRE-promote (Test runner `scripts/bench-opencode-cloud-free.ps1` + ADR research)
- Discovery PROACTIVE: rate-limit cloud free + qwen 2.5 family JSON raw NON eseguito identificate pre-routing
- Methodology piu' Step-2-like (multi-test + metric), validation positive

**Lesson**: ADR-0022 process e' piu' rigorous di ADR-0008. Quality Gate adoption formalize il pattern ADR-0022 come standard.

## Cross-pattern mapping proposta

### Step 1 SMOKE codemasterdd-mapped

**Input**: fixture task standard per tier candidate (cosmetic/behavior, single-file)
**Expected**: PASS 1st-try + diff verified + no silent-corruption + commit-msg conventional
**Idempotency**: re-run stesso fixture deve produrre stesso diff (deterministic) OR sub-stantially equivalent (LLM stochasticity tolerated)

**File location**: `scripts/quality-bench/tier-promotion-smoke/` (new dir, NON esistente)
**Effort setup**: 2-4h (fixture standard 3-5 task: JSDoc, refactor 1-file, multi-constraint 2-3)

### Step 2 RESEARCH codemasterdd-mapped

**Edge cases >= 3**:
- Subdir profonda + docstring self-ref (ADR-0008 lesson)
- Multi-constraint count = 5 (ADR-0016 boundary)
- File con character encoding mixed (cp1252 trigger condition)

**Metrics empirical** (codemasterdd-specific):
- silent-corruption rate (% diff con working-tree corruption non requested)
- retry rate (% task PASS 2nd-try o oltre)
- tok/s sustained (post warmup)
- constraint-count tolerance (n max constraint PASS-rate >80%)

**File location**: `docs/research/tier-<name>-quality-gate-<date>.md` (esistente convention)

### Step 3 TUNING codemasterdd-mapped

**Metric before/after**:
- Tier candidate vs incumbent (es. promote qwen3-coder:30b come tier 1 vs qwen2.5-coder:14b-q2 incumbent)
- Target empirical: silent-corruption < incumbent + retry-rate equivalent + tok/s reasonable

**Folder-move equivalent**: ADR Proposed -> Accepted via ratification 30gg

**File location**: ADR addendum con metric tracked + commit con metric in message

## Recommendations

### REC 1 -- NO adoption blind, proposed ADR formalize

**Decisione**: NON adottare vault Quality Gate methodology blind. Codemasterdd ha pattern empirical proprio (ADR-0008/0022 reactive vs proactive), Quality Gate mapping richiede formalization ADR.

**ADR-NEW candidate** (NON urgent): "Tier promotion methodology cross-pattern Quality Gate Step 2" formalize Step 1/2/3 mapping.

**Trigger ADR draft**: post 1 successful application empirical (es. promote-NEW-tier task in SPRINT_02+) o post 1 silent-corruption regression che richiede metodology piu' formal.

### REC 2 -- MODEL_ROUTING.md sezione future "Tier promotion methodology"

Aggiungere sezione (50-80 righe) in MODEL_ROUTING.md che documenta:
- Quality Gate 3-step adapted per code-edit (Step 1/2/3 sopra)
- Cross-link vault llm-routing.json + Quality Gate Step 2 inspirational source
- Empirical evidence ADR-0022 process compliant (case study positive)
- Empirical evidence ADR-0008 gap (case study negative pre-formalize)

**Effort scrittura**: 30-45min
**Trigger application**: NEXT tier promotion (post-Max scenario A operativo, qwen3-coder:30b o nuovo model emergent)

### REC 3 -- Cross-link memoria + ADR-0007/0008 retro-note

**Memoria** `project_vault_shared.md`: gia' contiene "Cross-pattern reference candidate" sezione. Aggiungere note "REC 1/2 V3 audit 12/5 sera -> ADR-NEW candidate".

**ADR-0007 + ADR-0008 retro-note** (opzionale): se ADR-NEW draft viene aperto, addendum minor ADR-0007/0008 con "post-hoc Quality Gate Step 1 mapping" per reference future.

### REC 4 -- Defer formal adoption fino post-Max scenario A operativo

ADR-0026 lesson "stop pattern audit fino post-Max" applies. Quality Gate adoption formal e' valore cross-session ma NON urgent pre-19/05. Trigger draft post 2026-05-20+ quando SPRINT_02 T2/T5/T7 empirical evidence emerge.

## Conclusioni

Vault Quality Gate methodology e' rigorous + cross-pattern candidate. Adoption codemasterdd-side richiede mapping content-routing -> code-edit context (NON blind copy). Empirical evidence supporta value (ADR-0008 silent-corruption regress prevention possible se Step 1 SMOKE formal era stato applicato pre-promote 14B).

**Decision**: NON adoption immediata. ADR-NEW candidate future post Three Strikes trigger (1 regress + 1 successful manual application + 1 emergent tier promote request). DEFER fino SPRINT_02+.

## Cross-link

- vault llm-routing v1.0: `C:/dev/vault-shared/Extras/config/llm-routing.json`
- vault Quality Gate research: `C:/dev/vault-shared/docs/research/` (5 report 2026-05-10 dated)
- codemasterdd MODEL_ROUTING: `MODEL_ROUTING.md` (305 righe, sezione "Research input esterno" 2026-05-10 update)
- ADR-0007 Aider Qwen quantization findings (empirical sweet spot Step-2-like)
- ADR-0008 Aider whole format silent-corruption (gap analysis Step 1 SMOKE retro)
- ADR-0016 constraint-count routing dimension (Step 2 multi-edge-case empirical n>=11)
- ADR-0022 OpenCode tool-use routing (process Step-2-rigorous validation)
- Memory `project_vault_shared.md` (sibling-peer policy + cross-pattern reference candidate)
- Bundle 2 reflexive companion: `docs/research/adr-0026-effectiveness-reflexive-audit-2026-05-12.md`
