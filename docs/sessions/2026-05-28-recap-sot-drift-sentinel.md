# Recap -- SoT Drift Sentinel (shipped + live) -- per uso su Ryzen

> **Authored-from**: Lenovo (CodeMasterDD / edusc / 192.168.1.10), 2026-05-28.
> **For-use-on**: Ryzen (DESKTOP-T77TMKT / Vgit / 192.168.1.11) o qualsiasi PC fleet.
> **Come arriva qui**: codemasterdd e' PRIVATE + synced -> su Ryzen `git -C C:/dev/codemasterdd-ai-station pull` (se clonato) e leggi questo file.
> Companion: handoff originale `docs/sessions/2026-05-28-handoff-sot-drift-A.md` + spec/plan in `docs/superpowers/`.

## TL;DR

SoT Drift Sentinel = mitigazione anti-pattern #19 (runtime Game corre avanti, doc SoT vault laggano). **Due componenti, ora LIVE**:
- **A (Game, PUBLIC)**: GitHub Action `sot-drift-sentinel` su push:main -> matcher dep-free -> apre issue `sot-drift-candidate`. Detection deterministica.
- **B (codemasterdd, PRIVATE)**: subagent `sot-drift-verifier` -> verdetto semantico gated + propone reconcile vault (branch+PR, mai auto-merge).

Stato: **A merged + primo CI run verde**; **B QG full-PASS**; privacy gap chiuso. Vedi sotto.

## Cosa e' shippato

| Cosa | Dove | Stato |
|------|------|-------|
| Action + matcher + watch-map + flag-issue | Game `.github/sot-drift/` + `tools/sot-drift/` + `.github/workflows/sot-drift-sentinel.yml` | PR #2406 MERGED (`29ac9102`), CI run sul merge = success 14s, 0 issue spurie |
| Subagent verdetto | codemasterdd `.claude/agents/sot-drift-verifier.md` | QG Step-1 PASS (live dispatch smoke) -- production-ready |
| Wiring tracking | codemasterdd `docs/KNOWLEDGE_MAP.md` section 8 | done |
| Privacy guard | codemasterdd `.aiderignore` (esclude `docs/ryzen-memory-archive/`) | done, smoke PASS |
| Lessons | `~/aa01/learnings/L-2026-05-038` (ESM CLI portability) + `L-2026-05-039` (branch-protection pitfall) | promosse |

## Come si OPERA (workflow runtime)

1. Game merge su main tocca un'area watched (`apps/backend/services/genetics/**`, `combat/**`, `data/core/economy*`, `data/core/biomes*`) -> Action apre/aggiorna **una** issue `sot-drift-candidate` (idempotente: edit, non duplica).
2. Su qualsiasi PC con codemasterdd + Claude Code: invoca il subagent. Trigger naturali: "verdict drift candidate", "is SoT stale", "controlla drift SoT". Oppure passa manualmente {sot_ref, Game commit/PR}.
3. Il subagent: legge il SoT vault reale (`C:/dev/vault/Spaces/Dev/Evo-Tactics/<ref>`, fetch first) + il change Game -> verdetto multi-signal (STALE solo se runtime shipped E SoT dice ancora not-done) + confidence.
4. Se STALE (>= med): propone reconcile vault via branch+PR (DEFERRED->SHIPPED). **Merge = Eduardo**. Commenta la issue Game con verdetto + link PR (non chiude).
5. Se NO-DRIFT: commenta + chiude la issue.

Boundary subagent: mai direct-push vault main, mai merge, mai edit Game oltre il commento issue. Confidence low/ambiguo -> report a Eduardo, no PR.

## Primo caso d'uso reale candidato

vault SoT `core/00-SOURCE-OF-TRUTH.md` section 24.6 (epigenome) dice ancora **DEFERRED**, ma il runtime ha shippato Fase-3 (Game #2402). Riconciliazione vault pending (reuse-queue KNOWLEDGE_MAP section 7). Quando vuoi: invoca `sot-drift-verifier` su quel ref -> dovrebbe dare STALE + proporre il reconcile.

## Sync su Ryzen (note fleet)

- **codemasterdd**: PRIVATE, `git pull` diretto. Porta giu' agent + .aiderignore + questo recap. NB: `.aiderignore` e' tracked apposta (esentato da `.aider*` via `!.aiderignore`) -> il guard propaga al clone Ryzen.
- **Game**: PUBLIC. Local Ryzen e' STALE (come Lenovo) + `.husky/pre-commit` skip-worktree blocca commit su main. **Per editare**: worktree fresco da origin/main, NON commit su main local:
  ```
  git -C C:/dev/Game worktree add -b claude/<topic> C:/dev/Game-<topic> origin/main
  # build -> commit sul branch -> push -> gh pr create -> git worktree remove C:/dev/Game-<topic> --force
  ```
- **vault**: sovereign. Branch+PR only, merge Eduardo. `git -C C:/dev/vault fetch` + verifica local == origin prima di leggere SoT come autorita'.

## Gotchas (non ri-scoprire)

1. **Game branch-protection pitfall** (memory `reference_game_branch_protection.md` + L-039): un PR che tocca solo `.github/**`+`tools/**` fa "skipping" i required check path-filtered (`python-tests`/`stack-quality`/`cli-checks`/`dataset-checks`) -> `mergeStateStatus: BLOCKED` anche se il codice e' OK. NON e' un problema di codice. Risoluzione: `gh pr merge <n> --admin --merge` (lecito, `enforce_admins:false`) MA = bypass governance -> **auth esplicita Eduardo prima**. Inoltre `strict:true` -> aggiorna il branch (`git merge origin/main`) prima del merge.
2. **ESM CLI entry-point** (L-038): in Node ESM usa `import.meta.url === pathToFileURL(process.argv[1]).href`, MAI il literal `file://${process.argv[1]}` (POSIX-only -> su Windows il CLI esce 0 senza output = smoke locale silently rotto mentre CI Linux e' verde). QG Step-1 di un CLI verifica l'OUTPUT, non l'exit code.
3. **tdd-guard**: se attivo blocca i Write `.mjs/.sh` ("Premature implementation") anche con plugin disabilitato. Fix: `.claude/tdd-guard/data/config.json` = `{"guardEnabled": false}` (gitignored, per-PC).
4. **gh CLI path** (Windows fleet): `"/c/Program Files/GitHub CLI/gh.exe"`.

## Commit policy (promemoria, ADR-0011)

Ogni commit: trailer `Coding-Agent: claude-...` + `Trace-Id: <uuid>`, NO `Co-Authored-By`. Subject <=72 char, minuscola dopo `type:`. Body prose ASCII-first (`--` non em-dash). Il pre-commit hook globale blocca non-ASCII su `ps1|sh|bat|cmd|py|js|json|ya?ml`.
