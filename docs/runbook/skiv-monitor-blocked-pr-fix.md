---
id: runbook-skiv-monitor-blocked-pr-fix
title: Runbook — fix loop skiv-monitor PR BLOCKED (Game/main)
type: runbook
status: active
created: 2026-05-16
owner: master-dd
language: it
tags: [runbook, ci, branch-protection, skiv-monitor, game, od-041, security]
related: [docs/cross-repo/EXECUTION-BOARD.md]
---

# Runbook — fix loop skiv-monitor PR BLOCKED

## Sintomo

`Game/` PR #2257 (`auto/skiv-monitor-update` → `main`, bot
github-actions, cron 4h) resta **MERGEABLE / BLOCKED** indefinitamente.
Si rigenera ogni 4h → debito ricorrente permanente.

## Diagnosi (verificata 2026-05-16, scope-limitata)

- Review: **APPROVED** (master-dd, submit in-scope PAT). ✅ soddisfatta.
- Branch up-to-date: ✅.
- Status checks riportati sul branch bot: **0**.
- Stato: `MERGEABLE/BLOCKED` persistente.
- Branch-protection `main` = **classic** (rulesets API vuota); dettaglio
  non leggibile con fine-grained PAT OD-041 (manca permesso
  Administration — esclusione by-design, blast-radius).

**Root cause (VERIFICATO browser+repo-audit 2026-05-16, NON ipotesi)**:
6 required status-check su `main`, **tutti vivi e reali** (nessuno
morto/obsoleto — premessa "check morto" FALSIFICATA):

| Check | Sorgente | Perché non riporta sul branch bot |
|---|---|---|
| `governance` | `docs-governance.yml` | required; il workflow stesso documenta workaround `gh workflow run docs-governance.yml --ref <branch>` |
| `paths-filter` | `ci.yml` | job base |
| `cli-checks` | `ci.yml` | `if: needs.paths-filter.outputs.cli\|\|data` → false su PR derived → SKIPPED |
| `python-tests` | `ci.yml` | `if: ...python\|\|data` → SKIPPED |
| `dataset-checks` | `ci.yml` | `if: ...data\|\|deploy` → SKIPPED |
| `stack-quality` | `ci.yml` | `if: ...stack` → SKIPPED |

PR skiv tocca solo `data/derived/skiv_monitor/` + `docs/skiv/MONITOR.md`
→ paths-filter output tutti false → 5 job ci.yml **SKIPPED**. GitHub
tratta required-check **skipped** come "Expected, waiting" (≠ pass) →
**BLOCK eterno by-design** della path-filter optimization. Review già
APPROVED. Non c'è check fantasma/morto: c'è deadlock skipped-required.

## Perché non auto-fixabile da sessione (boundary OD-041)

Ogni vettore di fix tocca un permesso che il PAT fine-grained OD-041
**esclude di proposito** (riduzione blast-radius — decisione master-dd):

| Vettore | Permesso richiesto | OD-041 |
|---|---|---|
| Modifica branch-protection | Administration | escluso |
| Editare `.github/workflows/` | Workflows | escluso |
| Bot auto-`--admin`-merge nel cron | (security regression) | rifiutato anche dal classifier — corretto |

L'auto-bypass nel workflow = indebolimento permanente della protezione
→ **NON è il fix ottimale, è un anti-pattern**. Scartato.

## Fix ottimale (zero security-loss) — azione master-dd

**Principio**: i 6 check restano enforced per i PR reali (controllo
sicurezza preservato). Si esenta SOLO il bot github-actions per i suoi
PR di soli dati-derived (path-scoped) = elimina il deadlock senza
toccare la sicurezza degli altri PR. NESSUNA rimozione di check.

### Step 1 — diagnosi (GIÀ FATTA, vedi tabella Root cause)

Diagnosi completata via browser read-only 2026-05-16: i 6 check sono
identificati e tutti vivi. **NON serve rimuovere nulla** (premessa
"check morto" falsificata). API `gh api .../branches/main/protection`
= 403 col PAT OD-041 (no Administration) — irrilevante, diagnosi fatta
via merge-box UI + repo audit.

### Step 2 — scegli il fix (azione master-dd; ❌ NIENTE rimozione check)

⚠️ **Opzione "rimuovi check morto" RIMOSSA**: nessun check è morto;
rimuoverli romperebbe la CI per i PR reali. Era ipotesi, falsificata.

- **2c — OTTIMALE (scoped bypass)**: GitHub ruleset / branch-protection
  con **bypass per `github-actions[bot]`** ristretto a PR che toccano
  SOLO `data/derived/skiv_monitor/**` + `docs/skiv/MONITOR.md`. I 6
  check restano enforced per ogni altro PR. Zero security-loss.
  (Settings → Rules → ruleset → bypass list. Admin tuo.)
- **2b — alt strutturale (gate-job)**: in `ci.yml` aggiungi un job
  "required-gate" che gira sempre (no path-filter) e riporta success
  quando i job condizionali sono skipped (pattern GitHub standard per
  skipped-required). Modifica workflow = perm Workflows, tua.
- **governance**: workaround documentato nel workflow stesso —
  `gh workflow run docs-governance.yml --ref auto/skiv-monitor-update`
  (sblocca 1/6; gli altri 5 ci.yml restano → serve comunque 2c/2b).

**Raccomandazione**: **2c** (chirurgico, zero security-loss, chiude il
debito ricorrente per sempre). 2b se preferisci fix CI-side.

### Step 3 — verifica

```bash
gh pr view 2257 --repo MasterDD-L34D/Game --json mergeStateStatus
# atteso: MERGEABLE/CLEAN
gh pr merge 2257 --repo MasterDD-L34D/Game --squash --delete-branch
```

Prossimo cron (4h) non ricreerà un PR BLOCKED (root-cause chiuso).

## Una-tantum (se non vuoi fixare ora)

`gh pr merge 2257 --repo MasterDD-L34D/Game --squash --admin`
(merge singolo via tuo privilegio admin). Il loop ricorrente resta →
torna a questo runbook per la chiusura strutturale.

## Cross-link
- Board: `docs/cross-repo/EXECUTION-BOARD.md`
- Decisione scope-PAT: vault `docs/decisions/OD-041-gh-token-scope-2026-05-16.md`
