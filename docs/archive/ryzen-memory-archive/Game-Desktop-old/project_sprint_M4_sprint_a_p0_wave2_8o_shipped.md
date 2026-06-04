---
name: Sprint A P0 Wave 2-8O complete shipped (2026-04-18/19)
description: Session playtest-driven. 21 PR stack merged to main via #1626 consolidated. 9 Wave iteration user feedback. Canvas responsive + onboarding tips + Codex MVP + multi-intent AP budget + HUD redesign.
type: project
originSessionId: ca63f88d-ac96-4661-9d83-291f4e5a8a6e
---
Maratona session 2026-04-18/19 M4 playtest live con 5 round iterative user feedback. Stack cresciuto 21 PR, tutti finali merged in main via #1626 consolidated (admin + --theirs strategy).

## PR merged finale

| Commits | Content |
|---|---|
| #1601-1604 | Docs: retrospective art gap + ADR plan-reveal + 44-HUD + USE_NEW_ART flag |
| #1605 | Round simultaneous + confirm action flags |
| #1627 | HUD cosmetic base (era #1606, re-open post auto-close) |
| #1626 | **Wave 2-8O consolidated** — 21 PR stack merged via --theirs + rebase main |

## Wave 2-8O content (dentro #1626)

| Wave | Focus |
|------|-------|
| W2 | HUD help + fullscreen + FX + job colors + tooltip |
| W3 | Range overlay + FX wire + simultaneous default + cursor crosshair |
| W4 | Round feedback + priority badge + auto-commit + planning timer |
| W5 | Speed label + events tail + 📊 Eval capture Flint v0.3 |
| W6 | Planning control + AP tiles + ✕ cancel per PG + ESC + per-PG HUD |
| W7 | Priority preview + ability chips per PG + emergencyResetRound |
| W8 | Inter typography + status SVG icons + research 15 refs + roadmap |
| W8b | getLocalStorageFlag + getUnits + constants + ARIA + normalizePos |
| W8c | handleDamageEvent + formatEventLine export + CSS tokens |
| W8d | XSS esc() + isUnitAlive/Dead predicates + AP Math.max(0) clamp |
| W8e | Enter shortcut + retry declareIntent + responsive breakpoints |
| W8f | Sidebar sections player/SIS + display names IT + prominent/dimmed |
| W8g | speciesNames.js map + getJobLabelIt → IT canonical (00E-NAMING) |
| W8h | Onboarding tips + AP label dark badge + error recovery |
| W8i | Tip modal center + backdrop + multi-step pages |
| W8j | Spotlight highlight targets + copy umano rewrite |
| W8k | Multi-intent per unit (ADR override) + timer toggle |
| W8k2 | Timer default OFF + backend clear-intent sync |
| W8L | Codex MVP (4 tabs: Tips/Glossario/Abilità/Status) + tip timing fix |
| W8M | HUD SVG icons + mini-label + unit body shapes + species abbrev IT |
| W8N | AP budget check client-side per pending + UI "−N" indicator |
| W8O | Canvas responsive (CELL dinamico) + ability bar bug fix + FX enhance + status chip +30% |

## Key architectural changes

1. **ADR override** (W8k): ADR-2026-04-15 "latest-wins intent per unit" → **multi-intent append**. User può dichiarare N azioni per unit finché AP budget sufficiente.
2. **Canvas responsive** (W8O): `CELL = let` dinamico, clamp(40-96px) da container viewport. Was fisso 64px.
3. **Onboarding tips system** (W8h-j): localStorage first-time flags, modal center backdrop, spotlight highlight target elementi, human copy.
4. **Codex MVP** (W8L): in-game wiki con 4 tab Tips re-reader + Glossario 14 term + Abilità + Status. A.L.I.E.N.A. full = Wave 9+ backlog.
5. **Naming canonical IT** (W8f-g): display_name_it species + label_it jobs da `docs/core/00E-NAMING_STYLEGUIDE.md`. "Predatore delle Dune · Schermidore" invece "p_scout".

## Research phases (3 pass multi-agent)

- Pass 1 code quality (10 findings + 6 quick wins) → W8b/8c applied
- Pass 2 security + perf + UX + a11y (10 findings) → W8d applied XSS + AP clamp + predicates
- Pass 3 test + i18n + mobile + obs + docs (10 findings) → W8e applied Enter + retry + responsive

## User playtest feedback run1 → run5

5 iterazioni user live playtest port 5180. Ogni round 3-8 bug/gap identificati + shipped mirato in waves.

## Backlog Wave 9+

- Full A.L.I.E.N.A. integration (6-tab per specie, plan doc in docs/planning/codex-in-game-aliena-integration.md)
- Visual roadmap W9-W13 (plan doc docs/planning/visual-roadmap-2026-04-19.md): moodboard HTML + palette master .ase + creature silhouettes 32×32 pixel art + tileset biome 9 palettes + animation 4-frame
- Attack range pointer line preview
- SIS intent hover detail threat_preview (backend contracts)
- Combat log verbose codification

## Files nuovi shipped

- `apps/play/src/tips.js` (onboarding tip modal system)
- `apps/play/src/codexPanel.js` (in-game wiki MVP)
- `apps/play/src/speciesNames.js` (IT display names map 44 species)
- `docs/planning/visual-research-2026-04-19.md` (15 ref games analysis)
- `docs/planning/visual-roadmap-2026-04-19.md` (W9-W13 plan)
- `docs/planning/codex-in-game-aliena-integration.md` (A.L.I.E.N.A. integration plan)
- `docs/playtest/2026-04-19-M4-run2-ux-gaps.md` (playtest report)

## Merge strategy lesson (per future session)

Stack 21 PR sequential con base chain caused merge cascade conflicts after first 5 squashed. Fix: merge PR base=main stack, poi rebase stack head su main con `--strategy-option theirs` + force push + admin merge consolidated. Closing intermediate PR as "superseded".

**Pattern da evitare**: non fare 21 PR sequenziali tutti open contemporaneamente. Merge bottom-up incrementale OR usa 1 PR per sprint feature pack.

## Session closing state

- Main HEAD = post #1626 merge (Wave 2-8O consolidated)
- Zero PR open (stack chiuso)
- Server play+backend running
- Next session: Wave 9 visual moodboard + codex A.L.I.E.N.A. full
