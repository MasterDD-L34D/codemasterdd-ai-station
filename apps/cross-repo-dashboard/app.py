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

__all__ = ["app", "fetch_healthchecks"]

import hmac
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from flask import Flask, Blueprint, jsonify, render_template, request

cross_repo_bp = Blueprint(
    'cross_repo', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static',
)

# P0 console-flash fix 2026-05-14 sera-tardi-ultra-2: every subprocess on Windows
# flashes brief console window unless CREATE_NO_WINDOW flag (0x08000000) is set.
# Eduardo "vedo finestre cmd aprirsi e richiudersi" reported recurring flicker.
# Dashboard auto-refresh 5min × 15+ git subprocess per cycle = visible flicker.
_NO_WINDOW_FLAG = 0x08000000 if sys.platform == "win32" else 0

# Pre-compiled regexes for performance (hoisted from loops/frequent functions)
_GATE_E_ROW_RE = re.compile(r"^\|\s*2026-\d{2}-\d{2}")
_ADR_STATUS_PROPOSED_RE = re.compile(r"\*{0,2}Status\*{0,2}\s*:\s*Proposed", re.IGNORECASE)
_ADR_RATIFY_DATE_RE1 = re.compile(r"\*{0,2}Ratification[^:\n]{0,80}date\*{0,2}\s*:.{0,200}?(20\d{2}-\d{2}-\d{2})", re.IGNORECASE | re.DOTALL)
_ADR_RATIFY_DATE_RE2 = re.compile(r"ratification[^.\n]{0,200}?(20\d{2}-\d{2}-\d{2})", re.IGNORECASE | re.DOTALL)
_ADR_RATIFY_DATE_RE3 = re.compile(r"\bentro\s+(20\d{2}-\d{2}-\d{2})", re.IGNORECASE)
_ADR_NUM_RE = re.compile(r"(\d{4})")
_OD_ENTRY_RE = re.compile(r"###\s+\[?(OD-\d+)\]?\s+([^\n]+)")
_JOURNAL_DATE_RE = re.compile(r"^## 20\d{2}-\d{2}-\d{2}")
_JOURNAL_HEADER_RE = re.compile(r"^## (.+)$")


# Acquire gh token once at startup (clean subprocess from main thread)
def _get_gh_token() -> str:
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True, text=False, timeout=10, check=False, shell=False,
            creationflags=_NO_WINDOW_FLAG,
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
# Machine-portable: aa01 lives at C:\Users\<user>\aa01 (VGit on Ryzen,
# edusc on Lenovo). Override via AA01_ROOT_PATH.
AA01_ROOT = Path(os.environ.get("AA01_ROOT_PATH", "").strip() or (Path.home() / "aa01"))
LOGS_DIR = CODEMASTERDD_ROOT / "logs"
ADR_DIR = CODEMASTERDD_ROOT / "docs" / "adr"
GOVERNOR_DB = CODEMASTERDD_ROOT / "apps" / "cross-repo-dashboard" / "governor.db"


def resolve_repo_path(env_var: str, *candidates: str) -> str:
    override = os.environ.get(env_var, "").strip()
    if override:
        return override
    for cand in candidates:
        if Path(cand).exists():
            return cand
    return candidates[-1] if candidates else ""

# Healthcheck endpoints
# HTTP-based (require service exposing /health or similar)
HEALTHCHECKS = [
    # Local AI inference (always-on)
    {"name": "Ollama", "url": "http://127.0.0.1:11434/api/tags", "timeout": 3, "category": "ai-inference"},
    # Stack ADR-0017 observability (Docker compose, scaffold opt-in DOWN by default)
    {"name": "LiteLLM proxy", "url": "http://127.0.0.1:4000/health/readiness", "timeout": 3, "category": "stack-adr-0017"},
    {"name": "Langfuse", "url": "http://127.0.0.1:3000/api/public/health", "timeout": 3, "category": "stack-adr-0017"},
    {"name": "dogfood-ui Flask", "url": "http://127.0.0.1:8080/api/health", "timeout": 6, "category": "stack-adr-0017"},
    # Dafne swarm (run manually via START-SWARM.ps1)
    {"name": "Dafne swarm", "url": "http://127.0.0.1:5000/health", "timeout": 3, "category": "dafne"},
]

