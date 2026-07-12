# Personal Agentic OS -- ricerca multi-source (2026-07-12)

> Input per ADR-0044. Metodo: (a) /last30days engine v3.8.3 (Reddit+HN+GitHub,
> 36 item, 30 giorni) + 6 WebSearch supplement; (b) deep-research Workflow
> (105 agent: 5 angoli di ricerca -> fetch 15 fonti -> estrazione claim ->
> verifica adversariale 3-voti). Raw social: `~/Documents/Last30Days/personal-agentic-os-raw-v3.md`.
> ASCII-first (ADR-0021).

## Limiti dichiarati del run

- Sorgenti social attive 3/5: X e YouTube non configurate (unlock: login x.com
  su Firefox; `yt-dlp`). Corpus Reddit sottile (4 thread).
- Fase verify del deep-research degradata: 37/105 agent persi per session limit
  (reset 19:00). 13 claim CONFERMATI (voti 3-0 o 2-0) prima del limite; i claim
  con verifier persi sono elencati come NON VERIFICATI e non fondano decisioni.
- Synthesis step del workflow fallito (stesso limite): sintesi fatta dal hub sui
  claim grezzi.

## Claim VERIFICATI (3-0 / 2-0, fonte primaria)

Architettura (arXiv 2604.14228, paper sull'architettura Claude Code):

1. Claude Code si decompone in 5 layer canonici: surface / core (agent loop +
   compaction) / safety-action (permissions, hook, tool, subagent) / state
   (context assembly, sessioni, CLAUDE.md + memoria) / backend.
2. Memoria persistente = file-based e stratificata: gerarchia CLAUDE.md a 4
   livelli + auto-memory scritta dal modello + transcript JSONL append-only.
   Il continuous learning nativo e' "append su file", non un database.
3. Safety = defense-in-depth a 7 meccanismi indipendenti; valutazione regole
   strettamente deny-first (deny vince sempre su allow, anche se allow e' piu'
   specifico).
4. I subagent girano su sidechain e tornano SOLO summary al parent: la
   composizione multi-agente passa per file condivisi, non contesto condiviso.
5. Anti-pattern documentato: la defense-in-depth puo' collassare in silenzio
   quando i layer condividono failure mode (es. >50 subcommand -> fallback a
   prompt generico invece del check per-subcommand). Testare i path di degrado.

Memoria (docs ufficiali code.claude.com/docs/en/memory):

6. Esattamente 2 meccanismi nativi cross-session: CLAUDE.md (user-written) +
   auto-memory (Claude-written); entrambi caricati a inizio conversazione.
7. Auto-memory e' machine-local e per-repository; NON condivisa tra macchine.
   (Per la flotta: coerente con la scelta gia' presente in
   `scripts/fleet/sync-claude-global.ps1` che esclude `memory/` dal sync.)
8. Di MEMORY.md vengono caricate solo le prime 200 righe / 25KB: il pattern
   canonico e' indice conciso + topic file on-demand.
9. CLAUDE.md e' advisory (consegnato come user message, nessuna garanzia di
   compliance): enforcement duro = SOLO hook (PreToolUse).

Scheduling (docs ufficiali code.claude.com/docs/en/scheduled-tasks):

10. Tre meccanismi con tradeoff distinti: Routines cloud (no macchina, no file
    locali, min 1h) / Desktop scheduled task (file locali, permessi
    configurabili, min 1min) / /loop di sessione (eredita permessi+MCP, richiede
    sessione aperta).
11. /loop e cron di sessione SCADONO automaticamente a 7 giorni (safety bound):
    automazione durabile = Routines o Desktop scheduled task.

Routing multi-provider (docs.litellm.ai/docs/routing -- riferimento di settore;
nota: gateway LLM per noi resta decommissionato, OD-009):

12. Strategia default e raccomandata in produzione = simple-shuffle (le
    alternative aggiungono latenza): il default zero-infrastruttura e' anche
    quello raccomandato dal vendor.
13. Failover deterministico via parametro `order` sui deployment (local-first ->
    cloud fallback esprimibile come ladder di priorita').

## Claim NON verificati (verifier persi per session limit -- direzionali, fonte autorevole)

Da anthropic.com/engineering/multi-agent-research-system:

- Orchestrator-worker (lead forte + worker economici) +90.2% vs single-agent
  sull'eval interno Anthropic.
- Multi-agente ~15x token di una chat (single agent ~4x): giustificato solo per
  task ad alto valore; cattivo fit per la maggior parte del coding.
- Pattern contesto: piano in memoria esterna, fasi riassunte su file, artifact
  scritti su filesystem dai subagent (non transitano dal lead).
- Anti-pattern delega vaga -> spawn eccessivo/duplicato; fix = delega esplicita
  (obiettivo, formato output, tool, boundary) + effort-scaling nel prompt.

Da docs/blog vari (stesso stato):

- Guida Anthropic: CLAUDE.md <200 righe, solo fatti continuamente validi;
  procedure -> skill (match: policy reorg 2026-06-03 gia' applicata).
- OpenClaw distingue cron (timing esatto, sessione isolata, task record) da
  heartbeat (~30min, inline nella sessione, no record) -- tassonomia utile per
  G1 anche se non verificata.

## Segnali community (last30days, 30 giorni)

- "Agentic OS" = termine caldo con due anime: enterprise (Fiserv agentOS,
  MindStudio 5-layer/9-componenti) e personal/hacker (Show HN: Istota, Wolffish,
  GSV "personal AI computer that unifies your machines"; repo itseffi/personal-os
  multi-runtime con skill canoniche + bridge). Persino accademico (workshop
  AgenticOS @ ASPLOS/SOSP 2026).
- Regola di design ricorrente: "Skill teaches the how, Hook enforces the rule,
  Subagent isolates the work" (ofox.ai).
- Chi l'ha costruito racconta 3 rebuild prima della stabilita' (mejba.me):
  la stratificazione esplicita paga.
- Pattern giugno 2026: Dynamic Workflows (fan-out massivo) + grader/rubric sui
  subagent (Totalum).
- Churn modelli = rumore dominante nelle community: l'OS deve essere
  model-agnostic nel routing (gia' vero: MODEL_ROUTING.md e' per-tier, non
  per-modello).

## Gap analysis vs dotazione esistente

| Layer canonico | Esistente | Gap |
|----------------|-----------|-----|
| Kernel/dottrina | ORCHESTRATION.md + ADR-0036/0037 | nessuno |
| Routing | MODEL_ROUTING.md + delegation-classifier + llmfit | nessuno |
| Esecutori | 16 subagent + skill + wrapper + Jules + Workflow | nessuno |
| Memoria | auto-memory + MEMORY.md index + AA01 + JOURNAL | nessuno (per-machine = design) |
| Scheduling | 2 cron R0 + jules-daily-digest | G1: heartbeat/brief R0 (governor-gated) |
| Self-maintenance | AA01 + continuous-learning-v2 + consolidate-memory + compass | G3: wiring non fatto (eval-gated) |
| Safety | hook stack + privacy guard + keys + allow-glob | nessuno |
| Leggibilita' d'insieme | -- | mappa unica assente -> AGENTIC_OS.md |

Conclusione: composizione, non costruzione. Dettaglio decisionale in
[ADR-0044](../adr/0044-personal-agentic-os-composition.md).
