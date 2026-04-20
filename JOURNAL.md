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
