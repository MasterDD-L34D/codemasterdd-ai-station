import importlib.util
from pathlib import Path
import pytest

_spec = importlib.util.spec_from_file_location(
    "autofill_disp", Path(__file__).resolve().parent / "autofill-disposition.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)
classify_topic = mod.classify_topic

def test_mixed_misc_outlier_default():
    assert classify_topic('mixed-misc') == ('HOLD', '')
    assert classify_topic('something outlier here') == ('HOLD', '')

def test_specific_keywords():
    assert classify_topic('torneo cremesi') == ('PROMOTE', 'GDR/TorneoCremesi')
    assert classify_topic('pathfinder campaign') == ('PROMOTE', 'GDR/Pathfinder')
    assert classify_topic('some api docs') == ('PROMOTE', 'Dev/_tech-meta')
    assert classify_topic('una canzone') == ('HOLD', '_personal')

def test_case_insensitivity():
    assert classify_topic('CREMESI') == ('PROMOTE', 'GDR/TorneoCremesi')
    assert classify_topic('PaThFiNdEr') == ('PROMOTE', 'GDR/Pathfinder')

def test_non_matching_label():
    assert classify_topic('unknown label with no keywords') == ('HOLD', '')

def test_precedence_mixed_misc():
    assert classify_topic('mixed-misc and cremesi') == ('HOLD', '')
