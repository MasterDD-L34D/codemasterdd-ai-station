# .claude/agents/ — sub-agent specializzati CodeMasterDD

Agent definition files per Claude Code. Invocati tramite `Agent` tool con `subagent_type: <name>`.

## Agent registrati

| Agent | Scope | When to invoke |
|-------|-------|----------------|
| [dogfood-analyst](dogfood-analyst.md) | Analizza log dogfood + tier routing suggestions | "analizza dogfood", "come va Fase 6", "che tier per questo task" |
| [bench-reporter](bench-reporter.md) | Report quality bench da results esistenti | "report bench", "qual è il migliore per X", "confronta A vs B" |
| [cost-monitor](cost-monitor.md) | Cost snapshot + budget alerts | "quanto spendo", "cost snapshot", "siamo sotto budget" |
| [repo-health-auditor](repo-health-auditor.md) | Audit cross-repo + refresh STATUS_MULTI_REPO | "audit cross-repo", "stato tutti i repo", "sync status" |
| [adr-drafter](adr-drafter.md) | Draft nuovi ADR seguendo MADR + policy | "scrivi ADR per X", "draft ADR", "formalizza decisione" |

## Invocazione pattern

```
Agent({
  subagent_type: "dogfood-analyst",
  description: "Review Fase 6 metrics",
  prompt: "Analizza il log dogfood del mese corrente e dimmi se siamo on-track verso i criteri ADR-0014. Report <300 parole."
})
```

## Policy governance

- Ogni agent ha **scope read-only di default** — se deve scrivere, specificato esplicitamente nella description
- **Nessun agent avvia servizi docker/processi long-running** — quello è responsabilità Eduardo + hub Claude Code
- **Nessun agent modifica logs/ dogfood direttamente** — quello è scrittura hub dopo ogni dogfood reale
- **ADR-drafter è l'unico autorizzato a creare file in `docs/adr/`** senza pre-approvazione Eduardo (ma produce sempre Proposed, mai Accepted)

## Aggiungere nuovo agent

1. Crea file `<name>.md` in `.claude/agents/`
2. Frontmatter YAML con `name`, `description` (usato per auto-matching), opzionale `model: sonnet|opus|haiku`
3. Body con system prompt + task specific instructions
4. Update questo README con riga tabella + scope
5. Commit

## Evoluzione

Agent candidates per future extensions (tracked in BACKLOG):

- **lang-checker**: verifica convenzioni Italian/English cross-repo
- **privacy-auditor**: check privacy policy compliance su repo mixed (Synesthesia quando riattivata)
- **release-notes-writer**: genera release notes da git log + ADR accettati
- **memory-consolidator**: già coperto da skill `anthropic-skills:consolidate-memory`, wrapper possibile

## Riferimenti

- [ADR-0017 UI + observability stack](../../docs/adr/0017-ui-observability-stack.md)
- [CLAUDE.md](../../CLAUDE.md) — convenzioni progetto
- Claude Code agents docs: https://docs.claude.com/en/docs/claude-code