# TCP-only services (no HTTP endpoint, port-open check)
# NOTE: Postgres NOT exposed to host by design (compose internal network only).
# Verified UP empirically via LiteLLM/Langfuse DB connection (they depends_on:postgres healthy).
# Removed from healthcheck list to avoid false-DOWN signal.
HEALTHCHECKS_TCP: list[dict[str, Any]] = []

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
        # Machine-portable: evo-swarm clone is C:\dev\evo-swarm on Ryzen
        # (DESKTOP-T77TMKT) and C:\Users\edusc\Dafne\workspace\swarm on Lenovo.
        # Override via DAFNE_REPO_PATH.
        "local_path": resolve_repo_path(
            "DAFNE_REPO_PATH", r"C:\dev\evo-swarm", r"C:\Users\edusc\Dafne\workspace\swarm"
        ),
        "privacy": "sovereign-only",
    },
    "vault": {
        "slug": "MasterDD-L34D/vault",
        "dormant": False,
        # Machine-portable: vault is C:\dev\vault on Ryzen (DESKTOP-T77TMKT) and
        # Lenovo, historically C:\dev\vault-shared. Override via VAULT_REPO_PATH.
        "local_path": resolve_repo_path(
            "VAULT_REPO_PATH", r"C:\dev\vault", r"C:\dev\vault-shared"
        ),
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
    """Fetch state for a single repo (cached unless force_refresh).

    Note: This function is actively called by `fetch_all_state()` to populate the
    `repos` dictionary key, which is then rendered in `index.html`.
    """
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
    # Enrich each repo with local git divergence + velocity
    for name, repo in repos_state.items():
        local_path = repo.get("local_path")
        if local_path and Path(local_path).exists():
            repo["git_local"] = fetch_git_local(local_path)
            repo["velocity"] = fetch_velocity(local_path)
        else:
            repo["git_local"] = {"available": False, "reason": "path not found"}
            repo["velocity"] = {"available": False}
    return {
        "timestamp": now_iso(),
        "force_refresh": force_refresh,
        "cache_ttl_sec": CACHE_TTL_SEC,
        "repos": repos_state,
        "healthchecks": fetch_healthchecks(force_refresh),
        "gate_e": fetch_gate_e_counter(),
        "adr_countdown": fetch_adr_countdown(),
        "open_decisions": fetch_open_decisions(),
        "journal_preview": fetch_journal_preview(),
        "activity_feed": fetch_activity_feed(repos_state),
    }


# ====================================================================== #
# Phase 1 v0.2 new data sources
# ====================================================================== #

def fetch_healthchecks(force_refresh: bool = False) -> list[dict[str, Any]]:
    """C1: ping HTTP endpoints + TCP port check + cache.

    Note: This function is actively called by `fetch_all_state()` to populate the
    `healthchecks` dictionary key, which is then rendered in `index.html`.

    Distinguishes:
    - 'up'      service responding 200 OK
    - 'down'    ConnectionError (not running)
    - 'timeout' slow but reachable
    - 'error'   non-200 response

    Categories grouped: ai-inference / stack-adr-0017 / dafne.
    """
    import socket
    cache_key = "healthchecks"
    if not force_refresh:
        cached = cache_get(cache_key)
        if cached and not cached["stale"]:
            return cached["payload"]
    results = []
    # HTTP healthchecks
    for hc in HEALTHCHECKS:
        try:
            r = requests.get(hc["url"], timeout=hc["timeout"])
            results.append({
                "name": hc["name"],
                "url": hc["url"],
                "category": hc.get("category", "other"),
                "status": "up" if r.status_code == 200 else "error",
                "http": r.status_code,
                "latency_ms": int(r.elapsed.total_seconds() * 1000),
            })
        except requests.ConnectionError:
            results.append({"name": hc["name"], "url": hc["url"], "category": hc.get("category", "other"),
                          "status": "down", "http": None, "latency_ms": None})
        except requests.Timeout:
            results.append({"name": hc["name"], "url": hc["url"], "category": hc.get("category", "other"),
                          "status": "timeout", "http": None, "latency_ms": None})
        except Exception as e:  # noqa: BLE001
            results.append({"name": hc["name"], "url": hc["url"], "category": hc.get("category", "other"),
                          "status": "error", "http": None, "error": str(e)[:100]})
    # TCP socket healthchecks (es. Postgres no HTTP)
    for hc in HEALTHCHECKS_TCP:
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(hc["timeout"])
            start = datetime.now(timezone.utc)
            result = sock.connect_ex((hc["host"], hc["port"]))
            elapsed_ms = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)
            if result == 0:
                results.append({"name": hc["name"], "url": f"tcp://{hc['host']}:{hc['port']}",
                              "category": hc.get("category", "other"), "status": "up",
                              "http": None, "latency_ms": elapsed_ms})
            else:
                results.append({"name": hc["name"], "url": f"tcp://{hc['host']}:{hc['port']}",
                              "category": hc.get("category", "other"), "status": "down",
                              "http": None, "latency_ms": None})
        except Exception:  # noqa: BLE001
            results.append({"name": hc["name"], "url": f"tcp://{hc['host']}:{hc['port']}",
                          "category": hc.get("category", "other"), "status": "down",
                          "http": None, "latency_ms": None})
        finally:
            if sock:
                try:
                    sock.close()
                except Exception:  # noqa: BLE001
                    pass
    cache_set(cache_key, results)
    return results


