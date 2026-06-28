"""TDD tests for governor.reconcile.reconcile_actor -- the only new autonomy surface.

A FAKE gh_api is injected -- network/gh NEVER hit. The actor opens/updates ONE branch+PR per
drifted reconciler, NEVER merges, is fail-closed on GOVERNOR_RECONCILE_TOKEN, and isolates a
per-reconciler failure (mirrors ingest_all). environ is passed explicitly for determinism.
"""
TOKEN_ENV = {"GOVERNOR_RECONCILE_TOKEN": "fake_write_token"}
MK = ("<!-- GOVERNOR-SYNC:signals BEGIN -->", "<!-- GOVERNOR-SYNC:signals END -->")

SIGNALS = [{"source": "game-governance-drift", "kind": "drift", "severity": "error",
            "summary": "3 errors", "produced_at": "2026-06-01", "ref": "http://x",
            "payload_hash": "h1"}]


def _store(tmp_path, signals):
    from governor.store import SignalStore
    from governor.signals import Signal
    s = SignalStore(tmp_path / "g.db")
    for sig in signals:
        s.upsert(Signal(**sig))
    return s


def _fake_gh_api(files=None):
    files = files or {}
    state = {"branches": {}, "prs": {}, "seq": [100]}
    calls = {"get_file": [], "open_or_update_pr": []}

    def get_file(repo, path):
        calls["get_file"].append((repo, path))
        return files.get(repo, {}).get(path, "")

    def open_or_update_pr(repo, branch, base, path, content, rid):
        calls["open_or_update_pr"].append({"repo": repo, "branch": branch, "base": base,
                                           "path": path, "content": content, "id": rid})
        if branch in state["prs"]:
            if state["branches"].get(branch) == content:
                return {"number": state["prs"][branch], "action": "reused"}
            state["branches"][branch] = content
            return {"number": state["prs"][branch], "action": "updated"}
        num = state["seq"][0]
        state["seq"][0] += 1
        state["prs"][branch] = num
        state["branches"][branch] = content
        return {"number": num, "action": "created"}

    return {"get_file": get_file, "open_or_update_pr": open_or_update_pr}, calls, state


def _status_reconciler():
    from governor.reconcile import Reconciler, render_status_multi_repo
    return Reconciler(
        id="status-multi-repo", repo="MasterDD-L34D/codemasterdd-ai-station",
        path="STATUS_MULTI_REPO.md", marker=MK, render=render_status_multi_repo,
        anchor="# STATUS_MULTI_REPO",
    )


def test_actor_render_none_is_skipped(tmp_path):
    from governor.reconcile import reconcile_actor
    store = _store(tmp_path, [])          # empty -> render None
    api, calls, _ = _fake_gh_api()
    res = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    assert res["skipped"] and res["skipped"][0]["reason"] == "render-none"
    assert calls["open_or_update_pr"] == []


def test_actor_no_drift_is_unchanged_no_pr(tmp_path):
    from governor.reconcile import reconcile_actor, splice, render_status_multi_repo
    store = _store(tmp_path, SIGNALS)
    region = render_status_multi_repo(store)
    synced = splice("# STATUS_MULTI_REPO\n", MK, region, anchor="# STATUS_MULTI_REPO")
    api, calls, _ = _fake_gh_api({"MasterDD-L34D/codemasterdd-ai-station":
                                  {"STATUS_MULTI_REPO.md": synced}})
    res = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    assert res["unchanged"] and res["unchanged"][0]["id"] == "status-multi-repo"
    assert calls["open_or_update_pr"] == []


def test_actor_drift_opens_one_pr(tmp_path):
    from governor.reconcile import reconcile_actor
    store = _store(tmp_path, SIGNALS)
    api, calls, _ = _fake_gh_api({"MasterDD-L34D/codemasterdd-ai-station":
                                  {"STATUS_MULTI_REPO.md": "# STATUS_MULTI_REPO\nstale\n"}})
    res = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    assert len(res["opened"]) == 1
    assert res["opened"][0]["pr"]["action"] == "created"
    assert len(calls["open_or_update_pr"]) == 1
    c = calls["open_or_update_pr"][0]
    assert c["branch"] == "auto/governor-reconcile-status-multi-repo"
    assert c["base"] == "main"


