# Recap -- SoT Drift Sentinel (shipped + live) -- per uso su Ryzen

> **Authored-from**: Lenovo (CodeMasterDD / edusc / <hub-ip>), 2026-05-28.
> **For-use-on**: Ryzen (DESKTOP-T77TMKT / Vgit / <ryzen-ip>) o qualsiasi PC fleet.
> **Come arriva qui**: codemasterdd e' PRIVATE + synced -> su Ryzen `git -C C:/dev/codemasterdd-ai-station pull` (se clonato) e leggi questo file.
> Companion: handoff originale `docs/handoffs/2026-05-28-handoff-sot-drift-A.md` + spec/plan in `docs/superpowers/` (entrambi codemasterdd).

## Repo legend (necessaria per navigare i path qui sotto)

I path nei `backtick` sono relativi al repo qualificato in chiaro. Aprili in editor con quel repo come root, oppure clicca i link GitHub forniti per i casi cross-repo critici.

| Tag | Path locale (fleet) | GitHub URL |
|-----|---------------------|------------|
| **`codemasterdd/...`** | `C:/dev/codemasterdd-ai-station/...` | https://github.com/MasterDD-L34D/codemasterdd-ai-station (PRIVATE) |
| **`Game/...`** | `C:/dev/Game/...` (Ryzen + Lenovo) | https://github.com/MasterDD-L34D/Game (PUBLIC) |
| **`vault/...`** | `C:/dev/vault/Spaces/Dev/Evo-Tactics/...` | https://github.com/MasterDD-L34D/vault (PRIVATE sovereign) |
| **`memory/...`** | `C:/Users/<user>/.claude/projects/C--dev-codemasterdd-ai-station/memory/...` | NON in git -- per-PC, non navigabile cross-fleet |
| **`aa01/...`** | `C:/Users/<user>/aa01/...` | NON in git (Personal Cognitive Studio) |

Cross-repo gotcha: il Game local sui due PC e' tipicamente stale (husky skip-worktree blocca FF-pull su main). Se un Game path qui non si apre, applica il runbook KM section 6 (`update-index --no-skip-worktree .husky/pre-commit` -> `git checkout -- .husky/pre-commit` -> `git pull --ff-only origin main` -> `update-index --skip-worktree .husky/pre-commit`). Sperimentato in sessione 2026-05-28: pull 91 commit, file `Game/docs/guide/games-source-index.md` poi apribile.

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
| Privacy guard | codemasterdd `.aiderignore` (esclude `docs/archive/ryzen-memory-archive/`) | done, smoke PASS |
| Lessons | `~/aa01/learnings/L-2026-05-038` (ESM CLI portability) + `L-2026-05-039` (branch-protection pitfall) | promosse |

## Come si OPERA (workflow runtime)

1. Game merge su main tocca un'area watched (`apps/backend/services/genetics/**`, `combat/**`, `data/core/economy*`, `data/core/biomes*`) -> Action apre/aggiorna **una** issue `sot-drift-candidate` (idempotente: edit, non duplica).
2. Su qualsiasi PC con codemasterdd + Claude Code: invoca il subagent. Trigger naturali: "verdict drift candidate", "is SoT stale", "controlla drift SoT". Oppure passa manualmente {sot_ref, Game commit/PR}.
3. Il subagent: legge il SoT vault reale (`C:/dev/vault/Spaces/Dev/Evo-Tactics/<ref>`, fetch first) + il change Game -> verdetto multi-signal (STALE solo se runtime shipped E SoT dice ancora not-done) + confidence.
4. Se STALE (>= med): propone reconcile vault via branch+PR (DEFERRED->SHIPPED). **Merge = Eduardo**. Commenta la issue Game con verdetto + link PR (non chiude).
5. Se NO-DRIFT: commenta + chiude la issue.

Boundary subagent: mai direct-push vault main, mai merge, mai edit Game oltre il commento issue. Confidence low/ambiguo -> report a Eduardo, no PR.

## Primo caso d'uso reale (eseguito 2026-05-28: NO-DRIFT)

