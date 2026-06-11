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


# --- STATUS-leg clock-leak fix (ADR-0039 ratify amendment P1 / dossier P1-1) -------------
#
# The stored severity of staleness-class sources (vault-eng-graph) is time-derived UPSTREAM
# (ingest passes `now` -> parse_eng_graph_moc folds a staleness band into severity +
# payload_hash). Rendering that severity leaked the calendar into the STATUS region: a
# byte-identical source could open a calendar-only PR. Fix: the STATUS render MASKS severity
# for those sources; every other column is content-derived.

def test_render_status_masks_time_derived_severity(tmp_path):
    """eng-graph severity cell is masked; content-based sources keep their severity."""
    from governor.reconcile import render_status_multi_repo
    store = _store(tmp_path, [
        {"source": "vault-eng-graph", "kind": "eng-graph", "severity": "warning",
         "summary": "eng-graph MOC: 2 repos indexed, last_verified 2026-06-01",
         "produced_at": "2026-06-01", "ref": "http://e", "payload_hash": "h1"},
        {"source": "vault-gap", "kind": "gap", "severity": "warning",
         "summary": "gap report", "produced_at": "2026-05-30", "ref": "http://g",
         "payload_hash": "h2"},
    ])
    out = render_status_multi_repo(store)
    eng_row = next(ln for ln in out.split("\n") if "vault-eng-graph" in ln)
    gap_row = next(ln for ln in out.split("\n") if "vault-gap" in ln)
    assert "warning" not in eng_row          # time-derived severity never rendered
    assert "masked" in eng_row               # masked cell is self-documenting
    assert "warning" in gap_row              # content-based severity untouched


def test_render_status_calendar_only_change_is_stable(tmp_path):
    """P1-1 regression (dossier probe): two stores identical EXCEPT the eng-graph
    time-derived severity (info vs warning -> distinct payload_hash) must render an
    IDENTICAL region -> the calendar alone can no longer open a STATUS PR."""
    from governor.reconcile import render_status_multi_repo
    base = {"source": "vault-eng-graph", "kind": "eng-graph",
            "summary": "eng-graph MOC: 2 repos indexed, last_verified 2026-06-01",
            "produced_at": "2026-06-01", "ref": "http://e"}
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    s_fresh = _store(tmp_path / "a", [dict(base, severity="info", payload_hash="06ebbb2bd685")])
    s_stale = _store(tmp_path / "b", [dict(base, severity="warning", payload_hash="5c8ee1a438b9")])
    assert render_status_multi_repo(s_fresh) == render_status_multi_repo(s_stale)


def test_render_status_stable_across_staleness_boundary(tmp_path):
    """Parser-routed P1-1 regression (harsh-review adopted): the REAL pipeline
    now -> parse_eng_graph_moc -> store -> render must be calendar-stable. Same MOC bytes,
    two `now` values straddling STALE_WARN_DAYS -> the parser emits DISTINCT severities +
    payload_hashes (the staleness band keeps working for the store/issue path), but the
    STATUS render must be byte-identical. Catches a future parser that leaks the calendar
    into summary/produced_at (the mask is severity-only)."""
    from datetime import date, timedelta
    from governor.parsers import parse_eng_graph_moc, STALE_WARN_DAYS
    from governor.reconcile import render_status_multi_repo
    from governor.store import SignalStore
    md = ("---\nlast_verified: 2026-06-01\n---\n"
          "<!-- eng-graph:auto -->\nrepo `vault`\nrepo `game`\n<!-- /eng-graph:auto -->")
    base = date.fromisoformat("2026-06-01")
    fresh = parse_eng_graph_moc(md, "http://moc", now=base + timedelta(days=1))
    stale = parse_eng_graph_moc(md, "http://moc", now=base + timedelta(days=STALE_WARN_DAYS + 10))
    assert fresh.severity != stale.severity            # band intact for store/issue actor
    assert fresh.payload_hash != stale.payload_hash    # distinct rows (worsened-delta intact)
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    s_fresh = SignalStore(tmp_path / "a" / "g.db")
    s_fresh.upsert(fresh)
    s_stale = SignalStore(tmp_path / "b" / "g.db")
    s_stale.upsert(stale)
    assert render_status_multi_repo(s_fresh) == render_status_multi_repo(s_stale)


def test_time_derived_severity_sources_pin_matches_parsers():
    """Pin: the masked-source set must track EXACTLY the parsers that accept a `now`
    parameter (the staleness-class). Adding a new now-aware parser without extending
    _TIME_DERIVED_SEVERITY_SOURCES (or vice versa) goes red here."""
    import inspect
    from governor import parsers
    from governor.reconcile import _TIME_DERIVED_SEVERITY_SOURCES
    now_aware = {
        name for name, fn in inspect.getmembers(parsers, inspect.isfunction)
        if name.startswith("parse_") and "now" in inspect.signature(fn).parameters
    }
    assert now_aware == {"parse_eng_graph_moc"}, (
        f"now-aware parsers changed ({sorted(now_aware)}): re-map them to "
        f"_TIME_DERIVED_SEVERITY_SOURCES in governor.reconcile"
    )
    assert _TIME_DERIVED_SEVERITY_SOURCES == frozenset({"vault-eng-graph"})
