# register-nightly-task.ps1 -- Register Windows Task Scheduler entry for nightly fetch.
#
# Creates daily task "ChatGPT Recovery Nightly Fetch" at 23:00 CET.
# Wakes computer if sleeping. Stops at 06:00 if still running.
#
# Run ONCE as Administrator:
#   powershell -ExecutionPolicy Bypass -File register-nightly-task.ps1
#
# Verify:
#   schtasks /Query /TN "ChatGPT Recovery Nightly Fetch"
#
# Manual trigger:
#   schtasks /Run /TN "ChatGPT Recovery Nightly Fetch"
#
# Stop/disable:
#   schtasks /Change /TN "ChatGPT Recovery Nightly Fetch" /DISABLE
#   schtasks /Delete /TN "ChatGPT Recovery Nightly Fetch" /F

$taskName = "ChatGPT Recovery Nightly Fetch"
$scriptPath = "C:\dev\codemasterdd-ai-station\.claude\worktrees\affectionate-easley-a43479\chatgpt-recovery\scripts\nightly-bulk-fetch.ps1"

if (-not (Test-Path $scriptPath)) {
    Write-Error "Script not found: $scriptPath"
    exit 1
}

# Check admin elevation
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Warning "Not running as Administrator. Task Scheduler may refuse to register or wake-from-sleep feature won't work."
    Write-Host "Re-run as admin: Start-Process powershell -Verb RunAs -ArgumentList '-ExecutionPolicy Bypass -File `"$PSCommandPath`"'"
}

# Build Action: run wrapper script
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" `
    -WorkingDirectory "C:\dev\codemasterdd-ai-station\.claude\worktrees\affectionate-easley-a43479\chatgpt-recovery\scripts"

# Trigger: daily at 23:00
$trigger = New-ScheduledTaskTrigger -Daily -At "23:00"

# Settings: wake computer, kill after 7h, run only if network available
$settings = New-ScheduledTaskSettingsSet `
    -WakeToRun `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 7) `
    -RestartCount 0 `
    -DontStopOnIdleEnd `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

# Principal: current user, run with highest available privileges (no SYSTEM to keep user env)
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Limited

# Build + register task
$task = New-ScheduledTask `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Nightly resume of brianjlacy/export-chatgpt for Evo-Tactics ChatGPT recovery. Runs at 23:00 CET (OpenAI off-peak), max 6h, auto-stops at 05:00."

try {
    # Delete existing if present
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

    Register-ScheduledTask -TaskName $taskName -InputObject $task | Out-Null
    Write-Host "[OK] Task registered: $taskName" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next run: $((Get-ScheduledTask -TaskName $taskName).Triggers[0].StartBoundary) (daily 23:00)"
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  schtasks /Query /TN `"$taskName`""
    Write-Host "  schtasks /Run /TN `"$taskName`"        # manual trigger"
    Write-Host "  schtasks /Change /TN `"$taskName`" /DISABLE   # temp disable"
    Write-Host "  schtasks /Delete /TN `"$taskName`" /F  # remove"
} catch {
    Write-Error "Failed to register task: $($_.Exception.Message)"
    Write-Host ""
    Write-Host "Fallback: register via schtasks CLI:"
    Write-Host "  schtasks /Create /SC DAILY /ST 23:00 /TN `"$taskName`" /TR `"powershell.exe -NoProfile -ExecutionPolicy Bypass -File '$scriptPath'`" /F"
    exit 1
}
