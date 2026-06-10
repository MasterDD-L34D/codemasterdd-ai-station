<#
.SYNOPSIS
Local bare-mirror backup of the org GitHub repos (SPOF insurance).

.DESCRIPTION
Mitigates the single-point-of-failure flagged in the 2026-05-28 VC governance
review: GitHub origin is the only off-machine hub. A `git clone --mirror` keeps
a full bare copy (all refs + history) locally, so the repos survive loss of the
GitHub account. Idempotent: first run clones --mirror, later runs fetch-update.

Repo set: discovered live via `gh repo list` (account-loss insurance must
cover the WHOLE org -- a static list drifts: 3 repos created after the
2026-05-28 snapshot were silently uncovered until 2026-06-11). If discovery
fails (gh missing / offline / unauthenticated) the script still mirrors the
static fallback list below, but exits 1 so the reduced coverage is visible
(no silent fail-open, lesson family L-041). Passing -Repos explicitly skips
discovery (subset use-case).

For disk-loss insurance too, sync $Dest to an external drive or a cloud folder
(this script does not do that step -- it is your infra choice; e.g. robocopy
$Dest to an external drive, or a second `git push` to another remote).

.PARAMETER Dest
Directory that holds the bare mirrors (default C:\dev\_mirror-backup, outside
any repo so it is never accidentally tracked).

.PARAMETER Repos
Explicit repo names under the org to mirror (skips gh discovery). Defaults to
a static org snapshot (2026-06-11) used only as fallback when discovery fails.

.EXAMPLE
powershell -ExecutionPolicy Bypass -File scripts\backup\mirror-repos.ps1
.EXAMPLE
powershell -ExecutionPolicy Bypass -File scripts\backup\mirror-repos.ps1 -Dest E:\git-mirrors -Repos codemasterdd-ai-station,vault
#>
param(
  [string]$Dest = "C:\dev\_mirror-backup",
  [string[]]$Repos = @(
    # Static fallback ONLY (authority = gh discovery below). Org snapshot 2026-06-11.
    "codemasterdd-ai-station",
    "Game",
    "Game-Godot-v2",
    "Game-Database",
    "vault",
    "evo-swarm",
    "synesthesia",
    "compass-marketplace",
    "evo-tactics-refs-meta",
    "LeaD",
    "Master-DD-Pathfinder-GPT",
    "pathfinder-1e-homebrew",
    "torneo-cremesi-site",
    "Item-generator",
    "Gpt"
  ),
  [string]$Org = "MasterDD-L34D"
)

# Do NOT use ErrorActionPreference=Stop here: git writes progress ("Cloning
# into...") to stderr, which PowerShell 5.1 turns into a terminating
# NativeCommandError under Stop -- falsely failing a clone that exited 0.
# Rely on $LASTEXITCODE only (the authoritative success signal for a native exe).
$ErrorActionPreference = "Continue"

# --- repo-set discovery (org = authority, static list = fallback) ---
$discoveryFailed = $false
if ($PSBoundParameters.ContainsKey('Repos')) {
  Write-Output "[list]    explicit -Repos override ($($Repos.Count) repos, discovery skipped)"
} else {
  $ghCmd = Get-Command gh -ErrorAction SilentlyContinue
  if ($null -eq $ghCmd) {
    # Get-Command miss leaves $LASTEXITCODE stale -- gate on the probe, not on it.
    $discoveryFailed = $true
  } else {
    $discovered = @(gh repo list $Org --limit 200 --json name --jq ".[].name")
    if ($LASTEXITCODE -eq 0 -and $discovered.Count -gt 0) {
      $Repos = $discovered | Sort-Object
      Write-Output "[list]    gh discovery: $($Repos.Count) repos in org $Org"
    } else {
      $discoveryFailed = $true
    }
  }
  if ($discoveryFailed) {
    Write-Output "[warn]    gh discovery FAILED (gh missing / offline / unauthenticated)"
    Write-Output "[warn]    falling back to static list ($($Repos.Count) repos) -- repos created after the snapshot are NOT covered this run"
  }
}

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
if ($discoveryFailed) {
  Write-Output "DONE (degraded) -- static-fallback mirrors current under $Dest, but org discovery failed: exit 1 so the coverage gap stays visible"
  exit 1
}
Write-Output "DONE -- all $($Repos.Count) org mirrors current under $Dest"
