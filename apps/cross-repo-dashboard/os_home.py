"""Pure helpers for the OS console home. Kept out of app.py so they stay
unit-testable without a Flask context.

Beyond parsing the layer map, these expose the LIVE per-layer state the OS home
surfaces (the research/spec point: the console must MOSTRARE lo stato dell'OS, not
just its static structure). Each helper is dependency-light (stdlib + optional
subprocess) and side-effect free, and every one that shells out accepts an
injectable callable so tests stay hermetic and CI (pytest-only) can import it.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable

HUB = Path(r"C:\dev\codemasterdd-ai-station")
_ROW = re.compile(r"^\|\s*\d+\s*\|\s*(?P<layer>[^|]+?)\s*\|\s*(?P<authority>[^|]+?)\s*\|")
_TASK_NAME_RE = re.compile(r"^[\w.\- ]+$")  # scheduled-task names are constants, not client input


def parse_layers(map_path: Path | None = None) -> list[dict[str, str]]:
    """Extract the 7 layer rows from AGENTIC_OS.md's layer table."""
    p = map_path or (HUB / "AGENTIC_OS.md")
    if not p.is_file():
        return []
    out: list[dict[str, str]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        m = _ROW.match(line)
        if m and m.group("layer").strip().lower() not in {"layer", "---"}:
            out.append({"layer": m.group("layer").strip(), "authority": m.group("authority").strip()})
    return out


def latest_brief(today: str, brief_dir: Path | None = None) -> str:
    """Return the latest morning brief text, or a placeholder if none for today."""
    d = brief_dir or (HUB / "logs" / "morning-brief")
    f = d / f"{today}.md"
    if f.is_file():
        return f.read_text(encoding="utf-8")
    return "(morning brief non ancora generato per oggi -- usa l'azione 'Morning brief')"


# ---- live per-layer signals (the "MOSTRA lo stato dell'OS" half) ---------- #

def _query_scheduled_task(name: str) -> dict[str, Any] | None:
    """Query one Windows scheduled task via PowerShell. Returns None if absent.

    Uses Get-ScheduledTaskInfo (stable English property names -> locale-proof,
    unlike schtasks LIST which localizes field labels)."""
    ps = (
        f"$i=Get-ScheduledTaskInfo -TaskName '{name}' -ErrorAction SilentlyContinue;"
        f"if($i){{$s=(Get-ScheduledTask -TaskName '{name}' -ErrorAction SilentlyContinue).State;"
        f"$lr=if($i.LastRunTime){{$i.LastRunTime.ToString('s')}}else{{''}};"
        f"[pscustomobject]@{{LastTaskResult=$i.LastTaskResult;LastRunTime=$lr;State=\"$s\"}}"
        f"|ConvertTo-Json -Compress}}"
    )
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True, text=True, timeout=15, check=False,
        )
    except Exception:  # noqa: BLE001
        return None
    out = (r.stdout or "").strip()
    if not out:
        return None
    try:
        return json.loads(out)
    except ValueError:
        return None


def scheduled_task_health(
    names: list[str], query_fn: Callable[[str], dict[str, Any] | None] | None = None
) -> list[dict[str, Any]]:
    """Live health of the Scheduling layer's tasks (morning-brief, jules-digest).

    `query_fn` is injectable so tests never touch the real Task Scheduler.
    healthy == last run returned exit 0."""
    q = query_fn or _query_scheduled_task
    out: list[dict[str, Any]] = []
    for name in names:
        info = q(name) if _TASK_NAME_RE.match(name) else None
        if not info:
            out.append({"name": name, "state": "absent", "last_result": None,
                        "last_run": None, "healthy": False})
            continue
        lr = info.get("LastTaskResult")
        out.append({
            "name": name, "state": info.get("State", "?"), "last_result": lr,
            "last_run": info.get("LastRunTime") or None, "healthy": lr == 0,
        })
    return out


def memory_index_size(path: Path | None = None) -> dict[str, Any]:
    """MEMORY.md index size (Memoria layer). Research: only first 200 lines / 25KB
    are loaded, so flag when the index outgrows that budget."""
    p = path or (Path.home() / ".claude" / "projects"
                 / "C--dev-codemasterdd-ai-station" / "memory" / "MEMORY.md")
    if not p.is_file():
        return {"available": False}
    txt = p.read_text(encoding="utf-8", errors="replace")
    lines = txt.count("\n") + 1
    kb = round(len(txt.encode("utf-8")) / 1024, 1)
    return {"available": True, "lines": lines, "kb": kb, "over_budget": lines > 200 or kb > 25}


def active_hooks(settings_path: Path | None = None) -> dict[str, Any]:
    """Enforced hooks (Safety layer) from a settings.json (project by default)."""
    p = settings_path or (HUB / ".claude" / "settings.json")
    if not p.is_file():
        return {"available": False, "events": [], "count": 0}
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        return {"available": False, "events": [], "count": 0}
    hooks = data.get("hooks", {})
    count = sum(len(v) for v in hooks.values() if isinstance(v, list))
    return {"available": True, "events": sorted(hooks.keys()), "count": count}


def count_agents(agents_dir: Path | None = None) -> dict[str, int]:
    """Subagent inventory (Esecutori layer): active *.md + _dormant/*.md."""
    d = agents_dir or (HUB / ".claude" / "agents")
    if not d.is_dir():
        return {"active": 0, "dormant": 0}
    active = sum(1 for f in d.glob("*.md") if f.name.lower() != "readme.md")
    dormant_dir = d / "_dormant"
    dormant = sum(1 for _ in dormant_dir.glob("*.md")) if dormant_dir.is_dir() else 0
    return {"active": active, "dormant": dormant}


def aa01_lesson_count(learnings_dir: Path | None = None) -> dict[str, Any]:
    """AA01 lessons count (Self-maintenance layer)."""
    d = learnings_dir or (Path.home() / "aa01" / "learnings")
    if not d.is_dir():
        return {"available": False, "count": 0}
    return {"available": True, "count": sum(1 for _ in d.glob("L-*.md"))}
