"""TDD tests for governor.digest -- build_attention_body + escalate_key."""


def test_escalate_key_is_stable_and_hex16():
    from governor.digest import escalate_key
    escalated = [
        {"source": "s1", "severity": "error", "summary": "boom", "reason": "error", "ref": "url1"},
        {"source": "s2", "severity": "warning", "summary": "bad", "reason": "worsened ok->warning", "ref": "url2"},
    ]
    key1 = escalate_key(escalated)
    key2 = escalate_key(escalated)
    assert key1 == key2
    assert len(key1) == 16
    assert all(c in "0123456789abcdef" for c in key1)


def test_escalate_key_is_order_independent():
    from governor.digest import escalate_key
    a = [
        {"source": "s1", "severity": "error"},
        {"source": "s2", "severity": "warning"},
    ]
    b = [
        {"source": "s2", "severity": "warning"},
        {"source": "s1", "severity": "error"},
    ]
    assert escalate_key(a) == escalate_key(b)


def test_escalate_key_differs_on_different_set():
    from governor.digest import escalate_key
    a = [{"source": "s1", "severity": "error"}]
    b = [{"source": "s1", "severity": "warning"}]
    assert escalate_key(a) != escalate_key(b)


def test_build_attention_body_contains_footer_and_source():
    from governor.digest import build_attention_body
    escalated = [
        {"source": "game-governance-drift", "severity": "error",
         "reason": "error", "summary": "3 errors", "ref": "https://example.com"},
    ]
    body = build_attention_body(escalated, dropped_count=4)
    assert "game-governance-drift" in body
    assert "error" in body
    assert "4 signal(s) below escalation threshold" in body
    assert "/governor pane" in body


def test_build_attention_body_has_no_timestamp():
    """Body must have NO timestamp so idempotency is preserved."""
    import re
    from governor.digest import build_attention_body
    escalated = [
        {"source": "s1", "severity": "error", "reason": "error", "summary": "x", "ref": ""},
    ]
    body = build_attention_body(escalated, dropped_count=0)
    # No ISO timestamp pattern (YYYY-MM-DD or HH:MM)
    assert not re.search(r"\d{4}-\d{2}-\d{2}", body), "body must not contain a date"
    assert not re.search(r"\d{2}:\d{2}:\d{2}", body), "body must not contain a time"


def test_build_attention_body_is_ascii_only():
    from governor.digest import build_attention_body
    escalated = [
        {"source": "s1", "severity": "error", "reason": "error", "summary": "ascii only", "ref": ""},
    ]
    body = build_attention_body(escalated, dropped_count=0)
    assert all(ord(c) < 128 for c in body), "body must be ASCII-only"
