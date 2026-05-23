# sync-opencode-api-env.ps1
# Validates centralized keys.env for OpenCode-related providers.
# OpenCode config does not support a top-level dotenv env-file binding.
# Default mode is dry-run. -Apply is intentionally refused to avoid
# writing an invalid opencode.jsonc.

[CmdletBinding()]
param(
    [string]$KeysFile = "$env:USERPROFILE\.config\api-keys\keys.env",
    [string]$ConfigPath = "$env:USERPROFILE\.config\opencode\opencode.json",
    [switch]$Apply,
    [switch]$CreateIfMissing
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Info([string]$Message) { Write-Host "[INFO] $Message" -ForegroundColor Cyan }
function Write-Warn([string]$Message) { Write-Host "[WARN] $Message" -ForegroundColor Yellow }
function Write-Ok([string]$Message) { Write-Host "[OK]   $Message" -ForegroundColor Green }
function Write-Fail([string]$Message) { Write-Host "[FAIL] $Message" -ForegroundColor Red }

if (-not (Test-Path -LiteralPath $KeysFile)) {
    Write-Fail "keys.env not found: $KeysFile"
    exit 1
}

$jsoncFallback = "$env:USERPROFILE\.config\opencode\opencode.jsonc"
if (-not (Test-Path -LiteralPath $ConfigPath) -and (Test-Path -LiteralPath $jsoncFallback)) {
    $ConfigPath = $jsoncFallback
}

$keysRaw = Get-Content -LiteralPath $KeysFile -ErrorAction Stop
$keyNames = @()
foreach ($line in $keysRaw) {
    if ($line -match '^([A-Z0-9_]+)=') {
        $keyNames += $matches[1]
    }
}

$required = @(
    "GROQ_API_KEY",
    "CEREBRAS_API_KEY",
    "GEMINI_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "HUGGINGFACE_API_KEY",
    "GITHUB_MODELS_API_KEY",
    "TAVILY_API_KEY"
)

$missing = @($required | Where-Object { $_ -notin $keyNames })
if ($missing.Count -gt 0) {
    Write-Warn "Missing keys in keys.env: $($missing -join ', ')"
} else {
    Write-Ok "All required API keys found in keys.env"
}

if (-not (Test-Path -LiteralPath $ConfigPath)) {
    if (-not $CreateIfMissing) {
        Write-Fail "OpenCode config not found: $ConfigPath"
        Write-Info "Create a minimal config with only `$schema, or launch OpenCode from an environment that already has API keys loaded."
        exit 1
    }

    Write-Warn "OpenCode config missing, creating minimal template in memory only"
    $parent = Split-Path -Parent $ConfigPath
    $cfgObj = [ordered]@{
        '$schema' = 'https://opencode.ai/config.json'
    }
} else {
    $cfgObj = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
}

Write-Info "OpenCode config: $ConfigPath"
Write-Info "Keys file:       $KeysFile"
if ($cfgObj.PSObject.Properties.Name -contains 'env') {
    Write-Warn "Config contains top-level 'env'. This is invalid for OpenCode 1.15.x and should be removed."
}

$providersCount = 0
if ($cfgObj.PSObject.Properties.Name -contains 'provider' -and $null -ne $cfgObj.provider) {
    $providersCount = @($cfgObj.provider.PSObject.Properties.Name).Count
}
Write-Info "Providers mapped: $providersCount"

if (-not $Apply) {
    Write-Ok "Dry-run complete. No files changed."
    Write-Info "Do not write a top-level env field to OpenCode config; load keys in the launcher process instead."
    exit 0
}

Write-Fail "Refusing to write OpenCode config: top-level env binding is not supported by the current schema."
Write-Info "Validated keys.env successfully. Launch OpenCode from a shell/process where the needed API keys are already exported."
exit 2
