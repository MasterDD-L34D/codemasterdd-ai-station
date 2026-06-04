---
name: feedback-concurrent-writer-standdown
description: "When the shared working tree is being modified by a concurrent actor for the same task, stand down rather than clobber"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 008b5f06-780d-4911-9480-7754bd97f18b
---

When working a task and the local working tree shows uncommitted edits I did not
make — especially if the modified-file set shifts between commands — treat it as
a live concurrent writer (another session, the user, or a bot like "@codex
address that feedback"). **Stand down: do not edit, commit, push, or reply over
their in-flight work.**

**Why:** 2026-05-21, while addressing Codex P1/P2 review on Game-Database PR #154,
the working tree was concurrently being changed by another actor implementing the
same fix (app-layer `assertNotInReleasedVersion` delete guards + backfill
empty-baseline gate). The file set changed between two `git status` calls. Eduardo
confirmed "stand down" as the correct call. Two agents editing the same files =
guaranteed clobber (CLAUDE.md anti-pattern #10 family, concurrent-edit drop).

**How to apply:** On detecting concurrent uncommitted edits I didn't author,
stop, investigate read-only (diffs, `git worktree list`, whether the edits already
address the task), then surface to the user and ask who owns the fix before
touching anything. Eduardo runs parallel sessions/agents on the fleet, so this is
a recurring situation, not a one-off. Prefer letting the active writer finish.
