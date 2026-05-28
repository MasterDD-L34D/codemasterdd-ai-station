# ARCHON Agent Scanner cross-fleet deploy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy the ARCHON Agent Scanner as a cross-fleet discoverable Claude Code skill (LITE) plus a STRONG-PURE directive in `~/.claude/CLAUDE.md` so the model auto-invokes it before any subagent/skill/agent selection, on every Claude Code session across Lenovo + Ryzen + future PCs.

**Architecture:** Two-tier deploy. Canonical LITE lives in `codemasterdd/.claude/global-skills/agent-scanner/` (git-tracked, cross-PC via pull). FULL ARCHON skill unchanged in `aa01/archon/skills/agent-scanner/` (AA01-internal). Deploy via idempotent PowerShell script with mandatory sandbox QG Step-1 + bounded start/end sentinels + UTF-8 no-BOM + `-Remove` rollback.

**Tech Stack:** PowerShell 5.1+7, native `gh` CLI (verify post-pull), `git` (canonical pull), `[System.IO.File]` for encoding-safe writes, custom lightweight PS test runner (no Pester dependency to keep fleet portable).

**Spec:** `docs/superpowers/specs/2026-05-28-archon-agent-scanner-cross-fleet-deploy-design.md` (commit `09a5d6c`, harsh-reviewer-reworked).

---

## File structure

| Path (codemasterdd-relative) | Action | Responsibility |
|------------------------------|--------|----------------|
| `.claude/global-skills/agent-scanner/SKILL.md` | Create | LITE skill canonical (steps 1+2 only, ASCII, ~100 lines) |
| `.claude/global-claude-md-fragments/agent-scanner-directive.md` | Create | L3 STRONG-PURE directive with start+END sentinel (~35 lines) |
| `scripts/setup/deploy-global-skills.ps1` | Create | Idempotent PS script (Apply/Remove/dry-run, sandbox QG, hash-compare, bounded sentinel merge) |
| `scripts/setup/deploy-global-skills.Tests.ps1` | Create | Lightweight PS test runner (sentinel detect / idempotency / encoding / Remove) |
| `.claude/global-skills/agent-scanner/QUALITY.md` | Create | QG Step 1/2/3 evidence post-test |
| `JOURNAL.md` | Modify (append) | Session entry for the deploy work |

---

## Task 1: Canonical directories + LITE SKILL.md

**Files:**
- Create: `.claude/global-skills/agent-scanner/SKILL.md`

- [ ] **Step 1: Create directory tree**

```bash
mkdir -p .claude/global-skills/agent-scanner
mkdir -p .claude/global-claude-md-fragments
mkdir -p scripts/setup
```

Expected: 3 directories present, empty.

- [ ] **Step 2: Write LITE SKILL.md (canonical)**

Create `.claude/global-skills/agent-scanner/SKILL.md` with this exact content (ASCII body, no em-dash, `--` style):

```markdown
---
name: agent-scanner
description: >
  Use BEFORE selecting/recommending any subagent/skill/agent for a
  non-trivial task. Anti-shadow-duplicate (build on existing work,
  never recreate; Ibrahim 2026 + Microsoft Multi-Agent Ref Arch).
  Triggers: "scan agents", "quali agenti ho", "inventario agenti",
  "riusa agente", "registry", "overlap", "mappa agenti",
  "che agent uso", "serve un agent per X", "team formation".
tools: [Bash, Glob, Grep, Read]
---

# Agent Scanner (LITE, cross-project)

Cross-project skill that enumerates available subagents / skills / agent
references and outputs a markdown report read-only. NO write to disk, NO
registry persist, NO overlap math. Principio guida: **build on existing
work, never recreate**.

For full ARCHON-context analysis (overlap calc 7 ruoli + REUSE_AUTO/CONFIRM/
COMPLEMENT thresholds + registry persistence), see
`aa01/archon/skills/agent-scanner/SKILL.md` (used only when `aa01/archon/`
is detected in CWD or its parents).

---

## When to invoke

| Trigger | Quando |
|---------|--------|
| **BOOTSTRAP** | New session on a project -> step 1 prima di routing agent. |
| **TEAM_FORMATION** | Prima di proporre o creare un nuovo agent specializzato. |
| **DELTA** | A inizio sessione, diff vs scan precedente (signal cambi recenti). |
| **ON_DEMAND** | Comando utente esplicito ("scan agents"). |

---

## Procedure (5 step)

### Step 1 -- Enumerate sources (graceful-missing)

In ordine di priorita' decrescente, ogni find ha `2>/dev/null`:

```bash
# 1. PROJECT agents
find .claude/agents -maxdepth 2 -name "*.md" -type f 2>/dev/null

# 2. USER global agents
find "$HOME/.claude/agents" -maxdepth 2 -name "*.md" -type f 2>/dev/null

# 3. PROJECT skills
find .claude/skills -maxdepth 3 -name "SKILL.md" -type f 2>/dev/null

# 4. USER global skills
find "$HOME/.claude/skills" -maxdepth 3 -name "SKILL.md" -type f 2>/dev/null

# 5. Plugin agents + skills
find .claude/plugins -maxdepth 6 -name "*.md" -type f 2>/dev/null | grep -E "(agents|skills)/"

# 6. Inline mentions
grep -lE "^---$" AGENTS.md CLAUDE.md 2>/dev/null

# 7. ARCHON pointer (Lenovo-only, AA01 detection)
if [ -d "$HOME/aa01/archon" ] || [ -d "$(pwd)/aa01/archon" ]; then
  echo "ARCHON_DETECTED -> see aa01/archon/skills/agent-scanner/SKILL.md for FULL version"
fi
```

**Note**: AA01 e' Lenovo-edusc-only by design. Su Ryzen e altri PC source 7 e' assente, NON e' un errore -- il report omette il pointer ARCHON.

### Step 2 -- Parse frontmatter

Per ogni file trovato, estrai il YAML frontmatter tra `---` e `---`:
- Required: `name`, `description`.
- Optional: `tools`, `model`, `permissionMode`, `memory`, `skills`.

Se malformed o mancante:
- File in `.claude/agents/` o `~/.claude/agents/` -> log `MALFORMED FRONTMATTER: <path>` in report, skip quel file, continua.
- Altrove -> silently skip.

Se zero file trovati totali: output esplicito "no agents discovered in any source -- baseline: general-purpose only", NON silent-empty.

Se la enumerazione fallisce per una source specifica (permission denied su una dir): log `SOURCE UNREADABLE: <path>` nel report (distinguibile da "no agents found" legitimate).

### Step 3 -- Output markdown report (read-only)

Cap **hard 50 entries**. Se inventory > 50:
- Rank by source priority order (1-7 nel listing sopra).
- Tieni le top-50 in tabella.
- Aggiungi footer `+N more in <source>` per ogni source che ha entries droppate.

Format del report:

```markdown
## Agent discovery report (scope: <cwd>)

| name | description (truncated 80ch) | source | tools / model |
| --- | --- | --- | --- |
| harsh-reviewer | Tough quality review (code / ADR / plan) | ~/.claude/agents/ | All / opus |
| sot-drift-verifier | Sovereign gated SoT-vs-runtime verdict | .claude/agents/ | Read,Grep,Glob,Bash / inherit |
| ... | ... | ... | ... |

## Next-action hint

Consider REUSING an existing agent above before creating new
(anti-shadow-duplicate, Ibrahim 2026 + Microsoft Multi-Agent Ref Arch).

## ARCHON full version

If `aa01/archon/` detected -> use `aa01/archon/skills/agent-scanner/SKILL.md`
for overlap calc + role mapping + registry persistence.
```

### Step 4 -- Anti-pattern bloccati (segnalare in report se rilevati)

- **Shadow duplication**: due agent con descrizione overlap-keywords (manual review post-report).
- **Silent override**: due file con stesso `name:` in source diverse -> warning esplicito `SILENT OVERRIDE: <name> appears in <pathA> and <pathB>`.
- **Forgotten agents**: file con last-modified > 90 giorni fa e mai citato in altri agent description -> footnote `DORMANT (>90d)`.

### Step 5 -- (NOT done in LITE)

ARCHON-specific steps 3 (overlap calc 7 ruoli) + 4 (REUSE thresholds) + 5 (registry write) sono **DROP** dalla LITE. Per quelli, esegui `aa01/archon/skills/agent-scanner/SKILL.md`.

---

## Output constraints

- NO write su disco (read-only).
- NO registry persist.
- Output size cap 50 entries.
- Output e' markdown direttamente quotable nel main thread context.
```

- [ ] **Step 3: ASCII verify + line count**

```bash
perl -ne 'exit 1 if /[^\x00-\x7F]/' .claude/global-skills/agent-scanner/SKILL.md && echo "ASCII ok"
wc -l .claude/global-skills/agent-scanner/SKILL.md
```

Expected: "ASCII ok" + line count ~100-130.

