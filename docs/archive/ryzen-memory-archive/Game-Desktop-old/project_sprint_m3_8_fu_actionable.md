---
name: Sprint M3.8 (2026-04-18) FU-M3.7 actionable
description: ToS verify Retro Diffusion + audio ADR ACCEPTED + MVP slice playbook 14h. 4 PR autonomous.
type: project
originSessionId: bacbe4b9-9e50-4dd9-9a8a-c21fcdd04a8a
---
**Sprint M3.8 post-M3.7 — AUTONOMO**. Eseguiti 3 FU-M3.7 actionable + audio ADR formalize. 4 PR merged.

## PR state (tutti merged)

| # | Lane | PR | Status |
|---|------|-----|:--:|
| 1 | ToS verify | #1591 Retro Diffusion audit + 43/ADR/CREDITS update | ✅ |
| 2 | Audio ADR | #1592 audio-direction DRAFT → ACCEPTED | ✅ |
| 3 | MVP playbook | #1594 asset-mvp-slice-playbook.md 14h | ✅ |
| 4 | Sprint close | #1596 sprint M3.8 doc | ✅ |

## Deliverables

### Retro Diffusion ToS verified

- Premium $10-25/mo → commercial + no watermark
- Training: licensed + pixel artists consent
- Free tier: watermarked, non-commercial
- `reports/asset_sourcing_audit_2026-04-18.md` — primo audit 90gg cycle

### Audio direction ACCEPTED

- Canonical "ambient organic + percussive cues"
- Ref: Hollow Knight + Into the Breach + Slay the Spire + Wildermyth
- 4 pillar audio (leggibilità tattica, ambient per biome, tension dinamica, TV co-op)
- Roadmap zero-cost (freesound + Bfxr/sfxr/Chiptone + OGA + Incompetech + Pixabay Music)
- Audio AI deferred (Suno/Udio RIAA lawsuits)
- Q-OPEN-21 + Q-OPEN-24 chiuse

### MVP slice playbook 14h

`docs/playtest/asset-mvp-slice-playbook.md` step-by-step:
- P0.1 Palette master .ase 3h (user Libresprite)
- P0.2 20+ UI icon Game-icons CC-BY 2h
- P1.1 Savana tileset Kenney 2h
- P1.2 Caverna Kenney+PixelFrog 2h
- P1.3 Foresta_acida OGA + AI Retro Diffusion 4h
- P1.4 Validation styleguide_lint.py 1h

Risk mitigation 6 categorie + execution log template.

## Gap status update

- **Gap #1 Art**: PIPELINE-READY (M3.7) + **PLAYBOOK-READY** (M3.8)
- **Gap #2 Audio**: DRAFT → **SPEC-COMPLETE + PIPELINE-READY**

## Q-OPEN closed totale (10 post-M3.6+M3.7+M3.8)

- M3.6: Q-15, Q-19, Q-22, Q-26, Q-27 (5)
- M3.7: Q-OPEN-19b downgrade 🔴→🟢
- M3.8: Q-21, Q-24 (2)

## Pattern tecnici acquisiti

1. **WebFetch + WebSearch combinati**: verify SaaS ToS current
2. **ADR DRAFT → ACCEPTED batch**: art (M3.6) + audio (M3.8) stesso pattern
3. **Branch switch bug recovery**: cherry-pick + amend quando commit finisce su wrong branch (ripetuto 3x in M3.8)
4. **Playbook step-by-step per user hands-on**: task granularity + commit messages + CLI snippet
5. **Audit log reports/ separato**: 90gg periodic verify history preserved
6. **Parallel session race**: altre session mergiano PR rapidly → rebase cascade repeated
7. **Stale CLEAN detection**: `BLOCKED` post-rebase spesso = CLEAN stale; verify via statusCheckRollup + try merge

## Follow-up FU-M3.8

| ID | Task | Blocker | Priorità |
|---|------|---------|:-:|
| A | Palette master `.ase` (user hands-on) | User tempo | 🟢 |
| B | MVP slice P0+P1 (14h playbook pronto) | User hands-on | 🟢 |
| C | Audio SFX cue list + ambient brief | User tempo | 🟡 |
| D | Audit next 2026-07-18 (90gg) | - | ⚪ |

## Memo guardrail rispettati

- Regola 50 righe: tutti PR docs only
- Nessun file in workflow/migrations/generation/contracts
- Nessuna dipendenza nuova
- Governance 0 errors

## Parallel session interference log

Durante M3.8 multiple PR parallel session mergiate su main:
- #1590 TKT-G (docs governance drift fix)
- #1593 TKT-C (replay telemetry verify)
- #1595 TKT-D (harness batch_calibrate vc_snapshot)

Ognuna ha causato rebase cascade M3.8 branches. Gestione: fetch + rebase + force-push sequenziale, recovery time ~3-5 min per ciclo.

## Critical path MVP (aggiornato post-M3.8)

- Art direction: PIPELINE-READY + PLAYBOOK-READY
- Audio direction: SPEC-COMPLETE + PIPELINE-READY (deferred post-MVP visuale)
- Asset commission: N/A (vincolo team)
- **Next actionable user task**: P0.1 palette master `.ase` 3h
