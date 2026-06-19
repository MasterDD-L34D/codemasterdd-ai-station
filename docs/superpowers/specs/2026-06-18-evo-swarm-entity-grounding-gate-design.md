---
title: evo-swarm entity-grounding pre-emit gate -- design
status: proposed
date: 2026-06-18
owner: Eduardo
author: claude-opus-4-8 (hub, supervised)
scope: evo-swarm (Dafne) verification upgrade -- lever 1 of 3
supersedes: none
related:
  - OPEN_DECISIONS OD-022 (swarm canonical validator, Game-side, batch)
  - Game tools/py/swarm_canonical_validator.py (DEPRECATED 2026-05-15)
  - Game scripts/check-canon-consistency.cjs (#2805/#2813, alias-aware)
  - docs/museum/cards/evo-swarm-run-5-discarded-claims.md (labeled corpus)
  - last30days research 2026-06-18 (MARCH info-asymmetry, entity-grounding)
---

# evo-swarm entity-grounding pre-emit gate -- design

## 1. Context and problem

The Dafne evo-swarm generates Game design content (species / traits / biomes /
balance / lore) with a high hallucination rate. Run #5 logged **7/13 claims
hallucinated (54%)** via a single dominant pattern: "take real canonical names and
combine attributes that are NOT supported in canon" (e.g. assert
`dune_stalker.biome_affinity = savana` when canon says otherwise). Ten run-5 items
were discarded at integration time (8 hallucinated + 2 redundant).

The swarm already has the raw material for a fix but does not use it. Per
`camel-agents/orchestrator.py`, every agent response carries a CO-02 v0.3
`canonical_refs` array, declared MANDATORY in the prompt for any claim that touches
a canonical species / biome / trait:

```json
"canonical_refs": [
  {"ref": "data/core/species.yaml#dune_stalker.biome_affinity", "claim": "savana"},
  {"ref": "data/core/traits/glossary.json#impulsi_bioluminescenti", "claim": "exists"}
]
```

The defect: these refs are **self-asserted and never verified before emit**. The
generator declares "this exists / this value is canonical" and nothing checks it.
That is textbook confirmation bias -- the same-context generator vouches for its own
output. The last30days research (2026-06-18) names the fix directly: an independent
ground-truth check (MARCH-style information asymmetry; entity-grounding verification
that cross-references named entities against a knowledge base and fails on an
invented entity).

