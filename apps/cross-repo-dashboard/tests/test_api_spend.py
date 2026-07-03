"""Tests for fetch_api_spend (ADR-0023 cap-watch card).

Behavior under test: aggregates '**Cumulative cost mese**: $X' across the
monthly gitignored spend logs, reports current-month MTD + all-time total,
and maps MTD to the soft cap band ($10/$15/$20). Absent month = $0 (the logs
are entry-triggered, not backfilled).

app.LOGS_DIR is monkeypatched to a tmp dir so no real logs are read.
"""

from __future__ import annotations


def _write(tmp_path, name, cost):
    (tmp_path / name).write_text(
        f"# spend\n\n- **Cumulative cost mese**: ${cost}\n", encoding="utf-8"
    )


def test_empty_dir_is_zero_ok_band(tmp_path, monkeypatch):
    import app
    monkeypatch.setattr(app, "LOGS_DIR", tmp_path)
    r = app.fetch_api_spend()
    assert r["mtd_cost"] == 0.0
    assert r["total_cost"] == 0.0
    assert r["band"] == "ok"
    assert r["months_tracked"] == 0


def test_aggregates_mtd_and_total(tmp_path, monkeypatch):
    import app
    monkeypatch.setattr(app, "LOGS_DIR", tmp_path)
    cur = app.datetime.now(app.timezone.utc).strftime("%Y-%m")
    _write(tmp_path, "claude-api-spend-2020-01.md", "0.5000")  # past month
    _write(tmp_path, f"claude-api-spend-{cur}.md", "12.5000")  # current month
    r = app.fetch_api_spend()
    assert r["mtd_cost"] == 12.5  # only current month counts toward MTD
    assert r["total_cost"] == 13.0  # all months
    assert r["months_tracked"] == 2


def test_band_thresholds(tmp_path, monkeypatch):
    import app
    monkeypatch.setattr(app, "LOGS_DIR", tmp_path)
    cur = app.datetime.now(app.timezone.utc).strftime("%Y-%m")
    for cost, expected in [("9.9999", "ok"), ("10.0000", "awareness"),
                           ("15.0000", "alert"), ("20.0000", "trigger")]:
        _write(tmp_path, f"claude-api-spend-{cur}.md", cost)
        assert app.fetch_api_spend()["band"] == expected, cost


def test_malformed_file_does_not_crash(tmp_path, monkeypatch):
    import app
    monkeypatch.setattr(app, "LOGS_DIR", tmp_path)
    (tmp_path / "claude-api-spend-2020-02.md").write_text("no cost here", encoding="utf-8")
    r = app.fetch_api_spend()
    assert r["total_cost"] == 0.0
    assert r["months_tracked"] == 1  # file counted, cost 0
