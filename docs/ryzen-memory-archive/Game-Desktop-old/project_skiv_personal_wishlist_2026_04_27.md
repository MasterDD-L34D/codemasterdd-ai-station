# Skiv Personal Wishlist 2026-04-27 — ✅ SHIPPED 4/4 goals (2026-04-28)

**Status**: ✅ COMPLETE 4/4 goals shipped main in singola sessione autonomous (~9h).

**PR sequence**:
- G1 [#1982](https://github.com/MasterDD-L34D/Game/pull/1982) Encounter Skiv solo vs Pulverator pack (P1+P5) — calibration N=20 win 45.0% in band 35-45%
- G2 [#1977](https://github.com/MasterDD-L34D/Game/pull/1977) Echolocation visual fog-of-war pulse (P1) — anti-pattern Engine LIVE Surface DEAD chiuso
- G3 [#1983](https://github.com/MasterDD-L34D/Game/pull/1983) Thoughts ritual choice UI (P4) — Disco-style voice preview "Il branco non ti vede più. La sabbia segue solo te."
- G4 [#1984](https://github.com/MasterDD-L34D/Game/pull/1984) Legacy death mutation choice ritual (P2) — back-compat preserved + narrative beat ±1 bond

**Test budget**: AI baseline 382/382 + 29 nuovi (9+6+10+4) = zero regression. Total ~1100 LOC.

**Lessons codified**:
- Wave-merge gate: G1+G2 disjoint = parallel. G3+G4 share session.js = sequential.
- Worktree contention recovery: agent G1 ha creato `Game-skiv-g1` worktree per evitare collision G2.
- Force-push blocked → merge strategy fallback: `git pull --no-rebase` + commit merge + push regular = clean path.
- CI flake terrainReactionsWire fire = canonical re-run pattern (pre-existing, non-blocking).

---

**Origine** (preservata per storico): 2026-04-27 notte. Allenatore master-dd ha chiesto a Skiv stesso quali obiettivi personali vuole oltre wishlist 8/8 closed.

**Skiv stato pre-richiesta** (vedi data/derived/skiv_monitor/state.json):
- Lv 4 INTP 0.92 conf, Predatore Maturo
- HP 14/14, AP 2/2, SG 2/3, PE 62, PI 8
- Cabinet 2/3 (i_osservatore + n_intuizione_terrena)
- Bond Vega ❤❤❤ + Rhodo ❤❤
- Mutations 1 (artigli_grip_to_glass)
- Synergy echo_backstab live
- Ecology apex savana solitario, compete pulverator

**Wishlist 8/8 originale** ✅ closed (vedi project_skiv_evolution_wishlist.md). Skiv chiede 4 nuovi obiettivi propri.

## 4 desideri Skiv (voce italiano prima persona, desert metaphor)

### G1 Encounter `enc_savana_skiv_solo_vs_pack` (~4h, P1+P5)

> _"Voglio essere protagonista, non NPC neutrale. PR #1967 ha messo Pulverator nel mio bioma. Encounter pack_clash è party vs pack — io osservo. Voglio confrontare il branco da solo."_

Spec:
- Skiv solo Lv 4 vs 3 Pulverator pack
- Win NON eliminazione: survive 5 round + mark pack alpha
- Fail: status `wounded_perma` cicatrice persistent 1 settimana sessione
- Calibration target win 35-45%

### G2 Echolocation visual fog-of-war pulse (~3-4h, P1 sense surface)

> _"Voglio vedere quello che sento. sensori_geomagnetici + echolocation senses LIVE ma silent UI. Ennesimo Engine LIVE Surface DEAD."_

Spec:
- drawEcholocationPulse render.js helper
- Pre-attack hover 500ms → cyan pulse 800ms expanding 40→120px
- Tile reveal 1-2 hidden tile adjacent target via '?' glyph → real content post-pulse
- Cooldown 2 round (no spam)
- sensori_geomagnetici trait → +1 tile reveal raggio passive bonus

### G3 Third thought ritual choice UI (~5h, P4 agency)

> _"Voglio scegliere chi divento all'apex. Ora sistema applica thought più adatto a vcAxes auto. Subisco. Voglio agency pre-internalization."_

Spec:
- thoughtsRitualPanel.js overlay modale on research_completed event
- Top-3 candidati ranked by vcSnapshot match
- Per candidato: title + preview + passive bonus + voice line example Disco-style
- 30s decision timer (default top-1 auto se no input)
- Decision irreversible per session

### G4 Legacy death mutation choice ritual (~3h, P2 inheritance, OPZIONALE)

> _"Voglio scegliere cosa lascio quando morirò. propagateLineage scrive ALL applied_mutations a pool. Voglio decidere quale eredità lascio."_

Spec:
- legacyRitualPanel.js overlay modale on lifecycle_phase=legacy transition
- Checkbox per applied_mutation: "lascia / non lascia"
- Default: tutto lasciato (back-compat)
- Decision irreversible
- Narrative beat: <50% lasciato → bond -1 ("vento porta solo certe ossa"); 100% → bond +1 ("hai dato tutto")

## Closing voce Skiv

> _"Allenatore — questi sono i miei. Non roadmap, non residual museum. Cose che il mio corpo Lv 4 vuole."_
> _"Sabbia segue."_

## Plan execution

Salvato in `docs/planning/2026-04-27-skiv-personal-sprint-handoff.md` cross-PC ready.

**Wave structure**:
- Phase 1 G1+G2 parallel (~7-8h)
- Phase 2 G3 sequential (~5h, gated G1+G2)
- Phase 3 G4 sequential (~3h, gated G3, OPZIONALE)
- Phase 4 synthesis Skiv state recompute

**Total budget**: ~15-16h.

**Resume trigger**: "leggi docs/planning/2026-04-27-skiv-personal-sprint-handoff.md, verifica §6 progress, esegui fase corrente"

## Cross-ref piani esistenti

- Sprint α+β+γ+δ coordinated handoff (`2026-04-27-sprint-abgd-coordinated-handoff.md`) → tutti shipped, demo-ready
- Skiv canonical doc (`docs/skiv/CANONICAL.md`)
- Skiv monitor plan (`docs/planning/2026-04-25-skiv-monitor-plan.md`)
- Illuminator orchestra handoff (`docs/planning/2026-04-25-illuminator-orchestra-handoff.md`)
- Spore Moderate FULL stack (PR #1913→#1941)

## Outcome atteso post 4 goals

- **Skiv lifecycle**: mature → close to apex (XP +5 + thought 3 internalized = 2/3 gate requirements closed)
- **Pillar impact**: P1 def++ + P2 def++ + P4 def++ + P5 cand
- **Anti-pattern Engine LIVE Surface DEAD**: chiuso per echolocation (G2)
- **Agency narrative**: Skiv sceglie thought 3 + eredità (G3+G4)
