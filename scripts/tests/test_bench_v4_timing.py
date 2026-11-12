"""Tests for scripts/bench-v4/bench_v4_timing.py (review PR582 P1-2: prompt prefix cache)."""
import importlib.util
from pathlib import Path

_P = Path(__file__).resolve().parents[1] / "bench-v4" / "bench_v4_timing.py"
_spec = importlib.util.spec_from_file_location("bench_v4_timing", _P)
bv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bv)


def test_each_prompt_is_unique_to_defeat_prefix_cache():
    a, b = bv.make_prompt(), bv.make_prompt()
    assert a != b
    assert a.endswith(bv.PROMPT) and b.endswith(bv.PROMPT)


def test_resume_with_different_predict_is_refused_before_any_write(tmp_path):
    bv.bind_config(tmp_path, {"models": ["A", "B"], "ctx": 8192, "predict": 300})
    (tmp_path / "raw.jsonl").write_text('{"phase": "cold"}\n', encoding="utf-8")
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    try:
        bv.bind_config(tmp_path, {"models": ["A", "B"], "ctx": 8192, "predict": 2048})
    except SystemExit as e:
        assert "predict" in str(e)
    else:
        raise AssertionError("mismatched config was accepted")
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before


def test_main_refuses_mismatched_dir_before_network(tmp_path, monkeypatch):
    bv.bind_config(tmp_path, bv.measurement_config(["A", "B"], 8192, 300))

    def boom(*a, **k):
        raise AssertionError("network touched")

    monkeypatch.setattr(bv, "unload_all", boom)
    monkeypatch.setattr(bv, "post", boom)
    monkeypatch.setattr(bv.sys, "argv", ["x", "--models", "A", "B", "--predict", "2048", "--out", str(tmp_path)])
    try:
        bv.main()
    except SystemExit as e:
        assert "predict" in str(e)
    else:
        raise AssertionError("main accepted a mismatched dir")
    assert not (tmp_path / "SUMMARY.md").exists()


def test_same_measurement_resumes_and_changed_prompt_is_refused(tmp_path, monkeypatch):
    cfg = bv.measurement_config(["A", "B"], 8192, 300)
    bv.bind_config(tmp_path, cfg)
    (tmp_path / "raw.jsonl").write_text('{"phase": "cold"}\n', encoding="utf-8")
    bv.bind_config(tmp_path, bv.measurement_config(["A", "B"], 8192, 300))  # --cold/--warm are not bound
    monkeypatch.setattr(bv, "PROMPT", bv.PROMPT + " Changed.")
    try:
        bv.bind_config(tmp_path, bv.measurement_config(["A", "B"], 8192, 300))
    except SystemExit as e:
        assert "prompt_sha" in str(e)
    else:
        raise AssertionError("changed prompt was accepted")


def test_corrupt_meta_is_refused_with_clear_message(tmp_path):
    (tmp_path / "meta.json").write_text("", encoding="utf-8")  # e.g. crash mid-write
    try:
        bv.bind_config(tmp_path, bv.measurement_config(["A", "B"], 8192, 300))
    except SystemExit as e:
        assert "meta.json" in str(e) and "unreadable" in str(e)
    else:
        raise AssertionError("corrupt meta.json was accepted")


def test_legacy_dir_with_raw_but_no_meta_is_refused(tmp_path):
    (tmp_path / "raw.jsonl").write_text('{"phase": "cold"}\n', encoding="utf-8")
    try:
        bv.bind_config(tmp_path, {"models": ["A", "B"], "ctx": 8192, "predict": 300})
    except SystemExit as e:
        assert "meta.json" in str(e)
    else:
        raise AssertionError("legacy dir without meta.json was accepted")
    assert not (tmp_path / "meta.json").exists()


def test_resume_reruns_warmup_when_block_incomplete():
    done = {("cold", "A", 0), ("cold", "B", 0), ("wup", "A", 0), ("warm", "A", 0), ("warm", "A", 1),
            ("wup", "B", 1), ("warm", "B", 100)}
    plan = bv.plan_runs(done, "A", "B", cold=1, warm=2)
    # block 1 (B) misses warm 101: its warmup must run again right before it (review PR582 P1-1)
    assert plan[:2] == [("B", "wup", 1, False), ("B", "warm", 101, False)]
