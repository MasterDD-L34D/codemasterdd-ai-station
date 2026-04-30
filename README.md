# CodeMasterDD AI Station

Repository di governance, documentazione e scaffold infrastrutturale per una
workstation AI locale.

## Stato corrente

Questa copia e' in fase di **structural recovery** dopo un trasporto su una
macchina diversa da quella originale.

Fonte di recupero corrente:

- `docs/recovery/2026-04-30-transplant-audit.md`
- `docs/recovery/original-system-intent.md`
- `docs/recovery/reconnect-from-main.md`
- `docs/recovery/pre-merge-checklist.md`
- `docs/recovery/pr-description-structural-reset.md`
- `SPRINT_02.md`
- `EXTERNAL_REPOS.md`

## Regola madre

Questo repo governa solo se stesso.

I repo esterni citati nello storico restano dormienti finche non vengono
riattivati con verifica esplicita. Vedi `EXTERNAL_REPOS.md`.

## Scope attivo

Attivo in questa copia:

- struttura del repo
- ADR e indice decisionale
- documentazione di setup e recovery
- script presenti nel repo
- scaffold `infra/` e `apps/dogfood-ui/`, solo come codice locale verificabile
- archivio storico, come riferimento

Dormiente in questa copia:

- Evo-Tactics / Game
- Synesthesia
- Dafne swarm / evo-swarm
- AA01
- runtime logs, DB SQLite, promptfoo outputs e backup non presenti

## Fonti principali

Leggere in questo ordine:

1. `docs/recovery/2026-04-30-transplant-audit.md`
2. `PROJECT_BRIEF.md`
3. `COMPACT_CONTEXT.md`
4. `BACKLOG.md`
5. `SPRINT_02.md`
6. `DECISIONS_LOG.md`
7. `EXTERNAL_REPOS.md`

Agent/client entry points:

- `AGENTS.md` for Codex.
- `CLAUDE.md` for Claude/OpenCode-compatible clients.
- `MASTER_PROMPT.md` for browser or non-repo contexts.

`JOURNAL.md` e `docs/sessions/` sono storia. Utili per audit, non per decidere
lo stato operativo corrente senza verifica.

## ADR

Il repo contiene 20 ADR in `docs/adr/`.

Le decisioni piu importanti per la recovery sono:

- ADR-0001: strategia AI sovereign
- ADR-0008: Aider whole format silent-corruption
- ADR-0011: commit governance cross-agent
- ADR-0014: timeline Fase 6 compressa
- ADR-0015: budget decision full-sovereign, ancora Proposed
- ADR-0016: constraint-count routing, ancora Proposed
- ADR-0017: UI + observability stack, validated-live storico ma non verificato qui
- ADR-0018: agent readiness protocol
- ADR-0019: Dafne process persistence, storico/dormiente qui
- ADR-0020: silent-fail Python guardrail

## Runtime evidence

Questa copia non contiene alcuni artefatti runtime citati nello storico:

- `logs/aider-delegation-2026-04.md`
- `apps/dogfood-ui/data/dogfood.sqlite`
- `results/promptfoo-smoke.json`
- backup sensibili

Questi file sono ignorati o non presenti. Non usarli come fonte di verita fino a
quando non vengono ripristinati o rigenerati localmente.

## Convenzione

Documentazione progetto in italiano.
Codice, identifier e commit message in inglese.
