# AI-Driven Smoke -- Vision-Judge layer

Autonomous QA of the Evo-Tactics Godot-v2 web screens against
`visual-screen-bible.md`. **No human eyes, no Claude in the judging loop** --
the judgment is produced by a local sovereign model + deterministic pixel logic.

## Design (evidence-proven, not assumed)

Two judge channels, merged:

| Item kind | Channel | Why |
|-----------|---------|-----|
| qualitative / structural (element present? dormant-looking? tofu? aesthetic family) | **vision-LLM** (Gemma-4, fleet Ollama `.10`) | reliable here |
| measurable (color / brightness / px / count) | **deterministic** (screenshot pixel-sample + Godot `window.__*` bridge) | vision **HALLUCINATES** values |

**Hard evidence for the split**: on a lobby background that is objectively
`RGB(77,77,77)` (30% gray), Gemma-4 reported *"near-black, 8% brightness, PASS"*
-- TWICE, including under a strict prompt that explicitly defined medium-gray as
a FAIL. Prompt-tuning did NOT fix it. So measurable items MUST be judged
deterministically; the model is for qualitative judgment only.

## Primitives (`judge_screen.py`, all TDD'd -- 4 pytest GREEN)

- `_prompt(screen)` + `SPECS` -- build the per-screen bible prompt.
- `_extract_json(text)` -- pull the JSON verdict array out of the model's free-form reply.
- `_is_dark_bg(rgbs, threshold=40)` -- deterministic bg-darkness from sampled pixel RGB.
- `_merge_verdicts(vision, det)` -- deterministic results WIN for measurable items; vision kept for the rest; each row tagged `source`.

## Flow

```
Playwright screenshot
  ├─ vision:        _prompt -> POST .10:11434/api/generate (gemma4) -> _extract_json
  └─ deterministic: PIL pixel-sample (corners) -> _is_dark_bg
                          \-> _merge_verdicts (deterministic overrides measurable) -> per-item PASS/FAIL
```

## Run

Tests: `python -m pytest scripts/ai-smoke/test_judge_screen.py --rootdir . -q`
(the `--rootdir .` form registers RED runs for tdd-guard).

The end-to-end combined judge currently runs via an inline harness (see session
notes); wiring `sample_bg()` + `judge()` (Ollama) + a `main()` CLI into the
module is tdd-gated glue follow-up.

## Status

- Core 4 primitives TDD'd GREEN; combined runner (vision + deterministic merge) proven end-to-end.
- Build-out: module CLI glue; scale to the 6 bible screens; calibrate thresholds;
  Godot `window.__<screen>_state` bridge for non-color measurables (font px, counts).

Refs: runbook `docs/runbook/godot-v2-first-playable-golive.md` sec 5; memory
`project_godot_first_playable`.
