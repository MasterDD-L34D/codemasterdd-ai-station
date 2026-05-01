param(
    [switch]$SkipPython
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function Invoke-Step($Name, [scriptblock]$Block) {
    Write-Host "==> $Name"
    & $Block
    Write-Host "OK: $Name"
    Write-Host ""
}

Invoke-Step "recovery consistency" {
    & (Join-Path $PSScriptRoot "check-recovery-consistency.ps1")
}

Invoke-Step "required recovery files" {
    $required = @(
        "PROJECT_STATE.yaml",
        "config/system-map.yaml",
        "config/machine-profile.example.yaml",
        "docs/recovery/active-vs-historical-boundary.md",
        "docs/recovery/pre-merge-checklist.md",
        "AGENTS.md",
        "CLAUDE.md"
    )

    foreach ($relativePath in $required) {
        $path = Join-Path $RepoRoot $relativePath
        if (-not (Test-Path -LiteralPath $path)) {
            throw "Missing required file: $relativePath"
        }
    }
}

Invoke-Step "basic YAML sanity" {
    $yamlFiles = @(
        "PROJECT_STATE.yaml",
        "config/system-map.yaml",
        "config/machine-profile.example.yaml"
    )

    foreach ($relativePath in $yamlFiles) {
        $path = Join-Path $RepoRoot $relativePath
        $content = Get-Content -LiteralPath $path
        if ($content -match "`t") {
            throw "Tabs are not allowed in YAML file: $relativePath"
        }
        if (-not ($content | Select-String -Pattern "^schema_version:")) {
            throw "Missing schema_version in YAML file: $relativePath"
        }
    }
}

if (-not $SkipPython) {
    Invoke-Step "python syntax" {
        $python = Get-Command python -ErrorAction SilentlyContinue
        if (-not $python) {
            throw "python not found; rerun with -SkipPython to skip syntax check"
        }

        Push-Location $RepoRoot
        try {
            & python -m py_compile `
                "apps/dogfood-ui/app.py" `
                "apps/dogfood-ui/db.py" `
                "apps/dogfood-ui/dafne_client.py" `
                "apps/dogfood-ui/langfuse_client.py" `
                "apps/dogfood-ui/stats.py" `
                "scripts/migrate-log-to-sqlite.py"
            if ($LASTEXITCODE -ne 0) {
                throw "python syntax check failed"
            }
        } finally {
            Pop-Location
        }
    }
}

Invoke-Step "git diff check" {
    Push-Location $RepoRoot
    try {
        & git diff --check
        if ($LASTEXITCODE -ne 0) {
            throw "git diff --check failed"
        }
    } finally {
        Pop-Location
    }
}

Write-Host "All checks passed."
