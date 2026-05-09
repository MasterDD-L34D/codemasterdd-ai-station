# Stop hook: detect HEAD git change vs session start marker, prompt JOURNAL/COMPACT update
# H12 ADR-0010 / harsh review C3 risoluzione
# Trigger: Stop event (Claude Code config in .claude/settings.json)
# Logic:
#   1. Leggi marker .claude/.session-start-head (creato da session-start-marker.ps1)
#   2. Compara con git rev-parse HEAD attuale
#   3. Se cambiato: emette systemMessage JSON con summary commit + reminder
#   4. Se invariato: silent (sessione read-only, no entry JOURNAL needed)

$ErrorActionPreference = "Continue"
$repoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$markerFile = Join-Path $repoRoot ".claude/.session-start-head"

$result = @{}

try {
    Push-Location $repoRoot

    if (-not (Test-Path $markerFile)) {
        # Marker mancante = session start hook non lanciato (es. prima volta o file deleted)
        # Skip silenziosamente, sara' creato a prossima SessionStart
        Pop-Location
        '{}' | Out-Host
        return
    }

    $startHead = (Get-Content $markerFile -Raw -ErrorAction Stop).Trim()
    $currentHead = (& git rev-parse HEAD 2>$null).Trim()

    if (-not $currentHead -or $LASTEXITCODE -ne 0) {
        Pop-Location
        '{}' | Out-Host
        return
    }

    if ($startHead -eq $currentHead) {
        # HEAD invariato: sessione read-only, no entry JOURNAL necessaria
        Pop-Location
        '{}' | Out-Host
        return
    }

    # HEAD cambiato: count commit + estrai messaggi
    $commitCount = (& git rev-list --count "$startHead..$currentHead" 2>$null).Trim()
    $commitSummary = (& git log --oneline "$startHead..$currentHead" 2>$null) -join "`n"

    $message = "Sessione significativa rilevata: $commitCount commit nuovi da inizio sessione (HEAD $($startHead.Substring(0,7)) -> $($currentHead.Substring(0,7))).`n`n" +
               "Commit summary:`n$commitSummary`n`n" +
               "Reminder JOURNAL/COMPACT drift mitigation (H12 ADR-0010):`n" +
               "- Aggiungi entry JOURNAL.md con riepilogo sessione (~1 min)`n" +
               "- Bump COMPACT_CONTEXT.md version se cambiamenti significativi (~30s)`n" +
               "- Update memory project_session_resumption.md se HEAD/scope cambiato (~30s)`n" +
               "Skip se sessione era solo read-only o trivial (es. fix typo)."

    $result = @{ systemMessage = $message }

    Pop-Location
} catch {
    # Silent fail
    if ((Get-Location).Path -ne $repoRoot) { try { Pop-Location } catch {} }
}

$result | ConvertTo-Json -Compress
