# ADR 0007 — Aider + Qwen quantization findings su RTX 5060 8GB

**Status**: Accepted
**Data**: 2026-04-20 (sessione pomeridiana)
**Decisore**: Eduardo Scarpelli
**Tipo decisione**: tecnica, strategica (revisione Fase 2 ADR-0001, follow-up ADR-0006)

## Contesto

### Motivazione

ADR-0006 ha dimostrato che **Cline + Qwen 7B** non è viable per workflow agentic. Follow-up richiesto: testare alternative per trovare uno stack sovereign effettivamente usabile. Due variabili da isolare:

1. **Client** (Cline SEARCH/REPLACE vs Aider whole-file)
2. **Modello** (Qwen 7B vs Qwen 14B con diverse quantizzazioni)

### Obiettivi

- Validare se **Aider** (diff whole-file invece di SEARCH/REPLACE) è più tollerante per modelli piccoli
- Misurare capability 14B vs 7B su task agentic
- Identificare quantization sweet-spot per 8 GB VRAM

## Setup test

- **Client**: Aider 0.86.2 (`python -m pip install aider-install && aider-install`, venv isolato via uv, binary in `C:\Users\edusc\.local\bin\aider.exe`)
- **Backend**: Ollama 0.21.0 con env vars Blackwell-optimized (ADR-0004)
- **Modelli testati**:
  - `qwen2.5-coder:7b` (Q4_K_M, 4.7 GB, digest `dae161e27b0e`)
  - `qwen2.5-coder:14b-instruct-q3_K_M` (7.3 GB, digest `e00d09afd55a`)
  - `qwen2.5-coder:14b-instruct-q2_K` (5.8 GB, digest `dfeff73b234d`)
- **Progetto test**: Synesthesia (clone baseline pulito, commit `05f8a92`)
- **Modalità**: `aider --message` single-shot, `--no-auto-commits`, `--yes-always`, `--model ollama_chat/<tag>`

Configurazione Aider per Ollama:
- `OLLAMA_API_BASE=http://localhost:11434`
- Edit format auto-selected: `whole` (riscrittura intera file)
- Repo-map: 4096 token auto-refresh

### Baseline benchmark throughput

Stesso prompt Python DoublyLinkedList:

| Modello | Load time | Prompt eval | Sustained eval | GPU offload | Note |
|---------|-----------|-------------|----------------|-------------|------|
| 7B Q4_K_M | <1 s (cache) | 2940 tok/s | **114.20 tok/s** | 100% | ADR-0004 baseline |
| 14B Q3_K_M | 21.9 s | 137 tok/s | **10.82 tok/s** | 61.6% (2.4 GB CPU spill) | VRAM overflow |
| 14B Q2_K | 12.3 s | 170 tok/s | **18.72 tok/s** | 73.0% (KV cache spill) | Weights fit, KV no |

Osservazione architetturale: anche Q2_K (5.8 GB) non entra full-GPU perché KV cache @ context 16384 + q8_0 occupa ~2 GB. Serve o ridurre `OLLAMA_CONTEXT_LENGTH` o GPU con più VRAM.

## Test eseguiti

Replica esatta delle 4 task ADR-0006, stesso progetto Synesthesia, stesso prompt verbatim.

### Task 1 — Read + cross-file inference

Prompt: *"Read app.js in this project and explain in 3 lines what it does."*

Aider invocation: `--chat-mode ask --read app.js --message "..."`.

**Risultato Aider + Qwen 7B**: ✅ **SUCCESSO**
> "Il file `app.js` è il punto di ingresso dell'applicazione Express. Configura l'applicazione con middleware, rotte e servizi necessari per gestire le richieste HTTP, autenticare gli utenti, interagire con il database e visualizzare le pagine."

Coerente, accurato, conciso. Equivalente a Cline Task 1 (entrambi successi).

### Task 2 — EDIT con JSDoc (task critico)

Prompt: *"Trova il file controller più piccolo nel progetto. Aggiungi JSDoc comment a ogni funzione pubblica. Non modificare il comportamento."*

Nessun file pre-aggiunto: Aider deve navigare repo-map, scegliere file, applicare edit whole-file.

