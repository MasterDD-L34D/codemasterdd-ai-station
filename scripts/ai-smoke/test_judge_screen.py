"""AI-smoke vision-judge -- contract for the model-response JSON extractor.

The sovereign vision-judge (Gemma-4 via Ollama) returns free-form text that
wraps a JSON verdict array (often fenced or prefaced). _extract_json must pull
the verdict array out robustly. RED-first per tdd-guard before judge_screen
exists.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from judge_screen import _extract_json  # noqa: E402


def test_extract_json_from_fenced_model_response():
    raw = (
        "Sure, here is my assessment:\n"
        "```json\n"
        '[{"item": 1, "verdict": "PASS", "reason": "room code centered"},'
        ' {"item": 4, "verdict": "FAIL", "reason": "background is flat gray"}]\n'
        "```\n"
        "Let me know if you need more."
    )
    out = _extract_json(raw)
    assert out == [
        {"item": 1, "verdict": "PASS", "reason": "room code centered"},
        {"item": 4, "verdict": "FAIL", "reason": "background is flat gray"},
    ]


def test_is_dark_bg_rejects_the_gray_gemma_false_passed():
    # Deterministic layer: the calibration finding as a test. Gemma-4 vision
    # FALSE-PASSED the real lobby bg RGB(77,77,77) (30% gray) as "dark void 8%".
    # The deterministic check must FAIL that gray and PASS a true near-black void.
    from judge_screen import _is_dark_bg

    assert _is_dark_bg([(77, 77, 77), (77, 77, 77)]) is False
    assert _is_dark_bg([(10, 10, 15), (8, 8, 12)]) is True


def test_merge_verdicts_deterministic_overrides_vision():
    # Combined judge core: deterministic check WINS for measurable items
    # (vision hallucinates color); vision kept for qualitative items.
    from judge_screen import _merge_verdicts

    vision = [
        {"item": 2, "verdict": "PASS", "reason": "slots present"},
        {"item": 4, "verdict": "PASS", "reason": "looks dark"},  # vision hallucinated
    ]
    det = {4: {"verdict": "FAIL", "reason": "bg mean RGB 77 >= 40 (not dark)"}}
    by_item = {v["item"]: v for v in _merge_verdicts(vision, det)}
    assert by_item[4]["verdict"] == "FAIL"
    assert by_item[4]["source"] == "deterministic"
    assert by_item[2]["verdict"] == "PASS"
    assert by_item[2]["source"] == "vision"


def test_sample_bg_reads_corner_pixels(tmp_path):
    # Screenshot-side deterministic IO: sample background corner pixels.
    from PIL import Image

    from judge_screen import sample_bg

    p = tmp_path / "solid.png"
    Image.new("RGB", (200, 200), (50, 60, 70)).save(str(p))
    rgbs = sample_bg(str(p))
    assert len(rgbs) >= 4
    assert all(c == (50, 60, 70) for c in rgbs)


def test_build_judge_payload_shapes_ollama_request():
    from judge_screen import build_judge_payload

    pl = build_judge_payload("B64DATA", "lobby", model="m")
    assert pl["model"] == "m"
    assert pl["images"] == ["B64DATA"]
    assert pl["stream"] is False
    assert "ITEMS:" in pl["prompt"]


def test_run_deterministic_overrides_vision_on_gray_bg():
    # End-to-end orchestration (DI: inject sampler + vision transport, no real IO).
    # Gray bg + vision saying "PASS" on item 4 -> deterministic FAIL must win.
    from judge_screen import run

    all_pass = (
        '[{"verdict":"PASS"},{"verdict":"PASS"},{"verdict":"PASS"},'
        '{"verdict":"PASS","reason":"looks dark"},{"verdict":"PASS"},{"verdict":"PASS"}]'
    )
    merged = run(
        "x.png",
        "lobby",
        40,
        sampler=lambda path, inset=40: [(77, 77, 77)] * 4,
        vision_post=lambda path, screen, host, model: all_pass,
    )
    by = {m["item"]: m for m in merged}
    assert by[4]["verdict"] == "FAIL"
    assert by[4]["source"] == "deterministic"
    assert by[1]["source"] == "vision"


def test_prompt_includes_screen_and_all_bible_items():
    from judge_screen import _prompt, SPECS

    p = _prompt("lobby")
    assert "Lobby" in p
    for it in SPECS["lobby"]["items"]:
        assert it in p


def test_form_pulse_spec_prompt_includes_radar_and_creature_verbs():
    # Screen 2 (Shared Form Pulse). bg stays item 4 (run() hardcodes det={4}).
    from judge_screen import _prompt, SPECS

    assert "form_pulse" in SPECS
    assert "void" in SPECS["form_pulse"]["items"][3].lower()  # item 4 = deterministic bg
    p = _prompt("form_pulse")
    assert "Form Pulse" in p
    assert "radar" in p.lower()
    for it in SPECS["form_pulse"]["items"]:
        assert it in p


def test_screens_3_4_6_specs_present_with_bg_as_item4():
    # Screens 3 (world_seed_reveal), 4 (world_setup), 6 (combat). Each keeps the
    # dark-void bg as item 4 so run()'s deterministic det={4} maps correctly.
    from judge_screen import _prompt, SPECS

    for screen in ("world_seed_reveal", "world_setup", "combat"):
        assert screen in SPECS, screen
        assert len(SPECS[screen]["items"]) == 6, screen
        assert "void" in SPECS[screen]["items"][3].lower(), screen
        _prompt(screen)  # builds without KeyError


def test_vision_post_posts_to_ollama_and_returns_response(tmp_path):
    # Real Ollama transport for run()'s vision channel. Reads image -> b64 ->
    # POST /api/generate -> returns the model 'response' text. urlopen injected,
    # no real network. This is the un-landed glue that makes run() invokable.
    import json as _j

    from PIL import Image

    from judge_screen import _vision_post

    p = tmp_path / "shot.png"
    Image.new("RGB", (8, 8), (0, 0, 0)).save(str(p))
    captured = {}

    class FakeResp:
        def read(self):
            return b'{"response": "[{\\"verdict\\":\\"PASS\\"}]"}'

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(req, timeout=None):
        captured["url"] = req.full_url
        captured["body"] = _j.loads(req.data)
        return FakeResp()

    out = _vision_post(str(p), "lobby", "host:1234", "m", urlopen=fake_urlopen)
    assert out == '[{"verdict":"PASS"}]'
    assert captured["url"] == "http://host:1234/api/generate"
    assert captured["body"]["model"] == "m"
    assert isinstance(captured["body"]["images"][0], str) and captured["body"]["images"][0]


def test_main_returns_1_when_smoke_has_a_fail():
    # CLI gate semantics: any FAIL verdict -> non-zero exit (autonomous smoke
    # trips). run_fn injected so no real IO; argv parsed by main's argparse.
    from judge_screen import main

    rc = main(
        ["--image", "x.png", "--screen", "lobby"],
        run_fn=lambda *a, **k: [
            {"item": 4, "verdict": "FAIL", "reason": "gray", "source": "deterministic"},
        ],
        out=lambda *a, **k: None,
    )
    assert rc == 1


def test_world_seed_reveal_item3_accepts_named_companion():
    # The reveal IS the companion appearance (Bible 3) -- a populated/named
    # Custode is correct, NOT a defect. item3 must not demand a dormant placeholder
    # (the Godot smoke now seeds a real Custode -> the old wording false-FAILed it).
    from judge_screen import SPECS

    item3 = SPECS["world_seed_reveal"]["items"][2].lower()
    assert "dormant" not in item3
    assert "companion" in item3


def test_scenario_brief_spec_present_with_bg_item4():
    # Screen 5 (Scenario Brief). bg stays item 4 so run()'s det={4} maps.
    from judge_screen import SPECS, _prompt

    assert "scenario_brief" in SPECS
    assert len(SPECS["scenario_brief"]["items"]) == 6
    assert "void" in SPECS["scenario_brief"]["items"][3].lower()
    p = _prompt("scenario_brief")
    assert "Scenario" in p


def test_debrief_spec_present_with_bg_item4():
    # Screen 7 (Debrief). bg stays item 4 so run()'s det={4} maps.
    from judge_screen import SPECS, _prompt

    assert "debrief" in SPECS
    assert len(SPECS["debrief"]["items"]) == 6
    assert "void" in SPECS["debrief"]["items"][3].lower()
    p = _prompt("debrief")
    assert "Debrief" in p


def test_combat_bg_is_vision_not_deterministic():
    # Combat board + chrome fill the screen -> no clean corner void to sample, so
    # the corner-sample false-FAILs (handoff finding). run() must NOT apply the
    # deterministic bg override for combat (item 4 -> vision).
    from judge_screen import run

    all_pass = (
        '[{"verdict":"PASS"},{"verdict":"PASS"},{"verdict":"PASS"},'
        '{"verdict":"PASS"},{"verdict":"PASS"},{"verdict":"PASS"}]'
    )
    merged = run(
        "x.png",
        "combat",
        40,
        sampler=lambda path, inset=40: [(77, 77, 77)] * 4,  # gray corners (chrome)
        vision_post=lambda path, screen, host, model: all_pass,
    )
    by = {m["item"]: m for m in merged}
    # gray corners would FAIL deterministically; combat opts out -> vision wins.
    assert by[4]["source"] == "vision"
    assert by[4]["verdict"] == "PASS"


def test_main_prints_merged_verdicts_and_exits_clean_on_all_pass():
    # Happy path: main emits the merged verdicts as JSON (via injected out) and
    # returns 0 when nothing FAILs. The autonomous smoke's machine-readable output.
    import json as _j

    from judge_screen import main

    captured = {}
    rc = main(
        ["--image", "x.png"],
        run_fn=lambda *a, **k: [
            {"item": 1, "verdict": "PASS", "reason": "ok", "source": "vision"},
        ],
        out=lambda s: captured.__setitem__("s", s),
    )
    assert rc == 0
    assert _j.loads(captured["s"])[0]["verdict"] == "PASS"


# --- S0 re-baseline: parchment anti-pattern -> Ferrospora biopunk canon ---
# The judge was certifying the shipped anti-pattern (parchment/bronze/gold) as
# PASS. Canon (vault 42-STYLE-GUIDE-UI): teal spore-glow #3acde5 is the PRIMARY
# accent, gold/bronze is SECONDARY. Color is measurable -> deterministic (the
# vision model hallucinates color, same lesson as _is_dark_bg), so item 5 (the
# accent line) gets a deterministic teal-presence override, not a vision verdict.


def test_classify_teal_pixel_accepts_spore_glow_rejects_gold_void_mycelium():
    # The primary-accent gate: teal #3acde5 = RGB(58,205,229) is the target;
    # gold #eedbae, near-black void, and mycelium #cd52d2 must NOT count as teal
    # (gold/mycelium are secondary, the void is bg) -- else parchment screens pass.
    from judge_screen import _classify_teal_pixel

    assert _classify_teal_pixel((58, 205, 229)) is True   # ferro-teal (primary)
    assert _classify_teal_pixel((40, 150, 170)) is True    # darker teal glow
    assert _classify_teal_pixel((238, 219, 174)) is False   # ferro gold (secondary)
    assert _classify_teal_pixel((10, 10, 15)) is False      # living void (bg)
    assert _classify_teal_pixel((205, 82, 210)) is False    # mycelium purple


def test_is_teal_accent_thresholds_a_minimum_fraction():
    # A parchment-only screen has ~0 teal pixels -> FAIL; a biopunk screen with a
    # teal-accented frame has a meaningful teal fraction -> PASS.
    from judge_screen import _is_teal_accent

    assert _is_teal_accent(0.0) is False
    assert _is_teal_accent(0.0001) is False   # below the min accent fraction
    assert _is_teal_accent(0.03) is True


def test_sample_accent_counts_teal_fraction(tmp_path):
    # Deterministic IO: scan the screenshot, return the teal-pixel fraction.
    from PIL import Image

    from judge_screen import sample_accent

    # half teal, half black -> fraction ~0.5
    im = Image.new("RGB", (200, 100), (10, 10, 15))
    for x in range(100):
        for y in range(100):
            im.putpixel((x, y), (58, 205, 229))
    p = tmp_path / "half_teal.png"
    im.save(str(p))
    assert sample_accent(str(p)) > 0.4

    # all gold parchment -> ~0 teal
    pg = tmp_path / "gold.png"
    Image.new("RGB", (64, 64), (238, 219, 174)).save(str(pg))
    assert sample_accent(str(pg)) < 0.001


def test_item5_specs_flipped_from_parchment_to_biopunk_teal():
    # The core re-baseline: every screen that had the parchment line now demands
    # the Ferrospora biopunk skin with teal as the PRIMARY accent; a parchment-
    # only gold-bordered panel is the FAIL exemplar, not the target.
    from judge_screen import SPECS

    parchment_screens = (
        "lobby", "form_pulse", "world_seed_reveal",
        "world_setup", "scenario_brief", "debrief",
    )
    for screen in parchment_screens:
        item5 = SPECS[screen]["items"][4].lower()
        assert "teal" in item5, screen
        assert ("biopunk" in item5 or "ferrospora" in item5
                or "spore" in item5), screen
        # the old wording certified parchment/gold as the target -- it must be gone
        assert "warm parchment/bronze theme with gold borders" not in item5, screen
        # this screen's accent line is deterministically teal-gated (item 5)
        assert SPECS[screen].get("accent_item") == 5, screen


def test_combat_has_no_parchment_accent_item():
    # Combat's item 5 is the selected-unit info panel, NOT a theme/color line --
    # it must NOT get the teal-color override (it would mis-gate a non-color item).
    from judge_screen import SPECS

    assert "accent_item" not in SPECS["combat"]
    assert "info panel" in SPECS["combat"]["items"][4].lower()


def test_run_applies_deterministic_teal_accent_override_on_parchment_screen():
    # End-to-end: a parchment screen (no teal) where vision says item 5 PASS must
    # be overridden to FAIL by the deterministic teal gate (color is measurable).
    from judge_screen import run

    all_pass = (
        '[{"verdict":"PASS"},{"verdict":"PASS"},{"verdict":"PASS"},'
        '{"verdict":"PASS"},{"verdict":"PASS","reason":"looks teal"},'
        '{"verdict":"PASS"}]'
    )
    merged = run(
        "x.png",
        "lobby",
        40,
        sampler=lambda path, inset=40: [(10, 10, 15)] * 4,  # dark void -> item4 PASS
        vision_post=lambda path, screen, host, model: all_pass,
        accent_sampler=lambda path: 0.0,  # no teal -> deterministic FAIL
    )
    by = {m["item"]: m for m in merged}
    assert by[5]["verdict"] == "FAIL"
    assert by[5]["source"] == "deterministic"
    # and with teal present the gate passes
    merged_ok = run(
        "x.png",
        "lobby",
        40,
        sampler=lambda path, inset=40: [(10, 10, 15)] * 4,
        vision_post=lambda path, screen, host, model: all_pass,
        accent_sampler=lambda path: 0.05,  # teal accent present -> PASS
    )
    by_ok = {m["item"]: m for m in merged_ok}
    assert by_ok[5]["verdict"] == "PASS"
    assert by_ok[5]["source"] == "deterministic"


def test_run_combat_keeps_item5_vision_no_teal_override():
    # Combat has no accent_item -> even with an accent_sampler the info-panel item
    # 5 must stay vision-judged (the override is parchment-screens-only).
    from judge_screen import run

    all_pass = (
        '[{"verdict":"PASS"},{"verdict":"PASS"},{"verdict":"PASS"},'
        '{"verdict":"PASS"},{"verdict":"PASS"},{"verdict":"PASS"}]'
    )
    merged = run(
        "x.png",
        "combat",
        40,
        sampler=lambda path, inset=40: [(77, 77, 77)] * 4,
        vision_post=lambda path, screen, host, model: all_pass,
        accent_sampler=lambda path: 0.0,
    )
    by = {m["item"]: m for m in merged}
    assert by[5]["source"] == "vision"
    assert by[5]["verdict"] == "PASS"


def test_sample_accent_ignores_central_teal_content_masking_parchment_chrome(tmp_path):
    # Codex P2 (judge_screen.py:220): teal *content* (e.g. a central 5-axis radar
    # or a teal chart) must NOT mask parchment/gold *chrome*. The item-5 gate
    # judges the panel SKIN, not gameplay graphics. sample_accent samples the
    # chrome band (outer frame) and excludes the central content region, so a teal
    # blob dead-center on a gold-panel screen scores ~0 -> the parchment FAIL is
    # preserved. (Whole-screen sampling false-PASSed this: 3600/40000 ~= 0.09.)
    from PIL import Image

    from judge_screen import sample_accent

    im = Image.new("RGB", (200, 200), (238, 219, 174))  # gold parchment chrome
    for x in range(70, 130):  # teal "radar" content, dead center
        for y in range(70, 130):
            im.putpixel((x, y), (58, 205, 229))
    p = tmp_path / "teal_center_gold_chrome.png"
    im.save(str(p))
    assert sample_accent(str(p)) < 0.005


def test_sample_accent_still_counts_teal_in_the_chrome_band(tmp_path):
    # The flip side of the chrome-band restriction: a real Ferrospora skin glows
    # teal on the frame/panels (the band), so a teal-framed screen still scores a
    # meaningful fraction -- the fix must not over-restrict and lose true teal.
    from PIL import Image

    from judge_screen import sample_accent

    im = Image.new("RGB", (200, 200), (10, 10, 15))  # living-void centre
    for x in range(200):
        for y in range(200):
            if x < 25 or x >= 175 or y < 25 or y >= 175:  # teal outer frame (chrome)
                im.putpixel((x, y), (58, 205, 229))
    p = tmp_path / "teal_frame.png"
    im.save(str(p))
    assert sample_accent(str(p)) > 0.3
