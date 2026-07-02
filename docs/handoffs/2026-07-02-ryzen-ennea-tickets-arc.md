# Handoff coordinamento -- Ryzen: arco ticket cross-repo "Ennea Combat Pulse"

> Da: sessione Claude Code coordinatore su Ryzen (DESKTOP-T77TMKT), 2026-07-02 sera.
> A: sessioni Claude attive su Lenovo (MAP-Elites arc, dashboard hub, Game bots) + bot Jules/skiv.
> Scopo: annunciare file target dei 3 ticket residui del seme Ennea Combat Pulse
> (handoff `2026-07-02-ryzen-ennea-combat-pulse-seed.md`) e chiedere non-collisione.
> Seme chiuso: 6 PR mergiate su GGv2 (#560/#566/#570/#571/#572/#575), flag
> `ENNEA_COMBAT_PULSE_ENABLED` default OFF.

## Stato arco: IN CORSO (aggiornare a ogni milestone)

| Ticket | Stato | PR |
|---|---|---|
| T1 retune Riformatore(1) canon parity | IN CORSO | Game: TBD, GGv2: TBD |
| T2 wire UI toggle "profilazione stile" | PENDING | - |
| T3 design+falsificazione stress per-unit (Stoico consumer) | PENDING | design PRIMA di codice |

## T1 -- file target (retune trigger Riformatore, canon cross-repo)

Evidenza: QA GGv2 `docs/godot-v2/qa/2026-07-02-ennea-pulse-firing-rate-sweep.md`
esito 3 -- trigger `setup_ratio>0.5 && attack_hit_rate>0.65` strutturalmente
irraggiungibile nel metric-space Godot (ogni attacco diluisce setup_ratio;
EndTurnAction nel ledger peggiora). Retune proposto: `setup_ratio>0.3`,
validato con sweep riproducibile prima della PR.

- **Game** (branch `feat/ennea-riformatore-retune`, worktree `C:\dev\_wt-game-ennea-t1`):
  - `data/core/telemetry.yaml` (ennea_themes, r.90-92) -- CANON.
  - `data/core/narrative/ennea_voices/type_1.yaml` (commento mirror r.7).
  - `tests/services/enneaEffectsWire.test.js` (fixture trigger r.372-391).
- **GGv2** (branch `feat/ennea-riformatore-retune`, worktree `C:\dev\_wt-ennea-t1`):
  - `scripts/ai/vc_scoring.gd` (r.52 commento + r.269-271 `_eval_ennea_triggers`).
  - `tests/unit/test_vc_scoring_full.gd` (fixture parity se tocca soglia).
  - `docs/godot-v2/qa/2026-07-02-ennea-pulse-firing-rate-sweep.md` (rerun sweep v4).
  - `tools/qa/ennea_firing_rate_sweep.gd` solo se serve probe nuovo.

## T2 -- file target (privacy toggle, dopo T1)

Runtime pronto da GGv2 #575 (`profiling_opt_out`, `set_ennea_profiling_consent`,
`ennea_amnesia`). Da toccare:

- **Game backend**: pref per-player nel coop store (pattern
  `session.profilingConsent`, `apps/backend/routes/session.js:4418+`).
- **GGv2 phone UI**: toggle diegetico (pattern `scripts/phone/phone_form_pulse_view.gd`).
- **GGv2 host wiring**: pref -> `profiling_opt_out` su unit roster + consent hook.

## T3 -- nessun file finche' design non falsificato

Design sistema stress per-unit Godot (Stoico(9) consumer). Il backend scala
`sgTracker.js accumulate(unit,{damage_taken})` PER-UNIT; l'SgTracker Godot e'
l'accumulator GLOBALE Sistema Gravity -- semantica diversa, NON si cabla li'.
Percorso: design doc -> panel critici multi-lente (freeze-compliance,
engine-feasibility, balance/anti-snowball, ops/test) -> solo dopo TDD.

## Richiesta non-collisione

- Evitare modifiche concorrenti a: `scripts/ai/vc_scoring.gd` + tests ennea (GGv2),
  `data/core/telemetry.yaml` + `tests/services/enneaEffectsWire.test.js` (Game)
  finche' le PR T1 non atterrano (stima: serata).
- Overlap verificato 2026-07-02 sera: Game #3183 (MAP-Elites edm, docs/playtest +
  tools calibration) e hub #460 = ZERO overlap coi file sopra. GGv2 nessuna PR aperta.
- Il checkout principale `C:\dev\Game-Godot-v2` NON viene toccato (worktree only).

## Riferimenti

- Handoff seme: `docs/handoffs/2026-07-02-ryzen-ennea-combat-pulse-seed.md`.
- QA sweep: GGv2 `docs/godot-v2/qa/2026-07-02-ennea-pulse-firing-rate-sweep.md`.
- Design authority: vault `core/90-FINAL-DESIGN-FREEZE.md` sect.13-14 (Enneagramma
  = micro-trigger secondari, soglie calibrabili) + `11-REGOLE_D20_TV.md` r.28.
