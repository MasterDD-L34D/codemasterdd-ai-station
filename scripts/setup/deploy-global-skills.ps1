<#
.SYNOPSIS
Deploy LITE agent-scanner skill + L3 directive to user-global ~/.claude/.
Idempotent, sandbox-tested, bounded-sentinel rollback.

.DESCRIPTION
Spec: docs/superpowers/specs/2026-05-28-archon-agent-scanner-cross-fleet-deploy-design.md
Plan: docs/superpowers/plans/2026-05-28-archon-agent-scanner-cross-fleet-deploy.md

.PARAMETER Apply
Actually write to ~/.claude/. Default is DRY-RUN preview.

.PARAMETER Remove
Rollback: remove skill dir + bounded directive section from CLAUDE.md.

.PARAMETER SkipSandbox
Skip mandatory sandbox QG Step-1. NOT recommended (anti-pattern #9).
#>
[CmdletBinding(DefaultParameterSetName='DryRun')]
param(
  [Parameter(ParameterSetName='Apply')][switch]$Apply,
  [Parameter(ParameterSetName='Remove')][switch]$Remove,
  [switch]$SkipSandbox
)

# Do NOT use Stop here: native commands write to stderr which becomes
# a terminating NativeCommandError under Stop (L-2026-05-040).
$ErrorActionPreference = 'Continue'

# Exit codes (sec 7.1 spec):
#   0 = success / dry-run preview
#   1 = generic failure (post-deploy verify fail)
#   2 = ~/.claude/ permission denied
#   3 = canonical missing in codemasterdd
#   4 = sentinel false-positive (start match but disambiguation fail)
#   5 = sandbox QG failed
$EXIT_OK = 0
$EXIT_FAIL = 1
$EXIT_NO_PERM = 2
$EXIT_NO_CANONICAL = 3
$EXIT_SENTINEL_AMBIGUOUS = 4
$EXIT_SANDBOX_FAIL = 5

# Path normalize (anti-pattern #9a: no ..\ residue).
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$canonicalSkill = Join-Path $repoRoot '.claude\global-skills\agent-scanner'
$canonicalFragment = Join-Path $repoRoot '.claude\global-claude-md-fragments\agent-scanner-directive.md'
$targetSkillsDir = Join-Path $env:USERPROFILE '.claude\skills'
$targetSkillDir = Join-Path $targetSkillsDir 'agent-scanner'
$targetClaudeMd = Join-Path $env:USERPROFILE '.claude\CLAUDE.md'

# Sentinels (sec 5.4 spec).
$startSentinel = '## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)'
$endSentinel   = '<!-- END agent-scanner-directive -->'
$disambigRegex = '^\*\*Rule\*\* \(STRONG'

# Dispatch based on mode.
switch ($PSCmdlet.ParameterSetName) {
  'Apply'   { Write-Output "MODE: APPLY (will write to ~/.claude/)" }
  'Remove'  { Write-Output "MODE: REMOVE (rollback)" }
  default   { Write-Output "MODE: DRY-RUN (preview only, no write). Pass -Apply to deploy." }
}

Write-Output "repoRoot:         $repoRoot"
Write-Output "canonicalSkill:   $canonicalSkill"
Write-Output "canonicalFragment:$canonicalFragment"
Write-Output "targetSkillDir:   $targetSkillDir"
Write-Output "targetClaudeMd:   $targetClaudeMd"

# Canonical existence check (exit 3 if missing).
if (-not (Test-Path $canonicalSkill) -or -not (Test-Path $canonicalFragment)) {
  Write-Error "Canonical assets missing. Run 'git pull origin main' or repo corrupt."
  exit $EXIT_NO_CANONICAL
}

# Skeleton ends here. Subsequent tasks fill in the real logic.
Write-Output "(skeleton only -- merge/copy/sandbox logic added in later tasks)"
exit $EXIT_OK
