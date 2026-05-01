# CodeMasterDD AI Station

Repository di governance, documentazione e scaffold infrastrutturale per una
workstation AI locale.

## Stato corrente

Questa copia e' in fase di **structural recovery** dopo un trasporto su una
macchina diversa da quella originale.

Fonte di recupero corrente:

- `PROJECT_STATE.yaml`
- `docs/recovery/2026-04-30-transplant-audit.md`
- `docs/recovery/original-system-intent.md`
- `docs/recovery/reconnect-from-main.md`
- `docs/recovery/active-vs-historical-boundary.md`
- `docs/recovery/pre-merge-checklist.md`
- `docs/recovery/pr-description-structural-reset.md`
- `docs/recovery/client-runtime-matrix.md`
- `SPRINT_02.md`
- `EXTERNAL_REPOS.md`
- `config/system-map.yaml`

## Regola madre

Questo repo governa solo se stesso.

I repo esterni citati nello storico restano dormienti finche non vengono
riattivati con verifica esplicita. Vedi `EXTERNAL_REPOS.md`.

## Scope attivo

Attivo in questa copia:

- struttura del repo
- mappa di sistema in `config/system-map.yaml`
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
2. `PROJECT_STATE.yaml`
3. `PROJECT_BRIEF.md`
4. `COMPACT_CONTEXT.md`
5. `BACKLOG.md`
6. `SPRINT_02.md`
7. `DECISIONS_LOG.md`
8. `EXTERNAL_REPOS.md`

Agent/client entry points:

- `AGENTS.md` for Codex.
- `CLAUDE.md` for Claude/OpenCode-compatible clients.
- `MASTER_PROMPT.md` for browser or non-repo contexts.

`JOURNAL.md` e `docs/sessions/` sono storia. Utili per audit, non per decidere
lo stato operativo corrente senza verifica.

## Config e diagnostica

- `config/system-map.yaml` descrive quali moduli sono active, scaffold,
  historical o dormant.
- `config/machine-profile.example.yaml` e' il template per un profilo macchina
  locale. Il profilo reale va creato come `config/machine-profile.local.yaml` e
  resta gitignored.
- `scripts/recovery-status.ps1` mostra branch, tool disponibili, path esterni e
  runtime evidence presenti.
- `scripts/check-all.ps1` esegue il check di recovery, sanity YAML, sintassi
  Python e `git diff --check`.
- `apps/dogfood-ui/` include una pagina `/recovery` per vedere lo stato
  strutturale dal browser. Il pannello Dafne resta disabilitato finche non si
  imposta esplicitamente `DAFNE_ENABLED=1`.

## ADR

Il repo contiene 21 ADR in `docs/adr/`.

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
- ADR-0021: structural recovery and external repo quarantine

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

## Recovery check

Run before committing recovery changes:

```powershell
.\scripts\check-recovery-consistency.ps1
.\scripts\check-all.ps1
git diff --check
```
