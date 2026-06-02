"""Governor Fase-2 R1 -- pure signal classifier.

classify(signal, prior_severity) -> {"action", "rank", "reason"}

Escalate iff:
  - signal["severity"] == "error"    (always on fire)
  - OR prior_severity is not None AND SEVERITY_RANK[signal["severity"]] > SEVERITY_RANK[prior_severity]
    (worsened delta vs a known previous state)

First-seen signals (prior_severity=None) are never escalated unless they are errors.
"""
from __future__ import annotations

from governor.signals import SEVERITY_RANK


def classify(signal: dict, prior_severity: str | None) -> dict:
    """Pure classifier.  No I/O.

    Args:
        signal: dict with at least "severity" key (str).
        prior_severity: severity string of the previous stored signal for the same
            source, or None if this is the first signal for the source.

    Returns:
        dict with keys "action" ("escalate" | "report"), "rank" (int), "reason" (str).
    """
    sev = signal["severity"]
    rank = SEVERITY_RANK.get(sev, -1)  # -1 so an unknown severity does not silently rank as "ok" (0)

    if sev == "error":
        return {"action": "escalate", "rank": rank, "reason": "error"}

    if prior_severity is not None:
        prior_rank = SEVERITY_RANK.get(prior_severity, -1)
        if rank > prior_rank:
            return {
                "action": "escalate",
                "rank": rank,
                "reason": f"worsened {prior_severity}->{sev}",
            }

    return {"action": "report", "rank": rank, "reason": "steady or improved"}
