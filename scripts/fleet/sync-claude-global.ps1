#requires -Version 5.1
<#
.SYNOPSIS
  Fleet sync of the ~/.claude governance SUBSET from the canonical host (Lenovo CODEMASTERDD) to a target (Ryzen).

.DESCRIPTION
  Syncs ONLY the governance subset: CLAUDE.md + rules/*.md + reference/*.md.
  Excludes machine-local state (memory/, sessions/, cache/, plugins/, settings.json) -- per fleet
  best-practice those stay per-machine (each machine accumulates its own auto-memory).
  Default is DRY-RUN; pass -Apply to actually push. One-way push: canonical (Lenovo) -> target.
  Backs up each target file before overwrite, then verifies line-count parity.

.NOTES
  Fleet rules: cross-PC mutating action -- run FROM the canonical owner (CODEMASTERDD) only.
  L-040: native ssh/scp stderr (PQ warning) is non-fatal -> ErrorActionPreference=Continue + gate on $LASTEXITCODE.
  Anti-pattern #9: idempotent write + verify on the real target (backup + re-check line counts).
  Extend -Files as the synced subset grows. NEVER add memory/ or settings.json (machine-local).

.EXAMPLE
  powershell -File scripts/fleet/sync-claude-global.ps1            # dry-run (default, safe)
  powershell -File scripts/fleet/sync-claude-global.ps1 -Apply     # push to Ryzen + verify
#>
param(
  # Ryzen SSH target: set $env:FLEET_RYZEN_SSH (real value in private store ~/.claude/reference/fleet-topology.md) or pass -Target.
  [string]$Target     = $env:FLEET_RYZEN_SSH,
  [string]$TargetHome = 'C:/Users/Vgit/.claude',
  [string]$SourceHome = "$env:USERPROFILE/.claude",
  [string[]]$Files    = @('CLAUDE.md', 'rules/encoding.md', 'reference/anti-patterns.md', 'reference/fleet-topology.md', 'skills/fleet-verify/SKILL.md'),
  [switch]$Apply,
  [switch]$NoBackup
)

# ssh/scp emit the PQ warning on stderr; under Stop that would abort. Gate on $LASTEXITCODE instead (L-040).
$ErrorActionPreference = 'Continue'
$stamp    = 'bak-sync-' + (Get-Date -Format 'yyyyMMdd')
$sourceId = $env:COMPUTERNAME + '/' + $env:USERNAME

Write-Host "[sync] source=$sourceId  target=$Target  apply=$Apply"

# Identity guard: only push FROM the canonical host (avoids pushing a stale clone over the canonical).
if ($env:COMPUTERNAME -ne 'CODEMASTERDD') {
  Write-Warning "[sync] ABORT: canonical host is CODEMASTERDD, you are on $sourceId. Run the push from the canonical owner."
  exit 2
}

if (-not $Target) {
  Write-Warning "[sync] ABORT: no target. Set `$env:FLEET_RYZEN_SSH or pass -Target (real value in ~/.claude/reference/fleet-topology.md)."
  exit 2
}

$issues = 0
foreach ($f in $Files) {
  $src = Join-Path $SourceHome $f
  if (-not (Test-Path -LiteralPath $src)) { Write-Warning "[skip] source missing: $src"; continue }
  $srcLines = (Get-Content -LiteralPath $src).Count
  $dst      = "$TargetHome/$f"
  $dstWin   = ($dst -replace '/', '\')
  Write-Host "[plan] $f  ($srcLines lines)  ->  $dst"

  if (-not $Apply) { continue }

  # ensure target subdir exists
  $dstDirWin = Split-Path $dstWin -Parent
  ssh -o BatchMode=yes $Target "if not exist `"$dstDirWin`" mkdir `"$dstDirWin`"" | Out-Null

  # backup target if present
  if (-not $NoBackup) {
    ssh -o BatchMode=yes $Target "if exist `"$dstWin`" copy /Y `"$dstWin`" `"$dstWin.$stamp`" >nul" | Out-Null
  }

  # push
  scp -o BatchMode=yes $src ("{0}:`"{1}`"" -f $Target, $dst) | Out-Null
  if ($LASTEXITCODE -ne 0) { Write-Warning "[FAIL] scp failed: $f"; $issues++; continue }

  # verify CONTENT parity on the real target via SHA256 (robust vs line-count/CRLF ambiguity; certutil = fast, no big-file transfer)
  $srcHash = (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash.ToLower()
  $tgtHash = ssh -o BatchMode=yes $Target "certutil -hashfile `"$dstWin`" SHA256" |
             Where-Object { $_ -match '^[0-9a-fA-F]{64}$' } | Select-Object -First 1
  if ($tgtHash) { $tgtHash = $tgtHash.Trim().ToLower() }
  if ($tgtHash -eq $srcHash) { Write-Host "[ok]   $f synced + verified ($srcLines lines, sha256 match)" }
  else { Write-Warning "[MISMATCH] $f  sha256 src=$srcHash tgt=$tgtHash"; $issues++ }
}

if (-not $Apply) {
  Write-Host "[sync] DRY-RUN complete (no changes). Re-run with -Apply to push."
  exit 0
}
if ($issues -gt 0) { Write-Warning "[sync] DONE with $issues issue(s) -- review above."; exit 1 }
Write-Host "[sync] DONE -- all files synced + verified."
exit 0
