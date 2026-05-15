"""Tests for migrate-log-to-sqlite.py extract_cumulative_table.

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
def migrate_module():
    """Load hyphenated script via importlib spec, scoped (no global pollution).

    Module loaded once per test module, returned to tests, NEVER registered in
    global sys.modules -- avoids the contamination anti-pattern.
    """
    script_path = Path(__file__).parent.parent / "migrate-log-to-sqlite.py"
    spec = spec_from_file_location("migrate_log_to_sqlite", str(script_path))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_extract_cumulative_table_invalid_id(migrate_module):
    """Rows with non-numeric id are skipped, valid numeric-id rows kept."""
    extract_cumulative_table = migrate_module.extract_cumulative_table

    md_text = """### Cumulative Fase 6 dataset

| # | Task | Classe | Stack | Retry | Success | Note |
|---|---|---|---|---|---|---|
| 1 | valid row | behavior | stack1 | 0 | ✅ | note |
| invalid_id | skipped row | behavior | stack2 | 0 | ✅ | note |
| 2 | valid row 2 | behavior | stack3 | 0 | ✅ | note |
"""

    rows = extract_cumulative_table(md_text)

    assert len(rows) == 2
    assert rows[0]["id"] == 1
    assert rows[1]["id"] == 2
