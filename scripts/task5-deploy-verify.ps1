<#
.SYNOPSIS
  OD-050 Task-5 helper: deploy canonical-3b (Ryzen local + Lenovo via SSH)
  + static-assert tdd-guard plugin=false BOTH PC. Collapses N-edit x 2-PC
  manual matrix to: 1 command + 1 human edit.
.DESCRIPTION
  Gate-compliant verification tooling for the APPROVED OD-050 C-raffinato
  plan (NO remediation code). Rationale: only CHANGED thing =
  enabledPlugins.tdd-guard@tdd-guard flag (static-verifiable). Plugin
  disabled => bundled hooks.json inert = documented Claude Code platform
  contract (not re-empirically-proven each deploy). ONE live human trigger
  Ryzen falsifies the exact OD-050 bug; Lenovo = script-identical +
  static-assert parity (canonical precedent hook_userprofile_fix
  "Lenovo verify-if-doubt, trust-by-parity"). Default DRY-RUN; -Apply writes.
  Idempotent. Lenovo via SSH only (no Claude session there = no rug-pull).
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

Say "`n[1] Ryzen local deploy ($mode)"
if (-not (Test-Path $DEPLOY)) { Say "  FATAL: $DEPLOY assente (git -C C:\dev\vault pull?)"; exit 2 }
if ($Apply) { & powershell -NoProfile -ExecutionPolicy Bypass -File $DEPLOY -Apply | Select-Object -Last 4 }
else        { & powershell -NoProfile -ExecutionPolicy Bypass -File $DEPLOY        | Select-String 'tdd-guard|DRY-RUN' }

Say "`n[2] Lenovo via SSH ($LENOVO)"
$lc = "git -C C:\dev\vault pull --ff-only origin main 2>&1 | Select-Object -Last 1; powershell -NoProfile -ExecutionPolicy Bypass -File $DEPLOY $(if($Apply){'-Apply'}) 2>&1 | Select-Object -Last 3"
try { (& ssh -i $KEY -o ConnectTimeout=10 $LENOVO "powershell -NoProfile -Command `"$lc`"" 2>&1) | ForEach-Object { Say "  L| $_" } }
catch { Say "  SSH-FAIL Lenovo: $($_.Exception.Message) -> deploy Lenovo manuale (runbook #181)" }

Say "`n[3] STATIC-ASSERT tdd-guard@tdd-guard == False (both PC)"
$rz = & powershell -NoProfile -Command $probe
$ln = try { (& ssh -i $KEY -o ConnectTimeout=10 $LENOVO "powershell -NoProfile -Command `"$probe`"" 2>&1) -join '' } catch { "SSH-FAIL" }
Say "  Ryzen  : $rz"
Say "  Lenovo : $ln"
$ok = ($rz -eq 'False') -and ($ln -eq 'False')
if (-not $Apply) { Say "`n[VERDICT] DRY-RUN — nothing written. Re-run -Apply then asserts." }
elseif ($ok) {
  Say "`n[VERDICT] STATIC PASS 2-PC (plugin=false both). Contract: plugin-disabled => hooks.json inert."
  Say "  REMAINING (1 human, Ryzen only; Lenovo trusted script-identical+static-parity):"
  Say "  -> FRESH Claude Code Desktop, select C:\dev\vault, edit any .md 1 line. EXPECT: NOT blocked."
  Say "     NOT blocked -> OD-050 RESOLVED (tell Claude). BLOCKED -> session not post-Apply-fresh / recheck settings.json."
} else { Say "`n[VERDICT] STATIC FAIL (R=$rz L=$ln). NOT resolved. Rollback=git revert canonical-3b (1-revert)." }
exit 0
