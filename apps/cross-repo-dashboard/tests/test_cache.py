"""Unit tests for cache_get / cache_set in cross-repo-dashboard app.

Coverage: happy path + missing key + stale entry (via public API + timestamp
monkey-patch, NOT raw CACHE schema mutation) + error storage + fresh entry.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app import CACHE, CACHE_TTL_SEC, cache_get, cache_set


def test_cache_set_stores_payload():
    cache_set("test_key", {"data": "value"})
    entry = CACHE["test_key"]
    assert entry["payload"] == {"data": "value"}
    assert entry["stale"] is False
    assert entry["error"] is None
    assert "fetched_at" in entry


def test_cache_get_retrieves_payload():
    cache_set("test_key", "some_data")
    result = cache_get("test_key")
    assert result is not None
    assert result["payload"] == "some_data"
    assert result["stale"] is False


def test_cache_get_returns_none_for_missing_key():
    assert cache_get("non_existent") is None


def test_cache_get_marks_stale_entry():
    """Stale detection: use public cache_set then patch fetched_at backward.

    Note: we mutate only the fetched_at field of an entry created via the
    public API, NOT the whole entry. If the CACHE schema evolves (extra
    fields), this test still works.
    """
    cache_set("stale_key", "old_data")
    old_iso = (
        datetime.now(timezone.utc) - timedelta(seconds=CACHE_TTL_SEC + 10)
    ).isoformat()
    CACHE["stale_key"]["fetched_at"] = old_iso

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
