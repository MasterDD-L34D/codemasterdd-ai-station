"""TDD tests for the REAL gh_api builder -- the LOAD-BEARING merge-block (spec sec 6.2).

codemasterdd is a free-tier PRIVATE repo with NO branch protection (gh api
branches/main/protection -> HTTP 403). So the merge-block is CODE: the REAL open_or_update_pr
command builder must NEVER emit a merge route/flag. We pin it TWO ways: (1) a runtime
recording-transport test that drives the REAL builder through create AND reuse and asserts no
recorded HTTP call hits a merge route; (2) a source-scan tripwire. Network/gh NEVER hit.
"""
import re


def _recorder(responses):
    """(http_fn, calls). http_fn pops a canned (status, data) per call, recording
    (method, url, body). Drives the REAL open_or_update_pr with NO network."""
    calls = []
    seq = list(responses)

    def http(method, url, token=None, json_body=None, timeout=20):
        calls.append({"method": method, "url": url, "body": json_body})
        return seq.pop(0) if seq else (200, {})

    http.remaining = seq   # tests assert it drains: a DROPPED http call must also go red
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
        (201, {}),                                         # POST create branch ref (fresh)
        (200, []),                                         # GET open prs (none)
        (404, {"message": "Not Found"}),                   # GET contents?ref=branch (new file)
        (201, {"content": {}}),                            # PUT contents
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
    # fresh-branch path: never a ref force-reset (PATCH is the GC-only verb)
    assert all(c["method"] in ("GET", "POST", "PUT") for c in calls)
    assert not http.remaining, "canned responses under-consumed (an http call was dropped)"


def test_real_open_or_update_pr_reuse_path_also_no_merge(monkeypatch):
    """Reuse path (an open PR already exists for the branch): still NEVER a merge route,
    and NEVER a ref force-reset (the open PR's branch is live, not stale -- anti-churn)."""
    from governor import reconcile
    monkeypatch.setattr(reconcile, "_write_token", lambda environ=None: "wtok")
    http, calls = _recorder([
        (200, {"object": {"sha": "basesha"}}),            # GET base ref
        (422, {"message": "Reference already exists"}),    # POST create branch ref (exists)
        (200, [{"number": 9, "html_url": "http://pr/9"}]), # GET open prs -> live branch, reuse 9
        (200, {"sha": "filesha", "encoding": "base64", "content": "b2xk"}),  # GET file ("old")
        (200, {"content": {}}),                            # PUT contents (content differs)
    ])
    monkeypatch.setattr(reconcile, "_http", http)
    out = reconcile._real_open_or_update_pr(
        "MasterDD-L34D/codemasterdd-ai-station",
        "auto/governor-reconcile-status-multi-repo", "main",
        "STATUS_MULTI_REPO.md", "NEW CONTENT", "status-multi-repo")
    assert out["action"] == "reused" and out["number"] == 9
    for c in calls:
        assert "/merge" not in c["url"], f"merge route emitted: {c}"
    assert all(c["method"] != "PATCH" for c in calls), "live open-PR branch must NOT be reset"
    assert not http.remaining, "canned responses under-consumed (an http call was dropped)"


