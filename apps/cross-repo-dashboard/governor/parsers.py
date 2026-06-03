from __future__ import annotations

import re
from datetime import date

from governor.signals import Signal, make_hash, severity_from_counts

# eng-graph staleness thresholds (days since last_verified). Monthly-ish MOC
# cadence -> warn past a month, error past a quarter. Tunable module constants.
STALE_WARN_DAYS = 30
STALE_ERROR_DAYS = 90


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


_RE_DATE = re.compile(r"Digest.*?(\d{4}-\d{2}-\d{2})")
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



_RE_ENG_GRAPH_LAST_VERIFIED = re.compile(r'^last_verified:\s*(\d{4}-\d{2}-\d{2})', re.MULTILINE)
_RE_ENG_GRAPH_CREATED = re.compile(r'^created:\s*(\d{4}-\d{2}-\d{2})', re.MULTILINE)
_RE_ENG_GRAPH_AUTO_REGION = re.compile(
    r'<!--\s*eng-graph:auto\s*-->(.*?)<!--\s*/eng-graph:auto\s*-->',
    re.DOTALL,
)
_RE_ENG_GRAPH_REPO = re.compile(r'repo\s+`([^`]+)`')


def parse_eng_graph_moc(md: str, ref: str, now: date | None = None) -> Signal:
    """eng-graph MOC signal with staleness-aware severity.

    `now` (a date) enables staleness: info if fresh, warning past STALE_WARN_DAYS,
    error past STALE_ERROR_DAYS vs the MOC's last_verified (or created fallback).
    now=None (clock-free callers/tests) -> severity stays info (staleness opt-in).
    Severity is folded into payload_hash so an info->warning transition is a DISTINCT
    row that the worsened-delta classifier (R1) escalates.

    CAVEAT -- first-seen-stale (harsh-reviewer P1, by design): a warning-stale MOC is
    escalated only by a worsened delta (info->warning), NOT first-seen. So on a fresh
    governor.db where the MOC is ALREADY 30-90d stale, it stays `report` (silent) until
    it crosses error/90d. This inherits the classifier's first-seen suppression (uniform
    with the noisy lint sources) rather than special-casing eng-graph in the pure
    classifier. An error-stale (>90d) MOC DOES escalate first-seen (severity == error).
    """
    text = md or ''
    m_lv = _RE_ENG_GRAPH_LAST_VERIFIED.search(text)
    m_cr = _RE_ENG_GRAPH_CREATED.search(text)
    if m_lv:
        produced_at, date_label = m_lv.group(1), 'last_verified'
    elif m_cr:
        produced_at, date_label = m_cr.group(1), 'created'
    else:
        produced_at, date_label = None, 'last_verified'
    m_region = _RE_ENG_GRAPH_AUTO_REGION.search(text)
    repo_count = len(_RE_ENG_GRAPH_REPO.findall(m_region.group(1))) if m_region else 0
    severity = 'info'
    if now is not None and produced_at:
        try:
            age_days = (now - date.fromisoformat(produced_at)).days
            # `>` not `>=` on purpose: exactly STALE_*_DAYS stays in the lower band
            # ("more than a month/quarter" stale -- 30d-exactly is still fresh).
            if age_days > STALE_ERROR_DAYS:
                severity = 'error'
            elif age_days > STALE_WARN_DAYS:
                severity = 'warning'
        except (ValueError, TypeError):
            # malformed produced_at, or a non-date `now` (e.g. a datetime) -> degrade
            # to info rather than erroring the whole source out in _produce.
            pass
    date_s = produced_at or '(undated)'
    summary_text = f'eng-graph MOC: {repo_count} repos indexed, {date_label} {date_s}'
    return Signal(
        source='vault-eng-graph',
        kind='eng-graph',
        severity=severity,
        summary=summary_text,
        counts={'repos': repo_count},
        produced_at=produced_at,
        ref=ref,
        payload_hash=make_hash('eng-graph', str(produced_at), str(repo_count), severity),
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


_RE_ARCHON_LESSON = re.compile(r'^(L-\d{4}-\d{2}-\d{3})')


def parse_archon_learnings(entries: list, ref: str) -> Signal:
    """ARCHON learnings count signal (vault-vendored aa01 lessons).

    `entries` is a contents-API dir listing; count the L-YYYY-MM-NNN-*.md lessons
    and name the latest (max by lesson id). INFO-severity by design: a lesson count
    is observability, never "on fire", and info never escalates (not error; a steady
    info->info is no worsened-delta). So this 8th source is pure R0 -- no autonomy change.
    """
    names = [str(e.get('name', '')) for e in (entries or [])]
    ids = sorted(
        m.group(1)
        for m in (_RE_ARCHON_LESSON.match(n) for n in names if n.endswith('.md'))
        if m
    )
    count = len(ids)
    latest = ids[-1] if ids else None
    # L-YYYY-MM-NNN carries no day, so produced_at is the YYYY-MM month of the latest.
    produced_at = latest[2:9] if latest else None
    summary_text = f'{count} ARCHON lessons, latest {latest}' if latest else '0 ARCHON lessons'
    return Signal(
        source='archon-learnings',
        kind='learnings',
        severity='info',
        summary=summary_text,
        counts={'lessons': count},
        produced_at=produced_at,
        ref=ref,
        payload_hash=make_hash('archon-learnings', str(count), str(latest)),
    )


_RE_JULES_DATE = re.compile(r"#\s*Jules daily digest\s+(\d{4}-\d{2}-\d{2})")
_RE_JULES_AWAITING = re.compile(r"Awaiting sessions:\s*(\d+)", re.IGNORECASE)
_RE_JULES_VERDICT = re.compile(r"\*\*(ARCHIVE|ACTIONABLE|DEFER|IN-PROGRESS|AMBIGUOUS)\b")


def parse_jules_digest(md: str, ref: str) -> Signal:
    """Jules daily-digest signal (the READ-ONLY enumerator output, G3 cron).

    Maps the digest's per-session verdicts to an R0 OBSERVE signal so the governor
    surfaces Jules cycles needing attention. **ACTIONABLE** (PR closed-unmerged/open or
    Jules-asking = NOT shipped) is the ONLY verdict that escalates to `warning`;
    AMBIGUOUS / DEFER / IN-PROGRESS are `info` (the digest is conservative-AMBIGUOUS, so
    escalating those would be noise); ARCHIVE-only / 0-awaiting are `ok`. A digest that
    self-reports an API-fetch failure (the script's `Sessions API fetch FAILED` marker)
    is `error`. Severity is folded into payload_hash so an ok/info -> warning transition
    is a DISTINCT row the R1 worsened-delta classifier escalates.

    NOT a self-licking loop (actor-criteria sec 4): it feeds NO unlock METRIC -- acted-on is
    HUMAN-gated (sec 5; the actor never calls record_acted_on) and issue escalations are not
    clean-PR-cycles (sec 6). The loop is severed AT THE METRIC, not at the input. (Provenance
    is the weaker secondary reason: the digest is an external cron + Claude advisory triage,
    not the governor actor's own output.)
    """
    text = md or ""
    m_date = _RE_JULES_DATE.search(text)
    produced_at = m_date.group(1) if m_date else None
    m_await = _RE_JULES_AWAITING.search(text)
    awaiting = int(m_await.group(1)) if m_await else 0
    verdicts = _RE_JULES_VERDICT.findall(text)
    counts = {
        "awaiting": awaiting,
        "actionable": verdicts.count("ACTIONABLE"),
        "defer": verdicts.count("DEFER"),
        "ambiguous": verdicts.count("AMBIGUOUS"),
        "archive": verdicts.count("ARCHIVE"),
        "in_progress": verdicts.count("IN-PROGRESS"),
    }
    date_s = produced_at or "(undated)"
    if "Sessions API fetch FAILED" in text:
        severity = "error"
        summary_text = f"jules digest {date_s}: API fetch FAILED (re-run -- NOT empty-set)"
    elif counts["actionable"] > 0:
        severity = "warning"
        summary_text = f"jules digest {date_s}: {counts['actionable']} actionable / {awaiting} awaiting"
    elif awaiting > 0:
        severity = "info"
        summary_text = f"jules digest {date_s}: {awaiting} awaiting (0 actionable)"
    else:
        severity = "ok"
        summary_text = f"jules digest {date_s}: 0 awaiting"
    return Signal(
        source="jules-digest",
        kind="jules-digest",
        severity=severity,
        summary=summary_text,
        counts=counts,
        produced_at=produced_at,
        ref=ref,
        payload_hash=make_hash(
            "jules-digest", str(produced_at), str(awaiting), str(counts["actionable"]), severity
        ),
    )
