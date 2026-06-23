# Design: Evo-Tactics Visual Identity Canonical Consolidation

> **Status (2026-06-23):** shipped-partial -- canonical index + collection done; production art-swap not shipped; shell layer superseded by Godot-v2

**Date**: 2026-05-16
**Author**: Claude Code (auto-mode con metodo) + Eduardo (approval)
**Status**: DRAFT v3 (v2 + harsh-reviewer REWORK applied: P0 index/canonical contradiction resolved, P1a Direction-A claim corrected via repo audit, P1b direct content-validity proof; awaiting Eduardo spec review -> implementation)
**Approach**: A -- Unified Visual Identity master-index in vault (approved 2026-05-16)
**Brainstorming**: superpowers:brainstorming flow, HARD-GATE design approved pre-implementation
**Review**: Protocol 5 harsh-reviewer subagent (governance-class pre-gate) -- verdict REWORK, 1 P0 + 2 P1 + 4 P2, all addressed in v3

## Revision note (v3, 2026-05-16)

v2 ran a 3-way vault reconciliation (Lenovo/origin/Ryzen) + gitignored
`_imported-2026-05-14/` corpus synthesis. v3 then applied a harsh-reviewer
pass that caught three load-bearing defects:

- **P0**: v2 was a self-contradiction -- "pure index, zero duplication" while
  section 2b promoted NEW canonical content (Ferrospora constants/pipeline)
  into 45. Resolved: 45 stays a pure index; constants -> 42-STYLE-GUIDE-UI,
  pipeline -> 43-ASSET-SOURCING as a **separate Eduardo-gated follow-up**, 45
  only links them.
- **P1a**: "Direction A not implemented" was absence-of-evidence overreach
  (the corpus is UI-skewed ChatGPT exports; it cannot contain a sprite
  generator). Repo audit of `C:/dev/Game` + `C:/dev/Game-Godot-v2`
  corrected it to **partially scaffolded** (generator + palette matrix run;
  Godot TileMap wired; pipeline orphaned). Projection **resolved** =
  orthogonal (confirmed in Godot code), not an open gap.
- **P1b**: content-validity rested on an indirect two-empty-logs argument;
  replaced with a direct `git diff origin/main -- <6 paths>` proof.

Net corrected thesis: A and B are **asymmetric in maturity** (B
production-mature; A scaffolded-but-orphaned), they compose (A inside B).

### 3-way reconciliation result (read-only audit, sovereign boundary)

(audit results = verified facts; the only prediction is explicitly marked)

| Source | HEAD | State | Unique content |
|--------|------|-------|----------------|
| Ryzen `C:/Users/VGit/Vault` (backup source) | `c2a7b485` -> now merged | RESOLVED: former Ryzen HEAD `c2a7b485` confirmed merged into origin/main on re-verify | none outstanding (gap closed, verified) |
| **origin/main (canonical)** | `d41c0120` (was `4ab9db62`) | OD-037 self-reconciled, U-4 obsidian MCP, +PR#17/#18/#19 since | The reconciled canonical truth |
| Lenovo `C:/dev/vault-shared` | `ba115b08` | 1 ahead / 49+ behind origin, 4 uncommitted (none in the 6 visual paths -- verified) | `ba115b08` OD-033 chatgpt-recovery (10411 ins) -- 0 Evo-Tactics paths, NOT pushed |

**Canonical-for-this-task = origin/main.** Content-validity proven
**directly** (P1b fix -- replaces the prior indirect log argument):
`git diff origin/main -- <6 visual paths>` = **EMPTY** (Lenovo working-tree
copies are byte-identical to origin/main) + `git status --porcelain
-- <6 paths>` = **EMPTY** (no uncommitted change to any of the 6) +
`ba115b08` touches **zero** Evo-Tactics paths. The collected visual quartet
== canonical. (L-029 stale-state concern resolved by direct diff, not
inference.)

