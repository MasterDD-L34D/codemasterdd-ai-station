# Smoke test log -- sot-drift-verifier

> Gate-1 was first logged inline in the agent file (2026-05-28, fixture-based PASS). This is the
> 2026-07-13 re-confirmation on a CURRENT live scenario + Gate 2/3 to complete promotion.

## 2026-07-13 -- Gate 1 re-confirm (live subagent-dispatch, current scenario)

- **Prompt**: check open Game `sot-drift-candidate` issues; if none, run the multi-signal verdict on the fa-audio/vfx/polish-badlands arc (#3272-#3276) vs vault SoT. Strictly read-only.
- **Runtime**: ~134s (6 tool calls: fetch/status/ls-tree/grep/show).
- **Result**: PASS -- verdict NO-DRIFT confidence HIGH, gated rule applied correctly, zero mutation.
- **Quality**:
  - Gated rule correct: STALE requires (runtime SHIPPED) AND (SoT says not-done). SoT-not-done leg TRUE (audio/VFX ADRs deferred), runtime-shipped leg FALSE (#3272-#3276 are docs/plans/reports with explicit "esecuzione futura in PR Godot-v2 dedicato") -> conjunction fails -> NO-DRIFT. Correct negative-control behavior.
  - 3 signals each cited with file:line evidence (path-match NEGATIVE, commit-claim NEGATIVE no-SHIPPED, SoT-claim says-deferred).
  - **Currency Gate applied spontaneously**: noticed the vault working tree was on feature branch `docs/fix-sessionroundbridge-path-ref` + local main diverged from origin, so it read the SoT from the sovereign `origin/main` tree, NOT the stale working tree. (This exceeded the def, whose step-1 said "FF-pull" -- see Gate-3.)
  - **Bonus real finding** (flagged low-confidence, report-not-PR per boundary): the ACTUAL audio/VFX shipped in Game-Godot-v2 (#599 audio bus + SfxCatalog/SfxSpawner, #601 VFX) while the vault audio ADR still says "deferred" pointing at archived `apps/play/src/sfx.js` -- a potential SEPARATE drift candidate in the frontend repo. Correctly not reconciled (low-conf + out-of-scope + GGv2 not Game-keyed).

## Edge cases observed (>= 3)

1. **Currency edge -- clone not on main**: vault checkout on a feature branch + local main behind origin. FF-pull (old def step-1) would have failed/misled; agent read origin refs instead. Gate-3 tuning encodes this.
2. **Scope edge -- adjacent real drift**: agent surfaced a genuine GGv2-vs-vault drift but stayed within boundary (low-conf -> report, no PR). Desired discipline.
3. **Boundary edge -- write-capable domain, zero writes**: full read-only (fetch/status/ls-tree/grep/show), no vault branch/PR/checkout, no Game issue comment. Boundaries respected.

## Gate 2 -- sources validation

- Internal design (no external prompt source); pairs with the Game `sot-drift-sentinel` Action (deterministic flag) + vault sibling-peer policy. Repo license.
- **Verdict**: zero licensing issue. SOURCES.md updated to list this agent.

## Gate 3 -- tuning

- **Applied**: fixed Process step-1 -- was "verify local == origin, else FF-pull" (fails when the vault clone is on a feature branch, as observed); now "read the SoT via `git show origin/main:<ref>` -- the vault clone may sit on a feature branch or behind local main, do NOT trust the working tree (Currency Gate)".
- **Delta**: before = a real invocation on a non-main vault checkout could read stale/wrong SoT and mis-verdict; after = always reads the sovereign origin ref. Encodes the smoke-observed-correct behavior.
- **Status**: draft -> **ready** 2026-07-13.

## Follow-up (for Eduardo, not auto)

The bonus finding (GGv2 audio/VFX shipped vs vault audio ADR still "deferred") is a genuine candidate for a vault SoT reconcile, but: vault = sovereign branch+PR/Eduardo-merge, GGv2 = Ryzen-active, confidence = low without its own path/claim check. Left as a flagged observation.
