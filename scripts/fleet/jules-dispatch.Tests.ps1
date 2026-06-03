<#
.SYNOPSIS
Lightweight test runner for jules-dispatch.ps1 pure gate-logic.
No external dependencies (avoid Pester install on fleet -- matches deploy-global-skills.Tests.ps1).
Dot-sources the function block (everything before '# === MAIN') and tests the pure units.
Run: powershell -NoProfile -File .\scripts\fleet\jules-dispatch.Tests.ps1
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
  if ($Condition) { $script:passed++; Write-Host "  [PASS] $Name" -ForegroundColor Green }
  else { $script:failed++; $script:failures += $Name; Write-Host "  [FAIL] $Name" -ForegroundColor Red }
}
function Assert-False { param([bool]$Condition, [string]$Name) Assert-True -Condition (-not $Condition) -Name $Name }
function Assert-Eq {
  param($Expected, $Actual, [string]$Name)
  $cond = ($Expected -eq $Actual)
  if (-not $cond) { $Name = "$Name (expected=$Expected actual=$Actual)" }
  Assert-True -Condition $cond -Name $Name
}

# --- Dot-source the pure function block from the script under test ---
$scriptPath = Join-Path $PSScriptRoot 'jules-dispatch.ps1'
if (-not (Test-Path $scriptPath)) { throw "SUT missing: $scriptPath (RED expected until built)" }
$scriptText = Get-Content -Raw $scriptPath
$cut = $scriptText.IndexOf('# === MAIN')
if ($cut -lt 0) { throw "Cannot find '# === MAIN' marker in $scriptPath" }
$functionsOnly = $scriptText.Substring(0, $cut)
. ([scriptblock]::Create($functionsOnly))

# Temp file helper
function New-TempFile { param([byte[]]$Bytes, [string]$Text)
  $p = Join-Path $env:TEMP ("jd-test-" + [guid]::NewGuid().ToString('N') + ".md")
  if ($PSBoundParameters.ContainsKey('Bytes')) { [IO.File]::WriteAllBytes($p, $Bytes) }
  else { [IO.File]::WriteAllText($p, $Text, (New-Object Text.UTF8Encoding $false)) }
  return $p
}

# ======================================================================
Write-Host "Test 1: Test-RepoWhitelisted (gate 1)"
Assert-True  (Test-RepoWhitelisted 'Game') 'Game whitelisted'
Assert-True  (Test-RepoWhitelisted 'codemasterdd-ai-station') 'codemasterdd whitelisted'
Assert-True  (Test-RepoWhitelisted 'Game-Godot-v2') 'Game-Godot-v2 whitelisted'
Assert-True  (Test-RepoWhitelisted 'Game-Database') 'Game-Database whitelisted'
Assert-False (Test-RepoWhitelisted 'synesthesia') 'synesthesia NOT whitelisted (sovereign)'
Assert-False (Test-RepoWhitelisted 'MasterDD-L34D/Game') 'owner/repo form NOT whitelisted (bare-name only)'
Assert-False (Test-RepoWhitelisted '') 'empty repo NOT whitelisted'

# ======================================================================
Write-Host "Test 2: Get-JulesSource (P0.1 owner constant)"
Assert-Eq 'sources/github/MasterDD-L34D/Game' (Get-JulesSource 'Game') 'source string for Game'
Assert-Eq 'sources/github/MasterDD-L34D/codemasterdd-ai-station' (Get-JulesSource 'codemasterdd-ai-station') 'source string for codemasterdd'

# ======================================================================
Write-Host "Test 3: Test-SessionActive (P0.2 terminal-denylist)"
Assert-False (Test-SessionActive 'COMPLETED') 'COMPLETED is terminal (not active)'
Assert-False (Test-SessionActive 'FAILED') 'FAILED is terminal'
Assert-False (Test-SessionActive 'CANCELLED') 'CANCELLED is terminal'
Assert-False (Test-SessionActive 'ARCHIVED') 'ARCHIVED is terminal'
Assert-False (Test-SessionActive 'completed') 'lowercase completed is terminal (case-insensitive)'
Assert-True  (Test-SessionActive 'IN_PROGRESS') 'IN_PROGRESS is active'
Assert-True  (Test-SessionActive 'AWAITING_USER_FEEDBACK') 'AWAITING_USER_FEEDBACK is active'
Assert-True  (Test-SessionActive 'PLANNING') 'unobserved PLANNING -> active (fail-closed)'
Assert-True  (Test-SessionActive '') 'empty state -> active (fail-closed)'
Assert-True  (Test-SessionActive $null) 'null state -> active (fail-closed)'

