# REFERENCE_INDEX

Current reference index after structural recovery started.

## Active recovery references

| Code | File | Purpose |
|------|------|---------|
| REC-01 | `docs/recovery/2026-04-30-transplant-audit.md` | Current audit of transplant drift, missing paths, missing evidence. |
| REC-02 | `EXTERNAL_REPOS.md` | Dormant external repo registry and reactivation gate. |
| REC-03 | `SPRINT_02.md` | Active sprint for structural recovery. |
| REC-04 | `BACKLOG.md` | Active actionable task list. |
| REC-05 | `COMPACT_CONTEXT.md` | Short current snapshot. |
| REC-06 | `docs/recovery/original-system-intent.md` | Reconstruction of original OpenCode/Ollama/Aider/system intent. |
| REC-07 | `docs/recovery/reconnect-from-main.md` | How to review and reconnect this branch from the correct PC. |
| REC-08 | `docs/recovery/instruction-files-policy.md` | Contract for AGENTS/CLAUDE/MASTER_PROMPT roles. |
| REC-09 | `docs/recovery/pre-merge-checklist.md` | Checklist before merging the recovery branch. |
| REC-10 | `docs/recovery/pr-description-structural-reset.md` | Draft PR description for GitHub review. |

## Active governance references

| Code | File | Purpose |
|------|------|---------|
| GOV-01 | `README.md` | Human entry point for this checkout. |
| GOV-02 | `PROJECT_BRIEF.md` | Current scope and success criteria. |
| GOV-03 | `DECISIONS_LOG.md` | ADR index and recovery decisions. |
| GOV-04 | `OPEN_DECISIONS.md` | Decisions still open during recovery. |
| GOV-05 | `ROADMAP.md` | Recovery roadmap. |
| GOV-06 | `MASTER_PROMPT.md` | Portable prompt with current recovery context. |
| GOV-07 | `AGENTS.md` | Codex entry point. |
| GOV-08 | `CLAUDE.md` | Claude/OpenCode-compatible entry point. |
| GOV-09 | `MODEL_ROUTING.md` | Recovery-safe routing policy. |

## Historical but retained

| Area | Status | Notes |
|------|--------|-------|
| `JOURNAL.md` | historical/live log | Useful for reconstruction, not automatic current state. |
| `docs/sessions/` | frozen | Old session logs. |
| `Archivio_Libreria_Operativa_Progetti/` | frozen library | Imported framework. Consult only when needed. |
| `STATUS_MULTI_REPO.md` | historical/dormant | Old cross-repo dashboard; see `EXTERNAL_REPOS.md` instead. |
| `.claude/agents/` | mixed | Core agents may remain useful; cross-repo agents require reactivation. |
| `docs/agent-smoke-tests/` | historical | Evidence of old agent validation, not current runtime state. |

## ADR

ADR directory: `docs/adr/`.

There are 20 ADR files. See `DECISIONS_LOG.md` for the current index.

## Runtime evidence

The following are not active references unless present in the current checkout:

- `logs/aider-delegation-*.md`
- `apps/dogfood-ui/data/*.sqlite`
- promptfoo results
- backup files
- external repo working trees

## Deprecated references

Old statements that say SPRINT_01 is active, 14 ADR exist, or cross-repo
services are live should be treated as stale unless updated during Sprint 02.
