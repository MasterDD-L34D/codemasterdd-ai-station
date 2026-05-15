from datetime import datetime, timedelta, timezone
from app import cache_get, cache_set, CACHE, CACHE_TTL_SEC

def test_cache_set_stores_payload():
    cache_set("test_key", {"data": "value"})
    assert "test_key" in CACHE
    assert CACHE["test_key"]["payload"] == {"data": "value"}
    assert CACHE["test_key"]["stale"] is False
    assert CACHE["test_key"]["error"] is None
    assert "fetched_at" in CACHE["test_key"]

def test_cache_get_retrieves_payload():
    cache_set("test_key", "some_data")
    result = cache_get("test_key")
    assert result is not None
    assert result["payload"] == "some_data"
    assert result["stale"] is False

def test_cache_get_returns_none_for_missing_key():
    assert cache_get("non_existent") is None

def test_cache_get_marks_stale_entry():
    # Manually set an old entry
    old_time = (datetime.now(timezone.utc) - timedelta(seconds=CACHE_TTL_SEC + 10)).isoformat()
    CACHE["stale_key"] = {
        "payload": "old_data",
        "fetched_at": old_time,
        "stale": False,
        "error": None
    }

    result = cache_get("stale_key")
    assert result is not None
    assert result["stale"] is True
    assert result["payload"] == "old_data"

def test_cache_set_stores_error():
    cache_set("error_key", None, error="Something went wrong")
    result = cache_get("error_key")
    assert result is not None
    assert result["payload"] is None
    assert result["error"] == "Something went wrong"

def test_cache_get_fresh_entry_remains_not_stale():
    cache_set("fresh_key", "fresh_data")
    result = cache_get("fresh_key")
    assert result is not None
    assert result["stale"] is False
