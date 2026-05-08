# MODEL_ROUTING

> Compilato dal template `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/MODEL_ROUTING.md` con stack reale codemasterdd-ai-station.
>
> Source-of-truth per routing strategico. Per istruzioni operative in-session vedi `CLAUDE.md` "Priorità modelli AI". Questo file è il **perché** strategico, CLAUDE.md è il **come** operativo.

## Scopo

Definire quale strumento / modello / accesso usare per ogni fase del progetto.

Evita:
- usare sempre lo stesso strumento per tutto
- accumulare modelli senza ruoli chiari
- mandare codice sensibile in cloud
- perdere tempo/$ su task delegabili più veloci/economici

## Regola madre

**Fonte complessa → Comprensione → Compressione → Decisione → Esecuzione → Compact → Archivio**

Applicata in concreto:
- **Comprensione**: Claude Code Opus 4.7 (fino 19/05) legge repo + docs + ADR
- **Compressione**: Claude Code stesso (multi-file synthesis) o Gemini 2.5 Flash (quick summary)
- **Decisione**: Claude Code (ADR draft) + utente (approvazione esplicita)
- **Esecuzione coding**: Aider + modello tier-appropriate (vedi matrice)
- **Compact**: Claude Code (/COMPACT via PROMPT_LIBRARY)
- **Archivio**: Claude Code scrive in docs/ / logs/ / memory

---

## Profilo progetto

- **Nome progetto**: CodeMasterDD AI Station
- **Tipo progetto**: infrastructure-as-code + registry decisionale
- **Contesto principale**: repo infrastructure + documentazione (ADR/patterns) + log operativi
- **Vincoli privacy**: repo personale OK cloud; progetti dipendenti hanno policy per-repo separata
- **Vincoli costo**: Claude Max fino 19/05 ($0 marginale); post-Max target <$20/mese
- **Vincoli hardware**: RTX 5060 8GB VRAM (full-GPU solo 7B) + 64GB RAM + Arrow Lake CPU
- **Vincoli velocità**: daily-driver 8-10h/giorno, iterazione rapida essenziale
- **Priorità principale**: **privacy + costo** (≥ qualità) in stato sovereign. Durante Max: qualità+velocità primarie.

---

## Stack disponibile

### Strumenti disponibili
- [x] **Claude Code 2.1.116** (Opus 4.7, OAuth Max fino 19/05 → poi API key o dismissione)
- [x] **Aider 0.86.2** (6 wrapper in `~/.local/bin/`)
- [x] **Ollama 0.21.0** (5 modelli attivi + 3 reference-only)
- [x] **API esterne**: Groq + Cerebras (free) + Gemini + OpenAI (paid)
- [x] **OpenCode v1.14.41** (npm global, installato 2026-05-08; tier multi-step agentic con tool calls; ADR-0022 Accepted 2026-05-09)
- [ ] NotebookLM → usato saltuariamente da browser per corpus analysis, non integrato repo
- [ ] ChatGPT → saltuario, non integrato

### Accessi disponibili
- [x] Locale puro (Ollama + Claude Code senza cloud)
- [x] Cloud integrato (Claude Code via Max OAuth)
- [x] API provider esterni (4 keys in `~/.config/api-keys/keys.env`)
- [x] Repo aperto in Claude Code + Aider
- [ ] Fonti documentali caricate (es. NotebookLM): **no**, docs vivono nel repo

---

## Routing per fase

| Fase | Obiettivo | Strumento | Accesso | Modello | Perché | Output atteso | Quando passare oltre |
|---|---|---|---|---|---|---|---|
| Comprensione | leggere repo + docs | Claude Code | cloud Max | Opus 4.7 | 1M context, read multi-file strategico | mental model + citation file:line | Opus satura / task execution |
| Sintesi | compattare | Claude Code | cloud Max | Opus 4.7 | synthesis cross-source | COMPACT_CONTEXT update | — (compact end-of-session) |
| Planning | ADR draft / sprint plan | Claude Code | cloud Max | Opus 4.7 | reasoning strategico + evaluation options | ADR MADR / SPRINT_NN.md | approvazione utente |
| Repo map | structure analysis | Claude Code | cloud Max | Opus 4.7 | Glob/Grep multi-pattern | reference index / repo overview | — (output stabile) |
| Coding cosmetic | JSDoc, rename, lint | Aider + wrapper | hybrid | Qwen 7B local OR Cerebras 8B cloud | fast + faithful | diff additive pulito | commit |
| Coding behavior | refactor, bug fix | Aider + wrapper | hybrid | Qwen 14B Q2 local OR Groq 70B cloud | safe-fail diff + capability | diff controlled | review manuale + commit |
| Coding escalation | 14B safe-fails | Aider + wrapper | hybrid | qwen3:30b MoE local OR Groq 70B cloud | higher capability locale OR cloud | retry success | commit |
| Capability-max | debug strategico, multi-file refactor | Claude Code | cloud Max | Opus 4.7 | frontier quality | resolution | — (non delegabile) |
| Review | QA edit recente | Claude Code | cloud Max | Opus 4.7 | `git diff` audit + semantics | approval or remediation | commit |
| Compact | chiusura sessione | Claude Code | cloud Max | Opus 4.7 | context engineering | COMPACT + JOURNAL + memory | end |
| Archivio | persist memory | Claude Code | local fs | — | file write | memory/docs updated | end |

