# ADR-0020 — Silent-fail Python guardrail (extension pre-commit globale)

> *TL;DR: il `/insights` audit (2026-04-25, Evo-Tactics repo, 51 sessioni / 161 commit) ha identificato che la guard rail chain ADR-0008/0011 protegge da silent-corruption (filename-as-content) e commit-message format, ma non da **silent-fail patterns** Python introdotti da Aider/LLM delegate (bare `except:`, silent `except+pass`, exception swallow). Esteso `~/.local/share/git-hooks/pre-commit` con Layer 2: scan added Python lines, block bare except + except+pass one-liner. Bypass marker `# silent-ok`. Smoke test 4 cases PASS.*

- **Status**: Accepted
- **Data**: 2026-04-25
- **Decisore**: Eduardo Scarpelli
- **Tipo decisione**: tecnica (estensione ADR-0011 guard rail chain)

## Context and Problem Statement

Il `/insights` audit ufficiale di Anthropic eseguito sul repo Evo-Tactics (51 sessioni Claude Code, 161 commit, 31 sessioni analizzate, finestra 2026-04-19 → 2026-04-25) ha prodotto in sezione `friction_analysis` + `usage_patterns.suggestions` la raccomandazione:

> **"Aider delegation needs guard rails"** — ADR-0008 already documents this. Operationalize it: after any Aider run, automatically diff the change, check for forbidden patterns (silent except, removed error handling, missing tests), and reject the commit if violations are found. You already have the commit-guard hook pattern working — extend it.

La guard rail chain corrente (ADR-0011 line 182-187) ha 4 layer:

1. `commit-msg` globale — Conventional Commits cross-agent
2. `pre-commit` globale — silent-corruption (filename-as-content)
3. Husky repo-local (Evo-Tactics)
4. Claude Code PreToolUse `commit-guard.js`

Nessuno scansiona il **contenuto del diff** per pattern code-quality. Il rischio è concreto: Qwen 14B Q2 + diff format è documentato (ADR-0008 Test 5 / dogfood n=5) per produrre talvolta codice "safe-fail" che bypassa logica downstream — bare `except:`, `except: pass`, removed `assert`, swallowed exceptions. Il commit passa i 4 gate esistenti ma introduce silent regression.

## Decision Drivers

- **Difensive against LLM blind spots**: Qwen 7B/14B addestrati su corpus dove `try/except` è comune; tendono a "rendere robusto" codice aggiungendo except blocks generici quando non richiesti.
- **Compatibility with reflection retry**: Aider retry può iterare su edit malformati; il guardrail non deve creare loop fail (bypass marker disponibile).
- **YAGNI minimalism (ADR-0005)**: estendere file esistente è preferibile a creare nuovo hook. Layer 2 nello stesso `pre-commit` mantiene single source of truth.
- **Cross-agent enforcement (ADR-0011 lesson)**: il guardrail deve girare per **qualsiasi** agent (Aider, Claude Code via Bash, manual git, futuri MCP), quindi git-level globale non Claude Code-specific.

## Considered Options

### Opzione A — Estendere `pre-commit` globale con Layer 2 (scelta)

Aggiungere blocco bash dopo il check Layer 1 silent-corruption. Scan `git diff --cached -U0` per pattern Python silent-fail su righe **aggiunte** (non pre-esistenti). Bypass marker `# silent-ok` o `# noqa: silent-fail` sulla riga `except`.

**Pro**: minimo impatto config (1 file modificato), coverage cross-agent automatica, bypass intentional-use granular.
**Contro**: bash regex su diff non è AST-aware → falsi negativi possibili (es. except con docstring poi pass). Trade-off accettabile per Layer 1 detection.

### Opzione B — Nuovo hook `pre-commit-quality` separato

File dedicato `~/.local/share/git-hooks/pre-commit-quality` chained nel main hook.

**Pro**: separation of concerns, easier to evolve.
**Contro**: 2 file da mantenere, duplicate setup (staged file iter), drift risk (ADR-0011 stesso anti-pattern).

### Opzione C — Strumento esterno (ruff/flake8 in pre-commit)

`ruff check --select E722,B902 file` come pre-commit hook.

**Pro**: AST-aware, copre più pattern.
**Contro**: dipendenza Python+ruff installato globalmente, friction setup, slower per piccoli diff. Per 2 pattern target (bare except, except+pass) il costo è eccessivo.

## Decision Outcome

**Scelto Opzione A**: estensione inline `pre-commit` globale.

### Pattern detected (Layer 2)

1. **Bare `except:`** — `^\+\s*except\s*:` su riga aggiunta. Match catches-all senza class.
2. **One-liner silent swallow** — `^\+\s*except[^:]*:\s*pass\s*$`. Match pattern `except X: pass` o `except: pass` su singola riga.

