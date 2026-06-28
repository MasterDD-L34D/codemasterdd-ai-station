import re

def test_first_int_match_returns_captured_int():
    from governor.parsers import _first_int
    rx = re.compile(r"(\d+) cycles")
    assert _first_int(rx, "5 cycles") == 5

def test_first_int_no_match_returns_zero():
    from governor.parsers import _first_int
    rx = re.compile(r"(\d+) cycles")
    assert _first_int(rx, "no number here") == 0

def test_first_int_none_text_returns_zero():
    from governor.parsers import _first_int
    rx = re.compile(r"(\d+)")
    assert _first_int(rx, None) == 0

def test_first_int_empty_text_returns_zero():
    from governor.parsers import _first_int
    rx = re.compile(r"(\d+)")
    assert _first_int(rx, "") == 0

def test_first_int_first_match_wins():
    from governor.parsers import _first_int
    rx = re.compile(r"(\d+)")
    assert _first_int(rx, "3 then 9") == 3

def test_first_int_leading_zeros_parse_as_int():
    from governor.parsers import _first_int
    rx = re.compile(r"(\d+)")
    assert _first_int(rx, "007 agents") == 7