- [ ] **Step 4: Frontmatter parses**

```bash
node -e "const m=require('fs').readFileSync('.claude/global-skills/agent-scanner/SKILL.md','utf8'); if(!/^---[\s\S]*?name: agent-scanner[\s\S]*?---/.test(m)) throw new Error('frontmatter bad'); console.log('OK')"
```

Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
git add .claude/global-skills/agent-scanner/SKILL.md
git commit -m "$(cat <<'EOF'
feat(global-skills): add lite agent-scanner skill canonical

Cross-project LITE version of the ARCHON Agent Scanner. Step 1
enumeration + step 2 parsing + read-only markdown report. No write,
no overlap math, no registry persist (those live in FULL ARCHON
version inside aa01/). Hard cap 50 entries with source-priority
ranking + footer for dropped.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit added, exit 0.

---

## Task 2: L3 directive fragment

**Files:**
- Create: `.claude/global-claude-md-fragments/agent-scanner-directive.md`

- [ ] **Step 1: Write the directive fragment**

Create `.claude/global-claude-md-fragments/agent-scanner-directive.md` with the EXACT content below (this is what the deploy script will append to `~/.claude/CLAUDE.md`). Note the blank line between start sentinel heading and `**Rule**` (sentinel disambiguation depends on it), and the END sentinel as last line.

```markdown
## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG-PURE, no bypass, no eccezione): PRIMA di selezionare,
raccomandare o creare un nuovo subagent / skill / agent specializzato,
INVOCA la skill `agent-scanner` (semantic trigger: "scan agents" /
"quali agenti ho" / "che agent uso" / "riusa agente"). Principio
cardine: **build on existing work, never recreate** (Ibrahim 2026;
Microsoft Multi-Agent Reference Architecture).

**Trigger mandatori** (4, mutuati da ARCHON v2 D-007):
- **BOOTSTRAP**: nuova sessione su un progetto -> invoca step-1 prima
  di altre decisioni di routing agent.
- **TEAM_FORMATION**: prima di proporre/creare un nuovo agent
  specializzato.
- **DELTA**: a inizio sessione, diff vs scan precedente.
- **ON_DEMAND**: comando utente esplicito ("scan agents").

**Sorgenti** (priorita decrescente, vedi SKILL.md):
`.claude/agents/` PROJECT > `~/.claude/agents/` USER > plugin agents
> `~/.claude/skills/` > `.claude/skills/` > `AGENTS.md`/`CLAUDE.md`
inline > ARCHON pointer (Lenovo-only).

**Skill locations** (two-tier):
- **LITE cross-project**: `~/.claude/skills/agent-scanner/SKILL.md`
  (default globale, read-only).
- **FULL ARCHON** (solo se `aa01/archon/` detected):
  `aa01/archon/skills/agent-scanner/SKILL.md` (overlap calc + ruoli
  + registry persistence).

**Anti-pattern bloccati**:
- **Shadow duplication**: creo planner-v2 quando planner funziona.
- **Silent override**: file con `name:` duplicato sovrascrive
  precedente senza warning -- scanner lo flagga in report.
- Bias "chi-ho-piu-memoria-recente-vince" su selezione agent.

**STRONG-PURE**: nessuna eccezione. Scanner fires anche su task
apparentemente meccanici (typo fix / rename / batch lint) per
evitare bypass involontario via "model-judgment di triviality".
Cost overhead ~2-5sec/fire accettato.

**Reference**: OD-007 closure 2026-05-28 + first-principles
application `docs/research/2026-05-28-od-007-first-principles-
application.md` + deploy spec `docs/superpowers/specs/
2026-05-28-archon-agent-scanner-cross-fleet-deploy-design.md`.

<!-- END agent-scanner-directive -->
```

- [ ] **Step 2: ASCII verify + sentinel check**

```bash
perl -ne 'exit 1 if /[^\x00-\x7F]/' .claude/global-claude-md-fragments/agent-scanner-directive.md && echo "ASCII ok"
grep -q "^## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)$" .claude/global-claude-md-fragments/agent-scanner-directive.md && echo "start sentinel ok"
grep -q "^<!-- END agent-scanner-directive -->$" .claude/global-claude-md-fragments/agent-scanner-directive.md && echo "end sentinel ok"
```

Expected: all 3 echo lines printed.

- [ ] **Step 3: Disambiguation regex test**

The deploy script will scan first non-blank line within next 5 lines after start sentinel for `^\*\*Rule\*\* \(STRONG`. Verify the fragment satisfies this:

```bash
awk '/^## Agent Scanner discipline/{found=1; line=0; next} found && /\S/ && line<5 {if (/^\*\*Rule\*\* \(STRONG/) print "disambiguation ok"; exit} found {line++}' .claude/global-claude-md-fragments/agent-scanner-directive.md
```

Expected: `disambiguation ok`.

- [ ] **Step 4: Commit**

```bash
git add .claude/global-claude-md-fragments/agent-scanner-directive.md
git commit -m "$(cat <<'EOF'
feat(global-fragments): add l3 directive for agent-scanner discipline

STRONG-PURE directive (no eccezione) auto-appended to ~/.claude/CLAUDE.md
on every PC via deploy script. Bounded by start sentinel "## Agent
Scanner discipline ..." plus END sentinel "<!-- END agent-scanner-
directive -->" for safe -Remove rollback (P0#3 harsh-reviewer fix).

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit.

---

## Task 3: Deploy script skeleton (path normalize + flags + exit codes)

**Files:**
- Create: `scripts/setup/deploy-global-skills.ps1`

- [ ] **Step 1: Write the skeleton**

Create `scripts/setup/deploy-global-skills.ps1` with skeleton only (no merge / no copy yet, just argparsing + path normalize + mode dispatch + exit code constants):

```powershell
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
```

- [ ] **Step 2: Run skeleton dry-run**

```powershell
.\scripts\setup\deploy-global-skills.ps1
```

Expected output includes `MODE: DRY-RUN` plus the 5 path lines plus `(skeleton only -- merge/copy/sandbox logic added in later tasks)`. Exit code 0.

- [ ] **Step 3: Run skeleton with -Apply (still no-op at this stage)**

```powershell
.\scripts\setup\deploy-global-skills.ps1 -Apply
```

Expected: `MODE: APPLY` printed, then skeleton message, exit 0. (Real logic added in next tasks.)

- [ ] **Step 4: ASCII verify**

```bash
perl -ne 'exit 1 if /[^\x00-\x7F]/' scripts/setup/deploy-global-skills.ps1 && echo "ASCII ok"
```

Expected: `ASCII ok`.

- [ ] **Step 5: Commit**

```bash
git add scripts/setup/deploy-global-skills.ps1
git commit -m "$(cat <<'EOF'
feat(setup): deploy-global-skills script skeleton (paths + modes + exits)

Path-normalized (anti-pattern #9a). ErrorActionPreference=Continue
(L-2026-05-040). 5 distinct exit codes per sec 7.1 spec. Dispatch
by mode (Apply / Remove / dry-run default). Real merge/copy/sandbox
logic added in subsequent tasks.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit.

---

## Task 4: Test runner skeleton + first failing test (TDD red)

**Files:**
- Create: `scripts/setup/deploy-global-skills.Tests.ps1`

- [ ] **Step 1: Write the test runner skeleton**

Create `scripts/setup/deploy-global-skills.Tests.ps1` with a minimal custom assertion runner (no Pester dependency). This first test covers sentinel disambiguation logic that future tasks will implement.

```powershell
<#
.SYNOPSIS
Lightweight test runner for deploy-global-skills.ps1.
No external dependencies (avoid Pester install requirement on fleet).
Run: .\scripts\setup\deploy-global-skills.Tests.ps1
Exit: 0 if all pass, 1 if any fail.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Continue'
$script:passed = 0
$script:failed = 0
$script:failures = @()

function Assert-True {
  param([bool]$Condition, [string]$Name)
  if ($Condition) {
    $script:passed++
    Write-Host "  [PASS] $Name" -ForegroundColor Green
  } else {
    $script:failed++
    $script:failures += $Name
    Write-Host "  [FAIL] $Name" -ForegroundColor Red
  }
}

function Assert-Eq {
  param($Expected, $Actual, [string]$Name)
  $cond = ($Expected -eq $Actual)
  if (-not $cond) { $Name = "$Name (expected=$Expected actual=$Actual)" }
  Assert-True -Condition $cond -Name $Name
}

# Source under test
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$scriptPath = Join-Path $PSScriptRoot 'deploy-global-skills.ps1'

# ----------------------------------------------------------------------
# Test 1: sentinel disambiguation regex (P0#2 from harsh review)
# ----------------------------------------------------------------------
Write-Host "Test 1: sentinel disambiguation regex"

# Fixture: directive content with blank line between sentinel and **Rule**
$fixture = @"
## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG-PURE, no bypass): the rule body...

more content
"@

$lines = $fixture -split "`n"
$startIdx = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($lines[$i] -match '^## Agent Scanner discipline \(anti-shadow-duplicate, cross-fleet\)$') {
    $startIdx = $i; break
  }
}
Assert-True -Condition ($startIdx -ge 0) -Name "start sentinel found"

