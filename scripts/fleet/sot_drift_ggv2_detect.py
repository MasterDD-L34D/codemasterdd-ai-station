"""SoT drift detector for Game-Godot-v2 (frontend) ships.

Polls merged GGv2 PRs (read-only, gh), matches changed paths against a JSON
watch-map, and opens/updates ONE Game issue (label sot-drift-candidate-ggv2)
listing the vault SoT refs to review. Read-only on GGv2 + vault; the only
write is the Game issue (owned repo). Semantic verdict + vault reconcile stay
with the sovereign sot-drift-verifier subagent (gated).

Design notes (from a pre-merge harsh review):
- PATH-FIRST recall: ANY merged PR touching a watched path flags, regardless
  of commit type. A safety detector must not silently miss drift shipped as
  fix/refactor. Commit type is kept only as a triage label in the issue.
- Checkpoint = a bounded SET of already-processed PR numbers, NOT a mergedAt
  watermark. PRs merged out of creation-order from long-lived branches would
  leapfrog a timestamp watermark (fall outside a "newest N" window while the
  watermark advances past them) and be missed forever. Recent merges are
  fetched by `updated` desc (a merge bumps updatedAt), so a just-merged old PR
  surfaces at the top and is processed exactly once via the seen-set.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

GGV2_REPO = "MasterDD-L34D/Game-Godot-v2"
GAME_REPO = "MasterDD-L34D/Game"
LABEL = "sot-drift-candidate-ggv2"
MARKER = "<!-- sot-drift-ggv2 -->"
SEEN_CAP = 500
GH_TIMEOUT = 120

_TYPE_RE = re.compile(r"^([a-z]+)(\([^)]*\))?!?:", re.IGNORECASE)


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


def commit_type(title):
    """Conventional-commit type prefix (feat/fix/refactor/...) for triage; '' if none."""
    m = _TYPE_RE.match((title or "").strip())
    return m.group(1).lower() if m else ""


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


def run_gh(args):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=GH_TIMEOUT)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed (rc={r.returncode}): {r.stderr.strip()}")
    return r.stdout


def fetch_recent_merged(runner, repo=GGV2_REPO, limit=100):
    """Merged PRs sorted by `updated` desc (a merge bumps updatedAt). READ-ONLY."""
    out = runner(["search", "prs", "--repo", repo, "--merged", "--sort", "updated",
                  "--order", "desc", "--limit", str(limit), "--json", "number,title"])
    return json.loads(out) if out.strip() else []


def fetch_pr_files(runner, number, repo=GGV2_REPO):
    """Changed file paths for one PR. READ-ONLY."""
    pr = json.loads(runner(["pr", "view", str(number), "--repo", repo,
                            "--json", "number,title,files"]))
    return [f["path"] for f in pr.get("files", [])]


def _write_tmp(body):
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(body)
    return path


def pr_section(item):
    pr = item["pr"]
    ct = f"[{item['commit_type']}] " if item.get("commit_type") else ""
    lines = [f"### GGv2 PR #{pr['number']} -- {ct}{pr['title']}"]
    for m in item["matches"]:
        refs = ", ".join(f"`{r}`" for r in m["sot_ref"])
        lines.append(f"- **{m['concept']}** (`{'`, `'.join(m['patterns'])}`) -> review SoT: {refs}")
        for f in m["files"]:
            lines.append(f"  - changed: `{f}`")
    lines.append("")
    return "\n".join(lines)


def build_issue_body(per_pr):
    header = [
        MARKER,
        "## SoT drift candidate -- Game-Godot-v2 frontend (auto-detected)",
        "",
        "Merged frontend PR(s) touched areas mapped to canonical vault SoT docs "
        "(path-first: any commit type; the [type] tag is triage only).",
        "**Deterministic flag only** -- semantic verdict is gated: invoke the sovereign",
        "`sot-drift-verifier` subagent to verdict + (if stale) propose a vault branch+PR reconcile.",
        "",
        "_Boundary: vault reconcile = branch+PR, merge human-only. GGv2 never written._",
        "",
        "---",
        "",
    ]
    return "\n".join(header) + "\n".join(pr_section(i) for i in per_pr)


def open_or_update_issue(runner, per_pr, repo=GAME_REPO):
    """Create the single GGv2 drift issue, or ACCUMULATE new PR sections onto it."""
    existing = runner(["issue", "list", "--repo", repo, "--label", LABEL, "--state", "open",
                       "--json", "number", "--jq", ".[0].number"]).strip()
    new_sections = "\n".join(pr_section(i) for i in per_pr)
    if existing and existing != "null":
        cur = json.loads(runner(["issue", "view", existing, "--repo", repo,
                                 "--json", "body"])).get("body", "")
        body = cur.rstrip() + "\n\n" + new_sections
        path = _write_tmp(body)
        try:
            runner(["issue", "edit", existing, "--repo", repo, "--body-file", path])
        finally:
            os.remove(path)
        return ("edit", existing)
    path = _write_tmp(build_issue_body(per_pr))
    try:
        out = runner(["issue", "create", "--repo", repo, "--label", LABEL,
                      "--title", "SoT drift candidate -- GGv2 frontend ahead of SoT docs",
                      "--body-file", path]).strip()
    finally:
        os.remove(path)
    return ("create", out)


def detect(runner, watch_map_path, checkpoint_path, limit=100, dry_run=False):
    watch_map = load_watch_map(watch_map_path)
    checkpoint = load_checkpoint(checkpoint_path)
    seen = set(checkpoint.get("seen", []))
    recent = fetch_recent_merged(runner, limit=limit)
    unseen = [p for p in recent if p["number"] not in seen]

    warnings = []
    if len(recent) >= limit and recent and recent[-1]["number"] not in seen and seen:
        warnings.append(f"fetch window full ({limit}); oldest fetched PR unseen -- "
                        "possible truncation, raise --limit or run more often")

    per_pr = []
    for pr in unseen:
        files = fetch_pr_files(runner, pr["number"])
        matches = match_changes(watch_map, files)
        if matches:
            per_pr.append({"pr": pr, "matches": matches, "commit_type": commit_type(pr["title"])})

    result = {"scanned": len(unseen), "flagged": len(per_pr)}
    if warnings:
        result["warnings"] = warnings
    if per_pr and not dry_run:
        action, ref = open_or_update_issue(runner, per_pr)
        result["issue"] = {"action": action, "ref": ref}
    elif per_pr:
        result["issue"] = {"action": "dry-run"}

    if not dry_run:
        seen |= {p["number"] for p in recent}
        checkpoint["seen"] = sorted(seen)[-SEEN_CAP:]
        checkpoint["last_run_at"] = datetime.datetime.now(
            datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        save_checkpoint(checkpoint_path, checkpoint)
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="SoT drift detector for Game-Godot-v2 frontend ships.")
    ap.add_argument("--watch-map", default="ops/sot-drift/ggv2-watch-map.json")
    ap.add_argument("--checkpoint", default="logs/sot-drift-ggv2-checkpoint.json")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    res = detect(run_gh, args.watch_map, args.checkpoint, limit=args.limit, dry_run=args.dry_run)
    print(json.dumps(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())