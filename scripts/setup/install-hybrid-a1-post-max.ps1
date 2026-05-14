<#
.SYNOPSIS
  Install Hybrid A1 post-Max orchestration architecture (ADR-0030).

.DESCRIPTION
  Components:
  1. opencode-with-claude plugin (Meridian bridge per Pro subscription)
  2. Gemini CLI free tier 1000 req/day baseline
  3. OpenRouter config opzionale emergency overflow
  4. OpenCode config update con nuovi provider

  Pre-req:
  - Eduardo subscribed Claude Pro $20/mo (manual via anthropic.com/claude/upgrade)
  - OpenCode v1.14.41+ installed (verified: C:/Users/edusc/AppData/Roaming/npm/opencode.cmd)

.PARAMETER SkipPlugin
  Skip opencode-with-claude plugin install (if already installed)

.PARAMETER SkipGemini
  Skip Gemini CLI install (if Eduardo doesn't want free tier)

.PARAMETER SkipOpenRouter
  Skip OpenRouter config (if Eduardo doesn't want emergency overflow)

.PARAMETER DryRun
  Print actions without executing

.EXAMPLE
  .\install-hybrid-a1-post-max.ps1
  .\install-hybrid-a1-post-max.ps1 -DryRun
#>

param(
  [switch]$SkipPlugin,
  [switch]$SkipGemini,
  [switch]$SkipOpenRouter,
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

Write-Host "=== Hybrid A1 post-Max setup (ADR-0030) ===" -ForegroundColor Cyan
Write-Host ""

# ---------------------------------------------------------------------------
# Pre-flight check
# ---------------------------------------------------------------------------
Write-Host "[Pre-flight] Verify OpenCode installed..." -ForegroundColor Cyan
$opencodeBin = "C:\Users\edusc\AppData\Roaming\npm\opencode.cmd"
if (-not (Test-Path $opencodeBin)) {
  Write-Host "FAIL: OpenCode not found at $opencodeBin" -ForegroundColor Red
  Write-Host "Install: npm install -g opencode-ai" -ForegroundColor Yellow
  Write-Host "  (npm package name is 'opencode-ai' NOT 'opencode')" -ForegroundColor Yellow
  exit 1
}
Write-Host "  PASS OpenCode binary exists" -ForegroundColor Green

# Pro subscription warning
Write-Host ""
Write-Host "[Pre-flight] Claude Pro subscription required" -ForegroundColor Yellow
Write-Host "  Verify https://www.anthropic.com/claude/upgrade Pro `$20/mo active"
Write-Host "  Without Pro, Meridian bridge cannot route to subscription tier."
Write-Host "  Continuing setup anyway (Eduardo subscribe when convenient)."
Write-Host ""

# ---------------------------------------------------------------------------
# 1. opencode-with-claude plugin (Meridian bridge)
# ---------------------------------------------------------------------------
if (-not $SkipPlugin) {
  Write-Host "[1/3] opencode-with-claude plugin install + opencode.json registration..." -ForegroundColor Cyan
  if ($DryRun) {
    Write-Host "  DRY-RUN: npm install -g opencode-with-claude"
    Write-Host "  DRY-RUN: update opencode.json -> plugin[]=opencode-with-claude + anthropic provider via 127.0.0.1:3456"
  } else {
    # Step 1a: install npm package
    npm install -g opencode-with-claude 2>&1 | Out-String | Write-Host
    Write-Host "  Plugin npm package installed." -ForegroundColor Green

    # Step 1b: register plugin in opencode.json (REQUIRED per plugin README, P2.1 Codex fix)
    # Without this step, OpenCode won't load the plugin -> Meridian bridge inactive
    $opencodeJsonPath = "$env:USERPROFILE\.config\opencode\opencode.json"
    if (-not (Test-Path $opencodeJsonPath)) {
      Write-Host "  WARN: opencode.json not found at $opencodeJsonPath" -ForegroundColor Yellow
      Write-Host "  Skipping registration. Run after opencode session creates config." -ForegroundColor Yellow
    } else {
      Write-Host "  Updating opencode.json plugin + anthropic provider..."
      try {
        $cfg = Get-Content $opencodeJsonPath -Raw | ConvertFrom-Json
        # Backup
        Copy-Item $opencodeJsonPath "$opencodeJsonPath.bak-$(Get-Date -Format yyyyMMddHHmmss)" -Force
        Write-Host "  Backup: $opencodeJsonPath.bak-*" -ForegroundColor Green

        # Add plugin array (idempotent)
        $pluginName = "opencode-with-claude"
        if ($cfg.PSObject.Properties.Name -contains "plugin") {
          if ($cfg.plugin -notcontains $pluginName) {
            $cfg.plugin = @($cfg.plugin) + $pluginName
          }
        } else {
          $cfg | Add-Member -MemberType NoteProperty -Name "plugin" -Value @($pluginName) -Force
        }

        # Add anthropic provider via Meridian local proxy (port 3456 default)
        if (-not $cfg.provider) {
          $cfg | Add-Member -MemberType NoteProperty -Name "provider" -Value (New-Object PSObject) -Force
        }
        $anthropicCfg = @{
          options = @{
            baseURL = "http://127.0.0.1:3456"
            apiKey = "dummy"
          }
        } | ConvertTo-Json -Depth 10 | ConvertFrom-Json
        $cfg.provider | Add-Member -MemberType NoteProperty -Name "anthropic" -Value $anthropicCfg -Force

        # Write
        $cfg | ConvertTo-Json -Depth 20 | Set-Content $opencodeJsonPath -Encoding UTF8
        Write-Host "  opencode.json updated:" -ForegroundColor Green
        Write-Host "    plugin: [...opencode-with-claude...]"
        Write-Host "    provider.anthropic: { baseURL: http://127.0.0.1:3456, apiKey: 'dummy' }"
        Write-Host "  Meridian bridge will auto-start on next 'opencode' session." -ForegroundColor Green
      } catch {
        $msg = $_.Exception.Message
        Write-Host "  FAIL JSON update: $msg" -ForegroundColor Red
        Write-Host "  Eduardo manual: edit $opencodeJsonPath and add:" -ForegroundColor Yellow
        Write-Host '    "plugin": ["opencode-with-claude"],' -ForegroundColor Yellow
        Write-Host '    "provider": { "anthropic": { "options": { "baseURL": "http://127.0.0.1:3456", "apiKey": "dummy" } } }' -ForegroundColor Yellow
      }
    }
  }
}

# ---------------------------------------------------------------------------
# 2. Gemini CLI free tier
# ---------------------------------------------------------------------------
if (-not $SkipGemini) {
  Write-Host ""
  Write-Host "[2/3] Gemini CLI install..." -ForegroundColor Cyan
  $geminiCheck = Get-Command gemini -ErrorAction SilentlyContinue
  if ($geminiCheck) {
    Write-Host "  Gemini CLI already installed: $($geminiCheck.Source)" -ForegroundColor Green
  } else {
    if ($DryRun) {
      Write-Host "  DRY-RUN: npm install -g @google/gemini-cli"
    } else {
      Write-Host "  Installing @google/gemini-cli..."
      npm install -g @google/gemini-cli 2>&1 | Out-String | Write-Host
    }
  }
  Write-Host "  Post-install: gemini auth login -> Google account free tier"
  Write-Host "  Quota: 1000 req/day Gemini 2.5 Pro 1M context"
}

# ---------------------------------------------------------------------------
# 3. OpenRouter config opzionale
# ---------------------------------------------------------------------------
if (-not $SkipOpenRouter) {
  Write-Host ""
  Write-Host "[3/3] OpenRouter emergency overflow config..." -ForegroundColor Cyan
  $keysEnv = "$env:USERPROFILE\.config\api-keys\keys.env"
  $hasKey = (Test-Path $keysEnv) -and (Select-String -Path $keysEnv -Pattern "OPENROUTER_API_KEY" -Quiet)
  if ($hasKey) {
    Write-Host "  OPENROUTER_API_KEY already in keys.env" -ForegroundColor Green
  } else {
    Write-Host "  Eduardo manual:"
    Write-Host "    1. Sign up https://openrouter.ai (free, BYOK pay-per-use)"
    Write-Host "    2. Get API key from dashboard"
    Write-Host "    3. Append a $keysEnv :"
    Write-Host "       OPENROUTER_API_KEY=sk-or-v1-..."
    Write-Host "    4. Update opencode.json provider 'openrouter' (template fornito in docs/cross-repo)"
  }
}

# ---------------------------------------------------------------------------
# Post-setup instructions
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "=== Setup completed ===" -ForegroundColor Green
Write-Host ""
Write-Host 'Next steps Eduardo manual:'
Write-Host '  1. Subscribe Claude Pro $20/mo: https://www.anthropic.com/claude/upgrade'
Write-Host '  2. Test OpenCode + Meridian + Pro: opencode --> select Claude Opus/Sonnet'
Write-Host '  3. Auth Gemini CLI: gemini auth login'
Write-Host '  4. (Optional) OpenRouter signup if want overflow'
Write-Host ''
Write-Host 'Validation criteria (1 mese post-Max 19/5 to 19/6):'
Write-Host '  - Cost actual le $50/mo'
Write-Host '  - Daily orchestration feasibility empirical pass'
Write-Host '  - Methodology cite count ge 80% baseline'
Write-Host '  - Sub-agent dispatch viability n ge 2 invocations'
Write-Host ''
Write-Host 'Reference: docs/adr/0030-post-max-orchestration-hybrid-a1.md'
exit 0
