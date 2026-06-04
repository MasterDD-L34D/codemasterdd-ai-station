<#
.SYNOPSIS
jules-dispatch.ps1 -- fail-closed wrapper for dispatching a human-authored scoped task to Jules
via REST POST /v1alpha/sessions. ADR-0037 path-to-standing for :create (ADR-0035 hard-constraints).

.DESCRIPTION
5-gate fail-closed stack (abort on first failure, non-zero exit):
  1. repo-whitelist        (NOT -Force/-ForceBlind overridable)
  2. ASCII-lint task-file  (NOT overridable; native byte-check)
  3. scoped-template lint  (NOT overridable; + Target<->task-file consistency)
  4. dedup vs ACTIVE        (-Force overrides a KNOWN overlap; -ForceBlind overrides cannot-verify)
  5. dispatch + audit-log

SDMG boundary: building/running this wrapper does NOT make :create standing. "Standing" =
allow-listing it in .claude/settings.json (a SEPARATE harsh-reviewer-gated autonomization).
Until then :create stays per-instance: a human runs this manually. External-repo MERGE stays
Eduardo-explicit (ADR-0037 decision 3). Spec: docs/superpowers/specs/2026-06-03-jules-dispatch-wrapper-design.md

.PARAMETER Repo        Bare repo name: Game | Game-Godot-v2 | codemasterdd-ai-station | Game-Database.
.PARAMETER TaskFile    Path to an ASCII scoped-strict markdown prompt (ADR-0035 template).
.PARAMETER Target      Identifier(s) dedup checks: a path and/or function (e.g. scripts/fleet/foo.ps1::Get-Bar).
.PARAMETER Title       Optional session title (default derived from Repo/Target/date).
.PARAMETER Force       Override a KNOWN dedup overlap only (gate 4). Never bypasses gates 1-3.
.PARAMETER ForceBlind  Override cannot-verify dedup (list-GET failure only -- pagination is now walked via Get-AllSessionPages). Louder audit tag.
.PARAMETER DryRun      Run all gates + build/show the REST body + write a DRYRUN audit line; do NOT POST.

.EXAMPLE
  scripts/fleet/jules-dispatch.ps1 -Repo Game -TaskFile task.md -Target services/combat/resolve.ts -DryRun
#>
param(
  [string]$Repo,
  [string]$TaskFile,
  [string]$Target,
  [string]$Title,
  [switch]$Force,
  [switch]$ForceBlind,
  [switch]$DryRun
)

# ====================================================================================
# PURE FUNCTIONS (dot-sourced + unit-tested by jules-dispatch.Tests.ps1).
# No side effects except Test-AsciiClean's file read. Constants inlined (dot-source safe).
# ====================================================================================

function Get-Whitelist {
  # Single source of truth for the repo whitelist (gate 1).
  return @('Game', 'Game-Godot-v2', 'codemasterdd-ai-station', 'Game-Database')
}

function Test-RepoWhitelisted {
  param([string]$Repo)
  return ((Get-Whitelist) -contains $Repo)
}

function Get-JulesSource {
  param([string]$Repo)
  # Owner is invariant across all 4 whitelisted repos (confirmed live + git remotes 2026-06-03).
  return "sources/github/MasterDD-L34D/$Repo"
}

function Test-SessionActive {
  param([string]$State)
  # ACTIVE = complement of a TERMINAL denylist (fail-closed: unknown/null/empty -> active).
  # Allowlisting {IN_PROGRESS, AWAITING_USER_FEEDBACK} was rejected (harsh-reviewer P0.2): an
  # unobserved in-flight state would silently false-ALLOW (the dangerous direction).
  if ([string]::IsNullOrWhiteSpace($State)) { return $true }
  $terminal = @('COMPLETED', 'FAILED', 'CANCELLED', 'ARCHIVED')
  return (-not ($terminal -contains $State.ToUpperInvariant()))
}

function Test-AsciiClean {
  param([string]$Path)
  # Native byte-level ASCII check (anti-#12). Equivalent to perl -ne 'exit 1 if /[^\x00-\x7F]/'
  # for our cases (BOM -> not-clean is INTENTIONAL); no external dep (fleet test-runner policy).
  $bytes = [IO.File]::ReadAllBytes($Path)
  foreach ($b in $bytes) { if ($b -gt 127) { return $false } }
  return $true
}

