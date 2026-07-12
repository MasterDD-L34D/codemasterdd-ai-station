# ADR-0044 -- Personal Agentic OS: composizione dell'esistente, non costruzione

- Status: Proposed
- Data: 2026-07-12
- Deciders: Eduardo (ratifica); autore draft: Claude (Fable 5, hub Lenovo)
- Contesto: richiesta Eduardo "creare il nostro Agentic OS personale" previa ricerca
  (last30days + deep-research). Ricerca completa: [report](../research/personal-agentic-os-2026-07-12.md).
- Protocolli applicati: agent-scanner (BOOTSTRAP+TEAM_FORMATION), Currency Gate,
  autoresearch multi-source (ADR-0026 P2), 3-approcci pre-decisione (ADR-0026 P6).

## TL;DR

L'"Agentic OS" richiesto ESISTE gia' al ~90% come federazione di pezzi maturi
(ORCHESTRATION.md, MODEL_ROUTING.md, 16 subagent, skill, hook, memoria file-based,
AA01, cron R0). Cio' che manca e' il layer unificante: una MAPPA che nomina il
sistema e collega layer -> authority, un guard-test anti-drift, e una roadmap
onesta dei 3 gap reali (tutti Eduardo-gated). Decisione proposta: Opzione C
(composizione). Nessun framework esterno, nessun componente runtime nuovo.

## Contesto

La ricerca (36 item social/HN/GitHub + 13 claim verificati 3-0 da fonti primarie:
paper arXiv 2604.14228 sull'architettura Claude Code, docs ufficiali memory/
scheduled-tasks, docs LiteLLM, blog engineering Anthropic multi-agent) converge su
un modello canonico di agentic OS a layer: instructions / routing / esecutori /
memoria / scheduling / self-maintenance / safety.

Audit dell'esistente (ground-truth 2026-07-12): ogni layer canonico ha GIA' una
authority matura in questo repo o nella dotazione globale -- dettaglio nella
tabella di [AGENTIC_OS.md](../../AGENTIC_OS.md). Tre finding di ricerca rilevanti
per il design:

1. **Memoria auto e' machine-local per design della piattaforma** (docs ufficiali,
   verificato 3-0) E il nostro `sync-claude-global.ps1` la esclude gia'
   deliberatamente dal sync. Il "gap fleet-memory" NON e' un gap: scelta ratificata.
2. **CLAUDE.md e' advisory, non enforcement** (verificato 3-0): garanzie dure solo
   via hook PreToolUse. Il nostro stack hook (commit-guard, ASCII, tdd-guard) e'
   gia' allineato a questo principio.
3. **Scheduling di sessione (/loop, cron) scade a 7 giorni** (verificato 3-0):
   automazione durabile = Desktop scheduled task / Routines cloud. I nostri 2 cron
   R0 + jules-daily-digest sono gia' sulla forma giusta.

## Opzioni considerate

### A. Adottare uno starter/framework esterno (agent-os, personal-os, claude-flow, ...)

- Pro: layer gia' impacchettati; community attiva (itseffi/personal-os ha il
  pattern multi-runtime `.agents/skills/` + bridge).
- Contro: shadow-duplicate massivo di 16 subagent + skill + dottrina esistente
  (OD-007); tasso storico integrazione materiale esterno ~25%; ADR-0036 sec 8
  esclude esplicitamente framework di orchestrazione (piu' failure surface che
  valore per solo-dev); ri-base = perdere 40+ ADR di dottrina gia' falsificata.
- Verdetto: **REJECT**.

### B. Costruire un layer OS nuovo (app runtime: scheduler + memory service + gateway)

- Pro: "OS" nel senso letterale; single pane.
- Contro: SDMG P7 (autonomizzazione self-designed senza falsificazione); duplica
  la roadmap governor gia' SDMG-disciplinata (spec 2026-06-01, R0 live); gateway
  LLM gia' decommissionato (OD-009). Il dato direzionale "multi-agente ~15x token"
  (blog Anthropic, NON verificato 3-0 -- vedi report) rafforza ma non fonda il
  rifiuto: gia' OD-009 + SDMG lo reggono da soli.
- Verdetto: **REJECT**.

### C. Composizione: mappa + guard-test + roadmap gated (scelta proposta)

- Pro: zero nuova superficie di rischio; da' al sistema il nome e la leggibilita'
  che mancano (il pain reale: "state lookup = grep many places", spec governor
  pain #4); anti-drift meccanico (test path-existence = Currency Gate cablato in
  pytest); ogni incremento futuro resta gated dai binari esistenti (earn-path
  governor, Quality Gate, ADR).
- Contro: non "costruisce" nulla di visibilmente nuovo oggi; i gap G1-G3 restano
  aperti finche' Eduardo non li ratifica.
- Verdetto: **ACCEPT (proposto)**.

## Decisione (proposta)

1. **[AGENTIC_OS.md](../../AGENTIC_OS.md)** in root = mappa dell'OS: 7 layer ->
   authority esistente, boot, principi verificati, gap onesti. Indice puro,
   nessuna authority nuova (le decisioni restano in ORCHESTRATION.md / ADR).
2. **Guard-test** `scripts/tests/test_agentic_os_map.py`: ogni link repo-relative
   della mappa deve esistere (con negative control, L-041). La mappa non puo'
   marcire in silenzio.
3. **CLAUDE.md**: la mappa entra nell'ordine di lettura come step 1b (1 riga).
4. **Ratifica del non-gap**: memoria auto per-machine resta il design (nessun sync
   di `memory/`); la conoscenza cross-fleet viaggia gia' via repo (JOURNAL,
   COMPACT_CONTEXT, docs) e vault.
5. **Roadmap gated** (nessuna azione senza decisione Eduardo):
   - G1 heartbeat/morning-brief = rung R0 report-only dentro l'earn-path governor
     (non un nuovo canale di autonomia).
   - G2 unlock sorgenti last30days (X via Firefox login, YouTube via yt-dlp).
   - G3 wiring `continuous-learning-v2` al ciclo AA01, previa eval Quality Gate.

## Conseguenze

- Positive: sistema nominabile e navigabile ("il nostro OS" = questa mappa);
  onboarding nuova sessione piu' rapido; drift dei riferimenti intercettato dai
  test; i finding di ricerca restano citabili (report in docs/research/).
- Negative/accettate: la mappa e' un file in piu' da tenere corrente (mitigato
  dal guard-test); i claim non verificati del report (verifier persi per session
  limit) restano etichettati come tali e non fondano decisioni.
- Follow-up: alla ratifica G1-G3, ciascun incremento apre il proprio percorso
  (governor spec / Quality Gate), NON questo ADR.

## Riferimenti

- Report ricerca: [personal-agentic-os-2026-07-12](../research/personal-agentic-os-2026-07-12.md)
- ADR-0036 (dottrina orchestrazione), ADR-0037 (merge autonomy), ADR-0026
  (protocolli cognitivi), ADR-0016 (constraint-count routing), OD-007 / OD-009.
- Fonti primarie chiave: arXiv 2604.14228 (architettura Claude Code a 5 layer);
  code.claude.com docs memory + scheduled-tasks; anthropic.com engineering
  multi-agent research system; docs.litellm.ai routing.
