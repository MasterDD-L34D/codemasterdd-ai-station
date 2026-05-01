param(
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

$activeFiles = @(
    "PROJECT_STATE.yaml",
    "README.md",
    "PROJECT_BRIEF.md",
    "COMPACT_CONTEXT.md",
    "ROADMAP.md",
    "BACKLOG.md",
    "DECISIONS_LOG.md",
    "OPEN_DECISIONS.md",
    "MASTER_PROMPT.md",
    "REFERENCE_INDEX.md",
    "STATUS_MULTI_REPO.md",
    "SPRINT_02.md",
    "EXTERNAL_REPOS.md",
    "AGENTS.md",
    "CLAUDE.md",
    "MODEL_ROUTING.md",
    "apps/dogfood-ui/README.md"
)

$forbidden = @(
    @{
        Pattern = "cb2e506|8446869|3b26173|5ef8e9c";
        Reason = "old HEAD hash in active guidance"
    },
    @{
        Pattern = "\b14 ADR\b|\b16 ADR\b|\b15 file\b";
        Reason = "old ADR/file count in active guidance"
    },
    @{
        Pattern = "Fase 6\s+(40|55|60)";
        Reason = "old Fase 6 progress claim in active guidance"
    },
    @{
        Pattern = "SPRINT_01\s+attivo|SPRINT_01\s+active";
        Reason = "old sprint revived as active"
    },
    @{
        Pattern = "Game\s+active|Dafne\s+active|Synesthesia\s+active|AA01\s+active";
        Reason = "external repo marked active without reactivation"
    },
    @{
        Pattern = "live\s+UP|server\s+UP|Flask\s+:5000\s+UP";
        Reason = "runtime service status claimed without current verification"
    },
    @{
        Pattern = "OpenCode\s+installed|OpenCode\s+is\s+active|Aider\s+wrappers\s+available";
        Reason = "tool availability claimed without current verification"
    }
)

$violations = @()

foreach ($relativePath in $activeFiles) {
    $path = Join-Path $repoRoot $relativePath
    if (-not (Test-Path $path)) {
        $violations += [pscustomobject]@{
            File = $relativePath
            Line = 0
            Reason = "active file missing"
            Text = ""
        }
        continue
    }

    $lines = Get-Content -LiteralPath $path
    for ($i = 0; $i -lt $lines.Count; $i++) {
        foreach ($rule in $forbidden) {
            if ($lines[$i] -match $rule.Pattern) {
                $violations += [pscustomobject]@{
                    File = $relativePath
                    Line = $i + 1
                    Reason = $rule.Reason
                    Text = $lines[$i].Trim()
                }
            }
        }
    }
}

if ($violations.Count -gt 0) {
    if (-not $Quiet) {
        Write-Error "Recovery consistency check failed:"
        $violations | Format-Table -AutoSize | Out-String | Write-Host
    }
    exit 1
}

if (-not $Quiet) {
    Write-Host "Recovery consistency check passed."
}
