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


def test_resume_reruns_warmup_when_block_incomplete():
    done = {("cold", "A", 0), ("cold", "B", 0), ("wup", "A", 0), ("warm", "A", 0), ("warm", "A", 1),
            ("wup", "B", 1), ("warm", "B", 100)}
    plan = bv.plan_runs(done, "A", "B", cold=1, warm=2)
    # block 1 (B) misses warm 101: its warmup must run again right before it (review PR582 P1-1)
    assert plan[:2] == [("B", "wup", 1, False), ("B", "warm", 101, False)]
