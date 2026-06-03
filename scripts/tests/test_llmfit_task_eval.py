"""Tests for llmfit-task-eval.py.

The script filename has hyphens so it cannot be imported via normal `import`.
We load it via importlib spec INSIDE a module-scoped fixture -- NOT at module
level with `sys.path.append` + `sys.modules[...] =` global mutation (that
pattern causes cross-test contamination; cf. L-2026-05-028 / L-2026-05-029
family + conftest fix on PR #102).
"""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def llmfit_module():
    """Load hyphenated script via importlib spec, scoped (no global pollution)."""
    script_path = Path(__file__).parent.parent / "llmfit-task-eval.py"
    spec = spec_from_file_location("llmfit_task_eval", str(script_path))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_extract_code(llmfit_module):
    """Test extracting code from markdown blocks with and without tags."""
    extract_code = llmfit_module.extract_code

    # 1. Fenced python block
    md_python = "```python\ndef test():\n    pass\n```"
    assert extract_code(md_python).strip() == "def test():\n    pass"

    # 2. Fenced block without python tag
    md_no_tag = "```\ndef test2():\n    pass\n```"
    assert extract_code(md_no_tag).strip() == "def test2():\n    pass"

    # 3. No fence at all
    md_no_fence = "def test3():\n    pass"
    assert extract_code(md_no_fence).strip() == "def test3():\n    pass"

def test_run_test_reference(llmfit_module):
    """Test that the reference implementation passes."""
    run_test = llmfit_module.run_test
    ref_code = llmfit_module._REFERENCE

    assert run_test(ref_code) is True

def test_run_test_broken(llmfit_module):
    """Test that a broken implementation fails."""
    run_test = llmfit_module.run_test
    broken_code = "def merge_intervals(intervals):\n    return intervals\n"

    assert run_test(broken_code) is False
