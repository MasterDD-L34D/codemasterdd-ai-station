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

## Stato attuale (verificato git/ls/gh 2026-07-02)
- **HEAD origin/main**: `8add847` (2026-07-02) -- `docs(journal): 07-02 MAP-Elites
  v2 arc -- pipe root-cause, 2 run, 4 PR (#459)`. 0 PR open sul hub.
- **Modello sessioni**: Claude Fable 5 attivo (trailer `claude-fable-5`); la
  finestra Max/Opus-crunch di giugno e' passata (journal 07-02 "siamo tornati
  con fable"). Roadmap post-Max: vedi ADR-0023/0030.
- **Arco 2026-07-02 MAP-Elites v2 CHIUSO in giornata** (memory
  `project_map_elites_v2`): Game #3181+#3182 e hub #453+#459 MERGED; residuo =
  Game #3183 (knob-space SoT + fix SPRT) in review -> BACKLOG M15 + OD-012.
  Lesson chiave: MAI backend Node spawnato con stdout=PIPE non drenato
  (event-loop freeze a buffer pieno; provato con drain-recovery).
- **Focus fleet altre lane** (journal 07-02, 3 sessioni stesso giorno): campagna
  doc-comment Godot-v2 ripresa (119/279, batch 26-31) + arco ennea chiuso (5 PR);
  filone opencode-headless CHIUSO (hang strutturale su Windows, 2 major testate).
- **ADR**: 43 file in `docs/adr/` (ls 2026-07-02; include SUPERSEDED inline).
  Cluster recente orchestration/autonomy: ADR-0036..0039.
- **Context-files reorg**: COMPLETE Fasi 1-6 (2026-06-03; memory
  `project_context_files_reorg`). Nessun follow-up aperto.
- **Stack decommissionato** (NON piu' presente): `infra/` (LiteLLM+Langfuse+
  Postgres docker-compose) e `apps/dogfood-ui/` RIMOSSI (ADR-0017 SUPERSEDED da
  ADR-0030 Hybrid A1). `apps/` ora contiene solo `cross-repo-dashboard/` +
  `fleet-tools-mcp/`.
- **OPEN_DECISIONS / DECISIONS_LOG**: vedi i file dedicati per lo stato corrente
  (aperte oggi: OD-010 monitoring, OD-011 hub-watch, OD-012 hub-watch).

## Prossimi passi

1. **M15**: Game #3183 review/merge Eduardo (knob-space SoT + fix SPRT +
   edm-run results); al merge, opzionale card RUN_MONITORS per v2-edm-run.
2. **Campagna doc-comment Godot-v2**: coda clean residua ~12 file (journal
   07-02 sera per la lista).
3. **Compass**: pilastro `cross-fleet-reproducibility` scoperto da 30+ commit
   (path candidato `scripts/backup/**`).
4. **Chiusura sessione**: aggiornare il blocco "Stato attuale" sopra (HEAD + ADR
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
