<#
.SYNOPSIS
  Dry-run validator for cross-repo PR drafting (Component 2 spec V3 Opt 1.5 REDUCED).

.DESCRIPTION
  Validates pre-PR conditions WITHOUT calling gh pr create:
    1. Repo target is in whitelist allow-list (Game / Godot-v2 / Dafne / vault)
    2. Cross-repo PR whitelist check passes (~/.config/cross-repo-pr-whitelist.txt)
    3. Local repo path exists + is git repo
    4. PR type is valid taxonomy
    5. Preview files exist + are readable

  Outputs DRAFT PR body to console (does NOT push).

.PARAMETER RepoTarget
  Target repo: Game / Godot-v2 / Dafne / vault

.PARAMETER Type
  PR type: policy-alignment / ADR-cross-ref / drift-fix / docs / governance-suggestion

.PARAMETER PreviewFiles
  Comma-separated paths of files this PR will touch

.PARAMETER Summary
  1-2 line summary of proposed change

.EXAMPLE
  .\dry-run-pr.ps1 -RepoTarget Game -Type docs -PreviewFiles "README.md,docs/adr/index.md" -Summary "Fix broken link"
#>

param(
  [Parameter(Mandatory=$true)]
  [ValidateSet('Game', 'Godot-v2', 'Dafne', 'vault')]
  [string]$RepoTarget,

  [Parameter(Mandatory=$true)]
  [ValidateSet('policy-alignment', 'ADR-cross-ref', 'drift-fix', 'docs', 'governance-suggestion')]
  [string]$Type,

  [Parameter(Mandatory=$true)]
  [string]$PreviewFiles,

  [Parameter(Mandatory=$true)]
  [string]$Summary
)

$ErrorActionPreference = 'Stop'

# Repo path mapping (Lenovo defaults)
$repoMap = @{
  'Game'     = 'C:\dev\Game'
  'Godot-v2' = 'C:\dev\Game-Godot-v2'
  'Dafne'    = 'C:\Users\edusc\Dafne\workspace\swarm'
  'vault'    = 'C:\dev\vault-shared'
}

$repoPath = $repoMap[$RepoTarget]

Write-Host "=== Cross-repo PR dry-run validator ===" -ForegroundColor Cyan
Write-Host "Repo target: $RepoTarget ($repoPath)"
Write-Host "PR type: $Type"
Write-Host ""

# Check 1: repo path exists
if (-not (Test-Path $repoPath)) {
  Write-Host "FAIL [1]: repo path not found: $repoPath" -ForegroundColor Red
  exit 1
}
Write-Host "PASS [1] repo path exists" -ForegroundColor Green

# Check 2: is git repo
if (-not (Test-Path "$repoPath\.git")) {
  Write-Host "FAIL [2]: not a git repo (no .git dir): $repoPath" -ForegroundColor Red
  exit 1
}
Write-Host "PASS [2] is git repo" -ForegroundColor Green

# Check 3: cross-repo PR whitelist
# Separate from aider-privacy-whitelist.txt (cloud LLM delegation semantics).
# Format per line: <name> <absolute-path> (whitespace-separated). Comments # ignored.
$whitelistPath = "$env:USERPROFILE\.config\cross-repo-pr-whitelist.txt"
if (-not (Test-Path $whitelistPath)) {
  Write-Host "FAIL [3]: cross-repo PR whitelist not found: $whitelistPath" -ForegroundColor Red
  exit 1
}

# Canonicalize local repo path (handles trailing slashes, case normalization)
try {
  $canonicalRepoPath = (Resolve-Path $repoPath).Path
} catch {
  $canonicalRepoPath = $repoPath
}

$whitelistLines = Get-Content $whitelistPath |
  Where-Object { $_ -notlike "#*" -and $_.Trim() -ne "" }

$repoMatchesWhitelist = $false
foreach ($line in $whitelistLines) {
  $parts = $line.Trim() -split '\s+', 2
  if ($parts.Count -lt 2) { continue }
  $wlName = $parts[0]
  $wlPath = $parts[1].Trim()

  # Canonicalize whitelist path for comparison
  try {
    $canonicalWlPath = (Resolve-Path $wlPath).Path
  } catch {
    $canonicalWlPath = $wlPath
  }

  # Match on name column OR canonical path (case-insensitive, Windows)
  if ($wlName -ieq $RepoTarget -or $canonicalWlPath -ieq $canonicalRepoPath) {
    $repoMatchesWhitelist = $true
    break
  }
}

if (-not $repoMatchesWhitelist) {
  Write-Host "FAIL [3]: repo $RepoTarget NOT in cross-repo PR whitelist ($whitelistPath)" -ForegroundColor Red
  exit 1
}
Write-Host "PASS [3] cross-repo PR whitelist" -ForegroundColor Green

# Check 4: preview files exist
$files = $PreviewFiles -split ','
foreach ($f in $files) {
  $f = $f.Trim()
  $fullPath = Join-Path $repoPath $f
  if (-not (Test-Path $fullPath)) {
    Write-Host "WARN [4]: preview file not found locally: $fullPath" -ForegroundColor Yellow
  } else {
    Write-Host "PASS [4] preview file exists: $f" -ForegroundColor Green
  }
}

# Output DRAFT PR body
Write-Host ""
Write-Host "=== DRAFT PR body (copy/paste into gh pr create) ===" -ForegroundColor Cyan
Write-Host ""
$body = @"
## Summary

$Summary

## Type

- Type: $Type
- codemasterdd ADR ref: <fill in ADR-NNNN or N/A>
- L-XXX lesson ref: <fill in L-2026-MM-NNN or N/A>

## Source codemasterdd

- Repo: ``MasterDD-L34D/codemasterdd-ai-station``
- Branch/commit: <fill in>
- File ref originale: <fill in>

## Proposed change

- Files touched in this PR:
$($files | ForEach-Object { "  - ``$($_.Trim())``" } | Out-String)

## Privacy class

- Repo target privacy: <fill in sovereign-only / mixed / cloud-OK>
- Whitelist check: PASSED (verified via dry-run-pr.ps1)

## Reversibility

- Reverting cost stimato: <minutes/hours/days>

## Governance interna repo target

- Decision: governance interna autosufficiente, accept/reject/amend a vostra discrezione
- codemasterdd-side: NO write-direct, NO push --force, NO bypass review

[Generated with Claude Code via cross-repo Component 2 workflow]
"@

Write-Host $body
Write-Host ""
Write-Host "=== Next steps ===" -ForegroundColor Cyan
Write-Host "1. cd $repoPath"
Write-Host "2. Make file changes on a new branch"
Write-Host "3. gh pr create --title '<type>(<scope>): <subject>' --body '<paste above>'"
Write-Host "4. Append outcome row to logs/cross-repo-pr-YYYY-MM.md"
Write-Host ""
Write-Host "DRY-RUN OK -- no actual PR created." -ForegroundColor Green
exit 0
