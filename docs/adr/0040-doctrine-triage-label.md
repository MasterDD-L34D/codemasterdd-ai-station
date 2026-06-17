# ADR-0040 -- Doctrine PR triage label (hint-only)

- Status: Proposed (2026-06-17; ratified on Eduardo merge)
- Deciders: Eduardo
- Related: ADR-0037 (merge autonomy), ADR-0038 (doctrine catch-all), ADR-0039 (no content classifier), docs/governance/actor-activation-criteria.md

## Context

Doctrine files (`.claude/**`, `docs/adr/**`, `docs/governance/**`, named root rule
files) are Eduardo-only-merge: the hub proposes branch+PR but NEVER merges its own
rule-book. A 2026-06-17 evidence review asked whether human-merge on EVERY doctrine
edit is research-mandated. Finding: SOTA (Meta "Agents Rule of Two", policy-as-code)
mandates the human gate for CAPABILITY-EXPANDING edits; the blanket rule is still
justified here because codemasterdd had no platform backstop. An adversarial red-team
REFUTED any "auto-merge the neutral edits" fast-lane: a deterministic regex sees diff
SHAPE, never DIRECTION (tighten vs loosen) nor a prose meaning-shift (`must` -> `should`,
a reference-URL swap, a threat-category rename -- verified live in PR #365's own diff).
So auto-merge of doctrine stays OFF.

The real pain is CADENCE (the per-PR human interrupt), not the gate. The accepted
relaxation is cadence-only: batch the human merge + a deterministic TRIAGE LABEL that
tells the human which doctrine PRs need full scrutiny vs a quick glance.

## Decision

Add `scripts/governance/doctrine_triage.py`: given a doctrine PR diff + changed files,
emit a label:
- `loosening-surface` -- the diff touches a capability/gate surface (a settings
  allow-rule, a hook, an autonomy rung/threshold, or a merge/permission token) -> FULL
  human scrutiny.
- `prose-only` -- no capability signal -> a QUICK human glance.

Properties (load-bearing):
- HINT ONLY. It NEVER merges and is NEVER a gate. The merge act on any doctrine file
  stays human (Eduardo), per ADR-0037/0038.
- FAIL-CLOSED. Any signal, or any non-markdown change to a governance code path, yields
  `loosening-surface`. Over-flagging (more scrutiny) is the safe direction.
- The regex limitation is EXPLICIT and intended: `prose-only` does NOT mean
  safe-to-automate; it means "no mechanical capability signal, still human-merge". A
  meaning-shift in prose can be capability-affecting and will read `prose-only` -- this
  is exactly why the label never gates.

Usage: Eduardo runs the CLI (`--pr N`) at merge time, or it is wired as a non-blocking
PR label. It informs scrutiny level; it does not change who merges.

## Consequences

- Faster human triage of the doctrine merge queue WITHOUT weakening the gate.
- No new auto-merge authority; the `.claude/settings.json` ceiling is unchanged (still
  `git push origin claude/*`, no merge).
- Validated: PR #365 (a threat-taxonomy remap the red-team called capability-affecting)
  classifies `loosening-surface` -- the tool flags exactly the case a naive "neutral
  label fix" view would have under-scrutinized.
- Tests: `scripts/tests/test_doctrine_triage.py` (10 cases, incl. fail-closed and the
  bug TDD caught: a charset `lstrip("./")` that dropped the leading dot of `.claude/`).

## Alternatives rejected

- Auto-merger of the "clean" bucket: REJECTED -- regex tests shape not direction; with
  no second human a false-negative auto-merges unreverted (red-team).
- LLM content-classifier of doctrine: REJECTED -- ADR-0039 dec.2 (no classifier in the
  merge-decision path).
- Tier-A/Tier-B doctrine split (hub merges "operational" doctrine): REJECTED -- reopens
  the "frame a loosening edit as operational" hole ADR-0038 closed.
