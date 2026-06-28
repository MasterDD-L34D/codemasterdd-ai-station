# ADR-0039 — R1 open-PR reconcile rung

> Status: **Accepted** 2026-06-11 (Eduardo; ratify dossier
> `docs/research/adr-0038-0039-ratify-dossier-2026-06.md` -- ACCEPT with amendment P1
> clock-free rescope + 3 R2 annotations, applied below). Proposed 2026-06-03. 3rd SDMG
> harsh-reviewer falsification on the BUILT code
> (Cognitive Protocol 7) done 2026-06-03 -- see "Falsification". This is a doctrine file
> (`docs/adr/**`) = Eduardo-only-merge per ADR-0037 dec.2 / ADR-0038, so the hub does NOT
> self-merge it (ratify PR merge = Eduardo). Implements the rung ADR-0037 dec.4 named as the
> (then-unbuilt) unblocker.
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
shipped issue actor (`act.py:run_r1`); both coexist. **Clock-free rescope (ratify amendment P1,
2026-06-11):** the clock-free claim holds for the RENDER and for the vault leg; the codemasterdd
STATUS leg has time-derived severity UPSTREAM of the render (eng-graph staleness band), so
STATUS-leg PR-cycles do NOT count toward R2 until that leak is fixed -- see dec.1.
**[Update 2026-06-28: that leak was FIXED by #333 (render mask, 2026-06-11); STATUS-leg
STEADY-STATE PR-cycles now count toward R2. See Addendum 2026-06-28.]**

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

