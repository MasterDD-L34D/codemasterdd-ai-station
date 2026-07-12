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
    # A tier-1 action must not only NAME a wrapper -- the wrapper must resolve to
    # a real file in the repo. A dangling label (the old "gh-draft-pr" that was
    # never a script) would let a bare, unguarded command masquerade as gated.
    repo_root = Path(__file__).resolve().parents[2]
    for a in ACTIONS:
        if a["tier"] == 1:
            assert a.get("wrapper"), f"{a['id']}: tier-1 must route through a named fail-closed wrapper"
            wp = a.get("wrapper_path")
            assert wp, f"{a['id']}: tier-1 must declare a wrapper_path"
            resolved = repo_root.joinpath(*wp.replace("\\", "/").split("/"))
            assert resolved.is_file(), f"{a['id']}: wrapper_path does not resolve to a file: {resolved}"


def test_argv_elements_are_literal_strings() -> None:
    # every argv token is a literal str: nothing to interpolate from client input
    for a in ACTIONS:
        for step in a.get("steps", []):
            for tok in step:
                assert isinstance(tok, str), f"{a['id']}: argv token not a literal string: {tok!r}"


def test_step_script_paths_resolve() -> None:
    # any .ps1/.py path token in a step must resolve to a real file in the repo.
    # Codex #552: governance-lint pointed at a non-existent scripts/governance-lint.py,
    # so the tier-0 action failed with file-not-found instead of producing the report.
    repo_root = Path(__file__).resolve().parents[2]
    for a in ACTIONS:
        for step in a.get("steps", []):
            for tok in step:
                if tok.endswith((".ps1", ".py")):
                    resolved = repo_root.joinpath(*tok.replace("\\", "/").split("/"))
                    assert resolved.is_file(), f"{a['id']}: step path does not resolve: {tok} -> {resolved}"


def test_params_are_whitelist_choices_only() -> None:
    for a in ACTIONS:
        for p in a.get("params", []):
            assert p.get("name") and isinstance(p.get("choices"), list) and p["choices"], \
                f"{a['id']}: param must have a name + non-empty whitelist choices"
            assert all(isinstance(c, str) for c in p["choices"]), f"{a['id']}: param choices must be strings"
            # every param must declare the fixed CLI flag it maps to: the endpoint
            # appends [flag, choice], so a param with no flag would be a dead dropdown.
            assert isinstance(p.get("flag"), str) and p["flag"].startswith("-"), \
                f"{a['id']}: param {p.get('name')!r} must declare a CLI flag (e.g. --repo)"


def test_param_actions_are_single_step() -> None:
    # params append to steps[-1] server-side; keeping param'd actions single-step
    # makes that append target unambiguous (no silent apply-to-wrong-step).
    for a in ACTIONS:
        if a.get("params"):
            assert len(a.get("steps", [])) == 1, \
                f"{a['id']}: an action with params must have exactly one step"


def test_negative_control_injection_id_not_in_registry() -> None:
    # a shell-injection-looking id must simply not resolve (dict lookup miss)
    ids = {a["id"] for a in ACTIONS}
    assert "fleet-verify; rm -rf /" not in ids
    assert not any(";" in i or "&&" in i or "|" in i for i in ids), "action ids must be plain slugs"


def test_parse_layers_reads_seven_rows(tmp_path) -> None:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "cross-repo-dashboard"))
    from os_home import parse_layers
    m = tmp_path / "AGENTIC_OS.md"
    m.write_text(
        "| # | Layer | Authority | Note |\n|---|---|---|---|\n"
        "| 1 | Kernel | ORCHESTRATION.md | x |\n| 2 | Routing | MODEL_ROUTING.md | y |\n",
        encoding="utf-8",
    )
    rows = parse_layers(m)
    assert rows == [{"layer": "Kernel", "authority": "ORCHESTRATION.md"},
                    {"layer": "Routing", "authority": "MODEL_ROUTING.md"}]


def test_latest_brief_placeholder_when_absent(tmp_path) -> None:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "cross-repo-dashboard"))
    from os_home import latest_brief
    assert "non ancora generato" in latest_brief("2099-01-01", tmp_path)


def _import_os_home():
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "cross-repo-dashboard"))
    import os_home  # noqa: PLC0415
    return os_home


def test_scheduled_task_health_injected() -> None:
    # hermetic: inject the query fn so no real Task Scheduler is touched.
    oh = _import_os_home()
    fake = {"morning-brief": {"LastTaskResult": 0, "State": "Ready", "LastRunTime": "2026-07-13T08:30:00"}}
    rows = oh.scheduled_task_health(["morning-brief", "jules-daily-digest"], query_fn=fake.get)
    by = {r["name"]: r for r in rows}
    assert by["morning-brief"]["healthy"] is True and by["morning-brief"]["state"] == "Ready"
    # absent task -> unhealthy, state 'absent' (must-fail branch, L-041)
    assert by["jules-daily-digest"]["healthy"] is False and by["jules-daily-digest"]["state"] == "absent"
    # a non-zero last result is NOT healthy
    bad = oh.scheduled_task_health(["x"], query_fn=lambda n: {"LastTaskResult": 1, "State": "Ready"})
    assert bad[0]["healthy"] is False


def test_active_hooks_parses(tmp_path) -> None:
    oh = _import_os_home()
    p = tmp_path / "settings.json"
    p.write_text('{"hooks": {"PreToolUse": [{"a":1}], "Stop": [{"b":2},{"c":3}]}}', encoding="utf-8")
    h = oh.active_hooks(p)
    assert h["available"] and h["count"] == 3 and h["events"] == ["PreToolUse", "Stop"]
    assert oh.active_hooks(tmp_path / "nope.json")["available"] is False


def test_memory_index_size_budget(tmp_path) -> None:
    oh = _import_os_home()
    small = tmp_path / "m1.md"
    small.write_text("a\nb\nc\n", encoding="utf-8")
    assert oh.memory_index_size(small)["over_budget"] is False
    big = tmp_path / "m2.md"
    big.write_text("\n".join(f"line {i}" for i in range(250)), encoding="utf-8")
    assert oh.memory_index_size(big)["over_budget"] is True
    assert oh.memory_index_size(tmp_path / "absent.md")["available"] is False


def test_count_agents_and_lessons(tmp_path) -> None:
    oh = _import_os_home()
    agents = tmp_path / "agents"
    (agents / "_dormant").mkdir(parents=True)
    (agents / "README.md").write_text("x", encoding="utf-8")
    (agents / "a.md").write_text("x", encoding="utf-8")
    (agents / "b.md").write_text("x", encoding="utf-8")
    (agents / "_dormant" / "d.md").write_text("x", encoding="utf-8")
    res = oh.count_agents(agents)
    assert res == {"active": 2, "dormant": 1}  # README excluded
    learn = tmp_path / "learnings"
    learn.mkdir()
    (learn / "L-001.md").write_text("x", encoding="utf-8")
    (learn / "notes.md").write_text("x", encoding="utf-8")  # not an L-*.md
    lc = oh.aa01_lesson_count(learn)
    assert lc["available"] and lc["count"] == 1
