# SPRINT_02 - Structural recovery

## Status

Active.

## Window

Starts 2026-04-30. Ends when the repo can be opened on a different machine
without resurrecting stale cross-repo plans.

## Objective

Make `codemasterdd-ai-station` portable, verifiable, and focused on its own
structure.

This sprint replaces the old "more dogfood" focus with a structural reset. The
previous dogfood dataset remains historical, but it is not actionable in this
checkout because the live logs and runtime DB are absent.

## Success criteria

- One current recovery audit exists.
- External repos are explicitly dormant unless reactivated.
- Root governance files agree on the same current state.
- ADR index includes all existing ADR files.
- `MASTER_PROMPT.md` no longer bootstraps stale state.
- `STATUS_MULTI_REPO.md` is historical or dormant, not a live dashboard.
- Backlog contains only tasks verifiable in this checkout.
- Missing runtime artifacts are documented instead of assumed.

## Tasks

### S2-01 - Recovery audit

- Create `docs/recovery/2026-04-30-transplant-audit.md`.
- Record real HEAD, missing paths, missing runtime artifacts, and drift.
- Mark the audit as the current recovery source for this sprint.

Status: done in this branch.

### S2-02 - External repo quarantine

- Create `EXTERNAL_REPOS.md`.
- Move all live cross-repo assumptions behind a reactivation gate.
- Treat Game, Synesthesia, Dafne, and AA01 as dormant until verified.

Status: done in this branch.

### S2-03 - Governance root refresh

Refresh:

- `README.md`
- `PROJECT_BRIEF.md`
- `COMPACT_CONTEXT.md`
- `ROADMAP.md`
- `BACKLOG.md`
- `DECISIONS_LOG.md`
- `OPEN_DECISIONS.md`
- `REFERENCE_INDEX.md`
- `MASTER_PROMPT.md`

Status: done in this branch.

### S2-04 - Dashboard demotion

- Mark `STATUS_MULTI_REPO.md` as historical/dormant.
- Point current cross-repo state to `EXTERNAL_REPOS.md`.
- Stop treating old service/runtime state as live.

Status: done in this branch.

### S2-05 - Agent surface reduction

- Keep `.claude/agents/` files for historical continuity.
- Mark cross-repo agents as dormant or requiring reactivation.
- Keep core agents usable only when their inputs exist in this checkout.

Status: done in this branch (`.claude/agents/README.md`).

### S2-06 - Runtime evidence policy

- Document that gitignored logs, SQLite DBs, and promptfoo results are local
  runtime evidence.
- Add a future export/import policy if those artifacts need to survive machine
  moves.

Status: done in this branch (`docs/recovery/runtime-artifacts-policy.md`).

### S2-07 - Encoding and portability pass

- Do not attempt a blind global rewrite.
- Prefer ASCII in newly edited docs.
- Later, normalize active root docs from mojibake to UTF-8 with explicit review.

Status: done in this branch (`docs/recovery/encoding-policy.md`).

### S2-08 - Original system reconstruction

- Reconstruct how the original system was supposed to work.
- Preserve OpenCode as architectural option/portability bridge, not active
  dependency.
- Add reconnect playbook for the correct PC.

Status: done in this branch (`docs/recovery/original-system-intent.md` and
`docs/recovery/reconnect-from-main.md`).

### S2-09 - Instruction surface cleanup

- Create clean tracked `AGENTS.md` for Codex.
- Add instruction-file policy for `AGENTS.md`, `CLAUDE.md`, and
  `MASTER_PROMPT.md`.
- Rebuild `MODEL_ROUTING.md` as recovery-safe routing policy.

Status: done in this branch.

### S2-10 - Merge readiness package

- Add pre-merge checklist.
- Add PR description draft.
- Make the branch easier to review from the correct PC.

Status: done in this branch.

## Out of scope

- Fixing or triaging Game.
- Running Synesthesia privacy validation.
- Starting Dafne or repairing its process model.
- Recreating missing dogfood logs from memory.
- Rebuilding old runtime services just to match stale docs.

## Working rule for this sprint

If a task needs a path that does not exist in this checkout, it is not a task
for this sprint. It becomes a reactivation candidate in `EXTERNAL_REPOS.md`.
