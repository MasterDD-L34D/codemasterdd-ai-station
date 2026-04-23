# ADR-0014 — Fase 6 timeline compression (3 mesi → 3-4 settimane)

> *TL;DR: ADR-0001 definiva Fase 6 tracking come "3 mesi di uso reale post-Claude Max" per rispondere a 2 domande chiave: (Q1) locale è capace?, (Q2) Claude Pro $240/anno giustificato?. Entrambe risolte infrastrutturalmente dall'ADR-0013 (cloud free tier 630-733 tok/s, $0/anno viable). Rimangono Q3 quality + Q4 reliability, time-bound settimane non mesi. Proposta: comprimere Fase 6 a 3-4 settimane (→ fine maggio 2026, coincide con expiration Claude Max 2026-05-19). Progetto 100% barra atteso fine maggio invece di fine agosto. -3 mesi guadagnati.*

- **Status**: **Accepted** (2026-04-23 02:05 — rationale confermato da quality bench 75 test + approvazione utente)
- **Data**: 2026-04-23 (Proposed + Accepted same day)
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)

## Context and Problem Statement

ADR-0001 "Sovereign AI strategy" (2026-04-19) e ADR-0006/0007/0008 (2026-04-20) definirono **Fase 6** come 3 mesi di "uso reale post-Claude Max" (atteso 2026-05-20 → 2026-08-20) per raccogliere dati empirici su 2 domande dominanti:

- **Q1 — Capability locale**: Qwen 7B/14B/30B MoE è sufficientemente capable per coprire il 90%+ workflow daily?
- **Q2 — Cost giustificazione**: Claude Pro $240/anno necessario come fallback tier 3, o locale basta?

Il tempo 3 mesi fu scelto per:
1. Raccogliere n≥30 dogfood reali (reliability statistica oltre n=5 pre-Fase 6)
2. Osservare coverage task varietà in workflow quotidiano normale
3. Misurare spend effettivo se pay-per-use (baseline $118/3gg ccusage)
4. Consentire decisione informata ADR budget Fase 7 (ibrido Pro vs full-sovereign)

**Il 2026-04-22 sera/notte (ADR-0012 + ADR-0013) ha radicalmente spostato il contesto**:

- **Hardware**: RAM 16→64 GB. qwen3:30b MoE +32% speed post-upgrade (23.3→30.67 tok/s), stabilizzato tier 2 escalation.
- **Acquisizione 4 API keys cloud free-tier** (Groq/Cerebras/Gemini/OpenAI): mai previste in roadmap originale.
- **Bench empirico cloud**: Groq llama-3.3-70b-versatile 630.86 tok/s (**20× vs qwen3:30b locale**), Cerebras llama3.1-8b 733.5 tok/s (**6× vs qwen 7B**).
- **ADR-0013 Validation-in-progress** (Accepted same session 2026-04-23 02:05 post quality bench): scenario "full-sovereign sub-$60/anno" diventa realistic default invece di upper-bound ottimistico.

### Impact sulle domande originali Fase 6

| Domanda originale | Status post 2026-04-22 |
|-------------------|------------------------|
| **Q1** — Capability locale | ✅ **Risolta infrastrutturalmente**. Cloud free tier copre il gap capability per task dove locale non basta; locale resta fallback sovereign per offline/privacy. Non serve n=30 dogfood per validarlo — è già vero per definizione di "posso sempre fallback cloud free". |
| **Q2** — Claude Pro $240/anno giustificato | ✅ **Risolta infrastrutturalmente**. Scenario default è ora full-sovereign ($0/anno via free tier + locale). Claude Pro è superfluo salvo emergere gap quality non coperto. |
| **Q3** — Quality cloud vs Claude (NEW) | 🔴 **Non coperta** originariamente. Serve quality bench scientifico (HumanEval pass@1 o equivalente) per decidere se llama general cloud batte qwen coder-specialist locale su task specifici. Time-bound: 2-3h setup + 1h run, non mesi. |
| **Q4** — Reliability statistica | 🟡 **Parziale**. n=6 attuali troppo piccoli. Target n≥20 ottenibile in **2-3 settimane uso normale**, NON 3 mesi. Fase 6 continua tracking, ma la timeline è over-budget 4×. |