def fetch_git_local(local_path: str) -> dict[str, Any]:
    """C2: git log local divergence vs origin/main (or origin/master).

    Note: This function is actively called by `fetch_all_state()` to populate the
    `git_local` dictionary key within each repository's state, rendered in `index.html`.
    """
    try:
        # HEAD short
        head = subprocess.run(
            ["git", "-C", local_path, "rev-parse", "--short", "HEAD"],
            capture_output=True, text=False, timeout=5, check=False,
            creationflags=_NO_WINDOW_FLAG,
        )
        if head.returncode != 0:
            return {"available": False, "reason": "git rev-parse failed"}
        head_short = head.stdout.decode("utf-8", errors="replace").strip()
        # Branch
        branch = subprocess.run(
            ["git", "-C", local_path, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=False, timeout=5, check=False,
            creationflags=_NO_WINDOW_FLAG,
        )
        branch_name = branch.stdout.decode("utf-8", errors="replace").strip() if branch.returncode == 0 else "?"
        # Divergence vs origin/main
        for base in ["origin/main", "origin/master"]:
            ahead = subprocess.run(
                ["git", "-C", local_path, "rev-list", "--count", f"{base}..HEAD"],
                capture_output=True, text=False, timeout=5, check=False,
                creationflags=_NO_WINDOW_FLAG,
            )
            behind = subprocess.run(
                ["git", "-C", local_path, "rev-list", "--count", f"HEAD..{base}"],
                capture_output=True, text=False, timeout=5, check=False,
                creationflags=_NO_WINDOW_FLAG,
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
    """C3: Count Gate E events from logs/coord-events-*.md aggregated.

    This function parses markdown logs to count Gate E events.
    It is actively called by fetch_all_state() to populate the 'gate_e' dictionary
    which is then rendered in the index.html template.
    """
    total = 0
    files_scanned = []
    current_month_events = 0
    cur_month = datetime.now(timezone.utc).strftime("%Y-%m")
    try:
        for f in LOGS_DIR.glob("coord-events-*.md"):
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                # Count rows: lines starting with "| 2026-" (date-prefixed table rows)
                events = len([line for line in content.split("\n") if _GATE_E_ROW_RE.match(line)])
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
    """D3: scan docs/adr/*.md for ratification check dates (status Proposed).

    ADR format esempio (ADR-0023):
    - Line 5: `**Status**: Proposed (...)` (with optional addendum after)
    - Line 47: `**Ratification check date**: ADR-NNNN entro 2026-MM-DD (...)`
    Or: `ratification` keyword inside narrative + ISO date within 200 chars.
    """
    items = []
    if not ADR_DIR.exists():
        return items
    try:
        for f in sorted(ADR_DIR.glob("*.md")):
            try:
                # Read full file (ratification date may be deep, not in first 2000 chars)
                content = f.read_text(encoding="utf-8", errors="replace")
                # Look for Status: Proposed (with optional ** markdown bold)
                if not _ADR_STATUS_PROPOSED_RE.search(content):
                    continue
                # Look for ratification date — broader pattern, multiple candidates
                # Pattern 1: "Ratification check date: ... 2026-MM-DD"
                # Pattern 2: "ratification ... 2026-MM-DD" within 200 chars
                # Pattern 3: "entro 2026-MM-DD" (Italian common pattern)
                date_match = (
                    _ADR_RATIFY_DATE_RE1.search(content)
                    or _ADR_RATIFY_DATE_RE2.search(content)
                    or _ADR_RATIFY_DATE_RE3.search(content)
                )
                if not date_match:
                    continue
                ratify_date_str = date_match.group(1)
                try:
                    ratify_date = datetime.fromisoformat(ratify_date_str).replace(tzinfo=timezone.utc)
                    days_remaining = (ratify_date - datetime.now(timezone.utc)).days
                except ValueError:
                    days_remaining = None
                # Extract ADR number from filename
                num_match = _ADR_NUM_RE.match(f.name)
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
    """D1: count active OD entries per repo (codemasterdd OPEN_DECISIONS.md primary).

    Note: This function is called by `fetch_all_state` to populate the
    `open_decisions` data used by `index.html`. It should not be removed.
    """
    od_file = CODEMASTERDD_ROOT / "OPEN_DECISIONS.md"
    if not od_file.exists():
        return {"available": False, "count_active": 0, "entries": []}
    try:
        content = od_file.read_text(encoding="utf-8", errors="replace")
        # Match headings like "### [OD-NNN] title"
        # Active = NOT prefixed with ~~strikethrough~~ AND NOT containing "CLOSED"
        all_entries = _OD_ENTRY_RE.findall(content)
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
# Phase 3 v0.3 NEW features 2026-05-14 sera-tardi-ultra-3
# ====================================================================== #

JOURNAL_PATH = CODEMASTERDD_ROOT / "JOURNAL.md"


def fetch_journal_preview(max_chars: int = 600) -> dict[str, Any]:
    """v0.3 NEW: read first 1-2 dated entries from JOURNAL.md.

    Note: This function is called by `fetch_all_state` to populate the
    `journal_preview` data used by `index.html`. It should not be removed.
    """
    if not JOURNAL_PATH.exists():
        return {"available": False, "reason": "JOURNAL.md not found"}
    try:
        content = JOURNAL_PATH.read_text(encoding="utf-8", errors="replace")
        # Find first dated entry (## YYYY-MM-DD pattern, NOT template)
        lines = content.split("\n")
        entries = []
        current_entry: list[str] | None = None
        for line in lines:
            if _JOURNAL_DATE_RE.match(line):
                if current_entry is not None:
                    entries.append("\n".join(current_entry))
                    if len(entries) >= 2:
                        break
                current_entry = [line]
            elif current_entry is not None and line.startswith("---"):
                entries.append("\n".join(current_entry))
                current_entry = None
                if len(entries) >= 2:
                    break
            elif current_entry is not None:
                current_entry.append(line)
        if current_entry and len(entries) < 2:
            entries.append("\n".join(current_entry))
        if not entries:
            return {"available": False, "reason": "no dated entries found"}
        latest = entries[0]
        # Extract header + first ~max_chars
        header_match = _JOURNAL_HEADER_RE.match(latest.split("\n")[0])
        header = header_match.group(1) if header_match else "?"
        preview_text = latest[:max_chars]
        if len(latest) > max_chars:
            preview_text += "..."
        return {
            "available": True,
            "header": header,
            "preview": preview_text,
            "total_entries_count": sum(1 for line in lines if _JOURNAL_DATE_RE.match(line)),
        }
    except Exception as e:  # noqa: BLE001
        return {"available": False, "reason": f"{type(e).__name__}: {str(e)[:100]}"}


def fetch_velocity(local_path: str) -> dict[str, Any]:
    """v0.3 NEW: commits per week last 4 weeks via git log --since.

    Note: This function is actively called by `fetch_all_state()` to populate the
    `velocity` dictionary key within each repository's state, rendered in `index.html`.
    """
    try:
        weeks_count = []
        for week_offset in range(4, 0, -1):  # 4 weeks ago, 3, 2, 1
            since = f"{week_offset} weeks ago"
            until = f"{week_offset - 1} weeks ago" if week_offset > 1 else None
            cmd = ["git", "-C", local_path, "log", "--oneline", f"--since={since}"]
            if until:
                cmd.append(f"--until={until}")
            result = subprocess.run(
                cmd, capture_output=True, text=False, timeout=5, check=False,
                creationflags=_NO_WINDOW_FLAG,
            )
            if result.returncode != 0:
                return {"available": False, "reason": "git log failed"}
            count = len([line for line in result.stdout.decode("utf-8", errors="replace").split("\n") if line.strip()])
            weeks_count.append(count)
        total = sum(weeks_count)
        max_count = max(weeks_count) if weeks_count else 1
        return {
            "available": True,
            "weeks": weeks_count,  # oldest first [w-4, w-3, w-2, w-1]
            "total_4w": total,
            "max_week": max_count,
            "avg_per_week": round(total / 4, 1),
        }
    except Exception as e:  # noqa: BLE001
        return {"available": False, "reason": f"{type(e).__name__}: {str(e)[:100]}"}


def fetch_activity_feed(repos_state: dict[str, Any], limit: int = 10) -> list[dict[str, Any]]:  # noqa
    """v0.3 NEW: aggregate last commits across all repos sorted by date desc.

    Note: This function is actively called by fetch_all_state() to populate the
    'activity_feed' data used by index.html. Do not remove it despite what static
    analysis tools might suggest.
    """
    activities = []
    for name, repo in repos_state.items():
        commit = repo.get("last_commit")
        if not commit:
            continue
        activities.append({
            "repo": name,
            "sha_short": commit.get("sha_short", "?"),
            "author": commit.get("author", "?"),
            "date": commit.get("date", "?"),
            "message_short": commit.get("message_short", "?"),
            "privacy": repo.get("privacy", "?"),
        })
    # Sort by date desc (ISO 8601 strings comparable as strings)
    activities.sort(key=lambda x: x.get("date", ""), reverse=True)
    return activities[:limit]


# ====================================================================== #
# Routes
# ====================================================================== #

@cross_repo_bp.route("/")
def index() -> Any:
    force = request.args.get("refresh") == "1"
    state = fetch_all_state(force_refresh=force)
    # Inject API_SECRET (if set) so same-origin dashboard JS can authenticate
    # to /api/draft-pr. Localhost-only single-user tool: same-origin JS holding
    # the token is acceptable (Codex P2 #111 fix -- supported credential path).
    return render_template(
        "cr_index.html", state=state, api_secret=os.environ.get("API_SECRET", "")
    )


@cross_repo_bp.route("/api/state")
def api_state() -> Any:
    force = request.args.get("refresh") == "1"
    return jsonify(fetch_all_state(force_refresh=force))


@cross_repo_bp.route("/<repo>")
def drill_down(repo: str) -> Any:
    """v0.3 NEW: per-repo detail view."""
    if repo not in REPOS:
        return jsonify({"error": f"unknown repo: {repo}"}), 404
    force = request.args.get("refresh") == "1"
    state = fetch_all_state(force_refresh=force)
    repo_state = state["repos"].get(repo)
    if not repo_state:
        return jsonify({"error": f"no state for repo: {repo}"}), 500
    return render_template("cr_drill_down.html", repo=repo_state, all_state=state)


@cross_repo_bp.route("/health")
def health() -> Any:
    return jsonify({"status": "ok", "version": "0.3.0-daily-use-features", "timestamp": now_iso()})


@cross_repo_bp.route("/governor")
def governor_pane() -> Any:
    """R0 read-only consolidated signal pane (Fase 1a). No action taken here."""
    from governor.store import SignalStore
    store = SignalStore(GOVERNOR_DB)
    signals = store.latest_per_source()
    return render_template(
        "cr_governor.html",
        signals=signals,
        acted_count=store.acted_on_count(),
        advisory=store.auto_observed_recent(limit=20),
    )


_NOTES_SAFE_REGEX = re.compile(r"^[A-Za-z0-9 .,_/:#\-+()=]{1,200}$")


@cross_repo_bp.route("/api/coord-event", methods=["POST"])
def coord_event_log() -> Any:
    """B1: Invoca scripts/cross-repo/coord-event-log.ps1 -Quiet -NotesQuick <notes>.

    Security (P0.2 harsh-reviewer 2026-05-14 fix):
    includes authentication (via API_SECRET if configured) and notes input
    regex-sanitized to prevent PowerShell command injection (CWE-77/78).
    Blocked chars: backtick (`), dollar ($), parens (), pipe (|), semicolon (;),
    redirect (<>), ampersand (&), quotes ('"), CR/LF, backslash escape sequences.
    Allowed: alphanumeric + space + common punctuation [.,_/:#-+()=].
    """
    api_secret = os.environ.get("API_SECRET")
    if api_secret:
        auth_header = request.headers.get("Authorization", "")
        # Constant-time compare to avoid timing side-channel.
        if not hmac.compare_digest(auth_header, f"Bearer {api_secret}"):
            return jsonify({"ok": False, "error": "unauthorized"}), 401

    notes = (request.json or {}).get("notes", "").strip()
    if not notes:
        return jsonify({"ok": False, "error": "notes required"}), 400
    if not _NOTES_SAFE_REGEX.match(notes):
        return jsonify({
            "ok": False,
            "error": "notes contains disallowed chars (only alphanumeric + space + .,_/:#-+()= allowed, max 200 chars)",
        }), 400
    script_path = CODEMASTERDD_ROOT / "scripts" / "cross-repo" / "coord-event-log.ps1"
    if not script_path.exists():
        return jsonify({"ok": False, "error": "script not found"}), 500
    try:
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path), "-Quiet", "-NotesQuick", notes],
            capture_output=True, text=False, timeout=15, check=False, shell=False,
            creationflags=_NO_WINDOW_FLAG,
        )
        out = result.stdout.decode("utf-8", errors="replace")[-500:]
        err = result.stderr.decode("utf-8", errors="replace")[-500:]
        return jsonify({"ok": result.returncode == 0, "stdout_tail": out, "stderr_tail": err, "returncode": result.returncode})
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}), 500


