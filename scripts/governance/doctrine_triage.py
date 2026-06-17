#!/usr/bin/env python3
"""Deterministic doctrine-PR triage label (ADR-0040).

Classifies a doctrine pull-request diff as:
  - "loosening-surface": the diff touches a capability/gate surface (settings
    allow-rules, hooks, autonomy rungs/thresholds, merge/permission tokens) ->
    the human reviewer should apply FULL scrutiny before merging.
  - "prose-only": pure prose/reference text with no capability signal -> a QUICK
    human glance suffices.

CRITICAL -- this is a TRIAGE HINT for a HUMAN reviewer. It NEVER merges anything
and is NEVER a gate. A regex sees the diff SHAPE, not the DIRECTION (tighten vs
loosen) nor a meaning-shift in prose (e.g. "must" -> "should", a reference-URL
swap, a threat-category rename). Therefore "prose-only" STILL requires a human
merge -- it only signals the expected scrutiny level. Fail-closed: any signal,
or any non-markdown change to a governance file, yields "loosening-surface".
"""
import re

LOOSENING = "loosening-surface"
PROSE_ONLY = "prose-only"

# Any change to one of these files is a capability surface.
_CAPABILITY_FILES = {
    ".claude/settings.json",
    ".claude/settings.local.json",
}
# A NON-markdown change under one of these dirs is non-prose governance code.
_GOVERNANCE_CODE_DIRS = (
    ".claude/",
    "scripts/hooks/",
    "scripts/governance/",
)
# Tokens that, if present in added/removed diff lines, flag a capability change.
_TOKEN_PATTERNS = [
    r'"allow"\s*:', r'Bash\(', r'\bgh pr merge\b', r'\bgh repo edit\b',
    r'--admin\b', r'--no-verify\b', r'--yes-always\b',
    r'auto[-_ ]?merge', r'enforce_admins', r'allow_force_pushes',
    r'allow_deletions', r'required_pull_request_reviews', r'\bbypass',
    r'hooksPath', r'branch[-_ ]?protection', r'\bpermissions?\b\s*[:=]',
    r'\bR[0-3]\b',
]
_THRESHOLD_RE = re.compile(
    r'(>=|<=)\s*\d+|\b\d+\s+(?:clean|cycles?|weeks?|repos?|distinct)\b',
    re.IGNORECASE,
)
_TOKEN_RES = [re.compile(p, re.IGNORECASE) for p in _TOKEN_PATTERNS]


def split_diff(diff_text):
    """Return (added, removed) content lines from a unified diff."""
    added, removed = [], []
    for line in (diff_text or "").splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            removed.append(line[1:])
    return added, removed


def triage(diff_text, changed_files):
    """Classify a doctrine diff. Returns {'label', 'signals'}. Fail-closed."""
    signals = []
    for f in (changed_files or []):
        nf = f.replace("\\", "/")
        if nf.startswith("./"):
            nf = nf[2:]
        if nf in _CAPABILITY_FILES:
            signals.append("capability-file:" + nf)
        elif not nf.endswith(".md") and any(nf.startswith(d) for d in _GOVERNANCE_CODE_DIRS):
            signals.append("non-prose-governance-file:" + nf)
    added, removed = split_diff(diff_text)
    body = "\n".join(added + removed)
    for pat, rx in zip(_TOKEN_PATTERNS, _TOKEN_RES):
        if rx.search(body):
            signals.append("token:" + pat)
    if _THRESHOLD_RE.search(body):
        signals.append("threshold-change")
    label = LOOSENING if signals else PROSE_ONLY
    return {"label": label, "signals": sorted(set(signals))}


def _main(argv=None):
    import argparse
    import json
    import subprocess
    import sys

    ap = argparse.ArgumentParser(
        description="Doctrine PR triage label (HINT only -- never merges, never a gate)."
    )
    ap.add_argument("--pr", help="PR number; uses 'gh pr diff/view'. Omit to read a diff from stdin.")
    ap.add_argument("--repo", default=None, help="owner/name (passed to gh as -R).")
    args = ap.parse_args(argv)

    if args.pr:
        rflag = ["-R", args.repo] if args.repo else []
        diff = subprocess.check_output(["gh", "pr", "diff", args.pr, *rflag], text=True)
        fj = subprocess.check_output(["gh", "pr", "view", args.pr, *rflag, "--json", "files"], text=True)
        files = [x["path"] for x in json.loads(fj)["files"]]
    else:
        diff = sys.stdin.read()
        files = [a for a in (args.repo,) if False]  # files unknown from stdin
    res = triage(diff, files)
    res["note"] = "HINT only -- human merge still required; prose-only != safe-to-automate."
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
