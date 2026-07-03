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
3. Node-type mapping for the extractor (VERIFIED 2026-07-03 against
   `tree-sitter-gdscript` via `tree-sitter-language-pack` 1.12.2, parsing 82 real
   Godot 4.x `.gd` files with 0 parse errors -- see "Verifica empirica" below):
   - functions: `function_definition` (name child `name`)
   - classes / inner classes: `class_name_statement` (top-level `class_name`) and
     `class_definition` (inner `class X:` -- confirmed via probe; rare in real code)
   - inheritance: `extends_statement` -> `[extends]` edge
   - signals: `signal_statement` -> node (Godot's decoupling primitive; high value)
   - members: `variable_statement`, `const_statement`, `enum_definition`
   - calls: free calls are `call`; member/method calls (`obj.method()`) are
     `attribute_call` nested under `attribute` -- BOTH needed for `[calls]` edges.
     Member calls are the plurality in OO GDScript (in the sample: 1349
     `attribute_call` vs 1214 `call`), so handling only `call` loses most edges.
   - `preload(...)` / `load(...)` and `extends "res://..."` -> `[imports]` edges
     (Godot's resource-path dependency graph -- worth first-classing). `preload`/
     `load` are `call` nodes whose callee identifier is `preload`/`load` (no
     dedicated node kind), so imports are recognized by callee name, not node type.

### Offer

Happy to open a PR if the maintainer agrees on the language-pack resolution
approach vs requiring a standalone binding. Would want guidance on: (a) preferred
`ts_module` resolution for pack-only grammars, (b) whether `.tscn`/`.tres` scene
graphs are in scope (they encode node trees + script attachments -- a second,
Godot-specific extractor -- or out of scope for a first cut), (c) target
tree-sitter version: graphify currently pins `tree-sitter` 0.25.x and uses the
property-style Python API (`node.type`, `tree.root_node`, `parser.parse(bytes)`),
whereas `tree-sitter-language-pack` 1.12 pulls `tree-sitter` 0.26 whose binding is
method-style (`node.kind()`, `tree.root_node()`, `parser.parse(str)`). Consuming
the pack would require either pinning an older pack that ships 0.25-compatible
grammars, or migrating the extractor to the 0.26 API. Is a standalone
`tree-sitter-gdscript` wheel (matching the existing per-language wheel pattern)
preferable to taking language-pack as a new dependency?

--- END ISSUE BODY ---

## Note operative (codemasterdd, non parte della issue)

- Boundary repo esterno: submit = Eduardo o gh-authed con OK esplicito. NON ancora
  sottomesso.
- Se accettato, il PR upstream evita la patch-fragile-su-site-packages (anti-pattern).
- Nel frattempo Godot-v2 code-nav resta coperto da `godot-engine-specialist` + LSP.

## Verifica empirica 2026-07-03 (codemasterdd, ground-truth -- Ryzen)

Il TODO "verificare i node-type reali prima di aprire il PR" e' ESEGUITO. Setup:
venv isolato, `tree-sitter-language-pack` 1.12.2 (+ `tree-sitter` 0.26.0), parser
`get_parser("gdscript")`, corpus = 82 file `.gd` first-party di Game-Godot-v2
(`scripts/**`, esclusi addons). **0 parse error** su tutto il corpus.

Esito claim node-type del draft (tutti confermati vs grammar reale):

| Draft kind | Verificato | Count sample |
|------------|-----------|--------------|
| `function_definition` | OK | 395 |
| `class_name_statement` | OK | 81 |
| `class_definition` (inner class) | OK (probe mirato; raro nel corpus reale, 0 nel sample) | 0/probe |
| `extends_statement` | OK | 81 |
| `signal_statement` | OK | 1 |
| `variable_statement` | OK | 1126 |
| `const_statement` | OK | 281 |
| `enum_definition` | OK | 1 |
| `call` | OK | 1214 |

Correzioni / scoperte NON nel draft (load-bearing):

1. **`attribute_call` mancava.** Le chiamate a membro/metodo (`obj.method()`, molto
   comuni in GDScript OO) NON sono `call` ma `attribute_call` annidato sotto
   `attribute`. Nel sample: 1349 `attribute_call` vs 1214 `call` -- la maggioranza
   degli edge di chiamata. Un extractor che gestisce solo `call` perde la maggior
   parte del call-graph. (Corretto nella issue sopra.)
2. **graphify NON usa tree-sitter-language-pack.** Meccanismo reale (letto da
   `detect.py` + `extract.py` installati): set piatto `CODE_EXTENSIONS` + tabella
   `LanguageSpec` con `ts_module="tree_sitter_<lang>"` caricato via
   `importlib.import_module(ts_module)` -- 25 wheel per-lingua installati, gdscript
   assente. Aggiungere gdscript via language-pack = NUOVA dipendenza per graphify,
   piu' invasivo del "just consumed" del draft. Ask minimale alternativo: chiedere
   un wheel `tree-sitter-gdscript` standalone -> allora il fix graphify = additivo
   sul pattern per-wheel esistente.
3. **`register_language_resolver` NON serve per aggiungere una lingua.** Da
   `resolver_registry.py`: e' SOLO per i pass di resolution cross-file post-parse
   (edge call/reference language-specific). L'estrazione AST base e' guidata dalla
   tabella `LanguageSpec` hardcoded in `extract.py` -> aggiungere gdscript richiede
   un change upstream (o patch site-packages fragile). Nessun plug-in locale
   pulito possibile via l'hook.
4. **Incompatibilita' versione tree-sitter.** language-pack 1.12 tira tree-sitter
   0.26 (API method-style: `root_node()`, `node.kind()`, `parse(str)`);
   graphify pinna 0.25.2 (property-style: `.type`, `parse(bytes)`). Le due API sono
   incompatibili -> "consumare language-pack" costringe graphify a pin pack piu'
   vecchio (grammar 0.25-compat) OPPURE migrazione API 0.26. (Aggiunto come
   domanda (c) alla issue.)

**Implicazione decisionale (per Eduardo).** L'ask upstream e' PIU' GRANDE di quanto
il draft suggeriva (nuova dipendenza + possibile migrazione versione). Opzioni:
(a) upstream PR corposo (nuova dep + node-map completo incl. `attribute_call`);
(b) chiedere al maintainer un wheel `tree-sitter-gdscript` standalone, poi il fix
graphify diventa additivo semplice (RACCOMANDATO come minimale se si vuole coprire
GDScript); (c) status quo -- Godot-v2 code-nav resta su `godot-engine-specialist`
+ LSP, zero-dep (il gap e' noto e non-bloccante, ADR-0043). Nessuna azione esterna
presa: la submit resta Eduardo-gated.
