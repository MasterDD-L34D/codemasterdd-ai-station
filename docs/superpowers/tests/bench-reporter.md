# Smoke test log — bench-reporter

## 2026-04-24 — Gate 1 initial

- **Prompt**: quality bench report da results (promptfoo + run-bench storici)
- **Runtime**: 85s (11 tool calls — file reads + parsing)
- **Result**: ✅ PASS con **catch honesty importante**
- **Quality**:
  - **Onestà**: ha flaggato esplicitamente che `promptfoo-smoke.json` non esisteva al path aspettato (mia assumption wrong nel prompt). Zero invention.
  - Parsato 75 test storici run-bench + dogfood log (n=12) correttamente
  - Pass@1 leaderboard: 5/6 modelli coder 100% su 75 test, deepseek-r1:8b 50% framework bug
  - Fail mode analysis con numeri reali (coin_change 314s outlier Qwen 14B Q2)
  - Correlazione dogfood ↔ bench: divergenza constraint-specific confermata, non capability
  - Raccomandazione tier routing Fase 7 con 5 decisioni data-driven
  - Action items honest: noted promptfoo eval non eseguito al path aspettato, va re-runato
- **Key behavior**: agent rifiuta di fabbricare dati "4/4 PASS" se file non esiste. Preferisce flag missing-data che hallucinate.
- **Iteration suggested**: none

## Gate 2 sources validation

- Path locali (docs/research, scripts/quality-bench) — our own
- Dati numerici tutti verificabili nei JSON/MD reali
- **Verdict**: ✅ zero license concern, zero phantom data

## Gate 3 tuning

- **Applicato**: nessuna modifica al prompt. Comportamento "rifiuta invention" è il pattern voluto.
- **Status**: 🟡 draft → ✅ **ready** 2026-04-24

## Action item da smoke test

- Eseguire `promptfoo eval -c promptfoo-smoke.yaml` di nuovo e verify JSON output salvato correttamente (precedente eval ha creato file ma path check è fallito)
