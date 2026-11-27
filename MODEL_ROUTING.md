# MODEL_ROUTING

> **Consolidated 2026-05-29 (ADR-0036):** the cross-executor routing authority is now
> `ORCHESTRATION.md`. This file is the LOCAL-FLEET detail (llmfit / Ollama 2-machine).
> For "which executor for task X" (local vs cloud vs Jules vs inline) see ORCHESTRATION.md.

> Source-of-truth per routing strategico (il **perche'**). Per istruzioni operative
> in-session vedi `CLAUDE.md` "Priorita' modelli AI" (il **come**). Compilato dal
> template `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/MODEL_ROUTING.md`.

## Stato al 27/11/2026 (leggere prima del resto)

- **Ruoli dei modelli locali**: fonte unica `C:\dev\codemasterdd-workspace\test-llm\INDICE-VALUTAZIONE-LLM.md`
  + riga Ruoli (sezione LLM locali) di `C:\dev\codemasterdd-workspace\user-config\REGOLE-COMUNI.md` (metodo: `METODO-SELEZIONE-LLM-20261107-v4.md`).
  Questo file non copia ruoli ne' numeri: se diverge, valgono quelle fonti. Il ruolo "codice" ha un modello di riferimento solo nella riga Ruoli.
  Un ruolo senza riferimento o promozione -> nessun default locale; uso di prova libero e dichiarato, non default (REGOLE-COMUNI: provare e usare un modello e' libero).
- **Modelli installati**: solo `ollama list` eseguito sull'host. Un nome scritto qui non prova che esista.
- **Rimossi il 27/11/2026 dal Lenovo**: `gpt-oss:120b`, `qwen2.5:32b`, `qwen2.5-coder:32b`, `qwen2.5-coder:14b` (q2_K e q3_K_M),
  `qwen2.5-coder:7b`, `deepseek-r1:14b`, `deepseek-r1:8b`, `phi4:14b`, `mistral:latest`. Il Ryzen non ha nessun qwen2.5
  (`qwen2.5-coder:14b` e `:7b` rimossi il 13/11, METODO v4 voce del 13 nov) ne' `deepseek-coder-v2:16b` (`ollama list` del 27/11). Le rotte su questi modelli, sotto, sono marcate SUPERATO e restano solo come storia.
- **Wrapper sospesi**: `aider-cosmetic` e `aider-refactor` (Lenovo `~/.local/bin`, sorgente `scripts/wrappers/`) chiamavano
  `qwen2.5-coder:7b` e `qwen2.5-coder:14b-instruct-q2_K`, non piu' installati. La sorgente ora e' uno stub che stampa un avviso
  ed esce 1; la copia sul Lenovo resta la vecchia finche' non si reinstalla (`install-wrappers.ps1 -Force`). Nessun sostituto locale:
  nessun ruolo promosso per cosmetic/refactor.
- **Claude**: abbonamento Max attivo (primario). ADR-0030 (Pro) e ADR-0023 (API on-demand) = piano di riserva se Max cessa,
  non stato attuale.

## Fleet 2-machine routing (llmfit standard, 2026-05-22)

> **AUTHORITY**: `C:\dev\tools\llmfit\LOCAL-LLM-STANDARD.md` (+ vault claude-global
> CLAUDE.md sezione "LLM locali"). Liste HW-fit: Ryzen `C:\dev\tools\llmfit\ryzen-llm-fit.{json,md}`,
> Lenovo `lenovo-llm-fit.md` (raw su .10 `C:\Users\edusc\llmfit-lenovo-*.json`).
> Refresh mensile auto (Ryzen, Windows Task Scheduler `llmfit-ryzen-refresh`).

Lo stack locale NON e' piu' single-machine. Fleet = 2 macchine a profilo OPPOSTO:

| Macchina | host | VRAM / RAM | Profilo | Ruolo locale |
|----------|------|------------|---------|--------------|
| **Ryzen** | `.11` DESKTOP-T77TMKT | RTX 4070S **12GB** / 31GB | VRAM-rich | dense fit-in-VRAM, veloce |
| **Lenovo** | `.10` CodeMasterDD (edusc) | RTX 5060 8GB / **64GB** | RAM-rich | MoE/grandi (expert-offload), host Ollama primario |

**Machine-routing** (profilo HW, ortogonale ai ruoli: QUALE modello lo decide l'indice, non questa lista):
- small/mid dense (fit in 12GB VRAM) -> **Ryzen**. SUPERATO (27/11/2026): ripiego Lenovo `mistral:latest` (rimosso) e "14B q4 su Ryzen" (nessun 14B installato).
- MoE / grandi (es. `qwen3-coder:30b`, `gemma4:26b`) -> **Lenovo** (RAM-offload 64GB). Lo swarm Dafne gira qui (modelli dello swarm: non verificati il 27/11).
  SUPERATO (27/11/2026): tier 120B `gpt-oss:120b` (rimosso).
- embedding -> entrambe (cheap).

**llmfit = 2-stage, NON 1** (caveat load-bearing OD-056 S4): la lista llmfit risponde a "cosa gira bene sul mio HW + qualita' generale di categoria", NON "quale modello fa meglio il MIO task". Pipeline: **llmfit shortlist-by-HW -> task-eval sul prompt reale** (soglie e N: METODO v4). HW-fit != task-fit. Per output-strutturato/rule-following preferire clean-instruct, NON reasoning/think (lezione storica su deepseek-r1, rimosso il 27/11).

**Parallelo ~2x (VALIDATED 2026-05-22)**: batch indipendenti (synthesis, calibration N-run, bulk tagging, swarm specialist batch) -> shard su 2 endpoint Ollama (`.10:11434` + Ryzen `localhost:11434`), 1 worker/macchina, `OLLAMA_HOST` pinned per worker. Precedente: `Game/tools/py/calibrate_parallel.py`. Gotcha port-bind: anti-pattern #16 / L-071. NON mettere 2 job VRAM-heavy sulla stessa GPU (contention -> piu' lento del seriale).

SUPERATO (27/11/2026): la matrice tier 7B/14B/30B sotto non decide piu' QUALE modello (i modelli 7B/14B non esistono piu'); il constraint-count ADR-0016 resta come criterio di delega. Scelta finale task concreto: **ruolo promosso nell'indice -> `ollama list` sull'host -> task-eval se serve un cambio**.

## Scopo

Definire quale strumento / modello / accesso usare per ogni fase. Evita: usare sempre lo stesso strumento per tutto; accumulare modelli senza ruoli chiari; mandare codice sensibile in cloud; perdere tempo/$ su task delegabili piu' veloci/economici.

**Regola madre**: Fonte complessa -> Comprensione -> Compressione -> Decisione -> Esecuzione -> Compact -> Archivio. In concreto: Comprensione/Sintesi/Decisione = Claude Code (read multi-file + ADR draft, approvazione utente esplicita); Esecuzione coding = Aider + wrapper cloud-free o modello locale di riferimento (matrice tier SUPERATO 27/11); Compact/Archivio = Claude Code (docs/ / logs/ / memory).

## Profilo progetto

- **Tipo**: infrastructure-as-code + registry decisionale (repo infra + ADR/patterns + log operativi).
- **Privacy**: repo personale OK cloud; progetti dipendenti hanno policy per-repo separata.
- **Costo**: Claude Max attivo (abbonamento primario); se cessa, target <$20/mese on-demand (ADR-0023/0030).
- **Hardware**: fleet 2-macchine (vedi "Fleet 2-machine routing" sopra). NON piu' single-machine 8GB-bound: il 7B-only/14B-Q2 era framing Lenovo-solo.
- **Velocita'**: daily-driver 8-10h/giorno, iterazione rapida essenziale.
- **Priorita'**: privacy + costo (>= qualita') in stato sovereign. Con Max attivo: qualita'+velocita' primarie.

## Stack disponibile

- **Claude Code** (OAuth Max attivo; riserva: API key on-demand, ADR-0023).
- **Aider** + wrapper in `~/.local/bin/` (Lenovo). `aider-cosmetic` e `aider-refactor` sospesi dal 27/11 (vedi "Stato").
- **Ollama** su entrambi gli host (elenco: `ollama list` sull'host; ruoli: indice).
- **OpenCode** (npm global; tier multi-step agentic con tool calls; ADR-0022 Accepted).
- **API esterne**: Groq + Cerebras (free) + Gemini + OpenAI (paid). Keys (conteggio NON hardcodato: leggi il file -- anti-rot stale-claim, OD-048) in `~/.config/api-keys/keys.env`.
- NotebookLM / ChatGPT: saltuari da browser, NON integrati repo.

## Routing per fase

| Fase | Obiettivo | Strumento | Modello | Output atteso |
|---|---|---|---|---|
| Comprensione | leggere repo + docs | Claude Code Max | Opus | mental model + citation file:line |
| Sintesi | compattare | Claude Code Max | Opus | COMPACT_CONTEXT update |
| Planning | ADR draft / sprint plan | Claude Code Max | Opus | ADR MADR / SPRINT_NN.md |
| Repo map | structure analysis | Claude Code Max | Opus | reference index / repo overview |
| Coding cosmetic | JSDoc, rename, lint | Aider + wrapper cloud | Cerebras 8B cloud (SUPERATO: Qwen 7B local) | diff additive pulito |
| Coding behavior | refactor, bug fix | Aider + wrapper cloud | Groq 70B cloud (SUPERATO: Qwen 14B Q2 local) | diff controlled + review manuale |
| Coding locale | 1 file, privacy/costo | nessun percorso operativo oggi (nessun wrapper punta al modello di riferimento): esegui diretto | riferimento "codice" nella riga Ruoli | diff + review manuale |
| Capability-max | debug strategico, multi-file refactor | Claude Code Max | Opus | resolution (non delegabile) |
| Review | QA edit recente | Claude Code Max | Opus | `git diff` audit + semantics |
| Compact / Archivio | chiusura sessione | Claude Code | Opus / fs | COMPACT + JOURNAL + memory |

**Piano di riserva se Max cessa (ADR-0030 Hybrid A1; Max resta attivo)**: "Capability-max" + "Planning strategico" -> **Claude Code Pro $20/mo** (primary); se Pro daily-limit -> **Claude API on-demand** (overflow ad-hoc, cap $10-20/mese ADR-0023, log via `scripts/claude-api/log_spend.py`); routine fallback **Groq/Cerebras cloud-free** (era Gemini CLI free; il path OAuth-login free e' RITIRATO 2026-06-18 -- vedi ADR-0030 addendum; resta `aider-gemini` via API-key); emergency **OpenRouter**. Daily coding resta Aider cloud-free (locale: vedi sopra).

## Routing consigliato per scenario

### Se ho molte fonti eterogenee
NotebookLM browser (Gemini Pro) per corpus analysis -> synthesis back a repo come `docs/research/NNNN.md`. Claude Code non e' ottimo su corpus massivo scattered.

### Se devo capire e toccare il repo
Claude Code nativa (Opus via Max; se Max cessa: API o Sonnet, ADR-0023). Integrazione nativa filesystem + Glob/Grep/Edit/Read -> file scritti nel repo (file-first).

### Se devo scrivere documenti, backlog, ADR
Claude Code Opus (Max). Se Max cessa (ADR-0030): Claude Code Pro (primary strategico) OR Claude API on-demand (overflow, ADR-0023) OR Groq 70B via `aider-groq-bypass` (ADR operativo semplice). Reasoning strategico + consistency di stile.

### Se devo lavorare in locale per privacy o costo
Default locale solo nei ruoli con riferimento o promozione nelle fonti; altrove nessun default locale (uso di prova libero e dichiarato, non default). Il caso "bugfix su 1 file con test" = ruolo worker Orca, testato e non promosso. Verifica `ollama list` sull'host prima.
SUPERATO (27/11/2026): `qwen2.5-coder:7b` (cosmetic) + `qwen2.5-coder:14b-q2_K` (behavior) + escalation "oltre capability 14B" -- modelli rimossi.

### Se devo usare il cloud
Aider + wrapper (`aider-groq-bypass`, `aider-cerebras`, `aider-gemini`, `aider-openai`). Modello primario: `groq/llama-3.3-70b-versatile` (free tier, LPU speed, capability 70B dense).
- **OpenCode + cloud free NON viable** (ADR-0022): TPM 6-12k Groq + context 8k Cerebras 8B << OpenCode default request ~50k token. OpenCode resta sovereign-only (Ollama 30B MoE: uso di prova libero e dichiarato, non default).
- **Cosa NON mandare al cloud**: codice repo cliente (sempre); Synesthesia `controllers/`/`routes/`/`middlewares/` (auth sensitive); segreti / env vars / API keys / token; output che contenga i sopra.

### Se devo fare task multi-step agentic con tool calls
OpenCode (NOT Aider, scope diverso). Modello: `ollama/qwen3-coder:30b` MoE A3B (Lenovo, ADR-0022) = uso di prova libero e dichiarato, non default: nelle fonti il ruolo "tool" non ha locali promossi. Tool calls: Read, Edit, Bash, ListFiles, Glob, Grep, MCP servers.
- **Cosa NON usare con OpenCode**: cloud free tier (rate-limited TPM o context-limited); qualsiasi task single-file edit semplice (Aider superiore: faithful diff; misura storica di maggio: 7B 5s vs OpenCode 30B 45s).

## Policy locale / cloud

**Locale prima? SI come filosofia, ma default solo nei ruoli con riferimento o promozione** -- filosofia sovereign (ADR-0001) + privacy-by-default + zero rate-limit dependency.

**Quando il locale basta**: solo nei ruoli con riferimento o promozione nelle fonti (SUPERATO 27/11: "cosmetic task; behavior-critical single-file" via tier Qwen); bench/framework iterativi; sperimentazione/prototipo; task con codice sensibile (sovereign guard rail).

**Quando il cloud e' giustificato**: speed-critical (Groq ~20x piu' veloce di locale 30B MoE); multi-file refactor >3 file target; ruolo senza locale promosso nell'indice; capability reasoning oltre il locale (debug architetturale); quality validation (second opinion); task volumetrici (>10min total locale).

**Materiali che NON devono uscire in cloud**: API keys, .env, credenziali; codice cliente / progetti NDA; Synesthesia backend auth (`controllers/`, `routes/`, `middlewares/`); log con path utente sensibili; dump database o dati personali.

## Modelli attivi del progetto

**Modelli locali**: nessuna tabella qui. Ruoli promossi -> indice (`INDICE-VALUTAZIONE-LLM.md`, vedi "Stato al 27/11/2026"); installati -> `ollama list` sull'host.
SUPERATO (27/11/2026), righe tolte: `qwen2.5-coder:7b` (tier 1 cosmetic), `qwen2.5-coder:14b-q2_K` (tier 2 behavior), `deepseek-r1:8b` (tier reasoning), `deepseek-coder-v2:16b` (speed-first Ryzen) -- non installati su nessun host; `qwen3-coder:30b` (escalation Aider / default OpenCode) e `gemma4:latest` (multimodale) -- installati sul Lenovo, ma senza ruolo promosso nell'indice.

| Modello | Runtime / accesso | Ruolo | Quando usarlo | Quando NON usarlo |
|---------|-------------------|-------|---------------|-------------------|
| `groq/llama-3.3-70b-versatile` | Cloud free (6k tok/min) | tier 3 behavior cloud | Online, privacy OK, capability 70B needed | repo sensitive, quota limit, offline |
| `cerebras/llama3.1-8b` | Cloud free | tier 3 cosmetic cloud fast | Online, cosmetic batch veloce | behavior complesso (8B capability limit possibile) |
| `gemini/gemini-2.5-flash` | Cloud 60 req/min | tier 3 quick query | fast explain / translate / summarize | coding edit (richiede `thinkingBudget=0` esplicito) |
| `openai/gpt-4o-mini` | Cloud paid | tier 4 capability-max | task estremi free-tier non copre | default daily (paid, ccusage monitor) |
| Opus (via Claude Code/Max) | Cloud Max OAuth | tier 0 strategic | comprensione, planning, ADR, multi-file, debug arch | operazioni meccaniche (spreco token) |

**Regola**: meglio **pochi modelli con ruoli chiari** che molti modelli sovrapposti. Modelli deprecati (in `docs/adr/` o marked reference-only): **non usare**.

**Scelte minime**: locale = il modello promosso nell'indice per il ruolo (SUPERATO 27/11/2026: `qwen2.5-coder:14b-q2_K` come locale principale). Cloud principale = `groq/llama-3.3-70b-versatile` (free + LPU speed + 70B quality parity). Fallback = `openai/gpt-4o-mini` (capability-max ultimo resort, paid, ccusage monitor).

## Regole anti-caos

1. Non fare la stessa cosa in tre strumenti (scegli uno per corpus).
2. Non mandare fonti grezze nel coding tool prima di capirle (fase Comprensione separata).
3. Non accumulare modelli "per sicurezza" (ADR-0005 YAGNI -- aggiungi solo quando trigger).
4. Non tenere implicito il routing: questo file e' la verita' per il routing, se non e' scritto qui **non e' una regola** (per i ruoli dei modelli locali valgono le fonti in "Stato").
5. Se un passaggio aumenta caos invece di ridurlo, fermati e consolida (es. tier 3 cloud fail rate >30% -> torna al locale di riferimento, se il ruolo ne ha uno, prima di debug wrapper).

**File da aggiornare dopo ogni passaggio importante**: `COMPACT_CONTEXT.md`, `DECISIONS_LOG.md` (strategiche -> ADR separato), `BACKLOG.md`, `REFERENCE_INDEX.md`, `JOURNAL.md`, `logs/aider-delegation-YYYY-MM.md`, memory `~/.claude/projects/.../memory/`.

## Constraint count -- seconda dimensione routing (ADR-0016)

Misura storica (maggio 2026, modelli in parte rimossi il 27/11: i tier 14B Q2 della tabella non esistono piu'; il criterio resta). Dogfood Fase 6 (n=8) ha rivelato che la success-rate delega degrada col numero di constraint espliciti, indipendentemente dalla classe (cosmetic/behavior):

| Constraint count | Esito | Regola |
|:---:|:---|:---|
| 1 (add-only / fix puntuale) | ~100% qualsiasi tier | Safe delega |
| 2-3 (fix + transform / logic change) | ~80-85% (14B Q2 / Groq 70B) | Preferire diff + review manuale |
| 5+ (multi-constraint strict + branch-semantic) | ~20% REJECT | **Rewrite manuale Claude Code** |

**Implicazione**: la matrice CLAUDE.md "Priorita' modelli AI" si basa su CLASSE task; ADR-0016 aggiunge **constraint-count** come seconda dimensione (estende, non sostituisce). Operativa: quando classifico pre-delega, conto i constraint espliciti -- se >=5 skip delega, rewrite direct. Distinzione transform vs preserve (7B skippa transform; 14B Q2 safe su preserve). Causa ipotetica: LLM <=70B preservano ~2-3 constraint simultaneamente, oltre "dimenticano" i meno prominenti (tipicamente i trasformativi). Matrice 2D completa + rationale empirico (n=11 cumulative, esempi dogfood #6/#7/#8): `docs/adr/0016-constraint-count-routing-dimension.md`.

## Status decisione (post-Fase 6 closure + ADR-0022 Accepted)

**Scenario A full-sovereign confermato Accepted 2026-05-07** (ADR-0015), pensato per la transition Max (oggi riserva: Max attivo). Soft-override esteso n>=12 con 5 rationale empirici; cumulative al 2026-05-09 zero trigger attivati (PASS OpenCode 30B MoE 3/3, Aider Fase 6 fail rate 8.3%).

- **Oggi (Max attivo)**: Claude Code per comprensione/planning/multi-file/strategic; locale solo nei ruoli promossi dall'indice; Aider + Groq/Cerebras cloud per coding 1-file speed-critical (privacy permitting); OpenCode + `qwen3-coder:30b` per multi-step agentic = uso di prova libero e dichiarato, non default (ADR-0022). SUPERATO (27/11/2026): "Aider + Qwen local (o Ryzen q4)".
- **Piano di riserva se Max cessa (Fase 8 sovereign)**: Aider + Ollama daily-driver; OpenCode + Ollama 30B MoE per agentic multi-step; cloud free Aider-side per speed/capability marginale (NON OpenCode, rate-limited). Claude Code Max dismesso. **Tier 0 strategic** -> Claude Code Pro $20/mo primary (ADR-0030 Hybrid A1, supersede parziale ADR-0023); Claude API on-demand = overflow ad-hoc se Pro daily-limit, budget cap $10-20/mese (ADR-0023), tracking `logs/claude-api-spend-*` via `scripts/claude-api/log_spend.py`. Per repo sensibili: modello locale promosso nell'indice + diff locale (SUPERATO: Qwen 14B Q2).
- **Privacy validation Synesthesia** (criterio #3 ADR-0014): DEROGATO retroattivo, completamento post agosto 2026 (riattivazione pre-esame UniUPO).
- **Trigger ri-evaluation soft-override**: silent-corruption working-tree >=1 caso reale -> ADR-0015 addendum + scenario B revisited; fail rate cumulative >15% -> revisione routing tier; privacy violation in repo non-sensitive -> ADR addendum reactive.
- **Prossimo test** (deferred SPRINT_02): n>=3 data points constraint-count addizionali per ADR-0016 Accepted; dogfood organici OpenCode reali verso n>=20 cumulative.

Dettaglio narrativo completo: ADR-0008 (whole-format silent-corruption), ADR-0015 (sovereign scenario A), ADR-0016 (constraint-count), ADR-0022 (OpenCode tool-use), ADR-0023 (tier 0 strategic post-Max).

## Research input esterno -- vault LLM routing matrix (reference only)

vault (`C:/dev/vault`, sibling-peer codemasterdd) ha una decision matrix derivata da bench A/B claude-vs-ollama. **NON adoption diretta** (vault scope = content-routing, codemasterdd = code-edit-routing): reference solo per pattern + methodology, NON ground-truth senza audit empirico codemasterdd-side.
- Path: `C:/dev/vault/llm-routing.json` + `vault/docs/research/` (5 report Quality Gate Step 2, 2026-05-10). Methodology rigorosa: split metrics (cold_load_s + inference_s + wall_s) + keep_alive=-1 + retries exponential backoff + output validation.
- Inspiration potenziale: metric "wall time reduction %"; distinzione esplicita content-routing vs code-edit-routing; multi-variant Claude self-tune A/B. Integrato 2026-05-10 via AA01 task research-long; memory `project_vault_shared.md` + STATUS_MULTI_REPO sezione 6.
