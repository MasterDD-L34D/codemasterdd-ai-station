"""Route smoke + tier gating for the OS console (Flask test client)."""
from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))

import sys as _sys

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


def test_os_home_renders(monkeypatch) -> None:
    # stub the scheduled-task query so the route never shells out to PowerShell
    monkeypatch.setattr(
        appmod, "scheduled_task_health",
        lambda names, **kw: [{"name": n, "state": "Ready", "last_result": 0,
                              "last_run": None, "healthy": True} for n in names],
    )
    r = client().get("/cross-repo/os")
    assert r.status_code == 200
    assert b"Agentic OS Console" in r.data
    # the home now surfaces LIVE per-layer state, not just the static map
    assert b"stato vivo" in r.data
    assert b"PR flotta" in r.data
    assert b"s-ok" in r.data  # at least one layer rendered a live status badge


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
    # fleet-pr-status has a working `repo` param (whitelist); a bogus repo must
    # 400 BEFORE any subprocess runs (negative control for the param->argv path).
    r = client().post("/cross-repo/api/run-action", json={"id": "fleet-pr-status", "repo": "evil; rm -rf"})
    assert r.status_code == 400


def test_run_action_tier1_requires_secret(monkeypatch) -> None:
    # tier-1 (mutating) must fail closed when no server API_SECRET is set, even
    # though tier-0 stays open. 403, no wrapper invoked.
    monkeypatch.delenv("API_SECRET", raising=False)
    r = client().post("/cross-repo/api/run-action", json={"id": "create-draft-pr"})
    assert r.status_code == 403


def test_run_action_happy_path_hermetic(monkeypatch) -> None:
    # One real happy-path through /api/run-action: inject a trivial tier-0 action
    # whose fixed argv just prints "ok" (portable, no external tool), and assert
    # the endpoint returns ok:True with that output. Proves the exec path, not
    # just the 4xx guards.
    monkeypatch.delenv("API_SECRET", raising=False)
    trivial = {
        "id": "selftest-echo", "label": "selftest", "tier": 0, "area": "audit",
        "desc": "hermetic self-test", "cwd": str(APP_DIR), "timeout": 30,
        "ok_exit_codes": [0], "steps": [[_sys.executable, "-c", "print('ok')"]],
    }
    monkeypatch.setattr(appmod, "ACTIONS", list(appmod.ACTIONS) + [trivial])
    r = client().post("/cross-repo/api/run-action", json={"id": "selftest-echo"})
    assert r.status_code == 200
    payload = r.get_json()
    assert payload["ok"] is True
    assert "ok" in payload["output"]


def test_run_action_applies_whitelisted_param_to_argv(monkeypatch) -> None:
    # Positive control for the P1 fix: a valid whitelisted choice must actually be
    # APPENDED to argv server-side as [flag, value]. Without this, reverting the
    # param->argv apply would leave the suite green (bad-param still 400s, the
    # param-less happy-path still passes) -- so this locks the exact fixed behavior.
    monkeypatch.delenv("API_SECRET", raising=False)
    echo_args = {
        "id": "selftest-echoargs", "label": "selftest", "tier": 0, "area": "audit",
        "desc": "echo argv tail", "cwd": str(APP_DIR), "timeout": 30, "ok_exit_codes": [0],
        "steps": [[_sys.executable, "-c", "import sys; print(sys.argv[1:])"]],
        "params": [{"name": "repo", "flag": "--repo", "choices": ["SAFE-CHOICE-XYZ"]}],
    }
    monkeypatch.setattr(appmod, "ACTIONS", list(appmod.ACTIONS) + [echo_args])
    r = client().post("/cross-repo/api/run-action",
                      json={"id": "selftest-echoargs", "repo": "SAFE-CHOICE-XYZ"})
    assert r.status_code == 200
    payload = r.get_json()
    assert payload["ok"] is True
    # both the fixed flag and the whitelisted value must appear in the executed argv
    assert "--repo" in payload["output"] and "SAFE-CHOICE-XYZ" in payload["output"]


def test_run_action_keep_lines_filters_output(monkeypatch) -> None:
    # keep_lines is a display-only filter: only stdout lines matching a keyword are
    # shown (drops verbose body dumps). Cosmetic -- must not affect ok/exit handling.
    monkeypatch.delenv("API_SECRET", raising=False)
    # the dropped marker is assembled at runtime so it is NOT a contiguous literal in
    # the argv echo header (which is always shown) -- it can only reach the output via
    # stdout, which keep_lines filters out.
    act = {
        "id": "selftest-keep", "label": "x", "tier": 0, "area": "audit", "desc": "x",
        "cwd": str(APP_DIR), "timeout": 30, "ok_exit_codes": [0], "keep_lines": ["KEEP"],
        "steps": [[_sys.executable, "-c", "print('KEEP one'); print('ZZ'+'DROPPED'+'ZZ'); print('KEEP two')"]],
    }
    monkeypatch.setattr(appmod, "ACTIONS", list(appmod.ACTIONS) + [act])
    r = client().post("/cross-repo/api/run-action", json={"id": "selftest-keep"})
    assert r.status_code == 200
    out = r.get_json()["output"]
    assert "KEEP one" in out and "KEEP two" in out
    assert "ZZDROPPEDZZ" not in out
