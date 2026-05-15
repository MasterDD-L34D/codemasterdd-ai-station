"""Pytest fixtures + hermetic mocks for cross-repo-dashboard tests.

Design notes:
- External deps (requests, flask, waitress, pystray, PIL) sono mockati a livello
  conftest perche' l'app li importa al top-level e non sono installati nel test env.
- Mocks su sys.modules registrati con cleanup hook `pytest_unconfigure` per
  evitare cross-test contamination se la pytest session include altri test dir.
- Test isolation per CACHE garantita da fixture autouse `clear_cache`.

How to run:
    # Scoped per-app (richiesto -- vedi caveat sotto):
    python -m pytest apps/cross-repo-dashboard/

Caveat -- combined-run con altri apps NOT supported:
- Il monorepo ha `apps/dogfood-ui/app.py` E `apps/cross-repo-dashboard/app.py` (sibling).
- Entrambi i `tests/conftest.py` iniettano la dir parent in sys.path -> import collision su `app`.
- Per evitare: invocare pytest scoped a un singolo app alla volta (mai `pytest apps/`).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_DEPS_TO_MOCK = ("requests", "flask", "waitress", "pystray", "PIL")
_MOCK_INSTANCES = {dep: MagicMock() for dep in _DEPS_TO_MOCK}
_ORIGINAL_MODULES: dict[str, object | None] = {}

# Apply mocks at conftest import time, BEFORE test modules are collected
# (test_cache.py imports `from app import ...` at top-level).
for _dep, _mock in _MOCK_INSTANCES.items():
    _ORIGINAL_MODULES[_dep] = sys.modules.get(_dep)
    sys.modules[_dep] = _mock

# Inject app dir into sys.path so `from app import ...` resolves.
_APP_DIR = Path(__file__).resolve().parent.parent
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))


def pytest_unconfigure(config):
    """Restore sys.modules at session end (prevent contamination across test dirs)."""
    for dep, original in _ORIGINAL_MODULES.items():
        if original is None:
            sys.modules.pop(dep, None)
        else:
            sys.modules[dep] = original


@pytest.fixture(autouse=True)
def clear_cache():
    """Ensure CACHE is empty before and after each test for isolation."""
    from app import CACHE
    CACHE.clear()
    yield
    CACHE.clear()
