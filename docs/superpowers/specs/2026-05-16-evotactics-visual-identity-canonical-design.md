# Design: Evo-Tactics Visual Identity Canonical Consolidation

**Date**: 2026-05-16
**Author**: Claude Code (auto-mode con metodo) + Eduardo (approval)
**Status**: DRAFT (awaiting Eduardo spec review -> implementation)
**Approach**: A -- Unified Visual Identity master-index in vault (approved 2026-05-16)
**Brainstorming**: superpowers:brainstorming flow, HARD-GATE design approved pre-implementation

## Problem

Evo-Tactics visual identity material is scattered across 3 repos with a
critical unreconciled finding: TWO parallel visual directions exist with no
document stating their canonical relationship.

### Collection synthesis (P2 autoresearch, 3 parallel Explore agents, read-only)

| Source | Material | Nature |
|--------|----------|--------|
| vault `Spaces/Dev/Evo-Tactics/core/` | 41-ART-DIRECTION + 42-STYLE-GUIDE-UI + 43-ASSET-SOURCING + 44-HUD-LAYOUT-REFERENCES + 00F-ART_AUDIO_BUSINESS + ADR-2026-04-18 (art-direction + zero-cost) + ADR-2026-04-26 (m15-coop-ui) | Design rationale source-of-truth (why + legal + pillar hierarchy + biome mood mapping + decision lifecycle) |
| Game (Vue3) `docs/core/41-43` | Mirror of vault docs + CSS tokens (theme.css, evogene-deck.css) + generate_visual_assets.py + CREDITS.md | Legacy Vue3 impl + provenance (sprite/world layer) |
| Game-Godot-v2 `docs/godot-v2/artstyle/ferrospora/` | FERROSPORA prompt library + image pipeline + AI handoff + final-drop manifest + theme hierarchy (cinzel.tres + tokens.gd + biome_palette.gd) + visual-screen-bible + ui-design-illuminator agent | Canonical engine UI/shell (post-pivot 2026-04-29, "biopunk tactical diorama") |
| Game-Database | 5 files (dashboard CRUD theme) | Negligible -- excluded |

### Critical finding: 2 unreconciled visual directions

- **Direction A** (vault + Game): "Naturalistic stylized pixel art" -- 32x32
  sprite, 9-biome palette matrix, species silhouette language, TV-first.
  Scope: **world / sprite / gameplay layer**.
- **Direction B** (Game-Godot-v2): "Ferrospora -- readable biopunk tactical
  diorama" -- dark bronze / mycelium / teal spore glow, ornate sigil UI,
  cinzel parchment theme. Scope: **UI / HUD / shell layer**.

Not inherently contradictory (A = in-world sprites, B = UI chrome) BUT no
document declares the hierarchy or how they compose. This is the central gap.

## Decision

Create a **master-index canonical doc** in vault as capstone of the existing
visual quartet (41-44), reconciling A+B and declaring canonical hierarchy
WITHOUT duplicating sub-spec content (link, not copy).

### File

`vault-shared/Spaces/Dev/Evo-Tactics/core/45-VISUAL-IDENTITY-CANONICAL.md`

(Slot `40` is taken by ROADMAP; the visual cluster is 41-44; `45` is the
natural capstone/index extending the sequence. Marked `source_of_truth: true`,
`doc_owner: Eduardo`, frontmatter consistent with sibling 41-44 docs.)

### Document structure

