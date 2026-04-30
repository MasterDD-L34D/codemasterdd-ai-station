# OPEN_DECISIONS

Open decisions for the structural recovery.

## OD-R1 - Operational file: `CLAUDE.md` vs `AGENTS.md`

- Level: repo / agent interoperability.
- Status: open.
- Context: `CLAUDE.md` is tracked and historically authoritative. `AGENTS.md`
  exists locally as untracked context in this checkout.
- Default: keep `CLAUDE.md` tracked for historical continuity, but add
  Codex-aware notes. Do not commit the current untracked `AGENTS.md` without
  review because it includes transplanted context.
- Next action: decide after Sprint 02 whether to create a clean tracked
  `AGENTS.md` generated from the refreshed scope.

## OD-R2 - Runtime evidence export format

- Level: repo / observability.
- Status: open.
- Context: important evidence lived in gitignored logs, SQLite DBs, promptfoo
  outputs, and backup folders.
- Default: keep sensitive/runtime data ignored, but add a redacted export
  format under `docs/recovery/` for machine moves.
- Next action: write `docs/recovery/runtime-artifacts-policy.md`.

## OD-R3 - Agent quarantine depth

- Level: repo / automation.
- Status: open.
- Context: many `.claude/agents/` files are cross-repo and contain old absolute
  paths.
- Options:
  - Label them dormant in README only.
  - Add per-file quarantine banners.
  - Move them to a dormant folder.
- Default: label first, move later only if confusion persists.
- Next action: update `.claude/agents/README.md`.

## OD-R4 - `apps/dogfood-ui` active or dormant

- Level: repo / app scope.
- Status: open.
- Context: the app code exists, but DB/runtime state is absent and it includes
  Dafne integration.
- Default: mark as scaffold/dormant until local DB and service endpoints are
  intentionally restored.
- Next action: update app README and root docs.

## OD-R5 - Mojibake cleanup

- Level: documentation / portability.
- Status: open.
- Context: many historical files show mojibake.
- Default: do not do a global rewrite. Fix active root docs first, then decide
  whether historical logs need cleanup.
- Next action: add encoding policy.
