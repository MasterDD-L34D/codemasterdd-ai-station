# Hardware + modelli locali -- CodeMasterDD AI Station

<!-- Spostato da CLAUDE.md 2026-06-03 (context-files reorg Fase 1). On-demand reference.
     Tabelle tok/s misurate (metodologia: docs/research/bench-*). Verifica modelli: ollama list. -->

## Hardware (definitivo)
- **CodeMasterDD** (Lenovo LOQ Tower 17IAX10, desktop)
  - Intel Core Ultra 7 255HX (24 core Arrow Lake HX, 2.40 GHz base)
  - NVIDIA RTX 5060 8GB VRAM (Blackwell sm_120, CUDA 13.2)
  - **64GB DDR5-5600** (2×32GB Micron CT32G56C46S5.C16D, dual channel ChannelA+ChannelB DIMM1) — upgrade 2026-04-22 da 16GB originali, vedi `docs/adr/0012-ram-upgrade-64gb-impact.md`
  - SSD 1TB Micron NVMe (~877 GB liberi post-cleanup bloatware)
- OS: Windows 11 Home 25H2 (build 26200, no KB5083769)

## Capacità AI locali (Lenovo da solo)
- Modelli **full-GPU** su 8 GB VRAM: fino a 7-8B a quality piena (Qwen 2.5 Coder 7B, Qwen 3 8B, DeepSeek 7B)
- Modelli **14B**: entrano parzialmente (60-75% GPU + CPU spill 25-40%) — usabili ma throughput ridotto
- Velocità **misurate** (sustained eval, prompt DoublyLinkedList Python isolated single-task):

| Modello | Tok/s isolato | GPU offload | Uso consigliato |
|---------|--------------|-------------|-----------------|
| Qwen 2.5 Coder 7B Q4_K_M | 114 | 100% | query one-shot, create, read/explain |
| Qwen 2.5 Coder 14B Q3_K_M | 10.8 | 62% | sconsigliato (hallucination su constraint) |
| Qwen 2.5 Coder 14B **Q2_K** | 18.7 | 73% | **agentic edit (sweet spot + faithful)** |

- Velocità **mixed-workload** (bench H9 2026-05-09, n=4 per tier, 11 swap forced, vedi `docs/research/bench-mixed-workload-2026-05-09.md`):

| Modello | Tok/s isolato | Tok/s mixed (n=4) | Drift | Note workflow misto |
|---------|--------------|------------------|-------|---------------------|
| Qwen 2.5 Coder 7B Q4_K_M | 114 | **100.75** | -12% | Realistic per workflow continuo |
| Qwen 2.5 Coder 14B Q2_K | 18.7-25 | **17.62** | **-30% vs 25 doc** | Sweet spot ma drift significativo |
| qwen3-coder:30b MoE A3B | 23 | **32.98** | **+43% upside** | **Discovery positiva**: superiore a doc precedente, ora competitive con 14B Q2 in throughput + capability superiore |

**Swap overhead** (workflow alternato 7B/14B/30B): **3047ms/swap × 11 swap = 33.5s su 79.2s totale = 42.3%** del workflow misto.

**Mitigation quantificata** (bench batched 2026-05-09): se task per stesso modello vengono raggruppati prima di switch (run [4×7B → 4×14B Q2 → 4×30B]), workflow time scende a **49.9s (saving 37%)** con solo 2 swap. Throughput per-modello invariato. Raccomandazione: **quando possibile, batch task per modello** (es. tutti i cosmetic 7B prima, poi tutti behavior 14B Q2, poi escalation 30B MoE).

- Stack agentic sovereign consigliato: **Aider + Qwen 14B Q2_K** — vedi `docs/adr/0007-aider-qwen-quantization-findings.md`
- Env vars Ollama applicate (User scope, persistenti) — config rationale: `docs/adr/0004-ollama-rtx5060-config.md` + `docs/adr/0007-aider-qwen-quantization-findings.md`
  - `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_KEEP_ALIVE=30m`
  - `OLLAMA_CONTEXT_LENGTH=8192` (ridotto da 16384 il 2026-04-20 su 16GB RAM: +36% speed su 14B Q2 liberando KV cache da CPU spill. Override per-request `num_ctx: 16384` per task multi-file. **Post upgrade 64GB 2026-04-22: il razionale originale è decaduto — rivalidare bench empirico prima di riportare default a 16384**, vedi `docs/adr/0012-ram-upgrade-64gb-impact.md`.)
