# Final review package

## Purpose

This is the final recovery handoff for branch `codex/structural-reset`.

Use it on the correct PC before deciding how to reconnect the branch to `main`.

## Current Branch State

- Branch: `codex/structural-reset`
- Current package includes commits through the final archive/review pass.
- Main policy: do not modify `main` from the transplanted checkout.
- Recovery mode: active on this branch.
- External repos: dormant until reactivated.

## What This Branch Is

This branch is a structural recovery package:

- it shrinks active scope to `codemasterdd-ai-station`;
- it quarantines external repos;
- it separates runtime evidence from tracked source;
- it rebuilds agent/client instruction surfaces;
- it adds diagnostics and review checklists;
- it preserves history without letting history drive current work.

## What This Branch Is Not

It is not:

- a Game fix branch;
- a Synesthesia privacy validation branch;
- a Dafne runtime repair branch;
- an AA01 review branch;
- a dogfood evidence reconstruction branch;
- a proof that LiteLLM, Langfuse, Ollama, Aider, or OpenCode are live here.

## Read In This Order

1. `PROJECT_STATE.yaml`
2. `docs/recovery/2026-04-30-transplant-audit.md`
3. `docs/recovery/plan-inventory-2026-05-01.md`
4. `docs/recovery/frozen-files-index.md`
5. `EXTERNAL_REPOS.md`
6. `docs/recovery/pre-merge-checklist.md`
7. `docs/recovery/reconnect-from-main.md`

## Merge Recommendation

Recommended path on the correct PC: hybrid merge.

Bring in:

- recovery docs;
- `EXTERNAL_REPOS.md`;
- clean instruction files;
- project state and system map;
- check scripts;
- dashboard recovery route.

Then decide, from fresh evidence, whether old root docs or runtime claims should
be reactivated.

Avoid full trust in either side:

- the old `main` may contain real original-machine facts;
- this branch contains correct transplant recovery facts;
- only the correct PC can reconcile both.

## Pre-Merge Command Set

```powershell
git switch main
git fetch origin
git status --short --branch
git log --oneline --decorate -5
git log --oneline main..origin/codex/structural-reset
git diff --stat main..origin/codex/structural-reset
```

Then run the checklist:

```powershell
.\scripts\check-recovery-consistency.ps1
.\scripts\check-all.ps1
```

## Reactivation Order

Reactivate at most one area at a time:

1. local machine profile;
2. runtime evidence;
3. Aider/hooks/model wrappers;
4. dogfood UI DB/logs;
5. LiteLLM/Langfuse/promptfoo;
6. Game;
7. Synesthesia;
8. Dafne;
9. AA01.

## Stop Conditions

Stop and reassess if:

- a path exists but remote/branch status is unknown;
- runtime evidence exists but contradicts the recovery docs;
- secrets or backup files appear in Git status;
- a frozen file is being used as live instruction;
- a cross-repo task appears before reactivation.

## Final Local Verdict

The transplanted checkout is now reviewable and controlled.

The next meaningful work belongs on the correct PC, not in this transplanted
checkout.
