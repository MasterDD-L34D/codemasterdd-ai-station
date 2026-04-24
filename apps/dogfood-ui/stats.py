"""Aggregation helpers per dogfood stats + promptfoo bench parsing."""
from __future__ import annotations

import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


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

    # Per class breakdown
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

    # Per stack breakdown
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

    # Cost cumulative
    total_cost = sum(float(e["cost_usd"] or 0) for e in entries)
    total_tokens_sent = sum(int(e["tokens_sent"] or 0) for e in entries)
    total_tokens_recv = sum(int(e["tokens_received"] or 0) for e in entries)

    # Fase 6 ADR-0014 criteria
    target_n = 20
    target_fail_rate_max = 0.30
    cost_budget_monthly = 20.0

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
        "phase6": {
            "target_n": target_n,
            "progress_pct": round((total / target_n) * 100, 1),
            "fail_rate_limit": target_fail_rate_max,
            # ADR-0014 criterio 2: "fail rate <30%" → threshold strict (30% esatto = FAIL)
            "fail_rate_status": "PASS" if fail_rate_strict < target_fail_rate_max else "FAIL",
            "cost_budget_monthly": cost_budget_monthly,
            # Budget $20/mo è hard cap (esatto 20 = FAIL)
            "cost_status": "PASS" if total_cost < cost_budget_monthly else "FAIL",
        },
    }


def empty_stats() -> dict[str, Any]:
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
