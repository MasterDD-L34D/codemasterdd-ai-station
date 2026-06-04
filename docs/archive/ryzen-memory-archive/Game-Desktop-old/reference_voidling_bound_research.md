---
name: Voidling Bound — research investigation 2026-04-26
description: 4-stage scope-down research per Voidling Bound (Hatchery Games 2026 TPS+monster collector) — 6 pattern P2 evolution donor + museum card M-2026-04-26-001
type: reference
originSessionId: 98fedcf8-2359-422a-a4dc-3da7283278a5
---
# Voidling Bound — research investigation 2026-04-26

## Identity (recon stage 1)

- **Game**: Voidling Bound (Hatchery Games, Quebec City — ex-Skylanders/Ubisoft/Beenox devs)
- **Steam app**: 2004680 — demo + playtest live
- **Release**: 2026-06-09 PC (Steam + Epic), console TBD
- **Genre**: Third-person shooter + monster collector/crafter — *player IS the monster* (NOT turn-based, NOT Pokémon-clone)
- **Core loop**: 47 base Voidling species → branching evolution + gene splicing + breeding → laboratory crafting → "The Abyss" roguelite endgame

## Why scope-down to 1 agent (not 3-agent fan-out)

Recon verdict: **relevance 2.5/5**, overlap solo P2 (evolution emergente). Zero match P1 (TPS != grid-tactics), P4 (no MBTI), P5 (no co-op confermato), P6 (skill-based action != turn-based asymmetry). Saved ~60-70% agent budget.

## 6 pattern shipped (creature-aspect-illuminator stage 2)

1. **Rarity-gated ability CLASS unlock** (not just power bump) — VB tiers unlock distinct ability *categories*, not stronger versions. ADOPT low effort. `mutation_catalog.yaml` add `unlocks_category` field.
2. **Element-choice as permanent path-lock** — mutual exclusion at first commit. ADOPT — add `mutually_exclusive_with` schema field.
3. **Spliced terminal endpoint** — max freedom, zero inheritance. ADAPT — map a Apex lifecycle phase (`build_mode: unrestricted`, `legacy_only: true`).
4. **3-currency separation** (Mutagen / Research Points / Attribute Points) — no dead-zone competition. ADOPT principle. Defer rename `pe_cost`→`mutagen_cost` a M14 mutation engine.
5. **Element-faction archetype affinity** — element gates combat matchup effectiveness (1.5x vs 0.75x). ADAPT — `resistanceEngine.js` already has hook site.
6. **Visual change mandatory at EVERY tier** — wiki confirmed. P0 gap doppio-confermato (VB + Wildermyth convergence). ADOPT, 0/30 mutations have `visual_swap_it` today.

## Cross-pillar gems

- **Apex as "Spliced" endpoint** — build-override + legacy-only reproduction
- **Research Points as job-depth currency** — gates jobs_expansion 48 perks separato da PE form evolution

## Outputs

- Research: `docs/research/2026-04-26-voidling-bound-evolution-patterns.md`
- Museum card: `docs/museum/cards/evolution_genetics-voidling-bound-patterns.md` (M-2026-04-26-001, score 4/5)
- MUSEUM.md: nuova sezione `Evolution genetics / Mutation engine` (12 card totali post-add)
- Registry `docs_registry.json` updated, governance check 0/0
- LIBRARY.md riga aggiunta tabella "Repo esterni studiati"

## Reuse paths

| Path | Effort | Action |
|---|---|---|
| Minimal | ~1h | TKT-MUTATION-P6-VISUAL — 30 mutation `visual_swap_it` field + `tools/py/lint_mutations.py` |
| Moderate | ~5-6h | Pattern 6 visual + Pattern 1 unlocks_category schema + lint enforcement |
| Full | ~15-20h | All 6 pattern wire M14 mutation engine + Apex Spliced + 3-currency separation |

## Anti-pattern guards

- Don't gate Apex via simple level grind
- Don't share Mutagen with MBTI PE
- Don't lift ALL Apex constraints (archetype affinities survive)
- Don't skip visual tier-up feedback (P0 confirmed gap)

## Sources verified

- https://store.steampowered.com/app/2004680/Voidling_Bound/
- https://www.voidlingbound.com/
- https://voidlingbound.wiki.gg/wiki/Rarity (Elements page)
- RPG Site / Gaming Debugged / Niche Gamer / Bleeding Cool launch coverage
