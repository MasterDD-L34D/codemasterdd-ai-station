"""Tests for the /entries/export.csv endpoint.

Edge cases covered: commas, embedded double-quotes, multi-line note fields,
empty DB, header columns including the latency_ms field.
"""
from __future__ import annotations

import csv
import io


def _seed(client, *payloads):
    for p in payloads:
        r = client.post("/api/entries", json=p)
        assert r.status_code == 201, r.get_json()


def test_csv_export_empty_returns_header_only(client):
    r = client.get("/entries/export.csv")
    assert r.status_code == 200
    assert r.mimetype == "text/csv"
    rows = list(csv.DictReader(io.StringIO(r.get_data(as_text=True))))
    assert rows == []


def test_csv_export_headers_and_filename(client):
    r = client.get("/entries/export.csv")
    cd = r.headers.get("Content-Disposition", "")
    assert cd.startswith('attachment; filename="dogfood-entries-')
    assert cd.endswith('.csv"')
    reader = csv.DictReader(io.StringIO(r.get_data(as_text=True)))
    assert reader.fieldnames is not None
    assert reader.fieldnames[0] == "id"
    # The latency_ms column added by the auto-pull feature must be in the export.
    assert "latency_ms" in reader.fieldnames
    assert "langfuse_trace_id" in reader.fieldnames


def test_csv_export_escapes_commas_quotes_and_newlines(client):
    _seed(client,
        {"task_description": "csv test alpha", "classe": "cosmetic",
         "stack": "7B-local-whole", "outcome": "success",
         "tokens_sent": 100, "tokens_received": 50, "cost_usd": 0.001,
         "commit_hash": "abcdef0", "langfuse_trace_id": "trace-1"},
        {"task_description": "csv test beta, with comma", "classe": "behavior",
         "stack": "14B-Q2-local-diff", "outcome": "partial",
         "tokens_sent": 200, "tokens_received": 150, "cost_usd": 0.005,
         "commit_hash": "1234567"},
        {"task_description": 'csv test gamma "with quotes"',
         "classe": "strategic", "stack": "claude-code-direct",
         "outcome": "success", "note": "line1\nline2"},
    )

    r = client.get("/entries/export.csv")
    assert r.status_code == 200
    rows = list(csv.DictReader(io.StringIO(r.get_data(as_text=True))))
    assert len(rows) == 3

    descs = {row["task_description"] for row in rows}
    assert "csv test alpha" in descs
    assert "csv test beta, with comma" in descs
    assert 'csv test gamma "with quotes"' in descs

    # Embedded newline preserved through CSV escaping.
    notes = [row["note"] for row in rows]
    assert any("line1\nline2" in n for n in notes)


def test_download_csv_button_on_entries_page(client):
    body = client.get("/entries").get_data(as_text=True)
    assert "Download CSV" in body
    assert "/entries/export.csv" in body
