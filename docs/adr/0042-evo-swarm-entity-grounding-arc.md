# ADR-0042 -- evo-swarm entity-grounding verification arc: 3-lever outcome + load-bearing lessons

- Status: Proposed (Eduardo ratifies)
- Date: 2026-06-20
- Deciders: Eduardo (hub: Claude Code / Opus 4.8, supervised)
- Related: spec 2026-06-18 (lever-1 entity-grounding gate), spec 2026-06-20 (lever-2 redundancy
  checker, REJECTED), spec 2026-06-20 (lever-3 constrained canonical_refs); ADR-0026 (SDMG
  Protocol 7); ADR-0036 (fleet-tools cross_check); evo-swarm OD-007, DECISIONS_LOG 012;
  lessons L-2026-05-033/034/035, L-2026-06-041.

## TL;DR

The Dafne evo-swarm generated Game design content with a ~54% hallucination rate (run #5). A
3-lever verification upgrade was planned. Outcome after a supervised design+build+falsify pass:
**lever-1 (entity-grounding gate) ADOPTED + landed; lever-2 (asymmetric redundancy checker)
REJECTED by SDMG falsification and archived as a learning-record; lever-3 (constrained
canonical_refs output) ADOPTED + landed, but only after the empirical A/B showed that constrained
output earns its keep ONLY when a ref-shape `pattern` is added to the schema.** Two of the three
self-designed levers were materially wrong as first specced; the SDMG falsification protocol
(ADR-0026) caught both before they shipped. Swarm stays PARKED; the gates are validated offline
and active for the next run, which they do not themselves trigger.

## Context

evo-swarm agents (Ollama-local, qwen3-coder:30b) emit Game design artifacts. Run #5 logged 7/13
claims hallucinated (54%), dominant pattern "hallucinate-by-association" (real canonical names +
unsupported attributes). The CO-02 v0.3 `canonical_refs` mechanism existed but was self-asserted
and never verified pre-emit. The 3-lever plan: L1 verify declared refs exist/match (ground-truth
existence); L2 catch the residual value/redundancy judgments existence cannot (asymmetric,
different-model-family judge); L3 make refs structurally mandatory at generation (constrained
schema-output). Each lever = a self-designed method, i.e. a hypothesis until externally falsified
(ADR-0026 Protocol 7, SDMG).

## Decision

| Lever | Decision | Where |
|-------|----------|-------|
| **L1 -- entity-grounding pre-emit gate** | ADOPTED + landed | evo-swarm #124/#125/#126, ratify #127. Build-on-existing: reused the mature `scripts/verify-swarm-claims.py` (the spec premise "build a resolver" was a recon gap -- the verifier already existed). Wired in `swarm_loop._run` pre-score; fail-open-but-loud. |
| **L2 -- asymmetric redundancy checker** | REJECTED (SDMG) -> archived learning-record | spec PR #400 (merged as record, status rejected-pending-rework). SDMG panel returned REJECT on 10 code-verified P1s. The real residual is STRUCTURAL schema-redundancy (a lever-1 extension), not a cloud-LLM-judge lever; the run-5 corpus was N=1; `cross_check` is MCP-only and unreachable from the detached swarm; the score formula it cited did not exist. Not built. |
| **L3 -- constrained canonical_refs output** | ADOPTED + landed (with ref pattern) | spec PR #402; impl evo-swarm #129 (merged). Ollama `format` JSON-schema on the live `swarm_loop._run` path. |
| **OD-007 -- biome SoT** | RESOLVED (correctness fix) | evo-swarm #128 (+ ec641c5). A loader bug (read the `biome_aliases.yaml` wrapper key, missed the 16 nested aliases + a phantom `aliases` sentinel), NOT a wrong-file. `data/core/biomes.yaml` is the authoring SoT; `packs/...` is derived via `sync:evo-pack`. |

## Load-bearing lessons

1. **SDMG works -- it caught two wrong designs before ship.** Lever-2 was REJECTED (the method
   targeted the wrong problem on a corpus that could not validate it). Lever-3's first spec was
   FIX-THEN-SHIP: the falsification found the wrong locus (`run_agent` is not the live path;
   `swarm_loop._run` is), a schema that would drop 8 consumer fields (Ollama `format` drops
   undeclared keys), and an unmeasurable quality gate. A self-designed method is a hypothesis
   until externally falsified; here, 2/3 levers needed correction or rejection. Trust-and-ship
   would have shipped two broken designs.

2. **Recon output is a hypothesis too.** A cross-repo recon workflow confidently asserted
   "packs/ is the primary biome SoT"; ground-truth (the `biome_aliases.yaml` header, the
   `sync:evo-pack` direction, the biome manifest) showed the opposite (data/core is authoring).
   Sub-agent / workflow conclusions about authority/SoT must be verified against primary source
   before being built on -- the same discipline as recon-before-build, extended to agent output.

3. **format without a pattern is ~zero value.** A/B N=40 on qwen3-coder:30b: constrained
   `format` added ~0 well-formed-ref rate over prompt-asking (delta -0.03), and ~22% of refs
   were malformed in BOTH arms -- because the schema required `ref: string` with no shape
   constraint, so lever-1 could not even parse those refs. Adding a JSON-schema `pattern`
   (`<path>#<entity>.<field>`, grammar-enforced) flipped it: re-A/B showed ON 96/96 refs
   well-formed (100%) vs OFF 69/97 (71%), +29 percentage points of lever-1-verifiable refs. The
   grammar-enforced pattern is the ONE thing a prompt cannot guarantee -- that is where
   constrained output earns its keep. The prompt-fix (declaring canonical_refs at all) is what
   moved emission 0 -> ~1.00; `format` is the structural guarantee on top.

4. **Measure, do not assume.** Every above correction came from empirical evidence (the A/B, the
   field-dump, the loader dump), not from the design's own claims. The 54%->gate value, the
   format-needs-pattern finding, and the OD-007 root-cause were all measured, not asserted.
   N-sample held throughout: N<=10 = direction-probe, N>=40 = ratify.

5. **Build-on-existing pays, recon-gaps cost.** L1 reused an existing verifier (the spec's
   "build a resolver" was a recon gap caught in writing-plans). L3 reused `call_ollama` + the
   live `_JSON_SCHEMA`. The one shadow-duplicate risk (a pre-existing `dafne_similarity` engine)
   was caught by the agent-scanner before lever-2 code was written.

## Consequences

- **Active gates**: L1 (existence) + L3 (structural ref-shape, 100% well-formed -> all refs
  verifiable). Together they attack the 54% rate at emit-time (L3) and pre-score (L1). Both
  fail-open-but-loud; reversible via env-flag / `response_format=None`.
- **Not built**: L2. The value-judgment residual (semantic redundancy) is deferred; if pursued,
  it is a structural lever-1 extension, not a cloud-judge -- and needs a real labeled corpus
  first (the 223 historical artifacts are all rejected -> no good-positive baseline).
- **Swarm stays PARKED**: gates validated offline; they do not trigger reactivation (Eduardo's
  call). Active for the next run whenever it happens.
- **Residuals**: quality-of-prose has no labeled baseline -> not gated (advisory only). Undeclared-
  in-prose inventions remain a measured, unclosed residual.

## References

- evo-swarm: scripts/verify-swarm-claims.py (L1 + OD-007), camel-agents/swarm_loop.py (L3
  CANONICAL_REFS_SCHEMA + _generate_constrained), orchestrator.py (call_ollama response_format),
  scripts/ab-lever3-canonical-refs.py (A/B harness), DECISIONS_LOG 012, OPEN_DECISIONS OD-007.
- PRs: #124/#125/#126/#127 (L1 + ratify), #128 (OD-007), #129 (L3); codemasterdd #400 (L2 spec
  rejected), #402 (L3 spec).
- specs: docs/superpowers/specs/2026-06-18-evo-swarm-entity-grounding-gate-design.md;
  2026-06-20-evo-swarm-asymmetric-redundancy-checker-lever2-design.md (rejected);
  2026-06-20-evo-swarm-lever3-constrained-canonical-refs-design.md.
- protocol: ADR-0026 (SDMG Protocol 7); lessons L-2026-05-033 (SDMG), L-034 (circular-validation),
  L-035 (currency gate), L-2026-06-041 (negative control).
