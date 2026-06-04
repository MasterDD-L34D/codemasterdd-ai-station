---
name: feedback-verify-scope-packs
description: "Game/ runtime config (ai_profiles.yaml etc.) lives in packs/evo_tactics_pack/data/, OUTSIDE data/+apps/ — verify-before-build greps MUST include packs/ or you'll wrongly conclude a flag is unset."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 20c560cf-9e4c-416c-a419-e0a1881db0cc
---

When verifying whether a config flag / profile / balance value is set in the Game/ repo, grep `packs/` too — not just `data/` and `apps/backend/`. The canonical runtime config the backend actually loads is under `packs/evo_tactics_pack/data/balance/` (and siblings), NOT `data/core/...`.

**Why:** 2026-05-22 I declared the "M1 overlay bypasses Utility AI" gap MOOT — I grepped `use_utility_brain` in `data/` + `apps/backend/` and found nothing, concluded no profile enables utility brain. WRONG: `aiProfilesLoader.js` loads `path.resolve(__dirname,'..','..','..','..','packs/evo_tactics_pack/data/balance/ai_profiles.yaml')`, where `aggressive: use_utility_brain: true` (line 48). So aggressive Sistema units DO take the utility path → the gap was REAL. A parallel chip caught it + shipped the fix (Game/ #2376). My grep scope missed `packs/` twice. (Note: `ai_profiles_extended.yaml` in `data/core/ai/` is a DIFFERENT, non-loaded file — a decoy.)

**How to apply:** for any "is X configured / enabled?" verification in Game/, run the grep across `packs apps/backend data` (all three roots), and confirm WHICH file the loader actually reads (check the loader's resolved path) before trusting a negative result. A negative grep scoped to the wrong dir = a false "moot". Ground-truth the loader path, not just the obvious data dir.

Related: [[feedback-parallel-chip-overlap]] — the chip that caught this. Anti-pattern #8 family (ground-truth > surface); verify-before-build only works if the grep scope is right.
