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
