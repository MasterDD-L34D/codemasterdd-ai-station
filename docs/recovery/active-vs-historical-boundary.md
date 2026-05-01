# Active vs historical boundary

## Purpose

This document defines what is active in the transplanted checkout and what is
historical or dormant.

If another document disagrees during recovery, prefer this boundary plus
`PROJECT_STATE.yaml`.

## Active

| Area | Active file or location | Meaning |
|------|-------------------------|---------|
| Project state | `PROJECT_STATE.yaml` | Machine-readable recovery status. |
| Recovery sprint | `SPRINT_02.md` | Current work plan. |
| Backlog | `BACKLOG.md` | Current actionable task list. |
| Codex instructions | `AGENTS.md` | Codex entry point. |
| Claude/OpenCode instructions | `CLAUDE.md` | Compatibility entry point. |
| Portable prompt | `MASTER_PROMPT.md` | Browser/non-repo bootstrap. |
| External registry | `EXTERNAL_REPOS.md` | Dormant repo list and reactivation gate. |
| Decisions | `DECISIONS_LOG.md` | Current ADR index plus recovery decisions. |
| Recovery docs | `docs/recovery/` | Active recovery evidence and policies. |

## Active but scaffold-only

| Area | Path | Boundary |
|------|------|----------|
| dogfood UI | `apps/dogfood-ui/` | Source exists; runtime DB absent. |
| infra stack | `infra/` | Config exists; service state not assumed. |
| scripts | `scripts/` | Source exists; machine effects must be verified. |
| model routing | `MODEL_ROUTING.md` | Policy only; no model availability guarantee. |

## Historical

| Area | Path | Use |
|------|------|-----|
| Journal | `JOURNAL.md` | Chronology and reconstruction. Not automatic current state. |
| Sessions | `docs/sessions/` | Frozen setup history. |
| ADR | `docs/adr/` | Decision history. Current interpretation in `DECISIONS_LOG.md`. |
| Research | `docs/research/` | Evidence snapshots. Verify time-sensitive claims. |
| Patterns | `docs/patterns/` | Reusable workflows, not always active. |
| Agent smoke tests | `docs/agent-smoke-tests/` | Historical validation from old context. |
| Archive framework | `Archivio_Libreria_Operativa_Progetti/` | Library/reference, not live sprint. |

## Dormant

| Area | Path or concept | Reactivation requirement |
|------|-----------------|--------------------------|
| Evo-Tactics / Game | old `C:\dev\Game` | Verify local clone, remote, status, privacy. |
| Synesthesia | old `C:\dev\synesthesia` | Verify local clone and privacy scope. |
| Dafne swarm | old `C:\Users\edusc\Dafne\workspace\swarm` | Verify workspace and runtime. |
| AA01 | old `C:\Users\edusc\aa01` | Verify workspace and user intent. |
| Aider wrappers | old user-local bin path | Verify binaries and models. |
| API keys | old user-local config path | Verify existence without committing secrets. |
| dogfood evidence | gitignored logs/DB | Restore or regenerate locally. |

## Red flags

Treat these as stale unless they appear inside an audit or historical note:

- old HEAD hashes;
- old percent-complete claims;
- "service is up" without a current check;
- "Game pending" as current work;
- "Dafne day-5" as current work;
- dogfood counts without logs or DB;
- model availability without local verification.

## Reactivation rule

Dormant work can return only through this path:

```text
verify local evidence
  -> update EXTERNAL_REPOS.md
  -> update PROJECT_STATE.yaml
  -> update current sprint/backlog
  -> then act
```

Do not shortcut directly from historical notes to execution.
