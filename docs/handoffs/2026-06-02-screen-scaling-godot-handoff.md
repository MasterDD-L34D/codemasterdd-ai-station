# Handoff -- AI-smoke screen scaling, Godot-ROOTED next session (2026-06-02 e)

> Turnkey continuation for the GDScript-heavy remainder. **Open Claude Code rooted in
> `C:/dev/Game-Godot-v2-golive`** (NOT codemasterdd) -- that repo's own `.claude` has
> worktree-guard + gdlint + GUT and NO tdd-guard, so `.gd` edits flow + GUT does RED/GREEN.
> From codemasterdd the project tdd-guard scope-leaks onto `.gd` and the auto-mode classifier
> blocks repeated temp-disables (per-disable consent). Live state of record: memory
> `project_godot_first_playable`.

## Where things are (ground-truth, verify first per anti-#19)

- Godot worktree `C:/dev/Game-Godot-v2-golive`, branch **`claude/screen1-green-aismoke`** (PR #386)
  -- all the WIP is here (committed): clear-color fix, lobby bridge, `?phase=` enabler
  (`AiSmokePhaseOverride`), form_pulse tofu fix, generic capture spec.
- Game backend worktree `C:/dev/Game-golive` @ origin/main, boots clean
  (`LOBBY_WS_SHARED=true PORT=3334 npm run start:api` -> HEALTH 200; Postgres-17 running;
  recipe = memory `ryzen-game-backend-boot`).
- Judge CLI on codemasterdd PR #263 branch `claude/ai-smoke-vision-judge`
  (`scripts/ai-smoke/judge_screen.py`, SPECS for 5 screens). Run it from there, OR
  `git show claude/ai-smoke-vision-judge:scripts/ai-smoke/judge_screen.py > /tmp/j.py`.
- Godot bin: `/c/Users/VGit/AppData/Local/Godot/godot.cmd` (bash needs the `.cmd`, not `godot`).

## Smoke status: 5/7 covered, 2 GREEN

| # | screen | status |
|---|--------|--------|
| 1 | lobby | GREEN 6/6 |
| 2 | form_pulse | GREEN 6/6 |
| 3 | world_seed_reveal | 4/6 soft-green (0 FAIL, 2 CONDITIONAL) |
| 4 | world_setup | 5/6 -- item6 FAIL = raw-key leak (FIX BELOW) |
| 6 | combat | 5/6 -- item4 bg spec-mismatch + WIP screen |
| 5 | scenario_brief | not covered (not a boot_phase) |
| 7 | debrief | not covered (no boot_phase) |

## The repeatable loop (proven)

1. Build MAIN web: `GODOT_BIN=/c/.../godot.cmd ./tools/web/build_web.sh --mode=main --output-dir=dist/web-main`
2. Mount: `cp -R dist/web-main/. /c/dev/Game-golive/apps/backend/public/`
3. Boot backend (above). Capture: `cd tools/playtest/playwright && PLAYTEST_BASE_URL=http://localhost:3334 PLAYTEST_PHASE=<phase> npx playwright test specs/lobby_populated.spec.ts --project=chromium-desktop` -> `captures/<phase>.png`.
4. Judge: `python scripts/ai-smoke/judge_screen.py --image captures/<phase>.png --screen <phase> --host 192.168.1.10:11434 --model gemma4:latest`.
5. Look at the PNG (vision misses tofu -- eyeball it). Fix at source. Rebuild -> re-capture -> re-judge.

## Next tasks (GDScript -> do them HERE in the Godot session)

### A. world_setup -> GREEN (resolves the smoke's real finding)
1. **Enrich the sample state** in `scripts/ai_smoke_phase_override.gd` `_sample_state()`: add a
   `world` dict so `WorldSetupState.get_biome_id()` is non-empty (kills the `missing_world.biome_id`
   leak; also makes Screen-3 show a real biome). `from_dict` reads `data.get("world", {})`.
   ```gdscript
   "world": {"biome_id": "badlands", "biome_label_it": "Badlands", "pressure": "low", "hazards": []},
   ```
   (valid biome ids in `data/biomes/biomes.json`: abisso_vulcanico, atollo_obsidiana, badlands, ...).
   GUT-TDD it: assert `host._initial_world_state.get_biome_id() != ""` after `apply(host,"world_setup")`.
2. **Remove the tofu**: `scenes/ui/WorldSetupHostView.tscn:129` `text = "✦  Conferma mondo  ✦"` -> `"Conferma mondo"`.
3. Rebuild -> re-capture world_setup + world_seed_reveal -> re-judge -> expect both green.

### B. scenario_brief (5) + debrief (7) -- not boot_phases
- `scenario_brief`: `PHASE_SCENARIO_BRIEF` const exists but `main.gd._ready` has no dispatch + no
  `_setup_scenario_brief_phase`. Check if `scenes/ui/ScenarioBriefView.tscn` exists; if so add a
  setup + a dispatch branch + add to `AiSmokePhaseOverride.WEB_OVERRIDE_PHASES`, seed state. Else
  drive lobby->...->brief via the flow.
- `debrief`: no boot_phase (combat-end sub-state, `DebriefState`). Likely needs a dedicated capture
  hook or flow-drive. Lowest priority.
- Then add `SPECS["scenario_brief"]`/`["debrief"]` (codemasterdd ai-smoke branch, Python, bg=item 4).

### C. (Python, NON-blocked -- can do from codemasterdd) combat bg-check refine
- `run()` hardcodes `det={4}` = corner pixel-sample. Combat has top-bar chrome at the corners (not a
  void) -> false FAIL. Make the deterministic bg sample a per-screen region (e.g. board-center for
  combat) OR drop the void item for combat. TDD in `judge_screen.py`.

### D. systemic tofu kill (optional, beats whack-a-mole)
- `✦` (U+2726) recurs because `resources/themes/cinzel.tres` has no symbol-capable font. Adding a
  fallback font with the glyph would fix ALL `✦` repo-wide (needs a font asset). Else keep removing
  per-`.tscn` (ASCII-first for UI text). Vision will NOT catch tofu -- source-fix is the only reliable path.

## Design laws (proven, do not re-litigate)
- vision-LLM judges QUALITATIVE; deterministic (pixel/bridge) judges MEASURABLE. Vision hallucinates
  COLOR and under-flags TOFU (3 VLM color data points + 3 tofu misses). Raw TEXT leaks ARE vision-catchable.
- bg fix = `project.godot default_clear_color` dark (systemic), NOT a Control mount bug.
- commit policy ADR-0011 (Coding-Agent + Trace-Id trailer, NO Co-Authored-By); commit subject <=72,
  description lowercase-first.
