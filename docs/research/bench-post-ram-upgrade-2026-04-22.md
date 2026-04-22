# Bench post-RAM-upgrade 2026-04-22

> Benchmark empirico eseguito dopo upgrade RAM 16 GB → 64 GB DDR5-5600 dual channel. Scopo: verificare se `OLLAMA_CONTEXT_LENGTH=8192` (scelto in ADR-0007 Test 1 con 16 GB RAM) resta ottimale, misurare escalation ctx per modelli tier 2, valutare candidato Qwen 2.5 Coder 32B dense.

## Metodologia

### Hardware
- CPU: Intel Core Ultra 7 255HX (24 core Arrow Lake HX)
- GPU: NVIDIA RTX 5060 8 GB VRAM (Blackwell sm_120, driver 595.79, CUDA 13.2)
- **RAM: 64 GB DDR5-5600 dual channel** (2×32 GB Micron CT32G56C46S5.C16D) — upgrade 2026-04-22
- Ollama 0.21.0
- Env vars Ollama attive: `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_KEEP_ALIVE=30m`

### Prompt standard
Per tutti i run, prompt identico (ricostruito dal contesto ADR-0007):

```
Write a Python implementation of a doubly-linked list class named DoublyLinkedList.
Include these methods: insert_head(value), insert_tail(value), delete_by_value(value),
find_by_value(value) returning the node or None, and __str__ for readable string
representation. Add a docstring to each method explaining its purpose, parameters,
and return value. Use type hints.
```

Parametri Ollama runtime:
- `stream: false`
- `num_predict: 300` (target output length per misura stabile sustained eval)
- `temperature: 0` (determinismo massimo)
- `num_ctx: variabile per run`

### Metriche estratte
Dal response JSON `POST /api/generate`:
- `prompt_eval_count` / `prompt_eval_duration` → prompt eval rate (tok/s)
- `eval_count` / `eval_duration` → **sustained eval rate (tok/s)** [metrica principale]
- `load_duration` → tempo caricamento weights
- `total_duration` → wall time totale

Post-caricamento, `ollama ps` per GPU offload %.

### Protocollo per-run
1. `ollama stop <previous_model>` (se diverso) per garantire fresh load
2. Warm-up: 1 richiesta `num_predict: 30` (carica pesi in VRAM, non misurata)
3. Misura: richiesta `num_predict: 300`, parse metriche
4. Annota: modello, num_ctx, tok/s eval, tok/s prompt eval, GPU offload %, RAM delta

## Baseline riferimento (ADR-0007 Test 1, su 16 GB RAM, pre-upgrade)

Stesso prompt, misure 2026-04-20:

| num_ctx | Speed eval (tok/s) | GPU offload | Note |
|---------|--------------------|-------------|------|
| 16384 | 18.72 | 73.0% | baseline originale |
| **8192** | **25.54** | 86.3% | **default attuale** |
| 4096 | 35.23 | 90.7% | ctx stretto per Aider |
| 4096 + num_gpu=-1 | 36.61 | ~98% | gold standard full-GPU |

qwen3-coder:30b a ctx 8192 (ADR-0009 addendum 2026-04-21, 16 GB RAM): **23.3 tok/s, RAM tight 1.3 GB free**.

---

## Risultati bench 2026-04-22

Tutti i run via `scripts/bench-ollama.ps1` (warm-up 30 tok + misura 300 tok, `temperature=0`).

### Qwen 2.5 Coder 14B Q2_K (dense, 5.8 GB weights)

| num_ctx | Eval tok/s | Prompt tok/s | GPU offload | Size caricato | Delta vs baseline ADR-0007 |
|---------|-----------:|-------------:|------------:|--------------:|----------------------------|
| 8192 | **25.39** | 2612.59 | 85% | 7.3 GB | +0.6% (sanity PASS) |
| 16384 | **17.28** | 1835.25 | 70% | 8.9 GB | -7.7% (leggera regressione, noise o Ollama 0.21 vs precedente) |
| 32768 | **11.62** | 1250.71 | 50% | 12 GB | n/a (non testato pre-upgrade) |

