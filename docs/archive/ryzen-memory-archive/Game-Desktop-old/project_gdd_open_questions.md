---
name: GDD Open Questions (28 domande dai draft) — CHIUSE 2026-04-17
description: 28 domande tutte chiuse. Decisioni Master DD prese sessione 2026-04-17 sera.
type: project
originSessionId: eeb0e45f-ed5d-4d5a-93c6-7fe32981f362
---
# GDD Open Questions — Tutte chiuse (2026-04-17)

28 domande decise. Aggiornato sessione serale 17/04 con batch Master DD.

## Decisioni finali

### Business / Identity

| # | Q | Decisione |
|---|---|---|
| 1 | Modello business | **Early Access Steam → premium 1.0** (indie tattico niche, no F2P) |
| 2 | Rating PEGI | **PEGI 16** (taglio adulto alla Mewgenics) |
| 3 | Localizzazione | **it+en al lancio**, i18n-ready (glossary già bilingue) |

### Art Direction

| # | Q | Decisione |
|---|---|---|
| 4 | Stile rendering | **2.5D isometrico** (leggibilità FFT-like, scala indie, TV-friendly) |
| 5 | Animazioni | **Sprite animato 4-8 frame/azione** (idle, move, attack, hit, ko) |
| 6 | Budget asset/creatura | **Medio** (sprite multi-stato, no 3D rig) |
| 7 | Moodboard | **Rimanda**: 3 ref al prossimo sprint art (FFT, Wargroove, Into the Breach) |
| 8 | Asset pipeline | **Aseprite primary + Blender opzionale** per backgrounds iso |

### Audio

| # | Q | Decisione |
|---|---|---|
| 9 | Budget musicale | **freesound.org prototype → asset pack produzione** (no composer MVP) |
| 10 | Voci creature | **Solo SFX ambientali/azione**, nessuna voce (bio-plausibile) |
| 11 | Volume default | Musica 70%, SFX 100%, master 80% |
| 12 | Prototype audio | freesound.org |

### Level design / Narrative / UX (già chiuse o confermate)

| # | Q | Decisione |
|---|---|---|
| 13 | Editor livelli | YAML manuale |
| 14 | Procedurale vs hand-crafted | Hand-crafted + wave procedurale |
| 15 | Formula difficulty | §15.4 SoT |
| 16 | Livelli co-op/PvP | **Solo co-op vs Sistema al lancio** (PvP/raid post) |
| 17 | Schema AJV encounter | `schemas/evo/encounter.schema.json` |
| 18 | Procedurale vs scritta | Mix: Ink briefing + Director/StressWave |
| 19 | Voice-over | Solo testo |
| 20 | NPC named | **Pattern A (Sistema-centric)**: creature anonime + Sistema unica voce Ink multi-profile (Calm→Apex). Hooks per Pattern B (Overlord + Custodi named) se playtest chiede calore umano |
| 21 | Tool narrativo | Ink (inkjs) |
| 22 | Accessibilità | Colorblind + difficoltà scalabile al lancio, TTS post |
| 23 | Deaf indicators | Indicatori visivi |
| 24 | Tutorial | Integrato nei primi encounter |
| 25 | Matchmaking | In lobby |
| 26 | Loading screen | Tip durante loading |
| 27 | Replay match | Event log replayable nel debrief |
| 28 | Controlli | Controller primary + keyboard + touch companion |

## Pattern narrativo D5 (Q20) — piano a due fasi

**Decisione Master DD 2026-04-17**: transizione pianificata, no opt-in incerto.

### Fase 1 (ora → MVP/EA): Pattern A Sistema-centric

- **Chi parla**: Solo Sistema (1 voce antagonista, multi-profile in `ai_profiles.yaml`)
- **Creature player**: mute, slot anonimi ("Wolf-03")
- **Integrazione**: mappa `sistema_pressure` tier (Calm/Apex) → ink knot selection in `services/narrative/narrativeEngine.js`
- **Estensione**: `ai_profiles.yaml` gets `narrative_voice` per profilo
- **Costo**: Basso (300-500 LOC ink, zero deps, zero refactor schema)
- **Perché ora**: non abbiamo ancora una storia scritta; Pattern A preserva emergent identity durante EA playtest.

### Fase 2 (quando scriviamo storia): transizione a Pattern B — Overlord + Custodi named (Descent ibrido)

- **Trigger**: green-light Master DD post-EA playtest → apertura workstream narrative campaign / story mode.
- **Contenuto**: 2-4 Custodi named (background + barks + skill narrativi, no meccaniche) + Ink multi-speaker + campaign arc strutturato.
- **Continuità**: Sistema persiste come Overlord cross-campaign. Custodi = layer sopra.
- **Reference repos tracciati** per story writing:
  - **Descent: Road to Legend** (FFG campaign structure) — Overlord plot-card rhythm, quest branching
  - **wesnoth/wesnoth** — campaign dialogue WML `[message]`, leader named come unità giocabile
  - **inkle/ink** + **inkle/inky** — multi-speaker knot, IDE writing
  - **OpenRA/OpenRA** — mission briefing + campaign scripting
  - **FFT War of the Lions** — acted scenes pattern named+generics
- **Cross-ref**: aggiornamento `reference_external_repos.md` quando apriamo fase 2 (promozione tier narrative-focus).

Alternative scartate:
- **Pattern C** (Comandante player-named): poca caratterizzazione autoriale, manca anchor narrativo.
- **Pattern D** (Ramza-light): single POV contraddice ownership co-op.
- **Descent puro**: Heroes named fissi contraddice creature modulari.

## Prossimi passi

1. Doc canonical: scrivere `docs/core/00F-ART_AUDIO_BUSINESS.md` con decisioni A/B/C (Master DD approval)
2. Art direction brief: 3 reference moodboard nel prossimo sprint art
3. Estendere `ai_profiles.yaml` con `narrative_voice` per pattern A (Q20 implementation)
4. Nessuna Q rimanente — triage v2 chiuso ufficialmente.
