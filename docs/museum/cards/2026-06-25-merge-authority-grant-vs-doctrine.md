---
title: Merge-authority -- grant verbale reattivo vs doctrine deliberata SDMG-survived
museum_id: M-2026-06-25-001
type: decision
domain: other
provenance:
  found_at: memory feedback_merge_authority + docs/adr/0037-merge-autonomy-model.md
  git_sha_first: "0d1fe1e (first exercise PR #410)"
  git_sha_last: "unknown (ongoing)"
  last_modified: 2026-06-25
  last_author: claude-opus-4-8
  buried_reason: unintegrated
relevance_score: 5
reuse_path: docs/adr/0037-merge-autonomy-model.md
related_pillars: []
status: curated
excavated_by: claude-opus-4-8
excavated_on: 2026-06-25
last_verified: 2026-06-25
---

# Merge-authority -- grant verbale vs doctrine SDMG-survived

## Summary (30s)

- **Cosa**: un grant verbale reattivo ("merge dopo review + procedi") NON supera una doctrine
  deliberata-e-falsificata (ADR-0037). Risolto: codemasterdd auto-merge-dopo-gate = ATTIVO;
  Game-family merge = SOLO via amendment ADR-0037 + SDMG harsh-review (non override).
- **Dove**: codemasterdd hub governance. ADR-0037 + memory `feedback_merge_authority`.
- **Perche' conta ora**: e' la 3a volta che un grant reattivo prova ad allargare la merge-autonomy;
  le 2 precedenti (ADR-0038/0039 grant-tier) furono SDMG-killed. Il pattern e' load-bearing.

## What was buried

2026-06-24/25 Eduardo: "dopo la review puoi fare i merge e procedere". Conflitto: ADR-0037
(Accepted, sopravvissuto a falsificazione harsh-reviewer) dice external-merge = Eduardo-explicit
finche' non earned via governor R0->R1->R2; fiat scoped standing-grant (Option B) = RIGETTATO
(grant-before-evidence). Risoluzione ratificata (AskUserQuestion, 2 card):
- **codemasterdd** merge-dopo-gate = ATTIVO (gia' coerente con ADR-0037 per-call classifier;
  gate = CI verde + P1 risolti + harsh-review su file security/governance/freeze; rebase per
  preservare i trailer ADR-0011).
- **Game-family** (Game/Godot-v2/Game-DB) = NON attivo; pursuit via amendment ADR-0037 + SDMG
  harsh-review, e comunque classifier-block a livello tool (settings.json P0-3 Eduardo-manual).

## Why it was buried

E' un landmark di governance, non un artifact sepolto: curato fresco perche' ricorrente. La
tentazione "grant verbale = autonomia" si ripresenta ogni volta che Eduardo, reattivo, allarga
la delega; senza un record la doctrine SDMG-survived viene erosa.

## Why it might still matter

Prossima volta che arriva un grant di merge-autonomy: NON estendere a repo esterni senza
amendment esplicito di ADR-0037 + un SDMG pass che superi le 3 obiezioni note (external
classifier-block; free-tier no-required-checks => "CI-gated" falso; allow-rule gh-pr-merge non
narrow-esprimibile). La via pulita verso Game-family = governor R2 earn-path (clean-cycle banking).

## Concrete reuse paths

1. **Minimal**: consulta `feedback_merge_authority` prima di agire su qualsiasi grant di merge.
2. **Moderate**: se serve Game-family merge -> drafta amendment ADR-0037 + harsh-reviewer SDMG.
3. **Full**: matura il governor R2 (>=4 clean reconcile-cycle, >=2 repo, fix STATUS clock-leak).

## Sources / provenance trail

- Memory: `feedback_merge_authority`, `feedback_external_repo_action_boundary`
- ADR: `docs/adr/0037-merge-autonomy-model.md` (+ 0038/0039 i grant killed)
- First exercise: PR #410 (rebase-merge, trailer ADR-0011 preservato), main 0d1fe1e
- Earn-path: `docs/governance/actor-activation-criteria.md` sec 3 (R2 conditions)

## Risks / open questions

- Game-family merge resta gated finche' R2 non earned -- NON aggirare il classifier-block.
- Il fix STATUS clock-leak (ADR-0039 dec.1) e' prerequisito per la distribuzione >=2-repo.
