# OD-050 L2: seed tdd-guard custom-instructions from tracked template.
# tdd-guard reads .claude/tdd-guard/data/instructions.md (gitignored,
# runtime). If absent it would create DEFAULT strict rules. We pre-seed
# from the tracked path-scope template so codemasterdd (mixed repo) exempts
# ops/docs. tdd-guard never overwrites an existing instructions.md, so
# seeding only-if-absent is safe + idempotent. Non-blocking by design.
$ErrorActionPreference = 'SilentlyContinue'
try {
  $root = $env:CLAUDE_PROJECT_DIR
  if (-not $root) { exit 0 }
  $tpl  = Join-Path $root 'scripts/hooks/tddguard-instructions.template.md'
  $data = Join-Path $root '.claude/tdd-guard/data'
  $dst  = Join-Path $data 'instructions.md'
  if (-not (Test-Path $tpl)) { exit 0 }
  if (-not (Test-Path $data)) { New-Item -ItemType Directory -Path $data -Force | Out-Null }
  if (-not (Test-Path $dst)) { Copy-Item -LiteralPath $tpl -Destination $dst -Force }
} catch { }
exit 0
