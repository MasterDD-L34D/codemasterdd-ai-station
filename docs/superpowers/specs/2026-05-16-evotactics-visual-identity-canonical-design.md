# Design: Evo-Tactics Visual Identity Canonical Consolidation

**Date**: 2026-05-16
**Author**: Claude Code (auto-mode con metodo) + Eduardo (approval)
**Status**: DRAFT v2 (revised post 3-way vault reconciliation + gitignored-corpus synthesis; awaiting Eduardo spec review -> implementation)
**Approach**: A -- Unified Visual Identity master-index in vault (approved 2026-05-16)
**Brainstorming**: superpowers:brainstorming flow, HARD-GATE design approved pre-implementation

## Revision note (v2, 2026-05-16)

Eduardo requested a full 3-way vault-source reconciliation (Lenovo local +
origin/main + Ryzen source `C:/Users/VGit/Vault/`) and explicit inclusion of
the gitignored `_imported-2026-05-14/` corpus. Both done. The reconciliation
+ corpus synthesis materially corrected the v1 central thesis: the A/B model
is **asymmetric** (B production-mature, A design-rationale-only), not "two
equal co-active layers". See Reconciliation, Critical finding, and section 1
below.

### 3-way reconciliation result (read-only audit, sovereign boundary)

| Source | HEAD | State | Unique content |
|--------|------|-------|----------------|
| Ryzen `C:/Users/VGit/Vault` (backup source) | `c2a7b485` backup 04:28:42 | 109 commits, 3 uncommitted, auto-backup origin | ~1-2 mechanical backup commits ahead of origin; self-resolves next push |
| **origin/main (canonical)** | `4ab9db62` | OD-037 self-reconciliation DONE, U-4 obsidian MCP migration, 7/7 production | The reconciled canonical truth |
| Lenovo `C:/dev/vault-shared` | `ba115b08` | 1 ahead / 49 behind origin, 4 uncommitted | `ba115b08` OD-033 chatgpt-recovery provenance (10411 ins) -- unrelated to visual, NOT pushed |

**Canonical-for-this-task = origin/main.** Empirically verified: the 49
origin-ahead commits did **NOT touch any visual doc** (41-44, 00F,
30-UI_TV_IDENTITA) -- only machinations spec.json + playtest notes. Therefore
the earlier collection of the visual quartet on the Lenovo working tree is
**content-valid** (L-029 stale-state concern resolved for the visual scope).

**Re-verification (L-029 pre-action, 2026-05-16 ~05:00Z):** origin/main
advanced `4ab9db62` -> `d41c0120` via PR #17 (OD-032 chatgpt ingest), #18
(Game-repo reconcile), #19 (5-repo ecosystem audit) + backups.
Re-checked: **none of the new commits touched any visual doc OR the
Evo-Tactics subtree at all** -- canonical claim holds, strengthened across
n=2 verification windows. Additionally the Ryzen-ahead gap **self-resolved**:
former Ryzen HEAD `c2a7b485` is now merged into origin/main (Ryzen->origin
sync occurred); only the Lenovo `ba115b08` OD-033 divergence remains as an
Eduardo-mediated follow-up.

**Eduardo-mediated follow-ups (NOT codemasterdd actions, sovereign boundary):**
- Lenovo `ba115b08` (OD-033) is the only true Lenovo divergence -- evaluate
  PR-to-origin vs confirm origin's parallel OD-033/OD-037 lineage supersedes.
  Not a blocker for this task.
- Ryzen cannot fetch via non-interactive SSH (no credential tty) -- next
  Ryzen->origin push (Eduardo interactive) flushes the 1-2 backup commits.
  Mechanical, low risk.

### `_imported-2026-05-14/` corpus (1703 files, gitignored by design)

Rule `.gitignore:59 Spaces/**/_imported-2026-05-14/` (added in `ba115b08`)
deliberately excludes this corpus as "regenerable derived artifacts" -- it is
in **no git ref anywhere** (not Lenovo-committed, not origin, not Ryzen),
present only as local working-tree material. Inventory: analisi-protocolli-ui
220, ecosistemi-funzioni-generatore 131, giochi-tile-design 400,
gioco-design-evolution 952 = raw ChatGPT conversation dumps. Synthesized via
2 parallel Explore agents (read-only). It is **provenance/lineage, not a
canonical spec** -- 45 references it as a source-of-record, the canonical
extraction is the production pipeline + Ferrospora constants below.

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

