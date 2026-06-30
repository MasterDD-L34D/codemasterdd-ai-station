# Jules task -- characterization tests for translatePathfinderStatblock

Repo: MasterDD-L34D/Game.

## Scope (single new test file, test-only, NO behaviour change)
Add a NEW test file that characterizes the EXPORTED function `translatePathfinderStatblock` in
`services/generation/biomeSynthesizer.js`. This is a test-only change: do NOT modify
`biomeSynthesizer.js`, `speciesBuilder.js`, or ANY production file (services/generation is a
freeze-sensitive path -- read it read-only). Assert the CURRENT behaviour (characterization /
golden-master), do not change it.

## Context (read first, read-only)
- `services/generation/biomeSynthesizer.js` (line ~144) exports `translatePathfinderStatblock(statblock, context = {})`:
  it calls `buildPathfinderProfile(statblock, { biomeId: context.biomeId || null, fallbackTraits: ensureArray(context.fallbackTraits) })`.
- `services/generation/speciesBuilder.js` (line ~429) `buildPathfinderProfile(statblock, options)`:
  - throws `Error('Statblock Pathfinder non valido')` when statblock is falsy or not an object.
  - returns an object with deterministic fields incl.:
    `id` = `pathfinder-<statblock.id>`; `display_name` = `statblock.name || statblock.id || 'Creatura Pathfinder'`;
    `functional_tags` = `['pathfinder', String(statblock.type||'').toLowerCase(), String(statblock.subtype||'').toLowerCase()]` filtered to truthy;
    `biomes` = `options.biomeId ? [options.biomeId] : []`; `playable_unit` = `false`;
    `environment_affinity.biome_class` = `options.biomeId || 'pathfinder_unknown'`;
    `traits.core` = deduped `['pathfinder', ...geneticTraits, ...fallbackTraits]`;
    `source_dataset` = `{ id: 'pathfinder', profile_id: statblock.id, cr: statblock.cr, axes }`.
  - READ `extractPathfinderLists(statblock, options)` to confirm exactly how `fallbackTraits` flows
    into `traits.core`, and assert only the OBSERVABLE result (do not guess internal shape).
- Mirror the existing sibling test `tests/services/biomeSynthesizerMetadata.test.js`:
  uses `require('node:test')` + `require('node:assert/strict')` and
  `const { translatePathfinderStatblock } = require('../../services/generation/biomeSynthesizer');`
  CommonJS, no new deps, no test framework change.

## File to modify (ONLY this one)
- NEW `tests/services/biomeSynthesizerPathfinder.test.js`

## What the tests must assert (CURRENT behaviour; assert exact values, do NOT "fix")
- Invalid input throws: `translatePathfinderStatblock(null)` and `translatePathfinderStatblock(42)`
  each throw an Error (message includes 'Statblock Pathfinder non valido').
- Minimal valid statblock (e.g. `{ id: 'gob', name: 'Goblin', type: 'Humanoid', axes: {} }`) with no
  context: result.id === 'pathfinder-gob'; display_name === 'Goblin'; functional_tags includes
  'pathfinder' and 'humanoid'; biomes deep-equals []; playable_unit === false;
  environment_affinity.biome_class === 'pathfinder_unknown'; traits.core includes 'pathfinder';
  source_dataset.profile_id === 'gob'.
- context.biomeId set (e.g. 'foresta'): biomes deep-equals ['foresta']; biome_class === 'foresta'.
- display_name fallbacks: statblock without name -> display_name === statblock.id; without name AND
  id -> display_name === 'Creatura Pathfinder'.
- context.fallbackTraits (e.g. ['x']): assert the observed effect on traits.core per
  extractPathfinderLists (read the source; assert what actually happens, do not assume).
Deterministic; no network, no filesystem, no DB.

## Constraints
- ASCII-only in all added code and comments.
- Pure node:test + node:assert/strict; no new dependencies; do not touch package.json/lockfile/config.
- Do NOT edit any production file (biomeSynthesizer.js / speciesBuilder.js / services/generation/**).
  Single new test file only.
- Conventional Commit subject (lowercase), e.g.:
  test(generation): characterize translatePathfinderStatblock output

## Acceptance (verify before delivering)
- The new test passes: `node --test tests/services/biomeSynthesizerPathfinder.test.js`.
- The existing test suite stays green (no regressions); production files unchanged.
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
