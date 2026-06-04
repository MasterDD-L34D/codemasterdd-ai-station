---
name: Sprint M11 Phase A — Jackbox WebSocket backend
description: PR #1680 merged 2026-04-20 — network beachhead P5 via ws@8.18.3, 4-letter room code, host-auth. Phase B frontend pending next session.
type: project
originSessionId: 3880055e-0f74-4d03-8695-011125e6f2c9
---
# Sprint M11 Phase A — Jackbox co-op WebSocket backend

**Data**: 2026-04-20
**PR**: [#1680](https://github.com/MasterDD-L34D/Game/pull/1680) merged `db4325f0`
**Branch**: `feat/m11-jackbox-coop` → main
**Sequenza session**: C ✅ (onboarding 60s) → B ✅ (meta Prisma) → A ✅ (M11 Jackbox)

## Cosa è stato shipped

- `apps/backend/services/network/wsSession.js` (~355 LOC): `LobbyService` Map-backed registry + `Room` class (host-auth, intent relay, reconnect via stable token, 30s heartbeat) + `createWsServer` factory (attach server o standalone port)
- `apps/backend/routes/lobby.js` (~95 LOC): POST `/api/lobby/{create,join,close}` + GET `/api/lobby/{state,list}`
- `apps/backend/app.js`: lobby service istanziato in `createApp()`, esposto nel return tuple
- `apps/backend/index.js`: WS bootstrap su porta **3341** (env `LOBBY_WS_PORT`, disable via `LOBBY_WS_ENABLED=false`), shutdown pulito via `shutdown(signal)`
- ADR `docs/adr/ADR-2026-04-20-m11-jackbox-phase-a.md` — Accepted
- Tests: 15/15 verdi (9 REST `lobbyRoutes.test.js` + 6 WS integration `lobbyWebSocket.test.js`)

**Key decisions**:

- **Zero nuove deps**: `ws@8.18.3` era già in node_modules. Niente Colyseus nuovo — resta tier-2 fallback.
- **4-letter code**: alfabeto 20 consonanti `BCDFGHJKLMNPQRSTVWXZ` — no vocali → no parole reali/obscenity. Spazio 160k, retry collisione 20×.
- **Host-authoritative**: solo `player_id == room.hostId` può `publishState`. Non-host `state` → error `not_host`. Intent relayed al solo host (non broadcast peers) per privacy Jackbox-pattern.
- **Reconnect**: stable token (HEX 16-byte) riusabile. `attachSocket` chiude socket precedente con close code `4000 superseded`.
- **Port 3341**: isolato da HTTP 3334, Vite 5180, calibration 3340 (vincolo prompt user).

## Baseline regression

- AI: 307/307 verde
- API: 299/299 verde (+15 nuovi = 314 post)
- Format: `npx prettier --check` verde
- Governance docs: `errors=0` (4 warning preesistenti unrelated)

## Fuori scope Phase A → Phase B next session (~8-10h)

1. Frontend lobby picker: `apps/play/src/lobby.html` + chiamata POST `/api/lobby/create`/join
2. TV dual-view: shared spectator (room state overview) vs phone-private (own player actions)
3. Client reconnect logic `apps/play/src/network.js`: backoff, token replay, state version reconciliation
4. Campaign-state live mirror via WS `state` channel — link a campaign engine M10
5. (opzionale Phase C) Prisma persistence adapter per room survival restart backend
6. (deferred Phase D) Rate-limit + DoS hardening se produzione pubblica

## Protocollo WS canonical

```json
S→C: { "type": "hello", "payload": { "role", "player_id", "name", "room", "state", "state_version" } }
S→C: { "type": "player_joined" | "player_connected" | "player_disconnected", "payload": { ... } }
C→S (host): { "type": "state", "payload": <arbitrary> }
S→C: { "type": "state", "version": N, "payload": <arbitrary> }
C→S (non-host): { "type": "intent", "payload": <arbitrary> }
S→C (host only): { "type": "intent", "payload": { "id", "from", "payload", "ts" } }
C↔S: { "type": "chat", "payload": { "from", "name", "text", "ts" } }
C↔S: { "type": "ping" | "pong", "payload": { "t" } }
S→C: { "type": "error", "payload": { "code", "message" } }
S→C: { "type": "room_closed", "payload": { "reason" } }
```

Connection URL: `ws://host:3341/ws?code=ABCD&player_id=p_xxx&token=YYY`

## Status Pilastri post-M11 Phase A

| # | Pilastro | Pre | Post | Note |
|---|----------|:---:|:----:|------|
| 1 | Tattica leggibile | 🟢 | 🟢 | — |
| 2 | Evoluzione emergente | 🟡 | 🟡 | Runtime Prisma live (L06), PI pack spender pending M10 |
| 3 | Identità Specie × Job | 🟡 | 🟡 | Level curves pending M9 |
| 4 | Temperamenti MBTI/Ennea | 🟡 | 🟡 | 3 axes partial pending M9 |
| 5 | Co-op vs Sistema | 🟡 | 🟡 (Phase A live) | Phase B chiude → 🟢 |
| 6 | Fairness | 🟡 | 🟡 | Hardcore deadlock pending M9 |

**Progress**: 1/6 🟢 → 1/6 🟢 + Phase A marker. Phase B chiude P5.
