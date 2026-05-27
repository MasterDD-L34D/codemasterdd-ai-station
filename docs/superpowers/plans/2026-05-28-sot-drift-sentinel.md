# SoT Drift Sentinel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Detect when a Game (public) merge touches a watched runtime area mapped to a vault SoT doc, flag it deterministically (Game issue), and provide a sovereign gated subagent to verdict + reconcile the SoT.

**Architecture:** Two isolated components. (A) Game-side GitHub Action runs a dep-free Node matcher (`detect.mjs`) against a committed `watch-map.yml` on push-to-main; on match it opens/updates one idempotent Game issue (label `sot-drift-candidate`). No vault access, no cross-repo secret. (B) Sovereign Claude Code subagent `sot-drift-verifier` (codemasterdd) is invoked on-demand to read the real vault SoT + Game change, give a gated multi-signal verdict, and propose a vault branch+PR reconcile (merge Eduardo-only).

**Tech Stack:** GitHub Actions (YAML), Node ESM + `node:test` (no new deps), `gh` CLI (issue create/edit), Claude Code subagent markdown.

**Repo locations:** Component A = `MasterDD-L34D/Game` (PUBLIC, edit via worktree branch + PR, governance-merge — husky blocks commit on `main`, use a `claude/<topic>` branch). Component B = `codemasterdd-ai-station` (PRIVATE, direct commit OK).

**Spec:** `docs/superpowers/specs/2026-05-28-sot-drift-sentinel-design.md`

---

## File structure

| File | Repo | Responsibility |
|------|------|----------------|
| `.github/sot-drift/watch-map.yml` | Game | Config: path-glob -> SoT-ref + concept |
| `tools/sot-drift/detect.mjs` | Game | Pure matcher: (watch-map, changedFiles) -> matches[]. Dep-free, unit-tested |
| `tools/sot-drift/detect.test.mjs` | Game | Unit tests for matcher (node:test) |
| `.github/workflows/sot-drift-sentinel.yml` | Game | Trigger push:main -> diff -> detect -> idempotent gh issue |
| `.claude/agents/sot-drift-verifier.md` | codemasterdd | Sovereign on-demand verdict subagent |
| `docs/KNOWLEDGE_MAP.md` (modify §7) | codemasterdd | Wire sentinel into reuse-queue/tracking |

---

## Task 1: watch-map.yml config (Game)

**Files:**
- Create: `.github/sot-drift/watch-map.yml`

- [ ] **Step 1: Create the watch-map**

```yaml
# Path-glob -> SoT doc refs. Consumed by tools/sot-drift/detect.mjs.
# sot_ref = vault Spaces/Dev/Evo-Tactics/<path>#<anchor> (heading slug or section number).
# Extend conservatively: only concepts that have a canonical SoT doc.
- pattern: "apps/backend/services/genetics/**"
  sot_ref: ["core/00-SOURCE-OF-TRUTH.md#24", "core/90-FINAL-DESIGN-FREEZE.md#21.3"]
  concept: "modello genetico D-HEIR/D-REPRO"
- pattern: "apps/backend/services/combat/**"
  sot_ref: ["core/10-SISTEMA_TATTICO.md", "core/11-REGOLE_D20_TV.md"]
  concept: "combat d20 / round loop"
- pattern: "data/core/economy*"
  sot_ref: ["core/26-ECONOMY_CANONICAL.md"]
  concept: "economia PT/PP/SG"
- pattern: "data/core/biomes*"
  sot_ref: ["core/28-NPC_BIOMI_SPAWN.md", "core/15-LEVEL_DESIGN.md"]
  concept: "biomi / spawn"
```

- [ ] **Step 2: Commit**

```bash
git add .github/sot-drift/watch-map.yml
git commit -m "feat(sot-drift): watch-map config (path-glob -> SoT ref)"
```

---

## Task 2: detect.mjs matcher logic (TDD)

**Files:**
- Create: `tools/sot-drift/detect.mjs`
- Test: `tools/sot-drift/detect.test.mjs`

