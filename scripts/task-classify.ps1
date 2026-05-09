# task-classify.ps1 -- Tooling per classificare task di delega e ritornare comando pronto
#
# BACKLOG M9 (deferred SPRINT_02): riduce cognitive overhead decision tree CLAUDE.md
# "Trigger delega in-session" + ADR-0008 hub pattern + ADR-0016 constraint-count + ADR-0022 OpenCode tier.
#
# Mode interactive (default) -> 5 domande, output comando + Set-Clipboard.
# Mode parametric -> tutti i parametri da CLI, output comando in stdout (per script wrapper / test).
#
# Install globale (Eduardo manual, post-test smoke):
#   Copy-Item scripts/task-classify.ps1 C:/Users/edusc/.local/bin/task-classify.ps1
#   New-Item C:/Users/edusc/.local/bin/task-classify.cmd -ItemType File -Value '@powershell -ExecutionPolicy Bypass -File "%USERPROFILE%/.local/bin/task-classify.ps1" %*'
#
# Usage interactive: task-classify path/to/file.py
# Usage parametric:  task-classify -File path/to/file.py -Workflow single -Class cosmetic -Constraints 1 -CloudOk no -SpeedCritical no
#
# Source-of-truth decision tree:
#   - CLAUDE.md sezione "Priorita modelli AI" + "Trigger delega in-session"
#   - MODEL_ROUTING.md sezione "Routing per fase" + "Finding empirico constraint-count"
#   - ADR-0008 (silent-corruption hub pattern), ADR-0016 (constraint-count), ADR-0022 (OpenCode tier)

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [string]$File = "",

    [ValidateSet("multi", "single")]
    [string]$Workflow = "",

    [ValidateSet("cosmetic", "behavior", "strategic")]
    [string]$Class = "",

    [int]$Constraints = -1,

    [ValidateSet("yes", "no")]
    [string]$CloudOk = "",

    [ValidateSet("yes", "no")]
    [string]$SpeedCritical = "",

    [ValidateSet("yes", "no")]
    [string]$SubdirSelfRef = "",

    [switch]$NoClipboard,
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"

function Write-Info {
    param([string]$Msg, [string]$Color = "Cyan")
    if (-not $Quiet) { Write-Host $Msg -ForegroundColor $Color }
}

function Read-Choice {
    param(
        [string]$Prompt,
        [string[]]$Choices,
        [string]$Default = ""
    )
    $choiceList = ($Choices | ForEach-Object {
        if ($_ -eq $Default) { "[$_]" } else { $_ }
    }) -join " / "
    while ($true) {
        $userInput = Read-Host "  $Prompt ($choiceList)"
        if ([string]::IsNullOrWhiteSpace($userInput) -and $Default) {
            return $Default
        }
        $normalized = $userInput.ToLower().Trim()
        if ($Choices -contains $normalized) {
            return $normalized
        }
        Write-Host "    -> scelta non valida, riprova" -ForegroundColor Yellow
    }
}

function Read-Int {
    param(
        [string]$Prompt,
        [int]$Min,
        [int]$Max,
        [int]$Default = -1
    )
    while ($true) {
        $defaultHint = if ($Default -ge 0) { " [$Default]" } else { "" }
        $userInput = Read-Host "  $Prompt$defaultHint"
        if ([string]::IsNullOrWhiteSpace($userInput) -and $Default -ge 0) {
            return $Default
        }
        $parsed = 0
        if ([int]::TryParse($userInput, [ref]$parsed)) {
            if ($parsed -ge $Min -and $parsed -le $Max) {
                return $parsed
            }
        }
        Write-Host "    -> numero non valido (atteso $Min-$Max)" -ForegroundColor Yellow
    }
}

# ---- Resolve File (richiesto sempre) ----
if ([string]::IsNullOrWhiteSpace($File)) {
    Write-Info "task-classify -- delega tier router (CLAUDE.md + ADR-0008/0016/0022)" "Green"
    Write-Info ""
    $File = Read-Host "  File target (path relativo o assoluto)"
}
if ([string]::IsNullOrWhiteSpace($File)) {
    Write-Host "ERROR: file target obbligatorio" -ForegroundColor Red
    exit 1
}

# ---- Q1: Workflow (multi-step vs single-file) ----
if (-not $Workflow) {
    Write-Info ""
    Write-Info "Q1. Workflow -- il task richiede tool calls coordinati (Read+Edit+Bash+Glob)?" "Cyan"
    Write-Info "    multi  = OpenCode tier (orchestrazione tool, multi-file, MCP)" "DarkGray"
    Write-Info "    single = single-file edit (Aider tier, default per cosmetic/behavior)" "DarkGray"
    $Workflow = Read-Choice "Scelta" @("multi", "single") "single"
}

