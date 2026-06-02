# Godot-v2 First Playable -- Go-Live Runbook

> Status: draft (prereq-gated). Created 2026-06-02 (Ryzen DESKTOP-T77TMKT). Goal owner: Eduardo.
> Scope: bring the ALREADY-ASSEMBLED Godot-v2 chain (lobby -> worldgen -> first
> tactical phases) live end-to-end on real devices (TV + phone), per the
> "TV+phones Jackbox" vision -- room-creation in the style of *Republic of Jungle*
> (host on TV, players join via room code from phone browser).
> Principle: **validate-not-build**. The chain is shipped; it has never been run live.

## 0. Why this exists (ground-truth 2026-06-02)

- Scene chain ASSEMBLED on `origin/main` (`scripts/main.gd`: 6 phases
  `lobby -> character_creation -> form_pulse -> world_seed_reveal -> world_setup -> combat`;
  web export forces entry = LOBBY).
- Bible surfaces shipped to spec (PR #287-299 cascade). Co-op "Nido" session loop
  shipped (#375-384, through 2026-06-01).
- The live-device smoke checklist `docs/godot-v2/qa/2026-05-20-pr284-visual-smoke.md`
  is **100% BLANK** -- the assembled chain has never been run live end-to-end.
- Therefore First-Playable = run that smoke + fix conditionals, NOT build new systems.

## 1. Deploy architecture (verified from deploy-quick.sh)

`Game-Godot-v2/tools/deploy/deploy-quick.sh` does it in one shot:
1. ensure `AUTH_SECRET` in `Game/.env` (auto-generates if missing)
2. build phone HTML5 (`build_web.sh --mode=phone`)
3. build TV HTML5 (`build_web.sh --mode=main`)
4. mount phone build -> `Game/apps/backend/public/phone/`
5. mount TV build -> `Game/apps/backend/public/` root (served at `/`)
6. boot Game Express in `LOBBY_WS_SHARED=true`, single port 3334 (REST + WS + static, same-origin)
7. Cloudflare tunnel: named `evo-tactics.com` if token present, else Quick Tunnel (random URL)

Client side: `scripts/net/web_origin_resolver.gd` reads `window.location.origin` on
web export -> same-origin REST + WS automatically. Phone deep-link `?room=XXXX`
already wired (`read_url_query("room")`). ONE tunnel covers TV + phone + API + WS.

Dependency: `GAME_DIR` defaults to `<godot-repo>/../../../Game` (sibling). The script
boots the GAME (Node) backend -- a current, bootable Game backend is required.

## 2. Prereq status (Ryzen DESKTOP-T77TMKT, 2026-06-02)

| Prereq | State |
|--------|-------|
| Clean Godot checkout | DONE -- worktree `C:/dev/Game-Godot-v2-golive` @ origin/main #384 |
| cloudflared | OK (winget) |
| Named tunnel token | OK -- `~/.cloudflared/evo-tactics-prod.token` -> stable `evo-tactics.com` |
| Godot 4.6 binary | MISSING -- `GODOT_BIN` unset, not in PATH |
| Game backend current | STALE -- `C:/dev/Game` on `feat/od-058-d2-wound-system`, 28 behind, 39 dirty (WIP combat, do NOT disturb) |
| Game backend boot (Ryzen) | FRICTION -- Docker broken -> standalone Postgres 17 + `@game/*` junction fix |
| Physical device smoke | Eduardo only (iPhone + TV) |

## 3. Gaps to clear BEFORE deploy

### Gap 1 -- Godot 4.6 binary
Locate or install Godot 4.6 (stable). `export GODOT_BIN=<path>` (build_web.sh honors it).
Verify: `"$GODOT_BIN" --version`.

### Gap 2 -- clean bootable Game backend @ origin/main
`C:/dev/Game` is a WIP combat branch -- do NOT use/disturb. Create a clean Game
worktree at origin/main, then boot:
- standalone PostgreSQL 17 (`winget install PostgreSQL.PostgreSQL.17`, service
  `postgresql-x64-17`, db `game`), `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/game`
- `prisma migrate deploy --schema apps/backend/prisma/schema.prisma`
- `@game/*` workspace junction fix (or `npm install`); verify `node -e "require.resolve('@game/contracts')"`
- OPEN: verify whether a minimal `lobby -> world -> combat` smoke can boot DB-less
  (Postgres backs Sistema-state / meta-loop; likely required).

Ref: memory `ryzen-game-backend-boot` (7d old -- verify vs current code).

## 4. Execution (post-gap) -- Claude runs

```bash
cd C:/dev/Game-Godot-v2-golive
export GODOT_BIN=<godot4.6>
GAME_DIR=<clean-Game-main> ./tools/deploy/deploy-quick.sh
```
-> TV host: `https://evo-tactics.com/`  |  phone players: `https://evo-tactics.com/phone/?room=XXXX`

## 5. Smoke (Eduardo, physical) -- the goal gate

Open `Game-Godot-v2/docs/godot-v2/qa/2026-05-20-pr284-visual-smoke.md` (40 items,
blank today). On TV `/` + iPhone Safari `/phone/?room=`, mark PASS / CONDITIONAL /
FAIL per surface. Worldgen payoff-legibility is exercised by the "World Seed Reveal"
items (resonance line, biome tint, eco_pressure readouts) -- this is the in-play check
against the "biodiversita invisibile" design risk.

## 6. Conditional loop -- Claude

Fix CONDITIONAL/FAIL surfaces -> PR -> re-smoke. Overlap-check `C:/dev/Game` WIP
wound-system (and Lenovo PHASEC combat work) before touching any combat-code.

## 7. Machine decision (open)

- Ryzen: named-tunnel token here + clean Godot worktree -> natural host. Cost = Godot
  binary + Game-backend boot (Postgres / junction).
- Lenovo: Game backend is the primary current clone, but busy with PHASEC combat +
  named token not present there.

## References

- Deploy: `Game-Godot-v2/tools/deploy/{deploy-quick,named-tunnel,setup-once}.sh`, `tools/web/build_web.sh`
- Smoke checklist: `Game-Godot-v2/docs/godot-v2/qa/2026-05-20-pr284-visual-smoke.md`
- Handoffs: `handoff-pr284-cascade-2026-05-20.md`, `handoff-2026-06-01-species-enrichment.md`
- Vision: codemasterdd `GOALS.md` (TV+phones Jackbox); RoJ reference = jungle.buzz room-code model
- Backend boot recipe: memory `ryzen-game-backend-boot`
