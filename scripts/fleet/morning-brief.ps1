<#
.SYNOPSIS
Morning brief R0 -- deterministic, read-only fleet snapshot (no LLM).

.DESCRIPTION
ADR-0044 gap G1, governor earn-path rung R0 (report-only). Aggregates:
open PRs across monitored repos (gh), local scheduled-task health, JOURNAL
and GOALS currency. Writes logs/morning-brief/<date>.md (gitignored) and
prints to stdout. NEVER writes outside logs/, never commits, never merges.

Cross-fleet: safe on BOTH PCs (local-log only, no shared artifact -> no
single-owner constraint, unlike jules-daily-digest).

L-040: native commands run under ErrorActionPreference=Continue and are
gated on $LASTEXITCODE (git/gh stderr under Stop = false-fail).
#>
[CmdletBinding()]
param(
  [string]$OutDir = 'C:\dev\codemasterdd-ai-station\logs\morning-brief',
  [string]$Owner = 'MasterDD-L34D',
  [string[]]$Repos = @('codemasterdd-ai-station', 'Game', 'Game-Godot-v2', 'Game-Database', 'vault'),
  [switch]$NoFile
)
$ErrorActionPreference = 'Continue'
$today = Get-Date -Format 'yyyy-MM-dd'
$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# Morning brief -- $today ($env:COMPUTERNAME)")
$lines.Add('')
$lines.Add('> R0 report-only (ADR-0044 G1). Deterministic aggregator, no LLM, no writes outside logs/.')
$lines.Add('')

# --- Open PRs per repo (gh, degraded-not-fatal) ---
$lines.Add('## Open PRs')
foreach ($r in $Repos) {
  $json = gh pr list --repo "$Owner/$r" --state open --json 'number,title,createdAt,author' --limit 20 2>$null
  if ($LASTEXITCODE -ne 0 -or -not $json) {
    $lines.Add("- ${r}: DEGRADED (gh error or unauthenticated)")
    continue
  }
  $prs = $json | ConvertFrom-Json
  if (-not $prs -or $prs.Count -eq 0) {
    $lines.Add("- ${r}: 0 open")
  } else {
    $lines.Add("- ${r}: $($prs.Count) open")
    foreach ($p in $prs) {
      $age = [int]((Get-Date) - [datetime]$p.createdAt).TotalDays
      $lines.Add("  - #$($p.number) $($p.title) ($($p.author.login), ${age}d)")
    }
  }
}
$lines.Add('')

# --- Scheduled task health ---
$lines.Add('## Scheduled tasks')
foreach ($tn in @('jules-daily-digest', 'morning-brief')) {
  $t = Get-ScheduledTask -TaskName $tn -ErrorAction SilentlyContinue
  if (-not $t) { $lines.Add("- ${tn}: not registered on this PC"); continue }
  $info = Get-ScheduledTaskInfo -TaskName $tn -ErrorAction SilentlyContinue
  $res = 'n/a'
  if ($info) {
    if ($info.LastTaskResult -eq 0) {
      $res = "last run $($info.LastRunTime), result OK"
    } else {
      $hex = '0x{0:X8}' -f $info.LastTaskResult
      $res = "last run $($info.LastRunTime), result WARN $hex"
    }
  }
  $lines.Add("- ${tn}: $($t.State), $res")
}
$lines.Add('')

# --- Doc currency (JOURNAL top entry + GOALS last refresh) ---
$lines.Add('## Doc currency')
$repoRoot = 'C:\dev\codemasterdd-ai-station'
$journal = Join-Path $repoRoot 'JOURNAL.md'
if (Test-Path $journal) {
  $m = Select-String -Path $journal -Pattern '^## (\d{4}-\d{2}-\d{2})' | Select-Object -First 1
  if ($m) {
    $d = [datetime]$m.Matches[0].Groups[1].Value
    $lines.Add("- JOURNAL top entry: $($m.Matches[0].Groups[1].Value) ($([int]((Get-Date) - $d).TotalDays)d ago)")
  } else { $lines.Add('- JOURNAL: no dated entry found (DEGRADED)') }
} else { $lines.Add('- JOURNAL.md missing (DEGRADED)') }
$goals = Join-Path $repoRoot 'GOALS.md'
if (Test-Path $goals) {
  $g = Select-String -Path $goals -Pattern 'Last refresh: \*\*(\d{4}-\d{2}-\d{2})' | Select-Object -First 1
  if ($g) {
    $d = [datetime]$g.Matches[0].Groups[1].Value
    $lines.Add("- GOALS last refresh: $($g.Matches[0].Groups[1].Value) ($([int]((Get-Date) - $d).TotalDays)d ago)")
  } else { $lines.Add('- GOALS: refresh marker not found (DEGRADED)') }
} else { $lines.Add('- GOALS.md missing (DEGRADED)') }
$lines.Add('')

# --- Emit ---
$text = $lines -join [Environment]::NewLine
Write-Host $text
if (-not $NoFile) {
  if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }
  $outPath = Join-Path $OutDir "$today.md"
  Set-Content -Path $outPath -Value $text -Encoding utf8
  Write-Host "[morning-brief] saved to $outPath"
}
exit 0
