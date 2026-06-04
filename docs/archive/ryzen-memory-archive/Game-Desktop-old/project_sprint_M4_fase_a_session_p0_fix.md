---
name: Sprint M4 Fase A — P0 session-debugger fix (AP exploit + sort stability)
description: PR #1628 MERGED c87e66cc 2026-04-19. 3 commit: P0-1 AP exploit + P0-2 sort + 2 hotfix (resolveTileImg Wave 8O regression + action/roundAction replace_all typo). 254 CI test pass. Lessons: replace_all caveat, test coverage api vs ai.
type: project
originSessionId: dd2a612f-e14f-41db-83e7-715cd5f8dc55
---
Fase A del piano fix-first post run4 playtest. User lavorò in parallelo 21 PR Wave 2-8O merged via #1626. Post approve review request, 5 agent + 3 test suite parallel launch rivelò 2 P0 backend invisibili senza audit.

**Why:** Wave 8k override ADR-2026-04-15 (declareIntent APPEND invece di latest-wins per multi-intent UX) introdotto senza regression test corrispondenti. Session-debugger trace rivelò AP accounting broken + sort stability gap. P0-1 = security-adjacent exploit.

**How to apply:** Per Wave 9+, qualunque tocco `apps/backend/routes/sessionRoundBridge.js` OR `apps/backend/services/roundOrchestrator.js` deve verificare regression su `tests/services/roundOrchestrator.multiIntent.test.js` (5 test). Se aggiungi nuova branch action_type resolver, ricordati di usare `Number(action.ap_cost || 1)` non hardcoded. Se aggiungi tiebreaker queue, preserva `intent_index` come ultimo.

## Commit / PR — MERGED

- PR #1628: **MERGED** `c87e66cc` su main 2026-04-19T06:03:34Z (squash merge)
- 3 commit dentro:
  - `02dc629a` — P0-1 AP exploit + P0-2 sort stability (core fix)
  - `014409c2` — hotfix resolveTileImg undef Wave 8O regression (render.js:493)
  - `6bdbdfed` — fix action/roundAction typo replace_all caveat (handleLegacyAttackViaRound scope)
- Branch `feat/play-sprint-a-p1-session-hardening-ap-exploit` pendente cleanup locale (worktree blocca delete dopo merge)

## Lessons emerse post-CI + user playtest

### Lesson 1: replace_all:true caveat

Pattern `actor.ap_remaining = Math.max(0, (actor.ap_remaining ?? actor.ap) - 1)` appariva in 7 scope diversi. 6 hanno variabile locale `action`, 1 ha `roundAction` (handleLegacyAttackViaRound line 245). `replace_all:true` ha omogeneizzato a `action.ap_cost` incorrect per lo scope del 7o → ReferenceError runtime (non build-time detect).

**Regola**: dopo replace_all su pattern complesso contenente identifier, sempre grep occorrenze + verifica nome variabile per ogni scope match. Non fidarsi del build.

### Lesson 2: tests/api vs tests/ai DoD gap

Fase A 02dc629a verificato localmente con:
- `tests/ai/*.test.js` → 161/161 ✓
- `tests/services/*.test.js` → 212/212 ✓
- `npm run format:check` → ✓

Ma `tests/api/abilityExecutor.test.js`, `apBudget.test.js`, `roundExecute.test.js`, `roundExecutePriorityQueue.test.js` NON erano in DoD #1 (che specifica solo `tests/ai/*.test.js`). CI stack-quality ha scoperto 11 test fail.

**Regola DoD update**: post-fix touching `apps/backend/routes/session*.js` eseguire **ANCHE** `ORCHESTRATOR_AUTOCLOSE_MS=2000 node --test tests/api/*.test.js` prima del push. Da codificare in CLAUDE.md DoD section.

### Lesson 3: agent review vs user runtime playtest

resolveTileImg undef bug (Wave 8O regression) non scoperto da 5 parallel agent review (inclusi Explore codebase-health thorough). User playtest live rivelò subito ("non vedo mappa"). Agent review trova static/semantic issues; runtime issues (ReferenceError su code path specifico) require browser execution.

**Pattern**: parallel-agent review + user live playtest = complementary. Agent copre largo scope (25 findings), user copre depth runtime (1 P0 crash). Entrambi necessari.

