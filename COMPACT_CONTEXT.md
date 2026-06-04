# COMPACT_CONTEXT

> **!! PR-BACKLOG GATE (2026-06-04) -- LEGGERE PRIMA DI INIZIARE QUALSIASI NUOVO LAVORO !!**
> La PRIMA azione di sessione, prima di aprire nuovi progetti/feature, e' rivedere + mergiare i PR
> aperti generati dalle sessioni Jules (+ il fix ADR-index). Eduardo li analizza; NON accodare
> nuovo lavoro finche' non sono triati/mergiati. Aperti al 2026-06-04:
> - Game-Godot-v2 #410 / #411 / #412 -- doc-comments GDScript safe-lane (batch 3/4/5, 11 file, CI-verde)
> - codemasterdd #303 -- reconcile ADR-index DECISIONS_LOG (righe 0037/0038/0039)
> - + eventuali PR ancora aperti da sessioni Jules nei repo Game / Game-Godot-v2 / Game-Database
> Rimuovere questo blocco quando il backlog PR e' chiuso.

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/COMPACT_CONTEXT.md`.
>
> Aggiornare in rituale chiusura sessione (CLAUDE_OPERATING_RULES.md #9): un solo
> blocco "Stato attuale" snapshot, niente accumulo storico (il log dettagliato
> 2026-05 e' archiviato in `docs/archive/compact-context-history-2026-05.md`).

## Progetto
- **Nome**: CodeMasterDD AI Station
- **Ruolo**: infrastructure-as-code + governance + dashboard operativa cross-repo
  per la fleet AI sovereign-first di Eduardo (vedi `CLAUDE.md` autoritativo).

## Stato attuale (verificato git/ls 2026-06-03)
- **HEAD origin/main**: `6a340ac` (2026-06-03) -- `docs(governance): context-files reorg Fase 1 -- slim CLAUDE.md (#270)`.
- **Fase 1 context-files reorg**: DONE (PR #270, slim CLAUDE.md).
- **Fase 2 governance reorg**: IN PROGRESS (slim dei file di contesto stantii;
  questa sessione = slim di COMPACT_CONTEXT.md, history -> `docs/archive/`).
- **ADR**: 36 totali in `docs/adr/` (verificato `ls | wc -l`). Cluster recente
  Jules/orchestration = ADR-0032..0036:
  - ADR-0032 Jules PR governance active model
  - ADR-0033 Jules governance resolved
  - ADR-0034 Jules autonomous-managed model (owner mandate, supersede ADR-0033)
  - ADR-0035 Jules-from-CLI proactive dispatch (async-remote-agent tier)
  - ADR-0036 Unified Orchestration Doctrine (multi-LLM + Jules + Opus 4.8)
- **Focus corrente** (derivato dai commit recenti origin/main): workstream
  governance "governor" + Jules orchestration -- governor signal sources
  (eng-graph, archon-learnings, least-priv token, R1 classifier +
  issue-escalation actor), AI-smoke sovereign judge (vision + deterministic),
  Jules digest/suggestions pipeline.
- **Stack decommissionato** (NON piu' presente): `infra/` (LiteLLM+Langfuse+
  Postgres docker-compose) e `apps/dogfood-ui/` RIMOSSI (ADR-0017 SUPERSEDED da
  ADR-0030 Hybrid A1). `apps/` ora contiene solo `cross-repo-dashboard/` +
  `fleet-tools-mcp/`.
- **OPEN_DECISIONS / DECISIONS_LOG**: vedi i file dedicati per lo stato corrente
  (numerazione OD ben oltre i blocchi storici del log 2026-05; non riportare qui
  conteggi -- consultare la fonte).

## Prossimi passi

1. **Completare Fase 2 governance reorg**: continuare lo slim degli altri file di
   contesto stantii a coppia "lean current snapshot + history archive"
   (stesso pattern applicato qui a COMPACT_CONTEXT.md).
2. **Consolidare la doctrine di orchestrazione**: allineare `ORCHESTRATION.md`
   (154 righe) con il cluster ADR-0034..0036 (Jules autonomous-managed +
   CLI proactive dispatch + Unified Orchestration Doctrine).
3. **Chiusura sessione**: aggiornare il blocco "Stato attuale" sopra (HEAD + ADR
   count + focus) via `git log`/`ls`, MAI copiare numeri stantii.

## Next session: ordine lettura
1. `CLAUDE.md` -- convenzioni progetto autoritative.
2. Questo file (`COMPACT_CONTEXT.md`) -- snapshot stato corrente.
3. `STATUS_MULTI_REPO.md` -- dashboard cross-repo (Game / Game-Godot-v2 /
   Game-Database / Dafne / vault / synesthesia).
4. `ORCHESTRATION.md` -- doctrine orchestrazione multi-LLM + Jules (ADR-0034..0036).
5. `AGENTS.md` SE la sessione e' Codex/OpenCode/sandbox-based -- preamble anti-confusion.
6. `BACKLOG.md` + `OPEN_DECISIONS.md` -- cosa e' aperto ora.
7. ADR rilevanti se il task tocca un topic noto.

(Voci rimosse perche' decommissionate: runbook `adr-0017-hot-restart`,
`docs/archive/plans/integration-aa01-vault-hyperspace`, validation hook `.session-start-head`,
dogfood-ui / infra docker -- vedi history archive.)

## Pointers
- **STATUS_MULTI_REPO.md** -- dashboard operativa cross-repo (status per-repo + HEAD).
- **DECISIONS_LOG.md** -- indice ADR (36) + decisioni operative non-ADR.
- **OPEN_DECISIONS.md** -- decisioni aperte (OD) correnti.
- **BACKLOG.md** -- backlog task corrente.
- **MEMORY.md** -- `~/.claude/projects/C--dev-codemasterdd-ai-station/memory/MEMORY.md` (auto-caricata).
- **Lessons L-038/L-039/L-040** (e cumulative L-001..L-040) -- `~/aa01/learnings/`
  (L-038 ESM CLI pathToFileURL guard, L-039 Game branch-protection footgun FIXED,
  L-040 PowerShell native-stderr-under-Stop false-fail).
- **History 2026-05** -- `docs/archive/compact-context-history-2026-05.md`
  (log dettagliato PR-by-PR 2026-05-07..05-12, archiviato in questa reorg).
