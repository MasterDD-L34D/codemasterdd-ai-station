# TDD Guard custom rules -- codemasterdd (mixed repo)

This repo is infra/governance: mostly docs, ADR/OD, ops scripts, glue.
A small designated behavior-code surface gets test-first. Scope is by
PATH ROLE, NOT by presence-of-tests (presence-based is circular: a new
module has no test -> would be exempt -> never gets a test -> TDD
defeated exactly when it matters most). Path-role is deterministic.

## ENFORCE test-first ONLY on (designated behavior-code allowlist)

Edit/write whose target path matches ANY:
- `apps/**/src/**` (mini-app source, e.g. dogfood-ui)
- `apps/**/*.py` excluding `apps/**/tests/**`
- `scripts/lib/**` (shared library modules -- real logic, reused)

For these: adding/modifying logic without a failing test first -> BLOCK.
A new behavior module here WITHOUT a test is exactly the case to block
(greenfield logic must start test-first), NOT exempt.

## ALWAYS PASS (everything else -- return valid, do NOT block)

- `**/*.md`, `docs/**`, `Archivio_*/**`, `.claude/**`, `**/*.tmp*`
- `*.json` / `*.yml` config & governance files
- One-off ops/maintenance scripts directly under `scripts/` and
  `scripts/hooks/**`, `scripts/setup/**`, `scripts/wrappers/**`
  (transformers, deploy, hooks, wrappers -- glue, not product logic)
- Test files themselves (`**/tests/**`, `test_*.py`, `*.test.*`)

## Tie-breaker

Uncertain whether a path is in the ENFORCE allowlist above? It is NOT
-> PASS. The ENFORCE set is an explicit allowlist; anything not listed
is non-blocking. This repo's value is cross-repo coordination and
governance, not blanket test-coverage of glue.
