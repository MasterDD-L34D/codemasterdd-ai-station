# AA01 handoff — scaffold paste-ready

> **🟢 4 task RESOLVED 2026-05-12 (anti-rot pointer)** — I 4 scaffold (A/B/C/D) sono SUPERSEDED dalla decisione finale 12-repo. Verdetti per-task nei banner in testa a ciascun file. Fonte-verità unica: `docs/reference/subagents-skills-candidates.md` §"Riepilogo decisioni preliminari" + canonical `Vault-ops-remote/claude-global/canonical-config.json` `shipped_triage_reference_ANTI_ROT`. Residuo NON-autonomo: repomix `npm i -g` (per-macchina) + everything-claude-code time-gated (~19/5). NON re-triagare i 12.

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

- `2026-05-12-vault-frontmatter-drift-handoff.md` — attivo
- **`archive/`** — 4 scaffold Wave-12 (A/B/C/D) **spenti/superseded** → vedi `archive/README.md`

> **🟢 Wave-12 RESOLVED + ARCHIVED 2026-05-17** — I 4 scaffold A/B/C/D **non eseguiti via rituale-paste** (final-table 12-repo li ha superseded prima). Spostati in `archive/`. **Meccanismo corretto per adoption-work**: loop `studio → conferma Eduardo → tuning → reiterazione → apply` (NON rituale-paste AA01, che resta valido solo per *nuovi* trigger spontanei). Esiti: #1 Instincts cherry-pick (vault canonical) · #11 → custom `godot-engine-specialist` agent (questo repo) · #6 parry/Rulesync parked-with-trigger · resto chiuso/Eduardo-direct. Fonte-verità: `docs/reference/subagents-skills-candidates.md`.

Trigger origin: screenshot OCR `TOP CLAUDE CODE REPOSITORIES` di Eduardo, sessione 2026-05-12 codemasterdd (this repo).

Index master: `docs/reference/subagents-skills-candidates.md` sezione "Wave 2026-05-12".

BACKLOG tracking: M11-M14 **CHIUSI** (Wave-12 resolved via final-table, scaffold archiviati 2026-05-17).

## Anti-pattern

- **NO** scrivere su `C:/Users/edusc/aa01/` da Claude Code session (boundary: AA01 e' personal discipline, NO write-path automatizzato da agent)
- **NO** clonare lifecycle AA01 in `docs/` (questo repo NON e' AA01 mirror, solo handoff staging)
- **NO** committare in questa dir scaffold gia processati da Eduardo (post-paste). Una volta processato, archive in `docs/archive/aa01-handoff/archive/` o delete se non-utile come reference futura.
