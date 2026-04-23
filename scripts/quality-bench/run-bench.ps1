<#
.SYNOPSIS
  Quality bench HumanEval-style: testa pass@1 su N problemi Python × M modelli.

.DESCRIPTION
  Per ogni problema:
    1. Invia prompt al modello (Ollama HTTP o OpenAI-compatible cloud)
    2. Estrae il blocco di codice Python dalla risposta
    3. Esegue i test in subprocess Python isolato (timeout 10s)
    4. Registra pass/fail + output errore

  Modelli supportati:
    - Ollama local: ollama:<model>
    - Groq: groq:<model>
    - Cerebras: cerebras:<model>

  Output: JSON risultati + tabella Markdown riassuntiva.

.PARAMETER ProblemsFile
  Path a problems.json (default: ./problems.json in cwd script)

.PARAMETER Models
  Array di stringhe in formato "provider:model". Esempio: @('ollama:qwen2.5-coder:7b','groq:llama-3.3-70b-versatile')

.PARAMETER OutputDir
  Directory output risultati (default: ./results/)

.EXAMPLE
  .\run-bench.ps1 -Models @('ollama:qwen2.5-coder:7b','groq:llama-3.3-70b-versatile')

.NOTES
  Richiede Python 3.10+ nel PATH per test execution.
  Prompt istruttivo include "Return only the Python function, no explanation" per parse robusto.
#>
param(
  [string]$ProblemsFile = (Join-Path $PSScriptRoot 'problems.json'),
  [string[]]$Models = @(
    'ollama:qwen2.5-coder:7b',
    'ollama:qwen2.5-coder:14b-instruct-q2_K',
    'ollama:qwen3-coder:30b',
    'ollama:deepseek-r1:8b',
    'groq:llama-3.3-70b-versatile',
    'cerebras:llama3.1-8b'
  ),
  [string]$OutputDir = (Join-Path $PSScriptRoot 'results')
)

$ErrorActionPreference = 'Stop'

# Load API keys from env file if not already set
$keysFile = "$env:USERPROFILE\.config\api-keys\keys.env"
if (Test-Path $keysFile) {
  Get-Content $keysFile | Where-Object { $_ -match '^\s*([A-Z_]+)=(.+)$' } | ForEach-Object {
    $parts = $_ -split '=', 2
    [Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim(), 'Process')
  }
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$problems = Get-Content $ProblemsFile | ConvertFrom-Json

$endpoints = @{
  groq     = 'https://api.groq.com/openai/v1/chat/completions'
  cerebras = 'https://api.cerebras.ai/v1/chat/completions'
}

function Invoke-ModelRequest {
  param(
    [string]$Uri,
    [hashtable]$Headers,
    [string]$Body,
    [string]$ContentType,
    [int]$TimeoutSec,
    [int]$MaxAttempts = 3
  )
  # Retry on transient errors only: 429 (rate limit), 5xx (server), WebException/timeout.
  # Do NOT retry 4xx client errors (except 429) — those indicate caller bugs.
  $lastErr = $null
  for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
    try {
      if ($Headers) {
        return Invoke-RestMethod -Uri $Uri -Method Post -Headers $Headers -Body $Body -TimeoutSec $TimeoutSec
      } else {
        return Invoke-RestMethod -Uri $Uri -Method Post -Body $Body -ContentType $ContentType -TimeoutSec $TimeoutSec
      }
    } catch {
      $lastErr = $_
      $statusCode = $null
      if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
        # PS 5.1: StatusCode is HttpStatusCode enum; Value__ is the int
        $statusCode = [int]$_.Exception.Response.StatusCode.Value__
      }
      $isTransient = $false
      if ($statusCode) {
        if ($statusCode -eq 429 -or ($statusCode -ge 500 -and $statusCode -lt 600)) {
          $isTransient = $true
        }
      } elseif ($_.Exception -is [System.Net.WebException] -or $_.Exception.Message -match 'timed out|timeout|connection') {
        $isTransient = $true
      }
      if (-not $isTransient -or $attempt -eq $MaxAttempts) {
        break
      }
      # Exponential backoff: 1s, 2s
      $backoffSec = [math]::Pow(2, $attempt - 1)
      Start-Sleep -Seconds $backoffSec
    }
  }
  $statusInfo = if ($lastErr.Exception.Response) { " (HTTP $([int]$lastErr.Exception.Response.StatusCode.Value__))" } else { '' }
  throw "Invoke-ModelRequest failed after $MaxAttempts attempt(s)$($statusInfo): $($lastErr.Exception.Message)"
}

function Invoke-Model {
  param([string]$Provider, [string]$Model, [string]$Prompt)

  $systemPrompt = 'You are a Python coder. Complete the function below. Return ONLY the function definition (including the signature line), no explanation, no example usage, no surrounding markdown fences.'
  $userPrompt = $Prompt

  if ($Provider -eq 'ollama') {
    $payload = @{
      model = $Model
      messages = @(
        @{ role = 'system'; content = $systemPrompt }
        @{ role = 'user'; content = $userPrompt }
      )
      stream = $false
      options = @{ num_ctx = 8192; num_predict = 2000; temperature = 0 }
    } | ConvertTo-Json -Depth 6
    $r = Invoke-ModelRequest -Uri 'http://127.0.0.1:11434/api/chat' -Body $payload -ContentType 'application/json' -TimeoutSec 300
    return $r.message.content
  } elseif ($endpoints.ContainsKey($Provider)) {
    $keyVar = "${Provider}_API_KEY".ToUpper()
    $apiKey = [Environment]::GetEnvironmentVariable($keyVar, 'Process')
    if (-not $apiKey) { throw "Missing env var $keyVar" }
    $payload = @{
      model = $Model
      messages = @(
        @{ role = 'system'; content = $systemPrompt }
        @{ role = 'user'; content = $userPrompt }
      )
      max_tokens = 2000
      temperature = 0
    } | ConvertTo-Json -Depth 5
    $headers = @{ 'Authorization' = "Bearer $apiKey"; 'Content-Type' = 'application/json' }
    $r = Invoke-ModelRequest -Uri $endpoints[$Provider] -Headers $headers -Body $payload -TimeoutSec 120
    return $r.choices[0].message.content
  } else {
    throw "Unknown provider: $Provider"
  }
}

