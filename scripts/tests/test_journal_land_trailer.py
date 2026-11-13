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


def test_merge_preserves_trailers():
    # squash-merge rewrites the commit: drops Coding-Agent/Trace-Id and adds a
    # GitHub Co-authored-by line (forbidden by ADR-0011). Seen on #591.
    # Rebase-merge keeps the authored commit message verbatim.
    merges = re.findall(r"gh pr merge[^\r\n]*", script_text())
    assert merges, "no gh pr merge call found"
    for line in merges:
        assert "--squash" not in line, f"squash drops ADR-0011 trailers: {line!r}"
        assert "--rebase" in line, f"merge must use --rebase: {line!r}"


def test_merge_waits_for_ci():
    # `gh pr merge --auto` on a repo without required checks merges at once,
    # before CI runs (#591 merged 4s, #593 5s after create, pytest still running).
    merges = re.findall(r"gh pr merge[^\r\n]*", script_text())
    for line in merges:
        assert "--auto" not in line, f"--auto skips the CI wait: {line!r}"


def test_merge_outcome_from_pr_state():
    # gh exits non-zero after a good merge when the clone has a detached HEAD
    # (local --delete-branch step), so success must be read from the PR state.
    assert re.search(r"gh pr view \$branch --json state", script_text()), \
        "merge outcome must be read from PR state, not exit code"
