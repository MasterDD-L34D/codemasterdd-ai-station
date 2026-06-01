def test_upsert_new_returns_true_then_false_on_same_hash(tmp_path):
    from governor.store import SignalStore
    from governor.signals import Signal
    store = SignalStore(tmp_path / "g.db")
    sig = Signal(source="s1", kind="drift", severity="warning",
                 summary="297 warnings", counts={"warnings": 297},
                 produced_at="2026-05-25T07:19:51+00:00", ref="url", payload_hash="h1")
    assert store.upsert(sig) is True      # new
    assert store.upsert(sig) is False     # unchanged (same source+hash)

def test_upsert_changed_hash_returns_true_and_latest_reflects_it(tmp_path):
    from governor.store import SignalStore
    from governor.signals import Signal
    store = SignalStore(tmp_path / "g.db")
    store.upsert(Signal(source="s1", kind="drift", severity="ok", summary="old", payload_hash="h1"))
    store.upsert(Signal(source="s1", kind="drift", severity="error", summary="new", payload_hash="h2"))
    rows = store.latest_per_source()
    assert len(rows) == 1
    assert rows[0]["summary"] == "new"
    assert rows[0]["severity"] == "error"

def test_latest_per_source_one_row_per_source(tmp_path):
    from governor.store import SignalStore
    from governor.signals import Signal
    store = SignalStore(tmp_path / "g.db")
    store.upsert(Signal(source="a", kind="gap", severity="ok", summary="A", payload_hash="1"))
    store.upsert(Signal(source="b", kind="digest", severity="info", summary="B", payload_hash="2"))
    sources = {r["source"] for r in store.latest_per_source()}
    assert sources == {"a", "b"}

def test_acted_on_count(tmp_path):
    from governor.store import SignalStore
    store = SignalStore(tmp_path / "g.db")
    assert store.acted_on_count() == 0
    store.record_acted_on("s1", "h1", note="merged PR")
    store.record_acted_on("s1", "h1", note="dup ignored")  # same key, idempotent
    store.record_acted_on("s2", "h9")
    assert store.acted_on_count() == 2

def test_auto_observed_is_separate_and_listable(tmp_path):
    from governor.store import SignalStore
    store = SignalStore(tmp_path / "g.db")
    store.add_auto_observed("s1", "signal-unconsumed", detail="new drift")
    recent = store.auto_observed_recent(limit=5)
    assert len(recent) == 1
    assert recent[0]["event"] == "signal-unconsumed"
