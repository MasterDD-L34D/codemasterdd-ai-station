---
name: feedback-parallel-chip-overlap
description: "Eduardo runs parallel chip/sessions that pick up spawned tasks — before building anything, check open PRs + branches + worktrees BOTH repos, or you redo work already done/in-flight."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 20c560cf-9e4c-416c-a419-e0a1881db0cc
---

Spawned tasks (the spawn_task chips) and parallel Claude sessions actively work the same backlog concurrently on Eduardo's fleet. Before starting ANY build, check current ground-truth in BOTH repos (`C:/dev/Game-Godot-v2` + `C:/dev/Game`): `gh pr list --state all` (open + recently merged), `git ls-remote --heads`, `git worktree list`, recent `origin/main` log. The thing you're about to build may already be done, merged, or in-flight on another branch/worktree.

**Why:** session 2026-05-21/22, FOUR overlaps in one session:
1. run.id collision fix — a parallel chip made a duplicate unmerged worktree (`claude/camp1-run-id-collision`) while I shipped #2374 (had to delete the dup).
2. CAMP-3a run_id plumbing — I was about to brainstorm/build it; verified it was ALREADY on main (shipped in #345 + a codex P2 fix `install_with_run_id`).
3. promotion/conviction `is_kill` wire — I spawned a ticket; turned out already in #345.
4. M1 utility-AI passthrough — I (wrongly) ticketed as latent; a chip implemented it correctly → #2376.

Each verify-before-build pass saved a redundant build. The one time I DIDN'T verify well (grep scope, see [[feedback-verify-scope-packs]]) I got it wrong + a chip corrected me.

**How to apply:** treat "is this already done?" as the FIRST step of any pickup, not an afterthought. When the user says "check your chip finished / use the cross-repo updates", they mean a chip has shipped something — find the branch/PR/worktree (`fix/*`, `feat/*`, `claude/*` not in your session) + read its commit + verify (run its tests) before continuing. Chips are trustworthy-but-verify (their premises can be stale too). Verify-before-build extends to chip output.

Related: [[feedback-verify-scope-packs]], [[project-camp-loop-m1-live]].
