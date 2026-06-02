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

**Convergence with the recovered RoJ design session (handoff #385, 2026-06-02).** A 2026-05-19
session analyzed the Godot-v2 screens (Playwright screenshots) against the RoJ/Jackbox model
-> produced `docs/godot-v2/design-conformance-gap-2026-05-19.md` (gap report, DRAFT) + baked the
6 RoJ patterns into `docs/godot-v2/visual-screen-bible.md` (A2 visual authority). Its verdict
(Screen-1 Lobby = critical: TV entry `/` 404 + phone zero-theme) was actioned by PR #284 cascade
-- but never verified live. Two independent threads (that 2026-05-19 design analysis + this
2026-06-02 impl-state audit) converge on the SAME move: deploy + smoke on real devices AGAINST
the bible. The device smoke is also the empirical answer to the gap report's never-run
`/ultrareview` (ground-truth on device > re-review of a 2-week-old doc, anti-pattern #8).

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
| Smoke execution | AI-driven harness (Playwright + bridge-state + vision-LLM), NO human -- see sec 5 |

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

## 5. AI-driven smoke (autonomous, NO human eyes) -- the goal gate

Replaces the human iPhone+TV pass. The existing `tools/playtest/playwright/` harness ALREADY
drives + screenshots the Godot web build (`phone_smoke.spec`, `combat_5r.spec`); only the final
visual JUDGMENT was human (README "Analysis pipeline: Master-dd browses report + reviews
screenshots"). Swap that human step for vision-LLM + bridge-state asserts.

**Smoke AGAINST** (3 reference layers): (1) surface grid `qa/2026-05-20-pr284-visual-smoke.md`
(40 items); (2) target spec `visual-screen-bible.md` (A2); (3) known-issue baseline
`design-conformance-gap-2026-05-19.md`. "Feels-like-RoJ" acceptance = 6 bible patterns (2-device,
room-code-dominant + QR + separate join-URL, hand-drawn, one-click join, digestible/accessible,
stream-friendly).

**Why it is non-trivial**: Godot HTML5 = `<canvas>` WebGL -> no inspectable DOM. Two reliable
channels only: screenshots (pixels) + Godot->JS bridge (structured state).

**3-layer autonomous harness**:
1. **Drive** (no human input): backend-script the phases via WS/REST (`tests/e2e/lobbyEndToEnd.mjs`
   pattern: createRoom / joinRoom / publishWorld / advance) + phone join via `?room=` URL (wired) +
   in-canvas coord-clicks (existing harness technique).
2. **Capture**: `page.screenshot()` per phase (visual items) + in-engine
   `get_viewport().get_texture().get_image().save_png()` (sovereign/CI path) + **bridge expose** --
   extend `main.gd` -> `window.__<screen>_state = {room_code, conn_color, theme, font_px, panel_present, ...}`
   (precedent: existing `window.__main_get_telemetry_summary` hook).
3. **Judge** (replaces the human): (a) DETERMINISTIC -- `page.evaluate()` reads bridge state ->
   assert vs bible exact numbers (font px, color, panel-vs-raw-label, StatusLabel player-facing);
   (b) SEMANTIC -- vision-LLM on screenshots vs bible per-screen -> PASS / CONDITIONAL / FAIL +
   reason (dark-void bg, biome-tint, hand-drawn, feels-like-RoJ). Vision model: Gemma-4 multimodal
   local (sovereign $0) first-pass + Claude vision (ADR-0023 budget) for ambiguous/critical.

**Split rule (load-bearing)**: quantitative -> bridge-assert (exact); qualitative/aesthetic ->
vision-LLM. Never ask vision to measure px/hex. Animations (fade/stagger) -> bridge tween-state,
not static screenshot.

**Autonomy boundary (honest)**: render / layout / color / state / flow = 100% AI-driven local
(chromium + native Godot). iOS-Safari-SPECIFIC items (emoji U+25CF fallback, touch-target,
Safari-mobile render) -> Playwright `webkit` approximates; TRUE iOS = cloud device-farm
(BrowserStack). The only residual non-100%-local slice.

Worldgen payoff-legibility -> exercised by the "World Seed Reveal" capture (resonance line, biome
tint, eco_pressure) -- in-play check vs "biodiversita invisibile".

**/ultrareview**: superseded by this autonomous smoke (ground-truth on render > stale-doc review,
anti-#8). Gap report = known-issue baseline only.

## 6. Conditional loop -- Claude (autonomous)

Vision/assert FAIL or CONDITIONAL -> Claude fixes the surface -> re-run the harness (no human) ->
re-judge -> PR. Overlap-check `C:/dev/Game` WIP wound-system (+ Lenovo PHASEC combat) before
touching any combat-code.

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
- RoJ design lineage: `Game-Godot-v2/docs/godot-v2/handoff-2026-06-02-republic-of-jungle-screen-ref.md` (#385, recovered) -> `visual-screen-bible.md` (A2) + `design-conformance-gap-2026-05-19.md` (gap report) + museum card `pr284-bible-conformance-cascade-methodology-2026-05-20.md`
- Backend boot recipe: memory `ryzen-game-backend-boot`
