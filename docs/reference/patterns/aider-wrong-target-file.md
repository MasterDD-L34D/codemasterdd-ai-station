# Pattern: Aider wrong-target-file (Qwen 7B + whole + subdirectory)

**Status**: documented 2026-05-07 (follow-up smoke test ADR-0015 closure)
**Occurrences**: n=1 (smoke test 2026-05-07, file `apps/dogfood-ui/dafne_client.py`)
**Severity**: medium -- file originale intatto (zero corruption), ma genera file inatteso alla root del repo
**Trigger ADR addendum**: n>=2 occorrenze documentate

## Pattern

`aider-cosmetic` (Qwen 2.5 Coder 7B + whole format) chiamato su file in subdirectory **con docstring header che si auto-referenzia** -- es. file `apps/dogfood-ui/dafne_client.py` con docstring riga 1 `"""Dafne swarm client -- proxy verso..."""` -- genera nuovo file alla **root del repo** (`./Dafne_client.py` con D maiuscola, su Windows case-insensitive vista come `dafne_client.py`) invece di modificare il file target nella subdirectory.

**Riproducibilita'**: confermata 2 volte (cwd worktree principale + cwd in subdirectory `apps/dogfood-ui/`). Workaround `cd subdir && aider-cosmetic file_senza_path` non risolve.

**Sintomo Git**: `git status` mostra `?? Dafne_client.py` (nuovo untracked file alla root). File originale invariato.

## Ipotesi sulla causa

Qwen 7B vede docstring "Dafne swarm client" e interpreta il filename come `Dafne_client.py`, generando il path output basato su quella stringa invece del path originale fornito. Aider whole format scrive l'intero file ricostruito senza validare path consistency.

## Mitigation

### Immediate

**Per task cosmetic su file in subdirectory profonde con docstring self-ref**: usare `aider-refactor` (Qwen 14B Q2 + diff format) anche se il task e' cosmetic. Il diff format **non** riproduce il pattern (test smoke-2 PASS su `apps/dogfood-ui/db.py`).

```bash
# Sconsigliato per file subdir + docstring self-ref:
aider-cosmetic apps/foo/bar.py --message "..."

# Consigliato:
aider-refactor apps/foo/bar.py --message "..."
```

### Verify post-edit (sempre)

```bash
git status --short
# Se appare ?? <Filename>.py alla root con name simile -> rollback:
rm -f <Filename>.py
git status --short  # confermare working tree pulito
```

Se file originale gia' modificato erroneamente:
```bash
git checkout HEAD -- apps/foo/bar.py  # ripristina target
rm -f Filename_root.py                 # cancella file off-target
```

### Prevention futura

- **Per file con docstring self-referenziato**: pre-flight check del path output (non implementato ad oggi)
- **Pre-commit hook check**: estendere pre-commit globale per warn quando appare nuovo `.py` alla root non-tracked (deferred fino a n>=2)
- **Wrapper update**: aggiungere `--map-tokens=0` o `--show-repo-map` a `aider-cosmetic.cmd` per testare se la repo map cambia il behavior (deferred, richiede test empirico)

## Out of scope (per questo pattern)

- File senza docstring self-ref: pattern NON riprodotto
- Diff format (aider-refactor + aider-groq + aider-cerebras + ecc.): pattern NON riprodotto
- File alla root del repo: pattern non applicabile

## Trigger escalation

Aggiornare questo doc + considerare ADR-0008 addendum o nuovo ADR-0022 quando emerge:

- n>=2 occorrenze documentate (es. file diverso, stesso pattern)
- Pattern che corrompe il file originale (oggi: zero corruption sull'originale)
- Pattern che persiste anche con diff format

## References

- Smoke test 2026-05-07 dogfood entry #13 in `logs/aider-delegation-2026-05.md`
- ADR-0008 silent-corruption Aider whole format (vector originario diverso)
- ADR-0015 follow-up post-closure action item #1 (validation tecnica scenario A)

## Workflow update CLAUDE.md

Sezione "Priorita' modelli AI" pointer aggiunto: per cosmetic task su file in subdir profonde, usare `aider-refactor` come default safe alternative.
