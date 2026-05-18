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
