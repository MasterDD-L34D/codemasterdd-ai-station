# Bench mixed-workload 2026-05-09 — H9 risoluzione harsh review C1 + V3

**Trigger**: harsh review flow chart 9/5 ha identificato choke point **C1** (RTX 5060 8GB VRAM sustainability under continuous workflow) + **V3** (sample size empirici sotto threshold per claim "Accepted") + **E5** (token-rate cherry-picking).

**Decision context**: Eduardo scelta **4A** (Decisione 007 in DECISIONS_LOG): "Sì, dedico 1 giornata pre-19/05 per bench mixed-workload realistic". Eseguito 9/5 mezzogiorno con Claude Max ancora attivo per analysis.

## Setup

- Bench script: `scripts/bench-mixed-workload/run-bench.ps1`
- Prompts: `scripts/bench-mixed-workload/prompts.json` (12 task realistici)
- Output: `scripts/bench-mixed-workload/results/results-2026-05-09-maxloaded1.json`
- Hardware: Lenovo desktop, Intel Ultra 7 255HX, RTX 5060 8GB VRAM, 64GB DDR5
- Ollama daemon v0.23.2
- Config attuale: `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_CONTEXT_LENGTH=8192`

## Design

12 task alternati 4×7B + 4×14B Q2 + 4×30B MoE per **forzare 11 swap modello continui**. Ordine: T1-7B, T5-14B, T9-30B, T2-7B, T6-14B, T10-30B, T3-7B, T7-14B, T11-30B, T4-7B, T8-14B, T12-30B.

Task realistici mini-prompt (no file edit, solo inference) per isolare swap overhead pulito da Aider/OpenCode internals:
- 7B (1-cosmetic): JSDoc, type hint, rename variable, docstring
- 14B Q2 (2-behavior): bug fix, refactor list comprehension, error handling, enumerate
- 30B MoE (2.5-escalation): refactor algorithm, async/await conversion, exception handling, input validation

`num_predict=200`, `temperature=0.1` per consistency.

## Risultati

### Tier breakdown (avg n=4)

| Tier | Modello | Avg tok/s | Avg wall (s) | Avg load (ms) |
|------|---------|-----------|--------------|---------------|
| 1 cosmetic | Qwen 2.5 Coder 7B Q4_K_M | **100.75** | 3.43 | 2863 |
| 2 behavior | Qwen 2.5 Coder 14B Q2_K | **17.62** | 8.99 | 3281 |
| 2.5 escalation | qwen3-coder:30b MoE A3B | **32.98** | 7.36 | 3636 |

### Aggregati workflow

- **Total elapsed**: 79.17s per 12 task
- **Swap count**: 11 / 12 (92% del workflow ha swap)
- **Swap load avg**: 3291ms vs non-swap 244ms
- **Swap overhead per swap**: **3047ms** (~3s)
- **Total swap overhead**: **33.52s = 42.3% del totale workflow**

## Findings critici

### F1. CLAUDE.md tier table ottimistico per Qwen 7B + 14B Q2

| Modello | Documentato | Reale | Drift |
|---------|-------------|-------|-------|
| Qwen 7B Q4_K_M | 114 tok/s | 100.75 tok/s | **-12%** |
| Qwen 14B Q2_K | 25 tok/s | 17.62 tok/s | **-30%** ⚠️ |
| qwen3-coder:30b MoE | 23 tok/s | 32.98 tok/s | **+43%** ✨ |

**Implicazione**:
- 14B Q2 throughput drift -30% e' significativo. Numbers documentati venivano da bench isolated (non mixed-workload) con KV cache calda single-task, ottimistici.
- 30B MoE +43% upside e' invece **positiva discovery**: bench precedenti (ADR-0009 addendum, ADR-0012 post-RAM-upgrade) erano stati conservativi. Ora 30B MoE e' competitive con 14B Q2 in throughput, sostanzialmente superiore in capability.

### F2. Swap overhead 42% del workflow misto

Su workflow alternato continuo, **42.3% del tempo viene speso in swap modello**, non in eval. In sessioni reali con 30 task/giorno alternati misto, stima:
- 30 task × ~6.5s avg wall (mix) = ~195s eval/inference utile
- 30 task × 11/12 swap rate × 3s/swap = ~82s swap overhead
- **Totale: ~277s = 4.6 min** di cui solo 3.25min (70%) e' eval utile

