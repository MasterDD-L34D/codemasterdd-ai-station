"""Regression guards for the backup mirror scripts (SPOF insurance).

History:
- L-040 (2026-05-28): git writes progress ("Cloning into...") to stderr;
  under $ErrorActionPreference=Stop PowerShell 5.1 turned successful clones
  into terminating NativeCommandError false-fails. Success must be gated on
  $LASTEXITCODE only.
- 2026-06-11 audit: the static repo list drifted -- 3 org repos created
  after the 2026-05-28 snapshot (compass-marketplace, evo-tactics-refs-meta,
  LeaD) were silently missing from account-loss coverage. Discovery via
  `gh repo list` is now the authority; a discovery failure must stay loud
  (exit 1, no silent fail-open -- lesson family L-041).

Static asserts only (no PowerShell execution): CI-safe, offline.
"""

import re
from pathlib import Path

BACKUP = Path(__file__).resolve().parents[1] / "backup"
MIRROR = BACKUP / "mirror-repos.ps1"
EXTERNAL = BACKUP / "copy-mirror-to-external.ps1"


def mirror_text():
    return MIRROR.read_text(encoding="utf-8")


def external_text():
    return EXTERNAL.read_text(encoding="utf-8")


def test_scripts_exist():
    assert MIRROR.is_file(), f"missing {MIRROR}"
    assert EXTERNAL.is_file(), f"missing {EXTERNAL}"


# --- L-040 family: native stderr must not fail successful git/robocopy ---

def test_l040_mirror_no_stop_preference():
    text = mirror_text()
    assert '$ErrorActionPreference = "Continue"' in text, "L-040 fix removed"
    stop_assign = re.search(
        r"\$ErrorActionPreference\s*=\s*[\"']Stop[\"']", text
    )
    assert stop_assign is None, "ErrorActionPreference=Stop reintroduced (L-040)"


def test_l040_mirror_gates_on_lastexitcode():
    assert "$LASTEXITCODE -ne 0" in mirror_text(), (
        "per-repo success must be gated on $LASTEXITCODE"
    )


def test_l040_external_continue_and_robocopy_convention():
    text = external_text()
    assert "$ErrorActionPreference = 'Continue'" in text, "L-040 fix removed"
    assert "-lt 8" in text, "robocopy <8 = benign convention removed"


# --- org discovery: anti static-list drift ---

def test_discovery_is_primary():
    assert "gh repo list" in mirror_text(), (
        "org discovery removed: static lists drift (3 repos missed 2026-06)"
    )


def test_explicit_repos_skips_discovery():
    assert "$PSBoundParameters.ContainsKey('Repos')" in mirror_text(), (
        "-Repos override must skip discovery (subset use-case)"
    )


def test_discovery_failure_is_loud():
    text = mirror_text()
    assert "$discoveryFailed" in text, "discovery-failure flag missing"
    assert "DONE (degraded)" in text, (
        "degraded-run marker missing: static fallback must end exit 1, "
        "not blend into the all-green DONE (no silent fail-open)"
    )


def test_gh_probe_avoids_stale_lastexitcode():
    # a missing gh.exe leaves $LASTEXITCODE stale; presence must be probed
    assert "Get-Command gh" in mirror_text(), (
        "gh presence probe missing (stale-$LASTEXITCODE trap)"
    )


# --- ADR-0021: no non-ASCII in script bodies ---

def test_scripts_are_ascii():
    for path in (MIRROR, EXTERNAL):
        raw = path.read_bytes()
        bad = [b for b in raw if b > 127]
        assert not bad, f"non-ASCII bytes in {path.name} (ADR-0021)"
