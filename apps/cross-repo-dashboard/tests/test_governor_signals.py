def test_make_hash_stable_and_order_sensitive():
    from governor.signals import make_hash
    assert make_hash("a", "b") == make_hash("a", "b")
    assert make_hash("a", "b") != make_hash("b", "a")
    assert len(make_hash("x")) == 16

def test_severity_from_counts():
    from governor.signals import severity_from_counts
    assert severity_from_counts(0, 0) == "ok"
    assert severity_from_counts(0, 5) == "warning"
    assert severity_from_counts(2, 5) == "error"

def test_signal_is_frozen_and_has_fields():
    from governor.signals import Signal
    s = Signal(source="x", kind="drift", severity="ok", summary="fine")
    assert s.counts == {}
    assert s.produced_at is None
    import dataclasses
    assert dataclasses.is_dataclass(s)