**Osservazione 14B Q2**:
- Raddoppio ctx → ~-32% speed, pattern lineare log
- CPU spill cresce proporzionalmente: 15% → 30% → 50%
- Il collo è **VRAM + CPU compute**, non RAM budget (la RAM extra non aiuta)
- Decisione: `OLLAMA_CONTEXT_LENGTH=8192` resta sweet spot, nessun cambio default

### Qwen3 Coder 30B (MoE, 30.5B total / 3B active, 18 GB weights)

| num_ctx | Eval tok/s | Prompt tok/s | GPU offload | Size caricato | Delta vs baseline ADR-0009 addendum |
|---------|-----------:|-------------:|------------:|--------------:|--------------------------------------|
| 8192 | **30.67** | 2438.47 | 32% | 19 GB | **+31.6%** (da 23.3 tok/s pre-upgrade) |
| 16384 | **30.65** | 2189.66 | 32% | 19 GB | n/a (non testato pre-upgrade) |
| 32768 | **29.78** | 2228.54 | 30% | 20 GB | n/a (non testato pre-upgrade) |

**Osservazione qwen3:30b — finding chiave del bench**:
- **+32% speed post-upgrade** su ctx 8192 (23.3 → 30.67 tok/s). Baseline pre-upgrade era "RAM tight 1.3 GB free" (ADR-0009 addendum) → ora ~35 GB headroom in caricamento. La RAM abbondante fa **differenza sostanziale** per modelli con spill >50% CPU.
- **Virtually FLAT** da ctx 8192 a ctx 32768 (delta -3%, rumore misura). MoE con 3B active params: KV cache cresce ma il compute active resta costante → raddoppio ctx sostanzialmente gratis.
- Questo è il caso d'uso in cui l'upgrade RAM paga di più.

### Sintesi speedup post-upgrade

| Modello | Caso | Pre-upgrade | Post-upgrade | Delta |
|---------|------|------------:|-------------:|-------|
| 14B Q2 | ctx 8192 | 25.54 | 25.39 | 0% (noise) |
| 14B Q2 | ctx 16384 | 18.72 | 17.28 | -7.7% |
| qwen3:30b | ctx 8192 | 23.3 | 30.67 | **+31.6%** |

### Qwen 2.5 Coder 32B dense (Q4_K_M, 19 GB disk / 21-23 GB loaded)

Pull 2026-04-22 sera (19 GB @ 9.3 MB/s → ~35 min download).

| num_ctx | Eval tok/s | Prompt tok/s | GPU offload | Size caricato |
|---------|-----------:|-------------:|------------:|--------------:|
| 8192 | **3.65** | 381.21 | 27% | 21 GB |
| 16384 | **3.52** | 369.94 | 25% | 23 GB |

**Osservazione 32B dense — verdetto scartato**:
- **8.4× più lento di qwen3:30b MoE** a parità di ctx (3.65 vs 30.67). Pattern CPU-bound:
  - MoE 30B (3B active params): 68% CPU spill + 32% GPU → compute effettivo ≈ 3B model → 30 tok/s
  - Dense 32B (32B attivi full-weight): 73% CPU + 27% GPU → compute full 32B ogni token → ~3.6 tok/s
- Ctx non sposta nulla (-3.6% da 8192 a 16384, rumore). Il collo è compute dense 32B, non KV cache.
- **NON viable come candidato tier 2** vs qwen3:30b MoE.
- Come reference capability potrebbe servire per confronti "pure dense 32B" in task specifici se emerge necessità, ma il throughput rende inutile per workflow iterativi.

### Tabella comparativa consolidata

Tutti i modelli post-upgrade RAM (64 GB), stesso prompt Python DoublyLinkedList, `temperature=0`, `num_predict=300`:

| Modello | Architettura | ctx | tok/s | GPU% | Candidato? |
|---------|--------------|-----|------:|-----:|------------|
| 14B Q2_K | dense 14B | 8192 | 25.39 | 85% | ✅ **tier 1 behavior default** (invariato ADR-0008) |
| 14B Q2_K | dense 14B | 16384 | 17.28 | 70% | ⚠️ override per multi-file, ma penalty -32% |
| 14B Q2_K | dense 14B | 32768 | 11.62 | 50% | ❌ troppo slow |
| qwen3:30b | MoE 30B/3B-active | 8192 | 30.67 | 32% | ✅ **tier 2 escalation (post-upgrade più veloce)** |
| qwen3:30b | MoE 30B/3B-active | 16384 | 30.65 | 32% | ✅ **promuovibile a default ctx tier 2 — zero penalty** |
| qwen3:30b | MoE 30B/3B-active | 32768 | 29.78 | 30% | ✅ **ancora viable per task multi-file large** |
| qwen2.5-coder:32b | dense 32B | 8192 | 3.65 | 27% | ❌ scartato — 8.4× più lento di MoE pari size |
| qwen2.5-coder:32b | dense 32B | 16384 | 3.52 | 25% | ❌ scartato |

