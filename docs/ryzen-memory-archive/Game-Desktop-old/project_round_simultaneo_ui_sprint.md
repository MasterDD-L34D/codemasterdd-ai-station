---
name: Round simultaneo UI sprint progress
description: Stato sprint UI planning-first (7 PR merged 2026-04-18) + prossimi step pianificati
type: project
originSessionId: ad7b4c38-9ddd-4c07-a3cf-09b519e075e8
---
Sessione 2026-04-18 ha completato sprint UI planning-first: 7 PR merged in main.

**Merged (in ordine)**:
1. #1536 — Fase A backend round simultaneo (/round/begin-planning + commit auto_resolve + unified resolver)
2. #1538 — /declare-intent server-side validation (9 codes: OUT_OF_RANGE, AP_INSUFFICIENT, ecc)
3. #1540 — visual preview intent (attack-target/move-dest markers) + multi-player labels
4. #1541 — shift-click own unit = clear intent
5. #1543 — scenari 3v3 + 4v4 coop
6. #1544 — pannello "Ordini pendenti" laterale con X button per clear
7. #1545 — resolve animation sequenziale 450ms pause tra azioni

**UI planning-first completa**: click unit → declare intent (preview) → shift-click o X button per clear → Risolvi Round (animazione ordinata per reaction_speed).

**Prossimo step proposto (non fatto)**:
- (B) Cell highlight durante animazione — cella attore pulsa arancione 400ms mentre azione risolve
- (D) Keyboard shortcuts — tasti 1-4 selezionano player unit, Enter = Risolvi, Esc = clear selezione

**Skip per ora**:
- Fase B planning timer (solo utile per networking, inutile hotseat)
- Fase C reazioni first-class (ADR-2026-04-15 follow-up #1, grosso refactor, aspetta playtest vero)
- Fog of intent server-side (SIS intents filtrati in response) — separato, ~1h
- Sound effects — polish, non bloccante

**Why**: gameplay UI era gap rispetto SoT §13.1 (planning simultaneo + reaction_speed ordered resolution). Sessione ha chiuso gap end-to-end backend + frontend.

**How to apply**: quando playtest vero rivela bug/gap, iterare sopra questo baseline. Non rifare round orchestrator da zero. Reazioni e timer sono ADR follow-up tracciati.
