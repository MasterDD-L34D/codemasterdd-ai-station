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


import argparse
import datetime
import subprocess
import sys
import tempfile

GGV2_REPO = "MasterDD-L34D/Game-Godot-v2"
GAME_REPO = "MasterDD-L34D/Game"
LABEL = "sot-drift-candidate-ggv2"


def run_gh(args):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed (rc={r.returncode}): {r.stderr.strip()}")
    return r.stdout


def fetch_merged_prs(runner, repo=GGV2_REPO, limit=50):
    out = runner(["pr", "list", "--repo", repo, "--base", "main", "--state", "merged",
                  "--json", "number,title,mergedAt,files", "--limit", str(limit)])
    return json.loads(out) if out.strip() else []


def _write_tmp(body):
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(body)
    return path


def open_or_update_issue(runner, body, repo=GAME_REPO):
    existing = runner(["issue", "list", "--repo", repo, "--label", LABEL, "--state", "open",
                       "--json", "number", "--jq", ".[0].number"]).strip()
    path = _write_tmp(body)
    try:
        if existing and existing != "null":
            runner(["issue", "edit", existing, "--repo", repo, "--body-file", path])
            runner(["issue", "comment", existing, "--repo", repo,
                    "--body", "Updated: new GGv2 SoT drift candidate detected."])
            return ("edit", existing)
        num = runner(["issue", "create", "--repo", repo, "--label", LABEL,
                      "--title", "SoT drift candidate -- GGv2 frontend ahead of SoT docs",
                      "--body-file", path]).strip()
        return ("create", num)
    finally:
        os.remove(path)


def detect(runner, watch_map_path, checkpoint_path, lookback_days=7, dry_run=False):
    watch_map = load_watch_map(watch_map_path)
    checkpoint = load_checkpoint(checkpoint_path)
    if not checkpoint.get("last_merged_at"):
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=lookback_days)
        checkpoint = {"last_merged_at": cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")}
    prs = new_prs_since(fetch_merged_prs(runner), checkpoint)
    per_pr = []
    for pr in prs:
        if not is_feature_pr(pr.get("title")):
            continue
        files = [f["path"] for f in pr.get("files", [])]
        matches = match_changes(watch_map, files)
        if matches:
            per_pr.append({"pr": pr, "matches": matches})
    result = {"scanned": len(prs), "flagged": len(per_pr)}
    if per_pr and not dry_run:
        action, num = open_or_update_issue(runner, build_issue_body(per_pr))
        result["issue"] = {"action": action, "number": num}
    elif per_pr:
        result["issue"] = {"action": "dry-run"}
    # Advance checkpoint to the newest merged PR we saw (only if fetch succeeded).
    if prs:
        checkpoint["last_merged_at"] = prs[-1]["mergedAt"]
        if not dry_run:
            save_checkpoint(checkpoint_path, checkpoint)
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="SoT drift detector for Game-Godot-v2 frontend ships.")
    ap.add_argument("--watch-map", default="ops/sot-drift/ggv2-watch-map.json")
    ap.add_argument("--checkpoint", default="logs/sot-drift-ggv2-checkpoint.json")
    ap.add_argument("--lookback-days", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    res = detect(run_gh, args.watch_map, args.checkpoint,
                 lookback_days=args.lookback_days, dry_run=args.dry_run)
    print(json.dumps(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