# ======================================================================
Write-Host "Test 4: Test-AsciiClean (gate 2, native byte-check)"
$ascii = New-TempFile -Text "plain ascii content, no accents"
Assert-True (Test-AsciiClean $ascii) 'pure ASCII file -> clean'
$nonascii = New-TempFile -Bytes ([byte[]](0x68,0x69,0xC3,0xA8))  # 'hi' + UTF8 e-grave
Assert-False (Test-AsciiClean $nonascii) 'file with 0xC3 0xA8 byte -> NOT clean'
$bom = New-TempFile -Bytes ([byte[]](0xEF,0xBB,0xBF,0x68,0x69))  # UTF8 BOM + 'hi'
Assert-False (Test-AsciiClean $bom) 'UTF8-BOM file -> NOT clean (intended, P1.1)'
$empty = New-TempFile -Bytes ([byte[]]@())
Assert-True (Test-AsciiClean $empty) 'empty file -> clean (gate 3 rejects empty separately)'
Remove-Item $ascii,$nonascii,$bom,$empty -Force -ErrorAction SilentlyContinue

# ======================================================================
Write-Host "Test 5: Test-ScopedTemplate (gate 3, 4 markers)"
$good = @"
Modify scripts/fleet/foo.ps1 only. Single-file, no logic change.
ASCII only, no accented chars.
Acceptance: tests pass and the diff touches one file.
"@
$r = Test-ScopedTemplate $good
Assert-True $r.Ok 'full-marker task-file -> Ok'
Assert-Eq 0 $r.Missing.Count 'full-marker -> zero missing'

$noAscii = "Modify scripts/fleet/foo.ps1 only. Single-file. Acceptance: tests pass."
$r2 = Test-ScopedTemplate $noAscii
Assert-False $r2.Ok 'missing ASCII clause -> not Ok'
Assert-True ($r2.Missing -contains 'ascii-only-clause') 'flags ascii-only-clause missing'

$noPath = "Improve the module. Single-file. ASCII only. Acceptance: tests pass."
$r3 = Test-ScopedTemplate $noPath
Assert-True ($r3.Missing -contains 'target-file-path') 'flags target-file-path missing'

$vague = "Improve code health and performance across the project."
$r4 = Test-ScopedTemplate $vague
Assert-False $r4.Ok 'vague code-health prompt -> rejected (ADR-0035 #1)'

# ======================================================================
Write-Host "Test 6: Get-TargetIdentifiers (derivation + stoplist)"
$idsA = @(Get-TargetIdentifiers 'scripts/fleet/foo.ps1')
Assert-True ($idsA -contains 'scripts/fleet/foo.ps1') 'path target -> full path id'
Assert-True ($idsA -contains 'foo') 'path target -> basename stem id'
$idsB = @(Get-TargetIdentifiers 'Get-Bar')
Assert-True ($idsB -contains 'get-bar') 'symbol target -> lowercased id'
$idsC = @(Get-TargetIdentifiers 'api utils')
Assert-Eq 0 $idsC.Count 'all-stoplist bare symbols -> zero ids (P1.4)'
$idsD = @(Get-TargetIdentifiers 'scripts/api/utils.ps1')
Assert-True ($idsD -contains 'scripts/api/utils.ps1') 'stoplisted-stem path keeps full path id'
Assert-False ($idsD -contains 'utils') 'stoplisted stem (utils) dropped'

# ======================================================================
Write-Host "Test 7: Test-TargetOverlap (gate 4 matcher -- load-bearing)"
Assert-True  (Test-TargetOverlap 'scripts/fleet/foo.ps1' 'today I work on scripts/fleet/foo.ps1 refactor') 'exact path -> overlap'
Assert-True  (Test-TargetOverlap 'flint_status.py' 'harden the flint_status helper dedupe') 'basename stem -> overlap'
Assert-True  (Test-TargetOverlap 'Get-Bar' 'refactor Get-Bar function signature') 'function token -> overlap'
Assert-False (Test-TargetOverlap 'fetch.js' 'optimize prefetchData and fetchAll caching layer') 'fetch vs prefetch/fetchAll -> NO overlap (boundary precision)'
Assert-False (Test-TargetOverlap 'scripts/a/alpha.ps1' 'working on scripts/b/beta.ps1 instead') 'distinct file -> no overlap'
Assert-True  (Test-TargetOverlap 'api' 'completely unrelated session text') 'generic-collapse target -> conservative overlap (abort)'
# KNOWN residual false-negative (spec sec 7#1) -- asserted honestly, NOT pretended-closed:
Assert-False (Test-TargetOverlap 'flint_status.py' 'fix the status helper that dedupes runs') 'KNOWN false-neg: synonym-named session is MISSED (disclosed sec 7#1)'

