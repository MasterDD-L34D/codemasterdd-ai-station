from __future__ import annotations

import re

from governor.signals import Signal, make_hash, severity_from_counts


def parse_game_governance_drift(raw: dict) -> Signal:
    summary = (raw or {}).get("summary") or {}
    total = int(summary.get("total", 0) or 0)
    errors = int(summary.get("errors", 0) or 0)
    warnings = int(summary.get("warnings", 0) or 0)
    produced_at = (raw or {}).get("generated_at")
    severity = severity_from_counts(errors, warnings)
    summary_text = f"{errors} errors, {warnings} warnings ({total} total)"
    return Signal(
        source="game-governance-drift",
        kind="drift",
        severity=severity,
        summary=summary_text,
        counts={"total": total, "errors": errors, "warnings": warnings},
        produced_at=produced_at,
        ref="https://raw.githubusercontent.com/MasterDD-L34D/Game/main/reports/docs/governance_drift_report.json",
        payload_hash=make_hash(str(produced_at), str(total), str(errors), str(warnings)),
    )


_RE_DATE = re.compile(r"Digest\s*--\s*(\d{4}-\d{2}-\d{2})")
_RE_CYCLES = re.compile(r"Cicli inclusi\**:\s*(\d+)", re.IGNORECASE)
_RE_GAPS = re.compile(r"Coverage gap\s*\((\d+)\s+entry\)", re.IGNORECASE)


def _first_int(rx, text: str) -> int:
    m = rx.search(text or "")
    return int(m.group(1)) if m else 0


def parse_evo_swarm_digest(md: str, ref: str) -> Signal:
    m_date = _RE_DATE.search(md or "")
    produced_at = m_date.group(1) if m_date else None
    cycles = _first_int(_RE_CYCLES, md)
    gaps = _first_int(_RE_GAPS, md)
    severity = "info" if (cycles or gaps) else "ok"
    summary_text = f"{cycles} cycles, {gaps} coverage gaps"
    return Signal(
        source="evo-swarm-digest",
        kind="digest",
        severity=severity,
        summary=summary_text,
        counts={"cycles": cycles, "coverage_gaps": gaps},
        produced_at=produced_at,
        ref=ref,
        payload_hash=make_hash(str(produced_at), str(cycles), str(gaps)),
    )
