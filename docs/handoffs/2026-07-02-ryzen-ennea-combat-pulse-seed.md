# Handoff coordinamento -- Ryzen: seme "Ennea Combat Pulse" su Game-Godot-v2

> Da: sessione Claude Code su Ryzen (DESKTOP-T77TMKT), 2026-07-02 pomeriggio.
> A: sessioni Claude attive su Lenovo (viste live: dashboard hub, skiv-monitor, Game bots).
> Scopo: annunciare il lavoro IN PARTENZA su GGv2 per evitare collisioni e permettere follow.

## Stato: DESIGN v2 APPROVATO (post-falsificazione) -- IMPLEMENTAZIONE IN CORSO su branch `feat/ennea-combat-pulse`

### Esito falsificazione (panel 4 critici, run wf_e9b5930f-e10): v1 REFUTED, v2 corretto

Difetti fatali del v1 (evidenza file:riga nel transcript workflow): archetipi Ennea
calcolati solo a session_ended (non "live a inizio round"); PassiveStatusApplier canale
sbagliato (allowlist 7 status, 99 turni); pattern `<stat>_bonus` JS documentato INERTE
nell'engine Godot; indici cumulativi senza decay -> buff de-facto permanente
(anti-snowball violato); soglie = artefatti scala HP; privacy toggle inesistente in GGv2;
3 stat su 5 senza consumer Godot; wire-playtest cieco sui buff client.

### Design v2 (in implementazione)

- Canale buff: riuso pattern beast_bond -- `status['attack_mod_buff'/'defense_mod_buff']`
  consumati da `status_modifiers.aggregate_*` gia' vivi; decay per-turn esistente.
- Timing: fine-round via hook in `combat_lifecycle_hook.gd` (ricomputo pure-fn per-round).
- Trigger: edge-trigger su ACQUISIZIONE archetipo + cooldown 3 round + max 3 trigger/combat
  + winner-take-all 1 archetipo/unita'. Solo fazione player (assert no-SISTEMA).
- Metriche: mini-ledger interno a `ennea_effects.gd` (damage_taken/max_hp normalizzato,
  kills da hp transitions) -- zero edit a vc_scoring*.
- Scope v1: solo attack_mod/defense_mod (archetipi mechanical; altri log_only asseriti);
  Individualista ESCLUSO (incentivo perverso low-HP camping).
- Privacy: nessuna etichetta archetipo esposta; toggle profilazione = debito freeze dichiarato.
- Test: GUT headless, `flag_on` iniettabile, casi da enneaEffectsWire.test.js incluso
  dedup best-per-stat; osservabilita' via debrief_payload.
- Flag: `ENNEA_COMBAT_PULSE_ENABLED` env Godot-side default OFF (pattern G6).
- Footprint: `scripts/ai/ennea_effects.gd` NUOVO + hook minimo in combat_lifecycle_hook.gd
  + test GUT. Quality Gate step 2 = firing-rate sweep HP 7/15/32 PRIMA del flag-flip.

## Cosa e' stato fatto oggi dal Ryzen (gia' pubblicato)

- **Fleet/infra**: SSH Ryzen->Lenovo riparato; parita' plugin CC (last30days 3.8.3, book-to-skill
  pip su entrambe); autoresearch WSL2 setup + runbook -> PR #442 hub (Codex P2 fixato).
- **Igiene GGv2 Ryzen**: branch `docs/creature-portrait-render-first-spec` triagiato SUPERSEDED
  (contenuto tutto su main via #528+, WIP locale identico a main) -> branch+worktree `gv2-hk`
  rimossi, Ryzen ora su main pulito allineato. Refs remoti fantasma pruned.
- **Recon Pillar 4** (Temperamenti): 4 agent paralleli su GGv2 runtime + Game data + vault
  design + telemetria playtest. Esito chiave sotto.

## Scoperta recon (corregge il briefing monitor)

Pillar 4 NON e' fermo: misurazione temperamento VIVA in GGv2 (`vc_scoring.gd`,
`vc_scoring_mbti.gd`, `personality_axes.gd` wired su `action_resolved`), dati Game ~95%
(16 Forme, 9 Ennea, telemetry.yaml), superficie debrief shipped. **Gap unico: zero
espressione in combat** -- il temperamento non tocca mai il gameplay.

## Piano proposto (in verifica): seme "Ennea Combat Pulse"

Chiudere il loop comportamento->effetto visibile, flag-gated OFF:

1. Port `Game/apps/backend/services/enneaEffects.js` -> `GGv2/scripts/ai/ennea_effects.gd`
   (tabella archetipo Ennea -> micro-buff per-round: attack_mod/defense_mod/move_bonus/evasion).
2. Subscribe a VcScoring (gia' vivo): a inizio round, archetipo attivo -> buff via canale
   `unit.traits`/PassiveStatusApplier esistente.
3. Chip diegetico sull'unita' al trigger (pattern imprint hint-chip).
4. Flag Godot-side `ENNEA_COMBAT_PULSE_ENABLED` default OFF (pattern MoveCostField/G6).
5. Test: parity fixture vs enneaEffects.js + asserts wire-playtest (pattern imprint 11/11).

Vincoli rispettati: design freeze 13-14 (soft, micro-trigger secondari, mai hard-lock),
build-on-existing (1 solo file nuovo), stesso pattern QA/flag delle feature G5/G6.

## Coordinamento richiesto alle sessioni Lenovo

- **File che il Ryzen tocchera'** (branch `feat/ennea-combat-pulse`, in arrivo):
  `scripts/ai/ennea_effects.gd` (NUOVO), hook leggero in `main.gd` o
  `combat_lifecycle_hook.gd`, test sotto `tests/`. NON si toccano vc_scoring*/personality_axes.
- **Chiedo**: evitare modifiche concorrenti a `scripts/ai/*` e `PassiveStatusApplier`
  su GGv2 finche' la PR non atterra (stimata: giornata). Tracker-regen/docs/assets = nessun conflitto.
- GGv2 main si muove (tracker-regen di oggi ok): il Ryzen rebasa prima della PR.
- Aggiornamenti di stato: su questa pagina + PR GGv2 quando apre.

## Riferimenti

- Recon completo: transcript workflow Ryzen `wf_c7331a41-e28` (4 reader, 163 tool-use).
- Runbook autoresearch: `docs/runbook/autoresearch-wsl2-fleet-setup.md` (PR #442).
- Design authority temperamenti: vault `core/90-FINAL-DESIGN-FREEZE.md` sect. 13-14,
  `Game/data/core/telemetry.yaml`, `Game/data/core/forms/mbti_forms.yaml`.
