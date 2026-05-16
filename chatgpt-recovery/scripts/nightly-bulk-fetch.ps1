# nightly-bulk-fetch.ps1 -- Automated nightly ChatGPT bulk fetch routine
#
# Trigger: Windows Task Scheduler daily at 23:00 CET (OpenAI off-peak US hours).
# Behavior: starts brianjlacy --projects-only with focused project filter, runs for
# max 6h or until completion. Auto-stops at 05:00 (avoid running into European morning peak).
#
# Resumable across nightly runs via .export-progress.json.
# Bearer token sourced from %TEMP%\chatgpt-bearer.env (NTFS ACL-protected).
#
# Logs: C:\dev\chatgpt-full-export-2026-05-14\nightly-YYYY-MM-DD.log
#
# Manual run: powershell -ExecutionPolicy Bypass -File nightly-bulk-fetch.ps1
# Stop: Task Scheduler -> "ChatGPT Recovery Nightly Fetch" -> End / Disable

param(
    [int]$MaxHours = 6,
    [string]$ProjectFilter = "g-p-68f5ed3d478c81919fc93c006d63452c",  # Evo-Tactics
    [string]$OutputDir = "C:\dev\chatgpt-full-export-2026-05-14",
    [string]$BearerEnvFile = "$env:TEMP\chatgpt-bearer.env"
)

$ErrorActionPreference = "Continue"
$startTime = Get-Date
$dateStamp = $startTime.ToString("yyyy-MM-dd")
$logFile = Join-Path $OutputDir "nightly-$dateStamp.log"

Write-Host "=== Nightly Bulk Fetch -- $($startTime.ToString('yyyy-MM-dd HH:mm:ss')) ===" -ForegroundColor Cyan

# Verify bearer env-file
if (-not (Test-Path $BearerEnvFile)) {
    $msg = "[$(Get-Date)] ABORT: bearer env-file missing at $BearerEnvFile. Eduardo needs to refresh token + recreate the file."
    Write-Host $msg -ForegroundColor Red
    Add-Content -Path $logFile -Value $msg
    exit 1
}

# Load bearer + account-id from env-file
Get-Content $BearerEnvFile | ForEach-Object {
    if ($_ -match '^([^=]+)=(.+)$') {
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    }
}

if (-not $env:CHATGPT_BEARER_TOKEN) {
    $msg = "[$(Get-Date)] ABORT: CHATGPT_BEARER_TOKEN not set after env-file load"
    Write-Host $msg -ForegroundColor Red
    Add-Content -Path $logFile -Value $msg
    exit 1
}

# Quick pre-flight: verify bearer still valid via /backend-api/me
Write-Host "Pre-flight: verifying bearer token..." -ForegroundColor Yellow
try {
    $h = @{
        "Authorization" = "Bearer $env:CHATGPT_BEARER_TOKEN"
        "Accept"        = "application/json"
    }
    if ($env:CHATGPT_ACCOUNT_ID) {
        $h["chatgpt-account-id"] = $env:CHATGPT_ACCOUNT_ID
    }
    $r = Invoke-WebRequest -Uri "https://chatgpt.com/backend-api/me" -Headers $h -Method GET -UseBasicParsing -TimeoutSec 30
    if ($r.StatusCode -ne 200) {
        throw "HTTP $($r.StatusCode)"
    }
    Write-Host "  Bearer valid (HTTP 200)" -ForegroundColor Green
} catch {
    $msg = "[$(Get-Date)] ABORT: bearer pre-flight failed ($($_.Exception.Message)). Token may be expired or rate-limited."
    Write-Host $msg -ForegroundColor Red
    Add-Content -Path $logFile -Value $msg
    exit 1
}

# Compute deadline (NOW + MaxHours OR 05:00 next day, whichever comes first)
$deadlineByHours = $startTime.AddHours($MaxHours)
$tomorrow5am = $startTime.Date.AddDays(1).AddHours(5)
$deadline = if ($deadlineByHours -lt $tomorrow5am) { $deadlineByHours } else { $tomorrow5am }
$durationMin = ($deadline - $startTime).TotalMinutes
Write-Host "Run window: until $($deadline.ToString('HH:mm')) ($([math]::Round($durationMin)) min)" -ForegroundColor Yellow

Add-Content -Path $logFile -Value "[$(Get-Date)] === START nightly fetch (deadline: $deadline) ==="

# Launch brianjlacy as a child process with timeout enforcement
$brianjlacyDir = "C:\dev\export-chatgpt"
if (-not (Test-Path $brianjlacyDir)) {
    $msg = "[$(Get-Date)] ABORT: $brianjlacyDir not found"
    Add-Content -Path $logFile -Value $msg
    exit 1
}

Push-Location $brianjlacyDir
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "cmd.exe"
$psi.Arguments = "/c npx export-chatgpt --projects-only --proj $ProjectFilter --throttle 30 --no-adaptive-throttle --no-user-dir --output `"$OutputDir`" --verbose >> `"$logFile`" 2>&1"
$psi.UseShellExecute = $false
$psi.WorkingDirectory = $brianjlacyDir
$psi.RedirectStandardOutput = $false
$psi.RedirectStandardError = $false

try {
    $proc = [System.Diagnostics.Process]::Start($psi)
    Write-Host "Started brianjlacy PID $($proc.Id)" -ForegroundColor Green
    Add-Content -Path $logFile -Value "[$(Get-Date)] brianjlacy PID $($proc.Id) launched"

    # Wait until deadline or process exits naturally
    while (-not $proc.HasExited) {
        if ((Get-Date) -ge $deadline) {
            Write-Host "Deadline reached, terminating brianjlacy..." -ForegroundColor Yellow
            Add-Content -Path $logFile -Value "[$(Get-Date)] DEADLINE reached, killing PID $($proc.Id)"
            try {
                $proc.Kill()
                $proc.WaitForExit(30000)
            } catch {
                Write-Host "Kill error: $_" -ForegroundColor Red
            }
            break
        }
        Start-Sleep -Seconds 60
    }

    if ($proc.HasExited) {
        Add-Content -Path $logFile -Value "[$(Get-Date)] brianjlacy exited with code $($proc.ExitCode)"
    }
} catch {
    Add-Content -Path $logFile -Value "[$(Get-Date)] ERROR launching brianjlacy: $($_.Exception.Message)"
    Write-Host "Error: $_" -ForegroundColor Red
} finally {
    Pop-Location
}

# Post-run snapshot
$endTime = Get-Date
$projDir = Join-Path $OutputDir "projects\Progetto_Gioco_Evo_Tactics\json"
$convCount = if (Test-Path $projDir) {
    (Get-ChildItem $projDir -Filter "*.json" -ErrorAction SilentlyContinue | Measure-Object).Count
} else { 0 }

$summary = "[$(Get-Date)] === END nightly fetch | duration: $([math]::Round(($endTime - $startTime).TotalMinutes)) min | Evo-Tactics conv on disk: $convCount/541 ==="
Write-Host $summary -ForegroundColor Cyan
Add-Content -Path $logFile -Value $summary

# Log rotation: keep last 14 days
Get-ChildItem $OutputDir -Filter "nightly-*.log" -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-14) } |
    Remove-Item -Force -ErrorAction SilentlyContinue
