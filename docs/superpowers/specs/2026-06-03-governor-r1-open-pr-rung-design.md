# Governor R1->open-PR rung -- design spec (the reconcile-PR earn-path)

> **Status (2026-06-23):** shipped -- R1 open-PR reconcile rung live (R2 earn-window active)

> Status: DRAFT v4 2026-06-03. Author: Claude (Opus 4.8) on Lenovo.
> SDMG (Cognitive Protocol 7) gate PASSED: v1 -> REJECT, v2 -> SURVIVE-WITH-CHANGES; all
> surviving harsh-reviewer findings adopted; ground-truth re-verified via gh api. **Eduardo
> decisions resolved 2026-06-03: D1 = (d) build a vault lint-status reconciler (NEW
> governor-owned doc in vault, EXPLICIT OK granted); D2 = new small ADR; D4 = build NOW (rung
> GO, do not wait for off-ramp acted-on>=3).** Pending: `superpowers:writing-plans` -> build
> (NEXT session per seed), behind the rung's own PR + its own ADR + a 3rd harsh-reviewer pass
> on the BUILT code (which MUST specifically falsify the new vault lint-status leg, sec 5.2).
> **This spec defines no rules and grants no autonomy by itself** -- the rung only OPENS PRs;
> auto-merge (R2) stays OFF, earned later via its own ADR.
> ASCII-first body (ADR-0021). Authority: ADR-0036 + ADR-0037 (dec.4) + ADR-0038 +
> `docs/governance/actor-activation-criteria.md`. Seed:
> `docs/superpowers/specs/2026-06-03-governor-r1-open-pr-rung-SEED.md`.

## 0. Honesty preamble (SDMG)

- This is the **R1 branch+PR variant** for the journal/doc-reconcile class. R1 is already
  defined (actor-criteria sec 1: "R1 = CLASSIFY + open a branch+PR / emit a drift
  escalation"); the SHIPPED R1 chose the issue-escalation variant (scope A, 2026-06-02),
  which accrues ZERO clean PR-cycles BY DESIGN (sec 6 addendum). This rung adds the PR variant
  so the R2 evidence stream (>=4 clean PR-cycles) can begin. It does NOT touch the issue actor
  (different signal->action mapping; both coexist).
- **Building this rung is itself reversible + an experiment** (mirrors the R0 off-ramp logic):
  the rung only OPENS PRs; a human merges. If reconcilers rarely fire, or Eduardo declines to
  merge them, that is the honest off-ramp signal that auto-merge of this class is NOT needed --
  the rung must SURFACE that, never manufacture churn to look productive.
- **No autonomy is granted here.** Auto-merge (R2) stays OFF, behind its own dedicated R2 ADR +
  the mechanical conditions (actor-criteria sec 3). `.claude/settings.json` ceiling is UNCHANGED
  (`git push origin claude/*`, no merge allow-rule).
- **Two BUILT reconcilers (post-decision):** (1) codemasterdd `STATUS_MULTI_REPO.md` signal
  snapshot (sec 5.1), (2) vault lint-status index (sec 5.2, D1=(d), Eduardo OK). Both are
  deterministic, **clock-free**, state-keyed, marker-bounded, NON-doctrine. The SDMG re-review
  KILLED the eng-graph staleness band-flag (it fired on a clock-tick); the vault lint-status leg
  is the clock-free alternative (vault lint severity is content-based, not time-based -- sec 5.2).

## 1. The gap this closes

ADR-0037 dec.4 (Accepted): standing external-merge is reachable ONLY via the governor
R0->R1->R2 earn-path, which is "currently UNREACHABLE -- the R1->open-PR rung that would emit
the required >=4 clean PR-cycles does not yet exist." This spec defines that rung (its core
deliverable: the governor opens REAL deterministic reconcile PRs a human merges).

```
R0 (shipped)        R1-issue (shipped)         R1-PR (THIS spec)          R2 (future ADR)
ingest+persist  ->  classify -> 1 GH issue  +  reconcile -> branch+PR  ->  auto-merge class
read-only pane      (error/regression)         (journal/doc-reconcile)     (gated, earned)
                    0 clean-PR-cycles           HUMAN merges each PR        needs >=4 clean
                    feeds acted-on only         -> clean cycles accrue       cycles + own ADR
```

## 2. Approaches considered

Scope set by Eduardo 2026-06-03: codemasterdd + vault, with D1=(d) -- a vault lint-status doc as
the 2nd leg. The real fork is **where the reconcile diff comes from** -- which decides whether
the clean-cycle evidence is trustworthy enough to later license auto-merge.

