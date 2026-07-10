# Jules task -- GDScript doc-comment batch 38 (trio, comment-only)

Repo: MasterDD-L34D/Game-Godot-v2.

## Scope (3 files, comment-only additions, NO logic change, no behavior change)

Add GDScript `##` doc-comments to the public API of exactly THREE files:

- `scripts/combat/biome_pool_loader.gd`
- `scripts/combat/terrain_reactions.gd`
- `scripts/main_wound_helpers.gd`

This is a comment-only change: ZERO deletions, zero edits to any existing line,
no rename/reformat/reorder, no other file touched. Every line to add is given
verbatim below and is pre-verified (gdformat unchanged, gdlint clean, all lines
ASCII and <= 100 chars). Copy each line byte-identical at the exact anchor.

Placement rule (load-bearing): each `##` line/block goes IMMEDIATELY above its
anchor line, with NO blank line between the `##` block and the anchor. Existing
`#` comments above the anchor stay where they are (insert the `##` lines BELOW
them, directly against the anchor line).

## Edits -- scripts/combat/biome_pool_loader.gd (7 lines)

Directly above the line `class_name BiomePoolLoader` insert:

```
## Memoized static loader for biome_pools.json: pools array, pool entry by id, role templates.
## Cache is injectable for tests via set_pools(); a missing file degrades to an empty Array.
```

Directly above `static func load_all_pools(path: String = "") -> Array:` insert:

```
## Loads and memoizes the biome pools JSON; empty path falls back to DEFAULT_POOLS_PATH.
```

Directly above `static func get_pool_by_id(biome_id: String, path: String = "") -> Variant:` insert:

```
## Returns the full pool entry Dictionary for biome_id, or null when missing or id is empty.
```

Directly above `static func get_role_templates(biome_id: String, path: String = "") -> Array:` insert:

```
## Returns the role_templates Array for a biome; [] when the pool or templates are missing.
```

Directly above `static func reset_cache() -> void:` insert:

```
## Clears the memoized pools cache (test-only).
```

Directly above `static func set_pools(pools_array: Array) -> void:` insert:

```
## Injects a pools Array directly, bypassing file load (test/runtime hook).
```

## Edits -- scripts/combat/terrain_reactions.gd (4 lines)

Directly above the line `class_name TerrainReactions` insert:

```
## Maps encounter terrain_features to per-unit modifiers for the cell a unit stands on.
## Per-type defaults live in TYPE_REACTIONS; a per-cell defense_mod field overrides them.
```

Directly above `static func modifiers_for_position(pos: Vector2i, terrain_features: Array) -> Dictionary:` insert:

```
## Returns the modifier Dictionary for the terrain at pos; all-zero no-op when none is found.
```

Directly above `static func tick_units(units: Array, terrain_features: Array) -> Array:` insert:

```
## Batch variant: returns an Array of {unit_id, modifiers} pairs for units standing on terrain.
```

## Edits -- scripts/main_wound_helpers.gd (3 lines)

Directly above the line `class_name MainWoundHelpers` (first line of the file) insert:

```
## Static wound-stack helpers extracted from main.gd: severity label + UnitInfoPanel dict.
```

Directly above `static func compute_wound_severity_label(wounds: Array) -> int:` insert:

```
## Derives the ranked severity label from a wound stack: 0 none, 1 lieve, 2 grave, 3 critica.
```

Directly above `static func unit_to_panel_dict(unit: Unit, campaign_state: CampaignState) -> Dictionary:` insert:

```
## Builds the UnitInfoPanel dict for a Unit; wound fields default to 0 without a CampaignState.
```

## Constraints (strict)

- ONLY the three files above; ONLY the 14 `##` lines given, byte-identical.
- ZERO deletions (git diff must show 0 removed lines), zero touched existing lines.
- ASCII-only; every added line starts with `## ` and is <= 100 characters.
- Do NOT add doc-comments to private (`_`-prefixed) functions or anywhere else.
- Conventional Commit subject (lowercase), e.g.:
  docs(scripts): doc-comment batch 38 -- biome_pool_loader + terrain_reactions + main_wound_helpers

## Acceptance (verify before delivering)

- `git diff --numstat` -> exactly 3 files, +7/+4/+3 added lines, 0 deletions each.
- Every added line starts with `## ` and sits directly above its anchor with no
  blank line in between.
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
