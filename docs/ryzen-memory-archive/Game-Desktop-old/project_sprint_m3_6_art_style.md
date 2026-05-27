---
name: Sprint M3.6 (2026-04-18) art direction + style guide canonical
description: ADR art-direction ACCEPTED + 41-AD + 42-SG + encounter visual_mood + styleguide lint. 6 PR autonomous, docs/schema/tools only.
type: project
originSessionId: bacbe4b9-9e50-4dd9-9a8a-c21fcdd04a8a
---
**Sprint M3.6 post-M3.5 — AUTONOMO**. 6 PR chain per art direction + UI style guide canonicali. Docs/schema/tools only, zero code change runtime.

## PR state

| # | Lane | PR | Status |
|---|------|-----|:--:|
| 1 | ADR accept | #1577 art-direction DRAFT→ACCEPTED | ✅ merged |
| 2 | Canonical | #1578 docs/core/41-ART-DIRECTION.md | ✅ merged |
| 3 | Canonical | #1579 docs/core/42-STYLE-GUIDE-UI.md | ✅ merged (rebase + force push) |
| 4 | Schema+data | #1580 encounter visual_mood + 9 retrofit | 🟡 CI pending |
| 5 | Tools | #1581 styleguide_lint.py + 10 test | 🟡 CI pending |
| 6 | Sprint close | #1582 docs/process/sprint-m3-6 | 🟡 CI pending |

## Deliverables

### 41-ART-DIRECTION.md (source_of_truth)

- 4 pillars: leggibilità tattica, specie carattere, biomi atmosferici, TV-first
- Direzione "naturalistic stylized" in pixel art (Into the Breach + AncientBeast)
- Pixel art spec: 32×32 tile, 10-16 frame sprite, palette indexed, integer upscaling
- Silhouette language 7 job
- **Palette matrix 9 biomi shipping** con HEX + accent + mood + light direction
- 10 colori funzionali universali
- UI hierarchy 6 livelli
- Accessibility gate (colorblind, contrast ≥4.5:1, scale S/M/L)
- Asset commission spec MVP per freelance

### 42-STYLE-GUIDE-UI.md (source_of_truth)

- Colors: 10 semantic + 6 surface + 4 text + 4 state (contrast ratio)
- Typography: Inter/Noto Sans, 8 scale TV-first (14-72px), 4 weight
- Spacing base 4px, 11 token
- Radius 6 token, Shadows 6 token
- Icon grid 16/24/32/48
- Component patterns button/card/tooltip/modal/unit card
- Accessibility WCAG 2.1 AA
- Responsive tv-1080p/tv-4k integer 2x
- Motion 150-500ms, prefers-reduced-motion
- Z-index 9 token

### Encounter visual_mood

Schema extension + 9 retrofit YAML (mood_tag, lighting, particle_effect, accent_override).

### Styleguide lint tool

`tools/py/styleguide_lint.py` — 5 check rules cross-document. 10/10 unit test.

## Q-OPEN closed (5)

- Q-OPEN-15: stile creature = naturalistic stylized pixel art
- Q-OPEN-19: palette biomi = matrix 9 shipping
- Q-OPEN-22: UI language = flat + alto contrasto + TV-first
- Q-OPEN-26: typography scale = 8 token
- Q-OPEN-27: spacing = base 4px, 11 token

## Pattern tecnici

1. **Dependency chain registry conflict**: 6 PR paralleli modificano tutti `docs_registry.json` → conflict post-merge #1578. Rebase + force push risolve. Pattern ripetibile per ogni PR chain che tocca registry.
2. **Draft promotion**: `docs/planning/draft-*.md` → `docs/core/NN-TOPIC.md` canonical + mark draft SUPERSEDED. Preserva reference history.
3. **Art direction separato da UI style guide**: 41-AD = visual identity (palette + silhouette + biomi), 42-SG = implementation tokens (CSS custom properties + component patterns). Separati per scope. 41-AD referenzia 42-SG, not vice versa.
4. **Schema extension no-breaking**: visual_mood campo opzionale, runtime no-op → zero impatto scenari legacy.
5. **Linter Python pure-text**: no backend dep, parsing tabella MD regex. Unit test con inline fixtures.

## Follow-up FU-M3.6-A..D

| ID | Task | Blocker | Priorità |
|---|------|---|:-:|
| A | Asset commission freelance | Budget + art lead | 🟢 |
| B | Palette 11 biomi non-shipping | Art curator + commission | 🟡 |
| C | Moodboard visivo PNG | Master DD tempo | 🟡 |
| D | Audio direction ADR (gap #3) | Audio lead TBD | ⚪ |

## Memo guardrail rispettati

- Regola 50 righe: tutti PR docs/schema/tools, zero apps/backend code
- No touch workflow/migrations/contracts/generation
- `schemas/evo/encounter.schema.json` (NON `packages/contracts/schemas/`) — schema locale, contracts non toccati
- Nessuna dipendenza nuova
- Sempre branch off origin/main, rebase quando registry conflict

## Test delta sessione

| Suite | Pre | Post | Δ |
|---|:-:|:-:|:-:|
| encounter schema | 12 | 12 | 0 (schema esteso, stessi encounter) |
| styleguide lint (python) | 0 | 10 | +10 |
| **Totale** | — | — | +10 |

## Art direction gap status

- **Pre-M3.6**: GDD audit gap critico #1 = TOTAL GAP (zero asset, zero styleguide, zero moodboard)
- **Post-M3.6**: SPEC-COMPLETE, ready-for-freelance commission

Step 1-7 roadmap ADR done (spec/docs/tools). Step 8-9 blocked su budget esterno.
