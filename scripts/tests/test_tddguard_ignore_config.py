"""Tests for scripts/setup/tddguard-ignore-config.py.

Gap 2026-07-10: ad-hoc git worktrees of fleet repos live OUTSIDE the repo dir
(C:/dev/_game-wt-*, C:/dev/Game-wt-*, Lenovo _gamewt-*) and did NOT match the
sibling glob **/Game/** -> tdd-guard false-blocked legit TDD there (episode:
CWE-20 fix in Game-wt-gridcap, Game PR #3256). Ref memory
feedback_tddguard_cross_repo_blindspot.

Hyphenated filename -> load via importlib spec inside a module-scoped fixture
(no sys.path/sys.modules global mutation; cf. L-2026-05-028/029 + PR #102).
"""

from __future__ import annotations

import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def cfg_module():
    """Load hyphenated script via importlib spec, scoped (no global pollution)."""
    script_path = (
        Path(__file__).parent.parent / "setup" / "tddguard-ignore-config.py"
    )
    spec = spec_from_file_location("tddguard_ignore_config", str(script_path))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_siblings_include_adhoc_worktree_globs(cfg_module):
    """Worktree conventions outside repo dirs must be exempted too."""
    expected = [
        "**/Game-wt*/**",      # C:/dev/Game-wt-gridcap + bare C:/dev/Game-wt
        "**/_game-wt-*/**",    # C:/dev/_game-wt-3246, -apfloor, ... (Ryzen)
        "**/_gamewt-*/**",     # _gamewt-lenovo-host (Lenovo convention)
        "**/vault-wt*/**",     # C:/dev/vault-wt (convention extends to vault)
    ]
    for pattern in expected:
        assert pattern in cfg_module.SIBLINGS, f"missing glob: {pattern}"


def test_main_writes_defaults_plus_siblings(cfg_module, tmp_path):
    """main(root) writes config under root; import alone must not write."""
    cfg_path = cfg_module.main(str(tmp_path))

    expected_path = tmp_path / ".claude" / "tdd-guard" / "data" / "config.json"
    assert Path(cfg_path) == expected_path
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)
    assert cfg["ignorePatterns"] == cfg_module.DEFAULTS + cfg_module.SIBLINGS


def test_main_preserves_guard_enabled(cfg_module, tmp_path):
    """Scoped guard-off toggle survives regeneration; stale patterns replaced."""
    cfg_dir = tmp_path / ".claude" / "tdd-guard" / "data"
    cfg_dir.mkdir(parents=True)
    (cfg_dir / "config.json").write_text(
        json.dumps({"guardEnabled": False, "ignorePatterns": ["stale"]}),
        encoding="utf-8",
    )

    cfg_module.main(str(tmp_path))

    cfg = json.loads((cfg_dir / "config.json").read_text(encoding="utf-8"))
    assert cfg["guardEnabled"] is False
    assert "stale" not in cfg["ignorePatterns"]


def test_main_idempotent(cfg_module, tmp_path):
    """Double run -> identical bytes (safe to re-run per machine)."""
    cfg_module.main(str(tmp_path))
    first = (tmp_path / ".claude" / "tdd-guard" / "data" / "config.json").read_text(encoding="utf-8")
    cfg_module.main(str(tmp_path))
    second = (tmp_path / ".claude" / "tdd-guard" / "data" / "config.json").read_text(encoding="utf-8")

    assert first == second
