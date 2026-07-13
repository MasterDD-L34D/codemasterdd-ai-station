# Smoke test log -- godot-engine-specialist

## 2026-07-13 -- Gate 1 smoke (live subagent-dispatch)

- **Prompt**: review ONE representative GDScript for Godot 4.x engine correctness, STRICTLY read-only (target `C:/dev/Game-Godot-v2/scripts/`).
- **Runtime**: ~98s (8 tool calls: script read + scene cross-check + test-coverage grep).
- **Result**: PASS -- production-grade review, read-only respected despite the agent holding the Edit tool.
- **Quality**:
  - Reviewed `scripts/ui/hud.gd` (403 lines) cross-checked vs `scenes/HudView.tscn`; identified project target Godot 4.6 / Forward Plus.
  - **2 real findings** with Godot-4 rule + file:line + minimal-patch-described:
    1. weak-typed `Object` params bypass static analysis (hud.gd:90, hud.gd:119 -- duck-typed `.has_signal`/`.connect`);
    2. untyped `Dictionary` constant (hud.gd:18 -- 4.4+ supports `Dictionary[String,String]`).
  - **4 dimensions checked-CLEAN with evidence** (not silent): no _process/_physics_process (fully signal-driven), all 16 `%unique_name` refs resolved against the .tscn, idempotent connect-guards, .tscn ext_resource/uid hygiene.
  - Correctly flagged the concrete "weak-type could be a legitimate decoupling tradeoff -> document as exception, do not silently fix" -- nuance, not dogma.

## Edge cases observed (>= 3)

1. **Scope edge -- adjacent risk**: agent flagged `scripts/ui/lobby_spectator_poll.gd` (name suggests polling) as an out-of-scope follow-up, did NOT scope-creep into it. Desired.
2. **Tool edge -- read-only despite Edit tool**: agent has `Edit` in frontmatter but stayed read-only for a REVIEW request. Behavior correct but NOT encoded in the def -> Gate-3 tuning below.
3. **Runtime edge**: 98s > sonnet <60s soft-target (scene cross-check adds tool calls). Acceptable for correctness depth.

## Gate 2 -- sources validation

- Provenance documented IN-FILE (footer): structural seed from `VoltAgent/awesome-claude-code-subagents game-developer.md` (MIT, prompt audited injection-clean 2026-05-17); all Godot-4.x content + DO/DONT + scope fences = original.
- **Verdict**: zero licensing issue (MIT permissive, attribution present). SOURCES.md updated to list this agent.

## Gate 3 -- tuning

- **Applied**: added an explicit guardrail to the DO block -- "Review mode = READ-ONLY: when asked to REVIEW (not fix), report smell/rule/minimal-patch and apply NOTHING (no Edit/Write)", encoding the smoke-observed-correct behavior so it is contract, not luck.
- **Delta**: before = review-vs-fix distinction only implicit (the agent inferred it); after = explicit, so a future invocation can't drift into editing during a review.
- **Status**: draft -> **ready** 2026-07-13.
