# Jules task -- backport encounter enrichments into YAML sources (Game issue #2744)

Repo: MasterDD-L34D/Game.

## Scope (6 files, mechanical additive edits, NO behavior change, no logic change)

Backport hand-authored dataset enrichments from the Godot frontend dataset
(`Game-Godot-v2/data/encounters/encounters.json`) into the YAML sources of this
repo, EXACTLY as specified below. Every edit is value-additive: you either
insert one new line, or rewrite one inline mapping line by inserting two new
keys in the middle of it. ZERO other changes: no key deleted, no value changed,
no reordering, no reformatting, no comment touched, no rename/refactor.

The exact edits below are pre-verified green (AJV schema validation 19/19 +
full ETL dataset regen reproduces the committed Godot dataset enrichments).
Apply them character-for-character.

## Edit list (apply ALL of these, and NOTHING else)

### 1. data/encounters/elite_01.yaml

Insert one new line directly below the line `difficulty: boss`:

```yaml
pressure_tier_floor: 3
```

Rewrite these three lines in `grid.terrain_features` (each keeps its original
content with only `terrain_type` + `elevation` inserted between `type` and
`defense_mod`):

- before: `    - { x: 3, y: 3, type: lava, defense_mod: -1 }`
- after:  `    - { x: 3, y: 3, type: lava, terrain_type: cinder, elevation: -1, defense_mod: -1 }`

- before: `    - { x: 2, y: 1, type: roccia, defense_mod: 2 }`
- after:  `    - { x: 2, y: 1, type: roccia, terrain_type: stone, elevation: 2, defense_mod: 2 }`

- before: `    - { x: 4, y: 5, type: roccia, defense_mod: 2 }`
- after:  `    - { x: 4, y: 5, type: roccia, terrain_type: stone, elevation: 2, defense_mod: 2 }`

### 2. data/encounters/enc_savana_pack_clash.yaml

Insert one new line directly below the line `difficulty: hardcore`:

```yaml
pressure_tier_floor: 4
```

Rewrite these five lines in `grid.terrain_features`:

- before: `    - { x: 2, y: 4, type: vegetazione_densa, defense_mod: 2 }`
- after:  `    - { x: 2, y: 4, type: vegetazione_densa, terrain_type: forest, elevation: 0, defense_mod: 2 }`

- before: `    - { x: 7, y: 6, type: vegetazione_densa, defense_mod: 2 }`
- after:  `    - { x: 7, y: 6, type: vegetazione_densa, terrain_type: forest, elevation: 0, defense_mod: 2 }`

- before: `    - { x: 5, y: 8, type: roccia, defense_mod: 2 }`
- after:  `    - { x: 5, y: 8, type: roccia, terrain_type: stone, elevation: 1, defense_mod: 2 }`

- before: `    - { x: 3, y: 2, type: duna, defense_mod: 1 }`
- after:  `    - { x: 3, y: 2, type: duna, terrain_type: none, elevation: 1, defense_mod: 1 }`

- before: `    - { x: 8, y: 1, type: duna, defense_mod: 1 }`
- after:  `    - { x: 8, y: 1, type: duna, terrain_type: none, elevation: 1, defense_mod: 1 }`

### 3. data/encounters/standard_01.yaml

Insert one new line directly below the line `difficulty: standard`:

```yaml
pressure_tier_floor: 2
```

Rewrite these three lines in `grid.terrain_features`:

- before: `    - { x: 2, y: 2, type: roccia, defense_mod: 2 }`
- after:  `    - { x: 2, y: 2, type: roccia, terrain_type: stone, elevation: 1, defense_mod: 2 }`

- before: `    - { x: 4, y: 3, type: roccia, defense_mod: 2 }`
- after:  `    - { x: 4, y: 3, type: roccia, terrain_type: stone, elevation: 1, defense_mod: 2 }`

- before: `    - { x: 1, y: 4, type: vegetazione_densa, defense_mod: 2 }`
- after:  `    - { x: 1, y: 4, type: vegetazione_densa, terrain_type: forest, elevation: 0, defense_mod: 2 }`

### 4. data/encounters/tutorial_01.yaml

Insert one new line directly below the line `difficulty: tutorial`:

```yaml
pressure_tier_floor: 1
```

No other change in this file.

### 5. docs/planning/encounters/enc_caverna_02.yaml

In the top-level `conditions:` list (NOT `objective.loss_conditions`), append a
third entry directly below the line `    effect: echo_feedback`:

```yaml
  - type: lethal
```

No other change in this file.

### 6. schemas/evo/encounter.schema.json

In the `conditions` items `type` enum, add `"lethal"` as the LAST enum value:

- before:
```json
              "environmental_mutation"
```
- after:
```json
              "environmental_mutation",
              "lethal"
```

No other change in this file.

## Constraints (strict)

- Touch ONLY the 6 files listed above. ASCII-only additions (all content above
  is pure ASCII -- keep it that way).
- Zero value-level deletions: every rewritten line keeps its full original
  content with only the two new keys inserted. No other line of any file
  changes. Do NOT re-indent, do NOT convert flow mappings to block style.
- Do NOT regenerate any JSON dataset, do NOT touch tests, configs, lockfiles,
  package.json, or any other file.
- Conventional Commit subject (lowercase), e.g.:
  fix(encounters): backport godot dataset enrichments into yaml sources (#2744)

## Acceptance (verify before delivering)

- `git diff --stat` -> exactly 6 files changed, no new files.
- Every `-` line in the diff reappears as a `+` line with only
  `terrain_type: <v>, elevation: <n>,` inserted (or, for the schema, the enum
  comma + `"lethal"` line added).
- IF the environment has node deps installed:
  `node --test tests/scripts/encounterSchema.test.js` and
  `node --test tests/services/combat/encounterGridSchema.test.js` -> all tests pass.
  If deps are not available, skip -- the edits are pre-verified green; the diff
  match above is the binding check.
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
