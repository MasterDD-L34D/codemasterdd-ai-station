# AA01 Task B — Subagent + memory evaluation (2 repo)

> **🟢 RESOLVED 2026-05-12 (anti-rot pointer, no re-triage)** — Scaffold AA01 SUPERSEDED dalla decisione finale. Verdetti shippati: **#4** claude-mem = INSTALLED 12/5 → DISABLED 14/5 (canonico `false`, upstream console-flash #19012) · **#11** VoltAgent subagents = REFRESH cherry-pick **dormant-no-trigger** (REFRESH≠INSTALL; nessun use-case reale fired — stack ha già jules-pr-triager + 18 subagent + superpowers). Fonte-verità: `docs/reference/subagents-skills-candidates.md` §"Riepilogo decisioni preliminari" + canonical `shipped_triage_reference_ANTI_ROT`. Nessuna azione autonoma residua. NON re-triagare.

> **Preset**: `research-long`
> **Slug**: `2026-05-12-B-subagent-memory-resources`
> **Effort stima**: 2-3 ore (claude-mem install + integration + subagent cherry-pick refresh)
> **Trigger origin**: screenshot OCR Eduardo 2026-05-12, sessione codemasterdd
> **Reference master**: `docs/reference/subagents-skills-candidates.md` sezione "Wave 2026-05-12 categoria B"
> **BACKLOG entry**: M12

## Scope

| # | Repo | Stars reali | Use case + path |
|---|------|-------------|----------------|
| 4 | `thedotmack/claude-mem` | ~70-75k | Persistent context cross-session via SQLite + SessionStart/Stop hooks. INSTALL `~/.local/bin/claude-mem` + `~/.claude/settings.json` hook wire-up |
| 11 | `VoltAgent/awesome-claude-code-subagents` (REFRESH) | ~8.1-8.5k (era 17.9k Apr 22 — OCR drift) | Cherry-pick subagent vs nostri 18. Refresh = re-audit catalogo per nuovi entry post-Apr 22 |

## Criteri DRAFT -> PROPOSED

**Repo #4 claude-mem**:
1. Install verify: `npm install -g @thedotmack/claude-mem` o equiv (verify install method README)
2. Security audit: SQLite locale only, NO network calls (grep source). License MIT.
3. Hook wire-up dry run: `~/.claude/settings.json` SessionStart + Stop con env vars test (NON-destructive prima di commit prod)
4. **Overlap decision** vs `affaan-m/everything-claude-code` Memory Persistence: scegli UNO. Recommended claude-mem (dedicato, 70k+ stars vs sub-feature, battle-tested standalone). DEPRECATE Memory Persistence subset di item #1 task A.
5. Smoke test: sessione codemasterdd 5 min con claude-mem attivo, verify context restoration prossima sessione

**Repo #11 subagent refresh**:
1. Re-scan catalogo VoltAgent: `git clone --depth 1 <url> ~/tmp-eval/voltagent-subagents && ls 04-quality-security/ 06-developer-experience/` etc
2. Compare vs i nostri 18 sub-agent (codemasterdd `.claude/agents/`): identificare gap, overlap, complementari
3. Audit i 4 candidati gia identificati (code-reviewer, test-automator, dependency-manager, debugger) — sono ancora validi? Manutenuti?
4. Eventuale nuovo candidato emerso post Apr 22 (es. ADR-drafter alternativo, PR-watcher, GitHub-agent)

PROPOSED: decisione INSTALL/SKIP per claude-mem + lista subagent da cherry-pick (con path target `.claude/agents/`).

## Criteri SHIP

- [ ] **claude-mem**:
  - Installato e operativo su codemasterdd session (smoke test PASS)
  - JOURNAL entry con setup procedura
  - Update `~/.claude/settings.json` committed in personal config (NON in repo se in `settings.local.json`)
  - **ADR-0027 candidato**: se hook wire-up impatta SessionStart workflow esistente codemasterdd (gia H12 hooks attivi) -> ADR necessario per documentare interaction. Trigger valutare durante SHIP.
- [ ] **subagent refresh**:
  - Re-audit completato, tabella `subagents-skills-candidates.md` line 9-14 aggiornata con stars reali + nuovi candidati
  - 0-2 subagent nuovi installati (cherry-pick selettivo, NO bulk)
- [ ] Lesson `learnings/L-2026-05-NNN-memory-subagent-cherry-pick.md`

## Anti-pattern

- Install claude-mem + Memory Persistence (#1) entrambi -> doppia memory + drift sync, SPOF (gia segnalato in task A)
- Bulk install tutti i 100+ subagent VoltAgent -> collision name con i nostri 18, confusion routing
- Hook wire-up senza dry run -> rischio rompere session start codemasterdd attuale (H12)
- Skip ADR-0027 candidato se SessionStart workflow cambia (documentare prima di committare config prod)

## Note operative

- **claude-mem install commands** (verifica README):
  ```bash
  npm install -g @thedotmack/claude-mem  # ipotetico, verify
  claude-mem init  # setup SQLite store
  # edit ~/.claude/settings.json
  ```
- **Settings hook pattern** (esempio scope wire-up):
  ```json
  {
    "hooks": {
      "SessionStart": [{ "type": "command", "command": "claude-mem restore" }],
      "Stop": [{ "type": "command", "command": "claude-mem capture" }]
    }
  }
  ```
- **Interaction con H12 hooks codemasterdd**: il nostro `SessionStart` hook salva HEAD in `.claude/.session-start-head`. claude-mem aggiunge `restore`. Compatibile (entrambi command type, sequential exec). Verify ordine + nessuna race.

## Output atteso

- 1 sistema memory persistente operativo (claude-mem o fallback decisione)
- 0-2 subagent nuovi in `.claude/agents/` codemasterdd (cherry-pick)
- 1 lesson decisional pattern memory choice + subagent cherry-pick
- 0-1 ADR-0027 candidato se SessionStart workflow impatto significativo
- Update `subagents-skills-candidates.md` con stato refresh
