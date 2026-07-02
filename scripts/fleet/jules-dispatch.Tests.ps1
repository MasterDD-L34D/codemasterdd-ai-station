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
$script:results = @()  # tdd-guard PS-reporter: per-assert {name,state} -> test.json at the end

function Assert-True {
  param([bool]$Condition, [string]$Name)
  $script:results += [pscustomobject]@{ name = $Name; state = $(if ($Condition) { 'passed' } else { 'failed' }) }
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
Write-Host "Test 11: Get-SessionId (P1-C POST-response shape guard -- no hollow success)"
$goodResp = [pscustomobject]@{ name = 'sessions/abc123'; state = 'IN_PROGRESS' }
Assert-Eq 'abc123' (Get-SessionId $goodResp) 'well-formed response -> id extracted'
$lroResp = [pscustomobject]@{ operation = [pscustomobject]@{ done = $false } }  # no .name
Assert-True ($null -eq (Get-SessionId $lroResp)) 'shapeless response (no .name) -> null (MAIN must abort, not log hollow success)'
Assert-True ($null -eq (Get-SessionId $null)) 'null response -> null'
$emptyName = [pscustomobject]@{ name = ''; state = 'IN_PROGRESS' }
Assert-True ($null -eq (Get-SessionId $emptyName)) 'empty name -> null'

# ======================================================================
Write-Host "Test 12: Resolve-AuditState (audit-state fallback chain -- never-throw)"
# Empirical (2026-06-03 sid 17389050512450210982): the create-POST returns an EMPTY state; the
# session is actually QUEUED, surfaced only by a follow-up GET /sessions/{id}. So the GET state,
# when present, must win; on GET failure ($null) fall back to the create-state, then to 'UNKNOWN'.
$fetchedQueued = [pscustomobject]@{ name = 'sessions/abc'; state = 'QUEUED' }
Assert-Eq 'QUEUED' (Resolve-AuditState -Fetched $fetchedQueued -CreateState '') 'empty create-state + GET QUEUED -> QUEUED (the fix)'
Assert-Eq 'QUEUED' (Resolve-AuditState -Fetched $fetchedQueued -CreateState 'IN_PROGRESS') 'GET state wins over a present create-state'
Assert-Eq 'IN_PROGRESS' (Resolve-AuditState -Fetched $null -CreateState 'IN_PROGRESS') 'GET failed (null) -> fall back to create-state'
$fetchedBlank = [pscustomobject]@{ name = 'sessions/abc'; state = '   ' }
Assert-Eq 'IN_PROGRESS' (Resolve-AuditState -Fetched $fetchedBlank -CreateState 'IN_PROGRESS') 'GET blank/whitespace state -> fall back to create-state'
$fetchedNoState = [pscustomobject]@{ name = 'sessions/abc' }
Assert-Eq 'IN_PROGRESS' (Resolve-AuditState -Fetched $fetchedNoState -CreateState 'IN_PROGRESS') 'GET shape has no state property -> fall back to create-state'
Assert-Eq 'UNKNOWN' (Resolve-AuditState -Fetched $null -CreateState '') 'GET failed + empty create-state -> UNKNOWN'
Assert-Eq 'UNKNOWN' (Resolve-AuditState -Fetched $null -CreateState $null) 'GET failed + null create-state -> UNKNOWN'
# P2#1 array-safety (harsh-reviewer): Invoke-RestMethod may return Object[]; member-enumeration of
# .state must NOT leak an array into the pipe-delimited audit spine (silent corruption worse than blank).
$fetchedMulti = @([pscustomobject]@{ state = 'QUEUED' }, [pscustomobject]@{ state = 'COMPLETED' })
Assert-True ((Resolve-AuditState -Fetched $fetchedMulti -CreateState '') -is [string]) 'array Fetched -> scalar string (never an array into the audit line)'
Assert-Eq 'QUEUED' (Resolve-AuditState -Fetched $fetchedMulti -CreateState '') 'array Fetched -> first element state (no space-join corruption)'
$fetchedArr1 = @([pscustomobject]@{ state = 'QUEUED' })
Assert-Eq 'QUEUED' (Resolve-AuditState -Fetched $fetchedArr1 -CreateState '') 'single-element array Fetched -> its state'
Assert-Eq 'IN_PROGRESS' (Resolve-AuditState -Fetched $null -CreateState @('IN_PROGRESS','EXTRA')) 'array CreateState -> first element (param not [string]-joined)'
$fetchedScalar = 'oops-not-an-object'
Assert-Eq 'IN_PROGRESS' (Resolve-AuditState -Fetched $fetchedScalar -CreateState 'IN_PROGRESS') 'scalar Fetched (no .state) -> fall back to create-state'

# ======================================================================
Write-Host "Test 13: Add-DispatchConstraints (anti-pollution guard -- skiv 121MB-binary root cause)"
$body13 = Add-DispatchConstraints 'ORIGINAL TASK BODY'
Assert-True ($body13.StartsWith('ORIGINAL TASK BODY')) 'original task content preserved at the start'
Assert-True ($body13 -match 'Do NOT add, create, download, or commit') 'anti-pollution clause present'
Assert-True ($body13 -match 'no engine/SDK/tool downloads') 'engine/binary-download ban present'
Assert-True ($body13.Length -gt 'ORIGINAL TASK BODY'.Length) 'guard appended (output longer than input)'

# ======================================================================
Write-Host "Test 14: Get-AllSessionPages (gate 4 pagination -- walk all pages, fix 2026-06-05)"
# Pure pagination over a fake fetcher (param: pageToken -> {sessions, nextPageToken}). The old
# gate-4 ABORTED on a paginated list (>100 sessions) so dedup could miss an active session on a
# later page (2026-06-05 collision root cause). This walks every page.
$page1 = [pscustomobject]@{ sessions = @('s1', 's2'); nextPageToken = 'P2' }
$page2 = [pscustomobject]@{ sessions = @('s3');       nextPageToken = $null }
$pageMap = @{ '' = $page1; 'P2' = $page2 }
$multiFetch = { param($t) $pageMap[[string]$t] }
$r14 = $null; try { $r14 = Get-AllSessionPages -Fetch $multiFetch } catch {}
Assert-Eq 3 (@($r14.Sessions).Count) 'walks 2 pages -> 3 sessions merged (s1,s2,s3)'
Assert-Eq 2 $r14.Pages '2 pages walked'
Assert-False ([bool]$r14.Truncated) 'followed token to null -> not truncated'
$onlyPage = [pscustomobject]@{ sessions = @('a'); nextPageToken = $null }
$r14b = $null; try { $r14b = Get-AllSessionPages -Fetch { param($t) $onlyPage } } catch {}
Assert-Eq 1 (@($r14b.Sessions).Count) 'single page -> 1 session'
Assert-Eq 1 $r14b.Pages 'single page -> 1 page walked'
$loopPage = [pscustomobject]@{ sessions = @('x'); nextPageToken = 'NEXT' }
$r14c = $null; try { $r14c = Get-AllSessionPages -Fetch { param($t) $loopPage } -MaxPages 3 } catch {}
Assert-Eq 3 $r14c.Pages 'always-token fetcher -> capped at MaxPages=3'
Assert-True ([bool]$r14c.Truncated) 'token still present at cap -> Truncated=true'

# ======================================================================
Write-Host "Test 15: Resolve-TaskFilePath (.NET-CWD independence -- worktree dispatch fix 2026-07-02)"
# [IO.File] resolves RELATIVE paths against the PROCESS CWD, which does NOT follow the PS
# location (Set-Location/Push-Location). Dispatching from a git worktree threw on a TaskFile
# that Test-Path had just validated -- and with a same-named decoy in the process CWD it would
# instead silently READ THE WRONG FILE (gates 2-3 would lint the decoy). Canonicalize first.
$dirA = Join-Path $env:TEMP ("jd-cwd-a-" + [guid]::NewGuid().ToString('N'))
$dirB = Join-Path $env:TEMP ("jd-cwd-b-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $dirA, $dirB | Out-Null
[IO.File]::WriteAllText((Join-Path $dirA 'task.md'), 'REAL task body')
[IO.File]::WriteAllText((Join-Path $dirB 'task.md'), 'DECOY body')
$savedLoc = Get-Location
$savedNet = [Environment]::CurrentDirectory
try {
  Set-Location $dirA                          # PS location = where the operator cd'd
  [Environment]::CurrentDirectory = $dirB     # process CWD = elsewhere (the worktree scenario)
  $resolved = $null; try { $resolved = Resolve-TaskFilePath 'task.md' } catch {}
  Assert-True ($null -ne $resolved) 'relative TaskFile resolves (no throw)'
  Assert-Eq (Join-Path $dirA 'task.md') $resolved 'resolves against the PS location, NOT the process CWD'
  $readBack = if ($resolved) { [IO.File]::ReadAllText($resolved) } else { '' }
  Assert-Eq 'REAL task body' $readBack 'ReadAllText on the resolved path reads the REAL file, not the decoy'
  $abs = $null; try { $abs = Resolve-TaskFilePath (Join-Path $dirA 'task.md') } catch {}
  Assert-Eq (Join-Path $dirA 'task.md') $abs 'absolute path passes through unchanged'
} finally {
  Set-Location $savedLoc
  [Environment]::CurrentDirectory = $savedNet
  Remove-Item $dirA, $dirB -Recurse -Force -ErrorAction SilentlyContinue
}

# ======================================================================
Write-Host ""
Write-Host "Results: $script:passed passed, $script:failed failed"

# --- tdd-guard PowerShell reporter (structural fix for the PS blind-spot) ---
# tdd-guard (npx tdd-guard) ships reporters for pytest/vitest/jest but NOT for hand-rolled
# PowerShell runners, so a PS .Tests.ps1 RED is invisible to the PreToolUse guard, which then
# false-blocks the GREEN implementation (hit 3x on 2026-06-04). Writing results to
# .claude/tdd-guard/data/test.json in the reporter schema lets the guard see PS outcomes.
# Reusable: any *.Tests.ps1 using Assert-True can copy this block.
try {
  $tddDir = Join-Path $PSScriptRoot '..\..\.claude\tdd-guard\data'
  if (Test-Path $tddDir) {
    $moduleId = 'scripts/fleet/jules-dispatch.Tests.ps1'
    $tests = @($script:results | ForEach-Object {
        @{ name = $_.name; fullName = "${moduleId}::$($_.name)"; state = $_.state }
      })
    $report = @{ testModules = @(@{ moduleId = $moduleId; tests = $tests }) }
    [IO.File]::WriteAllText((Join-Path $tddDir 'test.json'), ($report | ConvertTo-Json -Depth 6))
  }
} catch { Write-Host "  (tdd-guard reporter write skipped: $($_.Exception.Message))" }

if ($script:failed -gt 0) {
  Write-Host "Failures:" -ForegroundColor Red
  $script:failures | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
  exit 1
}
exit 0
