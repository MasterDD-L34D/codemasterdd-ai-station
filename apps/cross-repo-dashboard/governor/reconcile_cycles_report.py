"""EXTERNAL, READ-ONLY clean-cycle audit for the R1 reconcile rung (spec sec 7.1).

Anti-self-licking (actor-activation-criteria sec 4): this is ADVISORY ONLY -- it is NEVER a gate
input and the reconcile actor must NEVER import it. A clean R1 cycle (actor-criteria sec 6) =
a reconcile PR (a) MERGED BY A HUMAN, (b) not reverted within 7 days, (c) no same-line follow-up
fix within 7 days. The COUNT is computed here, OUTSIDE the actor, from git/gh facts; the actor's
own output can never license its own promotion.

Honest scope (spec sec 7.1): N clean cycles prove renderer DETERMINISM + REVERT-SAFETY, NOT
merge-JUDGMENT-safety. The R2 ADR must weigh that and justify auto-merge on reversibility +
class-restriction + the mechanical drop-check + a CI-watchlist -- the cycles are a NECESSARY
field-signal, never a SUFFICIENT one. This module writes NOTHING.
"""
from __future__ import annotations


def is_clean_cycle(pr: dict) -> bool:
    """Pure mechanical predicate over git/gh facts. The 7-day windows are pre-computed by the
    caller from history at R2-decision time (no clock here -> deterministic + unit-testable)."""
    return bool(
        pr.get("merged")
        and pr.get("merged_by_human")
        and not pr.get("reverted_within_7d")
        and not pr.get("same_line_followup_within_7d")
    )


def summarize(prs: list) -> dict:
    """Read-only advisory rollup. Writes nothing; NEVER a gate input (anti-self-licking)."""
    clean = [p for p in (prs or []) if is_clean_cycle(p)]
    return {
        "total": len(prs or []),
        "clean_cycles": len(clean),
        "clean_ids": [p.get("id") for p in clean],
        "advisory": True,   # marker: NEVER a gate input
    }
