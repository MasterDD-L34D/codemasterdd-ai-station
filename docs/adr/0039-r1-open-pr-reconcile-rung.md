# ADR-0039 — R1 open-PR reconcile rung

> Status: **Proposed** 2026-06-03. Pending: (a) 3rd SDMG harsh-reviewer falsification on the
> BUILT code (Cognitive Protocol 7), (b) Eduardo ratify + merge -- this is a doctrine file
> (`docs/adr/**`) = Eduardo-only-merge per ADR-0037 dec.2 / ADR-0038, so the hub does NOT
> self-merge it. Implements the rung ADR-0037 dec.4 named as the (then-unbuilt) unblocker.
> ASCII-first (ADR-0021). **This ADR grants NO autonomy by itself -- the rung only OPENS PRs;
> auto-merge (R2) stays OFF, earned later via its own dedicated ADR.**
>
> Authority/design: spec `docs/superpowers/specs/2026-06-03-governor-r1-open-pr-rung-design.md`
> (v4, merged #292); plan `docs/superpowers/plans/2026-06-03-governor-r1-open-pr-rung.md`.

## TL;DR

ADR-0037 dec.4 made standing external-merge reachable ONLY via the governor R0->R1->R2 earn-path,
and flagged that "the R1->open-PR rung that would emit the required >=4 clean PR-cycles does not
yet exist." This ADR records that rung, now BUILT: deterministic, **clock-free** reconcile actors
that OPEN (never merge) one branch+PR per drifted doc, so the R2 evidence stream (>=4 clean
HUMAN-merged PR-cycles) can begin. Two legs: codemasterdd `STATUS_MULTI_REPO.md` and vault
`Atlas/lint-status.md` (a new governor-owned doc, Eduardo OK 2026-06-03). It does NOT touch the
shipped issue actor (`act.py:run_r1`); both coexist.

## Context

- The SHIPPED R1 (2026-06-02) chose the issue-escalation variant (scope A), which accrues ZERO
  clean PR-cycles BY DESIGN (actor-criteria sec 6 addendum). So R2 was mechanically unreachable.
- ADR-0037 dec.4 (Accepted) named this exact gap. This rung is the anti-accretion fix: the base
  defect (no open-PR rung) is BUILT, not routed around.
- Building it is itself reversible + an experiment (mirrors the R0 off-ramp): the rung only OPENS
  PRs; a human merges. If reconcilers rarely fire or Eduardo declines to merge them, that silence
  IS the honest off-ramp signal that auto-merge of this class is unnecessary -- the rung must
  SURFACE that, never manufacture churn.

## Decision

### 1. The reconcile class (precise; spec sec 4)

A doc qualifies for an auto-reconciler IFF ALL hold: (1) the reconciled region is bounded by
GOVERNOR-SYNC markers (human prose outside is never touched); (2) the region body is a
deterministic pure function of signals already in `governor.db` -- **no LLM, no external
judgement, no wall-clock**; (3) the doc is NON-doctrine per ADR-0038; (4) the change is reversible
(a marker-region edit, `git revert` clean) and low-risk (status/snapshot, not behaviour/rules).
Explicitly OUT: code, behaviour, config, anything LLM-generated, anything time-derived, anything
outside a marker region, and every doctrine file.

### 2. Doctrine exclusion = static gate + a HUMAN review checkpoint (ADR-0038)

`is_doctrine(path, repo)` is a STATIC fail-closed path-classifier (globs `docs/adr/**`,
`docs/governance/**`, repo `.claude/**`, `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/**`; named
`CLAUDE.md`/`AGENTS.md`/`ORCHESTRATION.md`/`GOALS.md`/`DECISIONS_LOG.md`/`OPEN_DECISIONS.md`;
`~/.config/aider-privacy-whitelist.txt` + the `~/.claude/` governance subpaths). A `Reconciler`
aimed at a doctrine path **refuses to construct** (`__post_init__` assert), and the actor
re-checks at runtime before any write. ADR-0038's content-based CATCH-ALL is **not** an executable
path (a pure classifier cannot evaluate "is this content a rule") -- it is a HUMAN process
checkpoint: **adding ANY new reconciler REQUIRES an explicit Eduardo doctrine-classification review
of its target.** `docs/governance/EXECUTION-BOARD.md` is under `docs/governance/**` = DOCTRINE =
EXCLUDED (why the codemasterdd leg targets `STATUS_MULTI_REPO.md`, not the board).

### 3. Human-merge-only during the earn (load-bearing invariant; spec sec 6.1)

The rung OPENS the PR; a HUMAN (Eduardo) merges every reconcile PR. The hub MUST NOT self-merge
reconcile-class PRs during the earn window -- not even codemasterdd non-doctrine ones -- because a
CLEAN R1 cycle (actor-criteria sec 6) is DEFINED as human-merged; a hub-merged reconcile PR would
(correctly) NOT count. vault PRs are Eduardo-only regardless (sibling-peer). The actor never calls
merge. After R2 is earned (its own ADR), auto-merge of the class is enabled; not before.

### 4. No merge capability -- the block is code + invariant + ceiling ONLY (spec sec 6.2)

codemasterdd is a PRIVATE free-tier repo, so branch protection is UNAVAILABLE (gh api
`branches/main/protection` -> HTTP 403 "Upgrade to Pro", verified 2026-06-03 -- the same gap that
sank the killed auto-merge-grant draft). So the merge is blocked by exactly THREE things, all of
which must hold: (a) the actor code never calls merge -- pinned by a negative test against the
**REAL** `open_or_update_pr` builder (not only the injected fake), so a future merge-path addition
goes CI-red; (b) the human-merge-only invariant (3); (c) the unchanged `.claude/settings.json`
ceiling (`git push origin claude/*`, no merge allow-rule). The token (6) is NOT a merge-block (a
`pull_requests:write` PAT can technically merge via REST). No platform defence-in-depth -> the
negative test + this code review carry the weight; the R2 ADR MUST weigh "no branch protection".

### 5. The vault lint-status leg -- clock-free 2nd repo (D1=(d), Eduardo OK 2026-06-03)

A `vault-lint-status` reconciler syncs the three vault lint signals (`vault-gap`,
`vault-coherence`, `vault-whatsmissing`) into a NEW governor-owned doc `Atlas/lint-status.md`
(verified absent 2026-06-03; create-if-absent on first run). **Why clock-free (the falsification
fix vs the KILLED eng-graph staleness band):** `parse_vault_report` derives severity from CONTENT
(`BLOCK: N` / `WARN: N` / nonzero summary metrics) with NO `now` parameter, and `payload_hash`
keys on (source, produced_at, findings, block, warn). So the lint signal STATE changes only when
the vault lint report CONTENT changes, NEVER because the calendar advanced. Accepted cost (Eduardo
OK): a governor-owned write-target in the SOVEREIGN vault repo -- mitigated: real consumer
artifact, marker-bounded, NON-doctrine, branch+PR only, **merge Eduardo-only** (sibling-peer).

### 6. Token + permissions (spec sec 8)

`GOVERNOR_RECONCILE_TOKEN` = a fine-grained PAT scoped `contents:write` + `pull_requests:write` on
EXACTLY `codemasterdd-ai-station` + `vault` -- NO admin, NO merge-queue. Passed to any child via
env (`GH_TOKEN`), NEVER argv (CWE-214). Minting is a HUMAN step. Unset -> the WRITE actor no-ops
fail-closed (records the drifted reconciler under `skipped`/no-token; opens NOTHING). Unlike the
read-ish issue actor, the WRITE actor does NOT fall back to ambient `gh auth` for writes (reads
may). `.claude/settings.json` is UNCHANGED; adding a merge allow-rule is an R2-ADR matter.

### 7. Clean-cycle accounting is EXTERNAL (anti-self-licking; spec sec 7.1; actor-criteria sec 4)

The actor's own output MUST NOT feed its own promotion. The clean-cycle COUNT is computed OUTSIDE
the actor, read-only, from git/gh history at R2-decision time -- a separate advisory helper
`reconcile_cycles_report.py` (the actor never imports it; a CI test pins that). **Honest scope:** a
reconcile PR is a bounded marker-region diff, near-zero-judgment to merge, so N clean cycles
demonstrate renderer DETERMINISM + REVERT-SAFETY, NOT merge-JUDGMENT-safety. The R2 ADR must NOT
read these cycles as "a human vetted each merge"; it must justify auto-merge on reversibility +
class-restriction + the mechanical drop-check + a CI-watchlist -- the cycles are NECESSARY, not
SUFFICIENT.

### 8. Anti-scope (explicit NON-grant)

No auto-merge (R2+, its own ADR). No `.claude/settings.json` merge allow-rule. No LLM in the diff
path (approach B / `sot-drift-verifier` deferred to a future R3 rung gated on a different-FAMILY
judge -- using B's diffs to earn the R2 that gates B is circular). No cron promotion (Fase-4;
manual `python -m governor.reconcile` only). No time-derived / clock-tick / manufactured-churn
diffs. No doctrine-file targets, ever. No Game/Godot/external targets; vault writes limited to the
new `lint-status.md`. The ">=4 across >=2 repos" distribution (3+1 vs 2+2) is DEFERRED to the R2
ADR (two real legs now exist; do not pre-decide).

## Consequences

- **Positive:** the R2 evidence stream (human-merged reconcile PR-cycles across >=2 repos) can now
  begin; the gap ADR-0037 dec.4 named is closed by construction, not routed around. The class is
  deterministic + clock-free + marker-bounded + NON-doctrine, so promoting it to R2 (later) can
  never auto-merge a doctrine file or an LLM-authored diff.
- **Negative / accepted:** slow cadence -- change-triggered + deterministic = silent when stable;
  silence IS the off-ramp signal (the rung must not inflate). A governor-owned doc now lives in the
  sovereign vault (Eduardo OK; branch+PR, Eduardo-only merge). No platform merge-backstop on the
  free-tier private repo -> the code + invariant + ceiling are load-bearing (the R2 ADR re-weighs).
- **Create-if-absent reporting (P2.2, expected, not drift):** until the FIRST vault PR is
  human-merged, `get_file(main)` returns "" (the file is not yet on main), so each run re-derives
  the same drift and the actor reports the vault leg as `opened` (action `reused`). The real
  builder's branch-level base64 dedup skips the PUT on identical content -> no new commit, no
  churn; only the open PR is reused. This is expected create-if-absent behavior, not a cadence
  violation; once Eduardo merges, the leg goes `unchanged` when stable.

## Falsification (SDMG Protocol 7)

The DESIGN passed two harsh-reviewer rounds (v1 REJECT -> v2 SURVIVE-WITH-CHANGES, all adopted;
recorded in the spec's Falsification section). The 3rd pass ran on the BUILT code (2026-06-03) and
specifically attacked the new vault lint-status leg (sec 5).

**Round 3 -- BUILT-CODE verdict: SURVIVE-WITH-CHANGES (no P0).** The three load-bearing safety
claims HELD under direct attack: (a) `parse_vault_report` confirmed clock-free (no `now` param;
severity + payload_hash from BLOCK/WARN/nonzero CONTENT only -- contrast the KILLED clock-dependent
`parse_eng_graph_moc`); (b) create-if-absent splice is byte-idempotent (no timestamp in body; the
real builder's branch-level base64 dedup skips the PUT on identical content -> no new commit / no
new Trace-Id / no churn); (c) the sovereign vault write is branch+PR-only -- no `/merge` route in
any path of the REAL builder, pinned by the negative test. Adopted (pre-commit "se rigetta adotto,
non difendo"):
- **P1.1** -- rescoped the `is_doctrine` docstring: it is a fail-closed WRITE-REFUSAL SUPERSET of
  the static carve-out subset, NOT the canonical ADR-0038 classifier (which uses a positive
  ALLOW-list for global `~/.claude/`). Over-refusal is fail-safe for a write-gate; the claim was
  scoped down. Do not reuse for allow-decisions.
- **P1.2** -- added a construction-site note in `build_reconcilers` that adding ANY leg REQUIRES a
  recorded Eduardo doctrine-classification review (the content catch-all is human, not the static
  `__post_init__` backstop); filled this verdict line.
- **P1.3** -- extended the negative merge source-scan to ALSO cover `reconcile_actor` +
  `real_gh_api`, and added a test pinning `real_gh_api().keys() == {get_file, open_or_update_pr}`
  -- so a future merge call in the actor or a merge callable exported from the factory goes CI-red
  (closing the one real gap in the load-bearing test's coverage boundary).
- **P2.1** -- dropped the accept-then-ignore `argv` from `main()` (CWE-214 hygiene -- token is
  env-only); **P2.2** -- documented the create-if-absent reused-PR behavior (Consequences, below).
Held with no change: merge-block (3-part), clock-free render, fail-closed token, anti-self-licking
externality, doctrine `__post_init__` fail-closed.

## References

- ADR-0037 (merge-autonomy model -- dec.4 named this rung), ADR-0038 (doctrine carve-out used by
  `is_doctrine`), ADR-0036 (orchestration doctrine / monoculture), ADR-0011 (commit trailers),
  ADR-0021 (ASCII), ADR-0026 (Protocol 7 SDMG).
- `docs/governance/actor-activation-criteria.md` (rungs; sec 3 R1->R2; sec 4 anti-self-licking;
  sec 6 clean-cycle; sec 7 doctrine=Eduardo-merge) -- activation note added alongside this ADR.
- The proven open-PR shape generalized: `tools/playtest2-board-sync.sh`.
- memory `feedback_external_repo_action_boundary` (sovereign/external write boundary).
