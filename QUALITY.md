# QUALITY.md -- Code-graph tooling (CodeGraph + graphify)

Quality Gate evidence per l'adozione dei due code-graph tool sulla game repo
family. Standard: ADR-0043 + Quality Gate globale (3 step). Data: 2026-07-02.

## Step 1 -- Smoke (happy-path verde + output verificabile)

**CodeGraph** (`codegraph explore "combat simulation"` su Game):
```
Found 9 symbols across 3 files.
Blast radius:
- run_simulation (ermes_sim.py:81) -- 20 callers; tests present
- run_simulation (pi_shop_simulate.py:226) -- WARN no covering tests
- stats (pi_shop_simulate.py:261) -- WARN no covering tests
calls: run_simulation -> sample_tier / round / stats / execute_strategy ...
```
Index Game: 2203 file, 26.486 nodi, 96.898 archi, 82.75 MB (node:sqlite, WAL).

**graphify** (`graphify explain "run_simulation"` su Game):
```
Node: run_simulation() -- ermes_sim.py L81 -- Community 62 -- Degree 18
Connections (18): --> update_species [calls] / <-- run_multi_biome [calls] ...
```
GRAPH_REPORT: hub multimodal code+doc (`00-SOURCE-OF-TRUTH.md`, `runEncounter`,
`traitEffects.js`). Build no-LLM, token cost 0.

Verdetto step 1: **VERDE** entrambi.

## Step 2 -- Ricerca (>=3 edge case + comportamenti inattesi)

1. **Console-flash hook (Windows).** CodeGraph installer aggiunge un hook
   `UserPromptSubmit` non annunciato -> stesso pattern che ha fatto disabilitare
   claude-mem. RIMOSSO (tenuto MCP+direttiva). graphify installato skill-only,
   nessun hook. Flag: verificare footprint installer, non fidarsi del preview.
2. **Bundle-noise (graphify).** graphify indicizza bundle minified committati in
   `docs/mission-console/assets/` (Vite app buildato in docs) -> community-hub
   inquinati. CodeGraph li filtrava. Fix in step 3.
3. **GDScript gap.** Nessuno dei due parsa GDScript. Su Game-Godot-v2 CodeGraph
   indicizza 56 file peripheral (0/1015 `.gd`); graphify solo doc-map (258 md).
4. **Footprint global CLAUDE.md.** Entrambi scrivono nel file curato (blocco
   fenced CodeGraph + 3 righe graphify). Rimovibili, segnalati.

## Step 3 -- Tuning (>=1 iterazione + metrica delta before/after)

**graphify `.graphifyignore`** (esclude `docs/mission-console/assets/`,
`**/*.bundle.js`), rebuild `--force`:

| Metrica | Before | After | Delta |
|---|--:|--:|--:|
| Nodi | 47.100 | 44.867 | -2.233 |
| Archi | 65.517 | 58.121 | -7.396 |
| Noise-hub (bundle/esm/assets) | 24 | 1 | -23 |
| Community | 3.208 | 3.223 | +15 (segnale piu' pulito) |

Verdetto step 3: **tuning efficace** -- rumore bundle rimosso, signal migliorato.

## Rollout family (stato)

| Repo | CodeGraph | graphify | Note |
|---|---|---|---|
| Game (pilota) | 26.486 nodi | 44.867 nodi | full value, tuned |
| Game-Database | 2.168 nodi | 2.056 nodi | full value (TS/JS/MD) |
| Game-Godot-v2 | 56 file (0 gd) | doc-map 258 md | **thin -- GDScript blind** |

## Gate esito

Production-ready su **Game + Game-Database** (3 step verdi). Game-Godot-v2 =
doc-map only, in attesa di `tree-sitter-gdscript` per graphify (follow-up
ADR-0043). claude-mem = escluso by-design.
