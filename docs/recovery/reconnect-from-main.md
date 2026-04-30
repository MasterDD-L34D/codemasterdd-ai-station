# Reconnect this branch from the correct PC

## Goal

Use `codex/structural-reset` as a reviewable recovery branch without modifying
`main` blindly.

## On the current transplanted PC

Push the branch when ready:

```powershell
git push -u origin codex/structural-reset
```

Do not force push `main`.

## On the correct PC

From the original/correct checkout:

```powershell
git switch main
git fetch origin
git branch --show-current
git status --short
git log --oneline --decorate -5
git log --oneline main..origin/codex/structural-reset
git diff --stat main..origin/codex/structural-reset
```

Then inspect:

```powershell
git diff main..origin/codex/structural-reset -- README.md PROJECT_BRIEF.md COMPACT_CONTEXT.md BACKLOG.md ROADMAP.md
git diff main..origin/codex/structural-reset -- DECISIONS_LOG.md OPEN_DECISIONS.md MASTER_PROMPT.md REFERENCE_INDEX.md
git diff main..origin/codex/structural-reset -- docs/recovery EXTERNAL_REPOS.md SPRINT_02.md
```

## Before merging

Verify local reality on the correct PC:

```powershell
Test-Path C:\dev\Game
Test-Path C:\dev\synesthesia
Test-Path C:\Users\edusc\Dafne\workspace\swarm
Test-Path C:\Users\edusc\.local\bin
Test-Path C:\Users\edusc\.config\api-keys\keys.env
Test-Path logs\aider-delegation-2026-04.md
Test-Path apps\dogfood-ui\data\dogfood.sqlite
```

If the paths and runtime evidence exist there, do not simply undo the recovery.
Instead, update `EXTERNAL_REPOS.md` from dormant to reactivated one project at a
time.

## Merge options

### Option A - Full merge

Use if the structural reset is accepted as the new governance base:

```powershell
git switch main
git merge --no-ff origin/codex/structural-reset
```

### Option B - Cherry-pick recovery docs only

Use if old root docs should be preserved for now:

```powershell
git switch main
git checkout origin/codex/structural-reset -- docs/recovery EXTERNAL_REPOS.md SPRINT_02.md
```

Then commit manually.

### Option C - Hybrid

Use if the correct PC has real external repos and you want a softer transition:

1. bring in `docs/recovery/`;
2. bring in `EXTERNAL_REPOS.md`;
3. update root docs manually with fresh local evidence;
4. keep old historical content only where still accurate.

## Recommended path

Option C is safest on the correct PC.

The transplanted branch correctly identified structural drift, but only the
correct PC can decide which external systems still exist and should be
reactivated.

## Do not do

- Do not overwrite `main` with `reset --hard`.
- Do not restore cross-repo dashboards as live without checking paths.
- Do not trust old dogfood numbers unless logs or DB exist.
- Do not commit secrets or backup files.
- Do not merge runtime state into Git.
