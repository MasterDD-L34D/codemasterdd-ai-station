# COMPACT_CONTEXT

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/COMPACT_CONTEXT.md`.
>
> Aggiornare in rituale chiusura sessione (CLAUDE_OPERATING_RULES.md #9): un solo
> blocco "Stato attuale" snapshot, niente accumulo storico (il log dettagliato
> 2026-05 e' archiviato in `docs/archive/compact-context-history-2026-05.md`).

## Progetto
- **Nome**: CodeMasterDD AI Station
- **Ruolo**: infrastructure-as-code + governance + dashboard operativa cross-repo
  per la fleet AI sovereign-first di Eduardo (vedi `CLAUDE.md` autoritativo).

## Stato attuale (verificato git/ls/gh 2026-06-10)
- **HEAD origin/main**: `9bd8543` (2026-06-08) -- `docs(journal): resume Lenovo + sync Ryzen + vault hygiene (#314)`. 0 PR open.
- **Context-files reorg**: COMPLETE Fasi 1-6 (2026-06-03, 12+ PR; vedi memory
  `project_context_files_reorg`). Nessun follow-up aperto.
- **ADR**: 39 totali in `docs/adr/`. Cluster recente orchestration/autonomy:
  - ADR-0036 Unified Orchestration Doctrine (multi-LLM + Jules + Opus 4.8)
  - ADR-0037 merge-autonomy model
  - ADR-0038 doctrine carveout completion
  - ADR-0039 R1 open-PR reconcile rung
- **Focus corrente fleet** (verificato gh 2026-06-10): lane Game = Ryzen ATTIVA
  (OD-058 wound cutover D1->D3 flip ON #2713/#2714/#2720 + ER6 StressWave +
  coop quorum role-aware + SPEC-I active; 14 PR merged solo il 06-10; residuo =
  Gate-5 #2716 + tracker #2531). Godot-v2: stream #2679 chiuso, AI playtest
  item-3 co-op PASS (#465). Lane Lenovo = hygiene cdd + residui journal 06-08.
- **Scadenza**: Claude Max ~2026-06-17 -> front-load task tier-0 (roadmap
  journal 06-07: P1 SPEC / P2 K-tickets / P3 full-loop / P4 burn-down / P5 ADR-0036).
- **Stack decommissionato** (NON piu' presente): `infra/` (LiteLLM+Langfuse+
  Postgres docker-compose) e `apps/dogfood-ui/` RIMOSSI (ADR-0017 SUPERSEDED da
  ADR-0030 Hybrid A1). `apps/` ora contiene solo `cross-repo-dashboard/` +
  `fleet-tools-mcp/`.
- **OPEN_DECISIONS / DECISIONS_LOG**: vedi i file dedicati per lo stato corrente
  (numerazione OD ben oltre i blocchi storici del log 2026-05; non riportare qui
  conteggi -- consultare la fonte).

## Prossimi passi

1. **Residui journal 06-08** (non-blocking): clv2 hook fix settings.json
   (Eduardo-gated), vault gitlink `Master-DD-Pathfinder-GPT` (vault-PR gate),
   governance burn-down ~6 dir-batch (piano in Game BACKLOG #2614).
2. **Compass**: pilastro `cross-fleet-reproducibility` scoperto da 30 commit
   (path candidato `scripts/backup/**`).
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
