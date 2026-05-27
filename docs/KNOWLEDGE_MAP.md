# KNOWLEDGE_MAP -- mappa cross-repo design-knowledge (preservazione + confronto SoT)

> **Scopo**: punto unico per rispondere a tre domande su TUTTO il sapere-design Evo-Tactics:
> 1. **Dove vive** un contenuto (quale repo / path).
> 2. **Che autorita ha**: SoT canonical (governa) vs reference (informa) -- layer A0-A5.
> 3. **E' al sicuro?**: git-tracked (backup GitHub) oppure single-disk a rischio-perdita.
>
> Generato 2026-05-27 dopo audit "contenuto perso?" (root cause = path stale `vault-shared`->`vault` +
> ~139 memory Claude Ryzen-side NON in git). Companion di
> [EVO_TACTICS_ECOSYSTEM_GUIDE.md](EVO_TACTICS_ECOSYSTEM_GUIDE.md) (mappa 7-repo) +
> [EVO_TACTICS_DESIGN_DIGEST.md](EVO_TACTICS_DESIGN_DIGEST.md) (catalogo ispirazioni, §11.7 indice fonti + §12.2 authority map).

---

## 1. Authority layers A0-A5 (chi governa) -- da DESIGN_DIGEST §12.2

| Liv | Autorita | Governa | Precedenza |
|-----|----------|---------|------------|
| **A0** | `docs/governance/*`, `docs_registry.json` | Path, frontmatter, status, canonical-vs-storico | Vince su planning |
| **A1** | `docs/hubs/*`, `docs/combat/round-loop.md`, `docs/adr/*` | Boundary architetturali, contratti, runtime scope | Vince su freeze se boundary contraddetto |
| **A2** | `data/core/*`, `packs/.../data/*`, `schemas/*` | Verita meccanica/numerica/schema | Vince su doc descrittivi |
| **A3** | `docs/core/90-FINAL-DESIGN-FREEZE.md` | Sintesi prodotto, scope shipping | Vince su roadmap/planning |
| **A4** | `AGENTS.md`, `.claude/*`, `CLAUDE.md`, `SAFE_CHANGES.md` | Modo operativo agent, DoD | Governa "how" non "what" |
| **A5** | Canvas, appendici, playtest notes, research, **memory archive** | Contesto, intento, baseline | Solo informa; perde vs A0-A4 |

Principio: *governance colleziona, ADR delimita, YAML prova, freeze decide, agent-doc esegue, storico ispira ma non governa.*

---

## 2. SoT canonical (A0-A4) -- la verita che governa

| Cosa | Repo / Path | Layer | git |
|------|-------------|-------|-----|
| Design freeze (scope shipping) | Game `docs/core/90-FINAL-DESIGN-FREEZE.md` | A3 | OK (public) |
| Pilastri + vision + loop | vault `Spaces/Dev/Evo-Tactics/core/02-PILASTRI.md`, `01-VISIONE`, `03-LOOP` | A1-A3 | OK (sovereign) |
| Source of Truth unificata | vault `core/00-SOURCE-OF-TRUTH.md` (grid/campaign/evoluzione) | A1-A2 | OK (sovereign) |
| Combat ruleset | Game `docs/combat/round-loop.md` + `combat-canon.md` | A1 | OK (public) |
| Verita meccanica/numerica | Game `data/core/*` (species/traits/biomes YAML) | A2 | OK (public) |
| Governance machinery | Game `docs/governance/docs_registry.json` + vault `governance/` | A0 | OK |
| Serie core numerata 00-90 | Game `docs/core/NN-*.md` (canonical) + vault shadow | A1-A3 | OK |
| ADR game-design | vault `Spaces/Dev/Evo-Tactics/adr/` (~42) + Game `docs/adr/` (date-named) | A1 | OK |
| Modello genetico Fase-1 (D-HEIR/D-REPRO) | vault `core/00-SOURCE-OF-TRUTH.md` §24.6 + `90-FINAL-DESIGN-FREEZE.md` §21.3 (scoped-supersede 2026-05-26) + Game `docs/adr/ADR-2026-05-26-deep-genetics-phase1-supersede-freeze.md` + spec `docs/superpowers/specs/2026-05-26-repro-heir-genetic-model-design.md` | A2-A3 | OK (vault sovereign; Game-side **solo origin**, local 71-behind -- vedi §6) |

