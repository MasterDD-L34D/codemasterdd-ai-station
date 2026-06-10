"""Tests for scripts/claude-api/log_spend.py (ADR-0023 spend tracking helper).

Behavior under test: creates monthly log from template, appends entry rows,
recomputes cumulative cost, estimates cost from embedded pricing, enforces
budget-cap threshold messaging ($10/$15/$20 per ADR-0023).
"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "claude-api" / "log_spend.py"


def run_script(*args, log_dir):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--log-dir", str(log_dir), *args],
        capture_output=True,
        text=True,
    )


def test_script_exists():
    assert SCRIPT.is_file(), f"missing {SCRIPT}"


def test_creates_monthly_file_with_header(tmp_path):
    r = run_script(
        "--task", "smoke test",
        "--model", "claude-haiku-4-5",
        "--tokens-in", "20",
        "--tokens-out", "10",
        "--date", "2026-06-11T12:00",
        log_dir=tmp_path,
    )
    assert r.returncode == 0, r.stderr
    log_file = tmp_path / "claude-api-spend-2026-06.md"
    assert log_file.is_file()
    text = log_file.read_text(encoding="utf-8")
    assert "| Data/ora | Task | Model | Token sent | Token recv | Cost USD | Outcome |" in text
    assert "smoke test" in text
    assert "ADR-0023" in text


def test_appends_and_recomputes_cumulative(tmp_path):
    run_script(
        "--task", "first", "--model", "claude-haiku-4-5",
        "--tokens-in", "1000", "--tokens-out", "500",
        "--cost-usd", "1.50", "--date", "2026-06-11T12:00",
        log_dir=tmp_path,
    )
    r = run_script(
        "--task", "second", "--model", "claude-haiku-4-5",
        "--tokens-in", "1000", "--tokens-out", "500",
        "--cost-usd", "2.25", "--date", "2026-06-12T09:30",
        log_dir=tmp_path,
    )
    assert r.returncode == 0, r.stderr
    text = (tmp_path / "claude-api-spend-2026-06.md").read_text(encoding="utf-8")
    assert text.count("| 2026-06-") == 2
    assert "$3.75" in text  # cumulative recomputed
    assert "$3.75" in r.stdout


def test_cost_estimated_from_pricing_when_omitted(tmp_path):
    # haiku-4-5: $1/MTok in + $5/MTok out -> 1M in + 1M out = $6.00
    r = run_script(
        "--task", "estimate", "--model", "claude-haiku-4-5",
        "--tokens-in", "1000000", "--tokens-out", "1000000",
        "--date", "2026-06-11T12:00",
        log_dir=tmp_path,
    )
    assert r.returncode == 0, r.stderr
    text = (tmp_path / "claude-api-spend-2026-06.md").read_text(encoding="utf-8")
    assert "$6.0000" in text


def test_unknown_model_without_cost_fails(tmp_path):
    r = run_script(
        "--task", "x", "--model", "mystery-model-9",
        "--tokens-in", "10", "--tokens-out", "10",
        "--date", "2026-06-11T12:00",
        log_dir=tmp_path,
    )
    assert r.returncode != 0
    assert "cost-usd" in (r.stderr + r.stdout)


def test_threshold_warning_over_cap(tmp_path):
    r = run_script(
        "--task", "big", "--model", "claude-opus-4-8",
        "--tokens-in", "100", "--tokens-out", "100",
        "--cost-usd", "21.00", "--date", "2026-06-11T12:00",
        log_dir=tmp_path,
    )
    assert r.returncode == 0, r.stderr
    assert "reactivation" in r.stdout.lower()


def test_output_and_file_are_ascii(tmp_path):
    r = run_script(
        "--task", "ascii check", "--model", "claude-haiku-4-5",
        "--tokens-in", "10", "--tokens-out", "10",
        "--date", "2026-06-11T12:00",
        log_dir=tmp_path,
    )
    assert r.returncode == 0, r.stderr
    text = (tmp_path / "claude-api-spend-2026-06.md").read_text(encoding="utf-8")
    assert text.isascii(), "log file must be ASCII-first (ADR-0021)"
    assert r.stdout.isascii()
