# Dossier -- evo-swarm entity-grounding verification arc (2026-06-20)

> Cross-repo knowledge pack. Single entry-point reconstructing the full arc: what we built, what
> we falsified, what we kept, and the reusable lessons. Authoritative decision = ADR-0042; this
> dossier is the navigable end-to-end record + the distilled lessons.

- Date: 2026-06-20 (single supervised session)
- Author: claude-opus-4-8 (hub, supervised by Eduardo)
- Repos touched: evo-swarm (Dafne) = impl; codemasterdd = specs/ADR/this dossier; Game = canon SoT (read-only).
- Capstone decision: ADR-0042. Project decisions: evo-swarm DECISIONS_LOG 012 (lever-1) + 013 (archive/linter).

## 0. TL;DR

A 3-lever verification upgrade for the evo-swarm (which generated Game design content with a ~54%
hallucination rate, integration ~0%). Outcome:
- **L1 entity-grounding gate** -- ADOPTED + landed.
- **L2 asymmetric redundancy checker** -- REJECTED by SDMG falsification; archived as learning-record.
- **L3 constrained canonical_refs output** -- ADOPTED + landed, but only earned its keep after a
  grammar-enforced ref `pattern` was added (format alone added ~0 on the production model).
- **OD-007** -- a biome-alias loader bug, fixed.
- **Production verdict**: a falsifiable probe through the new gates FALSIFIED "use the swarm to
  accelerate Game production" (91.7% hallucination, 1 survivor / 12). The autonomous GENERATOR is
  retired; the VERIFIER (`verify-swarm-claims.py`, 153 tests) is promoted to a standalone
  entity-grounding linter -- the real reusable value of 6 weeks.

Two of three self-designed levers were materially wrong as first specced; the SDMG protocol caught
both before they shipped. "Shipped != solves": the levers raised the floor (output integrity), not
the ceiling (generation usefulness).

## 1. Chronology (end-to-end, with numbers + decisions)

### 1.1 Starting state
- evo-swarm: autonomous multi-agent loop, Ollama-local qwen3-coder:30b, generating Game design
  content. Run #5 = 54% hallucination (7/13), net-actionable ZERO. ~223 artifacts produced, only
  2 traits ever integrated to Game canon (echo_backstab, magnetic_rift_resonance) -- both BEFORE
  the hallucination era. Atto-2 score 1/10. Swarm PARKED.
- Plan: 3-lever verification upgrade (spec codemasterdd 2026-06-18, "lever 1 of 3").

### 1.2 Lever-1 -- entity-grounding pre-emit gate (DONE, merged)
- PRs #124/#125/#126; ratify #127 (DECISIONS_LOG 012).
- Build-on-existing: the verifier the spec proposed to BUILD (`canon_resolver.py`) already existed
  as `scripts/verify-swarm-claims.py` (mature, Tier-1 fuzzy, 106 tests). A writing-plans recon
  caught this -- a recon gap in the spec (sec 11 correction). No new resolver built; a thin gate
  wrapper wired the existing verifier PRE-SCORE in `swarm_loop._run`.
- SDMG: 2 harsh-review rounds. Round 1 falsified the first cut (caught only `contradicted`, missed
  pure-invention = 4/8 of the run-5 corpus) -> added `is_invented_entity`. Round 2 SHIP-IT.
- #125 unioned trait ids across glossary/active_effects/index; #126 resolved trait field-values.

### 1.3 OD-007 -- biome-SoT divergence (RESOLVED, merged)
- Surfaced doing the lever-1 parity check (spec sec 6.4): the swarm loader and Game's
  `check-canon-consistency.cjs` read DIFFERENT biome files. Recon first claimed "packs is primary
  SoT"; GROUND-TRUTH (the `biome_aliases.yaml` header "must resolve to a key in data/core/biomes.yaml"
  + the `sync:evo-pack` direction data/core -> packs + the biome manifest) showed the OPPOSITE:
  `data/core/biomes.yaml` is the authoring SoT, packs/ is derived.
