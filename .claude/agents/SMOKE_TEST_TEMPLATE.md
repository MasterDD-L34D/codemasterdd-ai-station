<!--
Template ispirato vault-shared sibling-peer (Karpathy LLM-wiki, MasterDD-L34D/vault) -- Edge case + Quality Gate body sections.
Aligned with codemasterdd ADR-0018 (agent-readiness-protocol, 2026-04-24) -- chiude gap file mai creato (promesso riga 175+202-208).
Audit-then-replay 2026-05-11 (AA01 task 2026-05-aa01-002).
NO clone vault files, NO commit hash citato (drift risk).
-->

# Smoke test template -- sub-agent codemasterdd

Template prescriptive per Gate 1 Smoke Test ADR-0018. Usare quando si crea/refinisce un sub-agent in `.claude/agents/` per produrre log smoke test consistente in `docs/superpowers/tests/<agent>.md` o commit message.

## Quick reference -- 3-gate ADR-0018

| Gate | Cosa verifica | Criterio PASS |
|------|---------------|---------------|
| 1 Smoke | Invocazione reale con prompt rappresentativo | 1+ invocazione produces output usable senza correzione manuale |
| 2 Ricerca | License + framework + pattern validity | Attribuzione confermata, zero fonti flagged problematic |
| 3 Tuning | Refinement basato su findings | 1+ commit di tuning post-smoke-test |

Promotion `🟡 draft` → `✅ ready` solo se tutti 3 gate documentati.

---

## Section 1 -- Prompt prescriptive per agent type

### Analyzer agent (dogfood-analyst, swarm-cycle-analyzer, bench-reporter, cost-monitor)

Smoke prompt template:
```
Analizza [data source reale, es. logs/aider-delegation-2026-05.md OR
docs/research/bench-mixed-workload-2026-05-09.md].

Focus: [aspetto specifico, es. fail rate trend, swap overhead pattern].

Output: <500 parole, formato bullet/table.

Verify dopo: paths citati esistono, numeri congruenti con file source.
```

Expected output: lista findings + 1-2 pattern key + raccomandazione operativa. NO hallucinated file path.

### Reviewer agent (harsh-reviewer, a11y-wcag-reviewer, owasp-security-auditor, dafne-proposal-triager)

Smoke prompt template:
```
Review [artifact reale, es. recent ADR draft / PR diff / template HTML].

Focus: [risk class, es. blocking issues, security vuln, accessibility].

Output: list BLOCKING (severity HIGH) + SIGNIFICANT (severity MEDIUM) + MINOR (severity LOW).

Verify dopo: ogni issue cita riga/file concreta, no generic platitude.
```

Expected output: ≥1 issue concreta (anche se "no blocking" deve cite cosa NON è issue). NO scoring inflation.

### Classifier agent (delegation-classifier, privacy-policy-enforcer)

Smoke prompt template:
```
Classifica [task reale, es. "edit single file aider-refactor candidate" /
"path Synesthesia/controllers/auth.js cloud-OK?"].

Output: 1-word category + rationale 1-line + suggested action.

Verify dopo: classificazione coerente con ADR di riferimento (ADR-0008/0013/0016/0022).
```

Expected output: classificazione deterministica + path citato a ADR governing. Runtime <20s (haiku).

### Designer agent (game-systems-designer, game-design-validator, database-schema-designer)

Smoke prompt template:
```
Design [scope reale ridotto, es. "1 sub-loop combat per Evo-Tactics" /
"1 SQL index per query Synesthesia ranking"].

Constraint: [budget time/complexity, es. <30min user, <3 table join].

Output: design proposal + 1-2 trade-off identified + test/validation plan.

Verify dopo: proposal compatible con stack documentato (ADR + CLAUDE.md).
```

Expected output: design ≥3 sezioni (proposal + trade-off + validation). Runtime <120s (opus/sonnet).

---

## Section 2 -- Output validation checklist

### Format compliance

- [ ] Output struttura corrisponde a system prompt template (sections, formato lista/table)
- [ ] Lunghezza nel range atteso (Analyzer <500w, Reviewer <300w, Classifier <50w, Designer <800w)
- [ ] Markdown ben formato (no broken table, no orphan code fence)

### Content plausibility

- [ ] Path file citati esistono (verifica con Read o Glob 2-3 sample)
- [ ] Numeri/metriche allineati con source data (cross-reference con file source)
- [ ] No phantom reference (es. "vedi sezione X" se X non esiste)
- [ ] Lingua corretta (italiano per output utente, inglese per code identifier)

### Runtime acceptability

| Tier | Target |
|------|--------|
| haiku | <20s per task tipico |
| sonnet | <60s per task tipico |
| opus | <120s per task tipico |

Misurare runtime via timestamp invocation start/end.

### Tool usage discipline