**Regola confronto**: in caso di divergenza reference-vs-SoT, vince A0-A4. vault `core/` (freeze A3) vince per scope-shipping; museum/digest = catalogo alternative + ROI. Drift reference-vs-SoT lo flagga l'agent `evo-tactics-design-watcher` (vault `production/agents/`).

---

## 3. Reference layer A5 (informa, non governa) -- dove + sicurezza

| Artifact | Repo / Path | Cosa contiene | git-tracked |
|----------|-------------|---------------|-------------|
| **DESIGN_DIGEST** | codemasterdd `docs/EVO_TACTICS_DESIGN_DIGEST.md` | ~31 giochi distillati (cosa piaceva / come farlo / fonte / stato) + convergenze + anti-ref + asset provenance | OK |
| **Games Source Index** | Game `docs/guide/games-source-index.md` | Catalogo completo Tier S/A/B/C/D/E + anti-ref + persona + GDD pubblici + **mappa 37 repo OSS** + agent illuminator owner | OK (public) |
| **Museum cards** | Game `docs/museum/cards/` (~45) + indice `MUSEUM.md` | Alternative scartate/parcheggiate Dublin Core + ROI + reuse-path | OK (public) |
| **Research cluster** | Game `docs/research/2026-04-2x-*` (cross-game extraction, indie-synthesis, tier-matrix) | Estrazione pattern multi-gioco | OK (public) |
| **Reports synthesis** | Game `docs/reports/2026-04-27-*synthesis*` | Sintesi ricerca strategica | OK (public) |
| **vault Cards/Atlas** | vault `Cards/`, `Atlas/`, `Spaces/Dev/Evo-Tactics/` | Knowledge atomizzato ACCESS (es. `game-design-references-direction-5`, `masterizzazionedigiochi-moc`) | OK (sovereign) |
| **Asset refs** | `evo-tactics-refs-meta/` (SKIV_REFS, CATALOG, CC0_SOURCES, HANDOFF) | Provenance asset 100% classificata (32136 file) | OK (private remote) |
| **Art Godot** | Game-Godot-v2 `docs/godot-v2/visual-screen-bible.md` + `visual-design-research.md` | Bibbia visiva 3-modi | OK (public) |
| **Ryzen memory archive** | codemasterdd `docs/ryzen-memory-archive/` (139 file, **NEW 2026-05-27**) | Storia-decisioni + reference + feedback da sessioni Claude Code Ryzen-side -- vedi §4 | **OK (era a rischio, ora captured)** |

---

## 4. Ryzen memory archive -- inventario (139 file, captured 2026-05-27)

**Provenance**: `Vgit@192.168.1.11:C:/Users/VGit/.claude/projects/*/memory/` via scp. Erano memory
auto-generate da Claude Code lato Ryzen, **fuori da ogni git** (single-disk) e gia semi-orfane
(chiave progetto `C--Users-VGit-Desktop-Game` = vecchio path; Game migrato a `C:/dev/Game` ->
nuove sessioni usano chiave `C--dev-Game`, set vecchio non piu auto-caricato). Snapshot punto-nel-tempo;
**non sincronizzato** (re-pull manuale se servono aggiornamenti). Worktree effimere (`*--claude-worktrees-*`)
NON incluse (transienti, duplicano i main key).

