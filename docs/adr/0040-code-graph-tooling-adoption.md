# ADR-0040 -- Code-graph tooling adoption (CodeGraph + graphify) for the game repo family

- Status: Accepted
- Data: 2026-07-02
- Deciders: Eduardo
- Contesto skill/tool-adoption: ADR-0010 (skill install richiede preview + ADR), OD-007 (agent-scanner anti-shadow-duplicate)

## Contesto

Eduardo voleva migliorare la pianificazione sulla game repo family (Game,
Game-Godot-v2, Game-Database) adottando 3 plugin: graphify + claude-mem +
CodeGraph. Pre-adozione, agent-scanner ha rilevato overlap/shadow-duplicate:

- **claude-mem** era GIA' installato e DISABILITATO apposta (`settings.json:
  "claude-mem@thedotmack": false`). Causa documentata (JOURNAL 2026-05-14):
  console-flash su Windows (5 hook, PostToolUse `*` = 20-100 flash/messaggio,
  upstream issue anthropics/claude-code#19012 CLOSED not-planned). Overlappa
  file-memory + AA01 + continuous-learning-v2 + supermemory-eval.
- **CodeGraph** e **graphify** = stessa classe (code knowledge graph), che
  overlappa anche `eng-graph` (SSE MCP gia' vivo, ma codemasterdd-scoped -> NON
  indicizza la game family, quindi un graph tool per la family E' valore netto).

## Decisione

1. **claude-mem: resta OFF.** Non e' un tool di pianificazione; ridondante;
   disabilitato per motivo Windows-flash tuttora valido. Re-enable solo se
   upstream windowsHide-fix o cambio tolleranza (trigger invariati).
2. **Adottare ENTRAMBI CodeGraph + graphify** con ruoli distinti (bake-off su
   pilota Game ha dimostrato complementarita', non duplicazione):
   - **CodeGraph** = lente impatto-codice (call-graph denso, blast-radius +
     test-coverage gaps, auto-sync watcher, MCP-native `codegraph_explore`).
   - **graphify** = lente architettura + doc (multimodal code+doc, Leiden
     community detection, `explain`/`path`/god-nodes).
3. **Windows flash-safety = vincolo duro.** Entrambi installati SENZA hook
   per-tool/per-prompt:
   - CodeGraph: rimosso l'hook `UserPromptSubmit codegraph prompt-hook` che
     l'installer aveva aggiunto (tenuti MCP global + auto-allow + direttiva
     CLAUDE.md fenced). Uso on-demand via `mcp__codegraph__*`.
   - graphify: installato solo come skill+MCP (nessun `graphify hook install`).
     Uso via `/graphify` in-session.
4. **Zero footprint sui file tracked della family.** Indici e config locali via
   `.git/info/exclude` (`.codegraph/`, `graphify-out/`, `.graphifyignore`).
   `.graphifyignore` candidato a commit futuro via PR (branch+PR, merge Eduardo).

## Evidenze (Quality Gate -- vedi QUALITY.md)

Pilota Game (2203/4976 file):
- CodeGraph: 26.486 nodi / 96.898 archi; smoke `explore "combat simulation"` ->
  9 simboli, blast-radius + test-coverage gaps (es. `run_simulation`
  pi_shop_simulate.py:226 = no covering tests).
- graphify: 44.867 nodi / 3.223 community post-tuning; smoke `explain` +
  GRAPH_REPORT con hub code+doc (`00-SOURCE-OF-TRUTH.md`, `runEncounter`).
- Tuning (step 3): `.graphifyignore` esclude bundle minified committati in
  `docs/mission-console/assets/` -> nodi 47.100 -> 44.867 (-2.233), noise-hub
  24 -> 1.

Rollout: Game-Database (CodeGraph 2.168 nodi / graphify 2.056, full value);
Game-Godot-v2 (thin -- vedi Consequences).

## Consequences

- **GDScript gap (load-bearing):** ne' CodeGraph (20+ lang) ne' graphify (26
  tree-sitter grammar) parsano GDScript. Su Game-Godot-v2 CodeGraph indicizza
  solo 56 file peripheral (0 dei 1015 `.gd`); graphify da' solo doc-map (258
  `.md`). Per la struttura-codice Godot i due tool sono ciechi.
- **Follow-up:** valutare l'aggiunta di `tree-sitter-gdscript` a graphify per
  coprire il frontend canonico Godot; altrimenti la lente code-graph resta
  Game-backend + Game-DB only.
- MCP `codegraph` visibile in-session solo dopo restart CC (config global
  scritta in `~/.claude.json`).
- Direttive scritte nel `~/.claude/CLAUDE.md` globale: blocco fenced CodeGraph
  (~15 righe, rimovibile) + registrazione skill graphify (3 righe).

## Alternatives considered

- **Solo CodeGraph** (piu' pulito, auto-sync): scartato -- perde la lente
  doc/architettura di graphify.
- **Estendere eng-graph alla family**: deferred -- eng-graph resta
  codemasterdd-scoped; rivalutabile se i due nuovi tool si rivelano ridondanti.
- **Tutti e 3 i plugin come richiesto**: scartato -- claude-mem gia'-off +
  shadow-duplicate; installare 3 tool overlapping = anti-pattern OD-007.
