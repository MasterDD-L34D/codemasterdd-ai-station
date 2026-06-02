"""TDD tests for the ARCHON-learnings 8th signal source.

ARCHON lessons (L-YYYY-MM-NNN-*.md) live -- vendored on GitHub -- in the vault
repo at Vault-ops-remote/claude-global/aa01-system/learnings/. The local aa01 is
NON-git, so the vault vendor is the fleet-visible surface the governor can fetch
via the same authed contents-API path it already uses for vault.

Signal is INFO-severity by design: a learnings count is observability, never
"on fire". info never escalates (not error; and a steady info -> info is no
worsened-delta), so this source adds R0 visibility WITHOUT any autonomy change.
"""
from __future__ import annotations


def test_parse_archon_learnings_counts_lessons_and_names_latest():
    from governor.parsers import parse_archon_learnings
    entries = [
        {"name": "README.md"},
        {"name": "L-2026-05-002-foo.md"},
        {"name": "L-2026-05-038-bar.md"},
        {"name": "L-2026-05-014-baz.md"},
        {"name": "not-a-lesson.txt"},
    ]
    sig = parse_archon_learnings(entries, "https://api.github.com/x")
    assert sig.source == "archon-learnings"
    assert sig.kind == "learnings"
    assert sig.severity == "info"
    assert sig.counts["lessons"] == 3
    assert "L-2026-05-038" in sig.summary  # latest by lesson id
    assert sig.ref == "https://api.github.com/x"


def test_produce_archon_learnings_via_json_getter():
    from governor.ingest import _produce, ARCHON_LEARNINGS_API
    entries = [
        {"name": "L-2026-05-038-x.md"},
        {"name": "L-2026-05-002-y.md"},
        {"name": "README.md"},
    ]

    def json_getter(url):
        if url == ARCHON_LEARNINGS_API:
            return entries
        raise AssertionError(f"unexpected json url {url}")

    src = {"id": "archon-learnings", "style": "archon-learnings", "api_url": ARCHON_LEARNINGS_API}
    sig = _produce(src, fetcher=None, json_getter=json_getter, content_getter=None)
    assert sig.source == "archon-learnings"
    assert sig.counts["lessons"] == 2
