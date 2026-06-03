# Jules daily digest 2026-05-18 (ADR-0034 Option D, READ-ONLY, heuristic v4.1: PR-state+files)
> Signal = Jules session -> linked GitHub PR -> {merge-state, changed files}. Independent of prompt text.
> ARCHIVE = linked PR MERGED & no freeze file (shipped, rework). ACTIONABLE = PR closed-unmerged/open or Jules-asking (NOT shipped).
> DEFER = PR touches / task targets a freeze-sensitive path (Eduardo-review, never auto, even if shipped). AMBIGUOUS = no clear signal.
> Verdicts ADVISORY. Generative (archive/respond/start) = Eduardo per-cycle batch-approve, NOT auto.

Awaiting sessions: 4

- `1111111111111111111` [MasterDD-L34D/Game] **ACTIONABLE (linked PR CLOSED unmerged -> NOT shipped)** -- fix a thing  | PR#10 closed-unmerged -> Claude: abandon/retry?
- `2222222222222222222` [MasterDD-L34D/Game] **ARCHIVE (shipped: linked PR merged)** -- already shipped  | PR#11 MERGED 2026-05-17 | files: a.js,b.js
- `3333333333333333333` [MasterDD-L34D/Game] **DEFER (freeze-path; PR merged but Eduardo-review)** -- combat tweak  | PR#12 MERGED, touches freeze: apps/backend/services/combat/x.js
- `4444444444444444444` [MasterDD-L34D/Game] **AMBIGUOUS (no PR, unclear activity)** -- unclear state  | f -> Claude-eval

## Manuale (non scriptabile)
- Suggestions: jules.google dashboard per-repo (browser-only, no API list).
- ACTIONABLE/IN-PROGRESS/AMBIGUOUS: Claude ground-truth (activities/diff) -> scoped response or start, drafted in batch.

## Gate (ADR-0034 Option D)
Digest = enumeratore advisory. Nessuna azione auto.
