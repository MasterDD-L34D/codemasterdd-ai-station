<#
.SYNOPSIS
Registers the morning-brief Windows scheduled task (idempotent).

.DESCRIPTION
ADR-0044 gap G1 (governor rung R0, report-only). Runs
scripts/fleet/morning-brief.ps1 daily. Unlike jules-daily-digest this task
is SAFE on both PCs (writes only local gitignored logs, no shared artifact),
so no single-owner constraint. No admin elevation (current-user, Limited).
ASCII-first (ADR-0021). Pattern: register-jules-digest-task.ps1.

Usage:
  powershell -NoProfile -ExecutionPolicy Bypass -File register-morning-brief-task.ps1
  powershell -NoProfile -ExecutionPolicy Bypass -File register-morning-brief-task.ps1 -Unregister
#>
[CmdletBinding()]
param(
  [switch]$Unregister,
  [string]$At = '08:30',
  [string]$ScriptPath = 'C:\dev\codemasterdd-ai-station\scripts\fleet\morning-brief.ps1'
)
$ErrorActionPreference = 'Stop'
$taskName = 'morning-brief'

if ($Unregister) {
  $existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
  if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "UNREGISTERED '$taskName' on $env:COMPUTERNAME."
  } else {
    Write-Host "'$taskName' not present on $env:COMPUTERNAME (nothing to do)."
  }
  return
}

if (-not (Test-Path $ScriptPath)) { throw "Brief script not found: $ScriptPath" }

$action    = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -ExecutionPolicy Bypass -File "' + $ScriptPath + '"')
$trigger   = New-ScheduledTaskTrigger -Daily -At $At
$principal = New-ScheduledTaskPrincipal -UserId "$env:COMPUTERNAME\$env:USERNAME" -LogonType Interactive -RunLevel Limited
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -DontStopOnIdleEnd
$desc      = "READ-ONLY morning fleet brief (ADR-0044 G1, governor rung R0). Writes logs/morning-brief/<date>.md (gitignored). Safe on both PCs."

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description $desc -Force | Out-Null

$t = Get-ScheduledTask -TaskName $taskName
Write-Host "REGISTERED '$taskName' on $env:COMPUTERNAME."
Write-Host ("  State    : " + $t.State)
Write-Host ("  Trigger  : daily @ " + (($t.Triggers | Select-Object -First 1).StartBoundary))
Write-Host ("  Action   : " + ($t.Actions | ForEach-Object { $_.Execute + ' ' + $_.Arguments }))
Write-Host "  Verify run-once: Start-ScheduledTask -TaskName '$taskName'; (Get-ScheduledTaskInfo '$taskName').LastTaskResult  # 0 = ok"
