# ADR-0022 — OpenCode tool-use model routing (separate tier from Aider)

> *TL;DR: smoke test 2026-05-08 (n=5 entries #16-#20) ha empiricamente validato che Qwen 2.5 Coder family (sia 7B che 14B Q2) NON e' tool-use native compatibile con OpenCode `run` mode -- emette tool call come JSON raw stringificato che OpenCode passa in stdout senza eseguire. Solo Qwen3-Coder 30B MoE A3B esegue correttamente i tool call. Si introduce **tier routing OpenCode-specifico** (distinto da Aider tier ADR-0008): default `ollama/qwen3-coder:30b`, NON usare Qwen 2.5 Coder family con OpenCode. Aider e OpenCode coesistono come tool per use case diversi (single-file edit vs multi-step agentic). Cloud free 70B (Groq llama-3.3) rate-limited TPM 12k vs context 50k OpenCode -- non viable senza upgrade Dev Tier o context trim.*

- **Status**: **Accepted (early, n=3, ratification check 2026-06-09)**
- **Data**: 2026-05-08 Proposed -> 2026-05-09 Accepted (early)
- **Decisore**: Eduardo Scarpelli
- **Tipo decisione**: tier routing tool-specifico (OpenCode workflow)
- **Early-acceptance rationale (ADR-0010 addendum 2026-05-09)**: validation n=3 (1 smoke read + 2 dogfood edit reali, 3/3 PASS Ollama qwen3-coder:30b MoE). Sample piccolo ma 3/3 e' signal forte, no contrarian. Ratification check obbligatorio entro 2026-06-09 con n>=10 task cumulative naturali OR contrarian event handled (es. tool-use raw JSON pattern Qwen3 family in nuovo modello).

## Context and Problem Statement

Durante la transizione attiva pre-Max expiration (8-19/05) e' stato introdotto OpenCode v1.14.41 come secondo client agentic sovereign accanto ad Aider. Il setup iniziale ha clonato la decision matrix Aider (ADR-0007/0008) come default OpenCode config (`"model": "ollama/qwen2.5-coder:14b-instruct-q2_K"`).

Smoke test n=5 eseguiti 2026-05-08 sera (entries #16-#20 in `logs/aider-delegation-2026-05.md`) hanno esposto un **gap di compatibilita' tool-use** non noto prima:

| Smoke | Stack | Tool-use req | Esito |
|-------|-------|--------------|-------|
| #16 | ollama/qwen2.5-coder:7b | NO (basic IO) | PASS "TEST" -> "TEST" |
| #17 | ollama/qwen2.5-coder:7b | YES (read tool) | **FAIL** raw JSON tool call non eseguita |
| #18 | groq/llama-3.3-70b-versatile | YES | **FAIL** rate limit TPM 12k vs request 50k |
| #19 | ollama/qwen3-coder:30b | YES | **PASS** read tool eseguita, output corretto |
| #20 | ollama/qwen2.5-coder:14b-instruct-q2_K | YES | **FAIL** stesso pattern di #17 (JSON raw) |

Il pattern fail di smoke #17 e #20 e' identico:

```text
input: "Read the file scripts/aider-log.sh and explain in 2 sentences"
expected: tool call eseguita -> file letto -> 2 frasi spiegazione
actual: stdout = {"name":"read","arguments":{"filePath":"C:\\dev\\..."}}
```

Qwen 2.5 Coder family emette il tool call come JSON stringificato in output testuale invece che attraverso il protocollo tool-use OpenAI-compatible che OpenCode si aspetta. Il modello "sa" che vorrebbe usare il tool ma non lo fa nel formato che OpenCode parsa.

Questo cambia significativamente il tier routing: il "sweet spot" Aider+14B Q2 (validato in ADR-0007/0008 con 5+ behavior-critical PASS) **non si trasferisce** a OpenCode workflow.

## Decision Drivers

- **Tool-use native requirement**: OpenCode richiede modelli tool-use trained nel formato OpenAI-compatible. Qwen 2.5 Coder family non lo e' (Qwen 2.5 Coder e' code-completion specialized, non tool-use trained per agentic frameworks).
- **Sovereign-first preservato**: ADR-0001/ADR-0015 scenario A. OpenCode default deve essere local, non cloud.
- **Aider workflow preservato**: ADR-0007/ADR-0008 restano validi per Aider. Non sostituire un tool, aggiungerne uno per scope diverso.
- **Cloud free tier rate-limit awareness**: Groq free tier llama-3.3-70b ha TPM 12k -- insufficiente per OpenCode default context (~50k token system + tool defs + file). Cerebras free tier da validare.
- **VRAM/RAM headroom**: post upgrade 64GB RAM (ADR-0012), modello 30B MoE entra senza pressione. 18 GB disk + ~22 GB loaded RAM, GPU partial offload OK.

## Considered Options

### Opzione A -- Status quo: clonare Aider tier per OpenCode

Default config OpenCode `"model": "ollama/qwen2.5-coder:14b-instruct-q2_K"` come per Aider behavior-critical.

**Pro**:
- Zero tier routing nuovi da imparare
- Coerenza apparente con ADR-0007/0008

**Contro**:
- Smoke #17 + #20 dimostrano fail mode silent (JSON raw in stdout, OpenCode `run` non capisce, user vede testo strano)
- Default scaduto: ogni `opencode run` con tool-use req fallirebbe silently
- Disinformativo: "Aider tier funziona ovunque" e' falso

### Opzione B (chosen) -- Tier routing OpenCode-specifico, distinto da Aider

Default config OpenCode aggiornato a `ollama/qwen3-coder:30b` (MoE A3B, validato tool-use native in smoke #19).

Tier routing OpenCode-specifico:

| Use case | OpenCode tier | Validato? |
|----------|---------------|-----------|
| Default agentic single-shot | `ollama/qwen3-coder:30b` | YES (smoke #19) |
| Cloud paid emergency | `openai/gpt-4o-mini` | non testato (tier 4 emergency) |
| **NON usare con OpenCode (modello locale)** | qwen2.5-coder family (7B/14B/32B) | smoke #17 + #20 fail tool-call raw JSON |
| **NON usare con OpenCode (cloud free)** | Groq/Cerebras free 8B-70B | smoke #18/#21/#22/#23 fail TPM/context limit |

**Cloud free providers -- findings consolidati (smoke #21-#24, addendum 2026-05-08 sera)**:

| Provider | Modello | Limit | Compat OpenCode default? |
|----------|---------|-------|--------------------------|
| Groq | llama-3.3-70b-versatile | TPM 12k | ❌ FAIL (request 50k) |
| Groq | llama-3.1-8b-instant | TPM 6k | ❌ FAIL (request 50k) |
| Cerebras | llama3.3-70b | paid-only | ❌ FAIL (no free access) |
| Cerebras | llama3.1-8b | context 8k | ❌ FAIL loop (request 12k+) |
| Google | gemini-2.0-flash-exp | deprecated v1beta | ❌ 404 |
| Google | gemini-2.5-flash | TBD | ❓ INCONCLUSIVE (output non captured) |

**Conclusione cloud free**: nessun provider cloud free tier testato e' viable per OpenCode default context (~50k token). Solo Ollama local sovereign opera senza rate-limit.

**Modelli cloud non ancora testati (OpenCode-compat TBD, probabili paid tier)**: Cerebras qwen-3-235b-a22b-instruct-2507, gpt-oss-120b, zai-glm-4.7.

**Conseguenza tier routing**: OpenCode workflow rimane **sovereign-only** (Ollama 30B MoE). Cloud free per agentic non viable senza Dev Tier paid upgrade. Aider-* wrapper restano via principale per cloud free delegation (constraint single-file, context << 50k).

Distinction esplicita Aider vs OpenCode:

| Workflow | Tool consigliato | Tier default | Razionale |
|----------|-----------------|--------------|-----------|
| Single-file edit (cosmetic/behavior) | Aider + diff/whole | qwen2.5-coder:14b-Q2 | ADR-0007/0008, faithful constraint-respect |
| Multi-step agentic con tool calls | OpenCode | qwen3-coder:30b | Tool-use native, smoke #19 |

**Pro**:
- Validazione empirica n=5 supporta decisione
- Default config previene fail mode silent (Qwen 2.5 + tool-use)
- Preserva Aider tier come autoritativo per single-file edit
- Scope chiaro: 2 tool, 2 use case, 2 tier matrix

**Contro**:
- Cognitive overhead: 2 decision matrix invece di 1
- Tier OpenCode richiede 30B MoE (latency ~45s vs 14B Q2 ~25s)
- 30B MoE consuma piu' VRAM/RAM (RAM upgrade ADR-0012 mitiga)

### Opzione C -- Skip OpenCode, mantenere Aider only

**Pro**:
- Zero complessita' aggiuntiva
- Aider gia' validato n=12 dogfood

**Contro**:
- OpenCode copre use case Aider non gestisce: multi-step agentic, MCP servers, multi-file refactor con tool calls coordinati, GitHub agent, web interface
- Investimento setup OpenCode (install + config + 5 smoke) sprecato
- Limita esplorazione sovereign workflow alternative pre-Max expiration

### Opzione D -- Migrazione completa a OpenCode, abbandonare Aider

**Pro**:
- Single tool, single tier matrix
- OpenCode piu' moderno (TUI + ACP + MCP support)

**Contro**:
- ADR-0007/0008 invaliderebbero (perdita 12 dogfood validation Aider)
- Aider e' superiore per single-file edit semplice (constraint-respect, latency 7B 114 tok/s)
- 30B MoE default OpenCode ha latency ~45s vs Aider 7B ~5s -- regressione UX su task semplici
- Anti-pattern "tool nuovo invalida tool vecchio" senza evidenza superiorita'

## Decision Outcome

**Scelto Opzione B**: tier routing OpenCode-specifico distinto da Aider.

### Config OpenCode applicata 2026-05-08 sera

`~/.config/opencode/opencode.json`:

```json
{
  "model": "ollama/qwen3-coder:30b",
  "small_model": "ollama/qwen3-coder:30b",
  "instructions": [
    "Default: ollama/qwen3-coder:30b MoE A3B (tool-use native, validated via smoke 2026-05-08).",
    "WARNING: Qwen 2.5 Coder family (7B + 14B Q2) emits tool calls as raw JSON in OpenCode run mode -- NOT executed. Use only for direct Ollama API calls or Aider workflows.",
    "Aider tier routing (separate from OpenCode): cosmetic 7B + whole, behavior 14B Q2 + diff. See CLAUDE.md.",
    "Cloud free 70B (e.g. groq/llama-3.3-70b-versatile): RATE-LIMITED to TPM 12k vs OpenCode context 50k. Use only on trimmed contexts or upgrade tier."
  ]
}
```

### Aider routing invariato

ADR-0007/0008 restano validi per Aider. Wrapper `aider-cosmetic` / `aider-refactor` / `aider-groq` / `aider-cerebras` / `aider-gemini` / `aider-openai` continuano a usare tier Aider documentato.

### Routing decision tree (Aider vs OpenCode)

```
Task type?
+- Single-file edit (cosmetic/behavior) ............... Aider
|  +- cosmetic JSDoc/docstring/rename ................. aider-cosmetic (7B + whole)
|  +- behavior refactor/bug fix ....................... aider-refactor (14B Q2 + diff)
|  +- behavior escalation safe-fail ................... aider + qwen3-coder:30b + diff
|  +- cloud delegation (privacy permitting) ........... aider-groq / aider-cerebras (70B + diff)
|
+- Multi-step agentic (tool calls, MCP, coord) ....... OpenCode
|  +- default sovereign ............................... opencode + ollama/qwen3-coder:30b
|  +- cloud agentic (privacy permitting) .............. opencode + cerebras/llama3.3-70b (TPM TBD)
|
+- Strategic (multi-file, design, ADR writing) ....... Claude Code direct (no delegate)
```

## Consequences

### Positive

- Default OpenCode previene fail mode silent (Qwen 2.5 + tool-use mismatch)
- Tier routing chiaro e validato empiricamente
- Aider preserva sweet spot 14B Q2 per single-file edit (zero regressione)
- 2 tool coexist, scope diversi e complementari
- Findings smoke utilizzati per affinare workflow PRE Max expiration (safety net 11gg residui)

### Negative

- Cognitive overhead: 2 decision matrix da memorizzare (Aider tier + OpenCode tier)
- 30B MoE default richiede ~22 GB RAM caricato (vs 14B Q2 ~6 GB) -- mitigato da upgrade 64GB ADR-0012
- Latency OpenCode default piu' alta vs Aider single-shot (45s vs 5s su task simili)
- Cloud free 70B rate-limit blocca scenario "OpenCode + cloud free per fast iteration"

### Neutral

- 5 smoke entries documentate in log (gitignored), validation reference
- ADR-0017 stack active mode + Langfuse traces utili per debugging futuro tool-use issues

## Ratification (Accepted 2026-05-09)

Trigger Accepted raggiunto:

- **Dogfood #25** (PR #17 mergeato): docstring `empty_stats()` in `apps/dogfood-ui/stats.py` -- PASS 1st-try, AST valid, diff +1/-0
- **Dogfood #26** (PR #18 mergeato): docstring `_auth_header()` in `apps/dogfood-ui/langfuse_client.py` -- PASS 1st-try, AST valid, diff +1/-0, indentazione classe (8 spaces) preservata correttamente

PASS rate cumulativo Ollama 30B MoE OpenCode: **3/3** (smoke read #19 + edit reali #25 + #26).

Pattern wrong-target-file (ADR-0008) NON osservato in nessuno dei 3 test reali.

Decision tree Aider vs OpenCode validato empiricamente:
- Aider single-file edit: tier 14B Q2 + diff (ADR-0007/0008) preservato
- OpenCode multi-step agentic: tier qwen3-coder:30b MoE (questo ADR) confermato

## Follow-up

- [x] Config OpenCode applicata (`~/.config/opencode/opencode.json` v2)
- [x] 11 entries log (`logs/aider-delegation-2026-05.md`, entries #16-#26: 9 smoke + 2 dogfood reali)
- [x] ADR-0022 scritto (questo file, Proposed -> Accepted 2026-05-09)
- [x] **Validare cloud free providers OpenCode-compat** (smoke #21-#24): tutti FAIL TPM/context limit. Solo Ollama local viable.
- [x] **Test OpenCode + qwen3-coder:30b su task edit reale** (dogfood #25 + #26 entrambi PASS 1st-try, PR #17 + #18 mergeati 2026-05-08)
- [x] **Trigger Accepted raggiunto**: 2/2 dogfood organici reali confermano tier routing senza fail mode nuovi
- [ ] Aggiornare CLAUDE.md sezione "Priorita' modelli AI" con sezione OpenCode tier (post-Accepted, ora attivabile)
- [ ] Aggiornare `MODEL_ROUTING.md` con decision tree Aider vs OpenCode
- [ ] Test cloud paid tier OpenCode-compat: cerebras qwen-3-235b / gpt-oss-120b / zai-glm-4.7 (deferred, condizionale a budget post-19/05)
- [ ] Aggiornare CLAUDE.md var name `GEMINI_API_KEY` -> nota dual-name (`GEMINI_API_KEY` per Aider/LiteLLM, `GOOGLE_GENERATIVE_AI_API_KEY` per OpenCode native Google provider)

## Riferimenti

- ADR-0007 -- Aider Qwen quantization findings: `0007-aider-qwen-quantization-findings.md`
- ADR-0008 -- Aider whole format silent-corruption + tier routing: `0008-aider-whole-format-silent-corruption.md`
- ADR-0012 -- RAM 64GB upgrade impact: `0012-ram-upgrade-64gb-impact.md`
- ADR-0013 -- Tier 3 cloud free providers: `0013-tier3-cloud-free-providers.md`
- ADR-0015 -- Fase 7 budget decision (scenario A full-sovereign): `0015-fase7-budget-decision-full-sovereign.md`
- ADR-0017 -- UI + observability stack (LiteLLM proxy + Langfuse): `0017-ui-observability-stack.md`
- Smoke test entries #16-#20: `logs/aider-delegation-2026-05.md` (gitignored)
- OpenCode docs: https://opencode.ai/
- Models registry: `opencode models <provider>`
