# run-post-export-pipeline.ps1 -- Orchestrator end-to-end post bulk export.
#
# Sequence:
#   1. Validate bulk export complete (.export-progress.json indexingComplete=true + projectsIndexingComplete=true)
#   2. Stage to vault (stage-to-vault.ps1)
#   3. Run classify.py on full vault staging dir
#   4. Run atomize.py with space mapping from vault-cross-reference-map.yaml
#   5. Generate final summary report
#   6. Cleanup bearer env-file (always, via finally block)
#
# Idempotent: each step has skip-if-done logic. Safe to re-run.
#
# Run AFTER bulk export task completes. Refuses if export incomplete unless -Force.

param(
    [switch]$Force,           # Bypass export-complete validation
    [switch]$NonInteractive   # Default abort on any prompt (CI/scheduled use)
)

$ErrorActionPreference = "Stop"

$root = "C:\dev\codemasterdd-ai-station\.claude\worktrees\affectionate-easley-a43479\chatgpt-recovery"
$exportSrc = "C:\dev\chatgpt-full-export-2026-05-14"
$vaultDst = "C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14"
$classifyOut = "$vaultDst\_processed\classification"
$atomizeOut = "$vaultDst\_processed\Cards"
$pythonExe = "$root\pipeline\.venv\Scripts\python.exe"
$bearerEnvFile = "$env:TEMP\chatgpt-bearer.env"
$summaryFile = "$vaultDst\_meta\final-summary.md"

Write-Host "=== ChatGPT Recovery Pipeline Orchestrator ===" -ForegroundColor Cyan

# ---- Step 1: Validate ----
Write-Host "`n[Step 1] Validating bulk export complete..." -ForegroundColor Yellow

$progressPath = "$exportSrc\.export-progress.json"
if (-not (Test-Path $progressPath)) {
    Write-Error "Export progress JSON missing: $progressPath"
    exit 1
}

$progress = Get-Content $progressPath | ConvertFrom-Json
# Archived gate: recovery uses --include-archived (see stage-to-vault provenance),
# so a final vault that silently omits archived conversations is incomplete.
# -Force still overrides for deliberate archived-skip runs.
if (-not $progress.indexingComplete -or -not $progress.projectsIndexingComplete -or -not $progress.archivedIndexingComplete) {
    Write-Host "  Regular indexing: $($progress.indexingComplete)"
    Write-Host "  Archived indexing: $($progress.archivedIndexingComplete)"
    Write-Host "  Projects indexing: $($progress.projectsIndexingComplete)"
    Write-Host "  Conversations downloaded: $($progress.downloadedIds.Count)"

    if ($Force) {
        Write-Warning "Bulk export incomplete, but -Force specified. Proceeding."
    } elseif ($NonInteractive) {
        Write-Error "Bulk export incomplete. Refusing to start in -NonInteractive mode. Use -Force to override."
        exit 1
    } else {
        Write-Warning "Bulk export incomplete. Continue anyway? (yes/no) [default: no]"
        $confirm = Read-Host
        if ($confirm -ne "yes") {
            Write-Host "Aborted (export not complete). Re-run when bulk export task finishes."
            exit 1
        }
    }
}

$convCount = $progress.downloadedIds.Count
$fileCount = $progress.downloadedFileIds.Count
Write-Host "  Conversations: $convCount"
Write-Host "  Files: $fileCount"
Write-Host "  Failed file downloads: $($progress.failedFileIds.PSObject.Properties.Count)"

# ---- Step 2: Staging ----
Write-Host "`n[Step 2] Staging to vault..." -ForegroundColor Yellow

if (Test-Path $vaultDst) {
    Write-Host "  Vault dest already exists. Re-running robocopy (will sync new files only)."
}

& "$root\scripts\stage-to-vault.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Staging failed."
    exit 1
}

# ---- Step 3: Classification ----
Write-Host "`n[Step 3] Running classification (BERTopic + Qwen 14B Q2 labeling)..." -ForegroundColor Yellow

if (Test-Path "$classifyOut\conversations-classified.json") {
    Write-Host "  Already classified, skipping. (Delete $classifyOut to re-run)"
} else {
    & $pythonExe "$root\pipeline\classify.py" `
        --input "$vaultDst" `
        --output "$classifyOut" `
        --embed-model "nomic-embed-text" `
        --label-model "qwen2.5-coder:14b-instruct-q2_K" `
        --min-topic-size 8 `
        --verbose

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Classification failed."
        exit 1
    }
}

# ---- Step 4: Atomize ----
Write-Host "`n[Step 4] Atomizing to Cards..." -ForegroundColor Yellow

if (Test-Path $atomizeOut) {
    $existingCardCount = (Get-ChildItem $atomizeOut -Filter "*.md" -Recurse | Measure-Object).Count
    if ($existingCardCount -gt 100) {
        Write-Host "  Already atomized ($existingCardCount cards present), skipping. (Delete $atomizeOut to re-run)"
    } else {
        & $pythonExe "$root\pipeline\atomize.py" `
            --input "$vaultDst" `
            --classification "$classifyOut" `
            --output "$atomizeOut" `
            --min-msg-length 50

        if ($LASTEXITCODE -ne 0) {
            Write-Error "Atomization failed."
            exit 1
        }
    }
} else {
    & $pythonExe "$root\pipeline\atomize.py" `
        --input "$vaultDst" `
        --classification "$classifyOut" `
        --output "$atomizeOut" `
        --min-msg-length 50

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Atomization failed."
        exit 1
    }
}

# ---- Step 5: Final summary ----
Write-Host "`n[Step 5] Generating final summary..." -ForegroundColor Yellow

