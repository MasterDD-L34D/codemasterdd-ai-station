"""Unit tests for machine-portable repo path resolution.

Background: vault `local_path` was hardcoded `C:\\dev\\vault-shared`, which does
not exist on the Ryzen machine (DESKTOP-T77TMKT/VGit) where the vault lives at
`C:\\dev\\vault`. The hardcoded path made the dashboard's local git rollup
(git_local + velocity) fail on Ryzen while gh-API reads kept working. Found
during ground-truth autogovernance 2026-06-01 (vault
docs/research/2026-06-01-autogovernance-ecosystem-map.md).

Resolution precedence (resolve_repo_path):
1. Env-var override (explicit operator intent, trusted as-is, no existence check).
2. First candidate that exists on disk.
3. Last candidate as fallback (preserves historical default for messaging).
"""

from __future__ import annotations


def test_resolve_repo_path_env_override_wins(monkeypatch, tmp_path):
    """Env var takes precedence even when a candidate exists on disk."""
    import app

    existing = str(tmp_path)  # real dir, exists
    monkeypatch.setenv("MY_REPO_PATH", r"X:\explicit\override")
    assert (
        app.resolve_repo_path("MY_REPO_PATH", existing) == r"X:\explicit\override"
    )


def test_resolve_repo_path_first_existing_candidate(monkeypatch, tmp_path):
    """With no env override, the first existing candidate is returned."""
    import app

    monkeypatch.delenv("MY_REPO_PATH", raising=False)
    primary = str(tmp_path)  # exists
    fallback = str(tmp_path / "nope")  # missing
    assert app.resolve_repo_path("MY_REPO_PATH", primary, fallback) == primary


def test_resolve_repo_path_skips_missing_primary(monkeypatch, tmp_path):
    """A missing primary candidate is skipped in favour of an existing one."""
    import app

    monkeypatch.delenv("MY_REPO_PATH", raising=False)
    primary = str(tmp_path / "missing")  # missing
    secondary = str(tmp_path)  # exists
    assert app.resolve_repo_path("MY_REPO_PATH", primary, secondary) == secondary


def test_resolve_repo_path_fallback_when_none_exist(monkeypatch, tmp_path):
    """When no candidate exists, the last candidate is returned as fallback."""
    import app

    monkeypatch.delenv("MY_REPO_PATH", raising=False)
    primary = str(tmp_path / "a")  # missing
    fallback = str(tmp_path / "b")  # missing
    assert app.resolve_repo_path("MY_REPO_PATH", primary, fallback) == fallback


def test_resolve_repo_path_blank_env_treated_as_unset(monkeypatch, tmp_path):
    """A blank/whitespace env var is treated as unset (falls through to candidates)."""
    import app

    monkeypatch.setenv("MY_REPO_PATH", "   ")
    existing = str(tmp_path)
    assert app.resolve_repo_path("MY_REPO_PATH", existing) == existing


def test_vault_local_path_is_machine_portable():
    """Regression guard for the hardcoded-path bug (2026-06-01).

    On any machine where a known vault clone exists (Ryzen: C:\\dev\\vault,
    Lenovo: also C:\\dev\\vault), the wired vault local_path MUST point at an
    existing directory -- never unconditionally at the stale C:\\dev\\vault-shared.
    On a fresh machine where neither candidate exists the assertion is vacuous.
    """
    from pathlib import Path

    import app

    vault_path = app.REPOS["vault"]["local_path"]
    candidates = [r"C:\dev\vault", r"C:\dev\vault-shared"]
    if any(Path(c).exists() for c in candidates):
        assert Path(vault_path).exists(), (
            f"vault local_path {vault_path!r} does not exist though a known "
            f"candidate does -- path is not machine-portable"
        )


def test_dafne_local_path_is_machine_portable():
    """Regression guard for the Dafne hardcoded-path bug (2026-06-01).

    The Dafne (evo-swarm) clone lives at C:\\dev\\evo-swarm on Ryzen
    (DESKTOP-T77TMKT/VGit) and at C:\\Users\\edusc\\Dafne\\workspace\\swarm on
    Lenovo (edusc). On any machine where a known clone exists, the wired Dafne
    local_path MUST point at an existing directory -- never unconditionally at
    the Lenovo-only C:\\Users\\edusc\\Dafne\\workspace\\swarm. On a fresh machine
    where neither candidate exists the assertion is vacuous. Same bug class as
    the vault fix (PR #237).
    """
    from pathlib import Path

    import app

    dafne_path = app.REPOS["Dafne"]["local_path"]
    candidates = [r"C:\dev\evo-swarm", r"C:\Users\edusc\Dafne\workspace\swarm"]
    if any(Path(c).exists() for c in candidates):
        assert Path(dafne_path).exists(), (
            f"Dafne local_path {dafne_path!r} does not exist though a known "
            f"candidate does -- path is not machine-portable"
        )
