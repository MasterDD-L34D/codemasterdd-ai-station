# AA01 handoff — scaffold paste-ready

AA01 workspace vive su `C:/Users/edusc/aa01/` (NON-git, disciplina personale Eduardo, non versionato in questo repo per design — vedi CLAUDE.md "Protocol 4 AA01 workspace audit trail").

Questa directory contiene **scaffold paste-ready** generati da Claude Code in sessioni codemasterdd quando emergono task evaluation che richiedono workflow AA01 (`inbox/ -> classify -> promote -> SHIP -> lesson`).

## Workflow di handoff

1. Claude Code genera file `YYYY-MM-DD-<slug>.md` qui (scaffold con preset + scope + criteri SHIP)
2. Eduardo paste copy in `C:/Users/edusc/aa01/inbox/<slug>.md`
3. Eduardo esegue `bash scripts/classify.sh inbox/<slug>.md`
4. Eduardo esegue `bash scripts/promote.sh inbox/<slug>.md <preset>` (preset suggerito nello scaffold)
5. Lavoro DRAFT -> PROPOSED -> SHIP secondo preset
6. Post-SHIP: lesson `learnings/L-YYYY-MM-NNN-<slug>.md` (Eduardo direct)
7. Archive `--status=SHIP` (Eduardo direct)

## File presenti

- `2026-05-12-A-skills-resources.md` — Task A: skills collection (#1 refresh, #3, #5, #10)
- `2026-05-12-B-subagent-memory-resources.md` — Task B: subagent + memory (#4, #11 refresh)
- `2026-05-12-C-dev-tools-resources.md` — Task C: dev-tools (#7, #8)
- `2026-05-12-D-guides-awesome-design-resources.md` — Task D: guides + awesome + design (#2, #6 refresh, #9, #12)

Trigger: screenshot OCR `TOP CLAUDE CODE REPOSITORIES` di Eduardo, sessione 2026-05-12 codemasterdd (this repo).

Index master: `docs/reference/subagents-skills-candidates.md` sezione "Wave 2026-05-12".

BACKLOG tracking: M11 (Task A), M12 (Task B), M13 (Task C), M14 (Task D).

## Anti-pattern

- **NO** scrivere su `C:/Users/edusc/aa01/` da Claude Code session (boundary: AA01 e' personal discipline, NO write-path automatizzato da agent)
- **NO** clonare lifecycle AA01 in `docs/` (questo repo NON e' AA01 mirror, solo handoff staging)
- **NO** committare in questa dir scaffold gia processati da Eduardo (post-paste). Una volta processato, archive in `docs/aa01-handoff/archive/` o delete se non-utile come reference futura.
