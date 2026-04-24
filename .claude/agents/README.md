# .claude/agents/ — sub-agent specializzati CodeMasterDD

Agent definition files per Claude Code. Invocati tramite `Agent` tool con `subagent_type: <name>`.

## ⚠️ Readiness protocol (ADR-0018)

Ogni agent ha status visibile in tabelle sotto:

- ✅ **ready**: passato 3 gate (smoke test + ricerca validated + tuning iteration)
- 🟡 **draft**: creato ma non completamente validato — usabile ma con cautela
- 🔴 **blocked**: validation failed, require rework

Riferimento completo: [ADR-0018 agent readiness protocol](../../docs/adr/0018-agent-readiness-protocol.md) + [SMOKE_TEST_TEMPLATE.md](SMOKE_TEST_TEMPLATE.md).

Stato 2026-04-24 (post batch P0 + P1): **11/18 ✅ ready** (smoke test live confermato), **7/18 🟡 draft**. Priorità validation documentata in ADR-0018.

- **Gate 1 PASS + Gate 2 validated + Gate 3 documented** (11 agent):
  - Mattina: `harsh-reviewer`, `delegation-classifier`, `swarm-cycle-analyzer`
  - Batch P0: `owasp-security-auditor`, `privacy-policy-enforcer`, `dogfood-analyst`
  - Batch P1: `adr-drafter`, `repo-health-auditor`, `bench-reporter`, `cost-monitor`, `compact-conversation`
- **Restano draft** (7 agent): game-* (4), dafne-proposal-triager, database-schema-designer, lore-consistency-checker, a11y-wcag-reviewer

Log smoke test completi: [docs/agent-smoke-tests/](../../docs/agent-smoke-tests/)

## Agent registrati (18 totali)

### 🎯 Operational — codemasterdd core (5)

| Agent | Status | Model | Scope | When to invoke |
|-------|:------:|-------|-------|----------------|
| [dogfood-analyst](dogfood-analyst.md) | ✅ ready | sonnet | Analizza log dogfood + tier routing suggestions | "analizza dogfood", "come va Fase 6" |
| [bench-reporter](bench-reporter.md) | ✅ ready | sonnet | Report quality bench da results esistenti | "report bench", "qual è il migliore per X" |
| [cost-monitor](cost-monitor.md) | ✅ ready | sonnet | Cost snapshot + budget alerts | "quanto spendo", "cost snapshot" |
| [repo-health-auditor](repo-health-auditor.md) | ✅ ready | sonnet | Audit cross-repo superficie + STATUS_MULTI_REPO refresh | "audit cross-repo", "stato tutti repo" |
| [adr-drafter](adr-drafter.md) | ✅ ready | sonnet | Scaffold nuovi ADR seguendo MADR | "scrivi ADR per X" |

### 🎮 Game (Evo-Tactics) — 4

| Agent | Status | Model | Scope | When to invoke |
|-------|:------:|-------|-------|----------------|
| [game-balance-auditor](game-balance-auditor.md) | 🟡 draft | sonnet | d20 combat balance, stat outlier, Numbers Policy | "check balance", "rivedi stats" |
| [game-systems-designer](game-systems-designer.md) | 🟡 draft | sonnet | Design core loop + sub-loop + experience arc | "design core loop", "progetta sistema X" |
| [game-design-validator](game-design-validator.md) | 🟡 draft | opus | First principles + Rule of Threes + elimination test | "valida design", "first principles game" |
| [lore-consistency-checker](lore-consistency-checker.md) | 🟡 draft | sonnet | Coerenza narrativa cross-artifact lore | "check lore", "coerenza narrativa" |

### 🐝 Dafne swarm — 2 (oltre a repo-health-auditor per quick check)

| Agent | Status | Model | Scope | When to invoke |
|-------|:------:|-------|-------|----------------|
| [swarm-cycle-analyzer](swarm-cycle-analyzer.md) | ✅ ready | sonnet | Deep pattern analysis cicli swarm + intervention effectiveness | "analisi cicli swarm", "pattern fail Dafne" |
| [dafne-proposal-triager](dafne-proposal-triager.md) | 🟡 draft | sonnet | Pre-filter proposals Dafne prima approvazione Eduardo | "triage dafne proposals", "review pending" |

