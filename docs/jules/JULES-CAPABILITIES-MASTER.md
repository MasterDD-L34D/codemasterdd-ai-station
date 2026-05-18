# JULES — Documento capacità/funzioni/wiring MASTER (unico, consolidato)

> Doc unico richiesto da Eduardo 2026-05-18. Consolida: modello governance
> (ADR-0032→0033→0034 Option D), wiring reale 3-layer (API/CLI/browser),
> matrice autorizzazioni + pattern-permessi esatti da applicare, runbook,
> finding empirici. **Authority**: ADR-0034 (Accepted Option D) governa;
> questo doc = riferimento operativo unico (supersede note sparse).

## 1. Modello governance (catena)

| ADR | Esito |
|-----|-------|
| 0032 Jules active-model | Self-distrutto (69% FP-close, 2 backfire #2294/#2313, 0 merge utili). Superseded. |
| 0033 Jules resolved | (1) throttle org-level PRIMARIO + (3) own-repo-active restano. (2) esterni-read-only superseded da 0034. |
| 0034 Jules autonomous-managed (Option D) | **Accepted 2026-05-18**. Full-auto triage+ground-truth + auto-exec-solo-non-generativo + generativo via batch-approve Eduardo. Option A (full-autonomous-corrective) REJECTED-redux da harsh-reviewer (SDMG, non difesa). |

**Rail hard R1-R7** (ADR-0034, non negoziabili): R1 ground-truth-gate ·
R2 verdict-logic · R3 scoped-response-template · R4 no-corrective-loop +
2-backfire→auto-revert · R5 anti-noise-cap (15 ceiling non target) ·
R6 suggestions-gate · R7 audit-trail `logs/jules-autonomous-YYYY-MM.md`.

## 2. Wiring reale 3-layer (empirico 2026-05-18)

| Layer | Copre | Stato |
|-------|-------|-------|
| **API ufficiale v1alpha** (`jules.googleapis.com/v1alpha`, header `x-goog-api-key: $JULES_API_KEY`) | **Sessioni: tutto** | **METODO CANONICO** (supera CLI+browser) |
| CLI `@google/jules` (`jules remote list/pull/new`) | sessioni list/pull/start (wrapper parziale, troncato) | fallback; richiede `jules login` one-time |
| Browser (Claude-in-Chrome) | **suggestions discovery SOLO** | irriducibile (API 404, CLI cieco); classifier-blocked |

### API endpoint mappati (read-only verificati)
- `GET /v1alpha/sessions[?pageSize=]` → list completa (name/title/state/sourceContext/prompt)
- `GET /v1alpha/sessions/{id}` → detail
- `GET /v1alpha/sessions/{id}/activities` → plan+steps+originator (conversazione/piano)
- `GET /v1alpha/sources` → repo+branch
- `POST /v1alpha/sessions/{id}:sendMessage` → respond/correct (WRITE)
- archive/approvePlan/create-session → endpoint da verificare read-first prima di documentare come autorizzabili (NON probare a caso = anti-pattern)

### Finding duri
- **Suggestions NON hanno API v1alpha** (404 su tutti i guess) + CLI cieco → discovery suggestions = SOLO browser dashboard. Fully-autonomous-suggestions NON ottenibile senza permission-rule browser + accettare rischio SDMG-rejected (start-from-suggestion = generativo esterno).
- API `x-goog-api-key` auth funziona (Bash curl, come gh-api). Read = nessun blocco.

## 3. Matrice autorizzazioni + pattern-permessi (Eduardo applica — agent self-mod BARRATO dal harness, corretto)

| Azione | Autorizzata? | Pattern |
|--------|--------------|---------|
| API read (`GET sessions/sources/activities`) | ✅ sì (Bash curl generico) | nessuna modifica |
| API `sendMessage` (respond/correct) | ✅ **già** | settings.json `autoMode.allow` riga 122 (esistente) |
| API archive/complete sessione | ⚠️ da autorizzare | **Eduardo aggiunge** a `~/.claude/settings.json` `autoMode.allow` una entry analoga a riga 122, es: `"Bash curl/python POST to https://jules.googleapis.com/v1alpha/sessions/*:<archiveMethod> to close ground-truth-verified-already-shipped Jules sessions, ADR-0034 Option D batch-approved only, key from ~/.config/api-keys/keys.env"` (sostituire `<archiveMethod>` col metodo reale dopo verifica read-only endpoint) |
| API create session (start da suggestion/task) | ⚠️ da autorizzare | analoga: `"... POST https://jules.googleapis.com/v1alpha/sessions to create Jules sessions for Eduardo-approved tasks, ADR-0034 Option D, ..."` |
| Browser jules.google (suggestions discovery) | ❌ classifier-blocked | Eduardo aggiunge permission per `mcp__Claude_in_Chrome__*` su jules.google **OPPURE** suggestions restano azione manuale Eduardo (raccomandato: API non le copre, alto-rischio autonomo) |
| Skill `update-config` (self-mod permessi) | ❌ barrato by-design | **SOLO Eduardo edita settings.json a mano** — l'agent NON può auto-concedersi guardrail (multi-layer, corretto, allineato SDMG/ADR-0034) |

**Principio**: l'agent documenta i pattern; Eduardo li applica. Il
batch-approve Option D resta il controllo-policy anche con permessi
tool-broadened (permesso = meccanismo harness; Option D = policy umana).

## 4. Modello operativo Option D (ciclo)

```
Claude: GET sessions/activities (API) → ground-truth vs origin/main (gh-api, R1)
  → verdict R2 (already-shipped→archive · open-sane→respond-scoped R3
     · sensitive/freeze→deferral · ambiguo→STOP-escalate)
  → DRAFT batch-artifact (docs/jules-batch/YYYY-MM-DD-batch-NN.md)
Eduardo: 1 batch approve/reject  ← UNICA interazione loop (fuori = intento ok)
Claude (post-approve, user-authorized): exec via API
  (sendMessage già-auth; archive/create post permission-pattern §3)
  → log R7
R4 kill-switch: 2 backfire finestra → auto-revert ADR-0033 read-only + escalate
R5: 15-cap = ceiling, riempito solo ROI-verificato; throttle org-level (Eduardo) = leva primaria
```

## 5. Stato batch-01 (2026-05-18) — pending Eduardo

`docs/jules-batch/2026-05-18-batch-01.md` (PR #170, approvato): 8 sessioni
Game Awaiting ground-truth 8/8. **7 ARCHIVE** (già-shippate verified) +
**1 RESPOND s8** (deferral freeze-scoped, = sendMessage già-autorizzato).
Suggestions Game (3× function-too-long) = defer (M1 freeze). + reco
throttle org-level. Exec bloccato solo da: archive-endpoint-authorization
(§3) — s8 sendMessage eseguibile (pre-auth) appena Option D ciclo lanciato.

## 6. Runbook collegati (non duplicare)
- `docs/runbook/jules-session-triage-via-cli.md` → **UPDATE**: API v1alpha
  e' canonico, CLI fallback. (questo doc lo supersede come riferimento.)
- `docs/adr/0034-...md` governance · `docs/adr/0033-...md` ledger+throttle.

## 7. Azioni Eduardo per autonomia piena (precise)
1. Verifica endpoint reale archive/create (read-only) → io lo documento esatto.
2. Aggiungi a `~/.claude/settings.json` `autoMode.allow` le 2 entry §3
   (archive + create) mirror riga 122. (agent barrato dal farlo.)
3. Suggestions: decidi — permission browser `mcp__Claude_in_Chrome__*`
   jules.google (autonomia suggestions, ma rischio SDMG) **o** restano tue
   (raccomandato: API non le copre, generativo-esterno = harsh-rejected).
4. Post-(2): Option D loop pienamente autonomo per sessioni (triage+respond
   +archive+create), Eduardo solo batch-approve + suggestions-manuali.

---
## 8. Daily-digest automation (Eduardo applica one-time — agent barrato self-bootstrap)

**Perche' locale-non-remoto**: routine remoti (`/schedule`) = cloud, ZERO
key/gh/browser locali → digest vuoto = false-confidence noise. Il digest
richiede `JULES_API_KEY` + `gh` + repo locali → **solo script locale**.
Automatizzabile: sessioni-API + ground-truth (scriptabile puro, no Claude/
browser). NON automatizzabile: suggestions (browser-only) + verdict-sfumato
(needs Claude) → il digest li FLAGGA manuali (no overclaim, lezione 69%-FP).

### Script (Eduardo salva come `scripts/jules-daily-digest.ps1`)

> Agent NON crea il .ps1 (TDD-guard premature-impl + self-bootstrap-infra
> barrato). Qui = documentato; Eduardo lo crea+installa. Read-only +
> scrive solo digest .md locale. ZERO mutazione Jules (no archive/send).

```powershell
# jules-daily-digest.ps1 -- READ-ONLY sessions digest (ADR-0034 Option D)
$ErrorActionPreference='Stop'
$env:JULES_API_KEY=(Get-Content "$HOME/.config/api-keys/keys.env" |
  Where-Object {$_ -match '^JULES_API_KEY='}) -replace '^JULES_API_KEY=',''
$repo='C:/dev/codemasterdd-ai-station'
$day=Get-Date -Format 'yyyy-MM-dd'
$out="$repo/docs/jules-batch/$day-digest.md"
$api='https://jules.googleapis.com/v1alpha'
$hdr=@{'x-goog-api-key'=$env:JULES_API_KEY}
$sess=(Invoke-RestMethod -Headers $hdr "$api/sessions?pageSize=100").sessions |
  Where-Object {$_.state -eq 'AWAITING_USER_FEEDBACK'}
$lines=@("# Jules daily digest $day (ADR-0034 Option D, READ-ONLY)",
 "> Verdetti FIRST-PASS scriptabili. Generative=Eduardo batch-approve.",
 "> Suggestions NON incluse (browser-only). Ambigui=Claude-review.","")
foreach($s in $sess){
  $id=$s.name -replace 'sessions/',''
  $src=$s.sourceContext.source -replace 'sources/github/',''
  # heuristic ground-truth: estrai 'File: <path>' dal prompt + marker
  $f=([regex]'File:\s*([^\s:]+)').Match($s.prompt).Groups[1].Value
  $verdict='NEEDS-CLAUDE-EVAL'; $ev=''
  if($f){
    $c=(gh api "repos/$src/contents/$f" --jq '.content' 2>$null |
        ForEach-Object {[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($_))})
    # marker = prima riga commento-fix significativa nel prompt context
    $mk=([regex]'(?m)^\s*//\s*(.{12,60})').Match($s.prompt).Groups[1].Value
    if($mk -and $c -match [regex]::Escape($mk)){ $verdict='ARCHIVE? (marker gia su origin/main)'; $ev="$f :: $mk" }
    elseif($f -match 'services/generation'){ $verdict='DEFER (services/generation = M1-freeze sensitive)' }
    else { $verdict='NEEDS-CLAUDE-EVAL'; $ev="$f (no marker match -> ambiguo)" }
  }
  $lines+="- ``$id`` [$src] **$verdict** -- $($s.title.Split([char]10)[0].Substring(0,[Math]::Min(70,$s.title.Length)))  | $ev"
}
$lines+="","## Manuale (non scriptabile)","- Suggestions: apri jules.google dashboard per-repo, review.","- NEEDS-CLAUDE-EVAL sopra: ping Claude per ground-truth profondo.","","## Gate","Nessuna azione auto. Eduardo: review -> approva batch (archive/respond) -> Claude esegue via API (sendMessage pre-auth riga 122; archive post §3-permission)."
Set-Content -Encoding utf8 $out ($lines -join "`n")
# reminder toast
[void][Windows.UI.Notifications.ToastNotificationManager,Windows.UI.Notifications,ContentType=WindowsRuntime]
Write-Host "DIGEST -> $out ($($sess.Count) Awaiting)"
```

### Scheduler (Eduardo one-time)

```powershell
$a=New-ScheduledTaskAction -Execute 'powershell' -Argument '-NoProfile -ExecutionPolicy Bypass -File C:\dev\codemasterdd-ai-station\scripts\jules-daily-digest.ps1'
$t=New-ScheduledTaskTrigger -Daily -At 8am
Register-ScheduledTask -TaskName 'jules-daily-digest' -Action $a -Trigger $t -Description 'ADR-0034 Option D daily Jules sessions digest (read-only)'
```

### Limiti onesti (encoded nel digest)
- Verdetti = **FIRST-PASS euristici** (marker-match). ARCHIVE? col `?` =
  candidato, NON auto-eseguito (Eduardo/Claude conferma — lezione 69%-FP).
- Suggestions: NON nel digest (browser-only). Riga manuale.
- Ambigui (no marker) → `NEEDS-CLAUDE-EVAL` → ping Claude per ground-truth.
- Script READ-ONLY: solo `GET` API + `gh api` + scrive .md locale. ZERO
  archive/sendMessage/start (quelli = Eduardo batch-approve → Claude API).

### Flusso risultante
Daily 8am → script → `docs/jules-batch/<day>-digest.md` + toast → Eduardo
apre, review (no copia-incolla dashboard) → approva azioni → Claude esegue
via API (Option D). Suggestions = check dashboard manuale quando vuole.

---

*Doc unico. Authority ADR-0034. Wiring empirico 2026-05-18. Supersede note
Jules sparse. §8 = digest automation (Eduardo installa). Update quando
endpoint archive/create verificati o API suggestions emerge.*
