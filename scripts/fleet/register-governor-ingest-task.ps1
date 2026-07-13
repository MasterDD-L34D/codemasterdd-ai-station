<#
.SYNOPSIS
Registers the governor-ingest Windows scheduled task (idempotent).

.DESCRIPTION
Keeps the fleet governor R0 signal pane (/cross-repo/governor) fresh: runs
`py -3 -m governor.ingest` daily, which re-fetches the 9 GitHub-hosted signal
sources into the CANONICAL governor.db the dashboard reads. Report-only (R0),
no outward action, writes only the local gitignored governor.db. ASCII-first
(ADR-0021). Pattern mirrors register-morning-brief-task.ps1.

-Unattended registers with LogonType S4U ("run whether the user is logged on or
not", no stored password) instead of Interactive, so an 08:45 task is not skipped
(0x800710E0) when the PC is booted but nobody is signed in. RECOMMENDED for the
real daily task; S4U registration needs an ELEVATED shell. Caveat: under S4U the
user profile is only partially loaded, so `gh auth` MAY be unavailable -> the
auth-only sources (vault/evo/archon contents API) can error and are skipped
(ingest_all is per-source fault-tolerant); the public raw sources still refresh.

Usage:
  powershell -NoProfile -ExecutionPolicy Bypass -File register-governor-ingest-task.ps1              # Interactive (only if you stay logged in)
  powershell -NoProfile -ExecutionPolicy Bypass -File register-governor-ingest-task.ps1 -Unattended  # S4U, survives logged-off (elevated shell)
  powershell -NoProfile -ExecutionPolicy Bypass -File register-governor-ingest-task.ps1 -Unregister
#>
[CmdletBinding()]
param(
  [switch]$Unregister,
  [switch]$Unattended,
  [string]$At = '08:45',
  [string]$WorkDir = 'C:\dev\codemasterdd-ai-station\apps\cross-repo-dashboard'
)
$ErrorActionPreference = 'Stop'
$taskName = 'governor-ingest'

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

if (-not (Test-Path (Join-Path $WorkDir 'governor'))) { throw "governor package not found under: $WorkDir" }

# Resolve the FULL path to the py launcher: under the scheduled-task principal the
# user-local Launcher dir is not on PATH, so a bare 'py.exe' fails 0x80070002. Do NOT
# use bare 'python' -- on this fleet it resolves to a hermes venv without the app deps.
$pyExe = (Get-Command py -ErrorAction SilentlyContinue).Source
if (-not $pyExe) { throw "py launcher not found on $env:COMPUTERNAME (need Python launcher for 'py -3')" }

$action    = New-ScheduledTaskAction -Execute $pyExe -Argument '-3 -m governor.ingest' -WorkingDirectory $WorkDir
$trigger   = New-ScheduledTaskTrigger -Daily -At $At
$logonType = if ($Unattended) { 'S4U' } else { 'Interactive' }
$principal = New-ScheduledTaskPrincipal -UserId "$env:COMPUTERNAME\$env:USERNAME" -LogonType $logonType -RunLevel Limited
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -DontStopOnIdleEnd
$desc      = "READ-ONLY governor R0 signal ingest. Re-fetches 9 fleet signal sources into governor.db (gitignored). Report-only, safe on both PCs."

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description $desc -Force | Out-Null

$t = Get-ScheduledTask -TaskName $taskName
Write-Host "REGISTERED '$taskName' on $env:COMPUTERNAME."
Write-Host ("  State    : " + $t.State)
Write-Host ("  Trigger  : daily @ " + (($t.Triggers | Select-Object -First 1).StartBoundary))
Write-Host ("  Action   : " + ($t.Actions | ForEach-Object { $_.Execute + ' ' + $_.Arguments }))
Write-Host "  Verify run-once: Start-ScheduledTask -TaskName '$taskName'; (Get-ScheduledTaskInfo '$taskName').LastTaskResult  # 0 = ok"
