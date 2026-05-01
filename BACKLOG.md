# BACKLOG

Backlog corrente per `SPRINT_02.md`.

Regola: se un task richiede un path esterno mancante, non e' actionable qui.
Diventa candidato di reactivation in `EXTERNAL_REPOS.md`.

## Alta priorita

- [x] **S2-01 Recovery audit** - creato `docs/recovery/2026-04-30-transplant-audit.md`.
- [x] **S2-02 External repo quarantine** - creato `EXTERNAL_REPOS.md`.
- [x] **S2-03 Governance root refresh** - file root riallineati allo scope corrente.
- [x] **S2-04 Dashboard demotion** - `STATUS_MULTI_REPO.md` reso storico/dormiente.
- [x] **S2-05 Agent surface reduction** - registry agent marcato mixed active/dormant.
- [x] **S2-06 Runtime evidence policy** - creato `docs/recovery/runtime-artifacts-policy.md`.
- [x] **S2-07 Encoding policy** - creato `docs/recovery/encoding-policy.md`.
- [x] **S2-08 Original system reconstruction** - creati `docs/recovery/original-system-intent.md` e `docs/recovery/reconnect-from-main.md`.
- [x] **S2-09 Instruction surface cleanup** - creato `AGENTS.md`, aggiunta policy instruction files, riscritto `MODEL_ROUTING.md`.
- [x] **S2-10 Merge readiness package** - creati checklist pre-merge e PR description.
- [x] **S2-11 Minimal state and anti-regression check** - creato `PROJECT_STATE.yaml`, boundary attivo/storico, e script `scripts/check-recovery-consistency.ps1`.

## Media priorita

- [x] Aggiornare `apps/dogfood-ui/README.md` per separare dogfood core da panel Dafne.
- [ ] Valutare se `infra/` resta active scaffold o viene marcato dormant.
- [ ] Aggiungere un piccolo `docs/recovery/runtime-artifacts-policy.md`.
- [ ] Aggiungere un piccolo `docs/recovery/encoding-policy.md`.
- [ ] Creare un indice dei file storici frozen.

## Bassa priorita

- [ ] Normalizzare mojibake nei file attivi dopo il reset di scope.
- [ ] Rivedere `PROMPT_LIBRARY.md`.
- [ ] Rivedere `MODEL_ROUTING.md` per un mondo post-transplant.
- [ ] Decidere sul PC giusto se OpenCode resta solo ponte di portabilita o diventa client secondario reale.
- [ ] Sul PC giusto, verificare se conviene full merge, cherry-pick o hybrid merge.
- [ ] Valutare se integrare `scripts/check-recovery-consistency.ps1` in un hook o CI leggero.
- [ ] Ridurre o archiviare `Archivio_Libreria_Operativa_Progetti/` se il repo deve diventare minimale.

## Dormant, non actionable in questa copia

- H2 dogfood cosmetic.
- H3 cp1252 wrapper monitoring.
- M5 Synesthesia privacy validation.
- Game ROSSO findings.
- Dafne voice/widget/chat work.
- AA01 proposed tasks.
- ADR-0015/0016/0017 ratification basata su dati runtime mancanti.

Questi item possono tornare attivi solo dopo reactivation o ripristino delle
evidenze mancanti.
