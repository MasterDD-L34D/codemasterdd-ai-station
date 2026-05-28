<#
.SYNOPSIS
Local bare-mirror backup of the fleet GitHub repos (SPOF insurance).

.DESCRIPTION
Mitigates the single-point-of-failure flagged in the 2026-05-28 VC governance
review: GitHub origin is the only off-machine hub. A `git clone --mirror` keeps
a full bare copy (all refs + history) locally, so the repos survive loss of the
GitHub account. Idempotent: first run clones --mirror, later runs fetch-update.

For disk-loss insurance too, sync $Dest to an external drive or a cloud folder
(this script does not do that step -- it is your infra choice; e.g. robocopy
$Dest to an external drive, or a second `git push` to another remote).

.PARAMETER Dest
Directory that holds the bare mirrors (default C:\dev\_mirror-backup, outside
any repo so it is never accidentally tracked).

.PARAMETER Repos
Repo names under the org to mirror.

.EXAMPLE
powershell -ExecutionPolicy Bypass -File scripts\backup\mirror-repos.ps1
.EXAMPLE
powershell -ExecutionPolicy Bypass -File scripts\backup\mirror-repos.ps1 -Dest E:\git-mirrors -Repos codemasterdd-ai-station,vault
#>
param(
  [string]$Dest = "C:\dev\_mirror-backup",
  [string[]]$Repos = @(
    "codemasterdd-ai-station",
    "Game",
    "Game-Godot-v2",
    "Game-Database",
    "vault",
    "evo-swarm",
    "synesthesia"
  ),
  [string]$Org = "MasterDD-L34D"
)

# Do NOT use ErrorActionPreference=Stop here: git writes progress ("Cloning
# into...") to stderr, which PowerShell 5.1 turns into a terminating
# NativeCommandError under Stop -- falsely failing a clone that exited 0.
# Rely on $LASTEXITCODE only (the authoritative success signal for a native exe).
$ErrorActionPreference = "Continue"

if (-not (Test-Path $Dest)) {
  New-Item -ItemType Directory -Force -Path $Dest | Out-Null
}

$failed = @()
foreach ($r in $Repos) {
  $bare = Join-Path $Dest "$r.git"
  $url  = "git@github.com:$Org/$r.git"
  if (Test-Path $bare) {
    Write-Output "[update]  $r"
    git -C $bare remote update --prune
  } else {
    Write-Output "[mirror]  $r -> $bare"
    git clone --mirror $url $bare
  }
  if ($LASTEXITCODE -ne 0) {
    Write-Output "[FAIL]    $r -- git exit $LASTEXITCODE"
    $failed += $r
  } else {
    Write-Output "[ok]      $r"
  }
}

if ($failed.Count -gt 0) {
  Write-Output "DONE with failures: $($failed -join ', ')"
  exit 1
}
Write-Output "DONE -- all mirrors current under $Dest"
