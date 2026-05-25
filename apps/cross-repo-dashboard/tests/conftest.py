"""Pytest fixtures + hermetic mocks for cross-repo-dashboard tests.

Design notes (post Codex P2 fix on PR #99):
- External deps (requests, flask, waitress, pystray, PIL) NOT installed in test env.
- Mocks applied at **function scope** via monkeypatch.setitem, so cleanup happens
  automatically post-test (NOT at session end). This prevents the cross-test
  contamination pattern flagged in PR #97 review (Jules) and re-applied incorrectly
  in PR #99 (my own first fix attempt -- meta anti-pattern documented in L-2026-05-025).
- Test files MUST import app symbols inside test functions (NOT at module top-level)
  so the autouse fixture runs first and sets up the mocks before import resolution.
- Test isolation per CACHE garantita da fixture autouse `clear_cache` (depends on
  `mock_external_deps` so it transitively activates mocks before app import).

How to run:
    python -m pytest apps/cross-repo-dashboard/

Combined-run con altri apps:
- pyproject.toml in this directory sets `--import-mode=importlib`, but combining
  `pytest apps/dogfood-ui apps/cross-repo-dashboard` still risks plugin
  re-registration because both have `tests/` packages. Function-scope mocks
  here mitigate the deeper contamination concern (sys.modules mutation).
- Best practice: invoke pytest scoped to a single app.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_DEPS_TO_MOCK = ("requests", "flask", "waitress", "pystray", "PIL")

# Inject app dir into sys.path so `from app import ...` (inside test functions)
# resolves. This is safe at module level since it only adds a path entry.
_APP_DIR = Path(__file__).resolve().parent.parent
# Ensure app dir is FIRST in sys.path (before repo root) to avoid name collision
# with other apps/app.py modules in the monorepo.
_APP_DIR_STR = str(_APP_DIR)
if _APP_DIR_STR in sys.path:
    sys.path.remove(_APP_DIR_STR)
sys.path.insert(0, _APP_DIR_STR)


@pytest.fixture
def mock_external_deps(monkeypatch):
    """Function-scope mocks for external deps NOT installed in test env.

    Uses `monkeypatch.setitem` which auto-restores sys.modules post-test,
    eliminating cross-test contamination (the bug Codex flagged on PR #99).
    """
    for dep in _DEPS_TO_MOCK:
        monkeypatch.setitem(sys.modules, dep, MagicMock())


@pytest.fixture(autouse=True)
def clear_cache(mock_external_deps):
    """Ensure CACHE is empty before/after each test for isolation.

    Depends on `mock_external_deps` so external mocks are active before
    `from app import CACHE` resolves.
    """
    from app import CACHE
    CACHE.clear()
    yield
    CACHE.clear()
