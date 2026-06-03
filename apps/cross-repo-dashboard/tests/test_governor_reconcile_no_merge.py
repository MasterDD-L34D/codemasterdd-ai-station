"""TDD tests for the REAL gh_api builder -- the LOAD-BEARING merge-block (spec sec 6.2).

codemasterdd is a free-tier PRIVATE repo with NO branch protection (gh api
branches/main/protection -> HTTP 403). So the merge-block is CODE: the REAL open_or_update_pr
command builder must NEVER emit a merge route/flag. We pin it TWO ways: (1) a runtime
recording-transport test that drives the REAL builder through create AND reuse and asserts no
recorded HTTP call hits a merge route; (2) a source-scan tripwire. Network/gh NEVER hit.
"""
import re


def _recorder(responses):
    """(http_fn, calls). http_fn pops a canned (status, data) per call, recording (method, url).
    Drives the REAL open_or_update_pr with NO network."""
    calls = []
    seq = list(responses)

    def http(method, url, token=None, json_body=None, timeout=20):
        calls.append({"method": method, "url": url})
        return seq.pop(0) if seq else (200, {})

    return http, calls


def test_uuid7_format():
    from governor.reconcile import _gen_uuid7
    u = _gen_uuid7()
    assert re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", u)


def test_real_get_file_returns_empty_on_404(monkeypatch):
    from governor import reconcile
    http, _ = _recorder([(404, {"message": "Not Found"})])
    monkeypatch.setattr(reconcile, "_http", http)
    monkeypatch.setattr(reconcile, "_ambient_token", lambda environ=None: "t")
    assert reconcile._real_get_file("MasterDD-L34D/vault", "Atlas/lint-status.md") == ""


def test_real_get_file_raises_on_non_200_non_404(monkeypatch):
    from governor import reconcile
    http, _ = _recorder([(500, {"message": "boom"})])
    monkeypatch.setattr(reconcile, "_http", http)
    monkeypatch.setattr(reconcile, "_ambient_token", lambda environ=None: "t")
    try:
        reconcile._real_get_file("MasterDD-L34D/vault", "Atlas/lint-status.md")
        assert False, "expected RuntimeError on HTTP 500"
    except RuntimeError:
        pass


def test_real_open_or_update_pr_never_emits_merge_route(monkeypatch):
    """LOAD-BEARING: drive the REAL builder through the create path; assert NO recorded HTTP
    call hits a merge route, and only read/create/update verbs are used."""
    from governor import reconcile
    monkeypatch.setattr(reconcile, "_write_token", lambda environ=None: "wtok")
    http, calls = _recorder([
        (200, {"object": {"sha": "basesha"}}),            # GET base ref
        (201, {}),                                         # POST create branch ref
        (404, {"message": "Not Found"}),                   # GET contents?ref=branch (new file)
        (201, {"content": {}}),                            # PUT contents
        (200, []),                                         # GET open prs (none)
        (201, {"number": 7, "html_url": "http://pr/7"}),   # POST create pr
    ])
    monkeypatch.setattr(reconcile, "_http", http)
    out = reconcile._real_open_or_update_pr(
        "MasterDD-L34D/codemasterdd-ai-station",
        "auto/governor-reconcile-status-multi-repo", "main",
        "STATUS_MULTI_REPO.md", "NEW CONTENT", "status-multi-repo")
    assert out["action"] == "created" and out["number"] == 7
    for c in calls:
        assert "/merge" not in c["url"], f"merge route emitted: {c}"
    assert all(c["method"] in ("GET", "POST", "PUT") for c in calls)


def test_real_open_or_update_pr_reuse_path_also_no_merge(monkeypatch):
    """Reuse path (an open PR already exists for the branch): still NEVER a merge route."""
    from governor import reconcile
    monkeypatch.setattr(reconcile, "_write_token", lambda environ=None: "wtok")
    http, calls = _recorder([
        (200, {"object": {"sha": "basesha"}}),            # GET base ref
        (422, {"message": "Reference already exists"}),    # POST create branch ref (exists)
        (200, {"sha": "filesha", "encoding": "base64", "content": "b2xk"}),  # GET file ("old")
        (200, {"content": {}}),                            # PUT contents (content differs)
        (200, [{"number": 9, "html_url": "http://pr/9"}]), # GET open prs -> reuse 9
    ])
    monkeypatch.setattr(reconcile, "_http", http)
    out = reconcile._real_open_or_update_pr(
        "MasterDD-L34D/codemasterdd-ai-station",
        "auto/governor-reconcile-status-multi-repo", "main",
        "STATUS_MULTI_REPO.md", "NEW CONTENT", "status-multi-repo")
    assert out["action"] == "reused" and out["number"] == 9
    for c in calls:
        assert "/merge" not in c["url"], f"merge route emitted: {c}"


def test_real_open_or_update_pr_failclosed_without_write_token(monkeypatch):
    from governor import reconcile
    monkeypatch.setattr(reconcile, "_write_token", lambda environ=None: "")
    http, calls = _recorder([])
    monkeypatch.setattr(reconcile, "_http", http)
    try:
        reconcile._real_open_or_update_pr("MasterDD-L34D/vault", "auto/x", "main",
                                          "Atlas/lint-status.md", "C", "vault-lint-status")
        assert False, "expected RuntimeError when GOVERNOR_RECONCILE_TOKEN is unset"
    except RuntimeError as e:
        assert "GOVERNOR_RECONCILE_TOKEN" in str(e)
    assert calls == []   # never touched the network without the write token


def test_no_merge_source_scan():
    """Cheap tripwire (the test_governor_act.py convention): the real gh-builder source contains
    no merge ROUTE / FLAG literal. Scoped to '/merge' + flags so PR-body prose ('human-merge-only'
    / 'a human merges') does NOT false-positive."""
    import inspect
    from governor import reconcile
    forbidden = ("/merge", "--merge", "--admin", "--squash", "--rebase", "pr merge")
    for fn_name in ("_real_open_or_update_pr", "_real_get_file", "_http", "_commit_message"):
        src = inspect.getsource(getattr(reconcile, fn_name))
        for tok in forbidden:
            assert tok not in src, f"{fn_name} contains forbidden merge token {tok!r}"