### Pattern non detected (deferred)

- **Multi-line `except: pass`** (except poi `pass` su riga successiva): richiede stato multi-riga, fattibile ma complica regex bash. **Effective workaround**: maggior parte di questi casi viene riformattata da black/ruff a one-liner se solo `pass` → ricadono in pattern 2. Defer fino a evidenza empirica di gap.
- **Removed `assert`**: richiede semantic diff (assert c'era, ora non c'è). Tool dedicato (semgrep) più appropriato. Defer.
- **Generic except clause con solo logging muto** (`except: logger.debug("oops")` senza re-raise): troppo permissivo da bloccare unconditional. Defer.

### Bypass mechanism

Comment `# silent-ok` o `# noqa: silent-fail` sulla riga `except`:
```python
try:
    cleanup()
except:  # silent-ok — defensive cleanup, exceptions explicitly ignored
    pass
```

Forza il committer a documentare l'intent. Aider (via reflection) può imparare il pattern dopo prima rejection — bypass è scrittura esplicita, non flag CLI.

### Smoke test (2026-04-25)

4 file `.py` in `/tmp/silent-fail-test`:

| File | Pattern | Expected | Actual |
|------|---------|----------|--------|
| `bad1.py` | bare `except:` + `pass` (multi-line) | block | ✅ block — rule A |
| `bad2.py` | `except Exception: pass` (one-liner) | block | ✅ block — rule B |
| `good.py` | `except ValueError:` + log + raise | pass | ✅ pass |
| `bypass.py` | bare `except:  # silent-ok` + pass | pass | ✅ pass |

Exit code 1 con violations 2/4 (atteso). Hook output stderr ben formato con file + line + remediation.

## Consequences

### Guard rail chain aggiornata
```
1. commit-msg globale         — Conventional Commits (ADR-0011)
2. pre-commit globale Layer 1 — silent-corruption filename-as-content (ADR-0008)
2. pre-commit globale Layer 2 — silent-fail Python patterns (ADR-0020) ← NEW
3. Husky repo-local            — Evo-Tactics specific
4. Claude Code PreToolUse      — fail-fast Bash gate (ADR-0011)
```

### Coverage gap residuo

| Pattern | Detection | Plan |
|---------|-----------|------|
| bare `except:` (added) | ✅ Layer 2 | done |
| `except X: pass` one-liner (added) | ✅ Layer 2 | done |
| `except X:\n    pass` multi-line (added) | ❌ deferred | gather data; if frequent, add multi-line state machine |
| Removed `assert` | ❌ deferred | semgrep / pylint future |
| Empty function body / `pass` only | ❌ out-of-scope | linter responsibility |
| Removed exception logging | ❌ out-of-scope | code review responsibility |

### Token cost

Zero per LLM. Hook bash overhead ~10ms su diff ≤200 LOC. Negligible.

### Reflection retry interaction

Se Aider commit blocca per silent-fail:
- Hook exit 1 → Aider reflection retry parte (default 3)
- Qwen vede stderr message → può rigenerare con `except SpecificError:` o aggiungere `# silent-ok`
- Pattern n=0 al momento (commit appena deployed); aspettarsi metriche da prossimo dogfood Python

## Follow-up

- [x] Estendere `~/.local/share/git-hooks/pre-commit` con Layer 2
- [x] Smoke test 4 casi (bad×2 + good + bypass) — PASS
- [x] Update CLAUDE.md guard rail chain reference (ADR-0011 line 226-230)
- [x] ADR-0020 scritto
- [ ] Tracking metriche prossimo dogfood Aider Python: numero false positive (legit defensive cleanup bloccato senza marker), numero true positive (silent-fail intercettati)
- [ ] Se false positive >20%: reconsider pattern A (bare except) → solo warn invece di block
- [ ] Se multi-line `except + pass` emerge come gap empirico (≥2 incident): implementare state machine 2-line
- [ ] Considerare estensione JS/TS per pattern equivalente: `catch {}` empty / `catch (e) { /* */ }` muto
- [ ] Future ADR su semgrep/ruff integration se pattern set cresce >5 regole

## Riferimenti

- ADR-0008 — silent-corruption Aider whole format: `0008-aider-whole-format-silent-corruption.md`
- ADR-0011 — cross-agent commit governance (guard rail chain baseline): `0011-cross-agent-commit-governance.md`
- Hook attuale: `~/.local/share/git-hooks/pre-commit` (Layer 1 + Layer 2, ~110 LOC totali)
- Insights audit Anthropic: file://C:\Users\edusc\.claude\usage-data\report.html (sessione 2026-04-25)
- Pattern reference Python: PEP 8 — bare except discouraged, [Sec. 4.2](https://peps.python.org/pep-0008/#programming-recommendations)
