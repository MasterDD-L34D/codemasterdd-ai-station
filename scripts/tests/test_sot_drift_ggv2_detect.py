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