**Ratify amendment P1 (2026-06-11, dossier P1-1 -- empirically confirmed).** Clause (2)'s "no
wall-clock" holds for the RENDER (no `now` parameter) and for the vault leg (content-derived
severity, dec.5). It does NOT yet hold end-to-end for the codemasterdd STATUS leg: the
`vault-eng-graph` severity is time-derived UPSTREAM of the render (`ingest.py`
`date.today()` -> `parse_eng_graph_moc(now)` -> staleness band info/warning/error ->
`payload_hash`), so a byte-identical source can yield a calendar-only region diff and open a PR
(probe 2026-06-11: same content, `now` +40 days -> severity info->warning, different region
row). Consequence: **STATUS-leg PR-cycles do NOT count toward R2 until the leak is fixed**
(equivalently: only vault-leg cycles count). The 2 cycles already banked (#296/#252) remain
valid as bootstrap-class evidence (the #296 diff was the region CREATION, not a staleness
flip). Safety is untouched: the no-merge 3-lock (dec.4) does not depend on clock-freedom; the
leak affects R2 EVIDENCE QUALITY only.

> **[Update 2026-06-28 -- leak FIXED, this exclusion LIFTED. See Addendum 2026-06-28.]** The
> leak was sealed by #333 (2026-06-11) at the render boundary: `render_status_multi_repo` now
> MASKS the time-derived severity cell for `vault-eng-graph`, so a calendar-only flip yields a
> byte-identical region and opens NO PR. The STATUS reconciler diffs that masked render
> (`build_reconcilers` -> `render=render_status_multi_repo`), so the leak cannot reach the
> PR-open decision. STATUS-leg STEADY-STATE PR-cycles therefore now count toward R2 (bootstrap
> #296 still excluded per annotation (b)). The dec.1 reasoning above is preserved as the
> pre-fix record.

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

## Ratify annotations for the future R2 ADR (2026-06-11)

Recorded at ratification (Eduardo 2026-06-11; source: ratify dossier, sec "Annotazioni R2").
Binding inputs for the future R2 ADR, alongside (a) = the amendment P1 clock-free rescope in
dec.1/TL;DR:

- **(b) Evidence class -- bootstrap vs steady-state:** create-if-absent PRs (bootstrap) and
  steady-state-drift PRs are DIFFERENT evidence classes; R2 needs the latter. The 2 banked
  cycles (#296/#252) are bootstrap-class (the first run CREATED the region/file). Suggested
  reading of dec.7/dec.8: "create-PRs and steady-state drift PRs are different evidence
  classes; R2 needs the latter".
- **(c) Human-merge attribution is not machine-provable:** no native git/gh signal
  distinguishes "Eduardo at the keyboard" from a hub session using the same account's ambient
  auth. The `merged_by_human` field of `reconcile_cycles_report.is_clean_cycle` is populated
  EXTERNALLY; the R2 count is worth exactly as much as whoever populates it.
  "Human-merge-only" remains operator discipline + post-hoc git audit, not enforcement by
  construction (branch protection unavailable: HTTP 403 re-verified 2026-06-11).
- **(d) Prolonged no-run = no-run, NOT no-drift (off-ramp honesty):** cadence is manual
  (`python -m governor.reconcile`, no cron per dec.8); no re-run since 2026-06-03, so current
  silence is absence of runs, not evidence of stability. Maturing the earn requires periodic
  manual runs -- OR the prolonged non-run is read honestly as the off-ramp signal that the
  class is unnecessary.

## Addendum 2026-06-11 -- stale-branch GC (vault #258 incident, same-day P2)

First post-ratify cadence run, same day as the ratification: the codemasterdd leg opened
cleanly (#336, human-merged), but the vault leg opened PR #258 CONFLICTING. Root cause
(ground-truth verified): the actor reuses the FIXED branch `auto/governor-reconcile-<id>`;
the vault branch was a leftover of merged PR #252 (2026-06-03 -- vault has no
delete-on-merge), so the new PR carried the OLD merge-base -> add/add conflict
(`Atlas/lint-status.md` exists on main since #252). Same failure family as the fold-race
lesson (push onto a branch whose PR already merged).

Fix shipped same day (PR #340, TDD + harsh-review SURVIVE-WITH-CHANGES adopted): the
builder enforces the invariant **branch-exists <=> open-PR-pending** -- the open-PR lookup
moved BEFORE any write; on branch-already-exists with ZERO open PRs the ref is force-reset
to the current base sha (garbage-collecting the actor's own dead commits); a LIVE branch
(open PR) is never reset (anti-churn); a failed lookup never resets (no destruction on
doubt). The `auto/governor-reconcile-*` namespace is actor-exclusive by contract: a human
commit parked there without an open PR is GC'd by design. The dec.4 merge-block is
untouched: `PATCH git/refs` is not a merge route; the negative tripwire + the pinned
`real_gh_api` surface stay green. Operationally: the conflicted #258 is closed (Eduardo)
and replaced by a fresh-branch PR from the fixed builder; the conflicted-PR episode is NOT
a failed clean cycle (sec 6 counts merged-then-reverted/followed-up PRs, not a never-merged
artifact PR), but it IS evidence for annotation (b): bootstrap/create-class mechanics carry
sharp edges that steady-state cycles must not inherit.

## Addendum 2026-06-28 -- STATUS-leg clock-leak FIXED (#333); dec.1 exclusion LIFTED

**Currency correction (ground-truthed 2026-06-28).** dec.1 / ratify-amendment-P1 (2026-06-11)
flagged that the codemasterdd STATUS leg still leaked the calendar (time-derived `vault-eng-graph`
severity upstream of the render) and therefore STATUS-leg PR-cycles did NOT count toward R2. That
leak was **FIXED the same day** by PR **#333 `fix(governor): mask time-derived severity in STATUS
render (ADR-0039 P1)` (35b2122, 2026-06-11 11:25, on origin/main)** -- but dec.1's text was never
amended, so the ADR (and downstream notes, incl. the 2026-06-24 merge-authority memory) kept
asserting the stale "STATUS-leg does not count / only vault-leg counts" claim for ~2.5 weeks. This
addendum closes that doctrine-vs-code gap (a currency-gate-class stale-pull: git recency > doc
authority; memory `feedback_currency_gate`).

**What #333 actually does (verified, not assumed).** `render_status_multi_repo` (governor/
reconcile.py) MASKS the `severity` cell for the time-derived source set
`_TIME_DERIVED_SEVERITY_SOURCES = {vault-eng-graph}` (cell text `(masked: time-derived)`), so a
calendar-only severity flip (info->warning) produces a BYTE-IDENTICAL rendered region. The STATUS
reconciler diffs exactly that masked render (`build_reconcilers` -> `status_block` with
`render=render_status_multi_repo`), so a calendar tick can no longer reach the PR-open decision.
The leak is sealed at the actor's decision boundary, not merely cosmetically. Guardrails (both
green 2026-06-28): `test_render_status_stable_across_staleness_boundary` (calendar advance ->
identical render) + `test_time_derived_severity_sources_pin_matches_parsers` (the mask source-set
stays pinned to the now-aware parsers, so a future now-aware parser added without masking goes
CI-red). Today severity is the only `now`-absorbing rendered column:
produced_at/summary/source/ref derive from MOC content, not the clock (the `parse_eng_graph_moc`
contract, parsers.py; produced_at = the artifact's own `last_verified`, never `now`). A future
parser leaking the calendar into summary/produced_at would reopen P1-1 -- caught by
`test_render_status_stable_across_staleness_boundary` (parser-routed) and pinned by
`test_time_derived_severity_sources_pin_matches_parsers`.

**Decision.** The dec.1 exclusion is **LIFTED**: STATUS-leg **STEADY-STATE** PR-cycles now count
toward R2 alongside vault-leg cycles. Unchanged: (1) the 2 banked cycles (#296/#252) stay
**bootstrap-class** and do NOT count (annotation (b) -- R2 needs steady-state drift, not
create-PRs); (2) the stored severity is still time-derived -- only the RENDER (hence the PR
evidence) is clock-free, which is all R2 evidence quality requires; the staleness band keeps
working for the ISSUE actor (worsened-delta reads the store, not this render); (3) this addendum
grants NO autonomy and earns NO rung -- R2 still requires >=4 clean STEADY-STATE cycles across
>=2 repos over >=2 weeks + the rest of actor-criteria sec 3 + its own R2 ADR. It only removes the
codemasterdd-leg DISQUALIFIER so the 2nd repo can contribute the cycles the ">=2 repos" condition
needs. No reconcile run has happened since 2026-06-03, so zero steady-state cycles are banked on
EITHER leg today (annotation (d): no-run != no-drift); maturing the earn requires periodic manual
`python -m governor.reconcile` runs.

**Doctrine-file (this ADR) = Eduardo-only-merge** (ADR-0037 dec.2 / ADR-0038); delivered as
branch+PR, NOT hub-self-merged. SDMG Protocol-7 harsh-review of this currency correction recorded
in the Falsification section below.

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

**Round 4 -- Addendum 2026-06-28 currency correction: SURVIVE-WITH-CHANGES (no P0).** harsh-reviewer
traced the actor diff path (`splice(current, render(store))`, reconcile.py) and confirmed the STATUS
leg diffs the MASKED render only (no raw-store severity path), so the leak is sealed at the PR-open
decision, not merely cosmetic; confirmed `parse_eng_graph_moc` is the ONLY now-aware parser (pinned)
and severity its only `now`-absorbing rendered column; confirmed the addendum grants no rung and
keeps the bootstrap-exclusion orthogonal. One P1 adopted: softened an over-confident absolute
("severity was the only leak vector") to the accurate "true-today + regression-guarded" claim
(parse_eng_graph_moc contract + the two render-stability/pin tests). P2 (extend the staleness-
boundary test to also straddle the error band) noted, deferred -- not a leak (the mask is
severity-value-agnostic).

## References

- ADR-0037 (merge-autonomy model -- dec.4 named this rung), ADR-0038 (doctrine carve-out used by
  `is_doctrine`), ADR-0036 (orchestration doctrine / monoculture), ADR-0011 (commit trailers),
  ADR-0021 (ASCII), ADR-0026 (Protocol 7 SDMG).
- `docs/governance/actor-activation-criteria.md` (rungs; sec 3 R1->R2; sec 4 anti-self-licking;
  sec 6 clean-cycle; sec 7 doctrine=Eduardo-merge) -- activation note added alongside this ADR.
- The proven open-PR shape generalized: `tools/playtest2-board-sync.sh`.
- memory `feedback_external_repo_action_boundary` (sovereign/external write boundary).
- Ratify dossier `docs/research/adr-0038-0039-ratify-dossier-2026-06.md` (2026-06-11: evidence
  check + harsh-review SDMG run + P1-1 empirical probe; source of amendment P1 and the R2
  annotations (b)-(d)).
