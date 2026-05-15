"""Aggregation helpers per dogfood stats + promptfoo bench parsing."""
from __future__ import annotations

import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _compute_class_breakdown(entries: list[sqlite3.Row], classes: Counter[str]) -> dict[str, dict[str, Any]]:
    class_breakdown: dict[str, dict[str, Any]] = {}
    for cls in classes:
        subset = [e for e in entries if e["classe"] == cls]
        n = len(subset)
        s = sum(1 for e in subset if e["outcome"] == "success")
        p = sum(1 for e in subset if e["outcome"] == "partial")
        r = sum(1 for e in subset if e["outcome"] == "reject")
        class_breakdown[cls] = {
            "n": n,
            "full_success": s,
            "partial": p,
            "reject": r,
            "success_rate": s / n if n else 0.0,
        }
    return class_breakdown


def _compute_stack_breakdown(entries: list[sqlite3.Row], stacks: Counter[str]) -> dict[str, dict[str, Any]]:
    stack_breakdown: dict[str, dict[str, Any]] = {}
    for stk in stacks:
        subset = [e for e in entries if e["stack"] == stk]
        n = len(subset)
        s = sum(1 for e in subset if e["outcome"] == "success")
        stack_breakdown[stk] = {
            "n": n,
            "full_success": s,
            "success_rate": s / n if n else 0.0,
        }
    return stack_breakdown


def _compute_phase6_status(total: int, fail_rate_strict: float, total_cost: float) -> dict[str, Any]:
    target_n = 20
    target_fail_rate_max = 0.30
    cost_budget_monthly = 20.0

    return {
        "target_n": target_n,
        "progress_pct": round((total / target_n) * 100, 1),
        "fail_rate_limit": target_fail_rate_max,
        # ADR-0014 criterio 2: "fail rate <30%" → threshold strict (30% esatto = FAIL)
        "fail_rate_status": "PASS" if fail_rate_strict < target_fail_rate_max else "FAIL",
        "cost_budget_monthly": cost_budget_monthly,
        # Budget $20/mo è hard cap (esatto 20 = FAIL)
        "cost_status": "PASS" if total_cost < cost_budget_monthly else "FAIL",
    }


def aggregate_stats(entries: list[sqlite3.Row]) -> dict[str, Any]:
    """Compute Fase 6 metrics: success rate, fail rate, breakdown per class/stack."""
    total = len(entries)
    if total == 0:
        return empty_stats()

    outcomes = Counter(e["outcome"] for e in entries)
    classes = Counter(e["classe"] for e in entries)
    stacks = Counter(e["stack"] for e in entries)

    full_success = outcomes.get("success", 0)
    partial = outcomes.get("partial", 0)
    reject = outcomes.get("reject", 0)
    errors = outcomes.get("error", 0)

    fail_rate_strict = reject / total if total else 0.0
    fail_rate_broad = (partial + reject + errors) / total if total else 0.0

    class_breakdown = _compute_class_breakdown(entries, classes)
    stack_breakdown = _compute_stack_breakdown(entries, stacks)

    # Cost cumulative
    total_cost = sum(float(e["cost_usd"] or 0) for e in entries)
    total_tokens_sent = sum(int(e["tokens_sent"] or 0) for e in entries)
    total_tokens_recv = sum(int(e["tokens_received"] or 0) for e in entries)

    return {
        "total": total,
        "outcomes": dict(outcomes),
        "classes": dict(classes),
        "stacks": dict(stacks),
        "full_success": full_success,
        "partial": partial,
        "reject": reject,
        "fail_rate_strict": round(fail_rate_strict, 4),
        "fail_rate_broad": round(fail_rate_broad, 4),
        "class_breakdown": class_breakdown,
        "stack_breakdown": stack_breakdown,
        "total_cost_usd": round(total_cost, 4),
        "total_tokens_sent": total_tokens_sent,
        "total_tokens_received": total_tokens_recv,
        "phase6": _compute_phase6_status(total, fail_rate_strict, total_cost),
    }


def empty_stats() -> dict[str, Any]:
    """Return empty stats dict matching aggregate_stats() schema for no-entries case."""
    return {
        "total": 0,
        "outcomes": {},
        "classes": {},
        "stacks": {},
        "full_success": 0,
        "partial": 0,
        "reject": 0,
        "fail_rate_strict": 0.0,
        "fail_rate_broad": 0.0,
        "class_breakdown": {},
        "stack_breakdown": {},
        "total_cost_usd": 0.0,
        "total_tokens_sent": 0,
        "total_tokens_received": 0,
        "phase6": {
            "target_n": 20,
            "progress_pct": 0.0,
            "fail_rate_limit": 0.30,
            "fail_rate_status": "PASS",
            "cost_budget_monthly": 20.0,
            "cost_status": "PASS",
        },
    }


