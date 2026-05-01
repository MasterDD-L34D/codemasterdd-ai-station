# AGENTS.md

Codex operating instructions for this repository.

## Current mode

Structural recovery.

This checkout was transplanted away from the original workstation. Do not assume
that old local paths, runtime services, logs, API keys, or external repos exist.

## Read first

1. `docs/recovery/2026-04-30-transplant-audit.md`
2. `PROJECT_STATE.yaml`
3. `PROJECT_BRIEF.md`
4. `COMPACT_CONTEXT.md`
5. `SPRINT_02.md`
6. `BACKLOG.md`
7. `EXTERNAL_REPOS.md`
8. `DECISIONS_LOG.md`

## Core rule

This repo governs only itself.

External projects are dormant until reactivated through `EXTERNAL_REPOS.md`:

- Evo-Tactics / Game
- Synesthesia
- Dafne swarm / evo-swarm
- AA01

Do not act on those projects from this checkout unless the user explicitly asks
and the local path/git/runtime state has been freshly verified.

## Active work

Active sprint: `SPRINT_02.md`.

Allowed recovery work:

- improve repository structure;
- update root governance docs;
- clarify instruction-file hierarchy;
- document missing runtime evidence;
- improve recovery playbooks;
- prepare branch integration material for the correct PC.

Out of scope:

- fixing Game/Synesthesia/Dafne/AA01;
- recreating missing dogfood logs from memory;
- claiming services are live without local checks;
- editing runtime secrets or backup files.

## Instruction files

- `AGENTS.md`: Codex entry point.
- `CLAUDE.md`: Claude/OpenCode compatibility entry point.
- `MASTER_PROMPT.md`: portable prompt for browser or non-repo contexts.

Keep these files short and aligned. Do not duplicate long historical state in
all three.

## Git

- Work on branch `codex/structural-reset` unless the user explicitly changes
  direction.
- Do not modify `main` from this transplanted checkout.
- Commit messages use Conventional Commits.
- Prefer small, meaningful commits.
- Push recovery branches so the correct PC can review them.

## Editing style

- New recovery docs should be ASCII unless non-ASCII is necessary.
- Do not perform blind global rewrites.
- Historical files may remain stale/mojibake unless they are active guidance.
- Prefer documenting dormancy/reactivation over deleting historical material.

## Verification

Before finalizing recovery work:

- run `git diff --check`;
- run `.\scripts\check-recovery-consistency.ps1`;
- inspect `git status --short --branch`;
- ensure root docs do not present missing external repos as live;
- keep runtime artifacts gitignored unless a redacted policy says otherwise.