#### Aider + Qwen 7B: ❌ FALLIMENTO CLEAN
- Qwen scelse `services/zen.service.js` (errore semantico: è un service, non un controller; Synesthesia non ha dir `controllers/` evidente in repo-map 4096 token)
- Output conversazionale ("Verrà ora aggiunto al chat") invece di whole-file formato Aider
- **Zero edit applicati**
- Working tree invariato
- **Differenza critica vs Cline**: clean failure, non loop, no intervento manuale richiesto

#### Aider + Qwen 14B Q3_K_M: ✅ SUCCESSO (con hallucination)
- Qwen scelse `controllers/page.controller.js` (file corretto, dir `controllers/` identificata nel repo-map)
- Output whole-file formato Aider rispettato
- **43 annotazioni `@param`/`@returns` aggiunte** su 13+ metodi
- Edit applicato: 104 insertions, 5 deletions

**MA**: Q3 ha **hallucinato behavior change** su `submitOnboarding`:
- Original: redirect a `/profile/${username}`, flash "Mappatura completata! La tua sfaccettatura dominante è X (Y). Scopri cosa significa nel tuo profilo."
- Q3 output: redirect a `/dashboard`, flash "Il tuo profilo è stato aggiornato con successo. Il tuo tipo enneagrammatico principale è X.", error handling semplificato (`catch { next(error) }`)

Constraint "Non modificare il comportamento" **violato**.

Tempo: ~2 min a 10.8 tok/s.

#### Aider + Qwen 14B Q2_K: ✅ SUCCESSO completo
- Stesso file corretto (`controllers/page.controller.js`)
- Whole-file format rispettato
- ~40 annotazioni JSDoc aggiunte (in inglese, vs italiano Q3 — consistent con stile interno Q2)
- Edit applicato
- **"No behavior change" rispettato**: `submitOnboarding` preservato byte-per-byte. Diff totale: solo aggiunta JSDoc + spostamento static block (semantic-equivalent) + rimozione 2 commenti originali sostituiti da JSDoc formale.

Tempo: ~2 min a 18.7 tok/s.

### Task 3 — CREATE file nuovo

Prompt: *"Crea un nuovo file utils/validate-email.js con funzione isValidEmail(email) basata su regex RFC-5322 semplificata. Aggiungi JSDoc completo. Export ES module."*

**Aider + Qwen 7B**: ✅ SUCCESSO
- Gestiti automaticamente 2 retry dopo `llama runner process has terminated` (backoff esponenziale)
- File creato con JSDoc IT + ES module export + regex semplificata + `String(email).toLowerCase()` defensive
- Differenze minori vs Cline output (stesso prompt, LLM non deterministici): regex più permissiva, stile 4-space

14B non testato (ridondante — se 7B riesce, 14B riesce).

### Task 4 — Auto-extension

**Non riproducibile con Aider `--message`**: architetturalmente single-shot, Aider termina dopo una risposta. Qwen non può chainare comandi autonomamente (come invece ha fatto Cline quando installò Jest).

**Per replicare comportamento catastrofico Cline**: servirebbe Aider in modalità TUI interattiva con user-input-free loop. Non testato (limitato dal tempo).

## Findings

### Client layer: Cline vs Aider

| Aspetto | Cline 3.79.0 | Aider 0.86.2 |
|---------|--------------|--------------|
| Edit format | SEARCH/REPLACE (byte-perfect) | whole (riscrittura intera) |
| Tolleranza modelli piccoli | Bassa (loop su mismatch) | Alta (no format strict su edit) |
| Auto-extension rischio | Alto (tool chaining autonomo) | Basso con `--message` (single-shot) |
| Failure mode quando modello non capace | Loop → blocca workflow | Output non applicato → clean fail |
| UX quando funziona | TUI VSCode integrata | CLI Python, TTY broken in Git Bash (serve cmd.exe) |
| Warning ufficiale "works best with Claude" | ✓ Esplicito | Non pertinente (funziona con LiteLLM multi-provider) |

**Conclusione client**: **Aider è sostanzialmente più tollerante di Cline** per modelli locali piccoli. Il whole-file edit format elimina la fragilità byte-level di SEARCH/REPLACE. Il single-shot `--message` elimina scope creep catastrofico.

