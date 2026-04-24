# ADR-0015 — Fase 7 budget decision: full-sovereign $0-50/anno con deroga criterio privacy

> *TL;DR: Fase 6 ha chiuso 3/4 criteri ADR-0014 PASS (quality 75 test / cost 0.074% budget / reliability on-track verso n=20). Criterio #3 (privacy Synesthesia n≥3) **de-facto non chiudibile** entro 2026-05-19: Synesthesia è progetto dormant fino esame UniUPO agosto 2026, dataset reale acquisibile solo post-agosto. Decisione: adottare **scenario A (full-sovereign $0-50/anno)** post-Max con deroga esplicita su criterio #3, completamento privacy validation rinviata a riattivazione Synesthesia. Trigger ADR-0008 "FULL-SOVEREIGN VIABLE" già confermato empirically mid-sprint (cosmetic 93% / behavior 70-80% / corruption 0 / mix success 83%). Claude Pro declassato definitivamente a opzione emergency-only.*

- **Status**: **Proposed** (2026-04-24 — draft preparatorio per ratification a review settimana 4 ~2026-05-17)
- **Data**: 2026-04-24
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)

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
