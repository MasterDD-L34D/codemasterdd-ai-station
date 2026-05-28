import pytest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

@pytest.fixture(scope="module")
def extract_module():
    """Load hyphenated script via importlib spec, scoped to avoid global pollution."""
    script_path = Path(__file__).parent.parent / "extract-entities.py"
    spec = spec_from_file_location("extract_entities", str(script_path))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

@pytest.mark.parametrize("input_text, expected", [
    ("", []),
    (None, []),
])
def test_extract_entities_empty_input(extract_module, input_text, expected):
    """Test behavior with empty or null input strings."""
    func = extract_module.extract_entities_from_text
    assert func(input_text) == expected

@pytest.mark.parametrize("input_text, expected", [
    ("il villaggio di Hao", ["Hao"]),
    ("il maestro Hao Jin", ["Hao Jin"]),
    ("capitano Jean-Luc", ["Jean-Luc"]),
    ("il demone Vhar'nak", ["Vhar'nak"]),
])
def test_extract_entities_valid_names(extract_module, input_text, expected):
    """Test extraction of single capitalized words, multi-word entities, hyphenated names, and apostrophes."""
    func = extract_module.extract_entities_from_text
    assert func(input_text) == expected

@pytest.mark.parametrize("input_text, unexpected", [
    ("Mockedword", "Mockedword"),
    ("Skipthis libro", "Skipthis"),
])
def test_extract_entities_skip_words(extract_module, input_text, unexpected, monkeypatch):
    """Test filtering of generic stop words by mocking the SKIP_WORDS list."""
    monkeypatch.setattr(extract_module, "SKIP_WORDS", {"Mockedword", "Skipthis"})
    func = extract_module.extract_entities_from_text
    assert unexpected not in func(input_text)

@pytest.mark.parametrize("input_text, unexpected", [
    ("il personaggio Bo", "Bo"),
    ("il nome Lu", "Lu"),
])
def test_extract_entities_short_words(extract_module, input_text, unexpected):
    """Test filtering of words shorter than 3 characters."""
    func = extract_module.extract_entities_from_text
    assert unexpected not in func(input_text)

def test_extract_entities_complex_sentence(extract_module):
    """Test extraction of multiple valid entities in a longer text."""
    func = extract_module.extract_entities_from_text
    text = "Vhar'nak ha parlato con Hao Jin a Waterdeep."
    entities = func(text)
    assert "Vhar'nak" in entities
    assert "Hao Jin" in entities
    assert "Waterdeep" in entities

def test_extract_entities_skip_words_exact_match(extract_module, monkeypatch):
    """Test that skip words don't prevent match on words starting with skip words."""
    monkeypatch.setattr(extract_module, "SKIP_WORDS", {"Mock"})
    func = extract_module.extract_entities_from_text
    assert "Mockingbird" in func("leggere Mockingbird")