**Re-verification (L-029 pre-action, 2026-05-16 ~05:00Z):** origin/main
advanced `4ab9db62` -> `d41c0120` via PR #17 (OD-032 chatgpt ingest), #18
(Game-repo reconcile), #19 (5-repo ecosystem audit) + backups.
Re-checked: **none of the new commits touched any visual doc OR the
Evo-Tactics subtree at all** -- canonical claim holds, strengthened across
n=2 verification windows. Additionally the Ryzen-ahead gap **self-resolved**:
former Ryzen HEAD `c2a7b485` is now merged into origin/main (Ryzen->origin
sync occurred); only the Lenovo `ba115b08` OD-033 divergence remains as an
Eduardo-mediated follow-up.

**Eduardo-mediated follow-up (NOT a codemasterdd action, sovereign boundary):**
- Lenovo `ba115b08` (OD-033) is now the **only** outstanding divergence
  (Ryzen gap self-resolved, verified). Evaluate PR-to-origin vs confirm
  origin's parallel OD-033/OD-037 lineage supersedes. Not a task blocker.

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

### Critical finding (v3, repo-audited): asymmetric-maturity 2-direction split

The corpus is UI-skewed ChatGPT exports -- it **cannot** contain sprite-gen
code, so "no A evidence in corpus" was scoped to the actual repos (P1a fix):

- **Direction A** (vault 41-ART-DIRECTION + Game + Godot-v2): "Naturalistic
  stylized pixel art" -- 32x32 sprite, 9-biome palette matrix, species
  silhouette. Scope: **world / sprite / gameplay layer**. **STATUS:
  partially scaffolded (NOT "not implemented").** Repo audit found
  `C:/dev/Game/tools/py/generate_visual_assets.py` actively generates
  32x32 indexed-PNG tiles (9 biomes x 3 = 27) + hardcoded 9-biome palette
  matrix + 64x64 creature silhouette sprites (8 archetypes) + 16 portraits.
  Godot-v2 has TileMap wired (`Main.tscn` GroundTileMap + 5 tileset `.tres`).
  **Gap**: procedural assets NOT bridged into the Godot build (legacy 16x16
  tilesets still loaded); production art-swap (Kenney/AI) not shipped. So:
  generator + palette real and runnable, authoring pipeline orphaned.
  Bounded scope of claim: `C:/dev/Game` + `C:/dev/Game-Godot-v2` as of
  2026-05-16.
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

**Projection RESOLVED** (was listed as an open gap): orthogonal, confirmed
in Godot code (`Main.gd` Camera2D zoom 2.0, no isometric shear/offset).

**v1 thesis "A=content, B=container, two equal co-active layers" was
imprecise.** They compose (A sprites render inside B Ferrospora chrome) but
are **asymmetric in maturity**: B = implemented canonical engine UI with a
mature image-gen pipeline; A = design + generator scaffolded, build
integration orphaned. 45 declares the composition rule + the maturity
asymmetry, and **points to** (does not host) the undocumented Ferrospora
pipeline whose canonical home is 43-ASSET-SOURCING (see P0 resolution).

### Abandoned visual direction (design-evolution provenance)