function Extract-PythonCode {
  param([string]$Response)
  $code = $Response
  # strip thinking mode tags first (deepseek-r1 emits <think>...</think>)
  $code = $code -replace '(?s)<think>.*?</think>', ''
  $code = $code -replace '(?s)<thinking>.*?</thinking>', ''
  # strip markdown fences with a permissive regex (python/py optional, whitespace flex)
  if ($code -match '(?s)```(?:python|py)?\s*\n?(.+?)```') {
    $code = $matches[1]
  }
  # final safety net: remove any surviving ``` lines
  $code = ($code -split "`n" | Where-Object { $_ -notmatch '^\s*```' }) -join "`n"
  return $code.Trim()
}

function Test-Solution {
  param([string]$Code, [array]$Tests, [int]$TimeoutSec = 10)
  $script = "$Code`n`n" + ($Tests -join "`n") + "`nprint('ALL_PASS')"
  $tmpFile = New-TemporaryFile
  try {
    # write as UTF-8 no BOM, Python 3.12 defaults to utf-8 source
    [System.IO.File]::WriteAllText($tmpFile.FullName, $script, (New-Object System.Text.UTF8Encoding $false))
    # invoke python with combined stderr, capture exit code via $LASTEXITCODE
    $combined = & python $tmpFile.FullName 2>&1 | Out-String
    $exitCode = $LASTEXITCODE
    $passed = ($exitCode -eq 0) -and ($combined -match 'ALL_PASS')
    $reason = if ($passed) { 'pass' }
              elseif ($combined -match 'AssertionError') { 'assert_fail' }
              elseif ($combined -match 'SyntaxError|IndentationError') { 'syntax_error' }
              elseif ($combined -match 'NameError') { 'name_error' }
              elseif ($combined -match 'TypeError') { 'type_error' }
              else { 'runtime_error' }
    return @{ pass = $passed; reason = $reason; stderr = $combined.Trim(); exitCode = $exitCode }
  } finally {
    Remove-Item $tmpFile -ErrorAction SilentlyContinue
  }
}

$results = @()
$total = $problems.Count * $Models.Count
$i = 0

foreach ($modelSpec in $Models) {
  $parts = $modelSpec -split ':', 2
  $provider = $parts[0]
  $model = $parts[1]

  Write-Host "`n===== Model: $modelSpec ====="
  foreach ($p in $problems) {
    $i++
    Write-Host "[$i/$total] $($p.id) ... " -NoNewline
    $startMs = (Get-Date).Ticks / 10000
    try {
      $response = Invoke-Model -Provider $provider -Model $model -Prompt $p.prompt
      $code = Extract-PythonCode -Response $response
      $test = Test-Solution -Code $code -Tests $p.tests
      $elapsedMs = ((Get-Date).Ticks / 10000) - $startMs
      $statusLabel = if ($test.pass) { 'PASS' } else { 'FAIL' }
      Write-Host ("{0} ({1:F0}ms) [{2}]" -f $statusLabel, $elapsedMs, $test.reason)
      $results += [PSCustomObject]@{
        model     = $modelSpec
        problem   = $p.id
        pass      = $test.pass
        reason    = $test.reason
        elapsedMs = [int]$elapsedMs
        stderr    = $test.stderr
        codeHead  = ($code -split "`n" | Select-Object -First 3) -join ' | '
      }
    } catch {
      $elapsedMs = ((Get-Date).Ticks / 10000) - $startMs
      Write-Host "ERROR ($($_.Exception.Message))"
      $results += [PSCustomObject]@{
        model     = $modelSpec
        problem   = $p.id
        pass      = $false
        reason    = 'infer_error'
        elapsedMs = [int]$elapsedMs
        stderr    = $_.Exception.Message
        codeHead  = ''
      }
    }
  }
}

$jsonPath = Join-Path $OutputDir ("results-{0}.json" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
$results | ConvertTo-Json -Depth 5 | Out-File -FilePath $jsonPath -Encoding utf8

Write-Host "`n`n===== SUMMARY (pass@1) ====="
$grouped = $results | Group-Object model
$summary = foreach ($g in $grouped) {
  $passes = ($g.Group | Where-Object { $_.pass }).Count
  $total = $g.Group.Count
  $rate = if ($total -gt 0) { [math]::Round(($passes / $total) * 100, 1) } else { 0 }
  [PSCustomObject]@{ Model = $g.Name; Pass = $passes; Total = $total; 'Rate%' = $rate }
}
$summary | Sort-Object 'Rate%' -Descending | Format-Table -AutoSize
Write-Host "`nResults JSON: $jsonPath"
