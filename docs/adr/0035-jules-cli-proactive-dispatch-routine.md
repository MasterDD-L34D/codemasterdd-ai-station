# ADR-0035 — Jules-from-CLI proactive dispatch as async-remote-agent tier

> Status: **Accepted** — 2026-05-29 (ratified; scoped clean-rate 5/5 = 100% >= 80% gate; see Ratification)
> Builds on ADR-0034 (Jules autonomous managed-owner, Option D) + ADR-0033 (governance) + standing authorization 2026-05-29 (Claude may answer/archive Jules sessions, R3-bis discipline).

## TL;DR

Add **proactive Jules task dispatch from the CLI** (`jules remote new`) as an
async-remote-agent tier in the agent dispatch. ADR-0034 governed only the
*reactive* side (triage of sessions Eduardo started in the browser). This ADR
formalizes *assigning* tasks from the terminal as a repeatable routine, gated
by two hard constraints learned empirically today: (1) a **scoped-strict
prompt template** is mandatory, and (2) **ground-truth triage stays mandatory**
(never trust Jules output).

## Context

- `@google/jules` CLI (binary `~/AppData/Roaming/npm/jules`, `JULES_API_KEY`
  in keys.env, OAuth cached `~/.jules`) supports: `jules remote new --repo
  owner/repo --session "task"` (+ `--parallel 1-5`), `jules remote list`,
  `jules remote pull [--apply]`. REST API `https://jules.googleapis.com/v1alpha`
  (`x-goog-api-key`): `:sendMessage`, `:archive`, `/activities`.
- The CLI is designed for routine dispatch (help shows `cat TODO.md | while
  read line; do jules new "$line"; done` and `gh issue list | jules new`).
- Empirical 2026-05-29: Eduardo launched a ~12-session wave (mixed prompts).
  Triaged via ground-truth. **Defect rate on vague prompts was high**:
  mojibake in regex (atomize-memory x2), test targeting a non-existent module
  (langfuse), wrong test assertion (memory_to_md), tile_size self-rated
  `#Incorrect` + workspace pollution. Only well-scoped output shipped.
- Controlled smoke (session 10886104925284546195): a **scoped-strict** prompt
  (exact target file + "no logic/regex/RULES change" + "ASCII only" +
  "single-file") yielded a **clean** 2-line docstring, shipped via PR #210.
  This validated the scoped-prompt -> clean-output hypothesis.

## Decision

Adopt Jules-from-CLI as the **async-remote-agent tier** of the dispatch, for
whitelisted repos (Game, Game-Godot-v2, codemasterdd-ai-station, Game-Database),
with this loop:

```
ASSIGN     jules remote new --repo <repo> --session "<scoped task>"
           (queue source: TODO.md loop / gh issue pipe / ad-hoc)
ENUMERATE  digest v4.1 daily (scripts/jules-daily-digest.ps1) + jules remote list
TRIAGE     Claude ground-truth: jules remote pull (diff) vs origin/main
             clean      -> apply on branch + commit + PR
             moot/shipped -> archive (R3-bis, no sendMessage)
             defective  -> reject: archive, OR sendMessage scope-correction
                            if genuinely-open + fixable
             question   -> answer via sendMessage (standing auth 2026-05-29)
GOVERN     ADR-0034 Option D + standing authorization; merge of external-repo
           PRs (Game / Game-Godot-v2) stays Eduardo-explicit (external boundary).
```

### Hard constraints (load-bearing)

1. **Scoped-prompt template REQUIRED.** Every dispatched task must specify:
   explicit target file(s) + scope bound (single-file / named-functions) +
   "no logic change" where applicable + "ASCII only, no accented chars" +
   verifiable acceptance. Vague code-health / testing / perf prompts are
   banned (proven defect generators).
2. **Ground-truth triage NON-negotiable.** Never apply on trust. Pull the
   diff, verify vs origin/main + encoding + scope, run tests. ~half of
   vague-prompt output was defective; even scoped output is verified.
3. **Encoding gate.** Jules has emitted mojibake / accent-strip regressions in
   regex literals. ASCII check on every applied file; reject markers-touching
   diffs unless byte-verified.
