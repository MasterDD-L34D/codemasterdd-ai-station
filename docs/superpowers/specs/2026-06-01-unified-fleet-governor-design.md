# Unified Fleet Governor -- design spec (phased, SDMG-disciplined)

> Status: DRAFT v2 2026-06-01 -- FALSIFIED by harsh-reviewer (SDMG P7 step 3),
> verdict SURVIVE-WITH-CHANGES, all 4 P0 + P1 adopted (adopt-not-defend). Author:
> Claude (Opus 4.8) on Ryzen.
> Scope of THIS spec: the north-star governor architecture + an HONESTLY-scoped rollout.
> Fase 0 (doctrine) + Fase 1 (observability) are COMMITTED. Fasi 2-4 are an
> evidence-gated ROADMAP -- each earns its own ADR + SDMG gate when lower-rung evidence
> justifies it. No autonomy is ratified ahead of evidence.
> ASCII-first body (ADR-0021). Authority chain: ADR-0036 (why) -> ORCHESTRATION.md
> (which-executor/autonomy) -> CLAUDE.md (how).

## 0. Naming honesty

"Unified Fleet Governor" is the NORTH STAR (the full observe->classify->act->schedule
loop). What ships first (Fase 1) is a **cross-repo signal aggregator (active)** -- a
cron that reads islands' committed signal files and renders a consolidated pane. The
grandiose name is kept for the destination only; do not let it license scope creep
(harsh-reviewer P2.3).

## 1. Problem

Governance is a FEDERATION of self-governing islands + a doctrine/observability hub
(this repo) + 2 autonomous crons. The pieces of a single governor exist; no single
observe->classify->act loop is wired. Goal: wire it WITHOUT breaking SDMG
(falsify-before-autonomy).

### 1.1 Ground-truth verified 2026-06-01 (Protocol 1, on Ryzen)

