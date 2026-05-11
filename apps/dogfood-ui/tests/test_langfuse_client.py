"""Unit tests for langfuse_client.extract_trace_metadata.

Covers the two main shapes the helper must tolerate:
  - trace-level usage/cost/latency fields
  - usage/cost aggregated from observations[]
  - latency in seconds vs milliseconds
"""
from __future__ import annotations

from langfuse_client import extract_trace_metadata


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
