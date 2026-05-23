<#
.SYNOPSIS
    Setup NotebookLM auth + MCP bridge per CodeMasterDD
.DESCRIPTION
    Guida Eduardo attraverso il setup NotebookLM su Lenovo (.10):
    1. Verifica tool installati (nlm.exe / notebooklm.exe)
    2. Lancia `notebooklm login` (browser OAuth interattivo -- richiede input Eduardo)
    3. Dopo auth: aggiunge MCP server a opencode.json (Lenovo) e mostra istruzioni per ~/.claude.json
    4. Verifica auth con `notebooklm auth check`
.NOTES
    Auth OAuth e' INTERATTIVO (browser). Questo script prepara tutto, ma Eduardo
    deve completare il login manualmente. Eseguire SU LENOVO (edusc@.10), non su Ryzen.
#>

param(
    [switch]$SkipLogin,
    [string]$OpencodeConfig = "$env:USERPROFILE\.config\opencode\opencode.json"
)

$ErrorActionPreference = "Stop"

function Write-Step($s) { Write-Host "`n=== $s ===" -ForegroundColor Cyan }
function Write-OK($s)  { Write-Host "[OK] $s" -ForegroundColor Green }
function Write-Warn($s) { Write-Host "[WARN] $s" -ForegroundColor Yellow }
function Write-Fail($s) { Write-Host "[FAIL] $s" -ForegroundColor Red }

function Resolve-CommandPath([string]$name) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd }
    $candidates = @(
        (Join-Path -Path $env:APPDATA -ChildPath "Python\\Python313\\Scripts\\$name.exe"),
        (Join-Path -Path $env:APPDATA -ChildPath "Python\\Python314\\Scripts\\$name.exe")
    )
    foreach ($p in $candidates) {
        if (Test-Path -LiteralPath $p) {
            return [pscustomobject]@{ Source = $p }
        }
    }
    return $null
}

function Write-JsonUtf8NoBom([string]$Path, $Object) {
    $json = $Object | ConvertTo-Json -Depth 10
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $json, $utf8NoBom)
}

Write-Step "1/5 -- Verifica tool NotebookLM"

$nlm = Resolve-CommandPath "nlm"
$notebooklm = Resolve-CommandPath "notebooklm"

if (-not $nlm) {
    Write-Warn "nlm.exe (MCP server) non trovato. Installalo con: uv tool install notebooklm-mcp-cli"
} else {
    Write-OK "nlm.exe trovato: $($nlm.Source)"
}

if (-not $notebooklm) {
    Write-Warn "notebooklm.exe (Python CLI) non trovato. Installalo con: pip install --user notebooklm-py[browser]"
} else {
    Write-OK "notebooklm.exe trovato: $($notebooklm.Source)"
}

if (-not $nlm -and -not $notebooklm) {
    Write-Fail "Nessun tool NotebookLM installato. Impossibile procedere."
    exit 1
}

Write-Step "2/5 -- Auth OAuth (richiede browser interattivo)"

if ($SkipLogin) {
    Write-OK "Saltato login (flag -SkipLogin)"
} elseif ($notebooklm) {
    Write-Warn "Sto per aprire browser per OAuth login Google NotebookLM."
    Write-Warn "Eduardo: completa l'auth nel browser, poi torna qui."
    Write-Host "Comando: notebooklm login" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    & $notebooklm.Source login
    if ($LASTEXITCODE -ne 0) {
        Write-Warn "Auth non completata o fallita. Puoi ritentare con: notebooklm login"
    } else {
        Write-OK "Auth NotebookLM completata!"
    }
} else {
    Write-Warn "notebooklm.exe non installato. Salto auth interattiva."
    Write-Warn "Installa prima: pip install --user notebooklm-py[browser]"
}

Write-Step "3/5 -- Verifica auth"

if ($notebooklm) {
    $storageState = Join-Path -Path $env:USERPROFILE -ChildPath ".notebooklm\\profiles\\default\\storage_state.json"
    & $notebooklm.Source auth check --test 2>&1
    if (Test-Path -LiteralPath $storageState) {
        Write-OK "Auth valida!"
    } else {
        Write-Warn "Auth non valida (storage_state assente). Esegui: notebooklm login"
    }
} else {
    Write-Warn "Impossibile verificare auth (CLI non installata)."
}

Write-Step "4/5 -- Configura MCP server in OpenCode (jsonc)"

$configDir = Split-Path -Parent $OpencodeConfig
if (-not (Test-Path -LiteralPath $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# Cerca file .json o .jsonc esistente
$finalConfig = $null
foreach ($ext in @(".json", ".jsonc")) {
    $candidate = [System.IO.Path]::ChangeExtension($OpencodeConfig, $ext)
    if (Test-Path -LiteralPath $candidate) {
        $finalConfig = $candidate
        break
    }
}

if (-not $finalConfig) {
    # Crea nuovo .jsonc
    $finalConfig = [System.IO.Path]::ChangeExtension($OpencodeConfig, ".jsonc")
    $cfg = @{
        '$schema' = "https://opencode.ai/config.json"
        mcpServers = @{
            notebooklm = @{
                command = "nlm"
                args = @("--transport", "stdio")
            }
        }
    }
    Write-JsonUtf8NoBom -Path $finalConfig -Object $cfg
    Write-OK "Creato OpenCode config con MCP NotebookLM: $finalConfig"
} else {
    $cfg = Get-Content -LiteralPath $finalConfig -Raw | ConvertFrom-Json
    if ($cfg.mcpServers -and $cfg.mcpServers.notebooklm) {
        Write-OK "MCP NotebookLM gia configurato in $finalConfig"
    } else {
        # Aggiungi mcpServers.notebooklm
        if (-not $cfg.mcpServers) {
            $cfg | Add-Member -NotePropertyName "mcpServers" -NotePropertyValue @{}
        }
        $cfg.mcpServers | Add-Member -NotePropertyName "notebooklm" -NotePropertyValue @{
            command = "nlm"
            args = @("--transport", "stdio")
        }
        Write-JsonUtf8NoBom -Path $finalConfig -Object $cfg
        Write-OK "Aggiunto MCP NotebookLM a $finalConfig"
    }
}

Write-Step "5/5 -- Istruzioni per Claude Code (Lenovo .10)"

$claudeJson = "$env:USERPROFILE\.claude.json"
if (Test-Path -LiteralPath $claudeJson) {
    Write-Host "Per attivare NotebookLM MCP in Claude Code:" -ForegroundColor Yellow
    Write-Host "  Aggiungi a $claudeJson sotto projects.<repo>.mcpServers:" -ForegroundColor Yellow
    Write-Host '    "notebooklm": { "command": "nlm", "args": ["--transport", "stdio"] }' -ForegroundColor Yellow
    Write-Host "  Poi riavvia Claude Code." -ForegroundColor Yellow
} else {
    Write-Host "Claude Code config non trovato. Salto istruzioni MCP CC." -ForegroundColor DarkGray
}

Write-Host "`n=== Setup NotebookLM completato ===" -ForegroundColor Cyan
Write-Host "Auth ancora da fare: notebooklm login (se saltato sopra)" -ForegroundColor Yellow
Write-Host "Auth check: notebooklm auth check --test" -ForegroundColor Yellow
Write-Host "Lista notebook: notebooklm list" -ForegroundColor Yellow
