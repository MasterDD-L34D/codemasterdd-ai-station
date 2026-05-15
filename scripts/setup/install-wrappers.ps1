<#
.SYNOPSIS
    Install Aider wrappers from scripts/wrappers/ to ~/.local/bin/ -- idempotente, hash-verified, backup-on-conflict.

.DESCRIPTION
    Risolve harsh-reviewer P1 #4 wrapper bus-factor: i 6 wrapper aider-* erano user-side only (~/.local/bin/) NO IaC, no installer, no recovery se workstation crash.
    Questo script copia da scripts/wrappers/ (canonical in repo) a ~/.local/bin/ (executable PATH).

    Pattern: idempotente (safe re-run), hash-verified (no silent overwrite of hand-edits), backup-on-conflict (.bak suffix preserva manual mods).

.PARAMETER DryRun
    Mostra cosa farebbe SENZA copiare. Default: false.

.PARAMETER Force
    Overwrite anche se hash differ (ATTENZIONE: perde hand-edits). Default: false.

.PARAMETER Verbose
    Output dettagliato per ogni file. Default: false.

.EXAMPLE
    .\install-wrappers.ps1
    Install/sync 6 wrapper to ~/.local/bin/. Skip if hash match. Backup .bak se hash differ.

.EXAMPLE
    .\install-wrappers.ps1 -DryRun
    Mostra cosa farebbe.

.EXAMPLE
    .\install-wrappers.ps1 -Force
    Overwrite tutti. Hand-edits PERSE.

.NOTES
    Created 2026-05-13 -- harsh-reviewer P1 #4 fix.
    Source: scripts/wrappers/*.cmd (canonical, repo-tracked).
    Target: ~/.local/bin/*.cmd (user-level, PATH).

    Wrapper ecosystem 8 active post-cluster T1 SPRINT_02 + post-harsh-review + 2026-05-15 free LLM audit:
    - aider-cosmetic.cmd (Qwen 7B + diff format, post-fix entry #34)
    - aider-refactor.cmd (Qwen 14B Q2 + diff)
    - aider-cerebras.cmd (Cerebras 8B + --map-tokens 0 mitigation)
    - aider-gemini.cmd (Gemini 2.5 Flash + --map-tokens 0)
    - aider-openai.cmd (gpt-4o-mini, post 10 EUR funding)
    - aider-groq-bypass.cmd (Groq 70B via openai/ + temp env-file P0 hardened)
    - aider-hf.cmd (HuggingFace Inference Providers, default DeepSeek-R1, added 2026-05-15)
    - aider-github-models.cmd (GitHub Models GPT-4o 150 req/day free, added 2026-05-15, PROPOSED)

    DEPRECATED removed:
    - aider-groq.cmd (LiteLLM Groq adapter buggy, use aider-groq-bypass)
#>

[CmdletBinding()]
param(
    [switch]$DryRun = $false,
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"

# Resolve paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
$SourceDir = Join-Path $RepoRoot "scripts\wrappers"
$TargetDir = Join-Path $env:USERPROFILE ".local\bin"

Write-Host "=== Aider Wrappers Install Script ===" -ForegroundColor Cyan
Write-Host "Source:  $SourceDir"
Write-Host "Target:  $TargetDir"
Write-Host "DryRun:  $DryRun"
Write-Host "Force:   $Force"
Write-Host ""

# Verify source dir
if (-not (Test-Path $SourceDir)) {
    Write-Error "Source dir non esiste: $SourceDir"
    exit 1
}

# Ensure target dir
if (-not (Test-Path $TargetDir)) {
    if ($DryRun) {
        Write-Host "[DryRun] Would create: $TargetDir" -ForegroundColor Yellow
    } else {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
        Write-Host "Created target dir: $TargetDir" -ForegroundColor Green
    }
}

# Get source files
$SourceFiles = Get-ChildItem -Path $SourceDir -Filter "*.cmd" -ErrorAction Stop
if ($SourceFiles.Count -eq 0) {
    Write-Error "Nessun .cmd file in $SourceDir"
    exit 1
}

Write-Host "Found $($SourceFiles.Count) wrapper(s) in source:" -ForegroundColor Cyan
foreach ($file in $SourceFiles) {
    Write-Host "  - $($file.Name)"
}
Write-Host ""

# Stats
$Installed = 0
$Skipped = 0
$BackedUp = 0
$Failed = 0

foreach ($SourceFile in $SourceFiles) {
    $TargetFile = Join-Path $TargetDir $SourceFile.Name
    $SourceHash = (Get-FileHash -Path $SourceFile.FullName -Algorithm SHA256).Hash

    Write-Host "Processing $($SourceFile.Name)..."

    if (Test-Path $TargetFile) {
        $TargetHash = (Get-FileHash -Path $TargetFile -Algorithm SHA256).Hash

        if ($SourceHash -eq $TargetHash) {
            Write-Host "  -> SKIP (hash match, already installed)" -ForegroundColor Green
            $Skipped++
            continue
        } else {
            # Hash differ: backup target prima di overwrite
            $BackupFile = "$TargetFile.bak.$(Get-Date -Format 'yyyy-MM-dd-HHmmss')"
            if ($Force -or (-not (Test-Path $BackupFile))) {
                if ($DryRun) {
                    Write-Host "  [DryRun] Would backup: $TargetFile -> $BackupFile" -ForegroundColor Yellow
                } else {
                    Copy-Item -Path $TargetFile -Destination $BackupFile -Force
                    Write-Host "  -> BACKUP: $BackupFile" -ForegroundColor Yellow
                    $BackedUp++
                }
            }

            if (-not $Force) {
                Write-Host "  -> WARN: hash differ, hand-edit detected. Re-run with -Force to overwrite. Skipping." -ForegroundColor Magenta
                $Skipped++
                continue
            }
        }
    }

    if ($DryRun) {
        Write-Host "  [DryRun] Would install: $($SourceFile.Name) (hash: $($SourceHash.Substring(0,12))...)" -ForegroundColor Yellow
    } else {
        try {
            Copy-Item -Path $SourceFile.FullName -Destination $TargetFile -Force
            $InstalledHash = (Get-FileHash -Path $TargetFile -Algorithm SHA256).Hash
            if ($InstalledHash -eq $SourceHash) {
                Write-Host "  -> INSTALL OK (hash: $($SourceHash.Substring(0,12))...)" -ForegroundColor Green
                $Installed++
            } else {
                Write-Host "  -> FAIL: hash mismatch post-copy (corruption?)" -ForegroundColor Red
                $Failed++
            }
        } catch {
            Write-Host "  -> FAIL: $($_.Exception.Message)" -ForegroundColor Red
            $Failed++
        }
    }
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "Installed:  $Installed" -ForegroundColor Green
Write-Host "Skipped:    $Skipped (hash match OR hand-edit detected without -Force)"
Write-Host "Backed up:  $BackedUp"
Write-Host "Failed:     $Failed" -ForegroundColor $(if ($Failed -gt 0) { 'Red' } else { 'White' })
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN -- nessuna modifica applicata." -ForegroundColor Yellow
}

# Verify PATH includes target dir
$PathDirs = $env:PATH -split ';'
if ($TargetDir -notin $PathDirs) {
    Write-Host "WARN: $TargetDir NON in PATH. Add it:" -ForegroundColor Yellow
    Write-Host "  [Environment]::SetEnvironmentVariable('PATH', `"$env:PATH;$TargetDir`", 'User')"
    Write-Host "  Restart terminal post-set."
}

if ($Failed -gt 0) {
    exit 2
} else {
    exit 0
}