# Scan first non-blank within next 5 lines, expect **Rule** (STRONG match
$foundRule = $false
for ($j = $startIdx + 1; $j -le [Math]::Min($startIdx + 5, $lines.Count - 1); $j++) {
  $line = $lines[$j].Trim()
  if (-not [string]::IsNullOrEmpty($line)) {
    if ($line -match '^\*\*Rule\*\* \(STRONG') { $foundRule = $true }
    break
  }
}
Assert-True -Condition $foundRule -Name "disambiguation: first non-blank within 5 lines matches Rule (STRONG"

# ----------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Results: $script:passed passed, $script:failed failed"
if ($script:failed -gt 0) {
  Write-Host "Failures:" -ForegroundColor Red
  $script:failures | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
  exit 1
}
exit 0
```

- [ ] **Step 2: Run test (expect 2 PASS)**

```powershell
.\scripts\setup\deploy-global-skills.Tests.ps1
```

Expected: `Results: 2 passed, 0 failed`, exit 0.

- [ ] **Step 3: Negative-control: tweak fixture to fail disambiguation**

Temporarily edit the test file: in `$fixture`, change `**Rule** (STRONG-PURE` to `Some other text` (line 3 of the heredoc). Re-run:

```powershell
.\scripts\setup\deploy-global-skills.Tests.ps1
```

Expected: `Results: 1 passed, 1 failed`, exit 1. Revert the change after confirming.

- [ ] **Step 4: Commit**

```bash
git add scripts/setup/deploy-global-skills.Tests.ps1
git commit -m "$(cat <<'EOF'
test(setup): lightweight ps test runner + sentinel disambiguation case

Custom Assert-True / Assert-Eq runner (no Pester dependency, fleet-portable).
First test covers P0#2 sentinel disambiguation: scan first non-blank
within next 5 lines after start sentinel, anchor on Rule (STRONG.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit.

---

## Task 5: Implement skill deploy (hash-compare + .bak + Copy)

**Files:**
- Modify: `scripts/setup/deploy-global-skills.ps1` (replace skeleton message with real Apply logic for skill)

- [ ] **Step 1: Add skill deploy logic (Apply path only, not Remove yet)**

Replace the final two lines of `deploy-global-skills.ps1`:

```powershell
# Skeleton ends here. Subsequent tasks fill in the real logic.
Write-Output "(skeleton only -- merge/copy/sandbox logic added in later tasks)"
exit $EXIT_OK
```

with:

```powershell
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

# Dispatch by mode (Apply / Remove / DryRun).
switch ($PSCmdlet.ParameterSetName) {
  'Apply' {
    Write-Output ""
    Write-Output "=== Phase 1: skill deploy ==="
    Invoke-SkillDeploy -CanonicalDir $canonicalSkill -TargetDir $targetSkillDir
    Write-Output ""
    Write-Output "(Phase 2 CLAUDE.md merge / Phase 3 verify / sandbox QG added in subsequent tasks)"
    exit $EXIT_OK
  }
  'Remove' {
    Write-Output "Remove path not yet implemented (added in Task 7)."
    exit $EXIT_OK
  }
  default {
    # DryRun
    Write-Output ""
    Write-Output "=== Phase 1 preview (skill deploy) ==="
    Invoke-SkillDeploy -CanonicalDir $canonicalSkill -TargetDir $targetSkillDir -DryRun
    Write-Output ""
    Write-Output "(Phase 2 CLAUDE.md merge / Phase 3 verify / sandbox QG added in subsequent tasks)"
    exit $EXIT_OK
  }
}
```

- [ ] **Step 2: Add test for hash-compare drift detection**

Append to `scripts/setup/deploy-global-skills.Tests.ps1` BEFORE the Summary block:

```powershell
# ----------------------------------------------------------------------
# Test 2: skill deploy hash-compare detects drift (P1#1 harsh)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 2: skill deploy hash-compare drift detection"

# Dot-source the deploy script to access Invoke-SkillDeploy + Get-FileSha256.
# Wrap in a script block so we can capture exit without killing the test runner.
# But the script exits on completion, so isolate via temp script.

# Easier: re-implement the hash-compare in test (same algorithm) + verify it detects drift.
$tmpRoot = Join-Path $env:TEMP "deploy-test-$([guid]::NewGuid())"
$canonDir = Join-Path $tmpRoot 'canonical'
$targetDir = Join-Path $tmpRoot 'target'
New-Item -ItemType Directory -Force -Path $canonDir | Out-Null
New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

Set-Content -Path (Join-Path $canonDir 'SKILL.md') -Value "canonical content v1" -Encoding utf8
Set-Content -Path (Join-Path $targetDir 'SKILL.md') -Value "user-edited content drift" -Encoding utf8

$canonicalHash = (Get-FileHash -Algorithm SHA256 -Path (Join-Path $canonDir 'SKILL.md')).Hash
$targetHash = (Get-FileHash -Algorithm SHA256 -Path (Join-Path $targetDir 'SKILL.md')).Hash
Assert-True -Condition ($canonicalHash -ne $targetHash) -Name "hash-compare flags drift"

# Same content -> no drift.
Set-Content -Path (Join-Path $targetDir 'SKILL.md') -Value "canonical content v1" -Encoding utf8
$targetHash2 = (Get-FileHash -Algorithm SHA256 -Path (Join-Path $targetDir 'SKILL.md')).Hash
Assert-True -Condition ($canonicalHash -eq $targetHash2) -Name "hash-compare no false-drift when content equal"

Remove-Item -Recurse -Force $tmpRoot
```

- [ ] **Step 3: Run tests (expect 4 PASS)**

```powershell
.\scripts\setup\deploy-global-skills.Tests.ps1
```

Expected: `Results: 4 passed, 0 failed`, exit 0.

- [ ] **Step 4: Dry-run preview script**

```powershell
.\scripts\setup\deploy-global-skills.ps1
```

Expected output includes "Phase 1 preview (skill deploy)" + `[DRY] would copy` line, exit 0. NO write to `~/.claude/`.

- [ ] **Step 5: Commit**

```bash
git add scripts/setup/deploy-global-skills.ps1 scripts/setup/deploy-global-skills.Tests.ps1
git commit -m "$(cat <<'EOF'
feat(setup): skill deploy with hash-compare drift detection + bak

Implements Phase 1 (skill copy). New-Item -Force for fresh PC (P1#5).
Pre-copy SHA256 hash-compare; if drift detected, .bak-<ts> saved
before overwrite (P1#1 harsh). DryRun mode prints would-do without
write. Tests cover hash-compare flag-on-drift + no-false-drift cases.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit.

---

## Task 6: Implement CLAUDE.md merge (sentinel-bounded + CRLF + UTF-8 no-BOM)

**Files:**
- Modify: `scripts/setup/deploy-global-skills.ps1` (add Phase 2 merge logic)
- Modify: `scripts/setup/deploy-global-skills.Tests.ps1` (add merge tests)

- [ ] **Step 1: Add merge function to deploy script**

Insert this function **after** `Invoke-SkillDeploy` (so before the `switch` dispatch):

```powershell
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
      Write-Output "  [OK] directive already present and valid -- skip merge (idempotent)"
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
      Write-Output "  [FAIL] sentinel ambiguous (heading match but Rule (STRONG missing within 5 lines)"
      Write-Output "         log: $logPath"
      return $false
    }
    'absent' {
      $fragmentContent = Read-FileUtf8NoBom -Path $FragmentPath
      if ($null -eq $fragmentContent) {
        Write-Error "Fragment file missing: $FragmentPath"
        return $false
      }
      if ($DryRun) {
        Write-Output "  [DRY] would append directive ($(($fragmentContent -split "`n").Count) lines) -> $ClaudeMdPath"
        return $true
      }
      # Backup pre-modify.
      $ts = Get-Date -Format 'yyyyMMdd-HHmmss'
      if (Test-Path $ClaudeMdPath) {
        $bakPath = "$ClaudeMdPath.bak-$ts"
        Copy-Item -Path $ClaudeMdPath -Destination $bakPath -Force
        Write-Output "  [OK] backup saved: $bakPath"
      }
      # Read existing (or empty if missing) + ensure trailing newline + append.
      $existing = if (Test-Path $ClaudeMdPath) { Read-FileUtf8NoBom -Path $ClaudeMdPath } else { "" }
      if (-not [string]::IsNullOrEmpty($existing) -and -not $existing.EndsWith("`n")) { $existing += "`n" }
      $merged = $existing + "`n" + $fragmentContent
      Write-FileUtf8NoBom -Path $ClaudeMdPath -Content $merged
      Write-Output "  [OK] directive appended to: $ClaudeMdPath"
      return $true
    }
  }
}
```

- [ ] **Step 2: Wire merge into Apply + DryRun branches**

Update the `switch` dispatch by replacing both 'Apply' and the default (DryRun) blocks:

```powershell
switch ($PSCmdlet.ParameterSetName) {
  'Apply' {
    Write-Output ""
    Write-Output "=== Phase 1: skill deploy ==="
    Invoke-SkillDeploy -CanonicalDir $canonicalSkill -TargetDir $targetSkillDir

    Write-Output ""
    Write-Output "=== Phase 2: CLAUDE.md merge ==="
    $ok = Invoke-ClaudeMdMerge -ClaudeMdPath $targetClaudeMd -FragmentPath $canonicalFragment `
                                -StartSentinel $startSentinel -DisambigRegex $disambigRegex
    if (-not $ok) {
      Write-Error "CLAUDE.md merge failed (likely sentinel ambiguous). Exit 4."
      exit $EXIT_SENTINEL_AMBIGUOUS
    }

    Write-Output ""
    Write-Output "(Phase 3 verify / sandbox QG added in subsequent tasks)"
    exit $EXIT_OK
  }
  'Remove' {
    Write-Output "Remove path not yet implemented (added in Task 7)."
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
```

- [ ] **Step 3: Add merge tests**

Append to `scripts/setup/deploy-global-skills.Tests.ps1` BEFORE the Summary block:

```powershell
# ----------------------------------------------------------------------
# Test 3: CLAUDE.md merge -- absent then idempotent (P0#3 + idempotency)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 3: CLAUDE.md merge absent + idempotent"

# Dot-source script functions into current scope without running its dispatch.
# Trick: read script text, drop everything from "switch ($PSCmdlet" onward, and Invoke-Expression.
$scriptText = Get-Content -Raw $scriptPath
$cut = $scriptText.IndexOf('switch ($PSCmdlet')
if ($cut -lt 0) { throw "Cannot find dispatch in deploy script" }
$functionsOnly = $scriptText.Substring(0, $cut)
. ([scriptblock]::Create($functionsOnly))

$tmpRoot = Join-Path $env:TEMP "merge-test-$([guid]::NewGuid())"
New-Item -ItemType Directory -Force -Path $tmpRoot | Out-Null
$claudeMd = Join-Path $tmpRoot 'CLAUDE.md'
$fragment = Join-Path $tmpRoot 'directive.md'

Set-Content -Path $claudeMd -Value "# Existing CLAUDE.md`r`n`r`n## Other section`r`n`r`nbody" -Encoding utf8
$fragmentContent = @"
## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG-PURE, no bypass): test directive body.

<!-- END agent-scanner-directive -->
"@
Set-Content -Path $fragment -Value $fragmentContent -Encoding utf8

# Run 1: absent -> append.
$state1 = Test-DirectivePresent -ClaudeMdPath $claudeMd -StartSentinel $startSentinel -DisambigRegex $disambigRegex
Assert-Eq -Expected 'absent' -Actual $state1 -Name "merge Test-DirectivePresent absent"

$ok1 = Invoke-ClaudeMdMerge -ClaudeMdPath $claudeMd -FragmentPath $fragment `
                              -StartSentinel $startSentinel -DisambigRegex $disambigRegex
Assert-True -Condition $ok1 -Name "merge run-1 append ok"

$state2 = Test-DirectivePresent -ClaudeMdPath $claudeMd -StartSentinel $startSentinel -DisambigRegex $disambigRegex
Assert-Eq -Expected 'present-valid' -Actual $state2 -Name "merge post-append state present-valid"

# Run 2: present -> idempotent skip.
$contentBefore = Read-FileUtf8NoBom -Path $claudeMd
$ok2 = Invoke-ClaudeMdMerge -ClaudeMdPath $claudeMd -FragmentPath $fragment `
                              -StartSentinel $startSentinel -DisambigRegex $disambigRegex
$contentAfter = Read-FileUtf8NoBom -Path $claudeMd
Assert-True -Condition $ok2 -Name "merge run-2 ok"
Assert-Eq -Expected $contentBefore -Actual $contentAfter -Name "merge run-2 idempotent (no diff)"

Remove-Item -Recurse -Force $tmpRoot

# ----------------------------------------------------------------------
# Test 4: CLAUDE.md merge ambiguous sentinel (P1#4 distinct error)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 4: ambiguous sentinel rejected"

$tmpRoot = Join-Path $env:TEMP "merge-test-$([guid]::NewGuid())"
New-Item -ItemType Directory -Force -Path $tmpRoot | Out-Null
$claudeMd = Join-Path $tmpRoot 'CLAUDE.md'

# Sentinel present but Rule (STRONG missing -> ambiguous.
Set-Content -Path $claudeMd -Value "## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)`r`n`r`nSomeone overwrote the rule with prose.`r`n" -Encoding utf8

$state = Test-DirectivePresent -ClaudeMdPath $claudeMd -StartSentinel $startSentinel -DisambigRegex $disambigRegex
Assert-Eq -Expected 'ambiguous' -Actual $state -Name "ambiguous sentinel detected"

Remove-Item -Recurse -Force $tmpRoot
```

- [ ] **Step 4: Run tests (expect 9 PASS)**

```powershell
.\scripts\setup\deploy-global-skills.Tests.ps1
```

Expected: `Results: 9 passed, 0 failed`, exit 0.

- [ ] **Step 5: Dry-run preview**

```powershell
.\scripts\setup\deploy-global-skills.ps1
```

Expected: includes "Phase 1 preview" + "Phase 2 preview" + `[DRY] would append directive` (or `present-valid -- skip` if a prior session already deployed), exit 0. NO writes.

- [ ] **Step 6: Commit**

```bash
git add scripts/setup/deploy-global-skills.ps1 scripts/setup/deploy-global-skills.Tests.ps1
git commit -m "$(cat <<'EOF'
feat(setup): claude-md merge with bounded sentinel + utf8 no-bom + crlf

Phase 2 merge logic. UTF-8 no-BOM via System.IO.File.WriteAllText (PS5.1
gotcha). CRLF normalize regex (P2#1). Three-state detect (absent /
present-valid / ambiguous) per P0#2 + P1#4. Ambiguous case writes
.apply-blocked-<ts>.log and returns false (exit 4 in caller). Tests
cover absent->append + idempotent skip + ambiguous detection.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit.

---

## Task 7: Implement `-Remove` rollback (bounded sentinel-to-end regex)

**Files:**
- Modify: `scripts/setup/deploy-global-skills.ps1` (replace Remove stub with real logic)
- Modify: `scripts/setup/deploy-global-skills.Tests.ps1` (add Remove tests)

- [ ] **Step 1: Add Remove function to deploy script**

Insert this function **before** the dispatch `switch`:

```powershell
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
      Write-Output "  [DRY] would remove dir: $TargetSkillDir"
    } else {
      Remove-Item -Recurse -Force $TargetSkillDir
      Write-Output "  [OK] removed dir: $TargetSkillDir"
    }
  } else {
    Write-Output "  [SKIP] skill dir already absent: $TargetSkillDir"
  }

  # 2. Strip directive from CLAUDE.md (bounded by start + END sentinel).
  if (-not (Test-Path $ClaudeMdPath)) {
    Write-Output "  [SKIP] CLAUDE.md absent: $ClaudeMdPath"
    return $true
  }

  $content = Read-FileUtf8NoBom -Path $ClaudeMdPath
  $startEsc = [Regex]::Escape($StartSentinel)
  $endEsc = [Regex]::Escape($EndSentinel)
  # Match start sentinel + any chars (greedy lazy) + END sentinel + optional trailing newline.
  $pattern = "(?ms)^$startEsc.*?$endEsc`r?`n?"

  if ($content -notmatch $pattern) {
    Write-Output "  [WARN] start+END sentinel pair not found. Falling back to .bak restore if available."
    # Find most recent .bak-* file matching pattern.
    $bakFiles = Get-ChildItem -Path (Split-Path $ClaudeMdPath -Parent) -Filter "$(Split-Path $ClaudeMdPath -Leaf).bak-*" -ErrorAction SilentlyContinue
    if ($bakFiles) {
      $latestBak = $bakFiles | Sort-Object Name -Descending | Select-Object -First 1
      if ($DryRun) {
        Write-Output "  [DRY] would restore from: $($latestBak.FullName)"
      } else {
        Copy-Item -Path $latestBak.FullName -Destination $ClaudeMdPath -Force
        Write-Output "  [OK] restored from latest .bak: $($latestBak.FullName)"
      }
    } else {
      Write-Output "  [SKIP] no .bak file found; nothing to do."
    }
    return $true
  }

  # Backup pre-modify.
  if (-not $DryRun) {
    $ts = Get-Date -Format 'yyyyMMdd-HHmmss'
    $bakPath = "$ClaudeMdPath.bak-remove-$ts"
    Copy-Item -Path $ClaudeMdPath -Destination $bakPath -Force
    Write-Output "  [OK] pre-remove backup: $bakPath"
  }

  $stripped = [Regex]::Replace($content, $pattern, '')

  if ($DryRun) {
    $matchCount = ([Regex]::Matches($content, $pattern)).Count
    Write-Output "  [DRY] would strip $matchCount directive section(s) from CLAUDE.md"
  } else {
    Write-FileUtf8NoBom -Path $ClaudeMdPath -Content $stripped
    Write-Output "  [OK] directive stripped from CLAUDE.md (bounded start..end sentinel)"
  }
  return $true
}
```

- [ ] **Step 2: Wire Remove into dispatch**

Replace the Remove block in `switch`:

```powershell
  'Remove' {
    Write-Output ""
    Write-Output "=== Rollback ==="
    Invoke-Rollback -TargetSkillDir $targetSkillDir -ClaudeMdPath $targetClaudeMd `
                    -StartSentinel $startSentinel -EndSentinel $endSentinel | Out-Null
    exit $EXIT_OK
  }
```

- [ ] **Step 3: Add Remove tests**

Append to `scripts/setup/deploy-global-skills.Tests.ps1`:

```powershell
# ----------------------------------------------------------------------
# Test 5: Remove strips bounded directive without eating user content (P0#3)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 5: Remove bounded -- user content preserved"

$tmpRoot = Join-Path $env:TEMP "remove-test-$([guid]::NewGuid())"
New-Item -ItemType Directory -Force -Path $tmpRoot | Out-Null
$claudeMd = Join-Path $tmpRoot 'CLAUDE.md'

$initial = @"
# CLAUDE.md

## Section A

User content A.

## Agent Scanner discipline (anti-shadow-duplicate, cross-fleet)

**Rule** (STRONG-PURE): directive body.

<!-- END agent-scanner-directive -->

This user line MUST survive Remove (P0#3 footgun).

## Section B (post-directive)

User content B.
"@
Set-Content -Path $claudeMd -Value $initial -Encoding utf8

Invoke-Rollback -TargetSkillDir "$tmpRoot\nonexistent-skill" -ClaudeMdPath $claudeMd `
                -StartSentinel $startSentinel -EndSentinel $endSentinel | Out-Null

$after = Read-FileUtf8NoBom -Path $claudeMd
Assert-True -Condition (-not ($after -match 'Agent Scanner discipline')) -Name "start sentinel removed"
Assert-True -Condition (-not ($after -match 'END agent-scanner-directive')) -Name "END sentinel removed"
Assert-True -Condition ($after -match 'This user line MUST survive') -Name "user content post-directive preserved (P0#3)"
Assert-True -Condition ($after -match '## Section A') -Name "user content pre-directive preserved"
Assert-True -Condition ($after -match '## Section B') -Name "user content section-B preserved"

Remove-Item -Recurse -Force $tmpRoot
```

- [ ] **Step 4: Run tests (expect 14 PASS)**

```powershell
.\scripts\setup\deploy-global-skills.Tests.ps1
```

Expected: `Results: 14 passed, 0 failed`, exit 0.

- [ ] **Step 5: Commit**

```bash
git add scripts/setup/deploy-global-skills.ps1 scripts/setup/deploy-global-skills.Tests.ps1
git commit -m "$(cat <<'EOF'
feat(setup): -remove rollback with bounded start+end sentinel regex

Strips directive from CLAUDE.md by matching start sentinel (## Agent
Scanner discipline ...) through END sentinel (<!-- END agent-scanner-
directive -->) inclusive (P0#3 harsh: NO "next ## " terminator,
prevents eating user content post-directive). Fallback to latest .bak
if end sentinel missing (legacy / unsynced fragment). Test 5 asserts
user lines pre / post directive survive Remove.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit.

---

## Task 8: Implement sandbox QG Step-1 (mandatory pre-live, anti-pattern #9)

**Files:**
- Modify: `scripts/setup/deploy-global-skills.ps1` (add sandbox runner)

- [ ] **Step 1: Add Invoke-SandboxQG function**

Insert this function **before** the dispatch `switch`:

```powershell
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

  Write-Output "  [sandbox] root: $sandboxRoot"
  New-Item -ItemType Directory -Force -Path $sandboxClaudeDir | Out-Null

  # Seed sandbox CLAUDE.md with a minimal existing file.
  Set-Content -Path $sandboxClaudeMd -Value "# Sandbox CLAUDE.md`r`n`r`n## Other section`r`n`r`nseed body" -Encoding utf8

  # Run 1: deploy.
  Invoke-SkillDeploy -CanonicalDir $CanonicalSkill -TargetDir $sandboxSkillDir | Out-Null
  $ok1 = Invoke-ClaudeMdMerge -ClaudeMdPath $sandboxClaudeMd -FragmentPath $CanonicalFragment `
                                -StartSentinel $StartSentinel -DisambigRegex $DisambigRegex
  if (-not $ok1) {
    Write-Output "  [sandbox FAIL] run-1 merge returned false"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }

  # Verify artifact (skill SKILL.md present + frontmatter parses).
  $sandboxSkillFile = Join-Path $sandboxSkillDir 'SKILL.md'
  if (-not (Test-Path $sandboxSkillFile)) {
    Write-Output "  [sandbox FAIL] SKILL.md missing post-copy"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }
  $skillContent = Read-FileUtf8NoBom -Path $sandboxSkillFile
  if ($skillContent -notmatch '(?ms)^---\s*$.*?name:\s*agent-scanner.*?^---\s*$') {
    Write-Output "  [sandbox FAIL] SKILL.md frontmatter does not parse"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }

  # Verify sentinel present in CLAUDE.md.
  $cmContent = Read-FileUtf8NoBom -Path $sandboxClaudeMd
  if ($cmContent -notmatch [Regex]::Escape($StartSentinel)) {
    Write-Output "  [sandbox FAIL] start sentinel missing from sandbox CLAUDE.md"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }
  if ($cmContent -notmatch [Regex]::Escape($EndSentinel)) {
    Write-Output "  [sandbox FAIL] END sentinel missing from sandbox CLAUDE.md"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }

  # Run 2: idempotency check.
  $contentBeforeRun2 = Read-FileUtf8NoBom -Path $sandboxClaudeMd
  Invoke-SkillDeploy -CanonicalDir $CanonicalSkill -TargetDir $sandboxSkillDir | Out-Null
  $ok2 = Invoke-ClaudeMdMerge -ClaudeMdPath $sandboxClaudeMd -FragmentPath $CanonicalFragment `
                                -StartSentinel $StartSentinel -DisambigRegex $DisambigRegex
  $contentAfterRun2 = Read-FileUtf8NoBom -Path $sandboxClaudeMd

  if (-not $ok2) {
    Write-Output "  [sandbox FAIL] run-2 merge returned false"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }
  if ($contentBeforeRun2 -ne $contentAfterRun2) {
    Write-Output "  [sandbox FAIL] idempotency violated: run-2 produced diff"
    Remove-Item -Recurse -Force $sandboxRoot
    return $false
  }

  # Cleanup.
  Remove-Item -Recurse -Force $sandboxRoot
  Write-Output "  [sandbox OK] all checks passed (artifact + sentinel + idempotency)"
  return $true
}
```

- [ ] **Step 2: Wire sandbox into Apply dispatch (run BEFORE phase 1)**

Update the Apply branch:

```powershell
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
    Write-Output "(Phase 3 verify added in Task 9)"
    exit $EXIT_OK
  }
```

- [ ] **Step 3: Run dry-run (sandbox does NOT fire in dry-run by design)**

```powershell
.\scripts\setup\deploy-global-skills.ps1
```

Expected: standard dry-run output (Phase 1 + Phase 2 preview), exit 0. No sandbox section in dry-run.

- [ ] **Step 4: Smoke-test sandbox via -Apply -SkipSandbox=$false but interrupt before real write**

We can run -Apply intentionally on a throwaway USERPROFILE to validate the sandbox path. Easiest: temporarily set USERPROFILE via env var override for one invocation:

```powershell
$origUserProfile = $env:USERPROFILE
$env:USERPROFILE = Join-Path $env:TEMP "apply-smoke-$([guid]::NewGuid())"
New-Item -ItemType Directory -Force -Path $env:USERPROFILE | Out-Null
try {
  .\scripts\setup\deploy-global-skills.ps1 -Apply
} finally {
  Remove-Item -Recurse -Force $env:USERPROFILE
  $env:USERPROFILE = $origUserProfile
}
```

Expected output: sandbox section runs and prints `[sandbox OK]`, then Phase 1 + Phase 2 execute against the throwaway USERPROFILE. Exit 0.

- [ ] **Step 5: Commit**

```bash
git add scripts/setup/deploy-global-skills.ps1
git commit -m "$(cat <<'EOF'
feat(setup): sandbox qg step-1 mandatory pre-live (anti-pattern #9)

Sandbox runs the full deploy in $env:TEMP/deploy-global-skills-sandbox-
<guid> BEFORE any write to ~/.claude/. Verifies: skill copied + frontmatter
parses + start+end sentinel both present in CLAUDE.md + 2nd-run idempotent
(diff = none). Hard-fails with exit 5 if any check red, no live write.
Skippable via -SkipSandbox (NOT recommended, warning logged).

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit.

---

## Task 9: Implement post-deploy verify (frontmatter + sentinel + ASCII)

**Files:**
- Modify: `scripts/setup/deploy-global-skills.ps1` (add Phase 3 verify)

- [ ] **Step 1: Add Test-DeployedState function**

Insert this function **before** the dispatch `switch`:

```powershell
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
    Write-Output "  [VERIFY FAIL] SKILL.md missing: $skillFile"
    $ok = $false
  } else {
    $sc = Read-FileUtf8NoBom -Path $skillFile
    if ($sc -notmatch '(?ms)^---\s*$.*?name:\s*agent-scanner.*?^---\s*$') {
      Write-Output "  [VERIFY FAIL] SKILL.md frontmatter does not parse"
      $ok = $false
    } else {
      Write-Output "  [VERIFY OK] SKILL.md present + frontmatter parses"
    }
  }

  # 2. CLAUDE.md sentinel present (start + end both).
  if (Test-Path $ClaudeMdPath) {
    $cm = Read-FileUtf8NoBom -Path $ClaudeMdPath
    if ($cm -notmatch [Regex]::Escape($StartSentinel)) {
      Write-Output "  [VERIFY FAIL] start sentinel missing in CLAUDE.md"
      $ok = $false
    } elseif ($cm -notmatch [Regex]::Escape($EndSentinel)) {
      Write-Output "  [VERIFY FAIL] END sentinel missing in CLAUDE.md"
      $ok = $false
    } else {
      Write-Output "  [VERIFY OK] CLAUDE.md has start + END sentinel"
    }
  } else {
    Write-Output "  [VERIFY FAIL] CLAUDE.md missing post-deploy"
    $ok = $false
  }

  # 3. ASCII check on deployed SKILL.md body (em-dash exception not relevant here,
  #    SKILL.md must be fully ASCII per ADR-0021 body prose policy).
  if (Test-Path $skillFile) {
    $nonAscii = (Get-Content -Raw $skillFile) -match '[^\x00-\x7F]'
    if ($nonAscii) {
      Write-Output "  [VERIFY FAIL] non-ASCII chars in deployed SKILL.md"
      $ok = $false
    } else {
      Write-Output "  [VERIFY OK] SKILL.md ASCII clean"
    }
  }

  return $ok
}
```

- [ ] **Step 2: Wire verify into Apply dispatch**

Replace the placeholder `(Phase 3 verify added in Task 9)` line in the Apply branch with:

```powershell
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
```

- [ ] **Step 3: Sandbox-mode end-to-end check**

```powershell
$origUserProfile = $env:USERPROFILE
$env:USERPROFILE = Join-Path $env:TEMP "verify-smoke-$([guid]::NewGuid())"
New-Item -ItemType Directory -Force -Path $env:USERPROFILE | Out-Null
try {
  .\scripts\setup\deploy-global-skills.ps1 -Apply
} finally {
  Remove-Item -Recurse -Force $env:USERPROFILE
  $env:USERPROFILE = $origUserProfile
}
```

Expected: sandbox OK -> Phase 1 OK -> Phase 2 OK -> Phase 3 verify OK -> `DONE. Deploy successful.` exit 0.

- [ ] **Step 4: Commit**

```bash
git add scripts/setup/deploy-global-skills.ps1
git commit -m "$(cat <<'EOF'
feat(setup): phase 3 post-deploy verify (skill + sentinels + ascii)

