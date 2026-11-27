"""Suspended Aider wrappers must fail loudly, never call a removed local model.

aider-cosmetic / aider-refactor pointed at qwen2.5-coder tags removed from the
fleet on 2026-11-27. No local role is promoted for cosmetic/refactor, so the
wrappers are stubs that print a suspension notice and exit non-zero.
"""
import subprocess
import sys
from pathlib import Path

import pytest

WRAPPERS_DIR = Path(__file__).resolve().parents[1] / "wrappers"
SUSPENDED = ["aider-cosmetic.cmd", "aider-refactor.cmd"]


@pytest.mark.parametrize("name", SUSPENDED)
def test_suspended_wrapper_has_no_executable_aider_line(name):
    lines = (WRAPPERS_DIR / name).read_text(encoding="ascii").splitlines()
    code = [ln.strip() for ln in lines if ln.strip() and not ln.strip().upper().startswith("REM")]
    assert not [ln for ln in code if ln.lower().startswith("aider")]
    assert "exit /b 1" in code


@pytest.mark.skipif(sys.platform != "win32", reason="cmd.exe wrapper")
@pytest.mark.parametrize("name", SUSPENDED)
def test_suspended_wrapper_exits_nonzero_with_notice(name):
    proc = subprocess.run(
        ["cmd", "/c", str(WRAPPERS_DIR / name), "somefile.py"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode != 0
    out = proc.stdout + proc.stderr
    assert "SOSPESO" in out
    assert "MODEL_ROUTING.md" in out
