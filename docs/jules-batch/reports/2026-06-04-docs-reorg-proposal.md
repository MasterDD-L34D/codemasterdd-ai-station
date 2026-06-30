# docs/ Reorganization Proposal (codemasterdd-ai-station)

## 1. Inventory by Group

| Directory | File Count | Purpose | Action |
| --- | --- | --- | --- |
| `docs/adr/` | 39 | Authoritative Architectural Decision Records | **Keep** |
| `docs/superpowers/` | 33 | Agent capabilities, plans, and specs | **Keep** |
| `docs/research/` | 28 | Exploratory technical research & prototyping | **Keep** |
| `docs/archive/` | 7 | General archive for retired documents | **Keep** |
| `docs/ryzen-memory-archive/` | 141 | Bloat/dumps from previous PC environment | **Archive** |
| `docs/sessions/` | 13 | Session handoffs & continuity logs | **Consolidate** -> `docs/handoffs/` |
| `docs/runbook/` | 10 | Operational playbooks & troubleshooting | **Keep** (Merge `docs/operations/` here) |
| `docs/agent-smoke-tests/` | 9 | Test reports for AI agents | **Consolidate** -> `docs/superpowers/tests/` |
| `docs/cross-repo/` | 9 | Cross-repo workflows & templates | **Consolidate** -> `docs/governance/` |
| `docs/jules-batch/` | 9 | Logs/digests of Jules batch runs | **Archive** |
| `docs/aa01-handoff/` | 7 | Specific AA01 project handoffs | **Archive** |
| `docs/patterns/` | 7 | AI/Dev methodology patterns | **Consolidate** -> `docs/reference/patterns/` |
| `docs/reference/` | 7 | Cheatsheets & reference material | **Keep** |
| `docs/lessons-learned/` | 3 | Postmortems & learnings | **Consolidate** -> `docs/reference/lessons/` |
| `docs/goals/` | 2 | Specific short-term goals/gaps | **Consolidate** -> root `GOALS.md` or Archive |
| `docs/jules/` | 1 | Master capabilities doc for Jules | **Consolidate** -> `docs/superpowers/` |
| `docs/operations/` | 1 | Key/task routing matrix | **Consolidate** -> `docs/runbook/` |
| `docs/plans/` | 1 | One-off integration plan | **Archive** |
| `docs/reviews/` | 1 | Review flowchart | **Consolidate** -> `docs/governance/` |
| `docs/strategy/` | 1 | Parallel execution strategy | **Consolidate** -> `docs/reference/patterns/` |

**Notable files in small dirs:**
- `docs/cross-repo/ESCALATION_GATES.md`, `PR_WORKFLOW.md` -> Highly relevant governance docs.
- `docs/patterns/self-designed-method-governance.md` -> Core methodology.
- `docs/jules/JULES-CAPABILITIES-MASTER.md` -> Core agent definition.

## 2. Problems Found

1. **The `ryzen-memory-archive` bloat**: Represents ~40% of the entire `docs/` tree (141 files). It's a
   raw dump from an old environment and clutters searches. It should be zipped or moved strictly to
   `docs/archive/ryzen-memory/`.
2. **Scattered Governance**: Cross-repo rules (`docs/cross-repo/`), review flows (`docs/reviews/`),
   and patterns (`docs/patterns/`) are fragmented. They should live in a unified `docs/governance/`
   or `docs/reference/` structure.
3. **Redundant Handoff/Session Dirs**: `docs/sessions/`, `docs/aa01-handoff/`, and
   `docs/jules-batch/` all serve similar ephemeral logging purposes. Many are stale and can be
   archived.
4. **Agent/Jules Fragmentation**: Jules documentation (`docs/jules/`, `docs/jules-batch/`), general
   agent tests (`docs/agent-smoke-tests/`), and superpowers (`docs/superpowers/`) are disjointed.
5. **Missing Indexes**: Most subdirectories lack a `README.md` explaining their purpose.
6. **Micro-directories**: Dirs with 1-3 files (`docs/goals/`, `docs/jules/`, `docs/operations/`,
   `docs/plans/`, `docs/reviews/`, `docs/strategy/`, `docs/lessons-learned/`) increase cognitive
   load without organizational benefit.

## 3. Proposed Structure

| Target Path | WHY |
| --- | --- |
| `docs/adr/` | (Keep) Single source of truth for architectural decisions. |
| `docs/superpowers/` | (Keep) Unified home for all AI agent capabilities, tests, and definitions. |
| `docs/research/` | (Keep) Active exploratory technical documents. |
| `docs/runbook/` | (Keep) Unified home for operational procedures and troubleshooting. |
| `docs/reference/` | (Keep) Cheatsheets, methodologies, lessons learned, and stable references. |
| `docs/governance/` | (New) Unified home for cross-repo workflows, PR templates, and gating rules. |
| `docs/handoffs/` | (New) Consolidated location for active session logs and continuity files. |
| `docs/archive/` | (Keep) Resting place for old batches, stale plans, and environment dumps. |

*Note: Each kept/new directory should have a `README.md` index file added.*

## 4. Migration Map

| Current Path | Proposed Path |
| --- | --- |
| `docs/ryzen-memory-archive/` | `docs/archive/ryzen-memory-archive/` |
| `docs/jules-batch/` | `docs/archive/jules-batch/` |
| `docs/aa01-handoff/` | `docs/archive/aa01-handoff/` |
| `docs/plans/` | `docs/archive/plans/` |
| `docs/cross-repo/` | `docs/governance/` |
| `docs/reviews/` | `docs/governance/reviews/` |
| `docs/patterns/` | `docs/reference/patterns/` |
| `docs/lessons-learned/` | `docs/reference/lessons/` |
| `docs/strategy/` | `docs/reference/patterns/` |
| `docs/agent-smoke-tests/` | `docs/superpowers/tests/` |
| `docs/jules/` | `docs/superpowers/jules/` |
| `docs/operations/` | `docs/runbook/operations/` |
| `docs/sessions/` | `docs/handoffs/` |
| `docs/goals/` | Archive (or merge into root `GOALS.md`) |

## 5. No-loss Note

This proposal strictly **GROUPS** and **ARCHIVES** documents. **NO CONTENT IS DELETED.**
Files marked for archiving (e.g., `ryzen-memory-archive`, `jules-batch`, `aa01-handoff`, old
`plans`) are moved to `docs/archive/` because they represent point-in-time snapshots or retired
environments that are no longer actively maintained but must be preserved for historical reference.
The goal is to reduce cognitive load and search clutter while maintaining a complete, byte-for-byte
history.