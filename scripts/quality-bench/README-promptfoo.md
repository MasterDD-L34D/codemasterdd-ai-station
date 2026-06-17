# promptfoo quality bench integration (ADR-0017)

## Perché promptfoo accanto a run-bench.ps1?

Entrambi eseguono HumanEval-style pass@1 su multi-model, ma:

| Feature | `run-bench.ps1` | `promptfoo` |
|---------|:---------------:|:-----------:|
| Test execution Python subprocess | ✅ | ✅ (via custom JS loader) |
| Output JSON | ✅ | ✅ |
| **Web viewer built-in** | ❌ | ✅ :15500 |
| **A/B diff prompt** | ❌ | ✅ |
| **LLM-as-judge** | ❌ | ✅ |
| **CI/CD integration** | manuale | ✅ GitHub Actions native |
| **LiteLLM Proxy routing** | ❌ (direct Ollama/cloud) | ✅ (via OpenAI-compat endpoint) |
| Config complexity | PowerShell script (~250 LOC) | YAML (~80 LOC) + JS loader (~60 LOC) |
| Dipendenze | PowerShell + Python | Node + Python |

**Policy**: **coesistenza dual-track** durante migrazione. `run-bench.ps1` resta come CLI-only / zero-Docker-needed fallback. `promptfoo` è il path primario per review sessions e Langfuse correlation.

## Quickstart

### Prerequisiti

1. Node 24.15.0 ✅ (già installato)
2. Python 3.12 ✅ (già installato)
3. **LiteLLM Proxy UP** (vedi `../../infra/README.md`) — promptfoo chiama `http://localhost:4000`
4. `npm i -g promptfoo` — install globale (una volta)

### Esegui bench

```bash
# Da scripts/quality-bench/
promptfoo eval
# → esegue tutti i problems.json su tutti i provider in config
# → risultati in ./results/promptfoo-latest.json

promptfoo view
# → apre viewer locale http://localhost:15500
# → side-by-side comparison, filters, export CSV
```

### Usare problems-hard.json invece

```bash
PROMPTFOO_PROBLEMS=problems-hard.json promptfoo eval
```

### Sotto-set di provider (es. solo local per validazione offline)

Commenta gli provider cloud in `promptfoo.config.yaml`, oppure:

```bash
promptfoo eval --filter-providers 'ollama-*'
```

### Export per Langfuse dataset

Ogni eval produce file JSON; il custom JS loader preserva `metadata.problem_id` + `metadata.num_tests` che finiscono in Langfuse se LiteLLM Proxy ha callback Langfuse abilitato (già in config).

Workflow: `promptfoo eval` → traces strutturati in Langfuse UI con tag `bench-run-YYYY-MM-DD` → correlation con dogfood entries via shared tag.

## Output interpretation

### pass@1 per provider
Il viewer mostra success rate (green bar) per ogni `ollama-*`, `groq-*`, `cerebras-*`.

### Fail mode breakdown
Il custom assertion script classifica il fail:
- `assert_fail` — output compila ma test assertion fallisce (wrong implementation)
- `syntax_error` / `indentation_error` — output non compila
- `name_error` — indefinito (function signature mancante)
- `type_error` — signature differs from expected
- `runtime_error` — altro crash runtime

Pattern utili:
- Cloud provider che hanno `syntax_error` > 20% → controllare `max_tokens` (probabilmente output truncated)
- Local 7B con `assert_fail` > 50% su problems-hard.json → capability gap (non format issue)
- R1 con `name_error` su semplici → thinking mode non strippato correttamente

## Integrazione dogfood-ui

La mini-app Flask `apps/dogfood-ui/` ha endpoint `/bench/latest` che parsea `results/promptfoo-latest.json` e mostra trend side-by-side con dogfood stack metrics. Vedi `../../apps/dogfood-ui/README.md`.

## Reproducibility (provenance)

Cosa e' pinnato per run riproducibili:
- **Decoding deterministico**: `temperature: 0` + `seed: 42` (entrambi i path: promptfoo
  providers + `run-bench.ps1` Ollama options/cloud payload). Caveat: il seed-passthrough
  promptfoo -> LiteLLM -> Ollama non e' garantito; `run-bench.ps1` lo passa diretto (affidabile).
- **Problem-set versionato**: `problems.json` / `problems-hard.json` sono git-tracked.
  `run-bench.ps1` registra `problems_sha256` nel sidecar provenance (sotto).
- **Provenance sidecar** (`run-bench.ps1`): ogni run scrive `results-<ts>.meta.json` con
  `git_commit` + `problems_file/sha256` + `models` + `ollama_digests` (da `ollama list`) +
  `decoding {temperature, seed, num_ctx, num_predict}`. Ricostruisce l'esatto setup di un run
  storico (bus-factor + N-sample audit, anti lucky-sample).

Cosa NON e' pinnato (gap noto, lightweight-by-design):
- **promptfoo path**: il mapping virtual-key -> modello reale vive in `infra/litellm/config.yaml`
  (LiteLLM proxy), che NON finisce nel provenance sidecar. Per un run pienamente riproducibile e
  auto-documentato usa `run-bench.ps1` (cattura i digest), oppure pinna i tag Ollama in
  `infra/litellm/config.yaml` e annota la sua revisione git.
- Niente DVC/W&B by design: problem-set piccoli + git-tracked, risultati = snapshot datati in
  `results/`. La disciplina (seed + sha + digest) basta; il tooling pesante sarebbe gold-plating (YAGNI).

## Limitazioni note

- **Subprocess Python isolation non completa**: i tests sharing global namespace via import. Per workload untrusted, wrappare in docker-sandbox.
- **Timeout rigido 10s per test**: problemi con recursion profonda (fibonacci(40)) possono falsamente failare. Aumenta in `load-problems.js` se necessario.
- **Promptfoo locale solo**: non usa account cloud, tutto on-disk. `sharing: false` in config preventa export accidentale.

## Troubleshooting

### "ECONNREFUSED 127.0.0.1:4000"
LiteLLM Proxy non UP. Check `docker compose ps` in `infra/`.

### "Model not found: ollama-cosmetic-7b"
Virtual key non in `infra/litellm/config.yaml`. Oppure LiteLLM non ha caricato config (check `docker compose logs litellm`).

### Bench lento (> 10 min per 20 problems × 6 providers)
Normale se Ollama deve caricare modello (30B MoE load ~40s). Accettabile.
Se cloud (Groq/Cerebras) lento → verifica rate limits API.

### Fail parsing custom assertion Python
Il JS loader escapes tests con single-quote. Se problema ha docstring con backtick particolare, potrebbe rompere eval template. In quel caso: sostituisci con assertion `contains-json` standard promptfoo.
