"""Route smoke + tier gating for the OS console (Flask test client)."""
from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))

import pytest  # noqa: E402

import app as appmod  # noqa: E402


@pytest.fixture
def mock_external_deps():
    """Override conftest's autouse mock for this module only.

    The other tests in this package are hermetic and mock `flask` (via
    monkeypatch.setitem in conftest) so they can call route functions directly.
    These route-smoke tests instead drive a REAL Flask test client, which needs
    the real `flask` package (test_client() lazily imports `flask.testing`).
    `import app` already resolves in this env, so nothing needs mocking here.
    """
    yield


def client():
    return appmod.create_app().test_client()


def test_os_home_renders() -> None:
    r = client().get("/cross-repo/os")
    assert r.status_code == 200
    assert b"Agentic OS Console" in r.data


def test_root_redirects_to_os() -> None:
    r = client().get("/")
    assert r.status_code in (301, 302, 308)
    assert "/cross-repo/os" in r.headers.get("Location", "")


def test_run_action_unknown_id_400() -> None:
    r = client().post("/cross-repo/api/run-action", json={"id": "nope"})
    assert r.status_code == 400


def test_run_action_tier2_forbidden() -> None:
    r = client().post("/cross-repo/api/run-action", json={"id": "merge-main"})
    assert r.status_code == 403


def test_run_action_bad_param_rejected() -> None:
    # jules-dispatch requires repo in whitelist; a bogus repo must 400 before any exec
    r = client().post("/cross-repo/api/run-action", json={"id": "jules-dispatch", "repo": "evil; rm -rf"})
    assert r.status_code == 400
