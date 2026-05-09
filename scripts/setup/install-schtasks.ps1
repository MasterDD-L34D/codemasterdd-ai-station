# install-schtasks.ps1 -- Setup Windows Task Scheduler entries M7 + M8
#
# BACKLOG M7 + M8 (deferred SPRINT_02): registra 2 scheduled task user-level:
#   - ApiKeysBackup       daily 03:00  -> backup-api-keys.ps1 -Quiet (M7)
#   - HookIntegritySmoke  weekly Sun 09:00 -> smoke-test-hooks.ps1 -Quiet (M8)
#
# Pattern safety:
#   - Idempotent: query prima di create (skip se esiste)
#   - User-level: NON richiede /RU SYSTEM o admin elevation
#   - Eduardo manual run (no sandbox permission per Unauthorized Persistence)
#
# Pre-requisiti:
#   - 3 script installati in C:\Users\edusc\.local\bin\ (cp da scripts/ del repo)
#
# Usage:
#   .\scripts\setup\install-schtasks.ps1            # install entrambi
#   .\scripts\setup\install-schtasks.ps1 -Uninstall # rimuovi entrambi
#   .\scripts\setup\install-schtasks.ps1 -Verify    # query stato senza modifiche

[CmdletBinding()]
param(
    [switch]$Uninstall,
    [switch]$Verify
)

$tasks = @(
    @{
        Name = "ApiKeysBackup"
        Script = "C:\Users\edusc\.local\bin\backup-api-keys.ps1"
        Schedule = @("/SC", "DAILY", "/ST", "03:00")
        Description = "M7 daily backup keys.env (DPAPI optional via -Encrypt edit)"
    },
    @{
        Name = "HookIntegritySmoke"
        Script = "C:\Users\edusc\.local\bin\smoke-test-hooks.ps1"
        Schedule = @("/SC", "WEEKLY", "/D", "SUN", "/ST", "09:00")
        Description = "M8 weekly Sunday hook integrity smoke test (12 cases)"
    }
)

function Test-TaskExists {
    param([string]$Name)
    schtasks /Query /TN $Name 2>&1 | Out-Null
    return $LASTEXITCODE -eq 0
}

function Install-Task {
    param([hashtable]$Task)

    if (-not (Test-Path $Task.Script)) {
        Write-Host "  ERROR: script non trovato: $($Task.Script)" -ForegroundColor Red
        Write-Host "         Pre-step: copia da repo scripts/ a ~/.local/bin/" -ForegroundColor DarkGray
        return $false
    }

    if (Test-TaskExists $Task.Name) {
        Write-Host "  [SKIP] $($Task.Name) gia' esistente (idempotent)" -ForegroundColor DarkGray
        return $true
    }

    $tr = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$($Task.Script)`" -Quiet"
    $args = @("/Create", "/TN", $Task.Name, "/TR", $tr) + $Task.Schedule + @("/F")

    & schtasks @args 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK]   $($Task.Name) creato -- $($Task.Description)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  [FAIL] $($Task.Name) creazione fallita (exit $LASTEXITCODE)" -ForegroundColor Red
        return $false
    }
}

function Uninstall-Task {
    param([hashtable]$Task)

    if (-not (Test-TaskExists $Task.Name)) {
        Write-Host "  [SKIP] $($Task.Name) non esistente" -ForegroundColor DarkGray
        return $true
    }

    & schtasks /Delete /TN $Task.Name /F 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK]   $($Task.Name) rimosso" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  [FAIL] $($Task.Name) rimozione fallita (exit $LASTEXITCODE)" -ForegroundColor Red
        return $false
    }
}

function Verify-Task {
    param([hashtable]$Task)

    $exists = Test-TaskExists $Task.Name
    if ($exists) {
        Write-Host "  [PRESENT] $($Task.Name)" -ForegroundColor Green
        & schtasks /Query /TN $Task.Name /FO LIST 2>&1 | Select-String -Pattern "(Stato|Status|Prossima esecuzione|Next Run Time):" | ForEach-Object {
            Write-Host "             $($_.Line.Trim())" -ForegroundColor DarkGray
        }
    } else {
        Write-Host "  [ABSENT]  $($Task.Name)" -ForegroundColor Yellow
    }
    return $exists
}

# ---- MAIN ----
Write-Host "install-schtasks -- M7 + M8 scheduled tasks" -ForegroundColor Cyan
Write-Host ""

if ($Verify) {
    Write-Host "Verify mode (read-only):" -ForegroundColor Yellow
    foreach ($t in $tasks) {
        Verify-Task $t | Out-Null
    }
    exit 0
}

if ($Uninstall) {
    Write-Host "Uninstall mode:" -ForegroundColor Yellow
    foreach ($t in $tasks) {
        Uninstall-Task $t | Out-Null
    }
    exit 0
}

# Default: install
Write-Host "Install mode (idempotent):" -ForegroundColor Yellow
$allOk = $true
foreach ($t in $tasks) {
    if (-not (Install-Task $t)) {
        $allOk = $false
    }
}

Write-Host ""
if ($allOk) {
    Write-Host "==> SETUP OK -- 2/2 schtasks ready" -ForegroundColor Green
    Write-Host "    Verify: .\scripts\setup\install-schtasks.ps1 -Verify" -ForegroundColor DarkGray
    Write-Host "    Uninstall: .\scripts\setup\install-schtasks.ps1 -Uninstall" -ForegroundColor DarkGray
    exit 0
} else {
    Write-Host "==> SETUP PARTIAL -- vedi errori sopra" -ForegroundColor Red
    exit 1
}