### Model layer: 7B vs 14B Q3 vs 14B Q2

| Dimensione | Speed (tok/s) | Capability file selection | Capability JSDoc format | Faithfulness (no-behavior-change) | Throughput-capability tradeoff |
|------------|---------------|---------------------------|-------------------------|-----------------------------------|-------------------------------|
| 7B Q4_K_M | 114 | ❌ Sbagliato (service vs controller) | ❌ Conversazionale, no format | N/A (no edit) | Veloce ma non capace |
| 14B Q3_K_M | 10.8 | ✅ Corretto | ✅ Corretto (43 JSDoc) | ❌ Hallucination | Capace ma infedele |
| **14B Q2_K** | **18.7** | ✅ Corretto | ✅ Corretto (~40 JSDoc) | ✅ Literal preserved | **Sweet spot** |

### Finding paradossale: Q2 > Q3 su faithfulness

Controintuitivo: la quantizzazione più aggressiva (Q2_K, ~4.8 bit/weight) è **più fedele** al file originale di Q3_K_M (~5.7 bit/weight). Ipotesi plausibili:

1. **Q3 "creativo"**: retiene capacità di riformulare testo → più propenso a riscrivere/migliorare
2. **Q2 "literal"**: perdita di capacità generativa → copia più fedele dell'input quando presente in context
3. **n=1**: singolo task, potrebbe essere varianza LLM. Servirebbero n>5 per statistica

Implicazione operativa: **Q2_K favorisce constraint-respect, desiderabile per refactor minimali**. Q3 favorisce creatività, potenzialmente desiderabile per "rewrite for clarity" esplicito.

### VRAM budget RTX 5060 8GB

Dati misurati:
- 7B Q4_K_M: full GPU (100%), 4.7 GB weights + KV cache quantizzato in VRAM → OK
- 14B Q3_K_M: weights 7.3 GB + KV cache → 10.34 GB totale → **spill 3.97 GB** (38%) su CPU
- 14B Q2_K: weights 5.8 GB + KV cache → 8.85 GB totale → **spill 2.39 GB** (27%) su CPU

Nessun 14B entra full-GPU su 8 GB. Workaround possibili (non testati):
- Ridurre `OLLAMA_CONTEXT_LENGTH=8192` (da 16384) → ~1 GB risparmio KV cache
- Quantizzare KV cache più aggressiva (`OLLAMA_KV_CACHE_TYPE=q4_0` vs attuale `q8_0`)
- Hardware upgrade: RTX 5060 Ti 16 GB / 5070 12 GB / Mac mini M4 Pro 48 GB unified

## Decisione

### Stack sovereign viable identificato

**Aider + Qwen 2.5 Coder 14B Q2_K + Ollama locale** è **viable** per workflow agentic limitato:

- **Forze**: capability sufficiente (file-selection + format compliance + faithful edit), clean failure mode, zero subscription
- **Debolezze**: 18.7 tok/s (6x più lento di 7B, ~3x più lento di Sonnet/Opus perceived), TTY broken in bash (serve cmd.exe/PowerShell per interactive)

### Uso consigliato per tipologia task

| Task | Stack consigliato | Perché |
|------|-------------------|--------|
| One-shot query (explain, discuss) | Qwen 7B via `ollama run` | 114 tok/s, zero overhead |
| Read + inference (Aider ask mode) | Aider + Qwen 7B | Quality adeguata, veloce |
| CREATE single file | Aider + Qwen 7B | Funziona bene, veloce |
| EDIT agentic (refactor, JSDoc, docstrings) | **Aider + Qwen 14B Q2_K** | Capability + faithfulness |
| Multi-file refactor complesso | Claude API (OpenRouter pay-per-use) o Claude Pro | Richiede planning multi-turn affidabile |
| Debug/architettura critica | Claude Sonnet/Opus | Nessun local equivalent |

### Scartato

- Cline + qualsiasi Qwen locale: la fragilità SEARCH/REPLACE non è risolvibile col modello corrente. Re-test solo quando Qwen 3 Coder rilasciato.
- 14B Q3_K_M per edit: hallucination di behavior è blocker. Usabile solo se "rewrite libero" è desiderato.

