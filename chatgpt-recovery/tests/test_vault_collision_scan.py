import pytest
from pathlib import Path
import sys
import importlib.util

# Load the script module programmatically since it has dashes in its name
script_path = Path("chatgpt-recovery/pipeline/vault-collision-scan.py")
spec = importlib.util.spec_from_file_location("vault_collision_scan", script_path)
vcs = importlib.util.module_from_spec(spec)
sys.modules["vault_collision_scan"] = vcs
spec.loader.exec_module(vcs)

def test_tokenize_empty():
    """Test empty string and None."""
    assert vcs.tokenize("") == set()
    assert vcs.tokenize(None) == set()

def test_tokenize_basic():
    """Test basic tokenization functionality."""
    assert vcs.tokenize("hello world") == {"hello", "world"}

def test_tokenize_case_insensitivity():
    """Test that words are converted to lowercase."""
    assert vcs.tokenize("HELLO WoRld") == {"hello", "world"}

def test_tokenize_stopwords():
    """Test that English and Italian stopwords are excluded."""
    # Italian stopwords from the script
    assert "con" not in vcs.tokenize("cane con gatto")
    assert "della" not in vcs.tokenize("storia della vita")
    assert "gli" not in vcs.tokenize("gli animali")

    # English stopwords from the script
    assert "the" not in vcs.tokenize("the dog is here")
    assert "are" not in vcs.tokenize("we are testing")
    assert "and" not in vcs.tokenize("cats and dogs")

def test_tokenize_length_filter():
    """Test that only words >= 3 characters are kept."""
    assert vcs.tokenize("a bb ccc dddd") == {"ccc", "dddd"}

def test_tokenize_accents():
    """Test that accented characters are handled correctly."""
    assert vcs.tokenize("città perché così") == {"città", "perché", "così"}

def test_tokenize_punctuation():
    """Test that punctuation is handled and splits words."""
    assert vcs.tokenize("hello, world! this-is a test.") == {"hello", "world", "this", "test"}
