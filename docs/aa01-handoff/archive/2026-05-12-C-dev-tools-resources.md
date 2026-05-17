# AA01 Task C — Dev-tools evaluation (2 repo)

> **🟢 RESOLVED 2026-05-12 (anti-rot pointer, no re-triage)** — Scaffold AA01 SUPERSEDED dalla decisione finale. Verdetti shippati: **#7** repomix = INSTALL `npm install -g repomix` (**azione utente per-macchina**, NON eseguito Ryzen 2026-05-17) · **#8** get-shit-done = BOOKMARK (no install, audit vs AA01). Fonte-verità: `docs/reference/subagents-skills-candidates.md` §"Riepilogo decisioni preliminari" + canonical `shipped_triage_reference_ANTI_ROT`. Unico residuo = repomix install per-macchina (utente). NON re-triagare.

> **Preset**: `research-long`
> **Slug**: `2026-05-12-C-dev-tools-resources`
> **Effort stima**: 2 ore (repomix install + use case validation + gsd audit comparativo)
> **Trigger origin**: screenshot OCR Eduardo 2026-05-12, sessione codemasterdd
> **Reference master**: `docs/reference/subagents-skills-candidates.md` sezione "Wave 2026-05-12 categoria C"
> **BACKLOG entry**: M13

## Scope

| # | Repo | Stars reali | Decisione preliminare |
|---|------|-------------|----------------------|
| 7 | `yamadashy/repomix` | ~24.6k | INSTALL via `npm install -g repomix` |
| 8 | `gsd-build/get-shit-done` | ~57.5k | BOOKMARK + audit comparativo vs AA01 workflow |

## Criteri DRAFT -> PROPOSED

**Repo #7 repomix**:
1. Verify license MIT + manutenzione recente
2. Install method: `npm install -g repomix` (NPM global) o `npx repomix` (one-shot)
3. Test smoke: `repomix --output ~/tmp/codemasterdd-pack.txt /home/user/codemasterdd-ai-station/` (o equiv windows) -> verify output: singolo file con tutto il repo
4. Use case validati:
   - Context handoff cross-session (es. nuova sessione Claude Code parte con `repomix` di vault-shared per context)
   - Compact representation per analisi multi-repo (es. AA01 batch task)
   - Backup snapshot leggibile (alternativa a git clone bulk)
5. Wrapper opzionale: `~/.local/bin/repomix-pack <repo>` con default config (output path standard)

**Repo #8 gsd**:
1. Clone read-only + scan README + struttura
2. Audit comparativo vs AA01 workflow Eduardo (preset DRAFT -> PROPOSED -> SHIP):
   - Quale pattern shared (spec-driven, context engineering)?
   - Quale pattern gsd ha che AA01 NON ha?
   - Vale cherry-pick singoli pattern o adoption integrale?
3. Decisione: BOOKMARK (default) o RIVALUTARE (se emerge gap concreto AA01)

PROPOSED: repomix INSTALL path definitivo + 1 doc lesson da gsd pattern adoption.

## Criteri SHIP

- [ ] **repomix**:
  - Installato globalmente, comando `repomix --version` funzionante
  - 1 use case reale eseguito (es. pack codemasterdd repo per test handoff)
  - Eventuale wrapper `~/.local/bin/repomix-pack` o alias documentato
  - Update CLAUDE.md sezione "Stack installato" con repomix versione
- [ ] **gsd**:
  - Audit lesson `learnings/L-2026-05-NNN-gsd-vs-aa01-pattern-comparison.md`
  - 0-N pattern cherry-pick documentati (se applicabili a AA01 evolution)
  - Update `subagents-skills-candidates.md` stato BOOKMARK + lesson reference
- [ ] JOURNAL entry sessione

## Anti-pattern

- Install repomix senza use case reale (overhead 30MB npm dep per zero benefit)
- Sostituire AA01 con gsd workflow (Eduardo personal discipline, NO disruption)
- Skip lesson gsd se pattern positivi emergono (perdita capitalizzazione)
- Wrapper repomix con default opachi (es. embed API keys nel pack accidentalmente — privacy guard rail compliance richiesta)

## Note operative

- **repomix privacy concern**: pack include TUTTO il repo. **Verify** `.gitignore` rispettato by default + opzione `--exclude` per file sensitivi. **Privacy guard rail trigger**: NON usare repomix su repo non-whitelisted senza review output (Synesthesia, repo cliente).
- **gsd metodologia overlap**: TACHES = "Test, Architecture, Context, Hypothesis, Execution, Spec-driven". Confronta vs AA01 preset:
  - `research-long` ~= TACHES Hypothesis + Execution
  - `code-sprint` ~= TACHES Spec-driven + Execution
  - Lesson da cercare: se TACHES ha step esplicito che AA01 fa solo implicito

## Output atteso

- 1 tool installato globalmente (repomix)
- 1 lesson comparativa gsd-vs-AA01
- 0-1 wrapper documentato
- Update CLAUDE.md stack + reference file con status INSTALLED/BOOKMARK
