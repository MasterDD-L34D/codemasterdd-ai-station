<#
.SYNOPSIS
Registers the sot-drift-ggv2 detector Windows scheduled task (idempotent).

.DESCRIPTION
Runs `py -3 scripts/fleet/sot_drift_ggv2_detect.py` daily on the canonical host
(Lenovo). Polls Game-Godot-v2 merged PRs READ-ONLY, and on a feat() ship that
touches a watched frontend area opens/updates ONE Game issue labelled
sot-drift-candidate-ggv2. The only write is that Game issue. Mirrors
register-governor-ingest-task.ps1.

Auth: needs `gh`. Interactive (default) uses the logged-in gh auth. -Unattended
(S4U, survives logged-off; ELEVATED shell) may lack the user gh auth under the
partial profile -> pass a GitHub token via the GH_TOKEN environment variable for
the task principal, or keep Interactive.

Usage:
  powershell -NoProfile -ExecutionPolicy Bypass -File register-sot-drift-ggv2-task.ps1
  powershell -NoProfile -ExecutionPolicy Bypass -File register-sot-drift-ggv2-task.ps1 -Unattended
  powershell -NoProfile -ExecutionPolicy Bypass -File register-sot-drift-ggv2-task.ps1 -Unregister
#>
[CmdletBinding()]
param(
  [switch]$Unregister,
  [switch]$Unattended,
  [string]$At = '09:00',
  [string]$WorkDir = 'C:\dev\codemasterdd-ai-station'
)
$ErrorActionPreference = 'Stop'
$taskName = 'sot-drift-ggv2'

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

$script = Join-Path $WorkDir 'scripts\fleet\sot_drift_ggv2_detect.py'
if (-not (Test-Path $script)) { throw "detector not found: $script" }

$pyExe = (Get-Command py -ErrorAction SilentlyContinue).Source
if (-not $pyExe) { throw "py launcher not found on $env:COMPUTERNAME" }

$action    = New-ScheduledTaskAction -Execute $pyExe -Argument "-3 scripts\fleet\sot_drift_ggv2_detect.py" -WorkingDirectory $WorkDir
$trigger   = New-ScheduledTaskTrigger -Daily -At $At
$logonType = if ($Unattended) { 'S4U' } else { 'Interactive' }
$principal = New-ScheduledTaskPrincipal -UserId "$env:COMPUTERNAME\$env:USERNAME" -LogonType $logonType -RunLevel Limited
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -DontStopOnIdleEnd
$desc      = "Sovereign SoT-drift detector for Game-Godot-v2 frontend ships. READ-ONLY poll; opens one Game issue (label sot-drift-candidate-ggv2). Verdict + vault reconcile stay human-gated."

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description $desc -Force | Out-Null

$t = Get-ScheduledTask -TaskName $taskName
Write-Host "REGISTERED '$taskName' on $env:COMPUTERNAME."
Write-Host ("  Trigger  : daily @ " + (($t.Triggers | Select-Object -First 1).StartBoundary))
Write-Host ("  Action   : " + ($t.Actions | ForEach-Object { $_.Execute + ' ' + $_.Arguments }))
Write-Host "  Verify run-once: Start-ScheduledTask -TaskName '$taskName'; (Get-ScheduledTaskInfo '$taskName').LastTaskResult  # 0 = ok"
