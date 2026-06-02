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


_RE_VAULT_DATE_TITLE = re.compile(r"^#\s+.*?(20\d{2}-\d{2}-\d{2})", re.MULTILINE)
_RE_VAULT_DATE_ANY = re.compile(r"(20\d{2}-\d{2}-\d{2})")
_RE_VAULT_BOLD_NUM = re.compile(r"\*\*(\d+)\*\*")
_RE_VAULT_SUMMARY = re.compile(r"^##\s+Summary\b(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
_RE_VAULT_BLOCK = re.compile(r"\bBLOCK:\s*(\d+)")
_RE_VAULT_WARN = re.compile(r"\bWARN:\s*(\d+)")


def parse_vault_report(md: str, source: str, kind: str, ref: str) -> Signal:
    """Generic vault lint-report parser (gap-scan, coherence, whatsmissing).

    R0 surface (presence + coarse severity; detail lives at `ref`):
    - date: anchored to the report's `# heading` line (a stray ISO date in body
      prose must not win and churn the change-hash every run).
    - severity: error ONLY if the structured verdict `BLOCK: N` has N>0 (NOT the
      bare word "BLOCK", which appears in policy prose -> false alarms); else
      warning if the `## Summary` section has any nonzero metric; else ok.
    - findings/metrics are restricted to the `## Summary` section (excludes corpus
      sizes like "Scanned **2249** md"). The summary STRING reports the count of
      nonzero metrics, NOT a conflated sum (a graph-density census is not an
      actionable finding total).
    """
    text = md or ""
    m_title = _RE_VAULT_DATE_TITLE.search(text)
    if m_title:
        produced_at = m_title.group(1)
    else:
        m_any = _RE_VAULT_DATE_ANY.search(text)
        produced_at = m_any.group(1) if m_any else None
    m_sum = _RE_VAULT_SUMMARY.search(text)
    nums = [int(n) for n in _RE_VAULT_BOLD_NUM.findall(m_sum.group(1) if m_sum else "")]
    findings = sum(nums)
    nonzero = sum(1 for n in nums if n > 0)
    m_block = _RE_VAULT_BLOCK.search(text)
    block_n = int(m_block.group(1)) if m_block else 0
    m_warn = _RE_VAULT_WARN.search(text)
    warn_n = int(m_warn.group(1)) if m_warn else 0
    if block_n > 0:
        severity = "error"
    elif nonzero > 0 or warn_n > 0:
        severity = "warning"
    else:
        severity = "ok"
    date_s = produced_at or "(undated)"
    if nums:
        summary_text = f"{kind} report {date_s}: {nonzero}/{len(nums)} summary metrics nonzero"
    elif block_n > 0 or warn_n > 0:
        summary_text = f"{kind} report {date_s}: BLOCK {block_n} WARN {warn_n}"
    else:
        summary_text = f"{kind} report present {date_s}"
    return Signal(
        source=source,
        kind=kind,
        severity=severity,
        summary=summary_text,
        counts={"findings": findings, "metrics": len(nums), "nonzero": nonzero, "block": block_n, "warn": warn_n},
        produced_at=produced_at,
        ref=ref,
        payload_hash=make_hash(source, str(produced_at), str(findings), str(block_n), str(warn_n)),
    )


def parse_sot_drift_issues(issues: list, ref: str) -> Signal:
    items = issues or []
    open_count = len(items)
    updated = [i.get("updatedAt") or i.get("updated_at") or "" for i in items]
    produced_at = max(updated) if updated and any(updated) else None
    severity = "warning" if open_count > 0 else "ok"
    summary_text = f"{open_count} open SoT drift candidate(s)"
    return Signal(
        source="game-sot-drift",
        kind="sot-drift",
        severity=severity,
        summary=summary_text,
        counts={"open": open_count},
        produced_at=produced_at,
        ref=ref,
        payload_hash=make_hash("sot-drift", str(open_count), str(produced_at)),
    )
