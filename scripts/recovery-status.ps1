param(
    [switch]$Json
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function Test-Command($Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Test-RelativePath($RelativePath) {
    return Test-Path -LiteralPath (Join-Path $RepoRoot $RelativePath)
}

function Get-GitValue($ArgsList) {
    try {
        $output = & git @ArgsList 2>$null
        if ($LASTEXITCODE -eq 0) {
            return ($output | Select-Object -First 1)
        }
    } catch {
        return $null
    }
    return $null
}

$externalPaths = [ordered]@{
    game = "C:\dev\Game"
    synesthesia = "C:\dev\synesthesia"
    dafne = "C:\Users\edusc\Dafne\workspace\swarm"
    aa01 = "C:\Users\edusc\aa01"
    aider_bin = "C:\Users\edusc\.local\bin"
    api_keys = "C:\Users\edusc\.config\api-keys\keys.env"
}

$runtimeEvidence = [ordered]@{
    dogfood_log = "logs\aider-delegation-2026-04.md"
    dogfood_db = "apps\dogfood-ui\data\dogfood.sqlite"
    promptfoo_results = "scripts\quality-bench\results"
}

$status = [ordered]@{
    repo_root = $RepoRoot.Path
    branch = Get-GitValue @("branch", "--show-current")
    head = Get-GitValue @("rev-parse", "--short", "HEAD")
    project_state = Test-RelativePath "PROJECT_STATE.yaml"
    active_sprint = Test-RelativePath "SPRINT_02.md"
    recovery_audit = Test-RelativePath "docs\recovery\2026-04-30-transplant-audit.md"
    external_repos_registry = Test-RelativePath "EXTERNAL_REPOS.md"
    tools = [ordered]@{
        git = Test-Command "git"
        python = Test-Command "python"
        node = Test-Command "node"
        docker = Test-Command "docker"
        ollama = Test-Command "ollama"
        aider = Test-Command "aider"
        opencode = Test-Command "opencode"
        gh = Test-Command "gh"
    }
    external_paths = [ordered]@{}
    runtime_evidence = [ordered]@{}
}

foreach ($item in $externalPaths.GetEnumerator()) {
    $status.external_paths[$item.Key] = Test-Path -LiteralPath $item.Value
}

foreach ($item in $runtimeEvidence.GetEnumerator()) {
    $status.runtime_evidence[$item.Key] = Test-RelativePath $item.Value
}

if ($Json) {
    $status | ConvertTo-Json -Depth 6
    exit 0
}

Write-Host "CodeMasterDD recovery status"
Write-Host "Repo:   $($status.repo_root)"
Write-Host "Branch: $($status.branch)"
Write-Host "HEAD:   $($status.head)"
Write-Host ""

Write-Host "Core files"
Write-Host "  PROJECT_STATE.yaml: $($status.project_state)"
Write-Host "  SPRINT_02.md:       $($status.active_sprint)"
Write-Host "  recovery audit:     $($status.recovery_audit)"
Write-Host "  external registry:  $($status.external_repos_registry)"
Write-Host ""

Write-Host "Tools"
foreach ($item in $status.tools.GetEnumerator()) {
    Write-Host ("  {0,-10} {1}" -f $item.Key, $item.Value)
}
Write-Host ""

Write-Host "External paths"
foreach ($item in $status.external_paths.GetEnumerator()) {
    Write-Host ("  {0,-12} {1}" -f $item.Key, $item.Value)
}
Write-Host ""

Write-Host "Runtime evidence"
foreach ($item in $status.runtime_evidence.GetEnumerator()) {
    Write-Host ("  {0,-16} {1}" -f $item.Key, $item.Value)
}
