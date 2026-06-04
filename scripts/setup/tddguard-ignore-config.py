#!/usr/bin/env python3
"""Idempotent setup: tdd-guard ignorePatterns so cross-repo edits are NOT false-blocked.

tdd-guard (PreToolUse hook) validates Edit/Write against the CURRENT project's test
state. Editing a sibling fleet repo (Game / Game-Database / Game-Godot-v2 / ...) from a
codemasterdd session makes it read the wrong reporter -> false-block of legit cross-repo
work (memory feedback_tddguard_cross_repo_blindspot). Fix: ignore sibling-repo paths via
ignorePatterns (minimatch matches both forward-slash and backslash separators; in-project
paths stay guarded).

.claude/tdd-guard/data/config.json is gitignored (local) -> run this once per machine
(Ryzen + Lenovo). Reversible: delete config.json (or remove ignorePatterns) -> defaults.
Preserves an existing guardEnabled toggle (scoped guard-off stays intact).
Run: python scripts/setup/tddguard-ignore-config.py
"""
import json, os

# tdd-guard DEFAULT_IGNORE_PATTERNS (config.ignorePatterns OVERRIDES defaults -> include them).
DEFAULTS = ["*.md", "*.txt", "*.log", "*.json", "*.yml", "*.yaml",
            "*.xml", "*.html", "*.css", "*.erb", "*.rst"]
# Sibling fleet repos to exempt (this project = codemasterdd-ai-station, stays guarded).
SIBLINGS = ["**/Game/**", "**/Game-Godot-v2/**", "**/Game-Database/**",
            "**/synesthesia/**", "**/vault/**", "**/Dafne/**"]

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(root, ".claude", "tdd-guard", "data", "config.json")
os.makedirs(os.path.dirname(path), exist_ok=True)

cfg = {}
if os.path.exists(path):
    try:
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
    except (ValueError, OSError):
        cfg = {}

cfg["ignorePatterns"] = DEFAULTS + SIBLINGS  # idempotent: same result each run
# guardEnabled (if present) is preserved as-is.

with open(path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")
print("tdd-guard config written:", path)
print("ignorePatterns:", len(cfg["ignorePatterns"]), "( defaults", len(DEFAULTS), "+ siblings", len(SIBLINGS), ")")
print("guardEnabled:", cfg.get("guardEnabled", "(absent -> default True)"))