- [ ] **Step 1: Write the failing test**

```js
// tools/sot-drift/detect.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { matchChanges } from './detect.mjs';

const MAP = [
  { pattern: 'apps/backend/services/genetics/**', sot_ref: ['core/00-SOURCE-OF-TRUTH.md#24'], concept: 'genetic' },
  { pattern: 'data/core/economy*', sot_ref: ['core/26-ECONOMY_CANONICAL.md'], concept: 'economy' },
];

test('matches a nested glob and collects the file', () => {
  const m = matchChanges(MAP, ['apps/backend/services/genetics/epigenome.js']);
  assert.equal(m.length, 1);
  assert.equal(m[0].concept, 'genetic');
  assert.deepEqual(m[0].files, ['apps/backend/services/genetics/epigenome.js']);
});

test('matches a prefix glob (economy*)', () => {
  const m = matchChanges(MAP, ['data/core/economy_canonical.yaml']);
  assert.equal(m.length, 1);
  assert.equal(m[0].concept, 'economy');
});

test('no match returns empty', () => {
  assert.deepEqual(matchChanges(MAP, ['README.md', 'apps/frontend/x.js']), []);
});

test('single entry deduped across multiple matching files', () => {
  const m = matchChanges(MAP, [
    'apps/backend/services/genetics/epigenome.js',
    'apps/backend/services/genetics/mutationEngine.js',
  ]);
  assert.equal(m.length, 1);
  assert.equal(m[0].files.length, 2);
});

test('* does not cross directory boundary', () => {
  // economy* must not match a deeper path segment after a slash
  const m = matchChanges(MAP, ['data/core/economy/sub/file.yaml']);
  assert.equal(m.length, 0);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tools/sot-drift/detect.test.mjs`
Expected: FAIL — `Cannot find module './detect.mjs'` / `matchChanges is not a function`.

- [ ] **Step 3: Write minimal implementation**

```js
// tools/sot-drift/detect.mjs
// Pure, dep-free glob matcher for SoT drift detection.

export function globToRegex(glob) {
  // Escape regex specials except '*'
  let re = glob.replace(/[.+^${}()|[\]\\]/g, '\\$&');
  // Order matters: '**/' (any dirs incl none) -> '*' (within a segment)
  re = re.replace(/\*\*\//g, '@@DOUBLEDIR@@');
  re = re.replace(/\*\*/g, '@@DOUBLE@@');
  re = re.replace(/\*/g, '[^/]*');
  re = re.replace(/@@DOUBLEDIR@@/g, '(?:[^/]+/)*');
  re = re.replace(/@@DOUBLE@@/g, '.*');
  return new RegExp('^' + re + '$');
}

export function matchChanges(watchMap, changedFiles) {
  const out = [];
  for (const entry of watchMap) {
    const rx = globToRegex(entry.pattern);
    const files = changedFiles.filter((f) => rx.test(f));
    if (files.length > 0) {
      out.push({ pattern: entry.pattern, sot_ref: entry.sot_ref, concept: entry.concept, files });
    }
  }
  return out;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test tools/sot-drift/detect.test.mjs`
Expected: PASS — 5 tests pass.

- [ ] **Step 5: Commit**

```bash
git add tools/sot-drift/detect.mjs tools/sot-drift/detect.test.mjs
git commit -m "feat(sot-drift): dep-free glob matcher + unit tests"
```

---

## Task 3: detect.mjs CLI entry (reads map from disk, files from argv)

**Files:**
- Modify: `tools/sot-drift/detect.mjs` (append CLI block)
- Test: `tools/sot-drift/detect.test.mjs` (add CLI-parse test for the loader)

- [ ] **Step 1: Write the failing test for the YAML-free loader**

Add to `detect.test.mjs`:

