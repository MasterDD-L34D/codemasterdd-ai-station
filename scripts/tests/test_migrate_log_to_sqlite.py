import pytest
import sys
from pathlib import Path

# Add scripts directory to sys.path to import migrate_log_to_sqlite
scripts_dir = Path(__file__).parent.parent
sys.path.append(str(scripts_dir))

from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location("migrate_log_to_sqlite", str(scripts_dir / "migrate-log-to-sqlite.py"))
migrate_log_to_sqlite = module_from_spec(spec)
sys.modules["migrate_log_to_sqlite"] = migrate_log_to_sqlite
spec.loader.exec_module(migrate_log_to_sqlite)

def test_extract_cumulative_table_invalid_id():
    from migrate_log_to_sqlite import extract_cumulative_table

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