- The real defect was a LOADER BUG: `load_canonical_index` iterated the top-level of
  `biome_aliases.yaml` (schema `{aliases: {...}}`) -> harvested only the wrapper key 'aliases' (a
  phantom sentinel) and MISSED the 16 real aliases -> false-rejected savanna/deserto_caldo/
  caverna_risonante/sinaptic_trench (the #2813 alias class). Fix = read the nested map (#128).
- Codex bot P2 caught a sequel: alias forms now resolved (is_invented) but the VALUE-compare path
  still marked savanna != savana as `contradicted`. Fixed by canonicalizing biome aliases before
  compare (a follow-up commit + ec641c5).

### 1.4 Lever-2 -- asymmetric redundancy checker (REJECTED, archived)
- Spec PR #400 (codemasterdd). Brainstormed scope (semantic redundancy, the run-5 reinvent-wheel
  residual), recon (cross-repo + last30days), wrote the spec.
- SDMG falsification panel (3 lenses, code-verified) -> REJECT, 10 P1s:
  - Wrong target axis (the run-5 #8/#9/#10 are STRUCTURAL biome-schema redundancy, not species
    I/E/L embedding); the corpus is N=1; the canonical loader harvests only ids (nothing to
    retrieve); artifacts are unstructured prose (no axes to extract).
  - `cross_check` (the proposed different-family judge) is an MCP tool, UNREACHABLE from the
    detached Python swarm. The R2 "key at-call" safety claim was false. The cited score formula
    did not exist.
- Per SDMG, adopted not defended. Lever-2 NOT built; spec merged as a learning-record
  (status rejected-pending-rework). The real residual is a structural lever-1 extension, not a
  cloud-LLM-judge -- and needs a real labeled corpus first.

### 1.5 Lever-3 -- constrained canonical_refs output (DONE, merged + ratified)
- Spec PR #402. Recon found the LIVE loop (`swarm_loop._run`, not `run_agent`) uses its own
  `_JSON_SCHEMA` that NEVER declared canonical_refs -> lever-1 was largely inert on the live path.
- SDMG -> FIX-THEN-SHIP (core premise survived empirically: format raises emission on 30b). 4 P1s
  adopted: locus = swarm_loop._run (not run_agent); schema must declare ALL live fields (Ollama
  `format` drops undeclared keys -> data-loss on handoff/Aider/scoring); quality-arm downgraded to
  advisory probe (no labeled baseline -- same flaw that rejected lever-2); symmetric kill-criterion.
- Two more codex P2s (A/B must hit the live `_run` path; split the HTTP-400 vs JSON-invalid
  fallback by call-site) + one (`security_alert` must be declared or format drops it) -- all fixed.
- Impl #129: `call_ollama(response_format=...)` + D5a HTTP-400 fallback; `CANONICAL_REFS_SCHEMA`
  (13 live fields + canonical_refs + security_alert, required = all consumed keys, nullable
  optional-value); `_generate_constrained` with D5b parse-site fallback.
- **A/B N=40 (qwen3-coder:30b)**: format alone added ~0 well-formed-ref rate vs prompt-asking
  (delta -0.03) and ~22% of refs were MALFORMED in BOTH arms (schema required ref:string, no
  shape). Adding a JSON-schema `pattern` (`<path>#<entity>.<field>`, grammar-enforced) flipped it:
  re-A/B ON 96/96 refs well-formed (100%) vs OFF 69/97 (71%), +29pt verifiable refs, zero
  schema-rejects. Ratified. Merged.

### 1.6 ADR-0042 capstone (merged)
- PR #404. Records the per-lever outcome + the load-bearing lessons. Codex P2 (add to the
  DECISIONS_LOG ADR index) fixed. Merged.

### 1.7 Production verdict -- assessment + probe (archive decision)
- Eduardo asked: "use the swarm to accelerate Game production -- still the plan?"
- 5-agent grounded assessment: integration ~0.4-0.9%; both integrations pre-hallucination-era;
  Atto-2 missed its own written criterion; Game ships 505 commits/30d WITHOUT the swarm (bottleneck
  = data-consistency/integration, NOT content volume); qwen3-coder:30b unfit for design-synthesis;
  gates are filters (REJECT not FIX) -> raising the floor doesn't raise the ceiling.
