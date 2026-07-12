"""Guard tests for the OS console action registry.

Mirrors test_dashboards_registry.py: schema integrity, the fixed-argv security
contract (the UI can never inject commands), tier enforcement, and negative
controls (L-041: a guard without a must-fail case proves nothing).
"""
from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[2] / "apps" / "cross-repo-dashboard"
sys.path.insert(0, str(APP_DIR))

from actions_registry import ACTIONS  # noqa: E402

VALID_TIERS = {0, 1, 2}


def test_ids_unique() -> None:
    ids = [a["id"] for a in ACTIONS]
    assert len(ids) == len(set(ids)), "duplicate action ids"


def test_schema_and_display_fields() -> None:
    for a in ACTIONS:
        assert a["tier"] in VALID_TIERS, f"{a['id']}: bad tier {a['tier']}"
        assert a.get("label") and a.get("area") and a.get("desc"), f"{a['id']}: missing display fields"


def test_tier0_and_tier1_have_executable_steps() -> None:
    for a in ACTIONS:
        if a["tier"] in (0, 1):
            assert a.get("steps") and all(isinstance(s, list) and s for s in a["steps"]), \
                f"{a['id']}: tier {a['tier']} needs non-empty argv steps"


def test_tier2_has_no_executable_steps() -> None:
    for a in ACTIONS:
        if a["tier"] == 2:
            assert not a.get("steps"), f"{a['id']}: tier-2 must not carry runnable steps"


def test_tier1_requires_wrapper() -> None:
    for a in ACTIONS:
        if a["tier"] == 1:
            assert a.get("wrapper"), f"{a['id']}: tier-1 must route through a named fail-closed wrapper"


def test_argv_elements_are_literal_strings() -> None:
    # every argv token is a literal str: nothing to interpolate from client input
    for a in ACTIONS:
        for step in a.get("steps", []):
            for tok in step:
                assert isinstance(tok, str), f"{a['id']}: argv token not a literal string: {tok!r}"


def test_params_are_whitelist_choices_only() -> None:
    for a in ACTIONS:
        for p in a.get("params", []):
            assert p.get("name") and isinstance(p.get("choices"), list) and p["choices"], \
                f"{a['id']}: param must have a name + non-empty whitelist choices"
            assert all(isinstance(c, str) for c in p["choices"]), f"{a['id']}: param choices must be strings"


def test_negative_control_injection_id_not_in_registry() -> None:
    # a shell-injection-looking id must simply not resolve (dict lookup miss)
    ids = {a["id"] for a in ACTIONS}
    assert "fleet-verify; rm -rf /" not in ids
    assert not any(";" in i or "&&" in i or "|" in i for i in ids), "action ids must be plain slugs"
