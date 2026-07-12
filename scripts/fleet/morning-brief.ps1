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
$prDegraded = 0
foreach ($r in $Repos) {
  $json = gh pr list --repo "$Owner/$r" --state open --json 'number,title,createdAt,author' --limit 20 2>$null
  if ($LASTEXITCODE -ne 0 -or -not $json) {
    $lines.Add("- ${r}: DEGRADED (gh error or unauthenticated)")
    $prDegraded++
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
if ($prDegraded -eq $Repos.Count -and $Repos.Count -gt 0) {
  $lines.Add('')
  $lines.Add('> WARN: every repo returned DEGRADED -- gh likely unauthenticated on this PC. PR section is unreliable.')
}
$lines.Add('')

# --- Scheduled task health ---
$lines.Add('## Scheduled tasks')
# Only genuinely-benign steady states are info: READY (0x41300), RUNNING
# (0x41301), HAS_NOT_RUN_YET (0x41303). Everything else stays WARN on purpose --
# DISABLED (0x41302), NO_MORE_RUNS (0x41304), and especially NOT_SCHEDULED
# (0x41305) / TERMINATED (0x41306) / NO_VALID_TRIGGERS (0x41307) mean the task
# is broken, which is exactly what this health line must surface, not hide.
$benignResults = @(0x00041300, 0x00041301, 0x00041303)
foreach ($tn in @('jules-daily-digest', 'morning-brief')) {
  $t = Get-ScheduledTask -TaskName $tn -ErrorAction SilentlyContinue
  if (-not $t) { $lines.Add("- ${tn}: not registered on this PC"); continue }
  $info = Get-ScheduledTaskInfo -TaskName $tn -ErrorAction SilentlyContinue
  $res = 'n/a'
  if ($info) {
    $code = $info.LastTaskResult
    if ($code -eq 0) {
      $res = "last run $($info.LastRunTime), result OK"
    } elseif ($benignResults -contains $code) {
      $hex = '0x{0:X8}' -f $code
      $res = "last run $($info.LastRunTime), status $hex (info)"
    } else {
      $hex = '0x{0:X8}' -f $code
      $res = "last run $($info.LastRunTime), result WARN $hex"
    }
  }
  $lines.Add("- ${tn}: $($t.State), $res")
}
$lines.Add('')

# --- Doc currency (JOURNAL top entry + GOALS last refresh) ---
$lines.Add('## Doc currency')
$repoRoot = 'C:\dev\codemasterdd-ai-station'
# TryParse (not [datetime] cast): a regex-matching-but-invalid date must
# DEGRADE this line, never throw and kill the whole brief (degrade-don't-die).
$journal = Join-Path $repoRoot 'JOURNAL.md'
if (Test-Path $journal) {
  $m = Select-String -Path $journal -Pattern '^## (\d{4}-\d{2}-\d{2})' | Select-Object -First 1
  $d = [datetime]::MinValue
  if ($m -and [datetime]::TryParse($m.Matches[0].Groups[1].Value, [ref]$d)) {
    $lines.Add("- JOURNAL top entry: $($m.Matches[0].Groups[1].Value) ($([int]((Get-Date) - $d).TotalDays)d ago)")
  } else { $lines.Add('- JOURNAL: no valid dated entry found (DEGRADED)') }
} else { $lines.Add('- JOURNAL.md missing (DEGRADED)') }
$goals = Join-Path $repoRoot 'GOALS.md'
if (Test-Path $goals) {
  $g = Select-String -Path $goals -Pattern 'Last refresh: \*\*(\d{4}-\d{2}-\d{2})' | Select-Object -First 1
  $d = [datetime]::MinValue
  if ($g -and [datetime]::TryParse($g.Matches[0].Groups[1].Value, [ref]$d)) {
    $lines.Add("- GOALS last refresh: $($g.Matches[0].Groups[1].Value) ($([int]((Get-Date) - $d).TotalDays)d ago)")
  } else { $lines.Add('- GOALS: refresh marker not found (DEGRADED)') }
} else { $lines.Add('- GOALS.md missing (DEGRADED)') }
$lines.Add('')

# --- Emit ---
# stdout always carries the brief. The saved file is the deliverable for the
# unattended scheduled run: a write failure MUST surface as a non-zero exit,
# else Task Scheduler reports success with no brief (silent failure). Set-Content
# is a cmdlet, so $LASTEXITCODE does not cover it under ErrorActionPreference
# Continue -- gate it explicitly with -ErrorAction Stop + try/catch (the native
# gh/git calls above stay on Continue so their stderr does not false-fail, L-040).
# Write-Output (not Write-Host): the brief goes to stdout so it is capturable,
# pipeable, and redirectable by a scheduler or a watcher. Write-Host would only
# reach the console and vanish under capture.
$text = $lines -join [Environment]::NewLine
Write-Output $text
if (-not $NoFile) {
  try {
    if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir -ErrorAction Stop | Out-Null }
    $outPath = Join-Path $OutDir "$today.md"
    Set-Content -Path $outPath -Value $text -Encoding utf8 -ErrorAction Stop
    Write-Host "[morning-brief] saved to $outPath"
  } catch {
    Write-Error "[morning-brief] failed to write brief to ${OutDir}: $_"
    exit 1
  }
}
exit 0
