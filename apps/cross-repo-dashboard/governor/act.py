"""Governor Fase-2 R1 -- actor: classify + escalate via GitHub issue.

run_r1(store, issue_api, now_iso=None) -> dict
    The only new autonomy surface.  Loads latest signals, classifies each,
    and opens/updates ONE GitHub issue (label governor-attention, codemasterdd only)
    when the escalate-set is non-empty.

    issue_api is an injected dict of callables (find_open, create, update)
    so tests can pass a fake -- gh is NEVER called in tests.

    NEVER opens a PR, NEVER merges, NEVER closes the issue.
    Label: governor-attention, repository: codemasterdd-ai-station only.

Public API
----------
    run_r1(store, issue_api, now_iso=None) -> dict
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from governor.classify import classify
from governor.digest import build_attention_body, escalate_key


# Label applied to the single managed issue.
_LABEL = "governor-attention"
# Title for the managed issue (stable; change-detection is by body key comment).
_ISSUE_TITLE = "Governor attention: escalated signals"


def run_r1(store, issue_api: dict, now_iso: "str | None" = None) -> dict:
    """Classify latest signals and open/update a GitHub issue if anything escalated.

    Args:
        store: SignalStore instance.
        issue_api: dict with callables:
            - find_open() -> dict|None  ({"number": int, "body_key": str|None} or None)
            - create(title, body, label) -> int  (issue number; body is already keyed)
            - update(issue_num, body) -> int  (body is already keyed; no new_key param)
        now_iso: unused (reserved for future audit logging); kept for API stability.

    Returns:
        {"escalated": 0, "noop": True}  -- if nothing escalated
        {"escalated": n, "issue": num, "action": "created"|"updated"|"noop"}  -- otherwise
    """
    signals = store.latest_per_source()

    escalated = []
    reported = []
    for sig in signals:
        source = sig["source"]
        prior = store.previous_severity(source)
        verdict = classify(sig, prior)
        enriched = dict(sig, **verdict)
        if verdict["action"] == "escalate":
            escalated.append(enriched)
        else:
            reported.append(enriched)

    if not escalated:
        return {"escalated": 0, "noop": True}

    key = escalate_key(escalated)
    body = build_attention_body(escalated, dropped_count=len(reported))
    # Embed the key ONCE here so both create and update receive an already-keyed body.
    # This is the single source of truth for the idempotency marker.
    keyed_body = body + "\n<!-- escalate-key: " + key + " -->"

    existing = issue_api["find_open"]()

    if existing is None:
        num = issue_api["create"](_ISSUE_TITLE, keyed_body, _LABEL)
        return {"escalated": len(escalated), "issue": num, "action": "created"}

    if existing.get("body_key") == key:
        # Same escalation set -- no update needed (idempotent).
        return {"escalated": len(escalated), "issue": existing["number"], "action": "noop"}

    num = issue_api["update"](existing["number"], keyed_body)
    return {"escalated": len(escalated), "issue": num, "action": "updated"}


# ---------------------------------------------------------------------------
# Real gh-issue API (used when running as __main__).
# Injected in tests via the issue_api parameter.
# ---------------------------------------------------------------------------

def _subprocess_env(environ: dict) -> "dict | None":
    """Subprocess env that forces the actor's gh CLI to use a dedicated
    least-privilege token, or None to inherit the ambient gh auth.

    GOVERNOR_ISSUE_TOKEN should be a fine-grained PAT scoped to issues:write on
    codemasterdd-ai-station ONLY (the actor opens/edits one issue -- it needs no
    `repo`/merge scope). It is passed to the child via GH_TOKEN in the ENV, never
    argv, so it never appears in the process arg list (CWE-214).

    Minting the PAT is a human step (account-credential = human-irreducible). Until
    GOVERNOR_ISSUE_TOKEN is set, this returns None and gh falls back to the ambient
    `gh auth` (functional but over-privileged) -- non-breaking.
    """
    tok = (environ.get("GOVERNOR_ISSUE_TOKEN") or "").strip()
    if not tok:
        return None
    return {**environ, "GH_TOKEN": tok}


def _gh(*args: str, capture: bool = True) -> str:
    """Run gh CLI and return stdout.  Raises on non-zero exit."""
    cmd = ["gh"] + list(args)
    r = subprocess.run(
        cmd, capture_output=capture, text=True, timeout=30,
        env=_subprocess_env(os.environ),
    )
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip() if capture else ""


def _real_find_open():
    """Find an open governor-attention issue and return its number + stored key.

    Returns dict {"number": int, "body_key": str|None} or None.
    The key is stored as an HTML comment in the body: <!-- escalate-key: HEXHEX -->
    """
    import json as _json
    import re as _re
    # Do NOT catch-all here: a gh list failure must propagate so the caller (run_r1)
    # aborts rather than falling through to create() and opening a duplicate issue.
    # Only return None when the list SUCCEEDS and is empty (legitimate "no open issue").
    out = _gh(
        "issue", "list",
        "--repo", "MasterDD-L34D/codemasterdd-ai-station",
        "--label", _LABEL,
        "--state", "open",
        "--json", "number,body",
        "--limit", "5",
    )
    issues = _json.loads(out or "[]")
    if not issues:
        return None
    issue = issues[0]
    num = issue["number"]
    body = issue.get("body", "")
    m = _re.search(r"<!-- escalate-key: ([0-9a-f]{16}) -->", body)
    stored_key = m.group(1) if m else None
    return {"number": num, "body_key": stored_key}


def _real_create(title: str, body: str, label: str) -> int:
    """Create a new issue and return its number.

    body is already keyed (<!-- escalate-key: HEX -->) by the caller (run_r1).
    Use it verbatim -- do NOT append the key here.
    """
    out = _gh(
        "issue", "create",
        "--repo", "MasterDD-L34D/codemasterdd-ai-station",
        "--title", title,
        "--body", body,
        "--label", label,
    )
    # `gh issue create` outputs the issue URL: https://github.com/.../issues/NN
    parts = out.rstrip("/").rsplit("/", 1)
    try:
        return int(parts[-1])
    except (ValueError, IndexError):
        raise RuntimeError(f"could not parse issue number from: {out!r}")


def _real_update(issue_num: int, body: str) -> int:
    """Update an existing issue body and return issue_num.

    body is already keyed (<!-- escalate-key: HEX -->) by the caller (run_r1).
    Use it verbatim -- do NOT append the key here.
    """
    _gh(
        "issue", "edit", str(issue_num),
        "--repo", "MasterDD-L34D/codemasterdd-ai-station",
        "--body", body,
    )
    return issue_num


def main() -> int:
    db = Path(__file__).resolve().parent.parent / "governor.db"
    if not db.exists():
        print(f"governor.act: db not found at {db} -- run ingest first", file=sys.stderr)
        return 1
    from governor.store import SignalStore
    store = SignalStore(db)
    real_api = {
        "find_open": _real_find_open,
        "create": _real_create,
        "update": _real_update,
    }
    result = run_r1(store, real_api)
    import json
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
