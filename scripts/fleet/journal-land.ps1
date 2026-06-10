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

  Safety contract (the whole point of the tool):
  - Does all branch/commit work in a THROWAWAY git WORKTREE based on a freshly fetched
    origin/main. It NEVER runs 'git switch' in the shared working tree, so it can never
    yank HEAD out from under a concurrent session on the same clone (shared-clone safe).
  - Carries the edit off the shared tree via a UNIQUELY-TAGGED stash and references that
    stash by its immutable COMMIT SHA for apply (never stash@{N}, a positional alias that
    a concurrent stash push would shift); drops it by re-resolving the tag at drop-time.
  - Keeps the safety-net stash until the commit SUCCEEDS, so a failed add/commit restores
    the edit instead of losing it.
  - If origin changed a journaled file concurrently (a clean 3-way merge would mix in
    content the session never reviewed) it ABORTS and restores the edit, unless
    -AcceptMerge is given.
  - Every recovery/exit-code is checked: it never silently strands the edit and never
    lies that it was restored (two-tier message: restored-to-tree vs preserved-in-stash).
  Spec: docs/superpowers/specs/2026-05-29-journal-land-cross-fleet-design.md
.PARAMETER Subject
  Conventional-commit subject, e.g. "docs(journal): coop-WS surface 3 PR".
.PARAMETER Path
  Files to include in the commit. Default JOURNAL.md. Each must exist and not be gitignored.
.PARAMETER CodingAgent
  Agent id for the ADR-0011 "Coding-Agent:" commit trailer. Resolution order:
  this parameter > $env:CLAUDE_MODEL > 'claude-code' (generic fallback).
.PARAMETER NoMerge
  Create the PR but do not auto-merge (default = create PR + auto-merge squash).
.PARAMETER AcceptMerge
  Allow a concurrent origin/main 3-way merge of a journaled file to be committed
  (default = abort + restore the edit so the operator reviews / redoes the insert).
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

function Get-StashShaByTag($tag) {
  # immutable commit SHA of OUR stash -- race-immune (apply/pop by stash@{N} would follow
  # the index, which a concurrent stash push shifts). $null if not found.
  $line = (& git stash list --format='%H %gs' | Select-String -SimpleMatch $tag | Select-Object -First 1)
  if (-not $line) { return $null }
  return (($line.ToString() -split '\s+')[0])
}

function Remove-StashByTag($tag) {
  # drop must use a stash@{N} ref (a SHA is rejected); re-resolve the index by tag AT
  # drop-time (it can have shifted), confirm it is still ours, then drop + check exit.
  $line = (& git stash list --format='%gd %gs' | Select-String -SimpleMatch $tag | Select-Object -First 1)
  if (-not $line) { return $true }   # already gone -> nothing to drop
  $ref = (($line.ToString() -split '\s+')[0])
  & git stash drop $ref *> $null
  return ($LASTEXITCODE -eq 0)
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

# --- changes present? (genuine 'tracked but no diff' is the only no-op now) ---
$changed = (& git status --porcelain -- $Path)
if (-not $changed) { Info "no changes in [$($Path -join ', ')] -- nothing to journal."; exit 0 }

# current branch is informational only: the worktree isolates us, so we never switch it
# back and detached HEAD is fine. Just nudge against an accidental ff-pull on a feature branch.
$origBranch = (& git rev-parse --abbrev-ref HEAD 2>$null)
if ($origBranch) { $origBranch = $origBranch.Trim() } else { $origBranch = '(detached)' }
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
  Info "  auto-merge : $([bool](-not $NoMerge))"
  Info "  shared HEAD: '$origBranch' (never switched)"
  exit 0
}

# --- record the session's content hash per file, to detect a silent 3-way merge later ---
$preHash = @{}
foreach ($p in $Path) { $preHash[$p] = (& git hash-object $p).Trim() }

# --- fetch clean base ---
& git fetch origin main
if ($LASTEXITCODE -ne 0) { Fail "git fetch origin main failed" }

# --- carry the edit off the SHARED tree via a UNIQUELY-TAGGED stash (-u: also new untracked) ---
$stashTag = "journal-land-$PID-$(Get-Date -Format 'HHmmssfff')"
& git stash push -u -m $stashTag -- $Path
if ($LASTEXITCODE -ne 0) { Fail "git stash failed" }
# resolve OUR stash to its immutable COMMIT SHA (apply by SHA is race-immune; stash@{N} is not)
$stashSha = Get-StashShaByTag $stashTag
if (-not $stashSha) { Fail "could not locate our stash ($stashTag) after push -- aborting before any branch work." }

