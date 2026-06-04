---
name: Codex review pattern — bundle P1/P2 into next sprint PR
description: Codex bot reviews shipped PRs post-merge; user prefers fixes bundled rather than separate hotfix branches
type: feedback
originSessionId: 585dba96-6d14-4988-ab48-b6cb8dcaf004
---
Codex bot reviews PRs post-merge with P1 (blocker) / P2 (medium) tickets via GitHub PR comments.

**Why:** Codex feedback arrives on already-merged PRs — separate hotfix branches per ticket would create noise. User prefers consolidating fixes into the next sprint PR when files overlap, OR a small chore PR when the next sprint has no overlap.

**How to apply:**
- Sweep step #1 always queries `gh api repos/MasterDD-L34D/Game-Godot-v2/pulls/<N>/comments --jq '.[].body'` for each recently-merged PR.
- If next sprint touches the same files → bundle codex fix in same PR + reference codex ticket in commit body (`Codex PR #NN P1 fix: ...`).
- If next sprint is orthogonal → standalone chore PR like `sprint/codex-pNN-fix-summary` with same `feat()` or `fix()` semver.
- Track bundled fixes in PR body under "Codex review fixes bundled" section.

Examples shipped:
- PR #33 (P.2): bundled 2× P1 from PR #30 + 1× P1 from PR #31.
- Standalone codex chore (post P.3): `_status_string_to_enum` disoriented mapping fix from PR #33 codex P2.
