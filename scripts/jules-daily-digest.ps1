# jules-daily-digest.ps1 -- READ-ONLY Jules sessions digest (ADR-0034 Option D)
# Eduardo formal auth 2026-05-18 + explicit tdd-guard bypass.
# Heuristic v3.1 (runbook "grep marker univoco del fix vs origin/main"):
#   v1 line-count + v2 substring falsified (whitespace/refactor drift -> all
#   AMBIGUOUS). v3 introduced unique intent-marker grep but had a PowerShell
#   scalar-trap (1-elem pipeline + [0] = first CHAR -> marker '/' -> false
#   ARCHIVE on all). v3.1 fixes selection via Select-Object -First 1.
#   Signal = distinctive intent-marker COMMENT Jules pastes in Context
#   ("// Codex PR #2031 P1 fix: ...", "// W8L fix: ...", "// GSD audit fix:").
#   Marker literal-present in origin/main = fix shipped -> ARCHIVE; absent ->
#   genuinely actionable. Validated vs robust gh-api ground-truth 2026-05-18.
# READ-ONLY: GET Jules API + gh api. ZERO Jules mutation. Error-safe:
#   never false-ARCHIVE; any parse/fetch failure -> AMBIGUOUS (Claude-eval).
$ErrorActionPreference = 'Stop'
$env:JULES_API_KEY = ((Get-Content "$HOME/.config/api-keys/keys.env" |
  Where-Object { $_ -match '^JULES_API_KEY=' }) -replace '^JULES_API_KEY=', '')
$repo='C:/dev/codemasterdd-ai-station'; $day=Get-Date -Format 'yyyy-MM-dd'
$out="$repo/docs/jules-batch/$day-digest.md"
$api='https://jules.googleapis.com/v1alpha'; $hdr=@{'x-goog-api-key'=$env:JULES_API_KEY}
$FREEZE='services/generation|services/rules|apps/backend/services/combat'
$sess=(Invoke-RestMethod -Headers $hdr "$api/sessions?pageSize=100").sessions |
  Where-Object { $_.state -eq 'AWAITING_USER_FEEDBACK' }
$lines=@(
 "# Jules daily digest $day (ADR-0034 Option D, READ-ONLY, heuristic v3.1)",
 "> ARCHIVE = fix intent-marker comment present in origin/main (already-shipped, rework).",
 "> OPEN = marker absent (genuinely actionable: respond-scoped or start-candidate).",
 "> DEFER = freeze-sensitive path (Eduardo-review, never auto). AMBIGUOUS = no marker / fetch fail -> Claude-eval.",
 "> Generative actions (archive/respond/start) = Eduardo batch-approve, NOT auto. Suggestions = browser-only.","")
foreach($s in $sess){
  $id=$s.name -replace 'sessions/',''
  $src=$s.sourceContext.source -replace 'sources/github/',''
  $p=[string]$s.prompt
  $verdict='AMBIGUOUS (no parseable fix-marker)'; $ev='-> Claude-eval'; $f=''
  try{
    $fm=[regex]::Match($p,'(?im)^[\*\-\s]*\**\s*File:?\**\s*`?([^\s:`]+)')
    if($fm.Success){ $f=$fm.Groups[1].Value }
    $cm=[regex]::Match($p,'(?s)```[a-zA-Z]*\s*(.*?)```')
    $ctx= if($cm.Success){ $cm.Groups[1].Value } else { '' }
    $pri=@(); $sec=@()
    foreach($ln in ($ctx -split "`n")){
      $t=$ln.Trim()
      if($t.Length -lt 20 -or $t.Length -gt 130){ continue }
      if($t -match '(fix:|PR #\d+)'){ $pri+=$t }
      elseif($t -match '(GSD audit|Bot review|Codex|Sprint \w|W\d+ )'){ $sec+=$t }
    }
    # PowerShell scalar trap: a 1-elem pipeline collapses to a string and
    # (...)[0] returns its first CHAR. Use Select-Object -First 1 (object-safe).
    $marker=''
    if(@($pri).Count){ $marker=[string]($pri | Sort-Object { $_.Length } -Descending | Select-Object -First 1) }
    elseif(@($sec).Count){ $marker=[string]($sec | Sort-Object { $_.Length } -Descending | Select-Object -First 1) }
    if($f -and ($f -match $FREEZE)){
      $verdict='DEFER (freeze-sensitive path)'
      $ev= if($marker){ "$f | marker: $($marker.Substring(0,[Math]::Min(50,$marker.Length)))" } else { "$f" }
    }
    elseif($f -and $marker -and $marker.Length -ge 12){
      $code=''
      try{ $b64=(gh api "repos/$src/contents/$f" --jq '.content' 2>$null)
        if($b64){ $code=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String(($b64 -replace '\s',''))) } }catch{ $code='' }
      if($code -and $code.Contains($marker)){
        $verdict='ARCHIVE (already-shipped: fix-marker in origin/main)'
        $ev="$f | marker present"
      } elseif($code){
        $verdict='OPEN (actionable: marker absent from origin/main)'
        $ev="$f | marker absent -> respond-scoped / start"
      } else {
        $verdict='AMBIGUOUS (file fetch failed)'; $ev="$f -> Claude-eval"
      }
    } else { $ev= if($f){ "$f (no fix-marker in Context) -> Claude-eval" } else { 'no File/Context -> Claude-eval' } }
  } catch { $verdict='AMBIGUOUS (parse error)'; $ev='-> Claude-eval' }
  $t0=(($s.title -split "`n")[0]).Trim(); $t0=$t0.Substring(0,[Math]::Min(64,$t0.Length))
  $lines+="- ``$id`` [$src] **$verdict** -- $t0  | $ev"
}
$lines+=@("","## Manuale (non scriptabile)",
 "- Suggestions: jules.google dashboard per-repo (browser-only, no API list).",
 "- AMBIGUOUS / OPEN: ping Claude per ground-truth + scoped response/start draft.","",
 "## Gate (ADR-0034 Option D)",
 "Nessuna azione auto-eseguita. Eduardo: review questo digest -> 1 batch-approve/reject -> Claude API exec (sendMessage/archive/create gia' pre-auth settings.json). Generativo NON auto.")
New-Item -ItemType Directory -Force -Path "$repo/docs/jules-batch" | Out-Null
Set-Content -Encoding utf8 $out ($lines -join "`n")
Write-Host "DIGEST v3.1 -> $out ($($sess.Count) Awaiting)"
