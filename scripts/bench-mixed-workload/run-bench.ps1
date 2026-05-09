# Bench mixed-workload H9 -- BACKLOG 2026-05-09 + harsh review V3 sample size + C1 swap overhead resolution
#
# Esegue 12 task alternati 7B/14B-Q2/30B-MoE forzando 11 swap continui.
# Misura: load_duration (swap overhead), eval_duration (inference), total_duration.
# Output JSON in results/results-YYYY-MM-DD.json
#
# Usage:
#   .\scripts\bench-mixed-workload\run-bench.ps1 [-MaxLoadedModels 1|2]
#
# Default: MAX_LOADED_MODELS=1 (current ADR-0004 config).
# Per testare =2: -MaxLoadedModels 2 (richiede preflight env var change + Ollama daemon restart manuale).

param(
    [int]$MaxLoadedModels = 1,
    [ValidateSet("mixed", "batched")]
    [string]$Order = "mixed"
)

$ErrorActionPreference = "Stop"
$promptsFile = Join-Path $PSScriptRoot "prompts.json"
$resultsDir = Join-Path $PSScriptRoot "results"
$null = New-Item -ItemType Directory -Path $resultsDir -Force

$dateStr = Get-Date -Format "yyyy-MM-dd"
$outFile = Join-Path $resultsDir "results-$dateStr-maxloaded$MaxLoadedModels-$Order.json"

Write-Host "Bench mixed-workload start | MAX_LOADED_MODELS=$MaxLoadedModels | outFile=$outFile"

# Verify Ollama daemon
try {
    $version = (Invoke-RestMethod -Uri 'http://localhost:11434/api/version' -TimeoutSec 5).version
    Write-Host "Ollama daemon up: $version"
} catch {
    Write-Error "Ollama daemon not reachable on localhost:11434. Aborting."
    exit 1
}

# Load prompts
$prompts = Get-Content $promptsFile -Raw | ConvertFrom-Json
$tasksById = @{}
foreach ($t in $prompts.tasks) { $tasksById[[int]$t.id] = $t }

