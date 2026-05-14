# Cross-repo Dashboard v0.2 — Full Integration

Component 1 per spec V4 2026-05-14. Read-active aggregator + workflow integration + production-ready.

## Quick start (3 modes)

### Mode 1: Dev (Werkzeug, ad-hoc test)
```powershell
cd C:\dev\codemasterdd-ai-station\apps\cross-repo-dashboard
pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:8081/
```

### Mode 2: Production (waitress, daily use)
```powershell
python app.py --prod
```

### Mode 3: System tray (windowless, autostart-able)
```powershell
pythonw tray.pyw
# Icon appears in system tray. Right-click for menu.
```

## Install desktop integration

```powershell
# Desktop icon + system tray autostart on login (recommended)
.\install-shortcut.ps1 -Desktop -Tray

# Or simple autostart (no tray, just Flask + browser)
.\install-shortcut.ps1 -Desktop -Autostart

# Uninstall
.\install-shortcut.ps1 -Uninstall
```

## Pre-requisiti

- Python 3.10+
- `gh` CLI installato + autenticato (`gh auth status`)
- VS Code installed con `code` CLI nel PATH (per B3 "Open in VS Code" button)
- Accesso ai 5 repo

## Features v0.2

### Data sources
- 5 git repo: PR open + last commit + local divergence vs origin
- 3 healthcheck: Flask dogfood-ui:8080 + Dafne:5000 + Ollama:11434
- Gate E counter (Component 1 build trigger cumulative + current month)
- ADR ratification countdown (next 5 ADR pending)
- OPEN_DECISIONS active count + entries
- Local git divergence ↑↓ per repo

### Workflow actions
- "Log coord event" button → `coord-event-log.ps1 -Quiet` POST API
- "Draft cross-repo PR" modal → `dry-run-pr.ps1` POST API (4 fields: repo / type / files / summary)
- "VS Code" link per repo (Open path in editor)
- "GitHub" link per repo
- Click PR # to open in browser

### UX
- GitHub dark theme card layout
- Auto-refresh every 5min (matches cache TTL)
- Force refresh `?refresh=1` button
- ESC key closes modals
- Dormant repos visually faded
- Stale source indicator

## Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | HTML dashboard (summary view) |
| `/?refresh=1` | GET | Force refresh cache |
| `/api/state` | GET | JSON dump complete state |
| `/api/state?refresh=1` | GET | JSON force refresh |
| `/api/coord-event` | POST `{"notes":"..."}` | Invoke `coord-event-log.ps1 -Quiet -NotesQuick` |
| `/api/draft-pr` | POST `{"repo_target","type","preview_files","summary"}` | Invoke `dry-run-pr.ps1` |
| `/api/open-vscode?path=...` | GET | Launch VS Code at whitelisted path |
| `/health` | GET | `{"status":"ok","version":"0.2.0-full-integration"}` |

## Architecture v0.2

```
[gh REST API] ─────┐
[3 healthcheck endpoints] ─┤
[git CLI local 5 repo] ────┼─> [Flask app + in-memory cache] ──> [HTML + JSON]
[logs/coord-events-*.md] ─┤        │
[logs/escalation-gates-*] │        ├── POST /api/coord-event → coord-event-log.ps1
[docs/adr/*.md] ──────────┤        ├── POST /api/draft-pr → dry-run-pr.ps1
[OPEN_DECISIONS.md] ──────┘        └── GET /api/open-vscode → code CLI launch
```

Cache TTL 5min in-memory dict. NO SQLite (defer to v1.x if needed).

## Troubleshooting

**Port 8081 already in use**: zombie processes from prior runs hold the port.
```powershell
Get-NetTCPConnection -LocalPort 8081 -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

**gh CLI not found**: `winget install GitHub.cli` + `gh auth login`.

**VS Code button does nothing**: ensure `code` CLI in PATH (VS Code Command Palette → "Shell Command: Install 'code' command in PATH").

**Tray icon doesn't appear**: pystray needs admin rights on some Windows configs. Try regular `python tray.pyw` (not pythonw) to see error output.

## Iteration plan (post v0.2 daily-use feedback)

- v0.3: filter / search box repos
- v0.4: PR velocity chart (commits/week timeline)
- v1.0: Tailscale LAN exposure for Ryzen access
- Future: post-Gate-E decision → consult `docs/research/component-1-design-options-archived-2026-05-13.md` for SQLite + cron + scaling decisions
