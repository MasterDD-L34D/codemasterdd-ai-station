# Frozen files index

## Purpose

This index identifies areas that are kept for memory, audit, or templates, but
must not be treated as current operating state in the transplanted checkout.

Use this together with:

- `PROJECT_STATE.yaml`
- `config/system-map.yaml`
- `docs/recovery/active-vs-historical-boundary.md`
- `docs/recovery/plan-inventory-2026-05-01.md`

## Frozen Or Historical Areas

| Area | Status | Use | Do not use for |
|------|--------|-----|----------------|
| `JOURNAL.md` | historical chronology | reconstruct what happened | current task state without verification |
| `docs/sessions/` | frozen session logs | audit old setup and decisions | live instructions |
| `docs/research/` | evidence snapshots | understand past research | time-sensitive current facts without recheck |
| `docs/agent-smoke-tests/` | historical validation | inspect old agent readiness work | current readiness claims |
| `Archivio_Libreria_Operativa_Progetti/` | imported framework/reference | templates, operating patterns, prompts | repo-specific current status |
| `STATUS_MULTI_REPO.md` | historical/dormant dashboard | see why cross-repo dashboard was demoted | live cross-repo monitoring |
| old ADR follow-up lists | historical decision context | understand prior intent | automatic active backlog |

## Mixed Areas

| Area | Status | Rule |
|------|--------|------|
| `.claude/agents/` | mixed active/dormant | use `.claude/agents/README.md` before invoking any agent |
| `docs/adr/` | historical plus active principles | current interpretation lives in `DECISIONS_LOG.md` |
| `docs/patterns/` | reusable patterns | check whether prerequisites exist locally |
| `scripts/` | source exists | machine effects must be verified before assuming success |
| `apps/dogfood-ui/` | scaffold/dormant | `/recovery` is safe; dogfood runtime needs DB/logs |
| `infra/` | scaffold/dormant | Docker/runtime state is not assumed |

## Active References

These are not frozen and should remain the current operating surface:

- `README.md`
- `PROJECT_STATE.yaml`
- `config/system-map.yaml`
- `AGENTS.md`
- `CLAUDE.md`
- `MASTER_PROMPT.md`
- `SPRINT_02.md`
- `BACKLOG.md`
- `ROADMAP.md`
- `DECISIONS_LOG.md`
- `OPEN_DECISIONS.md`
- `REFERENCE_INDEX.md`
- `EXTERNAL_REPOS.md`
- `docs/recovery/`

## Review Rule

When a frozen file contains a tempting "next action", do not execute it
directly. First ask:

1. Is the file current or historical?
2. Does the required path exist here?
3. Does `PROJECT_STATE.yaml` allow this area as active?
4. Is the task already represented in `BACKLOG.md` or `EXTERNAL_REPOS.md`?

If not, record it as historical or dormant.
