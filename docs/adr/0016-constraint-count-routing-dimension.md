# ADR-0016 — Constraint-count as second routing dimension

> *TL;DR: La matrice routing modelli di ADR-0008 (hub pattern) classifica per **natura task** (cosmetic/behavior/strategic). Dogfood Fase 6 n=11 rivela pattern empirico non catturato dalla prima dimensione: la success-rate della delega degrada con il **numero di constraint espliciti** nel prompt, indipendentemente dalla classe. Questo ADR formalizza **constraint-count** come seconda dimensione di routing. Soglia pratica: 1 constraint → qualsiasi tier; 2-3 constraint additivi/preserve → 14B Q2 local o 70B cloud; 2 constraint fix+transform → downgrade a 14B Q2 (7B skippa transform); 5+ constraint strict → **manual Claude Code** (delegazione anti-pattern). Dataset validation: 6 data points cross-tier + 11 cumulative + 0 silent-corruption.*

- **Status**: **Proposed** (2026-04-24)
- STATUS-CHECK: 2026-06-09 | trigger: n>=3 data point constraint-count OR SPRINT_02 close | default-if-elapsed: Escalate
- **Data**: 2026-04-24 (dopo sessione notturna con dogfood #9/#10/#11)
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)
- **Supersedes / Extends**: ADR-0008 (estende, non sostituisce: hub pattern resta backbone)
- **Driver ORIGINE**: OD-006 in `OPEN_DECISIONS.md` (proposto 2026-04-23 sera post dogfood #7 REJECT)

## Context and Problem Statement

ADR-0008 "Aider whole format silent-corruption" (2026-04-21) stabilì l'**hub pattern** tier routing attuale, classificando task in 3 classi:

1. **Cosmetic** (JSDoc, docstring, rename, lint-fix) → Qwen 7B + `whole` (faithfulness non critica, format compatibile)
2. **Behavior-critical** (refactor, bug fix, logic change) → Qwen 14B Q2 + `diff` (safe-fail; ~20-40% retry manuale ma zero silent-corruption)
3. **Strategic** (multi-file, synthesis, debug architetturale, ADR writing) → Claude Code direct (non delegabile)

Questa **prima dimensione** (natura task) funziona come backbone per decisioni coarse-grained. Tuttavia, dogfood Fase 6 ha rivelato che **all'interno della stessa classe**, la success-rate varia drasticamente in base al numero di constraint espliciti nel prompt.

### Evidenza empirica cumulativa (dogfood Fase 6 n=11, end 2026-04-24 02:30)

| # | Task (1 riga) | Classe | Stack | Constraint count | Compliance |
|:-:|---------------|--------|-------|:----------------:|:----------:|
| 1-3, 5 | Add-only (JSDoc, help, examples, exit codes) | cosmetic | 7B local / 70B wrap | **1** | **~100%** (n=4) |
| 4 | help extension bench-ollama | cosmetic | 70B Groq | **1** | 100% (small smell lingua) |
| 8 | apostrofo + NOTES condense | cosmetic | 7B local | **2** (fix + transform) | **50%** (1/2; 7B skippa transform) |
| 6 | retry Invoke-Bench | behavior | 70B cloud | **3** (signature + return + resilience) | 100% (small smell `HttpWebResponseException`) |
| 7 | retry Invoke-Model | behavior | 70B cloud | **5** strict semantic | **20% REJECT** (5 violations, 1 BLOCKING) |
| 9 | HEREDOC commit-guard | behavior | 14B Q2 local | **2** (fix + preserve) | 100% (small smell `console.log` → fisso in #11) |
| 10 | command.includes false-positive | behavior | 14B Q2 local | **3** (fix + preserve HEREDOC + preserve validation) | 100% clean |
| 11 | console.log → stderr polish | cosmetic | 7B local | **1** | 100% (1 auto-commit retry) |

### Pattern osservato

La matrice originale classe-based **non distingue** dogfood #6 (success, 3 constraint additivi) da #7 (REJECT, 5 constraint strict semantic) — entrambi erano "behavior-critical cloud Groq 70B". Eppure l'esito differisce radicalmente.

Osservazione: il **numero di constraint** che il modello deve preservare **simultaneamente** nel output correla forte con la success-rate, con soglie empiriche:

- **1 constraint**: task facile, qualsiasi tier OK (~100% compliance)
- **2-3 constraint additivi/preserve-type**: 14B Q2 local o 70B cloud gestiscono (~100% in n=3: #9, #10, #6)
- **2 constraint con transform-type**: 7B skippa la parte trasformativa → degrada a 50% (#8). 14B Q2 gestisce preserve-type ma non testato per transform-type.
- **5+ constraint strict semantic**: 70B cloud degrada a ~20% — **delega è anti-pattern empirico** (#7)

### Ipotesi causale

LLM ≤70B hanno "capacity finita" per preservare constraint simultaneamente nel planning output. Il limite empirico sembra ~3-4 constraint prima che i constraint meno prominenti (tipicamente transformativi vs fix puntuali) vengano "dimenticati". Questo è consistent con:

- Research su attention allocation in transformer (constraint prominence bias)
- Pattern "signal-to-noise" in prompt complessi
- Observation: il constraint più concreto (es. "aggiungi linea X") sopravvive; quello più astratto ("non modificare Y") viene skippato

**Non è un bug del modello, è un limite architetturale che il routing deve rispettare.**

## Decision Drivers

- **Scientificità**: pattern empirico 6 data points cross-tier + corroborato da n=11 cumulative — massa critica per formalizzazione
- **Safety**: il mancato matching di constraint produce silent-semantic-corruption (#7 return-branch divergent); il routing deve ridurre questa classe di errori
- **ADR-0008 compatibility**: hub pattern backbone resta valido; questo ADR **estende** la decision matrix con seconda dimensione
- **Pragmatismo operativo**: devo poter classificare un task in <30s prima di delegare. Constraint-count è **contabile meccanicamente** (conto gli imperativi nel prompt)
- **OD-006 resolution**: decisione aperta da 2026-04-23; chiuderla evita drift future

## Considered Options

### Opzione A — Non formalizzare (status quo, solo classe-based)

**Pro**: matrice semplice, nessun overhead cognitive routing.

**Contro**:
- Pattern empirico ignorato → prossimo task con 5+ constraint probabilmente delegato a cloud per inerzia → rischio REJECT ripetuto
- OD-006 resta aperto indefinitamente
- Silent-semantic-corruption #7 non ha mitigation sistematica

### Opzione B — Sostituire classe con constraint-count

**Pro**: unica dimensione, matrice stretta.

**Contro**:
- Distrugge ADR-0008 hub pattern validato — classe resta predittiva per cosmetic/behavior/strategic split
- Classe **cattura** la natura rischio (cosmetic non necessita diff; behavior sì): constraint-count non cattura questo
- Overcorrection: i dati non dicono che classe è irrelevant, dicono che constraint-count è **aggiuntivo**

### Opzione C — Aggiungere constraint-count come seconda dimensione (scelta)

**Pro**:
- Preserva ADR-0008 hub pattern (prima dimensione = classe)
- Aggiunge precisione empirica (seconda dimensione = constraint-count)
- Minimal API change: aggiunta ~4 righe table in CLAUDE.md
- Actionable: classificare task con count-then-route è ~30s

**Contro**:
- Matrice diventa 2D (più cognitive load)
- Distinzione "transform" vs "preserve" (qualitativa) richiede judgment oltre al count puro

### Opzione D — Formalizzare come prompt engineering pattern (riduci constraint)

**Pro**: risolve causa upstream (task con 5+ constraint riformulati in sotto-task con <3)

**Contro**:
- Non sempre possibile (es. task atomicamente multi-constraint come refactor API breaking)
- Complementare non alternativo a routing: utile MA serve comunque routing per task irriducibili

## Decision Outcome

### Scelta: Opzione C (seconda dimensione) + Opzione D come pratica complementare

Formalizzare **constraint-count** come seconda dimensione nel routing matrix. Classe resta prima dimensione. Quando possibile, **refactoring del prompt** per ridurre constraint-count è pratica preferita (complementare, non sostitutiva).

### Matrice routing aggiornata

```
┌─────────────┬─────────────────────┬──────────────────────────┬─────────────────────┐
│ Classe →    │ cosmetic            │ behavior                 │ strategic           │
│ Constraint↓ │                     │                          │                     │
├─────────────┼─────────────────────┼──────────────────────────┼─────────────────────┤
│ 1 (add)     │ 7B local whole      │ 14B Q2 local diff        │ Claude Code direct  │
│             │ OR 70B cloud wrap   │ OR 70B cloud diff        │ (non delegabile)    │
├─────────────┼─────────────────────┼──────────────────────────┼─────────────────────┤
│ 2-3         │ 14B Q2 local whole  │ 14B Q2 local diff        │ Claude Code direct  │
│ (additive / │ (7B skippa          │ OR 70B cloud diff        │                     │
│  preserve)  │  transform)         │                          │                     │
├─────────────┼─────────────────────┼──────────────────────────┼─────────────────────┤
│ 2-3         │ 14B Q2 local whole  │ 14B Q2 local diff        │ Claude Code direct  │
│ (fix +      │ (NOT 7B)            │ con review manuale       │                     │
│  transform) │                     │ esplicito                │                     │
├─────────────┼─────────────────────┼──────────────────────────┼─────────────────────┤
│ 5+ (strict  │ 70B cloud diff      │ **Claude Code manual**   │ Claude Code direct  │
│  semantic)  │ (degrada ~20%)      │ OR refactor prompt       │                     │
│             │ OR refactor prompt  │ in sotto-task            │                     │
└─────────────┴─────────────────────┴──────────────────────────┴─────────────────────┘
```

### Come contare constraint (operativo)

Un constraint è **un imperativo distinto** nel prompt che il modello deve rispettare simultaneamente nel output:

- ✅ Counts: "signature stays X", "return shape stays Y", "add retry logic", "use exponential backoff", "max 3 attempts", "discriminator 4xx vs 5xx", "preserve existing logic"
- ❌ Non-counts: lingua, formato commit, qualità generica ("clean code")

**Euristica pratica**: conta gli items numerati / bullet / imperativi nel prompt. Se ≥5, considera refactor in sotto-task.

### Trigger operativi

- **Pre-delega**: classificare task → class (cosmetic/behavior/strategic) → count constraint espliciti → consult matrice
- **Post-delega**: `git diff HEAD~1` verify contro tutti i constraint del prompt (not just sintassi)
- **Hard threshold**: task con ≥5 constraint strict → **non delegare cloud behavior-critical**. Preferire manual Claude Code o refactor.

### Classe transform vs preserve (nuova distinzione qualitativa)

La distinzione "transform" vs "preserve" emerge da dogfood #8 (7B skippa transform) e #9/#10 (14B Q2 safe su preserve):

- **Preserve constraint**: "non modificare X", "keep Y unchanged", "signature stays" → facile da rispettare (inerzia positiva)
- **Transform constraint**: "condense NOTES block", "restructure function", "reformulate logic" → richiede generazione attiva che 7B tende a skippare conservativamente

**Regola derivata**: task con ≥1 transform-constraint richiede **tier ≥ 14B Q2**; 7B è anti-pattern per transform anche con constraint-count=1.

## Consequences

### Positive

- **Matrice routing precisa**: seconda dimensione cattura pattern empirico
- **Safety**: riduce probabilità REJECT-silent-semantic (come #7) orientando task complessi su manual Claude Code
- **Empirical grounding**: 6 data points cross-tier è massa critica decente (n>5)
- **OD-006 chiuso**: decisione aperta da 1 giorno formalizzata con ADR

### Negative / tradeoff

- **Overhead routing**: ~30s addizionali per task vs lookup classe-only. Accettabile (< 1% del tempo task).
- **Judgment qualitativo**: transform vs preserve richiede valutazione; non è meccanico. Mitigation: euristica scritta in ADR.
- **Data points ancora limitati**:
  - n=0 per 14B Q2 con 4-5 constraint (gap)
  - n=0 per 14B Q2 con transform-constraint (gap)
  - n=0 per 70B cloud con 4 constraint (gap: abbiamo solo 3 e 5)
  - **Action**: raccogliere n≥3 aggiuntivi prima di Accepted.

### Neutral / observations

- **Quality bench 75 test non influenza**: i bench (2026-04-23) non avevano constraint-count variabile — misuravano pass@1 su problemi a 0-1 constraint. Il gap tra "100% quality bench" e "20% dogfood #7" è spiegato da questo ADR: non è incoerenza, è dimensione aggiuntiva.
- **ADR-0013 non perde validità**: cloud tier 3 resta primary per behavior-critical ≤3 constraint; degrada solo a 5+ strict.
- **ADR-0008 hub pattern resta backbone**: questo ADR estende, non sostituisce.

## Validation

### Dati attuali (n=6 data points cross-tier OD-006 relevant)

- Constraint=1: n=5 at 100% (cross-tier, dogfood #1/#2/#3/#4/#5 approximate)
- Constraint=2 additive: n=1 at 100% (#9 local 14B Q2)
- Constraint=2 fix+transform: n=1 at 50% (#8 local 7B)
- Constraint=3 mixed: n=2 at 100% (#6 cloud 70B, #10 local 14B Q2)
- Constraint=5 strict: n=1 at 20% (#7 cloud 70B)

### Target closure (movimento Proposed → Accepted)

Richiesti **n≥3 data points addizionali** per colmare gap:

1. **Constraint=4 mix any tier** — gap assoluto
2. **Constraint=2 transform tier 14B Q2** — validare predizione "14B Q2 safe su transform"
3. **Constraint=5 strict tier LOCAL** — validare se pattern 20% si ripete offline (non solo cloud)

Target: 2-3 settimane di uso normale (allineato Sprint 01 H6 + review settimana 2).

### Killswitch / revisione

Se dati successivi contraddicono pattern (es. 14B Q2 @ constraint=2 transform = 95% invece di predizione 50-85%) → revisione matrice, eventuale ADR-0016 Addendum.

## References

- **OD-006** in `OPEN_DECISIONS.md` — origin della decisione, triggering data #7 REJECT
- **Dogfood #6-#11** in `logs/aider-delegation-2026-04.md` — evidence empirica
- **ADR-0008** — hub pattern esteso da questo ADR
- **ADR-0011** — commit governance cross-agent, supplementare
- **ADR-0014** — Fase 6 compression, contexto temporale tracking

## Azioni derivate (da eseguire post-Accepted)

1. Aggiornare `CLAUDE.md` sezione "Priorità modelli AI" con seconda dimensione matrix (stile ADR qui)
2. Aggiornare `MODEL_ROUTING.md` "Routing per fase" con constraint-count column
3. Aggiornare `docs/patterns/delegation-to-aider.md` con step "conta constraint" in classificazione
4. Chiudere OD-006 in `OPEN_DECISIONS.md` (status: Resolved via ADR-0016)
5. Entry JOURNAL per tracking decisione

---

**Open questions per Accepted step**:

- Transform vs preserve distinction: dovrei includere esempi concreti più elaborati per euristica?
- Constraint-count matrix: 4 righe o più granulare (ad es. 4 constraint tier intermedio)?
- Quality bench v2 HumanEval (backlog L1): se discriminant power sufficient, tune matrix con quality bench data oltre dogfood?
