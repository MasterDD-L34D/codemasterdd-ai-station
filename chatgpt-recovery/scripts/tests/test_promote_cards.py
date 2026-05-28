from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

@pytest.fixture(scope="module")
def promote_module():
    script_path = Path(__file__).parent.parent.parent / "pipeline" / "promote-cards.py"
    spec = spec_from_file_location("promote_cards", str(script_path))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_parse_review_md_normal(promote_module, tmp_path):
    parse_review_md = promote_module.parse_review_md

    md_content = """
Here is some text.
```yaml
topic_id: 101
disposition: split
```
More text.
```yaml
topic_id: 102
disposition: KEEP # some comment
```
"""
    test_md = tmp_path / "test.md"
    test_md.write_text(md_content, encoding="utf-8")

    decisions = parse_review_md(test_md)
    assert len(decisions) == 2
    assert decisions[0] == {"topic_id": 101, "disposition": "SPLIT"}
    assert decisions[1] == {"topic_id": 102, "disposition": "KEEP"}

def test_parse_review_md_spacing(promote_module, tmp_path):
    parse_review_md = promote_module.parse_review_md

    md_content = """
# Test varied spacing
  ```yaml
topic_id: 1
disposition: keep
```
Text here.
```yaml
topic_id: 2
disposition: split
   ```
More text.
```yaml

topic_id: 3
disposition: drop
```
"""
    test_md = tmp_path / "test.md"
    test_md.write_text(md_content, encoding="utf-8")

    decisions = parse_review_md(test_md)
    assert len(decisions) == 3, f"Expected 3 blocks, found {len(decisions)}"
    assert decisions[0]["topic_id"] == 1
    assert decisions[1]["topic_id"] == 2
    assert decisions[2]["topic_id"] == 3
