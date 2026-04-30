# Runtime artifacts policy

## Purpose

Runtime artifacts are useful evidence, but they should not silently become
required for repository comprehension.

This policy exists because the transplanted checkout did not contain old logs,
SQLite DBs, promptfoo results, or backup files referenced by governance docs.

## Classes

### Git-tracked sources

Examples:

- ADR
- root governance docs
- scripts
- infra config
- app source code

These can be trusted as present if they are in Git.

### Runtime evidence

Examples:

- `logs/aider-delegation-YYYY-MM.md`
- `apps/dogfood-ui/data/dogfood.sqlite`
- promptfoo JSON outputs
- Langfuse/Postgres local data
- local service health snapshots

These are trusted only when they exist in the current checkout or have been
freshly regenerated.

### Sensitive local backups

Examples:

- API key backups
- `.env`
- SQLite DB with private data
- machine-specific registry exports

These stay gitignored. If a summary is needed, create a redacted markdown report
under `docs/recovery/` or `docs/reference/`.

## Machine move procedure

Before moving this repo to another machine, create an optional redacted bundle:

1. `docs/recovery/runtime-manifest-YYYY-MM-DD.md`
2. summary of available logs, counts, date ranges, and checksums;
3. no secrets;
4. no raw private DB dumps;
5. clear statement of what was intentionally omitted.

Do not edit governance docs to claim runtime evidence exists unless it is either
committed or explicitly restored on the target machine.

## Current recovery state

As of 2026-04-30, the old dogfood log, dogfood SQLite DB, and promptfoo result
files are absent in this checkout.
