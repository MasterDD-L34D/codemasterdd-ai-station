# Setup Playwright + Chromium for ChatGPT Custom GPTs scraping
# Run once. Idempotent.

$ErrorActionPreference = "Stop"

Write-Host "=== Playwright setup for ChatGPT Custom GPTs scrape ===" -ForegroundColor Cyan

# Verify Node version
$nodeVersion = node --version
Write-Host "Node version: $nodeVersion"
if ([Version]($nodeVersion -replace '^v', '') -lt [Version]"18.0.0") {
    Write-Error "Node 18+ required. Current: $nodeVersion"
    exit 1
}

# Move to script dir
Set-Location $PSScriptRoot

# Install Node deps (Playwright)
if (-not (Test-Path package.json)) {
    Write-Error "package.json missing. Run from chatgpt-recovery/scripts/"
    exit 1
}

Write-Host "`nInstalling npm dependencies..." -ForegroundColor Yellow
npm install

# Install Chromium browser (required for headed mode with auth)
Write-Host "`nInstalling Chromium browser..." -ForegroundColor Yellow
npx playwright install chromium

# Verify install
Write-Host "`n=== Verification ===" -ForegroundColor Green
npx playwright --version
Write-Host "Chromium installed at: $(npx playwright browsers list 2>$null | Select-String 'chromium')"

Write-Host "`n=== Setup complete ===" -ForegroundColor Green
Write-Host "Next: run scrape-custom-gpts.js with --auth-mode initial first time" -ForegroundColor Yellow
Write-Host "  node scrape-custom-gpts.js --auth-mode initial --output <dir>"
Write-Host "Then subsequent runs use saved auth state automatically."