$cardCount = (Get-ChildItem $atomizeOut -Filter "*.md" -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
$topicCount = if (Test-Path "$classifyOut\conversations-classified.json") {
    (Get-Content "$classifyOut\conversations-classified.json" | ConvertFrom-Json | Select-Object -ExpandProperty topic_id -Unique | Measure-Object).Count
} else { 0 }
$jsonTotal = (Get-ChildItem $vaultDst -Filter "*.json" -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
$mdTotal = (Get-ChildItem $vaultDst -Filter "*.md" -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
$filesTotal = (Get-ChildItem $vaultDst -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Directory.Name -eq "files" } | Measure-Object).Count
$dirSize = (Get-ChildItem $vaultDst -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$dirSizeMb = [math]::Round($dirSize / 1MB, 2)

$summary = @"
# ChatGPT Recovery -- Final Summary

**Date**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
**Source**: $exportSrc
**Staged to**: $vaultDst

## Counts

| Item | Count |
|---|---|
| Conversations exported | $convCount |
| Files downloaded | $fileCount |
| Failed file downloads | $($progress.failedFileIds.PSObject.Properties.Count) |
| JSON files total | $jsonTotal |
| Markdown files total | $mdTotal |
| Attachment files | $filesTotal |
| Topics detected | $topicCount |
| Cards atomized | $cardCount |
| Memory items | 83 (in _processed/memory/Cards/) |
| Custom Instructions | 1 (textareas empty, but enabled flag captured) |
| Disk usage | $dirSizeMb MB |

## Vault structure landed

``````
$vaultDst/
├── json/                                # Regular conversations JSON
├── markdown/                            # Regular conversations Markdown
├── files/                               # Regular conversation file assets
├── projects/                            # Project-scoped conversations
│   ├── project-index.json
│   ├── Progetto_Gioco_Evo_Tactics/      # ~541 conv
│   ├── Le_Sfide_dell_Arena_di_Hao_Jin/  # ~592 conv
│   ├── Creazione_gpts_Master_DD/        # ~624 conv
│   ├── Il_mio_Mondo_Fantasy/            # ~168 conv
│   ├── Torneo_Cremesi/                  # ~106 conv
│   ├── ... (12 projects total)
├── conversation-index.json              # All regular + archived
├── memory-items.json + .md              # 83 items
├── custom-instructions.json + .md
├── _processed/
│   ├── memory/Cards/                    # 83 memory cards
│   ├── classification/
│   │   ├── conversations-classified.json
│   │   ├── topics-summary.md
│   │   └── bertopic-model/
│   └── Cards/                           # ~$cardCount atomized cards
└── _meta/
    ├── provenance.json
    ├── final-summary.md (this file)
    └── staging.log
``````

## Next steps for Eduardo

1. **Review topic clusters**: open ``_processed/classification/topics-summary.md`` -- check that LLM labels make semantic sense.
2. **Sample Cards**: pick 5-10 cards from each topic, verify quality.
3. **Cross-reference vs existing vault**: use cross-reference-map.yaml to identify Cards that overlap with existing Spaces content.
4. **Selective promotion**: move quality-verified Cards from ``_processed/Cards/<topic>/`` to canonical ``Spaces/<space>/`` (Eduardo-direct workflow).
5. **Build MOC**: in ``Atlas/`` create ``chatgpt-recovery-2026-05-14-moc.md`` linking the atomized clusters.

## Caveats

- Some image/PDF files failed to download (HTTP 422 brianjlacy bug on multi-part file_id format). See ``failedFileIds`` in ``.export-progress.json``.
- LLM labels generated by qwen2.5-coder:14b-instruct-q2_K -- review for italian-language nuance.
- Memory cards used regex-based tag heuristics (no LLM). May need manual tagging for italian-specific entities.
- Cards land in ``_processed/Cards/`` staging area, NOT directly in canonical Spaces -- requires Eduardo promotion.

## Cleanup

After this summary is reviewed:
``````powershell
# Delete bearer env-file (token still valid until 2026-05-24 if needed)
Remove-Item $env:TEMP\chatgpt-bearer.env -Force

# Optional: archive source export (already in vault)
# Compress-Archive -Path C:\dev\chatgpt-full-export-2026-05-14 -DestinationPath C:\dev\backup\chatgpt-full-export-2026-05-14.zip
``````
"@

$summaryDir = Split-Path $summaryFile -Parent
New-Item -ItemType Directory -Path $summaryDir -Force | Out-Null
$summary | Out-File $summaryFile -Encoding utf8

Write-Host "`n=== Pipeline complete ===" -ForegroundColor Green
Write-Host "Summary: $summaryFile"
Write-Host "Cards: $atomizeOut ($cardCount cards)"
Write-Host "Topics: $classifyOut"
Write-Host "`nNext: review topics-summary.md + sample cards, then selective promote."

# ---- Cleanup: bearer env-file (always, even on prior errors via trap) ----
trap {
    if (Test-Path $bearerEnvFile) {
        Remove-Item $bearerEnvFile -Force -ErrorAction SilentlyContinue
        Write-Host "[cleanup] Bearer env-file deleted on error exit." -ForegroundColor DarkGray
    }
    break  # re-throw
}

if (Test-Path $bearerEnvFile) {
    Remove-Item $bearerEnvFile -Force
    Write-Host "[cleanup] Bearer env-file deleted: $bearerEnvFile" -ForegroundColor DarkGray
}

# Stale bearer files older than 1 day in %TEMP%
Get-ChildItem $env:TEMP -Filter "chatgpt-*.env" -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-1) } |
    Remove-Item -Force -ErrorAction SilentlyContinue
