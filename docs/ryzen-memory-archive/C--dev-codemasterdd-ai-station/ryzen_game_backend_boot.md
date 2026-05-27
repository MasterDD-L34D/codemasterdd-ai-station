---
name: ryzen-game-backend-boot
description: How to boot the Game (C:/dev/Game) backend on Ryzen for calibration/e2e — standalone Postgres + workspace junction fix (Docker is broken)
metadata: 
  node_type: memory
  type: project
  originSessionId: 2fb2d8b0-9096-4bc2-930b-93174bef2d84
---

Booting the Game backend on Ryzen (DESKTOP-T77TMKT) for calibration
(`tools/py/calibrate_parallel.py`) or sistema e2e requires two env fixes
discovered 2026-05-26:

**1. Database — Docker is broken, use standalone PostgreSQL 17.**
- Docker Desktop crashes on this PC (`initializing Inference manager: ...
  dockerInference: The file cannot be accessed`). The repo's `docker-compose`
  (postgres:16) is therefore unusable here.
- Standalone **PostgreSQL 17** installed via `winget install PostgreSQL.PostgreSQL.17`
  (unattended, superpassword `postgres`, port 5432). Service `postgresql-x64-17`.
- DB `game` created. Use `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/game`.
- Apply migrations: `node_modules/.bin/prisma migrate deploy --schema apps/backend/prisma/schema.prisma` (creates all incl. `0011_sistema_state`). `prisma generate` similarly.

**2. `@game/*` workspace links break Windows node.**
- `node_modules/@game/{contracts,ui,backend}` were MSYS-style symlinks: bash
  follows them, but Windows `node.exe` cannot → backend boot dies with
  `Cannot find module '@game/contracts'` (apps/backend/app.js).
- Fix: recreate as **Windows junctions** (PowerShell, from C:/dev/Game):
  `cmd /c rmdir node_modules\@game\contracts` then
  `cmd /c mklink /J node_modules\@game\contracts packages\contracts` (+ `ui`->packages\ui, `backend`->apps\backend).
  `npm install` also fixes them. Verify: `node -e "require.resolve('@game/contracts')"`.

After both, `calibrate_parallel.py --scenario hardcore_06 --n 40` spawns 4 shards
healthy in ~1s and N=40 runs in ~10s.

**Note**: `tools/py/calibrate_parallel.py` self-spawns backend shards (ports
3341-3344, sets `LOBBY_WS_ENABLED=false` per L-071 to avoid the HTTP/WS port
collision). It inherits `DATABASE_URL` from env.

See also [[ryzen-fleet-gotchas]] (if present).
