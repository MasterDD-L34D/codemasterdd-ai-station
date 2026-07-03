# Upstream feature-request draft -- graphify GDScript support

Target repo: `safishamsi/graphify` (PyPI `graphifyy`). Draft 2026-07-02 (ADR-0043
follow-up). English (upstream). Post as a GitHub issue; offer a PR.

--- ISSUE BODY BELOW (copy-paste) ---

## Feature request: GDScript (Godot) language support

### Motivation

graphify has no GDScript extractor, so Godot projects -- where the game logic
lives almost entirely in `.gd` files -- get no code-structure graph. On a real
Godot 4.x repo (~1000 `.gd` files) graphify currently produces only a doc-map
from the Markdown; the entire game codebase is invisible to `explain` / `path` /
god-node navigation. Godot is a large and growing OSS engine, so GDScript support
would unlock a whole ecosystem for graphify.

### Why this looks tractable

1. **Grammar already packaged.** `tree-sitter-language-pack` (>=1.12) bundles a
   maintained GDScript grammar (upstream `PrestonKnopp/tree-sitter-gdscript`), so
   no new grammar needs to be authored -- just consumed. (There is no standalone
   `tree-sitter-gdscript` wheel on PyPI, which is likely why it was skipped.)
2. **graphify already has the extension seams.** `detect.py` has a flat
   `CODE_EXTENSIONS` set, and `extract.py` defines per-language `LanguageSpec`
   entries (`ts_module=...`) plus a `register_language_resolver(...)` hook. Adding
   a language is a additive change along those existing seams.

### Concrete change sketch

1. `detect.py`: add `.gd` (and optionally `.tres`/`.tscn` as non-code assets) to
   `CODE_EXTENSIONS`.
2. `extract.py`: add a `LanguageSpec` for GDScript. Because the grammar is inside
   `tree-sitter-language-pack` rather than a `tree_sitter_gdscript` module, the
   `ts_module` resolution would need a small branch to load via
   `tree_sitter_language_pack.get_language("gdscript")` (or document language-pack
   as the resolution path for pack-only grammars).
3. Node-type mapping for the extractor (verify against the shipped grammar --
   node names below are indicative of `tree-sitter-gdscript`):
   - functions: `function_definition` (name child `name`)
   - classes / inner classes: `class_definition`, `class_name_statement`
   - inheritance: `extends_statement` -> `[extends]` edge
   - signals: `signal_statement` -> node (Godot's decoupling primitive; high value)
   - members: `variable_statement`, `const_statement`, `enum_definition`
   - calls: `call` expression -> `[calls]` edges
   - `preload(...)` / `load(...)` and `extends "res://..."` -> `[imports]` edges
     (Godot's resource-path dependency graph -- worth first-classing)

### Offer

Happy to open a PR if the maintainer agrees on the language-pack resolution
approach vs requiring a standalone binding. Would want guidance on: (a) preferred
`ts_module` resolution for pack-only grammars, (b) whether `.tscn`/`.tres` scene
graphs are in scope (they encode node trees + script attachments -- a second,
Godot-specific extractor -- or out of scope for a first cut).

--- END ISSUE BODY ---

## Note operative (codemasterdd, non parte della issue)

- Boundary repo esterno: submit = Eduardo o gh-authed con OK esplicito.
- Se accettato, il PR upstream evita la patch-fragile-su-site-packages (anti-pattern).
- Nel frattempo Godot-v2 code-nav resta coperto da `godot-engine-specialist` + LSP.
- Verificare i node-type reali: `python -c "from tree_sitter_language_pack import
  get_parser; ..."` su un `.gd` di Game-Godot-v2 prima di aprire il PR.
