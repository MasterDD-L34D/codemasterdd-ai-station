# tdd-guard Path-Scoped Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **GOVERNANCE GATE (regola-0):** Tasks touching `canonical-config.json`,
> `deploy_claude_global.ps1`, cross-PC deploy, or vault main are
> **Eduardo-authorization-gated**. Each such task is marked `GATE`. Do NOT
> execute a GATE task without explicit Eduardo approval for that task.
> Non-GATE tasks (per-repo settings on codemasterdd/Game/Godot feature
> branches, read-only verification) follow normal feature-branch+PR flow.

**Goal:** Make tdd-guard enforce test-first only in the derived ON-set
(behavior-code repos with test-reporter infra), structurally inert
elsewhere, fresh-worktree + cross-PC safe, with mixed ON repos
(codemasterdd) exempting ops/docs paths.

**Architecture:** Move the tdd-guard `Write|Edit|MultiEdit|TodoWrite`
hook OUT of canonical-config user-global INTO tracked per-repo
`.claude/settings.json` of ON-set repos only (structural lever; NON-set =
hook absent = inert). Mixed ON repos seed tdd-guard
`custom-instructions.md` from a tracked repo template via SessionStart so
non-test paths PASS. Backport W-2 + fix L43/L44 + deploy guard +
live-verify.

**Tech Stack:** Claude Code hooks (`.claude/settings.json`), tdd-guard
plugin (`npx tdd-guard@latest`), tdd-guard custom-instructions, vault
canonical-config JSON, `deploy_claude_global.ps1` (PowerShell), git.

---

## File Structure

| File | Responsibility | Repo | GATE? |
|---|---|---|---|
| `.claude/settings.json` (per ON repo) | register tdd-guard hook, tracked | codemasterdd, Game, Game-Godot-v2 (+M0 set) | no (feature-branch) |
| `scripts/hooks/tddguard-instructions.template.md` | path-scope rules source (mixed ON) | codemasterdd | no |
| `.claude/settings.json` SessionStart hook | seed instructions.md from template | codemasterdd (mixed ON) | no |
| `Vault-ops-remote/claude-global/canonical-config.json` | remove user-global tdd-guard hook; W-2 arg; L43/L44; _INERTE resolved-ref | vault | **GATE** |
| `Vault-ops-remote/claude-global/scripts/deploy_claude_global.ps1` | regression guard: never re-inject user-global tdd-guard hook | vault | **GATE** |
| `docs/decisions/OD-050-...md` | fold resolution, status update | vault | **GATE** |

---

## Task 0: Finalize M0 ON-set (read-only investigation)

**Files:** none (investigation; outputs a decided list appended to spec/OD-050).

- [ ] **Step 1: Verify Game-Database test-reporter compatibility**

Run:
```bash
cat "C:/dev/Game-Database/server/package.json" | grep -A2 '"scripts"'
ls "C:/dev/Game-Database/server/tests" "C:/dev/Game-Database/server/test" 2>/dev/null
grep -rl "vitest\|jest\|tdd-guard" "C:/dev/Game-Database/server" --include=package.json 2>/dev/null
```
Expected: confirms runner is custom `node ./test/run-tests.js` (no
vitest/jest reporter). Decision rule: if no standard reporter -> Game-DB =
ON-without-reporter (heuristic only) OR defer. Record verdict.

- [ ] **Step 2: Verify Item-generator + evo-swarm existence + infra (cross-PC)**

Run (Ryzen, then note Lenovo-side needs SSH check):
```bash
ls "C:/dev/Item-generator" 2>/dev/null || echo "Item-generator: ABSENT Ryzen"
ls "C:/Users/edusc/Dafne/workspace/swarm/tests" 2>/dev/null || echo "evo-swarm: Lenovo-side, SSH verify needed"
```
Expected: explicit presence/infra status per repo.

- [ ] **Step 3: Write decided ON-set**

