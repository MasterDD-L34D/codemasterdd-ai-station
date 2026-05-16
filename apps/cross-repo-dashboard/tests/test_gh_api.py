import sys
from unittest.mock import MagicMock

def test_gh_api_no_token(monkeypatch):
    import app
    monkeypatch.setattr(app, "GH_TOKEN", "")
    ok, data, err = app.gh_api("test")
    assert not ok
    assert data is None
    assert "no gh token" in err

def test_gh_api_success_json(monkeypatch):
    import app
    monkeypatch.setattr(app, "GH_TOKEN", "fake_token")
    mock_get = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"hello": "world"}
    mock_get.return_value = mock_response
    monkeypatch.setattr(app.requests, "get", mock_get)

    ok, data, err = app.gh_api("test-endpoint")
    assert ok
    assert data == {"hello": "world"}
    assert err is None

    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == f"{app.GH_API_BASE}/test-endpoint"
    assert kwargs["headers"]["Authorization"] == "Bearer fake_token"

def test_gh_api_success_text(monkeypatch):
    import app
    monkeypatch.setattr(app, "GH_TOKEN", "fake_token")
    mock_get = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError()
    mock_response.text = "plain text response"
    mock_get.return_value = mock_response
    monkeypatch.setattr(app.requests, "get", mock_get)

    ok, data, err = app.gh_api("test")
    assert ok
    assert data == "plain text response"
    assert err is None

def test_gh_api_rate_limit(monkeypatch):
    import app
    monkeypatch.setattr(app, "GH_TOKEN", "fake_token")
    mock_get = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "API rate limit exceeded"
    mock_response.headers = {"X-RateLimit-Reset": "1234567890"}
    mock_get.return_value = mock_response
    monkeypatch.setattr(app.requests, "get", mock_get)

    ok, data, err = app.gh_api("test")
    assert not ok
    assert data is None
    assert "rate limit: reset at 1234567890" in err

def test_gh_api_http_error(monkeypatch):
    import app
    monkeypatch.setattr(app, "GH_TOKEN", "fake_token")
    mock_get = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response
    monkeypatch.setattr(app.requests, "get", mock_get)

    ok, data, err = app.gh_api("test")
    assert not ok
    assert data is None
    assert "http 404: Not Found" in err

def test_gh_api_timeout(monkeypatch):
    import app
    class MockTimeout(Exception): pass
    class MockConnectionError(Exception): pass
    monkeypatch.setattr(app.requests, "Timeout", MockTimeout, raising=False)
    monkeypatch.setattr(app.requests, "ConnectionError", MockConnectionError, raising=False)

    monkeypatch.setattr(app, "GH_TOKEN", "fake_token")
    mock_get = MagicMock(side_effect=MockTimeout("timeout error"))
    monkeypatch.setattr(app.requests, "get", mock_get)

    ok, data, err = app.gh_api("test", timeout=10)
    assert not ok
    assert data is None
    assert "timeout after 10s" in err

def test_gh_api_connection_error(monkeypatch):
    import app
    class MockTimeout(Exception): pass
    class MockConnectionError(Exception): pass
    monkeypatch.setattr(app.requests, "Timeout", MockTimeout, raising=False)
    monkeypatch.setattr(app.requests, "ConnectionError", MockConnectionError, raising=False)

    monkeypatch.setattr(app, "GH_TOKEN", "fake_token")
    mock_get = MagicMock(side_effect=MockConnectionError("connection failed"))
    monkeypatch.setattr(app.requests, "get", mock_get)

    ok, data, err = app.gh_api("test")
    assert not ok
    assert data is None
    assert "conn error: connection failed" in err

def test_gh_api_generic_exception(monkeypatch):
    import app
    class MockTimeout(Exception): pass
    class MockConnectionError(Exception): pass
    monkeypatch.setattr(app.requests, "Timeout", MockTimeout, raising=False)
    monkeypatch.setattr(app.requests, "ConnectionError", MockConnectionError, raising=False)

    monkeypatch.setattr(app, "GH_TOKEN", "fake_token")
    mock_get = MagicMock(side_effect=RuntimeError("unexpected error"))
    monkeypatch.setattr(app.requests, "get", mock_get)

    ok, data, err = app.gh_api("test")
    assert not ok
    assert data is None
    assert "RuntimeError: unexpected error" in err
