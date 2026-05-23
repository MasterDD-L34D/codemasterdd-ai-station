<#
.SYNOPSIS
    Smoke test di integrazione: verifica dashboard + LiteLLM + Langfuse + OpenCode
.DESCRIPTION
    Testa ogni componente dello stack e riporta stato OK/FAIL per ciascuno.
    Exit code 0 = tutto ok, 1 = uno o piu' test falliti.
#>

$ErrorActionPreference = "Continue"
$passed = 0
$failed = 0

function Test-Step($name, $script) {
    try {
        $result = & $script
        if ($result) {
            Write-Host "[PASS] $name" -ForegroundColor Green
            $script:passed++
        } else {
            Write-Host "[FAIL] $name" -ForegroundColor Red
            $script:failed++
        }
    } catch {
        $errMsg = $_.Exception.Message
        Write-Host "[FAIL] $name - $errMsg" -ForegroundColor Red
        $script:failed++
    }
}

# Source keys.env for Tavily check
$KeysFile = "$env:USERPROFILE\.config\api-keys\keys.env"
if (Test-Path $KeysFile) {
    Get-Content $KeysFile | ForEach-Object {
        if ($_ -match '^([A-Z_][A-Z0-9_]*)=(.*)$') {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
        }
    }
}

Write-Host "=== Smoke Test Integrazione ===" -ForegroundColor Cyan
Write-Host "Data: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n" -ForegroundColor Cyan

# 1. Dashboard health
Test-Step "Dashboard /api/health" {
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:8080/api/health" -ErrorAction Stop
    ($r.status -eq "ok") -and ($r.app -eq "dogfood-ui")
}

# 2. Dashboard -- litellm reachable
Test-Step "Dashboard - litellm reachable" {
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:8080/api/health" -ErrorAction Stop
    $r.litellm.reachable -eq $true
}

# 3. Dashboard -- langfuse reachable
Test-Step "Dashboard - langfuse reachable" {
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:8080/api/health" -ErrorAction Stop
    $r.langfuse.reachable -eq $true
}

# 4. Dashboard -- opencode config exists
Test-Step "Dashboard - opencode config exists" {
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:8080/api/health" -ErrorAction Stop
    $r.opencode.config_exists -eq $true
}

# 5. Dashboard -- tavily configured (from keys.env)
Test-Step "Dashboard - tavily configured" {
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:8080/api/health" -ErrorAction Stop
    $r.tavily.configured -eq $true
}

# 6. Dashboard -- centralized keys.env detected on disk
Test-Step "Dashboard - api keys file present" {
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:8080/api/health" -ErrorAction Stop
    $r.opencode.api_keys_file_present -eq $true
}

# 7. LiteLLM readiness
Test-Step "LiteLLM /health/readiness" {
    $r = Invoke-RestMethod -Uri "http://localhost:4000/health/readiness" -ErrorAction Stop
    ($r.status -eq "healthy") -and ($r.db -eq "connected")
}

# 8. Langfuse health
Test-Step "Langfuse /api/public/health" {
    $r = Invoke-RestMethod -Uri "http://localhost:3000/api/public/health" -ErrorAction Stop
    $r.status -eq "OK"
}

# 9. LiteLLM proxy test -- list models (richiede virtual key o master key)
Test-Step "LiteLLM proxy - model list" {
    $headers = @{ Authorization = "Bearer sk-local-masterkey-change-me" }
    $r = Invoke-RestMethod -Uri "http://localhost:4000/models" -Headers $headers -ErrorAction Stop
    ($r.data -and $r.data.Count -ge 1)
}

# 10. LiteLLM proxy -- chat completion via Ollama (richiede master key)
Test-Step "LiteLLM proxy - chat completion (ollama-cosmetic-7b)" {
    $headers = @{ Authorization = "Bearer sk-local-masterkey-change-me" }
    $body = @{
        model = "ollama-cosmetic-7b"
        messages = @(@{ role = "user"; content = "Rispondi solo 'ok'." })
        max_tokens = 10
    } | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "http://localhost:4000/chat/completions" -Method Post -Body $body -Headers $headers -ContentType "application/json" -ErrorAction Stop
    ($r.choices -and $r.choices.Count -ge 1 -and $r.choices[0].message.content)
}

Write-Host "`n=== Risultati: $passed passed, $failed failed ===" -ForegroundColor Cyan

if ($failed -gt 0) {
    exit 1
}
exit 0
