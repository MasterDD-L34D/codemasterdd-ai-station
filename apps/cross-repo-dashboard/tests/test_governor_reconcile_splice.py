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


# --- binary-contamination defence (vault #260: 13 trailing NUL bytes after EOF make git treat
# the governor-owned doc as BINARY, so the reconcile region diff renders "Binary files differ"
# and the human-reviewable point of the rung is defeated). splice must STRIP C0 control bytes
# (except tab/newline/CR) from every text input so a contaminated source self-heals on the next
# reconcile instead of carrying the binary forward (get_file decodes NUL as U+0000, splice
# preserves it, the PUT re-encodes it -> it never self-heals without this gate).

def test_splice_strips_trailing_nul_from_contaminated_doc():
    from governor.reconcile import splice
    # mirrors the real vault doc: 13 NULs at EOF, AFTER the END marker -- OUTSIDE the replaced
    # region, so region-replacement alone never removes them; the whole doc_text is sanitized.
    contaminated = (
        "---\ntitle: x\n---\n\n# Vault lint status\n\n"
        + MARKER[0] + "\nOLD\n" + MARKER[1] + "\n" + ("\x00" * 13)
    )
    out = splice(contaminated, MARKER, "NEW")
    assert "\x00" not in out
    assert "NEW" in out and "OLD" not in out
    assert "# Vault lint status" in out                 # prose preserved
    assert out.count(MARKER[0]) == 1 and out.count(MARKER[1]) == 1


def test_splice_strips_c0_controls_but_preserves_tab_newline():
    from governor.reconcile import splice
    doc = "# H\n\ncol\tval\x01\x1f\x7f\n" + MARKER[0] + "\nX\n" + MARKER[1] + "\n"
    out = splice(doc, MARKER, "X")
    for junk in ("\x00", "\x01", "\x0b", "\x0c", "\x1f", "\x7f"):
        assert junk not in out
    assert "col\tval" in out                            # tab + newline kept (legit whitespace)


def test_splice_is_noop_on_already_clean_text():
    from governor.reconcile import splice
    # already clean + region already synced -> EXACT no-op (the sanitize must not mutate clean
    # text: clean input -> byte-identical output, so idempotency / no-churn is preserved).
    doc = "# H\n\nprose\n" + MARKER[0] + "\nX\n" + MARKER[1] + "\n"
    assert splice(doc, MARKER, "X") == doc


def test_splice_create_path_emits_no_control_bytes_even_if_region_contaminated():
    from governor.reconcile import splice
    # create-if-absent recreate: even if the rendered region somehow carried a NUL, the emitted
    # doc must be clean text -- a recreate self-heals, it never re-emits binary.
    out = splice("", MARKER, "row\x00row", create_header="---\ntitle: x\n---\n\n# H")
    assert "\x00" not in out
    assert "rowrow" in out


def test_splice_strips_nul_anywhere_in_doc_text():
    from governor.reconcile import splice
    # NUL interior (inside the existing region) AND after the END marker, both via a contaminated
    # doc_text -> all stripped by the whole-doc sanitize, not just region-replacement.
    doc = "# H\n" + MARKER[0] + "\nrow\x00row\n" + MARKER[1] + "\ntail\x00text\n"
    out = splice(doc, MARKER, "NEW")
    assert "\x00" not in out
    assert "tailtext" in out                            # prose after END kept, NUL gone


def test_splice_keeps_replacement_char_scope_is_control_bytes_only():
    from governor.reconcile import splice
    # SCOPE GUARD: the gate strips C0/DEL control bytes ONLY, NOT the U+FFFD replacement char
    # that decode(errors="replace") folds invalid UTF-8 into. U+FFFD re-encodes as valid UTF-8
    # (text, not binary) so it is intentionally preserved -- not an all-binary healer. (Fails if
    # someone widens the strip table to all non-ASCII.) Built via chr() to keep source ASCII.
    fffd = chr(0xFFFD)
    doc = "# H " + fffd + " ok\n" + MARKER[0] + "\nX\n" + MARKER[1] + "\n"
    out = splice(doc, MARKER, "X")
    assert fffd in out
    assert "\x00" not in out
