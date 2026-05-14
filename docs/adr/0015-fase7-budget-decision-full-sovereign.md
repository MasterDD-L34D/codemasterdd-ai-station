# ADR-0015 — Fase 7 budget decision: full-sovereign $0-50/anno con deroga criterio privacy

> *TL;DR: Fase 6 ha chiuso 3/4 criteri ADR-0014 PASS (quality 75 test / cost 0.074% budget / reliability on-track verso n=20). Criterio #3 (privacy Synesthesia n≥3) **de-facto non chiudibile** entro 2026-05-19: Synesthesia è progetto dormant fino esame UniUPO agosto 2026, dataset reale acquisibile solo post-agosto. Decisione: adottare **scenario A (full-sovereign $0-50/anno)** post-Max con deroga esplicita su criterio #3, completamento privacy validation rinviata a riattivazione Synesthesia. Trigger ADR-0008 "FULL-SOVEREIGN VIABLE" già confermato empirically mid-sprint (cosmetic 93% / behavior 70-80% / corruption 0 / mix success 83%). Claude Pro declassato definitivamente a opzione emergency-only.*

> **⚠️ AMENDMENT 2026-05-15 sera-tardi-ultra-3 (ADR-0030)**: Target $0-50/anno **VIOLATED by realism**. Eduardo realization mattina 15/5: scenario A copre code-editing tier MA NON copre orchestration + reasoning + methodology + sub-agents + skills (CC desktop unique value). Eduardo usage 75% Max settimanale = high-volume incompatibile free-tier-only. Decisione amendment: **scope rescoped da "$0-50/anno absolute"** → **"no Claude Max premium (~$1200/anno) + multi-provider flexibility + methodology preservation"**. Nuovo target realistico **$240-600/anno** via Hybrid A1 (CC Pro $20/mo + Meridian + OpenCode + Gemini CLI free + OpenRouter overflow). ADR-0030 supersedes scenario A absolute target. Vedi ADR-0030 per architectural detail + Implementation Plan + Validation criteria.

- **Status**: **Accepted con amendment 2026-05-15** (target $0-50/anno violated, scope rescoped per ADR-0030)
- **Data**: 2026-04-24 (Proposed) -- 2026-05-07 (Accepted) -- 2026-05-15 (Amendment ADR-0030 supersedes scenario target)
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)
- **Amendment trigger**: Eduardo statement 2026-05-15 mattina "non ho un modo effettivo per affrontare il tutto senza claude code desktop" + autoresearch Meridian/OpenCode plugin discovery

## Context and Problem Statement

ADR-0014 (Accepted 2026-04-23) ha compresso Fase 6 a 3-4 settimane con 4 criteri di closure:

1. Quality bench ≥1 test-suite comparativa local vs cloud
2. Reliability dogfood dataset n≥20, fail rate <30%, zero silent-corruption
3. **Privacy validation** ≥3 sessioni reali enforcement policy (Synesthesia mixed)
4. Cost tracking mensile <$20/mese cloud API

OD-001 definì 3 opzioni per ADR-0015:
- **A — full-sovereign** $0-50/anno (locale + cloud free tier)
- **B — ibrido Claude Pro** $240/anno (Pro + Ollama + cloud free)
- **C — extension** Fase 6 mirata 2-4 settimane

### Status criteri closure a 2026-04-24 (dataset n=12)

| Criterio | Status | Dato |
|----------|--------|------|
| #1 Quality bench | ✅ **PASS** | 75 test Leetcode, 5 stack 100% pass@1 (discriminant-limited ma baseline stabilito) |
| #2 Reliability | 🟡 **ON-TRACK** | 12/20 (60%), fail rate 8.3% (vs 30% threshold). Gap 8 → fattibile 3-4 sessioni opportunistic |
| #3 Privacy Synesthesia | 🔴 **BLOCKER** | 1/3 — **progetto dormant fino agosto 2026** (esame UniUPO), dataset reale non acquisibile entro 2026-05-19 |
| #4 Cost <$20/mese | ✅ **PASS** | $0.0148 cumulative (0.074% budget) |

### Input nuovo 2026-04-24

