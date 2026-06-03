"""TDD tests for governor.reconcile render legs -- deterministic + CLOCK-FREE.

The render output is a pure function of the signal store state. No wall-clock / no time-derived
value (spec sec 6.3); the vault leg severity is content-based (parse_vault_report, sec 5.2).
Network/gh NEVER hit (the store is a tmp SQLite db).
"""


def _store(tmp_path, signals):
    from governor.store import SignalStore
    from governor.signals import Signal
    s = SignalStore(tmp_path / "g.db")
    for sig in signals:
        s.upsert(Signal(**sig))
    return s


# --- status-multi-repo leg (Task 4) ----------------------------------------

def test_render_status_none_on_empty_store(tmp_path):
    from governor.reconcile import render_status_multi_repo
    assert render_status_multi_repo(_store(tmp_path, [])) is None


def test_render_status_deterministic_table(tmp_path):
    from governor.reconcile import render_status_multi_repo
    store = _store(tmp_path, [
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "3 errors", "produced_at": "2026-06-01", "ref": "http://x",
         "payload_hash": "h1"},
        {"source": "vault-gap", "kind": "gap", "severity": "warning",
         "summary": "gap report", "produced_at": "2026-05-30", "ref": "http://y",
         "payload_hash": "h2"},
    ])
    out1 = render_status_multi_repo(store)
    out2 = render_status_multi_repo(store)
    assert out1 == out2                       # deterministic
    assert "| source | severity | summary | produced_at | ref |" in out1
    assert "game-governance-drift" in out1 and "vault-gap" in out1
    # ordered by source (game- before vault-)
    assert out1.index("game-governance-drift") < out1.index("vault-gap")


def test_render_status_is_clock_free_source_scan():
    import inspect
    from governor.reconcile import render_status_multi_repo
    src = inspect.getsource(render_status_multi_repo)
    for forbidden in ("datetime", "date.today", "time.time", "time()", "now(", " now ", "utcnow"):
        assert forbidden not in src, f"clock token {forbidden!r} in render (must be clock-free)"


# --- vault-lint-status leg (Task 5) ----------------------------------------

def test_render_vault_lint_none_when_no_lint_sources(tmp_path):
    from governor.reconcile import render_vault_lint_status
    store = _store(tmp_path, [
        {"source": "game-governance-drift", "kind": "drift", "severity": "ok",
         "summary": "x", "payload_hash": "h"},
    ])
    assert render_vault_lint_status(store) is None


def test_render_vault_lint_filters_to_three_lint_sources(tmp_path):
    from governor.reconcile import render_vault_lint_status
    store = _store(tmp_path, [
        {"source": "vault-gap", "kind": "gap", "severity": "warning",
         "summary": "gap report 2026-05-30: 2/3 metrics nonzero", "produced_at": "2026-05-30",
         "ref": "http://g", "payload_hash": "h1"},
        {"source": "vault-coherence", "kind": "coherence", "severity": "ok",
         "summary": "coherence present", "produced_at": "2026-05-30", "ref": "http://c",
         "payload_hash": "h2"},
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "noise", "payload_hash": "h3"},
    ])
    out = render_vault_lint_status(store)
    assert "| report | severity | summary | produced_at | ref |" in out
    assert "gap" in out and "coherence" in out
    assert "game-governance-drift" not in out   # filtered out
    assert "noise" not in out


def test_render_vault_lint_severity_is_content_based_not_clock(tmp_path):
    """Two stores with IDENTICAL produced_at but DIFFERENT content-severity must render
    DIFFERENT severity cells -> severity tracks content (BLOCK/WARN/metrics), not the clock."""
    from governor.reconcile import render_vault_lint_status
    base = {"source": "vault-gap", "kind": "gap", "produced_at": "2026-05-30",
            "ref": "http://g"}
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    s_ok = _store(tmp_path / "a", [dict(base, severity="ok", summary="present",
                                        payload_hash="ok")])
    s_err = _store(tmp_path / "b", [dict(base, severity="error", summary="BLOCK 4 WARN 1",
                                         payload_hash="er")])
    out_ok = render_vault_lint_status(s_ok)
    out_err = render_vault_lint_status(s_err)
    assert "ok" in out_ok and "error" in out_err
    assert out_ok != out_err


def test_render_vault_lint_is_clock_free_source_scan():
    import inspect
    from governor.reconcile import render_vault_lint_status
    src = inspect.getsource(render_vault_lint_status)
    for forbidden in ("datetime", "date.today", "time.time", "time()", "now(", " now ", "utcnow"):
        assert forbidden not in src, f"clock token {forbidden!r} in vault render"
