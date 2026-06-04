---
name: Sprint M3.9+M3.10 (2026-04-18) real assets Flint kill-60
description: First real SVG icons + procedural tile generator + Kenney guide. Pipeline asset zero-skill end-to-end.
type: project
originSessionId: bacbe4b9-9e50-4dd9-9a8a-c21fcdd04a8a
---
**Sprint M3.9 + M3.10 post-M3.8 — AUTONOMO close sessione**. Flint design_hint caveman voice ha triggered course correction. User "non so disegnare" → ripensato workflow zero-skill.

## PR merged (3)

| # | Lane | PR |
|---|------|-----|
| M3.9 | First real SVG icons | #1597 (7 custom SVG) |
| M3.10 A | Procedural tile generator Python | #1598 (PIL + 3 tile + 12 test) |
| M3.10 B | Kenney community guide + sprint close | #1599 |

## Deliverables real

### 7 SVG icon custom (M3.9)

`data/art/icons/`:
- faction_player (triangolo blu)
- faction_sistema (rombo rosso)
- faction_neutral (esagono giallo)
- action_attack (slash)
- action_move (freccia)
- action_skip (pause)
- status_stunned (fulmine)

Shape geometrici, zero AI, MIT, palette 42-SG.

### 3 PNG tile procedurali (M3.10 A)

`data/art/tilesets/`:
- savana/grass_01.png (grass tufts + dirt)
- caverna_sotterranea/stone_01.png (cracks + bioluminescenza)
- foresta_acida/moss_01.png (moss + spore)

Via `tools/py/art/generate_tile.py` (Pillow + deterministic RNG + palette lock).

### Kenney community guide (M3.10 B)

`docs/playtest/kenney-community-asset-guide.md` step-by-step download+integrate:
- 3 pack Tier 1 (Roguelike/RPG, Tiny Dungeon, Pixel Platformer)
- Workflow 7-step
- User effort 45 min zero-skill

## Flint kill-60 enforcement finale

| Metric | Pre-sessione | Post-M3.10 |
|--------|:---:|:---:|
| SVG icon | 0 | **7** |
| PNG tile | 0 | **3** |
| Python generator | 0 | **1** (12 test) |
| Docs pipeline | spec only | asset-committed ✅ |
| Scope debt | 🔴 22 PR docs vs 0 asset | 🟢 pipeline dimostrata |

## Pattern tecnici acquisiti

1. **Flint voice = course correction signal**: caveman design_hint "0 pixel committed" ha triggered re-scope. Memory Flint → ripensare path concreto.
2. **Custom SVG = zero-license path**: shape geometrici authored from scratch = copyright 100% clean, zero attribution requirement.
3. **Python PIL procedural = zero-skill path**: Pillow install + algorithm custom → N tile PNG deterministic. 0 user drawing.
4. **Kenney CC0 workflow**: download ZIP → extract → copy → CREDITS update. 45 min zero-skill.
5. **A+C combo 95% time save**: 46 min vs 14h playbook M3.8 originale.
6. **Deterministic RNG**: hash-based seed biome+variant → idempotent output. Commit stabile cross-run.
7. **Naming convention cross-fonte**: `<type>_01.png` (procedural) vs `<type>_kenney_01.png` (community) → game code consuma entrambi same path.

## Q-OPEN closed sessione totale (10)

- Q-OPEN-15, 19, 22, 26, 27 (M3.6 art direction)
- Q-OPEN-19b (M3.7 AI gap-fill, M3.10 procedural path zero-cost)
- Q-OPEN-21, 24 (M3.8 audio direction)

Residue (post-M3.10):
- Q-OPEN-15b (budget frame T3)
- Q-OPEN-25 (day/night cycle)
- Q-OPEN-26b (icon set definitivo)
- Q-OPEN-27b (light mode UI)

## Gap GDD finale

- **#1 Art**: PIPELINE-READY + **ASSET-COMMITTED** (7 icon + 3 tile + generator Python)
- **#2 Audio**: SPEC-COMPLETE + PIPELINE-READY (deferred post-MVP visuale)
- **#3 Levels**: SPEC-COMPLETE (M3.5 sprint, 9 encounter YAML + 4 non-elim)

## Follow-up FU-M3.10

| ID | Task | Blocker | Priorità |
|---|------|---------|:-:|
| A | User run Kenney guide (45 min Tier 1) | User tempo | 🟢 |
| B | Estendere procedural patterns (sand/water/crystal) | Algorithm design | 🟡 |
| C | Sprite character procedural | Algorithm complex | ⚪ |
| D | Audio MVP slice (freesound + Bfxr) | User tempo + ADR step 1-2 | ⚪ |

## Sessione totale metriche

- **25 PR merged**: 22 docs + 1 SVG + 2 procedural/community
- **10 Q-OPEN closed**
- **7 icon SVG** + **3 PNG tile** + **1 Python generator** + **12 test unit**
- **Zero dep npm nuova** (Pillow on-demand Python)
- **Governance**: 0 errors finale
- **Flint kill-60**: ENFORCED

## Critical path MVP (close state)

- Art direction: ✅ ASSET-COMMITTED
- Audio direction: SPEC-COMPLETE + PIPELINE-READY
- Playtest batch: harness ready
- Blockers rimasti: user tempo (45 min Kenney) + playtest schedule

## Quirks sessione memorabili

- Flint caveman voice = best course correction tool di sessione
- User domanda "non so disegnare" ha rivelato gap playbook M3.8 (assumeva Libresprite skill)
- C+A combo pattern riusabile per future asset (audio, sprite, UI)
- Branch switching bug recovery pattern repeated 3-4 volte (cherry-pick + amend)
- Pillow install on-demand Python 3.13 (Python 3.14 system no packages)
