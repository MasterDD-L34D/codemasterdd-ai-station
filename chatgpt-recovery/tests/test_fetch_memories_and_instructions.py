import importlib.util
from pathlib import Path
import pytest
import datetime

@pytest.fixture(scope="module")
def fetch_script():
    script_path = Path(__file__).parent.parent / "scripts" / "fetch-memories-and-instructions.py"
    spec = importlib.util.spec_from_file_location("fetch_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class MockDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2024, 1, 1, 12, 0, 0)

def test_memory_to_md_happy_path(fetch_script, monkeypatch):
    monkeypatch.setattr(fetch_script, "datetime", MockDatetime)

    data = {
        "memory_num_tokens": 150,
        "memory_max_tokens": 1000,
        "memories": [
            {
                "id": "mem_123",
                "content": "User prefers Markdown formatting.",
                "created_at": 1704067200, # 2024-01-01T00:00:00 UTC
                "updated_at": 1704153600  # 2024-01-02T00:00:00 UTC
            },
            {
                "id": "mem_456",
                "text": "User is from Italy.",
                "created_at": 1704067200
            },
            {
                "id": "mem_789",
                "content": "No timestamps."
            }
        ]
    }

    result = fetch_script.memory_to_md(data)

    # fmt_ts() renders epoch seconds via datetime.fromtimestamp() (local tz),
    # so derive the expected strings the same way to stay timezone-independent.
    created_1 = datetime.datetime.fromtimestamp(1704067200).isoformat()
    updated_1 = datetime.datetime.fromtimestamp(1704153600).isoformat()

    assert "# ChatGPT Memory Items Export -- 2024-01-01T12:00:00" in result
    assert "Memory tokens used: 150 / 1000" in result
    assert "Total items: 3" in result

    assert "### 1. (id `mem_123`)" in result
    assert "User prefers Markdown formatting." in result
    assert f"_created: {created_1} | updated: {updated_1}_" in result

    assert "### 2. (id `mem_456`)" in result
    assert "User is from Italy." in result
    assert f"_created: {created_1}_" in result

    assert "### 3. (id `mem_789`)" in result
    assert "No timestamps." in result
    assert "_(no content field)_" not in result

def test_memory_to_md_empty(fetch_script, monkeypatch):
    monkeypatch.setattr(fetch_script, "datetime", MockDatetime)

    data = {}

    result = fetch_script.memory_to_md(data)

    assert "# ChatGPT Memory Items Export -- 2024-01-01T12:00:00" in result
    assert "Memory tokens used: ? / ?" in result
    assert "Total items: 0" in result
    assert "## Items" in result
