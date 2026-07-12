#requires -Version 5.1
<#
.SYNOPSIS
    Fail-closed draft-PR wrapper for the Agentic OS Console (tier-1 action
    "create-draft-pr").

.DESCRIPTION
    Refuses to open a PR unless BOTH guards pass:
      1. the current branch matches claude/*  (never a doctrine/topic branch);
      2. the branch is already pushed to origin (so no un-pushed WIP leaks,
         which on a PUBLIC repo would expose local work-in-progress).
    Then runs `gh pr create --draft --fill` with --head PINNED to the resolved
    branch, so no client input ever reaches the gh argv.

    Exit codes: 0 ok | 2 cannot resolve branch | 3 not a claude/* branch |
    4 branch not pushed | otherwise = gh's own exit code.

.NOTES
    ASCII-only (ADR-0021). ErrorActionPreference=Continue so native git/gh
    stderr does not terminate under a would-be Stop (L-040), gate on
    $LASTEXITCODE.
#>
[CmdletBinding()]
param(
    [string]$Repo = "MasterDD-L34D/codemasterdd-ai-station"
)

$ErrorActionPreference = "Continue"

$branch = (& git rev-parse --abbrev-ref HEAD | Select-Object -First 1)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($branch)) {
    Write-Output "draft-pr guard: cannot resolve current branch"
    exit 2
}
$branch = $branch.Trim()

if ($branch -notlike 'claude/*') {
    Write-Output "draft-pr guard: refusing to open a PR from '$branch' -- only claude/* branches are allowed"
    exit 3
}

& git ls-remote --exit-code --heads origin $branch | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Output "draft-pr guard: branch '$branch' is not pushed to origin -- push it first (git push -u origin $branch)"
    exit 4
}

Write-Output "draft-pr guard: OK -- branch '$branch' is a pushed claude/* branch; opening DRAFT PR on $Repo"
& gh pr create --draft --fill --repo $Repo --head $branch
exit $LASTEXITCODE
