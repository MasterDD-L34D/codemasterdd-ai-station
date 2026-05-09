# bench-opencode-cloud-free.ps1 -- Bench OpenCode + cloud free providers
#
# BACKLOG M10 (deferred SPRINT_02): verifica empirica se cloud free 70B/8B viable
# per task piccoli via OpenCode. Ipotesi: minimal-context task (no-file o single-file
# small) sotto rate limit Groq TPM 6-12k vs ADR-0022 finding "default 50k token rate-limited".
#
# Test matrix:
#   1. groq/llama-3.3-70b-versatile         (no file)        baseline minimal
#   2. groq/llama-3.3-70b-versatile         (small file 1k)  typical task
#   3. groq/qwen-2.5-coder-32b              (no file)        coder-specific 32B free
#   4. cerebras/llama3.1-8b                 (no file)        Cerebras 8B context 8k
#   5. cerebras/llama3.1-8b                 (small file 1k)  Cerebras 8B context budget
#
# Usage: .\scripts\bench-opencode-cloud-free.ps1
# Output: docs/research/bench-opencode-cloud-free-YYYY-MM-DD.md (manual write post-bench)
#         + console log per ogni test
#
# Pre-requisito: API keys in ~/.config/api-keys/keys.env (Groq + Cerebras)
# OpenCode npm v1.14.41 in C:/Users/edusc/AppData/Roaming/npm/opencode.ps1

[CmdletBinding()]
param(
    [string]$KeysFile = "$env:USERPROFILE\.config\api-keys\keys.env",
    [string]$OpencodeCmd = "$env:APPDATA\npm\opencode.ps1",
    [string]$SmallFile = "apps\dogfood-ui\db.py"
)

# ---- Load API keys into env ----
if (-not (Test-Path $KeysFile)) {
    Write-Host "ERROR: keys file non trovato: $KeysFile" -ForegroundColor Red
    exit 1
}

Get-Content $KeysFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith('#')) {
        if ($line -match '^(?:export\s+)?([A-Z_][A-Z0-9_]*)=(.*)$') {
            $name = $matches[1]
            $value = $matches[2].Trim('"').Trim("'")
            Set-Item -Path "env:$name" -Value $value
        }
    }
}
Write-Host "API keys loaded: GROQ=$(if($env:GROQ_API_KEY){'YES'}else{'NO'}) CEREBRAS=$(if($env:CEREBRAS_API_KEY){'YES'}else{'NO'})" -ForegroundColor Cyan

# Validate small file
if (-not (Test-Path $SmallFile)) {
    Write-Host "WARN: small file non trovato ($SmallFile), test 2/5 useranno solo prompt no-file" -ForegroundColor Yellow
    $SmallFile = $null
} else {
    $smallSize = (Get-Item $SmallFile).Length
    Write-Host "Small file: $SmallFile ($smallSize bytes)" -ForegroundColor DarkGray
}