Append to OD-050 §1b a `ON-SET-FINAL` block listing each repo + reporter
type + verdict (ON-with-reporter / ON-heuristic-only / OFF / DEFER).
Confirmed minimum: `Game` (vitest+pytest), `Game-Godot-v2` (GUT),
`codemasterdd` (pytest).

- [ ] **Step 4: Commit (vault feature branch)** — GATE (vault doc)

```bash
git -C C:/dev/vault/.claude/worktrees/<wt> add docs/decisions/OD-050-tddguard-enforcement-effectiveness-2026-05-19.md
git -C ... commit -m "docs(od-050): ON-SET-FINAL derived list (M0)"
```

---

## Task 1: codemasterdd L1+L2 (first; highest friction, fastest feedback)

**Files:**
- Modify: `C:/dev/codemasterdd-ai-station/.claude/settings.json` (merge tdd-guard PreToolUse hook + SessionStart hook; do NOT replace existing hooks)
- Create: `C:/dev/codemasterdd-ai-station/scripts/hooks/tddguard-instructions.template.md`
- Test: live-firing manual matrix (no unit harness for hooks)

- [ ] **Step 1: Write the verification check (expected: fails pre-change)**

Run (records current behavior — tdd-guard fires via user-global, no path-scope):
```bash
grep -c 'tdd-guard' C:/dev/codemasterdd-ai-station/.claude/settings.json 2>/dev/null || echo 0
ls C:/dev/codemasterdd-ai-station/scripts/hooks/tddguard-instructions.template.md 2>/dev/null || echo "NO template"
```
Expected PRE: `0` + `NO template` (hook only user-global; no path-scope) =
the defect state.

- [ ] **Step 2: Create the path-scope instructions template**

Create `C:/dev/codemasterdd-ai-station/scripts/hooks/tddguard-instructions.template.md`:
```markdown
# TDD Guard custom rules — codemasterdd (mixed repo)

This repo mixes behavior-code (pytest under `scripts/` modules with tests),
ops scripts, and docs/governance. Apply test-first ONLY to behavior-code.

ALWAYS PASS (not TDD-relevant) — return valid, do not block:
- Any path matching: `**/*.md`, `docs/**`, `**/*.tmp*`, `.claude/**`,
  `Archivio_*/**`, `*.json` governance files, one-off ops scripts under
  `scripts/` that have no co-located `test_*.py`
ENFORCE test-first ONLY on:
- Python modules with an existing co-located `tests/` or `test_*.py`
  (behavior-code). Edits adding logic without a failing test first -> block.

When uncertain whether a file is behavior-code vs ops/doc: PASS (favor
non-blocking; this repo's value is coordination, not test-coverage).
```

- [ ] **Step 3: Merge hooks into codemasterdd `.claude/settings.json`**

