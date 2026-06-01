from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

from governor.parsers import parse_game_governance_drift, parse_evo_swarm_digest

# Each source: id -> (url, parse-style). URLs overridable by env in Fase-1b.
GAME_DRIFT_URL = "https://raw.githubusercontent.com/MasterDD-L34D/Game/main/reports/docs/governance_drift_report.json"
EVO_DIGEST_URL = "https://raw.githubusercontent.com/MasterDD-L34D/evo-swarm/main/docs/exports/EXPORT-FOR-GAME-REPO-latest.md"

SOURCES = [
    {"id": "game-governance-drift", "url": GAME_DRIFT_URL, "style": "json"},
    {"id": "evo-swarm-digest", "url": EVO_DIGEST_URL, "style": "md"},
]


def raw_fetch(url: str) -> str:
    """Anonymous raw fetch (public repos). Fase-1b adds authed + gh-issue."""
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text


def _parse(source_id: str, style: str, body: str, url: str):
    if source_id == "game-governance-drift":
        return parse_game_governance_drift(json.loads(body))
    if source_id == "evo-swarm-digest":
        return parse_evo_swarm_digest(body, url)
    raise ValueError(f"no parser for {source_id}")


def ingest_all(store, fetcher=raw_fetch) -> dict:
    ingested = 0
    new = 0
    errors = 0
    for src in SOURCES:
        try:
            body = fetcher(src["url"])
            sig = _parse(src["id"], src["style"], body, src["url"])
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
