# Runbook -- Game backend prod restart (Lenovo)

status: ACTIVE
created: 2026-07-02
owner: Eduardo
incident-origine: 2026-07-02 (node nudo -> rollback silenzioso 5 flag live + persistence stub)

## Topologia (dove vive il prod)

Il backend Evo-Tactics "prod" su Lenovo NON gira dal clone `C:\dev\Game`:

| Componente | Valore |
|---|---|
| Worktree prod | `C:\dev\_gamewt-lenovo-host` (task EvoTacticsBackend) |
| Env prod | `.env` DEL WORKTREE (DATABASE_URL -> Postgres portable `pgdata-game`) + keys.env sourced dal launcher |
| Launcher | Scheduled task `EvoTacticsBackend` (killa node rogue sulla porta, sourcia env, avvia) |
| Porte | HTTP `:3334`, WebSocket `:3341` |
| Flag live via launcher | LETHAL / MOVE_TERRAIN / PRESSURE_TIER / INTEROCEPTION / META_NETWORK (+ quelli staged al momento del restart) |

NB: il Postgres su `:5432` e' il pgdata-game del backend (e/o il Game-Database CMS) --
"nessun DATABASE_URL nel clone" NON significa "nessun DB": l'env prod vive fuori repo.

## Procedura restart (unica supportata)

1. **Aggiorna il worktree prod** al commit voluto:
   `git -C C:\dev\_gamewt-lenovo-host fetch origin main` + checkout/reset al tip desiderato.
2. **Se ci sono migration Prisma nuove** (`apps/backend/prisma/migrations/`):
   dal worktree prod, CON l'env prod caricato:
   `npx prisma migrate deploy` poi `npx prisma generate` (da `apps/backend`).
3. **Restart via task** (MAI node a mano):
   `Start-ScheduledTask -TaskName EvoTacticsBackend`
   Il launcher termina eventuali node rogue sulla porta e riavvia con l'env corretto.
4. **Verifica boot log** (il launcher logga; in alternativa health + log del task):
   - `Database URL: [set]` -- se dice `[missing]` o `[prisma] ... stub in memoria` = env NON caricato, STOP.
   - `Prisma hydrate: N rooms` (persistence attiva).
   - `Invoke-WebRequest http://localhost:3334/api/health` -> 200.
   - PID su `:3334` = figlio della catena launcher (non un node lanciato a mano).

## Anti-pattern (vietato)

- **`node apps/backend/index.js` nudo** da qualunque checkout: parte senza keys.env e senza
  l'env del worktree prod -> rollback SILENZIOSO dei flag live + persistence degradata a
  stub in-memory. Il processo sembra sano (health 200, trait caricati) ma serve un gioco diverso.
- **Diagnosi env dal solo repo**: grep di DATABASE_URL/flag dentro `C:\dev\Game` non prova
  nulla sul deployment. Prima di toccare il processo sulla porta: `Get-ScheduledTask
  EvoTacticsBackend` + identificare cwd/catena del PID proprietario.
- **Kill del PID senza passare dal launcher**: se serve fermare, fermare il TASK
  (`Stop-ScheduledTask`), non il processo.

## Check rapido "sto guardando il prod vero?"

```powershell
Get-ScheduledTask -TaskName EvoTacticsBackend | Select TaskName,State
(Get-NetTCPConnection -LocalPort 3334 -State Listen).OwningProcess
# boot log del deployment corrente: cercare 'Database URL: [set]' e 'Prisma hydrate'
```

## Storia

- 2026-07-02: incident node-nudo (hub session) -> ripristino via SPEC-F session (auth Eduardo):
  migrate 0018+0019 applicate, restart via task (flag ripristinati, W6 anchor 1.15 + STAMINA
  flippati live come da staging). Lesson AA01: L-2026-07-042. Memory hub:
  `reference_game_backend_prod_restart`.

## Ref

- `docs/runbook/ssh-inbound-fleet-setup.md` (sibling fleet-ops)
- Game ADR-2026-04-14 game-database topology (scope glossary HTTP :3333)
