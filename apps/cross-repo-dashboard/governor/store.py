from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

_SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    source       TEXT NOT NULL,
    kind         TEXT NOT NULL,
    severity     TEXT NOT NULL,
    summary      TEXT NOT NULL,
    counts_json  TEXT NOT NULL DEFAULT '{}',
    produced_at  TEXT,
    ref          TEXT NOT NULL DEFAULT '',
    payload_hash TEXT NOT NULL,
    fetched_at   TEXT NOT NULL,
    UNIQUE (source, payload_hash)
);
CREATE TABLE IF NOT EXISTS acted_on (
    source       TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    acted_at     TEXT NOT NULL,
    note         TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (source, payload_hash)
);
CREATE TABLE IF NOT EXISTS auto_observed (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    observed_at  TEXT NOT NULL,
    source       TEXT NOT NULL,
    event        TEXT NOT NULL,
    detail       TEXT NOT NULL DEFAULT ''
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class SignalStore:
    """SQLite persistence for normalized signals. Single-writer, WAL.

    The `auto_observed` table is ADVISORY ONLY -- it is never read by any
    autonomy-promotion gate (see actor-activation-criteria.md sec 4).
    """

    def __init__(self, db_path):
        self.db_path = str(db_path)
        with self._connect() as c:
            c.executescript(_SCHEMA)

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def upsert(self, sig) -> bool:
        """Insert the signal. Returns True if (source, payload_hash) is new."""
        with self._connect() as c:
            exists = c.execute(
                "SELECT 1 FROM signals WHERE source=? AND payload_hash=?",
                (sig.source, sig.payload_hash),
            ).fetchone()
            if exists:
                return False
            c.execute(
                "INSERT INTO signals (source, kind, severity, summary, counts_json, "
                "produced_at, ref, payload_hash, fetched_at) VALUES (?,?,?,?,?,?,?,?,?)",
                (sig.source, sig.kind, sig.severity, sig.summary,
                 json.dumps(sig.counts), sig.produced_at, sig.ref,
                 sig.payload_hash, _now()),
            )
            return True

    def latest_per_source(self) -> list:
        """Most-recently-inserted signal per source.

        Ordered by the monotonic rowid (id) rather than only fetched_at, so two
        upserts within the same wall-clock second still resolve to a single,
        deterministic latest row per source.
        """
        with self._connect() as c:
            rows = c.execute(
                "SELECT s.* FROM signals s "
                "JOIN (SELECT source, MAX(id) AS mx FROM signals GROUP BY source) m "
                "ON s.source=m.source AND s.id=m.mx ORDER BY s.source"
            ).fetchall()
            out = []
            for r in rows:
                d = dict(r)
                d["counts"] = json.loads(d.pop("counts_json") or "{}")
                out.append(d)
            return out

    def record_acted_on(self, source: str, payload_hash: str, note: str = "") -> None:
        with self._connect() as c:
            c.execute(
                "INSERT OR IGNORE INTO acted_on (source, payload_hash, acted_at, note) "
                "VALUES (?,?,?,?)",
                (source, payload_hash, _now(), note),
            )

    def acted_on_count(self, since_iso: str | None = None) -> int:
        with self._connect() as c:
            if since_iso:
                row = c.execute(
                    "SELECT COUNT(*) AS n FROM acted_on WHERE acted_at >= ?",
                    (since_iso,),
                ).fetchone()
            else:
                row = c.execute("SELECT COUNT(*) AS n FROM acted_on").fetchone()
            return int(row["n"])

    def add_auto_observed(self, source: str, event: str, detail: str = "") -> None:
        with self._connect() as c:
            c.execute(
                "INSERT INTO auto_observed (observed_at, source, event, detail) "
                "VALUES (?,?,?,?)",
                (_now(), source, event, detail),
            )

    def auto_observed_recent(self, limit: int = 20) -> list:
        with self._connect() as c:
            rows = c.execute(
                "SELECT * FROM auto_observed ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]
    def previous_severity(self, source: str) -> 'str | None':
        """Return the severity of the SECOND-most-recent signals row for this source.

        Ordered by monotonic id (descending).  Returns None if fewer than 2 rows exist
        for this source.
        """
        with self._connect() as c:
            row = c.execute(
                "SELECT severity FROM signals WHERE source=? ORDER BY id DESC LIMIT 1 OFFSET 1",
                (source,),
            ).fetchone()
            if row is None:
                return None
            return row["severity"]
