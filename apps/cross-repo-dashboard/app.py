"""Cross-repo dashboard v0.2 — Component 1 spec V4 + Full Integration (2026-05-14).

Read-active aggregator per 5 git repos monitored + 3 healthcheck endpoints +
local git divergence + Gate E counter + OPEN_DECISIONS + ADR countdown.
Workflow integration: coord-event log + dry-run PR + VS Code link.

Sources:
- GitHub REST API via requests + token from `gh auth token`
- Healthcheck: Flask:8080 + Dafne:5000 + Ollama:11434
- Local git log: per repo local clone divergence vs origin/main
- Filesystem: logs/coord-events-*.md + logs/escalation-gates-*.md +
  docs/adr/*.md ratification dates + */OPEN_DECISIONS.md count

Run dev: python app.py
Run prod: python app.py --prod  (uses waitress, default localhost:8081)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Acquire gh token once at startup (clean subprocess from main thread)
def _get_gh_token() -> str:
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True, text=False, timeout=10, check=False, shell=False
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.decode("utf-8", errors="replace").strip()
    except Exception:  # noqa: BLE001
        pass
    return ""

GH_TOKEN = _get_gh_token()
GH_API_BASE = "https://api.github.com"
HTTP_TIMEOUT = 15

# Paths
CODEMASTERDD_ROOT = Path(r"C:\dev\codemasterdd-ai-station")
AA01_ROOT = Path(r"C:\Users\edusc\aa01")
LOGS_DIR = CODEMASTERDD_ROOT / "logs"
ADR_DIR = CODEMASTERDD_ROOT / "docs" / "adr"

# Healthcheck endpoints
HEALTHCHECKS = [
    {"name": "Flask dogfood-ui", "url": "http://127.0.0.1:8080/api/health", "timeout": 3},
    {"name": "Dafne swarm", "url": "http://127.0.0.1:5000/health", "timeout": 3},
    {"name": "Ollama", "url": "http://127.0.0.1:11434/api/tags", "timeout": 3},
]

# Repo config: name -> (owner/repo string, is_dormant flag)
REPOS: dict[str, dict[str, Any]] = {
    "Game": {
        "slug": "MasterDD-L34D/Game",
        "dormant": False,
        "local_path": r"C:\dev\Game",
        "privacy": "cloud-OK",
    },
    "Game-Godot-v2": {
        "slug": "MasterDD-L34D/Game-Godot-v2",
        "dormant": False,
        "local_path": r"C:\dev\Game-Godot-v2",
        "privacy": "cloud-OK",
    },
    "Dafne": {
        "slug": "MasterDD-L34D/evo-swarm",
        "dormant": False,
        "local_path": r"C:\Users\edusc\Dafne\workspace\swarm",
        "privacy": "sovereign-only",
    },
    "vault": {
        "slug": "MasterDD-L34D/vault",
        "dormant": False,
        "local_path": r"C:\dev\vault-shared",
        "privacy": "sovereign-only",
    },
    "Synesthesia": {
        "slug": "MasterDD-L34D/synesthesia",
        "dormant": True,
        "local_path": r"C:\dev\synesthesia",
        "privacy": "mixed",
    },
}

CACHE_TTL_SEC = 300  # 5 min
CACHE: dict[str, dict[str, Any]] = {}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def cache_get(key: str) -> Any | None:
    entry = CACHE.get(key)
    if not entry:
        return None
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(entry["fetched_at"])).total_seconds()
    if age > CACHE_TTL_SEC:
        entry["stale"] = True
    return entry


def cache_set(key: str, payload: Any, error: str | None = None) -> None:
    CACHE[key] = {
        "payload": payload,
        "fetched_at": now_iso(),
        "stale": False,
        "error": error,
    }


def gh_api(endpoint: str, timeout: int = HTTP_TIMEOUT) -> tuple[bool, Any, str | None]:
    """Call GitHub REST API via requests + token. Threading-safe.

    endpoint: path relativo (es. "repos/owner/repo/pulls?state=open")
    Returns: (ok, parsed_json, error_msg)
    """
    if not GH_TOKEN:
        return False, None, "no gh token (run `gh auth login`)"
    url = f"{GH_API_BASE}/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code == 200:
            try:
                return True, r.json(), None
            except ValueError:
                return True, r.text, None
        if r.status_code == 403 and "rate limit" in r.text.lower():
            return False, None, f"rate limit: reset at {r.headers.get('X-RateLimit-Reset','?')}"
        return False, None, f"http {r.status_code}: {r.text[:200]}"
    except requests.Timeout:
        return False, None, f"timeout after {timeout}s"
    except requests.ConnectionError as e:
        return False, None, f"conn error: {str(e)[:200]}"
    except Exception as e:  # noqa: BLE001
        return False, None, f"{type(e).__name__}: {str(e)[:200]}"


def fetch_repo_state(name: str, force_refresh: bool = False) -> dict[str, Any]:
    """Fetch state for a single repo (cached unless force_refresh)."""
    config = REPOS[name]
    slug = config["slug"]
    cache_key_pr = f"pr:{name}"
    cache_key_commit = f"commit:{name}"

    # PR list (gh REST API: pulls)
    if not force_refresh and (cached := cache_get(cache_key_pr)) and not cached["stale"]:
        prs_data = cached
    else:
        ok, payload, err = gh_api(f"repos/{slug}/pulls?state=open&per_page=30")
        if ok:
            # Normalize to compact shape (number, title, user.login, created_at)
            compact = [
                {"number": p.get("number"), "title": p.get("title", ""), "author": {"login": (p.get("user") or {}).get("login", "?")}, "createdAt": p.get("created_at", "")}
                for p in (payload if isinstance(payload, list) else [])
            ]
            cache_set(cache_key_pr, compact)
        else:
            cache_set(cache_key_pr, [], error=err)
        prs_data = CACHE[cache_key_pr]

    # Commit recent (gh REST API: commits)
    if not force_refresh and (cached := cache_get(cache_key_commit)) and not cached["stale"]:
        commits_data = cached
    else:
        ok, payload, err = gh_api(f"repos/{slug}/commits?per_page=5")
        if ok:
            cache_set(cache_key_commit, payload)
        else:
            cache_set(cache_key_commit, [], error=err)
        commits_data = CACHE[cache_key_commit]

    # Summary
    pr_count = len(prs_data["payload"]) if isinstance(prs_data["payload"], list) else 0
    last_commit = None
    if isinstance(commits_data["payload"], list) and commits_data["payload"]:
        c = commits_data["payload"][0]
        last_commit = {
            "sha_short": c.get("sha", "")[:7],
            "author": c.get("commit", {}).get("author", {}).get("name", "?"),
            "date": c.get("commit", {}).get("author", {}).get("date", "?"),
            "message_short": (c.get("commit", {}).get("message", "") or "").split("\n")[0][:80],
        }

    return {
        "name": name,
        "slug": slug,
        "dormant": config["dormant"],
        "privacy": config["privacy"],
        "local_path": config["local_path"],
        "pr_count": pr_count,
        "prs": prs_data["payload"] if isinstance(prs_data["payload"], list) else [],
        "last_commit": last_commit,
        "fetched_at": prs_data["fetched_at"],
        "stale": prs_data.get("stale", False) or commits_data.get("stale", False),
        "error": prs_data.get("error") or commits_data.get("error"),
    }


def fetch_all_state(force_refresh: bool = False) -> dict[str, Any]:
    repos_state = {name: fetch_repo_state(name, force_refresh) for name in REPOS}
    # Enrich each repo with local git divergence
    for name, repo in repos_state.items():
        local_path = repo.get("local_path")
        if local_path and Path(local_path).exists():
            repo["git_local"] = fetch_git_local(local_path)
        else:
            repo["git_local"] = {"available": False, "reason": "path not found"}
    return {
        "timestamp": now_iso(),
        "force_refresh": force_refresh,
        "cache_ttl_sec": CACHE_TTL_SEC,
        "repos": repos_state,
        "healthchecks": fetch_healthchecks(force_refresh),
        "gate_e": fetch_gate_e_counter(),
        "adr_countdown": fetch_adr_countdown(),
        "open_decisions": fetch_open_decisions(),
    }


# ====================================================================== #
# Phase 1 v0.2 new data sources
# ====================================================================== #

def fetch_healthchecks(force_refresh: bool = False) -> list[dict[str, Any]]:
    """C1: ping 3 endpoints + cache."""
    cache_key = "healthchecks"
    if not force_refresh:
        cached = cache_get(cache_key)
        if cached and not cached["stale"]:
            return cached["payload"]
    results = []
    for hc in HEALTHCHECKS:
        try:
            r = requests.get(hc["url"], timeout=hc["timeout"])
            results.append({
                "name": hc["name"],
                "url": hc["url"],
                "status": "up" if r.status_code == 200 else "error",
                "http": r.status_code,
                "latency_ms": int(r.elapsed.total_seconds() * 1000),
            })
        except requests.ConnectionError:
            results.append({"name": hc["name"], "url": hc["url"], "status": "down", "http": None, "latency_ms": None})
        except requests.Timeout:
            results.append({"name": hc["name"], "url": hc["url"], "status": "timeout", "http": None, "latency_ms": None})
        except Exception as e:  # noqa: BLE001
            results.append({"name": hc["name"], "url": hc["url"], "status": "error", "http": None, "error": str(e)[:100]})
    cache_set(cache_key, results)
    return results


def fetch_git_local(local_path: str) -> dict[str, Any]:
    """C2: git log local divergence vs origin/main (or origin/master)."""
    try:
        # HEAD short
        head = subprocess.run(
            ["git", "-C", local_path, "rev-parse", "--short", "HEAD"],
            capture_output=True, text=False, timeout=5, check=False,
        )
        if head.returncode != 0:
            return {"available": False, "reason": "git rev-parse failed"}
        head_short = head.stdout.decode("utf-8", errors="replace").strip()
        # Branch
        branch = subprocess.run(
            ["git", "-C", local_path, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=False, timeout=5, check=False,
        )
        branch_name = branch.stdout.decode("utf-8", errors="replace").strip() if branch.returncode == 0 else "?"
        # Divergence vs origin/main
        for base in ["origin/main", "origin/master"]:
            ahead = subprocess.run(
                ["git", "-C", local_path, "rev-list", "--count", f"{base}..HEAD"],
                capture_output=True, text=False, timeout=5, check=False,
            )
            behind = subprocess.run(
                ["git", "-C", local_path, "rev-list", "--count", f"HEAD..{base}"],
                capture_output=True, text=False, timeout=5, check=False,
            )
            if ahead.returncode == 0 and behind.returncode == 0:
                return {
                    "available": True,
                    "head_short": head_short,
                    "branch": branch_name,
                    "base": base,
                    "ahead": int(ahead.stdout.decode("utf-8", errors="replace").strip() or 0),
                    "behind": int(behind.stdout.decode("utf-8", errors="replace").strip() or 0),
                }
        return {"available": True, "head_short": head_short, "branch": branch_name, "ahead": 0, "behind": 0, "base": "unknown"}
    except Exception as e:  # noqa: BLE001
        return {"available": False, "reason": f"{type(e).__name__}: {str(e)[:100]}"}


def fetch_gate_e_counter() -> dict[str, Any]:
    """C3: Count Gate E events from logs/coord-events-*.md aggregated."""
    total = 0
    files_scanned = []
    current_month_events = 0
    cur_month = datetime.now(timezone.utc).strftime("%Y-%m")
    try:
        for f in LOGS_DIR.glob("coord-events-*.md"):
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                # Count rows: lines starting with "| 2026-" (date-prefixed table rows)
                events = len([line for line in content.split("\n") if re.match(r"^\|\s*2026-\d{2}-\d{2}", line)])
                total += events
                files_scanned.append({"file": f.name, "events": events})
                if cur_month in f.name:
                    current_month_events += events
            except Exception:  # noqa: BLE001
                continue
    except Exception:  # noqa: BLE001
        pass
    # Week E window: 2026-05-20 to 2026-06-19 (4 weeks)
    window_start = datetime(2026, 5, 20, tzinfo=timezone.utc)
    window_end = datetime(2026, 6, 19, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    if now < window_start:
        window_status = "not_started"
        days_to_start = (window_start - now).days
    elif now > window_end:
        window_status = "ended"
        days_to_start = 0
    else:
        window_status = "active"
        days_to_start = 0
    return {
        "total_events": total,
        "current_month_events": current_month_events,
        "files_scanned": files_scanned,
        "window_status": window_status,
        "days_to_window_start": days_to_start,
        "window_start": window_start.date().isoformat(),
        "window_end": window_end.date().isoformat(),
        "threshold_pass_per_week": 5,
        "threshold_minimal_min": 2,
    }


def fetch_adr_countdown() -> list[dict[str, Any]]:
    """D3: scan docs/adr/*.md for ratification check dates (status Proposed)."""
    items = []
    if not ADR_DIR.exists():
        return items
    try:
        for f in sorted(ADR_DIR.glob("*.md")):
            try:
                content = f.read_text(encoding="utf-8", errors="replace")[:2000]
                # Look for Status: Proposed + ratification date
                if not re.search(r"Status\*?\*?:\s*Proposed", content, re.IGNORECASE):
                    continue
                # Look for ratification date pattern YYYY-MM-DD
                date_match = re.search(r"ratification.{0,80}?(20\d{2}-\d{2}-\d{2})", content, re.IGNORECASE | re.DOTALL)
                if not date_match:
                    continue
                ratify_date_str = date_match.group(1)
                try:
                    ratify_date = datetime.fromisoformat(ratify_date_str).replace(tzinfo=timezone.utc)
                    days_remaining = (ratify_date - datetime.now(timezone.utc)).days
                except ValueError:
                    days_remaining = None
                # Extract ADR number from filename
                num_match = re.match(r"(\d{4})", f.name)
                items.append({
                    "adr": num_match.group(1) if num_match else "?",
                    "file": f.name,
                    "ratify_date": ratify_date_str,
                    "days_remaining": days_remaining,
                })
            except Exception:  # noqa: BLE001
                continue
    except Exception:  # noqa: BLE001
        pass
    # Sort by days remaining (most urgent first)
    items.sort(key=lambda x: (x["days_remaining"] if x["days_remaining"] is not None else 99999))
    return items


def fetch_open_decisions() -> dict[str, Any]:
    """D1: count active OD entries per repo (codemasterdd OPEN_DECISIONS.md primary)."""
    od_file = CODEMASTERDD_ROOT / "OPEN_DECISIONS.md"
    if not od_file.exists():
        return {"available": False, "count_active": 0, "entries": []}
    try:
        content = od_file.read_text(encoding="utf-8", errors="replace")
        # Match headings like "### [OD-NNN] title"
        # Active = NOT prefixed with ~~strikethrough~~ AND NOT containing "CLOSED"
        all_entries = re.findall(r"###\s+\[?(OD-\d+)\]?\s+([^\n]+)", content)
        active = []
        for od_id, title in all_entries:
            # Check if title has strikethrough or CLOSED
            if "~~" in title or "CLOSED" in title.upper() or "RATIFIED" in title.upper():
                continue
            active.append({"id": od_id, "title": title.strip()[:120]})
        return {"available": True, "count_active": len(active), "count_total": len(all_entries), "entries": active[:10]}
    except Exception as e:  # noqa: BLE001
        return {"available": False, "reason": str(e)[:100]}


# ====================================================================== #
# Routes
# ====================================================================== #

@app.route("/")
def index() -> Any:
    force = request.args.get("refresh") == "1"
    state = fetch_all_state(force_refresh=force)
    return render_template("index.html", state=state)


@app.route("/api/state")
def api_state() -> Any:
    force = request.args.get("refresh") == "1"
    return jsonify(fetch_all_state(force_refresh=force))


@app.route("/health")
def health() -> Any:
    return jsonify({"status": "ok", "version": "0.2.0-full-integration", "timestamp": now_iso()})


@app.route("/api/coord-event", methods=["POST"])
def coord_event_log() -> Any:
    """B1: Invoca scripts/cross-repo/coord-event-log.ps1 -Quiet -NotesQuick <notes>."""
    notes = (request.json or {}).get("notes", "").strip()
    if not notes:
        return jsonify({"ok": False, "error": "notes required"}), 400
    if len(notes) > 200:
        return jsonify({"ok": False, "error": "notes max 200 chars"}), 400
    script_path = CODEMASTERDD_ROOT / "scripts" / "cross-repo" / "coord-event-log.ps1"
    if not script_path.exists():
        return jsonify({"ok": False, "error": "script not found"}), 500
    try:
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path), "-Quiet", "-NotesQuick", notes],
            capture_output=True, text=False, timeout=15, check=False, shell=False,
        )
        out = result.stdout.decode("utf-8", errors="replace")[-500:]
        err = result.stderr.decode("utf-8", errors="replace")[-500:]
        return jsonify({"ok": result.returncode == 0, "stdout_tail": out, "stderr_tail": err, "returncode": result.returncode})
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}), 500


@app.route("/api/draft-pr", methods=["POST"])
def draft_pr() -> Any:
    """B2: Invoca scripts/cross-repo/dry-run-pr.ps1 con parametri form."""
    data = request.json or {}
    repo_target = data.get("repo_target", "").strip()
    pr_type = data.get("type", "").strip()
    preview_files = data.get("preview_files", "").strip()
    summary = data.get("summary", "").strip()
    if not all([repo_target, pr_type, preview_files, summary]):
        return jsonify({"ok": False, "error": "all 4 fields required"}), 400
    valid_targets = {"Game", "Godot-v2", "Dafne", "vault"}
    valid_types = {"policy-alignment", "ADR-cross-ref", "drift-fix", "docs", "governance-suggestion"}
    if repo_target not in valid_targets:
        return jsonify({"ok": False, "error": f"target must be one of {sorted(valid_targets)}"}), 400
    if pr_type not in valid_types:
        return jsonify({"ok": False, "error": f"type must be one of {sorted(valid_types)}"}), 400
    script_path = CODEMASTERDD_ROOT / "scripts" / "cross-repo" / "dry-run-pr.ps1"
    if not script_path.exists():
        return jsonify({"ok": False, "error": "script not found"}), 500
    try:
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path),
             "-RepoTarget", repo_target, "-Type", pr_type,
             "-PreviewFiles", preview_files, "-Summary", summary],
            capture_output=True, text=False, timeout=20, check=False, shell=False,
        )
        out = result.stdout.decode("utf-8", errors="replace")
        err = result.stderr.decode("utf-8", errors="replace")[-500:]
        return jsonify({"ok": result.returncode == 0, "draft": out, "stderr_tail": err, "returncode": result.returncode})
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}), 500


@app.route("/api/open-vscode")
def open_vscode() -> Any:
    """B3: Launch VS Code at given path (validated whitelist)."""
    path_str = request.args.get("path", "").strip()
    allowed_paths = {str(Path(r["local_path"])) for r in REPOS.values()} | {str(CODEMASTERDD_ROOT)}
    norm_path = str(Path(path_str))
    if norm_path not in allowed_paths:
        return jsonify({"ok": False, "error": "path not whitelisted"}), 400
    try:
        # Use 'code' CLI launcher (non-blocking detach via DETACHED_PROCESS on Windows)
        creationflags = 0x00000008 if sys.platform == "win32" else 0  # DETACHED_PROCESS
        subprocess.Popen(["code", norm_path], shell=True, creationflags=creationflags)
        return jsonify({"ok": True, "opened": norm_path})
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}), 500


def run_dev() -> None:
    """Werkzeug dev server (threaded=False per Windows subprocess fix)."""
    app.run(host="127.0.0.1", port=8081, debug=False, threaded=False)


def run_prod() -> None:
    """Waitress WSGI production server."""
    try:
        from waitress import serve
    except ImportError:
        print("waitress not installed. Install: pip install waitress")
        sys.exit(1)
    print("Cross-repo Dashboard v0.2.0 running on http://127.0.0.1:8081 (waitress production)")
    serve(app, host="127.0.0.1", port=8081, threads=4)


if __name__ == "__main__":
    if "--prod" in sys.argv:
        run_prod()
    else:
        run_dev()