## Findings e decisioni

### Finding 1 — La RAM extra NON aiuta 14B Q2

- ctx 8192: 25.39 (baseline 25.54 pre-upgrade, delta +0.6% = noise)
- ctx 16384: 17.28 (baseline 18.72 pre-upgrade, delta -7.7% = probabile drift Ollama version o rumore)
- Il collo per 14B Q2 è **VRAM + CPU compute**, non RAM budget. Su 16 GB RAM la RAM era già sufficiente per ospitare il CPU spill.

### Finding 2 — La RAM extra aiuta MASSICCIAMENTE qwen3:30b

- ctx 8192: 30.67 (baseline 23.3 pre-upgrade con "RAM tight 1.3 GB free", delta **+31.6%**)
- Root cause: su 16 GB RAM il modello da 18 GB disk + KV cache saturava RAM → swap pressure, page faults, cache eviction OS. Ora con 54 GB liberi in caricamento → workload CPU-spilled gira a piena velocità.
- **Il beneficio RAM è correlato al % CPU spill**: modelli con >50% CPU beneficiano, modelli con ≤30% CPU non beneficiano.

### Finding 3 — MoE vince nettamente su dense size-pari

qwen3:30b MoE (3B active) vs qwen2.5:32b dense (32B active):
- Tok/s: 30.67 vs 3.65 → **8.4×**
- GPU offload: 32% vs 27% (entrambi simili, il collo è compute non VRAM)
- Decisione: preferire MoE quando disponibile per footprint 20+ GB. Il dense 32B su RTX 5060 8GB è stuck in CPU-bound hell.

### Finding 4 — MoE è ctx-insensitive su questa hardware

qwen3:30b da ctx 8192 a ctx 32768 → -3% speed (rumore).
- KV cache grande, ma compute attivo ≈ 3B fisso → ctx non sposta il collo.
- **Implicazione operativa**: per tier 2 escalation possiamo usare ctx 16384 o 32768 senza pagare — ideale per task multi-file con repo-map ampia.

### Decisioni prese

1. **`OLLAMA_CONTEXT_LENGTH=8192` RESTA il default globale** — coerente con 14B Q2 tier 1 workflow.
2. **qwen3:30b tier 2: promozione a ctx 16384 default** via override per-request `options.num_ctx=16384` nel wrapper `aider-refactor.cmd` **solo quando** il task richiede multi-file context (repo-map ampia, diff su file >1000 righe). Per task single-file standard, ctx 8192 resta sufficiente.
3. **32B dense scartato** come candidato. Il modello resta scaricato per reference/comparison ma non va in tier routing.
4. **Regressione -7.7% su 14B Q2 @ ctx 16384** (17.28 vs 18.72) va tracciata come "noise or Ollama drift": se si ripresenta in uso reale post-upgrade, aprire indagine separata (possibili cause: Ollama 0.21 changelog, driver NVIDIA, thermal throttling).

### Follow-up deferred

- [ ] Aggiornare `aider-refactor.cmd` con override `num_ctx=16384` quando rileva task multi-file (euristica: presenza di `--file` multipli). Oppure creare nuovo wrapper `aider-refactor-multi.cmd` dedicato. Non urgente.
- [ ] Bench qwen3:30b @ ctx 32768 con workload reale Aider (non solo prompt bench isolato) per confermare che il -3% resta costante.
- [ ] Valutazione capability (non speed) di 32B dense su task behavior-critical: forse vale la pena come "slow but more capable" tier 3? Da decidere solo se Fase 6 rivela gap capability che 30B MoE non copre.
- [ ] Task #13 (deepseek-r1 + gpt-oss:120b): valutazione rimandata, vedi task tracking.