**Le domande time-bound mesi sono risolte. Le rimanenti sono time-bound settimane.**

Questo ADR formalizza la compressione timeline giustificata dal cambio di contesto, evitando il bias "perché abbiamo detto 3 mesi 4 giorni fa".

## Decision Drivers

- **Scientificità**: non mantenere timeline arbitrari quando il razionale originale è decaduto
- **Pragmatismo**: Claude Max expires 2026-05-19 — se Fase 6 chiude ~20/05 c'è continuità naturale (no gap coverage tier 1 strategic)
- **Data-driven**: n≥20 dogfood + 1 quality bench serio = dataset sufficiente per budget decision ADR-0015
- **Anti-hoarding**: fissarsi a "3 mesi perché ADR-0001" quando i dati cambiano è anti-pattern
- **YAGNI (ADR-0005)**: non collect data per collect data. Collect data per decidere.
- **Reality check**: già 6 dogfood in 36 ore + infrastructure completa + quality bench nightly. Il trend raccolta è 10×-20× più veloce dell'assumption originale.

## Considered Options

### Opzione A — Mantenere 3 mesi come da ADR-0001

**Pro**: Coerenza con piano originale. n statistica più larga (30+ garantiti).

**Contro**: 
- Timeline non più necessaria — le domande dominanti sono risolte
- 3 mesi in cui scenario sovereign è già operativo = tempo sprecato per "aspettare dati" quando la decisione è già informabile
- Opportunity cost: fase 7 bloccata per 3 mesi su dato ridondante
- Anti-pattern "path dependency" (seguire piano perché è piano, non perché serve)

### Opzione B (chosen) — Comprimere a 3-4 settimane (→ ~20/05/2026)