| Folder (chiave progetto) | File | Highlight |
|--------------------------|-----:|-----------|
| `Game-Desktop-old` (`C--Users-VGit-Desktop-Game`) | 84 | **Il grosso**: 11 `reference_*` (external_repos, tactical_postmortems, tier0_deep_dive, voidling_bound, flint_optimization, skiv_online_imports, gdd_audit, classification_4d, asset_workspace, deep_dive_phase2, prisma_adapter) + ~43 `project_session_/sprint_*` + `gdd_open_questions`, `parked_ideas`, `skiv_personal_wishlist`, `canonical_refactor`, `machinations_models` + 14 `feedback_*` |
| `C--dev-Game-Godot-v2` | 24 | Godot M1 loop, sistema-learning briefing, cascade closures, roadmap 2026-05-22 |
| `C--Users-VGit-Desktop-Game-Godot-v2` | 15 | Path A, schema-wire wave, design decisions w7, plan_v3 |
| `C--dev-vault` | 4 | eng_graph_mcp, evo_roadmap (stale), agents_tools |
| `C--dev-Game`, `C--dev-codemasterdd-ai-station` | 3+3 | set nuovi (piccoli): calibration_toolkit, n_sample_authority, genetic_model_thread, backend_boot |
| `C--dev-Game-Database`, `C--Users-VGit`, `evo-swarm` | 2+2+2 | concurrent_writer_standdown, repo_layout, compass_install_state |

**Nota duplicazione utile**: `reference_external_repos.md` (mappa 37 repo OSS) e' anche **inlined** in
Game `games-source-index.md` (righe 246-324) -- doppia copertura. Molti `project_session_*` e
`project_gdd_open_questions` / `parked_ideas` / `skiv_wishlist` sono invece **unici** (reasoning non
replicato in git altrove) = il vero valore preservato qui.

### 4.1 Re-pull (runbook idempotente)

