# dogfood-ui — Flask mini-app per tracking Fase 6 (ADR-0017)

Dashboard web per classificare dogfood delegations, visualizzare stats aggregate, correlare con promptfoo bench.

## Architettura

```
apps/dogfood-ui/
├── app.py                  # Flask main (~180 LOC, routes + API)
├── db.py                   # SQLite schema + CRUD (~80 LOC)
├── langfuse_client.py      # Langfuse REST API client (~50 LOC)
├── stats.py                # Aggregation helpers + promptfoo parser (~130 LOC)
├── requirements.txt
├── templates/
│   ├── base.html           # Layout + nav + flashes
│   ├── index.html          # Dashboard (KPI + breakdown)
│   ├── _entries_table.html # Partial shared
│   ├── entries.html        # List completa
│   ├── new_entry.html      # Form
│   ├── stats.html          # Raw stats JSON
│   └── bench.html          # Promptfoo viewer light
├── static/
│   ├── style.css           # Dark theme minimal
│   └── app.js              # Fetch helpers
├── data/                   # SQLite + runtime state (gitignored)
└── README.md
```

**No framework frontend**: Jinja2 server-side + vanilla JS (pattern copiato da Dafne `dashboard.html`). Zero React/Vue obbligatori.

## Setup

```bash
cd apps/dogfood-ui
python -m venv .venv
.venv\Scripts\activate   # Windows
# OR: source .venv/bin/activate  # Unix
pip install -r requirements.txt
```

## Avvio

```bash
# Dev mode (auto-reload + debug)
FLASK_DEBUG=1 python app.py

# Production mode (no reload)
python app.py
```

Default porta: 8080. Cambia con `PORT=9090 python app.py`.

## Routes

| Path | Method | Descrizione |
|------|--------|-------------|
| `/` | GET | Dashboard (KPI + breakdown + ultime 50 entries) |
| `/entries` | GET | Lista completa entries |
| `/entries/new` | GET/POST | Form nuova entry |
| `/entries/<id>/delete` | POST | Rimuovi entry |
| `/stats` | GET | Stats raw JSON (debug) |
| `/bench` | GET | Promptfoo latest bench results |
| `/dafne` | GET | Dafne swarm live status (proxy :5000, agents + cycles + intervention + drift) |
| `/api/entries` | GET/POST | REST — list/create entries |
| `/api/stats` | GET | REST — stats aggregate |
| `/api/health` | GET | Health check (DB + Langfuse + LiteLLM + Dafne) |
| `/api/dafne/snapshot` | GET | JSON aggregato Dafne (status + swarm + stats + dafne status + proposals) |

## Env vars

| Var | Default | Scopo |
|-----|---------|-------|
| `PORT` | 8080 | Porta HTTP |
| `FLASK_DEBUG` | (unset) | Mode debug + auto-reload |
| `FLASK_SECRET` | dev-only | Session secret (cambia in produzione) |
| `LITELLM_ENDPOINT` | http://localhost:4000 | LiteLLM Proxy URL |
| `LANGFUSE_HOST` | http://localhost:3000 | Langfuse URL |
| `LANGFUSE_PUBLIC_KEY` | — | Per ping + trace lookup (opzionale) |
| `LANGFUSE_SECRET_KEY` | — | Per ping + trace lookup (opzionale) |
| `DAFNE_HOST` | http://localhost:5000 | Dafne swarm API URL (per panel `/dafne`) |

Windows PowerShell (pre-carica da ~/.config/api-keys/keys.env):

```powershell
Get-Content ~/.config/api-keys/keys.env | ForEach-Object {
    if ($_ -match '^([A-Z_]+)=(.+)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}
python app.py
```

## Schema DB

Tabella singola `entries`:

