"""TDD tests for governor.act -- run_r1 actor.

All tests use a fake issue_api -- network/gh NEVER hit.
"""
import re


def _make_store(tmp_path, signals=None):
    """Helper: create a SignalStore with optional pre-loaded signals."""
    from governor.store import SignalStore
    from governor.signals import Signal
    store = SignalStore(tmp_path / "g.db")
    for s in (signals or []):
        store.upsert(Signal(**s))
    return store


def _extract_body_key(body: str):
    """Extract escalate-key from an HTML comment in the body, or None."""
    m = re.search(r"<!-- escalate-key: ([0-9a-f]{16}) -->", body)
    return m.group(1) if m else None


def _fake_issue_api(find_open_result=None, created_num=42, updated_num=42,
                    raise_on_find_open=None):
    """Return a fake issue_api dict with call tracking.

    P0.1 contract: create(title, body, label) and update(issue_num, body).
    The body is already keyed by the caller; the fake does NOT append the key.

    Special sentinel for find_open_result:
      "from_stored" -- find_open reads body_key from the body stored by the
                       most recent create() call; simulates run-2 after run-1.

    If raise_on_find_open is set, find_open raises that exception (P1.2 test).
    """
    calls = {"find_open": [], "create": [], "update": []}
    _stored = {"body": None}  # body from most recent create, for "from_stored" sentinel

    def find_open():
        calls["find_open"].append(True)
        if raise_on_find_open is not None:
            raise raise_on_find_open
        if find_open_result == "from_stored":
            if _stored["body"] is None:
                return None
            return {"number": created_num, "body_key": _extract_body_key(_stored["body"])}
        return find_open_result

    def create(title, body, label):
        calls["create"].append({"title": title, "body": body, "label": label})
        _stored["body"] = body
        return created_num

    def update(issue_num, body):
        calls["update"].append({"issue_num": issue_num, "body": body})
        return updated_num

    return {"find_open": find_open, "create": create, "update": update}, calls


def test_run_r1_empty_store_is_noop(tmp_path):
    from governor.act import run_r1
    store = _make_store(tmp_path)
    api, calls = _fake_issue_api()
    result = run_r1(store, api)
    assert result == {"escalated": 0, "noop": True}
    assert calls["create"] == []
    assert calls["update"] == []


def test_run_r1_error_signal_creates_issue(tmp_path):
    from governor.act import run_r1
    store = _make_store(tmp_path, signals=[
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "3 critical errors", "payload_hash": "h1"},
    ])
    api, calls = _fake_issue_api(find_open_result=None, created_num=99)
    result = run_r1(store, api)
    assert result["escalated"] == 1
    assert result["action"] == "created"
    assert result["issue"] == 99
    assert len(calls["create"]) == 1
    assert calls["create"][0]["label"] == "governor-attention"


def test_run_r1_same_key_is_noop(tmp_path):
    """If the open issue already has the same escalate-key, no update is emitted."""
    from governor.act import run_r1
    from governor.digest import escalate_key
    store = _make_store(tmp_path, signals=[
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "err", "payload_hash": "h1"},
    ])
    # Compute what key run_r1 will produce for this escalated set.
    signals = store.latest_per_source()
    key = escalate_key(signals)
    api, calls = _fake_issue_api(
        find_open_result={"number": 7, "body_key": key},
    )
    result = run_r1(store, api)
    assert result["action"] == "noop"
    assert result["escalated"] == 1
    assert calls["update"] == []
    assert calls["create"] == []


def test_run_r1_changed_key_updates_issue(tmp_path):
    """If the open issue has a stale key, update is called."""
    from governor.act import run_r1
    store = _make_store(tmp_path, signals=[
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "err", "payload_hash": "h1"},
    ])
    api, calls = _fake_issue_api(
        find_open_result={"number": 7, "body_key": "000000000000dead"},  # stale
        updated_num=7,
    )
    result = run_r1(store, api)
    assert result["action"] == "updated"
    assert result["issue"] == 7
    assert len(calls["update"]) == 1
    assert calls["create"] == []


# ---------------------------------------------------------------------------
# P1.2: find_open raising must propagate (not swallowed into None)
# ---------------------------------------------------------------------------

def test_run_r1_find_open_raise_propagates(tmp_path):
    """P1.2: if find_open raises (e.g. gh list failed), run_r1 must propagate,
    NOT silently return None and call create (which would create a duplicate issue).
    """
    import pytest
    from governor.act import run_r1
    store = _make_store(tmp_path, signals=[
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "err", "payload_hash": "h1"},
    ])
    api, calls = _fake_issue_api(
        find_open_result=None,
        raise_on_find_open=RuntimeError("gh list failed"),
    )
    with pytest.raises(RuntimeError, match="gh list failed"):
        run_r1(store, api)
    # create must NOT have been called (no duplicate issue).
    assert calls["create"] == []


