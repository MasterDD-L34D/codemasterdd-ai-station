<#
.SYNOPSIS
Registers the jules-daily-digest Windows scheduled task.

.DESCRIPTION
This script registers the jules-daily-digest Windows scheduled task on Ryzen, idempotently.
#>
# register-jules-digest-task.ps1 -- idempotent (un)register of the daily
# Jules digest Windows Scheduled Task. Cross-fleet, single-owner.
#
# G3 (2026-06-03): the digest enumerator (scripts/jules-daily-digest.ps1,
# READ-ONLY, v4.1) must run daily. This script registers / unregisters the
# scheduled task that runs it. ASCII-first (ADR-0021).
#
# OWNERSHIP = SINGLE-OWNER, NOT both PCs. Both clones writing the same-name
# docs/jules-batch/<day>-digest.md = cross-fleet drift (two divergent working
# trees + double commits). Owner today = Ryzen (DESKTOP-T77TMKT). To hand off
# to Lenovo: run this with -Unregister on the current owner FIRST, then run it
# (register) on the new owner. Never leave it registered on two PCs.
#
# Prereq on the owner PC: JULES_API_KEY in ~/.config/api-keys/keys.env + gh
# authed (the PR-state 2-source signal; without gh the digest still runs but
# verdicts degrade to AMBIGUOUS). No admin elevation needed (current-user,
# Limited run-level).
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File register-jules-digest-task.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File register-jules-digest-task.ps1 -Unregister
[CmdletBinding()]
param(
  [switch]$Unregister,
  [string]$At = '09:30',
  [string]$ScriptPath = 'C:\dev\codemasterdd-ai-station\scripts\jules-daily-digest.ps1'
)
$ErrorActionPreference = 'Stop'
$taskName = 'jules-daily-digest'

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

if (-not (Test-Path $ScriptPath)) { throw "Digest script not found: $ScriptPath" }

$action    = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -ExecutionPolicy Bypass -File "' + $ScriptPath + '"')
$trigger   = New-ScheduledTaskTrigger -Daily -At $At
$principal = New-ScheduledTaskPrincipal -UserId "$env:COMPUTERNAME\$env:USERNAME" -LogonType Interactive -RunLevel Limited
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 15) -DontStopOnIdleEnd
$desc      = "READ-ONLY Jules sessions digest (ADR-0034 Option D, heuristic v4.1). Writes docs/jules-batch/<day>-digest.md. Single-owner cross-fleet (G3)."

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description $desc -Force | Out-Null

$t = Get-ScheduledTask -TaskName $taskName
Write-Host "REGISTERED '$taskName' on $env:COMPUTERNAME (single-owner)."
Write-Host ("  State    : " + $t.State)
Write-Host ("  Trigger  : daily @ " + (($t.Triggers | Select-Object -First 1).StartBoundary))
Write-Host ("  Action   : " + ($t.Actions | ForEach-Object { $_.Execute + ' ' + $_.Arguments }))
Write-Host ("  Principal: " + $t.Principal.UserId + " / " + $t.Principal.LogonType + " / " + $t.Principal.RunLevel)
Write-Host "  Verify run-once: Start-ScheduledTask -TaskName '$taskName'; (Get-ScheduledTaskInfo '$taskName').LastTaskResult  # 0 = ok"