### Critical finding (v2 corrected): asymmetric 2-direction split

- **Direction A** (vault 41-ART-DIRECTION + Game): "Naturalistic stylized
  pixel art" -- 32x32 sprite, 9-biome palette matrix, species silhouette
  language, TV-first. Scope: **world / sprite / gameplay layer**. **STATUS:
  design-rationale-ONLY.** The gitignored-corpus synthesis (1352 files
  sampled) found **zero** tile-sheet / palette-matrix / sprite-execution
  evidence; `giochi-tile-design/` is mislabeled (holds character concept art,
  not tiles). A exists as canonical intent, **not implemented**.
- **Direction B** (Game-Godot-v2 + corpus): "Ferrospora -- readable biopunk
  tactical diorama". Scope: **UI / HUD / shell layer**. **STATUS:
  production-mature.** Corpus surfaces a full undocumented pipeline: live
  asset path `/assets/ui/ferrospora/`, concrete constants (teal
  `58,205,229`; mycelium/purple `205,82,210`; bronze-gold `238,219,174`;
  dark ground `7,7,7`; ornate frame gold `245,225,170`), sigil color
  language (move=teal, attack=orange-red, defend=blue, spore/trait=purple,
  wait=gold, ritual=lime), PIL extraction + 6 actions x 4 states x 5 sizes =
  120-PNG state-variant generation, manifest + Godot mapping codex
  (`CODEX_CORE_ACTION_ICONS_V1.md`). None of this is in canonical 42/43/44.