- **A (CHOSEN) -- Deterministic reconcile actors, governor-routed, change-triggered.** Each
  reconciler is a pure, **clock-free** function `(governor signals + current marker region) ->
  new marker region`; a change opens a branch+PR (the proven `playtest2-board-sync` shape
  generalized); identical -> no-op. **No LLM in the diff path.** The "clean cycle" is then
  genuinely mechanical (git facts), and the class is safe to later auto-merge because the diffs
  are deterministic + bounded to a marker region. Tradeoff: fires only on real drift -> slow
  accrual.
- **B -- Deterministic + LLM-semantic (wire `sot-drift-verifier` as a reconcile actor).** Richer
  reconciles, fires more often -> faster R2 evidence. REJECTED for the ENTRY rung: an LLM (Claude)
  in the diff path, judged by a same-family classifier, CONTAMINATES the clean-cycle evidence the
  R2 auto-merge gate exists to require (partial monoculture, ADR-0036 sec 7). The diff becomes
  semi-self-assessed. Deferred to a future R3 rung, AFTER a different-family judge (fleet-tools
  `cross_check`) is wired. Using B's diffs to earn the R2 that is supposed to gate B is circular.
- **C -- Issue-attached patch (status-quo+).** Keep R1 issue-only; attach the deterministic diff +
  an apply command in the issue body; Eduardo one-clicks. REJECTED: issues are not PRs (sec 6
  addendum) -> ZERO clean-PR-cycles -> does NOT unblock R2 -> fails the goal. Its honesty is folded
  into A (sec 0: if even A rarely fires, that is the off-ramp answer).

## 3. Architecture

New code lives in `apps/cross-repo-dashboard/governor/` (extends the shipped R0/R1 governor;
non-doctrine path, but the rung-activating PR is Eduardo-merged per sec 9, being an autonomy
increment). The issue actor (`act.py:run_r1`) is UNCHANGED. The BUILT reconciler set =
`[status-multi-repo, vault-lint-status]` (sec 5).

### 3.1 Units (design-for-isolation; each independently testable, narrow interface)

- **`reconcile.py` -- `Reconciler`** (a small dataclass/record):
  - `id: str` (stable: `status-multi-repo`, `vault-lint-status`).
  - `repo: str` (`MasterDD-L34D/codemasterdd-ai-station` | `MasterDD-L34D/vault`).
  - `path: str` (the target doc).
  - `marker: (begin: str, end: str)` (the GOVERNOR-SYNC region; human prose outside it is NEVER
    touched).
  - `render(store) -> str | None`: PURE (reads signals from the store; no network, no write, **no
    wall-clock**). Returns the new marker-region body, or `None` = "cannot compute" -> the actor
    skips this reconciler (no-op, never a junk PR). Deterministic: same store state -> same string.
    **A reconciler MUST NOT render any value derived from the current time** (sec 6.3) -- both
    built legs satisfy this (signal-STATE only; vault lint severity is content-based, sec 5.2).
  - **Doctrine guard, fail-closed AT CONSTRUCTION**: `__post_init__` asserts
    `not is_doctrine(path, repo)` (sec 4.2). A reconciler aimed at a doctrine path refuses to
    exist -> a config error fails fast, never silently opens a doctrine PR.

- **`reconcile.py` -- `splice(doc_text, marker, new_region) -> str`**: pure. Idempotent replace of
  the BEGIN..END region (re.DOTALL, count=1); first-time injection appends the block at a defined
  anchor (after a named heading); **if the target file does not exist (new vault doc, sec 5.2),
  create it with minimal frontmatter + heading + the block**. No timestamps inside the region body
  (idempotency; sec 6.4).

- **`reconcile.py` -- `reconcile_actor(store, reconcilers, gh_api) -> dict`**: the only new
  autonomy surface. For each reconciler (isolated; one failure never aborts the rest, mirroring
  `ingest_all`):
  1. `current = gh_api.get_file(repo, path)` (read; contents API; "" if the file does not exist).
  2. `new_region = R.render(store)`; if `None` -> record skip, continue.
  3. `patched = splice(current, R.marker, new_region)`.
  4. if `patched == current` -> **no-op** (no drift; NO branch, NO PR; record `unchanged`).
  5. else: `assert not is_doctrine(R.path, R.repo)` (runtime re-check, defence in depth);
     `gh_api.open_or_update_pr(repo, branch=f"auto/governor-reconcile-{R.id}", base="main", path,
     patched, commit_msg, pr_title, pr_body)` -- **NEVER merges**.
  - Returns `{"opened": [...], "unchanged": [...], "skipped": [...], "errors": [...]}`.
  - `__main__`: `python -m governor.reconcile` (manual; cron promotion = Fase-4, out of scope).