# --- throwaway worktree on freshly fetched origin/main: NEVER switches the shared HEAD ---
$wt = Join-Path ([IO.Path]::GetTempPath()) "jl-wt-$stashTag"
& git worktree add -b $branch $wt origin/main *> $null
if ($LASTEXITCODE -ne 0) {
  # worktree not created; we are still in the shared tree. Restore the edit there (by SHA).
  & git stash apply $stashSha *> $null
  # drop the stash ONLY if the restore succeeded; otherwise the stash is the last copy -- keep it
  if ($LASTEXITCODE -eq 0) { [void](Remove-StashByTag $stashTag); Fail "git worktree add failed (branch '$branch' exists, or a stale worktree). Edit restored to your working tree." }
  Fail "git worktree add failed AND restore failed. Edit PRESERVED in 'git stash list' ($stashTag) -- restore manually."
}

# --- apply the edit INTO the worktree by SHA (keep the stash as a safety net until commit) ---
& git -C $wt stash apply $stashSha
if ($LASTEXITCODE -ne 0) {
  Remove-Worktree $wt; & git branch -D $branch *> $null
  & git stash apply $stashSha *> $null            # restore to the shared tree (by SHA)
  if ($LASTEXITCODE -eq 0) { [void](Remove-StashByTag $stashTag); Fail "stash apply conflict vs origin/main (overlapping edit). Edit restored to your working tree. Run 'git pull --ff-only' on main, redo the insert, re-run." }
  Fail "stash apply conflict AND restore failed. Edit PRESERVED in 'git stash list' ($stashTag) -- resolve manually."
}

# --- detect a SILENT clean 3-way merge (origin changed a journaled file in a separate hunk) ---
$merged = @()
foreach ($p in $Path) {
  $wp = Join-Path $wt $p
  if (Test-Path -LiteralPath $wp) {
    $post = (& git -C $wt hash-object $p).Trim()
    if ($post -ne $preHash[$p]) { $merged += $p }
  }
}
if ($merged.Count -gt 0 -and -not $AcceptMerge) {
  # do NOT silently publish content the session never reviewed -> abort + restore
  Remove-Worktree $wt; & git branch -D $branch *> $null
  & git stash apply $stashSha *> $null
  if ($LASTEXITCODE -eq 0) { [void](Remove-StashByTag $stashTag); Fail "origin changed [$($merged -join ', ')] concurrently -- a clean 3-way merge would land content you did not review. Edit restored to your working tree. Run 'git pull --ff-only' on main, redo the insert, re-run (or pass -AcceptMerge to land the merged result)." }
  Fail "origin changed [$($merged -join ', ')] concurrently AND restore failed. Edit PRESERVED in 'git stash list' ($stashTag) -- resolve manually."
}
if ($merged.Count -gt 0) { Warn "origin changed [$($merged -join ', ')] concurrently; committing the 3-way merge result (-AcceptMerge)." }

# --- stage + commit in the worktree. Keep the safety stash until the commit SUCCEEDS. ---
& git -C $wt add -- $Path
if ($LASTEXITCODE -ne 0) {
  Remove-Worktree $wt; & git branch -D $branch *> $null
  & git stash apply $stashSha *> $null
  if ($LASTEXITCODE -eq 0) { [void](Remove-StashByTag $stashTag); Fail "git add failed. Edit restored to your working tree." }
  Fail "git add failed AND restore failed. Edit PRESERVED in 'git stash list' ($stashTag)."
}
$msgFile = [IO.Path]::GetTempFileName()
$body = "$Subject`n`nCoding-Agent: $CodingAgent`nTrace-Id: $(New-TraceId)`n"
[IO.File]::WriteAllText($msgFile, $body, (New-Object System.Text.UTF8Encoding($false)))  # no BOM
& git -C $wt commit -F $msgFile
$rc = $LASTEXITCODE
Remove-Item $msgFile -Force -ErrorAction SilentlyContinue
if ($rc -ne 0) {
  Remove-Worktree $wt; & git branch -D $branch *> $null
  & git stash apply $stashSha *> $null
  if ($LASTEXITCODE -eq 0) { [void](Remove-StashByTag $stashTag); Fail "git commit failed (commit-msg hook? check subject). Edit restored to your working tree." }
  Fail "git commit failed AND restore failed. Edit PRESERVED in 'git stash list' ($stashTag)."
}
# commit succeeded -> the edit is safely in a commit on $branch -> now drop the safety stash
if (-not (Remove-StashByTag $stashTag)) { Warn "could not drop the safety stash ($stashTag); remove manually with 'git stash drop' (non-fatal)." }
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
  & gh pr merge $branch --auto --squash --delete-branch
  if ($LASTEXITCODE -ne 0) { Info "auto-merge not enabled; PR left open for manual merge: $prUrl" }
  else { Info "auto-merge (squash) queued; remote branch deletes on merge." }
}

& git branch -D $branch *> $null     # local copy redundant (pushed); avoids per-session accumulation
if ($origBranch -eq 'main') { Info "reminder: 'git pull --ff-only' on main to sync after the squash lands." }
Info "done. shared working tree ('$origBranch') was never switched."
exit 0
