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
    before = sorted(p.name for p in tmp_path.iterdir())
    try:
        bv.bind_config(tmp_path, {"models": ["A", "B"], "ctx": 8192, "predict": 2048})
    except SystemExit as e:
        assert "predict" in str(e)
    else:
        raise AssertionError("mismatched config was accepted")
    assert sorted(p.name for p in tmp_path.iterdir()) == before


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
