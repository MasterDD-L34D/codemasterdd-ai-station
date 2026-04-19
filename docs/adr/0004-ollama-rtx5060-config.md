# ADR 0004 — Ollama config per RTX 5060 Blackwell

**Status**: Accepted
**Data**: 2026-04-20
**Decisore**: Eduardo Scarpelli
**Tipo decisione**: tecnica (performance, LLM locali)

## Contesto

### Hardware target

- **GPU**: NVIDIA RTX 5060 8GB VRAM (Blackwell sm_120)
- **Driver**: 595.79 + CUDA 13.2
- **Host RAM**: 16GB DDR5
- **OS**: Windows 11 Home

### Obiettivo

Configurare Ollama per eseguire LLM locali (Qwen 2.5 Coder 7B come primo modello)
con massima efficienza:
- Throughput elevato (tok/s)
- VRAM usage controllato (8GB limit)
- Qualità output preservata
- Compatibilità con Blackwell sm_120 (nuova architettura, alcune caveats)

### Constraints noti Blackwell

**Research pre-installazione** ha rivelato queste limitations specifiche
di Blackwell sm_120 su Ollama:

1. **NVFP4 MoE rotto** (CUTLASS issue #3096): modelli MoE con quantizzazione
   NVFP4 non funzionano. **Evita MoE per ora**.

2. **MXFP4 non compila in llama.cpp main**: quantizzazione MXFP4 sperimentale
   non supportata. **Usa GGUF Q4_K_M o Q8_0**.

3. **Vision models crashano** (ollama issue #14446): LLaVA, Qwen VL, bakllava
   possono crashare su Blackwell. **Solo text models per ora**.

4. **Flash Attention supportato**: Blackwell ha FlashAttention-3 ottimizzato,
   può dare +15-25% throughput.

5. **GDDR7 benefit**: la bandwidth superiore aiuta su KV cache access.

## Decisione

Adotto configurazione Ollama "ottimizzata Blackwell" tramite environment
variables User scope.

### Environment variables da settare

```powershell
[System.Environment]::SetEnvironmentVariable("OLLAMA_FLASH_ATTENTION", "1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KV_CACHE_TYPE", "q8_0", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_MAX_LOADED_MODELS", "1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "30m", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_CONTEXT_LENGTH", "16384", "User")
```

### Significato e giustificazione di ogni var

#### `OLLAMA_FLASH_ATTENTION=1`

**Cosa fa**: attiva Flash Attention algorithm (più efficiente del standard attention).

**Beneficio su Blackwell**:
- +15-25% throughput tok/s
- Meno VRAM per attention matrices
- Compatibile con CUDA 13.2

**Costo**: nessuno (disponibile su Blackwell senza caveat).

**Default Ollama**: spesso OFF. Forziamo ON.

#### `OLLAMA_KV_CACHE_TYPE=q8_0`

**Cosa fa**: quantizza il Key-Value cache (memoria attenzione) a 8-bit.

**Alternative**:
- `f16`: KV cache a 16-bit float (default, più preciso, più VRAM)
- `q8_0`: KV cache quantizzato 8-bit (meno VRAM, qualità quasi identica)
- `q4_0`: KV cache a 4-bit (molto meno VRAM, qualità degradata)

**Perché q8_0**:
- Risparmia ~50% VRAM della KV cache
- Quality loss < 1% (negligible per coding tasks)
- Permette context più lungo nella stessa VRAM

**Costo**: minimo, alcuni edge cases potrebbero avere piccoli drift qualitativi.

#### `OLLAMA_MAX_LOADED_MODELS=1`

**Cosa fa**: limita a 1 il numero di modelli tenuti in VRAM simultaneamente.

**Perché 1**:
- 8GB VRAM RTX 5060 non sopporta 2 modelli 7B insieme
- Un Qwen 2.5 Coder 7B Q4_K_M occupa ~5-6GB VRAM
- Con 2 modelli: OOM (out of memory) o forced swap RAM (~10x più lento)

**Costo**: switch modelli richiede reload (pochi secondi per 7B).

**Default Ollama**: 3. Forziamo 1.

#### `OLLAMA_KEEP_ALIVE=30m`

**Cosa fa**: tiene il modello in VRAM 30 minuti dopo ultima richiesta.

**Alternative**:
- `0`: unload immediato dopo ogni richiesta (lento se uso frequente)
- `5m`: default Ollama
- `30m`: tengo caldo per sessioni dev (1 sessione tipica)
- `-1`: mai unload (sempre in VRAM)

**Perché 30m**:
- Durante sessione dev faccio query multiple
- 30 min copre pause caffè, riflessioni, Slack check
- Dopo 30 min inattivo probabilmente faccio altro → unload è ok
- Evita "cold start" (10-15s per load 7B) per ogni query

**Costo**: VRAM occupata anche in idle. Ma è il mio PC dev, non shared server.

#### `OLLAMA_CONTEXT_LENGTH=16384`

**Cosa fa**: setta context window default a 16K tokens (vs default 4K/8K).

**Alternative**:
- 4K: default Ollama, spesso insufficiente per code review
- 8K: buono per chat
- 16K: buono per coding con molti file
- 32K: richiederebbe più VRAM, Qwen 7B supporta nativamente 32K
- 131K: Qwen 2.5 Coder massimo (richiederebbe >8GB VRAM con Q4)

**Perché 16K**:
- Sweet spot per dev workflow (un file + contesto)
- VRAM gestibile (KV cache cresce linearmente con context)
- Se serve più context → posso alzare on-demand con `-c 32768`

**Costo**: slightly più VRAM anche se non uso tutto (buffer allocation).

### Config Ollama anti-pattern

**NON settare** queste variabili (potrebbero causare problemi):

- `OLLAMA_NUM_PARALLEL > 1`: parallel requests su 8GB = OOM
- `OLLAMA_DEBUG=1`: verbose logging, rallenta (solo per debugging)
- `OLLAMA_LLM_LIBRARY`: forza library specifica, meglio default
- `OLLAMA_GPU_OVERHEAD`: manual tuning non necessario

## Conseguenze

### Positive misurate

**Benchmark reale post-config** (Qwen 2.5 Coder 7B Q4_K_M):
- **93.51 tok/s sustained** ⚡
- VRAM usage: ~6.2 GB / 8 GB
- Idle power: ~10W (quando modello non attivo)
- Active power: ~110-130W durante inference

**Comparazione con target**:
- Research diceva: 40-55 tok/s atteso su RTX 5060
- **Risultato**: +70% sopra massimo atteso

**Hypothesis su perché così veloce**:
1. Blackwell FlashAttention-3 è più ottimizzato di expected
2. GDDR7 bandwidth (504 GB/s) aiuta molto su KV cache reads
3. Q4_K_M quantizzazione ben ottimizzata su Blackwell
4. No altri carichi GPU (display uso iGPU, RTX dedicato solo a LLM)

### Positive qualitative

**Workflow dev fluido**:
- Query Qwen ha latenza ~100-200ms
- Risposta typical (100-500 tokens) in 1-5 secondi
- Feel "istantaneo" per single-turn, accettabile per multi-turn

**Qualità output** (prime impressioni):
- Qwen 2.5 Coder 7B: forte su Python, TypeScript, React
- Debole su linguaggi meno comuni (Rust, Go)
- Forte su code review e refactoring
- Medio su architettura complessa

### Negative

**Gap qualitativo vs Opus 4.7** (da misurare sistematicamente):
- Opus: capisce contesto di 1M tokens, reasoning complesso
- Qwen 7B: capisce fino 16K (config), reasoning limitato
- **Per task routine Qwen va bene. Per task complessi serve Opus o OpenRouter**.

**VRAM limit hard**:
- No modelli > 8B a full quality
- No modelli multi-modali (vision issues su Blackwell)
- Mitigation: mac mini futuro con 48GB unified memory

**Blackwell quirks**:
- Alcuni formati modello (MoE NVFP4, MXFP4) rotti
- Workflow: solo GGUF Q4_K_M / Q8_0 per ora
- Mitigation: Ollama ecosystem cambia rapidamente, fix probabile in mesi

## Alternative considerate

### Alternative 1: Default Ollama, zero env vars

**Pro**: zero setup, Ollama just works
**Contro**: performance sub-ottimale, 4K context limite
**Perché scartata**: lascio performance on the table

### Alternative 2: Flash Attention off (safer)

**Pro**: zero rischi su edge cases
**Contro**: -20% throughput
**Perché scartata**: Blackwell ha FA3 maturo, rischio basso

### Alternative 3: KV cache f16 (safer quality)

**Pro**: zero quality loss
**Contro**: +40% VRAM KV cache
**Perché scartata**: q8_0 loss è negligible, VRAM è preziosa

### Alternative 4: MAX_LOADED_MODELS=0 (no limit)

**Pro**: flessibilità massima
**Contro**: OOM garantito se provo 2 modelli 7B
**Perché scartata**: 8GB è hard limit

### Alternative 5: KEEP_ALIVE=-1 (always hot)

**Pro**: zero cold start
**Contro**: VRAM always occupied, GPU idle più alto
**Perché scartata**: 30m è sweet spot per sessioni di lavoro

## Procedure

### Setup iniziale

```powershell
# 1. Install Ollama
winget install Ollama.Ollama --accept-package-agreements --accept-source-agreements

# 2. Verifica installazione
ollama --version    # atteso: 0.21.0 o superiore

# 3. Set environment variables
[System.Environment]::SetEnvironmentVariable("OLLAMA_FLASH_ATTENTION", "1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KV_CACHE_TYPE", "q8_0", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_MAX_LOADED_MODELS", "1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "30m", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_CONTEXT_LENGTH", "16384", "User")

# 4. Restart Ollama service (per pick up env vars)
Restart-Service Ollama

# 5. Verify env vars applied (check log)
ollama ps
```

### Pull primo modello

```powershell
# Qwen 2.5 Coder 7B (coding specialist)
ollama pull qwen2.5-coder:7b

# Verifica
ollama list
# qwen2.5-coder:7b    4.7 GB    ...
```

### Benchmark tok/s

```powershell
# Single-shot benchmark
ollama run qwen2.5-coder:7b --verbose "Scrivi una funzione Python che legge un file CSV e ritorna lista di dict con gestione errori robusta"

# Cerca output "eval rate" nel terminal
# Esempio: "eval rate:    93.51 tokens/s"
```

### Quick test qualità

```powershell
# Test 1: refactoring semplice
ollama run qwen2.5-coder:7b "Refactor questa funzione per usare list comprehension:
def filter_evens(nums):
    result = []
    for n in nums:
        if n % 2 == 0:
            result.append(n)
    return result"

# Test 2: debug
ollama run qwen2.5-coder:7b "Trova il bug:
function calcularTotal(items) {
    return items.reduce((a, b) => a + b.price, 0);
}"

# Test 3: explain
ollama run qwen2.5-coder:7b "Spiega cosa fa questo codice Python:
from itertools import chain
def flatten(nested):
    return list(chain.from_iterable(nested))"
```

## Modelli raccomandati per RTX 5060 8GB

### Text LLM (Q4_K_M, 4-6GB VRAM)
| Model | Size | Use case | Tok/s target |
|-------|------|----------|--------------|
| qwen2.5-coder:7b | 4.7GB | Coding daily driver | ~90 |
| qwen3:8b | 5.2GB | Reasoning generale | ~75 |
| deepseek-r1:7b | 4.8GB | Math, logic | ~85 |
| llama3.1:8b | 4.9GB | General purpose | ~80 |
| mistral:7b | 4.4GB | Fast responses | ~95 |

### Embedding (piccoli, 0.5-1GB)
| Model | Size | Use case |
|-------|------|----------|
| nomic-embed-text | 274MB | General embedding (semantic search) |
| mxbai-embed-large | 669MB | Higher quality embedding |
| all-minilm | 45MB | Minimal embedding, veloce |

### Da evitare su 8GB VRAM
- Modelli ≥ 13B (OOM garantito)
- Multi-modali (vision crash Blackwell)
- MoE con NVFP4 (bug Blackwell)
- Modelli con context > 32K senza quantizzazione aggressiva

## Meta-learning

### Perché env vars > config file

Ollama supporta anche config file (`%APPDATA%/ollama/config.yaml`), ma
env vars hanno vantaggi:
- **Override per sessione**: posso lanciare Ollama con var diverse
- **Script-friendly**: PowerShell scripting naturale
- **Docker/container ready**: stesse var funzionano in Docker
- **Visibility**: `$env:OLLAMA_*` mostra tutto subito

### Perché User scope non System scope

- **User scope**: setting per il mio utente Windows (`edusc`)
- **System scope**: setting per tutti gli utenti (admin-only modifica)

**User scope** è sufficiente perché:
- Lenovo è solo-dev (solo io uso Ollama)
- Meno privilege = meno rischio
- Reversibile facilmente

### Il valore del benchmark reale

**Prima del benchmark**: speravo 40-55 tok/s (research generica).
**Dopo benchmark**: confermato 93 tok/s (hardware mio specifico).

**Impact decision**: ho alzato aspettative realistiche per workflow.
Per task routine (autocomplete, explain, refactor semplice), Qwen 7B è
**velocissimo** — feel quasi cloud-like.

**Lesson**: **numeri generici online sono indicativi, benchmark reali sono
auth**oritative per il tuo setup.

### Il rischio di "copypasta env vars"

Tanti blog online hanno env vars "ottimali per LLM" copy-paste.
**Pericoloso**: alcune var sono specifiche hardware, altre desktop vs server.

Ogni var che ho settato ha **giustificazione documentata** in questo ADR.
Se vuoi replicare, leggi il perché. Se cambia il tuo hardware, alcune
potrebbero non applicarsi.

### Watch-list: ri-benchmarkare in futuro

**Trigger per re-benchmark**:
- Ollama major version update (0.22, 0.23, ...)
- NVIDIA driver major update (siamo a 595, futuri 600+)
- CUDA update major (13.x → 14.x)
- Qwen 2.5 Coder → Qwen 3 Coder release

**Come re-benchmark**:
Stesso prompt di primo benchmark, confronto tok/s.
Registra in `docs/reference/ollama-benchmarks-log.md`.

## Riferimenti

- Ollama documentation: https://ollama.com/docs
- Ollama env vars reference: https://github.com/ollama/ollama/blob/main/docs/faq.md
- Blackwell sm_120 issues su Ollama GitHub: issue #14446 (vision), issue #15012 (MoE)
- Qwen 2.5 Coder model card: https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct
- FlashAttention paper: https://arxiv.org/abs/2205.14135 (v1), v3 in NVIDIA docs

## Follow-up

### Prossime verifiche

**Questa settimana**:
- [ ] Benchmark qualitativo: Qwen 7B vs Opus 4.7 su 5 task reali
- [ ] Misurare tempo risposta medio per sessione tipica dev

**Questo mese**:
- [ ] Valutare Qwen 3 8B come alternative reasoning
- [ ] Testare embedding models per RAG personale
- [ ] Context window stress test (lavoro con file grandi)

**Prossimi 3 mesi**:
- [ ] Re-benchmark su ogni major Ollama update
- [ ] Considerare modello specializzato (Phind, CodeLlama) come secondario
- [ ] Setup Cline VS Code extension con Ollama local backend
