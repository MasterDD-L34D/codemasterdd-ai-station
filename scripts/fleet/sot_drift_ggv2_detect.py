"""SoT drift detector for Game-Godot-v2 (frontend) ships.

Polls merged GGv2 PRs (read-only, gh), keeps only feat() PRs, matches changed
paths against a JSON watch-map, and opens/updates ONE Game issue (label
sot-drift-candidate-ggv2) listing the vault SoT refs to review. Read-only on
GGv2 + vault; the only write is the Game issue (owned repo). Semantic verdict
+ vault reconcile stay with the sovereign sot-drift-verifier subagent (gated).
"""
import re

_FEAT_RE = re.compile(r"^feat(\([^)]*\))?!?:", re.IGNORECASE)


def glob_to_regex(glob):
    # Escape regex specials except '*'. Then: '**/' = any dirs (incl none),
    # '**' = anything, '*' = within one path segment.
    s = re.sub(r"([.+^${}()|\[\]\\])", r"\\\1", glob)
    s = s.replace("**/", "@@DD@@").replace("**", "@@D@@").replace("*", "[^/]*")
    s = s.replace("@@DD@@", "(?:[^/]+/)*").replace("@@D@@", ".*")
    return re.compile("^" + s + "$")


def match_changes(watch_map, changed_files):
    out = []
    for entry in watch_map:
        rxs = [glob_to_regex(p) for p in entry["patterns"]]
        files = sorted({f for f in changed_files if any(rx.match(f) for rx in rxs)})
        if files:
            out.append({"concept": entry["concept"], "sot_ref": entry["sot_ref"],
                        "patterns": entry["patterns"], "files": files})
    return out


def is_feature_pr(title):
    return bool(_FEAT_RE.match((title or "").strip()))


import json
import os


def load_watch_map(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["entries"]


def load_checkpoint(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_checkpoint(path, data):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


MARKER = "<!-- sot-drift-ggv2 -->"


def new_prs_since(prs, checkpoint):
    last = checkpoint.get("last_merged_at") or ""
    fresh = [p for p in prs if (p.get("mergedAt") or "") > last]
    return sorted(fresh, key=lambda p: p.get("mergedAt") or "")


def build_issue_body(per_pr):
    lines = [
        MARKER,
        "## SoT drift candidate -- Game-Godot-v2 frontend (auto-detected)",
        "",
        "Frontend `feat` PR(s) touched areas mapped to canonical vault SoT docs.",
        "**Deterministic flag only** -- semantic verdict is gated: invoke the sovereign",
        "`sot-drift-verifier` subagent to verdict + (if stale) propose a vault branch+PR reconcile.",
        "",
    ]
    for item in per_pr:
        pr = item["pr"]
        lines.append(f"### GGv2 PR #{pr['number']} -- {pr['title']}")
        for m in item["matches"]:
            refs = ", ".join(f"`{r}`" for r in m["sot_ref"])
            lines.append(f"- **{m['concept']}** (`{'`, `'.join(m['patterns'])}`) -> review SoT: {refs}")
            for f in m["files"]:
                lines.append(f"  - changed: `{f}`")
        lines.append("")
    lines.append("_Boundary: vault reconcile = branch+PR, merge human-only. GGv2 never written._")
    return "\n".join(lines)
