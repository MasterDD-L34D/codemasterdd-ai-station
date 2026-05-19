<#
.SYNOPSIS
  DEPRECATED 2026-05-19. OD-050 Task-5 verification is handled by the
  runbook (manual-robust > fragile-automation, lesson encoded in
  docs/sessions/2026-05-19-continuity-handoff.md EVENING UPDATE).
.DESCRIPTION
  Original helper attempted to collapse the 2-PC deploy+verify matrix
  into one command. It cost 4 fix-iterations (em-dash mojibake +
  nested-quoting probe + SSH cmd-incompat `|tail` + deploy-unicode
  misread) and was still fragile. The robust path is direct
  findstr/file-read + the cross-PC runbook.

  CANONICAL VERIFY PATH:
    docs/runbook/tddguard-task5-cross-pc-verify.md  (PR #181)

  This stub prints the redirect and exits 2. Do not restore the original
  body. History preserved in git: commits ab49e4f, 5320832.
#>
param([switch]$Apply)
Write-Host "DEPRECATED: task5-deploy-verify.ps1 (OD-050 Task-5 helper)."
Write-Host "  Reason   : known-fragile; runbook is the supported path."
Write-Host "  Use      : docs/runbook/tddguard-task5-cross-pc-verify.md"
Write-Host "  History  : git log -- scripts/task5-deploy-verify.ps1"
exit 2
