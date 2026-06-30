# Digest Archive — evo-swarm → Game (manifest per hub codemasterdd)

> **Cosa e'**: archivio di tutti i report accumulati dalla routine settimanale `evo-swarm-weekly-digest`
> (Atto 2 Scenario A "Integration drive"). Distillati degli output swarm utili al Game repo.
> **Per l'hub codemasterdd**: questo file e' il punto d'ingresso. Analizza i report qui sotto per
> valutare salute pipeline swarm→Game e decidere se la routine va disabilitata/ri-puntata.

**Generato**: 2026-06-30 su CODEMASTERDD (hub locale .10).
**Path archivio**: `C:\Users\edusc\Dafne\workspace\swarm\docs\exports\digest-archive\`
**Source generatore**: `scripts/swarm-to-game-export.py` (input: `camel-agents/artifacts/cycle-log.md`).

---

## ⚠️ Stato critico per l'hub

- **Remote GitHub `MasterDD-L34D/evo-swarm` ARCHIVIATO / read-only** (confermato `gh repo view` isArchived=true, 2026-06-30). Push → `403`. La routine non puo' piu' aprire PR. I digest dal 2026-06-30 esistono **solo in locale**.
- **Trend collasso attivita'**: dopo 2026-04-27 lo swarm e' parked → 4 settimane consecutive a **0 cicli significativi** e **0 match diretti**. La pipeline produce solo coverage-gap (input candidati), nessun artifact integrabile.
- **Decisione pendente** (Eduardo): disabilitare la scheduled-task `evo-swarm-weekly-digest` oppure ri-puntare a nuovo remote.

---

## Indice report (ordine cronologico)

| Data | File | Finestra | Cicli signif. | Match diretti | Coverage gap | Note |
|------|------|----------|---------------|---------------|--------------|------|
| 2026-04-25 | `EXPORT-FOR-GAME-REPO-2026-04-25.md` | tutto cycle-log | 353 | — | — | bootstrap, full dump |
| 2026-04-25 | `EXPORT-FOR-GAME-REPO-2026-04-25-DELTA.md` | dal 04-25 | 33 | — | — | delta-only |
| 2026-04-25 | `EXPORT-FOR-GAME-REPO-2026-04-25-FINAL.md` | dal 04-22 | 391 | 2 | 50 | export consolidato |
| 2026-04-27 | `EXPORT-FOR-GAME-REPO-2026-04-27.md` | 04-20→04-27 | 432 | 2 | 50 | picco attivita' |
| 2026-04-27 | `PENDING-GAME-ISSUE-2026-04-27.md` | 04-20→04-27 | 432 | 2 | — | issue draft |
| 2026-05-07 | `EXPORT-FOR-GAME-REPO-2026-05-07.md` | 04-30→05-07 | 0 | 0 | 50 | swarm dormant |
| 2026-05-07 | `PENDING-GAME-ISSUE-2026-05-07.md` | 04-30→05-07 | 0 | 0 | 50 | issue draft |
| 2026-05-07 | `PENDING-ATTO2-HEALTH-2026-05-07.md` | 04-30→05-07 | 0 | — | — | ⚠️ health flag: repo dormant 11gg |
| 2026-05-27 | `EXPORT-FOR-GAME-REPO-2026-05-27.md` | 05-20→05-27 | 0 | 0 | 20 | swarm parked |
| 2026-05-27 | `PENDING-GAME-ISSUE-2026-05-27.md` | 05-20→05-27 | 0 | 0 | 20 | issue draft |
| 2026-06-30 | `EXPORT-FOR-GAME-REPO-2026-06-30.md` | 06-23→06-30 | 0 | 0 | 20 | solo locale (remote archiviato) |
| 2026-06-30 | `PENDING-GAME-ISSUE-2026-06-30.md` | 06-23→06-30 | 0 | 0 | 20 | solo locale |

## Tipi di file

- **`EXPORT-FOR-GAME-REPO-<data>.md`** — digest completo: TL;DR per Game team, cross-ref L9 (match diretti + coverage gap), proposte specialist pending.
- **`PENDING-GAME-ISSUE-<data>.md`** — body issue pronto da copia-incollare in `gh issue create --repo MasterDD-L34D/Game` (mai auto-creato).
- **`PENDING-ATTO2-HEALTH-<data>.md`** — flag salute Atto 2 (emesso quando 0 cicli / repo dormant).

---

## Cosa deve analizzare l'hub (focus suggerito)

1. **Decidere fate routine**: dato 4 settimane consecutive a 0 cicli + remote archiviato, la pipeline swarm→Game e' di fatto ferma. Disabilitare o ri-puntare.
2. **Coverage gap persistente**: 20 biomi `biomes_expansion.yaml` mai discussi dallo swarm (ferrous-badlands, cinder-dunes, saltglass-flats, basalt-grottos, zephyr-steppe + 15). Candidati input se si rilancia lo swarm.
3. **Confronto picco vs ora**: 2026-04-27 = 432 cicli / 2 match; 2026-06-30 = 0/0. Diagnosi del perche' lo swarm e' parked (vedi STATUS.md "swarm PARKED").
