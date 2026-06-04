---
name: Phone smoke 2026-05-08 Day 3/7 friends online retry
description: Iter3 friends-online phone smoke — 4 bug runtime nuovi caught (B-NEW-1→4) Phase A Day 3/7 monitoring impact, Phase B trigger gate moved
type: project
originSessionId: 6f617dd3-2830-4533-b793-3c96cbc7f444
---
# Phone smoke 2026-05-08 Day 3/7 friends online retry

**Sessione 2026-05-08 sera Phase A Day 3/7 monitoring** — prima sessione master-dd phone smoke real con amici online post-Phase-A-LIVE 2026-05-07. **Claude-driven** (Claude lancia stack + monitora + diagnostica live via REST + log tail). 4 bug runtime nuovi caught durante world setup → combat transition. Sessione fermata early su Option B (master-dd verdict: stop, log, ship fix next).

## Bug bundle 4 runtime nuovi

- **B-NEW-1 P0**: world setup tag/Accetto click no-op post 2nd player WS disconnect (vote stuck con state stale UI 2/2 ma backend ground truth 1 player)
- **B-NEW-2 P1**: lobby SFTN auto-close mid-vote 2-player (closed:true + state_version:3 + 2 player record connected:false; grace timer fire o idle timeout?)
- **B-NEW-3 P2**: deep-link `?room=XXXX` non auto-routes a Join (default Create → 3 lobby orfane in <5min)
- **B-NEW-4 P0**: phone exit during combat → return lobby = dead-end no rejoin path (player_token JWT non persisted localStorage; hydrated rooms back-compat #2036 non triggered)

## State backend post-sessione

3 lobby orfane:
- JMMV (REST POST mio, abandoned)
- SFTN (eddy + rufl, **closed:true** mid-vote)
- JFKN (eddy host only post B-NEW-1 stuck)

## Lessons

- **Claude-driven smoke = ~5x speedup vs ship+retest legacy**: Bash bg + Monitor tunnel URL + REST `/api/lobby/list` + backend log tail. Master-dd phone-only, zero terminale userland.
- **Backend log silente lobby events**: ZERO log line per join/vote/close/grace_fire/auto_close. RCA next session bloccato finché si aggiunge structured JSON log su `lobbyService.create/join/vote/close/grace_fire/auto_close`.
- **`jq` mancante MSYS** ma non bloccante (Python json.tool fallback).
- **3 lobby orfane in <5 min** = B-NEW-3 ha effetto cascade. Deep-link DEVE default Join se `?room=` query presente.

## Phase A Day 3/7 monitoring impact

- ❌ ZERO critical bug regression baseline → **violato** (4 nuovi P0/P1)
- ❌ p95 stable → **non capturable** (combat mai entrato)
- ⚠️ WS reconnect <5% → **non capturable** (ma B-NEW-4 dimostra reconnect path rotto cross-device)

**Phase B trigger gate MOVED**: 2026-05-14 → ≥ 2026-05-15+ (1+ day delay per fix bundle ship + retry).

## Resume trigger phrase

> _"resume phone smoke iter3 friends-online RCA, fix B-NEW-1 + B-NEW-4 + retry deploy-quick"_

OR

> _"leggi docs/playtest/2026-05-08-phone-smoke-results-day3-friends.md, ship fix bundle B-NEW + relaunch phone smoke"_

## Priority queue next session

1. B-NEW-4 P0 (phone exit → rejoin via localStorage token) — unblocks any future smoke
2. B-NEW-1 P0 (world vote tag click + 2nd player offline quorum)
3. B-NEW-2 P1 RCA (add log lines + repro)
4. B-NEW-3 P2 fix (deep-link default Join CTA)
5. Retry full smoke 5c + 5d post-fix bundle

**Estimated effort**: ~6-7h next session (3-4h critical + 2h polish + 1h retry).

## Refs

- [docs/playtest/2026-05-08-phone-smoke-results-day3-friends.md](docs/playtest/2026-05-08-phone-smoke-results-day3-friends.md) — full report
- [docs/playtest/2026-05-05-phone-smoke-step-by-step.md](docs/playtest/2026-05-05-phone-smoke-step-by-step.md) — userland playbook canonical
- [Game-Godot-v2 PR #169](https://github.com/MasterDD-L34D/Game-Godot-v2/pull/169) — bundle B1-B4 fix shipped
- [Game/ PR #2053](https://github.com/MasterDD-L34D/Game/pull/2053) — `LOBBY_HOST_TRANSFER_GRACE_MS=90000` + WS publishPhaseChange
