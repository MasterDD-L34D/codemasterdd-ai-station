# Jules task -- characterization tests for tools/py/report_kpi_alerts.py

Repo: MasterDD-L34D/Game.

## Scope (single new test file, test-only, NO behaviour change)
Create ONE new test file that characterizes the CURRENT behaviour of
`tools/py/report_kpi_alerts.py` (KPI baseline alert gate, CI-wired via
qa-kpi-monitor.yml). Test-only: do NOT modify `tools/py/report_kpi_alerts.py`
or ANY other existing file. The exact test content is provided below and has
been pre-verified green against the real module: copy it BYTE-IDENTICAL.
Do not rename, reformat, reorder, "improve" or add anything.

## Context (read-only)
- Target module: `tools/py/report_kpi_alerts.py` (77 lines, stdlib-only).
  Under test: `MetricsError`, `_load_json`, `_evaluate`, `main`.
- Sibling precedent: `tests/scripts/test_schema_enum_diff.py` (same home dir;
  here the sys.path insert points at `tools/py`). CI runs bare `pytest`.
- The basename `test_report_kpi_alerts.py` does not exist anywhere else in the
  repo (verified) -- no bare-pytest basename collision.

## File to create (ONLY this one)
- NEW `tests/scripts/test_report_kpi_alerts.py`

## Exact file content (copy byte-identical, ASCII-only)

```python
"""Characterization tests for tools/py/report_kpi_alerts.py (KPI baseline alert gate).

Behavior-only snapshot: the JSON-loading error message, the _evaluate drop-detection
rules (strict greater-than tolerance, drops-only, zero-baseline and non-numeric
guards, the bool-counts-as-numeric quirk, the exact Italian alert format with .1
percent rendering) and the main() print-vs-raise contract. A deliberate change to
these behaviors SHOULD update these assertions consciously -- that is the point of
a characterization test.
"""

import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOOLS_PY = PROJECT_ROOT / "tools" / "py"
if str(TOOLS_PY) not in sys.path:
    sys.path.insert(0, str(TOOLS_PY))

import report_kpi_alerts as r  # noqa: E402


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_metrics_error_is_a_runtime_error():
    assert issubclass(r.MetricsError, RuntimeError)


def test_load_json_missing_file_message(tmp_path):
    with pytest.raises(FileNotFoundError) as exc_info:
        r._load_json(tmp_path / "missing.json")
    assert "File JSON non trovato" in str(exc_info.value)


def test_load_json_roundtrip(tmp_path):
    p = tmp_path / "m.json"
    _write_json(p, {"a": 1})
    assert r._load_json(p) == {"a": 1}


def test_evaluate_drop_beyond_tolerance_exact_format():
    alerts = r._evaluate({"combat": {"wr": 8}}, {"combat": {"wr": 10}}, 0.1)
    assert alerts == ["[combat] metrica 'wr' scesa da 10 a 8 (variazione 20.0%)"]


def test_evaluate_increase_is_silent():
    assert r._evaluate({"combat": {"wr": 12}}, {"combat": {"wr": 10}}, 0.1) == []


def test_evaluate_drop_at_tolerance_is_silent():
    # strict > comparison: a drop exactly equal to the tolerance does not alert
    assert r._evaluate({"combat": {"wr": 9}}, {"combat": {"wr": 10}}, 0.1) == []


def test_evaluate_zero_baseline_is_skipped():
    assert r._evaluate({"s": {"k": -5}}, {"s": {"k": 0}}, 0.1) == []


def test_evaluate_non_numeric_values_are_skipped():
    assert r._evaluate({"s": {"k": 1}}, {"s": {"k": "x"}}, 0.1) == []
    assert r._evaluate({"s": {"k": "x"}}, {"s": {"k": 10}}, 0.1) == []


def test_evaluate_non_dict_or_missing_sections_are_skipped():
    assert r._evaluate({"s": 5}, {"s": {"k": 10}}, 0.1) == []
    assert r._evaluate({}, {"s": {"k": 10}}, 0.1) == []


def test_evaluate_bool_baseline_counts_as_numeric():
    # isinstance(True, int) holds, so a bool baseline is compared numerically
    alerts = r._evaluate({"s": {"k": 0}}, {"s": {"k": True}}, 0.1)
    assert alerts == ["[s] metrica 'k' scesa da True a 0 (variazione 100.0%)"]


def test_main_within_tolerance_prints_ok(tmp_path, capsys):
    m = tmp_path / "m.json"
    b = tmp_path / "b.json"
    _write_json(m, {"s": {"k": 10}})
    _write_json(b, {"s": {"k": 10}})
    rc = r.main(["--metrics", str(m), "--baseline", str(b)])
    out = capsys.readouterr().out
    assert rc is None
    assert "Nessuna deviazione KPI oltre la soglia configurata" in out


def test_main_prints_alerts_then_raises(tmp_path, capsys):
    m = tmp_path / "m.json"
    b = tmp_path / "b.json"
    _write_json(m, {"s": {"k": 5}})
    _write_json(b, {"s": {"k": 10}})
    with pytest.raises(r.MetricsError, match="Deviazioni KPI oltre soglia"):
        r.main(["--metrics", str(m), "--baseline", str(b)])
    out = capsys.readouterr().out
    assert "scesa da 10 a 5" in out


def test_main_tolerance_flag_silences_alert(tmp_path, capsys):
    m = tmp_path / "m.json"
    b = tmp_path / "b.json"
    _write_json(m, {"s": {"k": 5}})
    _write_json(b, {"s": {"k": 10}})
    rc = r.main(["--metrics", str(m), "--baseline", str(b), "--tolerance", "0.6"])
    assert rc is None
    assert "Nessuna deviazione" in capsys.readouterr().out
```

## Constraints (strict)
- Create ONLY `tests/scripts/test_report_kpi_alerts.py`, byte-identical to the
  block above.
- ZERO deletions, zero edits to any existing file. Do NOT touch
  `tools/py/report_kpi_alerts.py`, `pyproject.toml`, `pytest.ini`, package.json,
  lockfiles or any config.
- ASCII-only (the content above is pure ASCII -- keep it that way).
- No new dependencies; pytest is already the repo runner.
- Conventional Commit subject (lowercase), e.g.:
  test(tools): characterize report_kpi_alerts behavior

## Acceptance (verify before delivering)
- `pytest tests/scripts/test_report_kpi_alerts.py` -> 13 passed, 0 failed.
- No other file changed; `git diff --stat` shows exactly one new file.
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
