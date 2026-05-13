# ADR-0028 — Tier promotion methodology cross-pattern Quality Gate Step 2

## Status

**Proposed** 2026-05-13 notte tarda — auto-mode Eduardo override defer SPRINT_02+ Three Strikes trigger (V3 Bundle 2 research REC 4 originally DEFER). Adoption formal pending Accepted ratification empirical (Three Strikes condition documented sotto).

## Context and Problem Statement

### Genesis

V3 Bundle 2 research doc 2026-05-12 sera (`docs/research/model-routing-quality-gate-cross-pattern-2026-05-12.md`) ha identificato gap empirical tra:

- **Vault Quality Gate workflow** (sibling-peer reference): 3-step Smoke -> Research -> Tuning + folder-move smoke -> draft -> production + before/after metric empirical (es. ollama-dispatcher v1 -91% wall claim)
- **codemasterdd code-edit routing** (ADR-0007 + ADR-0008 + ADR-0016 + ADR-0022): tier matrix code-edit ma NO Quality Gate formal pre-promote nuovo modello/wrapper

### Empirical evidence gap impact

**ADR-0008 silent-corruption deterministic discovery (2026-04-22)**: reactive, NON identificata pre-promote 14B in routing. Se Step 1 SMOKE formal con fixture "edit single file con docstring header self-ref" era stato applicato pre-promote, silent-corruption sarebbe stato identificato earlier. Cost: 1 dogfood real-task corruption (recovered git reset) + ADR-0008 retro-formalization effort.

**ADR-0022 OpenCode tool-use discovery (2026-05-09)**: proactive via bench n=3 PRE-promote (`scripts/bench-opencode-cloud-free.ps1`). Methodology piu' Step-2-like rigorous, validation positive. Pattern ADR-0022 piu' rigorous di ADR-0008 = empirical proof Quality Gate adoption value.

### Cross-pattern adoption gap

V3 audit ha identificato 3 gap formal:

1. **NO formal Step 1 fixture**: dogfood task reale e' situational, NON replicable fixture standard
2. **NO Step 2 multi-edge-case explicit**: dogfood n>=11 e' organic, NON forced 3+ edge case per claim
3. **NO Step 3 before/after metric target**: ratification non specifica metric target a priori (es. silent-corruption rate < threshold X)

Risk se NON adopted: future tier promotion (es. nuovo model Ollama / nuovo wrapper Aider) ripete ad-hoc validation, possible regression (silent-corruption tipo ADR-0008 ripetibile).

## Decision

**Adopt Quality Gate 3-step methodology adapted code-edit context** per future tier promotion decisions. Mapping content-routing -> code-edit (NON blind copy):

### Step 1 SMOKE codemasterdd-mapped

**Input**: fixture task standard per tier candidate (cosmetic/behavior, single-file).

**Expected outputs**:
- PASS 1st-try
- `git diff HEAD` verified (no silent-corruption)
- Commit message Conventional Commits compliant
- No working-tree pollution (deletions non requested, etc.)

**Idempotency check**: re-run stesso fixture deve produrre stesso diff (deterministic) OR substantially equivalent (LLM stochasticity tolerated, semantic equivalence verified manual).

**File location**: `scripts/quality-bench/tier-promotion-smoke/` (NEW directory).

**Effort setup**: 2-4h (3-5 fixture standard: JSDoc one-liner, refactor 1-file logic change, multi-constraint count = 3, multi-constraint count = 5 edge case, subdir + docstring self-ref ADR-0008 case).

### Step 2 RESEARCH codemasterdd-mapped

**Edge cases >= 3** mandatory:
- Subdir profonda + docstring self-ref (ADR-0008 regression test)
- Multi-constraint count = 5 (ADR-0016 boundary saturation)
- File con character encoding mixed (cp1252 trigger condition, H3 BACKLOG)