## Implicazioni per Roadmap Sovereign (ADR-0001, revisione post-ADR-0006)

### Scenario "sovereign ottimistico" **rivalidato parzialmente**

Piano Fase 2 originale ADR-0001 ("90% workflow su Ollama locale") **torna plausibile** per:
- Query one-shot: 100% locale
- Single file edit/create: 100% locale
- Read + inference: 100% locale
- Refactor semplice con constraint espliciti: 100% locale (Q2_K)

**Non copre**:
- Multi-file refactor agentic con ragionamento cross-file
- Debug strategico
- Greenfield architectural decisions

Per questi: Claude Pro $20/mese come Plan B — scenario $300-420/anno validato in ADR-0006 resta attuale.

### Revisione target budget

| Scenario | Costo/anno | Probabilità stimata | Trigger |
|----------|------------|---------------------|---------|
| Sovereign ottimistico pre-ADR-0006 | $60-240 | Scartato | — |
| Ibrido Claude Pro + Ollama (ADR-0006 baseline) | $300-420 | Default | Aider+14B sufficiente per 70-80% task, Pro per 20-30% |
| Full-sovereign revisitato (14B Q2 copre più di previsto) | $60-180 | Possibile | Se dopo 3 mesi uso reale Q2 copre >90% task, skip Claude Pro |

La decisione definitiva slitta: **3 mesi di uso reale post-19/05 su Aider+14B Q2 decideranno** se serve Claude Pro o no.

### Hardware future: priorità aggiornata

Con 8 GB VRAM ogni 14B spilla a CPU. Upgrade diventa **utile ma non critico**:
- RTX 5060 Ti 16GB (~€500): 14B full-GPU, ~50-70 tok/s stimato
- Mac mini M4 Pro 48GB (~€2500): modelli 30B+ locale, unificato
- Non pianificato prima di 3 mesi uso reale stack corrente

## Follow-up

### Completato (stessa sessione, 2026-04-20 pomeriggio tardo)

#### Test 1: `OLLAMA_CONTEXT_LENGTH` tuning su 14B Q2_K

| num_ctx | num_gpu | Speed (tok/s) | GPU offload | Layers GPU | Verdict |
|---------|---------|---------------|-------------|------------|---------|
| 16384 | auto | 18.72 | 73.0% | 44/49 | Baseline (env vars originali ADR-0004) |
| **8192** | **auto** | **25.54** | **86.3%** | 44/49 | **+36% speed, default operativo nuovo** |
| 4096 | auto | 35.23 | 90.7% | 44/49 | Context stretto per edit medi |
| **4096** | **-1** | **36.61** | **~98%** | **48/49** | **Gold standard full-GPU**, solo output projection su CPU |
| 8192 | -1 | CRASH | — | — | VRAM insufficiente, llama runner terminated |

**Decisione operativa**:
- `OLLAMA_CONTEXT_LENGTH=8192` persistito come default (User scope, `setx`) — sweet spot per Aider con repo-map tipico (~4k token) + single file (~2-3k) + prompt.
- Override per-request `num_ctx: 16384` per task multi-file complessi.
- Override per-request `num_ctx: 4096, num_gpu: -1` per query veloci single-shot dove latency conta più di context (gold standard 36.6 tok/s).
- Gold standard full-GPU **solo a ctx 4096**, non estendibile a ctx 8192 senza hardware upgrade.

**Validation post-ctx-change**: Aider+14B Q2 Task 2 (JSDoc su controller) ripetuto con ctx 8192 server default — ✅ successo, 38 JSDoc aggiunti, behavior preservato byte-per-byte (submitOnboarding identico a HEAD).

#### Test 2: `OLLAMA_KV_CACHE_TYPE=q4_0` — NON viable su Blackwell

Tentativo di dimezzare KV cache (da q8_0) per liberare VRAM. Risultato: **CUDA error su RTX 5060 sm_120**:

```
ggml_cuda_host_malloc: failed to allocate 26.01 MiB of pinned memory: resource already mapped
CUDA error: shared object initialization failed
  current device: 0, in function launch_mul_mat_q at mmq.cuh:3724
  cudaFuncSetAttribute((mul_mat_q<type, mmq_x, false>), cudaFuncAttributeMaxDynamicSharedMemorySize, nbytes_shared)
```

Stesso errore sia con q4_0 sia con q8_0 dopo il primo fallimento (pinned memory leak permane finché Ollama non resetta cleanly). Restart completo + wait risolve.

**Diagnosi**: il kernel `mul_mat_q` con quantizzazione q4_0 richiede shared memory allocation non supportata su Blackwell sm_120. Constraint architetturale nota (simile a NVFP4 MoE / MXFP4 issues documentate in `docs/research/rtx5060-ollama-benchmarks.md`).

**Decisione**: **`OLLAMA_KV_CACHE_TYPE=q8_0` mantenuto**. q4_0 potrebbe diventare viable con:
- Driver NVIDIA newer (595.79 attuale; versioni 600+ potrebbero portare fix)
- Ollama update (0.21.0 attuale; upstream llama.cpp potrebbe aggiungere q4_0 kernel Blackwell-compatible)

Re-test quando driver/Ollama aggiornati.

**Implicazione per Aider**: Aider default repo-map = 4096 token + single file content (~2-3k) + prompt (~500). Tipico <8k token, fit in ctx 8192. Se overflow, ridurre `--map-tokens 2048`.

### Completato (rigor checks successivi)

#### Test 3: Q3 re-test Task 2 (reproducibility hallucination)

Re-run Aider+Q3 Task 2 (ctx 8192 default nuovo). Risultato: **NON ha hallucinato, ma neanche prodotto output utile**:
- Prima risposta Qwen: discussione conversazionale ("Ho aggiunto JSDoc..."), no whole-file output
- Seconda turn: solo "Ok." (2 token)
- **Zero edit applicati** (vs prima volta: edit applicato con hallucination)

**Finding**: Q3 non solo rischia hallucination ma ha **alta varianza di output** — stesso prompt produce comportamenti diversi:
- Run 1: whole-file corretto con hallucination su submitOnboarding
- Run 2: nessun whole-file output, solo "Ok."

**Decisione**: Q3 è **doppiamente inaffidabile** (capability intermittente + hallucination rischio). Scartato definitivamente per agentic editing. Mantenuto come comparison baseline, non per uso produttivo.

Caveat metodologico: n=2 non statisticamente conclusivo, ma la presenza di 2 failure mode diverse su 2 run è sufficiente per trattare Q3 come non-production-ready.

#### Test 4: Aider "speed mode" (ctx 4096 + num_gpu=-1) su Task 3 CREATE

Tentativo di applicare il gold standard config (36.6 tok/s) ad Aider tramite `.aider.model.settings.yml`:

```yaml
- name: ollama_chat/qwen2.5-coder:14b-instruct-q2_K
  extra_params:
    num_ctx: 4096
    num_gpu: -1
```

**Risultato**: ❌ **Fallimento edit format**
- Qwen genera codice JavaScript corretto (JSDoc + regex + ES module export)
- Ma senza prefisso `utils/validate-email.js` richiesto da Aider whole-file format
- Aider respinge con "No filename provided before \`\`\`" → 3 reflection retry → stop
- File NON creato

**Root cause**: ctx 4096 troppo stretto per Aider workflow. Il repo-map default (4096 token) occupa già l'intero context budget. Senza room per prompt istruzioni + response, Qwen produce output malformato.

**Trade-off finalizzato**:
| Scenario | Config consigliato | Speed | Usabilità |
|----------|---------------------|-------|-----------|
| Aider agentic editing | ctx 8192, auto offload | 25.5 tok/s | ✅ Full |
| Query one-shot via `ollama run` | ctx 4096, num_gpu=-1 | 36.6 tok/s | ✅ Solo CLI |
| Aider + speed mode | ctx 4096, num_gpu=-1 | N/A | ❌ Edit format broken |

**Decisione**: gold standard config **non combina con Aider**. Speed mode utilizzabile solo per `ollama run` o chiamate API dirette. Per Aider: rimanere su ctx 8192 default.