**Post-Max (2026-05-20+)**: colonna "Capability-max" + "Planning strategico" → passa a **Groq 70B** (free) o **OpenAI gpt-4o** (paid overflow). Claude Code stesso funziona via API key pay-per-use per task critici, ma routing shift verso Aider+cloud-free per daily work.

---

## Routing consigliato per scenario

### Se ho molte fonti eterogenee
- **Strumento preferito**: NotebookLM browser (capacità corpus analysis)
- **Modello / accesso**: Gemini Pro via NotebookLM
- **Motivo**: Claude Code non è ottimo su corpus massivo scattered
- **Output che voglio ottenere**: synthesis → bring back a repo come `docs/research/NNNN.md`

### Se devo capire e toccare il repo
- **Strumento preferito**: Claude Code nativa
- **Modello**: Opus 4.7 (fino 19/05); post-Max Opus via API o Sonnet 4.6 via API se costo eccessivo
- **Motivo**: integrazione nativa filesystem + Glob/Grep/Edit/Read
- **Output**: file scritti nel repo (file-first regola)

### Se devo scrivere documenti, backlog, ADR
- **Strumento preferito**: Claude Code Opus (fino 19/05)
- **Post-Max**: Claude Code API pay-per-use (ADR strategico) OR Groq 70B via `aider-groq` (ADR operativo semplice)
- **Motivo**: reasoning strategico + consistency di stile

### Se devo lavorare in locale per privacy o costo
- **Strumento preferito**: Aider + Ollama
- **Modello locale primario**: `qwen2.5-coder:7b` (cosmetic) + `qwen2.5-coder:14b-q2_K` (behavior)
- **Limiti hardware**: 8GB VRAM → 7B full-GPU, 14B spill ~27%, 30B MoE spill ~40%
- **Quando passare al cloud**: emerge task oltre capability 14B locale (safe-fail dopo 2 retry)

### Se devo usare il cloud
- **Strumento preferito**: Aider + wrapper (`aider-groq`, `aider-cerebras`, `aider-gemini`, `aider-openai`)
- **Modello cloud primario**: `groq/llama-3.3-70b-versatile` (free, 630 tok/s)
- **Perché proprio lui**: free tier 6000 tok/min + LPU speed + capability 70B dense
- **OpenCode + cloud free NON viable** (ADR-0022): TPM 6-12k Groq + context 8k Cerebras 8B << OpenCode default request ~50k token. OpenCode resta sovereign-only (Ollama 30B MoE).
- **Cosa NON mandare al cloud**:
  - Codice repo cliente (sempre)
  - Synesthesia `controllers/`/`routes/`/`middlewares/` (auth sensitive)
  - Segreti / env vars / API keys / token
  - Output che contenga i sopra

