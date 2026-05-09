# Bench OpenCode + cloud free providers (M10)

**Data**: 2026-05-09 sera
**Scope**: BACKLOG M10 deferred SPRINT_02. Verifica empirica se cloud free 70B/8B viable per task piccoli via OpenCode.
**Ipotesi**: minimal-context task (no-file o single-file small ~1-4kB) sotto rate limit Groq TPM 6-12k vs ADR-0022 finding "default 50k token rate-limited".

## Setup

- OpenCode v1.14.41 (`C:/Users/edusc/AppData/Roaming/npm/opencode.ps1`)
- API keys loaded da `~/.config/api-keys/keys.env` (Groq + Cerebras)
- Test runner: `scripts/bench-opencode-cloud-free.ps1`
- File piccolo per test attached: `apps/dogfood-ui/db.py` (4239 bytes)

## Test matrix

| ID | Provider/Model | Prompt | File attached | Hypothesis |
|----|----------------|--------|---------------|------------|
| T1 | groq/llama-3.3-70b-versatile | "Print hello world in python." | - | baseline minimal context |
| T2 | groq/llama-3.3-70b-versatile | "Summarize this code in 1 sentence." | db.py 4kB | typical small-file task |
| T3 | groq/qwen-2.5-coder-32b | "Print hello world in python." | - | coder-specific 32B free |
| T4 | cerebras/llama3.1-8b | "Print hello world in python." | - | Cerebras 8B context 8k |
| T5 | cerebras/llama3.1-8b | "Summarize this code in 1 sentence." | db.py 4kB | Cerebras 8B context budget |

## Risultati

| ID | Model | Verdict | Note empirico |
|----|-------|---------|---------------|
| T1 | groq/llama-3.3-70b-versatile | **FAIL rate-limit** | TPM 12000 limit, OpenCode richiesto 49698 token (1st try) + 32438 (retry). Entrambi BLOCKED 413-equivalent. |
| T2 | groq/llama-3.3-70b-versatile +file 4kB | SKIP test syntax | Flag `--file` consuma prompt positional come secondo file (yargs array greedy). Skip per non-blocker (T1 baseline gia' conclusivo). |
| T3 | groq/qwen-2.5-coder-32b | **FAIL DECOMMISSIONED** | Modello deprecato: `Error: model qwen-2.5-coder-32b has been decommissioned and is no longer supported`. **Side-finding**: refresh CLAUDE.md + `~/.config/opencode/opencode.json` per rimuovere reference. |
| T4 | cerebras/llama3.1-8b | **FAIL ctx-limit** | Context limit 8192 vs OpenCode richiesto 12228 token. Modello iniziato output structured plan (Goal/Constraints/Progress) prima del fail -- conferma overhead OpenCode anche per prompt 5-word. |
| T5 | cerebras/llama3.1-8b +file 4kB | SKIP test syntax | Stesso bug yargs T2. T4 baseline gia' conclusivo. |

**Note**: tutti i test ritornano exit code 0 nonostante il fail logico (errore stampato, processo terminato pulito). Validation richiede stderr/stdout content parse, non $LASTEXITCODE.

## Findings

### Conferma ADR-0022 (n=3 cumulative)

ADR-0022 finding "cloud free 8B-70B rate-limited TPM o context-limited vs OpenCode default request ~50k token" **CONFERMATO empiricamente** anche con prompt minimal 5-word ("Print hello world in python."):

| Provider | Modello | Limit | OpenCode richiesto | Margine |
|----------|---------|-------|--------------------|---------:|
| Groq    | llama-3.3-70b-versatile | TPM 12000 | 49698 (1st), 32438 (retry) | **-2.7x .. -4.1x** |
| Cerebras | llama3.1-8b              | ctx 8192  | 12228 | **-1.5x** |

Anche al retry (Groq abbassato a 32k) resta sopra TPM limit di 2.7x. Con file attached la differenza peggiora ulteriormente.

### Discovery overhead OpenCode

OpenCode aggiunge ~12-50k token di system context per prompt 5-word:
- Cerebras 8B: 12k overhead minimum
- Groq 70B: 50k overhead minimum (4x cerebras, possibile difference per provider context budget hint)

Origine probabile overhead: system prompt agent + tool call definitions (Read/Edit/Bash/Glob/Grep/ListFiles + MCP server schemas se attivi).

**Implicazione**: il flag `--max-tokens` (oggetto originale dell'M10 hypothesis) NON esiste su OpenCode `run` -- nessun knob esposto per limitare INPUT context da CLI. L'unico tuning possibile e' a livello provider config (es. limitare tool set), out-of-scope per opt-in workaround Eduardo.

### Side-finding: model deprecation Groq qwen-coder-32b

`groq/qwen-2.5-coder-32b` decommissionato da Groq. Refresh richiesto:
- `~/.config/opencode/opencode.json` rimuove dal provider Groq
- `CLAUDE.md` "Stack installato" + tier 3 cloud reference: nessuna menzione esplicita rilevante (cleanup opzionale)
- `MODEL_ROUTING.md` non lista esplicitamente qwen-2.5-coder-32b

## Decisione

**ADR-0022 status invariato (Accepted 2026-05-09)**. Nessun addendum necessario:
- Cloud free non viable per OpenCode default mode confermato cross-provider (Groq 70B + Cerebras 8B + 1 model decommissioned)
- Pattern decisionale invariato: OpenCode = sovereign-only (Ollama qwen3-coder:30b MoE), cloud paid emergency = `openai/gpt-4o-mini`
- Eventuale workaround context-trim non e' nativo OpenCode (no flag CLI). Da esplorare solo se trigger reale (es. budget gpt-4o-mini eccessivo): plugin custom o limitare tool set via config -- tracked come **L6** in BACKLOG se diventa rilevante.

**Side-action**: refresh `opencode.json` rimuovendo `groq/qwen-2.5-coder-32b` (deprecated).

## Riferimenti

- ADR-0022 (Accepted 2026-05-09): OpenCode tool-use model routing
- BACKLOG M10
- `scripts/bench-opencode-cloud-free.ps1` (5-test matrix runner, riusabile per future re-bench)
- `~/.config/opencode/opencode.json` (config provider OpenCode -- refresh post side-finding T3)

## Riferimenti

- ADR-0022 (Accepted 2026-05-09): OpenCode tool-use model routing
- BACKLOG M10
- `scripts/bench-opencode-cloud-free.ps1`
- JSON output: `logs/bench-opencode-cloud-free-YYYY-MM-DD-HHMM.json`
