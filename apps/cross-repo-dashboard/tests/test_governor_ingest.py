def test_raw_fetch_returns_text_and_raises_for_status(monkeypatch):
    from governor import ingest
    from unittest.mock import MagicMock
    resp = MagicMock()
    resp.text = "body-payload"
    mock_get = MagicMock(return_value=resp)
    monkeypatch.setattr(ingest.requests, "get", mock_get)
    out = ingest.raw_fetch("https://example/x")
    assert out == "body-payload"
    resp.raise_for_status.assert_called_once()
    mock_get.assert_called_once()

def test_main_runs_ingest_and_returns_zero(monkeypatch, tmp_path):
    from governor import ingest
    import governor.store as store_mod
    from unittest.mock import MagicMock
    # Avoid touching the real governor.db / network: stub the store + ingest_all.
    monkeypatch.setattr(store_mod, "SignalStore", lambda db: MagicMock())
    called = {}

    def fake_ingest_all(store, fetcher=None):
        called["ran"] = True
        return {"ingested": 2, "new": 0, "errors": 0}

    monkeypatch.setattr(ingest, "ingest_all", fake_ingest_all)
    rc = ingest.main()
    assert rc == 0
    assert called.get("ran") is True

def test_ingest_all_uses_injected_fetcher_and_persists(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")

    fixtures = {
        "game-governance-drift": '{"generated_at":"2026-05-25T07:19:51+00:00","summary":{"total":2,"errors":0,"warnings":2},"issues":[]}',
        "evo-swarm-digest": "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n",
    }

    def fake_fetcher(url: str) -> str:
        if "Game/main/reports" in url:
            return fixtures["game-governance-drift"]
        if "evo-swarm" in url:
            return fixtures["evo-swarm-digest"]
        raise AssertionError(f"unexpected url {url}")

    result = ingest_all(store, fetcher=fake_fetcher)
    assert result["ingested"] == 2
    assert result["new"] == 2
    sources = {r["source"] for r in store.latest_per_source()}
    assert sources == {"game-governance-drift", "evo-swarm-digest"}

def test_ingest_all_records_advisory_on_new_only(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    fx = '{"generated_at":"2026-05-25T07:19:51+00:00","summary":{"total":2,"errors":0,"warnings":2},"issues":[]}'
    digest = "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n"

    def fetcher(url):
        return fx if "Game/main/reports" in url else digest

    ingest_all(store, fetcher=fetcher)             # first run -> 2 new -> 2 advisory
    ingest_all(store, fetcher=fetcher)             # second run -> unchanged -> 0 advisory
    assert len(store.auto_observed_recent(limit=50)) == 2

def test_ingest_all_one_source_failure_does_not_abort_others(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    digest = "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n"

    def fetcher(url):
        if "Game/main/reports" in url:
            raise RuntimeError("network down")
        return digest

    result = ingest_all(store, fetcher=fetcher)
    assert result["errors"] == 1
    assert result["ingested"] == 1   # evo-swarm still ingested

def test_governor_route_renders(tmp_path, monkeypatch):
    import sys
    from governor.store import SignalStore
    from governor.signals import Signal

    # Re-import app with a route decorator that returns the original function,
    # so app.governor_pane is the REAL view (matches test_coord_event_auth.py).
    if "app" in sys.modules:
        del sys.modules["app"]
    mock_flask = sys.modules["flask"]

    def mock_route(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

    mock_flask.Flask.return_value.route = mock_route
    mock_flask.Blueprint.return_value.route = mock_route
    import app as appmod

    # point the route at a temp DB with one signal
    db = tmp_path / "g.db"
    store = SignalStore(db)
    store.upsert(Signal(source="game-governance-drift", kind="drift",
                        severity="warning", summary="0 errors, 297 warnings",
                        counts={"warnings": 297}, payload_hash="h1"))
    monkeypatch.setattr(appmod, "GOVERNOR_DB", db)
    # flask is mocked; render_template is a MagicMock, so we assert it was called
    appmod.governor_pane()
    appmod.render_template.assert_called()
    args, kwargs = appmod.render_template.call_args
    assert args[0] == "cr_governor.html"
    assert any(s["source"] == "game-governance-drift" for s in kwargs["signals"])
    assert kwargs["acted_count"] == 0
