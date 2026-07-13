"""Agentic OS Console action catalog (data-only, tiered).

SECURITY CONTRACT (mirrors dashboards_registry.py): `steps` are FIXED argv
lists (no shell, no client input ever interpolated). /api/run-action accepts
only an action id + whitelisted param CHOICES; it executes these exact argv
lists with shell=False. Adding an entry here is the only way to make something
runnable from the OS console -- reviewed like code, because it is code.

PARAMS -> ARGV: a param maps a whitelisted CHOICE to a fixed CLI `flag`. The
endpoint appends `[flag, value]` to the (single) step server-side; the flag
comes from this registry and the value only from `choices` -- never free text.
An action carrying `params` therefore has exactly ONE step (test-enforced), so
the append target is unambiguous.

Tiers: 0 = read/report (one-click, free) | 1 = mutating-reversible (human click
= authorization, MUST route through an existing fail-closed wrapper; also
requires API_SECRET to be set) | 2 = excluded (no executable steps;
merge-main/force-push/external comms stay off).
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
        "area": "report", "desc": "Open PRs for a monitored repo (dropdown).",
        "steps": [["gh", "pr", "list", "--state", "open", "--limit", "50"]],
        "cwd": HUB, "timeout": 120, "ok_exit_codes": [0],
        # working param: the chosen slug is appended as `--repo <slug>` server-side
        # (flag from here, value only from choices). Default (first) = the hub.
        "params": [{"name": "repo", "flag": "--repo", "choices": [
            "MasterDD-L34D/codemasterdd-ai-station", "MasterDD-L34D/Game",
            "MasterDD-L34D/Game-Godot-v2", "MasterDD-L34D/Game-Database",
        ]}],
    },
    {
        "id": "governance-lint", "label": "Governance lint", "tier": 0,
        "area": "audit", "desc": "Run the governance lint report.",
        # the generator is a .ps1 (there is no governance-lint.py); mirror the
        # dashboards_registry invocation so the action actually produces the report.
        "steps": [["powershell", "-NoProfile", "-File", r"scripts\governance-lint.ps1"]],
        "cwd": HUB, "timeout": 300, "ok_exit_codes": [0, 1],  # lint rc=1 when it finds items
    },
    {
        "id": "pytest-scripts", "label": "Pytest (scripts)", "tier": 0,
        "area": "audit", "desc": "Run the repo pytest suite.",
        "steps": [["py", "-m", "pytest", "-q", "scripts/tests"]],
        "cwd": HUB, "timeout": 300, "ok_exit_codes": [0],
    },
    # ---- tier 1: mutating-reversible (via a real fail-closed wrapper) ----
    {
        "id": "create-draft-pr", "label": "Crea draft-PR (branch corrente)", "tier": 1,
        "area": "delegate", "desc": "Guarded: open a DRAFT PR for the current claude/* branch (--head pinned).",
        "wrapper": "draft-pr",
        # the wrapper is fail-closed: aborts unless HEAD is a pushed claude/* branch,
        # then `gh pr create --draft` with --head pinned to that branch (no client input).
        "wrapper_path": r"scripts\fleet\draft-pr.ps1",
        "steps": [["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                   "-File", r"scripts\fleet\draft-pr.ps1"]],
        "cwd": HUB, "timeout": 120, "ok_exit_codes": [0],
    },
    # ---- tier 1: Jules scoped-dispatch PREVIEW (v2) ----
    # The jules-dispatch wrapper needs -Repo + -TaskFile + -Target, and gate 3
    # enforces Target<->task-file consistency -- so template and target are COUPLED
    # (independent dropdowns cannot satisfy the wrapper without a free-text Target,
    # which the whitelist-only model forbids). The whitelist-safe fit is therefore
    # ONE fixed-argv entry per pre-authored scoped task (reviewed like code), each
    # run with -DryRun: it exercises all 5 gates + builds the REST body + writes a
    # DRYRUN audit line, but does NOT POST (no outward dispatch). Add a new task by
    # committing a docs/jules/templates/*.md and a sibling entry here. Real dispatch
    # (dropping -DryRun) stays a human CLI action for now.
    {
        "id": "jules-preview-journal-land",
        "label": "Jules preview: docstring pass journal-land.ps1 (dry-run)", "tier": 1,
        "area": "delegate",
        "desc": "Validate a scoped Jules docstring task on scripts/fleet/journal-land.ps1 "
                "(5 gates -- incl. a live Jules session GET -- + REST body; NO POST/dispatch).",
        "wrapper": "jules-dispatch", "wrapper_path": r"scripts\fleet\jules-dispatch.ps1",
        "steps": [["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                   "-File", r"scripts\fleet\jules-dispatch.ps1",
                   "-Repo", "codemasterdd-ai-station",
                   "-TaskFile", r"docs\jules\templates\docstring-pass-journal-land.md",
                   "-Target", "scripts/fleet/journal-land.ps1", "-DryRun"]],
        "cwd": HUB, "timeout": 180, "ok_exit_codes": [0],
    },
    {
        "id": "jules-preview-morning-brief",
        "label": "Jules preview: docstring pass morning-brief.ps1 (dry-run)", "tier": 1,
        "area": "delegate",
        "desc": "Validate a scoped Jules docstring task on scripts/fleet/morning-brief.ps1 "
                "(5 gates -- incl. a live Jules session GET -- + REST body; NO POST/dispatch).",
        "wrapper": "jules-dispatch", "wrapper_path": r"scripts\fleet\jules-dispatch.ps1",
        "steps": [["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                   "-File", r"scripts\fleet\jules-dispatch.ps1",
                   "-Repo", "codemasterdd-ai-station",
                   "-TaskFile", r"docs\jules\templates\docstring-pass-morning-brief.md",
                   "-Target", "scripts/fleet/morning-brief.ps1", "-DryRun"]],
        "cwd": HUB, "timeout": 180, "ok_exit_codes": [0],
    },
    # ---- tier 2: excluded (documented, NOT runnable) ----
    {
        "id": "merge-main", "label": "Merge to main (doctrine)", "tier": 2,
        "area": "excluded", "desc": "Excluded from the panel -- Eduardo-only, classifier backstop.",
    },
]
