#requires -Version 5.1
<#
.SYNOPSIS
  Land a JOURNAL.md (and optional governance files) edit to origin/main via a
  pushable claude/journal-<host>-<date> branch -- identical on Lenovo + Ryzen.
.DESCRIPTION
  Kills the recurring cross-fleet journal-branch drift. Ryzen journal commits used
  to strand on chore/docs-prefixed branches (miss the claude/* push allow-rule) and
  its gh token is dead. This helper always lands content on origin via SSH push
  (works on both PCs); PR + CI-gated merge where gh is authed, graceful push-only
  where it is not. Never pulls on a feature branch. Content editing (newest-first JOURNAL
  insert) stays with the session; this does only the deterministic git landing.

  Safety contract (the whole point of the tool):
  - Does all branch/commit work in a THROWAWAY git WORKTREE based on a freshly fetched
    origin/main. It NEVER runs 'git switch' in the shared working tree, so it can never
    yank HEAD out from under a concurrent session on the same clone (shared-clone safe).
  - Carries the edit into the worktree by DIRECT FILE COPY (WYSIWYG): what lands is
    byte-identical to the working-tree content the session reviewed, verified by a
    pre/post git-hash check. It never runs 'git stash' -- a stash's merge base is the
    shared HEAD, so applying it on origin/main did a 3-way merge that ALWAYS conflicted
    when the shared tree sat on a divergent feature branch (n=2, 2026-07-12).
  - The shared working tree is NEVER mutated: on any failure there is nothing to
    restore, the edit is still sitting untouched in your working tree.
  - Anti-clobber: if origin/main moved a journaled file since your merge base AND your
    copy would DELETE lines currently on origin/main (stale base -> silent content
    loss), it ABORTS, unless -AcceptMerge is given.
  Spec: docs/superpowers/specs/2026-05-29-journal-land-cross-fleet-design.md
.PARAMETER Subject
  Conventional-commit subject, e.g. "docs(journal): coop-WS surface 3 PR".
.PARAMETER Path
  Files to include in the commit. Default JOURNAL.md. Each must exist and not be gitignored.
.PARAMETER CodingAgent
  Agent id for the ADR-0011 "Coding-Agent:" commit trailer. Resolution order:
  this parameter > $env:CLAUDE_MODEL > 'claude-code' (generic fallback).
.PARAMETER NoMerge
  Create the PR but do not merge (default = try auto-merge, else wait for CI and
  merge directly -- this repo has auto-merge disabled).
.PARAMETER AcceptMerge
  Land your working-tree copy as-is even though origin/main moved the file since your
  merge base and your copy drops lines currently on origin/main (default = abort so
  the operator rebuilds the entry on top of 'git show origin/main:<file>').
  Intentional rewrites of origin-touched files also trip the guard; review, then pass this.
.PARAMETER DryRun
  Print planned actions, mutate nothing.
.EXAMPLE
  scripts/fleet/journal-land.ps1 -Subject "docs(journal): session X shipped"
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)] [string] $Subject,
  [string[]] $Path = @('JOURNAL.md'),
  [string] $CodingAgent = '',
  [switch] $NoMerge,
  [switch] $AcceptMerge,
  [switch] $DryRun
)

# native git writes to stderr on success; gate on $LASTEXITCODE only (anti-pattern L-040)
$ErrorActionPreference = 'Continue'

function Info($m) { Write-Host "[journal-land] $m" }
function Warn($m) { Write-Host "[journal-land] WARNING: $m" -ForegroundColor Yellow }
function Fail($m) { Write-Host "[journal-land] ERROR: $m" -ForegroundColor Red; exit 1 }

function Remove-Worktree($wt) {
  # remove the throwaway worktree dir (branch ref is untouched) + prune registration
  if ($wt -and (Test-Path -LiteralPath $wt)) { & git worktree remove --force $wt *> $null }
  & git worktree prune *> $null
}

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

# --- resolve ADR-0011 "Coding-Agent:" trailer id: param > $env:CLAUDE_MODEL > generic ---
if (-not $CodingAgent) { $CodingAgent = $env:CLAUDE_MODEL }
if (-not $CodingAgent) { $CodingAgent = 'claude-code' }
$CodingAgent = $CodingAgent.Trim()
# trailer value must stay a single ASCII token: whitespace/control chars from a polluted
# env var would corrupt the trailer block (and ADR-0021 wants ASCII-only)
if ($CodingAgent -notmatch '^[A-Za-z0-9][A-Za-z0-9._/:+\[\]-]*$') {
  Warn "CodingAgent value not a plain ASCII token -- falling back to 'claude-code'."
  $CodingAgent = 'claude-code'
}

# --- validate -Path entries: must exist + not gitignored (a typo'd/ignored path must NOT 'succeed') ---
foreach ($p in $Path) {
  if (-not (Test-Path -LiteralPath $p)) { Fail "path not found: $p (typo? run from repo root)" }
  & git check-ignore -q -- $p
  if ($LASTEXITCODE -eq 0) { Fail "path is gitignored, cannot journal: $p" }
}

# current branch is informational only: the worktree isolates us, so we never switch it
# back and detached HEAD is fine. Just nudge against an accidental ff-pull on a feature branch.
$origBranch = (& git rev-parse --abbrev-ref HEAD 2>$null)
if ($origBranch) { $origBranch = $origBranch.Trim() } else { $origBranch = '(detached)' }

# --- changes present? (genuine 'tracked but no diff' is the only no-op now) ---
$changed = (& git status --porcelain -- $Path)
if (-not $changed) {
  # old habit that caused the original drift: entry COMMITTED on a feature branch -> the
  # working tree is clean here but the content is stranded. Hint instead of silent no-op.
  # (origin/main ref may predate a fetch -- hint only, not a gate.)
  foreach ($p in $Path) {
    $gp = $p -replace '\\', '/'
    $stranded = (& git rev-list origin/main..HEAD -- $gp 2>$null)
    if ($stranded) { Warn "'$p' has no working-tree edit but commits on '$origBranch' touch it (not on origin/main) -- this helper lands WORKING-TREE edits only; a committed entry stays stranded on the branch." }
  }
  Info "no changes in [$($Path -join ', ')] -- nothing to journal."; exit 0
}

if ($origBranch -ne 'main') {
  Info "current branch '$origBranch' is left untouched (work happens in a throwaway worktree)."
}

# --- branch name (host + date, collision suffix) ---
$hostTag = ($env:COMPUTERNAME).ToLower() -replace '[^a-z0-9-]', '-'
$dateTag = Get-Date -Format 'yyyy-MM-dd'
$branch  = "claude/journal-$hostTag-$dateTag"
& git rev-parse --verify --quiet "refs/heads/$branch" *> $null
if ($LASTEXITCODE -eq 0) { $branch = "$branch-$(Get-Date -Format 'HHmmss')" }

if ($DryRun) {
  Info "DRY-RUN -- no mutation:"
  Info "  base       : origin/main (would fetch)"
  Info "  branch     : $branch (in a throwaway worktree)"
  Info "  paths      : $($Path -join ', ')"
  Info "  subject    : $Subject"
  Info "  agent      : $CodingAgent (Coding-Agent trailer)"
  Info "  merge      : $([bool](-not $NoMerge)) (auto-merge try, else CI-wait + direct)"
  Info "  shared HEAD: '$origBranch' (never switched)"
  exit 0
}

# --- record the session's reviewed content hash per file (copy-fidelity check later).
# --no-filters: byte identity is the assertion; checkout-side .gitattributes must not skew it ---
$preHash = @{}
foreach ($p in $Path) { $preHash[$p] = ("$(& git hash-object --no-filters $p)").Trim() }

# --- fetch clean base ---
& git fetch origin main
if ($LASTEXITCODE -ne 0) { Fail "git fetch origin main failed" }

# --- throwaway worktree on freshly fetched origin/main: the shared tree is NEVER touched ---
$wt = Join-Path ([IO.Path]::GetTempPath()) "jl-wt-$PID-$(Get-Date -Format 'HHmmssfff')"
$wtOut = ((& git worktree add -b $branch $wt origin/main 2>&1) | Out-String)
if ($LASTEXITCODE -ne 0) { Fail "git worktree add failed: $($wtOut.Trim()). Nothing was touched (stale worktree? try 'git worktree prune')." }

# --- carry the edit by DIRECT COPY: what lands is byte-identical to what the session reviewed.
# (v3 2026-07-12: replaces stash push/apply -- a stash's merge base is the shared HEAD, so
# applying it on origin/main was a 3-way merge that ALWAYS conflicted with the shared tree on
# a divergent feature branch, even with the entry built on origin/main content; n=2.) ---
foreach ($p in $Path) {
  $dst = Join-Path $wt $p
  $dstDir = Split-Path $dst -Parent
  if (-not (Test-Path -LiteralPath $dstDir)) { New-Item -ItemType Directory -Force $dstDir | Out-Null }
  Copy-Item -LiteralPath $p -Destination $dst -Force
  $post = ("$(& git -C $wt hash-object --no-filters $p)").Trim()
  if ($post -ne $preHash[$p]) {
    Remove-Worktree $wt; & git branch -D $branch *> $null
    Fail "copy fidelity check failed for '$p' (landed hash != reviewed hash). Nothing was landed; your working tree is untouched."
  }
}

& git -C $wt add -- $Path
if ($LASTEXITCODE -ne 0) {
  Remove-Worktree $wt; & git branch -D $branch *> $null
  Fail "git add failed. Nothing was landed; your working tree is untouched."
}

# --- anti-clobber: landing a copy built on a STALE base would silently DROP content that is
# on origin/main now. Suspicious only when BOTH hold: origin moved the file since our merge
# base, AND our staged copy deletes lines vs origin/main (a pure newest-first insert deletes
# nothing, so the n=2 incident pattern -- entry rebuilt on origin content -- passes clean). ---
$mergeBase = (& git merge-base HEAD origin/main 2>$null)
if ($mergeBase) { $mergeBase = $mergeBase.Trim() }
$clobber = @()
foreach ($p in $Path) {
  $gp = $p -replace '\\', '/'
  $baseBlob   = (& git rev-parse --verify --quiet "${mergeBase}:${gp}" 2>$null)
  $originBlob = (& git rev-parse --verify --quiet "origin/main:${gp}" 2>$null)
  $moved = (-not $mergeBase) -or ("$baseBlob" -ne "$originBlob")
  if (-not $moved) { continue }
  # numstat: added<TAB>deleted<TAB>path ('-' = binary -> cannot verify -> treat as risk)
  $stat = (& git -C $wt diff --cached --numstat -- $gp | Select-Object -First 1)
  if ($stat) {
    $deleted = ("$stat" -split "`t")[1]
    if ($deleted -ne '0') { $clobber += $p }
  }
}
if ($clobber.Count -gt 0 -and -not $AcceptMerge) {
  Remove-Worktree $wt; & git branch -D $branch *> $null
  Fail "origin/main moved [$($clobber -join ', ')] since your base and your copy DROPS lines that are on origin/main now (stale base?). Nothing was landed; your working tree is untouched. Rebuild the entry on top of 'git show origin/main:<file>' and re-run, or pass -AcceptMerge to land your copy as-is (overwriting origin's version)."
}
if ($clobber.Count -gt 0) { Warn "landing a copy that rewrites origin/main content in [$($clobber -join ', ')] (-AcceptMerge)." }

# --- commit in the worktree ---
$msgFile = [IO.Path]::GetTempFileName()
$body = "$Subject`n`nCoding-Agent: $CodingAgent`nTrace-Id: $(New-TraceId)`n"
[IO.File]::WriteAllText($msgFile, $body, (New-Object System.Text.UTF8Encoding($false)))  # no BOM
& git -C $wt commit -F $msgFile
$rc = $LASTEXITCODE
Remove-Item $msgFile -Force -ErrorAction SilentlyContinue
if ($rc -ne 0) {
  Remove-Worktree $wt; & git branch -D $branch *> $null
  Fail "git commit failed (commit-msg hook? check subject). Nothing was landed; your working tree is untouched."
}
Info "committed locally on '$branch'"

# --- push (SSH; works on both PCs) ---
& git -C $wt push -u origin $branch
if ($LASTEXITCODE -ne 0) { Remove-Worktree $wt; Fail "git push failed. Commit is on local branch '$branch' (not lost). Re-push from main tree: git push -u origin $branch. Check SSH key / network." }
Info "pushed origin/$branch"

# branch is on origin + a local ref now; free the worktree so the branch is not checked out
# anywhere (lets 'gh --delete-branch' / 'git branch -D' succeed cleanly).
Remove-Worktree $wt

# --- PR via gh if authed; else graceful push-only (Ryzen) ---
& gh auth status *> $null
if ($LASTEXITCODE -ne 0) {
  & git branch -D $branch *> $null   # local copy redundant (pushed); keep the fleet tidy
  Info "gh NOT authenticated. Branch pushed to origin = content SAFE (not stranded)."
  Info "Open/merge the PR from the hub, or run 'gh auth login -h github.com'."
  exit 0
}
$prBody = "Automated journal landing via scripts/fleet/journal-land.ps1. Host: $hostTag. Base: origin/main."
& gh pr create --base main --head $branch --title $Subject --body $prBody
if ($LASTEXITCODE -ne 0) { Fail "gh pr create failed (branch '$branch' is pushed to origin; open the PR manually)." }
$prUrl = (& gh pr view $branch --json url --jq '.url' 2>$null)
if (-not $prUrl) { $prUrl = "$branch (PR URL lookup pending)" }
Info "PR: $prUrl"

if (-not $NoMerge) {
  # $branch is not checked out anywhere now -> --delete-branch succeeds without a false error
  & gh pr merge $branch --auto --squash --delete-branch *> $null
  if ($LASTEXITCODE -eq 0) { Info "auto-merge (squash) queued; remote branch deletes on merge." }
  else {
    # this repo has PR auto-merge DISABLED (GraphQL enablePullRequestAutoMerge fails) ->
    # bounded wait for CI (ascii-guard + pytest, runs on every PR), then merge directly
    Info "auto-merge unavailable on this repo -- waiting for CI (max 5 min), then merging directly."
    $deadline = (Get-Date).AddMinutes(5)
    $green = 0
    do {
      $checksOut = ((& gh pr checks $branch 2>&1) | Out-String)
      $checks = $LASTEXITCODE   # 0 = all registered checks green; 8 = pending; other = failed
      # a just-created PR can report no checks for a few seconds -> treat as pending
      if ($checks -ne 0 -and $checksOut -match 'no checks reported') { $checks = 8 }
      # require TWO consecutive green polls: right after create a fast job can register+green
      # before a slower sibling job registers, and exit 0 would merge past the missing gate
      if ($checks -eq 0) { $green++ } else { $green = 0 }
      if ($green -ge 2 -or ($checks -ne 0 -and $checks -ne 8)) { break }
      Start-Sleep -Seconds 15
    } while ((Get-Date) -lt $deadline)
    if ($green -ge 2) {
      & gh pr merge $branch --squash --delete-branch
      if ($LASTEXITCODE -eq 0) { Info "merged (squash) after CI green; remote branch deleted." }
      else { Info "direct merge failed; PR left open for manual merge: $prUrl" }
    }
    elseif ($checks -eq 8 -or $checks -eq 0) { Info "CI still pending after 5 min; PR left open. Merge with: gh pr merge $branch --squash --delete-branch" }
    else { Info "CI checks FAILED; PR left open for review: $prUrl" }
  }
}

& git branch -D $branch *> $null     # local copy redundant (pushed); avoids per-session accumulation
if ($origBranch -eq 'main') { Info "reminder: 'git pull --ff-only' on main to sync after the squash lands." }
Info "note: your working-tree edit stays in place (copy carry); on a feature branch discard it with 'git checkout -- <file>' once the PR is merged."
Info "done. shared working tree ('$origBranch') was never touched."
exit 0
