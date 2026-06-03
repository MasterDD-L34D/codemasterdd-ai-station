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