Eduardo ha comunicato che **Synesthesia è progetto dormant** fino alla sessione lavoro pre-esame UniUPO (agosto 2026). Conseguenze:

- Gap criterio #3 (2 sessioni privacy mancanti) non forzabile senza fabbricare task sintetici
- Task sintetici su Synesthesia non validerebbero empiricamente il workflow reale (anti-pattern)
- Extension Fase 6 fino ad agosto (scenario C) richiederebbe 3 mesi extra di bridge stack **senza lavoro reale** che generi i dati → costo ingiustificato per raccogliere dati non utilizzati

## Options

### Opzione A — Full-sovereign con deroga criterio #3 ✅ RACCOMANDATA

Chiudi Fase 6 a ~2026-05-20 con **3/4 criteri PASS + 1 derogato** con rationale documentato. Transizione post-Max a stack sovereign:

- **Tier 1-2 locale**: Qwen Coder 7B/14B Q2/30B MoE (Ollama, RTX 5060 + 64GB RAM)
- **Tier 3 cloud free**: Groq llama-3.3-70b primary + Cerebras llama3.1-8b secondary
- **Tier 4 cloud paid**: OpenAI gpt-4o-mini (emergency-only, monitorato via ccusage)

Privacy validation completata post-agosto quando Synesthesia riattivata → ADR-0014 criterio #3 **retroattivamente chiuso** senza bloccare Fase 7 transition.

**Costo annuo atteso**: $0-50 (solo emergency OpenAI se/quando).

**Pro**:
- Ratifica quanto empirically già validato (FULL-SOVEREIGN VIABLE trigger ADR-0008 confermato mid-sprint)
- Zero costo bridge per validation dati non ancora acquisibili
- Onest: deroga documentata > criterio finto-chiuso con test sintetico
- Reversibile: se post-agosto privacy testing rivela gap critici → ADR addendum correttivo

**Contro**:
- Criterio #3 tecnicamente non chiuso in modo "orthodoxo" → richiede accettazione esplicita deroga in questo ADR
- Rischio residuo (basso): privacy policy per-repo mai stress-tested su caso reale Synesthesia mixed

### Opzione B — Ibrido Claude Pro $240/anno

Mantieni Claude Pro come tier 3 backbone, sovereign come tier 1-2, skip extension Fase 6.

**Pro**: riduce rischio closure con criterio #3 derogato, Claude Pro copre gap quality ipotetici.

**Contro**:
- $240/anno spesa ricorrente per coprire rischio ipotetico **non dimostrato empirically** (12 dogfood mostrano sovereign 83% success)
- Quality bench 75 test ha mostrato parità 100% su 5 stack → Pro non aggiunge valore misurato
- ADR-0013 ha già declassato questo scenario da baseline a fallback
- Conflitto con target ADR-0001 "zero subscription ricorrenti"

**Verdict**: declassato a opzione residuale. Non raccomandato.

### Opzione C — Extension Fase 6 fino post-agosto

Prolunga Fase 6 di 3 mesi (2026-05-20 → ~2026-08-31) per completare criterio #3 quando Synesthesia riattivata.

**Pro**: tutti 4 criteri chiudono "regolarmente".

**Contro**:
- **Stack bridge 3 mesi** richiede Claude Max o Pro attivo → $60-240 spesa non giustificata da lavoro reale
- 12→20 reliability target raggiunto anche senza extension (solo 3-4 sessioni)
- Quality + cost già PASS → extension **serve solo per un criterio**
- Rischio che Synesthesia si riattivi oltre agosto (esame slittato, ecc.) → extension apre-ended
- Contraddice ADR-0014 "time-bound settimane non mesi"

**Verdict**: scartata. Costo >> beneficio.

## Decision

**Opzione A — Full-sovereign con deroga criterio #3**.

### Closure protocol Fase 6 (da applicare ~2026-05-20 @ review settimana 4)

1. **Verifica criterio #2 reliability — minimo accettabile n≥15 (soft-override esplicito del target originale n≥20)**:
   - Target originale ADR-0014: n≥20 con fail rate <30%.
   - **Soft-override documentato qui**: se n reale a 2026-05-17 è tra 15-19 con fail rate <15% (storicamente ≈9-10%), accettabile closure. Rationale: ogni dogfood opportunistic, non forzabile senza inventare task; trend statistico già robusto.
   - Se n<15 a 2026-05-17 → **hard blocker**, extension 1 settimana con target explicit "push a ≥15".
   - Se fail rate drift oltre 15% → **hard blocker**, revisione scenario A (possibile switch a B ibrido).