| Fact | Source | Reading |
|------|--------|---------|
| ADR-0036 = `Proposed`; ratify-trigger is **SDMG-incompatible** (NOT circular) | `docs/adr/0036-*.md` line 112 | The trigger is "rollout auto-merge under the gate stack, observe >=1 clean cycle/repo, then ratify" -- a standard ship-behind-reversibility pattern, meetable by definition. The defect is that it asks you to RUN auto-merge to GENERATE its own ratify-evidence; that is barred by SDMG (P7: no autonomize-before-falsify) and by anti-#10 (bot-rewrite-drop, a real logged incident). Conclusion: revise to an earn-path that accrues evidence at a lower, reversible rung first. (harsh-reviewer P0.1 corrected my earlier "circular" misread.) |
| Autonomy ceiling = `git push origin claude/*` | `.claude/settings.json` | No merge / no `gh pr merge`. Auto-merge NOT wired = confirmed. |
| Dashboard = Flask + in-memory cache, NO SQLite | `apps/cross-repo-dashboard/app.py` | "ingest + persist signals" = net-new code (the map's "SQLite" was wrong). |
| Gate-E real pain in-window = 0 | Lenovo `logs/coord-events-2026-05.md`, read via SSH | Only 2 entries, both 2026-05-14, both labeled test/probe. Window 2026-05-20..06-19. CAVEAT: verified via one-shot SSH read of Lenovo; NOT reproducible Ryzen-side (`logs/` gitignored, Lenovo-only). It only strengthens the zero. (harsh-reviewer P2.2.) |
| Map vault path-bug already fixed | `app.py resolve_repo_path(... "C:\\dev\\vault" first)` + commit #240 | Do NOT re-fix. Map authored pre-#240. |
| 2 crons already run lower rungs clean | vault coherence-pass `0 */6 * * *` (report-only) + codemasterdd `playtest2-board-sync` `0 4 * * 1` (PR-only) | The R0 (report) + R1 (open-PR) rungs already exist at small scale, clean. board-sync raw-fetches Game's signal -> PR, never auto-merge. This is the proven shape to generalize. |

### 1.2 The evidence basis -- stated honestly (harsh-reviewer P0.4 + P1.1)

Gate-E logged pain = 0. Eduardo asserts the pain is real but unlogged (L-016
abandonment). There are TWO readings of the zero, **indistinguishable on current data**:

- **A (build):** "pain real, I stopped logging" -> the federation needs the governor.
- **B (defer):** "pain below my action-threshold" -> ESCALATION_GATES.md line 43:
  `<2/wk = adoption successful = defer iteration`.

Eduardo's verbal "build the full thing" is a **destination authorization**, NOT evidence
that reading A is correct. SDMG step 5 (narrow adoption) forbids committing the whole
machine on an unfalsified assertion. Therefore:

- **Committed now:** Fase 0 (doctrine fix) + Fase 1 (R0 observability) -- because R0 is
  the SAME risk class as today's read-active dashboard, AND R0 is precisely **the
  experiment that distinguishes A from B**.
- **Roadmap (not committed):** Fasi 2-4. Each gets its own ADR + SDMG gate, unlocked
  only by real R0 evidence (sec 4 off-ramp).

This is the destination Eduardo chose (C, full governor) reached the SDMG way: build the
observability rung, let it produce honest pain data, then earn each autonomy increment.

### 1.3 The 4 confirmed pains (drive priority; mapped to rungs)

1. **Signals emitted, nobody acts** (Game `governance_drift_report.json` + sot-drift,
   vault gap-scan/coherence/whats_missing, evo-swarm weekly digest, ARCHON learnings).
   -> cured at **R0** (consolidated pane).
2. **Cross-repo propagation hand-carried** (only the 1 Game-pillar signal auto-PRs
   today). -> cured at **R1** (actor opens branch+PR; human merges).
3. **Drift found late -> rework** (stale pointers, anti-#19 tracker lag, SoT vs shipped).
   -> **R1** escalation.
4. **State lookup = grep many places** (dashboard only observes). -> **R0** pane.

Pains #1 and #4 are cured by the COMMITTED Fase-1 (R0) at near-zero risk. #2 and #3
need R1 (Fase 2, roadmap-gated).

## 2. Architecture -- north-star loop (built incrementally)

The governor = `cross-repo-dashboard` PROMOTED from read-active aggregator to active.
One loop, four stages; each maps to a rung and a Fase:

```
ISLANDS (signal producers)                GOVERNOR (this repo)            RUNG / FASE
  Game governance_drift_report.json  ->  [ OBSERVE ]  ingest+persist  ->  R0 / Fase 1  (cures #1,#4)
  Game sot-drift-sentinel            ->     read-only consolidated pane     COMMITTED
  vault gap/coherence/whats_missing  ->        |
  evo-swarm weekly digest            ->        v
  ARCHON learnings                   ->  [ CLASSIFY ] signal->action  ->  R1 / Fase 2  (cures #2,#3)
                                              per ADR-0036 ladder          ROADMAP (own ADR)
                                                 |  {report|open-PR|escalate}
                                                 v
                                          [ ACT ]     branch+PR        ->  R2 / Fase 3
                                              human merges; auto-merge      ROADMAP (own ADR,
                                              ONLY journal/doc-reconcile     harsh-reviewer
                                                 |  class, reversible        falsifies increment)
                                                 v
                                          [ SCHEDULE ] cron + kill-switch + acted-on gate  R3 / Fase 4
                                                                                            ROADMAP
```

Design-for-isolation (each stage = separate, independently-testable unit, narrow interface):

- **Ingestor** (per-island adapter): island signal location -> normalized `Signal`
  record persisted to SQLite. Reuses OD-042-A raw-fetch (consumer raw-fetches producer's
  git-committed file, NO cross-repo auth). Blind to classification.
- **Classifier** (Fase 2): `Signal` -> `LadderVerdict {action, risk_class, rationale,
  target_repo}`. Pure function; no I/O; ADR-0036 sec 5 as code + tests.
- **Actor** (Fase 2 R1 / Fase 3 R2): performs the action. Auto-merge is a SEPARATE
  gated capability (Fase 3), default OFF.
- **Persistence (SQLite)**: signal history + verdict log. NEW.

## 3. Autonomy ladder -- the earn-path (defined now, auto-merge NOT activated)

ADR-0036 sec 5 defines the ladder CLASSES. This spec defines the rungs + a CONCRETE,
MECHANICAL earn-path (harsh-reviewer P0.2 -- no hand-wavy "N=?", no self-assessed
"clean"). The earn-path is DEFINED in doctrine but R2+ stays HUMAN-GATED until a future
per-rung ADR verifies the earned evidence.

| Rung | Action | Unlock condition (mechanical) |
|------|--------|-------------------------------|
| R0 | report-only (write signal + verdict to store/pane) | none -- same risk class as today's dashboard |
| R1 | open branch+PR / emit escalation (HUMAN merges) | R0 ran + harsh-reviewer OK on the classifier + CI green. Reversible (a PR is inert until merged). |
| R2 | auto-merge LOWEST-risk reversible class ONLY (journal/doc-reconcile) | (i) >=4 distinct **clean R1 cycles** across >=2 repos over >=2 weeks; (ii) harsh-reviewer FALSIFIES this specific increment; (iii) revert path proven; (iv) a different-FAMILY judge in the gate (sec 5 note). Granted by a dedicated R2 ADR, not by this spec. |
| R3+ | wider auto-merge classes | each = its own SDMG increment + ADR; never a block |
| -- | irreversible/destructive, outward-facing, account-credential, external-comms, ADR-class | HUMAN irreducible -- never automated (ADR-0036 sec 5 residue) |

**Mechanical definition of a "clean R1 cycle"** (NOT hub self-assessment -- P0.2):
a PR opened by the actor, **merged by a human**, that is (a) NOT reverted within 7 days,
AND (b) has NO follow-up fix commit touching the same lines within 7 days (the anti-#10
drop-check). A cycle failing (a) or (b) resets the counter for that class.

What this fixes vs the old trigger: it removes the DEADLOCK (R1 is reversible AND
runnable today, so evidence accrues at a reversible rung without ever enabling
auto-merge first). It KEEPS promotion-on-observed-cycles -- which is fine precisely
because R1 is reversible and the "clean" test is mechanical, not my judgment.

## 4. Gate-E and the off-ramp -- SEVERED from the actor (harsh-reviewer P0.3)

The auto-instrument idea from v1 (actor auto-logs coordination events into the SAME
metric that gates Fase 4) was a **self-licking ice cream cone**: the governor would
manufacture the evidence that licenses the governor. KILLED.

Replacement (two separate, non-circular signals):

1. **`auto-observed-signals` log (advisory ONLY).** If the ingestor/classifier detects
   a signal-needing-action, it MAY record it to a clearly-labeled advisory log. This log
   is **explicitly EXCLUDED from every autonomy-promotion gate.** It informs Eduardo; it
   never votes for the actor's own expansion.
2. **`acted-on` count (the real pain signal the actor CANNOT fake).** The honest measure
   of whether the federation needs more governor = **how many surfaced signals Eduardo
   actually ACTS on**. Acting requires a human (merge a PR, fix a drift, make a
   decision) -- the actor cannot manufacture it. This is what gates Fase 2+ and Fase 4.

**Off-ramp decision rule (P1.1) -- pre-committed, lives in `actor-activation-criteria.md`:**
after 4 weeks of Fase-1 R0, proceed to Fase 2 IFF Eduardo acted on >= N surfaced signals
in that window; else reading B was right (pain below threshold) -> STOP at observability,
do not build the classifier/actor. N is Eduardo's to set (proposed default: 3).

## 5. Rollout -- committed vs roadmap (harsh-reviewer P0.4)

| Fase | Deliverable | Status | Max autonomy | Gate before merge |
|------|-------------|--------|--------------|-------------------|
| **0** (doc) | ADR-0036 revision (ratify spine; auto-merge rung -> "Deferred, earn-path defined in activation-criteria, granted by future R2 ADR") + ORCHESTRATION sec 5 rung annotation + `actor-activation-criteria.md` (ladder defs + clean-cycle + off-ramp) | **COMMITTED (this PR)** | none | harsh-reviewer (done: SURVIVE-WITH-CHANGES, adopted) + Eduardo merges |
| **1** (code, TDD) | ingestor adapters + SQLite + read-only consolidated pane + advisory auto-observed log | **COMMITTED (next PR)** | R0 | harsh-reviewer + CI green |
| **2** (code, TDD) | classifier (ladder as code) + R1 actor (open branch+PR / escalate) | **ROADMAP** -- gated by off-ramp (>=N acted-on over 4wk) + own ADR | R1 PR-only | harsh-reviewer + CI |
| **3** (code, TDD) | R2 auto-merge journal/doc-reconcile only, flag default-OFF | **ROADMAP** -- own R2 ADR | R2 gated | harsh-reviewer FALSIFIES increment + >=4 clean R1 cycles + revert proven + different-family judge |
| **4** (code+ops) | cron promote + kill-switch + acted-on gate | **ROADMAP** -- own ADR | scheduled | harsh-reviewer + CI |

Different-family judge note (harsh-reviewer P1.2): the harsh-reviewer is itself Claude
(partial monoculture). True different-family verification = fleet-tools `cross_check`
(Gemini/Groq). The R2 gate REQUIRES `cross_check` wired in, OR drops "different-model
judge" from its mitigation list and relies on reversibility + class-restriction +
drop-check + CI-watchlist. Decided at the R2 ADR.

Every phase: TDD where code; SDMG-gate before any autonomy bump; ADR + commit policy-C
(`Coding-Agent:` + `Trace-Id:` uuidv7, NO `Co-Authored-By`); ASCII-first body;
cross-repo writes = branch+PR only, never direct.

## 6. Fase 0 concrete deliverable (THIS PR -- doc-only, no code)

1. **`docs/adr/0036-*.md` revised**:
   - Status: `Proposed` -> `Accepted` for the SPINE (hub-and-spoke, 5 spokes, routing
     tree, mandatory verification gate, ladder-as-classification). The **auto-merge rung
     -> "Deferred"**: replace the SDMG-incompatible trigger (line 112) with a pointer to
     the earn-path; auto-merge granted only by a future R2 ADR per `actor-activation-criteria.md`.
   - Add "Ratify scope split" section (what is ratified vs deferred + why; cite the
     harsh-reviewer falsification).
   - Add the north-star governor + pointer to this spec.
2. **`ORCHESTRATION.md` sec 5**: annotate the ladder table with R0-R3 rungs + note
   auto-merge is default-OFF until R2 earned; point to the actor + activation-criteria.
3. **`docs/cross-repo/actor-activation-criteria.md` (new)**: rung table (sec 3) +
   mechanical clean-cycle def + the off-ramp decision rule (sec 4) + the advisory-vs-gate
   signal separation. This is the single checklist that decides when any autonomy
   increment is allowed.

No `.claude/settings.json` change (ceiling unchanged until a rung is earned). No actor code.

## 7. SDMG application (Cognitive Protocol 7)

1. DESIGN = hypothesis (declared).
2. TEST = ground-truth reads (sec 1.1). Necessary, not sufficient.
3. FALSIFICATION = harsh-reviewer subagent (done 2026-06-01): verdict
   SURVIVE-WITH-CHANGES; 4 P0 (premise misread, unfalsifiable earn-path, self-licking
   Gate-E, over-scope) + 3 P1. **All adopted in this v2 -- not defended.** Archon
   CALIBRATE: verdict = revise+narrow-scope; confidence HIGH (premise + sever + scope
   corrections rest on directly-read ground-truth + a real logged incident anti-#10);
   falsifying experiment = Fase-1 R0 off-ramp (if Eduardo acts on <N signals in 4wk, the
   build stops -- the design can be proven unnecessary).
4. ANTI-ACCRETION = the base defect (the SDMG-incompatible trigger) is FIXED, not
   accreted around. Pass.
5. NARROW ADOPTION = only Fase 0 + Fase 1 committed; each later rung = minimal flag +
   own ADR. (v1 violated this; v2 fixes it.)
6. TUNING-BEFORE-EXECUTE = the decider for "is the federation under-governed" is the
   `acted-on` count (human ground-truth), NEVER the actor's own classifier (the
   severed self-licking loop). 
7. POST-EXEC VALIDATION = each PR human-reviewed (Eduardo merges); harsh-reviewer per
   autonomy increment.

## 8. Anti-scope

- No heavy orchestration framework (LangGraph/CrewAI/AutoGen) -- ADR-0036 sec 8.
- No LLM gateway/proxy (LiteLLM/Langfuse) -- OD-009.
- No new autonomy in Fase 0/1; no auto-merge before R2 earned via its own ADR.
- No actor-written input to any autonomy-promotion gate (severed -- sec 4).
- No rewrite of islands' self-governance; the governor consumes their signals.
- No direct-to-main cross-repo writes ever (branch+PR only).

## 9. Risks

- **Anti-pattern #10 (bot-rewrite-drop)** -- a REAL logged incident; the reason
  auto-merge is the most dangerous rung and stays roadmap-gated. Mitigations: (a)
  reversibility (revert) -- load-bearing but NOT sufficient: the original #10 drop was
  caught by human suspicion + git-blame 8h later, so detection is the real gap; (b)
  lowest-risk reversible class only at R2; (c) the mechanical drop-check in the
  clean-cycle def; (d) a CI-watchlist (file<->test) so a drop goes CI-red; (e) a
  different-family judge (`cross_check`) at the R2 gate. "harsh-reviewer alone" is NOT a
  sufficient #10 mitigation (same family).
- **Building ahead of need** -- mitigated: Fase 1 is observability-class (today's
  dashboard risk), AND it is the off-ramp experiment that can prove the rest unnecessary.
- **SQLite concurrency (the real risk, not anti-#20)** -- the Flask dashboard (reader) +
  the cron actor (writer) on one SQLite file on Windows; plus any markdown mirror
  consistency. Minimal schema, single-writer discipline, WAL mode; detail in the Fase-1
  plan. (anti-#20 was a cognee/kuzu subprocess-daemon issue -- irrelevant here; removed.)
- **Advisory log mistaken for a gate** -- mitigated by explicit labeling + sec 8
  anti-scope + the gate reading only `acted-on`.

## 10. Testing strategy

- Fase 0: no code -> validation = harsh-reviewer falsification (done) + Eduardo PR review.
- Fasi 1-4: TDD. Ingestor adapters tested against fixture signal files; classifier
  tested as a pure function over fixtures -> expected verdict; actor tested in
  branch-only/dry-run mode. CI green required. Existing
  `apps/cross-repo-dashboard/tests/` extended, not replaced.
