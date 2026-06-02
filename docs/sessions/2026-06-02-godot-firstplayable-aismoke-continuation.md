# Continuation handoff — Godot-v2 First-Playable + AI-driven smoke (2026-06-02)

> Status: phase-close. Cold-start continuation doc. Live state lives in memory
> `project_godot_first_playable`; this is the human-readable session recap + next-workstream.

## TL;DR

Goal: bring the Evo-Tactics **Godot-v2** game live end-to-end on real devices --
room-creation a la *Republic of Jungle* (TV host + phone join via room-code) ->
worldgen-seeded world -> first tactical phases. Eduardo's hard constraint:
the QA smoke must be **AI-driven (no human eyes, no Claude in the judging loop)**.

This session: **validated the approach + built & landed the autonomous judge harness.**
The remaining work (scale to all 6 screens + populated-drive) is substantial and
belongs in the Godot-repo workflow. No pivot needed -- the design is empirically proven.

## What is TRUE (ground-truth, this session)

- The Godot-v2 chain is **already assembled** on `origin/main` (`scripts/main.gd`:
  6 phases `lobby -> character_creation -> form_pulse -> world_seed_reveal -> world_setup -> combat`;
  web export forces entry = LOBBY). Bible surfaces shipped (#287-299), co-op "Nido"
  loop shipped (#375-384). It had **never been run live** (smoke checklist 100% blank).
- The whole thing = **validate-not-build**, not build-from-scratch.

## DESIGN LAW (empirically proven this session)

Autonomous smoke = TWO judge channels, merged:
- **vision-LLM** (Gemma-4 / any VLM) for QUALITATIVE/structural items (element present?
  dormant? tofu? aesthetic family).
- **deterministic** (screenshot pixel-sample + Godot `window.__*` bridge) for MEASURABLE
  items (color / brightness / px / count).

**Why deterministic is MANDATORY (3 VLM data points)**: on a lobby bg objectively
`RGB(77,77,77)` = 30% gray, **Gemma-4 said 8% near-black PASS** (twice, incl. strict prompt)
and **Qwen2.5-VL said 5% near-black PASS** (worse). VLMs hallucinate color, model-independent.
Vision is for qualitative only; measurables go to the deterministic layer. Validated by
pixel ground-truth (PIL) + a combined-judge run where the deterministic check OVERRODE the
VLM's false-PASS on the bg.

## What is BUILT + LANDED

- **PR #263** -- `scripts/ai-smoke/` (codemasterdd): `judge_screen.py` with 7 TDD'd
  primitives (`_extract_json`, `_prompt`+`SPECS`, `_is_dark_bg`, `_merge_verdicts`,
  `sample_bg`, `build_judge_payload`, `run`) + `test_judge_screen.py` (7 pytest GREEN via
  `pytest --rootdir .`) + `README.md`. `run()` = DI-injectable combined judge (sampler +
  vision_post), end-to-end orchestration unit-tested without real IO. Real IO (Ollama
  urllib, PIL) proven via inline harness; a `main()` CLI wrapper is the only un-landed glue.
- **PR #262** -- `docs/runbook/godot-v2-first-playable-golive.md` (the AI-driven smoke design + deploy runbook).
- Conditional-loop demonstrated autonomously: `✦` (U+2726) tofu in `LobbyView.tscn` +
  `CompanionPanel.tscn` -> removed -> rebuild -> vision re-smoke confirmed clean
  (judge->fix->verify, no human). Changes live in worktree `C:/dev/Game-Godot-v2-golive` (uncommitted).
- F1 bg-gray root-caused: `Main.tscn` root = Node2D; `_setup_lobby_phase` add_child's the
  LobbyView Control without forcing full-rect -> its dark Background doesn't cover the
  viewport -> gray clear-color shows. Fix = `view.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)`
  after add_child in every `_setup_*_phase` (systemic). CONFIRMED correct, but tdd-gated (GDScript) -> Godot-workflow.
- F2 room-code-not-dominant = DISMISSED bare-boot artifact (`label_hero`=56px confirmed; "—" placeholder renders small).

## RESEARCH conclusion (tech-scout, 2026-06-02)

**No ready-made tool exists for our niche** (autonomous AI-driven visual+functional smoke
of a STOCK-Godot-4.6.2 HTML5 game vs spec, local-LLM, combined det+vision). Verified:
- **PlayGodot** (Randroids-Dojo, 33*, MIT, beta) = strong deterministic Godot driver
  (drive+assert+screenshot+MSE-regression+pytest) BUT requires a **CUSTOM Godot engine fork**
  + **desktop-only** (no HTML5/web) + no-vision -> **NOT adopt**.
- **gdUnit4** = stock Scene Runner drive/assert, but no-screenshot/no-web.
- Vision-QA-vs-spec local = **no framework**; only raw Ollama VLMs -> assemble it (= what we did).
- Agentic-game tools (GamingAgent/VideoGameBench/ScreenAgent/TITAN) = play/control/benchmark, cloud-mostly, NOT spec-QA.
- **Verdict: our custom harness IS the pragmatic best.** No model-swap (Qwen2.5-VL A/B refuted).
- (deep-research workflow's verify-phase is buggy -- all agents failed StructuredOutput -> false "all refuted"; verified directly via WebFetch instead.)

## Env state (Ryzen DESKTOP-T77TMKT)

- Godot 4.6.2 + Web export templates installed (`AppData/Local/Godot/`).
- Postgres-17 service Running; `Game-golive` worktree (`C:/dev/Game-golive` @ Game origin/main)
  boots clean (`npm run start:api` -> HEALTH 200, lobby-WS shared, db `game` migrated 0014-0017).
- Godot worktree `C:/dev/Game-Godot-v2-golive` @ Godot origin/main #385 (+ uncommitted ✦ fixes,
  the blocked `_publish_ai_probe`/probe RED-test in `tests/unit/test_lobby_ai_probe.gd`).
- Playwright + chromium installed in `Game-Godot-v2-golive/tools/playtest/playwright`; web build
  `dist/web`; `serve_local.sh :8060` (KILLED at session close).
- `qwen2.5vl:7b` on local Ryzen Ollama (localhost:11434); `gemma4:latest` on fleet `.10:11434`.

## NEXT WORKSTREAM (validated design, substantial -- Godot-workflow venue)

1. **Populated-drive** (resolves F2 + tests real state): run the full `deploy-quick.sh` flow
   (build mounted into `Game/apps/backend/public/`, served same-origin from Express :3334, so the
   Godot web client's `web_origin_resolver` -> same-origin works) + create a room via the WS
   LobbyService (`lobbyEndToEnd.mjs` pattern) -> real 4-letter room code on the lobby -> re-capture
   -> re-judge. (A bare `:8060` static serve canNOT reach the backend; must be same-origin via deploy-quick.)
2. **Scale to 6 screens**: capture form_pulse / world_seed_reveal / world_setup / combat / debrief.
   Needs phase-entry plumbing (a web `?phase=` URL override in `main.gd`, GDScript -> tdd-gated GUT)
   OR drive lobby->next via the populated flow. Add a `SPECS[screen]` entry per bible screen +
   the measurable-item map (which items are deterministic per screen).
3. **bg-fix F1** + **Godot bridge** `window.__<screen>_state` (the blocked `_publish_ai_probe` /
   `_collect_probe_state`) -- finish GREEN in the Godot-repo workflow where tdd-guard+GUT are wired.
4. **main() CLI** for `judge_screen.py` (thin glue over `run()`).

### Gotchas to budget for

- **GLOBAL tdd-guard is ultra-granular**: every new function = stub -> run -> populate -> impl,
  one test at a time, and it BLOCKS deleting a failing test. Budget many micro-cycles. Pure logic
  is fine; IO/CLI glue (urllib/PIL/argparse) it demands tests for (use dependency injection -> testable).
- **tdd-guard registers RED only via the observed test path**: for Python use `pytest --rootdir .`
  (it sees the RED); for **GUT/GDScript, a headless `godot ... gut_cmdln` bash run from this hub did
  NOT register** -> the bridge/bg GDScript must be done IN the Godot-repo workflow (GUT+tdd-guard wired).
- Game backend boot on Ryzen: Docker broken -> standalone Postgres-17 + `@game/*` Windows junction
  (npm install fixes); see memory `ryzen-game-backend-boot`.

## Refs

- Live state: memory `project_godot_first_playable` (authoritative current state).
- Design/runbook: `docs/runbook/godot-v2-first-playable-golive.md` (PR #262).
- Tool: `scripts/ai-smoke/` (PR #263).
- RoJ design lineage: `Game-Godot-v2/docs/godot-v2/handoff-2026-06-02-republic-of-jungle-screen-ref.md` (#385)
  -> `visual-screen-bible.md` + `design-conformance-gap-2026-05-19.md`.
- Open PRs: #262, #263 (Codex review rate-limited -- Eduardo merge call).
