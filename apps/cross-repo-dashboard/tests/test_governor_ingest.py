def test_resolve_evo_latest_url_picks_newest():
    from governor.ingest import resolve_evo_latest_url
    listing = [
        {"name": "EXPORT-FOR-GAME-REPO-2026-04-27.md"},
        {"name": "EXPORT-FOR-GAME-REPO-2026-05-27.md"},
        {"name": "README.md"},
    ]
    url = resolve_evo_latest_url(lister=lambda _u: listing)
    assert url.endswith("/docs/exports/EXPORT-FOR-GAME-REPO-2026-05-27.md")
    assert url.startswith("https://raw.githubusercontent.com/MasterDD-L34D/evo-swarm/main/")

def test_resolve_evo_latest_url_none_when_empty():
    from governor.ingest import resolve_evo_latest_url
    assert resolve_evo_latest_url(lister=lambda _u: []) is None

def test_gh_get_json_sends_correct_headers(monkeypatch):
    from governor import ingest
    from unittest.mock import MagicMock
    resp = MagicMock()
    resp.json.return_value = [{"name": "file.md"}]
    mock_get = MagicMock(return_value=resp)
    monkeypatch.setattr(ingest.requests, "get", mock_get)
    out = ingest.gh_get_json("https://api.github.com/test")
    assert out == [{"name": "file.md"}]
    resp.raise_for_status.assert_called_once()
    call_kwargs = mock_get.call_args
    headers = call_kwargs[1]["headers"] if "headers" in call_kwargs[1] else call_kwargs[0][1]
    assert "application/vnd.github+json" in headers.get("Accept", "")

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

    def fake_ingest_all(store, fetcher=None, json_getter=None):
        called["ran"] = True
        return {"ingested": 3, "new": 0, "errors": 0}

    monkeypatch.setattr(ingest, "ingest_all", fake_ingest_all)
    rc = ingest.main()
    assert rc == 0
    assert called.get("ran") is True

def test_ingest_all_uses_injected_fetcher_and_persists(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    fetcher, json_getter = _fakes()
    result = ingest_all(store, fetcher=fetcher, json_getter=json_getter)
    assert result["ingested"] == 2
    assert result["new"] == 2
    sources = {r["source"] for r in store.latest_per_source()}
    assert sources == {"game-governance-drift", "game-sot-drift"}

def test_ingest_all_records_advisory_on_new_only(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    fetcher, json_getter = _fakes()
    ingest_all(store, fetcher=fetcher, json_getter=json_getter)   # first run -> 2 new -> 2 advisory
    ingest_all(store, fetcher=fetcher, json_getter=json_getter)   # second run -> unchanged -> 0 advisory
    assert len(store.auto_observed_recent(limit=50)) == 2

def test_ingest_all_one_source_failure_does_not_abort_others(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    fetcher, json_getter = _fakes()

    def json_getter_sot_fails(url):
        if "labels=sot-drift-candidate" in url:
            raise RuntimeError("gh api down")
        return json_getter(url)

    result = ingest_all(store, fetcher=fetcher, json_getter=json_getter_sot_fails)
    assert result["errors"] == 1
    assert result["ingested"] == 1   # game-governance-drift still ingested (evo deferred to Fase-1c)

def _fakes():
    drift = '{"generated_at":"2026-05-25T07:19:51+00:00","summary":{"total":2,"errors":0,"warnings":2},"issues":[]}'
    digest = "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n"
    def fetcher(url):
        if "reports/docs/governance_drift" in url:
            return drift
        if "EXPORT-FOR-GAME-REPO" in url:
            return digest
        raise AssertionError(f"unexpected raw url {url}")
    def json_getter(url):
        if "contents/docs/exports" in url:
            return [{"name": "EXPORT-FOR-GAME-REPO-2026-05-27.md"}]
        if "labels=sot-drift-candidate" in url:
            return [{"number": 2477, "title": "x", "state": "OPEN", "updatedAt": "2026-06-01T20:51:08Z"}]
        raise AssertionError(f"unexpected json url {url}")
    return fetcher, json_getter


def test_produce_evo_dynamic_resolves_dated_url(tmp_path):
    """Dormant evo-dynamic dispatch branch (reactivated Fase-1c): _produce resolves
    the dated digest URL via json_getter, then fetches + parses it into a Signal."""
    from governor.ingest import _produce
    fetcher, json_getter = _fakes()
    resolved_urls = []

    def tracking_fetcher(url):
        resolved_urls.append(url)
        return fetcher(url)

    sig = _produce("evo-swarm-digest", "evo-dynamic", tracking_fetcher, json_getter)
    assert sig.source == "evo-swarm-digest"
    assert sig.produced_at == "2026-05-27"          # parsed from the dated digest body
    assert "2026-05-27" in sig.ref                  # URL resolved from listing, not static
    evo_urls = [u for u in resolved_urls if "EXPORT-FOR-GAME-REPO" in u]
    assert len(evo_urls) == 1

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