```js
import { parseWatchMap } from './detect.mjs';

test('parseWatchMap reads minimal yaml list', () => {
  const yaml = [
    '- pattern: "data/core/economy*"',
    '  sot_ref: ["core/26-ECONOMY_CANONICAL.md"]',
    '  concept: "economy"',
  ].join('\n');
  const m = parseWatchMap(yaml);
  assert.equal(m.length, 1);
  assert.equal(m[0].pattern, 'data/core/economy*');
  assert.deepEqual(m[0].sot_ref, ['core/26-ECONOMY_CANONICAL.md']);
  assert.equal(m[0].concept, 'economy');
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tools/sot-drift/detect.test.mjs`
Expected: FAIL — `parseWatchMap is not a function`.

- [ ] **Step 3: Implement parseWatchMap + CLI (dep-free minimal YAML)**

Append to `tools/sot-drift/detect.mjs`:

```js
// Minimal YAML-list parser for the constrained watch-map shape (no deps).
// Supports: list items with `pattern:`, `sot_ref:` (inline JSON array), `concept:`.
export function parseWatchMap(text) {
  const entries = [];
  let cur = null;
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.replace(/\s+$/, '');
    if (/^\s*#/.test(line) || line.trim() === '') continue;
    const item = line.match(/^-\s+pattern:\s*"(.+)"\s*$/);
    if (item) { cur = { pattern: item[1], sot_ref: [], concept: '' }; entries.push(cur); continue; }
    if (!cur) continue;
    const ref = line.match(/^\s+sot_ref:\s*(\[.*\])\s*$/);
    if (ref) { cur.sot_ref = JSON.parse(ref[1]); continue; }
    const con = line.match(/^\s+concept:\s*"(.+)"\s*$/);
    if (con) { cur.concept = con[1]; continue; }
  }
  return entries;
}

// CLI: node detect.mjs <watch-map.yml> <changed-files-file>
// changed-files-file = newline-separated paths (git diff output). Prints JSON matches to stdout.
if (import.meta.url === `file://${process.argv[1]}`) {
  const { readFileSync } = await import('node:fs');
  const mapPath = process.argv[2];
  const filesPath = process.argv[3];
  const map = parseWatchMap(readFileSync(mapPath, 'utf8'));
  const files = readFileSync(filesPath, 'utf8').split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
  const matches = matchChanges(map, files);
  process.stdout.write(JSON.stringify(matches, null, 2));
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test tools/sot-drift/detect.test.mjs`
Expected: PASS — all tests (matcher + parser) pass.

- [ ] **Step 5: Manual CLI smoke (local)**

```bash
printf 'apps/backend/services/genetics/epigenome.js\nREADME.md\n' > /tmp/changed.txt
node tools/sot-drift/detect.mjs .github/sot-drift/watch-map.yml /tmp/changed.txt
```
Expected: JSON array with one match (concept "modello genetico D-HEIR/D-REPRO", sot_ref incl. `core/00-SOURCE-OF-TRUTH.md#24`).

- [ ] **Step 6: Commit**

```bash
git add tools/sot-drift/detect.mjs tools/sot-drift/detect.test.mjs
git commit -m "feat(sot-drift): watch-map loader + CLI entry"
```

---

## Task 4: GitHub Action workflow (Game)

**Files:**
- Create: `.github/workflows/sot-drift-sentinel.yml`

- [ ] **Step 1: Create the workflow**

```yaml
name: SoT Drift Sentinel
on:
  push:
    branches: [main]
permissions:
  issues: write
  contents: read
jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2   # need previous commit to diff the merge
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Compute changed files
        run: git diff --name-only "${{ github.event.before }}" "${{ github.sha }}" > changed.txt || git diff --name-only HEAD~1 HEAD > changed.txt
      - name: Run matcher
        id: match
        run: |
          node tools/sot-drift/detect.mjs .github/sot-drift/watch-map.yml changed.txt > matches.json
          echo "count=$(node -e 'console.log(JSON.parse(require("fs").readFileSync("matches.json","utf8")).length)')" >> "$GITHUB_OUTPUT"
      - name: Open/update drift-candidate issue
        if: steps.match.outputs.count != '0'
        env:
          GH_TOKEN: ${{ github.token }}
        run: bash tools/sot-drift/flag-issue.sh "${{ github.sha }}"
```