Corpus documents a superseded decision: initial inner-circular-icon crop
(unstable, off-center, lost ornate border) -> **superseded by full-card crop
+ procedural state variants** ("la card conserva lo stile pittorico; la
cornice e parte dell'identita"). 45 records this so the rejection rationale
is not re-litigated.

## Decision

Create a **master-index canonical doc** in vault as capstone of the existing
visual quartet (41-44), reconciling A+B and declaring canonical hierarchy
WITHOUT duplicating sub-spec content (link, not copy). 45 hosts **no new
spec content** -- it is strictly an index + the one reconciliation/hierarchy
fact no sub-doc owns.

### P0 resolution: where the corpus-derived content actually lives

The Ferrospora constants + image-gen pipeline are NEW canonical content, not
index material. Putting them in 45 would make 45 a spec (and break "zero
drift via link-not-copy" the moment Godot edits a palette). So they go to
their natural owners as a **separate, separately-Eduardo-gated follow-up
workstream** (NOT part of the 45 deliverable):

- Ferrospora color/sigil constants -> **42-STYLE-GUIDE-UI** (already owns UI
  tokens)
- Ferrospora image-gen pipeline + `/assets/ui/ferrospora/` + state-variant
  workflow -> **43-ASSET-SOURCING** (already owns asset sourcing/generation)

45 only **links** to 42/43 for these. This follow-up = 2 additional
sovereign vault writes, scoped + authorized separately from 45. Until it
lands, 45's link target notes "pipeline doc-capture pending (follow-up)".

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
A=sprite/world (generator+palette scaffolded, build integration orphaned),
B=Ferrospora UI/shell (production-mature, live pipeline). They compose
(A renders inside B) but are asymmetric in maturity. Projection=orthogonal.

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
  regenerable raw ChatGPT dumps). Not a spec, cited as source-of-record;
  its canonical extraction lands in 43/42 (follow-up), not 45.
- **Maturity caveat**: layer B production-mature; layer A scaffolded
  (generator + palette run) but build-integration orphaned. The hierarchy
  answers "what is canonical" per layer AND flags A's orphaned-pipeline
  status so no one reads "A canonical" as "A shipped".

## 2. Two-layer visual model (A+B, asymmetric)
| Layer | Direction | Spec source | Scope | Impl status |
|-------|-----------|-------------|-------|-------------|
| World / sprite | A naturalistic pixel | vault 41-ART-DIRECTION + `Game/tools/py/generate_visual_assets.py` | In-grid creatures, biome tiles, 32x32, palette matrix | **scaffolded: generator+palette run; Godot-build bridge orphaned** |
| UI / HUD / shell | B Ferrospora biopunk | Godot-v2 FERROSPORA_* + cinzel.tres/tokens.gd | Action dock, panels, sigils, HUD chrome, menu | **production-mature (live `/assets/ui/ferrospora/` + Godot codex)** |
Composition rule: A sprites render INSIDE the B Ferrospora-framed tactical
board -- A is the contained sprite layer (scaffolded), B the container shell
(mature). They compose, not conflict; the asymmetry is maturity, not role.
45 states the composition rule + the maturity asymmetry so "where is
canonical X" never returns a scaffolded-but-orphaned answer as if shipped.

## 2b. Ferrospora pipeline -- INDEX POINTER ONLY (content lives in 43/42)
45 does NOT host the pipeline/constants (P0). It records the *pointer* +
the discovered-gap fact:
- "How is image generation managed" -> canonical home **43-ASSET-SOURCING**
  (follow-up will capture: AI master sheet -> PIL full-card crop ->
  procedural state variants -> 6x4x5=120 PNG -> manifest +
  `CODEX_CORE_ACTION_ICONS_V1.md`; live path `/assets/ui/ferrospora/`).
- Ferrospora color/sigil constants -> canonical home **42-STYLE-GUIDE-UI**
  (follow-up captures the RGB + sigil-color table).
- 45 states only: "this pipeline exists, is production-canonical, and was
  undocumented as of 2026-05-16; capture tracked as follow-up to 43/42."
  No RGB values, no pipeline steps duplicated in 45.

## 3. Single-source-per-topic map
| Topic | Authoritative spec | Repo location |
|-------|--------------------|---------------|
| Visual look mgmt | 41-ART-DIRECTION (world) + cinzel.tres/tokens.gd (UI) | vault core/ + Godot-v2 resources/themes + scripts/ui |
| Image generation | 43-ASSET-SOURCING (policy/sprites) + FERROSPORA_IMAGE_PIPELINE_DECISION_GUIDE (UI assets) | vault core/ + Godot-v2 docs/godot-v2/artstyle/ferrospora |
| Asset usage | 43-ASSET-SOURCING + CREDITS.md (sprite provenance) + FERROSPORA_FINAL_DROP_MANIFEST (UI assets) | Game + Godot-v2 |
| Overall + visual style | Pillar hierarchy (41 pillars 1-4) + visual-screen-bible (Ferrospora north star) | vault core/ + Godot-v2 |

## 4. Sub-spec authoritative links (link not copy -- zero drift)
Bulleted links to the 6 canonical sub-docs with 1-line "what it owns" each.

## 5. Known gaps / open decisions (consolidated, repo-audited)
- **Direction A build-integration orphaned** (NOT "unimplemented"):
  `generate_visual_assets.py` produces 32x32 tiles + palette, but Godot-v2
  still loads legacy 16x16 tilesets; no Game->Godot asset bridge. Real gap
  = the integration step, not the generator.
- **Ecosystem->visual mapping gap**: generator bioma score 0-100 spectrum
  defined ecologically with NO sprite/asset/tile visual binding.
- palette_master.ase file pending (43-ASSET-SOURCING blocker)
- 43-ASSET-SOURCING / 42-STYLE-GUIDE-UI do not yet document the live
  Ferrospora pipeline/constants -- doc/impl drift; P0 follow-up closes it
- typography v2 (Cinzel/IM Fell/VT323) partial in Game Vue3 (apps/play only)
- design-log underpopulated (no visual milestone entries)
- audio direction placeholder DRAFT (out of visual scope, noted for parity)

(RESOLVED, no longer a gap: projection iso-vs-orthogonal -> orthogonal,
confirmed in Godot `Main.gd` Camera2D zoom 2.0, no shear.)
```

(Optimization-pass is a PR checklist, NOT a section baked into the canonical
vault doc -- removed from 45's structure to keep the artifact reader-facing,
not process-facing. See "Optimization pass plan" below.)

## Architecture / isolation

**45 deliverable**: single new file, pure index/reconciliation, zero
modification of the 6 sub-specs, zero new spec content. 45 answers "what is
canonical and how do the pieces relate"; sub-specs answer "the detailed
spec for X".

**Separate follow-up workstream** (NOT in the 45 deliverable, separately
Eduardo-gated): capture Ferrospora pipeline -> 43-ASSET-SOURCING + constants
-> 42-STYLE-GUIDE-UI (2 additional sovereign vault writes). This is the only
content that modifies existing sub-specs; isolating it keeps 45 a clean
index and the zero-duplication guarantee literally true.

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

- NOT modifying 41/42/43/44 content **in the 45 deliverable** (the 42/43
  capture is a separate, separately-gated follow-up -- see Architecture)
- NOT creating Godot-v2 pointer doc (Approach C rejected -- over-engineered)
- NOT resolving open gaps (palette_master, ecosystem->visual binding,
  Game->Godot asset bridge) -- 45 DOCUMENTS them; resolution is future work
- NOT auditing beyond `C:/dev/Game` + `C:/dev/Game-Godot-v2` for Direction-A
  (claim bounded to that scope as of 2026-05-16)
- NOT touching Game-Database (negligible visual material)

## Success criteria

- 45-VISUAL-IDENTITY-CANONICAL.md exists in vault core/, frontmatter
  consistent with 41-44 siblings
- A+B model stated WITH the maturity asymmetry (B mature / A scaffolded-
  orphaned, repo-audited bounded claim), not the v1 "two equal layers"
- Ferrospora pipeline/constants **pointed to** (43/42 as canonical home),
  NOT hosted in 45 -- zero-duplication guarantee literally true
- 3-way reconciliation recorded (canonical=origin/main d41c0120; Ryzen gap
  self-resolved verified; Lenovo OD-033 = sole Eduardo-mediated follow-up)
- `_imported-2026-05-14/` corpus cited as provenance (not duplicated)
- Canonical hierarchy unambiguous per layer
- Zero content duplication -- now literally true (P0 resolved: no constants
  /pipeline copied into 45)
- Known gaps consolidated; projection gap closed (orthogonal)
- harsh-reviewer P0+2xP1 resolved, 4xP2 addressed (recorded in revision note)
- Eduardo can answer "where is canonical X?" for all 4 topics from this doc,
  including the bounded maturity status of layer A