**Timing rationale**:
- Inizio Fase 6: 2026-04-22 (inauguration con dogfood #1)
- Chiusura proposta: 2026-05-20 (circa, allineato Claude Max expiration 19/05)
- Durata: 4 settimane dalla inauguration

**Scope Fase 6 ridefinito**:
1. **Quality bench HumanEval-style** (early, settimana 1): primary output
2. **n≥20 dogfood mixed** (cosmetic+behavior, local+cloud): reliability statistica via uso normale
3. **Rate-limit stress cloud** (se emerge): edge case
4. **Privacy policy validation** (se emergono repo sensibili): guard rail check

**Pro**:
- Timeline proporzionata alle domande rimanenti (Q3 quality + Q4 reliability)
- Coincide naturalmente con fine Claude Max → no gap di transizione
- ADR-0015 budget decision prima invece di fine agosto → roadmap completato 3 mesi prima
- Dataset 4 settimane × uso normale = n≥20 plausibile (attuale pace: 6 dogfood in 36h = extrapolato ~100 in 4 settimane anche a pace ridotto)

**Contro**:
- n più piccolo di 30+ originale — meno significatività statistica
- Se emergono bug intermittenti raramente, 4 settimane potrebbero non triggerarli
- Revisione piano originale richiede discipline (non "shift right" se i dati non bastano)

### Opzione C — Eliminare Fase 6 del tutto, decidere ora

**Pro**: Massimo time savings.

**Contro**: 
- Quality bench non fatto → ADR-0013 resta Validation-in-progress
- n=6 dogfood è **troppo piccolo anche per analisi preliminare** (reliability stima ±40% a n=6 per proporzione binomiale)
- Anti-pattern "overcorrection" opposto al precedente

### Opzione D — Split Fase 6 in Short (2 settimane) + Long (residual 10 settimane optional)

**Pro**: Hedging — decide at 2 weeks, continue tracking if data inconclusive.

**Contro**: 
- Over-engineering — i criteri di "inconclusive vs conclusive" vanno pre-definiti, spesa cognitive alta
- YAGNI: se 4 settimane bastano per B, 2 non bastano. Se bastano, la Long è wasted.

## Decision Outcome

**Scelta Opzione B**. Compressione Fase 6 da 3 mesi → **~4 settimane** (chiusura atteso ~2026-05-20).

### Criteri di chiusura Fase 6

Fase 6 può passare a Fase 7 (ADR-0015 budget decision) quando **tutti** i criteri sono soddisfatti:

1. **Quality bench**: HumanEval-subset (≥10 problemi) eseguito su ≥5 modelli (3 local + 2 cloud minimum). Output: pass@1 per modello + ranking capability.
2. **Reliability dogfood**: n≥20 task cumulativi (cosmetic + behavior, local + cloud mix). Fail rate <30% (ADR-0009 T1 trigger threshold) E zero silent corruption.
3. **Privacy validation**: classificazione repo enforced in almeno 3 sessioni reali senza violation (no cloud su Synesthesia `controllers/`, es.).
4. **Cost tracking**: ccusage + cloud costs totale < $20/mese extrapolato. Se > $20 → rivedere routing.

Se uno dei 4 non soddisfatto entro 2026-05-20: estensione mirata (non full 3 mesi) con ADR-0014 Addendum specifico sul gap.

### Adjustments barra progetto

| Fase | Pre ADR-0014 | Post ADR-0014 |
|------|-------------|---------------|
| 6 Empirical tracking | 10% (3 mesi) | 10% (4 settimane) |
| 7 Budget decision | 2% (post-6) | 2% (post-6) |
| **ETA 100%** | **~fine agosto 2026** | **~fine maggio 2026** |

Barra **valore** invariato (88% ora → 100% fine). Barra **tempo** compressa 4×.

### Impact su ADR esistenti

- **ADR-0001**: super-sedente parziale su timeline. Strategy invariata, timing rivisto.
- **ADR-0006/0007/0008/0009**: invariati. La compressione non altera le decisioni tecniche fatte.
- **ADR-0013**: questa compressione **accelera** il path a Accepted (da 3 mesi a 4 settimane).

## Consequences

**Positive**:
- Roadmap 3 mesi più corta → completamento progetto fine maggio
- Focus su Q3 quality (non coperto in ADR originale) + Q4 reliability
- ADR-0015 budget decision in tempo per post-Claude-Max operativo (no gap)
- Time freed per altri progetti (Evo-Tactics development, Synesthesia features)

**Negative / rischi**:
- n=20 meno robust di n=30+. Confidence interval più largo.
- Se emergono bug rari (frequency < 1/settimana) potrebbero non manifestarsi in 4 settimane
- Decisione compressa = meno chance di "lessons learned" slow-brewing

**Mitigations**:
- Quality bench scientific pre-empts alcune delle domande che solo n alto poteva rispondere
- Dogfood variety (cosmetic/behavior/local/cloud) > raw volume
- Criteri di chiusura (4 punti) formalizzati → no temptation di chiudere prematuramente

**Neutral**:
- Se Fase 6 extension mirata serve (criterio 2 non soddisfatto), estendiamo con ADR-0014 Addendum specifico — non blank check 3 mesi

## Follow-up

- [x] Ottenere OK utente su ADR-0014 → passa a Accepted (2026-04-23 02:05)
- [x] **Quality bench immediato eseguito same-day** (docs/research/quality-bench-2026-04-23.md, 75 test 100% pass@1)
- [ ] Aggiornare memory `project_session_resumption.md` con nuova ETA barra 100%
- [ ] Aggiornare CLAUDE.md roadmap section
- [ ] Aggiornare `project_sovereign_evaluation.md` memory con nuova chiusura Fase 6
- [ ] Review a settimana 2 (2026-05-07): se 10+ dogfood → 50% Fase 6. Se no → investigate.
- [ ] Review a settimana 4 (2026-05-20): valutare chiusura vs estensione mirata con ADR-0014 Addendum.

## Riferimenti

- **ADR-0001** `0001-sovereign-ai-strategy.md` — timeline originale 3 mesi (superato parzialmente da questo ADR)
- **ADR-0006** `0006-cline-qwen-viability.md` — iniziale estimate fail rate + Pro $240/anno scenario
- **ADR-0009** `0009-upgrade-strategy.md` — trigger framework (fail rate ≥30% threshold resta valida)
- **ADR-0012** `0012-ram-upgrade-64gb-impact.md` — capability boost tier 2
- **ADR-0013** `0013-tier3-cloud-free-providers.md` — cloud free tier discovery (trigger diretto di questo ADR)
- **Bench empirico**: `docs/research/bench-post-ram-upgrade-2026-04-22.md`
- **Log dogfood**: `logs/aider-delegation-2026-04.md` (n=6 alla redazione di questo ADR)
