---
name: Colyseus deferred post-playtest
description: Co-op stack network — keep ws@8.18.3 native, NO Colyseus migrate. Re-eval gated post TKT-M11B-06 playtest live solo se 4 trigger soglia fire
type: feedback
originSessionId: 93bf5456-ea0f-4116-83fd-b0b7bec8d148
---
Quando user chiede "Colyseus / framework multiplayer adopt?" su Evo-Tactics → verdetto **NO migrate, keep ws@8.18.3 native canonical**.

**Why**:
- Scope mismatch: Colyseus ottimizza tick sync high-freq (action games, MMO). Evo-Tactics = turn-based d20 ≤0.1 Hz, intent FIFO, host-authoritative Jackbox-pattern. Pagare schema-class + room handler overhead per <0.1Hz = over-engineering.
- Sunk cost reale: Phase A merged PR #1680 (2026-04-20) ship 948 LOC + 38+ test verdi (lobbyWebSocket / lobbyRoutes / lobbyPersistence). Reconnect token, host transfer mid-combat (PR #1736 F-1/F-2/F-3), code collision retry, Prisma write-through Opzione C — tutti coperti. Migrate = riscrivere ~1k LOC + porting test, ZERO feature player-visible.
- P5 🟡 → 🟢 def gating = TKT-M11B-06 playtest live userland (4 amici reali phones+TV), NON infra. Anti-pattern Engine LIVE Surface DEAD risolto 8/8: debt residuo è surface, non backend.
- Friction CLAUDE.md: "nuove dipendenze npm/pip → approvazione esplicita" + regola 50 righe + ripple `services/generation/` + `packages/contracts/`. ADR-2026-04-16 aveva già rifiutato Colyseus per Phase A.

**How to apply**: 4 trigger riapertura decisione post-playtest:

| Trigger | Soglia | Action |
|---|---|---|
| State broadcast lag | payload >10KB mobile + frame stutter | Valuta `@colyseus/schema` standalone (NON full framework) per delta sync |
| Stanze concorrenti | >50 simul | Matchmaker Colyseus diventa value-add |
| Host drop UX rotto | 30s grace confonde, serve quorum/voting | Room lifecycle hooks (scrivibile anche ws nativo) |
| Reconnect replay needed | Server replay intent persi | Colyseus presence non risolve auto, app-owned |

Se nessuno fire post-playtest → close decisione "ws native canonical" definitivamente.

**Critical files (referenza)**:
- `apps/backend/services/network/wsSession.js:70` Room class
- `apps/backend/services/network/wsSession.js:236` publishState versionato
- `apps/backend/services/network/wsSession.js:436` LobbyService registry
- `apps/backend/services/network/wsSession.js:679` createWsServer
- `apps/backend/services/network/lobbyPersistence.js` Prisma write-through
- `docs/adr/ADR-2026-04-20-m11-jackbox-phase-a.md` (addendum 2026-04-28 contiene tabella trigger)

**Plan ref**: `~/.claude/plans/che-m-idici-di-swirling-sifakis.md`.

**Anti-pattern**: NON proporre Colyseus migrate spontaneamente in future session. Decisione frozen finché un trigger soglia non fire con evidenza concreta (telemetry / playtest report).