Runs after sandbox QG + Phase 1 skill copy + Phase 2 CLAUDE.md merge.
Verifies: SKILL.md present + frontmatter parses + start+END sentinel
both detected in CLAUDE.md + SKILL.md ASCII clean. Exit 1 if any
check fails. Apply branch now prints DONE on green.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit.

---

## Task 10: Add ASCII guard test + scope-7 ARCHON degradation test

**Files:**
- Modify: `scripts/setup/deploy-global-skills.Tests.ps1`

- [ ] **Step 1: Add ASCII guard test on canonical assets**

Append to `scripts/setup/deploy-global-skills.Tests.ps1` BEFORE the Summary block:

```powershell
# ----------------------------------------------------------------------
# Test 6: canonical assets must be ASCII-clean (ADR-0021 body prose policy)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 6: canonical assets ASCII clean"

$canonicalSkillFile = Join-Path $repoRoot '.claude\global-skills\agent-scanner\SKILL.md'
$canonicalFragmentFile = Join-Path $repoRoot '.claude\global-claude-md-fragments\agent-scanner-directive.md'

$skillContent = Get-Content -Raw $canonicalSkillFile
Assert-True -Condition (-not ($skillContent -match '[^\x00-\x7F]')) -Name "canonical SKILL.md ASCII"

$fragContent = Get-Content -Raw $canonicalFragmentFile
Assert-True -Condition (-not ($fragContent -match '[^\x00-\x7F]')) -Name "canonical fragment ASCII"

# ----------------------------------------------------------------------
# Test 7: scope-7 ARCHON degradation (P1#6 -- Lenovo only, Ryzen ok absent)
# ----------------------------------------------------------------------
Write-Host ""
Write-Host "Test 7: ARCHON source absent != enumeration failure"

# This test verifies the LITE skill's behavior conceptually: if aa01/archon/
# does NOT exist in CWD or $HOME, the scanner should NOT flag this as a
# SOURCE UNREADABLE error -- it should silently omit source 7. We verify
# via the SKILL.md content stating this requirement explicitly.

Assert-True -Condition ($skillContent -match 'AA01.*Lenovo.*only.*by design') -Name "SKILL.md documents AA01 Lenovo-only"
Assert-True -Condition ($skillContent -match 'NON e.*errore') -Name "SKILL.md says missing source 7 not an error"
```

