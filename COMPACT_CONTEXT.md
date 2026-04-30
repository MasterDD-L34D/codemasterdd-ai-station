# COMPACT_CONTEXT

## Snapshot corrente

Data: 2026-04-30.

Stato: recovery strutturale in corso.

Questa copia del repo non e' la workstation originale documentata nello storico.
I path esterni originali non esistono qui, quindi la governance cross-repo e'
stata sospesa.

## Stato Git

- Branch recovery: `codex/structural-reset`.
- HEAD di partenza audit: `ff3e91e`.
- `main` risultava allineato a `origin/main`.
- `AGENTS.md` era untracked all'inizio della recovery.

## Fonte corrente

Per questa fase leggere:

1. `docs/recovery/2026-04-30-transplant-audit.md`
2. `EXTERNAL_REPOS.md`
3. `SPRINT_02.md`
4. `BACKLOG.md`
5. `DECISIONS_LOG.md`

## Cosa e' attivo

- Questo repo.
- Root governance.
- ADR e documentazione.
- Script presenti localmente.
- Scaffold `infra/` e `apps/dogfood-ui/`, solo come codice presente.

## Cosa e' dormiente

- Evo-Tactics / Game.
- Synesthesia.
- Dafne swarm / evo-swarm.
- AA01.
- Dogfood runtime data non presente.
- Promptfoo result non presente.
- Vecchi path `C:\dev\...` e `C:\Users\edusc\...`.

## Problemi principali

1. Documenti root divergenti sullo stato reale.
2. ADR-0020 esistente ma non indicizzato nei vecchi file.
3. `MASTER_PROMPT.md` precedente riportava stato obsoleto.
4. `STATUS_MULTI_REPO.md` si comportava da dashboard live senza repo presenti.
5. Runtime evidence gitignored assunta come disponibile.
6. Molti file hanno mojibake; evitare riscritture globali cieche.

## Decisione operativa

Non cancellare storia nel primo pass. Ridurre la superficie attiva e marcare i
satelliti come dormienti.

## Prossimi passi

- Chiudere refresh dei file root.
- Demuovere `STATUS_MULTI_REPO.md` a storico.
- Marcare agent cross-repo come dormant/requires-reactivation.
- Definire export/import per runtime artifacts se serviranno in futuro.
