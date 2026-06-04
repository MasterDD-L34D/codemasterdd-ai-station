---
name: Classification 4D framework (Flint standard)
description: 4-axis framework per classificare asset (code/memory/doc/skill) prima di keep/kill/archive. Derivato da kill-60 Flint sessione 2026-04-18. Sync da flint/claude-integration/memory/reference_classification_4d.md — user-level copy per uso cross-project.
type: reference
originSessionId: ad7b4c38-9ddd-4c07-a3cf-09b519e075e8
---
Framework 4D riusabile per decisioni kill/keep/archive su asset software. Applicare PRIMA di eliminare o codificare, non dopo.

## I 4 assi

| Asse | Valori | Domanda che risponde |
|------|--------|----------------------|
| **Valore scope** | 🟢 alto · 🟡 medio · 🔴 basso | Serve davvero al progetto? |
| **Applicabilità** | universal / gamedev / data-ops / solo-dev / single-user / `<project>`-only | Chi può riusarlo oltre me? |
| **Stato sviluppo** | production / experimental / draft / deprecated / consolidated / killed | Maturità code/doc? |
| **Re-open cost** | XS (<30min) · S (≤2h) · M (≤1gg) · L (>1gg) · XL (>settimana) | Se kill e devo riportarlo, quanto costa? |

## Quando applicare

- Prima di archive (MANIFEST 4D obbligatorio, vedi `flint/archive-template/MANIFEST-template.md`)
- Prima di codificare memory file (gate: osservato ≥3 volte + 🟢 valore)
- Durante parked ideas catalog (`IDEAS_INDEX.md` format canonico)
- In ADR kill decision (per giustificare voto)
- Prima di commit drop esterno in repo (pattern E+K preservation)

## Regola kill-60

Asset 🔴 basso + single-user + draft + XS/S re-open cost → **kill candidate**.
Asset 🟢 alto + universal + production + L re-open cost → **keep hard**.

## Esempi riusciti

- **Flint achievement system** (PR #1556): 🔴 · single-user · draft · S → killed (research backfire)
- **Hook post-commit auto-speak** (PR #1558): 🔴 · single-user · draft · XS → killed (friction)
- **`/meta-checkpoint` command** (PR #1553): 🟢 · universal · production · L → **keep** (riusabile cross-project)
- **Research-critique §9** (flint/claude-integration): 🟢 · universal · production · M → **keep**
- **Drop Flint design sessions** (sessione 2026-04-18): 🟡 · universal · draft · L → **preserve off-repo** (E+K decision, no commit)

## Output canonico (tabella)

```
| Dimensione     | Valore                  |
|----------------|-------------------------|
| Valore scope   | 🟢 / 🟡 / 🔴            |
| Applicabilità  | <categoria>             |
| Stato sviluppo | <stato>                 |
| Re-open cost   | XS / S / M / L / XL     |
```

## Cross-ref

- Slash command: `/classify-4d <asset>` (se disponibile in `.claude/commands/`)
- Template archive: `flint/archive-template/MANIFEST-template.md`
- Workflow origin: kill-60 Flint sessione 2026-04-18 (voto 4/10, 40+ fonti)
- Feedback consolidated §10 preservation paranoid (E+K pattern) — quando 4D suggerisce "preserve" senza commit
