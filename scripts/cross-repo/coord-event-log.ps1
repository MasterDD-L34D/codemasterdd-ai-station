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

.PARAMETER ReminderOnly
  Non-interactive mode: write/append a reminder marker file logs/gate-e-reminder-due-YYYY-WW.md
  (week number). NO append to events log. Safe for schtasks (replaces msg.exe absent on Win 11 Home).

.EXAMPLE
  .\coord-event-log.ps1
  (interactive mode, default)

.EXAMPLE
  .\coord-event-log.ps1 -Quiet -NotesQuick "Grep cross-repo for PR status 15min cost"

.EXAMPLE
  .\coord-event-log.ps1 -ReminderOnly
  (schtasks mode: writes logs/gate-e-reminder-due-YYYY-WW.md marker file, exit 0)
#>

param(
  [switch]$Quiet,
  [string]$NotesQuick = "",
  [switch]$ReminderOnly
)

$ErrorActionPreference = 'Stop'

# -ReminderOnly mode: write file marker (safe for schtasks, no msg.exe required)
if ($ReminderOnly) {
  $now = Get-Date
  $weekNum = Get-Date -UFormat "%V"
  $year = $now.ToString("yyyy")
  $timestamp = $now.ToString("yyyy-MM-dd HH:mm")
  $reminderFile = "C:\dev\codemasterdd-ai-station\logs\gate-e-reminder-due-$year-W$weekNum.md"

  $reminderContent = "## Gate E reminder due [$timestamp]`n`n" +
    "Log past week coord events via ``scripts/cross-repo/coord-event-log.ps1``" +
    "`n"

  if (-not (Test-Path "C:\dev\codemasterdd-ai-station\logs")) {
    New-Item -ItemType Directory -Path "C:\dev\codemasterdd-ai-station\logs" -Force | Out-Null
  }

  Add-Content -Path $reminderFile -Value $reminderContent -Encoding UTF8
  Write-Host "PASS: reminder marker written to $reminderFile" -ForegroundColor Green
  exit 0
}

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
