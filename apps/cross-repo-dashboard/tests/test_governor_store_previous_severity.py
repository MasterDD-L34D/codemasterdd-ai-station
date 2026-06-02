"""TDD tests for SignalStore.previous_severity (R1 addition)."""


def test_previous_severity_returns_none_when_only_one_row(tmp_path):
    from governor.store import SignalStore
    from governor.signals import Signal
    store = SignalStore(tmp_path / "g.db")
    store.upsert(Signal(source="s1", kind="drift", severity="warning",
                        summary="one", payload_hash="h1"))
    assert store.previous_severity("s1") is None


def test_previous_severity_returns_second_most_recent(tmp_path):
    from governor.store import SignalStore
    from governor.signals import Signal
    store = SignalStore(tmp_path / "g.db")
    # Insert two distinct hashes for same source
    store.upsert(Signal(source="s1", kind="drift", severity="ok",
                        summary="old", payload_hash="h1"))
    store.upsert(Signal(source="s1", kind="drift", severity="warning",
                        summary="new", payload_hash="h2"))
    # latest = warning (h2), previous = ok (h1)
    assert store.previous_severity("s1") == "ok"
