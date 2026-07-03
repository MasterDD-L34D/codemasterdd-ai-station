"""Smoke tests for module-level pre-compiled regexes (PR #98 follow-up).

Verifica che ognuna delle 8 regex hoistate a module-level continui a:
- matchare pattern previsti (happy path)
- NON matchare pattern simili-ma-differenti (regression guard)
- estrarre group correttamente quando il pattern lo prevede

Se queste smoke spezzano dopo un refactor, la dashboard auto-refresh perderebbe
silenziosamente Gate E events / ADR countdown / OD entries / Journal preview.

Note: app imports moved INSIDE test functions (post Codex P2 fix on PR #99)
so the `mock_external_deps` autouse fixture runs first.
"""

from __future__ import annotations


def test_gate_e_row_re_matches_dated_table_row():
    from app import _GATE_E_ROW_RE
    assert _GATE_E_ROW_RE.match("| 2026-05-15 | event |") is not None
    assert _GATE_E_ROW_RE.match("|2026-12-31|noop|") is not None
    assert _GATE_E_ROW_RE.match("not a row") is None
    assert _GATE_E_ROW_RE.match("| 2025-05-15 | old year |") is None


def test_adr_status_proposed_re_matches_bold_and_plain():
    from app import _ADR_STATUS_PROPOSED_RE
    assert _ADR_STATUS_PROPOSED_RE.search("Status: Proposed") is not None
    assert _ADR_STATUS_PROPOSED_RE.search("**Status**: Proposed") is not None
    assert _ADR_STATUS_PROPOSED_RE.search("status:proposed") is not None  # ignorecase
    assert _ADR_STATUS_PROPOSED_RE.search("Status: Accepted") is None


def test_adr_ratify_date_re1_extracts_iso_date():
    from app import _ADR_RATIFY_DATE_RE1
    m = _ADR_RATIFY_DATE_RE1.search("**Ratification check date**: 2026-05-19")
    assert m is not None and m.group(1) == "2026-05-19"


def test_adr_ratify_date_re2_fallback_loose():
    from app import _ADR_RATIFY_DATE_RE2
    m = _ADR_RATIFY_DATE_RE2.search("ratification by 2026-06-30 expected")
    assert m is not None and m.group(1) == "2026-06-30"


def test_adr_ratify_date_re3_italian_entro():
    from app import _ADR_RATIFY_DATE_RE3
    m = _ADR_RATIFY_DATE_RE3.search("entro 2026-12-31 verra' chiuso")
    assert m is not None and m.group(1) == "2026-12-31"


def test_adr_num_re_extracts_four_digit_prefix():
    from app import _ADR_NUM_RE
    m = _ADR_NUM_RE.match("0030-post-max-orchestration.md")
    assert m is not None and m.group(1) == "0030"
    assert _ADR_NUM_RE.match("foo-bar.md") is None


def test_od_entry_re_extracts_id_and_title():
    from app import _OD_ENTRY_RE
    m = _OD_ENTRY_RE.search("### [OD-005] Tavily integration deferred")
    assert m is not None
    assert m.group(1) == "OD-005"
    assert "Tavily" in m.group(2)


def test_journal_date_re_matches_header():
    from app import _JOURNAL_DATE_RE
    assert _JOURNAL_DATE_RE.match("## 2026-05-15 (mezzogiorno)") is not None
    assert _JOURNAL_DATE_RE.match("## Generic header") is None


def test_journal_header_re_extracts_full_header_text():
    from app import _JOURNAL_HEADER_RE
    m = _JOURNAL_HEADER_RE.match("## 2026-05-15 -- entry title")
    assert m is not None and m.group(1) == "2026-05-15 -- entry title"


def test_spend_cum_re_extracts_dollar_amount():
    from app import _SPEND_CUM_RE
    m = _SPEND_CUM_RE.search("- **Cumulative cost mese**: $12.3456")
    assert m is not None and m.group(1) == "12.3456"
    assert _SPEND_CUM_RE.search("- **Cumulative cost mese**: $0.0000").group(1) == "0.0000"
    assert _SPEND_CUM_RE.search("no cumulative line here") is None