function Test-ScopedTemplate {
  param([string]$Content)
  # Gate 3: the 4 load-bearing markers of the ADR-0035 scoped-strict template.
  $missing = @()
  if ($Content -notmatch '[\\/][\w.-]+\.[A-Za-z0-9]{1,8}') { $missing += 'target-file-path' }
  if ($Content -notmatch '(?i)(single[\s-]?file|named function|no logic change|no behaviou?r change|docstring)') { $missing += 'scope-bound' }
  if ($Content -notmatch '(?i)ascii[\s-]?only') { $missing += 'ascii-only-clause' }
  if ($Content -notmatch '(?i)(accept|acceptance|verif|tests?\s+pass)') { $missing += 'acceptance' }
  return [pscustomobject]@{ Ok = ($missing.Count -eq 0); Missing = $missing }
}

function Get-TargetIdentifiers {
  param([string]$Target)
  # Derive dedup identifiers from -Target. Path-like part -> {full path, basename stem};
  # symbol-like part -> the token. Generic stop-tokens dropped (over-match). If NOTHING
  # survives, the caller (Test-TargetOverlap) treats it as overlap -> conservative abort.
  $stop = @('src', 'lib', 'app', 'apps', 'test', 'tests', 'scripts', 'services', 'main',
            'index', 'util', 'utils', 'core', 'api', 'docs', 'data', 'get', 'set', 'new',
            'run', 'build')
  $ids = New-Object System.Collections.Generic.List[string]
  $parts = $Target -split '[\s,]+|::' | Where-Object { $_ -ne '' }
  foreach ($p in $parts) {
    if ($p -match '[\\/]' -or $p -match '\.[A-Za-z0-9]{1,8}$') {
      $norm = ($p -replace '\\', '/').ToLowerInvariant()
      [void]$ids.Add($norm)
      $leaf = ($norm -split '/')[-1]
      $stem = $leaf -replace '\.[A-Za-z0-9]{1,8}$', ''
      if ($stem.Length -ge 3 -and ($stop -notcontains $stem)) { [void]$ids.Add($stem) }
    } else {
      $tok = $p.ToLowerInvariant()
      if ($tok.Length -ge 3 -and ($tok -match '^[a-z_][a-z0-9_.-]*$') -and ($stop -notcontains $tok)) {
        [void]$ids.Add($tok)
      }
    }
  }
  return ($ids | Select-Object -Unique)
}

function Test-TargetOverlap {
  param([string]$Target, [string]$SessionText)
  # Gate 4 core. Boundary-precise match of any target identifier against a session's title+prompt.
  # No surviving identifier -> $true (conservative: too-generic target aborts the dispatch).
  $ids = @(Get-TargetIdentifiers $Target)
  if ($ids.Count -eq 0) { return $true }
  $hay = $SessionText.ToLowerInvariant()
  foreach ($id in $ids) {
    $rx = '(?<![A-Za-z0-9_])' + [regex]::Escape($id) + '(?![A-Za-z0-9_])'
    if ([regex]::IsMatch($hay, $rx)) { return $true }
  }
  return $false
}

function Test-TargetInTaskFile {
  param([string]$Target, [string]$Content)
  # P1.3: at least one target identifier MUST appear in the task-file body, else the wrapper
  # would dedup-check a file the task does not touch. No identifier -> $false (forces a specific Target).
  $ids = @(Get-TargetIdentifiers $Target)
  if ($ids.Count -eq 0) { return $false }
  $hay = $Content.ToLowerInvariant()
  foreach ($id in $ids) {
    $rx = '(?<![A-Za-z0-9_])' + [regex]::Escape($id) + '(?![A-Za-z0-9_])'
    if ([regex]::IsMatch($hay, $rx)) { return $true }
  }
  return $false
}

function Find-ActiveOverlap {
  param($Sessions, [string]$Target, [string]$Source)
  # Gate 4 wiring (pure): over a session list, keep only ACTIVE (non-terminal) sessions on the
  # SAME repo source, and return the first whose title+prompt overlaps -Target ($null if none).
  $active = @($Sessions | Where-Object { (Test-SessionActive $_.state) -and ($_.sourceContext.source -eq $Source) })
  foreach ($s in $active) {
    $txt = ([string]$s.title) + ' ' + ([string]$s.prompt)
    if (Test-TargetOverlap $Target $txt) {
      return [pscustomobject]@{ Id = ($s.name -replace 'sessions/', ''); Title = (([string]$s.title -split "`n")[0]) }
    }
  }
  return $null
}

