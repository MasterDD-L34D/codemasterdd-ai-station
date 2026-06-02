"""TDD tests for eng-graph staleness-escalation (now-aware severity).

The eng-graph MOC signal was info-only (never escalated). This makes it
escalate when the MOC's last_verified goes stale: the parser derives severity
from age (now - last_verified) -- info if fresh, warning past STALE_WARN_DAYS,
error past STALE_ERROR_DAYS. Severity is folded into the payload_hash so a
staleness transition (e.g. info->warning) is a DISTINCT row, which the existing
worsened-delta classifier then escalates (R1). This IS an autonomy-behavior
change (the actor will now open an attention issue on a stale MOC).

now is injected (a datetime.date); the I/O boundary (ingest_all) passes
date.today(). When now is None the parser stays info (backward-compatible with
the clock-free callers), so staleness is opt-in and deterministic under test.
"""
from __future__ import annotations

from datetime import date

_MD = (
    "---\nlast_verified: 2026-05-31\n---\n"
    "<!-- eng-graph:auto -->\n"
    "- [[x]] repo `game`\n"
    "<!-- /eng-graph:auto -->\n"
)


def test_eng_graph_stale_beyond_warn_threshold_is_warning():
    from governor.parsers import parse_eng_graph_moc
    # last_verified 2026-05-31, now 2026-07-15 -> 45 days stale (> 30 warn).
    sig = parse_eng_graph_moc(_MD, "r", now=date(2026, 7, 15))
    assert sig.severity == "warning"


def test_eng_graph_stale_beyond_error_threshold_is_error():
    from governor.parsers import parse_eng_graph_moc
    # last_verified 2026-05-31, now 2026-09-30 -> ~122 days stale (> 90 error).
    sig = parse_eng_graph_moc(_MD, "r", now=date(2026, 9, 30))
    assert sig.severity == "error"


def test_eng_graph_severity_change_yields_distinct_hash():
    """Load-bearing: a staleness transition must be a DISTINCT signal row so the
    worsened-delta classifier escalates it. The signals table dedups by
    payload_hash, so severity must be folded into the hash -- otherwise the same
    MOC content at fresh vs stale `now` would collide and no escalation row exists."""
    from governor.parsers import parse_eng_graph_moc
    fresh = parse_eng_graph_moc(_MD, "r", now=date(2026, 6, 2))   # info
    stale = parse_eng_graph_moc(_MD, "r", now=date(2026, 7, 15))  # warning
    assert fresh.severity == "info" and stale.severity == "warning"
    assert fresh.payload_hash != stale.payload_hash


def test_produce_eng_graph_threads_now_for_staleness():
    """ingest._produce must forward `now` to the eng-graph parser, else staleness
    never activates in production (the parser would always see now=None = info)."""
    from governor.ingest import _produce, ENG_GRAPH_MOC_API

    def content_getter(url):
        if url == ENG_GRAPH_MOC_API:
            return _MD
        raise AssertionError(f"unexpected content url {url}")

    src = {"id": "vault-eng-graph", "style": "vault-fixed", "api_url": ENG_GRAPH_MOC_API}
    sig = _produce(src, fetcher=None, json_getter=None, content_getter=content_getter,
                   now=date(2026, 9, 30))  # ~122 days stale -> error
    assert sig.severity == "error"


def test_eng_graph_summary_labels_created_when_no_last_verified():
    """harsh-reviewer P2: when the date comes from the `created` fallback, the
    summary must say 'created', not mislabel it as 'last_verified'."""
    from governor.parsers import parse_eng_graph_moc
    md = (
        "---\ncreated: 2026-05-01\n---\n"
        "<!-- eng-graph:auto -->\n- [[x]] repo `g`\n<!-- /eng-graph:auto -->\n"
    )
    sig = parse_eng_graph_moc(md, "r")
    assert "created 2026-05-01" in sig.summary
    assert "last_verified" not in sig.summary


def test_eng_graph_datetime_now_degrades_to_info_not_crash():
    """harsh-reviewer P2: a future caller passing a datetime (not a date) must not
    crash the parser (datetime - date raises TypeError, NOT ValueError); degrade to
    info so the source does not silently become an ingest-error."""
    from datetime import datetime
    from governor.parsers import parse_eng_graph_moc
    sig = parse_eng_graph_moc(_MD, "r", now=datetime(2026, 9, 30, 12, 0))
    assert sig.severity == "info"


def test_eng_graph_same_warn_band_same_hash_no_spam():
    """harsh-reviewer P1: two `now` values in the SAME band yield the SAME hash, so
    a MOC stuck stale is ONE row -> the actor's escalate_key stays constant -> the
    issue is created once then noop (no spam). Pins the latch against hash refactors."""
    from governor.parsers import parse_eng_graph_moc
    a = parse_eng_graph_moc(_MD, "r", now=date(2026, 7, 15))  # 45d warning
    b = parse_eng_graph_moc(_MD, "r", now=date(2026, 7, 25))  # 55d warning
    assert a.severity == "warning" and b.severity == "warning"
    assert a.payload_hash == b.payload_hash
