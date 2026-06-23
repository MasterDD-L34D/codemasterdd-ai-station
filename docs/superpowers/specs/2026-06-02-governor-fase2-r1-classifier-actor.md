# Governor Fase 2 / R1 -- classifier + escalation actor (hub-only) design spec (v2)

> **Status (2026-06-23):** shipped -- R1 classifier + escalation actor live

> Status: DRAFT v2 2026-06-02 -- REJECTED v1 by harsh-reviewer (SDMG step 3), redesigned
> to the 6 survive-conditions + 1 improvement (escalate via GH ISSUE, not PR). Author:
> Claude (Opus) on Ryzen. First autonomy increment (R0 report-only -> R1 actor emits).
> ASCII-first. Authority: ADR-0036 + `docs/governance/actor-activation-criteria.md`.

## 0. Honesty preamble (SDMG)

- **Off-ramp WAIVED by Eduardo** (R0 shipped today; the 4wk/acted-on>=3 gate not met).
  R1 triggers on a heuristic, not on evidence of what Eduardo acts on. Flagged. The
  waiver is ALSO recorded in `actor-activation-criteria.md` itself (P1.4 fix), so the
  authority doc does not silently contradict the shipped state.
- **Scope = A (hub-only escalation)**, Eduardo-chosen. Writes ONLY to codemasterdd. No
  source-repo writes, no auto-merge, no cross-repo fix-PRs.
- **R1 = actor proposes, human disposes.** Only autonomy added: the actor opens/updates
  ONE GitHub ISSUE when something is on fire. Human closes (= seen). Fully reversible.

## 1. v1 REJECT -> v2 (what changed, per the falsification)

| harsh-reviewer finding (ground-truth confirmed) | v2 fix |
|---|---|
| P0.1 churn: timestamp + `fetched_at` in a committed file -> a PR every run | **No committed file. No PR.** Escalate = open/update ONE GH **issue**; idempotency keyed on a content-hash of the escalate-set (source+severity only), NOT timestamps. |
| P0.2 `{error,warning}` -> 5/6 escalate = R0-with-extra-steps | **Narrow rule: escalate iff `severity == "error"` OR severity WORSENED vs the prior stored signal (delta).** Probe-confirmed today: 5 warning + 1 info + 0 error -> R1 is a **no-op today** (correct: nothing on fire). Fires only on error/regression. |
| P0.3 "never merges" unenforced; token has `repo` scope (probe-confirmed merge-capable) | **It's an issue, not a PR -- structurally unmergeable.** Plus a negative test asserts the gh argv never contains `pr merge`/`--merge`/`--admin`. |
| P1.1 self-licking: merging attention-PR could count as acted-on | **Closing/seeing the issue != acted-on.** Recorded in `actor-activation-criteria.md` sec 5. Actor writes nothing to `acted_on`. |
| P1.2 self-certification: digest hides what was dropped | **Issue body footer lists the dropped (report-class) count + a pointer to the /governor pane** -> human reviews exclusions, restoring SDMG-6 separation. |
| P1.3 force-with-lease / per-day branch pile-up | **No branch.** One reused issue (search open issue with label `governor-attention`; update it; else create). Max 1 open at a time. |
| P1.4 earn-path doc contradiction | Amend `actor-activation-criteria.md` sec 2/8 to record the 2026-06-02 waiver in-place. |

## 2. Architecture (new in `apps/cross-repo-dashboard/governor/`)

- **`classify.py`** -- pure. `classify(signal: dict, prior_severity: str|None) -> Verdict`.
  - `Verdict = {"action": "escalate"|"report", "rank": int, "reason": str}`.
  - `_RANK = {"error":3,"warning":2,"info":1,"ok":0}` (single source of truth; export from signals.py).
  - **escalate iff** `severity == "error"` OR `_RANK[severity] > _RANK[prior_severity]` (worsened
    since last stored signal). Else `report`. `reason` states which (e.g. "error" / "worsened ok->warning").
  - Pure: caller passes `prior_severity`. No I/O.
- **`store.py`** (extend) -- `previous_severity(source) -> str|None`: the severity of the
  SECOND-most-recent signal row for that source (the signals table dedups by hash, so a
  severity change = a distinct prior row). None if only one (or zero) row.
- **`digest.py`** -- pure. `build_attention_body(escalated: list[dict], dropped_count: int) -> str`:
  ASCII markdown issue body -- a ranked list (source | severity | reason | summary | ref) +
  a footer `"N signal(s) below escalation threshold -- see /governor pane"`. NO timestamp in
  the body (idempotency). `escalate_key(escalated) -> str`: stable hash over
  sorted (source, severity) tuples -- the change-detector.