```
# 45 -- Visual Identity Canonical (master index)
[frontmatter: source_of_truth true, status active, review_cycle 90d,
 supersedes: scattered-cross-repo, related: 41/42/43/44 + Ferrospora]

## TL;DR
One-paragraph: vault = rationale source-of-truth, Godot-v2 = canonical
engine impl, Game = legacy Vue3 archive. Two-layer model: A=sprite/world,
B=Ferrospora UI/shell. They compose, not conflict.

## 1. Canonical hierarchy (the authoritative answer)
- vault Spaces/Dev/Evo-Tactics/core/ = DESIGN RATIONALE source-of-truth
  (the "why", legal framework, pillar hierarchy, decision lifecycle)
- Game-Godot-v2 = CANONICAL ENGINE implementation (Ferrospora UI/shell,
  post-pivot 2026-04-29; future frontend)
- Game (Vue3) = LEGACY ARCHIVE (Sprint Impronta gameplay logic; visual
  impl superseded by Godot-v2 for shell, sprite layer still reference)

## 2. Two-layer visual model (A+B reconciliation)
| Layer | Direction | Spec source | Scope |
|-------|-----------|-------------|-------|
| World / sprite | A naturalistic pixel | vault 41-ART-DIRECTION + Game generate_visual_assets.py | In-grid creatures, biome tiles, 32x32, palette matrix |
| UI / HUD / shell | B Ferrospora biopunk | Godot-v2 FERROSPORA_* + cinzel.tres/tokens.gd | Action dock, panels, sigils, HUD chrome, menu |
Composition rule: sprites (A) render INSIDE the Ferrospora-framed (B)
tactical board. A = content, B = container. Both active, distinct layers.

## 3. Single-source-per-topic map
| Topic | Authoritative spec | Repo location |
|-------|--------------------|---------------|
| Visual look mgmt | 41-ART-DIRECTION (world) + cinzel.tres/tokens.gd (UI) | vault core/ + Godot-v2 resources/themes + scripts/ui |
| Image generation | 43-ASSET-SOURCING (policy/sprites) + FERROSPORA_IMAGE_PIPELINE_DECISION_GUIDE (UI assets) | vault core/ + Godot-v2 docs/godot-v2/artstyle/ferrospora |
| Asset usage | 43-ASSET-SOURCING + CREDITS.md (sprite provenance) + FERROSPORA_FINAL_DROP_MANIFEST (UI assets) | Game + Godot-v2 |
| Overall + visual style | Pillar hierarchy (41 pillars 1-4) + visual-screen-bible (Ferrospora north star) | vault core/ + Godot-v2 |

## 4. Sub-spec authoritative links (link not copy -- zero drift)
Bulleted links to the 6 canonical sub-docs with 1-line "what it owns" each.

## 5. Known gaps / open decisions (consolidated from collection)
- palette_master.ase file pending (43-ASSET-SOURCING blocker)
- rendering projection iso vs orthogonal unspecified in 41-AD (00F says
  2.5D iso, 44-HUD ASCII shows orthogonal -- needs disambiguation)
- typography v2 (Cinzel/IM Fell/VT323) partial in Game Vue3 (apps/play only)
- design-log underpopulated (no visual milestone entries)
- audio direction placeholder DRAFT (out of visual scope, noted for parity)

## 6. Optimization pass record
Post-draft: P2 autoresearch cross-validation + superpowers
writing-clearly-and-concisely skill applied + structure self-review.
```

## Architecture / isolation

Single new file, pure index/reconciliation. Zero modification of the 6
existing sub-specs (they remain authoritative for their domain; 45 only
indexes + declares hierarchy + adds the A+B reconciliation that none of
them currently own). Clear boundary: 45 answers "what is canonical and how
do the pieces relate"; sub-specs answer "the detailed spec for X".

## Privacy / boundary (CRITICAL)

vault-shared is **sovereign-only sibling-peer**. codemasterdd has NO
default write-path. Per L-2026-05-012 ("vault sibling-peer write under
explicit authorization") + feedback_external_repo_action_boundary:

- Collection phase: **read-only** (DONE, compliant)
- This design spec: written to **codemasterdd** docs/superpowers/specs/
  (my repo, no boundary issue)
- The vault write (creating 45-VISUAL-IDENTITY-CANONICAL.md): requires
  **explicit Eduardo per-task authorization**. The brainstorming
  "user reviews spec" gate IS this authorization checkpoint. Implementation
  proceeds ONLY after Eduardo explicitly approves this spec + the vault write.

## Optimization pass plan (post-vault-write)

1. P2 autoresearch cross-validate: re-read 45 vs the 6 sub-specs for
   contradiction / drift (internal > external weighting)
2. superpowers `elements-of-style:writing-clearly-and-concisely` skill on
   45 prose (clarity/concision)
3. Optional gsd (get-shit-done) structure check IF Eduardo wants the
   deeper agent pass -- bookmark reference only unless requested
4. Vault commit Eduardo-mediated (sovereign push discipline)

## Out of scope (YAGNI)

- NOT modifying 41/42/43/44 content (they stay authoritative)
- NOT creating Godot-v2 pointer doc (Approach C rejected -- over-engineered
  double-write friction now; can add later if cross-nav friction emerges)
- NOT resolving the open gaps (palette_master, iso-vs-ortho) -- 45 DOCUMENTS
  them as known open decisions, resolution is separate future work
- NOT touching Game-Database (negligible visual material)

## Success criteria

- 45-VISUAL-IDENTITY-CANONICAL.md exists in vault core/, frontmatter
  consistent with 41-44 siblings
- A+B two-layer reconciliation explicitly stated (the central gap closed)
- Canonical hierarchy (vault=rationale / Godot-v2=engine / Game=legacy)
  unambiguous
- Zero content duplication (links to sub-specs, no copy)
- Known gaps consolidated in one place (was scattered across collection)
- Optimization pass applied + recorded
- Eduardo can answer "where is the canonical X?" for all 4 topics from
  this single doc
