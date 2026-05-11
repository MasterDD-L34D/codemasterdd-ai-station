"""Tests for daily aggregation + inline SVG sparkline rendering."""
from __future__ import annotations

from stats import aggregate_by_day, build_sparkline_svg


def _row(created_at: str, cost_usd: float = 0.0) -> dict:
    return {"created_at": created_at, "cost_usd": cost_usd}


def test_aggregate_by_day_groups_and_sums():
    rows = [
        _row("2026-05-11T08:00:00+00:00", 0.001),
        _row("2026-05-11T23:00:00+00:00", 0.002),
        _row("2026-05-10T12:00:00+00:00", 0.010),
        _row("2026-05-12T01:00:00+00:00", 0.000),
    ]
    daily = aggregate_by_day(rows)
    assert [d["date"] for d in daily] == ["2026-05-10", "2026-05-11", "2026-05-12"]
    by_date = {d["date"]: d for d in daily}
    assert by_date["2026-05-11"]["count"] == 2
    assert abs(by_date["2026-05-11"]["cost_usd"] - 0.003) < 1e-9
    assert by_date["2026-05-10"]["count"] == 1
    assert by_date["2026-05-12"]["count"] == 1


def test_aggregate_by_day_skips_missing_created_at():
    daily = aggregate_by_day([_row("", 0.5), _row(None, 0.5)])
    assert daily == []


def test_aggregate_by_day_empty_input():
    assert aggregate_by_day([]) == []


def test_sparkline_empty_renders_no_data_placeholder():
    svg = build_sparkline_svg([])
    assert svg.startswith("<svg")
    assert "no data" in svg


def test_sparkline_single_point_does_not_crash():
    svg = build_sparkline_svg([5.0])
    assert "<polyline" in svg
    # Single point should still render (degenerate line)
    assert "min 5" in svg and "max 5" in svg


def test_sparkline_normalizes_to_viewbox():
    svg = build_sparkline_svg([1, 2, 3, 4, 5], width=400, height=100)
    assert 'viewBox="0 0 400 100"' in svg
    # First point should be on the left edge (after padding), last on the right.
    # Default pad=8 → first x ≈ 8, last x ≈ 392
    assert "8.0," in svg
    assert "392.0," in svg
    assert "max 5" in svg and "min 1" in svg


def test_sparkline_handles_flat_series():
    # All-equal points (span=0) must not divide by zero.
    svg = build_sparkline_svg([3.0, 3.0, 3.0])
    assert "<polyline" in svg
    assert "max 3" in svg


def test_sparkline_label_used_as_aria():
    svg = build_sparkline_svg([1, 2, 3], label="Entries per day")
    assert 'aria-label="Entries per day"' in svg