function Get-SessionId {
  param($Created)
  # P1-C: extract the session id from a create-POST response, or $null if the response has no
  # usable name (LRO/error envelope / unexpected shape). MAIN aborts on $null rather than
  # writing a hollow "DISPATCHED" audit line with a blank id (the honesty axis).
  if ($null -eq $Created) { return $null }
  $n = $Created.name
  if ([string]::IsNullOrWhiteSpace($n)) { return $null }
  return ($n -replace 'sessions/', '')
}

function Resolve-AuditState {
  param($Fetched, $CreateState)
  # The create-POST response returns an EMPTY state (the session is actually QUEUED, surfaced only
  # by a follow-up GET /sessions/{id}; observed live 2026-06-03 sid 17389050512450210982). Resolve
  # the audit-log state with a never-throw fallback chain: the GET state (authoritative) -> the
  # create-POST state -> 'UNKNOWN'. Pure: the impure GET runs in MAIN; this only picks a value.
  # Array-safe (P2#1): Invoke-RestMethod may return Object[], and member-enumeration of .state then
  # yields an array. @(...)[0] + [string] hard-scalarizes so an array can NEVER leak into the
  # pipe-delimited audit spine (silent corruption worse than blank). $CreateState is left untyped
  # for the same reason -- a [string] param would space-join an array at bind time.
  $getState = if ($null -ne $Fetched) { [string](@($Fetched.state)[0]) } else { '' }
  if (-not [string]::IsNullOrWhiteSpace($getState)) { return $getState }
  $createState = [string](@($CreateState)[0])
  if (-not [string]::IsNullOrWhiteSpace($createState)) { return $createState }
  return 'UNKNOWN'
}

function Add-DispatchConstraints {
  param([string]$TaskContent)
  # Append non-negotiable scope + anti-pollution constraints to EVERY dispatched prompt. Root cause
  # (skiv 2026-06-04): Jules downloaded a 121MB Godot engine binary into its sandbox -> the change-set
  # ballooned to 121MB -> the session FAILED at delivery and the real 4-line work was lost (the REST
  # outputs gitPatch came back empty -- only an early activities snapshot held the clean diff). Hard
  # scoping the prompt prevents the bloat-then-FAIL class at the source.
  $guard = @'

--- HARD CONSTRAINTS (jules-dispatch wrapper, non-negotiable) ---
- Modify ONLY the named target file(s) above. Do NOT add, create, download, or commit ANY other
  file: no binaries, no engine/SDK/tool downloads, no build artifacts, no node_modules. A polluted
  working tree (e.g. a downloaded engine binary) makes the change-set too large to deliver and the
  session FAILS with the work lost.
- For a comment/doc/JSDoc-only task: do NOT build, run, compile, or download any tooling -- no
  execution or validation environment is needed; just edit the file.
'@
  return ($TaskContent + $guard)
}

function Get-AllSessionPages {
  param([scriptblock]$Fetch, [int]$MaxPages = 50)
  # Gate-4 pagination (fix 2026-06-05). The Jules sessions list paginates once total sessions
  # exceed pageSize (nextPageToken). The previous gate-4 ABORTED on a paginated list (or forced a
  # blind dispatch with -ForceBlind), so an active session sitting on page 2+ was invisible to the
  # dedup check -- the root cause of a cross-machine same-target re-dispatch on 2026-06-05. This
  # walks EVERY page via the $Fetch callback and returns the merged session array so dedup sees all
  # active sessions. $Fetch is a callback (param: pageToken -> a response object exposing .sessions
  # and .nextPageToken); keeping the impure Invoke-RestMethod inside the caller's callback leaves
  # this function pure + unit-testable with a fake multi-page fetcher. A throw from $Fetch
  # propagates to MAIN's gate-4 try/catch (degrade to -ForceBlind / abort), unchanged. $MaxPages
  # bounds a pathological walk (50 * 100 = 5000 sessions); Truncated flags hitting that bound.
  $all = @()
  $token = $null
  $pages = 0
  do {
    $page = & $Fetch $token
    if ($null -ne $page) { $all += @($page.sessions) }
    $token = if ($null -ne $page) { [string]$page.nextPageToken } else { '' }
    $pages++
  } while ((-not [string]::IsNullOrEmpty($token)) -and ($pages -lt $MaxPages))
  return [pscustomobject]@{
    Sessions  = $all
    Pages     = $pages
    Truncated = (-not [string]::IsNullOrEmpty($token))
  }
}

# === MAIN (impure orchestration -- not dot-sourced; everything below runs only on direct invoke) ===
$ErrorActionPreference = 'Stop'

