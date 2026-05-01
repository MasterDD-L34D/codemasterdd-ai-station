# ADR-0021 - Structural recovery and external repo quarantine

- Status: Accepted
- Date: 2026-05-01
- Deciders: Eduardo Scarpelli, Codex recovery branch

## Context

The repository was transplanted away from the original workstation. The
transplanted checkout did not contain the original external project paths,
runtime evidence, API key files, Aider wrappers, or service state referenced by
older governance docs.

Before recovery, root documents mixed:

- live workstation governance;
- historical dogfood evidence;
- cross-repo dashboards;
- external repo next actions;
- OpenCode/Aider/Ollama model-routing plans;
- app/infra scaffold;
- personal archive material.

That made future agents likely to revive stale plans as if they were current.

## Decision

Adopt structural recovery mode:

1. `codemasterdd-ai-station` governs only itself by default.
2. External repos are quarantined as dormant until reactivated.
3. `PROJECT_STATE.yaml` is the minimal machine-readable state.
4. `EXTERNAL_REPOS.md` is the registry and reactivation gate for external repos.
5. `docs/recovery/active-vs-historical-boundary.md` defines active vs
   historical/dormant areas.
6. `scripts/check-recovery-consistency.ps1` prevents obvious stale-state
   regressions in active guidance.
7. OpenCode remains a portability/client option, not an active dependency.
8. Aider remains the historical primary execution client, not locally assumed.
9. dogfood-ui and infra remain scaffold/dormant until runtime evidence is
   restored or regenerated.
10. Dafne integration is opt-in through `DAFNE_ENABLED=1`, never assumed live.

## Consequences

### Positive

- New agents can understand current scope quickly.
- Old cross-repo plans no longer become accidental tasks.
- The branch can be reviewed from the correct PC without modifying `main`.
- Runtime evidence must be explicit, not implied.
- OpenCode, Aider, and Ollama can be re-evaluated cleanly.

### Negative

- Some rich historical context is no longer in the primary instruction path.
- Cross-repo agents are less convenient until reactivation.
- The original dashboard semantics are reduced until runtime state is restored.

### Neutral

- Historical ADR, Journal, sessions, and archive material are retained.
- This is not a deletion pass.

## Alternatives considered

### Keep old cross-repo dashboard live

Rejected. The referenced paths are missing in the transplanted checkout, so the
dashboard would provide false confidence.

### Delete external repo material

Rejected. The historical context may be valuable on the correct PC.

### Merge everything into one instruction file

Rejected. It would recreate the original problem: too much state in one place.

### Make OpenCode the new primary client

Rejected for this branch. OpenCode is a useful portability bridge, but it is not
verified as installed or configured here.

## Implementation

- `PROJECT_STATE.yaml`
- `EXTERNAL_REPOS.md`
- `SPRINT_02.md`
- `docs/recovery/*`
- `AGENTS.md`
- `CLAUDE.md`
- `MODEL_ROUTING.md`
- `scripts/check-recovery-consistency.ps1`
- `scripts/recovery-status.ps1`
- `scripts/check-all.ps1`
- `config/system-map.yaml`
- `config/machine-profile.example.yaml`
- `apps/dogfood-ui/templates/recovery.html`

## Follow-up

- On the correct PC, run `docs/recovery/pre-merge-checklist.md`.
- Reactivate external repos one at a time.
- Decide whether OpenCode should become a real secondary client.
- Decide whether dogfood-ui runtime should be restored or kept as scaffold.