### 🔒 Cross-cutting quality/security (3)

| Agent | Status | Model | Scope | When to invoke |
|-------|:------:|-------|-------|----------------|
| [owasp-security-auditor](owasp-security-auditor.md) | ✅ ready | opus | OWASP Top 10 2025 + Agentic Skills Top 10 su endpoint/secrets | "security audit", "OWASP review" |
| [a11y-wcag-reviewer](a11y-wcag-reviewer.md) | 🟡 draft | sonnet | WCAG 2.2 AA scan su template HTML/EJS/Jinja2 | "check a11y", "WCAG review" |
| [harsh-reviewer](harsh-reviewer.md) | ✅ ready | opus | Quality gate generico multi-aspect (code, ADR, plan) | "harsh review", "che problemi vedi" |

### 🗄️ Database + privacy (2)

| Agent | Status | Model | Scope | When to invoke |
|-------|:------:|-------|-------|----------------|
| [database-schema-designer](database-schema-designer.md) | 🟡 draft | sonnet | Schema design + index + migration strategy cross-repo | "design schema DB", "review Prisma" |
| [privacy-policy-enforcer](privacy-policy-enforcer.md) | ✅ ready | haiku | Classifica file path per cloud-OK vs sovereign-only | "è cloud OK?", "classifica privacy" |

### 🧭 Meta / workflow (2)

| Agent | Status | Model | Scope | When to invoke |
|-------|:------:|-------|-------|----------------|
| [delegation-classifier](delegation-classifier.md) | ✅ ready | haiku | Classifica task + suggest tier routing (ADR-0016 formalizzato) | "classifica task", "che tier uso" |
| [compact-conversation](compact-conversation.md) | ✅ ready | sonnet | Produce compact markdown paste-ready per nuova sessione | "compact", "prepara handoff" |

## Model tier rationale

- **haiku** (fast, cheap): classifier / gate senza deep reasoning (delegation-classifier, privacy-policy-enforcer)
- **sonnet** (default): review + analisi + report (la maggior parte)
- **opus** (deep reasoning): first principles + harsh critique + OWASP (game-design-validator, harsh-reviewer, owasp-security-auditor)

## Invocazione pattern

```
Agent({
  subagent_type: "game-balance-auditor",
  description: "Evo-Tactics balance audit",
  prompt: "Audit balance su C:/dev/Game/data/core/species/*.yaml. Focus: outlier stat base. Report <500 parole."
})
```

## Policy governance

- **Read-only di default** — se deve scrivere, specificato esplicitamente nella description
- **No avvio servizi** (docker, processi) — responsabilità hub Claude Code
- **No modifica logs/ dogfood direttamente** — responsabilità hub
- **adr-drafter è l'unico autorizzato** a creare file in `docs/adr/` (sempre Proposed)
- **privacy-policy-enforcer è upstream gate** per tutti i delegation cloud

## Fonti / attribuzione

### Pattern dall'Archivio_Libreria_Operativa_Progetti
- `adr-drafter` ← Tech Lead + PM Tecnico + ADR-0010 MADR
- `harsh-reviewer` ← "Revisore severo ma utile" (02_LIBRARY/02_Modules:355)
- `game-design-validator` ← First Principles Repo Game (02_LIBRARY/03 + template 06)
- `database-schema-designer` ← Software Architect Repo Mapper (02_LIBRARY/02_Modules:141)

### Pattern da research esterna (MIT/Apache)
- `game-balance-auditor` ← Donchitos/Claude-Code-Game-Studios `balance-check` + Game Design Framework skill
- `a11y-wcag-reviewer` ← Community-Access/accessibility-agents (WCAG 2.2 AA)
- `owasp-security-auditor` ← agamm/claude-code-owasp + TarkinLarson/asvs-auditor
- `swarm-cycle-analyzer` ← jayminwest/overstory tiered watchdog pattern