@cross_repo_bp.route("/api/draft-pr", methods=["POST"])
def draft_pr() -> Any:
    """B2: Invoca scripts/cross-repo/dry-run-pr.ps1 con parametri form.

    Security: includes authentication (via API_SECRET if configured) and regex
    sanitization to prevent PowerShell command injection (CWE-77/78).
    """
    api_secret = os.environ.get("API_SECRET")
    if api_secret:
        auth_header = request.headers.get("Authorization", "")
        # Constant-time compare to avoid timing side-channel (cf. Game-Database #107).
        if not hmac.compare_digest(auth_header, f"Bearer {api_secret}"):
            return jsonify({"ok": False, "error": "unauthorized"}), 401

    data = request.json or {}
    repo_target = data.get("repo_target", "").strip()
    pr_type = data.get("type", "").strip()
    preview_files = data.get("preview_files", "").strip()
    summary = data.get("summary", "").strip()
    if not all([repo_target, pr_type, preview_files, summary]):
        return jsonify({"ok": False, "error": "all 4 fields required"}), 400
    if not _NOTES_SAFE_REGEX.match(preview_files) or not _NOTES_SAFE_REGEX.match(summary):
        return jsonify({
            "ok": False,
            "error": "inputs contain disallowed chars (only alphanumeric + space + .,_/:#-+()= allowed)",
        }), 400
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
            creationflags=_NO_WINDOW_FLAG,
        )
        out = result.stdout.decode("utf-8", errors="replace")
        err = result.stderr.decode("utf-8", errors="replace")[-500:]
        return jsonify({"ok": result.returncode == 0, "draft": out, "stderr_tail": err, "returncode": result.returncode})
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}), 500


