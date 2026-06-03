from __future__ import annotations

import base64
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import requests

from governor.parsers import (
    parse_archon_learnings,
    parse_eng_graph_moc,
    parse_game_governance_drift,
    parse_evo_swarm_digest,
    parse_jules_digest,
    parse_sot_drift_issues,
    parse_vault_report,
)

# Source URLs.
GAME_DRIFT_URL = "https://raw.githubusercontent.com/MasterDD-L34D/Game/main/reports/docs/governance_drift_report.json"
EVO_EXPORTS_API = "https://api.github.com/repos/MasterDD-L34D/evo-swarm/contents/docs/exports"
SOT_ISSUES_URL = "https://api.github.com/repos/MasterDD-L34D/Game/issues?labels=sot-drift-candidate&state=open"
VAULT_LINT_API = "https://api.github.com/repos/MasterDD-L34D/vault/contents/Extras/lint-reports"
ENG_GRAPH_MOC_API = "https://api.github.com/repos/MasterDD-L34D/vault/contents/Atlas/engineering-moc.md"
# ARCHON learnings are vendored on GitHub in the vault repo (local aa01 is NON-git).
ARCHON_LEARNINGS_API = "https://api.github.com/repos/MasterDD-L34D/vault/contents/Vault-ops-remote/claude-global/aa01-system/learnings"
# Jules daily-digest dir (codemasterdd's own repo; the G3 cron writes <date>-digest.md here).
JULES_DIGEST_API = "https://api.github.com/repos/MasterDD-L34D/codemasterdd-ai-station/contents/docs/jules-batch"

# 9 sources: 2 Game public + 1 evo private + 3 vault lint + 1 vault eng-graph + 1 archon learnings + 1 jules digest.
SOURCES = [
    {"id": "game-governance-drift", "style": "json"},
    {"id": "game-sot-drift", "style": "gh-issues"},
    {"id": "evo-swarm-digest", "style": "evo-private"},
    {"id": "vault-gap", "style": "vault", "prefix": "gap-", "kind": "gap"},
    {"id": "vault-coherence", "style": "vault", "prefix": "coherence-", "kind": "coherence"},
    {"id": "vault-whatsmissing", "style": "vault", "prefix": "whatsmissing-", "kind": "whatsmissing"},
    {"id": "vault-eng-graph", "style": "vault-fixed", "api_url": ENG_GRAPH_MOC_API},
    {"id": "archon-learnings", "style": "archon-learnings", "api_url": ARCHON_LEARNINGS_API},
    {"id": "jules-digest", "style": "jules-digest", "api_url": JULES_DIGEST_API},
]


def _gh_token() -> str:
    """Token from env, else `gh auth token` (mirrors app.py)."""
    import os
    t = os.environ.get("GH_TOKEN", "").strip() or os.environ.get("GITHUB_TOKEN", "").strip()
    if t:
        return t
    try:
        r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    return ""


def gh_get_json(url: str):
    """GET a GitHub REST endpoint -> parsed JSON. Token via _gh_token (public + private repos)."""
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    tok = _gh_token()
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()


def gh_get_file_content(api_url: str, getter=None) -> str:
    """GET a contents-API file URL -> decoded UTF-8 text (private-repo safe)."""
    getter = getter or gh_get_json
    obj = getter(api_url)
    if isinstance(obj, dict) and obj.get("encoding") == "base64":
        return base64.b64decode(obj.get("content", "")).decode("utf-8", errors="replace")
    raise ValueError("unexpected contents-API response (no base64 content)")


def resolve_latest_in_dir(api_url: str, prefix: str, getter=None) -> str | None:
    """List a contents dir, return the contents-API url of the newest prefix*.md."""
    getter = getter or gh_get_json
    entries = getter(api_url)
    cands = sorted(
        [e for e in (entries or [])
         if str(e.get("name", "")).startswith(prefix) and e.get("name", "").endswith(".md")],
        key=lambda e: e["name"],
    )
    if not cands:
        return None
    return cands[-1].get("url")  # contents-API url of the file


def resolve_latest_digest(api_url: str, getter=None) -> str | None:
    """List the jules-batch dir, return the contents-API url of the newest <date>-digest.md.

    Matches `YYYY-MM-DD-digest.md` ONLY (excludes `suggestions-*.md` etc.); newest by name.
    """
    getter = getter or gh_get_json
    entries = getter(api_url)
    cands = sorted(
        [e for e in (entries or [])
         if re.fullmatch(r"\d{4}-\d{2}-\d{2}-digest\.md", str(e.get("name", "")))],
        key=lambda e: e["name"],
    )
    return cands[-1].get("url") if cands else None


def raw_fetch(url: str) -> str:
    """Anonymous raw fetch (public repos)."""
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text


def _produce(src: dict, fetcher, json_getter, content_getter, now: date | None = None):
    """Fetch + parse one source into a Signal. Raises on failure (caller isolates)."""
    sid, style = src["id"], src["style"]
    if style == "json":
        return parse_game_governance_drift(json.loads(fetcher(GAME_DRIFT_URL)))
    if style == "gh-issues":
        return parse_sot_drift_issues(json_getter(SOT_ISSUES_URL), SOT_ISSUES_URL)
    if style == "evo-private":
        url = resolve_latest_in_dir(EVO_EXPORTS_API, "EXPORT-FOR-GAME-REPO", json_getter)
        if not url:
            raise ValueError("no evo export found")
        return parse_evo_swarm_digest(content_getter(url), url)
    if style == "vault":
        url = resolve_latest_in_dir(VAULT_LINT_API, src["prefix"], json_getter)
        if not url:
            raise ValueError(f"no vault {src['prefix']} report found")
        return parse_vault_report(content_getter(url), source=sid, kind=src["kind"], ref=url)
    if style == "vault-fixed":
        return parse_eng_graph_moc(content_getter(src["api_url"]), src["api_url"], now=now)
    if style == "archon-learnings":
        return parse_archon_learnings(json_getter(src["api_url"]), src["api_url"])
    if style == "jules-digest":
        url = resolve_latest_digest(src["api_url"], json_getter)
        if not url:
            raise ValueError("no jules digest found")
        return parse_jules_digest(content_getter(url), url)
    raise ValueError(f"unknown style {style} for {sid}")


def ingest_all(
    store,
    fetcher=raw_fetch,
    json_getter=gh_get_json,
    content_getter=gh_get_file_content,
    now: date | None = None,
) -> dict:
    ingested = 0
    new = 0
    errors = 0
    now = now or date.today()  # I/O boundary: the clock for staleness-aware sources
    for src in SOURCES:
        try:
            sig = _produce(src, fetcher, json_getter, content_getter, now=now)
            is_new = store.upsert(sig)
            ingested += 1
            if is_new:
                new += 1
                # ADVISORY ONLY -- never read by any autonomy gate.
                store.add_auto_observed(sig.source, "signal-changed", detail=sig.summary)
        except Exception as e:  # noqa: BLE001 -- one bad source must not abort the rest
            errors += 1
            store.add_auto_observed(src["id"], "ingest-error", detail=str(e)[:200])
    return {"ingested": ingested, "new": new, "errors": errors}


def main() -> int:
    from governor.store import SignalStore
    db = Path(__file__).resolve().parent.parent / "governor.db"
    store = SignalStore(db)
    result = ingest_all(store)
    print(f"governor ingest: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