**Metrics empirical** (codemasterdd-specific, NON content-routing):
- **silent-corruption rate**: % diff con working-tree corruption non requested (target: 0%)
- **retry rate**: % task PASS 2nd-try o oltre (target: <20%)
- **tok/s sustained** post warmup (informational, NOT promote-criterion blocker)
- **constraint-count tolerance**: n max constraint con PASS-rate >80% (per ADR-0016 2D matrix)

**File location**: `docs/research/tier-<name>-quality-gate-<date>.md` (existing convention bench-*.md / vault-patterns-*.md).

**Effort per tier candidate**: 1-2h (n=3 edge case + metric collection + interpretation).

### Step 3 TUNING codemasterdd-mapped

**Metric before/after target empirical** (a priori, NOT post-hoc):
- Tier candidate vs incumbent (es. promote qwen3-coder:30b vs qwen2.5-coder:14b-q2 incumbent)
- Target acceptance criteria:
  - silent-corruption rate <= incumbent
  - retry-rate equivalent or better (within +5%)
  - tok/s reasonable per use case
  - constraint-count tolerance NOT regressed

**Folder-move equivalent codemasterdd**: ADR Proposed (Step 2 research output) -> ADR Accepted via ratification 30gg default (ADR-0010 process).

**File location**: ADR addendum con metric tracked + commit con metric in message (es. "promote qwen3-coder:30b tier 1: silent-corruption 0/n=5 + retry 1/5 + tok/s 32.98 mixed").

## Application protocols (when to use)

### Trigger: nuovo tier candidate

Ogni volta che si valuta promozione di **nuovo modello / nuovo wrapper / nuovo tier**:
- Nuovo modello Ollama (es. emerge qwen4-coder:30b post-2026-Q3)
- Nuovo wrapper Aider configuration (es. aider-deepseek-r1-32b se applicabile)
- Nuovo provider cloud (es. Cerebras paid tier llama3.3-70b se budget allocation cambia)
- Nuovo OpenCode tool-use model

### NON applicare (skip)

- Aggiornamento minor di tier esistente (patch version Ollama, settings tuning)
- Configurazione operativa (env var change, num_ctx adjustment)
- Bug fix wrapper esistente (no new tier introduced)

### Workflow application step-by-step

```
1. Identify tier candidate + use case (es. tier 1 cosmetic / tier 2 behavior)
2. Step 1 SMOKE: run 3-5 fixture standard from scripts/quality-bench/tier-promotion-smoke/
   - Pass: continue Step 2
   - Fail: abort promotion + document failure pattern
3. Step 2 RESEARCH: 3+ edge case + metric collection
   - Output: docs/research/tier-<name>-quality-gate-<date>.md
4. Step 3 TUNING: before/after metric vs incumbent
   - If target met: ADR Proposed with metric in body
   - If target NOT met: skip promotion or escalate ADR with reasoning
5. ADR ratification 30gg default (ADR-0010 process)
```

## Consequences

### Positive

