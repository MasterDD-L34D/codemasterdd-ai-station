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

## Cosa è AUTO (residuo deep-metrics CHIUSO)

| Segnale | Stato | Fonte |
|---|---|---|
| Pillar **verdict** (bootstrap/…/verdetto) | ✅ AUTO | Game `tools/sim/pillar-baseline.json` (raw) |
| Baseline **samples** count | ✅ AUTO | idem |
| Baseline **updated_at** | ✅ AUTO | idem |
| Ultimo `ai-sim-nightly` **run conclusion** + data + link | ✅ AUTO | GitHub REST pubblica |
| Deep per-pilastro (P3 promos / P4 4-layer / P6 rewind% / OD-024 firing% / OD-026 skiv+biome-focus / perf p95) | ✅ AUTO | Game `tools/sim/playtest2-latest.json` (raw) |

**Residuo CHIUSO (Game `feat/playtest2-deep-metrics-digest`)**: il
`metrics.json` completo resta nell'artifact auth-gated (non raw-fetchabile,
invariato), ma la nightly Game ora ne **distilla un digest
board-consumabile** (`tools/sim/playtest2-digest.py` →
`tools/sim/playtest2-latest.json`) e lo committa **nello STESSO
baseline-update PR** di `pillar-baseline.json` (stesso branch
`auto/playtest2-baseline-<date>`, stesso guard di idempotenza/bootstrap —
churn solo-timestamp soppresso, niente PR se nulla cambia). codemasterdd
`tools/playtest2-board-sync.sh` raw-fetcha quel digest (sezione 2b, **no
cross-repo auth**) e arricchisce il blocco AUTO-SYNC con la riga
per-pilastro reale.

**Onestà preservata**:
- Game non ha ancora prodotto/committato il digest (bootstrap, o `main`
  vecchia) → fetch 404 → lo script **degrada al verdict-only** con una
  frase esplicita _"Deep per-pillar metrics: not yet published by Game
  (digest absent / bootstrap)"_. Mai crash, mai fabbricazione.
- Campo del digest assente (analyzer non l'ha prodotto) → reso come
  `n/a`, mai inventato.
- Digest identico fra run → blocco AUTO-SYNC identico (idempotente; il
  solo refresh data resta comportamento pre-esistente dello script,
  gated dal git-diff del workflow = no-spam PR).

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
5. **Digest deep-metrics 404 / assente (Game bootstrap o `main`
   vecchia)** → sezione 2b lascia `pillar_line` vuoto → blocco AUTO-SYNC
   degrada al verdict-only con frase esplicita, mai crash — verificato
   contro Game/main live (digest non ancora committato).
6. **Digest presente ma campo nullo** (analyzer non l'ha prodotto) →
   reso `n/a`, mai fabbricato — verificato con digest bootstrap-empty.

## Cross-link

- Board: `docs/cross-repo/EXECUTION-BOARD.md`
- Pattern: OD-042-A (skiv-monitor raw-fetch) →
  `docs/runbook/skiv-monitor-blocked-pr-fix.md`
- Producer: Game `.github/workflows/ai-sim-nightly.yml` Envelope-B B3/B4
