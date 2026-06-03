# Runbook — Jules session triage via CLI (read-only, ground-truth)

> Metodo PROVATO 2026-05-18 (gate-su-successo: CLI list+pull + ground-truth
> 8/8 completato). Rimpiazza il browser-scrape (fragile). Per ADR-0033:
> analisi read-only OK; **close/continue/respond su jules.google = Eduardo-
> explicit** (Claude NON muta sessioni Jules esterne — lezione backfire
> #2294/#2313).

## Precondizioni (one-time)

- `@google/jules` CLI installato (npm global, binary `~/AppData/Roaming/npm/jules`)
- `JULES_API_KEY` in `~/.config/api-keys/keys.env`
- **`jules login`** eseguito da Eduardo (OAuth Google interattivo, ~30s; token
  cached `~/.jules`, persistente — NON delegabile a Claude per design)

## Procedura (Claude, read-only)

```bash
set -a; source ~/.config/api-keys/keys.env 2>/dev/null; set +a

# 1. Enumera TUTTE le sessioni (no inferenza, no browser)
jules remote list --session

# 2. Filtra il set da triagare (es. Awaiting User Feedback su un repo)
jules remote list --session | grep "MasterDD-L34D/Game " | grep -i "Awaiting"

# 3. Per OGNI sessione del set: contenuto pieno (diff/task)
jules remote pull --session <ID>            # NON --apply (read-only)
```

**Solo comandi read-only**: `remote list`, `remote pull` (senza `--apply`).
VIETATI in triage: `remote new`, `--apply`, qualunque close/respond → quelli
sono azione Eduardo su jules.google.

## Verdict-logic per sessione (ground-truth obbligatorio)

Per ogni `pull`, NON fidarsi del task-description. Estrarre il diff, poi
**ground-truth vs `origin/main`** (gh api, non clone stale):

```bash
gh api repos/<owner>/<repo>/contents/<file> --jq '.content' | base64 -d \
  | grep -n "<marker-univoco-del-fix>"
```

| Esito ground-truth | Verdetto |
|--------------------|----------|
| Fix/refactor **già presente** su origin/main | **CLOSE** (rework, no-op). NON falso-positivo: verificato, ≠ 69% storico dashboard-guess |
| Codice target **ancora pre-fix** + diff sano | **CONTINUE** (reale) |
| Diff include scope-creep non-correlato (es. docs date-bump) | flag noise; verdetto sul fix-core |
| Path sensibile (`services/generation/`, hard-gate, freeze-active) | **Eduardo-review**, mai auto |
| Premessa task falsa (grep smentisce) | **CLOSE + flag premise-false** |

> **R3-bis (ADR-0034 addendum 2026-05-18, vincolante).** Verdetto
> `CLOSE`/already-shipped/task-moot → **archive-only via API, MAI
> `sendMessage`** (nessun messaggio di cortesia "superseded": risveglia
> la sessione = vettore backfire #2294/#2313, zero valore su sessione
> moot — evidenza empirica ciclo 1, L-2026-05-031). `sendMessage` SOLO
> su sessione genuinamente-open per scope-correction. Sequenza:
> archive PRIMA; post-archive ri-GET + conferma `archived=true`; se
> torna attiva → R4 stop+flag, NON ri-messaggiare.

## Output

Tabella per-sessione: `ID | task | ground-truth | verdetto`. Consegna a
Eduardo. **Eduardo agisce** su jules.google (close/continue). Claude stop.

## Leva primaria (ADR-0033, ricorrente)

Il triage e' il residuo: la leva PRIMARIA resta **throttle Jules org-level**
(Eduardo, jules.google) — taglia il ~41% rumore alla fonte. Il pattern
osservato 2026-05-18 (7/8 Awaiting = rework su codice gia' shippato) e'
esattamente il rumore che il throttle previene. Triage CLI = mitigazione,
non cura.

## Caso studio 2026-05-18 (validazione metodo)

8 sessioni Game "Awaiting User F": 7 ground-truth = gia'-shippate (W8L,
Codex#2031/#2034/W5.5, dead-band, GSD-pre-enrich, code-health species_builder)
-> CLOSE. 1 (code-health orchestrator.py) = non applicata, path sensibile
-> Eduardo-review. Browser-scrape aveva visto solo 5+inferenza (miss);
CLI ha dato 8/8 completo. Metodo CLI = canonical d'ora in poi.

## Daily digest cron (G3, registrato 2026-06-03)

L'enumeratore READ-ONLY `scripts/jules-daily-digest.ps1` (heuristic v4.1:
session -> linked-PR state+files, independent dal prompt) gira in automatico
via Windows Scheduled Task `jules-daily-digest` (daily 09:30, `-StartWhenAvailable`),
scrivendo `docs/jules-batch/<day>-digest.md`. Usa REST `x-goog-api-key` (no OAuth,
addendum ADR-0035 2026-06-02) + `gh pr view`.

- **Caveat reliability (LogonType Interactive)**: il task parte SOLO quando l'owner
  (Vgit) e' loggato interattivamente; `-StartWhenAvailable` recupera i miss da
  PC-spento/sospeso, NON da utente-disconnesso/lock-screen. NON e' un cron unattended
  puro -- best-effort when-logged-in. Il filename date-stamped rende il miss osservabile
  (nessun `<day>-digest.md` nuovo = non girato; resta il file del giorno prima). Per un
  unattended vero servirebbe un principal con credenziali memorizzate (admin) --
  scartato per tenere il "no admin".

- **Registrazione / handoff (idempotente)**: `scripts/fleet/register-jules-digest-task.ps1`
  (re-run = re-register `-Force`; `-Unregister` per rimuovere). No elevazione admin
  (current-user, RunLevel Limited).
- **Ownership = SINGLE-OWNER, NON entrambi i PC.** Due cloni che scrivono lo stesso
  `<day>-digest.md` = drift cross-fleet (due working-tree divergenti + doppio commit).
  **Owner attuale = Ryzen (DESKTOP-T77TMKT)** -- PC attivo del loop dispatch/triage,
  gh authed, JULES_API_KEY presente. Handoff a Lenovo: `-Unregister` su Ryzen PRIMA,
  poi register su Lenovo. Mai registrato su due PC insieme.
- **Prereq sull'owner**: `JULES_API_KEY` in `~/.config/api-keys/keys.env` + gh authed
  (il segnale a 2 sorgenti dello stato-PR). Taxonomy fallimenti (precisa): se fallisce
  il *lookup PR via gh* -> quella sessione degrada a AMBIGUOUS (no crash); se fallisce
  la *sessions API* (key assente/invalida) -> il digest e' un file ERROR esplicito con
  exit 1 (MAI empty-set silenzioso); path no-PR -> DEFER/AMBIGUOUS senza usare gh.
- **Gate (ADR-0034 Option D)**: il digest e' advisory, ZERO auto-exec. Eduardo/Claude
  fanno triage ground-truth (sezioni sopra) sul set ACTIONABLE/IN-PROGRESS/AMBIGUOUS;
  il generativo (archive/respond/start) resta batch-approve Eduardo.
- **QG Step-1 (2026-06-03)**: sandbox-run su target throwaway (artifact + encoding
  UTF-8-no-BOM verificati, non solo il log) PRIMA del register; poi run-once del task
  reale (`LastTaskResult 0x0`, digest reale prodotto no-BOM). Anti-pattern #9 onorato.