- [ ] **Step 2: Create the idempotent issue script**

Create `tools/sot-drift/flag-issue.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
SHA="$1"
BODY_FILE="$(mktemp)"
{
  echo "## SoT drift candidate (auto-detected)"
  echo ""
  echo "Commit \`${SHA}\` touched watched runtime areas mapped to canonical SoT docs."
  echo "**Deterministic flag only** — semantic verdict is gated (sovereign \`sot-drift-verifier\` subagent)."
  echo ""
  node -e '
    const m=JSON.parse(require("fs").readFileSync("matches.json","utf8"));
    for (const x of m) {
      console.log("- **"+x.concept+"** (`"+x.pattern+"`) -> review SoT: "+x.sot_ref.map(r=>"`"+r+"`").join(", "));
      for (const f of x.files) console.log("  - changed: `"+f+"`");
    }
  '
  echo ""
  echo "_Action: sovereign review -> verdict -> if stale, vault branch+PR reconcile (merge human-only)._"
} > "$BODY_FILE"

EXISTING="$(gh issue list --label sot-drift-candidate --state open --json number --jq '.[0].number' 2>/dev/null || true)"
if [ -n "${EXISTING:-}" ] && [ "${EXISTING}" != "null" ]; then
  gh issue edit "$EXISTING" --body-file "$BODY_FILE"
  gh issue comment "$EXISTING" --body "Updated: new drift candidate at commit \`${SHA}\`."
else
  gh issue create --title "SoT drift candidate (runtime ahead of SoT docs)" \
    --label sot-drift-candidate --body-file "$BODY_FILE"
fi
```

- [ ] **Step 3: Ensure label exists (one-time, document in PR body)**

Run (once, by a maintainer with repo access):
```bash
gh label create sot-drift-candidate --repo MasterDD-L34D/Game --color FBCA04 --description "Game runtime may be ahead of vault SoT docs" || true
```
Expected: label created (or already-exists no-op).

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/sot-drift-sentinel.yml tools/sot-drift/flag-issue.sh
chmod +x tools/sot-drift/flag-issue.sh
git commit -m "feat(sot-drift): GitHub Action + idempotent issue flag"
```

---

## Task 5: QG Step-1 smoke (Component A) — MANDATORY

**Files:**
- Test (ephemeral branch, no repo file)

- [ ] **Step 1: Push a fixture commit touching a watched path on a test branch**

```bash
git checkout -b test/sot-drift-smoke
mkdir -p apps/backend/services/genetics
echo '// smoke fixture' >> apps/backend/services/genetics/_smoke_fixture.js
git add apps/backend/services/genetics/_smoke_fixture.js
git commit -m "test(sot-drift): smoke fixture (genetics touch)"
```

- [ ] **Step 2: Run the matcher locally against this change (pre-CI proof)**

```bash
git diff --name-only HEAD~1 HEAD > changed.txt
node tools/sot-drift/detect.mjs .github/sot-drift/watch-map.yml changed.txt
```
Expected: one match, concept "modello genetico D-HEIR/D-REPRO", sot_ref includes `core/00-SOURCE-OF-TRUTH.md#24`.

- [ ] **Step 3: Verify idempotency logic locally**

Run the matcher twice; confirm `flag-issue.sh` would target the same single open issue (read the script branch: EXISTING found -> `gh issue edit`, not a second create). Document expected: no duplicate issue.

- [ ] **Step 4: Clean up fixture (do NOT merge smoke branch)**

```bash
git checkout main
git branch -D test/sot-drift-smoke
rm -f apps/backend/services/genetics/_smoke_fixture.js changed.txt matches.json
```

- [ ] **Step 5: Record smoke result in PR body**

In the Game PR description, add: "QG Step-1 smoke: matcher PASS on genetics fixture (1 match, correct SoT ref); idempotency verified (edit not create on 2nd run). Full CI smoke runs on first push-to-main after merge."

---

## Task 6: sot-drift-verifier subagent (codemasterdd)

