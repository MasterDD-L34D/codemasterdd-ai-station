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
