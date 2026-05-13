<!--
PR template codemasterdd-ai-station -- introdotto 2026-05-13 PR #84 (P1 #5 harsh-reviewer fix).
Sezione "Cognitive protocols applied" anti-aspirational measurement (ADR-0026 addendum 2026-05-13).
Threshold review 2026-08-13: se <30% adoption rate Protocol 5+6 su qualifying tasks -> amendment.

SKIP RULE micro PR (ratified 2026-05-13 post harsh-reviewer #2 P1 #4 finding):
- Doc-only PR <5 lines change OR cosmetic refresh (date / count / typo): COMPILA solo Summary + Files changed. SKIP "Cognitive protocols applied" + "Test plan" + "Trigger ADR".
- Single-commit cherry-pick OR revert: COMPILA solo Summary + Cross-references.
- Auto-merge automation PR (skiv-monitor / gh-bot equivalent): SKIP completamente template.
- Default: PR comportamento-critical OR ADR-class OR security/governance-critical => COMPILA template completo.
-->

## Summary

<!-- Cosa fa questo PR in 1-3 frasi. Cita ADR / lesson / harsh-reviewer finding rilevanti. -->

## Files changed

<!-- Bullet list file modificati + perche brevemente. -->

<!-- ============================================================ -->
<!-- BELOW SECTIONS: SKIP if doc-only <5 lines OR cosmetic refresh -->
<!-- ============================================================ -->

## Test plan

<!-- Checklist verify steps - inserire [x] post-test pre-merge. Skip se PR doc-only. -->

- [ ] ...

## Cognitive protocols applied (ADR-0026)

<!--
Anti-aspirational measurement field. Compilare onestamente. Threshold review 2026-08-13.
Trigger references: see CLAUDE.md "Cognitive workflow protocols" section.
-->

- **P1 Refresh-verify state interno**: Y / N (default Y se PR significativo, OBBLIGATORIO)
- **P2 Autoresearch multi-source**: Y / N (Y se external research / vendor-specific / framework bug investigation)
- **P3 Archon 7-step First Principles**: Y / N (Y se high-stakes irreversibile o pivot architecturale)
- **P4 AA01 workspace audit trail**: Y / N (Y se effort >=30min + cross-session value)
- **P5 harsh-reviewer subagent**: Y / N (Y se cluster >=3 PR same day OR file security/governance-critical)
- **P6 brainstorming skill**: Y / N (Y se ADR-class architectural decision generative)

<!-- Optional: brief note SU come applicato e con che outcome (es. "P5 invoked, 8 finding -> 5 fixed pre-merge"). -->

## Trigger ADR (se applicabile)

<!-- ADR-0015 silent-corruption / fail rate / privacy violation check. Skip se PR doc-only senza code change. -->

- silent-corruption working-tree: 0 / N>0 (default 0)
- fail rate cumulative: ...
- privacy violation: 0 / N>0 (default 0)

## Cross-references

<!-- Bullet list ADR / lesson / harsh-reviewer finding / sister PR / commit hash. -->

## Commits in this PR

<!-- Auto-fill da gh pr view o manual list. -->

1. `<sha>` <subject>
