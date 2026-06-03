# Jules suggestions snapshot 2026-06-03 (LIVE; READ-ONLY; Start = Eduardo)

> **LIVE sweep** via Claude-in-Chrome (Eduardo's connected browser, logged in jules.google),
> per `docs/runbook/jules-suggestions-snapshot.md`. Supersedes the earlier 2026-06-02 baseline.
> Read path: navigate `jules.google.com/repo/<owner>/<repo>/suggestions` -> screenshot ->
> read (the `/repo` accessibility tree is too large; screenshot is the reliable reader, as the
> runbook warns). Verdicts are ADVISORY stubs for a human/triage pass. Start / edit+submit /
> close / toggle = Eduardo (SDMG R6). Source: jules.google per-repo (no API). PRO, Gemini 3.1 Pro,
> daily session limit 3/100.

## Enabled state (live)

**3/5 repo max enabled** (the toggle count shown in-app): **codemasterdd-ai-station, Game,
Game-Godot-v2**. **Game-Database = suggestions OFF** now (it was ENABLED in the 2026-06-02
baseline; toggled off since -- plausibly after the #169/#170 security fixes landed). The 4
remaining repos in the selector (compass-marketplace, evo-swarm, evo-tactics-refs-meta, +
others) are not suggestions-configured.

## codemasterdd-ai-station (ENABLED)
- **[Security]** API Secret Exposure to Frontend
  - VERDICT-STUB: **triage** -- recurs from the 06-02 baseline; ground-truth the cited file
    (public-config false-positive vs a real leak). High-signal, verify before any action.
- **[Performance]** N+1 Database Insert in Loop
  - VERDICT-STUB: **triage** -- verify the loop is a real hot path (likely a script/migration).
- **[Cleanup]** Unused import: `os` / `Counter` / `defaultdict` / `shutil` / `hashlib` (5)
  - VERDICT-STUB: **likely-resolved-verify / batch** -- #267 already removed 11 unused imports;
    confirm these are residual/new. If real, a single scoped batch (grep-before-remove).
- **[Testing]** Missing test file for `llmfit-task-eval.py` functions; Missing edge-case test
  for `redact` with empty secrets array; Missing test for `map_outcome` in `migrate-log-to-sqlite.py`
  - VERDICT-STUB: **triage** -- legit coverage gaps if the functions exist; edit-before-Start.

## Game (ENABLED)
- **[Testing]** Test missing for `main`
- **[Testing]** Test missing for `fetchTraitRegistry`
- **[Performance]** N+1 Array Search in `session.js` (playerIntents loop)
  - VERDICT-STUB (all): **triage** -- the N+1 in the playerIntents loop is a plausible real hot
    path (matches the kind of perf chip already triaged this cycle); the 2 testing gaps are
    coverage-legit. edit-before-Start for any dispatch (anti-#10/anti-S5 guard-rail).

## Game-Godot-v2 (ENABLED)
- **[Testing]** Missing test for `nnResolution` in `SpeciesCatalog`
  - VERDICT-STUB: **triage** -- coverage gap, GDScript.
- **[Security]** Insecure default HTTP endpoint (~10 instances)
  - VERDICT-STUB: **drop** -- localhost/dev HTTP false-positives (the sec-9 + prior-session
    reject: "Godot insecure-HTTP = localhost FP"). Do NOT dispatch; same FP class repeated.
- **[Security]** Hardcoded HTTP URL schema (x2)
  - VERDICT-STUB: **defer-verify** -- probably the same localhost-FP class; confirm before any action.
- **[Cleanup]** Actionable URL routing implementation task (x4)
  - VERDICT-STUB: **triage** -- inspect one; if it is the URL-routing follow-up it may be real.
- **[Performance]** Dynamic Array Allocation for Membership Check (several)
  - VERDICT-STUB: **triage** -- GDScript perf; verify it is a hot path, not a cold-path micro-opt.

## Game-Database (OFF)
- Suggestions toggle OFF (was ENABLED 2026-06-02). Nothing to triage; re-enable in-app if the
  post-#169/#170 state should be re-scanned. Eduardo-only (toggle = config mutation, SDMG R6).

## Triage notes
- **edit-before-Start** (load-bearing): the generic "Start" launches a "Code Health Improvement
  Task" boilerplate WITHOUT our anti-#10 / anti-S5 constraints. For any suggestion that survives
  triage, Eduardo uses "edit" to paste the guard-rail (zero-behavior, single-file,
  minimal-diff/no-rewrite, grep-before-remove, lock-test CI-green) THEN Starts.
- **Net high-signal this sweep**: codemasterdd "API Secret Exposure to Frontend" (Security,
  verify) + the N+1s (codemasterdd DB-insert, Game session.js). **Net noise**: Godot-v2's ~10x
  "Insecure default HTTP endpoint" (localhost FP, drop) + the codemasterdd unused-imports
  (likely covered by #267). Categories live: Cleanup / Performance / Security / Code Health / Testing.
