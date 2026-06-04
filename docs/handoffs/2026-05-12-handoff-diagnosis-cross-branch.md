# Diagnosi cross-branch — handoff file missing sul PC fisico

> Trigger origin: nuova sessione Claude Code sul PC fisico Lenovo Eduardo (2026-05-12 dopo sera, post sessione cloud commit `f6dfbd8`) ha applicato Step 0 Protocol 1 refresh-verify e ha **stop-on-missing-prereq** correttamente quando ha cercato `docs/handoffs/2026-05-12-handoff-12-repos.md` e non l'ha trovato.

## Root cause empirico

Il file referenziato dal handoff ESISTE su remote, ma sul **branch separato** `claude/read-image-generate-list-iJwhs` (PR #57 draft non mergeato), NON su `main`. La nuova sessione lavorava in `main` checkout.

Verifica empirica (sessione cloud post Protocol 1):

```bash
# Su origin/main: file NON presente
git log origin/main -- docs/handoffs/2026-05-12-handoff-12-repos.md
# -> 0 risultati

# Su origin/claude/read-image-generate-list-iJwhs: file presente
git log origin/claude/read-image-generate-list-iJwhs -- docs/handoffs/2026-05-12-handoff-12-repos.md
# -> commit f6dfbd8 docs(sessions): handoff 12-repos wave con gate metodologico
```

PR #57: https://github.com/MasterDD-L34D/codemasterdd-ai-station/pull/57

## Anomalia "12 repos" scope chiarita

Nuova sessione PC ha correttamente osservato discrepanza tra "12 repos" del handoff e i **7 ecosystem entities monitored** (codemasterdd, Synesthesia, Game, Game-Godot-v2, Dafne swarm, AA01, vault-shared).

**Chiarimento**: "12 repos" NON e' inflazione del monitored ecosystem. E' lo **scope del trigger origin**: screenshot OCR `TOP CLAUDE CODE REPOSITORIES` di Eduardo inviato sessione cloud 12/5 sera, contenente 12 repository **esterni third-party** (skills/subagents/tools/guides/awesome-lists). Triagati in `docs/reference/subagents-skills-candidates.md` sezione "Wave 2026-05-12 batch evaluation". Pattern adozione previsto: cherry-pick selettivo (NO bulk install), 4 task AA01 raggruppati per categoria (BACKLOG M11-M14).

Lista 12 repo esterni:
1. affaan-m/everything-claude-code (refresh, gia' Apr 22)
2. shanraisshan/claude-code-best-practice
3. obra/superpowers
4. thedotmack/claude-mem
5. forrestchang/andrej-karpathy-skills
6. hesreallyhim/awesome-claude-code (refresh)
7. yamadashy/repomix
8. gsd-build/get-shit-done
9. dair-ai/Prompt-Engineering-Guide
10. anthropics/skills
11. VoltAgent/awesome-claude-code-subagents (refresh)
12. VoltAgent/awesome-design-md

## Tre opzioni fix (Eduardo direct)

### Opzione A -- Checkout branch del PR (read-only inspection)

```powershell
cd C:\dev\codemasterdd-ai-station
git fetch origin
git checkout claude/read-image-generate-list-iJwhs
ls docs/handoffs/2026-05-12-handoff-12-repos.md   # verify exists
# Adesso puoi rieseguire Step 0 Protocol 1 con file effettivamente disponibile
```

**Pro**: nessuna alterazione main. Rapido.
**Contro**: handoff vive solo su branch fino merge. Future ricerca con `main` checkout ripete stessa anomalia.

### Opzione B -- Merge PR #57 prima del pickup

```powershell
gh pr ready 57
gh pr merge 57 --squash
git checkout main && git pull origin main
ls docs/handoffs/2026-05-12-handoff-12-repos.md   # verify exists su main
```

**Pro**: file di riferimento accessibili su main per future sessioni. Single source of truth.
**Contro**: handoff stesso (sezione anti-pattern #6) raccomanda lasciare draft fino SHIP almeno 1 task M11-M14 per validare scaffold workflow end-to-end. Merge ora = skip validation.

**Mitigazione contro**: la validation SHIP non e' bloccante per merge -- e' best-practice. Lesson positiva (questa diagnosi cross-branch) e' gia validation parziale del handoff metodologico.

### Opzione C -- Read file senza checkout (one-shot lookup)

```powershell
git fetch origin
git show origin/claude/read-image-generate-list-iJwhs:docs/handoffs/2026-05-12-handoff-12-repos.md | less
# Oppure salva temp:
git show origin/claude/read-image-generate-list-iJwhs:docs/handoffs/2026-05-12-handoff-12-repos.md > C:\Temp\handoff-12-repos-readonly.md
```

**Pro**: zero modifiche repo, zero checkout. Esplorazione veloce.
**Contro**: file non versionato su PC fisico, perdita context se chiudi terminal.

## Pattern positivo da capitalizzare (lesson candidate)

Il comportamento **stop-on-missing-prereq** della nuova sessione e' esattamente il pattern desiderato dal handoff metodologico:

- ❌ NON auto-creato file mancante "per salvare sessione" (anti-pattern AGENTS.md AA01)
- ✅ Refresh-verify Protocol 1 empirico applicato (cross-repo search 5 repo + AA01 + Dafne)
- ✅ Stop + clarification request invece di assumption
- ✅ Anomalia "12 repos" segnalata empiricamente (non assunta come typo)

**Lesson candidate** `L-2026-05-NNN-handoff-cross-branch-anti-pattern`:
- Quando un handoff referenzia file `docs/handoffs/<file>.md`, il consumer deve sapere su quale **branch** vive il file
- Best practice handoff: includere esplicitamente in pickup commands `git checkout <branch>` o citare PR per chiarezza
- Best practice produttore handoff: se intent e' "file accessibile da main", merge PR PRIMA di passare il handoff (oppure dichiarare esplicitamente "file su branch X, NOT main")
- Pattern recovery: stop-on-missing-prereq + diagnosi cross-branch + 3 opzioni fix con trade-off espliciti (NO auto-fix)

## Anti-pattern evitati in questa diagnosi

1. **Auto-merge PR** senza conferma Eduardo (visible-to-others action, CLAUDE.md gate)
2. **Auto-creazione del file mancante** sul PC fisico per "salvare la nuova sessione" (anti-pattern AGENTS.md AA01)
3. **Assumption "Eduardo typo"** ("12 repos" -> "7 entities") senza verify empirico
4. **Skip della diagnosi documentale** e' direttamente "ok merge subito" (perdita lesson opportunity)