Snapshot statico -- per ri-allineare, da Lenovo (read-only su Ryzen, overwrite locale = idempotente).
Runbook diretto invece di script (anti-pattern #11: 1-comando-robusto > helper fragile):

```powershell
$base = "Vgit@192.168.1.11:C:/Users/VGit/.claude/projects"
$dst  = "C:/dev/codemasterdd-ai-station/docs/ryzen-memory-archive"
$map  = [ordered]@{
  "Game-Desktop-old"="C--Users-VGit-Desktop-Game"; "C--dev-Game"="C--dev-Game";
  "C--dev-Game-Godot-v2"="C--dev-Game-Godot-v2"; "C--Users-VGit-Desktop-Game-Godot-v2"="C--Users-VGit-Desktop-Game-Godot-v2";
  "C--dev-vault"="C--dev-vault"; "C--dev-Game-Database"="C--dev-Game-Database";
  "C--dev-codemasterdd-ai-station"="C--dev-codemasterdd-ai-station"; "C--Users-VGit"="C--Users-VGit";
  "C--Users-VGit-Desktop-pathfinder-master-dd-repo-evo-swarm"="C--Users-VGit-Desktop-pathfinder-master-dd-repo-evo-swarm"
}
foreach ($f in $map.Keys) {
  Remove-Item "$dst/$f" -Recurse -Force -ErrorAction SilentlyContinue   # idempotente: evita nesting su re-run
  scp -r -q "$base/$($map[$f])/memory" "$dst/$f"                        # niente 2>$null: i fail scp restano visibili
}
```

Poi `git add docs/ryzen-memory-archive` + commit se ci sono diff. Worktree effimere escluse (0 file, verificato 2026-05-27).

---

## 5. Come confrontare reference vs SoT (workflow)

1. **Precedenza**: A0 > A1 > A2 > A3 > A4 > A5. Se un reference (A5) contraddice freeze/YAML (A2-A3) -> vince SoT, il reference e' storico/intento.
2. **Drift detection**: agent `evo-tactics-design-watcher` (vault) flagga contraddizioni freeze/ADR/YAML/schema -> log `Q-001-DECISIONS-LOG.md`.
3. **Prova-di-eliminazione** (per decidere se un'idea-reference va costruita): rimuovila mentalmente -> se nessun pilastro/loop/vision fallisce = cerimonia, resta reference; se qualcosa fallisce = load-bearing, promuovi a SoT.
4. **Entry-point pratici**: parti da `games-source-index.md` (catalogo + path canonical per gioco) o DESIGN_DIGEST §11.7 (indice fonti). Questa mappa = livello sopra (dove-tutto + SoT-vs-ref + sicurezza).

---

## 6. Gap / rischi residui (stato 2026-05-27)

- **Re-pull manuale** -- ✅ RESOLVED: runbook idempotente §4.1.
- **Worktree memory** (`*--claude-worktrees-*`, ~40 chiavi) -- ✅ RESOLVED: verificato 2026-05-27, **0 file memory** nelle worktree (niente di unico). Safe da ignorare.
- **Memory split** Game (`Game-Desktop-old` 84 file storici vs `C--dev-Game` 3 file nuovi) -- ✅ RESOLVED-as-preserved: NON mergeati di proposito (ere diverse, zero overlap-loss). Entrambi archiviati. **Active going-forward = chiave `C--dev-Game`** (Game vive in `C:/dev/Game`); `Game-Desktop-old` = archivio storico read-only.
- **Local Game stale** -- ⏳ DEFERRED (Eduardo-gated): `C:/dev/Game` Lenovo HEAD `196a63a4`, **71 commit behind** origin/main (`637b3dc0`, verificato 2026-05-27). FF-pull **bloccato** da `.husky/pre-commit` (skip-worktree wrapper, mirror-dance Evo-Tactics). Origin = canonical, local = sandbox (no harm). Sync safe (da Eduardo): `git -C C:/dev/Game update-index --no-skip-worktree .husky/pre-commit; git checkout -- .husky/pre-commit; git pull --ff-only origin main; git update-index --skip-worktree .husky/pre-commit`.
- **Privacy** -- ✅ repo codemasterdd confermato **PRIVATE** (no leak). Caveat residuo: e' cloud-whitelisted per delega aider; se contenuto archivio non deve toccare cloud LLM, escludere `docs/ryzen-memory-archive/` via path-check nei wrapper cloud.

---

## 7. Reuse queue (anti-cimitero) -- triage 2026-05-28

Prova-di-eliminazione su 11 reference archiviati + 3 gap. **Onesto**: dei 11 ref, solo `classification_4d` e' genuinamente orfano-high-value; il resto = backup (contenuto gia assorbito in SoT/DIGEST/code). Dei "gap", 1 era stale-shipped, 1 e' defer-intenzionale gia tracked, 2 sono lavoro reale fresco.

| Item | Azione riuso | Stato |
|------|--------------|-------|
| `reference_classification_4d` (framework 4-axis keep/kill/archive, meta-tool unico, non in SoT) | PROMOTE → vault Card (A5 curated) | TODO -- branch+PR, Eduardo-merge-gate |
| Encounter-authoring CLI (da `reference_tactical_postmortems` / Fallout Tactics: `game_cli.py author-encounter`) | OPEN ticket Game backlog -- unblocks M3 content-slice volume | TODO -- Game (auth Eduardo) |
| `games-source-index.md:248` backlink rotto (dead Ryzen path) | repoint → `codemasterdd/docs/ryzen-memory-archive/Game-Desktop-old/` | TODO -- Game (FF-pull husky-blocked, vedi §6) |
| Genetics epigenome/Lamarck-lite (engine) | -- | **SHIPPED Fase-3** (Game #2402 `c359b576`, 2026-05-28: engine + mating wire + speciation + Frammenti). ⚠️ vault SoT §24.6 doc lagga (dice ancora "DEFERRED" -- riconciliazione vault pending; authority runtime = Game backend) |
| Genetics genealogie profonde + eco-repro lungo-termine | Fase-3+ build | TRACKED -- DEFERRED (non in #2402) |
| Voidling Pattern 6 visual_swap | -- | DONE (shipped 2026-05-05; claim "P0 gap" era stale, corretto DIGEST §11.5) |
| Altri 10 `reference_*` (tactical_postmortems, voidling, tier0, gdd_audit, deep_dive_phase2, flint, skiv_online, asset_workspace, prisma_adapter, external_repos) | LINK-from-DIGEST dove utile; contenuto gia in SoT/DIGEST/code | BACKUP -- no action (riviverli non cambia il gioco = backup, non riuso) |

**High-leverage reale** (muove il gioco): (1) repoint backlink games-index (~5min, Game), (2) encounter-authoring CLI (ticket M3), (3) classification_4d → vault Card. Il resto = preservato come backup, discoverable via cross-ref esistenti.