`sot-drift-verifier` invocato live su `vault/core/00-SOURCE-OF-TRUTH.md` section 24.6 (epigenome) vs [Game #2402](https://github.com/MasterDD-L34D/Game/pull/2402). Pre-check: `git -C C:/dev/vault fetch` -> local == origin (`553b56c6`). Verdetto: **NO-DRIFT (high confidence)**. Il SoT era gia' stato riconciliato dal vault commit `40992953e` ("docs(sot): reconcile epigenome DEFERRED -> SHIPPED (Fase-3)", 2026-05-28 00:59) da un'altra sessione (Ryzen .11) PRIMA del verdict: linee `Epigenome ... SHIPPED Fase-3 (2026-05-28)` con citazione #2401/#2402/#2404; `genealogie profonde + ambient-drift S5 + hybrid genuino` correttamente lasciate DEFERRED.

**Meta-lezione del primo run**: il sentinel ha beccato il marker stale in `codemasterdd/docs/KNOWLEDGE_MAP.md` section 7 (diceva "vault SoT lagga, riconciliazione pending"), NON il SoT. Anti-pattern #19 *ironico*: il proprio tracker era piu' stale del SoT che doveva monitorare. KM corretto in commit `1319428` ("docs(session): governance journal + epigenome no-drift verdict").

## Sync su Ryzen (note fleet)

- **codemasterdd**: PRIVATE, `git pull` diretto. Porta giu' agent + .aiderignore + questo recap. NB: `.aiderignore` e' tracked apposta (esentato da `.aider*` via `!.aiderignore`) -> il guard propaga al clone Ryzen.
- **Game**: PUBLIC. Local Ryzen e' STALE (come Lenovo) + `.husky/pre-commit` skip-worktree blocca commit su main. **Per editare**: worktree fresco da origin/main, NON commit su main local:
  ```
  git -C C:/dev/Game worktree add -b claude/<topic> C:/dev/Game-<topic> origin/main
  # build -> commit sul branch -> push -> gh pr create -> git worktree remove C:/dev/Game-<topic> --force
  ```
- **vault**: sovereign. Branch+PR only, merge Eduardo. `git -C C:/dev/vault fetch` + verifica local == origin prima di leggere SoT come autorita'.

## Gotchas (non ri-scoprire)

1. **Game branch-protection footgun** -- **FIXED 2026-05-28** (memory `memory/reference_game_branch_protection.md` + `aa01/learnings/L-2026-05-039`). **Storia**: un PR che toccava solo `Game/.github/**`+`Game/tools/**` faceva "skipping" i required check path-filtered (`python-tests`/`stack-quality`/`cli-checks`/`dataset-checks`) -> `mergeStateStatus: BLOCKED` anche se il codice era OK. Workaround era `gh pr merge <n> --admin --merge` (bypass governance, auth esplicita Eduardo). **Fix shipped**: [PR #2413](https://github.com/MasterDD-L34D/Game/pull/2413) ha aggiunto un job `ci-gate` aggregator (`always()` + `needs:` i 5 job required, passa su success-or-skipped); branch protection swap-pata a required `[governance, ci-gate]`. Da ora i PR tooling-only mergiano CLEAN senza admin. `strict:true` invariato -> aggiorna il branch (worktree `git merge origin/main`) se BEHIND.
2. **ESM CLI entry-point** (L-038): in Node ESM usa `import.meta.url === pathToFileURL(process.argv[1]).href`, MAI il literal `file://${process.argv[1]}` (POSIX-only -> su Windows il CLI esce 0 senza output = smoke locale silently rotto mentre CI Linux e' verde). QG Step-1 di un CLI verifica l'OUTPUT, non l'exit code.
3. **tdd-guard**: se attivo blocca i Write `.mjs/.sh` ("Premature implementation") anche con plugin disabilitato. Fix: `.claude/tdd-guard/data/config.json` = `{"guardEnabled": false}` (gitignored, per-PC).
4. **gh CLI path** (Windows fleet): `"/c/Program Files/GitHub CLI/gh.exe"`.

## Commit policy (promemoria, ADR-0011)

Ogni commit: trailer `Coding-Agent: claude-...` + `Trace-Id: <uuid>`, NO `Co-Authored-By`. Subject <=72 char, minuscola dopo `type:`. Body prose ASCII-first (`--` non em-dash). Il pre-commit hook globale blocca non-ASCII su `ps1|sh|bat|cmd|py|js|json|ya?ml`.