### Se devo fare task multi-step agentic con tool calls
- **Strumento preferito**: OpenCode (NOT Aider, scope diverso)
- **Modello sovereign default**: `ollama/qwen3-coder:30b` MoE A3B (tier 1 OpenCode, ADR-0022 Accepted 2026-05-09)
- **Tool calls supportati**: Read, Edit, Bash, ListFiles, Glob, Grep, MCP servers integration
- **Use case esempio**: refactor multi-file con orchestration di Read+Edit coordinati, GitHub agent, ACP server, esplorazione interattiva TUI mode
- **Cosa NON usare con OpenCode**:
  - Qwen 2.5 Coder family (7B/14B/32B): tool call raw JSON non eseguito
  - Cloud free tier (rate-limited TPM o context-limited)
  - Qualsiasi task adatto a single-file edit semplice (Aider e' superiore: faithful diff, latency 7B 5s vs OpenCode 30B 45s)

---

## Policy locale / cloud

### Locale prima?
- [x] Sì
- **Motivo**: filosofia sovereign (ADR-0001) + privacy-by-default + zero rate-limit dependency

### Quando il locale basta
- Cosmetic task (JSDoc, docstring, rename, lint-fix, typo batch)
- Behavior-critical task singolo file, logica chiara, constraint respecting
- Bench benchmark e framework iterativi
- Sperimentazione / prototipo
- Task con codice sensibile (sovereign guard rail)

### Quando il cloud è giustificato
- Speed-critical (Groq 20× più veloce di locale 30B MoE su stesso task)
- Multi-file refactor con >3 file target (14B Q2 safe-fails frequenti)
- Capability reasoning oltre Qwen Coder specialist (es. debug architetturale)
- Quality validation (seconda opinion su output locale dubbio)
- Task volumetrici (batch large quando locale impiegherebbe >10min total)

### Materiali che non devono uscire in cloud
- API keys, .env, credenziali
- Codice cliente / progetti con NDA
- Synesthesia backend auth (`controllers/`, `routes/`, `middlewares/`)
- Log che contengano path utente sensibili
- Dump database o dati personali

---

## Modelli attivi del progetto

| Modello | Runtime / accesso | Ruolo | Quando usarlo | Quando NON usarlo |
|---------|-------------------|-------|---------------|-------------------|
| `qwen2.5-coder:7b` | Ollama locale | tier 1 cosmetic | JSDoc, docstring, rename, batch≥5, working tree clean | behavior-critical (silent-corruption whole ADR-0008) |
| `qwen2.5-coder:14b-q2_K` | Ollama locale | tier 2 behavior default | refactor, bug fix, logic change single-file | task semplici <10 righe (overhead), multi-file >3 |
| `qwen3-coder:30b` (MoE) | Ollama locale | tier 2 escalation Aider + tier 1 default OpenCode | Aider: quando 14B Q2 safe-fails. OpenCode: default agentic single-shot (ADR-0022 Accepted, 3/3 PASS validati) | single-file semplice via Aider (overhead); task >70B capability needed; cloud free OpenCode (NON viable per OpenCode default context) |
| `deepseek-r1:8b` | Ollama locale | tier reasoning | chain-of-thought esplicito, debug logico, math/proof | coding standard (Qwen domina); batch/iterazione (thinking verbose) |
| `gemma4:latest` | Ollama locale | tier multimodal | OCR screenshot, audio dictation, vision analysis | coding (non coder-specialist); task text-only |
| `groq/llama-3.3-70b-versatile` | Cloud free (6k tok/min) | tier 3 behavior cloud | Online, privacy OK, capability 70B needed | repo sensitive, quota limit, offline |
| `cerebras/llama3.1-8b` | Cloud free | tier 3 cosmetic cloud fast | Online, cosmetic batch veloce | behavior complesso (8B capability limit possibile) |
| `gemini/gemini-2.5-flash` | Cloud 60 req/min | tier 3 quick query | fast explain / translate / summarize | coding edit (richiede `thinkingBudget=0` esplicito) |
| `openai/gpt-4o-mini` | Cloud paid | tier 4 capability-max | task estremi free-tier non copre | default daily (paid, ccusage monitor) |
| Opus 4.7 (via Claude Code/Max) | Cloud Max OAuth | tier 0 strategic | comprensione, planning, ADR, multi-file, debug arch | operazioni meccaniche (spreco token) — fino 19/05 |

**Regola**: meglio **pochi modelli con ruoli chiari** che molti modelli sovrapposti. Modelli deprecati sono in `docs/adr/` o marked reference-only — **non usare**.

---

## Scelte operative minime

### Modello locale principale
- **Nome**: `qwen2.5-coder:14b-q2_K`
- **Ruolo**: behavior-critical default (tier 2)
- **Perché lui**: sweet spot speed (25.4 tok/s) + faithfulness constraint-respect + safe-fail diff format

### Modello cloud principale
- **Nome**: `groq/llama-3.3-70b-versatile`
- **Ruolo**: online tier 3 behavior + fallback qualità
- **Perché lui**: free tier + LPU speed 630 tok/s + capability 70B dense + quality parity confermata (quality bench 2026-04-23)

### Modello fallback
- **Nome**: `openai/gpt-4o-mini`
- **Ruolo**: capability-max ultimo resort
- **Quando entra in gioco**: task quality-critical dove Groq 70B + Qwen 30B MoE safe-fail entrambi. Paid, ccusage monitor.

---

## Integrazione con la libreria

### Prompt ponte da usare tra strumenti
- **Da NotebookLM a Claude Code**: export synthesis → `docs/research/NNNN.md` + Claude Code carica file
- **Da ChatGPT a Claude Code**: screenshot/transcript → repo (via `Archivio_.../03_REFERENCE/`) + Claude Code consulta
- **Da Aider ad archivio**: post-edit `git diff` + entry `logs/aider-delegation-YYYY-MM.md` manuale (Claude Code hub)

### File da aggiornare dopo ogni passaggio importante
- [x] `COMPACT_CONTEXT.md` — snapshot stato corrente
- [x] `DECISIONS_LOG.md` — se decisioni granulari aggiunte (strategiche → ADR separato)
- [x] `BACKLOG.md` — priorità rifresh / task done / nuovi bloccanti
- [x] `REFERENCE_INDEX.md` — nuovi docs/reference aggiunti
- [x] `JOURNAL.md` — entry sessione significativa
- [x] `logs/aider-delegation-YYYY-MM.md` — ogni delegazione Aider
- [x] Memory `~/.claude/projects/.../memory/` — stato persistente cross-session

---

## Regole anti-caos

1. Non fare la stessa cosa in tre strumenti (es. non usare ChatGPT + Claude Code + NotebookLM sullo stesso corpus — scegli uno)
2. Non mandare fonti grezze nel coding tool se prima vanno capite (fase Comprensione separata)
3. Non accumulare modelli "per sicurezza" (ADR-0005 YAGNI — aggiungi solo quando trigger)
4. Non tenere implicito il routing: questo file è la verità, se non è scritto qui **non è una regola**
5. Se un passaggio aumenta caos invece di ridurlo, fermati e consolida (es. se tier 3 cloud fail rate >30%, torna a tier 2 locale prima di debug wrapper)

---

## Decisione finale attuale

- **Workflow primario del progetto**: Claude Code Opus (fino 19/05) per comprensione/planning/multi-file; Aider + Qwen local per coding 1-file routine; Aider + Groq cloud per coding 1-file speed-critical
- **Strumento principale di comprensione**: Claude Code nativo (Glob/Grep/Read)
- **Strumento principale di esecuzione**: Aider con wrapper tier-appropriate (classificazione CLAUDE.md)
- **Strumento principale di archivio / orchestrazione**: Claude Code scrive docs/, logs/, memory; ADR come decision persistence
- **Prossimo test da fare sul routing**: dogfood behavior-critical #3+ per bilanciare dataset cloud (1 success + 1 REJECT al 23/04 sera) + validare OD-006 constraint-count routing con n≥3 task di constraint-count variabile

---

## Finding empirico 2026-04-23 — Constraint count come seconda dimensione routing

Dogfood Fase 6 n=8 rivela **pattern nuovo non previsto nella matrice originale**: la success-rate delega degrada con il numero di constraint espliciti, indipendentemente dalla classe (cosmetic/behavior).

| Constraint count | Qwen 7B local whole | Qwen 14B Q2 local diff | Groq 70B cloud diff | Nota |
|:----------------:|:-------------------:|:----------------------:|:-------------------:|------|
| 1 (add-only / fix puntuale) | 100% (n=3) | n/a | 100% (n=2) | Safe delega, qualsiasi tier |
| 2-3 (fix + transform / logic change) | 50% (n=1) | ~80% (ADR-0007) | ~85% (n=1 small smell) | Preferire diff + review manual |
| 5+ (multi-constraint strict + branch-semantic) | n/a | n/a | **20% (n=1 REJECT)** | **Rewrite manuale Claude Code** raccomandato |

**Implicazione routing formalizzata** (OD-006 → ADR-0016 Proposed 2026-04-24):
- La matrice `CLAUDE.md "Priorità modelli AI"` si basa su CLASSE task. **ADR-0016** aggiunge **constraint-count** come seconda dimensione. Non sostituisce, estende.
- Regola operativa: **quando classifico task pre-delega, conta anche constraint espliciti nel prompt**. Se ≥5 → skip delega, rewrite direct.
- **Nuova distinzione qualitativa**: transform vs preserve constraint (7B skippa transform; 14B Q2 safe su preserve).
- Vedi `docs/adr/0016-constraint-count-routing-dimension.md` per matrice 2D completa + rationale empirico (n=11 cumulative, n=6 cross-tier).

**Esempi dogfood reference**:
- #6 (3 constraint: signature + return + resilience) → Groq 70B success con small smell
- #7 (5 constraint: signature + return-branch-divergent + max=3 + discriminator + informative) → Groq 70B **REJECT** con blocking bug
- #8 (2 constraint: fix + condense) → Qwen 7B applicato solo fix (1/2 compliance)

**Cause ipotetica**: LLM ≤70B hanno capacity per preservare ~2-3 constraint simultaneamente. Oltre, iniziano a "dimenticare" i meno prominenti nel prompt — tipicamente quelli trasformativi (vs fix puntuali più concreti).

## Evoluzione attesa post Fase 6 (ADR-0015)

Scenario **A full-sovereign** (preferito):
- Claude Code: dismesso daily, retained via API key solo per strategic raro (budget <$10/mese)
- Tier 0 strategic → Groq 70B via `aider-groq` per ADR/planning leggero
- Tier 1-4 invariato (free + locale)

Scenario **B ibrido Claude Pro**:
- Claude Pro $20/mese attivato → Claude Code OAuth continua daily-driver
- Qwen locale come privacy-first per repo sensibili
- Cloud free come speed backup

Decisione finale in ADR-0015 a ~2026-05-20.
