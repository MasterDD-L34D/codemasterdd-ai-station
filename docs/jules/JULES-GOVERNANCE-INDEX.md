---
title: Jules governance -- hub index (codemasterdd-ai-station)
status: live
last_updated: 2026-06-25
owner: master-dd
---

# Jules governance -- hub index

> Hub-rooted index of ALL Jules knowledge across the fleet. codemasterdd is the policy hub;
> start here before any Jules work. Process + doctrine + tooling + cross-repo map in one place.
> Links point to the canonical artifacts (this file does not duplicate them).

## 1. The canonical cycle (process; validated 2026-06-25, 8 dispatches)

```
sweep -> ground-truth -> dispatch -> monitor -> salvage -> gate -> merge|deliver -> archive
```

1. **Sweep / source a candidate.** Fresh Jules suggestions are browser-only (no API): run the
   read-only sweep (`docs/runbook/jules-suggestions-snapshot.md`) OR pick from backlog. The daily
   digest (`scripts/jules-daily-digest.ps1`) enumerates session->PR state (advisory).
2. **Ground-truth the candidate (MANDATORY).** Jules suggestions + old snapshots are stale-prone:
   verify the function/import/test is genuinely open before dispatch (many 2026-06 suggestions were
   already shipped/false-positive). Confirm it is a clean, scoped, single-file, ASCII-able task and
   NOT a freeze path (`services/generation|rules`, `apps/backend/services/combat`) unless test-only.
3. **Dispatch** via `scripts/fleet/jules-dispatch.ps1` (5 fail-closed gates: repo-whitelist / ASCII /
   scoped-template / dedup-vs-active / POST). `-DryRun` first, then real. `:create` is per-instance
   human-run (ADR-0037 SDMG boundary), authorized by Eduardo-in-chat.
4. **Monitor** the session state (Monitor tool poll, or the digest). Cover all terminal states.
5. **Salvage (the load-bearing step).** Jules almost ALWAYS delivers-misses on these dispatches:
   COMPLETED but NO PR, REST `gitPatch` empty -- the diff lives in `outputs[].changeSet` or the
   activities artifacts (last stable `unidiffPatch`). ALWAYS ground-truth `outputs[].pullRequest.url`
   before "shipped"; if absent, recover the patch, apply to an isolated branch, verify.
   (7/7 delivery-miss on 2026-06-25; see [[feedback_jules_failed_recovery]].)
6. **Gate.** CI green + read review comments (`pulls/<N>/comments` + `issues/<N>/comments`, triage
   P1/P2/P3, bot usage-limit notices are not P1) + harsh-reviewer on security/governance/freeze files.
7. **Merge | deliver.** codemasterdd self-repo non-doctrine = auto-merge after the gate (rebase to
   preserve ADR-0011 trailers). EXTERNAL repos (Game/Godot-v2/Game-DB) = deliver branch+PR, MERGE =
   Eduardo (classifier hard-block + ADR-0037). See [[feedback_merge_authority]].
8. **Archive** the shipped session (R3-bis archive-only, never sendMessage on a moot session).

## 2. Output taxonomy -- "session > PR" golden rule

Never conclude "wasted/empty/close" from the PR alone; the truth is the SESSION (state +
agentMessaged + gitPatch artifacts). Taxonomy S1-S7 (PR-faithful / scope-creep / sandbox-stale /
genuinely-empty / premise-false / behavior-under-cosmetic / duplicate):
`docs/research/jules-operating-model-study-2026-05-17.md`. S3 (push-lost) is the dominant state
in practice (the delivery-miss); salvage it, do not close it.

## 3. Governance doctrine (ADRs, chronological)

- `docs/adr/0032-jules-pr-governance-active-model.md` -- Model-3 (SUPERSEDED by 0033).
- `docs/adr/0033-jules-governance-resolved.md` -- external = read-only triage; owner-merge.
- `docs/adr/0034-jules-autonomous-managed-owner-mandate.md` -- Option D: advisory digest, Eduardo per-cycle approve, zero auto-exec; R3-bis no-message-on-moot.
- `docs/adr/0035-jules-cli-proactive-dispatch-routine.md` -- CLI dispatch (`:create`) per-instance; wrapper as enforcement, not a standing grant.
- `docs/adr/0037-merge-autonomy-model.md` (+ 0038 carve-out, 0039 R1 open-PR rung) -- merge autonomy; external-merge earn-path (governor R0->R1->R2).

## 4. Tooling

- `scripts/fleet/jules-dispatch.ps1` (+ `.Tests.ps1`) -- 5-gate fail-closed dispatch wrapper.
- `scripts/jules-daily-digest.ps1` + `scripts/fleet/register-jules-digest-task.ps1` -- advisory digest (single-owner = Lenovo as of 2026-06-25; was dual-registered, fixed).
- `.claude/agents/jules-pr-triager.md` -- harsh-review triage of open Jules PRs (read-only verdicts).

## 5. Runbooks + research + specs

- `docs/runbook/jules-session-triage-via-cli.md` -- read-only triage + verdict-logic.
- `docs/runbook/jules-suggestions-snapshot.md` -- browser suggestions sweep (no API).
- `docs/research/jules-operating-model-study-2026-05-17.md` -- taxonomy + bias analysis.
- `docs/research/jules-dispatch-wrapper-2026-06-03.md` -- wrapper QG report.
- `docs/superpowers/jules/2026-06-03-jules-autonomy-gaps.md` + `2026-06-03-jules-dispatch-wrapper.md` + `docs/superpowers/specs/2026-06-03-jules-dispatch-wrapper-design.md`.

## 6. Memory (cross-session, ~/.claude/.../memory)

- `reference_jules_workflow` -- API + digest heuristic + R3-bis + meta-patterns (THIS index supersedes its scope as the entry point).
- `feedback_jules_failed_recovery` -- delivery-miss salvage (incl. EXTERNAL-repo gh-API salvage + prettier-fix).
- `feedback_jules_respond_authorization` -- Claude may sendMessage/archive genuinely-open sessions.
- `feedback_merge_authority` -- codemasterdd auto-merge vs Game-family earn-path.

## 7. Cross-repo map (hub-rooted)

- **codemasterdd-ai-station (HUB)**: all tooling + governance ADRs + dispatch wrapper + digest +
  the hub museum (`docs/museum/`). Self-repo Jules merges = auto after gate.
- **Game / Game-Godot-v2 / Game-Database**: dispatch TARGETS (whitelisted). Game-DB is Jules-maintained
  (taxonomy CMS, heavy Jules history: S1a-S1d, GATE-5/6). External-merge = Eduardo. Each has its own
  `docs/museum/MUSEUM.md` (game-design archaeology), cross-linked with the hub museum (bidirectional).
- **vault** (`MasterDD-L34D/vault`): consult before research dives; sovereign, merge = Eduardo.
- **Museum network**: `docs/museum/MUSEUM.md` (hub) <-> Game/Godot museums <-> vault.

## 8. Logs / audit

- `logs/jules-dispatch-YYYY-MM.md` -- dispatch audit spine (gitignored).
- `logs/jules-salvage-<sid>.patch` -- recovered diffs (gitignored).
- `docs/jules-batch/<day>-digest.md` + `tasks/` + `reports/` -- digests, dispatched task prompts, pulled report-session content.
