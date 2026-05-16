# smoke-test-hooks.ps1 -- Hook integrity smoke test settimanale
#
# BACKLOG M8 (deferred SPRINT_02): verifica empirica che i guard rail commit globali
# bloccano i pattern attesi. Rilevamento drift: hook accidentalmente disinstallato,
# regex commit-msg corrotta, sed/grep non disponibile post-update Git for Windows, ecc.
#
# Hook coperti:
#   - commit-msg globale (ADR-0011 Conventional Commits cross-agent)
#   - pre-commit Layer 1 silent-corruption (ADR-0008)
#   - pre-commit Layer 2 silent-fail Python (ADR-0020)
#
# NON coperti (out of scope M8):
#   - Privacy guard rail wrapper aider-cloud (H8) - testato da scripts/setup/test-privacy-guard.cmd
#   - Stop hook H12 - testato durante uso real-world
#   - PreToolUse commit-guard.js Claude Code - duplica logica commit-msg, smoke implicito qui
#
# Test mode safe: usa $env:TEMP/hook-smoke-$PID scratch repo + git init (eredita core.hooksPath).
# NON tocca repo reale, NON modifica config globale, cleanup garantito via try/finally.
#
# Usage:
#   .\scripts\smoke-test-hooks.ps1                 # full suite, output verbose
#   .\scripts\smoke-test-hooks.ps1 -Quiet          # solo summary PASS/FAIL count
#   .\scripts\smoke-test-hooks.ps1 -ExitOnFail     # exit 1 al primo FAIL (CI-friendly)
#
# Schedule weekly via Windows Task Scheduler:
#   schtasks /Create /SC WEEKLY /D SUN /TN "HookIntegritySmoke" /TR "powershell -File C:\dev\codemasterdd-ai-station\scripts\smoke-test-hooks.ps1 -Quiet" /ST 09:00

[CmdletBinding()]
param(
    [switch]$Quiet,
    [switch]$ExitOnFail
)

# NOTA: ErrorActionPreference resta "Continue" (default).
# In PowerShell 5.1 il redirect 2>&1 di native exe wrappa stderr in ErrorRecord che
# con "Stop" abortisce. Capture stderr via temp file invece (vedi Run-CommitTest).
$scratchRoot = Join-Path $env:TEMP "hook-smoke-$PID"

function Write-TestInfo {
    param([string]$Msg, [string]$Color = "Cyan")
    if (-not $Quiet) { Write-Host $Msg -ForegroundColor $Color }
}

function Setup-ScratchRepo {
    param([string]$Name)
    $path = Join-Path $scratchRoot $Name
    if (Test-Path $path) { Remove-Item -Recurse -Force $path }
    New-Item -ItemType Directory -Force -Path $path | Out-Null
    Push-Location $path
    git init --quiet | Out-Null
    git config user.email "smoke@test.local" | Out-Null
    git config user.name "Hook Smoke" | Out-Null
    Pop-Location
    return $path
}

function Run-CommitTest {
    param(
        [string]$TestName,
        [string]$RepoSlug,           # short slug for scratch dir, 1 repo per test (no staging cross-contamination)
        [hashtable[]]$Files,         # @(@{Name='foo.py'; Content='...'}, ...)
        [string]$CommitMsg,
        [bool]$ExpectBlock           # $true se ci aspettiamo exit non-zero
    )

    $RepoPath = Setup-ScratchRepo $RepoSlug
    Push-Location $RepoPath
    try {
        # Write files
        foreach ($f in $Files) {
            $fpath = Join-Path $RepoPath $f.Name
            $fdir = Split-Path -Parent $fpath
            if (-not (Test-Path $fdir)) {
                New-Item -ItemType Directory -Force -Path $fdir | Out-Null
            }
            # Use UTF8NoBOM encoding to avoid Windows BOM artifacts in test files
            [System.IO.File]::WriteAllText($fpath, $f.Content, [System.Text.UTF8Encoding]::new($false))
            git add $f.Name | Out-Null
        }

        # Try commit. Redirect stderr to temp file (PS5.1 native cmd 2>&1 wraps in ErrorRecord).
        $tmpErr = [System.IO.Path]::GetTempFileName()
        try {
            git commit -m $CommitMsg 2>$tmpErr | Out-Null
            $exitCode = $LASTEXITCODE
            $stderr = (Get-Content $tmpErr -Raw -ErrorAction SilentlyContinue) -as [string]
        } finally {
            Remove-Item $tmpErr -ErrorAction SilentlyContinue
        }

        $blocked = ($exitCode -ne 0)
        $passed = ($blocked -eq $ExpectBlock)

        $verdict = if ($passed) { "PASS" } else { "FAIL" }
        $expected = if ($ExpectBlock) { "BLOCK" } else { "PASS" }
        $actual = if ($blocked) { "BLOCK" } else { "PASS" }

        $color = if ($passed) { "Green" } else { "Red" }
        Write-TestInfo "  [$verdict] $TestName -- expected: $expected, actual: $actual" $color

        if (-not $passed -and -not $Quiet -and $stderr) {
            $stderrSnippet = ($stderr -split "`n" | Select-Object -First 3) -join "`n         "
            Write-Host "         stderr: $stderrSnippet" -ForegroundColor DarkGray
        }

        return $passed
    } finally {
        Pop-Location
    }
}

# ============================================================================
# MAIN
# ============================================================================

Write-TestInfo "smoke-test-hooks -- M8 hook integrity weekly smoke" "Green"
Write-TestInfo "Hook globale: $(git config --global core.hooksPath)" "DarkGray"
Write-TestInfo ""

$results = @{ pass = 0; fail = 0; details = @() }