2. Verifica criterio #4 costo mensile (target <$20 ampiamente rispettato — cumulative attuale $0.0148).
3. Quality criterio #1 già PASS 2026-04-23.
4. Criterio #3 **derogato** con rationale documentato in questo ADR: dataset acquisibile solo post-agosto, privacy policy per-repo formalizzata e documented (CLAUDE.md), deroga time-boxed a riattivazione Synesthesia.
5. ADR-0015 Status → Accepted se criteri #1/#4 PASS + #2 n≥15 + #3 derogato.
6. Claude Max disattivato 2026-05-19. Transizione a wrapper tier 3-4 cloud + locale.

### Post-agosto protocol

Quando Synesthesia torna attiva (sessione lavoro reale pre-esame UniUPO):

1. Priorità immediata: completare gap privacy validation 2/3 rimanenti (tocca `views/` cloud OK + `controllers/` sovereign).
2. Tracking entries in `logs/aider-delegation-YYYY-MM.md` con field `privacy_policy_enforced: true/false`.
3. Al raggiungimento n=3 → ADR-0014 criterio #3 **retroattivamente PASS**, annotare in DECISIONS_LOG come "Decisione NNN".
4. Se emergono pattern anomali (policy violation / silent privacy leak) → ADR addendum correttivo immediato.

## Closure verdict 2026-05-07

ADR Accepted con closure anticipata vs target ~2026-05-17 originale. Rationale: 12 giorni di gap operativo su codemasterdd (24/04 -> 07/05) per shift focus su Game Sprint Impronta + Dafne Atto 2 day 11+ + AA01 driver-mode. Dataset codemasterdd-Fase 6 fermo a n=12 dal 24/04. Push a n>=15 in 12 giorni richiederebbe forzare task sintetici, anti-pattern documentato in ADR-0014 ("anti-hoarding... collect data per decidere, non per collect data").

### Status criteri ADR-0014 alla closure

| Criterio | Status finale | Dato | Note |
|----------|---------------|------|------|
| #1 Quality bench | PASS | 75 test Leetcode, 5 stack 100% pass@1 | Confermato 2026-04-23, no regressioni |
| #2 Reliability dogfood | PASS (soft-override) | n=12, fail rate strict 8.3% (1/12), behavior 5/3 superato (167%), zero silent-corruption working-tree | Vedi sotto |
| #3 Privacy Synesthesia | DEROGATO | 1/3 -- Synesthesia dormant fino esame UniUPO ~ago 2026 | Retroattivo post-agosto |
| #4 Cost <$20/mese | PASS | $0.0148 cumulative (0.074% budget) | Margine 99.93% |

### Soft-override criterio #2 esteso

ADR-0015 originale (2026-04-24) prevedeva soft-override n>=15 con fail rate <15%. Al 2026-05-07 il dataset reale e' n=12 (3 sotto target soft).

**Override esteso a n=12 con i seguenti rationale (additivi)**:

