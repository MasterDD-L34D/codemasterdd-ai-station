---
name: Parallel-agent review pattern pre-approval
description: Pattern workflow emerso sessione 2026-04-19. Quando user lavora ore in parallelo + chiede controllo comprehensive prima di approvare, lancia 5 agent + 3 test suite in single message. Trovati bug P0 invisibili a session-runtime.
type: feedback
originSessionId: dd2a612f-e14f-41db-83e7-715cd5f8dc55
---
Quando user dice "ho lavorato ore, controlla tutto e lancia tutti gli agent possibili prima che approvi", **LANCIA 5+ agent + 3+ test suite in single message parallel**. Non sequenziale. Non solo test. Non solo Bash.

**Why:** Sessione 2026-04-19: user shippò 21 PR Wave 2-8O via #1626 consolidated squash. Request: "controllo completo prima che approvi". Lancio parallel ha trovato 2 P0 invisibili a session-runtime corrente:
- P0-1 AP exploit backend (session-debugger) — curl bypass multi-intent
- P0-2 sort instability (session-debugger) — cross-runtime ambiguity
Plus 25 P1/P2 codebase-health findings + schema-ripple envelope gaps + balance drift verification.

Senza audit = shipped to main potentially broken. Con audit = 1 PR focused fix.

**How to apply:**

## Template agent selection (base 5)

| Agent | Focus | When |
|---|---|---|
| `general-purpose` / Explore | Branch reconciliation / codebase health | Sempre |
| `session-debugger` | Session engine trace post-change | Se touched `apps/backend/routes/session*` OR `services/roundOrchestrator` |
| `schema-ripple` | Contracts alignment | Se touched `packages/contracts` OR new API endpoint |
| `balance-auditor` | Balance YAML outliers | Se touched `data/core/`, `packs/evo_tactics_pack/data/balance/` |
| `sot-planner` | Source of truth coherence | Se touched canonical docs `docs/core/` |
| `migration-planner` | DB/schema migration | Se touched `apps/backend/prisma/` OR `migrations/` |
| `species-reviewer` | Species JSON completeness | Se touched `data/core/species/` |

## Test suite parallel (background)

```js
// In single message, parallel Bash calls:
Bash: node --test tests/ai/*.test.js                     // DoD #1
Bash: npm run format:check                               // DoD #2
Bash: python tools/check_docs_governance.py --strict     // docs
// Opzionale se touched:
Bash: PYTHONPATH=services/rules python -m pytest services/rules/tests/
Bash: node --test tests/services/*.test.js
```

## Launch pattern (single message)

```
<multiple Agent tool blocks con run_in_background: true>
<multiple Bash tool blocks con run_in_background: true>
```

Non Sequential. Se sequential = ogni agent bloccante, waste 5-10min.

## Wait pattern

- Agent notificano auto su completion
- Aggrego risultati come arrivano (update TodoWrite per track)
- Present aggregate summary + prioritized fix plan per user approval

## Output format (aggregate to user)

```
## Parallel review — aggregate

### ✅ GREEN (no action)
[list clean checks]

### 🔴 P0 FINDINGS (N totali)
[per finding: agent | file:line | description]

### 🟡 P1 FINDINGS (N totali)
[same format]

### 🟢 P2 (backlog)
[count only]

## Proposed fix plan
[phases con effort stima]

## Aspetto approvazione su: [specific questions]
```

## Scenario concreto 2026-04-19

Launch set (7 parallel):
1. Agent general-purpose → branch reconciliation (30 commit zero delta scoperto)
2. Agent Explore thorough → codebase health (25 findings)
3. Agent session-debugger → round engine trace (2 P0 + 2 P1)
4. Agent schema-ripple → contracts (green pre-existing gaps)
5. Agent balance-auditor → balance stable, 3 minor
6. Bash bg → AI tests 161/161
7. Bash bg → Prettier clean
8. Bash bg → docs governance clean

Total time user-facing: ~3 min wait (parallel). Sequential: ~15-20 min.

## Cross-ref

- `project_sprint_M4_fase_a_session_p0_fix.md` — applicazione pattern concreta
- `feedback_claude_workflow_consolidated.md` §9 research-critique + §13 PR stack
- `/meta-checkpoint` skill — similar multi-agent parallel pattern

## When NOT to apply

- User chiede fix puntuale immediate (1 bug) → single-agent enough
- Session fresh < 1h work → nothing complex to audit
- User dice "fast track" / "just do it" → skip audit, ship direct