- **`gh_api` (injected dict of callables)** -- real implementation uses the GitHub REST
  contents+pulls API (clone-agnostic; works for vault without a local vault clone). Tests inject a
  FAKE -> network/gh NEVER hit in tests. Real callables:
  - `get_file(repo, path) -> str` (contents API, base64-decoded; returns "" on 404 so a new-doc
    reconciler can create it; raises on other non-200 so the actor skips rather than corrupting).
  - `open_or_update_pr(...)`: get base SHA -> create/update the branch ref -> PUT file contents on
    the branch -> find an open PR for the branch (reuse) else `gh pr create`. **The real command
    builder NEVER emits a merge route/flag** (`pr merge` / `--merge` / `--admin` / REST merge);
    pinned by a negative test against the REAL builder, not only the fake (sec 6.2 / 10). Commit
    message carries policy-C trailers (`Coding-Agent:` + `Trace-Id:` uuidv7, NO `Co-Authored-By`).

### 3.2 Data flow

```
governor.db (signals; populated by the R0 ingestor -- unchanged)
      |
      v
reconcile_actor(store, [R_status, R_vault_lint], gh_api)
   per reconciler:
      current  = gh_api.get_file(repo, path)        # "" if new doc (404)
      region   = R.render(store)                     # deterministic, NO wall-clock; None -> skip
      patched  = splice(current, R.marker, region)   # create-if-absent for the new vault doc
      if patched == current: NOOP                    # honest cadence: no drift -> no PR
      else:
          assert not is_doctrine(R.path, R.repo)     # ADR-0038 fail-closed
          gh_api.open_or_update_pr(...)              # branch+PR, NEVER merge
      |
      v
   ONE open PR per reconciler (max), branch auto/governor-reconcile-<id>
      |
      v
   EDUARDO merges (human-irreducible during earn -- sec 6.1; vault = sibling-peer Eduardo-only)
      |
      v
   clean-cycle accounting (EXTERNAL, mechanical, read-only -- sec 7.1; NOT in the actor)
```

## 4. The reconcile class -- precise definition

### 4.1 What qualifies (journal/doc-reconcile ONLY)

A doc qualifies for an auto-reconciler IFF ALL hold:
1. The reconciled region is **bounded by GOVERNOR-SYNC markers**; human prose outside them is
   never touched.
2. The region body is a **deterministic pure function of signals the governor already holds** in
   `governor.db` (no LLM, no external judgement, no governor-private source, **no wall-clock**).
3. The doc is **NON-doctrine** per ADR-0038 (sec 4.2) -- so promoting the CLASS to R2 auto-merge
   can never auto-merge a doctrine file.
4. The change is **reversible** (a marker-region edit; `git revert` clean) and **low-risk**
   (status/snapshot content, not behaviour, not rules).

Explicitly OUT: code, behaviour, config, anything LLM-generated, anything time-derived, anything
outside a marker region, and every doctrine file (sec 4.2). R3+ wider classes = separate future
ADRs.

### 4.2 Doctrine exclusion (ADR-0038) -- a static gate + a human review checkpoint