**Files:**
- Create: `C:\dev\codemasterdd-ai-station\.claude\agents\sot-drift-verifier.md`

- [ ] **Step 1: Create the subagent definition**

```markdown
---
name: sot-drift-verifier
description: Use on-demand to verdict a Game `sot-drift-candidate` issue (or a manual SoT-ref). Reads the real vault SoT section + the Game change, gives a gated multi-signal verdict (is the SoT doc stale vs shipped runtime?), and if stale proposes a vault branch+PR reconcile. NEVER auto-merges SoT. Triggers: "verdict drift candidate", "is SoT §X stale", "reconcile SoT vs Game ship".
tools: Read, Grep, Glob, Bash
---

# sot-drift-verifier

## Role
Sovereign gated verdict on runtime(Game)-vs-SoT(vault) drift candidates flagged by the Game `sot-drift-sentinel` Action. Deterministic flag -> semantic verdict, human-gated.

## Input
- A Game issue labelled `sot-drift-candidate` (number), OR a manual {sot_ref, Game commit/PR}.

## Process (multi-signal, gated)
1. Read the flagged SoT ref(s) in vault `C:/dev/vault/Spaces/Dev/Evo-Tactics/<ref>` (sovereign, current — `git -C C:/dev/vault fetch` first; verify local == origin).
2. Read the Game change: `gh pr view <n> --repo MasterDD-L34D/Game` / `gh api` commit; identify what shipped (commit msg + diff + touched files).
3. Multi-signal verdict:
   - Signal 1 path-match (from the flag).
   - Signal 2 commit-message claim (e.g., "feat(epigenome): ... SHIPPED").
   - Signal 3 SoT-doc claim (does the SoT say DEFERRED/TODO/not-done for the shipped concept?).
   - Verdict = STALE only if runtime shipped AND SoT doc still says not-done. Else NO-DRIFT.
   - Output confidence (high/med/low) + the exact contradicting lines.
4. If STALE (confidence >= med): propose a vault reconcile via branch+PR:
   - `git -C C:/dev/vault checkout -b claude/sot-reconcile-<slug>`
   - Edit the SoT ref(s) DEFERRED->SHIPPED with the Game PR refs.
   - Commit (Conventional + Coding-Agent/Trace-Id trailers), push, `gh pr create` (merge = Eduardo).
   - Comment the Game issue with the verdict + vault PR link; do NOT close (Eduardo closes on merge).
5. If NO-DRIFT: comment the Game issue "no-drift, confidence X" + close.

## Boundaries
- NEVER direct-push vault main; NEVER merge any PR. Branch+PR only (vault sibling-peer policy).
- NEVER edit Game (public) beyond commenting the issue.
- If confidence low OR ambiguous -> report to Eduardo, no PR.

## Quality Gate — Step 1 smoke (run before marking production)
Input: a fixture where Game shipped concept X (commit msg "feat: X shipped") and a vault SoT fixture says "X -- DEFERRED".
Expected: verdict STALE (high confidence) + proposed reconcile diff (DEFERRED->SHIPPED) + NO auto-merge.
Status: [ ] not run — MUST run before production (do not repeat the existing watcher's "not run").
```

- [ ] **Step 2: Validate frontmatter parses (agent discoverable)**

