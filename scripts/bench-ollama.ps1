<#
.SYNOPSIS
  Benchmark singola run Ollama con override num_ctx runtime, parse metriche native.

.DESCRIPTION
  Esegue 1 warm-up (num_predict 30) + 1 misura (num_predict 300) contro Ollama HTTP API.
  Stampa riga markdown pronta per append al log bench.

.PARAMETER Model
  Nome modello Ollama (es. "qwen2.5-coder:14b-instruct-q2_K").

.PARAMETER NumCtx
  Valore num_ctx runtime override.

.EXAMPLE
  .\bench-ollama.ps1 -Model qwen2.5-coder:14b-instruct-q2_K -NumCtx 8192
.EXAMPLE
  .\bench-ollama.ps1 -Model qwen3-coder:30b -NumCtx 16384
.EXAMPLE
  .\bench-ollama.ps1 -Model qwen2.5-coder:7b -NumCtx 4096

.NOTES
  Il prompt utilizzato è un'implementazione Python di una classe DoublyLinkedList (hardcoded).
  La temperatura è impostata su 0.
  Il warm-up utilizza 30 token.
  La misura utilizza 300 token.
  Richiede Ollama HTTP API su 127.0.0.1:11434.
#>
param(
  [Parameter(Mandatory=$true)][string]$Model,
  [Parameter(Mandatory=$true)][int]$NumCtx
)

$ErrorActionPreference = 'Stop'

function Invoke-OllamaRequest($uri, $body) {
  $retryStatus = @(500, 502, 503, 504)
  $maxAttempts = 3
  $backoffSeconds = @(1, 2)

  for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    try {
      return Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 600
    } catch {
      $ex = $_.Exception
      $typeName = $ex.GetType().Name
      $statusCode = 0
      if ($ex.Response -and $ex.Response.StatusCode) {
        $statusCode = [int]$ex.Response.StatusCode
      }
      if ($statusCode) {
        $isTransient = $statusCode -in $retryStatus
      } else {
        $isTransient = $typeName -in @('WebException', 'HttpRequestException', 'HttpResponseException')
      }
      if ($isTransient -and $attempt -lt $maxAttempts) {
        Start-Sleep -Seconds $backoffSeconds[$attempt - 1]
        continue
      }
      if ($isTransient) {
        throw "Transient failure after $maxAttempts attempts (last status=$statusCode, type=$typeName): $($ex.Message)"
      }
      throw
    }
  }
}

$prompt = @'
Write a Python implementation of a doubly-linked list class named DoublyLinkedList.
Include these methods: insert_head(value), insert_tail(value), delete_by_value(value),
find_by_value(value) returning the node or None, and __str__ for readable string
representation. Add a docstring to each method explaining its purpose, parameters,
and return value. Use type hints.
'@

$warmupPayload = @{
  model = $Model
  prompt = $prompt
  stream = $false
  options = @{ num_ctx = $NumCtx; num_predict = 30; temperature = 0 }
} | ConvertTo-Json -Depth 5

$measurePayload = @{
  model = $Model
  prompt = $prompt
  stream = $false
  options = @{ num_ctx = $NumCtx; num_predict = 300; temperature = 0 }
} | ConvertTo-Json -Depth 5

Write-Host "[$(Get-Date -Format HH:mm:ss)] Warm-up $Model @ ctx=$NumCtx ..."
$null = Invoke-OllamaRequest -Uri 'http://127.0.0.1:11434/api/generate' -Body $warmupPayload

Write-Host "[$(Get-Date -Format HH:mm:ss)] Measure $Model @ ctx=$NumCtx ..."
$r = Invoke-OllamaRequest -Uri 'http://127.0.0.1:11434/api/generate' -Body $measurePayload

$evalTps = [math]::Round(($r.eval_count / ($r.eval_duration / 1e9)), 2)
$promptTps = if ($r.prompt_eval_duration -gt 0) { [math]::Round(($r.prompt_eval_count / ($r.prompt_eval_duration / 1e9)), 2) } else { 0 }
$loadSec = [math]::Round(($r.load_duration / 1e9), 2)
$totalSec = [math]::Round(($r.total_duration / 1e9), 2)

"`n---`n"
"| Model | num_ctx | Eval tok/s | Prompt tok/s | eval_count | Load s | Total s |"
"|-------|---------|-----------:|-------------:|-----------:|-------:|--------:|"
"| ``$Model`` | $NumCtx | **$evalTps** | $promptTps | $($r.eval_count) | $loadSec | $totalSec |"
"`n"

Write-Host "`nollama ps (post-measure):"
ollama ps
