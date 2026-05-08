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
