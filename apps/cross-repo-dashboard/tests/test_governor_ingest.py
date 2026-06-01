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
    monkeypatch.setattr(store_mod, "SignalStore", lambda db: MagicMock())
    called = {}

    def fake_ingest_all(store, fetcher=None, json_getter=None, content_getter=None):
        called["ran"] = True
        return {"ingested": 6, "new": 0, "errors": 0}

    monkeypatch.setattr(ingest, "ingest_all", fake_ingest_all)
    rc = ingest.main()
    assert rc == 0
    assert called.get("ran") is True

def test_ingest_all_uses_injected_fetcher_and_persists(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    fetcher, json_getter, content_getter = _fakes()
    result = ingest_all(store, fetcher=fetcher, json_getter=json_getter, content_getter=content_getter)
    assert result["ingested"] == 6
    assert result["new"] == 6
    sources = {r["source"] for r in store.latest_per_source()}
    assert "game-governance-drift" in sources
    assert "game-sot-drift" in sources
    assert "evo-swarm-digest" in sources
    assert "vault-gap" in sources
    assert "vault-coherence" in sources
    assert "vault-whatsmissing" in sources

def test_ingest_all_records_advisory_on_new_only(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    fetcher, json_getter, content_getter = _fakes()
    ingest_all(store, fetcher=fetcher, json_getter=json_getter, content_getter=content_getter)
    ingest_all(store, fetcher=fetcher, json_getter=json_getter, content_getter=content_getter)
    assert len(store.auto_observed_recent(limit=50)) == 6

def test_ingest_all_one_source_failure_does_not_abort_others(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    fetcher, json_getter, content_getter = _fakes()

    def json_getter_sot_fails(url):
        if "labels=sot-drift-candidate" in url:
            raise RuntimeError("gh api down")
        return json_getter(url)

    result = ingest_all(store, fetcher=fetcher, json_getter=json_getter_sot_fails, content_getter=content_getter)
    assert result["errors"] == 1
    assert result["ingested"] == 5

def _fakes():
    drift_json = '{"generated_at":"2026-05-25T07:19:51+00:00","summary":{"total":2,"errors":0,"warnings":2},"issues":[]}'
    digest_text = "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n"
    gap_text = "# Gap-scan report 2026-06-01 (OD-048)\n## Summary\n- G4 orphan: **1**\n"
    coherence_text = "# Coherence-check 2026-06-01\n## Summary\n- broken links: **0**\n"
    whatsmissing_text = "# Whats-missing 2026-06-01\n## Summary\n- missing: **2**\n"

    evo_file_url = "https://api.github.com/repos/MasterDD-L34D/evo-swarm/contents/docs/exports/EXPORT-FOR-GAME-REPO-2026-05-27.md"
    gap_file_url = "https://api.github.com/repos/MasterDD-L34D/vault/contents/Extras/lint-reports/gap-2026-06-01.md"
    coherence_file_url = "https://api.github.com/repos/MasterDD-L34D/vault/contents/Extras/lint-reports/coherence-2026-06-01.md"
    whatsmissing_file_url = "https://api.github.com/repos/MasterDD-L34D/vault/contents/Extras/lint-reports/whatsmissing-2026-06-01.md"

    _content_map = {
        evo_file_url: digest_text,
        gap_file_url: gap_text,
        coherence_file_url: coherence_text,
        whatsmissing_file_url: whatsmissing_text,
    }

    def fetcher(url):
        if "reports/docs/governance_drift" in url:
            return drift_json
        raise AssertionError(f"unexpected raw url {url}")

    def json_getter(url):
        if "evo-swarm/contents/docs/exports" in url:
            return [{"name": "EXPORT-FOR-GAME-REPO-2026-05-27.md", "url": evo_file_url}]
        if "labels=sot-drift-candidate" in url:
            return [{"number": 2477, "title": "x", "state": "OPEN", "updatedAt": "2026-06-01T20:51:08Z"}]
        if "vault/contents/Extras/lint-reports" in url:
            return [
                {"name": "gap-2026-06-01.md", "url": gap_file_url},
                {"name": "coherence-2026-06-01.md", "url": coherence_file_url},
                {"name": "whatsmissing-2026-06-01.md", "url": whatsmissing_file_url},
            ]
        raise AssertionError(f"unexpected json url {url}")

    def content_getter(url):
        if url in _content_map:
            return _content_map[url]
        raise AssertionError(f"unexpected content url {url}")

    return fetcher, json_getter, content_getter


def test_resolve_latest_in_dir_picks_newest():
    from governor.ingest import resolve_latest_in_dir
    listing = [
        {"name": "gap-2026-05-01.md", "url": "https://api.github.com/repos/x/vault/contents/gap-2026-05-01.md"},
        {"name": "gap-2026-06-01.md", "url": "https://api.github.com/repos/x/vault/contents/gap-2026-06-01.md"},
        {"name": "coherence-2026-06-01.md", "url": "https://api.github.com/repos/x/vault/contents/coherence-2026-06-01.md"},
    ]
    url = resolve_latest_in_dir("https://api.github.com/x", "gap-", getter=lambda _u: listing)
    assert url == "https://api.github.com/repos/x/vault/contents/gap-2026-06-01.md"


def test_gh_get_file_content_decodes_base64():
    import json
    from pathlib import Path
    from governor.ingest import gh_get_file_content
    obj = json.loads((Path(__file__).resolve().parent / "fixtures" / "contents_file_b64.json").read_text())
    text = gh_get_file_content("https://api.github.com/x", getter=lambda _u: obj)
    assert text == "hello vault"


def test_gh_token_prefers_env_over_subprocess(monkeypatch):
    import os
    from governor.ingest import _gh_token
    monkeypatch.setenv("GH_TOKEN", "tok-from-env")
    called = {}
    import subprocess as sp
    real_run = sp.run

    def spy_run(*a, **kw):
        called["ran"] = True
        return real_run(*a, **kw)

    monkeypatch.setattr("subprocess.run", spy_run)
    tok = _gh_token()
    assert tok == "tok-from-env"
    assert not called.get("ran"), "_gh_token should not call subprocess when GH_TOKEN is set"


def test_produce_evo_private_via_content_getter():
    from governor.ingest import _produce
    digest_text = "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n"
    evo_file_url = "https://api.github.com/repos/evo-swarm/contents/docs/exports/EXPORT-FOR-GAME-REPO-2026-05-27.md"

    def json_getter(url):
        if "contents/docs/exports" in url:
            return [{"name": "EXPORT-FOR-GAME-REPO-2026-05-27.md", "url": evo_file_url}]
        raise AssertionError(f"unexpected json url {url}")

    def content_getter(url):
        if url == evo_file_url:
            return digest_text
        raise AssertionError(f"unexpected content url {url}")

    src = {"id": "evo-swarm-digest", "style": "evo-private"}
    sig = _produce(src, fetcher=None, json_getter=json_getter, content_getter=content_getter)
    assert sig.source == "evo-swarm-digest"
    assert sig.produced_at == "2026-05-27"


def test_produce_vault_source_via_content_getter():
    from governor.ingest import _produce
    gap_file_url = "https://api.github.com/repos/vault/contents/Extras/lint-reports/gap-2026-06-01.md"
    gap_text = "# Gap-scan report 2026-06-01\n## Summary\n- G4 orphan: **1**\n"

    def json_getter(url):
        if "vault/contents/Extras/lint-reports" in url:
            return [{"name": "gap-2026-06-01.md", "url": gap_file_url}]
        raise AssertionError(f"unexpected json url {url}")

    def content_getter(url):
        if url == gap_file_url:
            return gap_text
        raise AssertionError(f"unexpected content url {url}")

    src = {"id": "vault-gap", "style": "vault", "prefix": "gap-", "kind": "gap"}
    sig = _produce(src, fetcher=None, json_getter=json_getter, content_getter=content_getter)
    assert sig.source == "vault-gap"
    assert sig.kind == "gap"
    assert sig.produced_at == "2026-06-01"


def test_governor_route_renders(tmp_path, monkeypatch):
    import sys
    from governor.store import SignalStore
    from governor.signals import Signal

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

    db = tmp_path / "g.db"
    store = SignalStore(db)
    store.upsert(Signal(source="game-governance-drift", kind="drift",
                        severity="warning", summary="0 errors, 297 warnings",
                        counts={"warnings": 297}, payload_hash="h1"))
    monkeypatch.setattr(appmod, "GOVERNOR_DB", db)
    appmod.governor_pane()
    appmod.render_template.assert_called()
    args, kwargs = appmod.render_template.call_args
    assert args[0] == "cr_governor.html"
    assert any(s["source"] == "game-governance-drift" for s in kwargs["signals"])
    assert kwargs["acted_count"] == 0
