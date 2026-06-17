"""Tests for scripts/governance/doctrine_triage.py (ADR-0040).

The triage label is a HINT for a human reviewer, never a gate. These tests pin
the deterministic classification + the fail-closed behaviour.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "governance"))
import doctrine_triage as dt  # noqa: E402


def test_hint_only_contract():
    # constants exist + the module documents that it never gates a merge
    assert dt.LOOSENING == "loosening-surface"
    assert dt.PROSE_ONLY == "prose-only"
    assert "NEVER merges" in dt.__doc__ or "never merges" in dt.__doc__.lower()


def test_split_diff_helper():
    diff = "+++ b/x\n--- a/x\n+added line\n-removed line\n context\n"
    added, removed = dt.split_diff(diff)
    assert added == ["added line"]
    assert removed == ["removed line"]


def test_pure_prose_typo_in_adr_is_prose_only():
    diff = "--- a/docs/adr/0002-x.md\n+++ b/docs/adr/0002-x.md\n-The repo is named CodeMasterDD.\n+The repo is named the CodeMasterDD AI Station.\n"
    res = dt.triage(diff, ["docs/adr/0002-codemasterdd-naming.md"])
    assert res["label"] == dt.PROSE_ONLY
    assert res["signals"] == []


def test_governance_md_prose_is_prose_only():
    diff = "+The human reviewer reads the change carefully before acting.\n"
    res = dt.triage(diff, ["docs/governance/actor-activation-criteria.md"])
    assert res["label"] == dt.PROSE_ONLY


def test_settings_json_change_is_loosening():
    res = dt.triage("+  some line\n", [".claude/settings.json"])
    assert res["label"] == dt.LOOSENING
    assert any(s.startswith("capability-file:.claude/settings.json") for s in res["signals"])


def test_allow_rule_token_is_loosening():
    diff = '+      "allow": ["Bash(gh pr merge:*)"]\n'
    res = dt.triage(diff, ["docs/governance/some-policy.md"])
    assert res["label"] == dt.LOOSENING


def test_autonomy_threshold_change_is_loosening():
    diff = (
        "-- [ ] >= 4 distinct CLEAN R1 cycles across >= 2 repos\n"
        "+- [ ] >= 2 distinct CLEAN R1 cycles across >= 1 repos\n"
    )
    res = dt.triage(diff, ["docs/governance/actor-activation-criteria.md"])
    assert res["label"] == dt.LOOSENING
    assert "threshold-change" in res["signals"]


def test_hook_code_change_is_loosening_non_prose_file():
    res = dt.triage("+  if (x) return 0;\n", ["scripts/hooks/commit-guard.js"])
    assert res["label"] == dt.LOOSENING
    assert any(s.startswith("non-prose-governance-file:") for s in res["signals"])


def test_fail_closed_non_md_governance_file_empty_diff():
    # no diff content at all, but a non-markdown governance file changed -> loosening
    res = dt.triage("", [".claude/agents/owasp-security-auditor.md"])
    # owasp file is .md prose -> prose-only (no signal)
    assert res["label"] == dt.PROSE_ONLY
    res2 = dt.triage("", [".claude/hooks.json"])
    assert res2["label"] == dt.LOOSENING


def test_enforce_admins_token_is_loosening():
    diff = "+  enforce_admins: false\n"
    res = dt.triage(diff, ["docs/adr/0040-x.md"])
    assert res["label"] == dt.LOOSENING
