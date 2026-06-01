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
# Test 3: CLAUDE.md merge -- absent then idempotent (P0#3 + idempotency)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 3: CLAUDE.md merge absent + idempotent"

$scriptText = Get-Content -Raw $scriptPath
# Find LAST switch (dispatch), not the early MODE switch.
$lastCut = $scriptText.LastIndexOf('switch ($PSCmdlet')
if ($lastCut -lt 0) { throw "Cannot find dispatch in deploy script" }
$functionsOnly = $scriptText.Substring(0, $lastCut)
. ([scriptblock]::Create($functionsOnly))

# Ensure sentinel variables are in scope (fallback if dot-source did not expose them).
if (-not (Get-Variable -Name 'startSentinel' -ErrorAction SilentlyContinue)) {
  $startSentinel = '## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)'
  $disambigRegex = '^\*\*Rule\*\* \(STRONG'
}

$tmpRoot = Join-Path $env:TEMP "merge-test-$([guid]::NewGuid())"
New-Item -ItemType Directory -Force -Path $tmpRoot | Out-Null
$claudeMd = Join-Path $tmpRoot 'CLAUDE.md'
$fragment = Join-Path $tmpRoot 'directive.md'

Set-Content -Path $claudeMd -Value "# Existing CLAUDE.md`r`n`r`n## Other section`r`n`r`nbody" -Encoding utf8
$fragmentContent = @"
## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG-PURE, no bypass): test directive body.

<!-- END agent-scanner-directive -->
"@
Set-Content -Path $fragment -Value $fragmentContent -Encoding utf8

$state1 = Test-DirectivePresent -ClaudeMdPath $claudeMd -StartSentinel $startSentinel -DisambigRegex $disambigRegex
Assert-Eq -Expected 'absent' -Actual $state1 -Name "merge Test-DirectivePresent absent"

$ok1 = Invoke-ClaudeMdMerge -ClaudeMdPath $claudeMd -FragmentPath $fragment `
                              -StartSentinel $startSentinel -DisambigRegex $disambigRegex
Assert-True -Condition $ok1 -Name "merge run-1 append ok"

$state2 = Test-DirectivePresent -ClaudeMdPath $claudeMd -StartSentinel $startSentinel -DisambigRegex $disambigRegex
Assert-Eq -Expected 'present-valid' -Actual $state2 -Name "merge post-append state present-valid"

$contentBefore = Read-FileUtf8NoBom -Path $claudeMd
$ok2 = Invoke-ClaudeMdMerge -ClaudeMdPath $claudeMd -FragmentPath $fragment `
                              -StartSentinel $startSentinel -DisambigRegex $disambigRegex
$contentAfter = Read-FileUtf8NoBom -Path $claudeMd
Assert-True -Condition $ok2 -Name "merge run-2 ok"
Assert-Eq -Expected $contentBefore -Actual $contentAfter -Name "merge run-2 idempotent (no diff)"

Remove-Item -Recurse -Force $tmpRoot

# ----------------------------------------------------------------------
# Test 4: CLAUDE.md merge ambiguous sentinel (P1#4 distinct error)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 4: ambiguous sentinel rejected"

$tmpRoot = Join-Path $env:TEMP "merge-test-$([guid]::NewGuid())"
New-Item -ItemType Directory -Force -Path $tmpRoot | Out-Null
$claudeMd = Join-Path $tmpRoot 'CLAUDE.md'

Set-Content -Path $claudeMd -Value "## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)`r`n`r`nSomeone overwrote the rule with prose.`r`n" -Encoding utf8

$state = Test-DirectivePresent -ClaudeMdPath $claudeMd -StartSentinel $startSentinel -DisambigRegex $disambigRegex
Assert-Eq -Expected 'ambiguous' -Actual $state -Name "ambiguous sentinel detected"

Remove-Item -Recurse -Force $tmpRoot

# ----------------------------------------------------------------------
# Test 5: Remove strips bounded directive without eating user content (P0#3)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 5: Remove bounded -- user content preserved"

$tmpRoot = Join-Path $env:TEMP "remove-test-$([guid]::NewGuid())"
New-Item -ItemType Directory -Force -Path $tmpRoot | Out-Null
$claudeMd = Join-Path $tmpRoot 'CLAUDE.md'

$initial = @"
# CLAUDE.md

## Section A

User content A.

## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG-PURE): directive body.

<!-- END agent-scanner-directive -->

This user line MUST survive Remove (P0#3 footgun).

## Section B (post-directive)

User content B.
"@
Set-Content -Path $claudeMd -Value $initial -Encoding utf8

if (-not (Get-Variable -Name 'endSentinel' -ErrorAction SilentlyContinue)) {
  $endSentinel = '<!-- END agent-scanner-directive -->'
}

Invoke-Rollback -TargetSkillDir "$tmpRoot\nonexistent-skill" -ClaudeMdPath $claudeMd `
                -StartSentinel $startSentinel -EndSentinel $endSentinel | Out-Null

$after = Read-FileUtf8NoBom -Path $claudeMd
Assert-True -Condition (-not ($after -match 'Agent Scanner discipline')) -Name "start sentinel removed"
Assert-True -Condition (-not ($after -match 'END agent-scanner-directive')) -Name "END sentinel removed"
Assert-True -Condition ($after -match 'This user line MUST survive') -Name "user content post-directive preserved (P0#3)"
Assert-True -Condition ($after -match '## Section A') -Name "user content pre-directive preserved"
Assert-True -Condition ($after -match '## Section B') -Name "user content section-B preserved"

Remove-Item -Recurse -Force $tmpRoot

# ----------------------------------------------------------------------
# Test 6: canonical assets must be ASCII-clean (ADR-0021 body prose policy)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 6: canonical assets ASCII clean"

$canonicalSkillFile = Join-Path $repoRoot '.claude\global-skills\agent-scanner\SKILL.md'
$canonicalFragmentFile = Join-Path $repoRoot '.claude\global-claude-md-fragments\agent-scanner-directive.md'

$skillContent = Get-Content -Raw $canonicalSkillFile
Assert-True -Condition (-not ($skillContent -match '[^\x00-\x7F]')) -Name "canonical SKILL.md ASCII"

$fragContent = Get-Content -Raw $canonicalFragmentFile
Assert-True -Condition (-not ($fragContent -match '[^\x00-\x7F]')) -Name "canonical fragment ASCII"

# ----------------------------------------------------------------------
# Test 7: scope-7 ARCHON detection (vendored in vault git, cross-PC; graceful-missing where deploy absent)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 7: ARCHON source absent != enumeration failure"

Assert-True -Condition ($skillContent -match 'vendored nel git del vault') -Name "SKILL.md documents ARCHON vendored in vault (not Lenovo-only)"
Assert-True -Condition ($skillContent -match 'NON e.*errore') -Name "SKILL.md says missing source 7 not an error"

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
