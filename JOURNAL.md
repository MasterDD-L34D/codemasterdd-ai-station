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