# ======================================================================
Write-Host "Test 8: Test-TargetInTaskFile (P1.3 gate3<->Target consistency)"
$tf = "Modify scripts/fleet/foo.ps1 only. ASCII only. Acceptance: tests pass."
Assert-True  (Test-TargetInTaskFile 'scripts/fleet/foo.ps1' $tf) 'Target named in task-file -> consistent'
Assert-False (Test-TargetInTaskFile 'scripts/fleet/bar.ps1' $tf) 'Target NOT in task-file -> inconsistent (would abort)'
Assert-True  (Test-TargetInTaskFile 'foo' $tf) 'stem Target present in task-file -> consistent'

# ======================================================================
Write-Host "Test 10: Find-ActiveOverlap (gate 4 wiring -- state+source filter over a session fixture)"
function New-FakeSession { param($Name,$State,$Source,$Title,$Prompt)
  [pscustomobject]@{ name=$Name; state=$State; sourceContext=[pscustomobject]@{ source=$Source }; title=$Title; prompt=$Prompt }
}
$gameSrc = 'sources/github/MasterDD-L34D/Game'
$dbSrc   = 'sources/github/MasterDD-L34D/Game-Database'
$sessions = @(
  (New-FakeSession 'sessions/111' 'IN_PROGRESS' $gameSrc 'harden combat resolve' 'Modify services/combat/resolve.ts only. ASCII only. Acceptance: tests pass.'),
  (New-FakeSession 'sessions/222' 'COMPLETED'   $gameSrc 'old resolve work'       'Touched services/combat/resolve.ts previously.'),
  (New-FakeSession 'sessions/333' 'IN_PROGRESS' $dbSrc   'db schema'              'Modify services/combat/resolve.ts in the DB repo.'),
  (New-FakeSession 'sessions/444' 'AWAITING_USER_FEEDBACK' $gameSrc 'spawn tuning' 'Modify services/ai/spawn.ts only. ASCII only. Acceptance: tests pass.')
)
$ov = Find-ActiveOverlap -Sessions $sessions -Target 'services/combat/resolve.ts' -Source $gameSrc
Assert-True  ($null -ne $ov) 'active overlapping session -> overlap found (MUST abort)'
Assert-Eq    '111' $ov.Id 'overlap is the IN_PROGRESS same-source session 111'
$ovCompleted = Find-ActiveOverlap -Sessions @($sessions[1]) -Target 'services/combat/resolve.ts' -Source $gameSrc
Assert-True  ($null -eq $ovCompleted) 'COMPLETED-only session -> NO overlap (terminal filtered out)'
$ovWrongSrc = Find-ActiveOverlap -Sessions @($sessions[2]) -Target 'services/combat/resolve.ts' -Source $gameSrc
Assert-True  ($null -eq $ovWrongSrc) 'active session on different repo source -> NO overlap'
$ovDistinct = Find-ActiveOverlap -Sessions @($sessions[3]) -Target 'services/combat/resolve.ts' -Source $gameSrc
Assert-True  ($null -eq $ovDistinct) 'active session on a distinct target -> NO overlap'

# ======================================================================
Write-Host "Test 9: Tuning evidence (QG Step 3 -- naive substring vs boundary matcher)"
$collisionText = 'optimize prefetchdata and fetchall caching layer'
$naiveWouldMatch = $collisionText.Contains('fetch')                 # naive .Contains -> TRUE (false-positive)
$boundaryMatches = (Test-TargetOverlap 'fetch.js' $collisionText)   # boundary -> FALSE
Assert-True  $naiveWouldMatch 'naive .Contains(fetch) WOULD false-positive (before)'
Assert-False $boundaryMatches 'boundary matcher does NOT false-positive (after) -- tuning delta'

# ======================================================================
Write-Host ""
Write-Host "Results: $script:passed passed, $script:failed failed"
if ($script:failed -gt 0) {
  Write-Host "Failures:" -ForegroundColor Red
  $script:failures | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
  exit 1
}
exit 0