Run: `node -e "const m=require('fs').readFileSync('.claude/agents/sot-drift-verifier.md','utf8'); if(!/^---[\s\S]*?name: sot-drift-verifier[\s\S]*?---/.test(m)) throw new Error('frontmatter bad'); console.log('OK')"`
Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/sot-drift-verifier.md
git commit -m "feat(agent): sot-drift-verifier sovereign gated verdict subagent"
```

---

## Task 7: QG Step-1 smoke (Component B) — MANDATORY

**Files:**
- Test (ephemeral fixtures under a temp dir, not committed)

- [ ] **Step 1: Build fixtures**

```bash
mkdir -p /tmp/sot-smoke
printf '# SoT fixture\n\n- **Epigenome** -- **DEFERRED Fase-3** (params TBD).\n' > /tmp/sot-smoke/sot-ref.md
printf 'feat(epigenome): Fase-3 Lamarck-lite SHIPPED (engine + live-loop)\n' > /tmp/sot-smoke/game-commit.txt
```

- [ ] **Step 2: Invoke the verifier on the fixture (manual session)**

Invoke `sot-drift-verifier` with: SoT ref = `/tmp/sot-smoke/sot-ref.md`, Game change = `/tmp/sot-smoke/game-commit.txt`.
Expected: verdict STALE (high confidence), cites "DEFERRED Fase-3" vs "SHIPPED" commit, proposes a DEFERRED->SHIPPED reconcile, does NOT auto-merge.

- [ ] **Step 3: Negative fixture (no-drift)**

```bash
printf '# SoT fixture\n\n- **Epigenome** -- **SHIPPED Fase-3** (#2402).\n' > /tmp/sot-smoke/sot-ref-current.md
```
Invoke verifier with the SHIPPED fixture + same commit. Expected: verdict NO-DRIFT, no PR proposed.

- [ ] **Step 4: Record smoke result + flip status**

Edit `.claude/agents/sot-drift-verifier.md` QG line: `Status: [x] PASS 2026-MM-DD (stale fixture -> STALE high + gated PR; current fixture -> NO-DRIFT)`.

```bash
git add .claude/agents/sot-drift-verifier.md
git commit -m "test(agent): sot-drift-verifier QG Step-1 smoke PASS"
rm -rf /tmp/sot-smoke
```

---

## Task 8: Wire into tracking (codemasterdd)

**Files:**
- Modify: `docs/KNOWLEDGE_MAP.md` (§7 reuse-queue or a new §8)

- [ ] **Step 1: Add a sentinel note to KNOWLEDGE_MAP**

Append under §7 (or new §8 "Drift automation"):

```markdown
## 8. Drift automation -- SoT Drift Sentinel (2026-05-28)

Anti-pattern #19 mitigation: Game Action `sot-drift-sentinel` flags runtime-vs-SoT
drift candidates (Game issue `sot-drift-candidate`); sovereign subagent
`sot-drift-verifier` (codemasterdd `.claude/agents/`) verdicts + proposes vault reconcile
(gated). Spec: `docs/superpowers/specs/2026-05-28-sot-drift-sentinel-design.md`.
watch-map: Game `.github/sot-drift/watch-map.yml`.
```

- [ ] **Step 2: Commit**

```bash
git add docs/KNOWLEDGE_MAP.md
git commit -m "docs(knowledge): wire SoT Drift Sentinel into KNOWLEDGE_MAP"
```

---

## Execution notes (repo logistics)

- **Component A tasks (1-5)** = Game PUBLIC. Use an isolated worktree from `origin/main` (Game local is stale + husky skip-worktree on main): `git -C C:/dev/Game worktree add -b claude/sot-drift-sentinel <path> origin/main`. Commit on the branch (husky allows non-main), push, single PR, remove worktree. Governance-merge (Eduardo/Game).
- **Component B tasks (6-8)** = codemasterdd PRIVATE. Direct commits to main + push (as this session).
- Commit trailers: every commit needs `Coding-Agent:` + `Trace-Id:` (ADR-0011), NO `Co-Authored-By`. Subject <= 72 chars.
- The two components are independent: B can be built + smoke-tested with fixtures even before A's PR merges.

## Self-review (done)
- Spec coverage: §3 arch -> Tasks 1-6; §4 Action -> T4; §5 subagent -> T6; §6 watch-map -> T1; §7 reliability -> multi-signal in T6 process + gated; §8 smoke -> T5 (A) + T7 (B). All covered.
- Placeholder scan: no TBD/TODO left as work-items (the QG `[ ] not run` is an intentional checkbox flipped in T7).
- Type consistency: `matchChanges`/`parseWatchMap`/`globToRegex` names consistent across T2/T3; issue label `sot-drift-candidate` consistent T4/T5/T6; `detect.mjs` output shape {pattern,sot_ref,concept,files} consistent matcher->flag-issue.sh.