try {
    # ============================================================================
    # GROUP 1: commit-msg hook (ADR-0011 Conventional Commits)
    # ============================================================================
    Write-TestInfo "Group 1: commit-msg (ADR-0011)" "Yellow"

    # T1: valid Conv Commit -> PASS
    $r = Run-CommitTest -TestName "T1 valid feat() format" -RepoSlug "t1" `
        -Files @(@{Name='a.txt'; Content='hello'}) `
        -CommitMsg 'feat(test): add hello file' -ExpectBlock $false
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    # T2: missing type -> BLOCK
    $r = Run-CommitTest -TestName "T2 missing type prefix" -RepoSlug "t2" `
        -Files @(@{Name='b.txt'; Content='hello'}) `
        -CommitMsg 'just a random commit' -ExpectBlock $true
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    # T3: subject >72 chars -> BLOCK
    $longMsg = 'feat(test): ' + ('x' * 80)
    $r = Run-CommitTest -TestName "T3 subject over 72 chars" -RepoSlug "t3" `
        -Files @(@{Name='c.txt'; Content='hello'}) `
        -CommitMsg $longMsg -ExpectBlock $true
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    # T4: trailing period -> BLOCK
    $r = Run-CommitTest -TestName "T4 trailing period" -RepoSlug "t4" `
        -Files @(@{Name='d.txt'; Content='hello'}) `
        -CommitMsg 'feat(test): valid description.' -ExpectBlock $true
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    # T5: uppercase description -> BLOCK
    $r = Run-CommitTest -TestName "T5 uppercase first letter" -RepoSlug "t5" `
        -Files @(@{Name='e.txt'; Content='hello'}) `
        -CommitMsg 'feat(test): Capitalized description' -ExpectBlock $true
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    Write-TestInfo ""

    # ============================================================================
    # GROUP 2: pre-commit Layer 1 silent-corruption (ADR-0008)
    # ============================================================================
    Write-TestInfo "Group 2: pre-commit silent-corruption (ADR-0008)" "Yellow"

    # T6: file with content = bare filename -> BLOCK
    $r = Run-CommitTest -TestName "T6 file content = filename" -RepoSlug "t6" `
        -Files @(@{Name='foo.py'; Content='foo.py'}) `
        -CommitMsg 'feat(test): add foo' -ExpectBlock $true
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    # T7: file with content = "# filename" -> BLOCK
    $r = Run-CommitTest -TestName "T7 file content = # filename" -RepoSlug "t7" `
        -Files @(@{Name='bar.py'; Content='# bar.py'}) `
        -CommitMsg 'feat(test): add bar' -ExpectBlock $true
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    # T8: normal file content -> PASS
    $r = Run-CommitTest -TestName "T8 normal file content" -RepoSlug "t8" `
        -Files @(@{Name='baz.py'; Content="def hello():`n    return 'world'"}) `
        -CommitMsg 'feat(test): add baz' -ExpectBlock $false
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    Write-TestInfo ""

    # ============================================================================
    # GROUP 3: pre-commit Layer 2 silent-fail Python (ADR-0020)
    # ============================================================================
    Write-TestInfo "Group 3: pre-commit silent-fail Python (ADR-0020)" "Yellow"

    # T9: bare except: -> BLOCK
    $bareExcept = @"
def fetch():
    try:
        return do_thing()
    except:
        return None
"@
    $r = Run-CommitTest -TestName "T9 bare except: clause" -RepoSlug "t9" `
        -Files @(@{Name='svc1.py'; Content=$bareExcept}) `
        -CommitMsg 'feat(test): add svc1' -ExpectBlock $true
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    # T10: except Foo: pass one-liner -> BLOCK
    $exceptPass = @"
def fetch():
    try:
        return do_thing()
    except KeyError: pass
"@
    $r = Run-CommitTest -TestName "T10 except: pass one-liner" -RepoSlug "t10" `
        -Files @(@{Name='svc2.py'; Content=$exceptPass}) `
        -CommitMsg 'feat(test): add svc2' -ExpectBlock $true
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    # T11: bypass marker # silent-ok -> PASS
    $silentOk = @"
def fetch():
    try:
        return do_thing()
    except KeyError: pass  # silent-ok
"@
    $r = Run-CommitTest -TestName "T11 bypass # silent-ok marker" -RepoSlug "t11" `
        -Files @(@{Name='svc3.py'; Content=$silentOk}) `
        -CommitMsg 'feat(test): add svc3' -ExpectBlock $false
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    # T12: normal try/except logged -> PASS
    $normalExcept = @"
import logging
def fetch():
    try:
        return do_thing()
    except KeyError as e:
        logging.error('miss: %s', e)
        return None
"@
    $r = Run-CommitTest -TestName "T12 logged except clause" -RepoSlug "t12" `
        -Files @(@{Name='svc4.py'; Content=$normalExcept}) `
        -CommitMsg 'feat(test): add svc4' -ExpectBlock $false
    if ($r) { $results.pass++ } else { $results.fail++ }
    if (-not $r -and $ExitOnFail) { exit 1 }

    Write-TestInfo ""
} finally {
    # Cleanup scratch root
    if (Test-Path $scratchRoot) {
        Remove-Item -Recurse -Force $scratchRoot -ErrorAction SilentlyContinue
    }
}

# ============================================================================
# REPORT
# ============================================================================
$total = $results.pass + $results.fail
$exitCode = if ($results.fail -gt 0) { 1 } else { 0 }

Write-Host ""
if ($results.fail -eq 0) {
    Write-Host "==> PASS $($results.pass)/$total -- guard rail integrity OK" -ForegroundColor Green
} else {
    Write-Host "==> FAIL $($results.fail)/$total -- guard rail drift detected!" -ForegroundColor Red
    Write-Host "    Investigate: hook content, git config core.hooksPath, sed/grep availability" -ForegroundColor Red
}

exit $exitCode
