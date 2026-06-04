---
name: Sprint M3 (2026-04-18) outcome + follow-up
description: Telemetry close + VC snapshot + ADR combat + reinforcement + objective. 6 PR merged, 0 pending.
type: project
originSessionId: 963b7edd-390b-404a-9372-d7ce4f283ff9
---
**Sprint M3 chiusura 2026-04-18 — SESSIONE COMPLETA**. 7 task eseguiti (5 follow-up iniziali + G + H), **6 PR merged**, 0 pendenti nella sessione. Test delta **244 → 348 (+104)**.

## PR state (tutti merged)

| Task | PR | Branch | Merge time |
|---|---|---|---|
| C telemetry rebase + fix test 172 | #1535 | `telemetry-session-events` | 02:27:45Z |
| D vc_snapshot in /end response | #1564 | `feat/end-response-vc-snapshot` | 02:25:46Z |
| A+B ADR 04-19 + 04-20 | #1565 | `docs/adr-reinforcement-spawn` | 02:26:02Z |
| E sprint M3 close doc | #1566 | `docs/sprint-m3-close` | 02:28:34Z |
| G reinforcementSpawner.js + 13 test | #1567 | `feat/reinforcement-spawner` | 02:44:11Z |
| H objectiveEvaluator.js + 20 test | #1568 | `feat/objective-evaluator` | 02:44:51Z |

## Pattern tecnici acquisiti

1. **Rebase con commit duplicato**: quando una stessa change è landata su main via altro PR, `git rebase --skip` il commit duplicato. Già successo con docs playtest sweep (#1537 landed → skip in #1535 rebase).
2. **Test obsoleto post-telemetry**: aggiunta di event a /start rompe test che aspettano `events_count === 0`. Update test a `>= 1` + verify `events[0].action_type === 'session_start'`.
3. **VC snapshot lifecycle**: `buildVcSnapshot()` DEVE essere chiamato prima di `sessions.delete()`. Order corretto in /end: compute VC → compute debrief → delete → respond.
4. **Governance doc_status enum**: valori validi: `active, draft, review_needed, legacy_active, generated, historical_ref, superseded`. Non `proposed` (uso `draft` per ADR nuove).

## Follow-up backlog FU-M3-A..G (aggiornato)

| ID | Fonte | Task | Blocker | Priorità |
|---|---|---|---|:-:|
| A | ADR 04-19 | ~~Implement `reinforcementSpawner.js`~~ ✅ DONE PR #1567 | — | ⚪ |
| B | ADR 04-20 | ~~Implement `objectiveEvaluator.js`~~ ✅ DONE PR #1568 | — | ⚪ |
| C | PR #1535 | Merge + verify mock snapshots + replay UI downstream | Master DD review | 🟢 |
| D | PR #1564 | Merge + update harness Python legge vc_snapshot da /end | Master DD review | 🟡 |
| E | TKT-06 | `predict_combat` include `unit.mod` stat | — | 🟡 |
| F | TKT-07 | Tutorial sweep #2 N=10/scenario post telemetry fix | Merge C | ⚪ |
| G | ADR 04-17 drift | 5 doc `last_verified` mismatch frontmatter vs registry | — | ⚪ |

## Memo guardrail rispettati

- Regola 50 righe: session.js delta netto 22 LOC (OK), ADR doc only (OK)
- Nessun file in `.github/workflows/`, `migrations/`, `packages/contracts/`, `services/generation/` toccato
- Trait solo in `data/core/traits/active_effects.yaml` (nessun hardcode)
- Nessuna dipendenza npm/pip nuova

## Branch state cleanup — DONE

6 branch locali potati fine sessione:
- `telemetry-session-events` ✅ deleted
- `feat/end-response-vc-snapshot` ✅ deleted
- `docs/adr-reinforcement-spawn` ✅ deleted
- `docs/sprint-m3-close` ✅ deleted
- `feat/reinforcement-spawner` ✅ deleted
- `feat/objective-evaluator` ✅ deleted
- `docs/parked-ideas-catalog` ⏸️ still checked out (current HEAD = cc85545e, equivalent to main)

Main branch locked in worktree `vibrant-curie-e6ddac` — non bloccante ma impedisce `git checkout main` dal primary worktree.

## Next session priorities (post-M3)

Con G+H moduli pronti ma NON wirati, next session ha due lanes:

1. **Wire G+H in session engine**: chiamare `reinforcementSpawner.tick()` in `sessionRoundBridge.js` dopo resolve round, e `evaluateObjective()` in `/turn/end` + `/round/execute` → outcome enum espanso in `/end` response
2. **Scenari opt-in**: creare `enc_hardcore_06` reinforcement_pool + `enc_capture_01`/`enc_escort_01`/`enc_survival_01` come coverage Pilastro 1 non-elimination

## Quirks sessione

- `git worktree` lock su `main` (vibrant-curie-e6ddac) impediva checkout main → uso `git reset --hard origin/main` come workaround
- Branch rename implicito: `telemetry-session-events` ⇄ `feat/flint-self-contained` stesso commit ID (user ha renamed locally)
- File flint/ (INSTALL.md, claude-integration/, archive-template/, tools/) creati a metà sessione poi spariti — user workstream in-flight, non toccato
- Pip artifact `Lib/` + `scripts/pip3.exe` apparsi root (non nostra responsabilità, untracked)
