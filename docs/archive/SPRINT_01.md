> ARCHIVED 2026-06-03 (context-files reorg Fase 2). SUPERSEDED -- live direction = GOALS.md + ORCHESTRATION.md.
> Historical record.

# SPRINT_01 — "Fase 6 push + cp1252 monitoring"

> Sprint 1 della Fase 6 compressa. Finestra: **2026-04-23 → 2026-05-06** (2 settimane, fino alla review settimana 2 ADR-0014).
>
> **Status 2026-04-24**: **CLOSED early-hit** (3° giorno su 14). Tutti gli obiettivi hard raggiunti o superati.
>
> **Sprint objective**: portare dataset Fase 6 da 6 → ≥12 dogfood (di cui ≥3 behavior-critical) + validare empiricamente il fix cp1252 + mantenere cost tracking attivo. Zero silent-corruption deve rimanere invariato.
>
> **Esito finale**: **12/12 dogfood ✅**, **5/3 behavior-critical ✅** oltrepassato, **0 silent-corruption ✅** mantenuto, **H4 cost snapshot anticipato ✅**, **H5 review settimana 2 anticipata ✅** (on-track). Soft-goal cp1252 fix: 9 dogfood consecutivi senza retry loop naturale → validation **inconclusive** (trigger mai attivato), soglia pazienza n=15. **ADR-0015 Proposed 2026-04-24** (deroga criterio #3 privacy per Synesthesia dormant fino agosto).

---

## Task

### T1. Dogfood behavior-critical cloud #2-3 [H1]
- **Cosa**: identificare 2 task behavior-critical reali che emergono durante uso normale e delegarli via `aider-groq` o `aider-cerebras` con `--edit-format diff --no-auto-commits`.
- **Esempi candidati (opportunistici)**: retry logic su `quality-bench/run-bench.ps1`, error handling su `aider-log.sh`, refactor di `bench-ollama.ps1` per parsing JSON robusto.
- **File/sistemi toccati**: script PowerShell/Bash nel repo. **NON** toccare `controllers/`/`routes/` di Synesthesia (privacy mixed).
- **Check**: post-edit `git diff HEAD~1` verify no silent-corruption; `logs/aider-delegation-2026-04.md` entry completa (classe, stack, retry, tokens, cost, esito).
- **Success**: ≥2 entry nuove con classe=behavior in log, ≥1 success 1st-try.
- **Safety note**: se emerge corruption o behavior drift inatteso → **stop sprint**, ADR-reactive.

### T2. Dogfood cosmetic mix n=5 [H2]
- **Cosa**: portare cosmetic a ≥10 entries cumulative via batch operazioni opportunistiche.
- **Esempi candidati**: JSDoc su `scripts/hooks/commit-guard.js` altre funzioni non ancora documentate, comment-based help su script PS1 residui (`disconnect-onedrive.ps1`, `bitlocker-hard-disable.ps1` — già quasi fatti), typo fixes discovered.
- **File toccati**: `scripts/`, `docs/patterns/`.
- **Check**: stesso di T1.
- **Success**: log cumulativo mostra ≥10 cosmetic entries, ≥50% via wrapper (non direct Claude Code).

### T3. Monitoring empirico fix cp1252 [H3/D2]
- **Cosa**: quando si verifica prima retry loop naturale (prevedibile in T1/T2), osservare se Aider completa safe-fail senza crash `UnicodeEncodeError '→'`.
- **File toccati**: `C:\Users\edusc\.local\bin\aider-*.cmd` (solo lettura diagnostica, nessun edit in questo sprint salvo fallimento).
- **Check**: log Aider stderr completo salvato in `logs/` se crash avviene.
- **Success**: 1+ retry loop osservato → decisione "fix tiene" / "fix fallisce → M3 attivato prossimo sprint".
- **Safety note**: crash non distrugge niente (working tree resta pulito), ok osservare.

### T4. Cost tracking cumulativo mid-sprint [H4]
- **Cosa**: fine settimana 1 (~2026-04-30) → snapshot `ccusage daily` ultimi 7gg + sum cost cloud da log dogfood. Entry sintetica in `logs/aider-delegation-2026-04.md` o JOURNAL.
- **Check**: proiezione mensile <$15 a settimana 1 → OK; tra $15-$20 → yellow flag, monitorare; >$20 → revisione routing urgente.
- **Success**: snapshot documentato, trend chiaro.

### T5. Review settimana 2 formale [H5]
- **Cosa**: sessione ~30min a ~2026-05-06: count dogfood totale + breakdown classe + cost proiezione + ETA chiusura Fase 6.
- **Output**: entry JOURNAL "Review settimana 2" + eventuale aggiornamento `COMPACT_CONTEXT.md` stato.
- **Success**: 3 decisioni chiare — on-track / mid-course correction / extension early-warning.

### T6. JOURNAL entry normalizzazione project files [M1]
- **Cosa**: entry 2026-04-23 documentando creazione dei 7 file di governance + rationale (perché ora, perché separati da CLAUDE.md).
- **File**: `JOURNAL.md` append.
- **Success**: entry breve (~15 righe), link ai file.

### T7. Memory refresh `project_session_resumption.md` [M2]
- **Cosa**: update memoria con HEAD attuale + pointer a `COMPACT_CONTEXT.md` come source snapshot (evita duplicazione).
- **File**: `~/.claude/projects/.../memory/project_session_resumption.md`.
- **Success**: memoria allineata, zero contraddizioni con git reality.

---

## File/sistemi toccati (aggregato)

| File/dir | Letto | Edited | Written |
|----------|:-----:|:------:|:-------:|
| `logs/aider-delegation-2026-04.md` | ✓ | ✓ | |
| `scripts/**` | ✓ | ✓ (via Aider) | |
| `JOURNAL.md` | ✓ | ✓ | |
| `COMPACT_CONTEXT.md` | ✓ | ✓ | |
| Memory files | ✓ | ✓ | |
| `~/.local/bin/aider-*.cmd` | read-only | — | (solo se T3 fallisce) |

---

## Criteri di successo sprint

- **Hard (must)**:
  - ✅ ≥12 dogfood totali (6 attuali + ≥6 nuovi), di cui ≥3 behavior-critical
  - ✅ 0 silent-corruption cumulative mantenuto
  - ✅ Cost mid-sprint snapshot documentato
  - ✅ Review settimana 2 completata
- **Soft (nice-to-have)**:
  - Fix cp1252 validated o contro-diagnosticato
  - Memory refresh + JOURNAL allineati

---

## Safety note trasversali

- **Working tree check post-Aider**: sempre `git status` dopo dogfood; se `M <file>` non committed → commit manuale Claude Code con messaggio conforme (fallback documentato ADR-0011 + dogfood #3).
- **Privacy guard**: qualsiasi dogfood su Synesthesia → check `git diff --stat` per verificare che non tocchi `controllers/`/`routes/`/`middlewares/`. Se tocca → abort e sovereign-only.
- **Cost alarm**: se singolo wrapper call supera $0.01 (10× base) → alarm, investigare (potrebbe essere paid model selezionato per errore).
- **No `--force` su main, no `--no-verify`**: convenzione fissa (CLAUDE.md + ADR-0011). Zero eccezioni.

---

## Rischi noti

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|:-----------:|:-------:|-------------|
| Dogfood opportunity scarse (lavoro non-coding nelle 2 settimane) | Medio | Alto (H1/H2 non raggiunti) | Proattivamente proporre delega su cleanup/JSDoc batch anche sub-threshold |
| cp1252 crash ricorrente | Medio | Medio (T3 decide) | Fix preventivo deployato; fallback M3 in prossimo sprint |
| Silent corruption compare (mai accaduto prima) | Basso | Altissimo (ADR-reactive, blocca tutto) | `git diff` rigoroso, ADR-0008 già scritto |
| Cost esplosivo (paid model per errore) | Basso | Medio | Alarm $0.01 + wrapper espliciti per provider |
| Rate limit Groq 6k tok/min su task iterativo | Basso | Basso | Fallback Cerebras (quota separata) |

---

## Out of scope (esplicito)

- Re-bench hard custom problems [L1]
- Deepseek-r1 framework fix [L2]
- Cerebras paid evaluation [L3]
- Gemma 4 multimodal use case [L4]
- ~~ADR-0015 draft (richiede closure Fase 6)~~ **Spostato in scope 2026-04-24 Proposed** post input Synesthesia dormant: draft preparatorio pre-closure, ratification a review sett.4 (~2026-05-17).
- Migrazione Evo-Tactics sovereign workflow (post-Max)

---

## Closure log

**2026-04-24 auto-mode session** — Sprint 01 chiuso early-hit:
- T1 (H1 behavior-critical cloud #2-3): ✅ superato con #6 success + #9/#10/#12 local + #7 reject. Dataset behavior 5, target ≥3.
- T2 (H2 cosmetic mix): 🟡 partial 7/10 (#3 via 7B local + #4/#5 via Groq + #8 partial + #11 polish). Gap 3 opportunistic, non-blocking.
- T3 (H3 cp1252 monitoring): 🟡 inconclusive — 9 dogfood consecutivi clean, trigger mai attivato. Soglia pazienza n=15.
- T4 (H4 cost snapshot): ✅ anticipato 2026-04-24 vs target 2026-04-30. $0.0148 cumulative / 0.074% budget.
- T5 (H5 review settimana 2): ✅ anticipata 2026-04-24. Esito on-track, no mid-course correction.
- T6 (M1 JOURNAL entry normalizzazione): ✅ entry + 2 addendum 2026-04-24 sessioni.
- T7 (M2 memory refresh): ✅ `project_session_resumption.md` + nuovo `project_synesthesia_dormant.md` 2026-04-24.
- Bonus: ADR-0016 Proposed (constraint-count) + ADR-0015 Proposed (closure path).

**Sprint obiettivi hard**: 4/4 ✅. **Soft**: cp1252 inconclusive (tracked), altri done. **Next sprint (SPRINT_02)**: focus reliability n=20 + pre-closure check settimana 4 + ADR-0015 ratification.
