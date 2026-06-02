from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


# Single source of truth for severity ordering (R1 classifier uses this).
SEVERITY_RANK: dict[str, int] = {"error": 3, "warning": 2, "info": 1, "ok": 0}


@dataclass(frozen=True)
class Signal:
    """Normalized cross-island signal record (R0 -- no action attached)."""
    source: str
    kind: str
    severity: str
    summary: str
    counts: dict = field(default_factory=dict)
    produced_at: str | None = None   # ISO timestamp from the artifact, if any
    ref: str = ""          # url / path / issue ref
    payload_hash: str = "" # change-detect / dedup key


def make_hash(*parts: str) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update((p or "").encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()[:16]


def severity_from_counts(errors: int, warnings: int) -> str:
    if errors > 0:
        return "error"
    if warnings > 0:
        return "warning"
    return "ok"
