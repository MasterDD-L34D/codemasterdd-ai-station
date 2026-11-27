"""Tests for scripts/hooks/commit-guard.js (PreToolUse hook, ADR-0011).

Decision 2026-11-27 (Eduardo): the "Co-Authored-By:" trailer is banned for EVERY co-author, human or AI,
as in the global rules. The 2026-06-17 scope (AI co-authors only) is reverted.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "commit-guard.js"


def run(command: str) -> int:
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}}
    return subprocess.run(["node", str(HOOK)], input=json.dumps(payload), capture_output=True, text=True).returncode


def test_messaggio_multiriga_misura_solo_l_oggetto():
    corpo = "spiegazione lunga " * 10
    assert run(f'git commit -m "fix(x): oggetto corto\n\n{corpo}"') == 0


def test_commit_msg_blocca_anche_il_co_author_umano(tmp_path):
    msg = tmp_path / "COMMIT_EDITMSG"
    msg.write_text("fix(x): corregge y\n\nCoding-Agent: test\nTrace-Id: 01a21d6a-57b8-7ed0-84d7-e523cc9471f5\n"
                   "Co-Authored-By: Mario Rossi <m@example.com>\n", encoding="utf-8")
    hook = HOOK.parent / "commit-msg"
    # absolute path: a bare "bash" on Windows resolves to System32 (WSL) before PATH and fails for its own reasons
    p = subprocess.run([shutil.which("bash"), str(hook), msg.name], cwd=tmp_path, capture_output=True, text=True)
    assert p.returncode != 0 and "VIETATO" in p.stderr


def test_commit_msg_nei_repo_pathfinder_esige_coding_agent(tmp_path):
    repo = tmp_path / "pathfinder-prova"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / "COMMIT_EDITMSG").write_text("fix(x): corregge y\n", encoding="utf-8")
    p = subprocess.run([shutil.which("bash"), str(HOOK.parent / "commit-msg"), "COMMIT_EDITMSG"],
                       cwd=repo, capture_output=True, text=True)
    assert p.returncode != 0 and "Coding-Agent" in p.stderr


def test_co_author_umano_e_bloccato():
    assert run('git commit -m "fix(x): corregge y" -m "Co-Authored-By: Mario Rossi <m@example.com>"') == 2
