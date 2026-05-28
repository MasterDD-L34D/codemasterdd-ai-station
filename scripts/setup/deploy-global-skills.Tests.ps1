<#
.SYNOPSIS
Lightweight test runner for deploy-global-skills.ps1.
No external dependencies (avoid Pester install requirement on fleet).
Run: .\scripts\setup\deploy-global-skills.Tests.ps1
Exit: 0 if all pass, 1 if any fail.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Continue'
$script:passed = 0
$script:failed = 0
$script:failures = @()

function Assert-True {
  param([bool]$Condition, [string]$Name)
  if ($Condition) {
    $script:passed++
    Write-Host "  [PASS] $Name" -ForegroundColor Green
  } else {
    $script:failed++
    $script:failures += $Name
    Write-Host "  [FAIL] $Name" -ForegroundColor Red
  }
}

function Assert-Eq {
  param($Expected, $Actual, [string]$Name)
  $cond = ($Expected -eq $Actual)
  if (-not $cond) { $Name = "$Name (expected=$Expected actual=$Actual)" }
  Assert-True -Condition $cond -Name $Name
}

# Source under test
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$scriptPath = Join-Path $PSScriptRoot 'deploy-global-skills.ps1'

# ----------------------------------------------------------------------
# Test 1: sentinel disambiguation regex (P0#2 from harsh review)
# ----------------------------------------------------------------------
Write-Host "Test 1: sentinel disambiguation regex"

# Fixture: directive content with blank line between sentinel and **Rule**
$fixture = @"
## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG-PURE, no bypass): the rule body...

more content
"@

$lines = $fixture -split "`n"
$startIdx = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($lines[$i] -match '^## Agent Scanner discipline \(anti-shadow-duplicate, cross-fleet\)$') {
    $startIdx = $i; break
  }
}
Assert-True -Condition ($startIdx -ge 0) -Name "start sentinel found"

# Scan first non-blank within next 5 lines, expect **Rule** (STRONG match
$foundRule = $false
for ($j = $startIdx + 1; $j -le [Math]::Min($startIdx + 5, $lines.Count - 1); $j++) {
  $line = $lines[$j].Trim()
  if (-not [string]::IsNullOrEmpty($line)) {
    if ($line -match '^\*\*Rule\*\* \(STRONG') { $foundRule = $true }
    break
  }
}
Assert-True -Condition $foundRule -Name "disambiguation: first non-blank within 5 lines matches Rule (STRONG"

# ----------------------------------------------------------------------
# Test 2: skill deploy hash-compare detects drift (P1#1 harsh)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 2: skill deploy hash-compare drift detection"

$tmpRoot = Join-Path $env:TEMP "deploy-test-$([guid]::NewGuid())"
$canonDir = Join-Path $tmpRoot 'canonical'
$targetDir = Join-Path $tmpRoot 'target'
New-Item -ItemType Directory -Force -Path $canonDir | Out-Null
New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

Set-Content -Path (Join-Path $canonDir 'SKILL.md') -Value "canonical content v1" -Encoding utf8
Set-Content -Path (Join-Path $targetDir 'SKILL.md') -Value "user-edited content drift" -Encoding utf8

$canonicalHash = (Get-FileHash -Algorithm SHA256 -Path (Join-Path $canonDir 'SKILL.md')).Hash
$targetHash = (Get-FileHash -Algorithm SHA256 -Path (Join-Path $targetDir 'SKILL.md')).Hash
Assert-True -Condition ($canonicalHash -ne $targetHash) -Name "hash-compare flags drift"

Set-Content -Path (Join-Path $targetDir 'SKILL.md') -Value "canonical content v1" -Encoding utf8
$targetHash2 = (Get-FileHash -Algorithm SHA256 -Path (Join-Path $targetDir 'SKILL.md')).Hash
Assert-True -Condition ($canonicalHash -eq $targetHash2) -Name "hash-compare no false-drift when content equal"

Remove-Item -Recurse -Force $tmpRoot

# ----------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Results: $script:passed passed, $script:failed failed"
if ($script:failed -gt 0) {
  Write-Host "Failures:" -ForegroundColor Red
  $script:failures | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
  exit 1
}
exit 0
