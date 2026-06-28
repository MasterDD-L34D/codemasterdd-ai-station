import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "atomize_mod", Path(__file__).resolve().parent / "atomize.py"
)
atomize_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(atomize_mod)

yaml_escape = atomize_mod.yaml_escape
detect_language = atomize_mod.detect_language

def test_yaml_escape():
    # yaml_escape(None) == '""' and yaml_escape("") == '""'.
    assert yaml_escape(None) == '""'
    assert yaml_escape("") == '""'

    # A plain word is wrapped in quotes: yaml_escape("plain") == '"plain"'.
    assert yaml_escape("plain") == '"plain"'

    # A backslash is doubled: input one backslash between a and b -> output has two backslashes
    # between a and b, inside the surrounding quotes.
    assert yaml_escape("a\\b") == '"a\\\\b"'

    # An embedded double-quote is backslash-escaped inside the quotes.
    assert yaml_escape('"quoted"') == '"\\"quoted\\""'

    # A newline in the value becomes a single space (no literal newline in the output).
    assert yaml_escape("line1\nline2") == '"line1 line2"'

def test_detect_language():
    # Italian-dominant text (e.g. "che della sono questo come quindi") -> 'it'.
    assert detect_language("che della sono questo come quindi") == "it"

    # English-dominant text with more than 3 english markers (e.g. "the and with that for this from")
    # and no italian markers -> 'en'.
    assert detect_language("the and with that for this from") == "en"

    # Text with no markers (e.g. "xyz foo bar") -> 'mixed'.
    assert detect_language("xyz foo bar") == "mixed"

    # Text with exactly 3 english markers and no italian markers (e.g. "the and with") -> 'mixed'
    # (the branch requires en_markers > 3).
    assert detect_language("the and with") == "mixed"