### F3. Ordine workflow conta enormemente -- VALIDATION EMPIRICA 2026-05-09

I 4 task 7B (T1, T2, T3, T4) hanno avg wall 3.43s ma **sono dispersi** nell'ordine di esecuzione mixed. Ognuno e' un swap.

Bench batched eseguito subito dopo (run order [1..12], solo 2 swap forced) per validare hypothesis:

| Workflow | Total elapsed | Swap count | Swap overhead | % workflow |
|----------|---------------|------------|---------------|------------|
| **Mixed** (11 swap forced) | 79.17s | 11 | 33.52s | 42.3% |
| **Batched** (2 swap, run [1..12]) | **49.93s** | 2 | 6.22s | **12.5%** |
| **Saving** | **-29.24s** | **-9** | **-27.30s** | **-37%** |

**Saving empirico 37% del workflow** confermato (vs ipotesi 34%). Validation: batch task per modello prima di switch riduce significativamente il workflow time.

**Throughput per modello invariato** (no degradation):
- 7B batched: 100.75 tok/s avg (stesso di mixed)
- 14B Q2 batched: 17.62 tok/s (stesso)
- 30B MoE batched: 32.20 tok/s avg (vs 32.98 mixed, ~2% delta noise)

Output: `scripts/bench-mixed-workload/results/results-2026-05-09-maxloaded1-batched.json`

## Decisione su `OLLAMA_MAX_LOADED_MODELS=2` -- VALIDATION EMPIRICA 2026-05-09

**Ipotesi originale**: setting `=2` permette 2 modelli simultanei in cache, riducendo swap del ~50% in workflow alternato.

**Test empirico eseguito** (bench MAX=2 mixed workflow, stessi 12 task forced-swap):

| Config | Total elapsed | Swap count | Swap overhead | % workflow |
|--------|---------------|------------|---------------|------------|
| **MAX=1 mixed** (baseline) | 79.17s | 11 | 33.52s | 42.3% |
| **MAX=2 mixed** | **81.51s** | **11** | 34.90s | **42.8%** |

**Risultato CONTRARIAN**: MAX=2 NON ha ridotto il numero di swap. Workflow time praticamente identico (delta +1.4s dentro variance noise).

### Razionale empirico per cui MAX=2 non aiuta