A Game-side validator exists (`tools/py/swarm_canonical_validator.py`, OD-022) but it
is the wrong tool to reuse as-is: it is **DEPRECATED 2026-05-15** (it reads the legacy
`data/core/species.yaml` SoT, superseded by `data/core/species/species_catalog.json`),
and it runs at distillation / pre-merge time (batch, end-of-run), not pre-emit
per-artifact. The current alias-aware resolver is the Node
`check-canon-consistency.cjs` (#2805/#2813), not the python validator.

## 2. Goal and non-goals

**Goal.** Stop hallucinated artifacts from ever being emitted by the swarm loop, by
verifying each artifact's declared `canonical_refs` against the CURRENT Game canon
SoT before the artifact is written / queued / scored. Make swarm output
integration-ready with low manual review, attacking the 54% hallucination rate at
the source.

**Non-goals (deferred to follow-up specs, explicitly OUT of this spec):**
- Lever 2: asymmetric independent Checker agent via fleet-tools `cross_check`
  (Gemini/Groq, different model family). Follow-up spec.
- Lever 3: constrained schema-output at generation (Ollama `format` schema enforcing
  CO-02). Follow-up spec.
- Full entity-extraction over prose (catching invented entities the agent did NOT
  declare). This MVP verifies declared refs only; the residual (undeclared-in-prose
  inventions) is measured, not yet closed -- lever 3 (mandatory refs) is the planned
  closure.
- Reactivating the swarm. The swarm stays PARKED. This gate is designed to be
  validated OFFLINE on a static corpus; it does not require a swarm run.

## 3. Ratified decisions

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Scope = lever-1 entity-grounding only | Highest-impact lever vs the 54% rate; ship + falsify ONE method before adding (SDMG, experiment-first). |
| D2 | Swarm-local resolver + parity-test (not reuse the deprecated validator, not runtime-shell-out to Node) | Sovereign + decoupled + reads CURRENT SoT; drift-risk vs Game's alias resolution mitigated by a parity-test, not by hard runtime coupling. |
| D3 | Coverage = declared `canonical_refs` only | Lean MVP; reuses the existing mechanism; low false-positive. Undeclared-in-prose residual measured, closed later by lever-3. |
| D4 | On fail = hard-reject pre-emit + per-cycle `hallucination_ratio` to Dafne | Existence/value check is GROUND-TRUTH, not a judgment -- it frees Dafne from mechanical checking and leaves her the quality assessment on what passes. Respects her coordinator role where it matters. |

## 4. Architecture

### 4.1 Locus

The gate fires inside `orchestrator.run_agent()`, AFTER the artifact JSON is produced
and BEFORE it is CO-02-wrapped / written to disk / scored / queued. A rejected
artifact never reaches `artifact_path` write or the scoring path.

### 4.2 Component: `camel-agents/canon_resolver.py` (new, swarm-local)

Single-purpose module. Inputs: a `canonical_refs` list + a canon root (the local Game
checkout). Output: a per-ref verdict list.

- Loads the CURRENT Game canon SoT, read-only:
  - species -> `data/core/species/species_catalog.json` (catalog v0.4.x)
  - traits -> `data/core/traits/index.json` (+ `glossary.json` for existence)
  - biomes -> `data/core/biomes.yaml` (+ its `aliases:` map)
- Parses each `ref` of shape `<file_path>#<entity>.<field>[.<subfield>]`. The
  `file_path` prefix is treated as a HINT only (the agent prompt still points at the
  legacy `species.yaml`); resolution is by `<entity>` + `<field>` against the current
  store, so a legacy-pathed ref still resolves. (The prompt examples are also updated
  to the current SoT -- see 4.4.)
- Resolution is **alias-aware and case-insensitive**, mirroring the Game fix #2813
  (resolve against {ids UNION aliases}, case-insensitive). This is the single most
  important correctness property: without it the gate false-rejects legitimate refs
  (the exact bug #2813 fixed Game-side).
- Per-ref verdict:
  - `VERIFIED` -- entity+field resolves AND the canonical value equals the `claim`
    (for `claim: "exists"`, the entity/trait existing is sufficient).
  - `HALLUCINATED` -- entity/field not found, OR canonical value != claim.
  - `UNRESOLVABLE` -- the ref string cannot be parsed into entity+field.

### 4.3 The gate (in `run_agent`)

For each produced artifact:
1. Resolve all `canonical_refs` via `canon_resolver`.
2. If ANY verdict is `HALLUCINATED` -> **hard-reject**: do not write / queue / score
   the artifact. Append a structured log entry `{artifact_id, agent, failed_refs[],
   reason}` to the run log.
3. `UNRESOLVABLE` is treated as a soft signal in the MVP: it does NOT hard-reject (a
   malformed ref string is a format bug, not a hallucination) but it is logged and
   counted separately, so a spike is visible. (Tightening UNRESOLVABLE -> reject is a
   measured follow-up, not the MVP default, to avoid false-rejects on ref-format
   drift.)
4. Compute, per cycle, `hallucination_ratio = rejected_artifacts / total_artifacts`.
   Surface it to Dafne's run-level assessment and the run report. This re-uses the
   OD-022 gate concept (run-5 ratio was 0.54) but moves it from batch-pre-merge to
   per-cycle, run-level.

### 4.4 Prompt currency fix (small, in-scope)

The CO-02 prompt examples in `orchestrator.py` point `ref` at the legacy
`data/core/species.yaml`. Update the examples to the current SoT
(`data/core/species/species_catalog.json`) so new artifacts declare refs against the
live store. The resolver tolerates both (4.2), so this is a clarity fix, not a hard
dependency.

### 4.5 Data flow

```
agent response JSON
  -> extract canonical_refs[]
  -> canon_resolver(refs, game_canon_root)
       -> [{ref, verdict, canonical_value}]
  -> gate:
       any HALLUCINATED? --yes--> REJECT (log + ratio++), artifact dropped
                          --no---> proceed: CO-02 wrap -> write -> score -> queue
```

## 5. Error handling and edge cases

- **Game checkout missing / SoT file absent** -> the resolver raises a hard config
  error (fail-closed for the run, not fail-open-pass-everything). A gate that cannot
  read canon must NOT silently pass artifacts (L-041 fail-open class).
- **Empty `canonical_refs`** -> pass (no claims to verify). The undeclared-in-prose
  risk is the known residual (non-goal), not this gate's job.
- **Alias collision / ambiguous entity** -> resolve to the alias-target id; if still
  ambiguous, `UNRESOLVABLE` (logged, not rejected) -- never a silent wrong-match.
- **SoT mid-migration (species.yaml being removed)** -> the resolver targets the
  catalog; a legacy-only entity (in species.yaml but not catalog) resolves via the
  catalog loader's compatibility, else `UNRESOLVABLE`.

## 6. SDMG falsification plan (load-bearing)

A self-designed gate is a HYPOTHESIS until externally falsified (ADR-0026 Protocol 7,
SDMG). The gate is NOT trusted -- and the swarm is NOT reactivated -- until this passes.

**6.1 Labeled corpus (already exists).**
- NEGATIVE (must be rejected): the 8 hallucinated items in
  `docs/museum/cards/evo-swarm-run-5-discarded-claims.md`.
- POSITIVE (must pass): the integrated OD-012 artifacts (e.g.
  `magnetic_rift_resonance`, `magnetic_sensitivity`, `rift_attunement`) -- swarm
  output that landed in canon with provenance.

**6.2 Metrics.** Run the resolver+gate over both sets. Require:
- Recall on hallucinations: the gate rejects the 8 negatives (target: all 8).
- Precision: the gate passes the known-good positives (target: zero false-reject).
- Emit a confusion matrix (TP/FP/TN/FN). A miss on either axis blocks the gate.

**6.3 Negative-control (L-041, anti-vacuous-test).** A test that injects a KNOWN-BAD
ref (entity that does not exist) and asserts REJECT, AND injects a KNOWN-GOOD ref and
asserts PASS. This proves the gate is not a pass-everything no-op (the L-041 / BOM /
fail-open failure class).

**6.4 Parity-test vs Game's alias-aware checker (drift catch).** On a shared ref
corpus, assert the swarm resolver's resolve/alias verdicts match Game's
`check-canon-consistency.cjs` (#2805/#2813). This is the mitigation for D2's
duplicate-logic drift risk: if the swarm resolver and the Game checker disagree on
alias/case resolution, the parity-test fails and we reconcile.

**6.5 External falsification (mandatory before trust).** A `harsh-reviewer` subagent
(different-model, anti-monoculture) reviews `canon_resolver.py` + the corpus results
before the gate is wired live. Per SDMG, a falsified finding is adopted, not defended.

## 7. Testing

- Unit: `canon_resolver` resolution (VERIFIED / HALLUCINATED / UNRESOLVABLE) on
  hand-built refs; alias + case-insensitive cases; fail-closed on missing SoT.
- Corpus: the 6.2 precision/recall harness as a repeatable test.
- Negative-control: 6.3.
- Parity: 6.4 (skippable in CI if Node unavailable; runnable on the fleet).
- TDD: tests authored before the resolver/gate per the repo Definition of Done.

## 8. Rollout (parked-safe)

1. Implement `canon_resolver.py` + the gate (behind the existing parked state).
2. Run the SDMG falsification (section 6) OFFLINE on the corpus -- no swarm run.
3. harsh-reviewer external falsification; fix findings.
4. Land via branch + PR on evo-swarm; merge = Eduardo. Record a `DECISIONS_LOG.md`
   entry on ratify.
5. The gate is active for the NEXT swarm run (whenever Eduardo reactivates) -- it does
   not itself trigger reactivation.

Reversibility: the gate is a pre-emit filter; disabling it (env flag) restores prior
behavior. No canon is mutated; the gate is read-only against the SoT.

## 9. Open questions / follow-ups

- Lever 2 (asymmetric checker via cross_check) -- follow-up spec; closes the
  value-judgment gap the existence-check does not cover.
- Lever 3 (constrained schema-output) -- follow-up spec; makes `canonical_refs`
  structurally mandatory, closing the undeclared-in-prose residual.
- UNRESOLVABLE tightening (4.3 step 3) -- measured decision after MVP data.
- Spec home: this design lives in the codemasterdd hub specs; the implementation +
  DECISIONS_LOG entry live in evo-swarm. Confirm whether a codemasterdd ADR is also
  wanted (Eduardo: non-trivial findings -> ADR) once the falsification produces data.

## 10. References

- `camel-agents/orchestrator.py` (CO-02 v0.3 canonical_refs schema + run_agent locus)
- Game `tools/py/swarm_canonical_validator.py` (OD-022, DEPRECATED -- do not reuse)
- Game `scripts/check-canon-consistency.cjs` (#2805/#2813, alias-aware, parity target)
- `docs/museum/cards/evo-swarm-run-5-discarded-claims.md` (labeled corpus)
- last30days research 2026-06-18 (MARCH info-asymmetry; entity-grounding; framework
  not the bottleneck)
- ADR-0026 Protocol 7 (SDMG); L-041 (fail-open / vacuous-test negative control)

## 11. Correction (2026-06-19) -- implementation recon superseded the build premise

Recon during the implementation (writing-plans phase) found that the verifier this
spec proposed to BUILD already exists and is mature: `scripts/verify-swarm-claims.py`
(swarm-local, Tier-1 fuzzy + categories C1-C4, 106 tests). It already does ref
parsing (`parse_canonical_ref`), entity#field value resolution
(`lookup_canonical_value`), per-ref classification (`verify_canonical_ref` ->
verified/contradicted/unverified/malformed_ref), and declared-ref extraction
(`extract_canonical_refs_from_artifact`). The spec's recon (sec 1) found only the
DEPRECATED Game validator + the Node checker and missed this live swarm-side verifier
-- a recon gap.

Consequences for the implementation (evo-swarm PR #124):
- No new `canon_resolver.py` was built. Lever-1 = build-on-existing: a thin gate
  wrapper (`orchestrator.entity_grounding_gate`) wiring the existing verifier
  PRE-SCORE in `swarm_loop._run`, plus one helper (`is_invented_entity`) for the
  pure-invention class.
- Sec 4.1 locus refined: the gate runs in `swarm_loop._run` (reusing the existing
  reject machinery) rather than inside `run_agent`'s write path. The artifact is
  still written to the gitignored `artifacts/` dir for audit but is never
  scored/accepted/queued -- satisfying the "pre-emit" intent (never enters the
  candidate pool).
- Sec 5 error-handling refined: fail-OPEN-but-loud on empty/unavailable canon, NOT
  fail-closed. The spec's fail-closed suited a CI gate; a live-loop gate that
  rejects-all on a transient/partial canon load would halt the swarm. Empty/None
  canon -> loud-skip + pass; the merge-gate `--strict` verify remains the backstop.
- SDMG (sec 6): 2 harsh-review rounds. Round 1 falsified the first cut (caught only
  'contradicted', missed pure-invention = 4/8 of the run-5 corpus) -> added
  `is_invented_entity`. Round 2 SHIP-IT (OD-012 known-good trio not false-rejected
  vs real canon). The run-5 corpus is exercised via targeted tests, not a separate
  harness (the existing 106 + new tests already cover the patterns).
- Follow-up (P2, latent, not triggered today): a trait authored in
  `active_effects.yaml`/`index.json` but not back-filled into `glossary.json` would
  false-reject; union the trait sources or add a CI invariant.

Lesson: build-on-existing recon must grep the TARGET repo's `scripts/`, not only the
cross-repo deps -- the spec premise "build a resolver" was a recon gap, caught before
any code by the writing-plans recon. See [[feedback_recon_before_build]].
