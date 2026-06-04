---
name: Parked ideas catalog 2026-04-18
description: 28 idee deferite + 7 completate durante sessione 2026-04-18. Cross-ref a docs/planning/ideas/IDEAS_INDEX.md per dettagli + trigger re-open. Evita perdita contesto prossima sessione.
type: project
originSessionId: ad7b4c38-9ddd-4c07-a3cf-09b519e075e8
---
Sessione 2026-04-18 (20 PR merged) ha prodotto 28 idee parked + 7 completate. Catalogo completo in `docs/planning/ideas/IDEAS_INDEX.md` (repo, team-visible). Questa è la quick-reference per Claude Code prossima sessione.

## Dove guardare

- **Canonical**: `docs/planning/ideas/IDEAS_INDEX.md` (5 sezioni + completate)
- **Trigger re-open** per ogni idea: inline tabelle IDEAS_INDEX
- **Archive kill-60**: `docs/archive/flint-kill-60-2026-04-18/MANIFEST.md` (per idee che ri-aprire violerebbe policy)
- **Flint roadmap**: `flint/PROJECT.md` §7 (v0.3/v1.0/v2.0 gated)

## Raggruppamento 28 parked

| Dimensione | Count | Priority re-open |
|------------|:---:|------------------|
| Round simultaneo follow-up | 8 | Alta se playtest reale rivela gap (Fase C reazioni, fog of intent) |
| Flint v0.3 roadmap | 6 | Media, gate 30gg dal 2026-04-18 (v0.3 valid) |
| Flint v1.0 adopter-gated | 6 | Bassa, richiede 1+ adopter esterno |
| Lean chat divergence | 4 | ⚠️ 1 ROSSO (hook auto-speak) = violazione kill-60 |
| Infrastruttura single-user | 4 | Host-specific, doc-only |

## Completate (non parked)

