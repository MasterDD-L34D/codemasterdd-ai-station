"""TDD tests for governor.reconcile -- is_doctrine + Reconciler fail-closed guard.

is_doctrine is the STATIC ADR-0038 doctrine carve-out classifier; a Reconciler aimed at a
doctrine path must REFUSE to construct (spec sec 3.1 / 4.2). Network/gh NEVER hit.
"""
import pytest

CARVE_OUTS_TRUE = [
    ("docs/adr/0039-x.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("docs/cross-repo/EXECUTION-BOARD.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("docs/cross-repo/actor-activation-criteria.md", "MasterDD-L34D/codemasterdd-ai-station"),
    (".claude/settings.json", "MasterDD-L34D/codemasterdd-ai-station"),
    (".claude/agents/harsh-reviewer.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/SAFE_CHANGES_ONLY.md",
     "MasterDD-L34D/codemasterdd-ai-station"),
    ("CLAUDE.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("docs/sub/CLAUDE.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("AGENTS.md", "MasterDD-L34D/Game"),
    ("ORCHESTRATION.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("GOALS.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("DECISIONS_LOG.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("OPEN_DECISIONS.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("~/.claude/rules/encoding.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("~/.config/aider-privacy-whitelist.txt", "MasterDD-L34D/codemasterdd-ai-station"),
]

TARGETS_FALSE = [
    ("STATUS_MULTI_REPO.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("Atlas/lint-status.md", "MasterDD-L34D/vault"),
]


@pytest.mark.parametrize("path,repo", CARVE_OUTS_TRUE)
def test_is_doctrine_true_for_each_carveout(path, repo):
    from governor.reconcile import is_doctrine
    assert is_doctrine(path, repo) is True


@pytest.mark.parametrize("path,repo", TARGETS_FALSE)
def test_is_doctrine_false_for_built_targets(path, repo):
    from governor.reconcile import is_doctrine
    assert is_doctrine(path, repo) is False


def test_is_doctrine_empty_path_is_failclosed_true():
    from governor.reconcile import is_doctrine
    assert is_doctrine("", "MasterDD-L34D/codemasterdd-ai-station") is True
    assert is_doctrine(None, "MasterDD-L34D/codemasterdd-ai-station") is True


def test_reconciler_constructs_for_nondoctrine_target():
    from governor.reconcile import Reconciler
    r = Reconciler(
        id="status-multi-repo",
        repo="MasterDD-L34D/codemasterdd-ai-station",
        path="STATUS_MULTI_REPO.md",
        marker=("<!-- B -->", "<!-- E -->"),
        render=lambda store: None,
    )
    assert r.id == "status-multi-repo"


def test_reconciler_raises_on_doctrine_path():
    from governor.reconcile import Reconciler
    with pytest.raises(ValueError, match="doctrine"):
        Reconciler(
            id="bad",
            repo="MasterDD-L34D/codemasterdd-ai-station",
            path="docs/adr/0001-x.md",
            marker=("<!-- B -->", "<!-- E -->"),
            render=lambda store: None,
        )
