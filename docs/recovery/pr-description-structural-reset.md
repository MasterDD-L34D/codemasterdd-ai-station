# PR description - structural recovery

## Summary

This branch resets `codemasterdd-ai-station` governance after the repo was
transplanted away from the original workstation.

The goal is not to delete history. The goal is to stop stale cross-repo plans
from presenting themselves as live work.

## What changed

- Added recovery audit documenting missing paths, missing runtime evidence, and
  source-of-truth drift.
- Added `PROJECT_STATE.yaml` as a minimal machine-readable recovery state.
- Added `EXTERNAL_REPOS.md` with a reactivation gate.
- Added `SPRINT_02.md` focused on structural recovery.
- Rewrote root governance files to describe the current repo state.
- Demoted `STATUS_MULTI_REPO.md` to historical/dormant.
- Added clean `AGENTS.md` for Codex and simplified `CLAUDE.md` for
  Claude/OpenCode-compatible clients.
- Rebuilt `MODEL_ROUTING.md` as a recovery-safe routing policy.
- Added policies for instruction files, runtime artifacts, encoding, pre-merge
  checks, and reconnecting from the correct PC.
- Added `scripts/check-recovery-consistency.ps1` to catch stale active-state
  regressions.
- Added `config/system-map.yaml` and `config/machine-profile.example.yaml`.
- Added `scripts/recovery-status.ps1` and `scripts/check-all.ps1`.
- Added `docs/recovery/client-runtime-matrix.md` and ADR-0021.
- Added a recovery dashboard route in `apps/dogfood-ui` and made Dafne opt-in
  through `DAFNE_ENABLED=1`.
- Preserved OpenCode as an architectural/portability option instead of treating
  it as an active dependency.

## Why

The original repo referenced local paths and runtime artifacts that are not
present in the transplanted checkout:

- Game / Evo-Tactics
- Synesthesia
- Dafne swarm
- AA01
- Aider wrappers
- API key file
- dogfood logs
- dogfood SQLite DB
- promptfoo outputs

Without a reset, future agents could revive old plans that cannot be verified on
this machine.

## Merge guidance

Do not merge blindly on the correct PC.

Recommended path:

1. fetch this branch;
2. read `docs/recovery/reconnect-from-main.md`;
3. run `docs/recovery/pre-merge-checklist.md`;
4. verify which external repos and runtime artifacts exist on the correct PC;
5. merge or cherry-pick recovery pieces;
6. reactivate external repos one at a time.

## Validation

- `git diff --check` passed during branch work.
- `scripts/check-recovery-consistency.ps1` passed during branch work.
- `scripts/check-all.ps1` passed during branch work.
- Main was not modified from the transplanted checkout.
- Recovery branch was pushed as `origin/codex/structural-reset`.

## Known follow-ups

- Decide whether OpenCode becomes a real secondary client on the correct PC.
- Decide whether `apps/dogfood-ui` remains scaffold or gets runtime restored.
- Decide whether to fill `config/machine-profile.local.yaml` on the correct PC.
- Decide whether cross-repo agents should stay labelled dormant or be moved into
  a dormant folder.
- Normalize mojibake only in active docs, not via blind global rewrite.