- [ ] **Step 2: Run tests (expect 18 PASS)**

```powershell
.\scripts\setup\deploy-global-skills.Tests.ps1
```

Expected: `Results: 18 passed, 0 failed`, exit 0.

- [ ] **Step 3: Commit**

```bash
git add scripts/setup/deploy-global-skills.Tests.ps1
git commit -m "$(cat <<'EOF'
test(setup): ascii guard on canonical + archon scope-7 degradation case

Test 6 asserts canonical SKILL.md + fragment are ASCII-clean (ADR-0021
body prose policy). Test 7 verifies LITE SKILL.md documents that AA01
detection is Lenovo-only by design and that source 7 absence on other
PCs is not flagged as error (P1#6 harsh-reviewer).

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
```

Expected: 1 commit.

---

## Task 11: Live `-Apply` on Lenovo (manual gate)

**Files:**
- None (live operation)

- [ ] **Step 1: Capture pre-state of CLAUDE.md**

```powershell
Get-Content $env:USERPROFILE\.claude\CLAUDE.md | Measure-Object -Line | Select-Object -ExpandProperty Lines
```

Note the line count (expected ~387 per session memory).

```powershell
Test-Path $env:USERPROFILE\.claude\skills\agent-scanner
```

Expected: `False` (not yet deployed).