| Colonna | Tipo | Note |
|---------|------|------|
| id | INTEGER PRIMARY KEY | Autoinc |
| created_at | TEXT | ISO UTC timestamp |
| task_description | TEXT | 1 riga |
| classe | TEXT | cosmetic / behavior / strategic |
| stack | TEXT | Vedi `VALID_STACKS` in `app.py` |
| constraint_count | INTEGER | Per ADR-0016 correlation |
| outcome | TEXT | success / partial / reject / safe-fail / hook-block / error |
| retry_count | INTEGER | |
| tokens_sent / tokens_received | INTEGER | |
| cost_usd | REAL | Costi cloud paid |
| commit_hash | TEXT | Short hash collegato |
| note | TEXT | Free-form |
| langfuse_trace_id | TEXT | Linking a Langfuse trace (opzionale) |

Indici su `created_at`, `classe`, `stack`, `outcome`.

Path DB: `apps/dogfood-ui/data/dogfood.sqlite` (gitignored).

## API JSON

### Create entry

```bash
curl -X POST http://localhost:8080/api/entries \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "JSDoc on commit-guard.js",
    "classe": "cosmetic",
    "stack": "7B-local-whole",
    "constraint_count": 1,
    "outcome": "success",
    "retry_count": 0,
    "tokens_sent": 1800,
    "tokens_received": 632,
    "cost_usd": 0,
    "commit_hash": "f087e52",
    "note": "dogfood #1"
  }'
```

### Get stats

```bash
curl http://localhost:8080/api/stats | jq .phase6
```

### Health check

```bash
curl http://localhost:8080/api/health | jq .
```

## Backup DB

```bash
# Windows
copy apps\dogfood-ui\data\dogfood.sqlite backup\dogfood-$(date +%Y%m%d).sqlite

# Unix
cp apps/dogfood-ui/data/dogfood.sqlite backup/dogfood-$(date +%Y%m%d).sqlite
```

## Integrazione con Langfuse (opzionale)

Una volta configurate `LANGFUSE_PUBLIC_KEY` + `LANGFUSE_SECRET_KEY`:

- Dashboard mostra "Langfuse: reachable" in health
- Se fornisci `langfuse_trace_id` in POST /api/entries (o via form `/entries/new`) -> appare colonna "Trace" nelle tabelle con link cliccabile alla UI Langfuse
- URL del link: `${LANGFUSE_HOST}/project/${LANGFUSE_PROJECT_ID}/traces/${trace_id}` quando `LANGFUSE_PROJECT_ID` e' configurato (canonical path Langfuse UI), altrimenti fallback `${LANGFUSE_HOST}/trace/${trace_id}` (best-effort redirect su Langfuse Cloud)
- Auto-pull metadata: se Langfuse e' raggiungibile, l'app fa GET `/api/public/traces/{id}` e auto-popola `tokens_sent`, `tokens_received`, `cost_usd`, `latency_ms` quando l'utente non li ha esplicitati nel POST. Valori espliciti del client NON vengono mai sovrascritti. Su 404 / connection error degrada silente (entry salvata senza enrichment)
- Configurazione: setta `LANGFUSE_PROJECT_ID` (oltre a `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY`/`LANGFUSE_HOST`) nell'env per attivare URL project-scoped e auto-pull

## Test

Smoke test manuale:

```bash
# 1. Start app
python app.py &

# 2. Health check
curl http://localhost:8080/api/health | jq .

# 3. Create test entry
curl -X POST http://localhost:8080/api/entries -H "Content-Type: application/json" -d '{
  "task_description":"smoke test","classe":"cosmetic","stack":"other",
  "outcome":"success"
}'

# 4. Verify
curl http://localhost:8080/api/stats | jq .total

# 5. Check UI
# → http://localhost:8080
```

Test formale pytest da aggiungere in `tests/` in sprint futuri.

## Future extensions

- Auto-import entries da `logs/aider-delegation-YYYY-MM.md` (parser markdown → SQLite)
- CSV/Excel export
- Charts (Chart.js o plotly) per trend temporali
- Filtro + search nella lista entries
- Trigger Aider direttamente dall'UI (POST form → subprocess `aider-refactor`)
- Pull trace metadata da Langfuse quando `langfuse_trace_id` specificato
- Light/dark theme toggle
