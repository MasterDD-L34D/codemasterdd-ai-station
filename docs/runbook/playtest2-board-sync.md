---
id: runbook-playtest2-board-sync
title: Runbook — OD-044 playtest#2 board auto-sync
type: runbook
status: active
created: 2026-05-17
owner: master-dd
language: it
tags: [runbook, cross-repo, automation, od-044, od-042-a, ci]
related: [docs/cross-repo/EXECUTION-BOARD.md, .github/workflows/playtest2-board-sync.yml, tools/playtest2-board-sync.sh]
---

# Runbook — OD-044 playtest#2 board auto-sync

> **Scopo**: chiude il gap **B4 manual-handoff** di OD-044. La riga
> `| **playtest#2 automation (OD-044)** |` in
> `docs/cross-repo/EXECUTION-BOARD.md` ora si auto-aggiorna via PR
> schedulata, non più sync manuale.

## Perché esiste

Game `.github/workflows/ai-sim-nightly.yml` Envelope-B **B4** lasciò il
board-sync come **manual-handoff onesto**: il `GITHUB_TOKEN` del workflow
Game è repo-scoped a Game e **non può** aprire PR cross-repo verso
codemasterdd. Il `GITHUB_TOKEN` di codemasterdd, invece, può PR
codemasterdd. Quindi automatizziamo **dal lato codemasterdd**, tirando il
segnale di Game in sola lettura.

## Pattern (OD-042-A, non reinventato)

Cross-repo data-flow senza cross-repo auth = **il consumer raw-fetcha il
file git-committato del producer**. Game committa
`tools/sim/pillar-baseline.json` su `Game/main` via il suo
baseline-update PR (Envelope-B B3). codemasterdd lo legge via
`raw.githubusercontent.com` + legge la conclusione dell'ultimo run
`ai-sim-nightly` via REST API pubblica (repo pubblico → nessun PAT).

## Cosa è AUTO vs RESIDUO ONESTO

| Segnale | Stato | Fonte |
|---|---|---|
| Pillar **verdict** (bootstrap/…/verdetto) | ✅ AUTO | Game `tools/sim/pillar-baseline.json` (raw) |
| Baseline **samples** count | ✅ AUTO | idem |
| Baseline **updated_at** | ✅ AUTO | idem |
| Ultimo `ai-sim-nightly` **run conclusion** + data + link | ✅ AUTO | GitHub REST pubblica |
| `metrics.json` deep (p3_promotions / p4_psicologico / p6_fairness / od024_interoception / od026_atlas / performance) | ❌ **RESIDUO** | solo nell'**artifact** Game (auth-gated, non raw-fetchabile) |

**Residuo onesto**: l'analyzer Game emette `metrics.json` (chiavi:
summary, p3_promotions, p4_psicologico, p6_fairness, od024_interoception,
od026_atlas, performance) **solo dentro l'artifact** del workflow Game.
Gli artifact non sono leggibili cross-repo senza auth. Quindi le metriche
per-pilastro **non** sono sincronizzate — non vengono fabbricate.

**TODO sblocco residuo**: Game committa `metrics.json` (o un estratto
stabile) a un path/branch noto (es. `docs/playtest/playtest-2-metrics.json`
su `main`, come fa già con `pillar-baseline.json`). Allora estendere
`tools/playtest2-board-sync.sh` per raw-fetchare anche quel file e
arricchire il blocco AUTO-SYNC con le 7 dim. Finché Game non committa
nulla di consumabile in più, il valore reale resta: verdict + samples +
run status/data/link auto-refreshati + questo runbook chiude il knowledge
gap.

## Come funziona

- Workflow: `.github/workflows/playtest2-board-sync.yml`
  - `schedule: cron '0 4 * * 1'` (lun 04:00 UTC, dopo i nightly Game
    dom/lun) + `workflow_dispatch`.
  - `permissions: contents:write + pull-requests:write` (token
    codemasterdd, pienamente autorizzato a PR codemasterdd).
- Script: `tools/playtest2-board-sync.sh`
  - Raw-fetcha `pillar-baseline.json` + REST run conclusion.
  - Rigenera SOLO il blocco fra i marker
    `<!-- AUTO-SYNC:playtest2 BEGIN -->` / `END` nella riga OD-044.
  - La prosa umana della riga **non** viene mai toccata.
- Idempotenza / no-spam:
  - Se il segnale è identico → zero diff → **nessun PR** (no spam).
  - Se Game irraggiungibile / privato / 404 / network-fail → script
    `exit 0` **no-op** (lo schedule non va mai rosso).
- Sicurezza:
  - Apre un PR, **non** auto-merge. Lo merge-a un umano / merge-cron.
  - Nessun indebolimento branch-protection, nessun `--admin`.

## Operazioni

**Trigger manuale**:
`gh workflow run playtest2-board-sync.yml --repo MasterDD-L34D/codemasterdd-ai-station`

**Verifica locale dello script**:
```bash
bash tools/playtest2-board-sync.sh
git diff docs/cross-repo/EXECUTION-BOARD.md
# diff presente = ci sarebbe un PR ; nessun diff = no-op idempotente
```

**Branch PR**: `auto/playtest2-board-sync-<YYYY-MM-DD>`. Re-run stesso
giorno → `--force-with-lease` aggiorna il PR esistente, non ne apre uno
nuovo.

## Edge case coperti (Quality Gate Step 2)

1. **Game data irraggiungibile / network-fail** → `curl` fallisce →
   script `exit 0` no-op, board invariata, schedule verde.
2. **Riga OD-044 già current (stesso segnale)** → patch produce zero
   diff → nessun PR (no-spam) — verificato.
3. **Game repo privato / 404** → JSON vuoto/non-parsabile → branch
   "baseline unreachable" → no-op `exit 0` — verificato (bad owner +
   host non risolvibile).
4. **Marker riga OD-044 assente** → patcher Python `exit 0`, no-op.

## Cross-link

- Board: `docs/cross-repo/EXECUTION-BOARD.md`
- Pattern: OD-042-A (skiv-monitor raw-fetch) →
  `docs/runbook/skiv-monitor-blocked-pr-fix.md`
- Producer: Game `.github/workflows/ai-sim-nightly.yml` Envelope-B B3/B4
