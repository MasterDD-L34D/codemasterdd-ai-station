# ADR-0024 — Vue3 Game archive + Godot v2 canonical: timeline 2026-09-30

> *TL;DR: Game-Godot-v2 (port pivot 2026-04-29) ha 215+ PR mergeati con governance interna autosufficiente. Game (Vue3) Sprint Impronta Ondata 1 in pausa dal 26/04, 2 PR DRAFT 9/5 mattino possibile Ondata 2 status-effect. Long-term Godot v2 frontend canonical, Vue3 archive (gia' dichiarato CLAUDE.md ma senza ADR). Decisione: **soft-deadline archive Vue3 entro 2026-09-30** (4 mesi) con review trimestrale. Trigger archive switch: 60gg senza commit Vue3 OR feature parity Godot v2 dichiarata da Eduardo. Bonus action: AA01 silent-driver attivato esplicitamente su Sprint Impronta Ondata 1+2 status-phase-a per accelerare closure feature flow Vue3 prima dell'archive.*

- **Status**: **Rejected (reconciled + ratified Eduardo 2026-06-08)** -- archive-codebase 2026-09-30 WITHDRAWN; cutover gia' eseguito; modello canonico = Game ADR-2026-05-05 sez.6.3 + `## Addendum reconcile 2026-06-08` in fondo. (Storia Proposed 2026-05-09 preservata sotto.)
- STATUS-CHECK: RETIRED da reconcile 2026-06-08 (review 2026-08-01 + trigger 60gg-silence MOOT)
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

## Sub-events timeline (addendum 2026-05-12)

**Trigger addendum**: Game OPEN_DECISIONS OD-023 (APERTA 2026-05-12) cita esplicitamente questo ADR e raccomanda clarification scope disjoint vs Game ADR-2026-05-05 (Phase B 7gg grace closure).

### Scope disjoint clarification

Vue3 codebase archive timeline ADR-0024 e Phase B web archive Game ADR-2026-05-05 sono **scope disjoint** (sub-event timeline distinta):

| Scope | ADR governance | Path target | Timeline | Sub-event relation |
|-------|----------------|-------------|----------|---------------------|
| **Phase B web archive** | Game `docs/adr/ADR-2026-05-05-cutover-godot-v2-fase-3-formal.md` | `Game/apps/play/` FE only (Cloudflare deploy + Web export) | **2026-05-14 mattina UTC** (formal closure Day 7 grace) | **Sub-event di** archive Vue3 repo-wide |
| **Vue3 codebase archive** | codemasterdd ADR-0024 (questo) | Game/ repo-wide (apps/ + frontend/ + tools/ + tests/ etc., escluso .git history preservata) | **2026-09-30 soft-deadline** (4 mesi) | Macro-event include Phase B come step intermedio |

### Cascade timeline graphical

```
2026-05-14 14:00 UTC -- Phase B formal closure (Game ADR-2026-05-05 §13.4 cascade actions)
                        |-- web-v1-final tag
                        |-- apps/play/ archive
                        |-- README banner
                        |
                        |  [Sprint Impronta Vue3 continues active per Game master-dd cascade verdict]
                        |  [Pillar deltas v40 confirmed: P4 closure imminent]
                        |
2026-08-01 -- Review trimestrale ADR-0024 mid-point check
              |-- commit count Vue3 30gg
              |-- feature parity Godot v2 assessment
              |-- ratification deadline: anticipa / conferma / estende
              |
2026-09-30 -- Soft-deadline ADR-0024 archive Vue3 codebase-wide
              |-- IF trigger objective hit (60gg silenzio O feature parity)
              |   -> archive activated via ADR-0024 addendum
              |-- IF trigger NOT hit
              |   -> review trimestrale dictate continue/extend/abort
```

### Verdict Game OD-023 (autonomous resolution path)

Game OD-023 propone **Path C ORA + Path A Day 8** (canonical execution 2026-05-14 mattina UTC). Path D "ADR amendment 30gg grace extension" (26/35 scoring) NON adottato. Codemasterdd ADR-0024 INVARIATO su soft-deadline 2026-09-30 -- solo clarification scope disjoint aggiunta qui.

**Cross-repo dependency note**: Game OD-023 marked "Cross-repo ai-station alignment" raccomanda "Amendment ai-station ADR-0024 § Sub-events timeline raccomandato Sprint Q+ NON oggi". Questo addendum risolve raccomandazione preserving original ADR-0024 decision invariato.

### No conflict reaffirmed

- Game ADR-2026-05-05 e codemasterdd ADR-0024 NON conflict: sub-event vs macro-event timeline
- Phase B archive 2026-05-14 NON archive Vue3 codebase-wide (continua attivo per Sprint Impronta + post-verdict cascade work)
- Vue3 codebase archive 2026-09-30 INCLUDE archive di `apps/play/` ma post-Phase-B-closure storia gia' completata
- Sprint Impronta + Brigandine + Conviction + trait-editor Vue3 rebuild work (200 PR 14d) sono **attivita interim** Vue3 pre-2026-09-30 deadline, NON contraddicono archive

## Riferimenti

- CLAUDE.md sezione "Progetti monitorati" -> "Evo-Tactics Godot v2 (Game-Godot-v2)" (descrittivo invariato, statement "Vue3 archive decisione futura" formalizzato in questo ADR)
- ADR-0021 -- Multi-client instruction files: `0021-multi-client-instruction-files.md` (Game-Godot-v2 governance autosufficiente validata)
- STATUS_MULTI_REPO.md sezioni Game (Vue3) + Game-Godot-v2
- memory `project_multi_repo_overview.md` (5 progetti attivi + 1 dormant)
- memory `project_aa01_studio.md` (FORBIDDEN actions, audit-replay pattern)
- Harsh review: `docs/governance/flow-chart-harsh-review-2026-05-09.md` (edge case HIGH "Game pivot Vue3->Godot")
- Decisione 007 in `DECISIONS_LOG.md` (Eduardo scelta 5A+)
- BACKLOG H11 (AA01 attivazione Ondata 1+2 Eduardo direct)
- Game `OPEN_DECISIONS.md` OD-023 -- Phase B execution date verdict 2026-05-12 (cross-repo dependency citata)
- Game `docs/adr/ADR-2026-05-05-cutover-godot-v2-fase-3-formal.md` -- scope `apps/play/` web archive Phase B

## Addendum anti-rot — evidence block CONTRADICTED (reconcile 2026-05-17)

⚠️ **La DECISIONE resta valida** (soft-deadline archive Vue3 2026-09-30,
status `Proposed`, trigger 60gg/feature-parity). **Ma il blocco-evidenza
Context era snapshot 2026-05-09 ora FALSIFICATO da git-truth** (audit
veracità ADR 2026-05-17, regola-0):

- "HEAD `5f42757a` invariato" → FALSO: `5f42757a` = commit **2026-04-26**
  (`Merge aa01/cap-15-imprint-phase`), non freeze-marker 9/5. Game `main`
  ora = `427db9a6` (2026-05-17), repo iper-attivo (2300+ PR, merge
  giornalieri). Premessa "Vue3 in pausa / HEAD frozen" contraddetta.
- "2 PR DRAFT #2138/#2139" → FALSO: **#2138 e #2139 sono MERGED**.
- "Game-Godot-v2 215+ PR / 0 open 9/5" + cascade-timeline + AA01-state =
  snapshot rotti.

**Trattamento**: decisione invariata (timeless, deadline futura); il
Context/§"NEW 9/5" = *snapshot storico 2026-05-09 rotto*, NON stato
corrente. Stato Game reale → git-truth / EXECUTION-BOARD, mai i conteggi
qui. (Stesso anti-rot pattern PR #154 / ADR-0027.)

## Addendum reconcile 2026-06-08 -- cutover GIA' eseguito, archive-codebase RITIRATA (WITHDRAWN)

> RECONCILE RATIFIED Eduardo 2026-06-08. Ground-truth verificato 2026-06-08
> (Ryzen, git + ADR cross-repo). Status -> Rejected (reconciled; archive-codebase WITHDRAWN, NON Accepted).

### Cosa e' cambiato dalla stesura (2026-05-09)

Il cutover Godot pianificato qui come futuro e' **gia' avvenuto ed e' ACCEPTED**
lato Game (Scenario 3 STAGED canary,
`Game/docs/adr/ADR-2026-05-05-cutover-godot-v2-fase-3-formal.md`):

- **2026-05-07 -- Phase A ACCEPTED**: Godot v2 = frontend primario; web v1 = fallback.
- **2026-05-14 -- Phase B ACCEPTED** (Path gamma): web v1 (`Game/apps/play/`)
  ARCHIVIATO formale (`apps/play.archive/`). Cutover completo.
- **Backend PRESERVATO by design** (ADR-2026-05-05 sez.6.3): `Game/apps/backend/`
  persiste cross-stack come server di Godot (coop/lobby/companion/wsSession LIVE)
  + balance authority + canon + sim lab.

### Perche' la decisione originale (Opzione A, archive Vue3 codebase-wide 2026-09-30) e' RITIRATA (WITHDRAWN)

Contraddice una decisione downstream gia' ACCEPTED: ADR-0024 voleva archive Game
**repo-wide** (apps/ + tools/ + tests/, vedi sez. Sub-events); Game ADR-2026-05-05
sez.6.3 decide l'OPPOSTO -- **preserva il backend**. Archiviare Game repo-wide
orfanerebbe il server da cui Godot dipende. L'addendum anti-rot 2026-05-17 aveva
gia' falsificato la premessa "Vue3 in pausa".

Quindi:
- **Decisione archive-codebase 2026-09-30: RITIRATA.** Niente archive repo-wide di Game.
- **Review trimestrale 2026-08-01 + trigger 60gg-silence + feature-parity-switch: MOOT**
  (la domanda "archiviamo Vue3?" e' gia' risolta: frontend web archiviato 14/05,
  backend tenuto per scelta).
- Decade anche la validita' affermata dall'anti-rot 2026-05-17 sez."decisione resta
  valida": quel soft-deadline 2026-09-30 NON regge piu'. (Nota MADR/ADR-0010: ADR-0024
  mai-Accepted -> si RITIRA/Withdraw, non si "supersede".)

### Decisione riconciliata (modello canonico ongoing)

1. **Game** = backend/sim/canon **permanente** + balance authority. NON archiviato.
   Archiviato solo il suo frontend web `apps/play` (2026-05-14). E' il server
   cross-stack + sorgente di verita' (SoT, ADR, dataset) + lab simulazione/balance headless.
2. **Game-Godot-v2** = **frontend canonico** del giocatore (cutover 2026-05-07/14).
   Consuma Game backend via HTTP/WS. Regola anti-duplicazione: no backend-logic in
   Godot (Godot CLAUDE.md).
3. **Combat a due motori = ratificato, NON drift.** Backend = balance authority (N=40);
   Godot = d20 client-side shipped-runtime (SoT sez.24.1). Tripwire:
   `Game-Godot-v2/tests/unit/test_combat_engine_parity_contract.gd` (#371).
   **Passivita' DIFFERITA**: quando Godot-combat passa da tutorial/preview a combat
   generale -> re-visit + N=40 (vedi
   `Game-Godot-v2/docs/godot-v2/architecture/combat-engine-divergence.md` sez.6/7).
   Tracciata, non urgente.
4. **Pipeline swarm-to-game (Dafne)**: target = Game (backend/canon/agents) per
   content/logic; Godot per frontend. Ambiguita' originale (sez. Context) risolta.

### Evidenza (snapshot git-truth 2026-06-08, Ryzen -- NON ricitare come stato corrente)

- Velocita' 90gg: Game 1576 commit, Godot 507 (entrambi daily-ship; Game = engine-room
  attivo, non frontend morto).
- Superficie: backend Game ~13.300 LOC (session.js 4185 + roundOrchestrator 1025 +
  vcScoring 1153 + policy 307 + 40 servizi combat ~6.800) vs slice combat/scoring
  client-side Godot ~1.603 LOC = ~8:1. Duplicazione reale = piccola + tripwired.
- Test: Game ~529 file (438 node + 36 tsx + 55 py) + Godot 358 GUT = doppia-suite
  (intrinseca a split client+backend, non spreco).

### Metodo (ADR-0026)

Refresh-verify + Currency Gate (P1): cross-repo git + 5 ADR letti, premesse 05-09
auto-corrette. Brainstorming 3-opt (P6): A reconcile [scelto] / B cutover-totale
[bocciato: ~13k LOC da reimplementare + perdita balance-lab] / C status-quo
[bocciato: review 08-01 su premessa falsa]. SDMG: il reframe NON e' self-designed,
allinea a Game ADR-2026-05-05 gia' Accepted. Harsh-reviewer P5 pre-ratify.

### Ratify gate (Eduardo)

RATIFIED Eduardo 2026-06-08: Status -> Rejected (reconciled); archive-codebase WITHDRAWN;
modello canonico = Game ADR-2026-05-05 sez.6.3 + questo addendum. File toccati (6):
questo ADR + `STATUS_MULTI_REPO.md` + `CLAUDE.md` + `DECISIONS_LOG.md` +
`docs/runbook/adr-status-check.md` + `OPEN_DECISIONS.md` (OD-010). Re-visit-trigger
combat (tutorial->generale = N=40) -> sorvegliato da **OD-010** (scelta Eduardo: OD).