## 4 file changed, 232+/17-

| File | Change |
|---|---|
| `apps/backend/routes/sessionRoundBridge.js` | `validatePlayerIntent` sum pending intents stesso actor (+apCost); `resolveFn` 7 occurrence `-= Number(action.ap_cost \|\| 1)` |
| `apps/backend/services/roundOrchestrator.js` | `buildResolutionQueue` queue items `intent_index: idx`, sort tiebreaker finale |
| `tests/services/roundOrchestrator.multiIntent.test.js` | NEW 5 test regression (queue tiebreaker + AP consumption + clamp + legacy fallback) |
| `tests/services/roundOrchestrator.test.js` | Update stale `latest-wins` test → `APPEND` spec (pre-existing gap Wave 8k non aggiornò) |

## Exploit concreto (P0-1)

```
pre-fix:
  unit ap=3
  POST /declare-intent → attack ap_cost=2 → accepted
  POST /declare-intent → attack ap_cost=2 → accepted (cada 2 ≤ 3 isolato)
  POST /commit-round   → resolveFn -=1 cada = consumo 2 AP tot
  RESULT: ability multi-AP consumate come base attack (gold farm)

post-fix:
  second /declare-intent → 400 AP_INSUFFICIENT
  "costo totale 4 (pending 2 + nuovo 2), disponibili 3"
```

## Sort instability (P0-2)

Wave 8k docstring promised "risolti in ordine di declare" ma sort era solo `(priority desc, unit_id asc)`. 2 intent stessa unit = stessa chiave → cross-runtime ambiguity (V8 stable JS OK, ma non spec-codificato).

Fix: aggiunto `intent_index` preservato da `pending_intents.forEach((intent, idx) => ...)` come tiebreaker finale.

## Verify DoD

- AI tests: 161/161 (143ms)
- Suite roundOrchestrator + endpoint: 212/212 (1.1s)
- `npm run format:check` clean
- Working tree pulito
- DoD #5 (vcScoring/policy): non toccato
- DoD #6 (services/rules): non toccato

## Non-scope shippato in Fase A

- **P1-3 trait double-dip**: zampe_a_molla fires 2× multi-intent attack. Lettura `data/core/traits/active_effects.yaml` conferma NO `once_per_round` flag per NESSUN trait (zampe/ferocia/denti_seghettati/intimidatore/stordimento/martello_osseo/pelle_elastomera). Design intent per-attack confermato. Solo ADR docs-only in backlog Wave 9+.
- **P1-4 clear/declare race**: async /clear-intent + /declare-intent concurrency senza lock. Backlog atomic `replaceIntent` endpoint.
- **25 codebase-health findings** Explore agent: /api/jobs hardcoded 3× frontend, localStorage 5+ prefix fragmented, ESC handler leak codexPanel, alert() antipattern, docs frontmatter drift. Fase 2 backlog.

## Lessons

1. **Wave 8k spec-change senza test-update** → P0-1/P0-2 latent. Regola futura: qualunque ADR override DEVE update test + scrivere nuovi regression first.
2. **Parallel-agent review efficace** — 5 agent + 3 test in single message trovò bug invisibili a session-runtime. Cross-ref `feedback_parallel_agent_review_pre_approval.md`.
3. **Evidence-based decision per trait dip** — Flint "chiedi-docs" pattern → lettura active_effects.yaml prima di fix. Risparmiato fix 2h inutile.

## Branch cleanup pre-Fase A

Pre-Fase A erano 30 commit ahead di main su branch `wave8o-canvas-responsive-ability-fx` ma **zero delta reale** (tutto consolidato in main via #1626 squash). Branch-reconciliation agent confermò. Procedura:

```bash
git branch -m feat/play-sprint-a-p1-session-hardening-ap-exploit  # rename in-place
git reset --hard origin/main  # sync a c1d84379
git branch --unset-upstream   # stale tracking
```

Pattern: quando #N PR consolidated squash assorbe tutti commit locali → zero-delta post-merge. Abbandono safe via rename+reset.

## Next step

Fase 2 candidati (post user playtest run5 evidence):
- F: clear/declare atomic endpoint (P1-4)
- G/H: API constants centralization + localStorage registry (P1 codebase-health cluster B+C)
- ADR doc zampe_a_molla per-attack intent (P1-3, doc-only)