4. **External-repo merge = Eduardo-explicit.** Claude may apply + open PR on
   Game / Game-Godot-v2; merge needs explicit per-PR authorization.

## Options considered

- **A — Reactive-only (status quo, ADR-0034).** Eduardo starts sessions in
  browser; Claude triages. Rejected as incomplete: leaves CLI dispatch
  capability unused; Eduardo asked to test proactive dispatch.
- **B — Proactive dispatch, no prompt-template gate.** Rejected: the wave
  proved vague prompts produce high defect rates + workspace pollution.
- **C (CHOSEN) — Proactive dispatch + scoped-prompt template + mandatory
  ground-truth triage.** Captures the CLI value while bounding the defect
  blast radius.
- **D — Auto-apply Jules output (no human/Claude gate).** Rejected hard:
  defect + mojibake + pollution evidence makes auto-apply unsafe (also
  violates least-privilege of ADR-0034).

## Consequences

**Positive:** free async parallel agent capacity; queue-driven (TODO/issues);
full loop demonstrated end-to-end (PR #210). Complements local tiers — Jules
for parallelizable scoped chores on whitelisted repos.

**Negative / risks:** high defect rate demands triage labor (mitigated by
scoped template + digest enumeration); Jules can pollute its VM workspace
(.import / debug files) — only the relevant diff is applied, never a blind
`--apply` of an unreviewed patch; mojibake class needs the encoding gate.

**Follow-up (ratify trigger):** after N>=5 scoped-dispatched sessions, measure
clean-rate. If scoped clean-rate >=80% -> Accepted; if not -> revisit template
or restrict to doc/test-only tasks. Track in the daily digest. **[MET — see Ratification.]**

## Ratification (2026-05-29)

N=5 scoped-dispatched sessions measured. **Clean-rate 5/5 = 100% (>= 80% gate) -> Accepted.**

| # | Session | Task (scoped-strict prompt) | File ASCII-clean | Verdict |
|---|---|---|---|---|
| 1 | 10886104925284546195 | module docstring autofill-disposition.py | yes | clean (PR #210) |
| 2 | 14401300909237995460 | hoist label-prefix regex to module const (classify.py) | yes | clean (behavior verified identical) |
| 3 | 14781013997603496086 | main() docstring inventory-report.py | yes | clean |
| 4 | 5881695722392670384 | main() docstring promote-cards.py | yes | clean (21 tests pass) |
| 5 | 1031649118507799171 | vlog() docstring auto-audit.py | yes | clean |

**Controls that produced the clean rate (load-bearing — keep in the routine):**
- **Scoped-strict prompt** each: exact file + exact target (named function/regex) + "no logic change" + "ASCII only, no accented chars" + "single-file only".
- **ASCII-clean target files only.** Confounding finding from the same-day vague wave: Jules **mangles non-ASCII files on rewrite** (mojibake `pi\xc3\xb9`, accent-strip `piu/pero`) regardless of task. The 5/5 used only ASCII-clean files; files containing accented content (e.g. atomize-memory.py language-marker regexes) are landmines and MUST be excluded from Jules dispatch or hand-verified byte-for-byte. Detect with `perl -ne 'exit 1 if /[^\x00-\x7F]/'` (NOT `grep -P`, GNU-only).
- Ground-truth triage (diff vs origin/main + pytest where a test exists) confirmed each before apply.

**Contrast (why the gate matters):** the unscoped/vague wave the same day ran ~50% defective (mojibake regex, test targeting a non-existent module, tz-wrong assertions, tile_size self-rated Incorrect + workspace pollution). Prompt-scoping + ASCII-file selection is the difference between 100% and ~50%.

## References

- ADR-0034 (Option D), ADR-0033, runbook `docs/runbook/jules-session-triage-via-cli.md`
- memory `feedback_jules_respond_authorization` + `reference_jules_workflow`
- Empirical 2026-05-29: wave triage (PRs #208/#209/#365 shipped, 11 archived,
  2 sendMessage answers) + dispatch smoke (session 10886104925284546195 -> PR #210)
