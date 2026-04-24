# Journal — CodeMasterDD AI Station

Diario operativo della workstation. Una entry per sessione di lavoro significativa.

## Template

```
## YYYY-MM-DD

### Completato
-

### Da fare
-

### Note
-
```

---

## 2026-04-19

### Completato
- Verifica ambiente: Lenovo LOQ Tower 17IAX10, RTX 5060 8GB, Core Ultra 7 255HX, CUDA 13.2, Claude Code 2.1.114
- Conferma configurazione Git (Eduardo Scarpelli <eduscarpelli@gmail.com>)
- Hardening iniziale della workstation:
  - BitLocker (triplo layer) disabilitato
  - OneDrive scollegato e sync bloccato
  - Rimosso bloatware (21 pacchetti)
- Definizione roadmap strategica: Lenovo come workstation **primaria e autosufficiente**; Mac mini declassato a estensione opzionale
- Inizializzazione repository `lenovo-ai-station` (infrastructure-as-code)
- Struttura base: `scripts/`, `docs/`, `logs/`, `backup/`
- File di progetto: `README.md`, `JOURNAL.md`, `.gitignore`, `CLAUDE.md`
- Primo commit (`chore: initial project structure`)

### Da fare
- Installazione Node.js 22 LTS, Python 3.10+, VS Code, GitHub CLI
- Installazione Ollama + pull Qwen 2.5 Coder 7B
- Benchmark reale tok/s di Qwen 2.5 Coder 7B su RTX 5060
- Settimana prossima: migrazione Evo-Tactics e Synesthesia dal Ryzen

### Note
- Prima sessione di lavoro con Claude Code sulla nuova workstation.
- Convenzioni di collaborazione stabilite in `CLAUDE.md` (un comando alla volta, approvazione esplicita, italiano per la comunicazione).
- Target strategico: zero subscription ricorrenti dal 2026-05-20 (post Claude Max).

---

## 2026-04-19 (sessione serale)

### Completato
- **Obiettivo 1 — GitHub push**
  - GitHub CLI 2.90.0 installato via winget (`GitHub.cli`)
  - Auth OAuth web browser come `MasterDD-L34D` (HTTPS, scopes: `gist`, `read:org`, `repo`, `workflow`)
  - Repo privato `MasterDD-L34D/codemasterdd-ai-station` creato con `gh repo create --source=. --remote=origin --push`
  - Description impostata: "Infrastructure-as-code e journal della workstation CodeMasterDD (Lenovo LOQ Tower 17IAX10) — setup, scripts, config, decisioni architetturali. Target: AI dev workstation sovereign."
  - 3 commit pushati su `origin/main`
- **Rename workstation label**: `Lenovo AI Station` → `CodeMasterDD AI Station` (applicato a `README.md`, `CLAUDE.md`, `JOURNAL.md`)
  - Motivazione: `CodeMasterDD` identifica il device, più future-proof rispetto al brand hardware
- **Obiettivo 2 — Dev stack base**
  - Node.js 24.15.0 LTS + npm 11.12.1 (winget `OpenJS.NodeJS.LTS`)
  - Python 3.12.10 (winget `Python.Python.3.12`)
  - VS Code 1.116.0 x64 — commit `560a9dba96f961efea7b1612916f89e5d5d4d679` (winget `Microsoft.VisualStudioCode`)
- **CLAUDE.md aggiornato**
  - Sezione "Stack installato" riconciliata con stato reale (aggiunti gh CLI, Node, Python)
  - Sezione "Stack da installare questa settimana" ridotta a VS Code (completato) + Ollama
  - Sezione Evo-Tactics: aggiunta nota "Compat runtime: useremo Node 24 a livello di sistema; installeremo nvm-windows solo se emergono incompatibilità"
- **.gitignore**: aggiunta esclusione `.claude/` (settings e memory locali Claude Code, per-machine, non vanno su repo condiviso)
- **Obiettivo 4 — Ollama + modello locale (estensione serale)**
  - Ollama 0.21.0 installato via winget (`Ollama.Ollama`, installer 1.80 GB), servizio Windows auto-start
  - Pull `qwen2.5-coder:7b` (Q4_K_M, 4.7 GB, digest `dae161e27b0e`) via `ollama pull`
  - Smoke test: classe `DoublyLinkedList` Python — codice corretto con type hints e docstrings
  - Benchmark sustained su 669 token output: **93.51 tok/s** (load cache-hit 64 ms, prompt eval 2940 tok/s)
  - Risultato **~2× sopra target** CLAUDE.md originale (40-55 tok/s atteso)

### Da fare
- Settimana prossima: migrazione progetti reali (Evo-Tactics `C:\dev\Game`, Synesthesia `C:\dev\synesthesia`) dal Ryzen
- Eventuale rinomina cartella locale `C:\dev\lenovo-ai-station` → `codemasterdd-ai-station` (rimandato, operazione separata e rischiosa)

### Note
- **Node 24 vs 22 (decisione)**: il manifest winget `OpenJS.NodeJS.LTS` è stato promosso a Node 24 (Active LTS dal 2025-10-28). Scelta: tenere Node 24 vanilla — è LTS ufficiale supportato fino ad aprile 2029, più future-proof. Synesthesia già testato su Node 24; Evo-Tactics usa `engines.node: ^22` → Node 24 al peggio emette warning.
- **nvm-windows differito (YAGNI)**: non installato preventivamente. Si valuterà solo se durante la migrazione progetti emergono incompatibilità reali.
- **Obiettivi 1-4 completati**; sessione estesa oltre i 90 min iniziali per non frammentare l'install Ollama + benchmark.
- **RTX 5060 Blackwell su GGML Q4 7B**: performance sopra attese (93 tok/s vs 40-55 target). Conferma la validità tecnica del piano "AI sovereign" con questa workstation.

---

## 2026-04-20

### Completato
- **Knowledge base import**: 17 file `docs/` da claude.ai browser sessions (5 ADR, 2 lessons-learned, 3 patterns, 3 research, 1 reference, 2 sessions, 1 README), ~28k parole, single source of truth per decisioni strategiche
- **Datazione uniformata** (D2): file `sessions/` allineati a date calendaristiche del JOURNAL (la sessione del 19/04 sera ora `2026-04-19-sessione-serale.md`, prima `2026-04-20-*`)
- **Ollama env vars Blackwell-optimized applicate** (User scope, persistenti dopo riavvio):
  - `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_KEEP_ALIVE=30m`, `OLLAMA_CONTEXT_LENGTH=16384`
- **Re-benchmark Qwen 2.5 Coder 7B**: **114.20 tok/s sustained** (+22% rispetto a vanilla 93.51 tok/s del 19/04). Numero in linea con +15-25% atteso da ADR-0004 grazie a Flash Attention + KV cache q8_0.
- **Test sovereign workflow Cline + Qwen 7B (sessione notturna)**:
  - Cline 3.79.0 VSCode extension installata + configurata backend Ollama
  - Synesthesia clonato in `C:\dev\synesthesia` (commit `05f8a92`, 273 deps via `npm install`)
  - 4 task agentici tentati:
    - ✅ Read + cross-file inference (app.js spiegato correttamente in <15s)
    - ❌ EDIT con SEARCH/REPLACE (Qwen genera pattern non byte-perfect → loop)
    - ✅ CREATE single file con JSDoc (validate-email.js generato pulito)
    - ❌ Auto-extension catastrofica: Qwen ha installato Jest + @testing-library/react su progetto Express, poi loop su `npx jest --init` interactive
  - Cleanup Synesthesia eseguito (git reset + clean + npm reinstall, 280 deps parassite rimosse)
  - **Finding**: Cline + Qwen 7B NON viable per workflow agentic complesso. Roadmap Fase 2 da rivedere. Analisi completa in `docs/adr/0006-cline-qwen-viability.md`.

### Da fare
- Migrazione progetti reali (Evo-Tactics, Synesthesia) dal Ryzen — settimana prossima
- Eventuale rinomina cartella locale `lenovo-ai-station` → `codemasterdd-ai-station`

### Note
- Backend Ollama attualmente girato da sessione Claude Code (PID 2660 da `ollama serve` in background). Al prossimo riavvio PC, tray app + backend ripartono con env vars persistent (no azione manuale richiesta).
- Pattern di valore: docs/ADR pre-formalizzati hanno guidato l'esecuzione (env vars già pianificate in ADR-0004, applicate in 5 min).
- Co-authoring sull'arco completo (sessioni 19-20/04): Claude Code Opus 4.7 (esecuzione) + claude.ai browser (stesura docs/).
- **Roadmap Fase 2 (sovereign transition post-19/05) da rivedere** in sessione dedicata a mente fresca. Opzioni: Qwen 14B (VRAM borderline), alternative a Cline (Aider, Continue.dev), workflow ibrido con Claude Pro $20/mese come Plan B (budget realistico $300-420/anno vs target originale $60-240).
- **Meta-lezione**: tok/s non è l'unica metrica. Capability (instruction-following, tool compliance, precision byte-level) è ortogonale al throughput. Qwen 7B veloce ma insufficientemente capable per agentic multi-turn.
- **Negative result = result**: sessione di 2h sovereign test senza "feature" tangibile, ma findings chiari che evitano mesi di frustrazione futura.

---

## 2026-04-20 (sessione pomeridiana)

### Completato
- **Aider 0.86.2 installato** via `python -m pip install aider-install && aider-install` (venv isolato uv, binary in `C:\Users\edusc\.local\bin\aider.exe`, 110 pacchetti Python)
- **Replica ADR-0006 test su Aider + Qwen 7B** (client diverso, stesso modello):
  - Task 1 (read/explain app.js): ✅ successo
  - Task 2 (JSDoc su smallest controller): ❌ **clean fail** (Qwen sceglie `services/zen.service.js` erroneamente, output conversazionale no edit applicato — vs Cline loop SEARCH/REPLACE intrusivo)
  - Task 3 (CREATE utils/validate-email.js): ✅ successo con 2 auto-retry su `llama runner terminated`
  - Task 4 (auto-extension): non riproducibile con `--message` single-shot (safe by design)
- **Pull + benchmark Qwen 14B in 2 quantizzazioni**:
  - `qwen2.5-coder:14b-instruct-q3_K_M` (7.3 GB): 10.82 tok/s sustained, 61.6% GPU (spill 2.4 GB su CPU)
  - `qwen2.5-coder:14b-instruct-q2_K` (5.8 GB): 18.72 tok/s sustained, 73.0% GPU (spill 2.4 GB KV cache)
  - Nessuno dei due entra full-GPU su 8 GB (KV cache a context 16384 occupa ~2 GB)
- **Replica Task 2 con Aider + Qwen 14B** (stesso client, modello diverso):
  - Q3_K_M: ✅ file-selection corretta (`controllers/page.controller.js`), 43 JSDoc aggiunti, MA **hallucination behavior change** su `submitOnboarding` (redirect, flash msg, error handling modificati)
  - Q2_K: ✅ file-selection corretta, ~40 JSDoc, **behavior preservato byte-per-byte** (only diff: JSDoc + spostamento static block semantic-equivalent)
- **Finding paradossale documentato**: quantizzazione più aggressiva (Q2) preserva constraint "no behavior change" meglio di Q3 — Q2 "literal", Q3 "creative"
- **ADR-0007 creato** (`docs/adr/0007-aider-qwen-quantization-findings.md`): analisi completa, decision matrix task→stack, revisione ADR-0001 Fase 2
- **CLAUDE.md aggiornato**: stack installato + capacità AI locali con tabella benchmark tri-modello + priorità task post-Max rivista

### Da fare
- Test con `OLLAMA_CONTEXT_LENGTH=8192` per verificare se 14B Q2 entra full-GPU (guadagno stimato ~10-15 tok/s)
- Test Aider in cmd.exe interattivo (bash ha TTY broken `xterm-256color` prompt_toolkit error)
- Post-19/05: 3 mesi uso reale Aider+14B Q2 → misurare fail rate → decisione definitiva Claude Pro o no
- Migrazione progetti reali (Evo-Tactics, Synesthesia) — settimana prossima

### Note
- **Stack sovereign viable identificato**: Aider + Qwen 2.5 Coder 14B Q2_K. 6x più lento di 7B ma con capability + faithfulness adeguate per edit agentic. Scartato Cline (ADR-0006) e Q3 per edit (hallucination rischio).
- **Target budget rivalidato plausibilmente ottimistico**: scenario full-sovereign ($60-180/anno, skip Claude Pro) torna possibile se Q2 copre >90% task quotidiani. Scenario baseline resta $300-420/anno (Claude Pro + OpenRouter). Decisione differita a uso reale post-19/05.
- **Aider `whole` edit format > Cline SEARCH/REPLACE** per local LLM: robust-first architecture tollera errori modelli piccoli, failure mode è "no edit" vs "loop infinito".
- **Safe failure mode Aider**: ogni fail lascia working tree pulito. Zero danno collaterale vs Cline Task 4 catastrofe (280 npm pkg parassite).
- **Meta-lezione quantization**: testare anche quant aggressive (Q2) su task specifici. La perdita di generative capacity può essere feature (faithfulness) non bug.
- **Sessione produttiva ~2h**: install Aider + 2 pull 14B + 3 benchmark + 3 test Aider task + documentazione ADR-0007 + aggiornamento CLAUDE/JOURNAL.

### Estensione (tardo pomeriggio): ctx tuning
- **Test `OLLAMA_CONTEXT_LENGTH` su 14B Q2_K**:
  - ctx 16384 (baseline): 18.72 tok/s, 73% GPU
  - **ctx 8192: 25.54 tok/s, 86.3% GPU** → +36% speed, nuovo default
  - ctx 4096: 35.23 tok/s, 90.7% GPU → +88% vs baseline ma context troppo stretto
- Nessuna config raggiunge full-GPU su 8 GB (weights Q2 6.9 GB + OS 1 GB troppo stretti). Upgrade hardware (RTX 5060 Ti 16GB) vantaggioso ma non essenziale.
- **`OLLAMA_CONTEXT_LENGTH=8192` persistito** (setx User scope). Override per-request `num_ctx: 16384` per task multi-file (Aider con repo-map grande).
- ADR-0007 e CLAUDE.md aggiornati con matrice benchmark + rationale.

### Estensione 2 (validation + optimization): ctx 8192 persistente + KV cache + full-GPU
- **Validation Aider+14B Q2 Task 2 post restart con env ctx 8192**: ✅ successo, 38 JSDoc aggiunti, submitOnboarding byte-perfect vs HEAD. Config nuovo non rompe edit.
- **Test `OLLAMA_KV_CACHE_TYPE=q4_0`**: ❌ **NON viable su Blackwell RTX 5060** — CUDA error `launch_mul_mat_q` shared memory allocation failure. Constraint architetturale (simile NVFP4/MXFP4 issues). Re-test quando driver 600+ o Ollama upstream fix. q8_0 mantenuto.
- **Test `num_gpu: -1` per forzare full-GPU**:
  - ctx 4096 + `num_gpu: -1`: **36.61 tok/s, 48/49 layer GPU** (gold standard full-GPU, solo output projection CPU)
  - ctx 8192 + `num_gpu: -1`: CRASH (VRAM insufficiente)
  - Full-GPU su 8 GB RTX 5060 raggiungibile **solo a ctx 4096**. Non scalabile a ctx 8192 senza hardware upgrade.
- **Decisione config finale**: default `ctx 8192 + auto offload` (25.5 tok/s, equilibrio speed/context). Override API `num_ctx: 4096, num_gpu: -1` per query veloci single-shot.
- **Issue operativo emerso**: dopo kill aggressivo Ollama, CUDA pinned memory non rilasciata immediatamente → restart Ollama deve aspettare ~5s. Documentare per operations.

