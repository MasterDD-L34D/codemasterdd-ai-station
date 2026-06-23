# journal-land cross-fleet Implementation Plan

> **Status (2026-06-23):** shipped -- journal-land.ps1 live

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans (inline; single-author ops change). Steps use checkbox (`- [ ]`).

**Goal:** Stop the recurring cross-fleet journal-branch drift by landing JOURNAL.md edits to origin/main via a canonical, pushable `claude/journal-<host>-<date>` branch identical on both PCs.

**Architecture:** One PowerShell helper (`scripts/fleet/journal-land.ps1`) does the deterministic git landing (fetch -> stash -> branch from origin/main -> commit -> SSH push -> gh PR+auto-merge OR graceful push-only). Doctrine (ORCHESTRATION.md + CLAUDE.md) tells sessions to use it and to never pull on a feature branch. Content editing stays with the session.

**Tech Stack:** Windows PowerShell 5.1, git 2.53 (origin=SSH on both PCs), gh CLI (authed on Lenovo, dead-token on Ryzen -> graceful degrade).

**Spec:** `docs/superpowers/specs/2026-05-29-journal-land-cross-fleet-design.md`

---

## File structure

- Create: `scripts/fleet/journal-land.ps1` -- the landing helper (one responsibility: git landing).
- Modify: `ORCHESTRATION.md` -- add "Journal / handoff landing (cross-fleet)" subsection.
- Modify: `CLAUDE.md` -- expand "## Aggiornamento JOURNAL" to mandate the helper + no-pull-on-branch.
- Already created: spec + this plan (carried onto the fix branch).
- No change: `.claude/settings.json` (`git push origin claude/*` already covers `claude/journal-*`).

