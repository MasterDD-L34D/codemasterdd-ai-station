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

function Get-FileSha256 {
  param([string]$Path)
  if (-not (Test-Path $Path)) { return $null }
  return (Get-FileHash -Algorithm SHA256 -Path $Path).Hash
}

function Invoke-SkillDeploy {
  param([string]$CanonicalDir, [string]$TargetDir, [switch]$DryRun)

  # Ensure parent dir exists (P1#5 harsh: fresh PC case).
  $skillsParent = Split-Path -Parent $TargetDir
  if (-not (Test-Path $skillsParent)) {
    if ($DryRun) {
      Write-Output "  [DRY] would mkdir: $skillsParent"
    } else {
      New-Item -ItemType Directory -Force -Path $skillsParent | Out-Null
      Write-Output "  [OK] created: $skillsParent"
    }
  }

  # Pre-copy drift check (P1#1 harsh).
  $canonicalSkillFile = Join-Path $CanonicalDir 'SKILL.md'
  $targetSkillFile = Join-Path $TargetDir 'SKILL.md'

  if (Test-Path $targetSkillFile) {
    $canonicalHash = Get-FileSha256 -Path $canonicalSkillFile
    $targetHash = Get-FileSha256 -Path $targetSkillFile
    if ($canonicalHash -ne $targetHash) {
      $ts = Get-Date -Format 'yyyyMMdd-HHmmss'
      $bakPath = "$targetSkillFile.bak-$ts"
      if ($DryRun) {
        Write-Output "  [DRY] DRIFT detected (target hash != canonical). Would backup -> $bakPath"
      } else {
        Copy-Item -Path $targetSkillFile -Destination $bakPath -Force
        Write-Output "  [OK] DRIFT detected. .bak saved: $bakPath"
      }
    }
  }

  # Copy from canonical.
  if ($DryRun) {
    Write-Output "  [DRY] would copy: $CanonicalDir\* -> $TargetDir\"
  } else {
    if (-not (Test-Path $TargetDir)) { New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null }
    Copy-Item -Path "$CanonicalDir\*" -Destination $TargetDir -Recurse -Force
    Write-Output "  [OK] skill copied: $CanonicalDir -> $TargetDir"
  }
}

function Read-FileUtf8NoBom {
  param([string]$Path)
  if (-not (Test-Path $Path)) { return $null }
  return [System.IO.File]::ReadAllText($Path)
}

function Write-FileUtf8NoBom {
  param([string]$Path, [string]$Content)
  # Normalize to CRLF on Windows write (P2#1 harsh: prevent mixed endings).
  $content = $Content -replace '(?<!\r)\n', "`r`n"
  $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
  [System.IO.File]::WriteAllText($Path, $content, $utf8NoBom)
}

function Test-DirectivePresent {
  param([string]$ClaudeMdPath, [string]$StartSentinel, [string]$DisambigRegex)

  # Returns: 'absent' / 'present-valid' / 'ambiguous'.
  if (-not (Test-Path $ClaudeMdPath)) { return 'absent' }

  $content = Read-FileUtf8NoBom -Path $ClaudeMdPath
  $lines = $content -split "`r?`n"

  $startIdx = -1
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -eq $StartSentinel) { $startIdx = $i; break }
  }
  if ($startIdx -lt 0) { return 'absent' }

  # Scan first non-blank within next 5 lines after sentinel.
  for ($j = $startIdx + 1; $j -le [Math]::Min($startIdx + 5, $lines.Count - 1); $j++) {
    $line = $lines[$j].Trim()
    if (-not [string]::IsNullOrEmpty($line)) {
      if ($line -match $DisambigRegex) { return 'present-valid' }
      return 'ambiguous'
    }
  }
  return 'ambiguous'
}

