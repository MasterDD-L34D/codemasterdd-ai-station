# Subagent + Skill candidates — preview-worthy (2026-04-22)

Catalogo curato post-rivalutazione approfondita del materiale research 2026-04-21. **NON sono installati**. Reference per futuro: se emerge use case reale, passare per `gh skill preview` (ADR-0010) o manual copy in `.claude/agents/` del repo target, audit markdown content prima.

## Subagent Claude Code — da `VoltAgent/awesome-claude-code-subagents` (17.9k⭐)

Subagent sono markdown statici con frontmatter `name/description/tools/model`. Supply chain risk = prompt injection nel system prompt, non RCE. Audit file-by-file prima di installare.

| Subagent | Path | Valore per lo stack | Install via |
|----------|------|---------------------|-------------|
| **code-reviewer** | `04-quality-security/code-reviewer.md` | Review post-Aider su behavior-critical edit; complementa guard rail pre-commit ADR-0008 | Manual copy in `.claude/agents/` repo target |
| **test-automator** | `04-quality-security/test-automator.md` | Scale-up test authoring su Evo-Tactics (710 test) e Synesthesia | Idem |
| **dependency-manager** | `06-developer-experience/dependency-manager.md` | Migrazione Node 22→24 + Python 3.10→3.12 check per Evo-Tactics | Idem |
| **debugger** | `04-quality-security/debugger.md` | Triage errori prima di escalation a Qwen 30B o Claude Pro (riduce costo tier) | Idem |

**Invocazione pattern** (dopo install): `> Use the code-reviewer subagent to review the last commit`

**Skip bulk plugin install** (`voltagent-qa-sec` porta 16 agent, ~60% off-topic). Cherry-pick file singoli.

## Skill — da `alirezarezvani/claude-skills` (12.2k⭐, Aider-compat)

235 skill totali, signal/noise ~40% pertinente per engineering stack vanilla. Autore 1-person project. License MIT.

**⚠️ Finding 2026-04-22**: repo **NON ha struttura `gh skill`-compatibile** standard (`skills/*/SKILL.md`). `gh skill preview` restituisce "no skills found, may be curated list". **Adozione richiede manual clone + run install script** (`./scripts/install.sh --tool claude-code`) che genera structure compatibile. Overhead significativo vs `gh skill install` diretto.

| Skill | Path | Valore | Priorità |
|-------|------|--------|----------|
| **skill-security-auditor** | `engineering/skill-security-auditor/` | **Meta-skill: operazionalizza ADR-0010 `gh skill preview`-before-install**. Scansiona skill per command injection / prompt injection | 🔴 Alta — coerente con security policy |
| **monorepo-navigator** | `engineering/monorepo-navigator/` | Match diretto Evo-Tactics (Node+Python mono, workspaces pnpm/npm) | 🟡 Media — dopo migrazione progetti |
| **dependency-auditor** | `engineering/dependency-auditor/` | Unified `npm audit` + `pip-audit` + license compliance | 🟡 Media — su 22 vuln Evo-Tactics upstream |
| **pr-review-expert** | `engineering/pr-review-expert/` | Blast-radius + coverage delta | ⚪ Bassa — complementa code-reviewer subagent |
| **tech-debt-tracker** | `engineering/tech-debt-tracker/` | Scanner + dashboard debito tecnico | ⚪ Bassa — nice-to-have |

**Caveat Aider conversione**: `./scripts/install.sh --tool aider` produce `CONVENTIONS.md` (rules-flat), **non** SKILL.md nativo. Per workflow hub-delegation (3-tier routing) è lossy. Skill restano utili sia via Claude Code (primary) sia standalone (script Python stdlib).

## Tool — da `affaan-m/everything-claude-code` (140k⭐)

Hackathon-winner, v1.10.0 aprile 2026. Già estratto: AgentShield (commit `be315c9`).

