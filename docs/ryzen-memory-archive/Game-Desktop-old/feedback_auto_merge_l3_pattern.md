---
name: Auto-merge L3 cascade pattern (post 2026-05-07 ADR)
description: Pattern canonical per auto-merge cascade Claude-shipped PR. 7 safety gate verification + cascade order rules + force-push rebase handling. Applica post ADR-2026-05-07-auto-merge-authorization-l3.
type: feedback
originSessionId: 9f6b53c5-849b-4278-a1eb-c7087a04edf9
---
# Auto-merge L3 cascade pattern

User formal authorization 2026-05-07 codified ADR-2026-05-07-auto-merge-authorization-l3. Apply this pattern ogni volta che Claude-shipped PR cluster pronto per merge cascade.

**Why**: master-dd manual gate × N PR = bottleneck. L3 cascade ~2-3x speedup confirmed sessione 2026-05-07 sera (4 PR shipped 17min vs ~30-60min manual).

**How to apply**:

## Pre-merge verification ritual (per ogni PR cascade)

```bash
# Gate 1 — CI 100% verde
gh pr checks <num> --repo <owner>/<repo> 2>&1 | grep -E "fail|pending"
# Empty grep = pass

# Gate 2 — Codex resolved
gh pr view <num> --repo <owner>/<repo> --json reviews --jq '.reviews[] | select(.author.login == "chatgpt-codex-connector") | {state, sha: (.body | capture("Reviewed commit:.*?`(?<sha>[a-f0-9]+)`") // {sha: "?"} | .sha)}'
# Verify state COMMENTED + no requested_changes su latest commit

# Gate 5 — forbidden paths
git diff origin/main...<branch> --name-only | grep -E "^(\.github/workflows|migrations|packages/contracts|services/generation|services/rules)/"
# Empty = pass

# Gate 6 — 50-line violation
git diff origin/main...<branch> --stat | awk '/^ apps\/backend/ {next} {if ($3+0 > 50) print}'
# Empty = pass

# Final: mergeStateStatus
gh pr view <num> --repo <owner>/<repo> --json mergeStateStatus,mergeable
# Want: CLEAN + MERGEABLE
```

## Cascade order rules

1. **Lint debt / CI hygiene fix** SEMPRE first (es. PR #209 main.gd refactor 1101→999 LOC). Altri PR dipendenti ereditano main verde.
2. **Doc-only PR** second (es. #2101 plan v3.2 close — file-disjoint vs feature).
3. **Policy ADR PR** (es. #2103 auto-merge ADR — codifica diventa retroattiva post-merge).
4. **Feature PR rebased post-cluster** last (es. #208 GAP-10 — needed rebase + extract subagent post #209 main.gd cap fix).

## Force-push rebase pitfall

Post `git rebase origin/main` + `git push --force-with-lease`:
- GitHub re-queues TUTTI i CI check (re-run from scratch)
- mergeStateStatus → BLOCKED finché re-run completa
- `gh pr merge --auto` non supportato free-tier private repo (`enablePullRequestAutoMerge GraphQL error`)

**Pattern**: loop-wait `while gh pr checks <num> | grep -q pending; do sleep 10; done`, poi `gh pr merge --squash`.

## CLAUDE.md cross-PR conflict avoidance

2 PR Game/ doc-only entrambi modificano CLAUDE.md → conflict garantito (Markdown table line shift). 2 strategie:

- **Strategy A (sequential merge)**: merge PR1 → rebase PR2 on main + resolve conflict (`git checkout --ours CLAUDE.md` + manual re-add lost edits). Slower ma cleaner.
- **Strategy B (squash bundling)**: combine 2 PR into 1 squash merge se possibile pre-open. Faster ma scope larger.

Default: A se PR aperti separati, B se proattivo.

## Stop-line conditions (abort cascade + escalate user)

- ANY safety gate red post-fix attempt
- Codex `requested_changes` state on latest commit (not just COMMENTED)
- Master-dd "stop auto-merge" comment posted on any PR thread
- New file in forbidden path appearing post-rebase
- CI flaky pattern detected (>2 retry su same job)

## Pre-cascade checklist (each session)

- [ ] User L3 authorization confirmed (verbal session OR codified ADR persistent)
- [ ] All target PR Claude-shipped (autore verified)
- [ ] All target PR file-disjoint OR sequential merge plan
- [ ] Test baseline command identified per repo (Game/: `node --test tests/ai/*.test.js`, Godot v2: GUT via `.github/workflows/test.yml` canonical command)
- [ ] Memory save ritual queued post-cascade (DoD CLAUDE.md "≥2 PR mergiati = save obbligatorio")

## Anti-pattern

- ❌ Skip gate 2 (Codex review) "perché PR doc-only" — Codex catches data inconsistency frequently (sentience audit P2+P3 catch 2026-05-07)
- ❌ Auto-merge mid-CI-pending — wait completa
- ❌ Auto-merge with conflict markers in tree
- ❌ Cascade order: feature PR before lint debt fix → CI eredita debt
- ❌ Force-push without `--force-with-lease` (race condition risk)
