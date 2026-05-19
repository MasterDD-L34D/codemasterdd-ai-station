<#
.SYNOPSIS
  OD-050 Task-5 helper: deploy canonical-3b (Ryzen local + Lenovo via SSH)
  + static-assert tdd-guard plugin=false BOTH PC. Collapses the
  N-edit x 2-PC manual matrix to: 1 command + 1 human edit.
.DESCRIPTION
  Gate-compliant verification tooling for the APPROVED OD-050 plan
  (NO remediation code). Only CHANGED thing = enabledPlugins
  tdd-guard@tdd-guard flag (static-verifiable). Plugin disabled =>
  bundled hooks.json inert = documented Claude Code platform contract.
  ONE live human trigger Ryzen falsifies the exact OD-050 bug; Lenovo =
  script-identical + static-assert parity (precedent hook_userprofile_fix).
  Default DRY-RUN; -Apply writes. Idempotent. Lenovo via SSH only.
  ASCII-only by policy (CLAUDE.md encoding: no em-dash/smart-quotes).
#>
param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$LENOVO = 'edusc@192.168.1.10'
$KEY    = "$env:USERPROFILE\.ssh\id_ed25519"
$DEPLOY = 'C:\dev\vault\Vault-ops-remote\scripts\deploy_claude_global.ps1'
$mode   = if ($Apply) { 'APPLY' } else { 'DRY-RUN (use -Apply)' }
function Say($m){ Write-Host $m }
Say "=== OD-050 Task-5 deploy+verify [$mode] ==="
$probe = '$p="$env:USERPROFILE\.claude\settings.json"; if(Test-Path $p){ try{ $j=Get-Content $p -Raw|ConvertFrom-Json; $v=$j.enabledPlugins."tdd-guard@tdd-guard"; if($null -eq $v){"ABSENT"}else{"$v"} }catch{"PARSE-ERR"} }else{"NO-SETTINGS"}'

Say ""
Say "[1] Ryzen local deploy ($mode)"
if (-not (Test-Path $DEPLOY)) { Say "  FATAL: $DEPLOY assente (git -C C:\dev\vault pull?)"; exit 2 }
if ($Apply) { & powershell -NoProfile -ExecutionPolicy Bypass -File $DEPLOY -Apply | Select-Object -Last 4 }
else        { & powershell -NoProfile -ExecutionPolicy Bypass -File $DEPLOY        | Select-String 'tdd-guard|DRY-RUN' }

Say ""
Say "[2] Lenovo via SSH ($LENOVO)"
$ap = if ($Apply) { '-Apply' } else { '' }
$lc = "git -C C:\dev\vault pull --ff-only origin main 2>&1 | Select-Object -Last 1; powershell -NoProfile -ExecutionPolicy Bypass -File $DEPLOY $ap 2>&1 | Select-Object -Last 3"
try { (& ssh -i $KEY -o ConnectTimeout=10 $LENOVO "powershell -NoProfile -Command `"$lc`"" 2>&1) | ForEach-Object { Say "  L| $_" } }
catch { Say "  SSH-FAIL Lenovo: $($_.Exception.Message) -- deploy Lenovo manuale (runbook tddguard-task5)" }

Say ""
Say "[3] STATIC-ASSERT tdd-guard@tdd-guard == False (both PC)"
$rz = & powershell -NoProfile -Command $probe
$ln = try { (& ssh -i $KEY -o ConnectTimeout=10 $LENOVO "powershell -NoProfile -Command `"$probe`"" 2>&1) -join '' } catch { "SSH-FAIL" }
Say "  Ryzen  : $rz"
Say "  Lenovo : $ln"
$ok = ($rz -eq 'False') -and ($ln -eq 'False')
Say ""
if (-not $Apply) {
  Say "[VERDICT] DRY-RUN -- nothing written. Re-run with -Apply, then asserts."
} elseif ($ok) {
  Say "[VERDICT] STATIC PASS 2-PC (plugin=false both). Contract: plugin-disabled => hooks.json inert."
  Say "  REMAINING 1 human action (Ryzen only; Lenovo trusted by script-identical+static-parity):"
  Say "  -> Open FRESH Claude Code Desktop, select folder C:\dev\vault, ask it to edit any .md 1 line."
  Say "     EXPECT: NOT blocked. If NOT blocked -> OD-050 RESOLVED (tell Claude)."
  Say "     If BLOCKED -> session not post-Apply-fresh, or recheck ~/.claude/settings.json."
} else {
  Say "[VERDICT] STATIC FAIL (Ryzen=$rz Lenovo=$ln). NOT resolved. Do NOT close OD-050."
  Say "  Rollback = git revert the canonical-3b commit in vault (single revert)."
}
exit 0
