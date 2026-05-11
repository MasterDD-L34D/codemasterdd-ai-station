# governance-lint.ps1 -- Read-only drift detection per governance docs codemasterdd
#
# Source: cherry-pick concept da vault-shared sibling-peer `production/agents/vault-linter.md`
# (sovereign-only, NO commit hash citato per drift risk).
# Audit-then-replay 2026-05-12 (AA01 task aa01-001-2026-05-11-vault-integration-readonly Pattern C ADOPT).
#
# Scope MVP: 3 check categories (CHECK-1 COMPACT HEAD sync, CHECK-2 Coda PR claim, CHECK-3 JOURNAL stale)
# Output: logs/governance-lint-YYYY-MM-DD.md (read-only report, gitignored via logs/*)
# Schedule: weekly via schtask GovernanceLintWeekly (Saturday 09:00, future install)
#
# Usage:
#   pwsh scripts/governance-lint.ps1                  # report to logs/
#   pwsh scripts/governance-lint.ps1 -Quiet           # only writes file, no stdout
#   pwsh scripts/governance-lint.ps1 -OutputStdout    # report to stdout, no file write
#
# Constraints respected:
# - READ-ONLY (no write/edit su file controllati, output solo in logs/)
# - NO LLM (PowerShell native + git + gh, allinea con vault routing read_only_lint: python_local)
# - NO bulk import vault (concept replay, implementation PowerShell-native)

param(
    [switch]$Quiet,
    [switch]$OutputStdout
)

$ErrorActionPreference = 'Stop'

# Resolve repo root (script can be invoked from any cwd)
$RepoRoot = git rev-parse --show-toplevel 2>$null
if (-not $RepoRoot) {
    Write-Error "Not in a git repo. Run from codemasterdd-ai-station worktree."
    exit 1
}

$ReportDate = Get-Date -Format "yyyy-MM-dd"
$ReportTime = Get-Date -Format "yyyy-MM-dd HH:mm"
$LogDir = Join-Path $RepoRoot "logs"
$LogFile = Join-Path $LogDir "governance-lint-$ReportDate.md"

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# Findings accumulator
$Findings = @()
$AllClear = @()

# ----------------------------------------------------------------------------
# CHECK-1: COMPACT_CONTEXT.md HEAD claim vs origin/main reality
# ----------------------------------------------------------------------------
$CompactPath = Join-Path $RepoRoot "COMPACT_CONTEXT.md"
if (Test-Path $CompactPath) {
    $CompactContent = Get-Content $CompactPath -Raw
    # Match pattern: HEAD origin/main `<sha>` (7+ hex chars, backtick delimited)
    if ($CompactContent -match "HEAD\s+origin/main\s+``([a-f0-9]{7,})``") {
        $ClaimedHead = $Matches[1]
        $RealHead = (git rev-parse --short=7 origin/main 2>$null).Trim()
        if ($ClaimedHead -ne $RealHead) {
            # Count lag commits
            $LagCountStr = (git rev-list --count "$ClaimedHead..origin/main" 2>$null)
            $LagCount = if ($LagCountStr) { [int]$LagCountStr } else { -1 }

            # Threshold: lag == 1 is expected post-merge (COMPACT mentions pre-merge HEAD,
            # squash-merge creates new SHA = +1). Only lag > 1 indicates real drift.
            if ($LagCount -eq 1) {
                $AllClear += "CHECK-1 COMPACT HEAD sync: lag=1 expected post-merge (claim ``$ClaimedHead``, reality ``$RealHead``)"
            } else {
                $LagDisplay = if ($LagCount -lt 0) { "?" } else { "$LagCount" }
                $Findings += @{
                    Id = "CHECK-1"
                    Severity = "WARNING"
                    Title = "COMPACT_CONTEXT.md HEAD claim drift"
                    Detail = "Claim: ``$ClaimedHead`` | Reality: ``$RealHead`` | Lag: $LagDisplay commit(s) (threshold WARNING: >1)"
                    Action = "Refresh COMPACT version + update HEAD line."
                }
            }
        } else {
            $AllClear += "CHECK-1 COMPACT HEAD sync: claim and reality match (``$RealHead``)"
        }
    } else {
        $Findings += @{
            Id = "CHECK-1"
            Severity = "INFO"
            Title = "COMPACT_CONTEXT.md HEAD claim not found"
            Detail = "Pattern 'HEAD origin/main ``<sha>``' non rilevato in COMPACT. Schema cambiato?"
            Action = "Verify COMPACT structure or update regex pattern in script."
        }
    }
} else {
    $Findings += @{
        Id = "CHECK-1"
        Severity = "INFO"
        Title = "COMPACT_CONTEXT.md missing"
        Detail = "File assente. Skip check."
        Action = "Create COMPACT_CONTEXT.md if governance schema requires it."
    }
}

