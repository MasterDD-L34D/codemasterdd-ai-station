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
| API read (`GET sessions/sources/activities`) | ✅ sì (Bash curl generico) | nessuna modifica |
| API `sendMessage` / archive / create (generativo) | 🔶 **per-ciclo, NON standing** | **Modello ADR-0034:15**: l'autorizzazione = **batch-approve esplicito Eduardo in chat per ciclo** (rende le azioni user-authorized → classifier OK), **NON** una standing entry in `settings.json`. Una standing `autoMode.allow` = la "broad-rule" che l'ADR ha **esplicitamente rigettato** (least-privilege: zero privilegio external-write permanente). |
| Browser jules.google (suggestions discovery) | ❌ classifier-blocked | Suggestions **restano azione manuale Eduardo** (API non le copre; permission browser autonoma = start-from-suggestion generativo = SDMG-rejected, NON pre-staged qui). |
| Skill `update-config` / edit `settings.json` (self-mod permessi) | ❌ barrato by-design | **SOLO Eduardo edita `settings.json` a mano** — l'agent NON può auto-concedersi guardrail (classifier blocca correttamente, allineato SDMG/ADR-0034). |

> **⚠️ P0-3 (harsh-reviewer cluster 2026-05-18, adottato non difeso).** Le 2
> standing entries archive/create aggiunte 2026-05-18 a `settings.json:123-124`
> **contraddicono ADR-0034:15** ("NON standing permission-rule"). Vanno
> **rimosse da Eduardo** (revert manuale; il classifier blocca il self-mod
> dell'agent, correttamente). Anche riga 122 (sendMessage, standing) è stessa
> classe → decisione consistenza Eduardo. Modello corretto = approve in chat
> per ciclo. Finché non risolto: exec del batch = manuale Eduardo.

**Principio**: l'agent **documenta** i pattern + **drafta** il batch; Eduardo
**autorizza per ciclo in chat** (= il throttle generativo Option D). Nessun
privilegio external-write standing. Permesso harness ≠ policy: la policy
(batch-approve per ciclo) è l'unico controllo, e non va sostituita da una
broad-rule in settings.json.

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

### Script — canonico: `scripts/jules-daily-digest.ps1` (v4.1, PR #172)

**NON incollare uno script inline qui.** Lo script canonico vive in
`scripts/jules-daily-digest.ps1` (commit su PR #172), già installato
(Windows ScheduledTask `jules-daily-digest`, daily 8am). Read-only:
solo `GET` Jules API + `gh` + scrive `docs/jules-batch/<day>-digest.md`.
ZERO mutazione Jules.

> **Storia euristica (SDMG/Protocol-7 — falsificata esternamente,
> adottata-non-difesa; lezione, NON vittoria):**
> - v1 prompt-marker `File:`+commento (era embeddata qui) / v2 substring →
>   **FALSIFICATE**. harsh-reviewer REJECT-cluster 3×P0 + asse indipendente
>   Jules-activities: i "marker" sono spesso il commento di **contesto
>   pre-esistente** (dal Codex/PR originale), non prova che Jules abbia
>   shippato. v3.1 sbagliava 4/8 incl. 3 false-ARCHIVE; "validated 8/8"
>   era **circolare** (stessa fonte gh-api per euristica e ground-truth).
> - **v4.1 (canonico)** = segnale **indipendente** a 2 fonti: Jules
>   session → linked GitHub PR → `{merge-state, files}`. `MERGED` &
>   nessun file freeze = ARCHIVE; `CLOSED`/`OPEN`/no-PR = ACTIONABLE
>   (non shippato); qualunque file PR sotto `services/generation|
>   services/rules|apps/backend/services/combat` = **DEFER**; no-PR +
>   File-hint non-parsabile = **DEFER** (conservativo: il freeze-miss è
>   la direzione pericolosa). false-ARCHIVE **strutturalmente impossibile**
>   (richiede una PR davvero merged). API-fetch-fail = digest ERROR
>   esplicito (non no-op silenzioso). 8/8 corretto vs ground-truth
>   indipendente 2026-05-18.
> - Vedi header dello script per il changelog completo v1→v4.1.

### Limiti onesti
- Il digest è un **ENUMERATORE advisory**, NON un motore di verdetti
  auto-eseguiti. I verdetti alimentano il **batch Claude-drafted** che
  Eduardo approva per ciclo (ADR-0034 Option D). Zero auto-exec.
- Suggestions: NON nel digest (browser-only, no API). Riga manuale Eduardo.
- ACTIONABLE / IN-PROGRESS / AMBIGUOUS → Claude ground-truth profondo
  (activities/diff) in fase di batch-draft.
- Generativo (archive/respond/start) = Eduardo approve in chat per ciclo,
  **non** standing settings entry (P0-3, §3).

### Flusso risultante
Daily 8am → script → `docs/jules-batch/<day>-digest.md` + toast → Eduardo
apre, review (no copia-incolla dashboard) → approva azioni → Claude esegue
via API (Option D). Suggestions = check dashboard manuale quando vuole.

---

*Doc unico. Authority ADR-0034. Wiring empirico 2026-05-18. Supersede note
Jules sparse. §8 = digest automation (Eduardo installa). Update quando
endpoint archive/create verificati o API suggestions emerge.*
