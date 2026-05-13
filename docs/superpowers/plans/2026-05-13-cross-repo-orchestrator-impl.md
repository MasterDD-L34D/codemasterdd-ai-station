# Cross-repo orchestrator pre-Max implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Component 2 (workflow + tracking + dry-run) + Component 3 (escalation gates + Gate E discipline) pre-Max. Component 1 dashboard NOT in scope (gated Gate E 30gg post-Max empirical).

**Architecture:** Doc-only + minimal PowerShell scripts. No new infrastructure, no Flask routes, no DB schema changes. Re-uses existing patterns: tracking markdown logs gitignored (already established `logs/aider-delegation-*.md`), schtasks weekly cron (already established `scripts/backup-api-keys.ps1` pattern + `scripts/smoke-test-hooks.ps1`), Aider whitelist guard rail (already established `~/.config/aider-privacy-whitelist.txt`).

**Tech Stack:** Markdown docs + PowerShell 5.1 (Windows 11) + schtasks scheduler + git + gh CLI. No new dependencies.

**Spec reference:** [docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md](../specs/2026-05-13-cross-repo-orchestrator-design.md) (V3, PR #87)

**Effort estimate:** ~2gg total pre-Max (~6-8h actual implementation + buffer). 14 tasks.

---

## File structure

**Component 2 — Proactive contributor channel** (4 files):
- `docs/cross-repo/PR_WORKFLOW.md` — workflow definition per cross-repo PR drafting (steps + PR type taxonomy + governance interna handling + dry-run protocol)
- `docs/cross-repo/PR_TEMPLATE.md` — markdown template per PR body cross-repo (issue + proposed change + ADR ref + privacy class + reversibility tier)
- `scripts/cross-repo/dry-run-pr.ps1` — dry-run validator: takes (repo target, PR type, file changes preview) → outputs DRAFT PR body to console + verifies privacy whitelist OK + verifies repo path exists + NO actual gh PR create
- `logs/cross-repo-pr-2026-05.md` — tracking template (gitignored via `logs/*`)

**Component 3 — Escalation gates + Gate E discipline** (5 files):
- `docs/cross-repo/ESCALATION_GATES.md` — Gate A/B/C/D/E criteria definitions + thresholds + escalation paths + revisability policy
- `scripts/cross-repo/coord-event-log.ps1` — helper script: interactive prompts (date/repo/severity 1-5/grep_count/cost_minutes/notes) → appends row to `logs/coord-events-YYYY-MM.md`
- `scripts/cross-repo/install-gate-e-reminder.ps1` — installs schtasks weekly Sunday 09:00 (matches existing `smoke-test-hooks.ps1` pattern) reminder to log events. Has `-DryRun` flag.
- `logs/coord-events-2026-05.md` — Gate E event tracking template (gitignored)
- `logs/escalation-gates-2026-05.md` — Gate A/B/C/D tracking template (gitignored)

**Test files** (smoke validators, NOT pytest):
- Manual smoke during build (run scripts with sample input, verify output) — no test framework setup needed for 2gg scope.

---

## Pre-flight check

- [ ] **Step 0.1: Verify worktree clean + on spec branch**

Run: `git -C C:/dev/codemasterdd-ai-station status --short && git -C C:/dev/codemasterdd-ai-station branch --show-current`
Expected: clean tree + branch `claude/cross-repo-orchestrator-spec-2026-05-13` OR new branch from main

- [ ] **Step 0.2: Confirm spec PR #87 exists**

Run: `gh pr view 87 --repo MasterDD-L34D/codemasterdd-ai-station --json state,title`
Expected: state OPEN, title "docs(spec): cross-repo orchestrator Opt 1.5 REDUCED design"

- [ ] **Step 0.3: Confirm scripts/ dir exists + check cross-repo/ subdir**

Run: `ls C:/dev/codemasterdd-ai-station/scripts/ 2>&1 ; ls C:/dev/codemasterdd-ai-station/scripts/cross-repo/ 2>&1`
Expected: scripts/ exists, cross-repo/ NOT yet (will create). Backup-api-keys.ps1 + smoke-test-hooks.ps1 visible (template references).

---

## Task 1: Bootstrap directory + docs/cross-repo/ scaffold

**Files:**
- Create: `docs/cross-repo/README.md`
- Create: `scripts/cross-repo/.gitkeep`

- [ ] **Step 1.1: Create docs/cross-repo/README.md as index**

Write:

```markdown
# Cross-repo coordination

Index per Component 2 (PR workflow) + Component 3 (escalation gates + Gate E discipline) — spec V3 Opt 1.5 REDUCED.

## Documenti

- [PR_WORKFLOW.md](PR_WORKFLOW.md) — workflow drafting PR cross-repo + governance interna handling
- [PR_TEMPLATE.md](PR_TEMPLATE.md) — body template PR cross-repo
- [ESCALATION_GATES.md](ESCALATION_GATES.md) — Gate A/B/C/D/E criteri + thresholds

## Scripts

- `scripts/cross-repo/dry-run-pr.ps1` — validatore dry-run pre-PR
- `scripts/cross-repo/coord-event-log.ps1` — helper logging coord events Gate E
- `scripts/cross-repo/install-gate-e-reminder.ps1` — schtasks weekly reminder

## Tracking logs (gitignored)

- `logs/cross-repo-pr-YYYY-MM.md` — PR outcome tracking
- `logs/coord-events-YYYY-MM.md` — Gate E event tracking
- `logs/escalation-gates-YYYY-MM.md` — Gate A/B/C/D tracking

## Riferimento spec

[docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md](../superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md) V3 (PR #87).
```

- [ ] **Step 1.2: Create empty scripts/cross-repo/.gitkeep**

Use Write tool: empty content (0 byte). Anchor dir in git.

- [ ] **Step 1.3: Verify files exist**

Run: `ls C:/dev/codemasterdd-ai-station/docs/cross-repo/ && ls C:/dev/codemasterdd-ai-station/scripts/cross-repo/`
Expected: README.md + .gitkeep visible.

- [ ] **Step 1.4: Commit bootstrap**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add docs/cross-repo/README.md scripts/cross-repo/.gitkeep
git -C C:/dev/codemasterdd-ai-station commit -m "feat(cross-repo): bootstrap docs + scripts directory"
```
Expected: commit succeeds, hook ADR-0011 PASS (subject <72ch + lowercase desc).

---

## Task 2: PR_WORKFLOW.md (Component 2 core doc)

**Files:**
- Create: `docs/cross-repo/PR_WORKFLOW.md`

- [ ] **Step 2.1: Write PR_WORKFLOW.md content**

Content sections (all required, no TBD):

```markdown
# Cross-repo PR workflow (Component 2)

> Spec ref: `docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md` V3 Opt 1.5 REDUCED PR #87

## Scope

Pattern write-via-PR L-012 (vault sibling-peer auth) esteso a **3 git repo target**:
- `MasterDD-L34D/Game` (Vue3)
- `MasterDD-L34D/Game-Godot-v2`
- `MasterDD-L34D/evo-swarm` (Dafne)

Plus 1 sibling-peer (vault) via L-012 per-task auth pattern esistente.

ESCLUSI da Component 2:
- AA01 (NON-git, alternative channel filesystem-direct via lesson promotion + inbox workflow personale Eduardo)
- Synesthesia (dormant + privacy mixed, fuori scope fino reactivation post UniUPO esame)

## PR type taxonomy

Ogni PR cross-repo deve avere type esplicito in PR title prefix:

| Type | Conv title prefix | When to use | Example |
|------|-------------------|-------------|---------|
| policy-alignment | `chore(policy):` | codemasterdd ADR Accepted impatta repo target | ADR-0021 encoding policy propagation a Game |
| ADR-cross-ref | `docs(adr):` | nuovo ADR codemasterdd cita repo target | ADR-0024 addendum a Game CLAUDE.md |
| drift-fix | `fix(drift):` | state diverge tra codemasterdd doc/memory e repo target reality | vault llm-routing.json IP hardcoded |
| docs | `docs:` | typo / link fix / cross-reference broken | Godot-v2 README link broken |
| governance-suggestion | `chore(governance):` | pattern noto codemasterdd applicable ma not yet adopted, SOFT-suggestion only | Protocol P1 Refresh-verify proposal |

## Workflow steps

1. **Identify cross-repo issue** durante uso normale codemasterdd (NO active scanning policy-driven, opportunistic only)
2. **Run dry-run validator**: `scripts/cross-repo/dry-run-pr.ps1 -RepoTarget <name> -Type <type> -PreviewFiles <paths>`
3. **Verify privacy whitelist** PASS (script auto-checks `~/.config/aider-privacy-whitelist.txt`)
4. **Draft PR** using template `docs/cross-repo/PR_TEMPLATE.md`
5. **Open PR** via `gh pr create` su repo target
6. **Log entry** in `logs/cross-repo-pr-YYYY-MM.md` con outcome PENDING
7. **Governance interna repo target** decide accept/reject/amend (decision time NON-controllable, days-weeks)
8. **Update log entry** con outcome finale + amend type se applicable

## Anti-pattern (avoid)

- Drafting PR senza dry-run (skip risk wrong-target)
- Auto-mode cross-repo PR drafting (richiede Eduardo authorization explicit each PR fino pattern proven >=1 acceptance)
- Bulk batching multiple PR senza tracking individual outcome
- Modifying file in target repo PRESERVED scope (es. Game-Godot-v2 governance interna CLAUDE.md territory)

## Reversibility tier (Gate D awareness)

Track cumulative PR accepted by external governance:
- **0-2 accepted**: full reversibility (~10min)
- **3-4 accepted**: graduated reversibility (~1-2h coordinated cleanup)
- **>=5 accepted**: soft lock-in confirmed → trigger Gate D → ADR formale per ritiro coordinato OR continuation explicit

Update Reversibility tier visible in `logs/cross-repo-pr-YYYY-MM.md` summary post-each accept.

## First 3 PR protocol (empirical validation)

I primi 3 PR accepted by external governance sono pattern-validating. Procedura:
1. Eduardo authorization EXPLICIT per ognuno (no auto-mode)
2. Outcome tracking dettagliato (response time + amend rate + comment count)
3. Post 3 acceptance → pattern validated → auto-mode acceptable per PR type validated

Pre-3rd-acceptance, ANY external governance reject → re-evaluate pattern (potential rescope a Component 2 declined).
```

- [ ] **Step 2.2: Verify Markdown parses + render readable**

Run: `cat C:/dev/codemasterdd-ai-station/docs/cross-repo/PR_WORKFLOW.md | head -30`
Expected: content displayed cleanly, headings rendered, table formatted.

- [ ] **Step 2.3: Commit**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add docs/cross-repo/PR_WORKFLOW.md
git -C C:/dev/codemasterdd-ai-station commit -m "feat(cross-repo): pr workflow doc with type taxonomy"
```

---

## Task 3: PR_TEMPLATE.md (Component 2 body template)

**Files:**
- Create: `docs/cross-repo/PR_TEMPLATE.md`

- [ ] **Step 3.1: Write PR_TEMPLATE.md content**

Content:

```markdown
# Cross-repo PR body template

Copy questo template come body quando apri PR cross-repo via Component 2 workflow.

---

## Summary

[1-2 frasi: cosa cambia + perché]

## Type

- Type: <policy-alignment | ADR-cross-ref | drift-fix | docs | governance-suggestion>
- codemasterdd ADR ref: <ADR-NNNN o N/A>
- L-XXX lesson ref: <L-2026-MM-NNN o N/A>

## Source codemasterdd

- Repo: `MasterDD-L34D/codemasterdd-ai-station`
- Branch/commit: <branch + commit hash>
- File ref originale: <docs/adr/0024-... o memory/...>

## Proposed change

- Files touched in this PR:
  - `path/to/file1.md`
  - `path/to/file2.py`
- Scope: minimal (NO functional behavior change unless drift-fix type)

## Privacy class

- Repo target privacy: <sovereign-only | mixed | cloud-OK>
- Whitelist check: PASSED (verified via `scripts/cross-repo/dry-run-pr.ps1`)
- Code shared con cloud LLM: <none | yes specify>

## Reversibility

- Reverting cost stimato: <minutes/hours/days>
- Cross-reference creates in this repo: <yes/no — if yes, list refs>

## Governance interna repo target

- Decision: governance interna autosufficiente, accept/reject/amend a vostra discrezione
- codemasterdd-side: NO write-direct, NO push --force, NO bypass review
- Eduardo coordinator: medierà eventuali round trip se serve

## Test plan (se applicabile)

- [ ] Lint/parse markdown se doc-only
- [ ] [Type-specific: ADR-cross-ref → verify cross-link bidirezionale; drift-fix → verify ground truth matches]

🤖 Generated with [Claude Code](https://claude.com/claude-code) via cross-repo Component 2 workflow
```

- [ ] **Step 3.2: Commit**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add docs/cross-repo/PR_TEMPLATE.md
git -C C:/dev/codemasterdd-ai-station commit -m "feat(cross-repo): pr body template with privacy + reversibility tracking"
```

---

## Task 4: dry-run-pr.ps1 (Component 2 validator)

**Files:**
- Create: `scripts/cross-repo/dry-run-pr.ps1`

- [ ] **Step 4.1: Write dry-run-pr.ps1**

Write script:

```powershell
<#
.SYNOPSIS
  Dry-run validator for cross-repo PR drafting (Component 2 spec V3 Opt 1.5 REDUCED).

.DESCRIPTION
  Validates pre-PR conditions WITHOUT calling gh pr create:
    1. Repo target is in whitelist allow-list (Game / Godot-v2 / Dafne / vault)
    2. Privacy whitelist check passes (~/.config/aider-privacy-whitelist.txt)
    3. Local repo path exists + is git repo
    4. PR type is valid taxonomy
    5. Preview files exist + are readable

  Outputs DRAFT PR body to console (does NOT push).

.PARAMETER RepoTarget
  Target repo: Game / Godot-v2 / Dafne / vault

.PARAMETER Type
  PR type: policy-alignment / ADR-cross-ref / drift-fix / docs / governance-suggestion

.PARAMETER PreviewFiles
  Comma-separated paths of files this PR will touch

.PARAMETER Summary
  1-2 line summary of proposed change

.EXAMPLE
  .\dry-run-pr.ps1 -RepoTarget Game -Type docs -PreviewFiles "README.md,docs/adr/index.md" -Summary "Fix broken link"
#>

param(
  [Parameter(Mandatory=$true)]
  [ValidateSet('Game', 'Godot-v2', 'Dafne', 'vault')]
  [string]$RepoTarget,

  [Parameter(Mandatory=$true)]
  [ValidateSet('policy-alignment', 'ADR-cross-ref', 'drift-fix', 'docs', 'governance-suggestion')]
  [string]$Type,

  [Parameter(Mandatory=$true)]
  [string]$PreviewFiles,

  [Parameter(Mandatory=$true)]
  [string]$Summary
)

$ErrorActionPreference = 'Stop'

# Repo path mapping (Lenovo defaults)
$repoMap = @{
  'Game'     = 'C:\dev\Game'
  'Godot-v2' = 'C:\dev\Game-Godot-v2'
  'Dafne'    = 'C:\Users\edusc\Dafne\workspace\swarm'
  'vault'    = 'C:\dev\vault-shared'
}

$repoPath = $repoMap[$RepoTarget]

Write-Host "=== Cross-repo PR dry-run validator ===" -ForegroundColor Cyan
Write-Host "Repo target: $RepoTarget ($repoPath)"
Write-Host "PR type: $Type"
Write-Host ""

# Check 1: repo path exists
if (-not (Test-Path $repoPath)) {
  Write-Host "FAIL [1]: repo path not found: $repoPath" -ForegroundColor Red
  exit 1
}
Write-Host "PASS [1] repo path exists" -ForegroundColor Green

# Check 2: is git repo
if (-not (Test-Path "$repoPath\.git")) {
  Write-Host "FAIL [2]: not a git repo (no .git dir): $repoPath" -ForegroundColor Red
  exit 1
}
Write-Host "PASS [2] is git repo" -ForegroundColor Green

# Check 3: privacy whitelist
$whitelistPath = "$env:USERPROFILE\.config\aider-privacy-whitelist.txt"
if (-not (Test-Path $whitelistPath)) {
  Write-Host "FAIL [3]: privacy whitelist not found: $whitelistPath" -ForegroundColor Red
  exit 1
}
$whitelist = Get-Content $whitelistPath
$repoMatchesWhitelist = $false
foreach ($line in $whitelist) {
  if ($line -like "*$RepoTarget*" -or $line -like "$repoPath*") {
    $repoMatchesWhitelist = $true
    break
  }
}
if (-not $repoMatchesWhitelist) {
  Write-Host "FAIL [3]: repo $RepoTarget NOT in privacy whitelist" -ForegroundColor Red
  exit 1
}
Write-Host "PASS [3] privacy whitelist" -ForegroundColor Green

# Check 4: preview files exist
$files = $PreviewFiles -split ','
foreach ($f in $files) {
  $f = $f.Trim()
  $fullPath = Join-Path $repoPath $f
  if (-not (Test-Path $fullPath)) {
    Write-Host "WARN [4]: preview file not found locally: $fullPath" -ForegroundColor Yellow
  } else {
    Write-Host "PASS [4] preview file exists: $f" -ForegroundColor Green
  }
}

# Output DRAFT PR body
Write-Host ""
Write-Host "=== DRAFT PR body (copy/paste into gh pr create) ===" -ForegroundColor Cyan
Write-Host ""
$body = @"
## Summary

$Summary

## Type

- Type: $Type
- codemasterdd ADR ref: <fill in ADR-NNNN or N/A>
- L-XXX lesson ref: <fill in L-2026-MM-NNN or N/A>

## Source codemasterdd

- Repo: ``MasterDD-L34D/codemasterdd-ai-station``
- Branch/commit: <fill in>
- File ref originale: <fill in>

## Proposed change

- Files touched in this PR:
$($files | ForEach-Object { "  - ``$($_.Trim())``" } | Out-String)

## Privacy class

- Repo target privacy: <fill in sovereign-only / mixed / cloud-OK>
- Whitelist check: PASSED (verified via dry-run-pr.ps1)

## Reversibility

- Reverting cost stimato: <minutes/hours/days>

## Governance interna repo target

- Decision: governance interna autosufficiente, accept/reject/amend a vostra discrezione
- codemasterdd-side: NO write-direct, NO push --force, NO bypass review

[Generated with Claude Code via cross-repo Component 2 workflow]
"@

Write-Host $body
Write-Host ""
Write-Host "=== Next steps ===" -ForegroundColor Cyan
Write-Host "1. cd $repoPath"
Write-Host "2. Make file changes on a new branch"
Write-Host "3. gh pr create --title '<type>(<scope>): <subject>' --body '<paste above>'"
Write-Host "4. Append outcome row to logs/cross-repo-pr-YYYY-MM.md"
Write-Host ""
Write-Host "DRY-RUN OK — no actual PR created." -ForegroundColor Green
exit 0
```

- [ ] **Step 4.2: Smoke test (success case)**

Run:
```powershell
powershell -File C:/dev/codemasterdd-ai-station/scripts/cross-repo/dry-run-pr.ps1 -RepoTarget Game -Type docs -PreviewFiles "README.md" -Summary "Smoke test dry-run"
```
Expected: 4 checks PASS (or WARN file not found), DRAFT PR body printed, "DRY-RUN OK" green at end. Exit 0.

- [ ] **Step 4.3: Smoke test (fail case — Synesthesia not in whitelist)**

Run:
```powershell
powershell -File C:/dev/codemasterdd-ai-station/scripts/cross-repo/dry-run-pr.ps1 -RepoTarget Synesthesia -Type docs -PreviewFiles "README.md" -Summary "Should fail"
```
Expected: PowerShell validation error "Cannot validate argument on parameter 'RepoTarget'" because Synesthesia not in ValidateSet. Exit non-zero.

- [ ] **Step 4.4: Commit**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add scripts/cross-repo/dry-run-pr.ps1
git -C C:/dev/codemasterdd-ai-station commit -m "feat(cross-repo): dry-run pr validator with privacy whitelist check"
```

---

## Task 5: cross-repo-pr-2026-05.md tracking template

**Files:**
- Create: `logs/cross-repo-pr-2026-05.md`

NOTE: `logs/*` is gitignored. File creato local only (not committed). Template è la "source-of-truth structure", non viene committato MA viene documentato in PR_WORKFLOW.md come reference. Per disciplina + per future Eduardo onboarding (es. nuovo PC), aggiungere anche template doc-only in repo.

- [ ] **Step 5.1: Create template doc (committed)**

Create `docs/cross-repo/_TEMPLATES/cross-repo-pr-tracking-template.md`:

```markdown
# Cross-repo PR tracking log

Template per `logs/cross-repo-pr-YYYY-MM.md` (gitignored). Copia in `logs/` quando inizia nuovo mese.

## Cumulative summary (top of file)

- Total PR opened this month: 0
- Accepted by external governance: 0
- Rejected: 0
- Amended (PR closed + new opened): 0
- Reversibility tier current: 0-2 accepted = full reversibility

## Per-PR entries

| # | Date opened | Repo | PR # | Type | Title | Outcome | Date closed | Response time (days) | Amend rate | Comment count | Notes |
|---|-------------|------|------|------|-------|---------|-------------|---------------------|------------|---------------|-------|
| 1 | 2026-MM-DD | Game | TBD | docs | "Fix broken link" | PENDING | - | - | - | - | First empirical PR |

## Notes

- Update Reversibility tier each PR accept (track cumulative >=5 → Gate D)
- First 3 PR are pattern-validating — explicit Eduardo authorization required per each
- Post 3 acceptance + zero reject → auto-mode acceptable for validated PR type
```

- [ ] **Step 5.2: Create initial empty logs/cross-repo-pr-2026-05.md**

Copy template content to `logs/cross-repo-pr-2026-05.md` (gitignored). Eduardo populate when first PR opened.

Use Write tool to write the same template content to logs/cross-repo-pr-2026-05.md.

- [ ] **Step 5.3: Verify logs/* gitignored**

Run: `git -C C:/dev/codemasterdd-ai-station check-ignore logs/cross-repo-pr-2026-05.md`
Expected: outputs `logs/cross-repo-pr-2026-05.md` (means file IS ignored).

- [ ] **Step 5.4: Commit template only (NOT log file)**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add docs/cross-repo/_TEMPLATES/cross-repo-pr-tracking-template.md
git -C C:/dev/codemasterdd-ai-station commit -m "feat(cross-repo): pr tracking template doc for monthly log"
```

---

## Task 6: ESCALATION_GATES.md (Component 3 core doc)

**Files:**
- Create: `docs/cross-repo/ESCALATION_GATES.md`

- [ ] **Step 6.1: Write ESCALATION_GATES.md content**

Write:

```markdown
# Cross-repo escalation gates (Component 3)

> Spec ref: `docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md` V3 Opt 1.5 REDUCED PR #87.
>
> Anti-L-016 discipline: weekly Gate E logging via `scripts/cross-repo/coord-event-log.ps1` + harsh-reviewer subagent week-4 audit.

## Purpose

Criteri **pre-definiti** per evoluzione paradigm cross-repo SE failure trigger empirico emerge. Tracking discipline previene drift "intent to log → abandoned" (anti-pattern L-2026-05-016).

## Gates definizione

### Gate E (PRE-Component-1 build)

**Purpose**: validate trigger #1 visibility gap empirically post-Max prima di commit Component 1 build effort.

**Empirical window**: 30 giorni post-Claude Max expiration (5/20 → 6/19).

**Measurement**:
- Eduardo logs coord-event ogni volta che ha "missed-coordination event":
  - grep manuale cross-repo >3 location per state lookup, OR
  - cross-repo policy drift discovered DOPO causing rework >30min, OR
  - two-way communication cross-repo per decision singola che richiede >2 round trip
- Log file: `logs/coord-events-YYYY-MM.md`
- Helper script: `scripts/cross-repo/coord-event-log.ps1` (interactive prompts)
- Weekly reminder: schtasks Sunday 09:00 (installed via `install-gate-e-reminder.ps1`)

**Thresholds** (after 4 weeks consecutive measurement):

| Avg events/week | Decision | Component 1 scope |
|-----------------|----------|-------------------|
| ≥5/wk | BUILD justified empirical | Full scope (extension dogfood-ui OR standalone, alternative A vs B decision) |
| 2-4.99/wk | BUILD MINIMAL | Extension dogfood-ui ONLY (drop standalone alternative + reduce SPRINT_02 T1-T2 scope) |
| <2/wk | NOT BUILT | Trigger #1 falsified empirical, defer indefinitely. Update STATUS_MULTI_REPO + close spec V3 |

**Threshold revisability**: post 1-week pilot, threshold revisable se events tipicamente cluster (1 day = revise weekly threshold) vs scattered (mantain). Document revision in `docs/cross-repo/ESCALATION_GATES.md` amendment + JOURNAL entry.

**Audit week 4**: invocare harsh-reviewer subagent (Protocol 5 ADR-0026 addendum) per verificare:
- Logging discipline consistency (no gap weeks)
- Severity tag distribution (NOT all = 1, NOT all = 5)
- Cost minutes documentation present
- Aggregate count plausibility vs JOURNAL entries cross-reference

Cost: ~$0.30-0.50 (~85K tokens). Sotto cap ADR-0023 $20/mese.

### Gate A (Opt 3 write-direct re-evaluation)

**Trigger**: >2 missed-coordination events/week × 4 weeks consecutive WITH severity ≥3 (subjective severity tag 1-5, weighted toward "high impact, no work-around").

**Action**: re-evaluate Opt 3 (write-direct cross-repo). Requires ADR amendment cross-repo with governance interna consent of 3 target repos (Game / Godot-v2 / Dafne). Conway's law cost upfront.

### Gate B (Opt 4 mesh-bus re-evaluation)

**Trigger**: repo count ≥7 (codemasterdd + Game + Godot-v2 + Dafne + vault + Synesthesia + ≥1 NEW = 7+) OR client production work attivo (Eduardo lavoro contrattuale terzi su codemasterdd-tooled workflow).

**Action**: re-evaluate Opt 4 (Dafne swarm extension cross-repo). Setup ~4-8 weeks bootstrap.

### Gate C (Eduardo bandwidth degraded)

**Trigger**: Eduardo bandwidth coordinator <50% available (es. lavoro full-time esterno, healthcare event, family commitment). Qualitative self-report monthly in JOURNAL or COMPACT_CONTEXT.

**Action**: Opt 1.5 enhanced via Dafne specialist routing automatic. Move coord overhead to Dafne agents (existing 11 agent runtime).

### Gate D (Component 2 reversibility threshold)

**Trigger**: ≥5 PR cumulative accepted by external governance WITH cross-reference adoption visible (target repo CLAUDE.md o AGENTS.md cita codemasterdd pattern).

**Action**: PAUSE Component 2 + audit lock-in scope cross-repo + ADR formale per ritiro coordinato OR continuation explicit. Soft lock-in converges Opt 1.5 cost toward Opt 3 cost asymmetric advantage lost.

## Tracking files

| File | Gate | Updated by | Refresh cadence |
|------|------|------------|-----------------|
| `logs/coord-events-YYYY-MM.md` | E | `coord-event-log.ps1` interactive | Each event (event-driven) |
| `logs/escalation-gates-YYYY-MM.md` | A/B/C/D | Eduardo manual + weekly | Weekly Sunday checkpoint |
| `logs/cross-repo-pr-YYYY-MM.md` | D | `dry-run-pr.ps1` reminder | Each PR open + outcome |

## Gates interaction

- Gate E precedes ALL altri (until Gate E resolved, Component 1 NOT built)
- Gate A + Gate B mutually exclusive (Opt 3 OR Opt 4 escalation, NOT both)
- Gate C independent (bandwidth event, doesn't trigger Opt 3/4)
- Gate D Component-2-specific (independent of Component 1 build)

## Reading the gates

This document is checkpoint, NOT prescription. Gate trigger does NOT mean automatic execution — it means **re-open the decision** with empirical data. Decision belongs to Eduardo + governance interna repo target (Gate A) or strategic context (Gate B/C).
```

- [ ] **Step 6.2: Commit**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add docs/cross-repo/ESCALATION_GATES.md
git -C C:/dev/codemasterdd-ai-station commit -m "feat(cross-repo): escalation gates A-E with thresholds + anti-L-016 discipline"
```

---

## Task 7: coord-event-log.ps1 (Gate E helper)

**Files:**
- Create: `scripts/cross-repo/coord-event-log.ps1`

- [ ] **Step 7.1: Write coord-event-log.ps1**

```powershell
<#
.SYNOPSIS
  Helper interactive script per logging missed-coordination events (Gate E spec V3).

.DESCRIPTION
  Prompts Eduardo per evento details + appends row a logs/coord-events-YYYY-MM.md.
  Auto-detects current month + creates file from template if not exists.
  Anti-L-016 discipline: questo script E' la riduzione di friction per logging.

.PARAMETER Quiet
  Skip interactive prompts, append only timestamp + Notes from parameter (for cron/scripted use).

.PARAMETER NotesQuick
  Use with -Quiet for one-line entry.

.EXAMPLE
  .\coord-event-log.ps1
  (interactive mode, default)

.EXAMPLE
  .\coord-event-log.ps1 -Quiet -NotesQuick "Grep cross-repo for PR status 15min cost"
#>

param(
  [switch]$Quiet,
  [string]$NotesQuick = ""
)

$ErrorActionPreference = 'Stop'

$today = Get-Date -Format "yyyy-MM-dd"
$month = Get-Date -Format "yyyy-MM"
$logFile = "C:\dev\codemasterdd-ai-station\logs\coord-events-$month.md"

# Create file if not exists with template header
if (-not (Test-Path $logFile)) {
  $header = @"
# Coord events tracking $month (Gate E spec V3)

> Anti-L-016 discipline. Helper: ``scripts/cross-repo/coord-event-log.ps1``.

## Weekly summary

| Week start | Events count | Avg severity | Total cost (min) | Threshold? |
|------------|--------------|--------------|------------------|------------|
| 2026-MM-DD | 0 | - | 0 | - |

## Events log

| Date | Time | Severity (1-5) | Type | Repos grepped | Cost (min) | Notes |
|------|------|----------------|------|---------------|------------|-------|

"@
  Set-Content -Path $logFile -Value $header -Encoding UTF8
  Write-Host "Created new log file: $logFile" -ForegroundColor Cyan
}

# Gather event details
$time = Get-Date -Format "HH:mm"

if ($Quiet) {
  if (-not $NotesQuick) {
    Write-Host "FAIL: -Quiet requires -NotesQuick" -ForegroundColor Red
    exit 1
  }
  $severity = 3  # default mid
  $eventType = "manual-quick"
  $reposGrepped = "N/A"
  $costMin = 5  # default
  $notes = $NotesQuick
} else {
  Write-Host "=== Log new coord event ===" -ForegroundColor Cyan
  Write-Host "Date: $today $time"
  Write-Host ""

  $severity = Read-Host "Severity 1-5 (1=trivial, 5=blocking)"
  if ($severity -notmatch '^[1-5]$') { Write-Host "Invalid severity, default 3"; $severity = 3 }

  Write-Host ""
  Write-Host "Event type:"
  Write-Host "  1) grep-manual-cross-repo (>3 location lookup)"
  Write-Host "  2) policy-drift-discovered (rework >30min)"
  Write-Host "  3) cross-repo-roundtrip (>2 RT for single decision)"
  Write-Host "  4) other"
  $typeChoice = Read-Host "Choice 1-4"
  $eventType = switch ($typeChoice) {
    '1' { 'grep-manual' }
    '2' { 'policy-drift' }
    '3' { 'cross-repo-roundtrip' }
    '4' { 'other' }
    default { 'other' }
  }

  $reposGrepped = Read-Host "Repos involved (comma-sep, es. Game,Godot-v2,vault)"
  $costMin = Read-Host "Cost in minutes (estimate)"
  if ($costMin -notmatch '^\d+$') { $costMin = 0 }
  $notes = Read-Host "One-line notes"
}

# Append entry
$row = "| $today | $time | $severity | $eventType | $reposGrepped | $costMin | $notes |"
Add-Content -Path $logFile -Value $row -Encoding UTF8

Write-Host ""
Write-Host "PASS: Event logged to $logFile" -ForegroundColor Green
Write-Host "Row: $row"
exit 0
```

- [ ] **Step 7.2: Smoke test interactive mode**

Run:
```powershell
powershell -File C:/dev/codemasterdd-ai-station/scripts/cross-repo/coord-event-log.ps1
```
Input prompts: severity=2, type choice=1, repos="Game,vault", cost=10, notes="smoke test entry".
Expected: file `logs/coord-events-2026-05.md` created with header + 1 row appended. "PASS" green. Exit 0.

- [ ] **Step 7.3: Smoke test quiet mode**

Run:
```powershell
powershell -File C:/dev/codemasterdd-ai-station/scripts/cross-repo/coord-event-log.ps1 -Quiet -NotesQuick "Quiet mode smoke test"
```
Expected: 1 more row appended (severity=3 default, type=manual-quick, cost=5 default). "PASS" green. Exit 0.

- [ ] **Step 7.4: Verify log file content**

Run: `cat C:/dev/codemasterdd-ai-station/logs/coord-events-2026-05.md`
Expected: header table + 2 rows visible.

- [ ] **Step 7.5: Clean smoke test data (keep file, remove rows)**

Edit `logs/coord-events-2026-05.md` to remove the 2 smoke rows. Leave only header + empty events log table.

- [ ] **Step 7.6: Commit script (file gitignored)**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add scripts/cross-repo/coord-event-log.ps1
git -C C:/dev/codemasterdd-ai-station commit -m "feat(cross-repo): coord event log helper with interactive + quiet mode"
```

---

## Task 8: install-gate-e-reminder.ps1 (weekly schtasks)

**Files:**
- Create: `scripts/cross-repo/install-gate-e-reminder.ps1`

- [ ] **Step 8.1: Write install script**

```powershell
<#
.SYNOPSIS
  Install schtasks weekly Sunday 09:00 reminder per Gate E logging discipline (spec V3).

.DESCRIPTION
  Crea Windows scheduled task che mostra reminder PowerShell weekly:
  "Gate E checkpoint: log coord events past week or run coord-event-log.ps1".

  Matches pattern esistente backup-api-keys.ps1 + smoke-test-hooks.ps1 (schtasks weekly).

.PARAMETER DryRun
  Print schtasks command but don't execute (for review pre-install).

.PARAMETER Uninstall
  Remove the scheduled task instead of installing.

.EXAMPLE
  .\install-gate-e-reminder.ps1 -DryRun
  .\install-gate-e-reminder.ps1
  .\install-gate-e-reminder.ps1 -Uninstall
#>

param(
  [switch]$DryRun,
  [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'

$taskName = "GateELoggingReminder"
$scriptPath = "C:\dev\codemasterdd-ai-station\scripts\cross-repo\coord-event-log.ps1"

if ($Uninstall) {
  Write-Host "Uninstalling task $taskName..." -ForegroundColor Yellow
  $cmd = "schtasks /Delete /TN $taskName /F"
  if ($DryRun) {
    Write-Host "DRY-RUN: $cmd"
    exit 0
  }
  Invoke-Expression $cmd
  Write-Host "PASS: task removed" -ForegroundColor Green
  exit 0
}

# Install command
$reminderText = "Gate E checkpoint: log coord events past week or run scripts/cross-repo/coord-event-log.ps1"
$reminderCmd = "powershell -Command `"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('$reminderText', 'Gate E Weekly Reminder', 'OK', 'Information')`""

$cmd = "schtasks /Create /SC WEEKLY /D SUN /TN $taskName /TR `"$reminderCmd`" /ST 09:00 /F"

if ($DryRun) {
  Write-Host "=== DRY-RUN ===" -ForegroundColor Cyan
  Write-Host "Task name: $taskName"
  Write-Host "Schedule: WEEKLY Sunday 09:00"
  Write-Host "Action: PowerShell MessageBox reminder"
  Write-Host ""
  Write-Host "Command that would execute:"
  Write-Host $cmd
  Write-Host ""
  Write-Host "DRY-RUN OK. Run without -DryRun to install." -ForegroundColor Green
  exit 0
}

Write-Host "Installing schtasks $taskName..." -ForegroundColor Cyan
Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
  Write-Host "PASS: task installed" -ForegroundColor Green
  Write-Host "Verify: schtasks /Query /TN $taskName"
  exit 0
} else {
  Write-Host "FAIL: task install failed (exit $LASTEXITCODE)" -ForegroundColor Red
  exit 1
}
```

- [ ] **Step 8.2: Smoke dry-run**

Run:
```powershell
powershell -File C:/dev/codemasterdd-ai-station/scripts/cross-repo/install-gate-e-reminder.ps1 -DryRun
```
Expected: prints task spec + command + "DRY-RUN OK" green. Exit 0. NO actual schtask created.

- [ ] **Step 8.3: Install scheduled task (real)**

Run:
```powershell
powershell -File C:/dev/codemasterdd-ai-station/scripts/cross-repo/install-gate-e-reminder.ps1
```
Expected: "PASS: task installed" green. Exit 0.

- [ ] **Step 8.4: Verify task created**

Run: `schtasks /Query /TN GateELoggingReminder`
Expected: task listed con next run time = next Sunday 09:00.

- [ ] **Step 8.5: Commit**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add scripts/cross-repo/install-gate-e-reminder.ps1
git -C C:/dev/codemasterdd-ai-station commit -m "feat(cross-repo): gate e weekly reminder schtasks installer"
```

---

## Task 9: escalation-gates tracking template doc

**Files:**
- Create: `docs/cross-repo/_TEMPLATES/escalation-gates-tracking-template.md`

- [ ] **Step 9.1: Write template doc**

```markdown
# Escalation gates tracking template

Template per `logs/escalation-gates-YYYY-MM.md` (gitignored).

## Gate E status

- Empirical window: 5/20 → 6/19 (4 weeks)
- Current week: <fill in week start date>
- Current count: <events>
- Avg events/wk this month: <calc>
- Threshold met? <yes/no/not-yet>

## Per-week summary

| Week start | Events count | Severity avg (1-5) | Total cost (min) | Gate E threshold (≥5)? | Anti-pattern flags |
|------------|--------------|--------------------|-----------------|-------------------------|---------------------|
| 2026-05-20 | 0 | - | 0 | - | - |
| 2026-05-27 | 0 | - | 0 | - | - |
| 2026-06-03 | 0 | - | 0 | - | - |
| 2026-06-10 | 0 | - | 0 | - | - |

## Gate A status (Opt 3 trigger)

- Current count high-severity events: <count>
- 4-week consecutive trigger met? <yes/no>

## Gate B status (Opt 4 trigger)

- Current repo count monitored: 6 (Game / Godot-v2 / Dafne / vault / Synesthesia / AA01)
- ≥7 trigger? NO
- Client work active? NO

## Gate C status (bandwidth)

- Eduardo bandwidth self-report monthly: <yes if applicable>

## Gate D status (Component 2 reversibility)

- Cumulative PR opened: 0
- Cumulative PR accepted: 0
- Cross-reference adoption count: 0
- ≥5 with adoption trigger? NO

## Week 4 audit checklist (harsh-reviewer subagent invocato)

- [ ] Logging discipline consistency check (no gap weeks)
- [ ] Severity tag distribution sanity (NOT all =1, NOT all =5)
- [ ] Cost minutes documentation present (NOT all = 0)
- [ ] Aggregate count plausibility vs JOURNAL cross-reference
- [ ] Gate E decision: BUILD full / BUILD MINIMAL / DEFER

Audit invoked via Claude Code:
> Spawn harsh-reviewer subagent. Read logs/coord-events-YYYY-MM.md + logs/escalation-gates-YYYY-MM.md.
> Verify: logging discipline + severity distribution + cost documentation + plausibility + Gate E threshold met.
> Output: P0/P1/P2 findings if drift detected + Gate E decision recommendation.

Cost stimato: ~$0.30 (~85K tokens). Sotto cap ADR-0023.
```

- [ ] **Step 9.2: Copy template to logs/ (gitignored)**

Copy content to `logs/escalation-gates-2026-05.md` (initial state).

- [ ] **Step 9.3: Commit template only**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add docs/cross-repo/_TEMPLATES/escalation-gates-tracking-template.md
git -C C:/dev/codemasterdd-ai-station commit -m "feat(cross-repo): escalation gates tracking template with week 4 audit"
```

---

## Task 10: BACKLOG + STATUS_MULTI_REPO integration

**Files:**
- Modify: `C:/dev/codemasterdd-ai-station/BACKLOG.md`
- Modify: `C:/dev/codemasterdd-ai-station/STATUS_MULTI_REPO.md`

- [ ] **Step 10.1: Add BACKLOG entries for Component 2+3+Gate E**

Edit BACKLOG.md, find section "Sprint corrente" (SPRINT_02) area, add new sub-section:

```markdown
### Task derivati da spec V3 cross-repo orchestrator (PR #87 Opt 1.5 REDUCED)

- [x] ~~**X1** Component 2 workflow doc + tracking template + dry-run validator (PR #87)~~ **DONE pre-Max**
- [x] ~~**X2** Component 3 escalation gates A-E + Gate E discipline + weekly reminder cron (PR #87)~~ **DONE pre-Max**
- [ ] **X3** Gate E empirical window 30gg post-Max (2026-05-20 → 2026-06-19): Eduardo logging discipline + week 4 harsh-reviewer audit
- [ ] **X4** Gate E decision evaluation (~2026-06-20): BUILD full / BUILD MINIMAL / DEFER based on empirical events count
- [ ] **X5** Component 1 dashboard implementation (CONDITIONAL on X4 outcome ≥5 events/wk OR 2-5 events/wk minimal scope)
```

- [ ] **Step 10.2: Add STATUS_MULTI_REPO entry**

Edit STATUS_MULTI_REPO.md, find apps section, add row:

```markdown
| Cross-repo coordination (Component 2+3) | `docs/cross-repo/` + `scripts/cross-repo/` | DOC + scripts pre-Max ✅ | Gate E empirical 30gg post-Max pending |
```

- [ ] **Step 10.3: Commit BACKLOG + STATUS update**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add BACKLOG.md STATUS_MULTI_REPO.md
git -C C:/dev/codemasterdd-ai-station commit -m "docs(backlog): cross-repo orchestrator X1-X5 tasks tracking"
```

---

## Task 11: JOURNAL entry

**Files:**
- Modify: `C:/dev/codemasterdd-ai-station/JOURNAL.md`

- [ ] **Step 11.1: Add JOURNAL entry**

Find top of JOURNAL.md (after first `---` divider), insert new entry:

```markdown
## 2026-05-13 (sera-tardi-ultra-2: cross-repo orchestrator design + impl pre-Max)

### Completato

- Brainstorming skill (Protocol 6) + Archon ciclo 1 + harsh-reviewer (Protocol 5) + Archon ciclo 2 self-falsification per cross-repo orchestrator decision strategic
- Spec V3 Opt 1.5 REDUCED post Eduardo "Riavvio Archon ciclo 2" (trigger #1 unverified self-falsification)
- PR #87 opened: spec V3 (3 commits v1 → v2 → v3 honest evolution)
- Writing-plans skill → implementation plan 11 task pre-Max
- Component 2 (PR_WORKFLOW + PR_TEMPLATE + dry-run-pr.ps1 + tracking template)
- Component 3 (ESCALATION_GATES + coord-event-log.ps1 + install-gate-e-reminder.ps1 + tracking template)
- BACKLOG X1-X5 tasks tracking
- 11 commits cumulative su branch claude/cross-repo-orchestrator-spec-2026-05-13

### Da fare

- Gate E empirical window 30gg post-Max (5/20 → 6/19): Eduardo logging discipline
- Week 4 audit via harsh-reviewer subagent
- Gate E decision evaluation (~6/20): Component 1 BUILD / MINIMAL / DEFER

### Note

- Methodology applied: 5 cognitive protocols cumulative (P1 + P3 ciclo 1 + P3 ciclo 2 + P5 + P6). Honest confidence trail 75% → 70% → 55%.
- Lesson candidate L-2026-05-017 in promotion: Archon ciclo 2 self-falsification pattern (user "riavvia ciclo" = strongest signal trigger unverified)
- Pre-Max residual: 6gg → 5gg post questa sessione
```

- [ ] **Step 11.2: Commit JOURNAL**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station add JOURNAL.md
git -C C:/dev/codemasterdd-ai-station commit -m "docs(journal): cross-repo orchestrator design + impl pre-max session"
```

---

## Final verification

- [ ] **Step F.1: Verify all 8 created files committed**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station log --stat --oneline -15
```
Expected: 11 commits visible (Task 1-11 + spec V3 + 2 prev spec versions). Files created:
- docs/cross-repo/README.md
- docs/cross-repo/PR_WORKFLOW.md
- docs/cross-repo/PR_TEMPLATE.md
- docs/cross-repo/ESCALATION_GATES.md
- docs/cross-repo/_TEMPLATES/cross-repo-pr-tracking-template.md
- docs/cross-repo/_TEMPLATES/escalation-gates-tracking-template.md
- scripts/cross-repo/.gitkeep
- scripts/cross-repo/dry-run-pr.ps1
- scripts/cross-repo/coord-event-log.ps1
- scripts/cross-repo/install-gate-e-reminder.ps1

- [ ] **Step F.2: Verify schtasks reminder installed**

Run: `schtasks /Query /TN GateELoggingReminder`
Expected: task listed with next run time.

- [ ] **Step F.3: Verify gitignored logs files exist locally**

Run: `ls C:/dev/codemasterdd-ai-station/logs/coord-events-2026-05.md C:/dev/codemasterdd-ai-station/logs/escalation-gates-2026-05.md C:/dev/codemasterdd-ai-station/logs/cross-repo-pr-2026-05.md`
Expected: 3 files exist locally (gitignored, NOT committed).

- [ ] **Step F.4: Push branch + update PR #87**

Run:
```powershell
git -C C:/dev/codemasterdd-ai-station push origin claude/cross-repo-orchestrator-spec-2026-05-13
gh pr edit 87 --repo MasterDD-L34D/codemasterdd-ai-station --body "$(cat <<'EOF'
[Existing PR body content + add new section:]

## Implementation complete pre-Max

Plan executed: `docs/superpowers/plans/2026-05-13-cross-repo-orchestrator-impl.md` (11 tasks, ~6-8h actual).

Files created:
- docs/cross-repo/README.md + PR_WORKFLOW.md + PR_TEMPLATE.md + ESCALATION_GATES.md + 2 templates
- scripts/cross-repo/dry-run-pr.ps1 + coord-event-log.ps1 + install-gate-e-reminder.ps1
- BACKLOG.md X1-X5 entries
- JOURNAL.md entry 2026-05-13 sera-tardi-ultra-2

schtasks GateELoggingReminder installed (weekly Sunday 09:00).

Next: Gate E empirical 30gg window 5/20 → 6/19. Week 4 audit via harsh-reviewer. Component 1 decision 6/20.
EOF
)"
```

- [ ] **Step F.5: Mark plan complete**

Update task list this plan (final task done) + report completion to Eduardo.

---

## Self-review checklist

**Spec coverage**: each spec V3 section mapped to task?
- Component 2 workflow doc → Task 2 (PR_WORKFLOW.md) ✓
- Component 2 PR template → Task 3 (PR_TEMPLATE.md) ✓
- Component 2 dry-run protocol → Task 4 (dry-run-pr.ps1) ✓
- Component 2 tracking template → Task 5 (template + log) ✓
- Component 3 Gate A-E criteria → Task 6 (ESCALATION_GATES.md) ✓
- Component 3 Gate E discipline → Task 7 (coord-event-log.ps1) ✓
- Component 3 weekly reminder → Task 8 (install-gate-e-reminder.ps1) ✓
- Component 3 tracking template → Task 9 (template + log) ✓
- Component 3 week 4 audit harsh-reviewer → Task 9 step 9.1 docs (audit invocation script-doc) ✓
- BACKLOG integration → Task 10 ✓
- JOURNAL entry → Task 11 ✓

**Placeholder scan**: zero TBD / TODO / "fill in details" / "implement later" / "similar to" without code ✓

**Type consistency**: 
- Script names consistent: `dry-run-pr.ps1` + `coord-event-log.ps1` + `install-gate-e-reminder.ps1` ✓
- ValidateSet for repo target: Game / Godot-v2 / Dafne / vault (consistent across tasks) ✓
- Log file paths consistent: `logs/coord-events-YYYY-MM.md` + `logs/escalation-gates-YYYY-MM.md` + `logs/cross-repo-pr-YYYY-MM.md` ✓

**YAGNI adherence**: NO Component 1 build, NO Flask routes, NO DB schema, NO new container, NO standalone app, NO write-direct cross-repo, NO auth/multi-tenant ✓

**Scope check**: 11 tasks ≈ 6-8h actual + buffer = 2gg pre-Max realistic ✓

---

**End of plan.**
