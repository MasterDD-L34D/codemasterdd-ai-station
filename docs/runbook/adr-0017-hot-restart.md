# Runbook -- ADR-0017 stack hot-restart

> Procedure operative per riavviare lo stack observability self-hosted (LiteLLM + Langfuse + Postgres) dopo periodo di down. Generato da edge case rilevati durante T3 SPRINT_02 pre-validation 2026-05-10.

## Quando usare

- Riavvio stack dopo `docker compose down` (default ADR-0017 scaffold OFF post-uso).
- Cold-start dopo riavvio host Windows / Docker Desktop restart.
- Recovery dopo down >7gg per verifica DB integrity.

## Quickstart

```bash
cd infra
docker compose up -d
# Atteso: ~12-15s per containers started + 2-3s per Langfuse ready
```

Verifica end-to-end:

```bash
# IMPORTANTE: usare 127.0.0.1 esplicito su Windows, NO localhost (vedi Edge case 1)
curl -sf http://127.0.0.1:4000/health/readiness   # LiteLLM 200 OK
curl -sf http://127.0.0.1:3000/api/public/health  # Langfuse 200 OK

# Trace count preserved (postgres volume persists)
docker exec codemasterdd-postgres psql -U langfuse -d langfuse -c "SELECT COUNT(*) FROM traces;"

# Stop quando finito (default scaffold OFF)
cd infra && docker compose down
```

## Edge cases noti

### 1. PowerShell `Invoke-WebRequest` IPv6 quirk (Windows)

**Sintomo**: `Invoke-WebRequest -Uri "http://localhost:4000/health/readiness"` timeout dopo 60+ retry mentre i container sono UP healthy (visibile via `docker ps` + container logs mostrano /health/readiness 200).

**Causa**: PowerShell risolve `localhost` a `::1` (IPv6) prima di `127.0.0.1` (IPv4). Docker Desktop binding `0.0.0.0:4000` + `[::]:4000` espone entrambi, ma il binding IPv6 a volte non risponde immediato post-up.

**Fix**: usare `127.0.0.1` esplicito.

```powershell
# NO
Invoke-WebRequest -Uri "http://localhost:4000/health/readiness"

# YES
Invoke-WebRequest -Uri "http://127.0.0.1:4000/health/readiness"
# o curl bash
curl -sf http://127.0.0.1:4000/health/readiness
```

**Validato**: T3 SPRINT_02 2026-05-10. PowerShell polling 60 retry / 122s tutti fail; curl bash 127.0.0.1 immediato 200 OK.

### 2. LiteLLM richieste health-check da `172.18.0.1` nei logs

**Sintomo**: `docker logs codemasterdd-litellm` mostra ripetuti `GET /health/readiness HTTP/1.1 200 OK` da `172.18.0.1:NNNN`.

**Causa**: Docker internal bridge network health-check polling. **Non sono richieste host-to-container**, sono container-to-container internal (Docker daemon polling). Comportamento atteso, non un sintomo di problema.

**Verifica reale**: usare `curl http://127.0.0.1:4000/health/readiness` da host. Se risponde 200, stack OK.

### 3. Trace count Langfuse: target 7+, atteso preservato

**Sintomo**: dopo restart `SELECT COUNT(*) FROM traces` ritorna numero atteso (es. 38 a 2026-05-10 dopo 13gg+ down).

**Causa**: volume `codemasterdd-postgres-data` persiste su disk. `docker compose down` (no `-v`) NON rimuove volumi.

**Failure mode**: se trace count = 0 dopo restart -> volume corrotto o `docker compose down -v` eseguito accidentalmente. Recovery:
- Backup disponibile: `docker compose exec -T langfuse-db psql -U langfuse langfuse < backup-langfuse-YYYYMMDD.sql`
- No backup: accept loss (scaffold stato), generare addendum ADR-0017 per documentare incident.

### 4. dogfood-ui regression VALID_STACKS desync (FIXED 2026-05-10)

**Sintomo storico**: `POST /api/entries` con `stack: "claude-code-direct"` (o altri stack moderni) ritornava `500 ValueError` dal db layer mentre app-layer validava OK.

**Causa**: `apps/dogfood-ui/db.py:56` aveva set `valid_stacks` outdated dal commit iniziale `6924482` (24/4) con short forms (`7B-local`, `claude`, `openai-mini`). `apps/dogfood-ui/app.py:184-196` `VALID_STACKS` era stato esteso in commit `8c70728` (smoke sovereign) con format-suffix discriminators (`7B-local-whole`, `14B-Q2-local-diff`) + R1/Gemma/Other senza updatare db.py.

**Fix applicato**: commit `8722212` (PR #35) sync db.py valid_stacks verbatim con app.py VALID_STACKS.

**Lesson**: validazione duplicata su layer multipli (Flask app-layer + DB layer) e' fragile -> single source-of-truth raccomandato. Out of scope SPRINT_02 T2 organic: factor `VALID_STACKS` in modulo separato + import in entrambi.

### 5. Field name desync residuo dogfood-ui (KNOWN, deferred)

**Sintomo**: payload API uses `retries`/`tokens_in`/`tokens_out`, db.py uses `retry_count`/`tokens_sent`/`tokens_received`. Functional silent default 0.

**Status**: tracked in PR #35 out-of-scope, deferred a SPRINT_02 T2 organic fix.

## Pattern operativi

### Routine post-restart (~30s)

1. `cd infra && docker compose up -d` (~12s)
2. Verify endpoint via `curl` 127.0.0.1 (NON localhost) (~3s)
3. Verify trace count preserved (~3s)
4. Avvia client se serve (Aider via LiteLLM proxy, dogfood-ui Flask) (~10s)

### Stop pulito

```bash
cd infra && docker compose down
# NON usare -v salvo reset deliberato (perde DB Langfuse)
```

### Recovery DB corrotto

```bash
cd infra
docker compose down
docker volume inspect codemasterdd-postgres-data  # verifica esistenza
docker compose up -d
docker exec codemasterdd-postgres pg_isready -U postgres
docker exec codemasterdd-postgres psql -U langfuse -d langfuse -c "SELECT COUNT(*) FROM traces;"
```

Se 0 trace dopo restart e backup esiste:

```bash
docker compose exec -T langfuse-db psql -U langfuse langfuse < backup/backup-langfuse-YYYYMMDD.sql
```

## Riferimenti

- [ADR-0017 UI + observability stack](../adr/0017-ui-observability-stack.md)
- [infra/README.md](../../infra/README.md) -- quickstart + virtual keys mapping
- [infra/docker-compose.yml](../../infra/docker-compose.yml) -- service definitions
- JOURNAL 2026-05-10 mattina -- T3 SPRINT_02 pre-validation findings
