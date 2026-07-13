# Smoke test log -- jules-pr-triager

## 2026-07-13 -- Gate 1 smoke (live subagent-dispatch)

- **Prompt**: triage open Jules code-health PRs on MasterDD-L34D/Game; if none open, retrospective smoke on the 3 most recent merged Jules PRs. Read-only.
- **Runtime**: ~203s (14 tool calls: pr list + committer-verify + 3 real diff reads).
- **Result**: PASS -- verdict logic correct on real historical data, read-only respected.
- **Quality**:
  - Correctly detected **0 open Jules code-health PRs** (only #3275 weekly-drift, author MasterDD-L34D, not Jules) -> ran the requested retrospective on #2301 / #2292 / #2293 (05-17 batch).
  - **committer > author nuance applied**: verified `google-labs-jules[bot]` via `commits[0].commit.committer.name`, NOT the GraphQL `author` field (which shows MasterDD-L34D regardless) -- exactly the doctrine the def encodes.
  - Read REAL diffs (not titles): all 3 = pure extract-method, no game-logic/data/balance touched -> 3 MERGE-OK, consistent with their actual merged outcome.
  - **Conflict analysis correct**: #2292/#2293 touch the same file (`species_builder.py`) but different non-overlapping functions -> NOT a "pick one" cluster (cluster doctrine = same-fn duplicates).
  - **Pattern-alert honesty**: flagged sampling bias ("3 recent-clean don't generalize; the full 05-17 batch is where the known anti-patterns live") + noted 0 PRs post-05-17 -> throttle not needed now.
  - Zero mutating action; produced Eduardo-ready batch framing.

## Edge cases observed (>= 3)

1. **Input edge -- empty queue**: 0 open Jules PRs. Agent handled it (ran retrospective per prompt) but the def had NO explicit empty-queue path -> risk of fabricating retrospective work unprompted. Gate-3 tuning below.
2. **Data edge -- author-field lies**: GraphQL `author` = MasterDD-L34D for bot PRs; agent fell back to committer.name correctly (doctrine already in def).
3. **Runtime edge**: 203s (longest of the batch) -- scales with PR count x diff size (14 tool calls for 3 diffs). Inherent to real-diff-reading; the def already caps via the >=10-open trigger.

## Gate 2 -- sources validation

- Doctrine derived from Archivio `02_LIBRARY` "Harsh Reviewer" + internal empirical triage (17 Jules PRs, 2026-05-17) + ADR-0033 Jules-governance reconciliation -- all internal, repo license.
- **Verdict**: zero licensing issue. SOURCES.md updated to list this agent.

## Gate 3 -- tuning

- **Applied**: added an explicit empty-queue guard to Modalita-1 -- "Se 0 PR Jules aperti -> riporta '0 pending, nessuna azione richiesta'; NON fabbricare un triage retrospettivo salvo richiesta esplicita".
- **Delta**: before = undefined behavior on 0 open PRs (could invent retrospective work); after = graceful no-op unless retrospective is explicitly requested. Prevents fabricated-work drift.
- **Status**: draft -> **ready** 2026-07-13.