Read current file first. Merge (preserve existing commit-guard/observe
hooks — MERGE not replace, per spec R3) adding:
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Write|Edit|MultiEdit|TodoWrite",
        "hooks": [ { "type": "command", "command": "npx tdd-guard@latest" } ] }
    ],
    "SessionStart": [
      { "matcher": "startup|resume|clear",
        "hooks": [ { "type": "command", "command": "tdd-guard" } ] }
    ]
  }
}
```
(If `.claude/settings.json` absent, create with only these + keep any
project hooks. If present, JSON-merge arrays, do not drop existing.)

- [ ] **Step 4: Verify static (expected: passes post-change)**

Run:
```bash
python -c "import json;d=json.load(open(r'C:/dev/codemasterdd-ai-station/.claude/settings.json'));print('tddguard-pre',any('tdd-guard' in h.get('command','') for b in d.get('hooks',{}).get('PreToolUse',[]) for h in b.get('hooks',[])));print('sessionstart',any('tdd-guard' in h.get('command','') for b in d.get('hooks',{}).get('SessionStart',[]) for h in b.get('hooks',[])))"
ls C:/dev/codemasterdd-ai-station/scripts/hooks/tddguard-instructions.template.md
```
Expected POST: `tddguard-pre True` + `sessionstart True` + template exists.

- [ ] **Step 5: Commit (codemasterdd feature branch — NOT gated)**

```bash
git add .claude/settings.json scripts/hooks/tddguard-instructions.template.md
git commit -m "feat(tddguard): codemasterdd per-repo hook + path-scope template (OD-050 L1/L2)"
```

- [ ] **Step 6: LIVE verify (manual, after Task 3 removes user-global hook)**

Deferred checkpoint (depends on Task 3): in a fresh codemasterdd session,
edit a `scripts/*.py` ops file -> expect PASS (not blocked); edit a
behavior module adding logic w/o test -> expect BLOCK. Record observed.

---

## Task 2: Game + Game-Godot-v2 L1 (pure-code ON repos)

**Files:**
- Modify: `C:/dev/Game/.claude/settings.json` (merge tdd-guard PreToolUse hook)
- Modify: `C:/dev/Game-Godot-v2/.claude/settings.json` (merge tdd-guard PreToolUse hook)

- [ ] **Step 1: Verify pre-state**

Run:
```bash
for R in C:/dev/Game C:/dev/Game-Godot-v2; do echo "$R:"; grep -c 'tdd-guard' "$R/.claude/settings.json" 2>/dev/null || echo 0; done
```
Expected PRE: `0` each (relies on user-global only).

- [ ] **Step 2: Merge tdd-guard PreToolUse hook into each**

For each repo's `.claude/settings.json` (read first, JSON-merge, preserve
existing hooks):
```json
{ "hooks": { "PreToolUse": [
  { "matcher": "Write|Edit|MultiEdit|TodoWrite",
    "hooks": [ { "type": "command", "command": "npx tdd-guard@latest" } ] } ] } }
```
No L2 template (pure code repos — test-first applies broadly). Optional:
minimal instructions.template.md exempting `docs/**`,`*.md` if these
repos carry governance docs (Game does: BACKLOG/ADR). Recommended: add the
same `**/*.md`,`docs/**` PASS rule to avoid doc-edit friction.

- [ ] **Step 3: Verify post**

Run the Step-1 command. Expected POST: `>=1` each.

- [ ] **Step 4: Commit (each repo, feature branch — NOT gated)**

```bash
git -C C:/dev/Game add .claude/settings.json [scripts/hooks/tddguard-instructions.template.md]
git -C C:/dev/Game commit -m "feat(tddguard): Game per-repo hook (OD-050 L1)"
# repeat Game-Godot-v2
```

---

## Task 3: canonical-config L3 patch  — GATE (vault, Eduardo)

**Files:**
- Modify: `C:/dev/vault/.../Vault-ops-remote/claude-global/canonical-config.json`

- [ ] **Step 1: Verify pre-state**

Run:
```bash
python -c "import json;d=json.load(open(r'C:/dev/vault/Vault-ops-remote/claude-global/canonical-config.json'));import re;s=json.dumps(d);print('userglobal-tddguard', 'tdd-guard' in s and 'settings_json_hooks' in s)"
grep -n 'observe.sh' C:/dev/vault/Vault-ops-remote/claude-global/canonical-config.json | head
```
Expected PRE: shows tdd-guard NOT in settings_json_hooks already (it
isn't — observe.sh + commit-guard are; tdd-guard fires via the PLUGIN
hooks.json `npx tdd-guard@latest`, user-global plugin-enabled). Adjust L1
accordingly: the lever is the PLUGIN being enabled user-global +
hooks.json matcher, not a canonical settings_json_hooks entry.

- [ ] **Step 2: Resolve the actual user-global firing source**

The plugin `tdd-guard@tdd-guard` is enabled in `~/.claude/settings.json`
(`enabledPlugins`) and its bundled `hooks.json` fires `npx tdd-guard@latest`
on Write|Edit globally. To make NON-set inert, the lever is: keep plugin
INSTALLED but disable its enforcement per-repo absence. Since the plugin
hooks.json cannot be per-repo, the effective mechanism = the
`tdd-guard off` state OR project-settings override is NOT sufficient.
**Decision point (Eduardo):** either (3a) keep plugin enabled + rely on
per-repo `.claude/tdd-guard/data` `tdd-guard off` default seeded by a
tracked SessionStart in NON-set repos (writes off-state on session start);
or (3b) disable the plugin user-global and register `npx tdd-guard@latest`
ONLY in ON-set per-repo `.claude/settings.json` (cleanest, matches spec
L1). Recommend 3b. Record Eduardo decision before proceeding.

- [ ] **Step 3: Apply chosen mechanism to canonical-config**

(3b path) In canonical-config: move `tdd-guard@tdd-guard` out of
user-global `enabledPlugins` set; document that ON-set repos register
`npx tdd-guard@latest` in their tracked `.claude/settings.json`
(Task 1/2). Add `_OD050_RESOLUTION` note referencing this plan + spec.

- [ ] **Step 4: W-2 observe.sh arg fix**

In canonical-config `settings_json_hooks` observe.sh hook commands, add
positional `pre` / `post` arg per event:
```json
"PreToolUse": [ ... { "command": "bash \"$HOME/.claude/skills/continuous-learning-v2/hooks/observe.sh\" pre", "async": true, "timeout": 10 } ]
"PostToolUse": [ ... { "command": "bash \"$HOME/.claude/skills/continuous-learning-v2/hooks/observe.sh\" post", "async": true, "timeout": 10 } ]
```

- [ ] **Step 5: L43/L44 + _INERTE resolution text**

Edit canonical-config: L44 drop `codemasterdd` from NON-setup list (L43
codemasterdd=ON authoritative); `_INERTE_CLAIM_FALSIFIED` append
`RESOLVED-BY-DESIGN 2026-05-19 -> OD-050 + spec/plan 2026-05-19-tddguard`.

- [ ] **Step 6: JSON valid + commit (vault feature branch) — GATE**

```bash
python -c "import json;json.load(open(r'.../canonical-config.json'));print('JSON OK')"
git add Vault-ops-remote/claude-global/canonical-config.json
git commit -m "fix(canonical): tdd-guard per-repo (OD-050 L1/L3) + W-2 observe arg + L43/L44"
```

---

## Task 4: deploy_claude_global.ps1 regression guard — GATE (vault, Eduardo)

**Files:**
- Modify: `.../Vault-ops-remote/claude-global/scripts/deploy_claude_global.ps1`

- [ ] **Step 1: Locate hook/plugin deploy logic**

Run:
```bash
grep -n 'tdd-guard\|enabledPlugins\|settings_json_hooks\|hooks' .../deploy_claude_global.ps1 | head
```
Expected: identify where it writes ~/.claude/settings.json enabledPlugins
+ merges hooks.

- [ ] **Step 2: Add guard — never write user-global tdd-guard enforcement**

Add explicit exclusion so the deploy does NOT add `tdd-guard@tdd-guard`
to user-global enabledPlugins nor a user-global tdd-guard hook (idempotent
assertion + comment referencing OD-050).

- [ ] **Step 3: DRY-RUN verify (Anti-Pattern#9 — not just dry)**

Run deploy in `-WhatIf`/throwaway-target, assert resulting settings.json
has NO user-global tdd-guard. Then a real `-Apply` to a sandbox target,
re-verify artifact (parse + content), per global CLAUDE.md anti-pattern#9.

- [ ] **Step 4: Commit — GATE**

```bash
git add .../deploy_claude_global.ps1
git commit -m "fix(deploy): regression guard no user-global tdd-guard (OD-050 L3)"
```

---

## Task 5: Deploy both PCs + LIVE verify matrix — GATE (Eduardo, cross-PC)

**Files:** none (operational).

- [ ] **Step 1: Eduardo merges vault PR (Task 3+4) + codemasterdd/Game PRs (Task 1/2)**

GATE: Eduardo authorization. Merge order: per-repo settings first, then
canonical/deploy.

- [ ] **Step 2: Deploy canonical both PCs**

Run `deploy_claude_global.ps1 -Apply` Ryzen + Lenovo (Eduardo or
authorized). Capture logs to `Extras/ollama-runs/`.

- [ ] **Step 3: LIVE-firing verification matrix (fresh session, BOTH PCs)**

| Repo | Action | Expected |
|---|---|---|
| vault | edit `.md` / `Vault-ops-remote/scripts/*.py` | NOT blocked (inert) |
| synesthesia | edit `.py` | NOT blocked |
| codemasterdd | edit `scripts/*.py` ops / `docs/*.md` | PASS |
| codemasterdd | edit behavior module + logic, no test | BLOCK |
| Game | edit behavior code, no test | BLOCK |
| Game | edit `BACKLOG.md` | NOT blocked |
| Game-Godot-v2 | edit `.gd` logic, no test | BLOCK |

Record observed vs expected. Any mismatch -> Phase-1 systematic-debug,
do not assume.

- [ ] **Step 4: 2nd deploy run = idempotent (no user-global tdd-guard reappears)**

Re-run deploy, re-verify matrix unchanged.

---

## Task 6: Fold resolution into OD-050 + close — GATE (vault doc)

- [ ] **Step 1: Update OD-050 status + resolution**

Edit OD-050: status `PROPOSED-NEEDS-DECISION` -> `RESOLVED-IMPLEMENTED
2026-XX-XX` with link to this plan + live-verify matrix results +
ON-SET-FINAL.

- [ ] **Step 2: Commit + PR (vault) — GATE**

```bash
git add docs/decisions/OD-050-*.md
git commit -m "docs(od-050): RESOLVED — tdd-guard path-scoped implemented + live-verified"
```

---

## Self-Review

**Spec coverage:**
- M0 set-derivation -> Task 0 ✓
- M1 effective default (structural hook-placement) -> Task 1/2/3 ✓
- M3 mixed-repo path-scope (codemasterdd) -> Task 1 (L2 template) ✓
- W-2 observe.sh arg -> Task 3 Step 4 ✓
- L43/L44 -> Task 3 Step 5 ✓
- deploy regression guard -> Task 4 ✓
- live-verify Anti-Pattern#9 -> Task 5 ✓
- fold OD-050 -> Task 6 ✓
- Spec R1 (custom-instr vs heuristic) -> Task 1 Step 6 live check + L2
  fallback bypass-convention (documented in spec §4 L2, exercised if
  Step-6 mismatch) ✓
- Spec R3 (settings merge not replace) -> Task 1 Step 3 / Task 2 Step 2
  explicit MERGE ✓

**Correction found in self-review (fixed inline):** Task 3 Step 1/2 —
spec L1 assumed tdd-guard hook lived in canonical `settings_json_hooks`;
ground-truth (this session's investigation) = it fires via the PLUGIN
(`tdd-guard@tdd-guard` enabledPlugins + bundled hooks.json `npx
tdd-guard@latest`), NOT a canonical settings_json_hooks entry. Plan Task 3
now surfaces this as an explicit Eduardo decision point (3a seed-off-state
vs 3b disable-plugin-user-global + per-repo register; recommend 3b). This
is the one real open mechanism question — flagged, not papered over.

**Placeholder scan:** no TBD/TODO; all steps have concrete
commands/content. ON-SET-FINAL values are produced by Task 0 (legitimate
investigation output, not placeholder).

**Type/name consistency:** hook matcher `Write|Edit|MultiEdit|TodoWrite`,
command `npx tdd-guard@latest`, SessionStart `tdd-guard`, template path
`scripts/hooks/tddguard-instructions.template.md` — consistent across Tasks
1/2/3.

**Open mechanism (Task 3 Step 2) is the highest-risk unknown** — recommend
executing Task 0 + Task 1 (codemasterdd, reversible feature branch) FIRST
to empirically validate L2 path-scope efficacy and the 3a-vs-3b lever
before any GATE task.
