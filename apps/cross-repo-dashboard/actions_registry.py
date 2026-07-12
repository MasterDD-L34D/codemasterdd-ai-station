"""Agentic OS Console action catalog (data-only, tiered).

SECURITY CONTRACT (mirrors dashboards_registry.py): `steps` are FIXED argv
lists (no shell, no client input ever interpolated). /api/run-action accepts
only an action id + whitelisted param CHOICES; it executes these exact argv
lists with shell=False. Adding an entry here is the only way to make something
runnable from the OS console -- reviewed like code, because it is code.

Tiers: 0 = read/report (one-click, free) | 1 = mutating-reversible (human click
= authorization, MUST route through an existing fail-closed wrapper) | 2 =
excluded (no executable steps; merge-main/force-push/external comms stay off).
"""
from __future__ import annotations

from typing import Any

HUB = r"C:\dev\codemasterdd-ai-station"

ACTIONS: list[dict[str, Any]] = [
    # ---- tier 0: read / report ----
    {
        "id": "fleet-verify", "label": "Fleet-verify (audit flotta)", "tier": 0,
        "area": "audit", "desc": "Machine-aware fleet audit (read-mostly).",
        "steps": [["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                   "-File", r"scripts\fleet\morning-brief.ps1", "-NoFile"]],
        "cwd": HUB, "timeout": 600, "ok_exit_codes": [0],
    },
    {
        "id": "morning-brief", "label": "Morning brief (rigenera)", "tier": 0,
        "area": "report", "desc": "Regenerate the R0 fleet heartbeat now.",
        "steps": [["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                   "-File", r"scripts\fleet\morning-brief.ps1"]],
        "cwd": HUB, "timeout": 300, "ok_exit_codes": [0],
    },
    {
        "id": "fleet-pr-status", "label": "PR flotta (gh)", "tier": 0,
        "area": "report", "desc": "Open PRs across monitored repos.",
        "steps": [["gh", "pr", "list", "--repo", "MasterDD-L34D/codemasterdd-ai-station",
                   "--state", "open", "--limit", "50"]],
        "cwd": HUB, "timeout": 120, "ok_exit_codes": [0],
    },
    {
        "id": "governance-lint", "label": "Governance lint", "tier": 0,
        "area": "audit", "desc": "Run the governance lint report.",
        "steps": [["py", "-3", r"scripts\governance-lint.py"]],
        "cwd": HUB, "timeout": 300, "ok_exit_codes": [0, 1],  # lint rc=1 when it finds items
    },
    {
        "id": "pytest-scripts", "label": "Pytest (scripts)", "tier": 0,
        "area": "audit", "desc": "Run the repo pytest suite.",
        "steps": [["py", "-m", "pytest", "-q", "scripts/tests"]],
        "cwd": HUB, "timeout": 300, "ok_exit_codes": [0],
    },
    # ---- tier 1: mutating-reversible (via existing fail-closed wrappers) ----
    {
        "id": "jules-dispatch", "label": "Dispatch Jules (scoped)", "tier": 1,
        "area": "delegate", "desc": "Dispatch a scoped Jules session via the fail-closed wrapper.",
        "wrapper": "jules-dispatch",
        "steps": [["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                   "-File", r"scripts\fleet\jules-dispatch.ps1", "-DryRun"]],
        "cwd": HUB, "timeout": 180, "ok_exit_codes": [0],
        "params": [{"name": "repo", "choices": ["Game", "Game-Godot-v2", "Game-Database", "codemasterdd-ai-station"]}],
    },
    {
        "id": "create-draft-pr", "label": "Crea draft-PR (branch corrente)", "tier": 1,
        "area": "delegate", "desc": "Push current claude/* branch + open a DRAFT PR.",
        "wrapper": "gh-draft-pr",
        "steps": [["gh", "pr", "create", "--draft", "--fill",
                   "--repo", "MasterDD-L34D/codemasterdd-ai-station"]],
        "cwd": HUB, "timeout": 120, "ok_exit_codes": [0],
    },
    {
        "id": "aider-delegate", "label": "Delega Aider (cosmetic)", "tier": 1,
        "area": "delegate", "desc": "Delegate a cosmetic edit via the privacy-guarded wrapper.",
        "wrapper": "aider-cosmetic",
        "steps": [["bash", "-lc", "aider-cosmetic --version"]],  # placeholder invocation; real target added at wire-time
        "cwd": HUB, "timeout": 120, "ok_exit_codes": [0],
        "params": [{"name": "repo", "choices": ["codemasterdd-ai-station", "Game", "Game-Godot-v2"]}],
    },
    # ---- tier 2: excluded (documented, NOT runnable) ----
    {
        "id": "merge-main", "label": "Merge to main (doctrine)", "tier": 2,
        "area": "excluded", "desc": "Excluded from the panel -- Eduardo-only, classifier backstop.",
    },
]
