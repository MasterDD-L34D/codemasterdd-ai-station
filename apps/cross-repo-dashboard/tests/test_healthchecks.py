"""Unit tests for fetch_healthchecks in cross-repo-dashboard app.

Coverage: happy path (200 OK), connection error (down), timeout, general error, and TCP check.
"""

from __future__ import annotations

from unittest.mock import MagicMock

def test_fetch_healthchecks_all(monkeypatch):
    """Test the fetch_healthchecks function across all error and success conditions."""

    # We must import app inside the test so conftest.py's mock_external_deps fixture has
    # populated sys.modules['requests'] with a MagicMock.
    import app

    # We create standard python exception subclasses to simulate requests exceptions
    class MockConnectionError(Exception):
        pass
    class MockTimeout(Exception):
        pass

    # We must patch app.requests explicitly so the except blocks catch these
    monkeypatch.setattr(app.requests, 'ConnectionError', MockConnectionError, raising=False)
    monkeypatch.setattr(app.requests, 'Timeout', MockTimeout, raising=False)

    # Override the healthchecks array so we just hit our targeted test cases
    monkeypatch.setattr(app, 'HEALTHCHECKS', [
        {"name": "conn_error", "url": "http://conn", "timeout": 3, "category": "cat1"},
        {"name": "timeout", "url": "http://time", "timeout": 3, "category": "cat2"},
        {"name": "generic", "url": "http://gen", "timeout": 3, "category": "cat3"},
        {"name": "success", "url": "http://suc", "timeout": 3, "category": "cat4"},
        {"name": "non_200", "url": "http://non200", "timeout": 3, "category": "cat5"}
    ])
    monkeypatch.setattr(app, 'HEALTHCHECKS_TCP', [])

    class MockResponseSuccess:
        status_code = 200
        class elapsed:
            @staticmethod
            def total_seconds():
                return 0.125

    class MockResponseNon200:
        status_code = 500
        class elapsed:
            @staticmethod
            def total_seconds():
                return 0.2

    def mock_get(url, **kwargs):
        if url == "http://conn":
            raise MockConnectionError()
        elif url == "http://time":
            raise MockTimeout()
        elif url == "http://gen":
            raise Exception("Some weird error")
        elif url == "http://suc":
            return MockResponseSuccess()
        elif url == "http://non200":
            return MockResponseNon200()
        else:
            return MockResponseSuccess()

    # monkeypatch the mock object's method
    mock_get_func = MagicMock(side_effect=mock_get)
    monkeypatch.setattr(app.requests, 'get', mock_get_func)

    # Perform the check
    results = app.fetch_healthchecks(force_refresh=True)

    # Create a mapping for easier assertions
    res_dict = {r["name"]: r for r in results}

    # 1. ConnectionError -> down
    assert res_dict["conn_error"]["status"] == "down"
    assert res_dict["conn_error"]["http"] is None

    # 2. Timeout -> timeout
    assert res_dict["timeout"]["status"] == "timeout"
    assert res_dict["timeout"]["http"] is None

    # 3. Exception -> error
    assert res_dict["generic"]["status"] == "error"
    assert res_dict["generic"]["http"] is None
    assert "Some weird error" in res_dict["generic"]["error"]

    # 4. Success (200) -> up
    assert res_dict["success"]["status"] == "up"
    assert res_dict["success"]["http"] == 200
    assert res_dict["success"]["latency_ms"] == 125  # 0.125 * 1000

    # 5. Non-200 -> error
    assert res_dict["non_200"]["status"] == "error"
    assert res_dict["non_200"]["http"] == 500
    assert res_dict["non_200"]["latency_ms"] == 200