def test_real_open_or_update_pr_resets_stale_branch_without_open_pr(monkeypatch):
    """Stale-branch GC (vault #258 incident 2026-06-11): the actor's contract is
    branch-exists <=> open-PR-pending. A branch that exists (422) with NO open PR is a
    leftover from an already-merged/closed PR (vault has no delete-on-merge): reusing it
    keeps the OLD merge-base -> add/add conflict with main (#252 -> #258). The builder must
    force-reset the ref to the CURRENT base sha BEFORE writing, so the new PR diffs cleanly
    against today's main."""
    from governor import reconcile
    monkeypatch.setattr(reconcile, "_write_token", lambda environ=None: "wtok")
    http, calls = _recorder([
        (200, {"object": {"sha": "basesha"}}),            # GET base ref
        (422, {"message": "Reference already exists"}),    # POST create branch ref (stale)
        (200, []),                                         # GET open prs -> NONE = stale leftover
        (200, {}),                                         # PATCH ref force-reset to basesha
        (200, {"sha": "mainsha", "encoding": "base64", "content": "b2xk"}),  # GET file (= main)
        (200, {"content": {}}),                            # PUT contents (region drifted)
        (201, {"number": 11, "html_url": "http://pr/11"}), # POST create pr (fresh diff)
    ])
    monkeypatch.setattr(reconcile, "_http", http)
    out = reconcile._real_open_or_update_pr(
        "MasterDD-L34D/vault", "auto/governor-reconcile-vault-lint-status", "main",
        "Atlas/lint-status.md", "NEW CONTENT", "vault-lint-status")
    assert out["action"] == "created" and out["number"] == 11
    patches = [c for c in calls if c["method"] == "PATCH"]
    assert len(patches) == 1, "exactly one ref force-reset for a stale branch"
    assert patches[0]["url"].endswith(
        "/git/refs/heads/auto/governor-reconcile-vault-lint-status")
    assert patches[0]["body"] == {"sha": "basesha", "force": True}
    # the reset happens BEFORE any content write
    put_idx = next(i for i, c in enumerate(calls) if c["method"] == "PUT")
    patch_idx = next(i for i, c in enumerate(calls) if c["method"] == "PATCH")
    assert patch_idx < put_idx
    for c in calls:
        assert "/merge" not in c["url"], f"merge route emitted: {c}"
    assert not http.remaining, "canned responses under-consumed (an http call was dropped)"


def test_stale_reset_with_content_equal_to_main_fails_closed(monkeypatch):
    """Documented fail-closed edge (harsh-review probe): UNREACHABLE via the actor (its
    contract guarantees `content` differs from main -- it only calls on drift), but a direct
    caller passing content identical to base must NOT open a junk/empty PR: post-reset the
    dedup skips the PUT and the zero-diff PR create surfaces as a raise (per-leg isolated)."""
    import base64 as _b64
    from governor import reconcile
    monkeypatch.setattr(reconcile, "_write_token", lambda environ=None: "wtok")
    same = "SAME AS MAIN"
    same_b64 = _b64.b64encode(same.encode("utf-8")).decode("ascii")
    http, calls = _recorder([
        (200, {"object": {"sha": "basesha"}}),            # GET base ref
        (422, {"message": "Reference already exists"}),    # POST create branch ref (stale)
        (200, []),                                         # GET open prs -> NONE = stale
        (200, {}),                                         # PATCH ref force-reset
        (200, {"sha": "ms", "encoding": "base64", "content": same_b64}),  # file == content
        (422, {"message": "No commits between main and branch"}),         # POST pr -> empty
    ])
    monkeypatch.setattr(reconcile, "_http", http)
    try:
        reconcile._real_open_or_update_pr(
            "MasterDD-L34D/vault", "auto/governor-reconcile-vault-lint-status", "main",
            "Atlas/lint-status.md", same, "vault-lint-status")
        assert False, "expected RuntimeError on zero-diff PR create"
    except RuntimeError as e:
        assert "create PR" in str(e)
    assert not any(c["method"] == "PUT" for c in calls), "dedup must skip the no-op PUT"
    for c in calls:
        assert "/merge" not in c["url"], f"merge route emitted: {c}"
    assert not http.remaining, "canned responses under-consumed (an http call was dropped)"


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
    / 'a human merges') does NOT false-positive.

    Scans BOTH the builder AND the actor's call site + the api factory (harsh-reviewer P1.3): the
    merge-block must stay CI-red if a future edit adds a merge call in reconcile_actor or exports
    a merge callable from real_gh_api -- not only if it lands in the builder."""
    import inspect
    from governor import reconcile
    forbidden = ("/merge", "--merge", "--admin", "--squash", "--rebase", "pr merge")
    for fn_name in ("_real_open_or_update_pr", "_real_get_file", "_http", "_commit_message",
                    "reconcile_actor", "real_gh_api"):
        src = inspect.getsource(getattr(reconcile, fn_name))
        for tok in forbidden:
            assert tok not in src, f"{fn_name} contains forbidden merge token {tok!r}"


def test_real_gh_api_exports_no_merge_callable():
    """harsh-reviewer P1.3: the injected api surface is EXACTLY get_file + open_or_update_pr.
    A future merge callable cannot be exported without going CI-red (no platform backstop)."""
    from governor.reconcile import real_gh_api
    assert set(real_gh_api().keys()) == {"get_file", "open_or_update_pr"}