# ----------------------------------------------------------------------------
# CHECK-2: COMPACT Coda PR claim consistency vs `gh pr list`
# ----------------------------------------------------------------------------
if (Test-Path $CompactPath) {
    $CompactContent = Get-Content $CompactPath -Raw
    # Match: "Coda PR codemasterdd: VUOTA" or "Coda PR codemasterdd: N PR"
    if ($CompactContent -match "Coda PR codemasterdd[^.]*?(VUOTA|(\d+)\s*PR)") {
        $ClaimedState = $Matches[1]
        $RealCount = 0
        try {
            $PrList = gh pr list --state open --json number 2>$null | ConvertFrom-Json
            if ($PrList) { $RealCount = @($PrList).Count }
        } catch {
            $RealCount = -1  # gh unavailable
        }

        if ($RealCount -eq -1) {
            $Findings += @{
                Id = "CHECK-2"
                Severity = "INFO"
                Title = "Coda PR check skipped"
                Detail = "gh CLI non disponibile o errore API."
                Action = "Install gh and authenticate, or skip this check."
            }
        } elseif ($ClaimedState -eq "VUOTA" -and $RealCount -gt 0) {
            $Findings += @{
                Id = "CHECK-2"
                Severity = "WARNING"
                Title = "Coda PR claim 'VUOTA' but $RealCount PR open"
                Detail = "COMPACT dichiara coda VUOTA. ``gh pr list`` mostra $RealCount PR open."
                Action = "Update COMPACT Coda PR section."
            }
        } elseif ($ClaimedState -ne "VUOTA" -and $Matches[2]) {
            $ClaimedNum = [int]$Matches[2]
            if ($ClaimedNum -ne $RealCount) {
                $Findings += @{
                    Id = "CHECK-2"
                    Severity = "WARNING"
                    Title = "Coda PR count drift"
                    Detail = "Claim: $ClaimedNum PR | Reality: $RealCount PR"
                    Action = "Update COMPACT Coda PR count."
                }
            } else {
                $AllClear += "CHECK-2 Coda PR sync: $RealCount PR open match"
            }
        } else {
            $AllClear += "CHECK-2 Coda PR VUOTA confermata (0 PR open)"
        }
    } else {
        $Findings += @{
            Id = "CHECK-2"
            Severity = "INFO"
            Title = "Coda PR claim not found in COMPACT"
            Detail = "Pattern 'Coda PR codemasterdd: VUOTA|N PR' non rilevato."
            Action = "Update regex pattern if COMPACT schema changed."
        }
    }
}

# ----------------------------------------------------------------------------
# CHECK-3: JOURNAL.md last entry stale (>14gg)
# ----------------------------------------------------------------------------
$JournalPath = Join-Path $RepoRoot "JOURNAL.md"
if (Test-Path $JournalPath) {
    $JournalContent = Get-Content $JournalPath
    # Find last entry pattern: "## YYYY-MM-DD" (h2 with ISO date)
    # JOURNAL.md is append-only (oldest first, newest last) -- take LAST match for most recent entry
    $LastEntry = $JournalContent | Where-Object { $_ -match "^##\s+(\d{4}-\d{2}-\d{2})" } | Select-Object -Last 1
    if ($LastEntry -and $LastEntry -match "^##\s+(\d{4}-\d{2}-\d{2})") {
        $LastDateStr = $Matches[1]
        try {
            $LastDate = [DateTime]::ParseExact($LastDateStr, "yyyy-MM-dd", $null)
            $DaysSince = (Get-Date) - $LastDate
            $DaysGap = [int]$DaysSince.TotalDays

            if ($DaysGap -gt 14) {
                $Findings += @{
                    Id = "CHECK-3"
                    Severity = "WARNING"
                    Title = "JOURNAL.md stale ($DaysGap days)"
                    Detail = "Last entry: $LastDateStr | Today: $($ReportDate) | Gap: $DaysGap gg (threshold 14gg)"
                    Action = "Add JOURNAL entry for recent sessions or close session ritual."
                }
            } else {
                $AllClear += "CHECK-3 JOURNAL freshness: last entry $LastDateStr ($DaysGap gg ago, within 14gg threshold)"
            }
        } catch {
            $Findings += @{
                Id = "CHECK-3"
                Severity = "INFO"
                Title = "JOURNAL date parse error"
                Detail = "Last entry date '$LastDateStr' non parsabile come yyyy-MM-dd."
                Action = "Verify JOURNAL date format."
            }
        }
    } else {
        $Findings += @{
            Id = "CHECK-3"
            Severity = "INFO"
            Title = "JOURNAL entries not found"
            Detail = "Nessuna entry pattern '## YYYY-MM-DD' in JOURNAL.md."
            Action = "Verify JOURNAL schema or update regex pattern."
        }
    }
} else {
    $Findings += @{
        Id = "CHECK-3"
        Severity = "INFO"
        Title = "JOURNAL.md missing"
        Detail = "File assente. Skip check."
        Action = "Create JOURNAL.md if governance schema requires it."
    }
}

