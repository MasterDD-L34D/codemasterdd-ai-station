# External repositories registry

This file replaces live cross-repo governance for the transplanted checkout.

Rule: an external repository is dormant until it passes the reactivation gate
below. Historical references remain valuable, but they are not active plans.

## Reactivation gate

Before this repo can govern or coordinate any external project again, verify:

1. Local path exists on the current machine.
2. Git remote is reachable and matches the expected repository.
3. Branch and working tree state are known.
4. Runtime dependencies, if any, are installed or intentionally skipped.
5. Sensitive files are absent from cloud delegation scope.
6. The current user explicitly wants that repo reactivated.
7. `STATUS_MULTI_REPO.md` is updated from fresh evidence, not old notes.

If any item fails, the repo stays dormant.

## Registry

| Project | Historical path | Expected remote | Current status | Recovery action |
|---------|-----------------|-----------------|----------------|-----------------|
| Evo-Tactics / Game | `C:\dev\Game` | `github.com/MasterDD-L34D/Game` | dormant, path missing in this checkout | Do not govern. Reactivate only from a real local clone. |
| Synesthesia | `C:\dev\synesthesia` | `github.com/MasterDD-L34D/synesthesia` | dormant, path missing in this checkout | Do not govern. Reactivate near real exam work only. |
| Dafne swarm / evo-swarm | `C:\Users\edusc\Dafne\workspace\swarm` | `github.com/MasterDD-L34D/evo-swarm` | dormant, path missing in this checkout | Do not start, patch, or monitor from here. |
| AA01 / Archon Atelier 01 | `C:\Users\edusc\aa01` | none recorded in repo | dormant, path missing in this checkout | Treat as personal external workspace, not part of this repo. |

## Active boundary

Active scope for this repository:

- repository structure
- ADR index and documentation consistency
- portable workstation setup documentation
- scripts and infra that live inside this repository
- dogfood/observability scaffolding only when local runtime evidence exists

Out of scope until reactivated:

- Game design, balance, lore, or swarm integration
- Synesthesia privacy validation
- Dafne process persistence and voice/widget/chat plans
- AA01 task review or archive flows

## Quarantine policy

Cross-repo references may remain in historical docs, ADR, session logs, and
agent definitions. They must be labelled dormant in current governance and must
not be used as active next actions.

Preferred language:

- "historical"
- "dormant"
- "requires reactivation"
- "not verified in this checkout"

Avoid language such as:

- "active"
- "up"
- "pending today"
- "ready to run"
- "source of truth"

unless verified on the current machine.
