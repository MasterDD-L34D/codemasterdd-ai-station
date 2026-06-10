# Runbook -- Post-Max cutover (~2026-06-17)

Playbook operativo per la scadenza Claude Max (~17/06/2026, rinnovata +1mo il
2026-05-17). Architettura target: **ADR-0030 Hybrid A1** (Accepted 2026-05-18).
ADR-0023 (API on-demand) e' SUPERSEDED parziale: resta valido come **overflow**
quando il Pro daily-limit e' esaurito.

Readiness verificata 2026-06-11 (smoke session, vedi sezione Evidenze).

## Cosa cambia il giorno X (~17/06)

| Prima (Max) | Dopo (Hybrid A1) |
|---|---|
| Claude Code OAuth Max, Opus per tutto | Claude Code **Pro $20/mo** primary per strategic/orchestration |
| Nessun budget concern marginale | Pro daily-limit -> overflow **Claude API on-demand** (cap $10-20/mese, ADR-0023) |
| -- | Routine fallback: **Gemini CLI free** (1000 req/day) |
| -- | Emergency: **OpenRouter** pay-per-use (ADR-0029 reactivated) |
| Tier sovereign (Aider/Ollama/OpenCode) | INVARIATI (cosmetic 7B / behavior 14B Q2 / escalation 30B MoE) |

Routing aggiornato: MODEL_ROUTING.md (sezioni "Routing per fase" e "Status
decisione") + CLAUDE.md "Priorita' modelli / tier routing".

## Chi fa cosa

### Eduardo (manuale, non delegabile)

1. **Subscribe Claude Pro $20/mo** -- timing: pre-17/06 o settimana stessa per
   evitare gap. ~5min su anthropic.com. (ADR-0030 Implementation Plan step 1.)
2. **Verifica OAuth post-switch**: aprire Claude Code, confermare che la
   sessione funziona sul piano Pro (limiti diversi, stesso login).
3. **Autorizzazione spend overflow**: ogni chiamata API on-demand resta
   esplicita ("questo e' strategic, autorizzo Claude API") -- pattern ADR-0023.

### Sistema (gia' pronto, verificato 2026-06-11)

- `ANTHROPIC_API_KEY` presente in `~/.config/api-keys/keys.env` (ACL-locked).
- Pipeline API validata end-to-end (smoke haiku, costo ~$0.00003).
- Spend tracking: `logs/claude-api-spend-YYYY-MM.md` + helper
  `scripts/claude-api/log_spend.py` (crea file mensile, appende entry,
  ricalcola cumulative, avvisa su soglie $10/$15/$20).
- Fallback sovereign smoke-tested: Ollama up, `aider-cosmetic` (7B) e
  `aider-refactor` (14B Q2) producono diff validi in `--dry-run`.

## Procedura tier-0 overflow (quando Pro daily-limit esaurito)

1. Trigger validi (ADR-0023): multi-file >=3 cross-ref / debug architetturale /
   ADR draft strategico / synthesis cross-source / constraint >=5 strict.
2. Mental check budget: month-to-date in `logs/claude-api-spend-2026-MM.md`
   vs cap $10-20.
3. Esegui la sessione API (es. `claude --print "<task>"` con API key, o call
   diretta). Modello a discrezione: haiku per validazioni cheap, opus per
   strategic vero.
4. Logga SUBITO la chiamata:

   ```
   py scripts/claude-api/log_spend.py --task "<desc>" --model <model-id> \
       --tokens-in <N> --tokens-out <M> [--cost-usd <X>] [--outcome "<esito>"]
   ```

   Senza `--cost-usd` il costo e' stimato dalla tabella pricing embedded
   (haiku 1/5, sonnet-4-6 3/15, opus-4-8 5/25 USD/MTok, cached 2026-06-11).
5. Soglie mensili (lo script le stampa da solo): $0-10 OK / $10-15 awareness /
   $15-20 alert / $20+ per 2 mesi consecutivi -> ADR-0023 addendum
   (revisita pay-per-use vs flat).

## Budget coherence (verdetto 2026-06-11)

NESSUNA contraddizione tra ADR-0023 e ADR-0030:

- ADR-0030 riga "ADR-0023 supersession partial": API on-demand "still valid
  for ad-hoc strategic if Pro daily limit hit".
- Il cap $10-20/mese (ADR-0023) e' la sotto-busta overflow dentro l'envelope
  realistico ADR-0030 ($20-50/mo totale = Pro $20 + overflow $0-30).
- Precedenza documentale: ADR-0030 (architettura) > ADR-0023 (procedura
  overflow). Entry-point cross-executor: ORCHESTRATION.md (ADR-0036).

## Rollback: Max renewal

Se post-cutover il volume reale rende Pro+overflow insufficiente o frizione
eccessiva (criteri validazione ADR-0030: cost >$50/mo, methodology cite drop,
daily orchestration fail):

1. Ri-acquisto Claude Max (~5min, stesso flusso del renewal 2026-05-17).
2. Routing torna alla colonna "Prima" della tabella sopra (Opus per tutto).
3. Documentare: addendum ADR-0030 con dati empirici del periodo Hybrid A1
   (il mese di validazione produce numeri reali, non stime).

Il renewal 2026-05-17 e' il precedente: differire la deadline NON annulla il
piano, sposta solo il trigger (ADR-0023 Addendum 2026-05-18).

## Evidenze readiness (smoke 2026-06-11)

| Check | Esito |
|---|---|
| 1. `ANTHROPIC` key in keys.env | PASS (grep -c = 1, valore mai stampato) |
| 2. Spend tracking pattern | PASS (2026-05 esistente; 2026-06 creato via helper nuovo + test pytest 7/7) |
| 3. Budget cap coherence 0023 vs 0030 | PASS (vedi sezione sopra; MODEL_ROUTING allineato) |
| 4. Fallback sovereign | PASS (ollama list 16 modelli; aider-cosmetic e aider-refactor dry-run OK) |
| 5. Smoke API tier-0 | PASS (haiku 12in/4out, "OK" verbatim, ~$0.00003, loggata in spend 2026-06) |

## Riferimenti

- docs/adr/0030-post-max-orchestration-hybrid-a1.md (architettura, Accepted)
- docs/adr/0023-strategic-tier-post-max-api-on-demand.md (overflow, superseded parziale)
- docs/adr/0036 / ORCHESTRATION.md (routing surface unificata)
- MODEL_ROUTING.md (routing per fase + status decisione)
- scripts/claude-api/log_spend.py + scripts/tests/test_log_spend.py
- logs/claude-api-spend-YYYY-MM.md (gitignored, runtime)