if ($Order -eq "batched") {
    $runOrder = @(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
} else {
    $runOrder = $prompts._run_order
}

Write-Host "Loaded $($prompts.tasks.Count) tasks, run order [$Order]: $($runOrder -join ',')"

# Bench results
$results = @{
    bench_id = "h9-mixed-workload-$dateStr"
    started_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
    max_loaded_models = $MaxLoadedModels
    ollama_version = $version
    run_order = $runOrder
    entries = @()
    aggregates = @{}
}

$prevModel = $null
$totalStart = Get-Date

foreach ($taskId in $runOrder) {
    $task = $tasksById[[int]$taskId]
    $model = $task.model
    $isSwap = ($prevModel -ne $null -and $prevModel -ne $model)
    Write-Host "`n--- Task #$($task.id) [$($task.tier)] model=$model swap=$isSwap ---"

    $body = @{
        model = $model
        prompt = $task.prompt
        stream = $false
        options = @{
            num_predict = 200
            temperature = 0.1
        }
    } | ConvertTo-Json -Depth 5

    $entryStart = Get-Date
    try {
        $response = Invoke-RestMethod -Uri 'http://localhost:11434/api/generate' -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 300
        $entryEnd = Get-Date
        $wallTimeSec = ($entryEnd - $entryStart).TotalSeconds

        # Ollama returns durations in nanoseconds
        $loadMs = [math]::Round($response.load_duration / 1e6, 0)
        $promptEvalMs = [math]::Round($response.prompt_eval_duration / 1e6, 0)
        $evalMs = [math]::Round($response.eval_duration / 1e6, 0)
        $totalMs = [math]::Round($response.total_duration / 1e6, 0)
        $tokenCount = $response.eval_count
        $tokPerSec = if ($evalMs -gt 0) { [math]::Round($tokenCount / ($evalMs / 1000), 2) } else { 0 }

        $entry = @{
            task_id = $task.id
            tier = $task.tier
            model = $model
            swap = $isSwap
            wall_time_sec = [math]::Round($wallTimeSec, 2)
            load_duration_ms = $loadMs
            prompt_eval_duration_ms = $promptEvalMs
            eval_duration_ms = $evalMs
            total_duration_ms = $totalMs
            eval_count = $tokenCount
            tokens_per_sec = $tokPerSec
            response_preview = ($response.response.Substring(0, [Math]::Min(120, $response.response.Length)) -replace '\r?\n', ' \n ')
        }
        $results.entries += $entry
        Write-Host "  wall=$($entry.wall_time_sec)s load=${loadMs}ms eval=${evalMs}ms tok/s=$tokPerSec"
    } catch {
        Write-Warning "Task #$($task.id) failed: $_"
        $results.entries += @{
            task_id = $task.id
            tier = $task.tier
            model = $model
            error = "$_"
        }
    }

    $prevModel = $model
}

$totalEnd = Get-Date
$totalElapsedSec = [math]::Round(($totalEnd - $totalStart).TotalSeconds, 2)

# Aggregates
$validEntries = $results.entries | Where-Object { $null -ne $_.load_duration_ms }
$swapEntries = $validEntries | Where-Object { $_.swap -eq $true }
$nonSwapEntries = $validEntries | Where-Object { $_.swap -eq $false }

$swapLoadAvg = if ($swapEntries.Count -gt 0) {
    $sum = 0; foreach ($e in $swapEntries) { $sum += $e.load_duration_ms }
    [math]::Round($sum / $swapEntries.Count, 0)
} else { 0 }
$nonSwapLoadAvg = if ($nonSwapEntries.Count -gt 0) {
    $sum = 0; foreach ($e in $nonSwapEntries) { $sum += $e.load_duration_ms }
    [math]::Round($sum / $nonSwapEntries.Count, 0)
} else { 0 }
$swapOverheadMs = $swapLoadAvg - $nonSwapLoadAvg

$results.completed_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
$results.aggregates = @{
    total_elapsed_sec = $totalElapsedSec
    swap_count = $swapEntries.Count
    swap_load_avg_ms = $swapLoadAvg
    nonswap_load_avg_ms = $nonSwapLoadAvg
    swap_overhead_ms = $swapOverheadMs
    swap_overhead_total_estimated_sec = [math]::Round(($swapOverheadMs * $swapEntries.Count) / 1000, 2)
    tier_breakdown = @{}
}

foreach ($tier in @('1-cosmetic', '2-behavior', '2.5-escalation')) {
    $tierEntries = $validEntries | Where-Object { $_.tier -eq $tier }
    if ($tierEntries.Count -gt 0) {
        $sumWall = 0; $sumTok = 0; $sumLoad = 0
        foreach ($e in $tierEntries) {
            $sumWall += $e.wall_time_sec
            $sumTok += $e.tokens_per_sec
            $sumLoad += $e.load_duration_ms
        }
        $results.aggregates.tier_breakdown[$tier] = @{
            count = $tierEntries.Count
            avg_wall_sec = [math]::Round($sumWall / $tierEntries.Count, 2)
            avg_tok_per_sec = [math]::Round($sumTok / $tierEntries.Count, 2)
            avg_load_ms = [math]::Round($sumLoad / $tierEntries.Count, 0)
        }
    }
}

$results | ConvertTo-Json -Depth 8 | Out-File -FilePath $outFile -Encoding utf8

Write-Host "`n========== BENCH SUMMARY =========="
Write-Host "Total elapsed: ${totalElapsedSec}s"
Write-Host "Swap count: $($swapEntries.Count) / 12 task"
Write-Host "Swap load avg: ${swapLoadAvg}ms vs non-swap ${nonSwapLoadAvg}ms"
Write-Host "Swap overhead: ${swapOverheadMs}ms per swap"
Write-Host "Total swap overhead: $($results.aggregates.swap_overhead_total_estimated_sec)s ($([math]::Round(($results.aggregates.swap_overhead_total_estimated_sec / $totalElapsedSec) * 100, 1))% del totale)"
Write-Host "Output: $outFile"
