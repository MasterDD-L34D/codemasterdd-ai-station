# Smoke test log — cost-monitor

## 2026-04-24 — Gate 1 initial

- **Prompt**: cost snapshot Fase 6 + proiezione Fase 7 + alert check
- **Runtime**: 64s (5 tool calls — ccusage + file reads)
- **Result**: ✅ PASS
- **Quality**:
  - ccusage invocato correttamente (monthly + weekly)
  - Cumulative cloud $0.0148 (4 Groq call) estratto dal log dogfood con accuracy
  - Breakdown per provider (4 provider tracked, 3 zero-usage, Groq 4 call)
  - Proiezione mensile lineare: $0.00493/giorno × 30 = $0.148/mese
  - Alert: nessuno (threshold $0.10/entry mai hit, running total <1% budget)
  - Raccomandazione Fase 7: scenario A matematicamente sostenibile ($1.78/anno su budget $50)
  - Clarification importante: $479.85 ccusage è Max subscription usage-equiv, NON out-of-pocket — non conta verso ADR-0014 criterio #4
  - Onesto noting: dogfood.sqlite non inizializzato, log Markdown resta source-of-truth
- **Iteration suggested**: none

## Gate 2 sources validation

- ccusage (npm package pubblico, MIT) — legacy tool accepted
- Log Markdown interno — our own
- ADR-0014 threshold — our own
- **Verdict**: ✅ zero external license concern

## Gate 3 tuning

- **Applicato**: nessuna modifica. Output già data-driven + onesto su distinzione Max-vs-pay-per-use.
- **Status**: 🟡 draft → ✅ **ready** 2026-04-24

## Next invocations attese

- Mid-sprint snapshot (~2026-04-30)
- Pre-closure check settimana 4 (~2026-05-17) — critical per ADR-0015 ratification
- Fase 7 quarterly report post-transition
