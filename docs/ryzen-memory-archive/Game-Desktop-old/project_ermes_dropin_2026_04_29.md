---
name: ERMES Drop-in Self Install 2026-04-29
description: ERMES (Ecosystem Research, Measurement & Evolution System) installato come prototype lab isolato + JSON exporter — PR #2009 merged main
type: project
originSessionId: 1f48344a-6a3e-4f06-b347-f632ba3fab74
---
# ERMES Drop-in Self Install — Sessione 2026-04-29

## TL;DR

User ha droppato `ERMES_dropin_self_install.zip` su Desktop. Pacchetto self-installing
Codex-oriented con installer Python, payload, prompt, manifest. Eseguito install →
validate → commit → PR → merge in singola sessione autonoma.

**PR mergiato main**: [#2009](https://github.com/MasterDD-L34D/Game/pull/2009) commit `2259634e`. 13 file, +449 LOC, 0 deletions.

## Cosa è ERMES

**E.R.M.E.S.** = **E**cosystem **R**esearch, **M**easurement & **E**volution **S**ystem.

Successor del progetto "Evolution Sim" assorbito dentro Evo Tactics. **NON** è un
nuovo gioco autonomo. È:

1. **Laboratorio locale** — sim deterministica fitness/survival/mutation/drift
2. **Dashboard analisi** — Streamlit opzionale
3. **Exporter JSON** — eco_pressure_report v0.1.0 schema
4. **Tuning harness** — experiment loop con scoring function
5. **Futuro ponte** — encounter bias, mutation bias, debrief, worldgen constraints

**Filosofia chiave**: _"ERMES misura e suggerisce. Evo Tactics decide e gioca."_

## Files shippati (sotto `prototypes/ermes_lab/`)

- `ermes_sim.py` (122 LOC) — Environment + Species dataclass, fitness/survival
  formula con sigmoid, mutation con stress amplifier, drift density-dependent,
  build_report con encounter_bias + mutation_bias + extinction_risk + debrief_notes,
  CLI fallback, 5 unittest interni
- `scoring.py` (34 LOC) — sample config from ranges, score_report (pressure target
  0.55 + risk target 0.35 + motion + extinction penalty), CSV + best.json output
- `ermes_dashboard.py` (20 LOC) — Streamlit (graceful skip se non installato)
- `configs/default.json` — biome=badlands, 3 species (Dune Stalker / Sand Burrower /
  Rust Scavenger), 150 generations, seed 7
- `configs/experiment_ranges.json` — grid sample (4 temp × 4 food × 4 pred × 4 vol ×
  3 gen × 4 mut_scale × 3 repro_scale)
- `adapters/{__init__.py, evo_tactics_export_schema.json}` — 3 test esterni
- `tests/test_ermes_lab.py` — 3 test (default_runs, score_bounded, serializable)
- `outputs/.gitkeep` — artifacts gitignored
- `.gitignore` — `outputs/*` + `__pycache__/`

Plus 2 doc planning con frontmatter draft:
- `docs/planning/2026-04-29-ermes-integration-plan.md` — roadmap E0-E8
- `docs/planning/2026-04-29-ermes-codex-execution-brief.md` — execution brief

## Validation evidence (pre-merge)

| Step | Risultato |
|------|-----------|
| `ermes_sim.py --test` | **5/5 PASS** (0.005s) |
| `ermes_sim.py --cli` | OK biome=badlands eco_pressure=0.238 final_pop=5340 (Sand Burrower estinta) |
| `scoring.py --runs 25` | OK best_score 0.977, 26 righe CSV |
| `unittest discover tests/` | **3/3 PASS** (0.003s) |

CI PR: 4 SUCCESS (paths-filter, governance, Workers Builds Cloudflare),
24 SKIPPED legittimi (paths-filter routing — modifiche solo in `prototypes/` +
`docs/planning/` non triggerano backend/dashboard CI heavy).
mergeable=MERGEABLE, mergeStateStatus=CLEAN.

## Roadmap E0-E8 (da integration plan)

| Fase | Stato post-PR #2009 |
|------|---------------------|
| E0 — Doc integration | ☑ |
| E1 — Prototype isolated | ☑ |
| E2 — CLI + deterministic sim | ☑ |
| E3 — Dashboard optional | ☑ |
| E4 — JSON export | ☑ |
| E5 — Experiment loop | ☑ |
| E6 — Codex validation | ☑ |
| E7 — Future runtime candidate (crossEventEngine design only) | ☐ deferred post-playtest + ADR |
| E8 — Future foodweb candidate (ecosystemLoader design only) | ☐ deferred post-playtest + ADR |

## Guardrail rispettati

- **Zero touch**: `apps/backend/`, `apps/play/`, `data/core/`, `packs/`,
  combat runtime, round orchestrator, Game-Database integration
- Installer enforcement via `SAFE_PREFIXES = ("docs/planning/", "prototypes/ermes_lab/")`
- Lab isolato: nessun service runtime importa ERMES output

## Workflow lessons

1. **Worktree branch from origin/main**: branch corrente
   `feat/deep-research-analysis-2026-04-28` aveva 20+ commit unrelated. PR pulito
   richiedeva branch separato da main. Tentativo iniziale con `git reset --soft
   origin/main` da branch corrente ha portato tutti i diff in stage. Recovery:
   `git stash` modified, switch back, delete temp branch, usare
   `git worktree add ../Game-ermes -b feat/ermes-dropin-2026-04-29 origin/main`.

2. **Copy untracked files to worktree**: ERMES files installati nel main repo
   working tree. Worktree nuovo da `origin/main` non li vede. Soluzione: `cp -r`
   selettivo (solo `prototypes/` + 2 docs), pulizia `__pycache__/` + artifacts
   `outputs/*` (per non committarli), aggiungere `.gitignore` ad-hoc nel lab dir.

3. **Drop-in transient dir**: `ERMES_dropin_self_install/` rimane untracked nel main
   repo working tree. Non gitignored a livello repo (sicurezza: user vede sempre
   cosa estrae). Da rimuovere manualmente con `rm -rf ERMES_dropin_self_install/`
   dopo merge.

## Path canonical

- Repo install: [prototypes/ermes_lab/](prototypes/ermes_lab/)
- Plan: [docs/planning/2026-04-29-ermes-integration-plan.md](docs/planning/2026-04-29-ermes-integration-plan.md)
- Brief: [docs/planning/2026-04-29-ermes-codex-execution-brief.md](docs/planning/2026-04-29-ermes-codex-execution-brief.md)
- Streamlit run: `pip install streamlit && streamlit run prototypes/ermes_lab/ermes_dashboard.py`

## Follow-up

- Registry update `docs/governance/docs_registry.json` per i 2 nuovi doc planning
- Cleanup main repo: `rm -rf ERMES_dropin_self_install/ prototypes/ docs/planning/2026-04-29-ermes-*.md`
  (i duplicati untracked nel branch deep-research; main pull li porterà tracked)
- Streamlit dashboard smoke test (opzionale, richiede `pip install streamlit`)
- E7-E8 runtime integration (futuro, gated da playtest + ADR)
