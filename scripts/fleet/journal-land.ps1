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

# --- carry the edit off the current branch (-u: also carry NEW untracked files in $Path) ---
& git stash push -u -m 'journal-land-temp' -- $Path
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