### Tecniche da TikTok sources
- `compact-conversation` ← Evolving AI Hack #6 + okaashish Hack #6 (Compact Skill)
- `harsh-reviewer` philosophy ← okaashish Caveman Method (no filler, direct)
- `delegation-classifier` formalizza Opus/Sonnet/Haiku routing (Evolving AI Hack #3)

### Custom codemasterdd
- `dogfood-analyst`, `bench-reporter`, `cost-monitor`, `repo-health-auditor` (Fase 6 operations)
- `privacy-policy-enforcer` (ADR-0013 policy enforcement)
- `delegation-classifier` (ADR-0016 formalizzazione)
- `swarm-cycle-analyzer`, `lore-consistency-checker` (integration Game+Dafne ecosystem)

## Coverage matrix per repo

| Repo | Primary agent(s) | Cross-cutting agents |
|------|------------------|----------------------|
| codemasterdd | dogfood-analyst, bench-reporter, cost-monitor, repo-health-auditor, adr-drafter, delegation-classifier, compact-conversation | owasp, database, privacy, harsh |
| Game (Evo-Tactics) | game-balance-auditor, game-design-validator, lore-consistency-checker | owasp, a11y, harsh |
| Dafne swarm | swarm-cycle-analyzer, repo-health-auditor | owasp, harsh |
| Synesthesia (dormant) | — | a11y, database, privacy, owasp, harsh (quando riattiva) |

## Aggiungere nuovo agent (workflow ADR-0018)

1. **Commit 1 `feat(agents): add <name> draft`**:
   - Crea file `<name>.md` con frontmatter YAML (`name`, `description`, opzionale `model`)
   - Body system prompt + task-specific instructions
   - Update README — status **🟡 draft**
   - Update SOURCES.md con attribuzione fonti (licenze da verificare in Gate 2)

2. **Commit 2 `test(agents): smoke test <name> gate 1`**:
   - Invoca agent via `Agent` tool con prompt rappresentativo del scope
   - Segui checklist [SMOKE_TEST_TEMPLATE.md](SMOKE_TEST_TEMPLATE.md)
   - Log risultato in commit message o `docs/agent-smoke-tests/<name>.md`

3. **Commit 3 `chore(agents): validate sources <name> gate 2`**:
   - Verifica licenze fonti (MIT/Apache/BSD preferite, flag AGPL/NC)
   - Confirm pattern/framework citati sono validati (non invented)
   - Aggiorna SOURCES.md se trovi issue

4. **Commit 4 `tune(agents): refine <name> gate 3 → ready`**:
   - Applica refinement basato sui findings smoke test
   - README status **🟡 draft** → **✅ ready**

**Anti-pattern**: 1 commit con 5+ nuovi agent senza gate. Se urgente (emergency response agent), usa tag `draft-emergency` con rationale esplicito.

## Evoluzione / TODO

Agent candidates tracked in BACKLOG, da considerare post ADR-0017 ratification:

- **bench-post-upgrade-runner**: automatizza bench pattern (da research `bench-post-ram-upgrade-2026-04-22.md`)
- **monorepo-boundary-guardian**: cross-language import check per Game (Node + Python)
- **memory-consolidator-wrapper**: invoca skill `anthropic-skills:consolidate-memory` con policy codemasterdd
- **release-notes-writer**: genera release notes da git log + ADR accepted
- **schema-privacy-classifier**: estensione specifica per-commit di privacy-policy-enforcer

## Riferimenti

- [ADR-0010 MADR format + skill policy](../../docs/adr/0010-madr-format-adoption-and-skill-policy.md)
- [ADR-0013 Tier 3 cloud free providers](../../docs/adr/0013-tier3-cloud-free-providers.md)
- [ADR-0016 Constraint-count routing dimension](../../docs/adr/0016-constraint-count-routing-dimension.md)
- [ADR-0017 UI + observability stack](../../docs/adr/0017-ui-observability-stack.md)
- [CLAUDE.md](../../CLAUDE.md) — convenzioni progetto
- [docs/patterns/delegation-to-aider.md](../../docs/patterns/delegation-to-aider.md)
- Claude Code agents docs: https://code.claude.com/docs/en/agent-teams
