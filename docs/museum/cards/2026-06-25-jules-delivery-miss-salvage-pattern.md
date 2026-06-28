---
title: Jules delivery-miss 7/7 -- salvage-da-changeSet obbligatorio nel ciclo
museum_id: M-2026-06-25-002
type: decision
domain: other
provenance:
  found_at: memory feedback_jules_failed_recovery + logs/jules-dispatch-2026-06.md
  git_sha_first: "0d1fe1e (PR #410)"
  git_sha_last: "733c8bd (PR #418)"
  last_modified: 2026-06-25
  last_author: claude-opus-4-8
  buried_reason: unintegrated
relevance_score: 5
reuse_path: scripts/fleet/jules-dispatch.ps1
related_pillars: []
status: curated
excavated_by: claude-opus-4-8
excavated_on: 2026-06-25
last_verified: 2026-06-25
---

# Jules delivery-miss 7/7 -- salvage-da-changeSet obbligatorio

## Summary (30s)

- **Cosa**: su 7/7 dispatch Jules (2026-06-25) la sessione e' arrivata a COMPLETED ma NON ha mai
  pubblicato il PR (delivery-miss). Il diff e' sempre stato recuperato da `outputs[].changeSet`
  o dagli activities artifacts -> salvage -> verify -> gate -> auto-merge.
- **Dove**: codemasterdd Jules workflow. Wrapper `scripts/fleet/jules-dispatch.ps1`.
- **Perche' conta ora**: il salvage NON e' un'eccezione di recovery -- e' una FASE FISSA del ciclo
  Jules. Ogni dispatch = dispatch + monitor + salvage + gate + merge.

## What was buried

Pattern empirico 7/7 (PR #410/#413/#414/#415/#416/#417/#418, tutti codemasterdd test/cleanup):
Jules esegue il lavoro (crea file, gira test, "all plan steps completed", sessionCompleted) ma la
consegna-PR non scatta e `outputs[].pullRequest` e' assente. Il diff vive in
`outputs[].changeSet.gitPatch.unidiffPatch` (a volte vuoto li' -> allora negli activities
`artifacts.changeSet.gitPatch.unidiffPatch`, ultimo snapshot stabile). Recupero deterministico:
estrai patch -> `git apply` su branch isolato -> run test -> commit (trailer ADR-0011) -> PR -> gate.

## Why it was buried

Non sepolto: pattern operativo fresco. Va in museum perche' contro-intuitivo -- "COMPLETED" suona
come "shipped", ma su questi dispatch COMPLETED != PR. Senza il record, una sessione futura
dichiarerebbe "Jules ha shippato" e perderebbe il lavoro.

## Why it might still matter

Ground-truth OBBLIGATORIO `outputs[].pullRequest.url` + `gh pr list` PRIMA di dire "shipped" su
QUALSIASI sessione Jules COMPLETED. Se assente -> delivery-miss -> salvage. Vale anche su sessioni
clean (no pollution): il gitPatch REST vuoto NON e' sempre causato da pollution.

## Concrete reuse paths

1. **Minimal**: dopo ogni Jules COMPLETED, check `outputs[].pullRequest.url`; assente -> salvage.
2. **Moderate**: estrai da `outputs[].changeSet` o activities artifacts (ultimo unidiffPatch),
   filtra scratch, applica solo i target contratti, verifica, PR.
3. **Full**: salvage come step standard del ciclo (vedi `feedback_jules_failed_recovery`).

## Sources / provenance trail

- Memory: `feedback_jules_failed_recovery` (broadened: COMPLETED-no-PR, non solo FAILED)
- Wrapper: `scripts/fleet/jules-dispatch.ps1` (5-gate, solido -- il gap e' la consegna, non l'authoring)
- Audit: `logs/jules-dispatch-2026-06.md`; 7 PR #410-#418 (main 0d1fe1e -> 733c8bd)
- Doctrine: `reference_jules_workflow`

## Risks / open questions

- Il gotcha uuidv7: `/proc/sys/kernel/random/uuid` NON esiste su Git-Bash Windows -> genera il
  Trace-Id ADR-0011 via `py -c` (secrets+time), mai quel path.
- Se Jules iniziasse a pubblicare i PR davvero, ri-verificare se il salvage e' ancora necessario.
