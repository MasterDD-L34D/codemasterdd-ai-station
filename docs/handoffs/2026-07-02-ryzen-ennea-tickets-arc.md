# Handoff coordinamento -- Ryzen: arco ticket cross-repo "Ennea Combat Pulse"

> Da: sessione Claude Code coordinatore su Ryzen (DESKTOP-T77TMKT), 2026-07-02 sera.
> A: sessioni Claude attive su Lenovo (MAP-Elites arc, dashboard hub, Game bots) + bot Jules/skiv.
> Scopo: annunciare file target dei 3 ticket residui del seme Ennea Combat Pulse
> (handoff `2026-07-02-ryzen-ennea-combat-pulse-seed.md`) e chiedere non-collisione.
> Seme chiuso: 6 PR mergiate su GGv2 (#560/#566/#570/#571/#572/#575), flag
> `ENNEA_COMBAT_PULSE_ENABLED` default OFF.

## Stato arco: CHIUSO E MERGIATO 2026-07-02 notte (autorizzazione owner)

| Ticket | Stato | PR |
|---|---|---|
| T1 retune Riformatore(1) canon parity | **MERGED** (coppia insieme, 18:53Z) | Game #3184 + GGv2 #579 |
| T2 wire UI toggle "profilazione stile" | **MERGED** (coppia insieme, 18:53Z) | Game #3186 + GGv2 #580 |
| T3 design "SG unit pool port" (v1 refuted, panel 4 lenti) | **MERGED** (doc-only) | GGv2 #583 |
| T3 impl `SgUnitPool` dark module (Stage A, flag OFF) | **MERGED** (squash, CI verde) | GGv2 #584 |

**Decisioni owner RATIFICATE (2026-07-02 notte, autorizzazione esplicita
Eduardo -- merge + raccomandazioni)**:
- Consumer Stoico = **Q2**: resta log_only finche' il retune soglie SG non
  fissa il metric-space; ampiezza decisa DOPO coi numeri del sweep.
- Retune soglie = **sweep-driven**: prima `sg_earn_rate_sweep` per-fascia,
  poi retune canon sui dati (stesso percorso del Riformatore T1).
- TDD del modulo dark `SgUnitPool` SBLOCCATO (fixture: Game
  tests/api/sgTracker.test.js, 12 casi; gate di flip invariati nel design doc).

Codex quota esaurita su tutte le PR -> review interno documentato sui thread.
Non-collisione rispettata: zero overlap coi file MAP-Elites per tutto l'arco.
Worktree rimossi a fine arco (branch restano su origin).

## T1 -- file target (retune trigger Riformatore, canon cross-repo)

Evidenza: QA GGv2 `docs/godot-v2/qa/2026-07-02-ennea-pulse-firing-rate-sweep.md`
esito 3 -- trigger `setup_ratio>0.5 && attack_hit_rate>0.65` strutturalmente
irraggiungibile nel metric-space Godot (ogni attacco diluisce setup_ratio;
EndTurnAction nel ledger peggiora). Retune proposto: `setup_ratio>0.3`,
validato con sweep riproducibile prima della PR.

**ESITO (2026-07-02 sera)**: retune shippato in review. Sweep v4: Riformatore
raggiungibile 3/3 fasce (tactician), zero falsi positivi, copertura mechanical
7/7. GUT 3784 pass / JS 31 pass. PR: Game #3184 + GGv2 #579 (parity, da
mergiare insieme).

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

**ESITO (2026-07-02 notte)**: shippato in review. Backend: pref per-player nel
coop store (character record additive + drain WS intent `profiling_consent_set`
+ broadcast). GGv2: toggle diegetico in PhoneFormPulseView (default ON, mai
lockato) + `MainProfilingConsent` observer host (gate per-unit + amnesia live,
pattern MainLethalConsent), main.gd invariato a 1099 righe. Test: 6/6 JS +
252/252 regressione coop; 16 GUT nuovi, suite 3804 0 fail. PR: Game #3186 +
GGv2 #580 (parity, da mergiare insieme). File toccati in piu' rispetto
all'annuncio iniziale (stesso arco, zero overlap con MAP-Elites):
coop_ws_peer.gd, combat_lifecycle_hook.gd, main{,_combat_setup,_debrief}.gd,
phone_form_pulse_{view,wire}.gd, main_profiling_consent.gd (nuovo);
coopOrchestrator.js, wsSession.js.

## T3 -- Stage A implementato (dark module, flag OFF) -- PR GGv2 #584

Design sistema stress per-unit Godot (Stoico(9) consumer). Il backend scala
`sgTracker.js accumulate(unit,{damage_taken})` PER-UNIT; l'SgTracker Godot e'
l'accumulator GLOBALE Sistema Gravity -- semantica diversa, NON si cabla li'.
Percorso: design doc -> panel critici multi-lente (freeze-compliance,
engine-feasibility, balance/anti-snowball, ops/test) -> TDD del modulo dark.

**ESITO (2026-07-02, Ryzen)**: Stage A MERGED su GGv2 main (squash `0c1efea`,
CI GUT+gdformat verde) -- PR GGv2 #584.
Modulo `scripts/combat/sg_unit_pool.gd` (RefCounted static, pattern
EnneaEffects), parity di meccanismo con `sgTracker.js` (12 casi fixture 1:1),
flag `SG_UNIT_POOL_ENABLED` default OFF. Wire dietro flag: taken in
`CombatSession.apply_damage` (copre attack + status_dot + terrain_dot), dealt
in `resolve_attack_action`, `begin_turn` proxy su EndTurnAction, reset in
`start()`; shield-transfer bond escluso by design. Stoico = Q2 (log_only,
`ennea_effects.gd` NON toccato). Costanti 5/8/3/2 = parity (retune canon =
ticket successivo). Sweep `tools/qa/sg_earn_rate_sweep.gd` conferma verdetto
balance #1: soglie assolute = artefatto scala HP (earn-rate spread 2.3x
cross-band + pinning 0/6->5/6 su fasce 7/15/32); controfattuale relativo
comprime a 1.1x -> dati per il retune in
`docs/godot-v2/qa/2026-07-02-sg-earn-rate-sweep.md`. Test: 19 modulo + 9 wire,
suite GUT 3828 pass / 0 fail, gdformat+gdlint verdi. Review adversarial interno
(4 dimensioni, verify per-finding): 0 finding confermati. VIETATO rispettati:
niente sg nel debrief_payload, zero tocco a SgTracker globale / main.gd.
Worktree dedicato `C:\dev\_worktrees\ggv2-t3-sg-unit-pool` (checkout
principale intatto). **Gate di flip residui** (NON in questa PR): retune soglie
CT-scale, spender DefyEngine riconciliato, HUD gauge SG, ratifica sweep.

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