- **Proactive silent-corruption prevention**: Step 1 SMOKE fixture standard cattura ADR-0008-like regression PRE-promote (not REACTIVE post)
- **Multi-edge-case rigor**: Step 2 RESEARCH N>=3 elimina single-data-point promote (ad-hoc validation gap V3 #1)
- **Before/after target empirical**: Step 3 TUNING richiede metric explicit (ad-hoc validation gap V3 #3)
- **Empirical reproducibility**: fixture standard + edge case + metric documented = future-session replicable validation
- **Cross-pattern reference**: vault Quality Gate Step 2 methodology + codemasterdd ADR-0022 process aligned = single mental model future tier work
- **Compatibility con stop pattern L-002**: methodology applied ONLY at tier promotion trigger, NOT continuous audit churn

### Negative / Trade-offs

- **Setup cost**: 2-4h scripts/quality-bench/tier-promotion-smoke/ fixture setup (one-time)
- **Per-promotion effort overhead**: ~3-5h per Quality Gate cycle vs ad-hoc ~1h (NON applicato per minor changes)
- **Risk over-engineering**: se fixture diventano stale o eccessive, methodology cost > value (L-002 anti-pattern). Mitigation: fixture set minimo + review periodico.
- **Stochastic LLM tolerance**: idempotency check Step 1 deve essere "semantic equivalence" NOT bit-exact (LLM non-determinism). Mitigation: tolerance documented in fixture spec.

### Reversibility

ADR Proposed status reversible. Se Accepted ratification fails (empirical evidence shows methodology cost > value), ADR addendum REJECTED + revert ad-hoc dogfood pattern. NON architectural lock-in.

## Ratification

### Trigger Accepted (Three Strikes condition, V3 REC 1 default)

ADR-0028 transition Proposed -> Accepted **require** 3 empirical evidence per pattern reinforcement:

1. **1 regress reale tier promotion ad-hoc** durante SPRINT_02+ (silent-corruption non identificato pre-promote, OR retry rate spike post-promote)
2. **1 successful manual Quality Gate application** (3-step seguito su tier candidate + outcome positive empirico)
3. **1 emergent tier promote request** (new model rotation o wrapper variant emerge da real-use)

Se 3/3 met entro 2026-Q3: ADR Accepted + apply forward.

### Trigger Skip (Default disposition)

Se 3/3 NON met entro 2026-Q4: ADR REJECTED + ad-hoc dogfood pattern continued (current state pre-ADR-0028).

### Trigger Hard-Accept (override Three Strikes)

Se ADR-0008-like silent-corruption regression occurs durante SPRINT_02+ post tier promotion AD-HOC (NON Quality Gate), ADR-0028 promoted Accepted immediato per prevention.

## References

- V3 Bundle 2 research doc 2026-05-12 sera: `docs/research/model-routing-quality-gate-cross-pattern-2026-05-12.md` (305-line analysis + 4 REC)
- vault llm-routing v1.0: `C:/dev/vault-shared/Extras/config/llm-routing.json` (post R5 fix HEAD `1abaa743`)
- vault Quality Gate research: `C:/dev/vault-shared/docs/research/` (5 report 2026-05-10 dated)
- codemasterdd MODEL_ROUTING: `MODEL_ROUTING.md` (305 righe, sezione "Tier promotion methodology" da aggiungere post-Accepted)
- ADR-0007 Aider Qwen quantization findings (empirical sweet spot Step-2-like, retro-Quality-Gate-mapped)
- ADR-0008 Aider whole format silent-corruption (Step 1 SMOKE gap regression case study)
- ADR-0016 constraint-count routing dimension (Step 2 multi-edge-case empirical n>=11)
- ADR-0022 OpenCode tool-use routing (process Step-2-rigorous validation case study)
- ADR-0026 cognitive workflow protocols (P1 Refresh-verify + P2 Autoresearch applied this ADR)
- Memory `project_vault_shared.md` (sibling-peer + cross-pattern reference candidate)
- Bundle 2 reflexive companion: `docs/research/adr-0026-effectiveness-reflexive-audit-2026-05-12.md`
- Lesson L-2026-05-014 (autoresearch first pattern, complement methodology adoption)

## Notes

- ADR drafted Eduardo override defer SPRINT_02+ trigger (V3 REC 4 originally DEFER). Justification: 6gg residui pre-Max, Opus depth Available, ADR document writing benefit from Opus quality drafting vs sovereign tier.
- Sub-agent ecosystem applicability (ADR-0018): Quality Gate Step 1+2+3 mapping potenzialmente applicabile a sub-agent promotion (12/18 ready, 6/18 draft). Out-of-scope this ADR (focus tier model routing), future ADR-0028 addendum se sub-agent promotion follows same pattern.
- MODEL_ROUTING.md section "Tier promotion methodology" formal write deferred a post-Accepted (REC 2 V3 audit). Effort 30-45min, trigger natural quando ADR Accepted.
- ASCII-first body prose (ADR-0021), em-dash em-dash conventionally used in titoli + section dividers acceptable per convention progetto.
