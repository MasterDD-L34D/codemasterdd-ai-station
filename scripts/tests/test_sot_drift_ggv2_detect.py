import importlib.util
import json
import pathlib

import pytest

_MOD = pathlib.Path(__file__).resolve().parents[1] / "fleet" / "sot_drift_ggv2_detect.py"
_spec = importlib.util.spec_from_file_location("sot_drift_ggv2_detect", _MOD)
det = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(det)

MAP = [
    {"concept": "audio", "patterns": ["assets/audio/**", "default_bus_layout.tres"],
     "sot_ref": ["adr/audio.md"]},
    {"concept": "ui", "patterns": ["scripts/ui/**"], "sot_ref": ["core/30.md"]},
]


# --- glob_to_regex / match_changes -----------------------------------------

def test_matches_nested_glob_and_collects_files():
    m = det.match_changes(MAP, ["assets/audio/sfx/hit.wav", "README.md"])
    assert len(m) == 1
    assert m[0]["concept"] == "audio"
    assert m[0]["files"] == ["assets/audio/sfx/hit.wav"]


def test_matches_exact_file_pattern():
    m = det.match_changes(MAP, ["default_bus_layout.tres"])
    assert len(m) == 1 and m[0]["concept"] == "audio"


def test_no_match_returns_empty():
    assert det.match_changes(MAP, ["scripts/combat/x.gd", "README.md"]) == []


def test_single_star_does_not_cross_directory():
    # 'scripts/ui/**' matches any depth; a bare '*' would not cross '/'
    rx = det.glob_to_regex("data/economy*")
    assert rx.match("data/economy_x.json")
    assert not rx.match("data/economy/sub/x.json")


# --- commit_type ------------------------------------------------------------

def test_commit_type_feat_with_scope():
    assert det.commit_type("feat(x): y") == "feat"


def test_commit_type_plain_fix():
    assert det.commit_type("fix: z") == "fix"


def test_commit_type_breaking_scoped():
    assert det.commit_type("refactor(a)!: b") == "refactor"


def test_commit_type_empty_string():
    assert det.commit_type("") == ""


# --- checkpoint --------------------------------------------------------------

def test_checkpoint_round_trip(tmp_path):
    p = tmp_path / "sub" / "cp.json"
    det.save_checkpoint(str(p), {"seen": [1, 2, 3]})
    assert det.load_checkpoint(str(p)) == {"seen": [1, 2, 3]}


def test_load_checkpoint_missing_returns_empty(tmp_path):
    assert det.load_checkpoint(str(tmp_path / "nope.json")) == {}


