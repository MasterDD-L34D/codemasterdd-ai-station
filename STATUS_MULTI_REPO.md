# STATUS_MULTI_REPO

## Status

Reactivated 2026-05-16 from fresh local evidence (reactivation gate
`EXTERNAL_REPOS.md`: criteria 1-3 verified via direct git audit, 5
satisfied — sensitive files gitignored/absent, 6 explicit user intent
2026-05-16, 7 = this rebuild). Rebuilt fresh, not patched from the old
historical dashboard, per the standing rule.

Evidence source: vault `docs/decisions/ecosystem-state-audit-2026-05-16.md`
+ `cross-stack-state-delta-2026-05-16.md` (cross-stack tracking layer).

## Verification method

Direct `git` audit on the current machine 2026-05-16: per repo branch,
detached state, dirty count, upstream sync (ahead/behind), worktree
count, last commit, remote. Only verified facts below; unconfirmed
roles labelled `unverified`.

## Repo matrix (verified 2026-05-16)

| Repo | Path | Branch | GitHub sync | Last commit | State |
|------|------|--------|-------------|-------------|-------|
| vault | `C:\Users\VGit\Vault` | main | ✅ 0/0 | 2026-05-16 | healthy — Karpathy LLM-wiki knowledge base |
| Game | `C:\Users\VGit\Desktop\Game` | root DETACHED 5d27fc50 | main-worktree ✅ 0/0 | 2026-05-16 (wt) | healthy — Evo-Tactics canonical Node repo; root detached cosmetic, work in worktrees |
| Game-Godot-v2 | `C:\Users\VGit\Desktop\Game-Godot-v2` | autoresearch/* | ✅ 0/0 active; main-wt 1-behind | 2026-05-16 | healthy — Godot v2 client (post-pivot) |
| Game-Database | `C:\Users\VGit\Desktop\repos\Game-Database` | feat/phase-4d-scope-b-* | ✅ HEAD==origin/main 0/0 | 2026-05-15 | healthy — species/taxonomy DB + API; no-upstream = branch config only |
| codemasterdd-ai-station | `C:\Users\VGit\Desktop\repos\codemasterdd-ai-station` | codex/* | ✅ 0/0 | 2026-05-01 | meta-orchestrator (this repo); was dormant, reactivating |
| evo-swarm | `C:\Users\VGit\Desktop\repos\evo-swarm` | main | ✅ 0/0 | 2026-05-08 | Dafne swarm runtime; registry=dormant, git healthy |
| synesthesia | `C:\Users\VGit\Desktop\repos\synesthesia` | main | ✅ 0/0 | 2026-04-16 | registry=dormant (exam/privacy); git healthy |
| Master-DD-Pathfinder-GPT | `C:\Users\VGit\Desktop\repos\Master-DD-Pathfinder-GPT` | codex-fix-* | ✅ 0/0 | 2026-04-10 | GDR GPT prompt project (unverified role) |
| pathfinder-1e-homebrew | `C:\Users\VGit\Desktop\repos\pathfinder-1e-homebrew` | main | ✅ 0/0 | 2026-02-26 | GDR homebrew content (unverified role) |
| claude-supermemory-local | `C:\Users\VGit\Desktop\repos\claude-supermemory-local` | main | ✅ 0/0 | 2026-04-16 | memory tooling (remote: claude-supermemory) |
| compass-marketplace | `C:\Users\VGit\Desktop\repos\compass-marketplace` | fix/* | ✅ 0/0 | 2026-04-25 | compass plugin marketplace (unverified role) |
| Item-generator | `C:\Users\VGit\Desktop\repos\Item-generator` | main | ✅ 0/0 | 2025-10-22 | utility, dormant (unverified role) |
| LeaD | `C:\Users\VGit\Desktop\repos\LeaD` | main | ✅ 0/0 | 2025-08-04 | utility, dormant (unverified role) |
| Gpt | `C:\Users\VGit\Desktop\repos\Gpt` | main | no-upstream | — | minimal/empty (unverified, no remote tracking) |
| evo-tactics-refs | `C:\Users\VGit\Documents\evo-tactics-refs` | master | ✅ 0/0 | 2026-04-29 | Evo-Tactics reference material (unverified role) |
| torneo-cremesi-site | `C:\Users\VGit\Desktop\repos\torneo-cremesi-site` | main | ⚠️ **0/20 behind** + 1 dirty | 2025-10-21 | **DRIFT** — 20 commits behind origin; side project (tournament site) |

## Findings

- 15 repos discovered (5 known + 10 new). **14/15 git-healthy + GitHub-synced.**
- **Only real drift**: `torneo-cremesi-site` (20 behind origin, 1 dirty) — low-priority side project, not core ecosystem.
- `Game` root detached HEAD (5d27fc50) is cosmetic — real work happens in worktrees, main worktree synced 0/0.
- `Gpt` has no upstream tracking and no commit history surfaced — likely minimal/empty; verify before use.
- The stale-tracking-doc reconciliation pattern (applied to vault OD-037, Game backlog) does NOT broadly apply: most repos are git-healthy, not doc-drifted. Reconcile only on demonstrated drift.

## Active boundary (unchanged)

Per `EXTERNAL_REPOS.md`: this repo governs repository structure, ADR
index, documentation consistency, portable setup docs, in-repo
scripts/infra. Game design/balance/lore, Synesthesia privacy, Dafne
process persistence remain out of scope until per-repo reactivation.

This dashboard is now a verified snapshot, not a live runtime monitor.
Re-verify with a fresh git audit before treating any row as current;
do not hand-edit rows from memory.

## Recovery note

Old historical content (dormant project list, stale HEADs) replaced
wholesale per the standing rule. Prior dormant state and demotion
rationale preserved in git history (pre-2026-05-16 revisions).