# ----------------------------------------------------------------------------
# Render report
# ----------------------------------------------------------------------------
$CriticalCount = @($Findings | Where-Object { $_.Severity -eq "CRITICAL" }).Count
$WarningCount = @($Findings | Where-Object { $_.Severity -eq "WARNING" }).Count
$InfoCount = @($Findings | Where-Object { $_.Severity -eq "INFO" }).Count

$ReportLines = @()
$ReportLines += "# Governance lint report -- $ReportTime"
$ReportLines += ""
$ReportLines += "**Source**: cherry-pick concept vault-shared ``production/agents/vault-linter.md`` (audit-then-replay PowerShell-native, Pattern C ADOPT 2026-05-12)."
$ReportLines += ""
$ReportLines += "## Summary"
$ReportLines += "- Checks run: 3 (MVP)"
$ReportLines += "- Findings: $($Findings.Count) ($CriticalCount critical / $WarningCount warning / $InfoCount info)"
$ReportLines += "- All-clear: $($AllClear.Count)"
$ReportLines += ""

if ($Findings.Count -gt 0) {
    $ReportLines += "## Findings"
    $ReportLines += ""
    foreach ($f in $Findings) {
        $ReportLines += "### [$($f.Id)] $($f.Severity) -- $($f.Title)"
        $ReportLines += ""
        $ReportLines += $f.Detail
        $ReportLines += ""
        $ReportLines += "**Action**: $($f.Action)"
        $ReportLines += ""
    }
}

if ($AllClear.Count -gt 0) {
    $ReportLines += "## All-clear checks"
    $ReportLines += ""
    foreach ($a in $AllClear) {
        $ReportLines += "- [x] $a"
    }
    $ReportLines += ""
}

$ReportLines += "## MVP scope"
$ReportLines += ""
$ReportLines += "Questa run copre 3 check categories (CHECK-1 COMPACT HEAD sync, CHECK-2 Coda PR claim, CHECK-3 JOURNAL stale)."
$ReportLines += "Three Strikes monitor durante SPRINT_03: se MVP value confermato + 3+ drift detection PASS reali in 30gg -> expand checks 4-7 (markdown links, OD-ADR cross-ref, ADR Proposed age, worktree orphan)."
$ReportLines += ""

$Report = $ReportLines -join "`r`n"

# Output
if ($OutputStdout) {
    Write-Output $Report
} else {
    Set-Content -Path $LogFile -Value $Report -Encoding UTF8
    if (-not $Quiet) {
        Write-Host "Governance lint report written to: $LogFile"
        Write-Host "Summary: $($Findings.Count) findings ($CriticalCount critical / $WarningCount warning / $InfoCount info), $($AllClear.Count) all-clear."
        if ($Findings.Count -gt 0) {
            Write-Host ""
            Write-Host "Findings preview:" -ForegroundColor Yellow
            foreach ($f in $Findings) {
                Write-Host "  [$($f.Id)] $($f.Severity): $($f.Title)" -ForegroundColor Yellow
            }
        }
    }
}

# Exit code: 0 if no warnings/critical, 1 if warnings, 2 if critical
if ($CriticalCount -gt 0) {
    exit 2
} elseif ($WarningCount -gt 0) {
    exit 1
} else {
    exit 0
}
