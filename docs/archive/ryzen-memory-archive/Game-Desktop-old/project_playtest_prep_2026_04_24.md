---
name: Playtest Prep + Live Smoke — 2026-04-24
description: Sessione prep playtest live. 4 PR mergiati main (#1727/#1728/#1729/#1730). Bugs runtime fix (V5 pool + launcher UX + coop hint dismiss + layout ultrawide + runtime-config WS). Playtest live interrotto per fix-round.
type: project
originSessionId: 118180d8-239a-4fa3-8df3-f69b810d1eca
---
# Playtest Prep + Live Smoke — 2026-04-24

## PR shipped main

| PR | Scope | Commit | Merged |
| --- | --- | --- | :-: |
| [#1727](https://github.com/MasterDD-L34D/Game/pull/1727) | V5 SG runtime wire abilityExecutor + UI rewards/packs | `b9a6dc73` | ✅ |
| [#1728](https://github.com/MasterDD-L34D/Game/pull/1728) | Bug critico publicSessionView: V5 pool sovrascritto da legacy stress gauge. Fix + rename legacy → `stress_gauge` + CSS cc-preview-packs | `0df68899` | ✅ |
| [#1729](https://github.com/MasterDD-L34D/Game/pull/1729) | Launcher UX rewrite (preflight + health probe + auto-open + QR + clipboard) | `a5d18248` | ✅ |
| [#1730](https://github.com/MasterDD-L34D/Game/pull/1730) | Fix playtest smoke: coop share hint dismiss + layout ultrawide + runtime-config.js fallback | `168a8d0d` | ✅ |

## Root cause bugs critici playtest

### Bug A — `publicSessionView` collision V5 pool vs legacy

`apps/backend/routes/sessionHelpers.js:221` spread preservava `u.sg` V5 (integer 0..3), linea successiva sovrascriveva `sg: Math.floor(stress*100)` → V5 pool mai esposto al client. Fix: preserve V5 + rename legacy → `stress_gauge`.

### Bug B — Launcher UX cryptic errors

Pre-PR #1729 launcher lanciava backend+ngrok senza preflight. Utente confuso su errori (port busy, ngrok authtoken missing, dist stale). Rewrite: 5 preflight check con ✓/✗ + fix hint + health probe `/api/health` + auto-open browser + clipboard copy URL + ANSI colorato banner.

### Bug C — Share hint dismiss race

`renderHostShareHint` visibile a `if (bridge.isHost)` dentro bridge init. Hint rendered BEFORE hello event con roster players. Dismiss solo su `player_joined` event → se player già in room al load, hint persiste. Fix multi-layer:
- `updateHostRoster` controlla roster, dismiss se hasOtherPlayer
- `client.on('player_connected')` aggiunto dismiss trigger
- `renderHostShareHint` self-poll setInterval 1s ispeziona DOM `li .role:not(.host)` → fallback robusto

### Bug D — Layout ultrawide 3436×1265

`fitCanvas` CELL cap 96 era TV-safe ma canvas minuscolo su desktop ultrawide. Cap alzato 96→160. `main` grid-template-columns 1fr 300px → 1fr 360px + `min-height: 0` + `.board justify-content: center`.

### Bug E — runtime-config.js missing → WS break via ngrok

`apps/play/index.html` carica `<script src="runtime-config.js" onerror="void 0">` che setta `window.LOBBY_WS_SAME_ORIGIN=true`. Backend intercepta `/play/runtime-config.js` dinamicamente basato su `LOBBY_WS_SHARED` env, MA `apps/play/public/runtime-config.js` file statico missing → fallback Vite dev server rompeva. Creato file statico `public/runtime-config.js` default `true`.

## Playtest flow smoke stato

- **Launcher OK** (preflight 5/5, health probe, tunnel, browser auto-open, clipboard)
- **Host browser UI**: layout funzionava (pre-fix CELL cap compresso UI top)
- **Share hint**: persistente pre-fix (race dismiss), dopo fix self-poll dovrebbe risolvere
- **Char creation overlay player side**: da verificare dopo fix runtime-config.js (WS ora connette via ngrok)
- **Narrative log**: terse format existing (`SIS · unit: attack → target (dmg)`). Prosa narrative = feature M18+ non implementata

## Residuo userland

- **TKT-M11B-06**: playtest live 4p ngrok effettivo (non automatizzabile)
- **Narrative log prose** feature: implementare modulo narrativeComposer.js

## Lessons

- **Ngrok single-tunnel richiede LOBBY_WS_SAME_ORIGIN=true** nel client per WS su `/ws` path stesso origin. Backend serve dynamic `/play/runtime-config.js` ma file statico fallback indispensabile per coverage edge case (Vite dev, altri host).
- **Race event-driven dismiss**: setInterval self-poll 1s è salvagente robusto rispetto a listener multipli su eventi WS che possono arrivare fuori ordine o essere missing.
- **Playtest audit 3-browser reale** rivela bug non visibili in unit test (smoke fra client-client via backend reale).