- **`act.py`** -- the actor (only new autonomy surface).
  - `run_r1(store, issue_api=<real gh-issue fns>, now_iso=None) -> dict`: load
    `latest_per_source()`; for each, `classify(sig, store.previous_severity(source))`; split
    escalate/report; if escalate-set EMPTY -> no-op (return `{"escalated":0,"noop":True}`);
    else compute `escalate_key`; find the open `governor-attention` issue; if none -> create
    with body; if exists and its stored key differs -> update body; if same key -> no-op
    (idempotent, no spam). Returns `{"escalated":n,"issue":num,"action":"created|updated|noop"}`.
  - `issue_api` injected (real = `gh issue list/create/edit`); tests pass a fake -> NO gh in tests.
  - NEVER opens a PR, NEVER merges, NEVER closes the issue (human closes). Label
    `governor-attention` on codemasterdd only.
  - `__main__`: `python -m governor.act` (manual; cron = Fase-4).

## 3. Safety / reversibility

- Artifact = ONE GitHub issue on codemasterdd (label `governor-attention`). No file, no
  branch, no PR, no merge -- structurally (an issue cannot be merged). Human closes.
- Idempotent: same escalate-set (by `escalate_key`) -> no issue update (no spam). The body
  excludes all timestamps; the change-key is severity-state only.
- `gh` token note (P0.3, probe-confirmed `repo`-scope = merge-capable): the actor does NOT
  call any merge; a negative test guards the argv. A least-privilege token is the stronger
  structural fix and is now IMPLEMENTED (2026-06-02): the actor's gh CLI reads
  `GOVERNOR_ISSUE_TOKEN` (a fine-grained PAT scoped `issues:write` on codemasterdd ONLY) and
  passes it via the child ENV (`GH_TOKEN`), never argv (CWE-214-safe); if unset it falls back
  to ambient `gh auth` (non-breaking). To activate: mint the PAT (human step,
  account-credential) + set `GOVERNOR_ISSUE_TOKEN`. Issue-only actor needs only `issues:write`,
  not `repo`; not blocking before activation because the artifact is unmergeable anyway.
- Fires rarely (error/regression only) -> low write-rate, no attention-fatigue.

## 4. SDMG

1. DESIGN = hypothesis (v2). 2. TEST = the 3 probes (run: 0 error / churn / repo-scope --
all confirmed the v1 reject). 3. FALSIFICATION = harsh-reviewer REJECTED v1; v2 implements
its 6 survive-conditions + the issue-improvement; the BUILT code gets a second
harsh-reviewer pass (build-review; I provide test outputs since the arbiter is now static).
4. ANTI-ACCRETION = v2 is a clean redesign, not an amendment onto the rejected v1.
5. NARROW = issue-only, propose-not-dispose, fires-rarely. 6. TUNING-BEFORE-EXECUTE = the
classifier is a heuristic; the decider stays Eduardo (he closes/acts); the footer exposes
exclusions so he decides over the FULL set. 7. POST-EXEC = each issue is human-reviewed;
closing = "seen" (NOT acted-on); acting on an underlying signal (a fix/OD/ADR) is the
off-ramp's acted-on event, counted manually, EXPLICITLY excluding the issue-close itself.

## 5. TDD plan (build after this spec is accepted)

- `classify`: pure -> fixtures (error -> escalate; worsened delta -> escalate; steady
  warning -> report; ok -> report). one test at a time (tdd-guard).
- `store.previous_severity`: tmp SQLite, insert 2 rows different severity -> returns prior.
- `build_attention_body` + `escalate_key`: pure -> deterministic, ASCII, footer count;
  same escalate-set -> same key (idempotency); body has NO timestamp.
- `run_r1`: fake `issue_api` + tmp store -> empty escalate -> noop; error signal -> create;
  same key -> noop; changed key -> update. Negative test: the (mocked) gh argv never
  contains `pr`/`merge`. Network/gh NEVER hit in tests.
- Live smoke (invoker-run): `python -m governor.act` against the real store -> expect
  `{"escalated":0,"noop":True}` TODAY (0 error, no deltas) = correct silent behavior.
  Firing path verified by tests (no live error to trigger).

## 6. Anti-scope
- No auto-merge (R2+, deferred). No PR, no committed file, no branch, no cross-repo writes.
- No cron (Fase-4). No `.claude/settings.json` change. No new signal sources.
