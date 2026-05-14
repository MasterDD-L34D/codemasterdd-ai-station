# Cross-repo Dashboard MVP

Component 1 MVP per spec V4 2026-05-14. Read-active aggregator per 5 git repos monitored.

## Quick start

```powershell
# Setup venv (one-shot)
cd C:\dev\codemasterdd-ai-station\apps\cross-repo-dashboard
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run
python app.py
```

Apri browser: <http://127.0.0.1:8081/>

## Pre-requisiti

- Python 3.10+
- `gh` CLI installato + autenticato (`gh auth status`)
- Accesso ai 5 repo: Game / Game-Godot-v2 / evo-swarm (Dafne) / vault / synesthesia

## Endpoint

- `/` — HTML summary 5 repo cards
- `/?refresh=1` — Force refresh cache
- `/api/state` — JSON dump complete
- `/api/state?refresh=1` — JSON con force refresh
- `/health` — Healthcheck `{"status": "ok", ...}`

## Scope MVP (5gg pre-Max window 2026-05-14 → 5-19)

### IN scope
- 5 git repo: Game / Godot-v2 / Dafne / vault / Synesthesia
- gh API: PR list state=open + commits recent
- In-memory cache TTL 5 min
- Manual refresh button + auto-refresh-on-stale
- Privacy/dormant/error badges
- Drill-down PR list (collapsible)

### NOT in scope MVP (post-MVP iteration)
- Healthcheck endpoints (Flask/Dafne/Ollama) — v1.1
- Git log local divergence — v1.1
- Memory MEMORY.md aggregation — v1.2
- AA01 filesystem read — v1.2
- SQLite persistent cache — v1.1 if needed
- Cron auto-refresh schtask — v1.1
- Authentication — never (localhost only)

## Architecture

```
[gh CLI] -> [Flask app.py] -> [in-memory dict cache] -> [Jinja2 templates] -> [browser]
```

Cache TTL 5 min auto-stale. Force refresh via query param `?refresh=1`.

## Troubleshooting

**gh CLI not found**: install via `winget install GitHub.cli` then `gh auth login`.

**Port 8081 busy**: change in `app.py` last line `app.run(port=8081)`.

**Repo access denied**: verify `gh auth status` + `gh repo view MasterDD-L34D/Game` works manually.

## Iteration plan

Post-MVP feedback Eduardo daily-use → v1.1 (healthcheck + git log + cron) → v1.2 (memory + AA01) → v2 (post-Gate-E full scope).
