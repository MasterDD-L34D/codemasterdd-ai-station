<#
.SYNOPSIS
    Avvia la dashboard dogfood-ui con waitress (production WSGI).
.DESCRIPTION
    Sourcing sicuro da keys.env + avvio waitress su 127.0.0.1:8080.
    Logga a file timestampato in Extras/dashboard-logs/.
.PARAMETER Action
    start (default), stop, restart, status
.PARAMETER Port
    Porta HTTP (default 8080)
.PARAMETER EnvFile
    Path al file chiavi (default ~/.config/api-keys/keys.env)
#>

param(
    [ValidateSet("start", "stop", "restart", "status")]
    [string]$Action = "start",
    [int]$Port = 8080,
    [string]$EnvFile = "$env:USERPROFILE\.config\api-keys\keys.env",
    [string]$FlaskSecret = $env:FLASK_SECRET
)

$RepoRoot = (Resolve-Path -LiteralPath (Join-Path -Path $PSScriptRoot -ChildPath "..\..")).Path
$AppDir = Join-Path -Path $RepoRoot -ChildPath "apps\dogfood-ui"
$LogDir = Join-Path -Path $RepoRoot -ChildPath "Extras\dashboard-logs"
$PidFile = "$env:TEMP\dogfood-dashboard.pid"

if (-not (Test-Path -LiteralPath $AppDir)) {
    Write-Error "AppDir non trovato: $AppDir"
    exit 1
}

if (-not (Test-Path -LiteralPath $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

function Get-PidValue {
    if (Test-Path -LiteralPath $PidFile) {
        $val = Get-Content -LiteralPath $PidFile -Raw
        $intVal = 0
        if ([int]::TryParse($val, [ref]$intVal)) { return $intVal }
    }
    return 0
}

function Is-Running {
    $pv = Get-PidValue
    if ($pv -gt 0) {
        $proc = Get-Process -Id $pv -ErrorAction SilentlyContinue
        if ($proc -and $proc.ProcessName -eq "python") {
            return $true
        }
    }
    return $false
}

switch ($Action) {
    "start" {
        if (Is-Running) {
            Write-Host "[WARN] Dashboard gia' in esecuzione (PID $(Get-PidValue))." -ForegroundColor Yellow
            exit 0
        }
        # Source env vars from keys.env
        if (Test-Path -LiteralPath $EnvFile) {
            Get-Content -LiteralPath $EnvFile | ForEach-Object {
                if ($_ -match '^([A-Z_][A-Z0-9_]*)=(.*)$') {
                    $key = $matches[1]
                    $val = $matches[2]
                    [Environment]::SetEnvironmentVariable($key, $val, 'Process')
                }
            }
            Write-Host "[OK] API keys caricati da $EnvFile" -ForegroundColor Green
        }
        if ([string]::IsNullOrWhiteSpace($FlaskSecret)) {
            $FlaskSecret = [Guid]::NewGuid().ToString("N")
            Write-Host "[WARN] FLASK_SECRET non definito: uso secret effimero per questa sessione." -ForegroundColor Yellow
        }
        [Environment]::SetEnvironmentVariable("FLASK_SECRET", $FlaskSecret, 'Process')
        [Environment]::SetEnvironmentVariable("PORT", "$Port", 'Process')

        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $logFile = Join-Path -Path $LogDir -ChildPath "dashboard-$timestamp.log"

        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "python"
        $psi.Arguments = "-m waitress --call --host=127.0.0.1 --port=$Port app:create_app"
        $psi.WorkingDirectory = $AppDir
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.CreateNoWindow = $true

        Get-ChildItem -Path Env:* | ForEach-Object {
            $psi.EnvironmentVariables[$_.Name] = $_.Value
        }

        $p = [System.Diagnostics.Process]::Start($psi)
        $p.Id | Out-File -LiteralPath $PidFile -Encoding Ascii

        $outTask = $p.StandardOutput.ReadToEndAsync()
        $errTask = $p.StandardError.ReadToEndAsync()

        Start-Sleep -Seconds 4

        if ($p.HasExited) {
            $outResult = $outTask.Result
            $errResult = $errTask.Result
            "$outResult`n$errResult" | Out-File -LiteralPath $logFile -Encoding utf8
            Write-Error "Dashboard exit code $($p.ExitCode). Log: $logFile"
            exit 1
        }
        Write-Host "[OK] Dashboard avviata su http://127.0.0.1:$Port (PID $($p.Id))" -ForegroundColor Green
        Write-Host "     Log: $logFile" -ForegroundColor DarkGray
    }
    "stop" {
        $pv = Get-PidValue
        if ($pv -gt 0) {
            Stop-Process -Id $pv -Force -ErrorAction SilentlyContinue
            Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
            Write-Host "[OK] Dashboard fermata (PID $pv)." -ForegroundColor Green
        } else {
            Write-Host "[WARN] Nessun PID trovato." -ForegroundColor Yellow
        }
    }
    "restart" {
        & $MyInvocation.MyCommand.Path -Action stop
        Start-Sleep -Seconds 2
        & $MyInvocation.MyCommand.Path -Action start -Port $Port -EnvFile $EnvFile
    }
    "status" {
        if (Is-Running) {
            Write-Host "[OK] Dashboard in esecuzione (PID $(Get-PidValue)) su http://127.0.0.1:$Port" -ForegroundColor Green
        } else {
            Write-Host "[WARN] Dashboard non in esecuzione." -ForegroundColor Yellow
        }
    }
}
