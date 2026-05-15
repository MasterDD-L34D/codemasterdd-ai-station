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
| `FLASK_SECRET` | _required_ | Session secret -- app fa fail-fast se non settata (vedi `.env.example`) |
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

### Pytest suite

```bash
# 1. Install pytest (one-off, already in requirements.txt)
pip install pytest

# 2. Run all tests (18 test cases, ~1s)
cd apps/dogfood-ui
python -m pytest tests/ -v
```

Coverage:

- `tests/test_langfuse_client.py` -> `extract_trace_metadata` shape tolerance (trace-level vs observations[], seconds-to-ms conversion, legacy promptTokens/completionTokens names, zero/empty handling).
- `tests/test_entries.py` -> health endpoint, form + JSON entry creation, validation errors, Langfuse auto-pull (fill / no-override / graceful degradation), project-scoped URL rendering, delete.
- `tests/test_csv_export.py` -> empty DB, headers + filename, CSV escaping (commas / quotes / embedded newlines), Download CSV button presence.

Ogni test usa una SQLite DB isolata in `tmp_path` via fixture `app_factory` (vedi `tests/conftest.py`) -> nessun side effect su `data/dogfood.sqlite`.

## Export CSV

`GET /entries/export.csv` -> download UTF-8 CSV con tutte le entries (limit 10000). Header `Content-Disposition: attachment; filename="dogfood-entries-<ISO-timestamp>.csv"`. Colonne: `id, created_at, task_description, classe, stack, constraint_count, outcome, retry_count, tokens_sent, tokens_received, cost_usd, latency_ms, commit_hash, note, langfuse_trace_id`. Pulsante "Download CSV" nella pagina `/entries`. Compatibile con Excel / LibreOffice / pandas (`pd.read_csv`).

## Trend giornaliero

La pagina `/stats` mostra due sparkline inline SVG (zero JS, zero CDN) sopra la dump JSON: **entries per giorno** + **cost USD per giorno**, raggruppati per data ISO UTC del `created_at`. Renderizzati server-side da `stats.build_sparkline_svg(points)` -> `<polyline>` + area fill scalati al viewBox. Sotto le sparkline c'e' una tabella `<details>` collassabile con i valori giornalieri esatti. Allineato con la postura sovereign-first del progetto: nessun script remoto, accessibile (role="img" + aria-label).

## Future extensions

- Auto-import entries da `logs/aider-delegation-YYYY-MM.md` (parser markdown -> SQLite)
- Excel `.xlsx` export (openpyxl) se l'UTF-8 CSV non basta per workflow downstream
- Filtro + search nella lista entries
- Trigger Aider direttamente dall'UI (POST form → subprocess `aider-refactor`)
- Pull trace metadata da Langfuse quando `langfuse_trace_id` specificato
- Light/dark theme toggle
