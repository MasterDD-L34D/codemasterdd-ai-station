"""Cross-repo dashboard MVP — Component 1 spec V4 (2026-05-14).

Read-active aggregator per 5 git repos monitored. Uses GitHub REST API via
`requests` library + token from `gh auth token` (subprocess once at startup).

PIVOT 2026-05-14: subprocess.run per ogni call sotto Flask/Werkzeug ha
TypeError race condition su Windows con large outputs. requests + token =
clean threading-safe.

In-memory cache TTL 5min. Manual refresh + auto-refresh-on-stale.

Run: python app.py
Port: 8081 (avoid 8080 dogfood-ui collision)
"""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
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
    return {
        "timestamp": now_iso(),
        "force_refresh": force_refresh,
        "cache_ttl_sec": CACHE_TTL_SEC,
        "repos": repos_state,
    }


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
    return jsonify({"status": "ok", "version": "0.1.0-mvp", "timestamp": now_iso()})


if __name__ == "__main__":
    # threaded=False per Windows subprocess race condition fix
    # (Werkzeug threading + subprocess.run on Windows can leave stdout=None when
    # reader thread crashes on cp1252 or buffer issues with large gh CLI output)
    app.run(host="127.0.0.1", port=8081, debug=False, threaded=False)
