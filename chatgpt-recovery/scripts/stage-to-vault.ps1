# stage-to-vault.ps1 -- Copy ChatGPT export to vault-shared/Sources/raw/chatgpt-export-2026-05-14/
#
# Use ONLY after bulk export complete (verify .export-progress.json indexingComplete: true
# AND projectsIndexingComplete: true).
#
# vault-shared boundary: sibling-peer NO-WRITE default. This script writes ONCE for this
# explicitly authorized recovery operation (Eduardo permission 2026-05-14).

$ErrorActionPreference = "Stop"

$src = "C:\dev\chatgpt-full-export-2026-05-14"
$dst = "C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14"
$logFile = "$dst\_meta\staging.log"

Write-Host "=== ChatGPT Export Staging to Vault ===" -ForegroundColor Cyan
Write-Host "Source: $src"
Write-Host "Destination: $dst"
Write-Host ""

# Validate source exists + export complete
if (-not (Test-Path $src)) {
    Write-Error "Source directory not found: $src"
    exit 1
}

$progressFile = "$src\.export-progress.json"
if (Test-Path $progressFile) {
    $progress = Get-Content $progressFile | ConvertFrom-Json
    Write-Host "Progress state:"
    Write-Host "  Regular indexing complete: $($progress.indexingComplete)"
    Write-Host "  Archived indexing complete: $($progress.archivedIndexingComplete)"
    Write-Host "  Projects indexing complete: $($progress.projectsIndexingComplete)"
    Write-Host "  Total downloaded conversations: $($progress.downloadedIds.Count)"
    Write-Host "  Total downloaded files: $($progress.downloadedFileIds.Count)"
    Write-Host ""

    if (-not $progress.indexingComplete -or -not $progress.projectsIndexingComplete) {
        Write-Warning "Bulk export NOT complete. Stage anyway? (yes/no)"
        $confirm = Read-Host
        if ($confirm -ne "yes") {
            Write-Host "Aborted."
            exit 0
        }
    }
}

# Create destination + _meta subdirectory
New-Item -ItemType Directory -Path $dst -Force | Out-Null
New-Item -ItemType Directory -Path "$dst\_meta" -Force | Out-Null

# Copy via robocopy (preserves attributes, supports large dirs, atomic per file)
Write-Host "Starting robocopy..." -ForegroundColor Yellow
$robocopyArgs = @(
    $src,
    $dst,
    "/E",                  # all subdirs incl empty
    "/COPY:DAT",           # data + attributes + timestamps
    "/R:3",                # retry 3 times on locked files
    "/W:5",                # wait 5s between retries
    "/MT:8",               # multithread 8 streams
    "/LOG:$logFile",
    "/TEE",                # output to console + log
    "/XF", ".export-progress.json"  # exclude progress state (don't clutter vault)
)
robocopy @robocopyArgs

$exitCode = $LASTEXITCODE
# robocopy exit codes 0-7 are success/info, 8+ are errors
if ($exitCode -ge 8) {
    Write-Error "robocopy failed with exit code $exitCode"
    exit 1
}

Write-Host "`n=== Staging stats ===" -ForegroundColor Green

# Count files + size
$srcStats = Get-ChildItem $src -Recurse -File | Measure-Object -Property Length -Sum
$dstStats = Get-ChildItem $dst -Recurse -File | Measure-Object -Property Length -Sum

Write-Host "Source: $($srcStats.Count) files, $([math]::Round($srcStats.Sum / 1MB, 2)) MB"
Write-Host "Destination: $($dstStats.Count) files, $([math]::Round($dstStats.Sum / 1MB, 2)) MB"

if ($srcStats.Count -ne $dstStats.Count + 1) {  # +1 because we excluded .export-progress.json
    Write-Warning "File count mismatch. Source: $($srcStats.Count), Dest: $($dstStats.Count) (expected $($srcStats.Count - 1))"
}

# Per-bucket breakdown
Write-Host "`n=== Per-bucket breakdown ==="
$regularJson = (Get-ChildItem "$dst\json" -Filter *.json -ErrorAction SilentlyContinue | Measure-Object).Count
$regularMd = (Get-ChildItem "$dst\markdown" -Filter *.md -ErrorAction SilentlyContinue | Measure-Object).Count
$projectCount = (Get-ChildItem "$dst\projects" -Directory -ErrorAction SilentlyContinue | Where-Object Name -notlike "_*" | Measure-Object).Count
$totalProjectJson = (Get-ChildItem "$dst\projects" -Filter *.json -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
$totalFiles = (Get-ChildItem "$dst" -Filter * -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Directory.Name -eq "files" } | Measure-Object).Count

Write-Host "Regular JSON: $regularJson"
Write-Host "Regular MD: $regularMd"
Write-Host "Projects: $projectCount"
Write-Host "Project JSON total: $totalProjectJson"
Write-Host "Attachment files: $totalFiles"

# Write provenance metadata
$provenance = @{
    source_path = $src
    staged_at = (Get-Date).ToString("o")
    staged_by = "claude-code+chatgpt-recovery"
    bearer_token_workspace = "Master DD team (account da989913-...)"
    tool_used = "brianjlacy/export-chatgpt@HEAD"
    flags_used = "--include-archived --throttle 8 --no-user-dir"
    privacy_classification = "sovereign-only"
    counts = @{
        regular_json = $regularJson
        projects = $projectCount
        project_json_total = $totalProjectJson
        attachments = $totalFiles
        memory_items = 83
        custom_instructions = "exported"
    }
}

$provenance | ConvertTo-Json -Depth 5 | Out-File "$dst\_meta\provenance.json" -Encoding utf8

Write-Host "`nProvenance: $dst\_meta\provenance.json" -ForegroundColor Green
Write-Host "Log: $logFile" -ForegroundColor Green
Write-Host "`nReady for classification pipeline." -ForegroundColor Cyan
Write-Host "Next: python pipeline/classify.py --input '$dst' --output '<classification-output-dir>'"