| Tool | Valore | Rischio |
|------|--------|---------|
| **Instincts** (`/instinct-import`) | Estrae pattern da sessioni con confidence scoring → **formalizza ADR empirici** (tipo 0007/0008) in regole auto-richiamate | Basso — autore nativo, bug #148 chiuso |
| **Memory Persistence hooks** | SessionStart/Stop hooks + SQLite state store v1.9 → **automatizza JOURNAL** a fine sessione | Basso — 997 test passing, hook profiles opt-in |
| **Model routing** (`/model-route`, `/harness-audit`) | Codifica dichiarativa tier 7B/14B/30B (ADR-0009) invece di decision-tree mentale | Medio — richiede wiring custom a Ollama |

**Install strategy**: clone repo, `./install.sh typescript` con profile `minimal`, cherry-pick `hooks/` + `instincts/`. **NO** marketplace plugin install.

## Reference esterni — da `hesreallyhim/awesome-claude-code` curator (40k⭐)

Progetti production-ready linkati dalla curator list. Non dal repo stesso.

| Repo | Valore | Quando attivare |
|------|--------|-----------------|
| **[nizos/tdd-guard](https://github.com/nizos/tdd-guard)** | Hook blocca file-ops che violano TDD → estende guard rail globale con layer "behavior-critical edit senza test modificato = block" | Post-migrazione Evo-Tactics (usa test heavy) |
| **[zippoxer/recall](https://github.com/zippoxer/recall)** | Full-text search + resume sessioni Claude Code → context recovery across sessions | Qualunque momento, basso costo setup |
| **[hagan/claudia-statusline](https://github.com/hagan/claudia-statusline)** | Rust + SQLite persistent stats + context progress bar | **Post-19/05/2026** (monitorare consumo Claude Pro / switch a Ollama tier) |

## Hook candidate salvato localmente — `commit-guard.js`

Script 41 righe JS standalone (zero dep) estratto da `rohitg00/awesome-claude-code-toolkit/hooks/scripts/commit-guard.js`. Salvato in `scripts/hooks/commit-guard.js` del repo come asset riutilizzabile.

**Cosa fa**: hook PreToolUse Claude Code — intercetta `git commit -m "..."` eseguito da Claude durante una sessione e valida Conventional Commits (type(scope): description, ≤72 chars, no trailing period, lowercase first word).

**Complementare al guard rail globale**: il guard rail git in `~/.local/share/git-hooks/pre-commit` blocca silent-corruption (ADR-0008) a livello git. commit-guard.js blocca commit malformati a livello Claude Code PreToolUse **prima** che il git commit sia eseguito. Catena difesa:
1. Claude Code: `commit-guard.js` valida messaggio (PreToolUse hook)
2. git nativo: guard rail globale valida contenuto (pre-commit hook)
3. Husky repo-locale (se presente): validazioni policy repo (es. branch block `main`)

**Install quando utile**: aggiungere a `.claude/settings.local.json`:
```json
"hooks": {
  "PreToolUse": [
    { "matcher": "Bash", "hooks": [
      { "type": "command", "command": "node scripts/hooks/commit-guard.js" }
    ]}
  ]
}
```

**Non installato now**: script presente nel repo, hook config NON attivata. Attivare se in sessione Claude Code emergono commit message malformati auto-generati da Aider (pattern già osservato in behavior-critical routing).

## Tool rimandati a trigger specifici

| Tool | Trigger attivazione |
|------|---------------------|
| `GateGuard` (pip install gateguard-ai) | Quando claim "+2.25 quality" viene replicato indipendentemente |
| `Agno framework full` | Quando parte use case "DM AI Evo-Tactics campaign state" (memory semantica + multi-agent) |
| `rohitg00/awesome-claude-code-toolkit` MCP configs | Quando emerge use case MCP reale (K8s, AWS, Figma non previsti ora) |
| `LambdaTest/agent-skills` pytest/mocha | Se adotto skill framework nel workflow (non urgente, test già funzionano senza) |

## Policy install (ricordo da ADR-0010)

1. `gh skill preview <repo> <skill>` → leggi SKILL.md
2. Assess content/author/license/last-commit
3. Match con use case reale (non speculativo)
4. Install via `gh skill install` + 1 riga JOURNAL
5. Se impatto architetturale (hooks, MCP, runtime): ADR dedicato
