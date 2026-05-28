<#
.SYNOPSIS
One-shot helper: copy C:\dev\_mirror-backup\ bare mirrors to an external drive.

.DESCRIPTION
Complements the scheduled task `codemasterdd-mirror-backup` (which keeps the
local bare mirrors fresh against GitHub account-loss). This script handles
disk-loss insurance: periodic mirror-to-external-drive copy.

Runbook: docs/runbook/mirror-external-drive.md

NOT a scheduled task. Manual invocation only (drive connected on demand).
Idempotent via robocopy /MIR (mirror mode: source state replicated exactly).

.PARAMETER Destination
Absolute path on the external drive where the bare mirrors live. Will be
created if missing.

.PARAMETER Source
Local bare-mirror root. Defaults to C:\dev\_mirror-backup.

.PARAMETER DryRun
Print what would be copied without writing.

.EXAMPLE
.\scripts\backup\copy-mirror-to-external.ps1 -Destination E:\codemasterdd-mirror-backup

.EXAMPLE
.\scripts\backup\copy-mirror-to-external.ps1 -Destination E:\codemasterdd-mirror-backup -DryRun
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$Destination,
  [string]$Source = 'C:\dev\_mirror-backup',
  [switch]$DryRun
)

# Avoid Stop here: robocopy writes progress to stderr-ish channel + uses non-zero
# exit codes for benign cases (1 = files copied, 2 = extra files, 3 = both).
# Treat <8 as success per robocopy convention.
$ErrorActionPreference = 'Continue'

Write-Host "=== Mirror -> external drive ==="
Write-Host "Source:      $Source"
Write-Host "Destination: $Destination"
Write-Host "DryRun:      $DryRun"
Write-Host ""

# Pre-flight checks.
if (-not (Test-Path $Source)) {
  Write-Error "Source missing: $Source. Run the scheduled task `codemasterdd-mirror-backup` first to populate it."
  exit 2
}

$bareCount = (Get-ChildItem -Path $Source -Directory | Where-Object Name -Like '*.git').Count
if ($bareCount -eq 0) {
  Write-Error "Source has no *.git directories: $Source. Bare mirrors not populated."
  exit 3
}
Write-Host "Source bare mirrors: $bareCount"

# Drive root must exist (drive connected).
$drive = (Split-Path -Qualifier $Destination)
if (-not (Test-Path "$drive\")) {
  Write-Error "Drive root not accessible: $drive (drive not connected?)"
  exit 4
}

# Ensure destination dir exists.
if (-not (Test-Path $Destination)) {
  if ($DryRun) {
    Write-Host "[DRY] would mkdir: $Destination"
  } else {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Write-Host "[OK] created: $Destination"
  }
}

# robocopy options:
#   /MIR  -- mirror (purge files not in source)
#   /R:2  -- retry 2x on locked file
#   /W:5  -- wait 5sec between retries
#   /NFL /NDL -- no per-file / per-dir log (quieter output)
#   /NP   -- no progress bar
#   /L    -- list-only (DryRun)
$robocopyArgs = @($Source, $Destination, '/MIR', '/R:2', '/W:5', '/NFL', '/NDL', '/NP')
if ($DryRun) { $robocopyArgs += '/L' }

Write-Host ""
Write-Host "Running: robocopy $($robocopyArgs -join ' ')"
Write-Host ""

& robocopy @robocopyArgs

# robocopy exit codes:
#   0    -- no change
#   1    -- some files copied (success)
#   2    -- extra files/dirs detected (no copy needed)
#   3    -- 1+2
#   >=4  -- mismatches / failed copies / fatal
$rc = $LASTEXITCODE
Write-Host ""

if ($rc -lt 8) {
  Write-Host "[OK] robocopy completed (exit $rc, benign per convention)."
} else {
  Write-Error "[FAIL] robocopy exit $rc (>=8 = mismatch / failed copy / fatal)."
  exit 1
}

# Post-copy verify.
if (-not $DryRun) {
  $dstBareCount = (Get-ChildItem -Path $Destination -Directory | Where-Object Name -Like '*.git').Count
  Write-Host ""
  Write-Host "=== Verify ==="
  Write-Host "Source bare mirrors:      $bareCount"
  Write-Host "Destination bare mirrors: $dstBareCount"

  if ($dstBareCount -ne $bareCount) {
    Write-Error "Bare-mirror count mismatch ($bareCount source vs $dstBareCount dest). Investigate."
    exit 5
  }

  # Sample HEAD check on first bare mirror found.
  $sample = Get-ChildItem -Path $Destination -Directory | Where-Object Name -Like '*.git' | Select-Object -First 1
  if ($sample) {
    $head = (git -C $sample.FullName rev-parse HEAD 2>$null)
    Write-Host "Sample HEAD ($($sample.Name)): $head"
  }
}

Write-Host ""
Write-Host "Done. Eject the drive cleanly when finished."
exit 0