# ---- Q2: Class ----
if (-not $Class) {
    Write-Info ""
    Write-Info "Q2. Class -- natura del task" "Cyan"
    Write-Info "    cosmetic  = JSDoc/docstring/rename/lint-fix (no behavior change)" "DarkGray"
    Write-Info "    behavior  = refactor/bug fix/logic change (verifica diff post-edit)" "DarkGray"
    Write-Info "    strategic = ADR/multi-file >=3/synthesis cross-source (NON delegabile)" "DarkGray"
    $Class = Read-Choice "Scelta" @("cosmetic", "behavior", "strategic") "behavior"
}

# ---- SHORT-CIRCUIT: strategic -> manual Claude Code, niente delega ----
if ($Class -eq "strategic") {
    Write-Info ""
    Write-Info "==> Strategic task: NON delegabile (ADR-0008)" "Yellow"
    Write-Info "    Esegui direttamente in Claude Code con tool nativi (Read/Edit/Glob/Grep)" "Yellow"
    Write-Info "    Tracking opzionale entry in logs/aider-delegation-YYYY-MM.md se rilevante" "DarkGray"
    exit 0
}

# ---- Q3: Constraint count (solo per single-file Aider) ----
if ($Workflow -eq "single" -and $Constraints -lt 0) {
    Write-Info ""
    Write-Info "Q3. Constraint count -- quanti vincoli ESPLICITI nel prompt task?" "Cyan"
    Write-Info "    1     = add-only / fix puntuale (qualsiasi tier OK)" "DarkGray"
    Write-Info "    2-3   = fix+transform / logic change (preferire diff + review)" "DarkGray"
    Write-Info "    4     = borderline (gap dati ADR-0016, default safer 14B Q2)" "DarkGray"
    Write-Info "    5+    = strict multi-constraint (SKIP delega, manual Claude Code)" "DarkGray"
    $Constraints = Read-Int "Numero" 1 20 2
}

# ---- SHORT-CIRCUIT: 5+ constraint -> manual ----
if ($Constraints -ge 5) {
    Write-Info ""
    Write-Info "==> Constraint count >=5: SKIP delega (ADR-0016 raccomandazione)" "Yellow"
    Write-Info "    REJECT empirico Groq 70B su 5-constraint (dogfood #7)" "Yellow"
    Write-Info "    Esegui direttamente in Claude Code o split task in subtask <=3 constraint" "Yellow"
    exit 0
}

# ---- Q4: Privacy (cloud OK?) ----
if (-not $CloudOk) {
    Write-Info ""
    Write-Info "Q4. Cloud OK -- repo whitelisted o file non-sensitive?" "Cyan"
    Write-Info "    yes = repo in ~/.config/aider-privacy-whitelist.txt (codemasterdd, Game, Godot-v2)" "DarkGray"
    Write-Info "    no  = repo non whitelisted o file sensitive (controllers/routes/middlewares)" "DarkGray"
    $CloudOk = Read-Choice "Scelta" @("yes", "no") "no"
}

# ---- Q5: Speed-critical (solo se cloud OK) ----
if ($CloudOk -eq "yes" -and -not $SpeedCritical) {
    Write-Info ""
    Write-Info "Q5. Speed-critical -- serve throughput cloud (>=300 tok/s)?" "Cyan"
    Write-Info "    yes = batch grosso o iterazione veloce (Groq 630 tok/s, Cerebras 733 tok/s)" "DarkGray"
    Write-Info "    no  = workflow normale (locale 25-114 tok/s sufficiente)" "DarkGray"
    $SpeedCritical = Read-Choice "Scelta" @("yes", "no") "no"
}

# ---- Q6 (cosmetic+single only): subdir + docstring self-ref edge case ----
if ($Workflow -eq "single" -and $Class -eq "cosmetic" -and -not $SubdirSelfRef) {
    Write-Info ""
    Write-Info "Q6. Edge case wrong-target-file -- file e' in subdir profonda CON docstring header che cita filename?" "Cyan"
    Write-Info "    yes = pattern bug Qwen 7B + whole + subdir + self-ref (n=1 al 7/5, mitigation: aider-refactor diff)" "DarkGray"
    Write-Info "    no  = no risk, default cosmetic 7B + whole" "DarkGray"
    $SubdirSelfRef = Read-Choice "Scelta" @("yes", "no") "no"
}

