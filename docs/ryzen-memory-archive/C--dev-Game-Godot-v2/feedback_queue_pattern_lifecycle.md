---
name: feedback-queue-pattern-lifecycle
description: Queue pattern (deferred emit) richiede lifecycle coverage — ogni state mutation path che tocca related state MUST also touch queue. PR #320 #322 #325 cascade evidence — queue introduced twice subito 1 codex bug each.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7c08f071-f7f8-4cf0-a16b-fcd6aba717fa
---

Queue pattern (`Array` queued state mutations + later flush) richiede **full lifecycle coverage** — ogni state mutation path che tocca related state MUST also touch queue. Reviewer subagents focus on diff scope, miss orphan reset paths.

**Evidence wave 2026-05-20**:

| PR | Queue introduced | Codex bug catched | Fix PR |
|---|---|---|---|
| #320 | (no queue, direct append) | P2 chronology (out-of-order) | #322 |
| #322 | `_pending_bond_broken: Array` introduced as fix | P2 reset_ledger leak (stale entries cross-encounter) | **#325** |
| #325 | `reset_ledger` clears queue | (clean async pending) | — |

**Pattern caught**: queue introduced PR #322 to fix #320 chronology → BUT queue NOT cleared on reset_ledger() → next bug. Same surface, two consecutive codex findings.

## Required lifecycle coverage matrix per queue

Quando introduci `_pending_X: Array` queue + later flush, MUST address ALL state mutation paths:

| Lifecycle event | Queue action |
|---|---|
| `append` during normal flow | OK (intended) |
| `session_ended` / flush trigger | flush + clear |
| `reset_ledger` / abort / teardown | **CLEAR** (prevent stale leak) |
| Hook destruction / queue_free | clear (defensive, optional) |
| `setup(orchestrator)` re-init | clear (fresh hook = fresh queue) |

## Test pattern for queue lifecycle coverage

Per ogni queue introduced, add tests:

```
test_<queue>_flushed_at_<flush_trigger>           # happy path
test_<queue>_cleared_on_reset                     # ABORT/teardown path
test_<queue>_cleared_on_re_setup                  # re-init path
test_<queue>_no_cross_session_leak                # multi-session integration
```

Skip `test_<queue>_cleared_on_re_setup` only if setup() doesn't exist or is no-op for queue state.

## Anti-pattern checklist pre-merge

Quando review PR che introduce queue:
- [ ] All public mutation methods touch queue?
- [ ] `reset_*` / abort methods clear queue?
- [ ] Hook setup/re-setup re-initializes queue?
- [ ] Lifecycle test asserts no cross-session leak?
- [ ] Spec self-review section on queue lifecycle paths?

## Subagent reviewer instructions update

`subagent-driven-development` code-quality-reviewer prompt should EXPLICITLY ask:

> "When reviewing implementations that introduce deferred-state queues (`_pending_*: Array`), verify ALL lifecycle paths (flush + reset + re-init) touch the queue. Reviewer's blind spot in PR #320/#322/#325 cascade: queue introduced but reset path orphaned. Reference: `feedback_queue_pattern_lifecycle.md`."

## Lessons codified

1. Queue patterns are NOT inherently safe — they shift bug location from "ordering" to "lifecycle coverage"
2. Same surface bug PRs lez than 1 hour apart (PR #322 introduced queue + PR #325 fixed queue lifecycle) = signal for stricter spec checklist
3. Codex async catches what reviewer subagents miss (cross-file + cross-lifecycle blind spots)
4. Spec write-up should EXPLICITLY enumerate queue lifecycle events

Related: [[feedback-codex-post-cascade-audit]] [[feedback-peer-review-blocker-pattern]] [[project-p4-storytelling-cascade-2026-05-20]]
