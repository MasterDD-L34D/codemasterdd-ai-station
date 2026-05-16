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

**Root cause (alta confidenza)**: branch-protection `main` ha un
**required status-check** che NON gira mai sul branch
`auto/skiv-monitor-update` (workflow skiv-monitor non lo triggera) →
GitHub lo tiene "Expected, waiting" → BLOCK eterno. La review è già
soddisfatta; l'unico residuo è il check fantasma.

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

**Principio**: la review umana resta enforced (controllo sicurezza
reale). Si elimina SOLO il required-check che nessun PR può mai
soddisfare sul branch bot = deadlock a valore-sicurezza zero.

### Step 1 — diagnosi precisa (tu, hai Administration)

```bash
gh api repos/MasterDD-L34D/Game/branches/main/protection \
  --jq '.required_status_checks'
```

Annota i `contexts` / `checks[].context`. Identifica quello che NON gira
sul branch `auto/skiv-monitor-update`.

### Step 2 — scegli il fix (decisione, non meccanica)

- **2a (consigliato se il check è obsoleto/morto)**: rimuovilo dai
  required. Pure cleanup, NON weakening (review resta).
  ```bash
  gh api -X PATCH repos/MasterDD-L34D/Game/branches/main/protection/required_status_checks \
    -f 'contexts[]=<SOLO i check ancora validi, escluso il fantasma>'
  ```
- **2b (se il check è valido ma non gira sul branch bot)**: fix
  strutturale corretto = far girare quel job anche su
  `auto/skiv-monitor-*` (modifica CI workflow — Workflows perm, tua).
  Mantiene il check ovunque, elimina il deadlock legittimamente.
- **2c (minimale, path-scoped)**: GitHub ruleset con **bypass per
  github-actions[bot]** ristretto a PR che toccano SOLO
  `data/derived/skiv_monitor/**` + `docs/skiv/MONITOR.md`. Bypass
  chirurgico, non blanket. (Settings → Rules → ruleset → bypass list.)

**Raccomandazione**: 2a se il check è morto (più probabile — 0 check
girano, nessuno lo riporta mai), altrimenti 2c (scoped, sicuro).
2b solo se il check ha valore reale da preservare su quel branch.

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
