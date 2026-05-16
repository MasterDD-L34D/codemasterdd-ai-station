"""Unit tests for coord-event API authentication."""

from unittest.mock import MagicMock

def test_coord_event_auth(monkeypatch):
    """Test the coord_event_log logic without relying on real Flask framework."""
    import sys

    # We want to re-import app but with a decorator that returns the original function
    if 'app' in sys.modules:
        del sys.modules['app']

    mock_flask = sys.modules['flask']
    # The route decorator is used like @app.route(...)
    # so app.route(...) returns a decorator function
    def mock_route(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

    mock_flask.Flask.return_value.route = mock_route

    import app
    # Now app.coord_event_log is the real function!
    # Let's test missing token when configured
    monkeypatch.setenv("API_SECRET", "super-secret-token")

    mock_request = MagicMock()
    mock_request.json = {"notes": "test notes"}
    mock_request.headers.get.return_value = ""
    app.request = mock_request

    # mock jsonify
    app.jsonify = lambda x: x

    result = app.coord_event_log()
    assert result == ({"ok": False, "error": "unauthorized"}, 401)

    # Test valid token
    mock_request.headers.get.return_value = "Bearer super-secret-token"
    app.request = mock_request

    class MockResult:
        returncode = 0
        stdout = b"success"
        stderr = b""
    monkeypatch.setattr(app.subprocess, "run", lambda *args, **kwargs: MockResult())
    monkeypatch.setattr(app.Path, "exists", lambda self: True)

    result = app.coord_event_log()
    assert result == {"ok": True, "stdout_tail": "success", "stderr_tail": "", "returncode": 0}

    # Test invalid token
    mock_request.headers.get.return_value = "Bearer wrong-token"
    app.request = mock_request
    result = app.coord_event_log()
    assert result == ({"ok": False, "error": "unauthorized"}, 401)

    # Test not configured
    monkeypatch.delenv("API_SECRET", raising=False)
    mock_request.headers.get.return_value = ""
    app.request = mock_request
    result = app.coord_event_log()
    assert result == {"ok": True, "stdout_tail": "success", "stderr_tail": "", "returncode": 0}
