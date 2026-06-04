---
name: Codex P2 review iteration pattern (2026-05-06 sessione)
description: Codex P2 review fa multiple round iterativi su stesso PR — round N+1 emerge solo dopo fix round N. Pattern affidabile per catch edge case post-fix. Sessione 2026-05-06 sera: 8× P2 across 4 PR, 3 round consecutivi su PR #193 Godot v2.
type: feedback
originSessionId: 74a9b30c-8a6a-4e9e-bfaf-285e90ee116a
---
# Codex P2 review iteration pattern

**Pattern**: Codex review automated fa MULTIPLE round iterativi sullo stesso PR. Round N+1 issues emergono SOLO dopo fix round N (Codex re-analizza diff + scopre edge case nuovi creati dal fix stesso o non visibili pre-fix).

**Why**: Codex usa LLM-based pattern recognition con context fisso (~commit reviewed). Quando code cambia significativamente, nuovo review trova nuove cose. Un singolo `@codex review` post-fix vale come "secondo paio occhi" gratis — costa 0 effort.

**How to apply**:

1. **Default workflow post-Codex-fix**: dopo aver pushato fix per Codex P2, ritrigger `gh pr comment <PR> --body "@codex review"` (o aspettare auto-trigger se Codex fired su push). NON considerare PR "done" dopo round 1 fix.
2. **Threshold round**: 3 round consecutivi è normal (sessione 2026-05-06 PR #193 Godot v2). Stop quando Codex ritorna "Didn't find any major issues. Delightful!" o equivalente clean-state.
3. **Round 1 vs 3 quality**: round 1 cattura issue ovvi (host filter, phase gate stretto). Round 2-3 cattura subtle race conditions / state-machine edge case (auto-select emit storm post-fail, transition stage bypass via phase_change ordering). Round 3 spesso il più valuable.
4. **Fix esempio sessione 2026-05-06**:
   - PR #2073 W4: 1 round host filter (allPids includeva hostId) → fix shipped
   - PR #2075 W7: 1 round phase gate widen + 2nd round "Delightful!" clean
   - PR #2076 plan v3 doc: 1 round 3 issues compositi (combat services misclassified + routes unversioned + auth route doesn't exist) → tutti fix in 1 commit
   - PR #193 Godot v2: **3 round consecutivi** — retryable choices → countdown reset + non-host transition → defer phase_change swap until transition_complete

**Anti-pattern**:

- ❌ Mergiare PR dopo round 1 fix senza re-trigger Codex review = perdere ~2-3 issue successivi affidabili
- ❌ Considerare comment OLD su commit pre-fix come "ancora aperto" — verifica `comment.commit_id` vs current HEAD; se diverge + outdated=True, già addressed
- ❌ Implementare fix speculativi senza grep verify (es. round 1 #2076 io ho assunto traitEffects.js fosse in combat/ — Codex caught + costretto reverify con `ls apps/backend/services/combat/`)

**Skip rules**:

- Doc-only PR con zero code change: 1-2 round basta
- PR con state machine complesso (M.6 Godot phone view race conditions WS-driven): aspettarsi 3+ round
- PR con timing-sensitive code (timeout, transition, retry): aspettarsi 2-3 round (Codex specifically catches these)

**Reference incidents**: docs/reports/2026-05-06-coop-phase-ws-audit.md addendum + memory project_session_2026_05_06_w4_w7_m6_codex_iteration.md.
