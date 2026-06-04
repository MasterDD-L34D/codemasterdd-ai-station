---
name: gdlint max-public-methods=20 → split test files
description: GUT test files hitting >20 public test methods must split before lint passes
type: feedback
originSessionId: 585dba96-6d14-4988-ab48-b6cb8dcaf004
---
Default gdlint config in this repo enforces `max-public-methods=20` per class.

**Why:** Repo enforces gdlint clean as Definition of Done. GUT test files naturally accumulate methods — when crossing the threshold, lint fails CI.

**How to apply:**
- When authoring a new test suite, plan splits ahead: by feature area (e.g. `test_lifecycle_catalog.gd` for catalog API + `test_lifecycle_stage.gd` for predicates).
- When hitting the limit on existing file, split by orthogonal axis (catalog vs stage, base predicate vs integration, etc.) into a new test file with same `extends GutTest` boilerplate.
- Test fixtures (factory helpers like `_make_catalog`, `_spawn`) duplicate across split files — GUT test isolation is per-file. Copy or extract to a shared `_helpers.gd` only when reuse is significant.

Examples shipped:
- P.x split: `test_trait_catalog_ally.gd` from `test_trait_catalog.gd`.
- P.3 split: `test_lifecycle_catalog.gd` (14) + `test_lifecycle_stage.gd` (13) + `test_lifecycle_catalog_full.gd` (7).
