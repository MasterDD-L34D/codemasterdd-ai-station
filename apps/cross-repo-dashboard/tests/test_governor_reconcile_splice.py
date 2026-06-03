"""TDD tests for governor.reconcile.splice -- pure idempotent region-replace + create-if-absent.

splice wraps the render output in GOVERNOR-SYNC markers and replaces the region in place; it
never touches prose outside the markers, never injects a timestamp, and creates the file when
absent (the new vault doc). Network/gh NEVER hit (pure function).
"""
import re

MARKER = ("<!-- GOVERNOR-SYNC:signals BEGIN -->", "<!-- GOVERNOR-SYNC:signals END -->")


def test_splice_first_inject_after_anchor_preserves_prose():
    from governor.reconcile import splice
    doc = "# STATUS_MULTI_REPO -- dashboard\n\nhuman prose here\n\n## Snapshot\nrow\n"
    out = splice(doc, MARKER, "TABLE", anchor="# STATUS_MULTI_REPO")
    assert "human prose here" in out
    assert "## Snapshot" in out
    assert MARKER[0] in out and MARKER[1] in out
    assert "TABLE" in out
    # block landed right after the anchor line, before the existing prose
    assert out.index(MARKER[0]) > out.index("# STATUS_MULTI_REPO")
    assert out.index(MARKER[0]) < out.index("human prose here")


def test_splice_is_idempotent():
    from governor.reconcile import splice
    doc = "# STATUS_MULTI_REPO -- dashboard\n\nprose\n"
    once = splice(doc, MARKER, "TABLE", anchor="# STATUS_MULTI_REPO")
    twice = splice(once, MARKER, "TABLE", anchor="# STATUS_MULTI_REPO")
    assert once == twice


def test_splice_replaces_region_on_drift():
    from governor.reconcile import splice
    doc = "# STATUS_MULTI_REPO\n"
    v1 = splice(doc, MARKER, "OLD", anchor="# STATUS_MULTI_REPO")
    v2 = splice(v1, MARKER, "NEW", anchor="# STATUS_MULTI_REPO")
    assert "NEW" in v2 and "OLD" not in v2
    assert v2.count(MARKER[0]) == 1 and v2.count(MARKER[1]) == 1


def test_splice_create_if_absent_uses_header():
    from governor.reconcile import splice
    header = "---\ntitle: x\n---\n\n# Vault lint status"
    out = splice("", MARKER, "TABLE", create_header=header)
    assert out.startswith("---")
    assert "# Vault lint status" in out
    assert MARKER[0] in out and "TABLE" in out and MARKER[1] in out
    # idempotent: re-splice the created doc -> identical
    assert splice(out, MARKER, "TABLE", create_header=header) == out


def test_splice_no_timestamp_in_region():
    from governor.reconcile import splice
    out = splice("", MARKER, "severity | ok", create_header="# x")
    region = out[out.index(MARKER[0]):out.index(MARKER[1])]
    assert not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", region)  # no ISO timestamp injected


def test_splice_backslash_in_region_is_literal():
    from governor.reconcile import splice
    out = splice("", MARKER, r"a\1b\g<0>c", create_header="# x")
    assert r"a\1b\g<0>c" in out  # no regex-replacement backref interpretation
