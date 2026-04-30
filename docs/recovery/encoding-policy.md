# Encoding policy

## Problem

Several historical markdown files show mojibake such as `Ã`, `â€”`, and similar
replacement artifacts. This appears to be an encoding/transport issue across
Windows tooling.

## Policy

- New recovery docs should use ASCII unless non-ASCII is necessary.
- Do not perform a blind global encoding rewrite.
- Fix active root docs first.
- Treat historical logs and session files as frozen unless they must be read for
  a current decision.
- When fixing a file, review the diff manually.

## Active files

The following are active and should stay readable:

- `README.md`
- `PROJECT_BRIEF.md`
- `COMPACT_CONTEXT.md`
- `ROADMAP.md`
- `BACKLOG.md`
- `DECISIONS_LOG.md`
- `OPEN_DECISIONS.md`
- `MASTER_PROMPT.md`
- `REFERENCE_INDEX.md`
- `EXTERNAL_REPOS.md`
- `SPRINT_02.md`
- `docs/recovery/*.md`

## Deferred files

The following may retain historical mojibake until needed:

- `JOURNAL.md`
- `docs/sessions/*`
- old ADR text
- imported archive framework material
- old cross-repo dashboards and smoke tests
