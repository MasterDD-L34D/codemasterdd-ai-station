## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG-PURE, no bypass, no eccezione): PRIMA di selezionare,
raccomandare o creare un nuovo subagent / skill / agent specializzato,
INVOCA la skill `agent-scanner` (semantic trigger: "scan agents" /
"quali agenti ho" / "che agent uso" / "riusa agente"). Principio
cardine: **build on existing work, never recreate** (Ibrahim 2026;
Microsoft Multi-Agent Reference Architecture).

**Trigger mandatori** (4, mutuati da ARCHON v2 D-007):
- **BOOTSTRAP**: nuova sessione su un progetto -> invoca step-1 prima
  di altre decisioni di routing agent.
- **TEAM_FORMATION**: prima di proporre/creare un nuovo agent
  specializzato.
- **DELTA**: a inizio sessione, diff vs scan precedente.
- **ON_DEMAND**: comando utente esplicito ("scan agents").

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
- Bias "chi-ho-piu-memoria-recente-vince" su selezione agent.

**STRONG-PURE**: nessuna eccezione. Scanner fires anche su task
apparentemente meccanici (typo fix / rename / batch lint) per
evitare bypass involontario via "model-judgment di triviality".
Cost overhead ~2-5sec/fire accettato.

**Reference**: OD-007 closure 2026-05-28 + first-principles
application `docs/research/2026-05-28-od-007-first-principles-
application.md` + deploy spec `docs/superpowers/specs/
2026-05-28-archon-agent-scanner-cross-fleet-deploy-design.md`.

<!-- END agent-scanner-directive -->
