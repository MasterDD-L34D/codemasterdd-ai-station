# ADR-0024 — Vue3 Game archive + Godot v2 canonical: timeline 2026-09-30

> *TL;DR: Game-Godot-v2 (port pivot 2026-04-29) ha 215+ PR mergeati con governance interna autosufficiente. Game (Vue3) Sprint Impronta Ondata 1 in pausa dal 26/04, 2 PR DRAFT 9/5 mattino possibile Ondata 2 status-effect. Long-term Godot v2 frontend canonical, Vue3 archive (gia' dichiarato CLAUDE.md ma senza ADR). Decisione: **soft-deadline archive Vue3 entro 2026-09-30** (4 mesi) con review trimestrale. Trigger archive switch: 60gg senza commit Vue3 OR feature parity Godot v2 dichiarata da Eduardo. Bonus action: AA01 silent-driver attivato esplicitamente su Sprint Impronta Ondata 1+2 status-phase-a per accelerare closure feature flow Vue3 prima dell'archive.*

- **Status**: Proposed
- **Data**: 2026-05-09
- **Decisore**: Eduardo Scarpelli
- **Tipo decisione**: cross-repo strategic timeline (Game Vue3 + Game-Godot-v2)

## Context and Problem Statement

Harsh review flow chart 2026-05-09 ha identificato **edge case HIGH**: Game pivot Vue3->Godot definitivo pre-settembre senza decision trigger formalizzato.

### Stato Game Vue3 (`C:\dev\Game`)

- **Sprint Impronta Ondata 1**: in pausa dal 26/04 (~13gg al 9/5)
- HEAD `5f42757a` invariato
- 8+ commit clusterati 25-26/04 driven da AA01 silent-driver (CAP-11 biome-resolution, CAP-12 telemetria, CAP-13 imprint mockup, CAP-14 onboarding v2, CAP-15 imprint phase V2)
- PR #2108 swarm-distillation MERGED 8/5 11:15 UTC
- **NEW 9/5 mattino**: 2 PR DRAFT `feat/status-phase-a-*` (#2138 glossary 5 traits + #2139 policy debuff target) -- possible Ondata 2 status-effect feature flow
- Owner: Eduardo + AA01 silent driver

### Stato Game-Godot-v2 (`C:\dev\Game-Godot-v2`)

- **Pivot 2026-04-29**: ricostruzione visuale + UX in engine native parallel-run con Game (Vue3)
- Cloned 2026-05-07 in workspace, 20.7 MB
- **215+ PR mergeati totali**, 0 open al 9/5 mattino
- 200 test file GUT (~1719 asserts, 178 scripts)
- Path A canonical CHIUSO end-to-end + Sprint AC bundle 15 sub-sprint chiuso
- Governance interna autosufficiente: CLAUDE.md proprio + AGENTS.md proprio + .claude/SAFE_CHANGES.md + .claude/TASK_PROTOCOL.md
- Hook globali codemasterdd applicati (commit-msg + pre-commit Layer 1+2)

### Statement esistente in CLAUDE.md (senza ADR)

> "Long-term: Godot v2 frontend canonical, Vue3 archive (decisione futura, NON ancora ADR)."

Questo statement vive solo nel descrittivo "Progetti monitorati". Non c'e' trigger di switch, non c'e' deadline, non c'e' criteria di feature parity. Risk:
- Vue3 manutenzione continua "per inerzia" anche dopo Godot v2 superseded feature parity
- Drift cross-repo (hook globali applicati a entrambi, doppia governance overhead)
- Pipeline swarm-to-game (Dafne H5 gate) target ambiguo (a quale repo invia agent files?)
- AA01 silent-driver continua su Vue3 indefinitamente

## Decision Drivers

- **YAGNI / lean**: NO archive prematuro. Vue3 ha ancora valore se Sprint Impronta produce feature gameplay non ancora in Godot v2.
- **Anti-drift**: senza deadline, "decisione futura" scivola via 12+ mesi. Pattern visto altrove (debt accumula).
- **AA01 active focus**: AA01 driver non puo' essere su 2 repo paralleli senza dispersione. Decision serve a indirizzare AA01 capacity.
- **Pipeline swarm-to-game**: Dafne integration deve sapere repo target. Ambiguita' = risk integration silent-broken.
- **Hook globali manutenzione**: due repo con governance autonoma = manutenzione doppia overhead.

## Considered Options

### Opzione A (chosen) -- Soft-deadline archive Vue3 entro 2026-09-30 + AA01 attivazione esplicita Ondata 1+2

Setup:
- **Soft-deadline archive Vue3**: 2026-09-30 (4 mesi da oggi)
- **Review trimestrale** (2026-08-01): assessment Sprint Impronta Vue3 status, feature parity check vs Godot v2, ratification estensione/anticipazione/conferma deadline
- **Trigger archive switch (qualunque dei due si verifichi prima)**:
  - **60gg senza commit Vue3 main** (non DRAFT/branch personali) -> archive automatic via ADR-0024 addendum
  - **Feature parity dichiarata da Eduardo** "Godot v2 copre tutto Vue3 gameplay" -> archive immediate
- **Bonus action AA01**: Eduardo attiva esplicitamente AA01 silent-driver mode su Sprint Impronta Ondata 1+2 status-phase-a (PR #2138 + #2139 DRAFT 9/5) per accelerare closure feature flow Vue3. Action e' Eduardo direct (AA01 NON git-tracked, codemasterdd non puo' driving).

**Pro**:
- Deadline forza chiarezza senza essere prematura
- Review trimestrale = check empirico
- Trigger objective (60gg silenzio) anti-drift
- AA01 attivazione accelera closure naturale Vue3 (anti-pause indefinito)

**Contro**:
- Soft-deadline puo' essere ignorata se Eduardo dimentica review trimestrale
- AA01 attivazione e' Eduardo direct, codemasterdd non puo' enforce

### Opzione B -- Aspetto Sprint Impronta closure naturale (no deadline)

**Pro**: pragmatic, no decisione prematura
**Contro**: drift indefinito. Sprint Impronta puo' tirare per mesi. Anti-pattern (visto altrove).

### Opzione C -- Skip per ora (YAGNI integral)

**Pro**: zero overhead decisione
**Contro**: scarica decisione su future Eduardo. Risk choice futuro in panico (es. quando manutenzione doppia diventa insostenibile).

## Decision Outcome

**Scelto Opzione A**: Soft-deadline archive Vue3 entro 2026-09-30 + AA01 attivazione esplicita Ondata 1+2.

### Action items applicati

1. **Soft-deadline registrato**: 2026-09-30 archive Vue3 main repo
2. **Review trimestrale calendar**: 2026-08-01 (mid-point check)
3. **Trigger objective monitorato**: ogni 14gg in routine governance refresh, check `git log -1 --format="%ci" main` su Game Vue3. Se >60gg silenzio -> trigger ADR-0024 addendum.
4. **Feature parity check**: gate Eduardo dichiara explicitly. Pattern: in chat dice "Godot v2 ha feature parity con Vue3, switch ADR" -> immediate archive.
5. **AA01 attivazione Ondata 1+2** (Eduardo direct action, non codemasterdd-driven): Eduardo apre AA01 workspace `C:\Users\edusc\aa01\` e attiva silent-driver mode su Sprint Impronta Ondata 1+2 status-phase-a (PR #2138 + #2139 DRAFT). codemasterdd traccia in BACKLOG H11 come task Eduardo standalone.

### Archive procedure (quando trigger si attiva)

```
1. Eduardo dichiara archive in chat o via commit message in codemasterdd
2. ADR-0024 addendum: status archive activated, data effettiva, trigger che si e' attivato
3. CLAUDE.md "Progetti monitorati" sezione Game Vue3 -> sezione Game-Godot-v2 only
4. STATUS_MULTI_REPO row Game Vue3 -> "ARCHIVED YYYY-MM-DD" con HEAD finale + reason
5. memory project_multi_repo_overview update (5 progetti -> 4 attivi + 1 archived + 1 dormant)
6. Pipeline swarm-to-game (Dafne) update: target Godot v2 only
7. Hook globali codemasterdd: invariati (Vue3 archive resta git-tracked, hook applicati ma repo passive)
```

## Consequences

### Positive

- Deadline forza decisione concreta entro 2026-09-30
- Review trimestrale 2026-08-01 e' check empirico (vs assumption)
- Trigger 60gg silenzio anti-drift automatic
- AA01 attivazione accelera closure naturale Vue3 (pause finita, focus su Ondata 1+2 closure)
- Pipeline swarm-to-game indirizzo chiaro post-archive
- Cognitive load dual-repo manutenzione finita

### Negative

- AA01 attivazione e' Eduardo direct (codemasterdd non enforce)
- Soft-deadline ignorabile se review trimestrale skipped
- Risk premature archive se Vue3 ha feature in arrivo non ancora visibili

### Neutral

- Game-Godot-v2 governance interna invariata (codemasterdd non sovrascrive)
- Vue3 git history preservata (archive non delete)
- Synesthesia dormant invariato (decisione separata)

## Follow-up

- [ ] **Eduardo direct (BACKLOG H11)**: attiva AA01 silent-driver mode su Sprint Impronta Ondata 1+2 status-phase-a (PR Game DRAFT #2138 + #2139)
- [ ] **Routine governance refresh**: ogni 14gg check `git log -1 --format="%ci" main` Game Vue3 (trigger 60gg silenzio)
- [ ] **2026-08-01 review trimestrale**: assessment Sprint Impronta status + feature parity Godot v2 + ratification deadline 2026-09-30 (anticipa/conferma/estende)
- [ ] **Pipeline swarm-to-game**: Dafne integration target documentation update (Vue3 OR Godot v2 OR both based on archive status)
- [ ] **Trigger Accepted** (status flip Proposed -> Accepted): post 2026-08-01 review trimestrale con dati empirici (commit count Vue3, feature parity check, AA01 driver progress).

## Riferimenti

- CLAUDE.md sezione "Progetti monitorati" -> "Evo-Tactics Godot v2 (Game-Godot-v2)" (descrittivo invariato, statement "Vue3 archive decisione futura" formalizzato in questo ADR)
- ADR-0021 -- Multi-client instruction files: `0021-multi-client-instruction-files.md` (Game-Godot-v2 governance autosufficiente validata)
- STATUS_MULTI_REPO.md sezioni Game (Vue3) + Game-Godot-v2
- memory `project_multi_repo_overview.md` (5 progetti attivi + 1 dormant)
- memory `project_aa01_studio.md` (FORBIDDEN actions, audit-replay pattern)
- Harsh review: `docs/reviews/flow-chart-harsh-review-2026-05-09.md` (edge case HIGH "Game pivot Vue3->Godot")
- Decisione 007 in `DECISIONS_LOG.md` (Eduardo scelta 5A+)
- BACKLOG H11 (AA01 attivazione Ondata 1+2 Eduardo direct)