- **Nuova capacità post 2026-04-22 (64GB RAM)**: modelli 30B+ non più RAM-bound; qwen3-coder:30b tier 2 non più borderline; Qwen 2.5 Coder 32B Q4 (~19-20GB) diventa candidato benchmarkable; 14B Q3_K_M potrebbe tornare competitivo con ctx più alto. Tutti i valori tok/s in tabella rimangono **validi** (misurati pre-upgrade, ma non RAM-bound) — rebench opzionale solo per scoprire se ctx più largo cambia la decision matrix.


- Modelli locali:
  - `qwen2.5-coder:7b` (Q4_K_M, 4.7 GB, digest `dae161e27b0e`, installato 2026-04-19) — **query one-shot, create single file, read/explain**
  - `qwen2.5-coder:14b-instruct-q3_K_M` (7.3 GB, digest `e00d09afd55a`, installato 2026-04-20) — capace ma rischio hallucination su constraint; 10.8 tok/s (CPU spill 38%)
  - `qwen2.5-coder:14b-instruct-q2_K` (5.8 GB, digest `dfeff73b234d`, installato 2026-04-20) — **sweet-spot agentic: 18.7 tok/s, faithful constraint-respect**, vedi `docs/adr/0007-aider-qwen-quantization-findings.md`
  - `qwen3-coder:30b` (Q4_K_M, 18 GB, digest `06c1097efce0`, MoE 30.5B/3B-active, 256K ctx, installato 2026-04-21) — **tier 2 escalation behavior-critical**: 23.3 tok/s @ ctx 8192. Resolve anti-pattern R1 dove 14B Q2 safe-fails. Vedi `docs/adr/0009-upgrade-strategy.md` addendum 2026-04-21. **Nota RAM tight (1.3 GB free) originale RIMOSSA 2026-04-22**: dopo upgrade a 64GB il modello ha ~40GB headroom in caricamento — promosso da tier 2 borderline a tier 2 stabile, vedi `docs/adr/0012-ram-upgrade-64gb-impact.md`
  - `gemma4:latest` (Q4_K_M, 9.6 GB disk / 10 GB loaded, digest `c6eb396dbd59`, 8.0B params, ctx 128K nativo, installato 2026-04-22) — **tier multimodal dedicato**: unico modello locale con vision + audio + tools + thinking (Apache 2.0). Speed: 39.26 tok/s @ ctx 8192 (GPU 32%, CPU spill 68% per overhead multimodal adapter). **NON coder-specialist**: per task coding continuare Qwen (7B/14B Q2/30B MoE). Usare Gemma 4 solo per screenshot/diagram OCR, audio dictation, o dogfood thinking-mode comparativo. Vedi `docs/research/bench-post-ram-upgrade-2026-04-22.md`
  - `deepseek-r1:8b` (Q4_K_M, 5.2 GB disk / 6.0 GB loaded, digest `6995872bfe4c`, 8.2B params, architecture qwen3 + R1 distillation, ctx 128K nativo, installato 2026-04-22) — **tier reasoning locale**: 74.57 tok/s @ ctx 8192 **100% GPU full-fit** (unico 8B locale full-VRAM), 47.46 @ ctx 16384. Thinking mode R1-distilled per chain-of-thought esteso. Usare per task reasoning/debug logica, NON coder-specialist (Qwen domina per coding). Vedi `docs/research/bench-post-ram-upgrade-2026-04-22.md`
  - `gpt-oss:120b` (MXFP4, 65 GB disk, digest `a951a23b46a1`, **116.8B params**, ctx 128K, installato 2026-04-22) — **NON viable locale**: runtime richiede ~70 GB RAM > 63 GB totali. Via Cerebras catalog free tier bloccato (paid-only). Tenuto su disco come reference per future upgrade RAM (96/128 GB) o paid cloud access. Bench non eseguito per safety OOM.
  - `qwen2.5-coder:32b` (Q4_K_M, 19 GB, digest `b92d6a0bd47e`, dense 32B, installato 2026-04-22) — **SCARTATO tier routing**: bench 3.65 tok/s @ ctx 8192 (ADR-0012 addendum), 8.4× più lento di qwen3-coder:30b MoE. Reference only per comparison dense vs MoE.
  - **Modelli aggiuntivi** (installati ~2 settimane fa per esplorazione, non bench-coperti codemasterdd, non in tier routing primario): `qwen3:8b` (5.2 GB, fallback chain Dafne tier 1), `qwen3.5:latest` (6.6 GB), `qwen3.6:latest` (23 GB), `qwen2.5:32b-instruct-q4_K_M` (19 GB, NON coder-specialist), `phi4:14b` (9.1 GB), `deepseek-r1:14b` (9.0 GB, scaling-up della 8b), `mistral:latest` (4.4 GB), `nomic-embed-text:latest` (274 MB, embedding utility). Bench/ADR opzionale post-Max se emergono use case concreti. Verifica presence: `ollama list`.
