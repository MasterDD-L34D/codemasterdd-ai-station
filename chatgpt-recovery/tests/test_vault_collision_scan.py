import pytest
from pathlib import Path
import sys
import importlib.util

# Load the script module programmatically since it has dashes in its name
script_path = Path(__file__).parent.parent / "pipeline" / "vault-collision-scan.py"
spec = importlib.util.spec_from_file_location("vault_collision_scan", script_path)
vcs = importlib.util.module_from_spec(spec)
sys.modules["vault_collision_scan"] = vcs
spec.loader.exec_module(vcs)

def test_tokenize_empty():
    assert vcs.tokenize("") == set()
    assert vcs.tokenize(None) == set()

def test_tokenize_basic():
    assert vcs.tokenize("hello world") == {"hello", "world"}

def test_tokenize_case_insensitivity():
    assert vcs.tokenize("HELLO WoRld") == {"hello", "world"}

def test_tokenize_stopwords():
    # Test that English/Italian stopwords are removed
    assert vcs.tokenize("con cane della gatto the house") == {"cane", "gatto", "house"}

def test_tokenize_length_filter():
    # Only words >= 3 chars should be kept
    assert vcs.tokenize("a bb ccc dddd") == {"ccc", "dddd"}

def test_tokenize_accents():
    assert vcs.tokenize("citt\u00e0 perch\u00e9 cos\u00ec") == {"citt\u00e0", "perch\u00e9", "cos\u00ec"}

def test_tokenize_punctuation():
    assert vcs.tokenize("hello, world! testing-is a test.") == {"hello", "world", "testing", "test"}

