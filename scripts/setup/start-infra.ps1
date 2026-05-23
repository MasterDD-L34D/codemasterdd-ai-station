<#
.SYNOPSIS
    Start/stop/restart lo stack Docker observability con API keys da keys.env
.DESCRIPTION
    Sourcing sicuro: carica keys.env in env del processo (non scrive .env file),
    poi esegue docker compose. Le chiavi non vengono mai scritte su disco in chiaro
    dentro il repo.
.PARAMETER Action
    up (default), down, restart, status, logs
#>

param(
    [ValidateSet("up", "down", "restart", "status", "logs")]
    [string]$Action = "up"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path  # scripts/setup
$RepoRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)  # scripts/setup -> scripts -> repo root
$InfraDir = Join-Path -Path $RepoRoot -ChildPath "infra"
$KeysFile = "$env:USERPROFILE\.config\api-keys\keys.env"
if (-not (Test-Path -LiteralPath $InfraDir)) {
    Write-Error "infra/ directory not found. Computed RepoRoot=$RepoRoot"
    exit 1
}
$InfraDir = Resolve-Path -LiteralPath $InfraDir

if (-not (Test-Path -LiteralPath $InfraDir\docker-compose.yml)) {
    Write-Error "docker-compose.yml non trovato in $InfraDir"
    exit 1
}

# Source keys.env into process environment
if (Test-Path -LiteralPath $KeysFile) {
    Get-Content -LiteralPath $KeysFile | ForEach-Object {
        if ($_ -match '^([A-Z_][A-Z0-9_]*)=(.*)$') {
            $key = $matches[1]
            $val = $matches[2]
            [Environment]::SetEnvironmentVariable($key, $val, 'Process')
        }
    }
    Write-Host "[OK] API keys caricati da $KeysFile" -ForegroundColor Green
} else {
    Write-Warning "keys.env non trovato in $KeysFile"
}

switch ($Action) {
    "up" {
        Write-Host "=== Avvio stack observability ===" -ForegroundColor Cyan
        Push-Location -LiteralPath $InfraDir
        try {
            docker compose up -d
        } finally { Pop-Location }
        Write-Host "[OK] Stack avviato. Verifica: docker compose ps" -ForegroundColor Green
    }
    "down" {
        Push-Location -LiteralPath $InfraDir
        try {
            docker compose down
            Write-Host "[OK] Stack fermato." -ForegroundColor Green
        } finally { Pop-Location }
    }
    "restart" {
        Push-Location -LiteralPath $InfraDir
        try { docker compose restart } finally { Pop-Location }
    }
    "status" {
        Push-Location -LiteralPath $InfraDir
        try { docker compose ps --format "table {{.Name}}	{{.Status}}	{{.Ports}}" } finally { Pop-Location }
    }
    "logs" {
        Push-Location -LiteralPath $InfraDir
        try { docker compose logs -f } finally { Pop-Location }
    }
}
