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
