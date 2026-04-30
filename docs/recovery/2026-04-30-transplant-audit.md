# Transplant audit 2026-04-30

## Summary

This repository was transported away from its original workstation context. In
the current copy, the repository is usable as a documentation and infrastructure
archive, but it is not able to govern the external projects it still references.

The main recovery decision is to freeze cross-repo governance and rebuild this
repo around a smaller, verifiable core:

- codemasterdd-ai-station governs only itself.
- External repositories are historical references until their local paths,
  remotes, working trees, runtime services, and evidence logs are verified.
- Runtime evidence that is gitignored must not be treated as present unless it
  exists in this checkout.

## Verified local state

- Current date: 2026-04-30.
- Current branch at audit start: `main`.
- Current branch after recovery work started: `codex/structural-reset`.
- Real HEAD at audit start: `ff3e91e`.
- `main` was aligned to `origin/main`.
- Local dirty state at audit start: untracked `AGENTS.md`.
- `rg.exe` was unavailable in this environment due to access denied, so the
  audit used Git and PowerShell fallback commands.

## Missing original-machine dependencies

The following paths referenced by repository docs and agents do not exist in
this transplanted checkout:

| Path | Current result | Meaning |
|------|----------------|---------|
| `C:\dev\Game` | missing | Evo-Tactics cannot be governed here |
| `C:\dev\synesthesia` | missing | Synesthesia cannot be governed here |
| `C:\Users\edusc\Dafne\workspace\swarm` | missing | Dafne swarm cannot be governed here |
| `C:\dev\codemasterdd-ai-station` | missing | canonical old path differs from current checkout |
| `C:\Users\edusc\aa01` | missing | AA01 is not present |
| `C:\Users\edusc\.local\bin` | missing | Aider wrapper claims are not locally verified |
| `C:\Users\edusc\.config\api-keys\keys.env` | missing | cloud key setup is not locally verified |

## Missing runtime evidence

These files or directories are cited by governance docs but are absent in this
checkout:

| Artifact | Current result | Notes |
|----------|----------------|-------|
| `logs/aider-delegation-2026-04.md` | missing | `logs/*` is intentionally gitignored |
| `apps/dogfood-ui/data/dogfood.sqlite` | missing | app runtime state is intentionally gitignored |
| `results/promptfoo-smoke.json` | missing | result artifact not present in this checkout |
| `scripts/quality-bench/results/` | missing/ignored | quality bench outputs are ignored |
| `backup/*` sensitive backups | missing | intentionally gitignored |

The design problem is not that these files are ignored. The problem is that
several docs speak as if they are available and authoritative. After transplant,
they are not.

## Source-of-truth drift

Multiple root files disagree about the current state:

| File | Drift observed |
|------|----------------|
| `README.md` | says stack updated 2026-04-23 and 14 ADR |
| `PROJECT_BRIEF.md` | cites HEAD `cb2e506`, 16 ADR, Fase 6 55 percent |
| `COMPACT_CONTEXT.md` | cites HEAD `8446869`, 15 ADR/ADR-0016 as latest in one section |
| `STATUS_MULTI_REPO.md` | cites HEAD `3b26173` and live cross-repo/runtime states from old machine |
| `ROADMAP.md` | says Fase 6 40 percent and "today" is 2026-04-23 |
| `MASTER_PROMPT.md` | would bootstrap a new agent into obsolete state: HEAD `5ef8e9c`, 14 ADR, Fase 6 40 percent |
| `REFERENCE_INDEX.md` | marks stale or missing artifacts as live |
| `DECISIONS_LOG.md` | indexes ADR-0019 but not ADR-0020 |

## Verified counts

Tracked file counts at audit time:

| Area | Count |
|------|------:|
| `Archivio_Libreria_Operativa_Progetti/` | 109 |
| `.claude/agents/` | 20 |
| `docs/adr/` | 20 |
| `apps/` | 18 |
| `scripts/` | 15 |
| root governance files | 17 |
| `docs/agent-smoke-tests/` | 9 |
| `infra/` | 6 |

The current repo is therefore dominated by imported framework material,
cross-repo agents, and historical governance. The self-governance core is much
smaller than the total tree.

## Operational verdict

The repo should not currently act as a live multi-repo control tower.

Until reactivation gates are satisfied, the following are dormant references:

- Evo-Tactics / Game
- Synesthesia
- Dafne swarm / evo-swarm
- AA01
- old original-machine runtime paths
- old dogfood and promptfoo runtime evidence

The active project is now:

> A portable structural recovery of `codemasterdd-ai-station` as a self-contained
> workstation governance archive and AI tooling scaffold.

## Immediate recovery actions

1. Mark cross-repo governance as dormant.
2. Replace stale status dashboards with a current structural snapshot.
3. Add `EXTERNAL_REPOS.md` as the only registry for external projects.
4. Create `SPRINT_02.md` focused on structural recovery.
5. Update `README.md`, `PROJECT_BRIEF.md`, `ROADMAP.md`, `BACKLOG.md`,
   `DECISIONS_LOG.md`, `MASTER_PROMPT.md`, and `REFERENCE_INDEX.md`.
6. Keep historical files for audit trail; do not delete or move them in the
   first recovery pass.

## Non-goals for this pass

- Do not fix Game, Synesthesia, Dafne, or AA01.
- Do not recreate missing logs from memory.
- Do not claim runtime services are up unless verified in this checkout.
- Do not remove historical ADR or session logs.
- Do not normalize all mojibake in one sweep; first reduce active surface area.