tdd-guard: `scripts/fleet/**` is NOT in the ENFORCE allowlist (apps/src, apps/*.py, scripts/lib) -> PASS. Test = integration smoke, not Pester.

---

## Task 1: Create the fix branch from a clean base

**Files:** none (git only)

- [ ] **Step 1: confirm working-tree state** (must not mix the unrelated fleet-tools branch work)

Run: `git status --porcelain`
Expected: only `docs/superpowers/specs/2026-05-29-...md` + `docs/superpowers/plans/2026-05-29-...md` as new files (plus the pre-existing untracked `docs/jules-batch/2026-05-29-digest.md`, which is NOT part of this fix).

- [ ] **Step 2: fetch + branch from origin/main, carrying only the spec+plan**

```powershell
git stash push -u -- docs/superpowers/specs/2026-05-29-journal-land-cross-fleet-design.md docs/superpowers/plans/2026-05-29-journal-land-cross-fleet.md
git fetch origin main
git switch -c claude/journal-drift-fix-2026-05-29 origin/main
git stash pop
```
Expected: on branch `claude/journal-drift-fix-2026-05-29`, spec+plan present, fleet-tools work + jules digest left behind on the old branch.

---

## Task 2: Write the helper `scripts/fleet/journal-land.ps1`

**Files:** Create `scripts/fleet/journal-land.ps1`

- [ ] **Step 1: write the complete script** (exact content below)

```powershell
#requires -Version 5.1
<#
.SYNOPSIS
  Land a JOURNAL.md (and optional governance files) edit to origin/main via a
  pushable claude/journal-<host>-<date> branch -- identical on Lenovo + Ryzen.
.DESCRIPTION
  Kills the recurring cross-fleet journal-branch drift. Ryzen journal commits used
  to strand on chore/docs-prefixed branches (miss the claude/* push allow-rule) and
  its gh token is dead. This helper always lands content on origin via SSH push
  (works on both PCs); PR+auto-merge where gh is authed, graceful push-only where it
  is not. Never pulls on a feature branch. Content editing (newest-first JOURNAL
  insert) stays with the session; this does only the deterministic git landing.
  Spec: docs/superpowers/specs/2026-05-29-journal-land-cross-fleet-design.md
.PARAMETER Subject
  Conventional-commit subject, e.g. "docs(journal): coop-WS surface 3 PR".
.PARAMETER Path
  Files to include in the commit. Default JOURNAL.md.
.PARAMETER NoMerge
  Create the PR but do not auto-merge (default = create PR + auto-merge squash).
.PARAMETER DryRun
  Print planned actions, mutate nothing.
.EXAMPLE
  scripts/fleet/journal-land.ps1 -Subject "docs(journal): session X shipped"
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)] [string] $Subject,
  [string[]] $Path = @('JOURNAL.md'),
  [switch] $NoMerge,
  [switch] $DryRun
)

# native git writes to stderr on success; gate on $LASTEXITCODE only (anti-pattern L-040)
$ErrorActionPreference = 'Continue'

function Info($m) { Write-Host "[journal-land] $m" }
function Fail($m) { Write-Host "[journal-land] ERROR: $m" -ForegroundColor Red; exit 1 }

function New-TraceId {
  # uuidv7 (RFC 9562): 48-bit unix-ms + version/variant + random. Fallback v4 on any error.
  try {
    $ms = [long][DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    $b  = [guid]::NewGuid().ToByteArray()   # random source
    $b[0] = [byte](($ms -shr 40) -band 0xFF); $b[1] = [byte](($ms -shr 32) -band 0xFF)
    $b[2] = [byte](($ms -shr 24) -band 0xFF); $b[3] = [byte](($ms -shr 16) -band 0xFF)
    $b[4] = [byte](($ms -shr 8)  -band 0xFF); $b[5] = [byte]($ms -band 0xFF)
    $b[6] = [byte](0x70 -bor ($b[6] -band 0x0F)); $b[8] = [byte](0x80 -bor ($b[8] -band 0x3F))
    $h = ($b | ForEach-Object { $_.ToString('x2') }) -join ''
    return ('{0}-{1}-{2}-{3}-{4}' -f $h.Substring(0,8),$h.Substring(8,4),$h.Substring(12,4),$h.Substring(16,4),$h.Substring(20,12))
  } catch { return [guid]::NewGuid().ToString() }
}

# --- repo root + identity guard ---
$repoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent   # scripts/fleet/ -> repo root
Set-Location $repoRoot
$originUrl = (& git config --get remote.origin.url)
if ($LASTEXITCODE -ne 0 -or $originUrl -notmatch 'codemasterdd-ai-station') {
  Fail "not the codemasterdd-ai-station repo (origin='$originUrl'). Refusing."
}

# --- validate subject (mirror commit-guard.js -> fail fast, not at the hook) ---
$convRe = '^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?!?:\s.+'
if ($Subject -notmatch $convRe) { Fail "subject not Conventional Commits: '$Subject'" }
if ($Subject.Length -gt 72)     { Fail "subject is $($Subject.Length) chars (max 72)" }
if ($Subject.EndsWith('.'))     { Fail "subject must not end with a period" }
$desc = $Subject -replace '^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?!?:\s+', ''
if ($desc.Length -gt 0 -and [char]::IsUpper($desc[0])) { Fail "description should start with a lowercase letter" }

# --- changes present? ---
$changed = (& git status --porcelain -- $Path)
if (-not $changed) { Info "no changes in [$($Path -join ', ')] -- nothing to journal."; exit 0 }

# --- branch name (host + date, collision suffix) ---
$hostTag = ($env:COMPUTERNAME).ToLower() -replace '[^a-z0-9-]', '-'
$dateTag = Get-Date -Format 'yyyy-MM-dd'
$branch  = "claude/journal-$hostTag-$dateTag"
& git rev-parse --verify --quiet "refs/heads/$branch" *> $null
if ($LASTEXITCODE -eq 0) { $branch = "$branch-$(Get-Date -Format 'HHmmss')" }
$origBranch = (& git rev-parse --abbrev-ref HEAD).Trim()

if ($DryRun) {
  Info "DRY-RUN -- no mutation:"
  Info "  base      : origin/main (would fetch)"
  Info "  branch    : $branch"
  Info "  paths     : $($Path -join ', ')"
  Info "  subject   : $Subject"
  Info "  auto-merge: $([bool](-not $NoMerge))"
  Info "  return to : $origBranch"
  exit 0
}

# --- fetch clean base ---
& git fetch origin main
if ($LASTEXITCODE -ne 0) { Fail "git fetch origin main failed" }

# --- carry the edit off the current branch ---
& git stash push -m 'journal-land-temp' -- $Path
if ($LASTEXITCODE -ne 0) { Fail "git stash failed" }

# --- branch from clean origin/main ---
& git switch -c $branch origin/main
if ($LASTEXITCODE -ne 0) { & git stash pop *> $null; Fail "git switch -c $branch origin/main failed" }

# --- re-apply edit ---
& git stash pop
if ($LASTEXITCODE -ne 0) {
  & git reset --hard HEAD *> $null
  & git switch $origBranch *> $null
  & git stash pop *> $null
  & git branch -D $branch *> $null
  Fail "stash pop conflict vs origin/main (concurrent JOURNAL edit?). Edit restored on '$origBranch'. Run 'git pull --ff-only' on main, redo the insert, re-run."
}

# --- commit (subject + ADR-0011 trailers via -F tempfile; ASCII no-BOM) ---
& git add -- $Path
if ($LASTEXITCODE -ne 0) { & git switch $origBranch *> $null; Fail "git add failed" }
$msgFile = [IO.Path]::GetTempFileName()
$body = "$Subject`n`nCoding-Agent: claude-opus-4.8`nTrace-Id: $(New-TraceId)`n"
[IO.File]::WriteAllText($msgFile, $body, (New-Object System.Text.UTF8Encoding($false)))  # no BOM
& git commit -F $msgFile
$rc = $LASTEXITCODE
Remove-Item $msgFile -Force -ErrorAction SilentlyContinue
if ($rc -ne 0) { & git switch $origBranch *> $null; Fail "git commit failed (commit-msg hook? check subject)" }

# --- push (SSH; works on both PCs) ---
& git push -u origin $branch
if ($LASTEXITCODE -ne 0) { & git switch $origBranch *> $null; Fail "git push failed. Commit is on local '$branch' (not lost). Check SSH key / network." }
Info "pushed origin/$branch"

# --- PR via gh if authed; else graceful push-only (Ryzen) ---
& gh auth status *> $null
if ($LASTEXITCODE -ne 0) {
  & git switch $origBranch *> $null
  Info "gh NOT authenticated. Branch pushed to origin = content SAFE (not stranded)."
  Info "Open/merge the PR from the hub, or run 'gh auth login -h github.com'. Returned to '$origBranch'."
  exit 0
}
$prBody = "Automated journal landing via scripts/fleet/journal-land.ps1. Host: $hostTag. Base: origin/main."
& gh pr create --base main --head $branch --title $Subject --body $prBody
if ($LASTEXITCODE -ne 0) { & git switch $origBranch *> $null; Fail "gh pr create failed (branch '$branch' is pushed; open PR manually)." }
$prUrl = (& gh pr view $branch --json url --jq '.url' 2>$null)
Info "PR: $prUrl"

if (-not $NoMerge) {
  & gh pr merge $branch --auto --squash --delete-branch
  if ($LASTEXITCODE -ne 0) { Info "auto-merge not enabled; PR left open for manual merge: $prUrl" }
  else { Info "auto-merge (squash) queued; remote branch deletes on merge." }
}

& git switch $origBranch *> $null
Info "done. returned to '$origBranch'."
exit 0
```

- [ ] **Step 2: ASCII verify** (ADR-0021 + anti-pattern #12)

Run: `powershell -NoProfile -Command "$b=[IO.File]::ReadAllBytes('scripts/fleet/journal-land.ps1'); ($b | Where-Object {$_ -gt 127}).Count"`
Expected: `0` (pure ASCII, no BOM, no non-ASCII byte).

---

## Task 3: Doctrine -- ORCHESTRATION.md

**Files:** Modify `ORCHESTRATION.md` (append a subsection after sec 6 "Standing permission classes")

- [ ] **Step 1: add the subsection**

```markdown
## 6b. Journal / handoff landing (cross-fleet)

Recording session work to `JOURNAL.md` (and `COMPACT_CONTEXT.md` / memory) MUST use
`scripts/fleet/journal-land.ps1` on BOTH PCs. It branches `claude/journal-<host>-<date>`
(matches the `claude/*` push allow-rule, sec 6) from a freshly fetched origin/main, commits,
pushes via SSH (works on Lenovo + Ryzen today), and -- where gh is authed -- opens the PR and
auto-merges (squash); where gh is not authed (e.g. Ryzen's token), it pushes anyway so the
content reaches origin and the PR is a trivial hub follow-up. Rules:
- NEVER journal on a `chore/`/`docs/`-prefixed local branch (misses the push allow-rule -> strands).
- NEVER `git pull` while on a feature branch (`git pull --ff-only` on main only) -- pulling on a
  branch creates stray `ort` merge commits and diverges fleet HEADs.
Root cause + design: `docs/superpowers/specs/2026-05-29-journal-land-cross-fleet-design.md`.
```

---

## Task 4: Doctrine -- CLAUDE.md "## Aggiornamento JOURNAL"

**Files:** Modify `CLAUDE.md` (the `## Aggiornamento JOURNAL` section)

- [ ] **Step 1: replace the section body**

Old:
```markdown
## Aggiornamento JOURNAL
A fine sessione significativa, aggiungere entry in JOURNAL.md:
- Data YYYY-MM-DD
- Sezioni: Completato | Da fare | Note
```
New:
```markdown
## Aggiornamento JOURNAL
A fine sessione significativa, aggiungere entry in JOURNAL.md:
- Data YYYY-MM-DD (newest-first, subito dopo il divisore `---` del template)
- Sezioni: Completato | Da fare | Note

Poi **landare** la entry con l'helper canonico (vale su ENTRAMBI i PC, Lenovo + Ryzen):
`powershell -File scripts/fleet/journal-land.ps1 -Subject "docs(journal): <descrizione>"`
L'helper crea il branch `claude/journal-<host>-<date>`, committa (Conventional + trailer
ADR-0011), pusha via SSH e apre/auto-mergia la PR (o, dove gh non e' autenticato, pusha
comunque -> contenuto su origin, PR follow-up dall'hub). **MAI** journalare su branch
`chore/`/`docs/` (non matcha la push allow-rule -> resta orfano); **MAI** `git pull` su un
feature branch (`git pull --ff-only` solo su main). Razionale: anti-pattern #19 (stale) +
spec `docs/superpowers/specs/2026-05-29-journal-land-cross-fleet-design.md`.
```

---

## Task 5: Commit + push the fix

- [ ] **Step 1: stage + commit**

```powershell
git add scripts/fleet/journal-land.ps1 ORCHESTRATION.md CLAUDE.md docs/superpowers/specs/2026-05-29-journal-land-cross-fleet-design.md docs/superpowers/plans/2026-05-29-journal-land-cross-fleet.md
git commit -F <tempfile with subject "feat(fleet): journal-land helper kills cross-fleet journal drift" + ADR-0011 trailers>
```
Expected: commit-msg hook passes (subject conventional, <=72, lowercase, no period).

- [ ] **Step 2: push**

```powershell
git push -u origin claude/journal-drift-fix-2026-05-29
```

---

## Task 6: Quality Gate Step 1 -- smoke (anti-pattern #9: exercise -Apply, not only -DryRun)

- [ ] **Step 1: DryRun preview** (no mutation)

Run: `powershell -NoProfile -File scripts/fleet/journal-land.ps1 -Subject "docs(journal): smoke test" -DryRun`
Expected: prints planned branch `claude/journal-<host>-<date>`, paths, subject, auto-merge true, return-to branch. No git mutation (verify `git status` unchanged, `git branch` unchanged).

- [ ] **Step 2: live sandbox -Apply** (real push path, no main pollution)

```powershell
Set-Content -Path _journal_land_smoke.tmp -Value "sentinel" -Encoding ascii
powershell -NoProfile -File scripts/fleet/journal-land.ps1 -Subject "chore(fleet): journal-land smoke sentinel" -Path _journal_land_smoke.tmp -NoMerge
```
Expected: branch created FROM origin/main, commit present with trailers, pushed to origin, PR created (-NoMerge so not merged), returned to `claude/journal-drift-fix-2026-05-29`.

- [ ] **Step 3: verify + clean up the sandbox**

```powershell
git log -1 --format="%s%n%b" <smoke-branch>      # subject conventional + Coding-Agent + Trace-Id present
gh pr close <smoke-branch> --delete-branch        # remove the sandbox PR + remote branch
git switch claude/journal-drift-fix-2026-05-29
git branch -D <smoke-branch>
Remove-Item _journal_land_smoke.tmp -Force
```
Expected: sandbox fully removed; main untouched; before/after documented in the PR description.

- [ ] **Step 4: negative case**

Run: `powershell -NoProfile -File scripts/fleet/journal-land.ps1 -Subject "docs(journal): noop"` (with JOURNAL.md clean)
Expected: "no changes in [JOURNAL.md] -- nothing to journal.", exit 0, no branch created.

---

## Task 7: Verification gate (ORCHESTRATION sec 4) + PR

- [ ] **Step 1: different-model judge** -- parallel adversarial review (Workflow, 3 lenses: cross-shell/PS5.1 footguns, both-PC correctness, anti-pattern #9/#11/#12/#13 compliance) and/or `harsh-reviewer`. P0 -> fix; P1 -> fix-or-defer; P2 -> ack.
- [ ] **Step 2: open the fix PR**, ensure CI green.
- [ ] **Step 3: auto-merge** (squash) iff CI green + judge OK (Eduardo-authorized autonomy ladder).

---

## Self-review (against spec)

- Spec sec 3-4 (architecture/interface) -> Task 2 full script. Covered.
- Spec sec 5 (doctrine) -> Tasks 3-4. Covered.
- Spec sec 6 (error handling/edge) -> script: identity guard, nothing-to-journal, collision suffix, stash-pop conflict recovery, push-fail recovery, gh-unauth degrade, auto-merge fallback. Covered.
- Spec sec 7 (testing) -> Task 6 (DryRun + sandbox -Apply + negative). Covered.
- Spec sec 8 (verification) -> Task 7. Covered.
- Spec sec 9 (out of scope) -> no monitor/cron/Action; Ryzen gh re-auth doc-only. Honored.
- Placeholder scan: Task 5 commit uses "<tempfile ...>" (execution detail) -- acceptable (the executor builds the temp file as the script does). No code placeholders.
- Naming consistency: `claude/journal-<host>-<date>` and `claude/journal-drift-fix-2026-05-29` (fix branch) are distinct and used consistently.
