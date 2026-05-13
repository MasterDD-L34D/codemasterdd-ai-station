# Cross-repo coordination

Index per Component 2 (PR workflow) + Component 3 (escalation gates + Gate E discipline) — spec V3 Opt 1.5 REDUCED.

## Documenti

- [PR_WORKFLOW.md](PR_WORKFLOW.md) — workflow drafting PR cross-repo + governance interna handling
- [PR_TEMPLATE.md](PR_TEMPLATE.md) — body template PR cross-repo
- [ESCALATION_GATES.md](ESCALATION_GATES.md) — Gate A/B/C/D/E criteri + thresholds

## Scripts

- `scripts/cross-repo/dry-run-pr.ps1` — validatore dry-run pre-PR
- `scripts/cross-repo/coord-event-log.ps1` — helper logging coord events Gate E
- `scripts/cross-repo/install-gate-e-reminder.ps1` — schtasks weekly reminder

## Tracking logs (gitignored)

- `logs/cross-repo-pr-YYYY-MM.md` — PR outcome tracking
- `logs/coord-events-YYYY-MM.md` — Gate E event tracking
- `logs/escalation-gates-YYYY-MM.md` — Gate A/B/C/D tracking

## Riferimento spec

[docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md](../superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md) V3 (PR #87).