@cross_repo_bp.route("/api/open-vscode")
def open_vscode() -> Any:
    """B3: Launch VS Code at given path (validated whitelist).

    Security (P0.3 harsh-reviewer 2026-05-14 fix):
    shell=False (was True, removed -- shell=True with list-args useless on Windows + dangerous
    pattern smell if allowed_paths ever extends with user input).
    Path strictly whitelisted from REPOS local_path + CODEMASTERDD_ROOT.
    """
    path_str = request.args.get("path", "").strip()
    allowed_paths = {str(Path(r["local_path"])) for r in REPOS.values()} | {str(CODEMASTERDD_ROOT)}
    norm_path = str(Path(path_str))
    if norm_path not in allowed_paths:
        return jsonify({"ok": False, "error": "path not whitelisted"}), 400
    try:
        # Find 'code' CLI executable to avoid shell=True
        code_cmd = "code.cmd" if sys.platform == "win32" else "code"
        creationflags = 0x00000008 if sys.platform == "win32" else 0  # DETACHED_PROCESS
        subprocess.Popen([code_cmd, norm_path], shell=False, creationflags=creationflags | _NO_WINDOW_FLAG)
        return jsonify({"ok": True, "opened": norm_path})
    except FileNotFoundError:
        return jsonify({"ok": False, "error": "code CLI not in PATH"}), 500
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}), 500


def create_app() -> Flask:
    """App factory: creates Flask instance and registers the cross-repo blueprint."""
    _app = Flask(__name__)
    _app.register_blueprint(cross_repo_bp, url_prefix='/cross-repo')
    return _app


def run_dev() -> None:
    """Werkzeug dev server (threaded=False per Windows subprocess fix)."""
    _app = create_app()
    _app.run(host="127.0.0.1", port=8081, debug=False, threaded=False)


def run_prod() -> None:
    """Waitress WSGI production server."""
    try:
        from waitress import serve
    except ImportError:
        print("waitress not installed. Install: pip install waitress")
        sys.exit(1)
    print("Cross-repo Dashboard v0.2.0 running on http://127.0.0.1:8081/cross-repo/ (waitress production)")
    serve(create_app(), host="127.0.0.1", port=8081, threads=4)


if __name__ == "__main__":
    if "--prod" in sys.argv:
        run_prod()
    else:
        run_dev()
