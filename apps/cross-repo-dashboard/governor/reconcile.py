"""Governor R1 open-PR reconcile rung -- deterministic, clock-free doc-reconcile actors.

The rung OPENS branch+PRs (never merges) for docs whose GOVERNOR-SYNC marker region drifted
from a pure function of the governor's signal store. It does NOT touch the issue actor
(act.py:run_r1). Authority: spec docs/superpowers/specs/2026-06-03-governor-r1-open-pr-rung-design.md
(v4, merged #292); ADR-0037 dec.4; ADR-0038 (doctrine carve-out); ADR-0011 (commit trailers);
ADR-0021 (ASCII). The spec wins on any conflict.

HARD invariants: NO auto-merge (R2, future ADR); NO LLM in the diff path; NO time-derived /
clock-tick render; doctrine files are NEVER targeted (fail-closed); the write actor is
fail-closed on GOVERNOR_RECONCILE_TOKEN (no ambient fallback for writes); clean-cycle accounting
is EXTERNAL (reconcile_cycles_report.py), never in the actor.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

_DOCTRINE_NAMES = frozenset({
    "CLAUDE.md", "AGENTS.md", "ORCHESTRATION.md",
    "GOALS.md", "DECISIONS_LOG.md", "OPEN_DECISIONS.md",
})
_DOCTRINE_DIR_PREFIXES = (
    "docs/adr/",
    "docs/cross-repo/",
    "Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/",
)
_DOCTRINE_BASENAMES_EXACT = frozenset({"aider-privacy-whitelist.txt"})


def _normalize_path(path: "str | None") -> str:
    p = (path or "").replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    if p.startswith("~/"):
        p = p[2:]
    return p.lstrip("/")


def is_doctrine(path: "str | None", repo: str) -> bool:
    """STATIC path-classifier for the ADR-0038 doctrine carve-out (fail-closed).

    True for ANY of the static carve-out set: dir globs (docs/adr/**, docs/cross-repo/**,
    Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/**), any `.claude/` segment (repo .claude/**
    AND the global ~/.claude/ governance subpaths -- home machine-junk is conservatively
    OVER-classified, which is FAIL-SAFE for a write-gate: refusing to auto-edit it is harmless,
    a doctrine path must never escape), named root rule files (CLAUDE.md/AGENTS.md/
    ORCHESTRATION.md/GOALS.md/DECISIONS_LOG.md/OPEN_DECISIONS.md, any level), and
    ~/.config/aider-privacy-whitelist.txt.

    NOT here (BY DESIGN): the ADR-0038 *content-based* catch-all -- a pure path-classifier
    cannot evaluate "does this file's content define rules". That clause is a HUMAN process
    checkpoint (spec sec 4.2): adding ANY new reconciler REQUIRES an explicit Eduardo
    doctrine-classification review of its target. This function enforces only the static set.

    `repo` is part of the stable interface (the carve-out is repo-agnostic in ADR-0038;
    `repo` is accepted for forward-compat with a future repo-specific carve-out). It does
    not change the verdict today.
    """
    p = _normalize_path(path)
    if not p:
        return True  # fail-closed: empty/None path -> treat as doctrine (refuse)
    for pref in _DOCTRINE_DIR_PREFIXES:
        if p == pref.rstrip("/") or p.startswith(pref):
            return True
    segments = p.split("/")
    if ".claude" in segments:
        return True
    base = segments[-1]
    if base in _DOCTRINE_NAMES or base in _DOCTRINE_BASENAMES_EXACT:
        return True
    return False


@dataclass(frozen=True)
class Reconciler:
    """A deterministic, clock-free doc-reconciler (spec sec 3.1 / 4).

    render(store) -> the INNER marker-region body (a table), or None = "cannot compute" (the
    actor skips it, never a junk PR). render MUST be pure: reads signals from the store, no
    network, no write, NO wall-clock (spec sec 6.3).
    """
    id: str
    repo: str
    path: str
    marker: Tuple[str, str]                       # (begin, end) GOVERNOR-SYNC region
    render: Callable[[object], Optional[str]]     # store -> inner region body, or None
    anchor: Optional[str] = None                  # heading to inject after (existing doc)
    create_header: Optional[str] = None           # frontmatter+heading for a NEW doc

    def __post_init__(self):
        # Fail-closed doctrine guard AT CONSTRUCTION (spec sec 3.1 / 4.2): a reconciler
        # aimed at a doctrine path refuses to exist -- a config error fails fast, never
        # silently opens a doctrine PR.
        if is_doctrine(self.path, self.repo):
            raise ValueError(
                f"Reconciler {self.id!r} targets a doctrine path {self.path!r} "
                f"(ADR-0038 carve-out) -- refusing to construct"
            )


def splice(doc_text, marker, new_region, anchor=None, create_header=None) -> str:
    """Pure, idempotent region-replace bounded by (begin, end) markers.

    - markers present          -> replace the BEGIN..END region in place (re.DOTALL, count=1).
    - target absent/empty       -> CREATE: `create_header` (frontmatter+heading) + the block.
    - markers absent + anchor    -> first-time injection AFTER the anchor line.
    - markers absent, no anchor   -> append the block at end (defensive; never drops prose).

    `new_region` is the INNER body (a table); splice wraps it with the markers. splice adds NO
    timestamp (idempotency: identical new_region -> identical output, spec sec 6.4). A function
    replacement is used in re.sub so backslashes in `new_region` are literal (no backref bug).
    """
    begin, end = marker
    block = f"{begin}\n{new_region}\n{end}"
    text = doc_text or ""

    if begin in text and end in text:
        pattern = re.escape(begin) + r".*?" + re.escape(end)
        return re.sub(pattern, lambda _m: block, text, count=1, flags=re.DOTALL)

    if not text.strip():
        header = (create_header or "").rstrip()
        return (header + "\n\n" + block + "\n") if header else (block + "\n")

    if anchor and anchor in text:
        out = []
        injected = False
        for ln in text.split("\n"):
            out.append(ln)
            if not injected and anchor in ln:
                out.append("")
                out.append(block)
                injected = True
        return "\n".join(out)

    return text.rstrip("\n") + "\n\n" + block + "\n"


# ---------------------------------------------------------------------------
# Render legs -- pure, deterministic, CLOCK-FREE (spec sec 5 / 6.3).
# ---------------------------------------------------------------------------

_STATUS_COLS = ("source", "severity", "summary", "produced_at", "ref")


def _md_cell(value) -> str:
    """Single-line markdown table cell (escape pipes/newlines). Pure."""
    s = "" if value is None else str(value)
    return s.replace("|", "\\|").replace("\n", " ").strip()


def _md_table(columns, rows_cells) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(cells) + " |" for cells in rows_cells]
    return "\n".join([header, sep] + body)


def render_status_multi_repo(store):
    """Deterministic, CLOCK-FREE governor signal snapshot from store.latest_per_source().

    Columns source|severity|summary|produced_at|ref, ordered by source (the store returns rows
    ORDER BY source). NO wall-clock / no time-derived value -- the change-key is signal STATE
    only (spec sec 5.1 / 6.3). produced_at is the artifact's own timestamp (from the signal),
    never the current time. Returns None when the store holds no signals (cannot compute).
    """
    rows = store.latest_per_source()
    if not rows:
        return None
    cells = [[_md_cell(r.get(c)) for c in _STATUS_COLS] for r in rows]
    table = _md_table(_STATUS_COLS, cells)
    note = ("\n\n_Auto-synced governor signal snapshot; human prose elsewhere is "
            "authoritative._")
    return table + note


_VAULT_LINT_SOURCES = ("vault-gap", "vault-coherence", "vault-whatsmissing")
_VAULT_LINT_COLS = ("report", "severity", "summary", "produced_at", "ref")


def render_vault_lint_status(store):
    """Deterministic, CLOCK-FREE vault lint dashboard from the three vault lint signals.

    Filters store.latest_per_source() to vault-gap / vault-coherence / vault-whatsmissing,
    iterated in fixed order (deterministic regardless of dict ordering). Columns
    report|severity|summary|produced_at|ref. Severity is CONTENT-based: parse_vault_report
    (parsers.py) derives it from BLOCK/WARN/nonzero metrics with NO `now` parameter (spec sec
    5.2), so the rendered state changes only when vault lint CONTENT changes, never on a
    clock-tick. Returns None when none of the three lint sources is present (cannot compute).
    """
    by_source = {r["source"]: r for r in store.latest_per_source()}
    if not any(s in by_source for s in _VAULT_LINT_SOURCES):
        return None
    cells = []
    for s in _VAULT_LINT_SOURCES:
        r = by_source.get(s)
        if r is None:
            continue
        report = s[len("vault-"):]   # gap / coherence / whatsmissing
        cells.append([
            _md_cell(report), _md_cell(r.get("severity")), _md_cell(r.get("summary")),
            _md_cell(r.get("produced_at")), _md_cell(r.get("ref")),
        ])
    table = _md_table(_VAULT_LINT_COLS, cells)
    note = ("\n\n_Auto-synced vault lint status (gap / coherence / whatsmissing); "
            "content-based severity, clock-free. Human prose elsewhere is authoritative._")
    return table + note
