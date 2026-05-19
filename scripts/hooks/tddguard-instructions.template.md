# TDD Guard custom rules -- codemasterdd (mixed repo)

This repo mixes behavior-code (Python modules under `scripts/` with
co-located tests), one-off ops scripts, and docs/governance (ADR, OD,
specs, plans, CLAUDE.md). Apply test-first ONLY to behavior-code.

## ALWAYS PASS (not TDD-relevant -- return valid, do NOT block)

Any edit/write whose target path matches:
- `**/*.md` (docs, ADR, OD, specs, plans, governance)
- `docs/**`, `Archivio_*/**`, `.claude/**`
- `**/*.tmp*`, `*.json` governance/config files
- One-off ops scripts under `scripts/` that have NO co-located
  `test_*.py` / `tests/` (transformers, wrappers, maintenance utilities)

## ENFORCE test-first ONLY on

- Python behavior modules that have an existing co-located `tests/`
  directory or `test_*.py`. Adding logic without a failing test first
  -> block.

## Tie-breaker

When uncertain whether a file is behavior-code vs ops/doc: **PASS**.
This repo's value is cross-repo coordination and governance, not test
coverage of glue scripts. Favor non-blocking.
