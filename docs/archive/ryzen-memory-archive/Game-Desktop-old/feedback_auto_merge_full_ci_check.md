---
name: Auto-merge watcher must check ALL CI not just required
description: Background watcher cascade L3 ha mergiato PR #2195 con CI rossa qa-reports (non-required check). Watcher condition deve verificare tutti checks not just mergeStateStatus.
type: feedback
originSessionId: b987ed2a-dae5-400d-bac1-6304ca94fcd0
---
# Auto-merge watcher must check ALL CI checks

**Why**: PR #2195 mergiato 2026-05-10 sera con `Generate QA baselines` (qa-reports workflow) RED. mergeStateStatus passato da BEHIND → CLEAN perché qa-reports NON è in branch protection required checks list. Watcher background ha proceduto merge ignorando red.

Required checks list confermata (8 jobs): paths-filter + governance + python-tests + cli-checks + dataset-checks + styleguide + stack-quality + (eventuali). qa-reports + altri workflow non-required = bypass automatico.

**Conseguenza**: post-merge follow-up PR #2196 obbligatorio per regen reports + close CI red. Costo +1 PR cycle vs verifica pre-merge.

**How to apply**: future watcher cascade L3 condition deve includere check completo via `bucket` field (NOT `conclusion`).

```bash
# OLD (bypass non-required red):
until [ "$(gh pr view N --json mergeStateStatus --jq .mergeStateStatus)" != "BEHIND" ] && \
      [ ... != "BLOCKED" ] && [ ... != "UNKNOWN" ]; do sleep 10; done

# WRONG (field --json conclusion non esiste, watcher stuck infinite):
... && [ "$(gh pr checks N --json conclusion --jq 'all(.[]; .conclusion != "FAILURE")')" = "true" ]

# CORRECT (use bucket field per `gh pr checks --json` schema):
until [ "$(gh pr view N --json mergeStateStatus --jq .mergeStateStatus)" != "BEHIND" ] && \
      [ ... != "BLOCKED" ] && [ ... != "UNKNOWN" ] && \
      [ "$(gh pr checks N --json bucket --jq 'all(.[]; .bucket != "fail")')" = "true" ]; do
  sleep 10
done
```

**Available fields** `gh pr checks --json`: bucket (pass/fail/pending/skipping), completedAt, description, event, link, name, startedAt, state, workflow.

**Trigger consultation**: ogni cascade L3 background watcher launch.

**Anti-pattern**: ignorare workflow non-required perché branch protection permette. RED è RED. Anche qa-reports / docs-governance / lint suggeriscono qualità — pre-merge check tutti.

**Validato 2026-05-10**: PR #2195 merged con qa-reports RED → follow-up #2196 ship reports regen `npm run export:qa`. Pattern post-mortem documentato.
