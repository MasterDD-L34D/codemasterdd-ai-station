# jules-daily-digest.ps1 -- READ-ONLY Jules sessions digest (ADR-0034 Option D)
# Eduardo formal authorization 2026-05-18 (tdd-guard bypass explicitly authorized).
# READ-ONLY: GET Jules API + gh api + writes local digest .md. ZERO Jules mutation
# (archive/sendMessage/start = Eduardo batch-approve -> Claude API, NOT here).
$ErrorActionPreference = 'Stop'
$env:JULES_API_KEY = ((Get-Content "$HOME/.config/api-keys/keys.env" |
  Where-Object { $_ -match '^JULES_API_KEY=' }) -replace '^JULES_API_KEY=', '')
$repo = 'C:/dev/codemasterdd-ai-station'
$day  = Get-Date -Format 'yyyy-MM-dd'
$out  = "$repo/docs/jules-batch/$day-digest.md"
$api  = 'https://jules.googleapis.com/v1alpha'
$hdr  = @{ 'x-goog-api-key' = $env:JULES_API_KEY }

$sess = (Invoke-RestMethod -Headers $hdr "$api/sessions?pageSize=100").sessions |
  Where-Object { $_.state -eq 'AWAITING_USER_FEEDBACK' }

$lines = @(
  "# Jules daily digest $day (ADR-0034 Option D, READ-ONLY)",
  "> Verdetti FIRST-PASS scriptabili. Generative = Eduardo batch-approve.",
  "> Suggestions NON incluse (browser-only). Ambigui = Claude-review.",
  ""
)
foreach ($s in $sess) {
  $id  = $s.name -replace 'sessions/', ''
  $src = $s.sourceContext.source -replace 'sources/github/', ''
  $f   = ([regex]'File:\s*([^\s:]+)').Match($s.prompt).Groups[1].Value
  $verdict = 'NEEDS-CLAUDE-EVAL'; $ev = ''
  if ($f) {
    try {
      $c = (gh api "repos/$src/contents/$f" --jq '.content' 2>$null |
        ForEach-Object { [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($_)) })
    } catch { $c = '' }
    $mk = ([regex]'(?m)^\s*//\s*(.{12,60})').Match($s.prompt).Groups[1].Value
    if ($mk -and $c -match [regex]::Escape($mk)) {
      $verdict = 'ARCHIVE? (marker gia su origin/main)'; $ev = "$f :: $mk"
    } elseif ($f -match 'services/generation') {
      $verdict = 'DEFER (services/generation = M1-freeze sensitive)'
    } else {
      $verdict = 'NEEDS-CLAUDE-EVAL'; $ev = "$f (no marker match -> ambiguo)"
    }
  }
  $t0 = ($s.title -split "`n")[0]
  $t0 = $t0.Substring(0, [Math]::Min(70, $t0.Length))
  $lines += "- ``$id`` [$src] **$verdict** -- $t0  | $ev"
}
$lines += @(
  "",
  "## Manuale (non scriptabile)",
  "- Suggestions: apri jules.google dashboard per-repo, review.",
  "- NEEDS-CLAUDE-EVAL sopra: ping Claude per ground-truth profondo.",
  "",
  "## Gate",
  "Nessuna azione auto. Eduardo: review -> approva batch -> Claude API exec."
)
New-Item -ItemType Directory -Force -Path "$repo/docs/jules-batch" | Out-Null
Set-Content -Encoding utf8 $out ($lines -join "`n")
Write-Host "DIGEST -> $out ($($sess.Count) Awaiting)"
