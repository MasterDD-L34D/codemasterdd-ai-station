# Evo-Swarm -> Game digest archive (POST-MORTEM)

> Record storico, congelato. Archiviato nell'hub codemasterdd il 2026-06-30.
> NON e' una pipeline viva: documenta un arco chiuso.

## Cos'e'

13 report prodotti da `scripts/swarm-to-game-export.py` (repo Dafne evo-swarm,
Atto 2 Scenario A "Integration drive"): distillati del `cycle-log` dello swarm in
digest destinati al Game repo. Sorgente originale (sovereign, Lenovo):
`C:\Users\edusc\Dafne\workspace\swarm\docs\exports\digest-archive\`.

- `INDEX.md` -- manifest cronologico (entry point originale verso l'hub).
- `EXPORT-FOR-GAME-REPO-<data>.md` -- digest completo per il Game team (TL;DR + cross-ref L9 + coverage gap).
- `PENDING-GAME-ISSUE-<data>.md` -- body issue pronto da copia-incollare (mai auto-creato).
- `PENDING-ATTO2-HEALTH-<data>.md` -- flag salute (emesso a 0 cicli / repo dormant).

## Perche' e' archiviato qui (non nel repo d'origine)

Il remote `MasterDD-L34D/evo-swarm` e' **ARCHIVED + PRIVATE** (`gh repo view`
`isArchived=true`, pushedAt 2026-06-22). Push -> `403`: il repo d'origine non
puo' piu' contenere ne' consegnare questi report. L'`INDEX.md` si rivolge gia'
esplicitamente all'hub codemasterdd come punto d'ingresso d'analisi. codemasterdd
(public, pushabile) = home durevole del record.

## Perche' la pipeline e' CHIUSA (3 assi, verificati 2026-06-30)

1. **Decisione 013** (evo-swarm #130, 2026-06-20): lo "swarm-as-production-accelerator"
   e' stato **FALSIFICATO** (12 artifact attraverso i gate L1/L3 -> 11 rejected,
   91.7% hallucination, kill-criterion raggiunto). Esito: swarm-generator archiviato,
   `verify-swarm-claims` promosso a linter standalone. Vedi memory `project_swarm_verification`.
2. **Traiettoria a zero**: picco 2026-04-27 (432 cicli significativi / 2 match diretti)
   -> **0 cicli per 8+ settimane** -> 2026-06-30 ancora 0/0. La pipeline non produce
   artifact integrabili dal 04-27; solo coverage-gap (20 biomi di `biomes_expansion.yaml`
   mai discussi = input-candidati, non deliverable).
3. **Routine non schedulata**: nessun task `evo-swarm-weekly-digest` registrato su
   CODEMASTERDD (`Get-ScheduledTask` -> assente). I 13 file hanno tutti mtime 2026-06-30
   = rigenerati a mano in quella data, NON accumulati da un cron.

**Stato finale**: CHIUSA. Nessun re-point (contraddirebbe Decisione 013, gia' ratificata).
Segnale residuo = 20 coverage-gap biomi, moot finche' lo swarm resta parked (e resta).

## Provenienza / encoding

Copia fedele frozen: emoji, frecce unicode, em-dash e accenti italiani sono
preservati as-is (i `.md` sono esenti dall'ASCII-guard CI di questo repo, scope
`.ps1/.sh/.py/.js/.json/.yml`). Nessuna riscrittura del contenuto storico.
