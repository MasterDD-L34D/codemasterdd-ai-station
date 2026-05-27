---
name: prd-exists-read-first
description: The canonical PRD already exists (vault SoT v5) + a live Godot build overlay — read them before deriving design or build status; re-deriving was the recurring rework
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4eb11182-03d0-4fa5-a6fe-5a7a702271d9
---

The unified PRD/GDD EXISTS — stop re-deriving design and build-status each session (the recurring rework master-dd flagged 2026-05-25: "sembra che ogni volta riscriviamo cose già fatte").

**Where the truth lives:**
- **Design / "what is the game" / loop / Nido / mating / specie / Forme / narrative** → vault `/c/dev/vault/Spaces/Dev/Evo-Tactics/core/00-SOURCE-OF-TRUTH.md` ("Source of Truth Unificata v5", 1343 lines) + numbered `core/{01-VISIONE,02-PILASTRI,03-LOOP,17-SCREEN_FLOW,20-SPECIE_E_PARTI,22-FORME_BASE_16,27-MATING_NIDO}.md` + `90-FINAL-DESIGN-FREEZE.md` (28-card freeze) + GDD-master (16-card). All 28 GDD open-questions CLOSED (SoT §19). Loop = §23. Heir = §9/§21 + Q20 Pattern-B.
- **"Is it built in Godot v2?"** → `Game-Godot-v2/docs/godot-v2/PRD-BUILD-STATUS-GODOT-V2.md` (live overlay). **NOT SoT §13** — that build-map is web-v1, dated 2026-04-16, PRE the Godot pivot (2026-04-29) = stale.

**Why:** Re-investigating "what's built" + re-deriving design wasted whole sessions (e.g. 2026-05-25 R1 brainstorm re-discovered things already in the backend + already in SoT). SoT §9 itself diagnoses it: "il progetto è stato modularizzato e disperso".

**How to apply:**
- Design question → read SoT v5 + the relevant `core/NN-*.md` FIRST. Don't re-derive.
- "Is X built?" → read the overlay, not SoT §13.
- Ship a system → update its overlay row same PR.
- CLAUDE.md (both repos) now has a read-first PRD pointer at top.
- SoT is master-dd's vault canon — propose addendums (don't edit the vault unilaterally). See [[project-session-closure-2026-05-25]] for the pivot contradictions (hex/square, server/client combat, Colyseus/custom-WS, web/Godot frontend).