# ---- DECISION TREE: ritorna comando ----

$cmd = ""
$rationale = ""
$tier = ""

if ($Workflow -eq "multi") {
    # OpenCode tier (ADR-0022)
    if ($CloudOk -eq "yes") {
        # Cloud free NON viable per OpenCode (rate-limited TPM/context)
        # Cloud paid = openai/gpt-4o-mini emergenza
        $tier = "OpenCode tier 4 paid"
        $cmd = "opencode run --model `"openai/gpt-4o-mini`" `"<task description per $File>`""
        $rationale = "Multi-step + cloud OK + speed/capability needed -> gpt-4o-mini paid (ccusage monitor). Cloud free non viable OpenCode (ADR-0022 addendum)."
    } else {
        # Sovereign default
        $tier = "OpenCode tier 1 sovereign"
        $cmd = "opencode run --model `"ollama/qwen3-coder:30b`" `"<task description per $File>`""
        $rationale = "Multi-step agentic + sovereign -> qwen3-coder:30b MoE A3B (ADR-0022 Accepted, 3/3 PASS validati)."
    }
} elseif ($Class -eq "cosmetic") {
    if ($CloudOk -eq "yes" -and $SpeedCritical -eq "yes") {
        $tier = "Aider tier 3 cloud cosmetic fast"
        $cmd = "aider-cerebras `"$File`""
        $rationale = "Cosmetic + cloud OK + speed-critical -> Cerebras 8B 733 tok/s. Privacy whitelist gia' enforced dal wrapper (H8)."
    } elseif ($SubdirSelfRef -eq "yes") {
        # Edge case wrong-target (n=1 7/5, mitigation safer): forzato refactor diff
        $tier = "Aider tier 2 behavior diff (mitigation wrong-target)"
        $cmd = "aider-refactor `"$File`""
        $rationale = "Cosmetic + subdir profonda + docstring self-ref -> aider-refactor (14B Q2 + diff) safer. Pattern wrong-target n=1 al 7/5, mitigation default."
    } else {
        $tier = "Aider tier 1 sovereign cosmetic"
        $cmd = "aider-cosmetic `"$File`""
        $rationale = "Cosmetic + locale -> Qwen 7B + whole 114 tok/s (ADR-0007). Format whole compatibile, faithfulness non critica."
    }
} elseif ($Class -eq "behavior") {
    # behavior-critical
    if ($Constraints -eq 4) {
        # Borderline: gap dati ADR-0016, default safer
        $tier = "Aider tier 2 behavior (borderline 4 constraint)"
        if ($CloudOk -eq "yes") {
            $cmd = "aider-groq `"$File`"  # OR aider-refactor `"$File`" (locale safer privacy)"
            $rationale = "Behavior + 4 constraint borderline + cloud OK -> Groq 70B 70-85% range (gap dati ADR-0016). Locale 14B Q2 alternativa safer privacy."
        } else {
            $cmd = "aider-refactor `"$File`""
            $rationale = "Behavior + 4 constraint borderline + sovereign -> 14B Q2 + diff. Se safe-fail -> escalation aider-30b (manual)."
        }
    } elseif ($CloudOk -eq "yes" -and $SpeedCritical -eq "yes") {
        $tier = "Aider tier 3 cloud behavior"
        $cmd = "aider-groq `"$File`""
        $rationale = "Behavior + cloud OK + speed-critical -> Groq llama-3.3-70b 630 tok/s (capability 70B dense)."
    } else {
        $tier = "Aider tier 2 sovereign behavior"
        $cmd = "aider-refactor `"$File`""
        $rationale = "Behavior + locale -> Qwen 14B Q2 + diff (sweet spot ADR-0008, safe-fail format). Verifica diff post-edit."
    }
}

# ---- OUTPUT ----
Write-Info ""
Write-Info "==> Tier scelto: $tier" "Green"
Write-Info "==> Razionale: $rationale" "DarkGray"
Write-Info ""
if (-not $Quiet) {
    Write-Info "Comando pronto:" "Yellow"
    Write-Host "  $cmd" -ForegroundColor White
    Write-Info ""
}

if (-not $NoClipboard -and -not $Quiet) {
    try {
        Set-Clipboard -Value $cmd
        Write-Info "(comando copiato in clipboard)" "DarkGray"
    } catch {
        Write-Info "(clipboard non disponibile, copia manuale)" "DarkGray"
    }
}

# Quiet mode: solo comando in stdout (per pipe o test)
if ($Quiet) {
    Write-Output $cmd
}