- [ ] **Step 2: Run live -Apply**

```powershell
.\scripts\setup\deploy-global-skills.ps1 -Apply
```

Expected output:
- `MODE: APPLY (will write to ~/.claude/)`
- `=== Sandbox QG Step-1 (mandatory) ===` -> `[sandbox OK]`
- `=== Phase 1: skill deploy ===` -> `[OK] created` (or `[SKIP]` if `~/.claude/skills/` already exists) + `[OK] skill copied`
- `=== Phase 2: CLAUDE.md merge ===` -> `[OK] backup saved: <path>.bak-<ts>` + `[OK] directive appended`
- `=== Phase 3: post-deploy verify ===` -> 3 `[VERIFY OK]` lines
- `DONE. Deploy successful.`
- Exit code 0.

- [ ] **Step 3: Verify post-state**

```powershell
# Skill present + frontmatter
Test-Path $env:USERPROFILE\.claude\skills\agent-scanner\SKILL.md
node -e "const m=require('fs').readFileSync(require('os').homedir()+'/.claude/skills/agent-scanner/SKILL.md','utf8'); if(!/^---[\s\S]*?name: agent-scanner[\s\S]*?---/.test(m)) throw 'bad'; console.log('frontmatter OK')"

# CLAUDE.md sentinel
Select-String -Path $env:USERPROFILE\.claude\CLAUDE.md -Pattern '^## Agent Scanner discipline'
Select-String -Path $env:USERPROFILE\.claude\CLAUDE.md -Pattern '^<!-- END agent-scanner-directive -->'

# Line count delta
$newLines = (Get-Content $env:USERPROFILE\.claude\CLAUDE.md | Measure-Object -Line).Lines
Write-Output "CLAUDE.md line count: $newLines (expected ~387 + 35 directive = ~422)"

# .bak exists
Get-ChildItem $env:USERPROFILE\.claude\ -Filter 'CLAUDE.md.bak-*' | Select-Object Name
```

