# Scoped task -- docstring / comment consistency pass: scripts/fleet/morning-brief.ps1

Scope: SINGLE FILE only -- scripts/fleet/morning-brief.ps1. NO logic change, NO behaviour
change. Only comments and the comment-based help block may be edited.

## Goal

Review the comment-based help and inline comments in scripts/fleet/morning-brief.ps1 for
accuracy against the current code: the R0 report sections it emits, the output path, and
the "never writes outside logs/" contract. Fix stale, missing, or misleading wording.
Leave every executable statement exactly as it is.

## Hard constraints (ADR-0035 scoped-strict)

- Single file: scripts/fleet/morning-brief.ps1. Do not create, rename, or edit any other file.
- No logic change / no behaviour change: touch only comment lines and the help block.
- ASCII-only output (ADR-0021): keep the file ASCII; use `--` not an em-dash, ASCII quotes.
- Preserve every existing parameter, function, and code path unchanged.

## Acceptance

- `git diff` shows ONLY comment / help-block lines changed -- zero executable-code tokens.
- The script still parses (no syntax error introduced).
- Verify the repo ASCII guard stays green and the existing tests pass where applicable.