function Invoke-ClaudeMdMerge {
  param(
    [string]$ClaudeMdPath,
    [string]$FragmentPath,
    [string]$StartSentinel,
    [string]$DisambigRegex,
    [switch]$DryRun
  )

  $state = Test-DirectivePresent -ClaudeMdPath $ClaudeMdPath -StartSentinel $StartSentinel -DisambigRegex $DisambigRegex

  switch ($state) {
    'present-valid' {
      Write-Host "  [OK] directive already present and valid -- skip merge (idempotent)"
      return $true
    }
    'ambiguous' {
      $ts = Get-Date -Format 'yyyyMMdd-HHmmss'
      $logPath = Join-Path $env:USERPROFILE ".claude\.apply-blocked-$ts.log"
      $content = Read-FileUtf8NoBom -Path $ClaudeMdPath
      $logContent = "Sentinel ambiguous on $ts`r`nClaudeMd: $ClaudeMdPath`r`nDump:`r`n$content"
      if (-not $DryRun) {
        if (-not (Test-Path (Split-Path $logPath -Parent))) {
          New-Item -ItemType Directory -Force -Path (Split-Path $logPath -Parent) | Out-Null
        }
        Set-Content -Path $logPath -Value $logContent -Encoding utf8
      }
      Write-Host "  [FAIL] sentinel ambiguous (heading match but Rule (STRONG missing within 5 lines)"
      Write-Host "         log: $logPath"
      return $false
    }
    'absent' {
      $fragmentContent = Read-FileUtf8NoBom -Path $FragmentPath
      if ($null -eq $fragmentContent) {
        Write-Error "Fragment file missing: $FragmentPath"
        return $false
      }
      if ($DryRun) {
        Write-Host "  [DRY] would append directive ($(($fragmentContent -split "`n").Count) lines) -> $ClaudeMdPath"
        return $true
      }
      # Backup pre-modify.
      $ts = Get-Date -Format 'yyyyMMdd-HHmmss'
      if (Test-Path $ClaudeMdPath) {
        $bakPath = "$ClaudeMdPath.bak-$ts"
        Copy-Item -Path $ClaudeMdPath -Destination $bakPath -Force
        Write-Host "  [OK] backup saved: $bakPath"
      }
      $existing = if (Test-Path $ClaudeMdPath) { Read-FileUtf8NoBom -Path $ClaudeMdPath } else { "" }
      if (-not [string]::IsNullOrEmpty($existing) -and -not $existing.EndsWith("`n")) { $existing += "`n" }
      $merged = $existing + "`n" + $fragmentContent
      Write-FileUtf8NoBom -Path $ClaudeMdPath -Content $merged
      Write-Host "  [OK] directive appended to: $ClaudeMdPath"
      return $true
    }
  }
}

function Invoke-Rollback {
  param(
    [string]$TargetSkillDir,
    [string]$ClaudeMdPath,
    [string]$StartSentinel,
    [string]$EndSentinel,
    [switch]$DryRun
  )

  # 1. Remove skill dir.
  if (Test-Path $TargetSkillDir) {
    if ($DryRun) {
      Write-Host "  [DRY] would remove dir: $TargetSkillDir"
    } else {
      Remove-Item -Recurse -Force $TargetSkillDir
      Write-Host "  [OK] removed dir: $TargetSkillDir"
    }
  } else {
    Write-Host "  [SKIP] skill dir already absent: $TargetSkillDir"
  }

  # 2. Strip directive from CLAUDE.md (bounded by start + END sentinel).
  if (-not (Test-Path $ClaudeMdPath)) {
    Write-Host "  [SKIP] CLAUDE.md absent: $ClaudeMdPath"
    return $true
  }

  $content = Read-FileUtf8NoBom -Path $ClaudeMdPath
  $startEsc = [Regex]::Escape($StartSentinel)
  $endEsc = [Regex]::Escape($EndSentinel)
  $pattern = "(?ms)^$startEsc.*?$endEsc`r?`n?"

  if ($content -notmatch $pattern) {
    Write-Host "  [WARN] start+END sentinel pair not found. Falling back to .bak restore if available."
    $bakFiles = Get-ChildItem -Path (Split-Path $ClaudeMdPath -Parent) -Filter "$(Split-Path $ClaudeMdPath -Leaf).bak-*" -ErrorAction SilentlyContinue
    if ($bakFiles) {
      $latestBak = $bakFiles | Sort-Object Name -Descending | Select-Object -First 1
      if ($DryRun) {
        Write-Host "  [DRY] would restore from: $($latestBak.FullName)"
      } else {
        Copy-Item -Path $latestBak.FullName -Destination $ClaudeMdPath -Force
        Write-Host "  [OK] restored from latest .bak: $($latestBak.FullName)"
      }
    } else {
      Write-Host "  [SKIP] no .bak file found; nothing to do."
    }
    return $true
  }

  if (-not $DryRun) {
    $ts = Get-Date -Format 'yyyyMMdd-HHmmss'
    $bakPath = "$ClaudeMdPath.bak-remove-$ts"
    Copy-Item -Path $ClaudeMdPath -Destination $bakPath -Force
    Write-Host "  [OK] pre-remove backup: $bakPath"
  }

  $stripped = [Regex]::Replace($content, $pattern, '')

  if ($DryRun) {
    $matchCount = ([Regex]::Matches($content, $pattern)).Count
    Write-Host "  [DRY] would strip $matchCount directive section(s) from CLAUDE.md"
  } else {
    Write-FileUtf8NoBom -Path $ClaudeMdPath -Content $stripped
    Write-Host "  [OK] directive stripped from CLAUDE.md (bounded start..end sentinel)"
  }
  return $true
}

function Invoke-SandboxQG {
  param(
    [string]$CanonicalSkill,
    [string]$CanonicalFragment,
    [string]$StartSentinel,
    [string]$DisambigRegex,
    [string]$EndSentinel
  )

  $sandboxRoot = Join-Path $env:TEMP "deploy-global-skills-sandbox-$([guid]::NewGuid())"
  $sandboxClaudeDir = Join-Path $sandboxRoot '.claude'
  $sandboxSkillsDir = Join-Path $sandboxClaudeDir 'skills'
  $sandboxSkillDir = Join-Path $sandboxSkillsDir 'agent-scanner'
  $sandboxClaudeMd = Join-Path $sandboxClaudeDir 'CLAUDE.md'

  Write-Host "  [sandbox] root: $sandboxRoot"
  New-Item -ItemType Directory -Force -Path $sandboxClaudeDir | Out-Null

  Set-Content -Path $sandboxClaudeMd -Value "# Sandbox CLAUDE.md`r`n`r`n## Other section`r`n`r`nseed body" -Encoding utf8

  Invoke-SkillDeploy -CanonicalDir $CanonicalSkill -TargetDir $sandboxSkillDir | Out-Null
  $ok1 = Invoke-ClaudeMdMerge -ClaudeMdPath $sandboxClaudeMd -FragmentPath $CanonicalFragment `
                                -StartSentinel $StartSentinel -DisambigRegex $DisambigRegex
  if (-not $ok1) {
    Write-Host "  [sandbox FAIL] run-1 merge returned false"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }

  $sandboxSkillFile = Join-Path $sandboxSkillDir 'SKILL.md'
  if (-not (Test-Path $sandboxSkillFile)) {
    Write-Host "  [sandbox FAIL] SKILL.md missing post-copy"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }
  $skillContent = Read-FileUtf8NoBom -Path $sandboxSkillFile
  if ($skillContent -notmatch '(?ms)^---\s*$.*?name:\s*agent-scanner.*?^---\s*$') {
    Write-Host "  [sandbox FAIL] SKILL.md frontmatter does not parse"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }

  $cmContent = Read-FileUtf8NoBom -Path $sandboxClaudeMd
  if ($cmContent -notmatch [Regex]::Escape($StartSentinel)) {
    Write-Host "  [sandbox FAIL] start sentinel missing from sandbox CLAUDE.md"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }
  if ($cmContent -notmatch [Regex]::Escape($EndSentinel)) {
    Write-Host "  [sandbox FAIL] END sentinel missing from sandbox CLAUDE.md"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }

  $contentBeforeRun2 = Read-FileUtf8NoBom -Path $sandboxClaudeMd
  Invoke-SkillDeploy -CanonicalDir $CanonicalSkill -TargetDir $sandboxSkillDir | Out-Null
  $ok2 = Invoke-ClaudeMdMerge -ClaudeMdPath $sandboxClaudeMd -FragmentPath $CanonicalFragment `
                                -StartSentinel $StartSentinel -DisambigRegex $DisambigRegex
  $contentAfterRun2 = Read-FileUtf8NoBom -Path $sandboxClaudeMd

  if (-not $ok2) {
    Write-Host "  [sandbox FAIL] run-2 merge returned false"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }
  if ($contentBeforeRun2 -ne $contentAfterRun2) {
    Write-Host "  [sandbox FAIL] idempotency violated: run-2 produced diff"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }

  Remove-Item -Recurse -Force $sandboxRoot
  Write-Host "  [sandbox OK] all checks passed (artifact + sentinel + idempotency)"
  return $true
}

function Test-DeployedState {
  param(
    [string]$TargetSkillDir,
    [string]$ClaudeMdPath,
    [string]$StartSentinel,
    [string]$EndSentinel
  )

  $ok = $true

  # 1. Skill file present + frontmatter parses.
  $skillFile = Join-Path $TargetSkillDir 'SKILL.md'
  if (-not (Test-Path $skillFile)) {
    Write-Host "  [VERIFY FAIL] SKILL.md missing: $skillFile"
    $ok = $false
  } else {
    $sc = Read-FileUtf8NoBom -Path $skillFile
    if ($sc -notmatch '(?ms)^---\s*$.*?name:\s*agent-scanner.*?^---\s*$') {
      Write-Host "  [VERIFY FAIL] SKILL.md frontmatter does not parse"
      $ok = $false
    } else {
      Write-Host "  [VERIFY OK] SKILL.md present + frontmatter parses"
    }
  }

  # 2. CLAUDE.md sentinel present (start + end both).
  if (Test-Path $ClaudeMdPath) {
    $cm = Read-FileUtf8NoBom -Path $ClaudeMdPath
    if ($cm -notmatch [Regex]::Escape($StartSentinel)) {
      Write-Host "  [VERIFY FAIL] start sentinel missing in CLAUDE.md"
      $ok = $false
    } elseif ($cm -notmatch [Regex]::Escape($EndSentinel)) {
      Write-Host "  [VERIFY FAIL] END sentinel missing in CLAUDE.md"
      $ok = $false
    } else {
      Write-Host "  [VERIFY OK] CLAUDE.md has start + END sentinel"
    }
  } else {
    Write-Host "  [VERIFY FAIL] CLAUDE.md missing post-deploy"
    $ok = $false
  }

  # 3. ASCII check on deployed SKILL.md body.
  if (Test-Path $skillFile) {
    $nonAscii = (Get-Content -Raw $skillFile) -match '[^\x00-\x7F]'
    if ($nonAscii) {
      Write-Host "  [VERIFY FAIL] non-ASCII chars in deployed SKILL.md"
      $ok = $false
    } else {
      Write-Host "  [VERIFY OK] SKILL.md ASCII clean"
    }
  }

  return $ok
}

# Dispatch by mode (Apply / Remove / DryRun).
switch ($PSCmdlet.ParameterSetName) {
  'Apply' {
    if (-not $SkipSandbox) {
      Write-Output ""
      Write-Output "=== Sandbox QG Step-1 (mandatory) ==="
      $sandboxOk = Invoke-SandboxQG -CanonicalSkill $canonicalSkill -CanonicalFragment $canonicalFragment `
                                     -StartSentinel $startSentinel -DisambigRegex $disambigRegex `
                                     -EndSentinel $endSentinel
      if (-not $sandboxOk) {
        Write-Error "Sandbox QG failed. Aborting before any write to ~/.claude/. Exit 5."
        exit $EXIT_SANDBOX_FAIL
      }
    } else {
      Write-Output "  [WARN] -SkipSandbox specified; QG Step-1 bypassed (NOT recommended)."
    }

    Write-Output ""
    Write-Output "=== Phase 1: skill deploy ==="
    Invoke-SkillDeploy -CanonicalDir $canonicalSkill -TargetDir $targetSkillDir

    Write-Output ""
    Write-Output "=== Phase 2: CLAUDE.md merge ==="
    $ok = Invoke-ClaudeMdMerge -ClaudeMdPath $targetClaudeMd -FragmentPath $canonicalFragment `
                                -StartSentinel $startSentinel -DisambigRegex $disambigRegex
    if (-not $ok) {
      Write-Error "CLAUDE.md merge failed. Exit 4."
      exit $EXIT_SENTINEL_AMBIGUOUS
    }

    Write-Output ""
    Write-Output "=== Phase 3: post-deploy verify ==="
    $verifyOk = Test-DeployedState -TargetSkillDir $targetSkillDir -ClaudeMdPath $targetClaudeMd `
                                     -StartSentinel $startSentinel -EndSentinel $endSentinel
    if (-not $verifyOk) {
      Write-Error "Post-deploy verify failed. Exit 1."
      exit $EXIT_FAIL
    }
    Write-Output ""
    Write-Output "DONE. Deploy successful."
    exit $EXIT_OK
  }
  'Remove' {
    Write-Output ""
    Write-Output "=== Rollback ==="
    Invoke-Rollback -TargetSkillDir $targetSkillDir -ClaudeMdPath $targetClaudeMd `
                    -StartSentinel $startSentinel -EndSentinel $endSentinel | Out-Null
    exit $EXIT_OK
  }
  default {
    Write-Output ""
    Write-Output "=== Phase 1 preview (skill deploy) ==="
    Invoke-SkillDeploy -CanonicalDir $canonicalSkill -TargetDir $targetSkillDir -DryRun

    Write-Output ""
    Write-Output "=== Phase 2 preview (CLAUDE.md merge) ==="
    Invoke-ClaudeMdMerge -ClaudeMdPath $targetClaudeMd -FragmentPath $canonicalFragment `
                          -StartSentinel $startSentinel -DisambigRegex $disambigRegex -DryRun | Out-Null

    Write-Output ""
    Write-Output "(Phase 3 verify / sandbox QG added in subsequent tasks)"
    exit $EXIT_OK
  }
}
