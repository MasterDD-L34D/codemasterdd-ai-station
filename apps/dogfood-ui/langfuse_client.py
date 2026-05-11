"""Minimal Langfuse API client — ping + optional trace-id resolution."""
from __future__ import annotations

import base64
from typing import Any

import requests


class LangfuseClient:
    def __init__(self, host: str, public_key: str, secret_key: str, timeout: float = 3.0) -> None:
        self.host = host.rstrip("/")
        self.public_key = public_key
        self.secret_key = secret_key
        self.timeout = timeout

    def _auth_header(self) -> dict[str, str]:
        """Returns Basic auth header dict for Langfuse API requests, or empty dict if keys are not configured."""
        if not (self.public_key and self.secret_key):
            return {}
        token = base64.b64encode(f"{self.public_key}:{self.secret_key}".encode("utf-8")).decode("ascii")
        return {"Authorization": f"Basic {token}"}

    def ping(self) -> bool:
        """True if Langfuse reachable with valid keys."""
        try:
            r = requests.get(
                f"{self.host}/api/public/health",
                headers=self._auth_header(),
                timeout=self.timeout,
            )
            return r.status_code < 500
        except (requests.ConnectionError, requests.Timeout):
            return False

    def get_trace(self, trace_id: str) -> dict[str, Any] | None:
        """Fetch trace details. Returns None on 404/error."""
        if not (self.public_key and self.secret_key):
            return None
        try:
            r = requests.get(
                f"{self.host}/api/public/traces/{trace_id}",
                headers=self._auth_header(),
                timeout=self.timeout,
            )
            if r.status_code == 200:
                return r.json()
            return None
        except (requests.ConnectionError, requests.Timeout):
            return None

    def fetch_metadata(self, trace_id: str) -> dict[str, Any]:
        """Best-effort extraction of tokens/cost/latency from a Langfuse trace.

        Returns {} when the trace cannot be fetched. Otherwise returns a dict
        with any of: tokens_sent, tokens_received, cost_usd, latency_ms.
        Defensive across Langfuse API shape variants: trace-level fields first,
        then aggregated observations[].
        """
        trace = self.get_trace(trace_id)
        if not trace:
            return {}
        return extract_trace_metadata(trace)


def extract_trace_metadata(trace: dict[str, Any]) -> dict[str, Any]:
    """Pure function: project a Langfuse trace JSON into dogfood-ui fields.

    Tolerates several API shapes (older/newer Langfuse versions):
    - usage: trace.usage.{input,output} OR sum of observations[].usage.{input,output}
    - cost: trace.totalCost OR trace.calculatedTotalCost OR sum of observations[]
    - latency: trace.latencyMs OR trace.latency (seconds -> ms)
    """
    out: dict[str, Any] = {}
    observations = trace.get("observations") or []

    usage = trace.get("usage") or {}
    tokens_in = usage.get("input") or usage.get("promptTokens")
    tokens_out = usage.get("output") or usage.get("completionTokens")
    if tokens_in is None and observations:
        tokens_in = sum(
            (o.get("usage") or {}).get("input") or (o.get("usage") or {}).get("promptTokens") or 0
            for o in observations
        ) or None
    if tokens_out is None and observations:
        tokens_out = sum(
            (o.get("usage") or {}).get("output") or (o.get("usage") or {}).get("completionTokens") or 0
            for o in observations
        ) or None
    if tokens_in:
        out["tokens_sent"] = int(tokens_in)
    if tokens_out:
        out["tokens_received"] = int(tokens_out)

    cost = trace.get("totalCost") or trace.get("calculatedTotalCost")
    if cost is None and observations:
        cost = sum(
            (o.get("calculatedTotalCost") or o.get("totalCost") or 0) for o in observations
        ) or None
    if cost:
        out["cost_usd"] = float(cost)

    latency_ms = trace.get("latencyMs")
    if latency_ms is None:
        latency_s = trace.get("latency")
        if latency_s is not None:
            latency_ms = float(latency_s) * 1000.0
    if latency_ms:
        out["latency_ms"] = int(latency_ms)

    return out
