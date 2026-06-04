---
name: Round simultaneo Fase A
description: PR #1536 apre planning-first flow (SoT §13.1 + ADR-2026-04-15). Context per sprint successivi.
type: project
originSessionId: ad7b4c38-9ddd-4c07-a3cf-09b519e075e8
---
PR #1536 (branch feat/round-simultaneo-fase-a) implementa Fase A round simultaneo:
- Endpoint nuovo POST /api/session/round/begin-planning → SIS dichiara in planning condivisa, hazard/bleeding applicati
- /commit-round ora supporta { auto_resolve: true } → risolve round completo in un call
- UI playtest HTML default-switched a planning-first (click=intent, Risolvi=commit+resolve)
- Scenario 2v2 "coop_2v2" + UI multi-player con pendingIntents map keyed by unit_id

**Why**: SoT §13.1 + ADR-2026-04-15 definiscono modello planning simultaneo → commit → resolve ordinato per reaction_speed. Flow precedente era sequenziale (/action istantaneo per player, /turn/end per SIS dopo). Gap documentato nel SoT ma mai wirato.

**How to apply**:
- Modificare flow round UI: modificare apps/backend/public/Evo-Tactics — Playtest.html (NON più apps/dashboard/)
- Nuovo resolver unificato: apps/backend/routes/sessionRoundBridge.js → buildUnifiedRoundResolver(session) gestisce player + SIS in stesso resolve pass
- Legacy /action + /turn/end mantenuti per retrocompat test — nuovo UI li bypassa
- shouldAutoAdvance({ requirePlayerOnly: true }) per ready check player-only

**Gap residui (follow-up)**:
- /declare-intent NON valida range/AP server-side → intent fuori range accettato poi fallisce a resolve
- SIS pressure_cap limita intents/round (Calm=1, Apex=3) — in 2v2+ serve pressure>=25 per 2 SIS agire insieme
- playerView() fog-of-intent non implementato → needed solo per networking Fase 2
- Planning timer (is_planning_expired) solo in Python, non portato Node (ADR-2026-04-15 follow-up #6)
- Reazioni first-class (counter/overwatch via API) ancora embedded in resolve (ADR follow-up #1)
