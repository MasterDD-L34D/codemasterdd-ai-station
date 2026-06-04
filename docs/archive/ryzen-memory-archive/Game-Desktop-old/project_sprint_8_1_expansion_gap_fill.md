---
name: Sprint 8.1 ability r3/r4 expansion gap-fill 2026-05-05
description: PR #2057 shipped main 626ecb51 — 8 ability r3/r4 (4 expansion job × 2 tier) close roster 11/11 r1→r4. Pillar P3 🟢ⁿ → 🟢++.
type: project
originSessionId: 6b247de8-9e20-4fe4-b925-7b812e67f1b4
---
# Sprint 8.1 Ability r3/r4 Expansion Gap-Fill (codename snoopy-milner)

**Merged main**: PR [#2057](https://github.com/MasterDD-L34D/Game/pull/2057) squash SHA `626ecb51` (2026-05-05).

## Audit trigger

Audit 2026-05-05 ha rilevato 4 expansion job orphan (`data/core/jobs_expansion.yaml`): Stalker, Symbiont, Beastmaster, Aberrant — solo r1/r2 wired. PR #1978 originale (Sprint 8 Tier S #6 closure) shippò r3/r4 sui **7 base** ma non sui 4 expansion. Codename interno: "snoopy-milner".

## Decisione + ship

Estendere stesso cost ladder canonical (r3=14 / r4=22 PI) ai 4 expansion. **Stesso vincolo runtime PR #1978 preservato**: zero nuovi `effect_type` runtime, extension data-only.

### 8 ability shipped

| Job         | r3 (cost_pi=14)     | effect_type | r4 (cost_pi=22)     | effect_type      | Resource gate r4 |
| ----------- | ------------------- | ----------- | ------------------- | ---------------- | ---------------- |
| stalker     | shadow_mark         | debuff      | shadow_assassinate  | execution_attack | PP ≥ 10          |
| symbiont    | bond_amplify        | team_buff   | unity_surge         | team_heal        | PT ≥ 8           |
| beastmaster | feral_dominion      | aoe_buff    | apex_pack           | aoe_buff         | PT ≥ 10          |
| aberrant    | stabilized_mutation | buff        | perfect_mutation    | surge_aoe        | SG ≥ 80          |

### Files modificati (6, scope chiuso ~408 LOC)

- `data/core/jobs_expansion.yaml` — v0.2.0 → v0.3.0
- `tests/api/jobs.test.js` — +4 test (expansion ladder + naming + version + rank sort), 14→18
- `tests/api/abilityExecutor.test.js` — +5 r4 smoke (dervish/headshot/apocalypse/lifegrove + shadow_assassinate), 36→41
- `docs/adr/ADR-2026-04-27-ability-r3-r4-tier.md` — §6 expansion roster
- `docs/balance/2026-04-27-numeric-reference-canonical.md` — §12 expansion table
- `BACKLOG.md` — close-mark 2026-05-05

## Outcome

- **Coverage**: 11/11 job r1→r4 wired (7 base + 4 expansion)
- **Pillar P3** (Identità Specie × Job): 🟢ⁿ → 🟢++
- **Test gate**: jobs+abilityExecutor 59/59 + AI 383/383 zero regression
- **CI**: stack-quality + dataset-checks + governance + tutti gate verde

## Lessons

- **Audit catalog mirror**: `npm run sync:evo-pack` può applicare format drift unrelated (60+ species files multiline JSON). **Revert pattern**: `git checkout -- docs/evo-tactics-pack/ packs/evo_tactics_pack/docs/catalog/ public/docs/evo-tactics-pack/` quando drift NON correla allo scope corrente.
- **Plan deviation**: CLAUDE.md sprint context append SKIPPED per "max 3 sprint context" policy già satura. BACKLOG entry sufficiente per traceability.
- **Codename surface**: User ha rivelato "snoopy-milner" = codename interno feature, non entità di gioco. Plan filename hint sufficiente per disambiguare scope tra Sprint 8 originale e Sprint 8.1 gap-fill.
- **r4 smoke pattern**: Tutorial scenario p_scout/p_tank ha resource pool sufficiente per dispatch r4 capstone (cost_pp=10/12, cost_sg=100, cost_pt=10). `stress_after` post-surge_aoe undefined se SG insufficient — assertion soft-coded a effect_type + ability_id verify only.

## Userland pending post-merge

- `npm run sync:evo-pack` lato Game/ (rebuild catalog mirror — Sprint 8.1 NON tocca species, drift unrelated)
- `npm run evo:import` lato Game-Database (catalog import)

## Anti-pattern preservato

Vincolo PR #1978 mantenuto: zero nuovi `effect_type` runtime → zero modifica `abilityExecutor.js`. Tutte 8 ability nuove riusano i 18 effect_type esistenti (debuff, execution_attack, team_buff, team_heal, aoe_buff, buff, surge_aoe). Extension data-only.

## Wire verify post-merge (2026-05-05)

Backend live + 6/6 surface check verde:

- ✅ `/api/jobs` count=11 + `ability_ids` broadcast nuovi
- ✅ `/api/jobs/:id` ritorna 5 ability per ciascun expansion (alpha_strike+silent_step+deathmark+shadow_mark+shadow_assassinate per stalker, ecc.)
- ✅ `/api/session/action` dispatch live verde 8/8 (shadow_mark→debuff, shadow_assassinate→execution_attack, bond_amplify→team_buff, unity_surge→team_heal, feral_dominion→aoe_buff, apex_pack→aoe_buff, stabilized_mutation→buff, perfect_mutation→surge_aoe)
- ✅ Frontend `apps/play/src/{abilityPanel.js:57, codexPanel.js:420, ui.js:152}` iterano `abilities[]` dinamicamente — auto-respect senza modifiche
- ✅ Mission Console pre-built Vue bundle fetcha runtime via `/api/jobs` — auto-respect
- ✅ Catalog mirror (`docs/evo-tactics-pack/`, `packs/evo_tactics_pack/docs/catalog/`) NON contiene jobs (solo species/biomes/traits) → **Sprint 8.1 fuori scope mirror**, nessun regen necessario per Game-Database side

**Conclusione**: wire 100% complete senza userland chore. Game-Database integration HTTP runtime feature-flagged OFF (`GAME_DATABASE_ENABLED=false`) — l'unico flusso jobs è live API runtime, non build-time import.
