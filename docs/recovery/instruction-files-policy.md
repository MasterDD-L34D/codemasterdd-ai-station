# Instruction files policy

## Purpose

This repo may be opened by different coding agents or clients. During recovery,
instruction files must prevent stale state from being reintroduced.

## Files and roles

| File | Primary audience | Role |
|------|------------------|------|
| `AGENTS.md` | Codex | Short operational entry point for this repo. |
| `CLAUDE.md` | Claude Code / OpenCode-compatible clients | Compatibility entry point. |
| `MASTER_PROMPT.md` | Browser chats / external tools | Portable prompt when repo files are not automatically loaded. |

## Hierarchy

When these files disagree during recovery:

1. `docs/recovery/2026-04-30-transplant-audit.md`
2. `PROJECT_BRIEF.md`
3. `COMPACT_CONTEXT.md`
4. `SPRINT_02.md`
5. `AGENTS.md` or `CLAUDE.md`, depending on client
6. `MASTER_PROMPT.md`
7. historical docs

## Design rules

- Keep instruction files short.
- Do not copy full hardware inventories into every instruction file.
- Do not include external repo status unless it is verified in the current
  checkout.
- Link to recovery docs instead of duplicating recovery details.
- Prefer "dormant until reactivated" over "pending" for unavailable external
  repos.

## OpenCode compatibility

OpenCode was part of the original system as an evaluated client and portability
bridge. Its value was not only execution; it could read repo-native instruction
files.

Therefore:

- keep `CLAUDE.md` clean and compatible;
- keep `AGENTS.md` clean for Codex;
- keep shared policy in recovery docs;
- do not make OpenCode an active dependency unless it is installed and tested on
  the correct PC.

## Update protocol

When changing active scope:

1. update `PROJECT_BRIEF.md`;
2. update `COMPACT_CONTEXT.md`;
3. update `SPRINT_02.md` or current sprint;
4. update `AGENTS.md` and `CLAUDE.md` only if agent behavior changes;
5. update `MASTER_PROMPT.md` only if portable bootstrap behavior changes.

## Anti-patterns

- Three instruction files with three different project states.
- Prompt files that hard-code old HEAD values.
- Client-specific files that revive cross-repo work without reactivation.
- Treating OpenCode/Aider/Claude/Codex as the system itself.

The system is the repo governance loop; clients are replaceable execution
surfaces.
