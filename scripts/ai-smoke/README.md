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

## Primitives (`judge_screen.py`, all TDD'd -- 23 pytest GREEN)

- `_prompt(screen)` + `SPECS` -- build the per-screen bible prompt.
- `_extract_json(text)` -- pull the JSON verdict array out of the model's free-form reply.
- `_is_dark_bg(rgbs, threshold=40)` -- deterministic bg-darkness from sampled pixel RGB.
- `_classify_teal_pixel(rgb)` -- is this pixel Ferrospora spore-glow teal (`#3acde5`, the PRIMARY accent)? Excludes gold/bronze + mycelium + void.
- `_is_teal_accent(fraction, min_fraction=0.005)` -- deterministic primary-accent verdict: a parchment-only screen lands ~0 teal -> FAIL.
- `sample_accent(image_path)` -- PIL whole-screen teal-fraction (the deterministic IO behind item 5).
- `_merge_verdicts(vision, det)` -- deterministic results WIN for measurable items; vision kept for the rest; each row tagged `source`.
- `sample_bg(image_path)` -- PIL corner pixel-sample (the deterministic IO).
- `build_judge_payload(b64, screen, model)` -- pure Ollama `/api/generate` request body.
- `_vision_post(image, screen, host, model)` -- real Ollama transport (image -> b64 -> POST -> response text); `urlopen` injectable.
- `run(...)` -- DI-orchestrated combined judge (sampler + vision_post merged).
- `main(argv)` -- CLI wrapper; exits non-zero iff any item FAILs (autonomous-smoke gate).

## Flow

```
Playwright screenshot
  ├─ vision:        _prompt -> POST .10:11434/api/generate (gemma4) -> _extract_json
  └─ deterministic: PIL pixel-sample (corners) -> _is_dark_bg
                          \-> _merge_verdicts (deterministic overrides measurable) -> per-item PASS/FAIL
```

## Run

Smoke a screenshot (autonomous, no human, no Claude):

```
python scripts/ai-smoke/judge_screen.py \
  --image <screenshot.png> --screen lobby \
  --host 192.168.1.10:11434 --model gemma4:latest [--threshold 40]
```

Prints the merged per-item verdict array as JSON; **exits non-zero iff any item
FAILs** (so it gates a CI/loop). `--screen` keys into `SPECS`; `--host`/`--model`
pick the Ollama vision endpoint; `--threshold` is the dark-bg brightness cutoff.

Tests: `python -m pytest scripts/ai-smoke/test_judge_screen.py --rootdir . -q`
**run from the repo root** -- the `tdd-guard-pytest` reporter writes
`.claude/tdd-guard/data/test.json` keyed by rootdir, so the cwd must be the
project root for tdd-guard to observe RED runs (running from `scripts/ai-smoke/`
writes the wrong path and the guard sees a stale pass).

### Verified end-to-end (2026-06-02, real PIL + real Gemma-4 on `.10`)

On the POC lobby PNG: item4 bg = **FAIL `source=deterministic`** (`RGB(77,77,77)`
gray), overriding what every VLM false-PASSes; item6 tofu PASS (the `✦` fixes);
items 2/3/5 vision verdicts; item1 room-code FAIL (= the known bare-boot artifact,
resolved by the populated-drive). Exit code 1. The full loop ran with no human and
no Claude in the judgment.

### Re-baseline 2026-06-03 (S0 -- parchment anti-pattern -> Ferrospora canon)

The judge was certifying the **wrong target**: SPEC item 5 read *"warm
parchment/bronze theme with gold borders = PASS"* -- i.e. it scored the shipped
parchment-fantasy anti-pattern as conformant. Per the canon (vault
`42-STYLE-GUIDE-UI`), **teal spore-glow `#3acde5` is the PRIMARY accent**, gold is
SECONDARY. Item 5 (the 6 theme screens) is flipped to demand the Ferrospora
biopunk skin, and -- because the vision model hallucinates color (the `_is_dark_bg`
lesson) -- the accent verdict is now **deterministic** (`sample_accent` ->
`_is_teal_accent`), wired in `run()` via `SPECS[screen]["accent_item"]`. Combat
opts out (its item 5 is the info panel).

Proven on the golive captures: `world_seed_reveal` / `world_setup` /
`scenario_brief` / `debrief` all score `teal_frac=0.00000 -> item5 FAIL` (was a
false PASS). The smoke now tells the truth -- the shipped screens fail the canon
until the Ferrospora skin (S1+) lands.

## Status

- All 12 primitives + CLI TDD'd GREEN (23 pytest); combined runner proven
  end-to-end against real PIL + real Gemma-4 (the CLI is landed, not an inline harness).
- Build-out: populated-drive (real room code); calibrate the teal `min_fraction`
  against the first real Ferrospora frames (S1); Godot `window.__<screen>_state`
  bridge for non-color measurables (font px, counts) -- done in the Godot-repo
  workflow (GUT + tdd-guard).

Refs: runbook `docs/runbook/godot-v2-first-playable-golive.md` sec 5; memory
`project_godot_first_playable`.
