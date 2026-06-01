from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

from governor.parsers import parse_game_governance_drift, parse_evo_swarm_digest, parse_sot_drift_issues

# Each source: id -> (url, parse-style). URLs overridable by env in Fase-1b.
GAME_DRIFT_URL = "https://raw.githubusercontent.com/MasterDD-L34D/Game/main/reports/docs/governance_drift_report.json"
EVO_EXPORTS_API = "https://api.github.com/repos/MasterDD-L34D/evo-swarm/contents/docs/exports"
EVO_RAW_BASE = "https://raw.githubusercontent.com/MasterDD-L34D/evo-swarm/main/docs/exports/"
SOT_ISSUES_URL = "https://api.github.com/repos/MasterDD-L34D/Game/issues?labels=sot-drift-candidate&state=open"


def gh_get_json(url: str):
    """GET a GitHub REST endpoint -> parsed JSON. Token optional (public repos)."""
    import os
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    tok = os.environ.get("GH_TOKEN", "").strip()
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()


def resolve_evo_latest_url(lister=gh_get_json) -> str | None:
    """List the exports dir, return the raw URL of the newest dated digest."""
    entries = lister(EVO_EXPORTS_API)
    names = sorted(
        e["name"] for e in (entries or [])
        if str(e.get("name", "")).startswith("EXPORT-FOR-GAME-REPO") and e["name"].endswith(".md")
    )
    if not names:
        return None
    return EVO_RAW_BASE + names[-1]

# evo-swarm deferred to Fase-1c (PRIVATE repo -> needs authed-contents-fetch, like vault)
SOURCES = [
    {"id": "game-governance-drift", "style": "json"},
    {"id": "game-sot-drift", "style": "gh-issues"},
]


def raw_fetch(url: str) -> str:
    """Anonymous raw fetch (public repos). Fase-1b adds authed + gh-issue."""
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text


def _produce(source_id: str, style: str, fetcher, json_getter):
    """Fetch + parse one source into a Signal. Raises on failure (caller isolates)."""
    if style == "json":
        body = fetcher(GAME_DRIFT_URL)
        return parse_game_governance_drift(json.loads(body))
    if style == "evo-dynamic":
        url = resolve_evo_latest_url(json_getter) or (EVO_RAW_BASE + "EXPORT-FOR-GAME-REPO-latest.md")
        return parse_evo_swarm_digest(fetcher(url), url)
    if style == "gh-issues":
        issues = json_getter(SOT_ISSUES_URL)
        return parse_sot_drift_issues(issues, SOT_ISSUES_URL)
    raise ValueError(f"unknown style {style} for {source_id}")


def ingest_all(store, fetcher=raw_fetch, json_getter=gh_get_json) -> dict:
    ingested = 0
    new = 0
    errors = 0
    for src in SOURCES:
        try:
            sig = _produce(src["id"], src["style"], fetcher, json_getter)
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
