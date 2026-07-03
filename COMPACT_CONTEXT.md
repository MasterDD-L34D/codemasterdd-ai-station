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

## Stato attuale (verificato git/ls/gh 2026-07-03, fleet audit)
- **HEAD origin/main**: `eca45fe`+ (2026-07-03; avanza a ogni land, hub molto
  attivo Ryzen+Lenovo in parallelo). 0 PR miei aperti sul hub.
- **Fleet health VERDE** (audit 2026-07-03, workflow 5-probe + verify 4-agent,
  overall_go): dashboard registry 10/10 + run-monitor 50/50, Game/GGv2
  origin/main CI verde. Unico RED era **Game-DB "Evo Import Sync"** (giu' 3gg,
  bot 403 + `_game` gitlink) -> **FIXATO #233** (permissions block + gitignore)
  MERGED e **provato live** (workflow_dispatch SUCCESS). Blueprint fleet-verify
  -> Artifact `claude.ai/code/artifact/78108b9b`.
- **Modello sessioni**: sessione avviata Fable 5, switch a Opus 4.8 a fine
  giornata (trailer commit riflette il modello attivo al commit). Finestra
  Max/Opus-crunch di giugno passata. Roadmap post-Max: ADR-0023/0030.
- **Arco MAP-Elites v2 CHIUSO+MERGED** (memory `project_map_elites_v2`): Game
  #3181+#3182+#3183 e hub #453+#459+#460+#465 tutti MERGED (2026-07-02 20:16Z),
  **0 residui**. M15 = card `map-elites-hc06-v2-edm` + fix conteggio (iter
  SPRT-evicted NON scrivono iter-json -> done = max(json, iter distinte
  checkpoint.jsonl); VERIFICATA comportamentalmente 50/50 COMPLETE sul dir
  reale via funzione shippata). Lesson chiave: MAI backend Node spawnato con
  stdout=PIPE non drenato; checkpoint.jsonl = contatore autoritativo.
- **Campagna doc-comment GGv2**: **134/280 (48%)** post batch 34 (#581+#582,
  primo dispatch da Lenovo -- gate-4 dedup = guardia cross-machine, runbook
  aggiornato multi-machine `93fe89d`). Lane policy ratificata:
  `docs/reference/jules-lane-policy.md` (FILLER-ONLY max 1 trio/sessione in
  coda, stop a pool vuoto, ~9 file clean residui; 100% NON e' un goal).
- **Compass**: DI ~72-82 (oscilla con la window same-day). Due drift risolti =
  falsi positivi da mis-scoping (#469 scripts/fleet, #473 fleet-tools-mcp).
  `agentic-tooling` drift = artefatto di finestra (30 commit same-day), NON
  neglect -- recon scope-vs-neglect PRIMA di ogni commit (anti L-016).
- **Fleet altre lane 07-03**: Ryzen lane L3 char-test attiva (telemetry-bridge
  #3187, vc_telemetry_harness #3188, pe_candidates #3189, generate_open_decisions
  #3195 -- PR-to-owner do-NOT-merge); July-spend chip -> card dashboard cap-watch
  su main; code-graph tooling landato (ADR-0043).
- **ADR**: ~43 file; **collision 0040 RISOLTA** (#482: 0040-code-graph ->
  0043-code-graph-tooling-adoption; resta 0040-doctrine-triage-label). Recenti
  0041 sovereign-SD, 0042 evo-swarm entity-grounding, 0043 code-graph.
- **Stack decommissionato** (NON piu' presente): `infra/` (LiteLLM+Langfuse+
  Postgres docker-compose) e `apps/dogfood-ui/` RIMOSSI (ADR-0017 SUPERSEDED da
  ADR-0030 Hybrid A1). `apps/` ora contiene solo `cross-repo-dashboard/` +
  `fleet-tools-mcp/`.
- **OPEN_DECISIONS / DECISIONS_LOG**: vedi i file dedicati per lo stato corrente
  (aperte oggi: OD-010 monitoring, OD-011 hub-watch, OD-012 hub-watch).

## Prossimi passi

1. **Chip game-family (spawned 2026-07-03)**: sessione hub pulita che applica
   Fasi 1-4+7 del blueprint fleet-verify su Game/GGv2/Game-DB (topologia +
   salute repo + dashboard game + governance, ogni RED verificato adversarial,
   sintesi Artifact). Read-mostly, draft-PR + hand-merge.
2. **Fronte playtest Game** = prossima sessione piena (journal 07-02 sera-2:
   leggere prima memory `project_godot_visual_asset_pipeline` + coordinarsi
   con arco Game). Baricentro progetto, critical path.
3. ~~agentic-tooling recon~~ **FATTO 2026-07-02 sera**: verdetto = artefatto di
   finestra (30 commit window = tutto same-day; wrappers toccato 06-30), NO
   neglect, nessun commit aspirazionale; unica omissione scope reale =
   `apps/fleet-tools-mcp/**` aggiunto al pillar (#473 MERGED). Non rifare.
4. **Campagna GGv2**: prossimo filler trio (pool ~9, by NA):
   ai/ai_personality_loader + main_ai_progress + combat/resistance_engine --
   SOLO in coda a sessione con altro focus (lane policy).
5. **Chiusura sessione**: aggiornare il blocco "Stato attuale" sopra (HEAD + ADR
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
