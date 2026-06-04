---
name: GDD Audit — Evo-Tactics vs GDDMarkdownTemplate
description: Coverage matrix mapping 13 GDD standard sections against docs/core/ — identifies 3 critical gaps (levels, art, audio), 7 significant gaps, 7 strong areas
type: reference
---

# GDD Audit (2026-04-16)

Matrice confronto GDDMarkdownTemplate (13 sezioni standard) vs docs/core/ + hubs.

## Matrice di Copertura

| # | Sezione GDDTemplate | Stato | File(s) | Gap |
|---|---|---|---|---|
| 1 | Copyright | ❌ | — | Nessun doc copyright/licensing |
| 2 | Version History | ✅ | 90-FINAL-DESIGN-FREEZE.md, changelog in planning/ | OK |
| 3 | Game Overview | ✅ parziale | 01-VISIONE, 02-PILASTRI, 03-LOOP, DesignDoc-Overview | **Target Audience** non esplicito. **Look & Feel** assente. **Project Scope** (counts) non formalizzato |
| 4 | Gameplay & Mechanics | ✅ forte | 10-SISTEMA_TATTICO, 11-REGOLE_D20_TV, 25-REGOLE_SBLOCCO_PE, combat.md, PI-Pacchetti-Forme | **Screen Flow** chart assente. **Save/Load** non documentato. **Game Options** assente |
| 5 | Story, Setting & Character | ✅ parziale | 28-NPC_BIOMI_SPAWN, 20-SPECIE_E_PARTI, 22-FORME_BASE_16, SistemaNPG-PF-Mutazioni | **Narrative/Plot** assente. **Character sheets** assente — manca lore framing |
| 6 | Levels | ❌ | — | Level design doc completamente assente |
| 7 | Interface | ✅ parziale | 30-UI_TV_IDENTITA, docs/frontend/ | **Audio design** assente. **Controls mapping** assente. **Help/tutorial** non documentato |
| 8 | Artificial Intelligence | ✅ forte | ai-policy-engine.md, declareSistemaIntents.js, policy.js | **Player AI assistance** (hints) non documentato |
| 9 | Technical | ✅ parziale | docs/adr/, hubs/backend.md, hubs/flow.md | **Hardware req** assente. **Networking arch** non formalizzato. **Perf targets** assente |
| 10 | Game Art | ❌ | — | Art direction completamente assente |
| 11 | Secondary Software | ✅ parziale | trait-editor.md, Mission Console | **Installer/distribution** assente. **Update system** assente |
| 12 | Management | ✅ parziale | 40-ROADMAP, hubs/ops-qa.md, planning/ | **Budget** assente. **Risk matrix** assente. **Localization** assente. **QA test plan** strutturato assente |
| 13 | Appendices | ❌ | — | Nessun asset inventory audio/visual |

## Gap per priorità

### 🔴 Critici (sezioni mancanti)
1. **Level Design** — nessun doc livelli/mappe/encounter concreti
2. **Art Direction** — zero concept art, style guide, asset pipeline
3. **Audio Design** — nessun doc sound, music, SFX

### 🟡 Significativi (sezione parziale)
4. Target Audience — player personas assenti
5. Screen Flow — chart navigazione schermate mancante
6. Narrative/Lore — manca framing narrativo (backstory, plot hook, tono)
7. Save/Load system — non documentato
8. Networking architecture — co-op è pilastro ma design rete non formalizzato
9. Risk matrix — nessun risk register formale
10. Controls mapping — input non documentato

### 🟢 Forte (copertura eccellente)
- Combat system & d20 mechanics
- AI Sistema (policy engine + intents)
- Progression & economy (PE, pacchetti, sblocchi)
- Temperaments (MBTI/Ennea + VC telemetry)
- Species & traits pipeline
- Tooling & validation
- Governance & design freeze
