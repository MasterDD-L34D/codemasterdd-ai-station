# .claude/agents

Recovery status: mixed active/dormant.

This registry was created for the original multi-repo workstation. In this
transplanted checkout, the external paths for Game, Synesthesia, Dafne, and AA01
are missing.

## Rule

Do not invoke cross-repo agents as live operators until the relevant repository
passes the reactivation gate in `../../EXTERNAL_REPOS.md`.

## Agent categories

### Potentially usable for this repo

These may be useful when their local inputs exist:

- `adr-drafter`
- `bench-reporter`
- `compact-conversation`
- `cost-monitor`
- `delegation-classifier`
- `dogfood-analyst`
- `harsh-reviewer`
- `owasp-security-auditor`
- `repo-health-auditor`

Even these agents must not assume missing runtime artifacts such as
`logs/aider-delegation-*.md` or `apps/dogfood-ui/data/dogfood.sqlite`.

### Dormant until external reactivation

These depend on missing external projects or old cross-repo context:

- `a11y-wcag-reviewer`
- `dafne-proposal-triager`
- `database-schema-designer`
- `game-balance-auditor`
- `game-design-validator`
- `game-systems-designer`
- `lore-consistency-checker`
- `privacy-policy-enforcer`
- `swarm-cycle-analyzer`

## Historical status

Before recovery, this registry listed 18 agents with 12 ready and 6 draft. That
status belongs to the original workstation context. It is not a current runtime
guarantee in this checkout.

## Reactivation

To reactivate an agent:

1. verify the target repository or runtime artifact exists locally;
2. verify the agent file does not contain stale path assumptions;
3. run a fresh smoke test;
4. update this README with the new current status.
