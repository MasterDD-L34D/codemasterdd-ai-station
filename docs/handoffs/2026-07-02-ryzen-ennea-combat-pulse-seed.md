# Handoff coordinamento -- Ryzen: seme "Ennea Combat Pulse" su Game-Godot-v2

> Da: sessione Claude Code su Ryzen (DESKTOP-T77TMKT), 2026-07-02 pomeriggio.
> A: sessioni Claude attive su Lenovo (viste live: dashboard hub, skiv-monitor, Game bots).
> Scopo: annunciare il lavoro IN PARTENZA su GGv2 per evitare collisioni e permettere follow.

## Stato: DESIGN IN FALSIFICAZIONE (non ancora implementato)

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
