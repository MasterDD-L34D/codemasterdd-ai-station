---
name: feedback-loc-sum-check
description: Pre-merge audit must sum LOC deltas of all PRs touching same file near cap (1000-LOC limit). Local content auto-merge clean ≠ structural cap preserved.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7c08f071-f7f8-4cf0-a16b-fcd6aba717fa
---

Pre-merge LOC sim ≠ post-stack invariant verify. When 2+ PRs touch the same large file near the 1000-LOC gdlint cap, sum each PR's `+LOC` deltas against current `main` HEAD LOC. Local `git merge --no-commit` clean ≠ resulting file under cap.

**Why:** 2026-05-20 cascade incident on `scripts/phone/phone_composer_view.gd`: PR #289 (P0-2, +9 LOC) + PR #292 (P1-1+P1-5, +13 LOC) each landed standalone at 1000 LOC exact. Sim-merge predicted CLEAN auto-merge. Post-stack actual = 1009 LOC. gdlint failed on subsequent #291 CI re-run, blocking pipeline. Hotfix #293 needed (comment compaction).

**How to apply:**
- Before executing merge cascade, run for each composer/main-cap-near file: `gh pr view <PR> --json files --jq '.files[] | select(.path | contains("<file>")) | .additions'` per touched PR; sum + check vs `wc -l <file>` + 1000 cap.
- If sum exceeds cap, hold one PR + helper-extract trim BEFORE cascade.
- Files known to live near cap on Godot-v2 main: `scripts/main.gd`, `scripts/phone/phone_composer_view.gd` (extraction pattern: `main_*.gd` + `composer_*.gd` static helper modules — see [[project-pr-284-cascade-closure]]).

Related: [[feedback-peer-review-blocker-pattern]] — peer review caught content BLOCKERS but missed this structural overflow.
