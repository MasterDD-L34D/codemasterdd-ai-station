# jules-daily-digest.ps1 -- READ-ONLY Jules sessions digest (ADR-0034 Option D)
# Eduardo formal auth 2026-05-18 + explicit tdd-guard bypass.
#
# Heuristic history (SDMG/Protocol-7: self-designed, externally falsified,
# adopted-not-defended -- a LESSON, not a victory):
#   v1 line-count / v2 substring -> drift -> all AMBIGUOUS.
#   v3/v3.1 prompt-marker-vs-origin/main -> harsh-reviewer REJECT + Jules-
#     activities axis FALSIFIED: markers are often the PRE-EXISTING context
#     comment, not proof Jules shipped; wrong 4/8 incl 3 false-ARCHIVE;
#     "validated 8/8" spurious (circular: same gh-api source).
#   v4 prompt-File freeze parse flaky in-loop (harsh-reviewer P1-2).
#   v4.1 = INDEPENDENT 2-source signal, no prompt parse on the PR path:
#     Jules session --(API)--> linked GitHub PR --(gh)--> {state, files}.
#     MERGED + no freeze file = ARCHIVE (shipped). CLOSED/OPEN/no-PR = NOT
#     shipped (actionable). Freeze = ANY PR file under services/generation|
#     services/rules|apps/backend/services/combat -> DEFER (Eduardo-review,
#     never auto, even if merged). No-PR + File-hint unparseable -> DEFER
#     (conservative: freeze-miss is the dangerous direction). NEVER ARCHIVE
#     unless PR MERGED & zero freeze files. Any uncertainty -> AMBIGUOUS.
#
# Digest = ENUMERATOR + advisory signal feeding the Claude-drafted batch
# Eduardo per-cycle batch-approves (ADR-0034 Option D). Zero auto-exec.
$ErrorActionPreference = 'Stop'
$env:JULES_API_KEY = ((Get-Content "$HOME/.config/api-keys/keys.env" |
  Where-Object { $_ -match '^JULES_API_KEY=' }) -replace '^JULES_API_KEY=', '')
$repo='C:/dev/codemasterdd-ai-station'; $day=Get-Date -Format 'yyyy-MM-dd'
$out="$repo/docs/jules-batch/$day-digest.md"
$api='https://jules.googleapis.com/v1alpha'; $hdr=@{'x-goog-api-key'=$env:JULES_API_KEY}
$FREEZE='services/generation|services/rules|apps/backend/services/combat'
function IsFreeze($paths){ foreach($x in $paths){ if($x -match $FREEZE){ return $true } } return $false }
try{ $resp=Invoke-RestMethod -Headers $hdr "$api/sessions?pageSize=100" }
catch{
  $m="# Jules daily digest $day -- ERROR`n`n> Sessions API fetch FAILED ($($_.Exception.Message)). NOT empty-set; re-run / check JULES_API_KEY."
  New-Item -ItemType Directory -Force -Path "$repo/docs/jules-batch" | Out-Null
  [IO.File]::WriteAllText($out,$m,(New-Object Text.UTF8Encoding $false))
  Write-Host "DIGEST v4.1 -> ERROR (API fetch failed)"; exit 1 }
$sess=@($resp.sessions | Where-Object { $_.state -eq 'AWAITING_USER_FEEDBACK' })
$lines=@(
 "# Jules daily digest $day (ADR-0034 Option D, READ-ONLY, heuristic v4.1: PR-state+files)",
 "> Signal = Jules session -> linked GitHub PR -> {merge-state, changed files}. Independent of prompt text.",
 "> ARCHIVE = linked PR MERGED & no freeze file (shipped, rework). ACTIONABLE = PR closed-unmerged/open or Jules-asking (NOT shipped).",
 "> DEFER = PR touches / task targets a freeze-sensitive path (Eduardo-review, never auto, even if shipped). AMBIGUOUS = no clear signal.",
 "> Verdicts ADVISORY. Generative (archive/respond/start) = Eduardo per-cycle batch-approve, NOT auto. Suggestions = browser-only.","",
 "Awaiting sessions: $($sess.Count)","")
