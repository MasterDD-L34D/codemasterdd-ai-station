import sys
from pathlib import Path
from unittest.mock import MagicMock

# Mock dependencies that are not available in the environment
sys.modules['requests'] = MagicMock()
sys.modules['flask'] = MagicMock()
sys.modules['waitress'] = MagicMock()
sys.modules['pystray'] = MagicMock()
sys.modules['PIL'] = MagicMock()

import pytest

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

@pytest.fixture(autouse=True)
def clear_cache():
    from app import CACHE
    CACHE.clear()
    yield
    CACHE.clear()
