# Governance

Home consolidata per la governance cross-repo: PR workflow, escalation gates,
criteri di attivazione attori, review discipline, execution board.
Consolida gli ex `cross-repo/` + `reviews/` (riassetto 2026-06-04).

## Documenti

- [PR_WORKFLOW.md](PR_WORKFLOW.md) -- workflow drafting PR cross-repo + governance interna handling
- [PR_TEMPLATE.md](PR_TEMPLATE.md) -- body template PR cross-repo
- [ESCALATION_GATES.md](ESCALATION_GATES.md) -- Gate A/B/C/D/E criteri + thresholds
- [actor-activation-criteria.md](actor-activation-criteria.md) -- earn-path + clean-cycle definition + off-ramp (N=3) per gli attori del governor
- [gate-e-evidence.md](gate-e-evidence.md) -- evidence log Gate E (adoption / health signals)
- [flow-chart-harsh-review-2026-05-09.md](flow-chart-harsh-review-2026-05-09.md) -- flow chart harsh review (ex `reviews/`)
- [EXECUTION-BOARD.md](EXECUTION-BOARD.md) -- board cross-repo, regione AUTO-SYNC mantenuta da `tools/playtest2-board-sync.sh`
- `_TEMPLATES/` -- template riutilizzabili

## Scripts collegati

- `scripts/cross-repo/dry-run-pr.ps1` -- validatore dry-run pre-PR
- `scripts/cross-repo/coord-event-log.ps1` -- helper logging coord events Gate E
- `scripts/cross-repo/install-gate-e-reminder.ps1` -- schtasks weekly reminder

(Nota: gli script restano in `scripts/cross-repo/`, non spostati.)

## Codice che referenzia questa dir

- `apps/cross-repo-dashboard/governor/reconcile.py` -- carve-out doctrine include `docs/governance/`
- `tools/playtest2-board-sync.sh` + `.github/workflows/playtest2-board-sync.yml` -- scrivono `EXECUTION-BOARD.md`

## Tracking logs (gitignored)

- `logs/cross-repo-pr-YYYY-MM.md` -- PR outcome tracking
- `logs/coord-events-YYYY-MM.md` -- Gate E event tracking
- `logs/escalation-gates-YYYY-MM.md` -- Gate A/B/C/D tracking

## Riferimento spec

[docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md](../superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md) V3 (PR #87).
