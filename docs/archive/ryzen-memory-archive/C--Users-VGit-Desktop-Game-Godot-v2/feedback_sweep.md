---
name: Sweep routine before each sprint step
description: Pre-step audit checklist user expects before any meaningful change
type: feedback
originSessionId: 585dba96-6d14-4988-ab48-b6cb8dcaf004
---
Run sweep before every sprint step (memorized supermemory f1729730).

**Why:** User has been bitten by drift between sprint chips when working in parallel worktrees. Codex review comments accumulate; doc state diverges; format/lint warnings pile up. Routine sweep keeps trunk healthy.

**How to apply** (8 checks):
1. `gh api repos/MasterDD-L34D/Game-Godot-v2/pulls/<N>/comments` — pending codex feedback on recent PRs
2. `git status` clean (only `.claude/worktrees/` submodule modifications acceptable)
3. `python -m gdtoolkit.formatter --check $(find scripts tests -name "*.gd")` clean
4. `python -m gdtoolkit.linter $(find scripts tests -name "*.gd")` no problems
5. `godot.cmd --headless --path . --import` zero errors
6. `godot.cmd --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://tests/ -ginclude_subdirs -gexit` all pass
7. PowerShell cleanup orphan ports (3334, 3341, 8000, 8443, 4040)
8. CLAUDE.md doc consistency: PR count, Sprint X.Y status, GUT total, NEXT marker

**Drift remediation:** if any check fails → branch fix → PR → CI green → squash merge before continuing main work.