---

## Bench cloud tier 3 2026-04-22 (serata tardi)

Validazione empirica post ADR-0013. Stesso prompt DoublyLinkedList. Via `scripts/bench-cloud.ps1` (warm-up 30 tok + misura 300 tok, temperature 0).

### Risultati cloud providers

| Provider/Model | Eval tok/s | Completion tok | Prompt tok | Wall s | Note |
|----------------|-----------:|---------------:|-----------:|-------:|------|
| `groq/llama-3.3-70b-versatile` | **630.86** | 300 | 109 | 0.85 | usage.completion_time (nativo Groq) |
| `cerebras/llama3.1-8b` | **733.5** | 300 | 109 | 0.41 | wall-clock approx (Cerebras no native metric) |

### Confronto tier routing locale vs cloud

| Tier | Model | Speed tok/s | Moltiplicatore vs locale | Capability nominal |
|------|-------|------------:|-------------------------:|--------------------|
| cosmetic locale | qwen2.5-coder:7b | 114 | 1× | 7B coder specialist |
| behavior locale | qwen2.5-coder:14b Q2 | 25.39 | 1× | 14B coder specialist Q2 |
| escalation locale | qwen3-coder:30b MoE | 30.67 | 1× | 30B/3B-active coder |
| **cosmetic cloud** | cerebras/llama3.1-8b | **733.5** | **6.4×** vs 7B | 8B general |
| **behavior/escalation cloud** | **groq/llama-3.3-70b** | **630.86** | **20.6×** vs qwen3:30b | 70B dense general |

### Finding strategico — cloud ridefinisce il tier routing

**Online mode** (internet up, free tier non exhausted):
- Groq llama 70B > qwen3:30b su TUTTI i fronti: speed 20×, capability 70B > 30B MoE, cost $0 free
- Cerebras 8B > qwen 7B su speed 6×, capability generale simile (8B general vs 7B coder-specialist — possibile tradeoff qualità coder)

**Offline mode / quota exhausted**:
- Locale Qwen tier resta valido (sovereign guaranteed)

**Pattern proposto** (pending review utente + empirical Fase 6):
- **Tier 1 cosmetic ONLINE**: `cerebras/llama3.1-8b` se quota disponibile → fallback `qwen2.5-coder:7b` locale
- **Tier 2 behavior ONLINE**: `groq/llama-3.3-70b-versatile` se quota disponibile → fallback `qwen2.5-coder:14b-q2` locale
- **Tier 3 escalation**: `groq/qwen-2.5-coder-32b` (se disponibile su Groq) o `qwen3-coder:30b` locale
- **Tier 4 capability-max**: `openai/gpt-4o`, `gemini/2.5-pro` (pay-per-use o limited free)

### Caveat da considerare

1. **Privacy**: send source code to cloud = data retention per Groq/Cerebras ToS. Per codice proprietario/cliente → sovereign-first obbligatorio. Per repo personali → rischio basso, accettabile.
2. **Quality coder**: bench tok/s dice nulla su quality code generato. Groq/Cerebras usano llama 3 general, non coder-specialist. Qwen 2.5 Coder è potenzialmente più preciso su task strettamente coding anche a parità di speed. Bench quality (es. HumanEval, pass@1) richiesto prima di declaration definitiva.
3. **Rate limit**: Groq 6000 tok/min sostenuti → task iterativi molti (es. Aider 5+ round) potrebbero saturare. Cerebras quota non chiara su free tier.
4. **Availability**: provider outage = workflow blocked. Locale = guarantee uptime.
5. **Bench singolo**: n=1 speed test. Quality + reliability statistica richiedono Fase 6 dogfood reali.

### Decisioni pre-ADR-0013 addendum

1. **NON aggiornare tier routing CLAUDE.md ora** — serve dogfood Fase 6 per quality validation prima di shift paradigmatico cloud-first.
2. **ADR-0013 status**: Proposed → **Validation-in-progress** (bench speed PASS, quality pending).
3. **Nuovo pattern documentabile come esperimento**: usare cloud per N task nei prossimi giorni, registrare in log Fase 6 ciò che funziona e fallisce.
4. **Privacy check**: attivare cloud solo su repo non-sensitive (lenovo-ai-station OK, eventuali repo cliente NO).