**v1 thesis "A=content, B=container, two equal co-active layers" was
empirically wrong.** They do compose (sprites render inside Ferrospora
chrome) BUT the asymmetry is the real central finding: B is the implemented
canonical engine UI with a mature image-generation pipeline; A is
not-yet-implemented design intent. 45 must declare BOTH the composition rule
AND the implementation-status asymmetry, and must index the undocumented
Ferrospora image-gen pipeline (the de-facto answer to "how to manage image
generation", currently absent from 43-ASSET-SOURCING).

### Abandoned visual direction (design-evolution provenance)

Corpus documents a superseded decision: initial inner-circular-icon crop
(unstable, off-center, lost ornate border) -> **superseded by full-card crop
+ procedural state variants** ("la card conserva lo stile pittorico; la
cornice e parte dell'identita"). 45 records this so the rejection rationale
is not re-litigated.

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
One-paragraph: vault (origin/main) = rationale source-of-truth, Godot-v2 =
canonical engine impl, Game = legacy Vue3 archive. Two-layer model:
A=sprite/world (design-intent, NOT yet implemented), B=Ferrospora UI/shell
(production-mature, live pipeline). They compose (A inside B) but are
asymmetric in impl status.

## 1. Canonical hierarchy (the authoritative answer)
- vault Spaces/Dev/Evo-Tactics/core/ = DESIGN RATIONALE source-of-truth
  (the "why", legal framework, pillar hierarchy, decision lifecycle).
  Canonical state = **origin/main** (verified visual-quartet unchanged by
  the 49 origin-ahead commits).
- Game-Godot-v2 = CANONICAL ENGINE implementation (Ferrospora UI/shell layer
  B, production-mature, post-pivot 2026-04-29; future frontend)
- Game (Vue3) = LEGACY ARCHIVE (Sprint Impronta gameplay logic; visual
  impl superseded by Godot-v2 for shell, sprite layer still reference)
- `_imported-2026-05-14/` corpus = PROVENANCE/lineage only (gitignored
  regenerable raw ChatGPT dumps; canonical extraction = pipeline in 2b +
  constants). Not a spec, cited as source-of-record.
- **Impl-status caveat**: layer B implemented, layer A (pixel/world)
  design-rationale-only. The hierarchy answers "what is canonical" per
  layer AND flags A as not-yet-built.

## 2. Two-layer visual model (A+B, asymmetric)
| Layer | Direction | Spec source | Scope | Impl status |
|-------|-----------|-------------|-------|-------------|
| World / sprite | A naturalistic pixel | vault 41-ART-DIRECTION + Game generate_visual_assets.py | In-grid creatures, biome tiles, 32x32, palette matrix | **design-rationale ONLY, not implemented** |
| UI / HUD / shell | B Ferrospora biopunk | Godot-v2 FERROSPORA_* + cinzel.tres/tokens.gd + corpus pipeline | Action dock, panels, sigils, HUD chrome, menu | **production-mature (live `/assets/ui/ferrospora/` + Godot codex)** |
Composition rule: sprites (A) render INSIDE the Ferrospora-framed (B)
tactical board. A = content, B = container. They compose, NOT conflict --
BUT B is implemented and A is pending. 45 states the composition rule AND
the impl-status asymmetry explicitly so "where is the canonical X" never
returns a not-yet-built answer as if it shipped.

## 2b. Ferrospora image-generation pipeline (NEW canonical -- was undocumented)
The de-facto answer to "how is image generation managed" (absent from
43-ASSET-SOURCING). Promote to canonical:
- Master AI-generated sheet -> PIL full-card crop (NOT inner-circle, see
  abandoned-direction note) -> procedural state variants (normal/hover/
  selected/disabled) via glow/ring/grayscale layers -> 6 actions x 4 states
  x 5 sizes = 120 PNG -> manifest + `CODEX_CORE_ACTION_ICONS_V1.md` Godot map.
- Live path `/assets/ui/ferrospora/` is production-canonical.
- Constants (promote into 42-STYLE-GUIDE-UI or 45): teal `58,205,229`,
  mycelium/purple `205,82,210`, bronze-gold `238,219,174`, dark ground
  `7,7,7`, ornate frame gold `245,225,170`; sigil colors move=teal /
  attack=orange-red / defend=blue / spore-trait=purple / wait=gold /
  ritual=lime.

## 3. Single-source-per-topic map
| Topic | Authoritative spec | Repo location |
|-------|--------------------|---------------|
| Visual look mgmt | 41-ART-DIRECTION (world) + cinzel.tres/tokens.gd (UI) | vault core/ + Godot-v2 resources/themes + scripts/ui |
| Image generation | 43-ASSET-SOURCING (policy/sprites) + FERROSPORA_IMAGE_PIPELINE_DECISION_GUIDE (UI assets) | vault core/ + Godot-v2 docs/godot-v2/artstyle/ferrospora |
| Asset usage | 43-ASSET-SOURCING + CREDITS.md (sprite provenance) + FERROSPORA_FINAL_DROP_MANIFEST (UI assets) | Game + Godot-v2 |
| Overall + visual style | Pillar hierarchy (41 pillars 1-4) + visual-screen-bible (Ferrospora north star) | vault core/ + Godot-v2 |

## 4. Sub-spec authoritative links (link not copy -- zero drift)
Bulleted links to the 6 canonical sub-docs with 1-line "what it owns" each.

## 5. Known gaps / open decisions (consolidated from collection + corpus)
- **Direction A unimplemented**: no tile-sheet / palette-matrix / sprite
  execution exists (corpus confirms). 41-ART-DIRECTION is intent only.
- **Ecosystem->visual mapping gap**: generator bioma score 0-100 spectrum
  (Desert/Steppe/Forest/Rainforest/Anomalous) defined ecologically with NO
  sprite/asset/tile visual binding -- blocks Direction A worldgen.
- palette_master.ase file pending (43-ASSET-SOURCING blocker)
- rendering projection iso vs orthogonal unspecified in 41-AD (00F says
  2.5D iso, 44-HUD ASCII shows orthogonal; corpus adds NO evidence --
  remains unresolved, needs disambiguation)
- 43-ASSET-SOURCING does not document the live Ferrospora image-gen
  pipeline (section 2b) -- doc/impl drift to close
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
- A+B model stated WITH the impl-status asymmetry (B mature / A intent-only),
  not the v1 "two equal layers" framing
- Ferrospora image-gen pipeline + constants indexed (section 2b) -- the
  previously-undocumented de-facto image-generation answer
- 3-way reconciliation result recorded (canonical=origin/main; Lenovo OD-033
  + Ryzen backup-source noted as Eduardo-mediated follow-ups)
- `_imported-2026-05-14/` corpus cited as provenance (not duplicated)
- Canonical hierarchy unambiguous per layer
- Zero content duplication (links to sub-specs, no copy)
- Known gaps consolidated in one place
- Optimization pass applied + recorded
- Eduardo can answer "where is the canonical X?" for all 4 topics from
  this single doc, including impl-status for layer A