### Estensione 3 (rigor + edge case): Q3 reproducibility + Aider speed mode
- **Q3 re-test Task 2**: Q3 ha **varianza output alta** — run 1 hallucinated, run 2 nessun edit (solo "Ok." 2 token). Q3 **doppiamente inaffidabile** (capability intermittente + hallucination). Scartato definitivamente per agentic.
- **Aider + speed mode (ctx 4096 + num_gpu=-1) su Task 3 CREATE**: ❌ FAIL edit format. Qwen genera codice valido ma senza prefisso filename → Aider respinge → 3 reflection retry → stop. **ctx 4096 troppo stretto per Aider**: repo-map default 4k occupa intero budget, no room per prompt/response.
- **Trade-off finale config**: gold standard (36.6 tok/s) **non combina con Aider** (edit format broken). Speed mode usabile solo per `ollama run` CLI o API dirette. Per Aider: ctx 8192 default rimane config produttiva.
- **Issue operativo (ricorrente)**: CUDA pinned memory leak dopo kill. Soluzione permanente: usare tray app (`ollama app.exe`) per restart puliti invece di bash kill + background serve. Tray app gestisce CUDA state meglio.

### Estensione 4 (map-tokens + varianza format)
- **Aider + `--map-tokens 2048` + speed mode** su Task 3 CREATE: ❌ stesso fallimento format. Tokens sent dimezzati (5.6k vs 11k) ma Qwen omette filename prefix → Aider respinge.
- **Root cause rivisto**: varianza output format di Qwen 14B Q2, non budget context. Il filename prefix è inconsistente run-to-run.
- **Meta-finding importante**: anche lo stack consigliato (Aider+14B Q2 @ ctx 8192) ha **fail rate non-zero su format compliance**. In produzione aspettarsi ~10-20% edit respinti che richiedono retry manuale.
- Implicazione sovereign roadmap: il "full sovereign" ottimistico va valutato con fail rate realistico (non 0%). Budget scenario ibrido ($300-420/anno con Claude Pro fallback) probabilmente più realistico del full-sovereign ($60-180).

---

## 2026-04-21

### Completato
- **Memoria persistente popolata** (`~/.claude/projects/.../memory/`): 6 file (user profile, feedback decision style, feedback communication style, project sovereign evaluation, project migrations pending, reference strategic docs) + `MEMORY.md` index. Evitate duplicazioni con CLAUDE.md; focus su pattern di collaborazione e stato decisionale in sospeso.
- **Validation Aider in cmd.exe (JOURNAL 20/04 "Da fare")**: ✅ Aider interactive parte pulito in cmd.exe (no `prompt_toolkit` xterm-256color error come in bash). Banner corretto, prompt `>` responsive, Y/N prompts funzionanti.
- **`OLLAMA_API_BASE` persistito** (User scope, `setx`) a `http://localhost:11434` per silenziare warning Aider.
- **Scoperta grave: silent corruption Aider whole + 14B Q2** — non era su "Da fare", emerso durante validation cmd.exe:
  - Test 1 (9 righe, interactive): file → `demo.js` (1 insertion, 9 deletions); commit message misleading (`docs: add JSDoc...`)
  - Test 2 (9 righe, retry interactive): identico, **deterministico**
  - Test 3 (9 righe, `--message`): identico → **NON interactive-specific**
  - Test 4 (46 righe, `--message`): identico con `// demo.js` → **NON size-dependent**
  - Test 5 (46 righe, `--edit-format diff`): **safe failure**, no edit, file intatto → `diff` mitigation valida
  - Test 6 (46 righe, Qwen **7B**, whole): ✅ **success**, 47 JSDoc applicati, logic preserved → 7B output format compatibile
- **Root cause cristallizzato**: Qwen 14B Q2 emette filename *dentro* un code block (pattern "due block": filename-only-block + content-block). Aider `whole` parser prende il primo block come contenuto file → overwrite distruttivo. Qwen 7B emette filename fuori dal block (formato Aider-nativo) → parser OK.
- **ADR-0008 creato** (`docs/adr/0008-aider-whole-format-silent-corruption.md`): documentazione completa, matrice test, root cause, dual-stack task-routing come mitigation.
- **ADR-0007 annotato** con forward reference (header "Partially Superseded"). La raccomandazione single-stack è deprecata; restano validi benchmark, env vars, paradox quantization Q2>Q3.
- **CLAUDE.md aggiornato**: priority table ora con task-routing (cosmetic → 7B+whole, behavior-critical → 14B Q2+diff) + safety protocol Aider (diff check post-edit, no `--yes-always` su repo sporco).

### Da fare
- [ ] `udiff` edit format test (potrebbe risolvere sia silent-corruption sia no-edit di diff)
- [ ] Reproducibility 7B success su ≥3 run (n=1 attuale)
- [ ] Prompt-engineering "emit filename on its own line" per Qwen 14B Q2 (recupero marginale whole format)
- [ ] File-watcher/hook che rifiuta commit con file = solo filename (guard rail automatico)
- [ ] Wrapper script `aider-cosmetic` / `aider-refactor` per ridurre cognitive load dual-stack
- [ ] Migrazione progetti reali (Evo-Tactics, Synesthesia) — settimana prossima (da 27/04)

### Note
- **Meta-lezione "safe failure mode è asserzione, non proprietà"**: ADR-0007 aveva *inferito* safe-failure di Aider dall'architettura robust-first. Test empirici mostrano che parser può accettare input malformato e scrivere garbage in silenzio. Safety claims richiedono evidenza empirica su failure mode specifico, non inferenza.
- **Meta-lezione "display ≠ on-disk state"**: Aider mostra in output quello che il parser *credeva* di applicare (secondo block con JSDoc completo), non quello che scrive sul disco (primo block con filename). Verification obbligatoria via `git diff HEAD~1` dopo auto-commit.
- **Meta-lezione "test in condizioni triviali"**: ADR-0007 ha testato su controller reale (~180 righe) con context ricco — condizioni dove il format quirk di Qwen 14B Q2 non si manifesta. Il bug emerge con file dummy piccolo. Lezione generalizzabile: test "troppo semplici per fallire" catturano bug che complessità nasconde.
- **Pattern collaborazione confermato**: sessione open-ended con autonomia delegata dopo validation iniziale ("procedi finché non hai qualcosa di davvero importante da chiedermi") → batch di 3 test + scrittura ADR + update docs senza interruzioni non necessarie. Modello ha stoppato autonomamente quando decisione strategica richiedeva input utente (scelta tra 3 opzioni direction per ADR update).
- **Budget impact**: nessuna revisione numerica immediata (ibrido $300-420/anno resta baseline). Dual-stack aggiunge cognitive overhead — se in uso reale risulta frizione alta, spinge verso Claude Pro fallback più spesso.
- **Test artifacts**: `C:\dev\aider-tty-test\` preservato (directory throwaway ma git history contiene commit malformati `ebc2513`, `7d529c4`, `0aa511e`, `e58ecaf` — utili per ispezione futura del pattern corruption).

### Estensione 1 (delegation infrastructure, post-ADR-0008)
- **Motivazione**: ridurre consumo token Claude Max delegando task appropriati a stack locale, senza aspettare la migrazione progetti. Unlock token savings da subito (~4 settimane prima di 19/05).
- **Wrapper CLI installati** in `C:\Users\edusc\.local\bin\` (già in User PATH):
  - `aider-cosmetic.cmd` → `aider --model ollama/qwen2.5-coder:7b --edit-format whole %*`
  - `aider-refactor.cmd` → `aider --model ollama/qwen2.5-coder:14b-instruct-q2_K --edit-format diff --no-auto-commits %*`
  - Entrambi testati: `aider-cosmetic --version` e `aider-refactor --version` → `aider 0.86.2`
- **Guard rail pre-commit hook** installato globale:
  - Script bash in `C:\Users\edusc\.local\share\git-hooks\pre-commit` (msys-safe, niente regex alternation)
  - Activated via `git config --global core.hooksPath "C:/Users/edusc/.local/share/git-hooks"` (prima config globale hooks — no override di precedenti)
  - Detection: file ≤200 byte il cui contenuto (post-strip whitespace + comment prefix `//`, `#`, `;`, `--`) corrisponde a filename/basename → exit 1, ADR-0008 referenziato nel messaggio
  - Validato 3 scenari: `demo.js` pure filename → block, `// demo.js` commento → block, 47-line real edit → pass. Integration test `git commit` con corruption → blocked con exit 1
  - Bypass: `git commit --no-verify` (non raccomandato). Uninstall: `git config --global --unset core.hooksPath`
- **Delegation protocol documentato** in `docs/patterns/delegation-to-aider.md`:
  - Decision tree classification (cosmetic / behavior-critical / strategic)
  - Formato handoff ready-to-paste (cmd.exe + prompt target)
  - Review loop: cosa controllo quando torna output (success / safe fail / hook-blocked / silent corruption sospetta)
  - Tabella tracking per log `logs/aider-delegation-YYYY-MM.md` (gitignored) → foundation per Fase 6 evaluation post-19/05
  - Scenari operativi (cosmetic semplice, refactor minimale, query strategica, borderline)
  - Limitazioni note (cognitive overhead, wrapper cmd.exe-only, fail rate 14B Q2 diff ~20-40%)
- **CLAUDE.md aggiornato** con:
  - Reference al safety protocol hook (comando attivazione + uninstall)
  - Lista wrapper CLI installati
  - Link al delegation protocol

### Progress tracker
- Barra progetto: **50% → 60%** (fase 4.5 "delegation infrastructure" chiusa). Restano: migrazione progetti (15%), 3-mesi uso reale (15%), decisione budget finale (10%).

### Estensione 2 (hub model + dogfood + tracking foundation)
- **Motivazione**: feedback utente "non puoi fare tutto senza che io passo dal cmd a questo serve un hub" → architettura aggiornata: Claude Code orchestrator, user stays in chat, bash/PowerShell invoca Aider non-interattivo.
- **Dogfood 1 — cosmetic 7B+whole**: JSDoc su demo.js (46 righe) via hub. Aider invocato da bash `--message` `--no-pretty --no-stream --no-show-release-notes`. Success: commit `9280e1b`, 47 insertions, no corruption. Reproducibility 7B+whole → n=2.
- **Dogfood 2 — behavior-critical 14B Q2+diff+no-auto-commits**: refactor `divide()` da throw a return null. **Finding inatteso**: Aider diff format ha **reflection retry resilience**. Prima risposta Qwen senza filename → Aider respinto → Aider ha ri-chiesto → Qwen self-corrected con filename esplicito al 2° tentativo → edit applicato precisamente. Commit manuale `fffcbda` (workflow `--no-auto-commits` rispettato). 1 insertion, 1 deletion, preciso.
- **Finding nuovo vs ADR-0008**: la classificazione "14B Q2 + diff = safe-fail only" era pessimistica. Con reflection enabled (default 3 retry), diff format recupera da format errors comuni. Non cambia la decision (diff resta strettamente migliore di whole per safety), ma aumenta viability reale.
- **delegation-to-aider.md riscritto** con hub-first model:
  - Architettura diagram (User → Claude Code → bash → Aider → Qwen)
  - Invocation pattern canonico con flag rationale (yes-always, no-pretty, no-stream, no-show-release-notes)
  - Review loop automatico (exit code, corruption check, commit hash, diff sanity, hook output)
  - Fallback wrappers cmd.exe mantenuti come secondary
  - Sezione "Ottimizzazioni token" onesta: hub vince su file grandi/task complessi, break-even su task trivial piccoli
  - Limitazioni note (CRLF warnings, auto-translate commit, llama runner termination, reflection retry)
- **aider-delegation-log-template.md creato**: schema tabella colonne (data, task, classe, stack, esito, retry, tokens, durata, note). Esempi compilati. Aggregati mensili + trigger decisioni per Fase 6. Path template `docs/patterns/`, istanze mensili `logs/aider-delegation-YYYY-MM.md` (gitignored).

### Progress tracker
- Barra progetto: **60% → 70%** (fase 4.6 "hub completion + dogfood" chiusa). Restano: migrazione progetti (10%), 3-mesi uso reale (15%), decisione budget finale (5%).

### Estensione 3 (stress test + hook hardening)
- **Test B — stress hub su Python**: file `inventory.py` 86 righe (3 functions, 2 classes, 8 methods, no docstrings). Delegato cosmetic "Add PEP 257 docstrings" a 7B+whole via hub (bash `--message`). Success pulito: +74 insertions, -1 deletion, commit `26ee1a5` nel repo `aider-tty-test`. Tokens Aider: 1.6k sent / 1.0k received. Nessuna modifica config tra JS e Python. **Reproducibility 7B+whole: n=3 cumulativa** (JSDoc JS commit `9280e1b`, refactor JS `fffcbda` su 14B Q2, docstrings Python `26ee1a5`).
- **Test C — battery 9 edge case guard rail hook**: corruption pattern vs pass pattern. Detection 6/9 iniziale (C1 `#` prefix, C2 subdir basename, C3 subdir full path, C6 trailing whitespace, C7 empty-file-skip corretto, C5 no false positive). Gap identificati: C4 HTML `<!-- -->`, C9 C-block `/* */`.
- **Hook extended**: aggiunti 8 needle pattern in `C:\Users\edusc\.local\share\git-hooks\pre-commit` (varianti `<!-- $file -->` con/senza spazi + `/* $file */` con/senza spazi). Post-patch: **9/9 scenari coperti**, regression tests C1+C5 pass.
- **Documentazione**: ADR-0008 aggiornato con addendum "hook coverage extended + cross-language validation" — tabella scenari, matrice pre/post patch, note su coverage residua.

### Progress tracker
- Barra progetto: **70%** (iterativo: hub hardening + cross-language coverage, nessuno shift di fase). Prossimo shift: migrazione progetti (10% → 80%).

### Estensione 4 (behavior-critical reliability matrix + env fix)
- **Dogfood behavior-critical 14B Q2 + diff** 3 test varianti complessità su demo.js:
  - R1 (trivialissimo, `round()` default 3): ⚠️ **safe fail** 3 reflection exhausted, SEARCH block context mismatch byte-exact. Tokens ~1.2k/40.
  - R2 (medium, rename `Calc.mul`→`multiply`): ✅ success con drift. Qwen ha esteso rename alla string literal `op: "mul"`→`"multiply"` in history push (fuori scope esplicito ma coerente). 0 retry, 3.0k/150 tokens, 25s.
  - R3 (high strutturale, extract `_record` private method): ✅ success first-pass clean. 2 SEARCH/REPLACE block corretti, behavior preserved, pattern "extract method" riconosciuto. 0 retry, 3.1k/331 tokens, 37s.