`is_doctrine(path, repo) -> bool` is a STATIC path-classifier that returns True for ANY of
(complete vs ADR-0038's Decision set):
- globs: `docs/adr/**`, `docs/governance/**`, repo `.claude/**`,
  **`Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/**`** (the hub
  autonomous-change envelope -- a BLOCKING add in ADR-0038's own falsification; v1 OMITTED it);
- named root rule files: `CLAUDE.md` (any level), `AGENTS.md`, `ORCHESTRATION.md`, `GOALS.md`,
  `DECISIONS_LOG.md`, `OPEN_DECISIONS.md`;
- `~/.config/aider-privacy-whitelist.txt` and the ADR-0038 `~/.claude/` governance subpaths.

**The ADR-0038 content-based catch-all is NOT an executable code path** -- a pure
`is_doctrine(path, repo)` cannot evaluate "am I uncertain". It is a **human process checkpoint**:
adding ANY new reconciler to the class REQUIRES an explicit Eduardo doctrine-classification review
of its target (recorded in the rung's ADR / a follow-up). The code's fail-closed `__post_init__`
assert enforces only the static set; the catch-all is enforced by that human review. (The new
vault `lint-status.md` target, sec 5.2, was Eduardo-reviewed 2026-06-03 = non-doctrine vault
status index.)

Consequence for the built targets:
- `STATUS_MULTI_REPO.md` -- explicitly NON-doctrine in ADR-0038 -> OK.
- vault `Atlas/lint-status.md` (new) -- a vault status index, not a hub rule file -> NON-doctrine.
- `docs/governance/EXECUTION-BOARD.md` -- under `docs/governance/**` = DOCTRINE -> EXCLUDED (why the
  codemasterdd leg targets `STATUS_MULTI_REPO.md`, not the board; the standalone board-sync cron is
  a separate concern, sec 12.3).

A unit test asserts `is_doctrine` returns True for a sample of EACH carve-out class (including
`Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/**`) and False for the two built targets; a
reconciler constructed against a doctrine path must raise.

## 5. The two built reconcilers

### 5.1 `status-multi-repo` (codemasterdd) -- reliable, deterministic, clock-free

- repo: codemasterdd; path: `STATUS_MULTI_REPO.md`; marker:
  `<!-- GOVERNOR-SYNC:signals BEGIN -->` .. `<!-- GOVERNOR-SYNC:signals END -->`.
- `render(store)`: a compact ASCII markdown table from `store.latest_per_source()` -- columns
  `source | severity | summary | produced_at | ref`, ordered by source, + a trailing italic line
  "Auto-synced governor signal snapshot; human prose elsewhere is authoritative." **NO timestamp /
  no time-derived value** (the change-key is the signal STATE only -> no clock-tick, sec 6.3).
- Fires when any source's latest signal state changes (real drift). Reliable leg: data is
  governor-owned, transform is pure + clock-free, drift is genuine.
- First run injects the marker block (after a defined heading). Subsequent runs replace the region.
- **Useful consumer, not churn:** `STATUS_MULTI_REPO.md` is the COMMITTED cross-repo dashboard
  Eduardo + agents read at session start (CLAUDE.md reading order); the R0 Flask pane is
  machine-local only. (If Eduardo judges it redundant with the pane, pick another non-doctrine
  committed doc rather than churn.)

### 5.2 `vault-lint-status` (vault) -- D1=(d), the clock-free 2nd leg (Eduardo OK 2026-06-03)

- repo: vault; path: `Atlas/lint-status.md` (NEW governor-owned doc; exact location confirmable at
  build -- `Atlas/` index style proposed); marker:
  `<!-- GOVERNOR-SYNC:lint BEGIN -->` .. `<!-- GOVERNOR-SYNC:lint END -->`. First run CREATES the
  file (minimal MoC frontmatter + heading + the marker block).
- `render(store)`: a table from the three vault lint signals already ingested -- `vault-gap`,
  `vault-coherence`, `vault-whatsmissing` (`store.latest_per_source()` filtered to those sources):
  columns `report | severity | summary | produced_at | ref`. Pure + **clock-free**.
- **Why this is clock-free (the falsification fix, vs the killed band-flag):** `parse_vault_report`
  (parsers.py) derives severity from CONTENT -- `BLOCK: N` / `WARN: N` / nonzero summary metrics --
  with NO `now` parameter, and `payload_hash` keys on (source, produced_at, findings, block, warn).
  So the lint signal STATE changes only when the vault lint report content changes, NEVER because
  the calendar advanced. (Contrast the eng-graph staleness band, which `parse_eng_graph_moc`
  computes from `now - last_verified` -> clock-tick -> KILLED in v3.)
- Fires when a vault lint report's state changes (a real gap/coherence/whatsmissing drift). Higher
  cadence than the rejected eng-graph leg (lint reports change with vault content), and genuinely
  deterministic. Real consumer value: a committed vault-side lint dashboard.
- **Accepted cost (Eduardo OK):** introduces a governor-owned doc in the SOVEREIGN vault repo (the
  "manufactured write-target" smell flagged at D1). Mitigated: it is a real consumer artifact (like
  STATUS_MULTI_REPO for codemasterdd), marker-bounded (governor owns only the block), NON-doctrine,
  branch+PR only, **merge Eduardo-only** (vault sibling-peer, ADR-0038).
- **Build-phase SDMG note:** this leg is a self-designed addition made AFTER the design
  falsification. The 3rd harsh-reviewer pass (on the BUILT code, next session) MUST specifically
  falsify it: confirm `parse_vault_report` is truly clock-free, the new-doc creation/injection is
  safe + idempotent, and the sovereign-repo write respects sibling-peer (branch+PR, never merge).

## 6. Safety, reversibility, invariants

### 6.1 Human-merge-only during the earn (load-bearing)

The rung OPENS the PR; a HUMAN (Eduardo) merges every reconcile PR. **The hub MUST NOT self-merge
reconcile-class PRs during the earn window** -- not even codemasterdd non-doctrine ones that
ADR-0037 dec.1 (classifier-per-call) would otherwise permit -- because a CLEAN R1 cycle
(actor-criteria sec 6) is defined as **merged by a human**. A hub-merged reconcile PR would
(correctly) NOT count. The reconcile actor never calls merge; Eduardo disposes. (vault PRs are
Eduardo-only regardless, sibling-peer.) After R2 is earned, the R2 ADR enables auto-merge of the
class; not before.

### 6.2 No merge capability exercised -- the merge-block is code + invariant + ceiling ONLY

The actor never calls a merge endpoint/command. **There is NO branch-protection backstop**:
codemasterdd is a PRIVATE free-tier repo, so branch protection is unavailable (gh api
`branches/main/protection` -> HTTP 403 "Upgrade to Pro", verified 2026-06-03 -- the same free-tier
gap that sank the killed auto-merge-grant draft). So the merge is blocked by exactly THREE things,
all of which must hold: (a) the actor code never calls merge -- pinned by a negative test against
the **REAL** `open_or_update_pr` command builder (not only the injected fake, so a future
merge-path addition goes CI-red; sec 10); (b) the human-merge-only invariant (6.1); (c) the
unchanged `.claude/settings.json` ceiling (no merge allow-rule). The token (sec 8) is NOT a
merge-block (it is merge-capable). No platform defence-in-depth -> the negative test + the rung's
code review are load-bearing.

### 6.3 No manufactured churn (anti-self-licking at the cadence level) -- INVARIANT-TRUE

Reconcilers fire ONLY on real signal-STATE change (sec 3.1 step 4: identical -> no-op). **No
reconciler renders any time-derived value** (sec 3.1 / 4.1): BOTH built legs key on signal state
only (the codemasterdd snapshot; the vault lint severity is content-based per `parse_vault_report`,
sec 5.2). The clock-tick-fragile eng-graph band-flag is NOT built (KILLED v3). So a PR opening
always corresponds to a real content change, never to the calendar advancing. The clean-cycle's
7-day no-revert + no-same-line-follow-up windows (sec 7.1) are the mechanical backstop if a
low-value diff still slips through.

### 6.4 Idempotency

Identical signal state -> identical rendered region -> `patched == current` -> no-op (no PR). Max
ONE open PR per reconciler (reuse the open PR for `auto/governor-reconcile-<id>`; force-with-lease
push updates it). Mirrors the issue actor's "max 1 open issue."

### 6.5 Fail-closed token + degrade-to-no-op

No `GOVERNOR_RECONCILE_TOKEN` -> the actor refuses to open PRs (logs + no-op). Unlike the read-ish
issue actor, a WRITE actor does NOT fall back to the ambient over-privileged `gh auth`. Any
fetch/render/splice failure on one reconciler -> that reconciler no-ops; the run never crashes and
never opens a junk PR (board-sync's defensive contract).

## 7. Evidence accrual toward R2

### 7.1 Clean-cycle accounting is EXTERNAL + mechanical -- and proves LESS than it looks

The actor's own output MUST NOT feed its own promotion (actor-criteria sec 4 anti-self-licking).
The clean-cycle COUNT is computed OUTSIDE the actor, read-only, from git/gh history at R2-decision
time (manual + auditable). An optional helper `reconcile_cycles_report.py` MAY render the audit
(read-only; advisory; not a gate input; writes nothing). A clean cycle (actor-criteria sec 6) = a
reconcile PR (a) merged by Eduardo, (b) not reverted within 7 days, (c) no follow-up fix touching
the same lines within 7 days.

**Honest scope of what these cycles prove (falsifier P1.1):** a reconcile PR is a BOUNDED
marker-region diff, near-zero-judgment to merge. So N clean cycles demonstrate **renderer
DETERMINISM + REVERT-SAFETY**, NOT **merge-JUDGMENT-safety**. Therefore the R2 ADR must NOT treat
these cycles as "a human vetted each merge"; it must justify auto-merge on **reversibility +
class-restriction + the mechanical drop-check + a CI-watchlist** (actor-criteria sec 3) -- the
cycles are a NECESSARY field-signal (the class ran cleanly), not a SUFFICIENT one.

### 7.2 The ">=2 repos" requirement -- 2 real sources now exist; distribution DEFERRED to R2 ADR

With D1=(d), there are TWO reliable repo sources: codemasterdd (`STATUS_MULTI_REPO`) + vault
(`lint-status`). So `>=2 repos` (actor-criteria sec 3) is now mechanically REACHABLE. But this spec
does NOT pre-decide the exact distribution (">=4 across >=2" -- e.g. 3+1, or 2+2): that is the R2
ADR's to ratify, with real cadence data in hand (v1 bent the reading to fit a weak leg; corrected).
The entry rung delivers both legs + the cycle streams; R2 judges sufficiency.

### 7.3 Honest cadence + the off-ramp

Deterministic + change-triggered => the rung is SILENT when nothing drifts. If, over the R2 window,
reconcilers fire rarely / 0 clean cycles accrue, that is the off-ramp evidence that auto-merge of
this class is unnecessary. The rung records this honestly (advisory log / pane: "reconcile actor
silent N weeks, 0 drift") and never inflates activity. R2 stays unreached until the evidence
genuinely exists -- a principled hold, not a stall (ADR-0037 dec.4).

## 8. Token + permissions

- `GOVERNOR_RECONCILE_TOKEN`: a fine-grained PAT scoped `contents:write` + `pull_requests:write` on
  EXACTLY `codemasterdd-ai-station` + `vault` (D1=(d)) -- NO admin, NO merge-queue, NOTHING else.
  Passed to any child via env (`GH_TOKEN`), NEVER argv (CWE-214). Minting is a human step
  (account-credential = human-irreducible).
- **Residual, stated bluntly:** a `pull_requests:write` PAT CAN technically merge via the REST API.
  The token is NOT a merge-block. Combined with the no-branch-protection reality (6.2), the ONLY
  things stopping a merge are code (negative test on the REAL builder) + the human-merge-only
  invariant + the unchanged settings ceiling. No platform defence-in-depth -> the R2 ADR must weigh
  "no branch protection" before enabling any auto-merge.
- `.claude/settings.json`: UNCHANGED. No merge allow-rule. (Adding one is an R2-ADR matter.)

## 9. SDMG application (Cognitive Protocol 7)

1. **DESIGN = hypothesis** (v4, post two falsification rounds + Eduardo decisions).
2. **TEST = ground-truth reads** (necessary, not sufficient): the shipped governor code
   (`act.py`/`store.py`/`ingest.py`/`parsers.py`, incl. that `parse_vault_report` is clock-free
   while `parse_eng_graph_moc` is not), the proven `playtest2-board-sync` shape, the repo's only 2
   workflows (no merge-cron -- verified 2026-06-03), ADR-0037/0038, actor-criteria, the boundary
   memory, the LIVE vault MOC + the codemasterdd branch-protection state via gh api.
3. **FALSIFICATION** = harsh-reviewer subagent; pre-committed "if rejected I adopt, I do not
   defend." v1 -> REJECT (2 P0); v2 -> SURVIVE-WITH-CHANGES (2 P1 + 3 P2). All adopted (Falsification
   section). A THIRD pass runs on the BUILT code next session AND must specifically falsify the new
   vault lint-status leg (sec 5.2).
4. **ANTI-ACCRETION**: a clean new variant; the base defect ADR-0037 named (no open-PR rung) is
   BUILT, not routed around.
5. **NARROW ADOPTION**: deterministic-only, clock-free, 2 docs/2 repos, PR-only, human-merge-only,
   fires-rarely. LLM-semantic (B) deferred.
6. **TUNING-BEFORE-EXECUTE**: the decider for "is auto-merge warranted" is the mechanical
   clean-cycle count + acted-on (human ground-truth), NEVER the actor's classifier. Eduardo merging
   each PR is the tuning loop.
7. **POST-EXEC VALIDATION**: each PR human-reviewed (Eduardo merges); the rung ships behind its own
   PR + its own ADR (D2); harsh-reviewer per increment (design done x2; code next session).

The rung-activating change ships as: (1) the actor code (TDD, CI green); (2) **its own ADR** (D2,
"R1 open-PR reconcile rung") recording the class def (sec 4), the doctrine exclusion +
reconciler-addition human review checkpoint (4.2), the human-merge-only invariant (6.1), the
no-branch-protection reality (6.2), the external clean-cycle accounting + its honest scope (7.1),
and the vault lint-status leg (5.2) -- plus an activation note in
`docs/governance/actor-activation-criteria.md` (DOCTRINE -> Eduardo merges). Eduardo merges the
rung-activating PR (autonomy increment, actor-criteria sec 7).

## 10. TDD plan (build phase -- NEXT session, NOT now)

One test at a time (tdd-guard), network/gh NEVER hit:
- `is_doctrine`: True for each carve-out class sample (incl. `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/**`);
  False for `STATUS_MULTI_REPO.md` + vault `Atlas/lint-status.md`. Constructing a `Reconciler`
  against a doctrine path RAISES.
- `render` (both legs): pure over fixture store states -> deterministic string; `None` when data
  absent; **asserts the output contains no time-derived value** (clock-free, sec 6.3). The vault leg
  asserts severity tracks BLOCK/WARN/metrics content (not the clock).
- `splice`: idempotent region replace; first-time injection; **create-if-absent for the new vault
  doc**; human prose preserved; no timestamp in body; identical input -> identical output.
- `reconcile_actor` with a FAKE gh_api + tmp store: no drift -> `unchanged`/no PR; drift -> one PR
  opened; re-run same state -> reuse/no-op; one reconciler error -> isolated, others proceed.
- **Negative merge test against the REAL builder (load-bearing, no platform backstop, sec 6.2):**
  assert the REAL `open_or_update_pr` builder NEVER emits `pr merge` / `--merge` / `--admin` / the
  REST merge route -- so a future merge-path addition goes CI-red.
- Live smoke (invoker-run, next session): `python -m governor.reconcile` against the real store ->
  expect mostly `unchanged` today (steady signals); firing path proven by tests.

## 11. Anti-scope

- No auto-merge (R2+, own ADR). No `.claude/settings.json` merge allow-rule.
- No LLM in the diff path (B deferred to R3 + a different-family judge).
- No cron promotion (Fase-4). Manual `python -m governor.reconcile` only.
- No doctrine-file targets, ever (sec 4.2). No EXECUTION-BOARD (doctrine).
- No time-derived / clock-tick / manufactured-churn diffs (sec 6.3). No eng-graph staleness band-flag.
- No Game/Godot/external targets. vault writes limited to the new `lint-status.md` (branch+PR,
  Eduardo-merge).
- No new signal sources; no change to the R0 ingestor or the R1 issue actor.
- No actor-written input to any unlock gate (clean-cycle accounting is external).

## 12. Risks (named, not hidden)

1. **vault lint-status doc = a governor-owned write-target in a sovereign repo.** Accepted by
   Eduardo (D1=(d), explicit OK). Mitigated: real consumer artifact, marker-bounded, NON-doctrine,
   branch+PR + Eduardo-only merge, clock-free (no churn). The code-phase harsh-reviewer must confirm
   the clock-free + create-if-absent claims (sec 5.2 build note).
2. **Slow cadence -> R2 far off.** Change-triggered + deterministic = silent when stable. Accepted:
   silence IS the off-ramp signal (sec 7.3); the rung must not inflate.
3. **The standalone `playtest2-board-sync` cron opens doctrine-path PRs -- but cannot auto-land
   them.** VERIFIED 2026-06-03: codemasterdd has only 2 workflows -- `ci.yml` (`contents:read`,
   cannot merge) and board-sync (`gh pr create` only, never merges). The "merge-cron" string in
   board-sync's PR body is aspirational, NOT wired. So the doctrine-leak-via-cron risk is INERT;
   it would arise only if a merge automation is later added, which MUST exclude `docs/governance/**`.
   This rung keeps the board OUT of its class (4.2) regardless.
4. **Low-judgment diffs counted as cycles.** Addressed in sec 7.1: cycles prove determinism +
   revert-safety, not merge-judgment-safety; the R2 ADR justifies auto-merge on reversibility +
   class-restriction + drop-check + CI-watchlist.
5. **Monoculture if B ever creeps in.** Hard anti-scope: no LLM diff in this class. B is a separate
   future rung gated on a different-family judge.
6. **Token over-privilege + NO branch protection.** The merge-block is code + invariant + settings
   ceiling ONLY (6.2/8); no platform backstop on this free-tier private repo. The negative test on
   the REAL builder + the rung code-review carry the weight; the R2 ADR must weigh this.
7. **SQLite reader/writer concurrency** (Flask pane reader + this actor writer) -- the Fase-1 risk;
   single-writer discipline + WAL; the actor is a short manual run.

## 13. The R2 ADR (later, separate -- NOT this spec)

After enough clean cycles (sec 7) across >=2 repos over >=2 weeks with zero bad-merge, a DEDICATED
R2 ADR -- harsh-reviewer FALSIFIED specifically -- may grant gated auto-merge of THIS class only,
and must: resolve the `>=2 repos` distribution (sec 7.2 / D3); add the narrow
`.claude/settings.json` merge permission for the one class; add a CI-watchlist (file<->essential-test,
anti-#10); add a different-FAMILY judge (fleet-tools `cross_check` / Gemini / Groq) OR argue an
explicit drop; explicitly weigh that codemasterdd has NO branch protection (6.2); and honor the
"cycles prove determinism not judgment" reading (7.1). R2 is out of scope here by construction.

## 14. Decisions (Eduardo, 2026-06-03)

- **D1 -- vault leg / 2nd repo: RESOLVED = (d).** Build a `vault-lint-status` reconciler (new
  governor-owned doc `Atlas/lint-status.md`, synced clock-free from the gap/coherence/whatsmissing
  signals). Eduardo granted EXPLICIT OK for the new doc in the sovereign vault repo. Options (a)
  band-flag and (b) `last_verified`-stamp stay dropped (clock-tick / circular). (c) defer not chosen.
- **D2 -- rung-activation vehicle: RESOLVED = new small ADR** ("R1 open-PR reconcile rung") +
  activation note in actor-criteria. (Drafted in the build session with the code.)
- **D3 -- ">=2 repos" distribution: DEFERRED to the R2 ADR** (sec 7.2; two real sources now exist,
  distribution ratified later with cadence data).
- **D4 -- build now vs wait: RESOLVED = build NOW** (rung GO; do not wait for off-ramp acted-on>=3).
  Per the seed + the goal ("fermati allo spec"), the CODE build is the NEXT session via
  `writing-plans`, behind the rung's own PR + ADR + the 3rd harsh-reviewer pass.

## Falsification (SDMG Protocol 7, 2026-06-03)

Two external harsh-reviewer rounds. Pre-commit "se rigetta adotto, non difendo" honored both times.

**Round 1 -- v1 verdict: REJECT** (2 P0, 4 P1, 3 P2). Adopted into v2:
- **P0.1 (vault ground-truth):** v1 asserted the vault marker/last_verified from the PARSER, not
  the live file. The v1 falsifier countered "absent" -- but read a STALE local vault clone. gh-api
  settled it: live MOC HAS `last_verified` + `eng-graph:auto`. Fix: cite VERIFIED ground-truth.
- **P0.2 (>=2 repos bent):** deferred the distribution to the R2 ADR.
- **P1.1-P1.4 + P2.1-P2.3:** clean-cycle evidence downgraded; `is_doctrine` completed (+Archivio/07);
  board-sync residual documented; build-at-1/3 surfaced; status-doc consumer justified;
  branch-protection vapor removed; band timing-dependence noted.

**Round 2 -- v2 verdict: SURVIVE-WITH-CHANGES** (2 P1, 3 P2; reviewer used gh-api ground-truth, no
stale-clone repeat; confirmed v1 fixes real; did not invent a P0). Adopted into v3:
- **P1.1 (vault leg CAN clock-tick):** the eng-graph staleness band is `f(now - last_verified)`
  folded into payload_hash -> a band-crossing opens a PR on a pure clock-tick, contradicting sec 6.3;
  the fallback `last_verified`-stamp is circular. ADOPTED: DROP the band-flag. (v4: the vault leg is
  now the CLOCK-FREE `vault-lint-status` per Eduardo D1=(d) -- lint severity is content-based, not
  time-based, so it does NOT reintroduce the clock-tick. sec 5.2.)
- **P1.2 (weak vault leg ~0 cycles):** addressed in v3 by deferral; in v4 by switching to the
  higher-cadence clock-free lint-status leg (D1=(d)).
- **P2.1 (phantom ADR-0039):** ADOPTED -- references changed to "the killed auto-merge-grant draft
  (un-numbered; SEED 2026-06-03)".
- **P2.2 (board-sync merge-cron):** ADOPTED + RE-VERIFIED (only `ci.yml` contents:read + board-sync
  no-merge; no merge-cron) -> sec 12.3 states it inert.
- **P2.3 (negative test vs fake only):** ADOPTED -- the negative merge test pins the REAL command
  builder (sec 6.2 / 10).

What both rounds could NOT refute (held): no disguised standing/auto grant; clean-cycle accounting
genuinely external (self-licking severed at the metric, matches shipped `store.py`); doctrine
carve-out complete + fail-closed (no leak); B correctly rejected for the entry rung; anti-accretion
holds; deterministic + clock-free prevents churn.

**v4 status: SDMG design gate PASSED (v2 SURVIVE-WITH-CHANGES, all changes adopted) + Eduardo
decisions D1(d)/D2/D4 resolved.** The new vault lint-status leg (D1=(d)) is a self-designed
post-falsification addition; it mirrors the already-survived clock-free/state-keyed/marker-bounded
pattern, but the 3rd harsh-reviewer pass (on the BUILT code, next session) MUST falsify it
specifically. Next: `superpowers:writing-plans` -> build.