foreach($s in $sess){
  $id=$s.name -replace 'sessions/',''
  $src=$s.sourceContext.source -replace 'sources/github/',''
  $verdict='AMBIGUOUS'; $ev='-> Claude-eval'
  try{
    $raw=($s | ConvertTo-Json -Depth 12 -Compress)
    $prm=[regex]::Match($raw,'github\.com/[\w.-]+/[\w.-]+/pull/(\d+)')
    if($prm.Success){
      $prn=$prm.Groups[1].Value; $st=''; $mg=''; $pf=@()
      try{ $j=(gh pr view $prn --repo $src --json state,mergedAt,files 2>$null | ConvertFrom-Json)
        $st=$j.state; $mg=$j.mergedAt; $pf=@($j.files | ForEach-Object { $_.path }) }catch{ $st='' }
      $fz=IsFreeze $pf
      if($st -eq 'MERGED'){
        if($fz){ $verdict='DEFER (freeze-path; PR merged but Eduardo-review)'; $ev="PR#$prn MERGED, touches freeze: $(@($pf|?{$_ -match $FREEZE}) -join ',')" }
        else { $verdict='ARCHIVE (shipped: linked PR merged)'; $ev="PR#$prn MERGED $mg | files: $(@($pf|Select -First 3) -join ',')" }
      } elseif($st -eq 'CLOSED'){
        $verdict= if($fz){'DEFER (freeze-path; PR closed-unmerged)'} else {'ACTIONABLE (linked PR CLOSED unmerged -> NOT shipped)'}
        $ev="PR#$prn closed-unmerged -> Claude: abandon/retry?"
      } elseif($st -eq 'OPEN'){
        $verdict= if($fz){'DEFER (freeze-path; PR open)'} else {'IN-PROGRESS (linked PR OPEN)'}
        $ev="PR#$prn open -> Claude: monitor/scope-check"
      } else { $verdict='AMBIGUOUS (PR state unknown)'; $ev="PR#$prn -> Claude-eval" }
    } else {
      # No linked PR: get FULL session (list payload trusted only for the
      # PR-link scan above). File-hint parse is best-effort; uncertain ->
      # DEFER (conservative: freeze-miss is the dangerous direction).
      $f=''
      try{ $full=Invoke-RestMethod -Headers $hdr "$api/sessions/$id"
        $fm=[regex]::Match([string]$full.prompt,'(?im)^[\*\-\s]*\**\s*File:?\**\s*`?([^\s:`]+)')
        if($fm.Success){ $f=$fm.Groups[1].Value } }catch{ $f='' }
      $acts=$null
      try{ $acts=(Invoke-RestMethod -Headers $hdr "$api/sessions/$id/activities?pageSize=50").activities }catch{ $acts=$null }
      if($f -and ($f -match $FREEZE)){
        $verdict='DEFER (freeze-path; no PR)'; $ev="$f -> Eduardo-review"
      } elseif(-not $f){
        $verdict='DEFER (file-hint unparseable -> conservative)'; $ev='no parseable File -> Eduardo-review (avoid freeze-miss)'
      } elseif($acts){
        $np=@($acts | Where-Object { $_.PSObject.Properties.Name -contains 'planGenerated' }).Count
        $done=@($acts | Where-Object { $_.PSObject.Properties.Name -contains 'sessionCompleted' }).Count
        $am=@($acts | Where-Object { $_.PSObject.Properties.Name -contains 'agentMessaged' }).Count
        if($done -gt 0){ $verdict='AMBIGUOUS (completed, no linked PR)'; $ev="$f | shipped elsewhere? -> Claude-eval" }
        elseif($np -eq 0 -and $am -gt 0){ $verdict='ACTIONABLE (Jules investigating/asking, no plan/PR)'; $ev="$f | Jules awaiting guidance -> Claude: scoped reply" }
        else { $verdict='AMBIGUOUS (no PR, unclear activity)'; $ev="$f -> Claude-eval" }
      } else { $verdict='AMBIGUOUS (no PR, activities unavailable)'; $ev="$f -> Claude-eval" }
    }
  } catch { $verdict='AMBIGUOUS (parse error)'; $ev='-> Claude-eval' }
  $t0=(($s.title -split "`n")[0]).Trim(); $t0=$t0.Substring(0,[Math]::Min(60,$t0.Length))
  $lines+="- ``$id`` [$src] **$verdict** -- $t0  | $ev"
}
$lines+=@("","## Manuale (non scriptabile)",
 "- Suggestions: jules.google dashboard per-repo (browser-only, no API list).",
 "- ACTIONABLE/IN-PROGRESS/AMBIGUOUS: Claude ground-truth (activities/diff) -> scoped response or start, drafted in batch.","",
 "## Gate (ADR-0034 Option D)",
 "Digest = enumeratore advisory. Nessuna azione auto. Eduardo: review -> 1 batch-approve/reject del batch Claude-drafted -> exec. Generativo NON auto. Standing settings.json entries: P0-3 Eduardo-manual (classifier blocca self-mod).")
New-Item -ItemType Directory -Force -Path "$repo/docs/jules-batch" | Out-Null
[IO.File]::WriteAllText($out,(($lines -join "`n")+"`n"),(New-Object Text.UTF8Encoding $false))
Write-Host "DIGEST v4.1 -> $out ($($sess.Count) Awaiting)"