### Test ancora da fare (bassa priorità)

- [ ] Test Aider in cmd.exe interattivo (Task 2 + follow-up "riprova perché hai cambiato redirect"): verifica se Qwen sa auto-correggere quando notificato di un errore
- [ ] Test ridurre `--map-tokens 2048` per vedere se ctx 4096 diventa usabile con Aider (repo-map dimezzato libera budget)
- [ ] Re-test Q3 con temperature=0 per isolare varianza stocastica vs capability intrinseca

### Test più lunghi (quando time permette)

- [ ] Batch benchmark qualitativo: 10-15 task coding standard, matrice (7B, 14B Q3, 14B Q2) × (create, edit small, edit medium, refactor multi-function)
- [ ] Aider con Qwen 3 Coder (quando rilasciato 2026)
- [ ] Continue.dev + Qwen 7B: alternativa da valutare? (tempo permettendo)
- [ ] Aider scripting mode (batch messages) per task parallelizzabili

### Decisioni strategiche differite

- [ ] Post-19/05 per 3 mesi: uso esclusivo Aider+14B Q2 per task quotidiane. Track fail rate (quali task richiedono fallback Claude)
- [ ] Dopo 3 mesi: rivedere budget scenario. Se fail rate <10% → skip Claude Pro. Se 10-30% → Pro. Se >30% → Mac mini upgrade o Claude Max downgrade plan
- [ ] Revisione ADR-0001 con finding validati da uso reale

## Lezioni meta

### Quantizzazione aggressiva può migliorare faithfulness

Controintuitivo ma reale: Q2_K più fedele di Q3_K_M sul constraint "no behavior change". Prima di dismissing quant aggressive come "sempre peggio", testare su **task specifici**. La perdita di creative capacity può essere **feature**, non bug, per refactor minimali.

Framework di scelta quant rivisto: non "la più alta che VRAM permette", ma "la più bassa che preserva capability desiderata per task target".

### Aider `whole` edit format vince su SEARCH/REPLACE per local LLM

Cline's Claude-centric design (SEARCH/REPLACE richiede reasoning preciso byte-level) è **architettura fragile** per modelli locali piccoli. Aider's whole-file rewrite format è **robustness-first** design: anche se modello commette errori, non entra in loop — l'edit viene applicato o fallisce pulito.

Meta-regola: quando si sceglie un client agentic per stack non-frontier, **preferire architetture robust-first** (whole-file, diff tolleranti, retry graceful) a performance-first (search/replace byte-perfect, tool chaining aggressivo).

### "Più veloce ≠ più utile"

Qwen 7B @ 114 tok/s è **inutile per edit agentic** (capability insufficient). Qwen 14B Q2 @ 18.7 tok/s è **utile** per edit agentic (capability + faithfulness). Un 6x slowdown che sblocca use case vale un ordine di grandezza vs 6x speedup su task che non riesce comunque.

Framework decisionale: capability-first, speed-second. Se speed è sufficiente (>10 tok/s feels acceptable), ottimizzare per capability.

### Negative results compongono

ADR-0006 (Cline+Qwen 7B fail) + ADR-0007 (Aider+Qwen 14B Q2 success) insieme **definiscono lo spazio viable**: non solo "cosa non funziona", ma **dove cercare**. Un singolo negative result è informativo; la sequenza negative→positive con variabili isolate mappa lo spazio delle soluzioni.

## Riferimenti

- Aider: https://aider.chat, https://github.com/paul-gauthier/aider
- Aider edit formats doc: https://aider.chat/docs/more/edit-formats.html
- LiteLLM Ollama provider: https://docs.litellm.ai/docs/providers/ollama
- ADR-0001 Sovereign AI Strategy (Fase 2 revisione confermata): `0001-sovereign-ai-strategy.md`
- ADR-0004 Ollama RTX 5060 config (env vars invariati): `0004-ollama-rtx5060-config.md`
- ADR-0006 Cline+Qwen viability (precedente): `0006-cline-qwen-viability.md`
- Qwen 2.5 Coder 14B: https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct
- Ollama model page: https://ollama.com/library/qwen2.5-coder