# --- required-arg validation (param is non-mandatory so the test can dot-source without a prompt) ---
if (-not $Repo)     { Write-Error 'ABORT: -Repo required';     exit 2 }
if (-not $TaskFile) { Write-Error 'ABORT: -TaskFile required'; exit 2 }
if (-not $Target)   { Write-Error 'ABORT: -Target required';   exit 2 }

# --- Gate 1: repo whitelist (NOT overridable) ---
if (-not (Test-RepoWhitelisted $Repo)) {
  Write-Error "ABORT gate1: repo '$Repo' not whitelisted. Allowed: $((Get-Whitelist) -join ', ')"
  exit 1
}

# --- load + validate task-file ---
if (-not (Test-Path $TaskFile)) { Write-Error "ABORT: TaskFile not found: $TaskFile"; exit 2 }
$taskContent = [IO.File]::ReadAllText($TaskFile)
if ([string]::IsNullOrWhiteSpace($taskContent)) { Write-Error 'ABORT: task-file is empty'; exit 1 }

# --- Gate 2: ASCII-lint (NOT overridable) ---
if (-not (Test-AsciiClean $TaskFile)) {
  Write-Error "ABORT gate2: task-file '$TaskFile' has non-ASCII bytes (anti-#12). Make it ASCII-only."
  exit 1
}

# --- Gate 3: scoped-template lint + Target consistency (NOT overridable) ---
$tmpl = Test-ScopedTemplate $taskContent
if (-not $tmpl.Ok) {
  Write-Error "ABORT gate3: task-file missing scoped markers: $($tmpl.Missing -join ', ') (ADR-0035 #1; vague prompts are proven defect generators)"
  exit 1
}
if (-not (Test-TargetInTaskFile $Target $taskContent)) {
  Write-Error "ABORT gate3: -Target '$Target' is not named in the task-file -- dedup would check the wrong file. Align -Target with the scoped target."
  exit 1
}

# --- Gate 4: dedup vs ACTIVE sessions ---
# P1-A: guard the key read -- keys.env is ACL-locked (edusc+SYSTEM); on a host where the current
# user is excluded, an access-denied is a TERMINATING error under Stop. Catch it to a clean exit-2.
$apiKey = $null
try {
  $keysPath = "$HOME/.config/api-keys/keys.env"
  if (Test-Path $keysPath) {
    $apiKey = ((Get-Content $keysPath -ErrorAction Stop |
                Where-Object { $_ -match '^JULES_API_KEY=' }) -replace '^JULES_API_KEY=', '')
  }
} catch { Write-Error "ABORT gate4: cannot read keys.env ($($_.Exception.Message))"; exit 2 }
if (-not $apiKey) { Write-Error 'ABORT gate4: JULES_API_KEY not found in ~/.config/api-keys/keys.env'; exit 2 }
$api = 'https://jules.googleapis.com/v1alpha'
$hdr = @{ 'x-goog-api-key' = $apiKey }
$source = Get-JulesSource $Repo

$overlap = $null
$listOk = $false
try {
  $pageResult = Get-AllSessionPages -Fetch {
    param($tok)
    $u = "$api/sessions?pageSize=100"
    if ($tok) { $u += "&pageToken=$tok" }
    return (Invoke-RestMethod -Headers $hdr $u -ErrorAction Stop)
  }
  $listOk = $true
  $allSessions = @($pageResult.Sessions)
  if ($pageResult.Truncated) {
    # Pathological only (>5000 sessions): the walk hit the page bound, so a later page MAY hold an
    # unseen active session. Honest warning (not a silent gap); archive old terminal sessions to fix.
    Write-Warning "gate4: session list exceeded $($pageResult.Pages) pages (>5000 sessions) -- dedup scanned a bounded prefix; archive old terminal sessions."
  }
  $activeCount = @($allSessions | Where-Object { (Test-SessionActive $_.state) -and ($_.sourceContext.source -eq $source) }).Count
  Write-Host "gate4: $activeCount active session(s) on $source ($($pageResult.Pages) page(s) scanned)"
  $overlap = Find-ActiveOverlap -Sessions $allSessions -Target $Target -Source $source
} catch {
  $listOk = $false
  if (-not $ForceBlind) {
    Write-Error "ABORT gate4: cannot enumerate active sessions ($($_.Exception.Message)). Re-run with -ForceBlind to dispatch with NO dedup verification."
    exit 1
  }
  Write-Warning 'DISPATCHING WITH NO DEDUP VERIFICATION (-ForceBlind: list-GET failed).'
}