def test_actor_rerun_same_state_reuses_pr(tmp_path):
    from governor.reconcile import reconcile_actor
    store = _store(tmp_path, SIGNALS)
    files = {"MasterDD-L34D/codemasterdd-ai-station":
             {"STATUS_MULTI_REPO.md": "# STATUS_MULTI_REPO\nstale\n"}}
    api, calls, _ = _fake_gh_api(files)   # main stays stale (PR not merged)
    r1 = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    r2 = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    assert r1["opened"][0]["pr"]["action"] == "created"
    assert r2["opened"][0]["pr"]["action"] == "reused"      # no NEW pr
    assert r1["opened"][0]["pr"]["number"] == r2["opened"][0]["pr"]["number"]


def test_actor_token_unset_is_failclosed_skip(tmp_path):
    from governor.reconcile import reconcile_actor
    store = _store(tmp_path, SIGNALS)
    api, calls, _ = _fake_gh_api({"MasterDD-L34D/codemasterdd-ai-station":
                                  {"STATUS_MULTI_REPO.md": "# STATUS_MULTI_REPO\nstale\n"}})
    res = reconcile_actor(store, [_status_reconciler()], api, environ={})   # NO token
    assert res["skipped"] and res["skipped"][0]["reason"] == "no-token"
    assert calls["open_or_update_pr"] == []      # NEVER called without the write token


def test_actor_one_reconciler_error_is_isolated(tmp_path):
    from governor.reconcile import reconcile_actor, Reconciler
    def boom(store):
        raise RuntimeError("render kaboom")
    bad = Reconciler(id="bad", repo="MasterDD-L34D/codemasterdd-ai-station",
                     path="docs/research/scratch.md", marker=MK, render=boom)
    store = _store(tmp_path, SIGNALS)
    api, calls, _ = _fake_gh_api({"MasterDD-L34D/codemasterdd-ai-station":
                                  {"STATUS_MULTI_REPO.md": "# STATUS_MULTI_REPO\nstale\n"}})
    res = reconcile_actor(store, [bad, _status_reconciler()], api, environ=TOKEN_ENV)
    assert any(e["id"] == "bad" for e in res["errors"])
    assert len(res["opened"]) == 1               # the good one still proceeded


def test_actor_self_heals_binary_contaminated_source(tmp_path):
    """vault #260: the governor-owned doc carries trailing NUL bytes (binary). get_file decodes
    them (errors='replace' -> U+0000); the actor must treat that as DRIFT and open a PR whose
    content is CLEAN text -- so the contamination self-heals on merge instead of propagating
    forward forever (the builder faithfully preserves whatever it decodes)."""
    from governor.reconcile import reconcile_actor, splice, render_status_multi_repo
    store = _store(tmp_path, SIGNALS)
    region = render_status_multi_repo(store)
    synced = splice("# STATUS_MULTI_REPO\n", MK, region, anchor="# STATUS_MULTI_REPO")
    contaminated = synced + ("\x00" * 13)   # region already in-sync BUT binary-contaminated EOF
    api, calls, _ = _fake_gh_api({"MasterDD-L34D/codemasterdd-ai-station":
                                  {"STATUS_MULTI_REPO.md": contaminated}})
    res = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    assert len(res["opened"]) == 1          # contamination alone counts as drift -> opens a PR
    put = calls["open_or_update_pr"][0]["content"]
    assert "\x00" not in put                # the opened PR carries CLEAN text (self-heal)


def test_build_reconcilers_two_legs_nondoctrine_targets():
    from governor.reconcile import build_reconcilers
    recs = build_reconcilers()
    by_id = {r.id: r for r in recs}
    assert set(by_id) == {"status-multi-repo", "vault-lint-status"}
    assert by_id["status-multi-repo"].repo.endswith("/codemasterdd-ai-station")
    assert by_id["status-multi-repo"].path == "STATUS_MULTI_REPO.md"
    assert by_id["vault-lint-status"].repo.endswith("/vault")
    assert by_id["vault-lint-status"].path == "Atlas/lint-status.md"
    assert by_id["vault-lint-status"].create_header is not None       # NEW doc
    assert by_id["status-multi-repo"].marker[0] == "<!-- GOVERNOR-SYNC:signals BEGIN -->"
    assert by_id["vault-lint-status"].marker[0] == "<!-- GOVERNOR-SYNC:lint BEGIN -->"


def test_build_reconcilers_targets_are_not_doctrine():
    from governor.reconcile import build_reconcilers, is_doctrine
    for r in build_reconcilers():
        assert is_doctrine(r.path, r.repo) is False


def test_real_gh_api_exposes_two_callables():
    from governor.reconcile import real_gh_api
    api = real_gh_api()
    assert callable(api["get_file"]) and callable(api["open_or_update_pr"])
