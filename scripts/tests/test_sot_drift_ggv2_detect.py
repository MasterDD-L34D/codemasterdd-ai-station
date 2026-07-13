import importlib.util
import pathlib

_MOD = pathlib.Path(__file__).resolve().parents[1] / "fleet" / "sot_drift_ggv2_detect.py"
_spec = importlib.util.spec_from_file_location("sot_drift_ggv2_detect", _MOD)
det = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(det)

MAP = [
    {"concept": "audio", "patterns": ["assets/audio/**", "default_bus_layout.tres"],
     "sot_ref": ["adr/audio.md"]},
    {"concept": "ui", "patterns": ["scripts/ui/**"], "sot_ref": ["core/30.md"]},
]


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


def test_is_feature_pr():
    assert det.is_feature_pr("feat(audio): bus layout")
    assert det.is_feature_pr("feat: something")
    assert det.is_feature_pr("feat(vfx)!: breaking")
    assert not det.is_feature_pr("fix(audio): crackle")
    assert not det.is_feature_pr("chore: bump")
    assert not det.is_feature_pr("docs: readme")
    assert not det.is_feature_pr("")


import json


def test_load_watch_map(tmp_path):
    p = tmp_path / "wm.json"
    p.write_text(json.dumps({"entries": [{"concept": "a", "patterns": ["x/**"], "sot_ref": ["y"]}]}), encoding="utf-8")
    wm = det.load_watch_map(str(p))
    assert wm == [{"concept": "a", "patterns": ["x/**"], "sot_ref": ["y"]}]


def test_checkpoint_round_trip(tmp_path):
    p = tmp_path / "sub" / "cp.json"
    det.save_checkpoint(str(p), {"last_merged_at": "2026-07-13T00:00:00Z"})
    assert det.load_checkpoint(str(p)) == {"last_merged_at": "2026-07-13T00:00:00Z"}


def test_load_checkpoint_missing_returns_empty(tmp_path):
    assert det.load_checkpoint(str(tmp_path / "nope.json")) == {}


def test_load_checkpoint_corrupt_returns_empty(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    assert det.load_checkpoint(str(p)) == {}


def test_new_prs_since_filters_and_sorts():
    prs = [
        {"number": 3, "title": "feat: c", "mergedAt": "2026-07-13T10:00:00Z"},
        {"number": 1, "title": "feat: a", "mergedAt": "2026-07-12T09:00:00Z"},
        {"number": 2, "title": "feat: b", "mergedAt": "2026-07-13T08:00:00Z"},
    ]
    fresh = det.new_prs_since(prs, {"last_merged_at": "2026-07-12T12:00:00Z"})
    assert [p["number"] for p in fresh] == [2, 3]  # PR1 too old; sorted asc


def test_new_prs_since_empty_checkpoint_uses_all():
    prs = [{"number": 1, "title": "feat: a", "mergedAt": "2026-07-13T08:00:00Z"}]
    assert len(det.new_prs_since(prs, {})) == 1


def test_build_issue_body_lists_prs_and_refs():
    per_pr = [
        {"pr": {"number": 599, "title": "feat(audio): bus"},
         "matches": [{"concept": "audio", "sot_ref": ["adr/audio.md"], "patterns": ["assets/audio/**"],
                      "files": ["assets/audio/x.wav"]}]},
    ]
    body = det.build_issue_body(per_pr)
    assert "<!-- sot-drift-ggv2 -->" in body
    assert "#599" in body
    assert "adr/audio.md" in body
    assert "sot-drift-verifier" in body


class FakeGh:
    """Records gh argv; returns queued stdout per matched command prefix."""
    def __init__(self, responses):
        self.responses = responses  # list[(match_substr, stdout)]
        self.calls = []

    def __call__(self, args):
        self.calls.append(args)
        joined = " ".join(args)
        for sub, out in self.responses:
            if sub in joined:
                return out
        return ""


def test_open_or_update_creates_when_none_open():
    gh = FakeGh([("issue list", "")])  # no existing open issue
    det.open_or_update_issue(gh, "body-x", repo="OWN/Game")
    joined = [" ".join(c) for c in gh.calls]
    assert any("issue list" in j for j in joined)
    assert any("issue create" in j for j in joined)
    assert not any("issue edit" in j for j in joined)


def test_open_or_update_edits_when_open_exists():
    gh = FakeGh([("issue list", "42\n")])  # existing issue #42
    det.open_or_update_issue(gh, "body-x", repo="OWN/Game")
    joined = [" ".join(c) for c in gh.calls]
    assert any("issue edit" in j and "42" in j for j in joined)
    assert not any("issue create" in j for j in joined)