def test_lint_no_pr_merge_literals_in_gh_calls(tmp_path):
    """SOURCE-LINT TRIPWIRE (P1.3): real gh functions must not contain pr/merge/--admin
    string literals in their gh argv constructions.

    NOTE: this is a source-scan lint, NOT a runtime argv assertion.
    The real runtime guarantee is structural: the managed object is a GitHub Issue
    (which is unmergeable by design) combined with the restricted token scope used
    for the gh CLI. This scan is a cheap tripwire to catch accidental argv regressions.
    """
    import inspect
    from governor import act as act_module

    # Source-level guard: scan real gh functions for forbidden argv.
    forbidden = ("pr", "merge", "--admin", "--merge", "force-push")
    for fn_name in ("_real_create", "_real_update", "_real_find_open", "_gh"):
        fn = getattr(act_module, fn_name, None)
        if fn is None:
            continue
        src = inspect.getsource(fn)
        for token in forbidden:
            assert f'"{token}"' not in src, (
                f"{fn_name} contains forbidden token {token!r} in gh argv"
            )
            assert f"'{token}'" not in src, (
                f"{fn_name} contains forbidden token {token!r} in gh argv"
            )


# ---------------------------------------------------------------------------
# P0.1: create embeds key in body + run-2-noop idempotency invariant
# ---------------------------------------------------------------------------

def test_run_r1_create_embeds_key_in_body(tmp_path):
    """P0.1: the body passed to create() must contain <!-- escalate-key: HEX -->."""
    from governor.act import run_r1
    store = _make_store(tmp_path, signals=[
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "err", "payload_hash": "h1"},
    ])
    api, calls = _fake_issue_api(find_open_result=None, created_num=10)
    run_r1(store, api)
    assert len(calls["create"]) == 1
    body = calls["create"][0]["body"]
    assert _extract_body_key(body) is not None, (
        "create() body must embed <!-- escalate-key: HEX --> for idempotency"
    )


def test_run_r1_run2_same_signals_is_noop(tmp_path):
    """P0.1 idempotency invariant: run-1 creates; run-2 with same signals -> noop, NOT update.

    The fake find_open extracts body_key from the body stored by the create() call,
    proving that the key embedded in the body by run_r1 is sufficient for
    idempotency on run-2 without any additional update step.
    """
    from governor.act import run_r1
    store = _make_store(tmp_path, signals=[
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "err", "payload_hash": "h1"},
    ])
    # "from_stored" sentinel: find_open returns the body_key stored by the first create.
    api, calls = _fake_issue_api(find_open_result="from_stored", created_num=55)

    # Run 1 -- should create.
    r1 = run_r1(store, api)
    assert r1["action"] == "created"
    assert len(calls["create"]) == 1

    # Run 2 -- same store, same signals: must be noop (NOT update).
    r2 = run_r1(store, api)
    assert r2["action"] == "noop", (
        f"run-2 with identical signals must be noop, got {r2['action']!r}"
    )
    assert len(calls["create"]) == 1  # no second create
    assert len(calls["update"]) == 0  # no update


# ---------------------------------------------------------------------------
# Least-privilege token (deferred R1-spec hardening): the actor's gh CLI uses a
# dedicated issues:write-scoped token (GOVERNOR_ISSUE_TOKEN) via the child env,
# never argv, instead of the ambient repo-scope `gh auth token`.
# ---------------------------------------------------------------------------

def test_subprocess_env_injects_least_priv_token_when_set():
    """When GOVERNOR_ISSUE_TOKEN is set, the actor's subprocess env forces gh to
    use it via GH_TOKEN (not argv -> no CWE-214 leak), preserving the rest of env."""
    from governor.act import _subprocess_env
    env = _subprocess_env({"PATH": "/usr/bin", "GOVERNOR_ISSUE_TOKEN": "ghp_least_priv"})
    assert env is not None
    assert env["GH_TOKEN"] == "ghp_least_priv"
    assert env["PATH"] == "/usr/bin"


def test_subprocess_env_returns_none_when_token_absent():
    """Without GOVERNOR_ISSUE_TOKEN, return None -> subprocess inherits the ambient
    gh auth (current behavior, non-breaking). Blank/whitespace also counts as absent."""
    from governor.act import _subprocess_env
    assert _subprocess_env({"PATH": "/usr/bin"}) is None
    assert _subprocess_env({"GOVERNOR_ISSUE_TOKEN": "   "}) is None