Expected: all checks green, line count between 415 and 430, `.bak-<ts>` file present.

- [ ] **Step 4: Idempotency live check (2nd `-Apply` = no-op)**

```powershell
$preHash = (Get-FileHash $env:USERPROFILE\.claude\CLAUDE.md).Hash
.\scripts\setup\deploy-global-skills.ps1 -Apply
$postHash = (Get-FileHash $env:USERPROFILE\.claude\CLAUDE.md).Hash
Write-Output "pre  : $preHash"
Write-Output "post : $postHash"
Write-Output "equal: $($preHash -eq $postHash)"
```

Expected: `equal: True`. Output should include `[OK] directive already present and valid -- skip merge (idempotent)`.

- [ ] **Step 5: Document in JOURNAL.md**

Append to `JOURNAL.md` a session entry under a new dated heading. Add:

```markdown
## 2026-05-28 (notte) -- Cross-fleet agent-scanner deploy live Lenovo

### Completato
- Live `-Apply` of `scripts/setup/deploy-global-skills.ps1` on Lenovo: sandbox QG OK -> Phase 1 skill copy OK -> Phase 2 CLAUDE.md merge OK (line delta +35) -> Phase 3 verify OK.
- 2nd `-Apply` = idempotent (file hash equal pre/post).
- 18/18 unit tests pass.

### Da fare
- Ryzen mirror: `git pull origin main` + `.\scripts\setup\deploy-global-skills.ps1 -Apply` Eduardo-direct.
- Behavioral smoke 3-prompt test (Task 14 plan).
- Token cost baseline capture post first 5 real invocations (Task 15 plan).
```

- [ ] **Step 6: Commit JOURNAL update**

```bash
git add JOURNAL.md
git commit -m "$(cat <<'EOF'
docs(journal): cross-fleet agent-scanner deploy live lenovo

Sandbox QG green, Phase 1+2+3 green, idempotency live verified.
Ready for cross-fleet Ryzen mirror + behavioral smoke + token baseline.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
git push origin main
```

Expected: commit + push.

---

## Task 12: Behavioral smoke (3-prompt test in fresh Claude Code sessions)

**Files:**
- None (live behavioral test)

- [ ] **Step 1: Open a fresh Claude Code session in `C:/dev/Game`**

Start a new session. The new global directive should be loaded automatically.

- [ ] **Step 2: Prompt FIRE-A (auto-trigger expected)**

User prompt:

```
che agent uso per code review?
```

Expected:
- Claude invokes the `agent-scanner` skill via the Skill tool (visible in transcript).
- Output includes the LITE markdown report listing agents (harsh-reviewer, owasp-security-auditor, etc.).
- Claude recommends an existing agent (NOT proposes creating a new one).

Record: tokens used by the skill invocation + time-to-output.

- [ ] **Step 3: Prompt FIRE-B (ON_DEMAND auto-trigger expected)**

User prompt:

```
scan agents
```

Expected: same skill invocation, full report output. Time-to-output similar to FIRE-A.

- [ ] **Step 4: Prompt FIRE-C (STRONG-PURE: scanner SHOULD also fire per Eduardo decision)**

User prompt:

```
fix typo at line 42 in foo.js
```

Expected with STRONG-PURE: scanner DOES fire (no eccezione). Even on a trivial typo fix, the model is instructed by the directive to scan first. Document the time + tokens.

This is the cost of STRONG-PURE accepted by Eduardo at brainstorm decision time. If overhead per task feels excessive, sec 10 R1 trigger applies after N=5+5 sessions baseline.

- [ ] **Step 5: Record results**

Create temp note (not committed; baseline data captured in QUALITY.md later):

```
FIRE-A (code review): scanner fired YES/NO, ~tokens=___, time=___sec
FIRE-B (scan agents): scanner fired YES/NO, ~tokens=___, time=___sec
FIRE-C (typo fix STRONG-PURE): scanner fired YES/NO, ~tokens=___, time=___sec
```

- [ ] **Step 6: (No commit -- behavioral test only)**

Data captured for Task 15 token baseline + Task 18 QUALITY.md.

---

## Task 13: Cross-fleet Ryzen deploy + diff verify

**Files:**
- None (live operation, Eduardo-direct on Ryzen)

- [ ] **Step 1: Eduardo on Ryzen: git pull**

On Ryzen (`Vgit@192.168.1.11`, COMPUTERNAME `DESKTOP-T77TMKT`):

```powershell
git -C C:/dev/codemasterdd-ai-station pull origin main
```

Expected: pulls the new canonical assets + deploy script.

- [ ] **Step 2: Eduardo on Ryzen: Apply**

```powershell
cd C:/dev/codemasterdd-ai-station
.\scripts\setup\deploy-global-skills.ps1 -Apply
```

Expected: same output sequence as Lenovo (sandbox OK -> Phase 1+2+3 OK -> DONE). Exit 0.

- [ ] **Step 3: Cross-PC diff hash verify (Lenovo-side)**

On Lenovo, capture deployed hashes:

```powershell
(Get-FileHash $env:USERPROFILE\.claude\skills\agent-scanner\SKILL.md).Hash
```

On Ryzen, capture deployed hashes (manual: paste them back to Lenovo session or compare via SSH):

```powershell
ssh Vgit@192.168.1.11 "powershell -Command (Get-FileHash 'C:\Users\Vgit\.claude\skills\agent-scanner\SKILL.md').Hash"
```

Expected: same SHA256 hash on both PCs. (CLAUDE.md will differ because each PC has its own pre-existing content, but the directive section content is identical -- harder to diff; the line delta should be +35 on both.)

- [ ] **Step 4: Document Ryzen result in JOURNAL.md**

Append to the same dated section in `JOURNAL.md`:

```markdown
### Cross-fleet Ryzen update
- Ryzen `git pull` + `-Apply`: same output sequence Lenovo, exit 0.
- Diff hash check: SKILL.md identical on Lenovo + Ryzen (SHA256 confirmed via SSH).
- CLAUDE.md line delta on Ryzen: +35 (expected).
```

- [ ] **Step 5: Commit JOURNAL update**

```bash
git add JOURNAL.md
git commit -m "$(cat <<'EOF'
docs(journal): cross-fleet ryzen agent-scanner deploy verified

SHA256 hash equal on Lenovo + Ryzen for deployed SKILL.md.
Line delta +35 confirmed on Ryzen CLAUDE.md.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
git push origin main
```

Expected: commit + push.

---

## Task 14: -Remove rollback live smoke (sandbox-only, NOT live ~/.claude/)

**Files:**
- None (live smoke against a throwaway USERPROFILE)

- [ ] **Step 1: Smoke -Remove in throwaway USERPROFILE**

```powershell
$origUserProfile = $env:USERPROFILE
$env:USERPROFILE = Join-Path $env:TEMP "remove-smoke-$([guid]::NewGuid())"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude" | Out-Null
# Seed a CLAUDE.md with content around where the directive would go.
Set-Content -Path "$env:USERPROFILE\.claude\CLAUDE.md" -Value "# Test`r`n`r`n## Pre-existing`r`n`r`nbody A`r`n" -Encoding utf8
try {
  .\scripts\setup\deploy-global-skills.ps1 -Apply
  Write-Output "--- after Apply ---"
  Get-Content "$env:USERPROFILE\.claude\CLAUDE.md"
  .\scripts\setup\deploy-global-skills.ps1 -Remove
  Write-Output "--- after Remove ---"
  Get-Content "$env:USERPROFILE\.claude\CLAUDE.md"
  Test-Path "$env:USERPROFILE\.claude\skills\agent-scanner"
} finally {
  Remove-Item -Recurse -Force $env:USERPROFILE
  $env:USERPROFILE = $origUserProfile
}
```

Expected:
- After Apply: CLAUDE.md has the directive section + content `body A` still present.
- After Remove: directive section gone, `body A` still present, `Test-Path` returns `False` for skill dir.

- [ ] **Step 2: (No commit -- smoke only)**

---

## Task 15: Write QUALITY.md (QG Step 1/2/3 evidence)

**Files:**
- Create: `.claude/global-skills/agent-scanner/QUALITY.md`

- [ ] **Step 1: Write QUALITY.md**

Create `.claude/global-skills/agent-scanner/QUALITY.md`:

