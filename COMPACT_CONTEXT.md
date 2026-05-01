# COMPACT_CONTEXT

## Snapshot corrente

Data: 2026-05-01.

Stato: recovery strutturale avanzata su branch `codex/structural-reset`.

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
6. `config/system-map.yaml`
7. `docs/recovery/client-runtime-matrix.md`

## Cosa e' attivo

- Questo repo.
- Root governance.
- `PROJECT_STATE.yaml` e `config/system-map.yaml`.
- ADR e documentazione.
- Script di recovery presenti localmente, incluso `scripts/check-all.ps1`.
- Scaffold `infra/` e `apps/dogfood-ui/`, solo come codice presente.
- Dashboard `/recovery` dentro `apps/dogfood-ui`.

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

- Usare `scripts/check-all.ps1` come check pre-commit/pre-merge.
- Sul PC corretto, compilare eventualmente `config/machine-profile.local.yaml`.
- Riattivare repo esterni solo uno alla volta tramite `EXTERNAL_REPOS.md`.
- Decidere dopo merge se mantenere `apps/dogfood-ui` come dashboard recovery o
  ripristinare il dogfood runtime.
