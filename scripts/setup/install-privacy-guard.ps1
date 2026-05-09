# Install / re-install privacy guard rail H8 per wrapper Aider cloud
# Risoluzione harsh review V2 BLOCKING + ADR-0023.
#
# Cosa fa:
# 1. Crea/aggiorna whitelist in ~/.config/aider-privacy-whitelist.txt
# 2. Verifica i 4 wrapper cmd cloud hanno il privacy guard block (4 file in ~/.local/bin/)
#
# Uso: .\scripts\setup\install-privacy-guard.ps1 [-DryRun]
#
# Idempotente: rilanciabile per refresh whitelist o verify wrapper integrity.

param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ConfigDir = "$env:USERPROFILE\.config"
$WhitelistPath = "$ConfigDir\aider-privacy-whitelist.txt"
$BinDir = "$env:USERPROFILE\.local\bin"
$CloudWrappers = @("aider-groq.cmd", "aider-cerebras.cmd", "aider-gemini.cmd", "aider-openai.cmd")

$WhitelistContent = @"
# Aider privacy guard rail whitelist (H8 ADR-0023 / harsh review V2 BLOCKING resolution)
#
# File listed here = repo with cloud delegation OK (Groq/Cerebras/Gemini/OpenAI free/paid tiers).
# Repo NON listed = sovereign-only enforcement (wrapper aider-* cloud abort with error).
#
# Format: 1 absolute path per line (Windows), case-INsensitive match against ``git rev-parse --show-toplevel``.
# Comments with # ignored. Empty lines ignored.

# === codemasterdd-ai-station (policy hub, fully cloud OK)
C:\dev\codemasterdd-ai-station

# === Game (Evo-Tactics Vue3) -- public repo, gameplay code, cloud OK in pratica
C:\dev\Game

# === Game-Godot-v2 -- public repo, port phase, governance interna autosufficiente
C:\dev\Game-Godot-v2

# === Synesthesia: NOT in whitelist -- mixed privacy (controllers/ sovereign-only, views/ cloud-OK)
# Wrapper deve essere bypassato manualmente con check Eduardo per views/ se serve.
# Razionale: safe-by-default. Sub-path whitelist non implementato (futuro enhancement).
# C:\dev\synesthesia  -- DELIBERATAMENTE COMMENTATO

# === Repo cliente: MAI cloud, sovereign-only sempre.
# Aggiungere al whitelist solo se cliente esplicitamente OK con cloud delegation.
"@

Write-Host "Privacy guard rail H8 installer (DryRun=$DryRun)"
Write-Host ""

# Step 1: ConfigDir
if (-not (Test-Path $ConfigDir)) {
    if ($DryRun) { Write-Host "DRY: would create $ConfigDir" } else { New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null; Write-Host "Created: $ConfigDir" }
}

# Step 2: Whitelist
$whitelistExists = Test-Path $WhitelistPath
if ($whitelistExists) {
    Write-Host "Whitelist EXISTS: $WhitelistPath"
    Write-Host "  Run with -DryRun to see content. Will NOT overwrite (manual edit preserved)."
} else {
    if ($DryRun) {
        Write-Host "DRY: would create whitelist $WhitelistPath ($($WhitelistContent.Length) chars)"
    } else {
        $WhitelistContent | Set-Content -Path $WhitelistPath -Encoding UTF8
        Write-Host "Created whitelist: $WhitelistPath"
    }
}

# Step 3: Verify wrappers have privacy guard block
Write-Host ""
Write-Host "Verifying wrapper integrity..."
$missingGuard = @()
foreach ($wrapper in $CloudWrappers) {
    $path = Join-Path $BinDir $wrapper
    if (-not (Test-Path $path)) {
        Write-Warning "  MISSING wrapper: $path"
        continue
    }
    $content = Get-Content $path -Raw
    if ($content -match 'aider-privacy-whitelist' -and $content -match 'privacy guard rail H8') {
        Write-Host "  OK: $wrapper has privacy guard block"
    } else {
        Write-Warning "  GUARD MISSING: $wrapper -- needs manual update with privacy guard block (vedi docs)"
        $missingGuard += $wrapper
    }
}

# Step 4: Test
Write-Host ""
Write-Host "Smoke test:"
$testCmd = Join-Path $PSScriptRoot "test-privacy-guard.cmd"
if (Test-Path $testCmd) {
    Push-Location $PWD.Path
    try {
        $result = & cmd /c "$testCmd" 2>&1 | Out-String
        Write-Host "  Test result (current dir $($PWD.Path)):"
        Write-Host "    $result"
    } finally { Pop-Location }
} else {
    Write-Warning "  test-privacy-guard.cmd not found at $testCmd"
}

# Summary
Write-Host ""
Write-Host "========== SUMMARY =========="
Write-Host "Config dir: $ConfigDir"
Write-Host "Whitelist: $WhitelistPath ($(if (Test-Path $WhitelistPath) {'EXISTS'} else {'MISSING'}))"
Write-Host "Wrappers checked: $($CloudWrappers.Count)"
if ($missingGuard.Count -gt 0) {
    Write-Warning "Wrappers MISSING guard block: $($missingGuard -join ', ')"
    Write-Host "  -> manually update those .cmd with privacy guard block (vedi scripts/setup/aider-wrapper-template.txt)"
} else {
    Write-Host "All wrappers OK (privacy guard block present)"
}
