"""Governor Fase-2 R1 -- pure digest builder.

build_attention_body(escalated, dropped_count) -> str
    ASCII markdown issue body.  NO timestamp (idempotency).

escalate_key(escalated) -> str
    Stable 16-hex hash over sorted (source, severity) tuples.
    Change-detector for the open-issue idempotency check.
"""
from __future__ import annotations

import hashlib


def escalate_key(escalated: list[dict]) -> str:
    """Return a stable 16-hex hash over the escalated set.

    Keyed on sorted (source, severity) pairs ONLY -- intentionally invariant to
    enriched fields (action, reason, rank) that classify() adds to signal dicts.
    This means run_r1 can safely key over enriched dicts and still produce the
    same key as keying over raw signals with identical (source, severity) pairs.
    No timestamps, no summaries.  Same set -> same key (idempotent).
    Different (source, severity) set -> different key.
    """
    pairs = sorted((d["source"], d["severity"]) for d in escalated)
    h = hashlib.sha256()
    for src, sev in pairs:
        h.update(src.encode("utf-8"))
        h.update(b"\x00")
        h.update(sev.encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()[:16]


def build_attention_body(escalated: list[dict], dropped_count: int) -> str:
    """Build the GitHub issue body for an escalation event.

    Args:
        escalated: list of signal dicts that crossed the escalation threshold.
            Each dict must have keys: source, severity, reason, summary, ref.
        dropped_count: number of signals that were classified "report" (below threshold).

    Returns:
        ASCII-only markdown string.  NO timestamp anywhere (idempotency).
    """
    lines = [
        "## Governor attention -- escalated signals",
        "",
        "| source | severity | reason | summary | ref |",
        "|--------|----------|--------|---------|-----|",
    ]
    # Sort by severity rank descending for readability
    from governor.signals import SEVERITY_RANK
    sorted_signals = sorted(
        escalated,
        key=lambda d: SEVERITY_RANK.get(d.get("severity", "ok"), 0),
        reverse=True,
    )
    for sig in sorted_signals:
        source = sig.get("source", "")
        severity = sig.get("severity", "")
        reason = sig.get("reason", "")
        summary = sig.get("summary", "")
        ref = sig.get("ref", "")
        # Escape pipe chars to avoid breaking markdown table
        def _esc(s: str) -> str:
            return s.replace("|", "&#124;").replace("\n", " ")
        lines.append(f"| {_esc(source)} | {_esc(severity)} | {_esc(reason)} | {_esc(summary)} | {_esc(ref)} |")
    lines.append("")
    lines.append(
        f"{dropped_count} signal(s) below escalation threshold -- see /governor pane"
    )
    return "\n".join(lines)