if ($overlap) {
  if (-not $Force) {
    Write-Error "ABORT gate4: -Target '$Target' overlaps active session $($overlap.Id) ($($overlap.Title)). Re-run with -Force only if this is NOT a real overlap."
    exit 1
  }
  Write-Warning "FORCED-OVERRIDE-OVERLAP $($overlap.Id): proceeding despite overlap (-Force)."
}

# --- forced-tag for the audit line ---
$forcedTag = ''
if ($Force -and $overlap) { $forcedTag = " | FORCED-OVERRIDE-OVERLAP $($overlap.Id)" }
elseif ($ForceBlind -and -not $listOk) { $forcedTag = ' | FORCED-BLIND' }

# --- build dispatch body (ADR-0035 verified schema) ---
if (-not $Title) { $Title = "[$Repo] $Target ($(Get-Date -Format 'yyyy-MM-dd'))" }
$body = @{
  prompt        = (Add-DispatchConstraints $taskContent)
  title         = $Title
  sourceContext = @{
    source            = $source
    githubRepoContext = @{ startingBranch = 'main' }
  }
} | ConvertTo-Json -Depth 8

# --- audit-log (logs/ is gitignored) ---
# P1-B: GetFullPath normalizes '..\..' WITHOUT touching the filesystem (Resolve-Path throws under
# Stop if the path is not resolvable -- e.g. junction/symlink fleet layouts). The audit spine must
# never be the thing that throws.
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$log = Join-Path $repoRoot ("logs/jules-dispatch-$(Get-Date -Format 'yyyy-MM').md")
$ts = (Get-Date -Format 'o')
function Write-Audit {
  param([string]$Line)
  New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
  [IO.File]::AppendAllText($log, $Line + "`n", (New-Object Text.UTF8Encoding $false))
}

# --- DryRun: show body + DRYRUN audit, no POST ---
if ($DryRun) {
  Write-Host '--- DRYRUN: all gates PASSED. Dispatch body (NOT posted): ---'
  Write-Host $body
  Write-Audit "$ts | DRYRUN | $Repo | $Target | (no-session) | (dryrun) | $Title$forcedTag"
  Write-Host "DRYRUN complete. Audit-log: $log"
  exit 0
}

# --- Gate 5: dispatch + audit ---
try {
  $created = Invoke-RestMethod -Method Post -Headers $hdr -ContentType 'application/json' -Body $body "$api/sessions" -ErrorAction Stop
  # P1-C: do NOT record a dispatch we cannot name. A 200 with no .name (LRO/error envelope) must
  # abort, not write a hollow "DISPATCHED" audit line with a blank id.
  $sid = Get-SessionId $created
  if (-not $sid) {
    Write-Error "ABORT gate5: POST returned no session name (shape: $($created | ConvertTo-Json -Depth 3 -Compress))"
    exit 1
  }
  # The create-POST returns an EMPTY state (the session is QUEUED, surfaced only by a follow-up
  # GET). Fetch the real state for an accurate audit line; the audit spine must never throw, so any
  # GET failure degrades to the create-response state, then to 'UNKNOWN' (Resolve-AuditState).
  $fetched = $null
  try {
    # -TimeoutSec caps a hung audit-only GET so it can never stall the audit-spine write (P3): the
    # dispatch already succeeded, so this GET is best-effort enrichment, not part of the exit path.
    $fetched = Invoke-RestMethod -Headers $hdr -TimeoutSec 15 "$api/sessions/$sid" -ErrorAction Stop
  } catch {
    Write-Warning "gate5: post-dispatch GET /sessions/$sid failed ($($_.Exception.Message)); audit state degrades to create-response/UNKNOWN."
  }
  # P2#2 honesty axis (mirrors Get-SessionId's loud abort): a 200-but-shapeless GET (no usable
  # .state) must WARN, not be silently logged as the fallback -- else 'UNKNOWN' is ambiguous between
  # "GET threw" (warned above) and "GET returned junk" (otherwise silent). Array-safe scalarize.
  if ($null -ne $fetched -and [string]::IsNullOrWhiteSpace([string](@($fetched.state)[0]))) {
    Write-Warning "gate5: GET /sessions/$sid returned no usable state (shape: $($fetched | ConvertTo-Json -Depth 3 -Compress)); audit state from create-response/UNKNOWN."
  }
  $state = Resolve-AuditState -Fetched $fetched -CreateState $created.state
  Write-Audit "$ts | $Repo | $Target | $sid | $state | $Title$forcedTag"
  Write-Host "DISPATCHED session $sid (state=$state). Audit-log: $log"
  exit 0
} catch {
  Write-Error "ABORT gate5: dispatch POST failed ($($_.Exception.Message))"
  exit 1
}
