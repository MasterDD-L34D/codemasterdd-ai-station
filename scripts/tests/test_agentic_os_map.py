"""Guard test for AGENTIC_OS.md (ADR-0044).

The OS map is an index of existing authorities: every repo-relative markdown
link in it must point at a file/dir that exists, so the map cannot rot
silently (Currency Gate, mechanized). Out-of-repo paths are backticked in the
doc by convention and are NOT checked here.

Includes a negative control (L-041: a guard test without a must-fail case
proves nothing).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OS_MAP = REPO_ROOT / "AGENTIC_OS.md"

LINK_RE = re.compile(r"\]\(([^)#\s]+)\)")


def repo_relative_links(text: str) -> list[str]:
    """Markdown link targets that are repo-relative paths (no scheme, no ~)."""
    out = []
    for target in LINK_RE.findall(text):
        if "://" in target or target.startswith(("~", "mailto:")):
            continue
        out.append(target)
    return out


def test_map_exists() -> None:
    assert OS_MAP.is_file(), "AGENTIC_OS.md missing at repo root"


def test_all_repo_links_exist() -> None:
    links = repo_relative_links(OS_MAP.read_text(encoding="utf-8"))
    assert links, "no repo-relative links found -- extractor broken or map emptied"
    missing = [l for l in links if not (REPO_ROOT / l).exists()]
    assert not missing, f"AGENTIC_OS.md links to missing paths: {missing}"


def test_negative_control_detects_missing_path() -> None:
    fake = "see [ghost](docs/adr/9999-does-not-exist.md) and [web](https://x.example)"
    links = repo_relative_links(fake)
    assert links == ["docs/adr/9999-does-not-exist.md"], "extractor must skip URLs, keep repo paths"
    assert not (REPO_ROOT / links[0]).exists(), "negative-control path unexpectedly exists"
