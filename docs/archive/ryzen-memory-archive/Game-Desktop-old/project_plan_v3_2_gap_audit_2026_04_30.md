# Plan v3.2 gap audit + pillar promotion ADR — 2026-04-30

## Context

Post pivot Godot 2026-04-29 + plan v3.1 ASSET PIPELINE + ERMES ROADMAP, master-dd request gap audit pre Sprint M.1 spawn: _"verifichiamo se ci sono altri gap nel piano + di progettazione rispetto a doc e file"_.

## Output — PR #2026 merged main `e8967285`

### P0 fix plan v3.2

1. **Line 305 ADR-2026-04-19 contraddizione**: `services/rules/resolver.py` (Python deprecated) → Node `apps/backend/services/combat/resistanceEngine.js` + `apps/backend/routes/session.js` canonical
2. **Counts inflated**: 60+ encounter → **14** reali (4 `data/encounters/` + 10 `docs/planning/encounters/`); 100+ species → **15** lifecycle YAML; 458 trait verified accurate
3. **Sprint N gate exit**: P3 (Specie×Job ability + bond reactions) + P5 (Co-op room-code lobby + 4-player WS) row aggiunte → verdict 6/6 → 10/10
4. **Pillar promotion criteria informal** → NEW ADR

### NEW deliverables

- **`docs/adr/ADR-2026-04-30-pillar-promotion-criteria.md`** — tier ladder formal (🔴/🟡/🟡++/🟢 candidato/🟢/🟢++/🟢ⁿ) + demotion trigger + Gate 5 anti-pattern Engine LIVE Surface DEAD cross-ref
- **`docs/research/2026-04-30-gap-audit-plan-v3-2-synthesis.md`** — synthesis 3 agent paralleli (Agent A plan precedenti + Agent B design docs + Agent C repo files), ~30 gap classified P0/P1/P2/P3

## Methodology

3 agent paralleli single-message scope disjoint:

- **Agent A**: plan precedenti (Sprint M3-Fase 1, IDEAS_INDEX, BACKLOG, OPEN_DECISIONS)
- **Agent B**: design docs (`docs/core/`, EVO_FINAL_DESIGN, ADR canonical)
- **Agent C**: repo files reali (services backend/, routes/, data/core/, packs/)

Convergence: 4 P0 (FIXED v3.2) + 8 P1 (deferred v3.3 non bloccanti) + 4 P2 + 3 P3.

## P1 deferred plan v3.3 (next session post Sprint M.1 spawn)

1. §Sprint O 16+ combat services Node port matrix
2. §Sprint R 26 routes HTTP backend whitelist Godot client
3. §Sprint O.4 8 AI services Node port matrix
4. ADR drop HermeticOrmus formal (~30min)
5. §Sprint S Mission Console deprecation row
6. Path drift correction table (~1h grep audit)
7. §Sprint M.3 7 silhouette spec addendum (~30min)
8. §Sprint N.5 accessibility parity bullet (colorblind + aria-label + reduced-motion)

## Pattern + lessons

- **Triple agent paralleli scope disjoint = high signal**: Agent A/B/C convergent su counts inflated + ADR contraddizione + missing P3/P5 Sprint N gate. Single agent avrebbe missed almeno 30%.
- **Tier ladder formal anti-Engine LIVE Surface DEAD**: pillar promotion criterio ora reproducibile + auditable + demotion path esplicit (vedi P5 web stack 2026-04-29 pre-pivot Godot).
- **P0/P1 split pragmatic**: ship subito P0 (4 bloccanti pre Sprint M.1) + defer P1 (8 non bloccanti, integrabili plan v3.3 quando reach Sprint M-N-O scope). Evita "perfect = enemy of good".

## Resume trigger phrase canonical

> _"leggi COMPACT_CONTEXT.md v22 + docs/planning/2026-04-29-master-execution-plan-v3.md v3.2 + docs/adr/ADR-2026-04-29-pivot-godot-immediate.md + docs/research/2026-04-30-gap-audit-plan-v3-2-synthesis.md. Spawn Sprint M.1 chip: NEW repo Game-Godot-v2 + Donchitos template adopt + Godot 4.x install + 3 spike (M.5 cross-stack + M.7 phone + M.6 CI)."_

## Files modified

- `docs/planning/2026-04-29-master-execution-plan-v3.md` — line 305 + counts + gate row
- `docs/adr/ADR-2026-04-30-pillar-promotion-criteria.md` (NEW)
- `docs/research/2026-04-30-gap-audit-plan-v3-2-synthesis.md` (NEW)
- `docs/governance/docs_registry.json` — 2 entry nuove
- `reports/docs/governance_drift_report.json` — autoregen

## Next session

Sprint M.1 chip spawn: `feat/sprint-m-1-godot-bootstrap-2026-04-30` su NEW repo `MasterDD-L34D/Game-Godot-v2` (separate working dir).