- `/meta-checkpoint` pattern codificato (PR #1553)
- Research-critique workflow (feedback §9)
- Classification framework 4D riusabile
- Archive preservation pattern
- Flint rename + self-contained + PROJECT.md canonical

## Top-5 priority re-open (se Evo-Tactics torna attivo domani)

1. **Fase C reazioni first-class** (#2) — core gameplay, ADR follow-up #1 aperto
2. **Fog of intent server-side** (#3) — networking Fase 2 prerequisite
3. **Action preview panel** (#6) — UX reale giocatore
4. **5v5+ scenari** (#8) — stress test multi-player
5. **Eval set classifier** (#11) — Flint v0.3 diagnostica credibile

## Anti-pattern da evitare (kill-60 enforcement)

Idee 🔴 che ri-aprire senza motivo validato violerebbe policy:

- #14 Achievement progress Flint (gamification backfire — Liberty/NTNU)
- #24 Hook post-commit auto-speak (friction — Stackdevflow 2026)

Se utente chiede queste → prima rileggere `reference_flint_optimization_guide.md` + chiedere sample validation.

## Idea Engine backend status

Infrastruttura presente (`apps/backend/` route `/api/ideas/*` + `docs/config/idea_engine_taxonomy.json`) ma **storage vuoto** (no DB, no submissions). Usa `IDEAS_INDEX.md` come registro canonico invece del backend finché non validato. Tracking pattern: doc-first, DB-later.

## Why this file

User ha chiesto espressamente (sessione 2026-04-18, post kill-60): "che idee abbiamo messo da parte in questa conversazione? che idee abbiamo nell'idea engine?". Risposta: 28 parked, 0 in idea engine backend. Questo catalogo evita perdita cross-session.

## How to apply

- Prossima sessione: leggi questo + IDEAS_INDEX
- Se utente chiede "cosa è rimasto aperto?" → cita top-5 priority
- Se utente chiede idea specifica di re-open → verifica trigger + classification prima
- Se nuova idea emerge in sessione → append a IDEAS_INDEX con trigger re-open esplicito

## Drop off-repo (2026-04-18 E+K decision)

Drop design sessions chat Linea B preservato OFF-REPO a `C:\Users\VGit\Downloads\flint-repo-drop.zip` + estratto in `flint-repo-drop/`. Zero commit in repo (decisione E) — scope creep doc + viola kill-60 [G] scala pre-validazione.

Contenuto drop (18 file, ~6400 LOC):

- 2 ADR (`ADR-2026-04-18-flint-kill-60-policy.md` + `-design-reconciliation.md`)
- Archive `flint-design-sessions-2026-04-17_18/` con MANIFEST + 00-summary + 6 sottodir
- 01-original-design/ (v1 + anime + profiles addendum)
- 02-lean-design/ (DESIGN_DOC Lean post-critique)
- 03-research/ (DEEP_RESEARCH_v2_critique + ANALISI_MASTER)
- 04-guides/ (RESEARCH_TODO + GUIDA_FASE_A + PROMPT_PER_CODEX)
- 05-reusable-patterns/ (6 pattern originali + 4 promossi 2026-04-18)
- 06-research-addendum/ (DEEP_RESEARCH_2026-04-18 50+ fonti)

## Re-open conditions dettagliate 4D (da ADR-2026-04-18-flint-design-reconciliation §2.3)

Cross-ref a IDEAS_INDEX §4 (Lean chat divergence) con classificazione 4D full:

### #21 — 4 archetipi "Anime" (Arbitro/Bestiario/Archivista/Sentinella)

- Valore teorico: Alto (varietà narrativa + modular architecture)
- Applicabilità: Low-fit (1 solo-dev, 1 tool, 0 adopter)
- Stato: Killed-pending-rework (riesumabile con architettura diversa)
- Re-open: **≥3 voci distinte emergono spontaneamente dall'uso reale** OR team ≥3 richiede separazione ruoli

### #22 — 3 lingue (IT/EN/ES grammatica rotta autentica)

- Valore teorico: Medio (ampliamento utenza potenziale)
- Applicabilità: No-fit (0 adopter non-italiani)
- Stato: Killed-clean
- Re-open: **≥1 adopter esterno non-italiano richiede localizzazione**

### #XX — PR suggestion come commento (NON in IDEAS_INDEX attuale)

- Valore teorico: Alto (workflow review automatico)
- Applicabilità: No-fit (solo-dev, 0 PR review process attivo)
- Stato: Killed-clean
- Re-open: **Team ≥3 AND PR review collo di bottiglia misurato ≥1 settimana dati**

### #23 — Persona switching (4 persona-file markdown)

- Valore teorico: Alto (clean architecture voice multiple)
- Applicabilità: Low-fit (1 sola voce attualmente)
- Stato: Killed-pending-rework
- Re-open: **≥3 persone/voci distinte emergono dall'uso**

## Re-open workflow

Se utente chiede re-open di una di queste 4:

1. Verifica condition misurabile vs stato attuale
2. Se ≥1 condition soddisfatta → apri drop `flint-repo-drop/docs/archive/flint-design-sessions-2026-04-17_18/02-lean-design/DESIGN_DOC.md` per design base
3. Se nessuna condition soddisfatta → cita memory + rifiuta (kill-60 enforcement)
4. Se insistito con override esplicito → scrivi nuovo ADR reconciliation, non discussione ad-hoc

## Pattern NON cherry-picked (still in drop off-repo)

Questi pattern del drop sono rimasti OFF-REPO perché violano kill-60 o duplicano memory attuale:

- Layer 3 Tombstone primitive (novel synthesis N=1, viola [E])
- Cognitive-load budget (novel N=1 experimental)
- Layer 2 Spark→TIL→ADR ladder (valido ma 0 uso reale — parked)
- State+Date kill criteria YAML (concetto già in `reference_classification_4d.md` re-open cost)

Se in sessione futura 3+ volte pattern emerge → apri drop e valuta cherry-pick.
