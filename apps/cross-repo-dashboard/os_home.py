"""Pure helpers for the OS console home. Kept out of app.py so they stay
unit-testable without a Flask context."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

HUB = Path(r"C:\dev\codemasterdd-ai-station")
_ROW = re.compile(r"^\|\s*\d+\s*\|\s*(?P<layer>[^|]+?)\s*\|\s*(?P<authority>[^|]+?)\s*\|")


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
