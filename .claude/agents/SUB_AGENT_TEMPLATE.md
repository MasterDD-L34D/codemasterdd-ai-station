<!--
Template ispirato vault-shared sibling-peer (Karpathy LLM-wiki, MasterDD-L34D/vault) -- structural pattern 7/7 production agents.
Aligned with codemasterdd ADR-0018 (agent-readiness-protocol, 2026-04-24) -- workflow add new agent.
Audit-then-replay 2026-05-11 (AA01 task 2026-05-aa01-002).
NO clone vault files, NO commit hash citato (drift risk).
-->

# Sub-agent scaffolding template -- codemasterdd

Template strutturale per creare nuovo agent in `.claude/agents/<name>.md`. Body sections vault-informed + frontmatter Claude Code convention.

**NOT a runnable agent**: copy + rename per nuovo agent. Do NOT invoke `subagent_type: SUB_AGENT_TEMPLATE` (Claude Code skipperà).

---

## How to use

1. Copy `SUB_AGENT_TEMPLATE.md` → `<your-agent-name>.md`
2. Sostituire placeholder `<...>` con valori specifici
3. README.md status entry → 🟡 draft
4. SOURCES.md attribution se pattern derivato esterno
5. Eseguire workflow ADR-0018 (4 commit gate: feat → smoke → validate → tune)

---

## Template

```markdown
---
name: <slug-agent-lowercase-dashed>
description: <1-2 line scope + trigger phrases ("USA PROATTIVAMENTE quando..." se proactive)>
tools: <list comma-separated, es. Read, Glob, Grep, Write OR "All tools">
model: sonnet|opus|haiku
---

# <agent-name display>

## Ruolo

<1 line scope essenziale. Es. "Audit accessibility WCAG 2.2 AA su template HTML.">

## Input

<Spec input:
- file path types
- data structures attesi
- JSON schema se applicabile
- default behavior se nessun input>

## Processo

1. <Step 1 azione concreta>
2. <Step 2>
3. <...>
<max 7 steps consigliato (vault convention); se serve più, scope è troppo largo>

## Output

<Path output (se write) o format output (se return-only).
Template struttura es:

`Extras/<agent-name>/YYYY-MM-DD-HHMM.md`:

\`\`\`
# <Report title>
## Section A
## Section B
\`\`\`
>

## Edge case (research TODO)

- <Edge case 1: input edge>
- <Edge case 2: tool/runtime edge>
- <Edge case 3: integration edge>
<target >=3 edge case (vault Quality Gate Step 2 convention).
Compilare durante smoke test, refinire durante Gate 3 tuning.>

## Quality Gate -- Step 1 smoke test

\`\`\`
Input: <fixture concrete riproducibile>
Expected: <output osservabile + criterio correctness>
Target perf: <haiku <20s | sonnet <60s | opus <120s>
Status: [ ] not run | [x] PASS | [✗] FAIL <date>
\`\`\`

## Policy + boundary

- <Specifico per agent: read-only? write su path X? need orchestration con altro agent?>
- <Cosa NON deve fare (anti-pattern guardrail)>

## Riferimenti

- <ADR/research/skill rilevanti per scope>
- [SMOKE_TEST_TEMPLATE.md](SMOKE_TEST_TEMPLATE.md) per Gate 1 procedure
- [README.md](README.md) status matrix entry
```

---

## Convention key

### Frontmatter fields (Claude Code)

| Field | Required | Note |
|-------|----------|------|
| `name` | YES | slug match filename (without .md) |
| `description` | YES | trigger phrases for hub auto-routing |
| `tools` | YES | minimal set, default `Read, Glob, Grep` if read-only |
| `model` | RECOMMENDED | tier rationale -- haiku/sonnet/opus |

### Body sections (vault-informed)

Sezioni canoniche cherry-picked dal pattern vault 7/7 production agents:
- `## Ruolo` -- 1 line scope (NON ridondare con description)
- `## Input` -- spec input dettagliato
- `## Processo` -- numbered steps ≤7
- `## Output` -- path + template structure
- `## Edge case (research TODO)` -- ≥3 edge case formal
- `## Quality Gate -- Step 1 smoke test` -- fixture + expected + target + status checkbox IN BODY

**Status checkbox IN BODY, NOT frontmatter**: vault production folder/status: draft sync drift (vedi `docs/research/vault-patterns-adoption-2026-05-11.md` sez 1.3) — lesson learnt.

### Model tier guidelines

- **haiku**: classifier / gate senza deep reasoning (delegation-classifier, privacy-policy-enforcer)
- **sonnet** (default): review + analisi + report (la maggior parte)
- **opus**: first principles + harsh critique + OWASP (game-design-validator, harsh-reviewer, owasp-security-auditor)

### Policy + boundary section

Specifico per agent. Pattern comuni:
- Read-only di default (write esplicito se autorizzato)
- No avvio servizi
- Orchestration handoff (es. delegation-classifier → privacy-policy-enforcer chain)
- ADR-0018 governance compliance

---

## Esempio compilato (reference)

Vedi esempio compilato: [game-balance-auditor.md](game-balance-auditor.md) (✅ ready, frontmatter sonnet + tools list + ## Ruolo body section).

---

## Riferimenti

- [ADR-0018 agent-readiness-protocol](../../docs/adr/0018-agent-readiness-protocol.md) (workflow 4-commit gate)
- [SMOKE_TEST_TEMPLATE.md](SMOKE_TEST_TEMPLATE.md) (Gate 1 procedure dettagliata)
- [README.md](README.md) (status matrix + invocation pattern)
- [SOURCES.md](SOURCES.md) (attribuzione policy)
- [docs/research/vault-patterns-adoption-2026-05-11.md](../../docs/research/vault-patterns-adoption-2026-05-11.md) (research origin di questo template, Pattern B Part 2 EXPAND ADOPT)
- Claude Code agents docs: https://code.claude.com/docs/en/agent-teams
