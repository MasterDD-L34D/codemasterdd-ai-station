# SessionStart hook: salva HEAD git attuale in marker file per detect drift al Stop event
# H12 ADR-0010 / harsh review C3 risoluzione
# Trigger: SessionStart event (Claude Code config in .claude/settings.json)
# Output: file .claude/.session-start-head (gitignored) contenente SHA HEAD

$ErrorActionPreference = "Continue"
$markerFile = Join-Path $PSScriptRoot "../../.claude/.session-start-head"

try {
    Push-Location (Split-Path $PSScriptRoot -Parent | Split-Path -Parent)
    $head = (& git rev-parse HEAD 2>$null).Trim()
    if ($LASTEXITCODE -eq 0 -and $head) {
        $head | Out-File -FilePath $markerFile -Encoding ascii -NoNewline
    }
    Pop-Location
} catch {
    # Silent fail: hook non deve mai bloccare session start
}

# Output JSON vuoto (no systemMessage)
'{}'
