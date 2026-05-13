# Cross-repo PR body template

Copy questo template come body quando apri PR cross-repo via Component 2 workflow.

---

## Summary

[1-2 frasi: cosa cambia + perché]

## Type

- Type: <policy-alignment | ADR-cross-ref | drift-fix | docs | governance-suggestion>
- codemasterdd ADR ref: <ADR-NNNN o N/A>
- L-XXX lesson ref: <L-2026-MM-NNN o N/A>

## Source codemasterdd

- Repo: `MasterDD-L34D/codemasterdd-ai-station`
- Branch/commit: <branch + commit hash>
- File ref originale: <docs/adr/0024-... o memory/...>

## Proposed change

- Files touched in this PR:
  - `path/to/file1.md`
  - `path/to/file2.py`
- Scope: minimal (NO functional behavior change unless drift-fix type)

## Privacy class

- Repo target privacy: <sovereign-only | mixed | cloud-OK>
- Whitelist check: PASSED (verified via `scripts/cross-repo/dry-run-pr.ps1`)
- Code shared con cloud LLM: <none | yes specify>

## Reversibility

- Reverting cost stimato: <minutes/hours/days>
- Cross-reference creates in this repo: <yes/no -- if yes, list refs>

## Governance interna repo target

- Decision: governance interna autosufficiente, accept/reject/amend a vostra discrezione
- codemasterdd-side: NO write-direct, NO push --force, NO bypass review
- Eduardo coordinator: medierà eventuali round trip se serve

## Test plan (se applicabile)

- [ ] Lint/parse markdown se doc-only
- [ ] [Type-specific: ADR-cross-ref → verify cross-link bidirezionale; drift-fix → verify ground truth matches]

🤖 Generated with [Claude Code](https://claude.com/claude-code) via cross-repo Component 2 workflow
