# ROADMAP

## Principio

La roadmap corrente non e' piu la roadmap della macchina originale. E' la
roadmap della copia trapiantata.

Obiettivo: rendere il repo portabile, coerente e utilizzabile senza dipendere da
repo fantasma o runtime non presenti.

## Fase R0 - Audit transplant

Status: done.

Output:

- `docs/recovery/2026-04-30-transplant-audit.md`
- verifica path esterni mancanti
- verifica runtime artifacts mancanti
- conteggio aree repo
- identificazione source-of-truth drift

## Fase R1 - Scope reset

Status: done.

Decisione:

- il repo governa solo se stesso;
- i repo esterni sono dormienti;
- `EXTERNAL_REPOS.md` e' il registro unico per eventuale reactivation;
- vecchi piani cross-repo restano storici.

## Fase R2 - Governance refresh

Status: done.

File da allineare:

- `README.md`
- `PROJECT_BRIEF.md`
- `COMPACT_CONTEXT.md`
- `BACKLOG.md`
- `DECISIONS_LOG.md`
- `OPEN_DECISIONS.md`
- `REFERENCE_INDEX.md`
- `MASTER_PROMPT.md`
- `STATUS_MULTI_REPO.md`

Definition of done:

- nessun file root dichiara live un path assente;
- tutti gli ADR esistenti sono indicizzati;
- `SPRINT_02.md` e' il piano attivo.

## Fase R3 - Surface reduction

Status: done.

Azioni:

- marcare agent cross-repo come dormant/requires-reactivation;
- chiarire che `apps/dogfood-ui` e `infra/` sono scaffold, non servizi live;
- lasciare `Archivio_Libreria_Operativa_Progetti/` come library frozen;
- creare policy per runtime artifacts gitignored.

## Fase R4 - Encoding and portability

Status: partly done.

Azioni:

- normalizzare solo file attivi;
- evitare rewrite globale cieco;
- aggiungere regola UTF-8 per nuovi documenti;
- tenere i log storici mojibake come materiale frozen finche non serve leggerli.
- mantenere `config/machine-profile.local.yaml` fuori da git.

## Fase R4b - Self-diagnostic structure

Status: done.

Output:

- `config/system-map.yaml`
- `config/machine-profile.example.yaml`
- `scripts/recovery-status.ps1`
- `scripts/check-all.ps1`
- `docs/recovery/client-runtime-matrix.md`
- `/recovery` in `apps/dogfood-ui`
- Dafne opt-in con `DAFNE_ENABLED=1`

## Fase R5 - Optional reactivation

Status: future.

Un repo esterno puo tornare attivo solo passando il gate in `EXTERNAL_REPOS.md`.

Possibili reactivation:

- Game, se viene clonato localmente e richiesto da Eduardo.
- Synesthesia, quando torna lavoro reale pre-esame.
- Dafne, solo sulla macchina dove esiste il workspace.
- AA01, solo se presente e se Eduardo vuole includerlo.

## Calendario

- 2026-04-30: structural recovery start.
- Next: completare Sprint 02.
- After Sprint 02: decidere se il repo resta solo governance archive o se
  riattivare moduli infra/app uno per volta.
