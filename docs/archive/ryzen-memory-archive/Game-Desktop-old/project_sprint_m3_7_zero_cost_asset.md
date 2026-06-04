---
name: Sprint M3.7 (2026-04-18) zero-cost asset policy + AI pipeline
description: ADR zero-cost policy + 43-ASSET-SOURCING canonical + CREDITS + README disclaimer. 5 PR autonomous, docs only.
type: project
originSessionId: bacbe4b9-9e50-4dd9-9a8a-c21fcdd04a8a
---
**Sprint M3.7 post-M3.6 — AUTONOMO**. Correzione scope: team = solo-dev + AI curator, no freelance, no budget. 5 PR merged.

## PR state (tutti merged)

| # | Lane | PR | Status |
|---|------|-----|:--:|
| 1 | ADR policy | #1584 zero-cost-asset-policy + AI legal | ✅ merged |
| 2 | Canonical | #1585 43-ASSET-SOURCING.md source_of_truth | ✅ merged |
| 3 | Update 41-AD | #1586 remove freelance refs | ✅ merged |
| 4 | CREDITS+README | #1587 disclaimer template | ✅ merged |
| 5 | Sprint close | #1589 sprint M3.7 doc | ✅ merged |

## Deliverables

### ADR zero-cost-asset-policy

- **70% foundation CC0/MIT**: Kenney + OGA + Lucide + Game-icons + Heroicons + Google Fonts
- **30% gap-fill AI** + human authorship layer obbligatorio
- Tool approvati: Retro Diffusion primary, Adobe Firefly fallback, SDXL+LoRA local, Flux Pro
- Tool NON usabili: Midjourney default, PixelLab.ai, Suno/Udio
- BANNED: LPC (viral CC-BY-SA), Spriters, Pixel Joint
- Disclosure obbligatoria README + in-game credits + Steam

### 43-ASSET-SOURCING.md (source_of_truth)

- Libraries matrix 12 sources + URL + licenza + attribution
- Prompt template AI + divieti (no style replication)
- Human authorship layer 4 steps (palette lock + Libresprite + compositional + provenance)
- Palette master spec: 10 colori funzionali + sub-palette 9 biomi
- Tool editing free (Libresprite/Piskel/Krita/GIMP/ImageMagick/upscayl)
- CLI batch palette lock snippet
- Roadmap 14h MVP slice, 100h full 9 biomi
- Audio stub deferred

### CREDITS.md + README

- Template ready-to-populate
- AI disclosure completo con ethical commitments
- Compliance US Copyright + EU AI Act + Steam policy 2024

## Q-OPEN update

- Q-OPEN-15b: 🔴 artist → 🟡 post-MVP playtest
- Q-OPEN-19b: 🔴 commission → 🟢 AI gap-fill (CHIUDIBILE)

## Gap #1 Art status

- Pre-M3.7: SPEC-COMPLETE (blocked budget)
- Post-M3.7: **PIPELINE-READY** (14h MVP actionable immediately)

## Pattern tecnici

1. **Vincolo team esplicito in ADR**: solo-dev + AI incorporato come first-class constraint nella policy, supersedes implicit "freelance" assumption.
2. **AI legal framework 2026**: US Copyright → human layer sufficiente, EU AI Act → disclosure obbligatoria, Steam → spunta + descrizione workflow. Documented per future compliance.
3. **BANNED list viral license**: LPC CC-BY-SA 3.0 marcata come NON USABILE per commercial safety. Documentation esplicita evita errore futuro.
4. **Human authorship as copyright layer**: palette lock + Libresprite cleanup + compositional decisions = ownership difendibile anche con AI output.
5. **Dependency chain PR cycles**: 5 PR tutti modificano `docs/governance/docs_registry.json` → rebase cascade post-merge ciascuno. Pattern ripetibile.
6. **Branch switching bug recovery**: cherry-pick `git commit` da branch sbagliato al corretto, reset erroneous branch. Safe pattern.

## Follow-up FU-M3.7

| ID | Task | Blocker | Priorità |
|---|------|---------|:-:|
| A | Palette master `.ase` 32 colori (user hands-on) | User tempo | 🟢 |
| B | MVP slice P0+P1 (~14h: palette + 20 icon + 3 biomi) | - | 🟢 |
| C | Verify Retro Diffusion ToS current | - | 🟡 |
| D | Audio direction ADR formalize | Audio lead futuro | ⚪ |

## Memo guardrail rispettati

- Regola 50 righe: tutti PR docs only, zero code
- Nessun file in `.github/workflows/`, `migrations/`, `services/generation/`, `packages/contracts/`
- Trait: zero modifica
- Nessuna dipendenza nuova
- Vincolo team esplicito incorporato in ADR canonical

## Critical path MVP updated

- Pre-M3.7: blocked budget freelance
- Post-M3.7: **actionable immediately** solo-dev + AI
- Tempo stimato MVP visuale: 14h (P0 palette + 20 icon + 3 biomi P1)
- Full 9 biomi + sprite: 100h

## Quirks sessione

- Research agent profondo (1 general-purpose) produce 1550 parole + 40+ URL verificati
- Branch `fix/tkt-06-predict-combat-unit-mod` parallelo (non mia sessione) mergiato su main durante M3.7 → rebase cascade
- Branch switching bug recovery: git checkout -b occasionalmente redirect su altro branch, fix via cherry-pick + reset
- Tutti 5 PR M3.7 rebased + forced-pushed per allinearsi con TKT-06 merge intermedio
- Stash pattern per governance_drift_report.json auto-regenerato
