<#
.SYNOPSIS
  Benchmark singola run cloud provider (OpenAI-compatible API), parse metriche native.

.DESCRIPTION
  Esegue 1 warm-up (max_tokens 30) + 1 misura (max_tokens 300) contro OpenAI-compatible
  endpoint. Stampa riga markdown pronta per append al log bench. Supporta provider
  Groq, Cerebras, OpenAI. Gemini ha API format diverso (non supportato qui).

.PARAMETER Provider
  Nome provider. Supported: groq, cerebras, openai.

.PARAMETER Model
  Model name per il provider (es. "llama-3.3-70b-versatile" per Groq).

.PARAMETER ApiKey
  API key plaintext (o via env var, se non specificata legge da <PROVIDER>_API_KEY).

.EXAMPLE
  .\bench-cloud.ps1 -Provider groq -Model llama-3.3-70b-versatile

.EXAMPLE
  .\bench-cloud.ps1 -Provider cerebras -Model llama3.1-8b

.EXAMPLE
  .\bench-cloud.ps1 -Provider openai -Model gpt-4o-mini

.NOTES
  Prompt identico a bench-ollama.ps1 (Python DoublyLinkedList hardcoded, temperature 0).
  Richiede env var <PROVIDER_UPPER>_API_KEY o param -ApiKey esplicito.
  Metriche usage.completion_tokens / usage.completion_time per Groq (nativo),
  calcolo manuale wall-clock per altri provider.
#>
param(
  [Parameter(Mandatory=$true)][ValidateSet('groq','cerebras','openai')][string]$Provider,
  [Parameter(Mandatory=$true)][string]$Model,
  [string]$ApiKey
)

$ErrorActionPreference = 'Stop'

$endpoints = @{
  groq     = 'https://api.groq.com/openai/v1/chat/completions'
  cerebras = 'https://api.cerebras.ai/v1/chat/completions'
  openai   = 'https://api.openai.com/v1/chat/completions'
}

$envKey = @{
  groq     = 'GROQ_API_KEY'
  cerebras = 'CEREBRAS_API_KEY'
  openai   = 'OPENAI_API_KEY'
}

if (-not $ApiKey) {
  $ApiKey = [Environment]::GetEnvironmentVariable($envKey[$Provider], 'Process')
  if (-not $ApiKey) {
    Write-Error "API key not provided and env var $($envKey[$Provider]) not set"
    exit 1
  }
}

$url = $endpoints[$Provider]
$headers = @{
  'Authorization' = "Bearer $ApiKey"
  'Content-Type'  = 'application/json'
}

$prompt = @'
Write a Python implementation of a doubly-linked list class named DoublyLinkedList.
Include these methods: insert_head(value), insert_tail(value), delete_by_value(value),
find_by_value(value) returning the node or None, and __str__ for readable string
representation. Add a docstring to each method explaining its purpose, parameters,
and return value. Use type hints.
'@

function Invoke-Bench($maxTokens) {
  $payload = @{
    model       = $Model
    messages    = @(@{ role = 'user'; content = $prompt })
    max_tokens  = $maxTokens
    temperature = 0
  } | ConvertTo-Json -Depth 5

  # Retry on transient: HTTP 429/5xx, WebException, HttpRequestException.
  # PS 5.1 Invoke-RestMethod raises WebException with .Response.StatusCode (HttpStatusCode enum);
  # PS 7+ raises HttpResponseException. Handle both.
  $retryStatus = @(429, 500, 502, 503, 504)
  $maxAttempts = 3
  $backoffSeconds = @(1, 2)

  for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    try {
      $sw = [Diagnostics.Stopwatch]::StartNew()
      $r = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $payload -TimeoutSec 300
      $sw.Stop()
      return @{ response = $r; wallMs = $sw.ElapsedMilliseconds }
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
        throw "Transient failure after $maxAttempts attempts for $Provider/$Model (last status=$statusCode, type=$typeName): $($ex.Message)"
      }
      throw
    }
  }
}

Write-Host "[$(Get-Date -Format HH:mm:ss)] Warm-up $Provider/$Model ..."
$null = Invoke-Bench 30

Write-Host "[$(Get-Date -Format HH:mm:ss)] Measure $Provider/$Model ..."
$m = Invoke-Bench 300
$r = $m.response
$wallMs = $m.wallMs

$completionTokens = $r.usage.completion_tokens
$promptTokens     = $r.usage.prompt_tokens

# Groq has usage.completion_time (seconds); others need wall-clock approximation
$completionSec = if ($r.usage.completion_time) {
  [double]$r.usage.completion_time
} else {
  $wallMs / 1000.0
}

$evalTps = if ($completionSec -gt 0) { [math]::Round($completionTokens / $completionSec, 2) } else { 0 }
$wallSec = [math]::Round($wallMs / 1000.0, 2)

"`n---`n"
"| Provider/Model | Eval tok/s | Completion tok | Prompt tok | Wall s | Source |"
"|----------------|-----------:|---------------:|-----------:|-------:|--------|"
$source = if ($r.usage.completion_time) { 'usage.completion_time' } else { 'wall-clock approx' }
"| ``$Provider/$Model`` | **$evalTps** | $completionTokens | $promptTokens | $wallSec | $source |"
"`n"
