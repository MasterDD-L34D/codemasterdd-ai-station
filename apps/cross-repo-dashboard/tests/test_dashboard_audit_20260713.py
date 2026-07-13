"""Regression tests for the 2026-07-13 dashboard truthfulness/completeness audit.

Locks the behavior added by that audit so it cannot silently regress:
- F1  healthchecks carry an `always_on` flag (only Ollama is always-on; the rest
      are opt-in, so the home can render their DOWN as "idle" not "broken").
- F2A fetch_adr_countdown surfaces EVERY Status:Proposed ADR, including undated
      ones that ratify-on-merge (ratify_date/days_remaining None), not only those
      with an explicit deadline date.
- F5  the OS-console Scheduling layer queries the governor-ingest task (added #564),
      not just morning-brief + jules-daily-digest.
"""
from __future__ import annotations

from unittest.mock import MagicMock


def test_healthcheck_config_only_ollama_always_on():
    import app
    always = [h for h in app.HEALTHCHECKS if h.get("always_on")]
    assert [h["name"] for h in always] == ["Ollama"], "only Ollama must be always_on"
    # every other real entry is opt-in (absent/falsey always_on)
    assert all(not h.get("always_on") for h in app.HEALTHCHECKS if h["name"] != "Ollama")


def test_fetch_healthchecks_propagates_always_on(monkeypatch):
    import app

    class MockConnErr(Exception):
        pass

    monkeypatch.setattr(app.requests, "ConnectionError", MockConnErr, raising=False)
    monkeypatch.setattr(app.requests, "Timeout", type("T", (Exception,), {}), raising=False)
    monkeypatch.setattr(app, "HEALTHCHECKS", [
        {"name": "core", "url": "http://up", "timeout": 3, "category": "c", "always_on": True},
        {"name": "optin", "url": "http://down", "timeout": 3, "category": "c"},
    ])
    monkeypatch.setattr(app, "HEALTHCHECKS_TCP", [])

    class Ok:
        status_code = 200
        class elapsed:
            @staticmethod
            def total_seconds():
                return 0.01

    def fake_get(url, **kw):
        if url == "http://down":
            raise MockConnErr()
        return Ok()

    monkeypatch.setattr(app.requests, "get", MagicMock(side_effect=fake_get))
    res = {r["name"]: r for r in app.fetch_healthchecks(force_refresh=True)}
    # always_on propagates through BOTH the up-branch and the down-branch
    assert res["core"]["always_on"] is True and res["core"]["status"] == "up"
    assert res["optin"]["always_on"] is False and res["optin"]["status"] == "down"


def test_adr_countdown_includes_undated_proposed(tmp_path, monkeypatch):
    import app
    (tmp_path / "0099-undated.md").write_text(
        "# ADR-0099\n\n**Status**: Proposed (Eduardo ratifies)\n\nbody\n", encoding="utf-8")
    (tmp_path / "0098-dated.md").write_text(
        "# ADR-0098\n\n**Status**: Proposed\n\n**Ratification check date**: entro 2099-01-01\n",
        encoding="utf-8")
    (tmp_path / "0097-accepted.md").write_text(
        "# ADR-0097\n\n**Status**: Accepted\n", encoding="utf-8")
    monkeypatch.setattr(app, "ADR_DIR", tmp_path)

    items = {i["adr"]: i for i in app.fetch_adr_countdown()}
    assert "0097" not in items, "Accepted ADRs must not appear"
    assert "0099" in items and items["0099"]["ratify_date"] is None, "undated Proposed must surface"
    assert items["0099"]["days_remaining"] is None
    assert items["0098"]["ratify_date"] == "2099-01-01", "dated deadline still parsed"


def test_scheduling_layer_queries_governor_ingest(monkeypatch):
    import app
    seen = {}

    def rec(names, *a, **k):
        seen["names"] = list(names)
        return []

    monkeypatch.setattr(app, "scheduled_task_health", rec)
    app._layer_live_state()  # calls scheduled_task_health(...) unconditionally
    assert "governor-ingest" in seen["names"]
    assert "morning-brief" in seen["names"] and "jules-daily-digest" in seen["names"]
