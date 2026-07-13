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
