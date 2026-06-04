---
name: feedback-peer-review-blocker-pattern
description: Dispatch general-purpose peer-review agent on every Claude-authored PR batch BEFORE cascade execution. Catches semantic-inversion + state-leak BLOCKERS Claude self-misses.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7c08f071-f7f8-4cf0-a16b-fcd6aba717fa
---

Always dispatch independent general-purpose code-reviewer agent (or `engineering:code-review` skill) on Claude-authored PRs before merge cascade. Claude is poor self-critic on semantic inversion + production-vs-test build distinction + lambda capture lifetime.

**Why:** 2026-05-20 cascade pre-merge audit:
- Peer agent caught PR #289 BLOCKER: `_set_status(text, debug: bool = true)` default suppressed 30+ user-actionable errors in release builds (auth_expired, Connessione chiusa, send_intent fallito, Re-mint fallito). Claude flipped the semantic the wrong way — release default should be visible, debug=true should opt-in. Production users would have seen blank label on errors.
- Peer agent caught PR #292 BLOCKER A: P1-3 `OS.is_debug_build()` gate removed host recovery CTA from Cloudflare demo path. Spec premise ("post P0-3 TV deployment canonical") not yet validated — TV phase_change may silently fail (2026-05-05 smoke iter6 B-NEW-14 precedent). Without recovery CTA host stuck silently in production. Reverted to text-rename only.
- Peer agent caught PR #292 BLOCKER B: `tween.finished` lambda captured `tint_rect` Node without `is_instance_valid` guard — risk of firing on freed Node during rapid phase swaps.
- Total: 2 P0 BLOCKERS + 4 P2 nits surfaced in single peer-review pass cost ~227k token total.

**How to apply:**
- After self-impl + CI green + before any `gh pr merge`, dispatch peer-review agent.
- Prompt template: read-only review, list specific files + diff command, request punch-list (≤500 words) with severity + file:line + 1-sentence rationale.
- 2 parallel agents = OK for P0+P1 batches (single agent per ~3 PRs).
- Specifically scrutinize: defensive-default flip semantics, async lambda lifetime, gate-flag scope (release vs debug), state-leak invariants (server-vs-cache resolution).

Related: [[feedback-loc-sum-check]] — peer review caught content correctness but missed LOC overflow structural issue (different concern domain).
