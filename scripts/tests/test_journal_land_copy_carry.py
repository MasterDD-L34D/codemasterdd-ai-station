"""Regression guard: journal-land.ps1 must carry the edit by COPY, never by stash.

History: the v2 carry (git stash push on the shared tree + stash apply in the
origin/main worktree) did a 3-way merge whose base was the shared HEAD, so it
ALWAYS conflicted when the shared tree sat on a feature branch divergent from
origin/main (n=2: journal landings #539 and #543, 2026-07-12). v3 copies the
reviewed working-tree bytes directly (WYSIWYG) and adds an anti-clobber guard.
These static asserts block a stash-carry reintroduction without executing
PowerShell (same pattern as test_journal_land_trailer.py).
"""

import re
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "fleet" / "journal-land.ps1"


def script_text():
    return SCRIPT.read_text(encoding="utf-8")


def test_no_stash_carry():
    # a 'git stash <subcommand>' invocation is the conflict-prone carry coming
    # back; also catch the v2 worktree form 'git -C <wt> stash apply' (the
    # header PROSE may mention 'git stash' while explaining the ban)
    hit = re.search(r"git\s+(-C\s+\S+\s+)?stash\s+(push|apply|pop|drop)", script_text())
    assert hit is None, f"stash carry reintroduced: {hit.group(0)!r} (guaranteed conflict on divergent feature branch)"


def test_copy_carry_with_fidelity_check():
    text = script_text()
    assert "Copy-Item -LiteralPath" in text, "direct copy carry missing"
    assert "hash-object" in text, "pre/post copy-fidelity hash check missing"


def test_anti_clobber_guard():
    text = script_text()
    assert "merge-base" in text, "origin-moved-since-base signal missing"
    assert "--numstat" in text, "deleted-lines signal missing"
    assert "$AcceptMerge" in text, "-AcceptMerge escape hatch missing"


def test_merge_fallback_when_auto_merge_disabled():
    text = script_text()
    assert text.count("gh pr merge") >= 2, "need --auto attempt plus direct-merge fallback"
    assert "gh pr checks" in text, "CI wait before the direct merge missing"