# ---- Bench runner ----
function Invoke-Bench {
    param(
        [string]$TestId,
        [string]$Model,
        [string]$Prompt,
        [string]$AttachFile = ""
    )

    Write-Host ""
    Write-Host "========== $TestId : $Model ==========" -ForegroundColor Yellow
    Write-Host "  Prompt: $Prompt" -ForegroundColor DarkGray
    if ($AttachFile) {
        Write-Host "  File:   $AttachFile" -ForegroundColor DarkGray
    }

    $argList = @("run", "--model", $Model, "--log-level", "WARN")
    if ($AttachFile) {
        $argList += @("--file", $AttachFile)
    }
    $argList += $Prompt

    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $tmpOut = [System.IO.Path]::GetTempFileName()
    $tmpErr = [System.IO.Path]::GetTempFileName()

    try {
        # Pre-compute argument list (PS5.1 bug: '+' su array dentro -ArgumentList mal-parsato come positional)
        $psArgs = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $OpencodeCmd) + $argList
        $proc = Start-Process -FilePath "powershell" `
            -ArgumentList $psArgs `
            -RedirectStandardOutput $tmpOut `
            -RedirectStandardError $tmpErr `
            -NoNewWindow -PassThru -Wait

        $exitCode = $proc.ExitCode
        $stdout = (Get-Content $tmpOut -Raw -ErrorAction SilentlyContinue) -as [string]
        $stderr = (Get-Content $tmpErr -Raw -ErrorAction SilentlyContinue) -as [string]
    } finally {
        Remove-Item $tmpOut -ErrorAction SilentlyContinue
        Remove-Item $tmpErr -ErrorAction SilentlyContinue
    }

    $stopwatch.Stop()
    $elapsed = [math]::Round($stopwatch.Elapsed.TotalSeconds, 1)

    $verdict = if ($exitCode -eq 0) { "PASS" } else { "FAIL" }
    $color = if ($exitCode -eq 0) { "Green" } else { "Red" }

    Write-Host "  Exit: $exitCode  Verdict: $verdict  Time: ${elapsed}s" -ForegroundColor $color

    if ($stdout) {
        $outSnippet = ($stdout -split "`n" | Select-Object -First 4) -join "`n    "
        Write-Host "  stdout (first 4 lines):" -ForegroundColor DarkGray
        Write-Host "    $outSnippet" -ForegroundColor DarkGray
    }
    if ($stderr -and $exitCode -ne 0) {
        $errSnippet = ($stderr -split "`n" | Select-Object -First 6) -join "`n    "
        Write-Host "  stderr (first 6 lines):" -ForegroundColor Red
        Write-Host "    $errSnippet" -ForegroundColor Red
    }

    return @{
        TestId = $TestId
        Model = $Model
        Prompt = $Prompt
        AttachFile = $AttachFile
        ExitCode = $exitCode
        Verdict = $verdict
        ElapsedSec = $elapsed
        StdoutHead = if ($stdout) { ($stdout -split "`n" | Select-Object -First 4) -join " | " } else { "" }
        StderrHead = if ($stderr -and $exitCode -ne 0) { ($stderr -split "`n" | Select-Object -First 4) -join " | " } else { "" }
    }
}

# ---- Test matrix ----
$results = @()

$results += Invoke-Bench -TestId "T1" -Model "groq/llama-3.3-70b-versatile" `
    -Prompt "Print hello world in python."

$results += Invoke-Bench -TestId "T2" -Model "groq/llama-3.3-70b-versatile" `
    -Prompt "Summarize this code in 1 sentence." -AttachFile $SmallFile

$results += Invoke-Bench -TestId "T3" -Model "groq/qwen-2.5-coder-32b" `
    -Prompt "Print hello world in python."

$results += Invoke-Bench -TestId "T4" -Model "cerebras/llama3.1-8b" `
    -Prompt "Print hello world in python."

$results += Invoke-Bench -TestId "T5" -Model "cerebras/llama3.1-8b" `
    -Prompt "Summarize this code in 1 sentence." -AttachFile $SmallFile

# ---- Summary ----
Write-Host ""
Write-Host "========== SUMMARY ==========" -ForegroundColor Green
$passCount = ($results | Where-Object { $_.Verdict -eq "PASS" }).Count
$failCount = ($results | Where-Object { $_.Verdict -eq "FAIL" }).Count
Write-Host "PASS: $passCount/$($results.Count)" -ForegroundColor Green
Write-Host "FAIL: $failCount/$($results.Count)" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

$results | ForEach-Object {
    $verdictColor = if ($_.Verdict -eq "PASS") { "Green" } else { "Red" }
    $fileNote = if ($_.AttachFile) { " +file" } else { "" }
    Write-Host ("  {0} {1,-40} {2,5}s  [{3}{4}]" -f $_.TestId, $_.Model, $_.ElapsedSec, $_.Verdict, $fileNote) -ForegroundColor $verdictColor
    if ($_.StderrHead) {
        Write-Host "       err: $($_.StderrHead.Substring(0, [Math]::Min(150, $_.StderrHead.Length)))" -ForegroundColor DarkGray
    }
}

# Export results JSON for research doc
$jsonOut = "logs\bench-opencode-cloud-free-$(Get-Date -Format 'yyyy-MM-dd-HHmm').json"
if (-not (Test-Path "logs")) { New-Item -ItemType Directory -Force -Path "logs" | Out-Null }
$results | ConvertTo-Json -Depth 4 | Set-Content $jsonOut -Encoding UTF8
Write-Host ""
Write-Host "Results JSON: $jsonOut" -ForegroundColor Cyan
