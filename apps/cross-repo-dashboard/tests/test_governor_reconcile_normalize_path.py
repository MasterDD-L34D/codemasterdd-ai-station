"""Direct edge-case tests for _normalize_path in governor.reconcile."""
import pytest
from governor.reconcile import _normalize_path


def test_normalize_path_none_and_empty():
    """None -> "" and "" -> "" """
    assert _normalize_path(None) == ""
    assert _normalize_path("") == ""


def test_normalize_path_backslashes():
    """Backslashes become forward slashes."""
    assert _normalize_path("a\\b\\c") == "a/b/c"


def test_normalize_path_surrounding_whitespace():
    """Surrounding whitespace stripped."""
    assert _normalize_path("  x/y  ") == "x/y"


@pytest.mark.parametrize("path,expected", [
    ("./x", "x"),
    ("././x", "x"),
])
def test_normalize_path_leading_dot_slash(path, expected):
    """Leading "./" stripped repeatedly."""
    assert _normalize_path(path) == expected


def test_normalize_path_single_leading_tilde_slash():
    """A single leading "~/" stripped."""
    assert _normalize_path("~/foo") == "foo"


@pytest.mark.parametrize("path,expected", [
    ("/abs/path", "abs/path"),
    ("///a", "a"),
])
def test_normalize_path_leading_slashes(path, expected):
    """Leading slashes stripped."""
    assert _normalize_path(path) == expected


def test_normalize_path_order_sensitive_combo():
    """Order-sensitive combo: '~/./x' -> './x'"""
    assert _normalize_path("~/./x") == "./x"


def test_normalize_path_backslash_introduced_dot_slash():
    """A backslash-introduced './' is normalized then stripped."""
    assert _normalize_path(".\\x") == "x"
