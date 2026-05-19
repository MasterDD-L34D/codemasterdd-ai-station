# Design Spec -- tdd-guard path-scoped enforcement (C-raffinato)

- Date: 2026-05-19
- Status: PROPOSED (design only; impl Eduardo-gated, regola-0)
- Cross-link: vault OD-050 (PR #130) §1a/1b/1c + M0/M1/M2/M3, canonical-config
  `_INERTE_CLAIM_FALSIFIED_2026_05_18` (L46) + `_ON_list_RESOLVED` (L43)
- Method: superpowers brainstorming -> approach C-raffinato (confirmed by
  Eduardo 2026-05-19 after read-only investigation of tdd-guard config schema)

## 1. Problem

tdd-guard PreToolUse hook (`Write|Edit|MultiEdit|TodoWrite` -> `npx
tdd-guard@latest`) is registered in canonical-config user-global
(`~/.claude/settings.json` deploy) -> fires in EVERY repo/worktree. Its
native default = ENABLED with heuristic-block even without a test-reporter
("Premature implementation - write test first"). Decision (a)
(canonical L43: default-OFF + ON-5) was recorded but never implemented; no
effective `guardEnabled:false` exists anywhere. Lived evidence: this
session (OD-049/linter/observe.sh ops `.py`) was repeatedly blocked in a
fresh codemasterdd worktree. = Anti-Pattern#9 (decided-not-validated-live)
+ #8 (canonical claim != behavior).

Investigation (2026-05-19, read-only, tdd-guard docs authoritative):
- `guardEnabled` on/off state lives in `.claude/tdd-guard/data/` which
  tdd-guard docs say MUST be `.gitignore`d -> a tracked default-OFF flag
  there is impossible (falsifies original approach A "tracked
  data/config.json"). Fresh worktree -> fresh data dir -> native default
  (ENABLED).
- tdd-guard has NO native path-glob / ignore option (config = env vars +
  custom validation rules only).
- The deterministic, git-tracked, fresh-worktree-safe, cross-PC lever is
  WHERE the hook is registered: per-repo project `.claude/settings.json`
  (in the repo tree, tracked) vs user-global (current, fires everywhere).
- `custom-instructions.md` (`.claude/tdd-guard/data/instructions.md`) can
  encode validation rules -> can express "edits to non-test paths PASS".
  SessionStart hook creates it from a template if absent (never
  overwrites) -> a tracked repo template can seed it.

## 2. Goal / Non-goals

Goal: tdd-guard enforces test-first ONLY in the derived ON-set
(behavior-code repos with test-reporter infra), provably inert elsewhere,
deterministic + cross-PC + fresh-worktree-safe + no per-worktree manual
hack; mixed ON repos (codemasterdd) do not block ops/docs/non-test edits.

Non-goals: changing tdd-guard upstream; adding tests to vault ops-glue
scripts (accepted as smoke-validated, OD-050 §1c reco-i); fixing
unrelated canonical-config drift (only L43/L44 + W-2 in scope).

## 3. Constraints

- canonical-config = vault sovereign, cross-PC, deployed by
  `deploy_claude_global.ps1`. Changes Eduardo-gated (regola-0: NON
  guess-fix; design -> approval -> impl).
- codemasterdd = ON, non-negotiable (primary cross-repo coordination hub),
  but mixed content (behavior-code + ops-scripts + docs).
- vault / synesthesia / others = OFF (prose / no test infra).
- Must validate LIVE post-deploy (Anti-Pattern#9), not assume.
- Reversible.

## 4. Design (C-raffinato)

### L1 -- structural hook-placement (resolves M0 + M1)

1. REMOVE the tdd-guard `Write|Edit|MultiEdit|TodoWrite` (+ any
   tdd-guard `UserPromptSubmit`) hook from canonical-config
   `settings_json_hooks` (user-global). Net effect: tdd-guard stops firing
   universally.
2. ADD the same hook to the tracked project `.claude/settings.json` of
   each ON-set repo only.
3. ON-set = DERIVED, recomputable: `{monitored-ecosystem roster} INTERSECT
   {has integrable test-reporter infra (vitest/jest/pytest/GUT/go/...)}`.
   Confirmed: Game, Game-Godot-v2, codemasterdd. To resolve: Game-Database
   (`node ./test/run-tests.js` custom -> reporter-compat verify),
   Item-generator + evo-swarm (existence + infra verify, Lenovo-side).
4. Because project `.claude/settings.json` is in the repo tree and
   git-tracked, every worktree + both PCs inherit it automatically. NON-set
   repos have no tdd-guard hook = structurally inert (no heuristic block,
   no gitignored-flag dependency). Solves the fresh-worktree root cause
   deterministically.

### L2 -- custom-instructions path-scope for mixed ON repos (resolves M3)

For ON repos that are mixed (codemasterdd; potentially others):
- Maintain a TRACKED template `scripts/hooks/tddguard-instructions.template.md`
  in the repo with rules: "Edits to `**/*.md`, `scripts/**`, `docs/**`,
  `**/*.tmp*`, `.claude/**` are NOT TDD-relevant -> always PASS. Enforce
  test-first only on behavior-code (`src/**`, `apps/**`, package source)."
- SessionStart hook copies template -> `.claude/tdd-guard/data/
  instructions.md` if absent (tdd-guard creates-if-absent + never
  overwrites; supplying our template pre-empts the default rules).
- Net: codemasterdd ON, behavior-code guarded, ops/docs/.py-glue exempt =
  zero recurring friction (the OD-049 pain class).
- Fallback if custom-instructions proves insufficient against the
  heuristic validator (RISK R2): documented `// tdd-guard-skip` /
  commit-trailer bypass convention for ops/docs in mixed ON repos
  (explicit, minimal, accepted).

### L3 -- canonical cleanup + integrity + live-verify

- Backport W-2: observe.sh hook command in canonical missing positional
  `pre`/`post` arg (PreToolUse misclassified as post). Add `pre`/`post`.
- Fix L43<->L44 contradiction: codemasterdd = ON (L43 correct); L44 drop
  codemasterdd from the NON-setup list.
- Update canonical-config to reflect L1 (tdd-guard hook NOT user-global;
  per-repo). Update `_INERTE_CLAIM_FALSIFIED` -> RESOLVED-by-design ref.
- `deploy_claude_global.ps1`: ensure it no longer re-injects the
  user-global tdd-guard hook (regression guard).
- LIVE-firing verification matrix (Anti-Pattern#9, post-deploy, fresh
  session both PCs): for each repo assert observed = expected ON/OFF;
  for codemasterdd assert ops/docs `.py` edit PASSES + behavior-code
  edit-without-test BLOCKS.

## 5. Components / data flow

| Artifact | Location | Tracked? | Role |
|---|---|---|---|
| tdd-guard hook | per-repo `.claude/settings.json` (ON-set only) | YES (repo) | fires tdd-guard only in ON-set; fresh/cross-PC safe |
| canonical-config | vault `Vault-ops-remote/claude-global/canonical-config.json` | YES (vault) | NO LONGER carries user-global tdd-guard hook; documents policy |
| instructions.template.md | per-repo `scripts/hooks/tddguard-instructions.template.md` (mixed ON) | YES (repo) | path-scope rules source |
| instructions.md | `.claude/tdd-guard/data/instructions.md` | NO (gitignored) | runtime, seeded from template via SessionStart |
| guard on/off state | `.claude/tdd-guard/data/` | NO (gitignored) | runtime only; NOT the control lever (structural hook-placement is) |
| deploy script | `deploy_claude_global.ps1` | YES (vault) | must not re-inject user-global tdd-guard hook |

Control flow: hook present (repo in ON-set) -> tdd-guard runs -> reads
instructions.md (template-seeded path-scope) -> PASS non-test paths /
enforce behavior-code. Hook absent (NON-set) -> nothing runs = inert.

## 6. Edge cases / error handling

- Fresh worktree of ON repo: project `.claude/settings.json` present
  (tracked) -> hook fires; instructions.md absent -> SessionStart seeds
  from tracked template -> path-scope active. Safe.
- Fresh worktree of NON-set repo: no hook -> inert. Safe (the bug fixed).
- Repo not yet classified (new repo): default = NOT in ON-set = inert
  until explicitly added (fail-safe direction = OFF, opposite of today).
- SessionStart not configured in a repo: instructions.md may be absent ->
  tdd-guard default rules (strict). Mitigation: L2 requires SessionStart
  present in mixed ON repos (part of the per-repo settings bundle).
- deploy_claude_global re-injects old user-global hook: L3 regression
  guard + live-verify catches.

## 7. Testing / verification

- Static: canonical-config no tdd-guard user-global hook; each ON-set
  repo `.claude/settings.json` has it; mixed ON repos have
  instructions.template.md.
- LIVE matrix (post-deploy, fresh session, BOTH PCs) -- Anti-Pattern#9:
  - vault/synesthesia: edit `.py`/`.md` -> NOT blocked (inert).
  - Game/Godot: behavior-code edit w/o test -> blocked; test edit -> ok.
  - codemasterdd: `scripts/*.py` / `docs/*.md` edit -> PASS; behavior-code
    (e.g. real module) edit w/o test -> blocked.
- Regression: 2nd deploy run = no user-global tdd-guard hook reappears.

## 8. Rollout (incremental, gated, reversible)

1. Eduardo approves spec.
2. Resolve M0 ON-set (verify Game-DB/Item-gen/evo-swarm) -> final list.
3. Per-repo: add tracked `.claude/settings.json` tdd-guard hook +
   (mixed) instructions.template.md + SessionStart. One PR per repo or a
   coordinated batch; codemasterdd first (highest friction, fastest
   feedback).
4. canonical-config patch (remove user-global hook, L43/L44, W-2) +
   deploy_claude_global guard -> vault PR (Eduardo merge).
5. Deploy both PCs -> LIVE verify matrix -> only then mark RESOLVED.
Rollback: re-add user-global hook in canonical (one revert) restores
prior behavior.

## 9. Risks / open items

- R1: custom-instructions may not fully suppress the heuristic validator
  (it is LLM-ish). Mitigation: L2 fallback bypass-convention; validate in
  step-3 codemasterdd-first before wider rollout.
- R2: Game-Database `node ./test/run-tests.js` not a standard reporter ->
  tdd-guard may not integrate cleanly -> Game-DB may be ON-without-reporter
  (heuristic only) = partial. Decide: include with custom-instructions or
  defer Game-DB.
- R3: per-repo `.claude/settings.json` may collide with other hooks
  (commit-guard, observe.sh) -> must MERGE not replace per-repo settings.
- R4: Item-generator / evo-swarm existence + infra unverified from Ryzen
  (Lenovo-side) -> M0 finalization needs cross-PC check.
- Open: should ON-set live as data (canonical-config list) re-derived
  periodically, or computed by a script (drift-audit reconcile.py
  extension)? Recommend: canonical-config explicit list + reconcile.py
  check that flags roster/test-infra drift (audit, not auto-mutate).

## 10. Governance

This spec = proposal. Implementation (canonical-config patch, per-repo
settings, deploy, cross-PC verify) is Eduardo-gated (regola-0, sovereign
cross-PC). Folds into OD-050 as the resolution design for M0/M1/M3 + W-2 +
L43/L44.
