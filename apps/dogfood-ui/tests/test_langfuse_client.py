"""Unit tests for langfuse_client.

Covers:
  - extract_trace_metadata (trace shapes, observations, legacy keys, empty/zero)
  - health() vs ping() contracts (different endpoints, auth handling)
"""
from __future__ import annotations

from unittest.mock import patch

import requests
from langfuse_client import LangfuseClient, extract_trace_metadata


def test_trace_level_fields():
    m = extract_trace_metadata({
        "usage": {"input": 100, "output": 200},
        "totalCost": 0.0042,
        "latencyMs": 1234,
    })
    assert m == {
        "tokens_sent": 100,
        "tokens_received": 200,
        "cost_usd": 0.0042,
        "latency_ms": 1234,
    }


def test_aggregates_from_observations_and_converts_seconds_to_ms():
    m = extract_trace_metadata({
        "observations": [
            {"usage": {"input": 50, "output": 30}, "calculatedTotalCost": 0.001},
            {"usage": {"input": 20, "output": 70}, "calculatedTotalCost": 0.002},
        ],
        "latency": 2.5,  # seconds
    })
    assert m == {
        "tokens_sent": 70,
        "tokens_received": 100,
        "cost_usd": 0.003,
        "latency_ms": 2500,
    }


def test_legacy_prompt_completion_token_names():
    m = extract_trace_metadata({
        "usage": {"promptTokens": 11, "completionTokens": 22},
    })
    assert m["tokens_sent"] == 11
    assert m["tokens_received"] == 22


def test_empty_trace_returns_empty_dict():
    assert extract_trace_metadata({}) == {}


def test_zero_values_are_skipped():
    # Zero tokens/cost/latency shouldn't surface as filled fields
    # (no point auto-filling a zero on top of a zero default).
    m = extract_trace_metadata({
        "usage": {"input": 0, "output": 0},
        "totalCost": 0,
        "latencyMs": 0,
    })
    assert m == {}


class TestLangfuseClientHealthPing:
    """Verify health() vs ping() have different contracts.

    - health(): no auth required, calls /api/public/health
    - ping():   requires auth keys, calls /api/public/traces
    """

    def test_health_calls_public_endpoint_without_auth(self):
        client = LangfuseClient(
            host="http://lf.example.com",
            public_key="pk-test", secret_key="sk-test",
        )
        with patch.object(client, "_auth_header", return_value={"Authorization": "Basic dGVzdA=="}) as mock_auth:
            with patch("langfuse_client.requests.get") as mock_get:
                mock_get.return_value.status_code = 200
                result = client.health()
                assert result is True
                mock_get.assert_called_once_with(
                    "http://lf.example.com/api/public/health",
                    timeout=3.0,
                )
                mock_auth.assert_not_called()

    def test_health_returns_false_on_connection_error(self):
        client = LangfuseClient(
            host="http://lf.example.com",
            public_key="", secret_key="",
        )
        with patch("langfuse_client.requests.get", side_effect=requests.exceptions.ConnectionError):
            assert client.health() is False

    def test_ping_calls_traces_endpoint_with_auth(self):
        client = LangfuseClient(
            host="http://lf.example.com",
            public_key="pk-test", secret_key="sk-test",
        )
        with patch("langfuse_client.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            result = client.ping()
            assert result is True
            mock_get.assert_called_once_with(
                "http://lf.example.com/api/public/traces?limit=1",
                headers={"Authorization": "Basic cGstdGVzdDpzay10ZXN0"},
                timeout=3.0,
            )

    def test_ping_returns_false_when_keys_missing(self):
        client = LangfuseClient(
            host="http://lf.example.com",
            public_key="", secret_key="",
        )
        with patch("langfuse_client.requests.get") as mock_get:
            result = client.ping()
            assert result is False
            mock_get.assert_not_called()

    def test_ping_returns_false_on_401(self):
        client = LangfuseClient(
            host="http://lf.example.com",
            public_key="pk-bad", secret_key="sk-bad",
        )
        with patch("langfuse_client.requests.get") as mock_get:
            mock_get.return_value.status_code = 401
            assert client.ping() is False
