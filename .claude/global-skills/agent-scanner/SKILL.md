---
name: agent-scanner
description: >
  Use BEFORE selecting/recommending any subagent/skill/agent for a
  non-trivial task. Anti-shadow-duplicate (build on existing work,
  never recreate; Ibrahim 2026 + Microsoft Multi-Agent Ref Arch).
  Triggers: "scan agents", "quali agenti ho", "inventario agenti",
  "riusa agente", "registry", "overlap", "mappa agenti",
  "che agent uso", "serve un agent per X", "team formation".
tools: [Bash, Glob, Grep, Read]
---

# Agent Scanner (LITE, cross-project)

Cross-project skill that enumerates available subagents / skills / agent
references and outputs a markdown report read-only. NO write to disk, NO
registry persist, NO overlap math. Principio guida: **build on existing
work, never recreate**.

For full ARCHON-context analysis (overlap calc 7 ruoli + REUSE_AUTO/CONFIRM/
COMPLEMENT thresholds + registry persistence), see
`aa01/archon/skills/agent-scanner/SKILL.md` (vendored nel git del vault,
cross-PC; used only when `aa01/archon/` is detected in CWD or `$HOME`).

---

## When to invoke

| Trigger | Quando |
|---------|--------|
| **BOOTSTRAP** | New session on a project -> step 1 prima di routing agent. |
| **TEAM_FORMATION** | Prima di proporre o creare un nuovo agent specializzato. |
| **DELTA** | A inizio sessione, diff vs scan precedente (signal cambi recenti). |
| **ON_DEMAND** | Comando utente esplicito ("scan agents"). |

---

## Procedure (5 step)

### Step 1 -- Enumerate sources (graceful-missing)

In ordine di priorita' decrescente, ogni find ha `2>/dev/null`:

```bash
# 1. PROJECT agents
find .claude/agents -maxdepth 2 -name "*.md" -type f 2>/dev/null

# 2. USER global agents
find "$HOME/.claude/agents" -maxdepth 2 -name "*.md" -type f 2>/dev/null

# 3. PROJECT skills
find .claude/skills -maxdepth 3 -name "SKILL.md" -type f 2>/dev/null

# 4. USER global skills
find "$HOME/.claude/skills" -maxdepth 3 -name "SKILL.md" -type f 2>/dev/null

# 5. Plugin agents + skills (PROJECT)
find .claude/plugins -maxdepth 6 -name "*.md" -type f 2>/dev/null | grep -E "(agents|skills)/"

# 5b. Plugin agents + skills (USER global cache, e.g. caveman cavecrew)
find "$HOME/.claude/plugins" -maxdepth 6 -name "*.md" -type f 2>/dev/null | grep -E "(agents|skills)/"

# 6. Inline mentions
grep -lE "^---$" AGENTS.md CLAUDE.md 2>/dev/null

# 7. ARCHON pointer (AA01 detection -- fires wherever aa01/archon present)
if [ -d "$HOME/aa01/archon" ] || [ -d "$(pwd)/aa01/archon" ]; then
  echo "ARCHON_DETECTED -> see aa01/archon/skills/agent-scanner/SKILL.md for FULL version"
fi
```

**Note**: ARCHON/AA01 e' vendored nel git del vault (`Vault-ops-remote/claude-global/aa01-system/archon`, codemasterdd PR #72 / vault commit `275f8bc5f`) e presente su Ryzen -- NON e' Lenovo-only. Source 7 scatta su qualunque PC dove `aa01/archon` e' deployato (Ryzen incluso) -> il tier FULL si attiva. Su un PC senza quel deploy source 7 e' assente, NON e' un errore -- il report omette semplicemente il pointer ARCHON (graceful-missing).

### Step 2 -- Parse frontmatter

Per ogni file trovato, estrai il YAML frontmatter tra `---` e `---`:
- Required: `name`, `description`.
- Optional: `tools`, `model`, `permissionMode`, `memory`, `skills`.

Se malformed o mancante:
- File in `.claude/agents/` o `~/.claude/agents/` -> log `MALFORMED FRONTMATTER: <path>` in report, skip quel file, continua.
- Altrove -> silently skip.

Se zero file trovati totali: output esplicito "no agents discovered in any source -- baseline: general-purpose only", NON silent-empty.

Se la enumerazione fallisce per una source specifica (permission denied su una dir): log `SOURCE UNREADABLE: <path>` nel report (distinguibile da "no agents found" legitimate).

### Step 3 -- Output markdown report (read-only)

Cap **hard 50 entries**. Se inventory > 50:
- Rank by source priority order (1-7 nel listing sopra).
- Tieni le top-50 in tabella.
- Aggiungi footer `+N more in <source>` per ogni source che ha entries droppate.

Format del report:

```markdown
## Agent discovery report (scope: <cwd>)

| name | description (truncated 80ch) | source | tools / model |
| --- | --- | --- | --- |
| harsh-reviewer | Tough quality review (code / ADR / plan) | ~/.claude/agents/ | All / opus |
| sot-drift-verifier | Sovereign gated SoT-vs-runtime verdict | .claude/agents/ | Read,Grep,Glob,Bash / inherit |
| ... | ... | ... | ... |

## Next-action hint

Consider REUSING an existing agent above before creating new
(anti-shadow-duplicate, Ibrahim 2026 + Microsoft Multi-Agent Ref Arch).

## ARCHON full version

If `aa01/archon/` detected -> use `aa01/archon/skills/agent-scanner/SKILL.md`
for overlap calc + role mapping + registry persistence.
```

### Step 4 -- Anti-pattern bloccati (segnalare in report se rilevati)

- **Shadow duplication**: due agent con descrizione overlap-keywords (manual review post-report).
- **Silent override**: due file con stesso `name:` in source diverse -> warning esplicito `SILENT OVERRIDE: <name> appears in <pathA> and <pathB>`.
- **Forgotten agents**: file con last-modified > 90 giorni fa e mai citato in altri agent description -> footnote `DORMANT (>90d)`.

### Step 5 -- (NOT done in LITE)

ARCHON-specific steps 3 (overlap calc 7 ruoli) + 4 (REUSE thresholds) + 5 (registry write) sono **DROP** dalla LITE. Per quelli, esegui `aa01/archon/skills/agent-scanner/SKILL.md`.

---

## Output constraints

- NO write su disco (read-only).
- NO registry persist.
- Output size cap 50 entries.
- Output e' markdown direttamente quotable nel main thread context.
