# infra/ — Observability stack self-hosted

> Docker Compose stack per ADR-0017 (UI + observability). Zero subscription, tutto self-hosted.

## Servizi

| Servizio | Ruolo | Porta | Image |
|----------|-------|------:|-------|
| **LiteLLM Proxy + Admin UI** | Gateway unificato tier 1-4, virtual keys, budget enforcement, spend dashboard | 4000 | `ghcr.io/berriai/litellm:main-latest` |
| **Langfuse web** | Observability + tracing + evals + prompt mgmt | 3000 | `langfuse/langfuse:latest` |
| **Postgres** | DB Langfuse (traces + users + projects) | 5432 (internal) | `postgres:15-alpine` |

## Quickstart

### 1. Prima esecuzione — inizializzazione secrets

```bash
cd infra/langfuse
cp .env.example .env
# Genera NEXTAUTH_SECRET e SALT (32 chars random)
openssl rand -base64 32  # → incolla in NEXTAUTH_SECRET
openssl rand -base64 32  # → incolla in SALT
```

### 2. Avvia lo stack

```bash
# Da infra/
docker compose up -d

# Primo avvio: ~60s per postgres ready + langfuse migrations
# Check logs
docker compose logs -f langfuse
```

### 3. Prima configurazione Langfuse (automatica, zero browser)

Al primo avvio, `LANGFUSE_INIT_*` env variables **auto-seedano**:
- Organizzazione "CodeMasterDD"
- Progetto "fase6-dogfood"
- User admin (`admin@codemasterdd.local` / `changeme-8char-min`)
- API key pair (`pk-lf-codemasterdd-local` / `sk-lf-codemasterdd-local-change-me`)

Le stesse keys sono passate automaticamente a LiteLLM callback via env expansion nel docker-compose.

**Verifica funzioni**:
```bash
# Chat completion via LiteLLM → trace automatica in Langfuse
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-local-masterkey-change-me" \
  -H "Content-Type: application/json" \
  -d '{"model":"ollama-cosmetic-7b","messages":[{"role":"user","content":"Test"}]}'

# Check DB trace count (dovrebbe incrementare)
docker exec codemasterdd-postgres psql -U langfuse -d langfuse -c "SELECT COUNT(*) FROM traces;"

# Browse UI (login con credenziali sopra)
# http://localhost:3000
```

### 4. Opzionale: rotate secrets per deployment multi-user

Se devi cambiare le keys di default (es. condividi macchina):
1. Edit `.env` con nuovi valori per `LANGFUSE_INIT_PUBLIC_KEY` + `LANGFUSE_INIT_SECRET_KEY`
2. **ATTENZIONE**: per re-seeding, serve reset DB: `docker compose down -v && docker compose up -d`
3. Altrimenti le keys vecchie restano in DB (seed avviene solo primo up)

### 5. Verifica end-to-end

```bash
# Test chiamata via LiteLLM Proxy
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-local-testkey" \
  -d '{
    "model": "ollama-cosmetic-7b",
    "messages": [{"role": "user", "content": "say hello"}]
  }'

# Check trace in Langfuse UI: http://localhost:3000 → Traces
```

### 6. Aggiorna Aider per usare endpoint unificato

```yaml
# ~/.aider.conf.yml — aggiungi override per LiteLLM Proxy
openai-api-base: http://localhost:4000
openai-api-key: sk-local-testkey  # virtual key, non real key
```

I wrapper `aider-cosmetic.cmd`, `aider-refactor.cmd`, etc. continuano a funzionare; ora routano via LiteLLM Proxy invece che direttamente a Ollama/cloud.

## Virtual keys configurate

Vedi `litellm/config.yaml` per lista completa. Mapping tier:

| Virtual key | Provider | Modello | Budget/mo |
|-------------|----------|---------|----------:|
| `ollama-cosmetic-7b` | Ollama | qwen2.5-coder:7b | $0 |
| `ollama-refactor-14b-q2` | Ollama | qwen2.5-coder:14b-instruct-q2_K | $0 |
| `ollama-refactor-30b-moe` | Ollama | qwen3-coder:30b | $0 |
| `ollama-reasoning-r1-8b` | Ollama | deepseek-r1:8b | $0 |
| `ollama-multimodal` | Ollama | gemma4:latest | $0 |
| `groq-70b` | Groq | llama-3.3-70b-versatile | $5 cap |
| `cerebras-8b` | Cerebras | llama3.1-8b | $5 cap |
| `gemini-flash` | Gemini | gemini-2.5-flash | $5 cap |
| `openai-4o-mini` | OpenAI | gpt-4o-mini | $10 cap |

## Stop / restart / update

```bash
docker compose down           # stop (preserva volumi)
docker compose down -v        # stop + rimuovi volumi (RESET Langfuse DB)
docker compose pull           # aggiorna immagini
docker compose up -d          # riavvia
```

## Troubleshooting

### Langfuse non parte al primo avvio

Cause comuni:
- Postgres non ready: aumenta healthcheck timeout in `docker-compose.yml`
- NEXTAUTH_SECRET missing: genera con `openssl rand -base64 32`
- Porta 3000 già occupata (Grafana? Open WebUI?): cambia port mapping

### LiteLLM non trova Ollama

Su Windows, `localhost` dentro container != localhost host. Usa `host.docker.internal`:

```yaml
# litellm/config.yaml
model_list:
  - model_name: ollama-cosmetic-7b
    litellm_params:
      model: ollama/qwen2.5-coder:7b
      api_base: http://host.docker.internal:11434
```

(Già configurato in template, vedi `litellm/config.yaml`.)

### Cloud API keys non si caricano

Verifica:
1. `~/.config/api-keys/keys.env` esiste e ha permessi `CODEMASTERDD\edusc:(F)` only
2. `infra/litellm/.env` riferisce correttamente le keys (format `GROQ_API_KEY=$GROQ_API_KEY` OR hardcode per test)
3. Se usi Tavily in agent workflow, esporta anche `TAVILY_API_KEY` (il compose la propaga al container LiteLLM per tooling custom)

### Stack consuma troppa RAM

Langfuse + postgres baseline ~1.2GB. LiteLLM ~200MB. Totale ~1.5GB su 64GB = trascurabile.
Se altro processo ha saturato RAM: `docker stats` per check.

## Backup / ripristino

### Backup Langfuse DB

```bash
docker compose exec langfuse-db pg_dump -U langfuse langfuse > backup-langfuse-$(date +%Y%m%d).sql
```

### Restore

```bash
docker compose exec -T langfuse-db psql -U langfuse langfuse < backup-langfuse-YYYYMMDD.sql
```

## Riferimenti

- [ADR-0017 UI + observability stack](../docs/adr/0017-ui-observability-stack.md) — decisione architetturale
- [LiteLLM docs](https://docs.litellm.ai/docs/proxy/quick_start)
- [Langfuse self-hosting](https://langfuse.com/self-hosting/local)
- [ADR-0013 Tier 3 cloud free providers](../docs/adr/0013-tier3-cloud-free-providers.md) — API keys policy
