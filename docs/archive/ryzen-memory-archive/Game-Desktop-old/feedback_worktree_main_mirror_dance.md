---
name: Worktree-main mirror dance pattern
description: Edit nel worktree, mirror to main per run tests (node_modules), revert main pre-commit. Prevent main repo accidental staging. Pattern ricorrente sessione 2026-05-06.
type: feedback
originSessionId: 43af369a-a1ea-416b-87cb-0cbe6f22509e
---
## Why

Worktree (`/c/Users/VGit/Desktop/Game/.claude/worktrees/<slug>`) NON ha node_modules installato. Tests + harness + format require `npm` + libs from main repo's node_modules.

**Pattern**: edit in worktree → cp file to main → run tests/format/lint → revert main → commit from worktree.

## How to apply

**Edit phase** (worktree):
```bash
# Edit ALL files in worktree path:
# C:/Users/VGit/Desktop/Game/.claude/worktrees/<slug>/...
```

**Test phase** (mirror + run main):
```bash
cp /c/Users/VGit/Desktop/Game/.claude/worktrees/<slug>/<file> /c/Users/VGit/Desktop/Game/<file>
cd /c/Users/VGit/Desktop/Game && node --test tests/<area>/*.test.js
cd /c/Users/VGit/Desktop/Game && npx prettier --check <file>
```

**Format phase** (mirror back if prettier reformatted):
```bash
cp /c/Users/VGit/Desktop/Game/<file> /c/Users/VGit/Desktop/Game/.claude/worktrees/<slug>/<file>
```

**Pre-commit cleanup** (revert main):
```bash
cd /c/Users/VGit/Desktop/Game && git checkout <tracked-files>
cd /c/Users/VGit/Desktop/Game && rm -f <new-files-only>
cd /c/Users/VGit/Desktop/Game && rmdir <new-dirs-if-empty> 2>/dev/null
```

**Commit from worktree** (current shell cwd):
```bash
git status --short  # verify only worktree mods present
git add <files>
git commit -m "..."
git push
```

## Common gotchas

1. **Edit dispatch confusion**: Edit tool path must be EXPLICIT worktree (`/c/.../worktrees/<slug>/...`) o main path. Defaulting to cwd-relative breaks if cwd resets.

2. **Test file mirror mancante**: se test file modificato non viene copiato a main, run tests dal main repo USA OLD version → fail spurious. Mirror BOTH source + test.

3. **Yaml mirror mancante**: similar — yaml data file (mbti_forms.yaml, active_effects.yaml) loaded by helper non mirrored = fail spurious.

4. **Hooks reset**: prettier/eslint via npm-script reset cwd shell, ricontrolla path next command.

5. **Untracked file revert**: `git checkout` non rimuove untracked. Use `rm -f` esplicito.

## Anti-pattern

- ❌ Edit in main repo → cp main → worktree (loses changes if main reverted before mirror back)
- ❌ Run tests from worktree path expecting node_modules resolve up → does NOT auto-traverse
- ❌ Forget revert main pre-commit → main staging area pollutes branch reference
