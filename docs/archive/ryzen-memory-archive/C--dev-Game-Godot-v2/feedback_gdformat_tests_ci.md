---
name: feedback-gdformat-tests-ci
description: "Godot v2 CI \"gdformat lint\" check covers tests/unit/*.gd too; gdlint-clean does NOT imply gdformat-clean. Always gdformat BOTH script + test files before commit."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6b508d26-ce2f-4ad4-a74d-82a0d64f6470
---

Run `gdformat` on BOTH the script AND its test file before committing GDScript in Game-Godot-v2 — not just the script.

**Why:** The repo CI job `gdformat lint` (`.github/workflows/test.yml`) runs `gdformat --check` across the whole tree including `tests/unit/*.gd`. `gdlint` passing does NOT imply `gdformat --check` passing — they are different tools (lint = style rules, format = canonical layout). 2026-05-21 M2 PR #339: subagent ran `gdformat scripts/data/encounter_definition.gd` but NOT the test file; `gdlint` was clean so it looked done, but CI `gdformat lint` failed on `tests/unit/test_encounter_definition_conditions.gd` (gdformat wanted to wrap a long `EncounterDefinition.from_dict({...})` call + nested dict). Cost one CI round + a fix commit.

**How to apply:** in any task that creates/edits a `.gd` test file, run `gdformat <script> <test>` (both) then `gdlint <script> <test>` (both) as the pre-commit gate. When briefing implementer subagents for GDScript work, state explicitly: "gdformat AND gdlint must pass on BOTH the script and the test file." GUT tests passing + gdlint clean is insufficient — gdformat-check is the third independent gate. Related: [[feedback-loc-sum-check]] (other pre-merge CI gate discipline).