def test_load_checkpoint_corrupt_returns_empty(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    assert det.load_checkpoint(str(p)) == {}


# --- load_watch_map -----------------------------------------------------------

def test_load_watch_map(tmp_path):
    p = tmp_path / "wm.json"
    p.write_text(json.dumps({"entries": [{"concept": "a", "patterns": ["x/**"], "sot_ref": ["y"]}]}), encoding="utf-8")
    wm = det.load_watch_map(str(p))
    assert wm == [{"concept": "a", "patterns": ["x/**"], "sot_ref": ["y"]}]


# --- build_issue_body ----------------------------------------------------------

def test_build_issue_body_lists_prs_refs_and_triage_tag():
    per_pr = [
        {"pr": {"number": 599, "title": "fix(audio): bus"},
         "matches": [{"concept": "audio", "sot_ref": ["adr/audio.md"], "patterns": ["assets/audio/**"],
                      "files": ["assets/audio/x.wav"]}],
         "commit_type": "fix"},
    ]
    body = det.build_issue_body(per_pr)
    assert det.MARKER in body
    assert "#599" in body
    assert "adr/audio.md" in body
    assert "sot-drift-verifier" in body
    assert "[fix]" in body


# --- FakeGh -------------------------------------------------------------------

class FakeGh:
    """Routes gh argv by prefix; records every call for assertions."""

    def __init__(self, prs=None, files_by_number=None, issue_list_out="",
                 issue_view_body="", fail_on_search=False):
        self.prs = prs or []
        self.files_by_number = files_by_number or {}
        self.issue_list_out = issue_list_out
        self.issue_view_body = issue_view_body
        self.fail_on_search = fail_on_search
        self.calls = []
        self.edit_body = None
        self.create_body = None

    def __call__(self, args):
        self.calls.append(list(args))
        if args[0] == "search" and args[1] == "prs":
            if self.fail_on_search:
                raise RuntimeError("gh search prs failed (rc=1): boom")
            return json.dumps(self.prs)
        if args[0] == "pr" and args[1] == "view":
            number = int(args[2])
            paths = self.files_by_number.get(number, [])
            title = next((p["title"] for p in self.prs if p["number"] == number), "")
            return json.dumps({"number": number, "title": title,
                               "files": [{"path": p} for p in paths]})
        if args[0] == "issue" and args[1] == "list":
            return self.issue_list_out
        if args[0] == "issue" and args[1] == "view":
            return json.dumps({"body": self.issue_view_body})
        if args[0] == "issue" and args[1] == "edit":
            # Read the --body-file NOW: the caller deletes it right after this
            # returns (finally: os.remove(path)), so capture content at call time.
            body_file = args[args.index("--body-file") + 1]
            self.edit_body = pathlib.Path(body_file).read_text(encoding="utf-8")
            return ""
        if args[0] == "issue" and args[1] == "comment":
            return ""
        if args[0] == "issue" and args[1] == "create":
            body_file = args[args.index("--body-file") + 1]
            self.create_body = pathlib.Path(body_file).read_text(encoding="utf-8")
            return "https://github.com/MasterDD-L34D/Game/issues/999"
        return ""


def _wm(tmp_path, patterns=("assets/audio/**",), sot_ref=("adr/a.md",)):
    p = tmp_path / "wm.json"
    p.write_text(json.dumps({"entries": [{"concept": "audio", "patterns": list(patterns),
                                          "sot_ref": list(sot_ref)}]}), encoding="utf-8")
    return str(p)


# --- open_or_update_issue -------------------------------------------------------

def test_open_or_update_creates_when_none_open():
    gh = FakeGh(issue_list_out="")
    per_pr = [{"pr": {"number": 5, "title": "fix(audio): x"},
              "matches": [{"concept": "audio", "sot_ref": ["adr/a.md"], "patterns": ["assets/audio/**"],
                           "files": ["assets/audio/x.wav"]}], "commit_type": "fix"}]
    action, ref = det.open_or_update_issue(gh, per_pr, repo="OWN/Game")
    assert action == "create"
    joined = [" ".join(str(x) for x in c) for c in gh.calls]
    assert any("issue create" in j for j in joined)
    assert not any("issue edit" in j for j in joined)


def test_open_or_update_edits_and_accumulates_when_open_exists():
    gh = FakeGh(issue_list_out="42\n", issue_view_body="PRIOR BODY TEXT MARKER")
    per_pr = [{"pr": {"number": 6, "title": "feat(audio): y"},
              "matches": [{"concept": "audio", "sot_ref": ["adr/a.md"], "patterns": ["assets/audio/**"],
                           "files": ["assets/audio/y.wav"]}], "commit_type": "feat"}]
    action, ref = det.open_or_update_issue(gh, per_pr, repo="OWN/Game")
    assert action == "edit"
    assert ref == "42"
    edit_calls = [c for c in gh.calls if c[0] == "issue" and c[1] == "edit"]
    assert len(edit_calls) == 1
    assert "PRIOR BODY TEXT MARKER" in gh.edit_body
    assert "#6" in gh.edit_body


# --- detect --------------------------------------------------------------------

def test_detect_is_path_first_flags_fix_pr(tmp_path):
    wm = _wm(tmp_path)
    gh = FakeGh(prs=[{"number": 5, "title": "fix(audio): crackle"}],
                files_by_number={5: ["assets/audio/x.wav"]})
    res = det.detect(gh, wm, str(tmp_path / "cp.json"), dry_run=True)
    assert res["flagged"] == 1
    assert res["scanned"] == 1


def test_detect_no_match_no_flag(tmp_path):
    wm = _wm(tmp_path)
    gh = FakeGh(prs=[{"number": 7, "title": "feat(net): reconnect"}],
                files_by_number={7: ["scripts/net/peer.gd"]})
    res = det.detect(gh, wm, str(tmp_path / "cp.json"), dry_run=True)
    assert res["flagged"] == 0


def test_detect_skips_already_seen_prs(tmp_path):
    wm = _wm(tmp_path)
    cp = tmp_path / "cp.json"
    cp.write_text(json.dumps({"seen": [5]}), encoding="utf-8")
    gh = FakeGh(prs=[{"number": 5, "title": "fix(audio): crackle"}],
                files_by_number={5: ["assets/audio/x.wav"]})
    res = det.detect(gh, wm, str(cp), dry_run=True)
    assert res["scanned"] == 0
    assert res["flagged"] == 0


def test_detect_advances_checkpoint_seen_set(tmp_path):
    wm = _wm(tmp_path)
    cp = tmp_path / "cp.json"
    gh = FakeGh(prs=[{"number": 10, "title": "fix(audio): a"},
                     {"number": 11, "title": "chore: b"}],
                files_by_number={10: ["assets/audio/x.wav"], 11: ["README.md"]})
    det.detect(gh, wm, str(cp), dry_run=False)
    checkpoint = det.load_checkpoint(str(cp))
    assert set(checkpoint["seen"]) == {10, 11}


def test_detect_dry_run_does_not_write_checkpoint(tmp_path):
    wm = _wm(tmp_path)
    cp = tmp_path / "cp.json"
    gh = FakeGh(prs=[{"number": 20, "title": "fix(audio): a"}],
                files_by_number={20: ["assets/audio/x.wav"]})
    det.detect(gh, wm, str(cp), dry_run=True)
    assert not cp.exists()


def test_detect_does_not_advance_checkpoint_on_gh_failure(tmp_path):
    wm = _wm(tmp_path)
    cp = tmp_path / "cp.json"
    cp.write_text(json.dumps({"seen": [1, 2, 3]}), encoding="utf-8")
    before = cp.read_text(encoding="utf-8")
    gh = FakeGh(fail_on_search=True)
    with pytest.raises(RuntimeError):
        det.detect(gh, wm, str(cp), dry_run=False)
    after = cp.read_text(encoding="utf-8")
    assert before == after


def test_detect_skips_noise_commit_types(tmp_path):
    wm = _wm(tmp_path, patterns=("scripts/combat/**",), sot_ref=("core/10.md",))
    gh = FakeGh(prs=[{"number": 9, "title": "docs(scripts): gdscript doc-comments"}],
                files_by_number={9: ["scripts/combat/round.gd"]})
    res = det.detect(gh, wm, str(tmp_path / "cp.json"), dry_run=True)
    assert res["flagged"] == 0  # docs PR ships no behavior -> not drift
    # noise guard skips BEFORE fetch_pr_files -> no `pr view` gh call for it
    assert not any(c[0] == "pr" and c[1] == "view" for c in gh.calls)