- **Aggregato n=4 cumulativi** (con dogfood #2 `fffcbda`): 75% success (di cui 25% via reflection), 25% safe fail, **0% corruption**.
- **Meta-finding controintuitivo**: task 1-riga trivialissimo (R1) fail dove task strutturale complesso (R3) success. Ipotesi: Qwen struggle più su SEARCH exact-match su singola riga (include troppo context preamble) che su pattern strutturali canonici (extract method = training-data-friendly). Implicazione: per cambi `value → new_value` singoli preferire whole (7B) o edit manuale.
- **Fix env `OLLAMA_API_BASE` warning**: il `setx` di stamattina non ha preso effetto sulla mia bash Claude Code (spawned prima, non rilegge env). Aider docs confermano: dual-setup necessario. Creato `~/.env` con `OLLAMA_API_BASE=http://127.0.0.1:11434` (aider auto-legge in home + cwd + git root). Warning sparito, tutti i prossimi invocation puliti.
- **Aider docs fetch** da https://aider.chat/docs/llms/ollama.html: raccomandato `127.0.0.1` (non `localhost`, funzionalmente equivalente ma doc-compliant).
- **ADR-0008 aggiornato** con addendum "behavior-critical reliability matrix (n=4)".
- **delegation-to-aider.md aggiornato** sezione Prerequisiti: dual-setup (setx Windows PATH + `~/.env` bash) documentato con rationale.

### Progress tracker
- Barra progetto: **70%** (stabile: validation più robusta, noise ridotto, reliability matrix documentata).

### Estensione 5 (fase 4.7 operational hardening)
- **Knowledge update** via WebFetch aider docs: multi-file `aider f1 f2 ...` nativo, `.aider.conf.yml` in home/git-root/cwd, `set-env` per Ollama (noi già usiamo ~/.env)
- **Ottimizzazione piano**: consolidato token measurement IN test (no step separato), deferred autocomplete script, moved .aider.conf.yml template a Fase 5, elimina 30 min vs piano iniziale
- **`.gitattributes`** in `codemasterdd-ai-station` + `aider-tty-test` (`* text=auto eol=lf`): elimina CRLF warning ricorrente
- **`.aider.conf.yml` mini-template** in aider-tty-test: defaults 7B + whole + auto-commits + pretty:false + stream:false (CLI override per task-specific). Esclusione `!.aider.conf.yml` aggiunta al .gitignore per non essere ignorato da pattern `.aider*`
- **Step 3 — Multi-file delegation test**: `aider demo.js helpers.js --message "..."` → **success**. Entrambi file editati in single commit `9ab03bc`. Tokens 1.1k sent / 916 received, 25s. conf.yml defaults applicati correttamente. **Multi-file pattern validato**.
- **Step 4 — Cross-lang behavior-critical Python**: billing.py refactor `apply_discount(discount_percent 0-100)` → `apply_discount(discount_fraction 0.0-1.0)` con 14B Q2 diff + --no-auto-commits. **Success first-pass**, 0 retry, tokens 3.1k/118, 19s. Commit manuale `30c8391`. **Python + behavior-critical + diff + hub validato**.
- **n=5 cumulative behavior-critical**: 4 success (80%) + 1 safe fail (20%) + 0 corruption.
- **Step 5 — Ops docs batch**: `delegation-to-aider.md` aggiornato con:
  - Anti-pattern "value-change singola riga su diff format" (R1-lesson): preferire 7B+whole o Edit diretto per cambi trivial
  - Sezione "Task strategic non-delegabili" protocol (criteri, cosa cambia, no-compensation attesa)
  - Recovery flow algoritmo (4 step: read fail signal → classifica azione → budget retry ≤2 → escalation path)
  - Rollback pattern table (4 situazioni: reset hard / reset soft / revert / checkout)
  - Scenario 4 riscritto per multi-file cosmetic (nuovo), Scenario 5 per multi-file refactor
  - CRLF warning marcato risolto con riferimento `git add --renormalize`

### Progress tracker
- Barra progetto: **70% → 75%** (fase 4.7 "operational hardening" chiusa). Restano: migrazione progetti (10% → 85%), 3-mesi uso reale (10% → 95%), decisione budget finale (5% → 100%).

### Estensione 6 (test hub su strategic content + ADR-0009)
- **Obiettivo**: testare il hub su task "strategic content" (ADR con research online) che per ADR-0008 è esplicitamente classificato **non-delegable**. Verificare empiricamente se la regola regge.
- **Research phase (me)**: 2 WebSearch su "Qwen 3 Coder 2026" e "Aider 2026 roadmap". Findings raccolti in `docs/research/ai-stack-evolution-2026.md`:
  - Qwen3-Coder-Next rilasciato Feb 2026: MoE 80B/3B-active, 256K ctx, performance ~Claude Sonnet 4 agentic
  - Aider 2026: ancora attivo (39K stars, 4.1M installs), support Gemini 2.5 + OpenAI o-series
- **Delega phase (Aider 7B + whole, hub bash)**: invocato con `--read` research file + `--message` structured prompt per CREATE `docs/adr/0009-upgrade-strategy.md`. Aider ha creato + committato auto in 2 commit consecutivi (`b231500` prep + `ea08e86` content). Tokens Aider: **2.7k sent / 710 received**, 25s.
- **Review phase (me)**: Aider draft quality **D+**. Issues critici:
  - Data sbagliata (`2023-04-21` invece di `2026-04-21`, Qwen hallucination)
  - Content shallow: bullet-point riassunto del research, non analisi/sintesi
  - Trigger criteria non concreti ("se il benchmark verificato lo consente" — vago)
  - Opzioni non sono opzioni ma restatement del prompt
  - No cross-references ad ADR 0001/0007/0008
  - No risk analysis, no budget impact scenari, no timeline
  - Path separator backslash vs convention forward-slash
  - Style inconsistente (no tabelle comparative come altri ADR)
- **Azione (opzione B scelta)**: draft Aider tenuto in git history + rewrite completo via mio Write tool. Dai 2 commit Aider → 3° commit con refactor completo. Git history mostra before/after per documentazione empirica.
- **Token accounting finale**:

| Fase | Tokens miei stimati | Note |
|------|---------------------|------|
| WebSearch ×2 | ~3400 (input) | costo fisso, identico in entrambi i path |
| Write research file | ~2500 (output) | necessario in entrambi i path |
| Invoke Aider + read output | ~700 | solo hub path |
| Review Aider output | ~600 (output) | solo hub path |
| Rewrite ADR completo | ~4500 (output) | hub path: rewrite ~70%; direct path: full write |
| JOURNAL entry + commit | ~1000 (output) | uguale entrambi |
| **Total hub path** | **~12700** | — |
| **Total direct path (stimato)** | **~9000-10000** | senza Aider delega |

- **Verdict empirico**: hub ~25-40% **più costoso** del direct su strategic content. **Conferma ADR-0008 rule** "strategic non-delegable" basata su empiria, non solo teoria.
- **Finding interessante**: Qwen 7B ha **hallucinato la data** (2023 vs 2026) — segnale che il modello non ha contesto temporale affidabile senza training cutoff recente. Rilevante per T1 trigger ADR-0009: se usiamo Qwen3-Coder-Next in futuro, verificare temporal grounding prima di task che richiedono date accurate.
- **ADR-0009 prodotto** (versione rewrite): framework trigger-based per upgrade modello/hardware/client 2026-2027. Definisce T1 (modello → Qwen3-Coder-Next con 4 condizioni) + T2 (hardware con trade-off RTX 5060 Ti €500 vs Mac mini €2500) + T3 (Aider switch, no trigger attivo). Integra findings research (MoE efficiency, Aider longevity) con reliability matrix di ADR-0008.
- **Meta-lezione**: il TEST STESSO ha generato value misto: (a) draft scartato lato contenuto, ma (b) conferma empirica della regola ADR-0008 + (c) dato pricing preciso su "cost strategic delega". Il test NON è fallito anche se la delega è stata scarsa — abbiamo imparato con dati.

### Progress tracker
- Barra progetto: **75%** stabile (test di validation empirica, no phase shift). ADR-0009 deliverable aggiuntivo oltre scopo originale fase 4.7.

### Estensione 7 (memory hygiene + aider-log helper)
- **Memory hygiene**: tutte le memorie file-based aggiornate per riflettere stato post-fase 4.7 + ADR-0009. Nuovo `feedback_hub_delegation_pattern.md` documenta hub-first pattern + regola strategic non-delegable empiricamente confermata. `project_sovereign_evaluation.md` aggiornato con reliability matrix n=5 + trigger decisionali ADR-0009. `reference_strategic_docs.md` esteso con ADR-0009, research file, delegation doc, infrastruttura out-of-repo.
- **Script `aider-log`** (`C:\Users\edusc\.local\bin\aider-log`, bash + chmod +x): helper auto-compilazione tracking log. Input: output Aider via stdin + flag metadata. Parsing auto di tokens (1.1k/916), commit hash, outcome (heuristic: hook-block > safe-fail > success > error), retry count (awk). Crea `logs/aider-delegation-YYYY-MM.md` con header al primo uso del mese, poi appende righe tabellari.
- **Validato 3 scenari** sintetici: success pulito, behavior con 2 retry, hook-block. Tutti parsed correttamente. Bug iniziale (retry count duplicato da `grep -c || echo`) fixato con `awk`-counter.
- **Doc aggiornati**: `delegation-to-aider.md` sezione Tracking + `aider-delegation-log-template.md` istruzioni "Come usare" → pipe Aider output a `aider-log` con metadata. Fallback manuale mantenuto per scenari non-pipe-friendly.

### Progress tracker
- Barra progetto: **75%** stabile (wrap-up items, no phase shift). Tutta la fase 4.7+4.8 "operational hardening & meta hygiene" chiusa. Prossimo step naturale: Fase 5 migrazione (10% → 85%).

### Estensione 8 (audit + qwen3-coder:30b discovery + validation)
- **Audit repo** (PowerShell script utente) eseguito 2026-04-21 02:55. Repo clean, origin allineato, 20 commit recenti coerenti. Anomalie: (1) CLAUDE.md versione Claude Code 2.1.114 vs actual 2.1.116, (2) scripts/ vuota. Fix immediati: version bump + copia `aider-log` in `scripts/aider-log.sh` come source-of-truth repo (commit `813dedf`).
- **Discovery critico**: `qwen3-coder:30b` (18 GB, MoE 30.5B/3B-active, Q4_K_M, 256K ctx) **già installato** ~4h prima. ADR-0009 T1 trigger Condition 1 (Ollama support) **empiricalmente già MET**.
- **Benchmark suite qwen3-coder:30b** via ollama API diretta:
  - ctx default (256K) → ❌ OOM `12.2 GiB required, 10.0 GiB available`
  - ctx 2048 → ✅ 23.8 tok/s (1543 tokens in 64.9s)
  - ctx 4096 → ✅ 24.0 tok/s (1601 tokens in 66.6s, 9.4s cold reload)
  - ctx 8192 → ✅ 23.3 tok/s (1826 tokens in 78.4s) — **RAM 14.1/15.4 GB used, 1.3 GB free, CPU/GPU 66/34, VRAM 91%**
- **Finding bottleneck revisionato**: RAM (non VRAM) è il limiting factor. MoE richiede tutti i weights loadable anche se 3B attivi. Implicazione ADR-0009 T2: upgrade 32 GB DDR5 (~€80) sblocca qwen3 margine confortevole, **cheap path** vs RTX 5060 Ti 16GB (€500).
- **Quality validation dogfood** (Aider + qwen3-coder:30b + diff su `aider-tty-test`):
  - **R3 extract method**: ✅ success first-pass, diff **byte-identical** a 14B Q2 R3 reference (ADR-0008). Tokens 3.0k/310, 70s (vs 14B Q2 37s → speed 2× slower prompt-eval overhead MoE)
  - **R1 value-change 1-line** (anti-pattern documentato in delegation-to-aider.md — 14B Q2 safe-fail 3 retry exhausted): ✅ **success first-pass** 🎯. Qwen3 ha emesso SEARCH block minimale (solo function target, zero preamble) → byte-exact match. Tokens 3.0k/84, 41s. **Capability jump reale confermato**.
- **Decisione operativa** (non switch totale, promozione tier escalation):
  - 14B Q2 rimane default behavior-critical (speed 2× + RAM margine 3.7× più largo)
  - qwen3:30b diventa **tier 2 escalation** quando 14B Q2 safe-fails (R1-type o anti-pattern simili)
  - Claude Pro/OpenRouter tier 3 solo se anche qwen3 fallisce
  - T2 hardware ridefinito: RAM upgrade 32GB come priorità, non GPU
- **Doc aggiornati**: ADR-0009 addendum completo con matrice benchmark + quality validation + decisione rivista + routing aggiornato tier 1/2/3 per task class; delegation-to-aider.md anti-pattern R1 extension con workaround Qwen3; CLAUDE.md modelli locali + priority routing con tier escalation; JOURNAL estensione 8.
- **Meta-finding**: Qwen3-Coder-30B-A3B MoE risolve empiricamente un anti-pattern che avevamo classificato "non-delegable sotto certa classe" con 14B Q2. Upgrade senza hardware change (per uso occasionale tier 2) è immediatamente possibile. Il full-daily use richiederebbe 32GB RAM.

### Progress tracker
- Barra progetto: **75%** stabile (validation work, no phase shift). Qwen3-30b entra come tier 2 escalation validato empiricamente; non rimpiazza stack attuale. Prossimo step: Fase 5 migrazione (10% → 85%) o test ulteriori su Qwen3 quality spectrum.

### Estensione 9 (qwen3-coder quality spectrum extension)
- **R2 rename** (14B Q2 aveva success+drift su string literal): qwen3:30b **byte-identical + same drift**. Tokens 3.0k/115, 89s. Parity con 14B Q2. Il drift è comportamento LLM generale, non modello-specifico.
- **R-cosmetic JSDoc whole format** (14B Q2 = silent corruption; 7B = clean success): qwen3:30b **clean success**, 46→93 righe, +47 insertions 0 deletions. Tokens 1.2k/720, 210s. Commit `2b1680f` in aider-tty-test.
- **Finding strutturale**: qwen3:30b NON ha il silent-corruption bug di 14B Q2 su whole. Emette formato Aider-nativo corretto (filename on own line + single code block). Stessa famiglia architetturale di 7B su questo aspetto.
- **n=4 cumulative qwen3:30b** con Aider dogfood: tutti success (R1, R2, R3, R-cosmetic), 0 safe-fail, 0 corruption. Parity capability con 14B Q2 su task "normali" (R2, R3), capability jump su R1 anti-pattern.
- **Speed penalty consolidata**:
  - Cosmetic JSDoc: 8× slower che 7B (210s vs 25s) — qwen3 NOT viable replacement per 7B
  - Behavior diff: 2-3.5× slower che 14B Q2 (70-89s vs 25-37s) — qwen3 come escalation ok
- **Decisione stack confermata** (nessuna revisione ADR-0009):
  - Cosmetic default 7B + whole (speed imbattibile)
  - Behavior default 14B Q2 + diff (speed + margine RAM)
  - Behavior escalation qwen3:30b + diff (capability R1-type) — tier 2 validato
  - Bonus: qwen3:30b + whole disponibile come safe fallback (no corruption risk)
- **Qwen3 value proposition chiarita**: non game-changer speed ma **architectural safety upgrade** — eliminates silent-corruption risk che afflige 14B Q2 su whole format. Resolve R1-type anti-pattern. Stack sovereign diventa più robusto con qwen3 come tier 2 invece che Claude Pro direct fallback.

### Progress tracker
- Barra progetto: **75%** stabile (Qwen3 quality spectrum mappato, n=4 validation). Prossimo shift: Fase 5 migrazione.

### Chiusura sessione 2026-04-21

**Sessione densa**: 13 commit, 50% → 75% (+25 punti). Tutta la fase operativa hub/safety/escalation + validazione Qwen3 chiusa.

**Commit timeline della giornata**:
1. `0cc905a` — ADR-0008 silent-corruption finding + dual-stack decision
2. `5a35cb7` — delegation infrastructure v1 (wrappers + hook + protocol)
3. `0f9b37d` — hub-first rewrite + tracking template
4. `95b1b90` — hook 9/9 coverage + cross-language validation
5. `b3b6e10` — reliability matrix n=4 + OLLAMA_API_BASE env fix
6. `abd7b38` — fase 4.7 operational hardening (multi-file + cross-lang + ops docs)
7. `b231500` + `ea08e86` — Aider auto-commits ADR-0009 draft (D+ quality)
8. `4c1e0e0` — ADR-0009 upgrade strategy rewrite + hub strategic-content test findings
9. `60fd17c` — aider-log helper + memory hygiene
10. `813dedf` — audit anomaly fixes (Claude Code 2.1.114→2.1.116, aider-log in scripts/)
11. `4cda62d` — qwen3-coder:30b validato tier 2 escalation
12. `80b8825` — qwen3-coder:30b n=4 validation + architectural safety finding

**Finale highlights**:
- Hub Claude Code → Aider → Qwen locale: pattern operativo validato
- 3-tier task routing: 7B cosmetic / 14B Q2 behavior / qwen3:30b escalation / Claude strategic
- Guard rail hook silent-corruption: 9/9 coverage, global activation
- Qwen3-Coder-30B-A3B (MoE): installato + validato (R1/R2/R3/R-cosmetic all success, resolve anti-pattern R1 dove 14B Q2 fallisce)
- ADR-0007/0008/0009 coerenti con empiria n=4+5+3 test
- Tracking infrastructure: `aider-log` helper + `logs/aider-delegation-YYYY-MM.md` schema
- Memory files aggiornati per ripartenza domani: nuovo `project_session_resumption.md` snapshot + MEMORY.md index esteso

**Ripartenza domani — punto operativo**:
- Barra 75% → next 85% è Fase 5 migrazione
- 3 opzioni discusse (A full / B solo Synesthesia / C pre-prep only): decisione differita
- Open topic parallelo: RAM upgrade 32GB DDR5 (~€80) sblocca qwen3 default + ctx 16384
- Memoria primaria da leggere al restart: `project_session_resumption.md` per snapshot completo

**Stato repo fine giornata**: working tree clean, origin/main allineato, 0 commit locali non pushati. Tutti i 13 commit della sessione sono su `github.com/MasterDD-L34D/codemasterdd-ai-station`.

---

## 2026-04-22

### Completato

**Parte 1 — Integrazione materiale esterno (sessione claude.ai web 2026-04-21)**

- Triage selettivo `final-research-and-snippets-2026-04-21-v3.md` (42KB, 5 sezioni + 4 snippet + 3 idee ADR)
- Curation ratio: 3/12 blocchi integrati (~25%), zero bulk-dump
- Commit `f164f90`: +51 righe `docs/research/ai-stack-evolution-2026.md` (74→125 righe)
  - Sezione OpenCode come alternativa client valutata (Claude Code-compatibilità + portabilità codex by-design)
  - Sezione OpenRouter rate limits reali (50/day no-credit vs 1000/day con $10 one-time) + scenari budget + trigger riattivazione
  - Sezione framework "5 Levels of Agentic Software" (Agno) come bookmark concettuale (posizionamento attuale: L2 sofisticato con routing custom)
- `gh skill` CLI esplorato (rilasciato 16/04/2026, gh 2.90.0 compatibile): 3 skill bookmarked senza install (`openrouter-aider-orchestration`, `aider expert`, `migrate-to-claude`)
- Scartato: lista repo GitHub (reference-only), snippet script one-time OneDrive/BitLocker (già eseguiti), RotationPool Python (non applicabile Ollama puro), meta-lezione filosofica rubber duck, idee ADR format (marginali ADR-0010+)
- Materiale sorgente retained local-only via `.git/info/exclude` (pattern `final-research-and-snippets-*.md`)
- Memory entry creata: `feedback_external_material_triage.md` documenta pattern triage (25% ratio, test "già nel codex?", adattamento tono, retain-no-cancel)

**Parte 2 — Fase 5 migrazione Evo-Tactics completata**

- Pre-prep Synesthesia: scoperto **già migrato** (sync perfetto con origin/main dal 20/04, node_modules OK, working tree clean)
- Migrazione Evo-Tactics (`github.com/MasterDD-L34D/Game` → `C:\dev\Game`): clone + full validation in ~50 min
- **Step-by-step**:
  1. Clone 75 MB, ultimo commit `d319404e` (M11 Phase B→TKT-05)
  2. Engines inspect: no `engines` in root, solo `tools/memory-plugin` richiede `node>=18` → Node 24 compatibile
  3. `HUSKY=0 npm install`: 402 packages in 53s, HUSKY=0 rispettato (`.husky/_/` NON creato, hooksPath resta globale)
  4. Guard rail dual-layer: modificato `.husky/pre-commit` con wrapper che chiama `~/.local/share/git-hooks/pre-commit` alla fine. Marcato `skip-worktree` (invisibile a git status, zero upstream contamination)
  5. `npm run prepare`: husky attivato, `core.hooksPath=.husky/_`
  6. **Test empirico wrapper**: branch throwaway + file `test-dummy.txt` con contenuto `test-dummy.txt` → commit blocked da silent-corruption check (ADR-0008) → **catena wrapper validata end-to-end**
  7. Python deps: `pip install -r requirements-dev.txt` (30 packages totali inclusi transitive), `evo_schema_lint.py --help` gira clean
  8. `npm run lint:stack`: exit 0
  9. **`npm run test:api`: tutti gli stage della catena `&&` PASSANO su Node 24** (~20 min). Include api/*.test.js, tsx orchestrator tests, serviceActor, tutorialSpeciesExistence, speciesIndex 37 test, damage_curves 10 test, ecc. — stima 710+ test totali cumulativi
- **D2=c confermato empiricamente**: zero nvm-windows fallback necessario

### Da fare

- Fase 6: 3-mesi uso reale + tracking log compilation (maggio→agosto 2026, non comprimibile)
- Fase 7: budget decision ADR finale post-Fase 6 (~30 min)
- Opzionale parallelo: upgrade RAM 32GB DDR5 (~€80) per sbloccare qwen3:30b default + ctx 16384

### Note

**Finding Step 8 — shell incompatibility (non Node)**:
- Primo tentativo `npm run test:api` fallito con `"ORCHESTRATOR_AUTOCLOSE_MS" non è riconosciuto` (Windows cmd.exe default non comprende sintassi Unix env-inline)
- Root cause: monorepo Game scritto con pattern Unix `VAR=val command`, senza cross-env
- **Fix user-level**: `npm config set script-shell "C:\Program Files\Git\bin\bash.exe" --location=user` → impatta TUTTI i progetti npm Windows futuri
- Alternative considerate e scartate: install cross-env (invasivo upstream), `.npmrc` locale (duplica tra repo), wrap bash -c (fragile)
- Rischio side-effect globale: basso (progetti npm moderni usano cross-env o equivalenti; se un progetto ha script Windows-specific si rompe, reversibile con `npm config delete script-shell --location=user`)

**Finding Step 9 — security upstream**:
- `.env` NON in `.gitignore` del repo Game (best-practice gap upstream, NON introdotto da noi)
- `apps/trait-editor/.env.local` tracked MA contiene solo config Vite pubblica (no secret)
- 22 npm vulnerabilities da `npm install` (1 critical, 12 high, 8 moderate, 1 low) — upstream, da triagiare in Fase 6 o PR upstream separato
- 0 secret hardcoded trovati (2 match pattern-based = false positive su base64 embed PNG e video)

**Decisioni architetturali**:
- **D1=a** (husky wrapper preserva entrambi i guard rail): validato empiricamente, pattern riusabile per futuri repo con husky propri
- **D2=c** (Node 24 first, zero fallback): YAGNI vincente, CLAUDE.md policy onorata
- Skill `security-review` non adatta a fresh clone (opera su pending changes) → custom grep + npm audit più efficaci

**Pattern emersi utili**:
- `git update-index --skip-worktree` per modifiche locali a file tracked che non devono finire upstream (es. guard rail wrapper)
- Test empirico hook con file che triggera check specifico = validazione catena wrapper infinitamente più affidabile di "trust the wiring"
- Expected-value tempo decisionale: (c) YAGNI preferibile se P(success) > 25% — regola generale per decisioni setup-preventive

### Progress tracker

- Barra progetto: **75% → 85%** (Fase 5 migrazione completata in 1 sessione grazie a pre-prep Synesthesia already-done + Evo-Tactics clean D2=c)
- Prossimo shift naturale: Fase 6 (tracking log 3 mesi, maggio→agosto) — NON comprimibile

**Stato repo fine sessione**: working tree codemasterdd-ai-station clean, 1 commit pushato (`f164f90`). Repo `Game` clonato e operativo ma non modificato upstream (solo skip-worktree lato client).

### Parte 3 — Security scan + rivalutazione approfondita materiale esterno (serale)

**AgentShield one-shot baseline**:
- `npx ecc-agentshield scan` su codex → Grade B (80/100), 11 findings
- Hardening applicato:
  - ACL CLAUDE.md ristretto via `icacls` (Authenticated Users rimossi)
  - Rimosso wildcard `Bash(python -c ' *)` da `.claude/settings.local.json` allow
  - Aggiunta `deny` list esplicita 9 pattern (git push --force, rm -rf /, sudo, --no-verify, chmod 777, ssh, > /dev/)
- Report salvato `docs/reference/agentshield-scan-2026-04-22.md` (commit `be315c9`)
- Verdetto tool: pattern-matcher ingenuo (false positive su deny rule itself, Unix-centric su Windows). One-shot accettabile, no CI integration.

**Rivalutazione approfondita materiale esterno** (spawn 6 subagent research paralleli):
- **A1 Repo list**: verificato metadata 8 repo tramite `gh`. Top finding: `affaan-m/everything-claude-code` 162k⭐ + `rohitg00/awesome-claude-code-toolkit` ha killer companion apps (ccusage 11.5k⭐ offline token tracking, getburnd cost-control)
- **A2 OpenRouter rotation**: pattern standard 2026 = **`models: [...]` array native** in request body. RotationPool custom = anti-pattern deprecato. LiteLLM overkill per single-provider
- **A3 Agno cookbook Ollama**: cartella dedicata Ollama nel cookbook, pattern tool use 15 righe copiabile as-is. Bookmark snippets, no framework adoption
- **A4 MADR**: 129 repo GitHub vs 723 Nygard. v4.0.0 corrente (09/2024). Tool ecosystem (adr-kit, VSCode extension). Adottare da ADR-0010+, NO retrofit
- **A5 Y-Statement**: marginale 2024-2026, Zimmermann stesso deprecato in MADR. Uso 1-liner TL;DR informale in italics invece
- **A6 gh skill testing/python**: 2 skill LambdaTest (pytest-skill, mocha-skill) thin templates, autore enterprise, MIT. Preview eseguito, no install senza use case

**Azioni implementate (post-rivalutazione)**:
- Creato ADR-0010 in formato MADR bare-minimal (adozione MADR da 0010+ + skill policy `gh skill preview`-before-install)
- Aggiunto TL;DR 1-liner retroattivo su tutti i 9 ADR esistenti (add-only, zero logic change)
- Salvati 2 script PowerShell in `scripts/` (disconnect-onedrive.ps1, bitlocker-hard-disable.ps1) per future setup machines
- Creato `docs/reference/agno-ollama-snippets.md` (1 pattern tool-use 15 righe + link cookbook)
- Estesa sezione OpenRouter in `ai-stack-evolution-2026.md` con pattern rotation corretto (`models: []` native)
- Aggiunta sezione "Claude Code companion apps" in `ai-stack-evolution-2026.md` con ccusage/getburnd/cc-safe-setup come candidati post-Max tracking

**Scartato consapevolmente (rivalutazione conferma)**:
- Y-Statement formale → sostituito da 1-liner informale
- VoltAgent subagent → primary concept Claude Code, non Aider-compatible
- joelhooks/opencode-config → opencode-specific + stale (gennaio 2026)
- Rubber duck meta-filosofia → pattern già nei fatti
- RotationPool custom → anti-pattern 2024+
- Migrazione retroattiva 9 ADR a MADR → sunk-cost, no ROI

**Obiettivo file sorgente raggiunto al 100%**: tutte le proposte integrate o scartate consapevolmente. `final-research-and-snippets-2026-04-21-v3.md` candidato a cancellazione quando l'utente autorizzerà.

**Stato repo fine Parte 3**: 14 file changes (10 modificati + 4 nuovi) pronti per commit unico bundle.

### Parte 4 — Steelman review onesto degli scarti + ammissioni bias

**Motivazione**: user ha chiesto esplicitamente re-evaluation obiettiva di tutto ciò scartato/parziale, senza difesa delle decisioni precedenti ("se porta vantaggi dobbiamo riconsiderarlo").

**Metodo**: spawn 6 subagent paralleli in **modalità steelman esplicita** (fai il caso più forte PRO l'adozione di ciascun item, poi verdict onesto).

**2 bias mio scoperti e ammessi**:

1. **Agno Pattern 2 (memory)** — scarto "richiede Postgres" era **falso**. `SqliteDb(db_file=...)` è drop-in nativo Agno, zero infrastructure. Il mio ragionamento era pigro (non ho cercato alternativa). Corretto in `docs/reference/agno-ollama-snippets.md`.
2. **VoltAgent subagent** — scarto "non Aider-compatible" era **category error**. Claude Code È il primary orchestrator documentato nel hub pattern. Subagent Claude Code sono first-class nel tuo stack. Aider è il tier delegato, non il controller. Corretto in nuovo `docs/reference/subagents-skills-candidates.md`.

**6 scarti riconsiderati con valore emerso**:
- VoltAgent: 4 subagent utili (code-reviewer, test-automator, dependency-manager, debugger)
- alirezarezvani/claude-skills: `skill-security-auditor` operazionalizza ADR-0010; `monorepo-navigator` match Evo-Tactics
- affaan-m oltre AgentShield: `instincts` (formalizza ADR empirici) + `memory hooks` (automatizza JOURNAL)
- rohitg00 oltre companion apps: `commit-guard.js` complementare al guard rail
- hesreallyhim: 3 external tool concreti (TDD Guard, recall, claudia-statusline) — non bookmark-only
- Rubber duck meta-pattern: valore documentale per future sessioni Claude (non "pratica ovvia")

**5 scarti confermati con rationale stress-tested**:
- MADR retrofit 9 ADR esistenti (ROI marginale, TL;DR retroattivo già copre 80%)
- RotationPool Python custom (anti-pattern, `openrouter-free` PyPI copre casi free-tier multipli)
- Y-Statement formale (sostituito da 1-liner italics)
- OpenCode configs (stack non usa OpenCode)
- GateGuard pip install (aspetta replica indipendente claim quality +2.25)

**Correzione verdetto preview alirezarezvani/claude-skills**:
Tentato `gh skill preview alirezarezvani/claude-skills engineering/skill-security-auditor` → **FAIL**: "no skills found. This repository may be a curated list rather than a skills publisher". Repo ha struttura custom non `gh skill`-compatibile standard. Adozione richiede manual clone + run `./scripts/install.sh --tool claude-code`. Finding aggiornato in `docs/reference/subagents-skills-candidates.md` con caveat.

**Integrazione concreta**:
- Clone read-only di `rohitg00/awesome-claude-code-toolkit` in `C:\dev\scratch\` per inspezione
- `commit-guard.js` (41 righe JS zero-dep) copiato localmente in `scripts/hooks/commit-guard.js` come asset. **Non attivato** come hook — documentato il pattern per activation on-demand
- Template `monorepo.md` ispezionato ma non salvato (Evo-Tactics ha già CLAUDE.md 35KB dedicato, ROI nullo)

**4 azioni nuove implementate**:
1. `docs/reference/agno-ollama-snippets.md` Pattern 2 corretto con SqliteDb drop-in
2. `docs/reference/subagents-skills-candidates.md` (nuovo) — catalogo curato 5+ subagent + 5 skill + 3 external tool + 1 hook preview-worthy
3. `docs/lessons-learned/ai-as-thinking-partner.md` (nuovo) — rubber duck meta-pattern per future sessioni Claude
4. `docs/research/ai-stack-evolution-2026.md` estesa con 3 external tool (TDD Guard, recall, claudia-statusline)

**Memory aggiornata**: `feedback_external_material_triage.md` ora include lesson #10 (steelman review scopre bias primo round) + lesson #11 (verificare empiricamente compatibility dichiarata).

**Stato repo fine Parte 4**: 2 modificati (agno-snippets, ai-stack-evolution) + 3 nuovi (subagents-skills-candidates, ai-as-thinking-partner, scripts/hooks/commit-guard.js) + memory local.

### Parte 5 — Inaugurazione Fase 6 + trigger delega in-session (A+D)

**Motivazione**: user ha fatto audit della sessione — 5 commit, zero deleghe ad Aider nonostante hub pattern esistesse. "Perché uso ancora solo token Claude Code?"

**Root cause**: hub pattern ADR-0008 esiste ma **manca feedback loop** in-session che ricordi di classificare+delegare prima di default Claude-direct.

**Azione A — Inaugurazione Fase 6**:
- Creato `logs/aider-delegation-2026-04.md` (local-only, gitignored) dal template esistente
- Entry baseline + **audit retroattivo** sessione 2026-04-22: delega mancata significativa solo sui 9 TL;DR retroattivi ADR (savings stimato ~2000-3000 token Claude, ~$0.03-0.05). Tutto il resto classificato strategic (non-delegabile) o break-even. Stima ~70% strategic / 30% mechanical
- Periodo utile raccolta dati: 2026-04-23 → 2026-04-30 (8 giorni residui aprile)

**Azione D — Regola trigger delega in-session in CLAUDE.md**:
- Nuovo bullet sotto "Priorità modelli AI" → "Trigger delega in-session (SEMPRE attivo, non solo post-Max)"
- Policy: prima di ogni Edit/Write file esistente, classificare cosmetic/behavior/strategic e proporre delega se cosmetic o behavior-critical
- **Soglia trigger principale**: batch operazioni simili ≥5 (es. 9 TL;DR retroattivi)
- Task <1 riga meccanica skip (overhead > savings)
- Anti-pattern esplicitamente vietato: "default inerziale 'faccio io direct' senza classification"

**Impatto architetturale**: questa regola cambia TUTTE le future sessioni — prima di Edit/Write esistente, classification step obbligatorio. Contribuisce a Fase 6 empirical tracking.

**Lezione**: hub pattern funziona solo se accompagnato da trigger loop esplicito. La regola è più importante del tool.

**Stato finale sessione 2026-04-22**: 6 commit totali (commit sesto in Parte 5), barra 85% → ~87%, Fase 6 formalmente inaugurata, codex autoconscio dei propri bias metodologici (Parte 4) + istituzionalmente vincolato a delegare quando appropriato (Parte 5).

### Parte 6 — Activation commit-guard hook + ccusage install (A1+A2 azioni residue)

**Azione 1 — commit-guard.js hook attivato**:
- Adattato script da formato `process.argv[2]` (Claude Code legacy) a **stdin JSON** (Claude Code 2.1+ standard)
- Test manuale PASS: messaggio malformato (`"bad message without colon"`) → exit 2 + stderr; messaggio valido (`"feat: add new feature"`) → exit 0
- Hook config aggiunto in `.claude/settings.local.json` (gitignored):
  ```json
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [
        { "type": "command", "command": "node scripts/hooks/commit-guard.js" }
      ]}
    ]
  }
  ```
- Complementare al guard rail globale git: ora PRIMA del git commit, Claude intercetta messaggio malformato

**Azione 2 — ccusage installato + baseline findings**:
- `npm install -g ccusage` → 368ms, 0 deps, MIT, `ryoppippi/ccusage@18.0.11`
- Report daily dei 3 giorni precedenti via analisi `~/.claude/projects/*.jsonl` (offline, zero API):

| Data | Tokens totali | Cost equivalente |
|------|---------------|------------------|
| 2026-04-19 | 8.1M | $8.16 |
| 2026-04-20 | 58.3M | $41.09 |
| 2026-04-21 | 93.1M | $69.51 |
| **Totale 3 giorni** | **159.5M** | **$118.76** |

**Finding economicamente rilevante**: ~$40/giorno medio. Se post-19/05 pagassi Opus 4.7 pay-per-use senza Max, sarebbe ~$1200/mese = **6× il costo Claude Max attuale** (€200 ≈ $215). **Conferma empirica necessità delegation Aider + Ollama per sostenibilità economica post-Max**.

Cost observation: cache read (155M su 159M totali, 97%) indica prompt caching Anthropic sta funzionando bene — il cost sarebbe 3-4× superiore senza cache. Adopter di Claude Code 2.1+ beneficia automaticamente.

**Dataset Fase 6 arricchito**: ora ho baseline spending + tracking passivo automatizzato per i prossimi 3 mesi. Quando Fase 6 chiude ad agosto, confronto pre/post delega Aider sarà misurabile in $.

**Stato finale sessione 2026-04-22**: **7 commit totali** (commit settimo in Parte 6), barra ~87% → ~88%, stack operativamente completo con:
- Hub pattern ADR-0008 operationalized (trigger delega in CLAUDE.md)
- Fase 6 tracking attivo su 2 dimensioni (aider-delegation-log manuale + ccusage token automatico)
- commit-guard PreToolUse hook attivo (defense-in-depth commit message quality)
- AgentShield baseline hardening + skill-policy preview-before-install (ADR-0010)
- Reliability validation tools pronti (TDD Guard, recall documentati come candidati futuri)

---

## 2026-04-22 (addendum — hardware RAM upgrade)

### Completato
- **Upgrade RAM fisico**: 16 GB DDR5 → **64 GB DDR5-5600** (2×32 GB Micron CT32G56C46S5.C16D, dual channel ChannelA-DIMM1 + ChannelB-DIMM1). Misura post-upgrade: 63.37 GB totali, 54.38 GB liberi idle.
- Verifica empirica via `Get-CimInstance Win32_PhysicalMemory` — 2 moduli identici, velocità configurata 5600 MT/s.
- **CLAUDE.md aggiornato**: hardware section + nota modelli AI post-upgrade + `OLLAMA_CONTEXT_LENGTH=8192` marcato come "razionale decaduto, rivalidazione richiesta" + `qwen3-coder:30b` promosso da tier 2 borderline a tier 2 stabile (rimossa nota "RAM tight 1.3 GB free").
- **ADR-0012 scritto** (MADR format): `docs/adr/0012-ram-upgrade-64gb-impact.md` — documenta cosa cambia subito (decisioni a rischio zero) e cosa è deferred a bench empirico (14B Q2 @ ctx 16384, qwen3:30b rebench, candidati 30B+ dense come Qwen 2.5 Coder 32B Q4).
- Memory `project_sovereign_evaluation.md` aggiornata: blocker RAM tight rimosso dal ragionamento tier 2.

### Da fare (task deferred, sessione separata)
- **Bench empirico** con prompt standard ADR-0007 (DoublyLinkedList Python) + condizioni controllate:
  - 14B Q2 @ ctx 8192 vs 16384 vs 32768 → se ctx 16384 ≥90% speed di 8192, promuovere env var default. Se regressione >10%, il collo è VRAM/KV compute non RAM.
  - qwen3-coder:30b @ ctx 8192 ripetuto (sanity check post-upgrade) + @ ctx 16384/32768.
  - (Opzionale) Pull Qwen 2.5 Coder 32B Q4_K_M (~19-20 GB) come candidato tier 2 dense.

### Note
- Upgrade **opportunistic**, NON triggerato formalmente da ADR-0009 T2. Documentato retroattivamente come materializzazione parziale del trigger senza attraversare decision framework (ADR-0012 nota esplicita).
- **Numeri tok/s pre-upgrade restano validi**: misurati empiricamente, non RAM-bound alla sorgente. L'upgrade apre finestra rebench, non la forza — evita di inquinare Fase 6 mid-stream.
- **Impatto Fase 6**: dogfood cosmetic 7B-whole già raccolti (n=3) intatti. Dogfood futuri behavior-critical (14B Q2) continuano con ctx 8192 default finché non esiste bench.
- **Impatto Fase 7 budget decision**: scenario sovereign rafforzato qualitativamente (tier 2 locale più solido → meno escalation pay-per-use). Non quantificabile ora, dipende da fail rate empirico Fase 6.
- Barra progetto invariata **88%**: l'upgrade non avanza Fase 6 (serve tempo) né Fase 7 (serve dato).

---

## 2026-04-22 (sera tardi — bench empirico eseguito)

### Completato
- **Bench 8 run totali** con prompt standard ADR-0007 (Python DoublyLinkedList, `temperature=0`, `num_predict=300`), metriche via API `/api/generate` parse JSON:
  - 14B Q2 @ ctx 8192/16384/32768 → 25.39 / 17.28 / 11.62 tok/s
  - qwen3:30b @ ctx 8192/16384/32768 → 30.67 / 30.65 / 29.78 tok/s
  - qwen2.5-coder:32b dense @ ctx 8192/16384 → 3.65 / 3.52 tok/s (Run 7 + 7b bonus)
- **Pull Qwen 2.5 Coder 32B Q4_K_M** (19 GB @ 9.3 MB/s, ~35 min download background)
- **Script bench creato** `scripts/bench-ollama.ps1` (warm-up + misura + parse JSON, ctx override runtime via API)
- **Log completo** `docs/research/bench-post-ram-upgrade-2026-04-22.md` (metodologia + risultati + findings + decisioni)
- **Addendum ADR-0012** con sintesi findings + decisioni finalizzate

### Findings chiave
1. **RAM extra NON aiuta 14B Q2** (25.39 tok/s @ ctx 8192 vs baseline 25.54 = noise). Collo è VRAM+compute.
2. **RAM extra aiuta MASSICCIAMENTE qwen3:30b**: +31.6% @ ctx 8192 (30.67 vs 23.3 baseline "RAM tight"). Beneficio correlato a % CPU spill.
3. **qwen3:30b MoE ctx-insensitive**: da ctx 8192 a 32768 solo -3% (rumore). Ctx doppio gratis per multi-file.
4. **32B dense scartato**: 3.65 tok/s, 8.4× più lento di qwen3:30b MoE a size pari. CPU-bound (73% CPU, 32B attivi full-weight).
5. **Regressione -7.7% su 14B Q2 @ ctx 16384** (17.28 vs 18.72 baseline ADR-0007) — tracking: Ollama drift o rumore, non blocker perché default resta ctx 8192.

### Decisioni prese
- `OLLAMA_CONTEXT_LENGTH=8192` **RESTA default globale** (tier 1 14B Q2 coerence)
- qwen3:30b tier 2 **promosso a ctx 16384 default** via override per-request (zero penalty, raddoppia effective ctx)
- qwen2.5-coder:32b dense **scartato** come candidato tier routing (reference only)
- Hub pattern ADR-0008 **invariato e rafforzato**
- Scenario sovereign Fase 7 rafforzato qualitativamente

### Da fare (deferred)
- **Task #13**: valutare deepseek-r1 + gpt-oss:120b pullati parallelamente (2026-04-22) — non prioritario
- **Task #14**: indagare file API keys su Desktop — cautela, chiedere utente prima di leggere
- Integrare override `num_ctx=16384` in `aider-refactor.cmd` per task multi-file (o wrapper dedicato)
- Monitorare regressione 14B Q2 ctx 16384 in uso reale

### Note
- Bench durato ~2h totali (inclusi 35 min pull 32B in background)
- Monitor Claude Code nativo usato per attendere pull (pattern riproducibile per long-running background task)
- Modelli aggiuntivi scaricati dall'utente in parallelo (deepseek-r1:8b, gpt-oss:120b) non benchati in questa sessione — task #13 dedicato
- Barra progetto invariata **88%** (bench è dato empirico non avanzamento fase)

---

## 2026-04-22 (notte — combo F: cloud tier 3 validation)

### Completato
- **Step A — Validazione 4 provider cloud** via curl minimal:
  - Groq `llama-3.3-70b-versatile` ✅
  - OpenAI `gpt-4o-mini` ✅
  - Gemini `gemini-2.5-flash` ✅ (richiede `thinkingBudget: 0`)
  - Cerebras `llama3.1-8b` ✅ — ma `gpt-oss-120b`/`qwen-3-235b` nel catalog inaccessibili (paid tier)
- **Step B — Primo dogfood reale Aider + Groq** (Fase 6 #4):
  - Target: `scripts/bench-ollama.ps1`, task cosmetic additive (2 `.EXAMPLE` + `.NOTES`)
  - Result: SUCCESS, 11 insertions, 1 retry format, **~10s wall**, $0.0033 cost ($0 free tier)
  - Primo validation end-to-end del pattern `.aider.conf.yml` + `env-file` auto-load
- **Step E — Bench speed cloud vs locale** stesso prompt DoublyLinkedList:
  - **Groq llama-3.3-70b: 630.86 tok/s** (20.6× vs qwen3:30b locale)
  - **Cerebras llama3.1-8b: 733.5 tok/s** (6.4× vs qwen 7B locale)
- Script `scripts/bench-cloud.ps1` creato (riusabile per future bench)
- ADR-0013 Addendum scritto: da **Proposed** a **Validation-in-progress**

### Findings strategici
- **Cloud ridefinisce tier routing online**: speed 6-20× vs locale, capability 70B > 30B MoE
- **MA**: 3 caveat bloccanti prima di shift definitivo:
  1. Privacy (source code to cloud = data retention)
  2. Quality coder non validato (llama general vs qwen coder-specialist)
  3. Bench singolo n=1 (variabilità + reliability statistica pending)
- **Decisione**: tier routing CLAUDE.md NON aggiornato ancora; continuare Fase 6 dogfood reali per quality + reliability validation
- Pattern proposto documentato in ADR-0013 Addendum per review + esperimento controllato

### Da fare (deferred)
- Quality bench (HumanEval-like) Qwen Coder vs Llama general
- Dogfood Fase 6 behavior-critical cloud (attualmente solo cosmetic validato)
- Eventuale wrapper `aider-cloud` con routing esplicito provider (opzione D menu, non attivata)
- Task #13 deepseek-r1 + gpt-oss:120b locali (deferred, ortogonale a cloud)

### Note
- Utente ha concesso auto-pilot ("continua in automatico chiedimi conferma solo per cose veramente importanti") → sessione eseguita con minimi interrupt su decisioni strategiche
- **Dogfood #4 è il primo task reale con cloud tier 3** — milestone Fase 6
- Costo sessione combo F: $0.0033 Groq (dogfood) + $0 bench (usage non-chargeable per bench endpoint). Free tier ampiamente sufficiente
- Privacy nota: repo `lenovo-ai-station` è infrastructure-as-code personale, nessun segreto. Cloud OK qui. Per repo cliente revisione caso-per-caso

---

## 2026-04-23 (notte — ADR ratification + fix sweep)

### Completato
- **ADR-0014 scritto + Accepted** stessa sessione: Fase 6 timeline compression da 3 mesi → ~4 settimane (rationale: ADR-0013 risolve Q1+Q2 infrastrutturalmente; Q3 quality validabile in settimane; Q4 reliability ottenibile con n≥20 in 4 settimane).
- **Quality bench framework creato** (`scripts/quality-bench/`): 10 problemi easy + 5 hard Python, runner multi-provider, sandbox subprocess, parse resilience.
- **2 iterazioni bench eseguite**: v1 easy 60 test, v2 hard 25 test. **Totale 75 test, 100% pass@1 universale su 5 modelli coder**. deepseek-r1 framework-limited su thinking mode (5/10 con num_predict=2000, non capability issue).
- **Finding strategico**: problem set standard non discrimina modelli moderni coder-capable → quality parity locale/cloud **confermata** → shift cloud-first ha senso solo per speed, non capability.
- **Dogfood #6** behavior-critical reale: retry logic su `scripts/bench-cloud.ps1` via wrapper `aider-groq`, 1st-try success, $0.0030 free tier. Primo behavior-critical cloud Fase 6.
- **ADR-0013 → Accepted** (ratificato): speed + quality + privacy + wrapper + dogfood tutti PASS + OK utente.
- **ADR-0014 → Accepted** (ratificato): rationale confermato dal bench 75 test + OK utente.
- **Sweep check pre-close**: 4 fix applicati
  1. Retry logic `bench-cloud.ps1` refactored (dead branch `HttpWebResponseException` inventato da dogfood #6 → rewrite pulito con `$statusCode` + transient detection robusta PS 5.1/7+)
  2. README.md aggiornato (hardware 64GB, stack full, roadmap compressa)
  3. ADR-0004 status con superseded notes (num_ctx 8192 + "evitare MoE" superati)
  4. Questo JOURNAL entry

### Findings strategici
- **Timeline progetto compressa -3 mesi**: ETA barra 100% da ~fine agosto 2026 → ~**fine maggio 2026**
- **Budget scenario target**: da ibrido Claude Pro $240-420/anno → **full-sovereign $0-50/anno** via free-tier cloud (Groq+Cerebras) + Ollama locale
- **Zero subscription ricorrenti** realistica come default post 2026-05-19

### Da fare (Fase 6 compressa, ~4 settimane)
- Raccolta passive ≥14 dogfood aggiuntivi per n≥20 target
- Cost tracking mensile <$20/mese check via ccusage
- Privacy validation in sessioni reali (Synesthesia mixed particolare attenzione)
- Review settimana 2 (~2026-05-07) + settimana 4 (~2026-05-20) per decisione chiusura Fase 6

### Note
- Sessione totale 22-23/04: **~8.5 ore, 14 commit** (da 2c37172 a commit finale fix sweep)
- **3 ADR strategici ratificati** same-night: 0012 (RAM) + 0013 (cloud) + 0014 (compression)
- **4 wrapper cloud + 2 wrapper locali** operativi con cp1252 fix preventivo
- **6 dogfood Fase 6 inaugurali** (3 locale + 2 cloud cosmetic + 1 cloud behavior-critical) — 100% success cumulative
- **Quality bench framework** riusabile per future re-run mirati
- Barra globale **88% → 88%** invariata (fasi-based, attende chiusura Fase 6), ma "robustezza dell'88%" cresciuta significativamente

---

## 2026-04-23 (sera — integrazione framework archivio + normalizzazione governance)

### Completato
- **Analisi strutturale "Principal Engineer + Systems Architect + Technical PM + Archivist"** dello stato reale del progetto, con produzione 9 sezioni (snapshot, reality map, core priorities, continuation strategy, phased roadmap, sprint plan, open decisions, backlog, next action)
- **Primo round governance files**: scritti 7 file root-level (PROJECT_BRIEF, COMPACT_CONTEXT, DECISIONS_LOG, BACKLOG, OPEN_DECISIONS, ROADMAP, SPRINT_01) con schema custom basato sull'analisi del progetto reale
- **Scoperta `Archivio_Libreria_Operativa_Progetti/`** (~130 file, importato 20:42 stesso giorno): framework operativo multi-progetto con bootstrap kit + 07_CLAUDE_CODE_OPERATING_PACKAGE + libreria prompt + workflow + template reali + reference OCR TikTok. Framework è **game-biased** per default (master orchestrator menziona "game repository", FIRST_PRINCIPLES_GAME_CHECKLIST, ecc.)
- **Conflitto fonti riconciliato** (CLAUDE_OPERATING_RULES regola 1 "non scegliere in silenzio"):
  - Schema template archivio ≠ schema custom dei miei 7 file
  - 4 file del kit mancanti nella mia prima scrittura (MASTER_PROMPT, REFERENCE_INDEX, PROMPT_LIBRARY, MODEL_ROUTING)
  - `FIRST_PRINCIPLES_GAME_CHECKLIST` N/A (non game repo)
  - Meta-regole 07_OPERATING_PACKAGE da coabitare con CLAUDE.md progetto-specifico
- **Proposta riconciliazione A+B+C+D+E presentata all'utente** con opzioni esplicite (rewrite totale / merge ibrido / solo missing files) + **OK utente "procedi"** ricevuto
- **Secondo round governance files** (merge ibrido):
  - 5 file riscritti seguendo schema bootstrap-kit mantenendo contenuto ricco (PROJECT_BRIEF 9 sezioni template, COMPACT_CONTEXT 9 sezioni template, DECISIONS_LOG ibrido ADR-index + "Decisioni NNN", OPEN_DECISIONS formato `[OD-NNN]`, BACKLOG con "Primo sprint consigliato" inline)
  - 4 file creati nuovi compilati col contesto reale (MASTER_PROMPT portabile, REFERENCE_INDEX con 30+ asset catalogati per categoria GOV/ADR/PAT/RES/LES/REF/SES/LOG/ARC/X, PROMPT_LIBRARY con prompt universali + 7 progetto-specifici + scenari, MODEL_ROUTING con 10 modelli + 4 policy + evoluzione post-Fase-6)
  - ROADMAP + SPRINT_01 retained come extension progetto-specifica (non nel kit standard ma high-value)
- **3 Decisioni non-ADR registrate** in `DECISIONS_LOG.md`:
  - Decisione 001 — Adozione schema framework archivio per governance files
  - Decisione 002 — `FIRST_PRINCIPLES_GAME_CHECKLIST` N/A per questo repo
  - Decisione 003 — Regole 07_OPERATING_PACKAGE restano nell'archivio, non duplicate al root
- **Pointer propagati**: `CLAUDE.md` sezione "Governance meta-operativa" + ordine lettura nuove sessioni; `README.md` indice 11 file governance
- **Commit `4f5227c`** (122 file, +7867 righe): envelope A basso rischio, zero codice toccato. Push `a23b533..4f5227c main -> main` ✅
- **Memory refresh** `project_session_resumption.md` trasformata in lean pointer (HEAD aggiornato + nota integrazione + pointer a `COMPACT_CONTEXT.md` per snapshot completo). Evita duplicazione contenuto.

### Da fare (post-sessione)
- **SPRINT_01 T1** — Dogfood behavior-critical cloud #2 (retry logic su `scripts/quality-bench/run-bench.ps1` via `aider-groq`) per sbloccare P1 + validare fix cp1252
- **SPRINT_01 T2** — Dogfood cosmetic batch JSDoc/help su script residui
- **M3 condizionale** — Wrapper PowerShell alternative se fix cp1252 fallisce sotto retry reale
- **M5** — Privacy validation sessione Synesthesia (criterio 3 ADR-0014)
- **Review settimana 2** ~2026-05-07

### Note
- **Lezione meta-metodologica**: la mia prima analisi "Principal Engineer" è stata completa sul dominio-progetto ma **cieca al framework operativo importato la stessa mattina**. L'utente ha dovuto indicare esplicitamente "dovresti trovare tutto qui" → scoperta archivio → necessità di rifare. Insegnamento: aprire sessione con `ls` root + `ls` cartelle recenti quando lavoro su analisi strutturale, non assumere che il CLAUDE.md sia l'unica fonte di governance.
- **CLAUDE_OPERATING_RULES regola 1** applicata correttamente nel secondo round: conflitto esplicitato + riconciliazione proposta + OK utente prima di procedere. Questo rituale ha prevenuto rewrite ciechi.
- **File-first regola** (CLAUDE_OPERATING_RULES #4) rispettata: la sessione produce 11 file + 2 edit + 1 memory refresh + 1 commit, non long chat explanations.
- **Change budget** envelope A (basso rischio): solo docs, zero codice, zero impatto stack AI operativo. Sessione ~1h ma output durevole (framework setup + navigable governance).
- **Barra progetto invariata 88%**: governance normalization non è progresso fase, è **infrastructure quality**. L'ETA di chiusura Fase 6 non cambia, ma il progetto è ora **materialmente più operabile** da sessioni future (umane o agenti) grazie a schema prescrittivo consistente.

---

## 2026-04-23 (sera tardi — SPRINT_01 T1+T2 execution)

### Completato

**T1 — Dogfood behavior-critical cloud #2 (REJECT)**
- Target: refactor `Invoke-Model` in `scripts/quality-bench/run-bench.ps1` per retry logic con exponential backoff (5 constraint: signature preservation, return values per 2 branch divergenti, max 3 attempts, discriminator 429/5xx vs 4xx, informative exhaustion)
- Delega: `aider-groq.cmd` con Groq llama-3.3-70b-versatile + diff + `--no-auto-commits`
- Cost: $0.0059 (free tier $0)
- **Outcome**: ❌ REJECT manual — **5 constraint violations di cui 1 BLOCKING**:
  - 🔴 Bug #1 BLOCKING: `return $r.message.content` usato per entrambi branch, ma cloud richiede `$r.choices[0].message.content` → cloud branch **silent-fails return null**
  - Bug #2: `$maxAttempts = 5` vs richiesto 3
  - Bug #3: retry su QUALSIASI exception, zero discriminator 4xx
  - Bug #4: `throw $_` senza attempt count informativo
  - Bug #5: comment in italiano (convention violation)
- Rescue: `git checkout` revert + Edit manuale Claude Code con helper `Invoke-ModelRequest` rispettando TUTTI 5 constraint. PowerShell parser validation PASS, 48 insertions / 2 deletions. Commit `f80ab3c`.

**T2 — Dogfood cosmetic #8 (partial success)**
- Target: fix apostrofo elisione `"un implementazione"` → `"un'implementazione"` + condensare NOTES in `scripts/bench-ollama.ps1` (bug introdotto da Groq in dogfood #4)
- Delega: `aider-cosmetic.cmd` con Qwen 7B local + whole + `--git-commit-verify` + `--commit-prompt English`
- Cost: $0 (locale)
- **Outcome**: 🟡 partial — fix apostrofo ✅, condensazione NOTES ❌ (7B conservativo, skippa transformation)
- Auto-commit retry observed: 1° msg `\`\`\`docs:...\`\`\`` → commit-msg hook BLOCK ✅ → Aider self-retry → 2° msg `fix: correct spelling error in script comment` → passed → commit `2dccec7`
- Zero silent-corruption, 0 retry sull'edit

**Documentazione findings**
- `OPEN_DECISIONS.md` + OD-006 (routing threshold constraint-count)
- `MODEL_ROUTING.md` + sezione "Finding empirico 2026-04-23 — constraint count come seconda dimensione routing"
- `BACKLOG.md` + H6 (validare OD-006 con n≥3 dogfood aggiuntivi)
- `logs/aider-delegation-2026-04.md` + entries dogfood #7 + #8 con breakdown per classe aggiornato

### Findings strategici

**Fase 6 dataset n=8 (end 2026-04-23 22:20)**:
- Cosmetic: 5 full success + 1 partial (92% rate)
- Behavior: 1 success + 1 REJECT (50% rate)
- Silent-corruption working-tree: 0 ✅
- Silent-semantic-corruption intercepted at review: 1 (#7 return-value divergence)
- Cost cumulative: $0.0148 (~0.07% di $20/mese budget)

**Pattern constraint-count routing** (OD-006):
- 1 constraint semplice: qualsiasi tier ~100%
- 2-3 constraint mix fix+transform: local 14B Q2 o cloud 70B ~80-85%
- 5+ constraint strict semantic: cloud 70B **degrada a ~20%** — manual rewrite preferito
- Ipotesi: capacity LLM ≤70B di preservare simultaneamente constraint = ~3, oltre "dimentica" i trasformativi

**cp1252 monitoring H3**: ANCORA pending dopo 5 dogfood consecutivi (#4-#8) senza retry loop naturale. 4 success 1st-try + 1 auto-retry 2nd-try. Considerare test sintetico se nessun trigger entro n=12.

**Criteri ADR-0014 closure update**:
- Criterio 2 (reliability): 8/20 (40%), fail rate 12.5% (vs 30% threshold) ✅, zero corruption ✅
- Criterio 3 (privacy): invariato 1/3
- Criterio 4 (cost): 0.07% di soglia ✅
- Trend on-track per closure ~2026-05-20

### Da fare
- **H1** — +3 behavior-critical per chiudere target n≥5 (attuale 2)
- **H2** — +4 cosmetic per n≥10 (attuale 6)
- **H3** — continuare monitoring cp1252 fino n=12 o test sintetico
- **H6** — validare OD-006 con n≥3 dogfood di constraint-count variabile
- **M5** — Synesthesia privacy session (criterio 3)
- **Review settimana 2** ~2026-05-07

### Note
- **Primo REJECT cloud dopo 3 success**: dato rilevante per ridimensionare euforia ADR-0013. Cloud 70B NON è silver bullet — rafforza "Claude Code review manuale MANDATORY" come safety net non opzionale.
- **Hook ADR-0011 validato empirically dogfood #8**: 1° message invalido bloccato, 2° message passato. Gate funziona come da design — Aider self-retry è compatibile con commit-msg policy.
- **Lesson per SPRINT_01 T2**: non forzare batch ≥5 cosmetic se non ci sono candidates naturali. Singolo task opportunistico (apostrofo fix + potential condense) è comunque valid data point. Target numerici arbitrari vanno rivisitati se realtà non li supporta.
- **File-first regola rispettata**: output sessione = 2 commit codice + 4 docs update + 1 log local entry. No long chat explanations.
- **Sessione durata**: ~1h (T1 delega + rescue + commit + T2 delega + auto-commit + 4 docs update). Bilancio positivo: 2 dogfood + 2 commit pushati + strategic findings consolidated.
- Barra progetto **invariata 88%**: Fase 6 ora 40% (8/20) vs precedente 30% (6/20). Progress Fase 6 non muove barra fasi-based ma conta per chiusura.

## 2026-04-24 (notte — governance drift audit + commit-guard hardening + ADR-0016 draft)

### Contesto
Sessione auto-mode con trust esplicito utente ("fai tutto da solo"). Obiettivi emersi in-session: audit drift governance post-sera T1+T2 + opportunistic dogfood reali + chiusura OD-006 via ADR formalizzazione. Nessun task pre-pianificato.

### Completato

**Governance drift audit** (commit `9ab01e9`)
- Scan cross-file di: `PROJECT_BRIEF`, `ROADMAP`, `MODEL_ROUTING`, `MASTER_PROMPT`, `COMPACT_CONTEXT`
- 4 file disallineati post-sera identificati. Fix: HEAD refs, Fase 6 30% → 40%, $0.0089 → $0.0148 cumulative, P1 n=1 → n=2, rimosso P4 self-reference drift-memory (già risolto), aggiunto P7 cloud degradation (OD-006 driver).
- `COMPACT_CONTEXT` lasciato aggiornato dal commit precedente (non in questo batch).
- File touched: 4, insertions 12, deletions 12.

**Dogfood #9 — HEREDOC false-positive commit-guard** (commit `0fa0016`)
- **Discovery in-session**: il hook `scripts/hooks/commit-guard.js` ha bloccato un mio commit con HEREDOC pattern (`git commit -m "$(cat <<'EOF' ... EOF)"`) perché la regex `/-m\s+["']([^"']+)["']/` cattura `$(cat <<` come messaggio.
- **Delega**: `aider-refactor` (Qwen 14B Q2 diff) con message-file 3-righe + 2 constraint esplicit (fix + preserve).
- **Risultato**: 1st-try, 0 retry, 7.0k/282 tok, diff additive 6 righe (check `command.includes('<<')` + `console.log` + `exit 0`). Test 3/3 pass (HEREDOC skip, valid pass, invalid block).
- **Small smell accettato**: `console.log` inquina stdout del hook. Polish deferred a #11.
- **Meta**: self-referential — fix sblocca il bug che bloccava il fix.

**Dogfood #10 — command.includes() false-positive commit-guard** (commit `3156edf`)
- **Discovery in-session**: scrivendo il prompt file per #10, la mia bash command conteneva la stringa "git commit" nel contenuto del file, e il hook `commit-guard.js` è scattato perché `command.includes('git commit')` matcha substring ovunque.
- **Delega**: `aider-refactor` (Qwen 14B Q2 diff), 3 constraint (replace check + preserve HEREDOC + preserve validation).
- **Risultato**: 1st-try, 0 retry, 7.0k/**169** tok (più efficient di #9), edit 1-line (regex start/separator). Test 6/6 pass (valid commit, chained, invalid block, echo skip, cat/heredoc skip).
- **Secondo consecutive behavior-critical local 100%** — 14B Q2 tier confermato top-range ADR-0008 hub pattern.

**Dogfood #11 — polish console.log → stderr** (commit `3231e2e`)
- **Polish** smell di #9. `aider-cosmetic` (Qwen 7B whole), 1 constraint (change stream).
- **Risultato**: 1st-try edit, **1 auto-commit retry** (1° msg Qwen 7B = `Subject: scripts\hooks\commit-guard.js` — file path as subject disaster mode come #2, hook block, auto-retry genera `fix: update log level...` valid).
- **Pattern auto-commit retry confermato n=2** (dopo #8): gate + Aider self-retry = architettura robusta ADR-0011 Gap 2C.

**ADR-0016 draft — Constraint-count as second routing dimension** (commit `9bcc2a4`)
- **Formalizzazione OD-006** con n=6 data points cross-tier + n=11 cumulative.
- **Proposta**: matrice 2D routing (classe × constraint-count) estende ADR-0008 hub pattern.
- **Soglie empiriche**:
  - 1 constraint → qualsiasi tier ~100%
  - 2-3 additive/preserve → 14B Q2 local o 70B cloud ~100%
  - 2 fix+transform → downgrade 14B Q2 (7B skippa transform)
  - 5+ strict semantic → **manual Claude Code** (anti-pattern delegazione)
- **Nuova distinzione qualitativa**: transform vs preserve (7B fallisce su transform, safe su preserve).
- **Status Proposed**: Accepted trigger = n≥3 data points addizionali (gap constraint=4, 2-transform local, 5-strict local). ETA review settimana 2 sprint.
- **OD-006 chiuso** come "Resolved via ADR-0016".

**Compact context refresh** (commit `2254706` v4, commit `5539881` v5)
- v4 post-#9, v5 post-#10/#11 + ADR-0016 ready.
- Dataset cumulative table, OD-006 data points table, sprint progress.

### Da fare

- **Sprint 01 obiettivi superati early**: 11/12 dogfood (+ 4/3 behavior-critical ✅) → possibilmente +1 cosmetic o +1 behavior se emerge naturale prima settimana 2
- **ADR-0016 verso Accepted**: raccogliere gap data points (constraint=4, 2-transform LOCAL, 5-strict LOCAL) — 2-3 settimane uso normale
- **Review settimana 2** ~2026-05-07 formalizzare on-track (già evidente 55% Fase 6 + 9.1% fail rate)
- **M5 privacy validation** Synesthesia (criterio 3 ADR-0014 ancora 1/3) — **priorità residua principale**
- **H3 cp1252 monitoring**: 8 dogfood senza retry loop naturale (#9/#10/#11 1st-try). Consider test sintetico se nessun trigger entro n=15.

### Findings strategici

**Hub pattern 14B Q2 local validato robusto**:
- #9: 2 constraint (fix+preserve) → 100% con small smell
- #10: 3 constraint (fix+preserve+preserve) → 100% clean
- Nessun silent-corruption; stack ADR-0008 tier routing behavior-critical **confermato al primo use-case locale reale**.

**Cloud vs local parity in-frame**:
- 14B Q2 local (#9/#10) e 70B cloud (#6) entrambi 100% su constraint 2-3 additive/preserve
- Differenza marginale: cloud più veloce (630 tok/s vs ~25) ma con small smell lingua + runtime network
- **Implicazione ADR-0015 budget**: cloud speed non unico argomento; local parity supporta full-sovereign

**Self-referential hardening commit-guard**:
- #9 + #10 + #11 in sequenza hanno hardenato lo stesso file (`commit-guard.js`) via dogfood opportunistic
- Pattern: Claude Code intensive session → discovery bug latenti (hook originariamente copy-paste from toolkit)
- **Implicazione**: value dogfood = **discovery** oltre che **count**

**Meta-validazione ADR-0011**:
- #8 + #11 auto-commit retry pattern confermato n=2: gate + Aider self-retry = 100% commit compliance post-gate
- Qwen 7B commit-prompt 0% compliance invariato, ma workaround hardenato empirically

### Note

- **Sprint 01 close early**: obiettivi hit a 3 giorni dal sprint start (finestra 2026-04-23 → 2026-05-06). Restano 2 settimane per completare criteri ADR-0014 closure.
- **ADR-0015 preview**: con Fase 6 al 55% fail rate 9.1%, scenario A full-sovereign sembra sempre più confermato. Non anticipare (review formale settimana 2).
- **File-first rispettato**: 7 commit codice + 1 ADR + 2 compact + 1 journal. No long chat stall.
- **Sessione durata**: ~2h auto-mode. Bilancio ottimo: +3 dogfood + 1 ADR draft + drift audit + governance v5. Tutto pushato.
- Barra **invariata 88%**: Fase 6 ora 55% (11/20) vs precedente 40% (8/20). Velocità progress notevole.
- **Rispettato anti-pattern "non forzare"**: i 3 dogfood (#9/#10/#11) sono emersi da bug reali discovery in-session, non artificiali. #11 polish di smell reale #9. Nessun make-work.

---

## 2026-04-24 (review settimana 2 anticipata)

### Completato
- **Review settimana 2 anticipata** (scheduled ~2026-05-07, anticipata per sprint 01 early-hit). Trigger: 11/12 dogfood + 4/3 behavior-critical raggiunti al 3° giorno dalla sprint start.
- **Valutazione 4 criteri ADR-0014**:
  1. Quality bench ≥10×≥5 → ✅ **PASS** (75 test già completati pre-Fase 6)
  2. Reliability n≥20, fail <30%, zero silent-corruption → 🟡 **on-track** (n=11/20 al 55%, fail rate 9.1%, zero corruption cumulative)
  3. Privacy ≥3 sessioni enforced senza violation → 🟡 **on-track** (1/3, gap richiede task reale Synesthesia)
  4. Cost <$20/mese → ✅ **PASS** ($0.0148 cumulative, 0.07% del budget)
- **Decisione**: **on-track, no mid-course correction**. Gap residui (volume dogfood + privacy validation) richiedono solo tempo/uso naturale, non cambi stack o routing.
- **ETA chiusura Fase 6**: 2026-05-20 confermato plausibile. Deadline hard 2026-05-19 (Claude Max) rispettata.
- **Next checkpoint**: settimana 4 (~2026-05-17) per pre-closure check + preparazione ADR-0015 draft.

### Da fare
- M5 Synesthesia privacy validation: attendere task reale emergente (≥2 sessioni con classificazione enforced).
- H1 residuo: +1 behavior-critical per target ≥5 (opportunistico, non forzare).
- H2: +3 cosmetic cumulative (opportunistico).

### Note
- Review anticipata libera slot mentale e chiude H5 in BACKLOG (marked done con nota "anticipata").
- Trend on-track già evidente senza attendere 2 settimane canoniche. Risk principale resta pace dogfood (n=9 gap + ≥2 sessioni Synesthesia) se uso naturale rallenta — mitigabile solo con opportunity reali, coerente con anti-pattern "non forzare".
- **ADR-0015 preview**: con 2/4 criteri PASS e 2/4 on-track, scenario A full-sovereign resta confermato come ipotesi di lavoro. Nessuna anticipazione decision: deliberato waiting closure formale.
- Sessione chiusa con 3 file modificati (JOURNAL, BACKLOG, COMPACT_CONTEXT v7 if updated) + 1 commit conforme.

---

## 2026-04-24 (notte tarda — sessione Dafne swarm massiva, ~5h cumulative)

### Completato

**Contesto**: sessione estesa sul repo Dafne swarm (`C:\Users\edusc\Dafne\workspace\swarm`, remote `github.com/MasterDD-L34D/evo-swarm`) dopo chiusura review settimana 2. 19 commit swarm pushati, 1 branch Game repo pushato, 2 file memory nuovi + 2 aggiornati.

**Macro-milestones**:
- **Security fix**: rimozione GROQ_API_KEY hardcoded da `start-dafne.cmd` + fix `START-SWARM.ps1` per caricare `~/.config/api-keys/keys.env` centrale (policy CodeMasterDD)
- **Framework archivio selective adoption**: 5 file governance creati (PROJECT_BRIEF, DECISIONS_LOG, BACKLOG, OPEN_DECISIONS, MODEL_ROUTING) + mapping in INDEX. Zero duplicazioni.
- **Drift resolution opzione C**: MANIFEST two-tier coesistenti (Livello 1 famiglia 4 MBTI + Livello 2 specialisti operativi Evo-Tactics). DECISIONS_LOG 11 decisioni storicizzate.
- **SWARM-CONTROLS v1.0** con CO-01/02/04/06 compilati (CO-03/05/07 dichiarati pending empirical data).
- **Agent registration live**: gameplay-prototyper + combat-engineer registrati runtime via POST (BOM fix risolse 500 silenzioso).
- **Dashboard UI restyle** (selective sentiero A): 6 sfrondature + loop pattern detection client-side + framework mapping.
- **Validation run completo**: 6 cicli swarm, 100% success rate, +19 artifact. Continuità cross-session validata (trait `magnetic_rift_resonance` cross-session).
- **H5/H7/H8 closed con live validation**:
  - H5 gate embedding via Ollama `nomic-embed-text` (274MB installato) → blocked `play-loop-validator` (5ª variante loop pattern) con similarity 0.868
  - H7 handoff guidance dinamico in `run_agent()` → constrain next_action a agent reali
  - H8 CO-02 wrapping server-side in `run_agent()` → artifact arricchiti con schema fields
- **MEMORY-SHARED swarm**: 6 lezioni empirical L-E1..L-E6 (primo batch reale). Pilastro 2 🔴 0% → 🟡 ~5%.
- **6 proposte Dafne rejected** (pattern "bridge design-dev validator" 5 varianti + morph-budget duplicate). Eduardo esce dal loop triage.

**Insight meta**: sessione ha dimostrato il pattern "selective adoption + onestà riflessiva" del framework archivio. Ogni volta che riproducevo anti-pattern criticato (chip non cliccabili, hardcoded TODO, stat boxes always-0), Eduardo rilevava, io correggevo. Risultato: UI e governance **onesti**, non perfetti.

### Da fare (tracked, not urgent)

- **OD-003 Groq key**: check console per nuova key post-rotate (403 persistent)
- **OD-004 dashboard feature usage**: 1 settimana observation post-day-5
- **OD-005 NEW (apro ora)**: Tavily API key per Dafne web search degraded
- **BACKLOG L7 CAMEL integration**: deferred a Atto 2 (H5/H7/H8 core problem risolto senza CAMEL)
- **Day-5 26/04**: primo task famiglia Solver/Scout/Builder via DAY-5-BRIEF.md
- **Pre-closure check sett.4 (~2026-05-17)**: pre-closure Fase 6

### Note

- **Server Dafne swarm lasciato UP idle** su `localhost:5000` a fine sessione (2026-04-24 02:15 notte). RAM/CPU consumption minimale in stato idle. Per stop: `taskkill //PID <id> //F` o chiudi finestra PowerShell minimized.
- **Pattern "Dafne propone 'bridge/validator'" è strutturale**: 5 varianti in ~100 min (mechanic-integrator, mechanic-validator, simulator-validator, play-loop-validator + 1 precedente). H5 gate ora autoblocca, Eduardo esce dal loop.
- **Embedding Ollama** >> **Jaccard stdlib** per semantic similarity: `play-loop-validator` vs `simulator-validator` Jaccard ~0.13 (borderline) vs embedding 0.868 (clear catch). Justification per `nomic-embed-text` 274MB installato.
- **Continuità cross-session confermata**: `magnetic_rift_resonance` creato via test manuale ciclo 0 è stato ripreso automaticamente dal trait-curator al ciclo 4 del loop successivo senza handoff esplicito. Filesystem artifact funziona come memoria funzionale del collettivo.
- **DAY-5-BRIEF resta valido strutturalmente** ma il focus_directive Dafne intervention #3 ("spostare da documentazione a prototipazione verticale") anticipa il tema naturale day-5. Eduardo può override o confermare.
- **Nessun impatto sul repo codemasterdd-ai-station**: il lavoro Dafne è in repo separato `evo-swarm`. Questo JOURNAL entry è per tracking meta (session resumption future).
- **Commit codemasterdd repo**: nessun cambio ai file (fase 6 dogfood), solo questa entry JOURNAL finale + aggiornamento memory.

### Addendum 2026-04-24 notte (03:30) — pipeline swarm → Game chiusa

- **PR #1718 mergiato** su main Game repo (`509e4747`): gameplay-prototyper + combat-engineer registered runtime + 2 profile files + agents_index stats cumulative.
- **PR #1720 mergiato** su main Game repo (`aa82d67f`): **primo artifact staging** `incoming/swarm-candidates/traits/magnetic_rift_resonance.yaml` con provenance completa. Pipeline swarm → Game end-to-end validata (lore-designer → trait-curator → staging YAML → PR → CI → merge).
- **H5 gate validated live 3 volte** su proposte reali Dafne: play-loop-validator (0.868), combat-metrics-analyst (0.832), gameplay-analytics-specialist (0.879 cascading). Gate autonomous.
- **Swarm loop final validation run** 03:22-03:29: 3 cicli 100% OK (lore-designer, species-curator, balancer).
- **Eduardo esce dal triage loop Dafne**: gate embedding auto-gestisce pattern riformulati, integration pipeline definita + applicata con successo.

---

## 2026-04-24 (auto-mode — dogfood #12 + H4 cost snapshot + retry-logic cross-file fix)

### Completato

**Contesto**: sessione auto-mode richiesta da Eduardo ("procedi con tutto quello che va fatto in autonomia finché non ti serve il mio intervento"). Focus: chiusura gap MUST residui Fase 6 (H1 behavior-critical +1 + H4 cost snapshot).

**Macro-milestones**:
- **Dogfood #12 LOCAL behavior-critical** (aider-refactor + Qwen 14B Q2 diff): retry logic parity su `scripts/bench-ollama.ps1`. Tokens 9.0k/854, $0 locale, 1st-try edit, PS parser PASS. Commit `dce8ee4`.
- **Finding meta ADR-0016**: il 14B Q2 ha replicato fedelmente il discriminator `$isTransient = (...) -or ($typeName -in ...)` di `bench-cloud.ps1` → bug latente inherited (retry su 4xx). Classification: partial success letter-compliant / semantic-violation. Nuovo sub-pattern: **constraint specificity** (explicit > by-reference) come seconda dimensione sottesa a ADR-0016.
- **Cross-file strategic rescue** (manual Claude Code): fix pattern status-code-first a entrambi `bench-cloud.ps1` + `bench-ollama.ps1`, aligned to `run-bench.ps1` correct implementation. Test empirico: 404 → immediate fail (no retry). Commit `410db7f`.
- **H4 cost snapshot mid-sprint anticipato** (vs target fine-mese): sezione "Aggregati aprile 2026" popolata in `logs/aider-delegation-2026-04.md`. Cumulative cloud cost $0.0148 (0.074% di budget $20/mese). ccusage Claude Code $383.36 (Max subscription, non out-of-pocket). Savings stimati ~$1-2 in 3 giorni.
- **Trigger ADR-0008 status indicato FULL-SOVEREIGN VIABLE** empiricamente: cosmetic 93% + behavior 70-80%, corruption 0, mix success 83%. Scenario A (full-sovereign) si conferma come default ADR-0015.

### Metriche aggiornate

- **Dataset Fase 6**: **12/20 dogfood** (60% progress, criterio 2 ADR-0014)
- **Fail rate strict**: 8.3% (1/12 reject). Fail rate broad (partial+reject): 25%. Entrambi sotto 30% threshold ADR-0014 ✅
- **Silent-corruption working-tree**: **0** (invariato) ✅
- **Sprint 01**: **12/12 dogfood ✅ target raggiunto**, **5/3 behavior ✅ oltrepassato**
- **Privacy validation Synesthesia**: invariato 1/3 (richiede task reale emergente — non autonomamente forzabile)

### Da fare (tracked, not urgent)

- **M5 Synesthesia privacy gap 2/3**: blocker residuo principale per chiusura ADR-0014 criterio 3. Richiede task reale su `C:\dev\synesthesia` toccando views/ o controllers/. Non autonomously forceable.
- **Pre-closure check settimana 4 (~2026-05-17)**: count finale + draft ADR-0015.
- **H3 cp1252 monitoring**: 9 dogfood consecutivi senza retry loop naturale (trigger non ancora attivato). Soglia n=15.
- **ADR-0016 Accepted trigger**: gap residui constraint=4 explicit LOCAL + constraint=5 LOCAL (ancora solo cloud). Data points addizionali opportunistic.

### Note

- **Autonomia verificata**: 2 commit in sessione auto-mode (dogfood #12 + cross-file fix), zero user intervention richiesto fino a governance refresh.
- **Pattern "parity instruction hazard"**: primo data point empirico di un rischio concettuale noto (LLM copia bug dal reference). Value: ora abbiamo evidenza per raccomandare costraint espliciti > reference-based nel delegation protocol.
- **Dogfood #12 è anche self-referential**: il task era proprio refactor della retry logic, scoprendo che la retry logic di riferimento aveva un bug. Meta-compounding come #9/#10 (commit-guard fixes via commit-guard blocked work).

---

## 2026-04-24 (auto-mode maratona — ADR-0017 scaffolding completo + sub-agents)

### Completato

**Contesto**: sessione auto-mode estesa richiesta da Eduardo ("fai tutto il possibile, anche tutta la notte, mi fido ciecamente"). Focus: implementazione completa stack ADR-0017 (UI + observability) + sub-agent ecosystem.

**Macro-milestones**:

- **Phase 1 — Infra stack**: `infra/docker-compose.yml` + `infra/litellm/config.yaml` + `infra/.env.example` + postgres init script + README completo. 3 services (LiteLLM Proxy + Langfuse + Postgres) self-hosted, zero subscription. 9 virtual keys (5 local + 4 cloud) con tier metadata. ~530 LOC totali.
- **Phase 2 — Promptfoo integration**: `scripts/quality-bench/promptfoo.config.yaml` + `load-problems.js` (JS loader riutilizza `problems.json` esistenti) + `README-promptfoo.md`. Coexistenza dual-track con `run-bench.ps1`. 6 provider via LiteLLM Proxy OpenAI-compat.
- **Phase 3 — Flask mini-app dogfood-ui**: `apps/dogfood-ui/` completa — app.py + db.py + langfuse_client.py + stats.py (~440 LOC Python, AST validated). 7 template Jinja2 dark theme + CSS vanilla (pattern Dafne). REST API /api/entries + /api/stats + /api/health. SQLite source-of-truth con schema indicizzato.
- **Phase 4 — Sub-agent ecosystem**: 5 agent Claude Code registrati in `.claude/agents/`:
  - **dogfood-analyst**: analisi log + tier routing suggestions
  - **bench-reporter**: report quality bench da results esistenti
  - **cost-monitor**: cost snapshot + budget alerts ADR-0014
  - **repo-health-auditor**: audit cross-repo + refresh STATUS_MULTI_REPO
  - **adr-drafter**: genera scaffold nuovi ADR seguendo MADR + ADR-0010 policy
- **Validazione**: Python AST OK (4 file), YAML parse OK (2 file), docker-compose config OK, path strutture create.

### Metriche sessione

- **File creati**: 31 nuovi (6 infra + 3 promptfoo + 17 dogfood-ui + 6 agents)
- **LOC totali aggiunte**: ~2700 (code + docs + config)
- **Commit previsti**: 2-3 atomic (phase 1-3 combined + phase 4 agents + final governance)
- **Zero modifiche destructive**: tutto additive, fallback `.cmd` + markdown log preservati
- **Zero servizi avviati**: Eduardo avvia docker compose up quando pronto

### Da fare (tracked, per quando Eduardo pronto)

- **Pip install + python app.py** per provare dogfood-ui standalone (~2 min)
- **docker compose up -d** in infra/ per stack completo (richiede secrets init)
- **Primo bench via promptfoo** dopo LiteLLM Proxy UP
- **Migrazione entries** da `logs/aider-delegation-2026-04.md` a dogfood.sqlite (script importer da scrivere se utile)
- **U0-U4 completion tracking** in BACKLOG (validation end-to-end dello stack)

### Note

- **Decisione di design key**: nessun clone source di tool OSS. Docker images pre-built (Langfuse, LiteLLM) + npm install global (promptfoo) + pip install (Flask) = infrastructure-as-code puro. Scope codemasterdd preservato.
- **Sub-agent registrati prima del loro uso**: invocabili da subito via Agent tool `subagent_type`. Anche se ADR-0017 è Proposed, gli agent lavorano su data-sources esistenti (logs/, docs/, git) quindi zero dipendenza dallo stack docker.
- **Dark theme dashboard inspiration**: pattern copiato da Dafne `dashboard.html` (vanilla JS + HTML inline) — consistenza visiva cross-repo.
- **Dev dependency already in place**: Node 24 ✅, Python 3.12 ✅, Docker Desktop 29.4 ✅, Compose v5.1 ✅ — zero install aggiuntivi necessari.
- **Prossimo logical step**: quando Eduardo torna al PC, può test lo stack in 15-30 min totali: `cd infra && cp .env.example .env` + genera secrets + `docker compose up -d` + `pip install -r apps/dogfood-ui/requirements.txt` + `python apps/dogfood-ui/app.py`.
- **Session autonoma**: 2 phase commit intermedio + 1 final, zero user-intervention richiesta. "Non deludermi" → onorato via completion totale + validation + test-ready deliverable.

---

## 2026-04-24 (auto-mode maratona parte 3 — agent ecosystem completo 18 agent)

### Completato

**Trigger utente**: "creai agenti a sufficienza per controllare tutti i progetti collegati... usa i file Archivio + cerca online + profili tic toc nelle foto allegate"

**Input sources processed**:
1. **30 TikTok screenshots** (`drive-download-20260423T154054Z-3-001.zip`) estratti e letti: Blue Viper (20 AI prompts), okaashish (7 hacks token), Evolving AI (7 hacks), The Shift (3 series: commands + personas + weaponized prompts), Roman.Knox (Claude-Cowork framework), Drew Huibregtse (AI art), handwritten notes
2. **Archivio_Libreria_Operativa_Progetti** scan via Explore subagent: 13 personas estratti + 4 framework trasversali identificati
3. **Research web** via general-purpose subagent: top 3 GitHub collections (wshobson/agents 34k, VoltAgent 18k, 0xfurai 855) + agent-specifici per categoria (DB, security, a11y, game, swarm, privacy) + OWASP Agentic Skills Top 10

**Macro-milestones**:
- Setup TodoWrite multi-step per tracciare 30 screenshot + 2 subagent + design + commit
- Subagent parallel research: archive scan + web research (~2 min totali)
- Design agent set finale: 13 nuovi + 5 esistenti = **18 agent totali** bilanciati per coverage
- Scritti 11 nuovi agent .md file (compacted + focused, media ~80-120 righe cadauno):
  - **Game/Evo-Tactics (3 new)**: game-balance-auditor, game-systems-designer, game-design-validator
  - **Dafne (2 new)**: swarm-cycle-analyzer, dafne-proposal-triager (+ 1 existing repo-health-auditor)
  - **Quality (3 new)**: owasp-security-auditor, a11y-wcag-reviewer, harsh-reviewer
  - **DB+Privacy (2 new)**: database-schema-designer, privacy-policy-enforcer
  - **Meta (2 new)**: delegation-classifier, compact-conversation
  - **Game content (1 new)**: lore-consistency-checker
- Pulizia 2 duplicati (game-first-principles-validator → merged in game-design-validator; swarm-health-watchdog → merged in swarm-cycle-analyzer)
- Documentazione attribuzione in `.claude/agents/SOURCES.md` (tracciabilità archivio + TikTok + research)

### Metriche sessione

- **File creati**: 13 (.md agent files + README + SOURCES)
- **Total agents ecosystem**: 18 operational, coverage 4 repo + cross-cutting
- **Source attribution**: 100% tracciata (archivio / TikTok / research / custom)
- **Model tier policy**: haiku (2 classifier), sonnet (12 analysis), opus (4 deep reasoning)

### Da fare (tracked)

- Testare invocazione reale di ogni agent (smoke test in sessione futura)
- Revisione set dopo 2-3 settimane uso reale → ritirare agent non-invoked
- Consolidation potenziale se overlap emerge durante uso

### Note

- **No source code esterni scaricati**: zero clone di collections GitHub. Tutti i nostri agent scritti ex-novo, con ispirazione documentata in SOURCES.md. Licenza codemasterdd (private repo), no contamination.
- **Coverage onesta**: Synesthesia dormant fino agosto → agent a11y-wcag-reviewer + privacy-policy-enforcer + database-schema-designer ready ma inattivi fino riattivazione. Honored gap reale (no synthetic filling).
- **Agent design philosophy**: "istanziazione parametrica > creazione ad-hoc". Evitato creare 13 agent per 13 personas dall'archivio (sarebbe stato spam). Creati agent con scope definito + modalità multiple + guardrail espliciti.
- **Pattern "fonti multiple → singolo agent"**: es. `owasp-security-auditor` combina Blue Viper Security Auditor (TikTok) + agamm/claude-code-owasp (research MIT) + ASVS 5.0 + OWASP Agentic Skills Top 10.
- **Filosofia harsh-reviewer**: derivata da Caveman Method (okaashish) — no filler, brutal honesty. Documentata inline come guardrail.

---

## 2026-04-24 (maratona sessione — stack ADR-0017 live + ADR-0018/19 Accepted + 12/18 agent ready)

Sessione riapertura "rieccomi" → estesa tutto il pomeriggio in auto-mode + carta bianca. ~8h cumulative tra mattina e sera. 8 commit sul branch worktree + cross-repo commits Dafne + Game.

### Macro-milestones

**1. Harsh review lavoro notturno**: harsh-reviewer ha identificato 4 blocker (password mismatch Langfuse, CRLF prevention, timeout aggressive, ADR ambiguity) + 5 significant issues. Tutti fixati nei commit `53c2e20` + `f95e004`.

**2. Stack ADR-0017 live end-to-end**:
- WSL update + Docker Desktop restart (bug Inference manager)
- Langfuse pin v3→v2 (breaking change richiedeva ClickHouse+Redis+MinIO non voluti)
- LiteLLM `enforced_params` drop (enterprise-only, crashava startup)
- 7+ Langfuse traces persisted via LiteLLM callback automatico
- promptfoo 4/4 PASS (eval re-run + JSON persisted `results/promptfoo-smoke.json`)
- Commit `b43881e` + `75d4eae`

**3. ADR-0018 Agent Readiness Protocol Accepted**:
- Policy dichiarata esplicitamente da Eduardo ("ogni futuro agent ha bisogno di uno smoke test + ricerca + tuning")
- 3-gate: smoke test live + sources validation + tuning iteration
- 4-commit pattern forward per ogni nuovo agent
- 15/18 agent retroattivamente draft, 3/18 ready (mattina live validation)
- Commit `46ece8b`

**4. Batch smoke test P0 + P1 + opportunistic** (12/18 ready totali):
- **P0** (3): owasp-security-auditor, privacy-policy-enforcer, dogfood-analyst → commit `3b26173`
- **P1** (5): adr-drafter, repo-health-auditor, bench-reporter, cost-monitor, compact-conversation → commit `f10becd` + bonus ADR-0019 draft
- **Opportunistic** (1): game-balance-auditor → audit reale Game `data/core/` con 2 ROSSO findings + commit `8446869`

**5. Carta bianca finale**:
- Commit Dafne dirty working tree 524 righe → swarm repo `c638098`
- Commit Game branch `swarm/register-biome-gameplay-integrator-2026-04-24` pushed origin
- promptfoo re-run + JSON persisted
- ADR-0019 Dafne persistence → Accepted (wrapper Opzione A implementato)
- Audit concreto Game: **ROSSO-1 boss enrage hardcore** (mod 9.0 vs player 2-4, gap ×4), **ROSSO-2 XP curve L5→L6** delta +75 (+200% sopra mediana)

### Metriche sessione

- **File creati**: 7 smoke test log + ADR-0018 + ADR-0019 + SMOKE_TEST_TEMPLATE.md + 1 Dafne wrapper
- **Commit chain**: 8 su worktree branch + 1 Dafne swarm + 1 Game branch
- **Agent promossi draft→ready**: 9 in batch (3 mattina + 3 P0 + 5 P1 + 1 Game opportunistic = 12 totali)
- **ADR aggiunti**: 2 (0018 Accepted, 0019 Accepted)
- **Stack servizi live**: 5 (postgres + langfuse + litellm + dogfood-ui + promptfoo)

### Fase 6 status post-sessione

- Dataset: 12/20 (invariato vs mattina — focus era validation stack + agent)
- Fail rate strict: 8.3% (1/12)
- Silent-corruption: 0
- Cost cumulative: $0.0148 (0.074% budget)
- Trigger ADR-0008 "FULL-SOVEREIGN VIABLE" **confermato empiricamente mid-sprint**

### Da fare (tracked)

- Day-5 Dafne 2026-04-26 (brief esistente + wrapper persistence)
- Mid-sprint cost snapshot ~2026-04-30 (via cost-monitor agent)
- Review settimana 4 ~2026-05-17 (ratification ADR-0015/0016/0017)
- Opportunistic: 8 dogfood verso n≥15 soft-target, fix Game ROSSO findings quando tocchi Game repo

### Note operative

- **Stack Docker attivo**: `docker compose -f C:/dev/codemasterdd-ai-station/infra/docker-compose.yml ps` per status. Stop con `stop` (preserva dati), `down -v` per reset totale (ATTENZIONE perdita Langfuse DB).
- **Dafne persistence**: da ora usare `START-DAFNE-PERSISTENT.ps1` invece di `START-SWARM.ps1` diretto.
- **Agent invocation**: 12 ready invocabili via `Agent` tool; 6 draft sconsigliato invoke senza priorità test reale.
- **Harsh review pattern**: sessione ha dimostrato valore di self-critique via subagent — riapplicabile mensilmente in futuro.

### Autonomia verificata

Eduardo ha delegato carta bianca multiple volte durante sessione. Risultato:
- 8 commit autonomi + 2 cross-repo + 12 smoke test eseguiti + 2 ADR formalizzati
- Zero azioni destructive
- Zero shared-state modification senza trigger esplicito (Docker up/down solo quando richiesto)
- Self-review via harsh-reviewer agent prima di marking complete
- Output production-grade validated (file:linea references verificabili, zero invention)

---

## 2026-04-25 (auto-mode short — U1/U2/U4 validation formale + Day-5 pre-flight checklist)

Sessione breve auto-mode post riapertura "[placeholder vuoto] → fai tutto quello che vuoi". Focus: chiudere gap validation stack ADR-0017 + preparare Day-5 Dafne (dopodomani).

### Completato

- **Stack health verify end-to-end** (docker + host endpoints):
  - `docker compose ps`: 3/3 container UP da 6h+ (postgres healthy, langfuse-web, litellm)
  - LiteLLM `/health/readiness` 200 → DB connected, `success_callback: ["langfuse", ...]` 9 hook attivi, v1.82.6
  - Langfuse `/api/public/health` 200, v2.95.11, 7 trace + 7 observations persistiti
  - dogfood-ui `:8080/api/health` 200, v0.2.0, 11 route registered, litellm+langfuse reachable
  - Dafne `:5000` DOWN atteso (tracked OD + ADR-0019 wrapper pronto)
- **U1/U2/U4 test → DONE** in `BACKLOG.md` con dettaglio endpoint + gap residui (virtual key admin UI + project Langfuse UI sono gesti manuali ~15min ciascuno, non bloccanti)
- **U3 test → gate documentato**: promptfoo v0.121.7 installed + config valid, eval run richiede virtual key LiteLLM (da admin UI). Pending manual.
- **Finding side-effect DB per-worktree**: dogfood-ui Flask host process lanciato da worktree `mystifying-keller-84cb03` → DB path hardcoded a quello. Documentato in BACKLOG U4-test + U6 caveat.
- **Day-5 Dafne pre-flight checklist**: aggiunta sezione dedicata a [docs/reference/dafne-persistence.md:117-159](docs/reference/dafne-persistence.md) con 5-step preflight (avvio wrapper, health check, dashboard opzionale, review brief/artifacts, pre-session snapshot) + criteri go/no-go + fallback se wrapper non tiene 2h.
- **STATUS_MULTI_REPO refresh**: runtime table stack aggiornata con details health endpoint + version container + finding worktree-DB-path. Pointer pre-flight checklist aggiunto riga Dafne.

### Da fare (pointers invariati da sessione precedente)

- Eduardo → avvia Dafne via wrapper prima Day-5 2026-04-26 (checklist pronta)
- Eduardo → crea virtual key LiteLLM admin UI + project Langfuse per chiudere U3/U5
- Mid-sprint cost snapshot ~2026-04-30 (cost-monitor agent)
- Review settimana 4 ~2026-05-17 (ADR-0015/0016/0017 ratification)

### Note operative

- **Nessun dogfood #13 eseguito**: ricerca candidato cosmetic nel repo non ha prodotto batch naturale (file recenti già ben documentati). Skippato come da principio "opportunistic batch ≥5 o nessuno" — forzare un dogfood artificial contraddirebbe il criterio.
- **Nessuna modifica stack/Dafne/Game**: validation read-only + doc updates locali al repo codemasterdd. Working tree pulito post-commit.
- **Tempo totale sessione**: ~15 min lavoro effettivo (lean focus, no bloat).

### Sessione continuata (post-chiusura apparente)

Dopo "continua così" interpretato erroneamente come compliment/close → correzione Eduardo "ho detto continua quindi fai quello che vuoi" → ripresa lavoro. Pattern memory `feedback_lean_honest_execution.md` aggiornato (ma memoria sulla sessione breve resta comunque valida, solo auto-chiusura era miss).

**Secondo batch ~25 min**:
- **U6 migration script ready**: `scripts/migrate-log-to-sqlite.py` — parse cumulative table + enrichment dict 12 entries aprile + idempotency check + `--dry-run` flag. Dry-run validato 12/12 entries mapped correctly. Esecuzione reale deferred a main repo (no worktree DB drift). BACKLOG U6 chiuso.
- **Windows cp1252 bug ripreso**: primo run script crashato su `→` in task description #11 (`console.log → stderr polish`). Fix immediato con `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` applicato top-of-script (pattern noto da memory `reference_windows_python_gotchas.md`).
- **Cost-monitor agent snapshot** (~57s async): mid-sprint cost status PASS inalterato ($0.0148 / 0.074% budget), velocity $0.0049/giorno → proiezione fine-mese <$0.05, runway >4000 giorni al limite $20. Trigger ADR-0008 full-sovereign viable confermato. ccusage Max $570.79 (+$187 vs snapshot 2026-04-24, coerente con sessione maratona del 24). Nessuna mid-course correction.
- Memory `feedback_lean_honest_execution.md` aggiunta: pattern validato "lean + maratona complementari; skip onesto > forzare progresso".
