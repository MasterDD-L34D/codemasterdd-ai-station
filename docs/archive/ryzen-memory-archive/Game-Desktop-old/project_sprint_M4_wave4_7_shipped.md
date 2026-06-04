---
name: Sprint M4 P0 Wave 4-7 shipped + run4 playtest bug report
description: Wave 4 round feedback + Wave 5 preflight + Wave 6 planning control + Wave 7 per-PG abilities merged to main. Run4 user playtest 2026-04-19 rivela 8 bug (3 P0 blocker + 3 P1 UX + 2 P2).
type: project
originSessionId: dd2a612f-e14f-41db-83e7-715cd5f8dc55
---
Continuazione di [project_sprint_M4_p0_wave2_shipped.md](project_sprint_M4_p0_wave2_shipped.md). Wave 2+3 PR #1607+#1608 merged. Wave 4-7 ship diretto main (commits 14c3cba3, 6dd6274b, c28e6581, fb927f60).

**Why:** User playtest iterativo run2→run3 rivela gap UX dopo ogni Wave. Wave 4-7 hanno chiuso 15+ gap, ma run4 (2026-04-19) mostra 8 bug nuovi/residui — 3 P0 blocker bloccano Wave 8 visual scope.

**How to apply:** Wave 8 branch attivo `feat/play-sprint-a-p0-wave8-visual-base-typo-icons` (scope originale = typography + SVG icons). **User report run4 sovrascrive scope**: shippare visual su base funzionalmente rotta = polish inutile. Raccomandazione **Opzione A fix-first**: W8-emergency (P0 bug) → W8b (visual originale) → W9 (P1 UX) → W10 (P2).

## Wave 4 (commit 14c3cba3, +332/-39)

Round feedback layer, 5 items ADR-2026-04-15:
- Priority queue display (initiative+speed-penalty)
- Action-type badges sul tail
- Plan-reveal placeholder (threat_preview)
- Result popup expanded (damage+hit+miss+kill)
- Round summary on `/round/execute` resp

## Wave 5 (commit 6dd6274b, +85/-35)

Preflight polish:
- Speed label HUD (initiative visible)
- Events tail expose via `publicSessionView.events[]` in `sessionHelpers.js` (fix backlog Wave 3 item 3)
- Eval capture JSONL endpoint (TKT-WAVE4-01 chiuso)
- Governance drift cleanup

## Wave 6 (commit c28e6581, +197/-10)

Planning control + per-PG HUD (4 bug run3):
- Planning toggle UI
- Per-PG HUD panel (stat inline)
- Render per-PG selection highlight
- Style buff/debuff badges

## Wave 7 (commit fb927f60, +228/-46)

Planning preview + per-PG abilities + defensive reset:
- Abilities panel per-PG (data-driven da unit.abilities)
- Defensive state reset on new round
- Plan preview panel (threat_preview wire)

## Run4 user playtest 2026-04-19 — 8 bug report

| # | User verbatim | Tier | Feature esistente | Root cause candidato |
|---|---|:-:|---|---|
| 5 | "commit-round exception: failed to fetch" | **P0 CRIT** | /round/execute Wave 3 | Backend crash/timeout, network layer |
| 1 | "non si capisce come attivare abilità" | **P0** | Wave 7 per-PG abilities | Trigger non scopribile (click? key? tooltip assente) |
| 8 | "abilità non compaiono" | **P0** | Wave 7 abilities panel | Condition/data mismatch, panel vuoto |
| 4 | "cose che posso fare non chiare" | **P1** | Wave 2 help + tooltip | Help modal non discovery, tooltip stub |
| 2 | "risultati turni non facilmente visibili" | **P1** | Wave 4 round feedback | Popup volanti, no persistent summary |
| 6 | "tizio morto non capito perché" | **P1** | Wave 5 events tail | No kill chain inline + cause-of-death |
| 3 | "selezione nemico confonde" | **P2** | — | Inspect enemy = stesso UI di ally, no separation |
| 7 | "cose sotto schede unità non chiare" | **P2** | Wave 6 per-PG HUD | Labels/legend missing (stat/status criptici) |

## Raccomandazione Wave 8 split (Opzione A fix-first)

| Wave | Scope | Effort | Priority |
|---|---|:-:|:-:|
| **W8-emergency** | Fix bug #5 crash + #1/#8 abilità visibility | 4-6h | P0 |
| **W8b** | Wave 8 visual originale (typography Inter + SVG status icons) | 6h | P1 |
| **W9** | #4 action affordance + #2 result persistent + #6 kill chain | 6h | P1 |
| **W10** | #3 enemy inspect UI + #7 unit card labels/legend | 4h | P2 |

## File da toccare Wave 8-emergency (ipotesi, da verificare)

- `apps/play/src/abilityPanel.js` (esiste, verifica data flow)
- `apps/play/src/api.js` (commit-round error handler + retry)
- `apps/play/src/main.js` (ability trigger wire)
- Backend `apps/backend/routes/session.js` (/round/execute error path)

## Cross-ref

- [docs/planning/visual-research-2026-04-19.md](../../../Desktop/Game/docs/planning/visual-research-2026-04-19.md) — Wave 8 visual research (scope originale)
- [project_sprint_M4_p0_wave2_shipped.md](project_sprint_M4_p0_wave2_shipped.md) — Wave 2+3
- Commit range: 182ebcf7..fb927f60 (5 commits)
