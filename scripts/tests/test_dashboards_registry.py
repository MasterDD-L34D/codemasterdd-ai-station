"""Tests for the fleet dashboards catalog (apps/cross-repo-dashboard).

Covers: registry schema integrity, the regen security contract (fixed argv
lists only -- the UI can never inject commands), route smoke via Flask test
client, and negative controls on /api/regen-dashboard (L-041: a guard test
without a must-block case proves nothing).
"""
from __future__ import annotations

import sys
from pathlib import Path, PureWindowsPath

import pytest

APP_DIR = Path(__file__).resolve().parents[2] / "apps" / "cross-repo-dashboard"
sys.path.insert(0, str(APP_DIR))

from dashboards_registry import DASHBOARDS, RUN_MONITORS  # noqa: E402

VALID_STATUS = {"live", "regenerable", "stale", "one-shot"}
VALID_KIND = {"served", "generator", "static", "monitor"}


def test_registry_schema() -> None:
    ids = [d["id"] for d in DASHBOARDS]
    assert len(ids) == len(set(ids)), "duplicate dashboard ids"
    for d in DASHBOARDS:
        assert d["status"] in VALID_STATUS, f"{d['id']}: bad status {d['status']}"
        assert d["kind"] in VALID_KIND, f"{d['id']}: bad kind {d['kind']}"
        assert d.get("name") and d.get("area") and d.get("desc"), f"{d['id']}: missing display fields"
        assert d.get("open"), f"{d['id']}: missing open target"


def test_regen_security_contract() -> None:
    """Every regen block is a fixed list of argv string-lists (no shell strings,
    no format placeholders): the API only ever dict-looks-up and executes these."""
    for d in DASHBOARDS:
        regen = d.get("regen")
        if not regen:
            continue
        # PureWindowsPath: the registry targets the Windows fleet host by design;
        # CI runs on Linux where Path("C:\\...") would be relative (false fail).
        assert isinstance(regen.get("cwd"), str) and PureWindowsPath(regen["cwd"]).is_absolute(), \
            f"{d['id']}: regen.cwd must be absolute"
        steps = regen.get("steps")
        assert isinstance(steps, list) and steps, f"{d['id']}: regen.steps empty"
        for argv in steps:
            assert isinstance(argv, list) and all(isinstance(a, str) for a in argv), \
                f"{d['id']}: step is not an argv string-list: {argv!r}"
            joined = " ".join(argv)
            assert "{" not in joined and "%s" not in joined, \
                f"{d['id']}: placeholder in argv suggests interpolation: {argv!r}"


def test_run_monitors_schema() -> None:
    for m in RUN_MONITORS:
        assert m.get("id") and m.get("name") and m.get("trial_dir")
        assert int(m.get("total_iter", 0)) > 0


@pytest.fixture(scope="module")
def client():
    # CI "dep-light stable set" has no flask/requests: the registry-contract
    # tests above still run there; these route tests run where the app's real
    # deps exist (dev machines, dashboard host).
    pytest.importorskip("flask")
    pytest.importorskip("requests")
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_dashboards_page_renders(client) -> None:
    r = client.get("/cross-repo/dashboards")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert "catalogo fleet" in body
    # a known entry from each layer
    assert "AI-Playtest dashboard" in body
    assert "Swarm observability" in body
    # argv step contents must NEVER leak into the page
    assert "aggregate_session_logs.py" not in body


def test_regen_unknown_id_blocked(client) -> None:
    r = client.post("/cross-repo/api/regen-dashboard", json={"id": "does-not-exist"})
    assert r.status_code == 400  # negative control: must block


def test_regen_non_regenerable_blocked(client) -> None:
    # 'mission-console' exists but has no regen block -> must block too
    r = client.post("/cross-repo/api/regen-dashboard", json={"id": "mission-console"})
    assert r.status_code == 400