- [ ] Agent rispetta tools dichiarati in frontmatter (no tool fuori scope)
- [ ] Read-only di default (se write, esplicito in description -- ADR-0018 § Policy governance)
- [ ] No avvio servizi (docker, processi)

---

## Section 3 -- Tuning iteration pattern

Post-smoke, applicare ≥1 iterazione refinement basata su findings. Pattern tipici:

### Prompt adjustments
- Sezioni system prompt ridondanti rimosse
- Nuovi edge case discovered durante smoke documentati
- Output format clarification (es. "se nessuna issue, dichiara esplicitamente")

### Scope narrowing
Se agent fa cose out-of-scope durante smoke:
- Aggiungere guardrail "NON fare X"
- Restringere description trigger phrases
- Add coverage matrix entry README per chiarire scope

### Model tier review
- haiku → sonnet promotion se reasoning depth insufficient
- opus → sonnet demotion se overkill (cost saving)
- Documenta rationale in commit message tune commit

### Integration check
Se agent orchestra con altri agent/tool:
- Documentare handoff flow in README matrix
- Identificare upstream/downstream agent dipendenze
- Test orchestration end-to-end (es. delegation-classifier + privacy-policy-enforcer chain)

---

## Section 4 -- Edge case to document (vault-informed pattern)

Per smoke test produrre log usable, documenta ≥3 edge case osservati:

Esempi edge case category (ispirato vault Quality Gate Step 2):
- **Input edge**: file mancante, encoding UTF-16 BOM, path con spazi/emoji
- **Tool edge**: Glob/Grep timeout, Bash command su comando inesistente
- **Output edge**: lunghezza outlier, format breakdown, language mismatch
- **Integration edge**: handoff a altro agent fail, dipendenza esterna unreachable
- **Scope edge**: prompt ambiguo, scope creep verso task adjacent
- **Runtime edge**: timeout, OOM su file grandi, retry pattern

Pattern documentazione edge case:
```markdown
### Edge case N -- <short title>
- **Trigger**: <quando avviene>
- **Behavior osservato**: <cosa fa agent>
- **Behavior desiderato**: <cosa dovrebbe fare>
- **Mitigation**: <guardrail aggiunto in tune commit>
```

---

## Section 5 -- Smoke test log template

Output finale smoke test (1 file per agent in `docs/superpowers/tests/<agent>.md` OR commit message):

```markdown
# Smoke test -- <agent-name> (Gate 1)

**Data**: YYYY-MM-DD
**Tester**: Eduardo / Claude Code session
**Agent file**: `.claude/agents/<agent-name>.md`
**Status pre-smoke**: 🟡 draft

## Setup
- **Prompt**: <prompt invocazione esatto>
- **Data source**: <path o description input reale>
- **Constraint dichiarati**: <es. <500 parole, sonnet tier, runtime <60s>

## Resultati

### Format compliance
- [x|✗] Structure match system prompt
- [x|✗] Length nel range atteso
- [x|✗] Markdown valido

### Content plausibility
- [x|✗] Path citati verificati
- [x|✗] Numeri/metriche allineati source
- [x|✗] No phantom reference
- [x|✗] Lingua corretta

### Runtime
- Misurato: <X>s
- Target tier: <haiku <20s | sonnet <60s | opus <120s>
- [x|✗] Within target

## Edge case osservati (≥3)

1. <edge case 1 con behavior + mitigation>
2. <edge case 2>
3. <edge case 3>

## Verdict Gate 1
- [x] PASS -- output usable senza correzione manuale
- [ ] FAIL -- raccolto findings, rework richiesto

## Next steps
- Gate 2 (Ricerca): <link SOURCES.md entry da audit>
- Gate 3 (Tuning): <commit tune previsto, scope refinement>
```

---

## Section 6 -- ADR-0018 anti-pattern (riferimenti)

NO go forward:
- 1 commit con 5+ nuovi agent senza gate
- Status `ready` senza smoke test log
- `SOURCES.md` claim senza license verification
- Agent senza tuning iteration commit

Eccezione `draft-emergency` (1-shot use case):
- Gate 1+2 PASS + uso 1-shot documentato
- Tag temporaneo, downgrade entro 30gg

---

## Riferimenti

- [ADR-0018 agent-readiness-protocol](../../docs/adr/0018-agent-readiness-protocol.md) (3-gate framework Accepted 2026-04-24)
- [README.md status matrix](README.md) (12/18 ready, 6/18 draft stato 2026-04-24)
- [SOURCES.md](SOURCES.md) (attribuzione fonti agent per Gate 2)
- [docs/research/vault-patterns-adoption-2026-05-11.md](../../docs/research/vault-patterns-adoption-2026-05-11.md) (pattern strutturale vault-informed)
- [docs/superpowers/tests/](../../docs/superpowers/tests/) (log smoke test per-agent)
