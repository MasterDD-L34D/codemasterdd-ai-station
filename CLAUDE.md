# CLAUDE.md

Recovery-first operating context for CodeMasterDD AI Station.

## Current status

This repository was transplanted to a machine that does not contain the original
external project paths or runtime evidence. Older versions of this file
described the original workstation in detail, but that context is now historical
unless revalidated.

## Read first

1. `docs/recovery/2026-04-30-transplant-audit.md`
2. `PROJECT_BRIEF.md`
3. `COMPACT_CONTEXT.md`
4. `SPRINT_02.md`
5. `BACKLOG.md`
6. `EXTERNAL_REPOS.md`
7. `DECISIONS_LOG.md`

## Active rule

This repo governs only itself.

External projects are dormant until reactivated:

- Evo-Tactics / Game
- Synesthesia
- Dafne swarm / evo-swarm
- AA01

Use `EXTERNAL_REPOS.md` as the reactivation gate.

## Active work

Active sprint: `SPRINT_02.md` - Structural recovery.

Do:

- keep root governance coherent;
- separate historical memory from current plan;
- verify local paths before trusting old instructions;
- document missing runtime evidence;
- prefer small, reviewable structural changes.

Do not:

- act on Game/Synesthesia/Dafne/AA01 tasks from this repo;
- assume old logs or SQLite DBs exist;
- claim runtime services are up without checking locally;
- revive stale Sprint 01 dogfood tasks as current work.

## Language and style

- Communicate with Eduardo in Italian.
- Use English for code identifiers and commit messages.
- Prefer ASCII in newly edited docs during recovery.
- Keep historical files unless there is a clear reason to rewrite them.

## Git

- Main branch: `main`.
- Recovery branch convention: `codex/...`.
- Conventional commits remain preferred.
- No force push to `main`.

## Historical note

The previous `CLAUDE.md` contained detailed original-machine context: hardware,
Ollama models, Aider wrappers, cross-repo projects, and Fase 6 dogfood rules.
That material was intentionally replaced during structural recovery because it
referenced missing paths and stale plans. Use Git history if that original
context must be inspected.
