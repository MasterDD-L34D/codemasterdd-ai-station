---
name: evo-roadmap-2026-05-26-stale
description: "evo-state-roadmap-2026-05-26 surface-dead inventory is ~1 month stale — most 'engine live/surface dead' systems already shipped in Game/ git; ground-truth before acting on its verdicts"
metadata: 
  node_type: memory
  type: project
  originSessionId: 35045b88-61f0-4361-8d7f-40b54ba9be7c
---

`Spaces/Dev/Evo-Tactics/evo-state-roadmap-2026-05-26.md` describes a "ENGINE LIVE, SURFACE DEAD" pattern across 8 runtime systems (mating, objectiveEvaluator, biomeSpawnBias, QBN 17 events, briefingVariations, Thought Cabinet 18, isTurnLimit, threatPreview) and treats them as pending work. **This inventory is stale by ~1 month.**

Ground-truth from `C:/dev/Game` git (verified 2026-05-27): the §C.2 Surface-DEAD sweep was **7/8 closed by 2026-04-28** (PR #1988). Only residuo = #3 Spore mutation dots (~15h external authoring). Specifically OD-001 V3 Mating surface wire SHIPPED late April: #1844 (frontend MVP) + #1879 (backend re-apply, supersedes #1877 closed-unmerged) + #1988 (Sprint 12 lifecycle, §C.2 #4 → 🟢).

**Why this happened:** the roadmap-2026-05-26 (a vault Claude session) appears to have inherited the surface-dead framing from the V2-inspect Drive audit (`Sources/raw/gdrive-evo/Evo_V2_inspect_vision_spec_gap.md`) without ground-truthing Game/ git. A later session (2026-05-27) then formalized it into a vault ADR + OD-001 record + PILLARS_STATUS that were stale-on-arrival (anti-pattern #19 cascade: stale roadmap → stale ADR). Corrected in commit `d9188dc1b`.

**How to apply:** before acting on ANY "surface dead / pending wire / PR N/M" verdict from roadmap-2026-05-26 (or the V2-inspect source), VERIFY current `C:/dev/Game` git state first (`gh pr list --search "<feature> in:title" --state all` + grep `apps/play/src`). Note: the canonical Game/ repo on Ryzen is `C:/dev/Game` (NOT `C:/Users/VGit/Desktop/Game` — that path appears in old docs but doesn't exist). `PILLARS_STATUS.md` was corrected and is now more trustworthy than the roadmap; trust git over both. See [[fleet-pc-identity]].
