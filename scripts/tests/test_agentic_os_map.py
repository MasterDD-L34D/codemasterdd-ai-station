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

LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def repo_relative_links(text: str) -> list[str]:
    """Repo-relative link targets (no scheme, no ~), with any #fragment or
    ?query stripped so a link like `ORCHESTRATION.md#cost-ladder` is validated
    against the file rather than silently skipped."""
    out = []
    for target in LINK_RE.findall(text):
        if "://" in target or target.startswith(("~", "mailto:", "#")):
            continue
        path = target.split("#", 1)[0].split("?", 1)[0]
        if path:
            out.append(path)
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


def test_fragment_link_is_validated_not_skipped() -> None:
    # a link to a section (#anchor) must resolve to the base file, not be dropped
    links = repo_relative_links("see [x](CLAUDE.md#ordine) and [y](docs/adr/9999-nope.md#s1)")
    assert links == ["CLAUDE.md", "docs/adr/9999-nope.md"], "fragment must be stripped, base kept"
    assert (REPO_ROOT / links[0]).exists(), "real base file behind #anchor must be checked"
    assert not (REPO_ROOT / links[1]).exists(), "missing base behind #anchor must still be caught"
