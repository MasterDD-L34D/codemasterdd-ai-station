## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG-SCOPED, no bypass): INVOCA `agent-scanner` PRIMA di
creare o dispatchare un nuovo subagent/agent, oppure quando serve un
inventario degli agenti disponibili. Non e' necessario per usare una
skill esistente, all'avvio di una sessione o in un subagent gia' dispacciato.
Principio cardine: **build on existing work, never recreate**.

**Trigger mandatori** (3):
- **TEAM_FORMATION**: prima di proporre o creare un nuovo agent specializzato.
- **AGENT_DISPATCH**: prima di dispatchare un subagent/agent, se consentito.
- **ON_DEMAND**: inventario esplicito ("scan agents", "quali agenti ho").

**Sorgenti** (priorita decrescente, vedi SKILL.md):
`.claude/agents/` PROJECT > `~/.claude/agents/` USER > plugin agents
> `~/.claude/skills/` > `.claude/skills/` > `AGENTS.md`/`CLAUDE.md`
inline > ARCHON pointer (vendored nel git del vault, fires dove aa01/archon e' presente -- Ryzen incl., NON Lenovo-only).

**Skill locations** (two-tier):
- **LITE cross-project**: `~/.claude/skills/agent-scanner/SKILL.md`
  (default globale, read-only).
- **FULL ARCHON** (solo se `aa01/archon/` detected):
  `aa01/archon/skills/agent-scanner/SKILL.md` (overlap calc + ruoli
  + registry persistence).

**Anti-pattern bloccati**:
- **Shadow duplication**: creo planner-v2 quando planner funziona.
- **Silent override**: file con `name:` duplicato sovrascrive
  precedente senza warning -- scanner lo flagga in report.
- Scanner su bootstrap o selezione di skill esistenti: parti dal task.

**Reference**: OD-007 closure 2026-05-28 + first-principles
application `docs/research/2026-05-28-od-007-first-principles-
application.md` + deploy spec `docs/superpowers/specs/
2026-05-28-archon-agent-scanner-cross-fleet-deploy-design.md`.

<!-- END agent-scanner-directive -->
