<#
.SYNOPSIS
  Install Windows shortcuts for Cross-repo Dashboard v0.2.

.DESCRIPTION
  Creates:
  - Desktop .lnk shortcut launching dashboard + browser (A1)
  - Optional Startup folder .lnk for autostart on login (A3)
  - Optional system tray launcher (.lnk to tray.pyw) (A4)

.PARAMETER Desktop
  Install desktop shortcut (default true)

.PARAMETER Autostart
  Install Startup folder entry for autostart on login

.PARAMETER Tray
  Install tray launcher in Startup folder (alternative to -Autostart)

.PARAMETER Uninstall
  Remove all installed shortcuts

.EXAMPLE
  .\install-shortcut.ps1 -Desktop -Tray
  (recommended: desktop icon + tray autostart)

.EXAMPLE
  .\install-shortcut.ps1 -Uninstall
#>

param(
  [switch]$Desktop = $true,
  [switch]$Autostart,
  [switch]$Tray,
  [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'

$dashboardDir = "C:\dev\codemasterdd-ai-station\apps\cross-repo-dashboard"
$batLauncher = "$dashboardDir\start-dashboard.cmd"
$trayLauncher = "$dashboardDir\tray.pyw"
$iconPath = "$env:SystemRoot\System32\imageres.dll,109"  # Generic dashboard icon

$desktopPath = [Environment]::GetFolderPath("Desktop")
$startupPath = [Environment]::GetFolderPath("Startup")

$desktopShortcut = "$desktopPath\Cross-repo Dashboard.lnk"
$startupShortcut = "$startupPath\Cross-repo Dashboard.lnk"
$trayStartupShortcut = "$startupPath\Cross-repo Dashboard Tray.lnk"

function New-Shortcut($Path, $Target, $Arguments = "", $WorkingDir = "", $Description = "", $Icon = "") {
  $shell = New-Object -ComObject WScript.Shell
  $sc = $shell.CreateShortcut($Path)
  $sc.TargetPath = $Target
  if ($Arguments) { $sc.Arguments = $Arguments }
  if ($WorkingDir) { $sc.WorkingDirectory = $WorkingDir }
  if ($Description) { $sc.Description = $Description }
  if ($Icon) { $sc.IconLocation = $Icon }
  $sc.Save()
  Write-Host "  Created: $Path" -ForegroundColor Green
}

if ($Uninstall) {
  Write-Host "Uninstalling shortcuts..." -ForegroundColor Yellow
  foreach ($p in @($desktopShortcut, $startupShortcut, $trayStartupShortcut)) {
    if (Test-Path $p) {
      Remove-Item $p -Force
      Write-Host "  Removed: $p" -ForegroundColor Green
    }
  }
  Write-Host "Uninstall complete." -ForegroundColor Green
  exit 0
}

# Sanity check launcher exists
if (-not (Test-Path $batLauncher)) {
  Write-Host "FAIL: launcher not found at $batLauncher" -ForegroundColor Red
  exit 1
}

Write-Host "=== Cross-repo Dashboard shortcut installer ===" -ForegroundColor Cyan

if ($Desktop) {
  Write-Host "Installing desktop shortcut..." -ForegroundColor Cyan
  New-Shortcut -Path $desktopShortcut `
    -Target $batLauncher `
    -WorkingDir $dashboardDir `
    -Description "Cross-repo Dashboard v0.2 -- Component 1 codemasterdd" `
    -Icon $iconPath
}

if ($Autostart) {
  Write-Host "Installing autostart (Startup folder, plain Flask)..." -ForegroundColor Cyan
  New-Shortcut -Path $startupShortcut `
    -Target $batLauncher `
    -WorkingDir $dashboardDir `
    -Description "Cross-repo Dashboard autostart" `
    -Icon $iconPath
}

if ($Tray) {
  if (-not (Test-Path $trayLauncher)) {
    Write-Host "WARN: tray.pyw not found, skipping tray autostart" -ForegroundColor Yellow
  } else {
    Write-Host "Installing tray autostart (Startup folder, system tray icon)..." -ForegroundColor Cyan
    # Use pythonw.exe for windowless execution
    $pythonwPath = (Get-Command pythonw -ErrorAction SilentlyContinue).Source
    if (-not $pythonwPath) { $pythonwPath = "pythonw.exe" }
    New-Shortcut -Path $trayStartupShortcut `
      -Target $pythonwPath `
      -Arguments "`"$trayLauncher`"" `
      -WorkingDir $dashboardDir `
      -Description "Cross-repo Dashboard system tray launcher" `
      -Icon $iconPath
  }
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Write-Host "Verify desktop: Test-Path '$desktopShortcut' => $(Test-Path $desktopShortcut)"
Write-Host "Verify startup: Test-Path '$startupShortcut' => $(Test-Path $startupShortcut)"
Write-Host "Verify tray:    Test-Path '$trayStartupShortcut' => $(Test-Path $trayStartupShortcut)"
Write-Host ""
Write-Host "To uninstall: .\install-shortcut.ps1 -Uninstall"
exit 0
