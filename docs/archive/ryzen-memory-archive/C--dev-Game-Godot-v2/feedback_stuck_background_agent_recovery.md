# Stuck background subagent across session resume — recovery

**Date**: 2026-05-22 (CAMP-3c, PR #350)

## What happened
A subagent dispatched right before a session resume ("Implement Unit B") got backgrounded by the harness and HUNG: 64min, 84.9k tokens, 18 tool uses, never returned. It had partially executed: committed Task 3 (`2ffaf06`) AND left Task 4 edits uncommitted in the working tree — then appeared idle. The resume session had no `agentId` handle for it (it never returned a result).

## Recovery procedure (worked)
1. **Ground-truth git FIRST on resume** — `git status -s` + `git log` + `git diff`. Do NOT assume where the flow left off; a backgrounded actor may have committed/edited since. Here the tree held an in-flight Task 4 (incl. a real `queue_free` fix) that I had to verify (ran the tests → 2 failing assertions → fixed) before continuing.
2. Treat the working-tree leftover as "implementer output to review": run tests, fix, commit clean, then two-stage review the whole unit.
3. **Killing it**: `TaskStop` needs a `task_id`; a hung agent that never returned gives no id, and `TaskList` shows only the TODO list (TaskCreate items), NOT background agents. → No programmatic handle from the controller. The lever is the UI **"Interrompi"** button (background-activity card) — ask the user to click it.

## Rules
- On any resume: assume parallel/backgrounded actors advanced the work. Ground-truth before building (extends verify-before-build to "what did the backgrounded agent already commit/edit").
- A hung backgrounded subagent with no returned id is not controller-stoppable — surface it + ask user to Interrompi. It's idle (not editing), so a clean tree = no harm; main risk is wasted tokens + a future wake racing your commits.
- Don't re-dispatch a unit whose work is already in the tree — recover it, don't duplicate.
