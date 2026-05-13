<#
.SYNOPSIS
  Helper interactive script per logging missed-coordination events (Gate E spec V3).

.DESCRIPTION
  Prompts Eduardo per evento details + appends row a logs/coord-events-YYYY-MM.md.
  Auto-detects current month + creates file from template if not exists.
  Anti-L-016 discipline: questo script E' la riduzione di friction per logging.

.PARAMETER Quiet
  Skip interactive prompts, append only timestamp + Notes from parameter (for cron/scripted use).

.PARAMETER NotesQuick
  Use with -Quiet for one-line entry.

.EXAMPLE
  .\coord-event-log.ps1
  (interactive mode, default)

.EXAMPLE
  .\coord-event-log.ps1 -Quiet -NotesQuick "Grep cross-repo for PR status 15min cost"
#>

param(
  [switch]$Quiet,
  [string]$NotesQuick = ""
)

$ErrorActionPreference = 'Stop'

$today = Get-Date -Format "yyyy-MM-dd"
$month = Get-Date -Format "yyyy-MM"
$logFile = "C:\dev\codemasterdd-ai-station\logs\coord-events-$month.md"

# Create file if not exists with template header
if (-not (Test-Path $logFile)) {
  $header = @"
# Coord events tracking $month (Gate E spec V3)

> Anti-L-016 discipline. Helper: ``scripts/cross-repo/coord-event-log.ps1``.

## Weekly summary

| Week start | Events count | Avg severity | Total cost (min) | Threshold? |
|------------|--------------|--------------|------------------|------------|
| 2026-MM-DD | 0 | - | 0 | - |

## Events log

| Date | Time | Severity (1-5) | Type | Repos grepped | Cost (min) | Notes |
|------|------|----------------|------|---------------|------------|-------|

"@
  Set-Content -Path $logFile -Value $header -Encoding UTF8
  Write-Host "Created new log file: $logFile" -ForegroundColor Cyan
}

# Gather event details
$time = Get-Date -Format "HH:mm"

if ($Quiet) {
  if (-not $NotesQuick) {
    Write-Host "FAIL: -Quiet requires -NotesQuick" -ForegroundColor Red
    exit 1
  }
  $severity = 3
  $eventType = "manual-quick"
  $reposGrepped = "N/A"
  $costMin = 5
  $notes = $NotesQuick
} else {
  Write-Host "=== Log new coord event ===" -ForegroundColor Cyan
  Write-Host "Date: $today $time"
  Write-Host ""

  $severity = Read-Host "Severity 1-5 (1=trivial, 5=blocking)"
  if ($severity -notmatch '^[1-5]$') { Write-Host "Invalid severity, default 3"; $severity = 3 }

  Write-Host ""
  Write-Host "Event type:"
  Write-Host "  1) grep-manual-cross-repo (>3 location lookup)"
  Write-Host "  2) policy-drift-discovered (rework >30min)"
  Write-Host "  3) cross-repo-roundtrip (>2 RT for single decision)"
  Write-Host "  4) other"
  $typeChoice = Read-Host "Choice 1-4"
  $eventType = switch ($typeChoice) {
    '1' { 'grep-manual' }
    '2' { 'policy-drift' }
    '3' { 'cross-repo-roundtrip' }
    '4' { 'other' }
    default { 'other' }
  }

  $reposGrepped = Read-Host "Repos involved (comma-sep, es. Game,Godot-v2,vault)"
  $costMin = Read-Host "Cost in minutes (estimate)"
  if ($costMin -notmatch '^\d+$') { $costMin = 0 }
  $notes = Read-Host "One-line notes"
}

# Append entry
$row = "| $today | $time | $severity | $eventType | $reposGrepped | $costMin | $notes |"
Add-Content -Path $logFile -Value $row -Encoding UTF8

Write-Host ""
Write-Host "PASS: Event logged to $logFile" -ForegroundColor Green
Write-Host "Row: $row"
exit 0