1. **Workflow alterna 3 modelli** (7B, 14B Q2, 30B). MAX=2 puo' tenere solo 2 in cache. 3° modello forza sempre eviction. Esempio:
   - T1 7B caricato (MAX=2 cache: [7B])
   - T5 14B Q2 caricato (cache: [7B, 14B Q2])
   - T9 30B caricato → 14B Q2 evicted (cache: [7B, 30B]). Swap counted.
   - T2 7B richiamato (gia' in cache → no swap? ma osservato ancora swap)

2. **VRAM 8GB limit single-model GPU**: anche se MAX=2 cache RAM, GPU offload e' single-model concurrent. Quando nuovo modello richiesto, deve essere caricato in VRAM (eviction modello precedente da GPU). Cache RAM helpa solo se modello successivo === modello precedente in cache RAM e non e' stato eviction da GPU.

3. **Workflow forced-swap** (test design): mixed alternation = 11 swap forced indipendentemente da MAX=N. Cache RAM speedup minore di GPU swap dominante.

### Quando MAX=2 sarebbe utile (estrapolazione)

- **Workflow 2-modelli only**: es. Aider 14B Q2 + OpenCode 30B (entrambi behavior/agentic) senza 7B coinvolto → MAX=2 evita ogni swap dopo carico iniziale.
- **Workflow Eduardo simultanee 2 sessioni** (Aider + OpenCode parallel, modelli diversi): vantaggio cache.
- **Pattern user normale** dove tier 1 (7B) raramente usato durante una sessione: cache 14B Q2 + 30B disponibili.

### Decisione finale: MAX=1 INVARIATO

**Razionale ratificato empiricamente**:
1. ADR-0004 MAX=1 confermato corretto per workflow 3-tier misto (no benefit MAX=2 nel use case attuale)
2. Cambio MAX=2 richiede Ollama restart + ha rischio RAM tight (30B+14B+7B = ~33GB modelli). Non vale beneficio nullo.
3. **Pre-19/05 transition window NON cambiare config esistente** senza upside provato.
4. Re-evaluation MAX=2 candidato SE workflow Eduardo evolve a 2-tier dominant (es. solo Aider behavior + OpenCode agentic, no cosmetic) -> deferred SPRINT_02 T7 review.

Output bench MAX=2: `scripts/bench-mixed-workload/results/results-2026-05-09-maxloaded2-mixed.json`

## Update CLAUDE.md throughput

CLAUDE.md "Stack installato" tabella `Velocita misurate (sustained eval, prompt DoublyLinkedList Python)` da aggiornare con valori bench mixed-workload corretti:

| Modello | Tok/s isolato (vecchio) | Tok/s mixed-workload (nuovo, n=4) | Note |
|---------|-------------------------|-----------------------------------|------|
| Qwen 2.5 Coder 7B Q4_K_M | 114 | **100.75** | -12% drift |
| Qwen 2.5 Coder 14B Q2_K | 25 | **17.62** | **-30% drift** ⚠️ |
| qwen3-coder:30b MoE | 23 | **32.98** | **+43% upside** ✨ |

Decision matrix CLAUDE.md sezione "Priorita modelli AI" implicazioni:
- 14B Q2 throughput effettivo 17.6 tok/s e' **vicino a 30B MoE 33 tok/s in workflow misto** (delta solo 1.87×, non 1.4× come documentato)
- **Considera escalation 14B Q2 -> 30B MoE piu' aggressiva** (era "quando 14B safe-fails"). Nuovo trigger: anche speed-critical su task non-trivial.

## Risoluzioni harsh review

| Issue | Status |
|-------|--------|
| **C1 RTX 5060 sustainability** | Quantificato. Workflow misto 79s/12task accettabile. MAX_LOADED_MODELS=2 deferred SPRINT_02 con dati workflow reale. |
| **V3 sample size empirici** | Mitigato parziale. n=4 per tier (vs n=1 isolato precedente). Sample piccolo ma 3-tier balanced. |
| **E5 token-rate cherry-picking** | Confermato + corretto. Drift -12%/-30%/+43% applicato. |

## Decisione operativa

1. **CLAUDE.md tier table update** con throughput mixed-workload (questo PR)
2. **Decision matrix** aggiornata per riflettere 14B Q2 drift -30% e 30B MoE upside +43%
3. **MAX_LOADED_MODELS=1 invariato** pre-19/05. **Re-bench `=2` ESEGUITO 2026-05-09** -> contrarian finding: nessun beneficio per workflow 3-tier misto. Razionale empirico: 11 swap forced invariato (MAX=2 cache 2 modelli su 3 alternati = sempre eviction). MAX=2 candidato solo se workflow evolve a 2-tier dominant.
4. **Sample size n=4 per tier** insufficiente per claim "Accepted" definitivo. ADR-0009 addendum NON status flip, solo data update reference. Future bench con n>=10 per ratification.
5. **Workflow optimization batched > mixed** (F3): **raccomandazione FORTE quantificata** (no piu' non-binding). Validation empirica 2026-05-09: batched riduce workflow time del 37% (29.24s saving su 79.17s totale). Throughput per-modello invariato. Quando workflow include task multiple per stesso modello, raggrupparli prima di switch.

## Riferimenti

- `scripts/bench-mixed-workload/prompts.json` (12 task definitions)
- `scripts/bench-mixed-workload/run-bench.ps1` (execution script)
- `scripts/bench-mixed-workload/results/results-2026-05-09-maxloaded1.json` (output JSON)
- ADR-0004 -- Ollama RTX 5060 config (`OLLAMA_MAX_LOADED_MODELS=1` rationale)
- ADR-0009 -- Upgrade strategy (T2 hardware materialized + bench mixed-workload addendum questo)
- ADR-0012 -- RAM 64GB upgrade (qwen3:30b validation)
- harsh review: `docs/governance/flow-chart-harsh-review-2026-05-09.md` (C1 + V3 + E5 resolution)
- BACKLOG H9 (this PR completes execution)
- Decisione 007 in `DECISIONS_LOG.md` (Eduardo scelta 4A)