def aggregate_by_day(entries: list[sqlite3.Row]) -> list[dict[str, Any]]:
    """Group entries by UTC day -> [{'date': 'YYYY-MM-DD', 'count': int, 'cost_usd': float}, ...]

    Sorted ascending by date. Missing days within the [min, max] range are NOT
    backfilled — the consumer (e.g. sparkline) can interpolate / step.
    """
    if not entries:
        return []
    daily: dict[str, dict[str, float]] = {}
    for e in entries:
        created = (e["created_at"] or "")[:10]  # 'YYYY-MM-DD' prefix from ISO
        if not created:
            continue
        bucket = daily.setdefault(created, {"count": 0, "cost_usd": 0.0})
        bucket["count"] += 1
        bucket["cost_usd"] += float(e["cost_usd"] or 0)
    return [
        {"date": d, "count": int(v["count"]), "cost_usd": round(v["cost_usd"], 4)}
        for d, v in sorted(daily.items())
    ]


def build_sparkline_svg(
    points: list[float],
    *,
    width: int = 480,
    height: int = 120,
    pad: int = 8,
    stroke: str = "#3b82f6",
    fill: str = "#3b82f650",
    label: str = "",
) -> str:
    """Render a minimal polyline + area sparkline as inline SVG.

    No JS, no external CSS. Returns an empty <svg> placeholder when points is
    empty or has a single value (no meaningful trend).
    """
    if not points:
        return (
            f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'role="img" aria-label="{label or "empty chart"}">'
            f'<text x="{width // 2}" y="{height // 2}" text-anchor="middle" '
            f'fill="#9ca3af" font-size="13">no data</text></svg>'
        )

    pmin, pmax = min(points), max(points)
    span = (pmax - pmin) or 1.0
    n = len(points)
    inner_w = width - 2 * pad
    inner_h = height - 2 * pad

    def x(i: int) -> float:
        return pad + (inner_w * i / max(n - 1, 1))

    def y(v: float) -> float:
        return pad + inner_h - (inner_h * (v - pmin) / span)

    coords = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(points))
    # Area fill: close the polyline down to the baseline
    area = f"{pad:.1f},{pad + inner_h:.1f} {coords} {pad + inner_w:.1f},{pad + inner_h:.1f}"

    aria = label or "trend"
    return (
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="{aria}">'
        f'<polygon points="{area}" fill="{fill}" stroke="none"/>'
        f'<polyline points="{coords}" fill="none" stroke="{stroke}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<text x="{pad}" y="{pad + 4}" font-size="11" fill="#6b7280">max {pmax:g}</text>'
        f'<text x="{pad}" y="{height - pad // 2}" font-size="11" fill="#6b7280">min {pmin:g}</text>'
        f'</svg>'
    )


def parse_promptfoo_results(path: Path) -> dict[str, Any]:
    """Parse promptfoo JSON output into dashboard-friendly structure."""
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    results = data.get("results", {})
    table = results.get("table", {})
    stats: defaultdict[str, dict[str, int]] = defaultdict(lambda: {"pass": 0, "fail": 0, "total": 0})

    # promptfoo structure: results.table.body[].outputs[] per provider
    for row in table.get("body", []):
        outputs = row.get("outputs", [])
        for i, output in enumerate(outputs):
            providers = table.get("head", {}).get("prompts", [])
            provider_label = providers[i].get("label", f"provider_{i}") if i < len(providers) else f"provider_{i}"
            stats[provider_label]["total"] += 1
            if output.get("pass"):
                stats[provider_label]["pass"] += 1
            else:
                stats[provider_label]["fail"] += 1

    provider_stats = []
    for provider, s in stats.items():
        rate = s["pass"] / s["total"] if s["total"] else 0.0
        provider_stats.append({
            "provider": provider,
            "pass": s["pass"],
            "fail": s["fail"],
            "total": s["total"],
            "pass_rate": round(rate, 3),
        })

    provider_stats.sort(key=lambda x: x["pass_rate"], reverse=True)

    return {
        "timestamp": data.get("createdAt") or data.get("timestamp"),
        "num_tests": len(table.get("body", [])),
        "providers": provider_stats,
    }
