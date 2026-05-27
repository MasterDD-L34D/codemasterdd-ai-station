---
name: Machinations balance models (Evo-Tactics)
description: 4 modelli di bilanciamento visuale specificati in docs/balance/MACHINATIONS_MODELS.md per validare Pilastro 6 Fairness
type: project
originSessionId: ad853972-71c9-44d5-8ef0-7f655955b921
---
Machinations.io integrato come tool di bilanciamento visuale per Evo-Tactics. 4 modelli specificati in `docs/balance/MACHINATIONS_MODELS.md` (added 2026-04-17, registry entry + cross-ref in `docs/guide/external-references.md`):

1. `d20_attack_economy` — d20 vs DC con MoS tiers, dati da `trait_mechanics.yaml` + `terrain_defense.yaml`. Verify contro `predict_combat.py` (N=1000).
2. `pt_pool_combo_meter` — accumulo PT e soglie combo (3/6/10), dati da `roundOrchestrator.js` + `action_speed.yaml`.
3. `damage_step_fairness_cap` — overflow DAMAGE_STEP_CAP su N turni, flag in `trait_balance_summary.md`.
4. `status_propagation_decay` — 7 status (panic/rage/stunned/focused/confused/bleeding/fracture), decay vs cleanse gate, dati da `statusEffectsMachine.js`.

**Why:** Pilastro 6 Fairness passato da 🟡 a 🟢, ma mancava tool visuale per calibrare. Machinations è documentazione, non autorità — source of truth rimane YAML + rules engine Python.

**How to apply:** quando tocchi balance YAML o roundOrchestrator.js, rerun il modello pertinente nel tool, diff con output Python, documenta in PR. File `.machinations` da salvare in `docs/balance/machinations/` (da creare primo export).
