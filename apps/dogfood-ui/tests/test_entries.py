"""Integration tests for entries lifecycle (form + JSON API + Langfuse auto-pull)."""
from __future__ import annotations

from unittest.mock import patch


FAKE_TRACE = {
    "id": "trace-xyz",
    "usage": {"input": 1000, "output": 500},
    "totalCost": 0.025,
    "latencyMs": 4200,
}


def test_health_endpoint(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.get_json()
    assert body["status"] == "ok"
    assert body["app"] == "dogfood-ui"


def test_create_entry_via_form_persists_trace_id(client):
    # Mock get_trace so the form POST does not fire a real HTTP request to
    # http://lf.example.com via enrich_from_langfuse. This test only cares
    # about URL rendering, not metadata auto-pull (covered separately).
    with patch("langfuse_client.LangfuseClient.get_trace", return_value=None):
        r = client.post("/entries/new", data={
            "task_description": "form test",
            "classe": "cosmetic",
            "stack": "other",
            "constraint_count": "0",
            "outcome": "success",
            "retry_count": "0",
            "tokens_sent": "0",
            "tokens_received": "0",
            "cost_usd": "0",
            "commit_hash": "",
            "langfuse_trace_id": "form-trace-001",
            "note": "",
        }, follow_redirects=True)
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    # Fallback URL (no LANGFUSE_PROJECT_ID set in the default fixture)
    assert "http://lf.example.com/trace/form-trace-001" in body


def test_create_entry_via_json_api(client):
    r = client.post("/api/entries", json={
        "task_description": "json test",
        "classe": "behavior",
        "stack": "14B-Q2-local-diff",
        "outcome": "success",
    })
    assert r.status_code == 201
    body = r.get_json()
    assert body["status"] == "created"
    assert isinstance(body["id"], int)
    assert body["langfuse_autofilled"] == []  # no trace_id => no autopull


def test_validation_errors_on_bad_classe(client):
    r = client.post("/api/entries", json={
        "task_description": "bad classe",
        "classe": "garbage",
        "stack": "other",
        "outcome": "success",
    })
    assert r.status_code == 400
    assert "classe" in r.get_json()["errors"][0]


def test_autopull_fills_zero_fields_from_langfuse(client):
    with patch("langfuse_client.LangfuseClient.get_trace", return_value=FAKE_TRACE):
        r = client.post("/api/entries", json={
            "task_description": "autopull test",
            "classe": "behavior",
            "stack": "14B-Q2-local-diff",
            "outcome": "success",
            "langfuse_trace_id": "trace-xyz",
        })
    body = r.get_json()
    assert r.status_code == 201
    assert sorted(body["langfuse_autofilled"]) == [
        "cost_usd", "latency_ms", "tokens_received", "tokens_sent",
    ]
    entries = client.get("/api/entries?limit=5").get_json()
    e = entries[0]
    assert e["tokens_sent"] == 1000
    assert e["tokens_received"] == 500
    assert abs(e["cost_usd"] - 0.025) < 1e-9
    assert e["latency_ms"] == 4200


def test_autopull_does_not_override_explicit_user_values(client):
    with patch("langfuse_client.LangfuseClient.get_trace", return_value=FAKE_TRACE):
        r = client.post("/api/entries", json={
            "task_description": "explicit test",
            "classe": "cosmetic",
            "stack": "7B-local-whole",
            "outcome": "success",
            "tokens_sent": 999,
            "cost_usd": 0.999,
            "langfuse_trace_id": "trace-xyz",
        })
    body = r.get_json()
    # Only fields that were zero should have been filled.
    assert sorted(body["langfuse_autofilled"]) == ["latency_ms", "tokens_received"]


def test_autopull_degrades_gracefully_when_langfuse_unreachable(client):
    with patch("langfuse_client.LangfuseClient.get_trace", return_value=None):
        r = client.post("/api/entries", json={
            "task_description": "unreachable test",
            "classe": "cosmetic",
            "stack": "other",
            "outcome": "success",
            "langfuse_trace_id": "trace-xyz",
        })
    assert r.status_code == 201
    assert r.get_json()["langfuse_autofilled"] == []


def test_trace_link_uses_project_scoped_url_when_configured(client_with_project):
    client_with_project.post("/api/entries", json={
        "task_description": "project url test",
        "classe": "cosmetic",
        "stack": "other",
        "outcome": "success",
        "langfuse_trace_id": "trace-xyz",
    })
    body = client_with_project.get("/entries").get_data(as_text=True)
    assert "http://lf.example.com/project/proj-abc/traces/trace-xyz" in body
    # And the fallback /trace/ path must NOT be used when project_id is set.
    assert "lf.example.com/trace/trace-xyz" not in body


def test_stats_page_renders_sparklines_when_entries_exist(client):
    # Seed one entry → daily aggregation has 1 day → sparkline emits a polyline
    client.post("/api/entries", json={
        "task_description": "sparkline seed",
        "classe": "cosmetic",
        "stack": "other",
        "outcome": "success",
        "cost_usd": 0.0042,
    })
    body = client.get("/stats").get_data(as_text=True)
    assert "<svg" in body
    assert "Entries per giorno" in body
    assert "Cost USD per giorno" in body


def test_stats_page_renders_empty_state_with_no_entries(client):
    body = client.get("/stats").get_data(as_text=True)
    assert "Nessuna entry ancora" in body


def test_delete_entry(client):
    r = client.post("/api/entries", json={
        "task_description": "to delete",
        "classe": "cosmetic",
        "stack": "other",
        "outcome": "success",
    })
    entry_id = r.get_json()["id"]

    # Authenticate before deleting
    client.post("/login", data={"password": "test-api-secret"})

    r = client.post(f"/entries/{entry_id}/delete", follow_redirects=True)
    assert r.status_code == 200
    entries = client.get("/api/entries").get_json()
    assert all(e["id"] != entry_id for e in entries)

def test_delete_entry_requires_auth(client):
    r = client.post("/api/entries", json={
        "task_description": "to delete unauth",
        "classe": "cosmetic",
        "stack": "other",
        "outcome": "success",
    })
    entry_id = r.get_json()["id"]

    # Unauthenticated deletion attempt should fail with 401
    r = client.post(f"/entries/{entry_id}/delete", follow_redirects=True)
    assert r.status_code == 401
