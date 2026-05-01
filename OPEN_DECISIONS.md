# OPEN_DECISIONS

Open decisions for the structural recovery.

## OD-R1 - Operational file: `CLAUDE.md` vs `AGENTS.md`

- Level: repo / agent interoperability.
- Status: resolved in Sprint 02.
- Context: `CLAUDE.md` is tracked and historically authoritative. `AGENTS.md`
  now exists as a clean tracked Codex entry point.
- Default: keep `CLAUDE.md` tracked for historical continuity and keep
  `AGENTS.md` as the Codex entry point.
- Resolution: keep both. `AGENTS.md` is the Codex entry point; `CLAUDE.md` is
  the Claude/OpenCode-compatible entry point.

## OD-R2 - Runtime evidence export format

- Level: repo / observability.
- Status: partly resolved.
- Context: important evidence lived in gitignored logs, SQLite DBs, promptfoo
  outputs, and backup folders.
- Default: keep sensitive/runtime data ignored, but add a redacted export
  format under `docs/recovery/` for machine moves.
- Resolution: policy exists in `docs/recovery/runtime-artifacts-policy.md`.
- Remaining question: whether a redacted export bundle is needed later.

## OD-R3 - Agent quarantine depth

- Level: repo / automation.
- Status: partly resolved.
- Context: many `.claude/agents/` files are cross-repo and contain old absolute
  paths.
- Options:
  - Label them dormant in README only.
  - Add per-file quarantine banners.
  - Move them to a dormant folder.
- Default: label first, move later only if confusion persists.
- Resolution: label first. Move later only if confusion persists.

## OD-R4 - `apps/dogfood-ui` active or dormant

- Level: repo / app scope.
- Status: partly resolved.
- Context: the app code exists, but DB/runtime state is absent and it includes
  Dafne integration.
- Default: mark as scaffold/dormant until local DB and service endpoints are
  intentionally restored.
- Resolution: scaffold/dormant with a recovery dashboard. Dafne is opt-in via
  `DAFNE_ENABLED=1`.

## OD-R5 - Mojibake cleanup

- Level: documentation / portability.
- Status: partly resolved.
- Context: many historical files show mojibake.
- Default: do not do a global rewrite. Fix active root docs first, then decide
  whether historical logs need cleanup.
- Current policy: `docs/recovery/encoding-policy.md`.
- Resolution: `PROMPT_LIBRARY.md` was rewritten as a recovery-safe ASCII prompt
  catalogue. Historical files remain frozen unless edited for another reason.
- Next action: clean only active files when they are edited for another reason.