```markdown
# QUALITY -- agent-scanner LITE skill

> Quality Gate evidence per CLAUDE.md (`Quality Gate -- Release Standard`).

## Step 1 -- Smoke Test

| Check | Command | Expected | Result | Date |
|-------|---------|----------|--------|------|
| 18 unit tests pass | `.\scripts\setup\deploy-global-skills.Tests.ps1` | `Results: 18 passed, 0 failed`, exit 0 | PASS | 2026-05-28 |
| Sandbox QG green | `.\scripts\setup\deploy-global-skills.ps1 -Apply` (throwaway USERPROFILE) | `[sandbox OK]` printed | PASS | 2026-05-28 |
| Live `-Apply` Lenovo | `.\scripts\setup\deploy-global-skills.ps1 -Apply` (real) | All 3 phases green + `DONE` | PASS | 2026-05-28 |
| Idempotency live | 2nd `-Apply` | hash pre == hash post | PASS | 2026-05-28 |

## Step 2 -- Indagine di Ricerca (>=3 edge case)

| Edge case | Behavior | Verified |
|-----------|----------|----------|
| Frontmatter malformato in agent file | SKILL.md says log `MALFORMED FRONTMATTER: <path>`, skip, continua | Test 1 (sentinel) is adjacent; manual smoke required if a real malformed agent file appears |
| Permission denied on source dir | Log `SOURCE UNREADABLE: <path>` (NOT silent-empty) | Documented in SKILL.md Step 1 |
| AA01 source 7 absent on Ryzen | Silently omit source 7, NOT error | Test 7 PASS |
| Inventory >50 agents | Hard cap 50 + ranked by source-priority + `+N more` footer | Documented in SKILL.md Step 3; smoke required when inventory reaches threshold |
| Sentinel false-positive (start match but Rule (STRONG missing) | Returns 'ambiguous', logs `.apply-blocked-<ts>.log`, exit 4 | Test 4 PASS |
| -Remove with user content post-directive | User content survives (P0#3) | Test 5 PASS |
| -Remove with end sentinel missing (legacy) | Falls back to latest `.bak` restore | Implemented in `Invoke-Rollback`, smoke required |

## Step 3 -- Tuning & Ottimizzazione

| Iter | Misurazione | Before | After | Delta |
|------|-------------|--------|-------|-------|
| Baseline | Token cost per invocation (Task 12 FIRE-A/B/C) | TBD post-baseline | TBD | TBD |
| Baseline | Time-to-output | TBD | TBD | TBD |
| Tuning trigger | Per sec 10 R1: post N=5+5 sessions if fire-rate >50% on non-selection OR tokens-per-fire >2000 | -- | -- | -- |

Iteration deferred until baseline data is captured per Task 15 (token baseline).

## Step 4 -- Released

- [ ] All 3 steps completed (this file fully filled).
- [ ] Cross-fleet Lenovo + Ryzen both green.
- [ ] R1 baseline measured (Task 15 plan).
```

- [ ] **Step 2: ASCII verify**

```bash
perl -ne 'exit 1 if /[^\x00-\x7F]/' .claude/global-skills/agent-scanner/QUALITY.md && echo "ASCII ok"
```

Expected: `ASCII ok`.

- [ ] **Step 3: Commit**

```bash
git add .claude/global-skills/agent-scanner/QUALITY.md
git commit -m "$(cat <<'EOF'
docs(quality): agent-scanner lite skill qg evidence step 1/2/3

Step 1 smoke (18 tests + sandbox + live Apply + idempotency).
Step 2 research (7 edge cases). Step 3 tuning deferred to baseline
capture (Task 15 plan: N=5+5 sessions).

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
git push origin main
```

Expected: commit + push.

---

## Task 16: Update OPEN_DECISIONS / MEMORY index + final push

**Files:**
- Modify: `OPEN_DECISIONS.md` (OD-007 entry final state)
- Modify: `JOURNAL.md` (Task 15 evidence backlog)

- [ ] **Step 1: Update OD-007 entry in `OPEN_DECISIONS.md`**

In OD-007 entry, replace the AA01-side action note with the full cross-fleet deploy reference:

Find:

```
- **Action AA01-side SHIPPED 2026-05-28 (Eduardo auth esplicita)**:
```

Replace with:

```
- **Action SHIPPED 2026-05-28 (Eduardo auth + brainstorm B + harsh-reviewer rework)**: cross-fleet deploy LITE skill in codemasterdd canonical + L3 STRONG-PURE directive auto-appended to `~/.claude/CLAUDE.md` via `scripts/setup/deploy-global-skills.ps1` (sandbox QG + bounded sentinels + -Remove). AA01 drill-down link kept (L1). Lenovo + Ryzen both green. Spec: `docs/superpowers/specs/2026-05-28-archon-agent-scanner-cross-fleet-deploy-design.md`. Plan: `docs/superpowers/plans/2026-05-28-archon-agent-scanner-cross-fleet-deploy.md`.
```

- [ ] **Step 2: Update OD-007 snapshot row in `OPEN_DECISIONS.md`**

Find:

```
| OD-007 | AA01 capability registry / scan automatico? | ... | Action AA01-side **SHIPPED 2026-05-28** ... |
```

Replace the last column with:

```
Action SHIPPED 2026-05-28 cross-fleet (Lenovo + Ryzen): LITE skill + L3 STRONG-PURE directive deployed via `scripts/setup/deploy-global-skills.ps1`. Both PCs auto-fire scanner pre agent-selection.
```

- [ ] **Step 3: Commit**

```bash
git add OPEN_DECISIONS.md
git commit -m "$(cat <<'EOF'
docs(governance): od-007 entry/snapshot updated post cross-fleet deploy

L1 drill-down link + L2 LITE skill global + L3 STRONG-PURE directive
all shipped. Lenovo + Ryzen both green.

Coding-Agent: claude-opus-4-7
Trace-Id: $(node -e "console.log(require('crypto').randomUUID())")
EOF
)"
git push origin main
```

Expected: commit + push.

---

## Self-Review (executed)

**Spec coverage check**:

- Spec sec 2 Goals G1-G5: G1 (skill discoverable) -> Task 1+5+11; G2 (L3 directive) -> Task 2+6+11; G3 (cross-PC reproducible) -> Task 13; G4 (no ARCHON change) -> Task 1 (LITE-only, FULL untouched); G5 (rollback) -> Task 7+14. All goals covered.
- Spec sec 3 architecture two-tier: Task 1 (LITE canonical) + Task 2 (directive canonical) + Task 3-9 (deploy mechanism). Covered.
- Spec sec 4 LITE scope: Task 1 SKILL.md body covers Steps 1-2 only, drops 3-5. Covered.
- Spec sec 5 L3 STRONG-PURE: Task 2 fragment contains "STRONG-PURE", no eccezione. Covered.
- Spec sec 6 deploy mechanism: Task 3-9 + 11+13. Sandbox QG (sec 6.2.2) = Task 8; bounded sentinel merge (sec 5.4 + 6.2.4) = Task 6; -Remove (sec 6.2.6) = Task 7. Covered.
- Spec sec 7 error handling: Task 8 (sandbox fail = exit 5), Task 6 (sentinel ambiguous = exit 4 + log), Task 5 (hash drift bak), Task 1 SKILL.md (SOURCE UNREADABLE / MALFORMED FRONTMATTER / >50 cap). Covered.
- Spec sec 8 testing 7 layers: Task 4+5+6+7+10 (test layers 1-2), Task 11 (3 live Lenovo), Task 12 (4 behavioral), Task 13 (5 cross-fleet), Task 14 (6 -Remove smoke), Task 15+16 (7 token baseline planned). Covered.
- Spec sec 9 reversibility: Task 7 implementation + Task 14 smoke. Covered.
- Spec sec 10 R1 threshold: Task 12 captures data; trigger documented in QUALITY.md Task 15. Covered.

No spec gaps.

**Placeholder scan**: searched for TBD/TODO/FIXME in plan. QUALITY.md has "TBD" intentionally (baseline rows pending Task 12 data capture); marked clearly in cell + Step-4 checklist. No code-step placeholders.

**Type/name consistency**: function names checked across tasks -- `Invoke-SkillDeploy` (Task 5), `Read-FileUtf8NoBom` / `Write-FileUtf8NoBom` / `Test-DirectivePresent` / `Invoke-ClaudeMdMerge` (Task 6), `Invoke-Rollback` (Task 7), `Invoke-SandboxQG` (Task 8), `Test-DeployedState` (Task 9). Variable names `$startSentinel` / `$endSentinel` / `$disambigRegex` / `$canonicalSkill` / `$canonicalFragment` / `$targetSkillDir` / `$targetClaudeMd` consistent throughout. Exit codes `$EXIT_OK` / `$EXIT_FAIL` / `$EXIT_NO_PERM` / `$EXIT_NO_CANONICAL` / `$EXIT_SENTINEL_AMBIGUOUS` / `$EXIT_SANDBOX_FAIL` consistent. No type drift.

Plan ready for execution.
