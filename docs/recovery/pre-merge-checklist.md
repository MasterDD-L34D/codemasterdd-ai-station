# Pre-merge checklist

Use this before merging `codex/structural-reset` into `main` on the correct PC.

## 1. Confirm branch context

```powershell
git switch main
git fetch origin
git status --short --branch
git log --oneline --decorate -5
git log --oneline main..origin/codex/structural-reset
git diff --stat main..origin/codex/structural-reset
```

## 2. Verify local machine reality

```powershell
Test-Path C:\dev\Game
Test-Path C:\dev\synesthesia
Test-Path C:\Users\edusc\Dafne\workspace\swarm
Test-Path C:\Users\edusc\aa01
Test-Path C:\Users\edusc\.local\bin
Test-Path C:\Users\edusc\.config\api-keys\keys.env
```

## 3. Verify runtime evidence

```powershell
Test-Path logs\aider-delegation-2026-04.md
Test-Path apps\dogfood-ui\data\dogfood.sqlite
Test-Path scripts\quality-bench\results
```

If these are missing, keep the recovery branch's dormant classification.

If they exist, inspect them before changing status:

```powershell
Get-Item logs\aider-delegation-2026-04.md
Get-Item apps\dogfood-ui\data\dogfood.sqlite
```

## 4. Review instruction files

Check:

- `AGENTS.md`
- `CLAUDE.md`
- `MASTER_PROMPT.md`
- `docs/recovery/instruction-files-policy.md`

They should agree that:

- repo governs itself by default;
- external repos require reactivation;
- stale path assumptions are not live facts.

## 5. Decide merge style

Recommended: hybrid merge.

Bring in recovery docs and clean governance, then re-enable any external repo
from fresh evidence.

Avoid:

- `git reset --hard` to this branch;
- blind full merge if old machine state is actually live and should be
  preserved in a more nuanced form;
- restoring old `STATUS_MULTI_REPO.md` as live without verification.

## 6. Reactivate one external repo at a time

For each repo:

1. verify path;
2. verify git remote;
3. verify branch/status;
4. verify privacy class;
5. update `EXTERNAL_REPOS.md`;
6. update `STATUS_MULTI_REPO.md` only if cross-repo dashboard is being revived.

## 7. Post-merge checks

```powershell
git diff --check
git status --short --branch
```

Then open the repo in the intended agent/client and confirm it reads the correct
instruction file.