1. **Trigger ADR-0008 "FULL-SOVEREIGN VIABLE" confermato empiricamente mid-sprint** (sessione 2026-04-24 dogfood #12): cosmetic 93% / behavior 70-80% / corruption 0 / mix success 83%. Il valore decisionale del dataset e' raggiunto -- dogfood aggiuntivi ridondanti per decision support.
2. **Behavior-critical 5/3 superato (167%)**: il sotto-target piu' rilevante dal punto di vista qualita' (behavior change vs cosmetic) e' superato di larga misura. Il numero assoluto n=12 sotto-pesa la composizione qualitativa del dataset.
3. **Fail rate strict 8.3% << threshold 30%**: il margine di sicurezza statistico (banda 21.7 punti percentuali sotto threshold) sostiene la decisione anche con n moderato.
4. **Zero silent-corruption working-tree** su 12 esecuzioni reali: il rischio operativo principale identificato in ADR-0008 e' empiricamente assente.
5. **Forzatura a n>=15 in 12 giorni produce dogfood sintetici** (non organici): contraddice ADR-0014 "data per decidere".

### Trigger di ri-evaluation rimasti attivi

Soft-override e' valido se nei 12 giorni residui (07/05 -> 19/05) NON emergono questi pattern:

- silent-corruption >= 1 caso reale (non test): hard blocker, switch a scenario B ibrido
- fail rate cumulative >15% (oltre il margine di sicurezza)
- privacy violation in repo non-sensitive (cloud delegation leak)

Se dataset cresce naturalmente con qualche dogfood opportunistic da smoke test sovereign (vedi ADR-0015 follow-up post-closure), update inline metriche senza riaprire ADR.

### Decisione confermata

**Scenario A -- Full-sovereign $0-50/anno** post 2026-05-19. Stack:

- Tier 1-2 locale: Qwen Coder 7B / 14B Q2 / 30B MoE (RTX 5060 + 64GB RAM)
- Tier 3 cloud free: Groq llama-3.3-70b primary + Cerebras llama3.1-8b secondary
- Tier 4 cloud paid: OpenAI gpt-4o-mini emergency-only (ccusage monitorato)
- Claude Max: disattivato 2026-05-19, non rinnovato
- Claude Pro: NOT acquired, scenario B declassato definitivamente

### Action items post-closure

1. Smoke test full-sovereign empirico end-to-end (3 wrapper aider-cosmetic + aider-refactor + aider-groq) -- validation tecnica, dogfood entries opzionali
2. SPRINT_02 abbozzo (post-Max scenario A operativo) -- handoff per prima sessione 20/05+
3. Privacy validation Synesthesia rinviata a riattivazione ~agosto 2026 -- ADR-0014 criterio #3 retroattivo a quel momento
4. STATUS_MULTI_REPO + COMPACT v11 update con stato closure
5. JOURNAL entry chiusura Fase 6

## Consequences

### Positive

- **Ratifica empirica**: closure basata su dati reali n=12 + quality 75 test, non su extrapolation
- **Budget zero ricorrente**: allinea ADR-0001 target post-maggio 2026 senza compromessi
- **Onestà metodologica**: deroga esplicita > criterio finto-chiuso con test sintetico
- **Reversibilità**: se post-agosto privacy test rivela gap → ADR addendum, no rollback architetturale

### Negative

- Criterio #3 tecnicamente non chiuso orthodoxamente, richiede accettazione deroga
- Rischio residuo (basso): privacy policy per-repo mai stress-tested empirically prima di agosto

### Mitigations

- Deroga **time-boxed**: Se Synesthesia non torna attiva entro 2026-10-31, revisitare in ADR addendum
- Synthetic smoke-test opzionale in Sprint 02 (dopo closure Fase 6): NON sostituto del criterio, ma sanity-check che il classifier policy per-repo non abbia bug ovvi
- Privacy audit manuale CLAUDE.md sezione "API keys tier 3 cloud" + privacy policy Synesthesia periodicamente

## Related

- **ADR-0001** — Sovereign AI strategy (target zero subscription)
- **ADR-0008** — Hub pattern tier routing (trigger FULL-SOVEREIGN VIABLE)
- **ADR-0013** — Tier 3 cloud free providers (scenario baseline shift)
- **ADR-0014** — Fase 6 timeline compression (criteri closure)
- **ADR-0016** — Constraint-count routing dimension (Proposed, influenza Tier routing post-Max)
- **OD-001** — (Closed by this ADR) Scenario budget Fase 7

## Notes

- Questo ADR è **Proposed** 2026-04-24 preparatorio. **Ratification a review settimana 4** (~2026-05-17) dopo verifica criteri #2 e #4. Se tutti gli indicatori confermati → Accepted; altrimenti revisione mid-course con addendum.
- Gap 8 dogfood residui verso n=20 NON bloccano questo ADR — target #2 è "on-track", non "completato". Closure a n=20 preferibile ma non hard-blocker.
- Trigger review: se tra 2026-04-24 e 2026-05-17 emerge fail rate >30% cumulative OR silent-corruption >0 → re-evaluation opzione A, possibile escalation a opzione B.
