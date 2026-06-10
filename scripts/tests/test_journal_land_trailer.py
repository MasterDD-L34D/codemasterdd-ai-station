"""Regression guard: journal-land.ps1 ADR-0011 trailer must stay parameterized.

History: the Coding-Agent trailer was hardcoded to a model id (claude-opus-4.8)
and went stale once sessions ran on other models (fixed in PR #316). These
static asserts block reintroduction without executing PowerShell.
"""

import re
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "fleet" / "journal-land.ps1"


def script_text():
    return SCRIPT.read_text(encoding="utf-8")


def test_script_exists():
    assert SCRIPT.is_file(), f"missing {SCRIPT}"


def test_no_model_pinned_trailer():
    # a literal model id after "Coding-Agent:" is the stale-hardcode regression
    pinned = re.search(r"Coding-Agent:\s*claude-(?!code\b)[\w.\-\[\]]+", script_text())
    assert pinned is None, f"model-pinned trailer reintroduced: {pinned.group(0)!r}"


def test_trailer_uses_variable_and_traceid():
    text = script_text()
    assert "Coding-Agent: $CodingAgent" in text, "trailer must use $CodingAgent variable"
    assert "Trace-Id: $(New-TraceId)" in text, "Trace-Id trailer must stay (ADR-0011)"


def test_param_env_fallback_chain():
    text = script_text()
    assert re.search(r"\[string\]\s*\$CodingAgent", text), "missing -CodingAgent param"
    assert "$env:CLAUDE_MODEL" in text, "missing CLAUDE_MODEL env fallback"
    assert "'claude-code'" in text, "missing generic 'claude-code' fallback"


def test_sanitizer_present():
    # polluted env var must not be able to corrupt the trailer block
    assert re.search(r"\$CodingAgent\s+-notmatch\s+'", script_text()), "missing ASCII-token sanitizer"
