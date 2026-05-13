<#
.SYNOPSIS
  Install schtasks weekly Sunday 09:00 reminder per Gate E logging discipline (spec V3).

.DESCRIPTION
  Crea Windows scheduled task che mostra reminder PowerShell weekly:
  "Gate E checkpoint: log coord events past week or run coord-event-log.ps1".

  Matches pattern esistente backup-api-keys.ps1 + smoke-test-hooks.ps1 (schtasks weekly).

.PARAMETER DryRun
  Print schtasks command but don't execute (for review pre-install).

.PARAMETER Uninstall
  Remove the scheduled task instead of installing.

.EXAMPLE
  .\install-gate-e-reminder.ps1 -DryRun
  .\install-gate-e-reminder.ps1
  .\install-gate-e-reminder.ps1 -Uninstall
#>

param(
  [switch]$DryRun,
  [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'

$taskName = "GateELoggingReminder"
$scriptPath = "C:\dev\codemasterdd-ai-station\scripts\cross-repo\coord-event-log.ps1"

if ($Uninstall) {
  Write-Host "Uninstalling task $taskName..." -ForegroundColor Yellow
  $cmd = "schtasks /Delete /TN $taskName /F"
  if ($DryRun) {
    Write-Host "DRY-RUN: $cmd"
    exit 0
  }
  Invoke-Expression $cmd
  Write-Host "PASS: task removed" -ForegroundColor Green
  exit 0
}

# Install command
# Use msg.exe for simple user-visible popup to avoid nested quote complexity with schtasks /TR
# msg * displays a dialog to the current session user
$reminderText = "Gate E checkpoint: log coord events past week or run scripts/cross-repo/coord-event-log.ps1"
$trAction = "msg %USERNAME% $reminderText"

if ($DryRun) {
  Write-Host "=== DRY-RUN ===" -ForegroundColor Cyan
  Write-Host "Task name: $taskName"
  Write-Host "Schedule: WEEKLY Sunday 09:00"
  Write-Host "Action: msg %USERNAME% popup reminder"
  Write-Host ""
  Write-Host "TR action that would be registered:"
  Write-Host $trAction
  Write-Host ""
  Write-Host "DRY-RUN OK. Run without -DryRun to install." -ForegroundColor Green
  exit 0
}

Write-Host "Installing schtasks $taskName..." -ForegroundColor Cyan
schtasks /Create /SC WEEKLY /D SUN /TN $taskName /TR $trAction /ST 09:00 /F

if ($LASTEXITCODE -eq 0) {
  Write-Host "PASS: task installed" -ForegroundColor Green
  Write-Host "Verify: schtasks /Query /TN $taskName"
  exit 0
} else {
  Write-Host "FAIL: task install failed (exit $LASTEXITCODE)" -ForegroundColor Red
  exit 1
}
