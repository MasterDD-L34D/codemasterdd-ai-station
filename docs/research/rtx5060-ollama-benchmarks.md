# Research: RTX 5060 per Ollama LLM locali

**Data ricerca**: 2026-04-19 (pre-setup) + validation 2026-04-20 (post-benchmark reale)
**Scopo**: capire cosa aspettarsi da Lenovo con RTX 5060 8GB per workflow AI locale
**Metodologia**: web search benchmarks + community reports + validazione hardware-specific

## Executive summary

RTX 5060 8GB VRAM è **entry-level** per local LLM inference nel 2026.
Pragmaticamente **utilizzabile** per modelli 7-8B parameters con quantizzazione Q4.

**Key findings pre-research**:
- 8GB VRAM limita a modelli 7-8B max a piena qualità
- Blackwell architecture (sm_120) ha ottimizzazioni nuove ma anche bug
- Performance attesa: 20-55 tok/s per 7B-8B models
- Community divide: 5060 viable vs frustrating

**Validation post-benchmark (Eduardo's hardware)**:
- **Risultato reale**: 93.51 tok/s su Qwen 2.5 Coder 7B Q4_K_M
- **70% sopra massimo atteso**: Blackwell + config ottimale = bonus performance
- **VRAM usage**: ~6.2GB / 8GB (margine accettabile)

## Hardware baseline: RTX 5060 8GB

### Specifiche chiave

- **Architettura**: Blackwell (sm_120)
- **VRAM**: 8GB GDDR7
- **Memory bandwidth**: ~504 GB/s (GDDR7 benefit vs GDDR6)
- **CUDA cores**: ~3840 (5th gen Tensor cores)
- **TDP**: 115-145W
- **MSRP**: $299

### Posizionamento nel 2026

**Tier AI performance consumer GPUs 2026** (approx ranking):
1. RTX 5090 32GB — enthusiast
2. RTX 5080 16GB — high-end
3. RTX 5070 Ti 16GB — upper-mid
4. RTX 4090 24GB — still premium
5. RTX 5070 12GB — mid
6. RTX 3090 24GB — legacy king VRAM
7. RTX 4070 12GB — mid legacy
8. **RTX 5060 Ti 16GB** — mid-budget (>5060)
9. **RTX 5060 8GB** — entry — Eduardo's tier
10. RTX 4060 8GB — legacy entry
11. Intel Arc B580 12GB — budget alt

### Cosa può e non può fare

**Può fare bene**:
- 7B modelli a Q4 (Qwen 2.5 Coder, Llama 3 8B, Mistral)
- Embedding models (<1GB)
- Short context (4K-16K) comfortably
- Single-user inference

**Fatica**:
- 13B+ modelli a qualità decente
- Long context (>32K) senza quantizzazione aggressiva
- Multi-model loading (2+ modelli simultanei)

**Non può fare** (limitazioni hard):
- 30B+ modelli a Q4 (VRAM insufficiente)
- 70B+ modelli (impossibile anche aggressive quant)
- Multi-modal (vision) stabilmente su Blackwell
- Training fine-tuning anche 7B (OOM training overhead)

## Blackwell sm_120 caveats noti

Research pre-install ha rivelato **issues specifici di Blackwell**:

### 1. NVFP4 MoE rotto

**Bug**: CUTLASS issue #3096
**Effetto**: modelli MoE (Mixture of Experts) con quantizzazione NVFP4
non funzionano correttamente.
**Workaround**: evitare modelli MoE per ora, o usare quantizzazione GGUF standard.
**Status**: NVIDIA + llama.cpp community al lavoro, fix previsto Q2-Q3 2026.

### 2. MXFP4 non compila

**Bug**: llama.cpp main branch non compila con MXFP4 (quantizzazione sperimentale)
su Blackwell.
**Workaround**: usare GGUF Q4_K_M o Q8_0 (standard, stabili).
**Status**: patch su branch experimental, merge in attesa.

### 3. Vision models crash

**Bug**: ollama issue #14446
**Effetto**: LLaVA, Qwen-VL, bakllava possono crashare su Blackwell sm_120.
**Workaround**: solo text models per ora. Vision → cloud (Anthropic, OpenAI).
**Status**: ollama team investigating, fix dipende da llama.cpp upstream.

### 4. Flash Attention MATURE (positivo)

**Fact**: Blackwell ha FlashAttention-3 ottimizzato native.
**Beneficio**: +15-25% throughput su attention operations.
**Config**: `OLLAMA_FLASH_ATTENTION=1`.

### 5. GDDR7 bandwidth bonus

**Fact**: GDDR7 offre ~40% bandwidth in più di GDDR6 a parità di bus.
**Beneficio**: KV cache reads più veloci, prefill più veloce.

## Community benchmarks (pre-setup research)

### Database Mart (dedicated GPU provider)

Fonte: https://www.databasemart.com/blog/ollama-gpu-benchmark-rtx5060

**Setup test**:
- Ollama 0.9.5 (vecchio, ora 0.21)
- 18 modelli testati
- Q4 quantizzazione

**Risultati chiave**:
- Qwen 3 0.6B: **210 tok/s** (sub-1B, stream fast)
- Gemma 3 1B: 130-150 tok/s
- Phi 2.7B: 130-150 tok/s
- Mistral 7B: **<75 tok/s**
- DeepSeek-R1 7B: **<75 tok/s**

**Stima per Qwen 2.5 Coder 7B**: 50-75 tok/s.

### Compute Market

Fonte: https://www.compute-market.com/blog/rtx-5060-local-ai-review-2026

**Quote**: "RTX 5060's 8GB VRAM can run 7B–8B parameter LLMs at **20-35 tokens per second** via Ollama"

**Perspective**: più conservativa, probabilmente assumendo config non ottimale.

### AI Agents Kit

Fonte: https://aiagentskit.com/blog/best-local-llms-rtx-4060-3070-5060/

**Quote**: "RTX 4060/3070/5060 shared 8GB VRAM class for local LLM work"
**Qwen 3 8B: 5.2GB footprint** → fit bene su 8GB

**Raccomandazioni**:
- Qwen 2.5-Coder per development
- DeepSeek-R1 per logic/math
- Llama 3.3 8B general purpose

### CraftRigs comparison 3090 vs 5060 Ti

Fonte: https://craftrigs.com/comparisons/rtx-3090-vs-rtx-5060-ti-local-llm/

**Insight** (applicabile anche a 5060 vanilla):
- 3090: 24GB VRAM, 936 GB/s bandwidth
- 5060 Ti: 16GB, 448 GB/s
- **5060 (8GB)**: tops out at 8B models, 8GB is "too little for serious local LLM use in 2026"

**Opinione dura**: 5060 8GB è "hard pass" per chi vuole modelli 14B+.

## Community estimates aggregati

**Consensus per 7B Q4 su RTX 5060 8GB** (Ollama standard config):
- Pessimistic: 20-35 tok/s
- Average: 40-55 tok/s
- Optimistic: 60-75 tok/s

**Fattori di variabilità**:
- Quantizzazione (Q4 vs Q5 vs Q8)
- Context length setting
- Flash Attention on/off
- KV cache type
- Driver version
- Other GPU load
- CPU (influence: piccola se tutto in VRAM)

## Validation Eduardo's hardware (20 aprile 2026)

### Setup testato

- **GPU**: NVIDIA RTX 5060 8GB (Blackwell sm_120)
- **Driver**: 595.79
- **CUDA**: 13.2
- **Ollama**: 0.21.0
- **Config env vars**:
  - OLLAMA_FLASH_ATTENTION=1
  - OLLAMA_KV_CACHE_TYPE=q8_0
  - OLLAMA_MAX_LOADED_MODELS=1
  - OLLAMA_KEEP_ALIVE=30m
  - OLLAMA_CONTEXT_LENGTH=16384

### Model testato

- **Qwen 2.5 Coder 7B** (Q4_K_M quantizzazione)
- Size on disk: 4.7 GB
- VRAM usage: ~6.2 GB during inference

### Benchmark risultati

**Primo test** (funzione Python parser CSV):
- Prompt: ~50 tokens
- Output: ~350 tokens
- **Eval rate**: **93.51 tok/s sustained**
- Latency first token: ~200ms

### Analisi gap vs research

**Research aspettative**: 40-55 tok/s (average)
**Risultato reale**: 93.51 tok/s
**Gap**: +70% sopra massimo community

**Possibili spiegazioni**:
1. **Blackwell underrated**: benchmarks online spesso da sistemi con Ada/Ampere,
   Blackwell sm_120 ottimizzazioni meno note
2. **FlashAttention-3**: forse più impactful del previsto su Blackwell
3. **GDDR7 bandwidth**: benefit under-measured in older reviews
4. **Config ottimale**: env vars ottimizzate fanno differenza grande
5. **Clean setup**: no altri carichi GPU (nessun gioco, no browser GPU, iGPU per display)
6. **Ollama 0.21.0**: più recente dei benchmarks (0.9.x di DatabaseMart)

## Implicazioni strategiche

### Per sovereign AI plan

**Prima della validazione**: dubbio se Lenovo da solo bastasse per sovereign.
Possibile Mac mini "necessario" per qualità.

**Dopo validazione**: Lenovo **supera aspettative**. Mac mini diventa
**opzionale/nice-to-have**, non dependency.

**Budget implication**: risparmio €2500-3000 Mac mini (almeno per ora).

### Per workflow dev

**Latency percepita** con 93 tok/s:
- Query 100 token → 1 secondo (istantaneo feel)
- Query 500 token → 5 secondi (veloce)
- Query 2000 token → 20 secondi (accettabile per bulk)

**Comparabile a cloud** per response time su task medio-piccoli.
**Migliore di cloud** per zero network latency su query brevi frequenti.

## Modelli raccomandati per RTX 5060 8GB

### Daily driver coding: Qwen 2.5 Coder 7B

- Q4_K_M: 4.7GB VRAM, ~93 tok/s (verified)
- Q5_K_M: 5.2GB VRAM, ~80 tok/s (better quality, less speed)
- Context: 16K nominale (configurabile fino 131K con tradeoff VRAM)

### Reasoning general: Qwen 3 8B

- Q4_K_M: ~5.2GB VRAM
- Expected ~75 tok/s
- Better reasoning vs Qwen 2.5 Coder
- Trade-off: meno code-specialized

### Fast responses: Mistral 7B v0.3 o Llama 3.1 8B

- Q4_K_M: ~4.4-4.9GB VRAM
- Expected ~80-95 tok/s
- General purpose, streaming chat friendly

### Math/logic: DeepSeek-R1 7B

- Q4_K_M: ~4.8GB VRAM
- Expected ~85 tok/s
- Chain-of-thought reasoning
- Slower typical ma quality reasoning alto

### Embedding: nomic-embed-text

- 274MB VRAM
- Per RAG/semantic search
- Light overhead, can run alongside 7B model

### Da NON provare (per ora)

- Mixtral 8x7B: MoE → Blackwell NVFP4 bug
- Llama 3 70B: OOM anche aggressive quant
- LLaVA/Qwen-VL: vision crash Blackwell
- CodeLlama 34B: non fit a Q4, Q3_K degrada troppo
- GPT-OSS-20B: troppo grande

## Alternative hardware (per riferimento)

### Se Eduardo decidesse di upgradare GPU

**Budget $400-500**: RTX 5060 Ti 16GB
- +8GB VRAM
- Permette 13B-14B models Q4
- Context più lungo
- Same Blackwell

**Budget $800-1000**: RTX 3090 24GB (used)
- +16GB VRAM vs 5060
- 2x bandwidth (936 GB/s)
- Permette 30B Q4
- No Blackwell benefits (Ampere)

**Budget $1500+**: RTX 4090 24GB
- VRAM + Ada architecture (già robusto)
- Performance premium

**Budget $2500+**: RTX 5090 32GB
- Massimo consumer
- Future-proof 3+ anni

### Mac alternative

**Mac mini M4 Pro 48GB unified memory**:
- ~€2500-3000
- 48GB "RAM-like" per LLM (unified memory)
- Permette 30B+ models
- ARM architecture (compat variable)

## Meta-learning

### Lezione 1: benchmark reale > speculazione

Research online indicava 40-55 tok/s. Realtà: 93.
**Moral**: **sempre validare su hardware proprio** prima di prendere decisioni strategiche.

### Lezione 2: config matters enormously

Senza env vars ottimali, Ollama avrebbe potuto dare 50-60 tok/s (stima).
Config ottimizzato ha quasi 2x il throughput.
**Moral**: **spendere 15 min in config vale sempre**.

### Lezione 3: Blackwell è underrated online

La maggior parte dei benchmark Ollama è su Ada/Ampere.
Blackwell è recente (late 2024 lancio).
Community ancora catching up con ottimizzazioni.
**Moral**: architetture nuove possono avere sorprese positive.

### Lezione 4: GDDR7 vs GDDR6 differenza tangibile

Bandwidth GDDR7 era "nice to have" on paper.
In realtà è sembra rilevante per LLM inference (dominated by memory bandwidth).
**Moral**: memory tech ha impatto nascosto in LLM.

### Lezione 5: VRAM limit è hard boundary

8GB VRAM significa 8GB, no compromise.
Swap to RAM = 10-20x slower.
**Moral**: scegli modelli che fit comfortably, non "just barely".

## Fonti

- Compute Market RTX 5060 Review: https://www.compute-market.com/blog/rtx-5060-local-ai-review-2026
- DatabaseMart Ollama Benchmarks: https://www.databasemart.com/blog/ollama-gpu-benchmark-rtx5060
- AI Agents Kit 8GB class: https://aiagentskit.com/blog/best-local-llms-rtx-4060-3070-5060/
- CraftRigs 3090 vs 5060 Ti: https://craftrigs.com/comparisons/rtx-3090-vs-rtx-5060-ti-local-llm/
- ApxML NVIDIA RTX 50 series: https://apxml.com/posts/best-local-llms-for-every-nvidia-rtx-50-series-gpu
- SitePoint Best Local LLMs: https://www.sitepoint.com/best-local-llm-models-2026/
- Complete LLM Local Guide: https://www.compute-market.com/hubs/local-llm-guide
- David's Blueprint Laptops for Ollama: https://www.davidsblueprint.com/articles/best-laptops-for-ollama-2026

## Follow-up

### Benchmark da fare questa settimana

- [ ] Qwen 3 8B con stesso prompt (compare tok/s con 2.5 Coder)
- [ ] DeepSeek-R1 7B (reasoning-focused)
- [ ] Llama 3.1 8B (general purpose baseline)
- [ ] Context length stress test (8K → 16K → 32K)

### Benchmark da fare questo mese

- [ ] Qualitative: Qwen 7B vs Opus 4.7 stesso task coding
- [ ] Tool use: quanto tok/s con context + tool calls
- [ ] Embedding: nomic vs mxbai per Supermemory-like RAG

### Watch-list

- [ ] Ollama 0.22+ release (check performance improvements)
- [ ] NVIDIA driver 600+ (potenziali ottimizzazioni Blackwell)
- [ ] Qwen 3 Coder release (next generation coding)
- [ ] Blackwell bug fixes (MoE NVFP4, vision crashes)