- **Falsifiable probe** (1 run through L1/L3, Aider disabled = no Game-touch): 12 specialist
  artifacts -> 11 L1-rejected (91.7% hallucination, WORSE than run-5's 54%), 1 survivor. The
  kill-criterion (<2 net-actionable / 30) met with margin. Mechanism: lever-3 forces canonical_refs
  declaration -> the model INVENTS them -> L1 exposes the true (previously masked) hallucination
  rate.
- Decision (DECISIONS_LOG 013, PR #130): RETIRE the autonomous generator (parked, runtime 0);
  PROMOTE `verify-swarm-claims.py` (153 tests) to a standalone entity-grounding linter.

## 2. Final state

- **On main (evo-swarm)**: L1 gate, OD-007 fix, L3 constrained output (all reversible: env-flag /
  `response_format=None`). The autonomous generator is PARKED (runtime 0).
- **Retired**: swarm-as-production-accelerator (falsified, not opinion).
- **Saved/promoted**: `verify-swarm-claims.py` = entity-grounding linter (`scripts/verify-swarm-claims-LINTER.md`).
- **Not built**: lever-2.
- **Game**: untouched throughout. Continues its own production cadence.

## 3. Distilled lessons (load-bearing, reusable across projects)

1. **SDMG works -- it caught 2/3 self-designed levers as materially wrong before ship.** A
   self-designed method is a hypothesis until externally falsified. Lever-2 REJECTED; lever-3 first
   spec had the wrong locus + a data-loss schema. Trust-and-ship would have shipped both broken.
2. **Recon output is a hypothesis too.** The cross-repo recon's "packs is primary SoT" was false vs
   ground-truth (data/core authoring). Verify sub-agent/workflow claims about authority/SoT against
   PRIMARY source (the file's own header, the sync script, the manifest) before building on them.
3. **Constrained-output (Ollama `format`) without a grammar-enforced ref pattern is ~zero value.**
   On a capable model, prompt-asking already gets the field; `format` only earns its keep via a
   `pattern` the grammar enforces (shape a prompt cannot guarantee). Measured: with-pattern ON 100%
   vs OFF 71% well-formed refs; without-pattern delta ~0.
4. **Verification != generation. Raising the floor does not raise the ceiling.** Gates are filters
   (REJECT not FIX). A pipeline whose offensive value (net-actionable design) measured ZERO is not
   rescued by stricter filters -- it stays ~0, just cleaner.
5. **Measure, do not assume.** Every correction came from empirical evidence (the A/B, the
   field-dump, the loader dump, the probe), not the design's own claims. N-sample held: N<=10
   probe, N>=40 ratify.
6. **Build-on-existing pays; recon-gaps cost.** L1 reused an existing verifier (the spec's "build a
   resolver" was a recon gap). The one shadow-duplicate risk (a pre-existing similarity engine) was
   caught by agent-scanner before lever-2 code was written.

Operational notes worth keeping: commit-msg hook requires a lowercase description after the type;
heredoc commit bodies with backticks need `<<'EOF'` (quoted) to avoid command-substitution
mangling; detached long runs survive session interruptions via PowerShell `Start-Process` (a plain
background bash dies on resume); the headless probe coordinator runs slow on Ollama-30b (no
Dafne-active-Groq) and hits the 120s timeout -- a probe-config artifact, not a swarm bug.

## 4. Reusable assets

| Asset | What | Where |
|-------|------|-------|
| `verify-swarm-claims.py` | entity-grounding linter (claims vs Game canon), 153 tests, CLI `--strict`/`--json` | evo-swarm scripts/ (doc: verify-swarm-claims-LINTER.md) |
| L1 `entity_grounding_gate` | pre-score reject of contradicted/invented refs | evo-swarm orchestrator.py / swarm_loop.py |
| L3 `CANONICAL_REFS_SCHEMA` + `_generate_constrained` | constrained output + ref pattern + fallbacks | evo-swarm swarm_loop.py |
| A/B harness | well-formed-ref rate, live `_run` path, ON vs OFF | evo-swarm scripts/ab-lever3-canonical-refs.py |
| Probe harness | bounded gated run + counters, Aider-disabled | evo-swarm scripts/probe-30cycle-gated.py |

## 5. Cross-repo pointers

- codemasterdd: ADR-0042 (capstone), specs 2026-06-18 (L1), 2026-06-20 (L2 rejected), 2026-06-20
  (L3), this dossier.
- evo-swarm: DECISIONS_LOG 012 (L1) + 013 (archive/linter); OPEN_DECISIONS OD-007; PRs
  #124/#125/#126/#127 (L1), #128 (OD-007), #129 (L3), #130 (archive/linter); #400/#402/#404 cross.
- Game: canon SoT (data/core/* authoring; packs/ derived via sync:evo-pack). check-canon-consistency.cjs
  (internal consistency) is complementary, not duplicated by the linter.
- AA01 / protocol: ADR-0026 (SDMG Protocol 7); lessons L-2026-05-033/034/035, L-2026-06-041.

## 6. Open follow-up (the dedicated chip)

**Game-CI linter integration** (cross-repo, Game): wire `verify-swarm-claims.py --strict` into the
Game repo CI so docs/PRs that cite canonical entities are linted for canon-grounding before merge
(catches hallucinate-by-association regardless of author -- human or AI). This is the agreed
continuation; it runs as a dedicated chip on Eduardo's go.

## 7. Resolution -- linter integrated + generator RETIRE reconfirmed (2026-06-21)

The Sec 6 follow-up SHIPPED. The linter is vendored into Game CI: PR #2915 (squash `4ce1d0cb`)
added `scripts/verify-swarm-claims.py` + a markdown adapter (lint design-doc/PR prose, not only
JSON artifacts) + `contradicted`-gating (the real hallucinate-by-association bucket, which the
bare upstream exit-code missed) + retired the deprecated `tools/py/swarm_canonical_validator.py`;
PR #2926 (`66e76e42`) fixed a markdown heading-bigram false-positive; PR #2920 recorded it in the
Game reference docs. Two CI tiers (JSON `--strict` hard-fail on `docs/research/swarm/**.json`;
markdown advisory on `docs/research/**/*.md`); 169 tests run in Game `python-tests`. Codex was
rate-limited throughout, so a compensating harsh self-review caught + fixed 2 P1 false-greens.

Before archiving evo-swarm, the revive-vs-retire question was RE-LITIGATED with fresh evidence
(Eduardo's call), since stronger open-weight models had shipped:
- **last30days**: Qwen3 Coder Next / GLM-5.2 / MiniMax M3 shipped, but the 2026 consensus is
  ground -> judge -> gate (= the linter) and hallucination is inherent to autoregressive LLMs.
- **deep-research** (adversarially verified, ~10M tokens over 2 runs; the 1st was rate-limited and
  resumed after editing the workflow to serialize verification + make verifiers throttle-resilient):
  the standing thesis HOLDS (verification != generation); MULTI-agent is the WRONG lever (MAD does
  not beat single-agent CoT, replicated by 2026 compute-matched studies); model-swap + RAG is NOT
  the lever (RAG lifts factual recall, not creative usefulness); the ONLY regime that rescues
  self-correction is an external sound verifier + narrow scope + cheap re-rolls.
- **Narrow probe** (the only evidence-defensible revive shape) built + run:
  `evo-swarm scripts/probe-narrow-single-agent.py` (branch merged to main, Decisione 014) --
  single-agent + narrow constrained-recombination (pick ONE existing canon trait per species) +
  the canon linter as the external sound gate + 3 re-rolls + the CURRENT model qwen3.6 + same
  net-actionable kill-criterion, N=15. **RESULT: 0/15 clean, net-actionable upper-bound = 0 ->
  RETIRE-CONFIRMED.** Dominant failure `invented_trait` = 35/39 successful attempts (the current
  model invents non-canon traits despite an explicit pick-existing instruction + the species'
  canon record in-context); 6 timeouts were a run artifact (qwen3.6 23GB heavy-offload), not signal.

**Verdict: triple-confirmed RETIRE** (the dossier prior + external literature + a fresh local probe
that measured the exact previously-unmeasured configuration -> 0). evo-swarm is archived read-only
(reversible via `gh repo unarchive`). The autonomous generator is dead as a production hypothesis;
the canon entity-grounding linter is the durable value of the arc. The narrow probe is reusable +
falsifiable (kill < 2) for any future re-litigation with stronger models. Capstone remains ADR-0042.
