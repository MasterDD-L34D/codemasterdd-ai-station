"""Migrate markdown dogfood log entries into dogfood.sqlite (U6 BACKLOG).

Usage:
    python scripts/migrate-log-to-sqlite.py --db <path> --log <log.md> [--dry-run]

Reads the LATEST `Cumulative Fase 6 dataset` table in the log markdown
(source of truth for dogfood count + status) and inserts rows into the
entries table of dogfood.sqlite. Token / cost / commit fields are
enriched from a hardcoded per-dogfood dict (parsed from narrative
sections during April 2026 dogfood window); unknown entries default
to zero/None.

Safe to re-run: uses idempotency check (match on task_description +
classe + stack) to skip duplicates. Use --force to override.

Exit codes:
    0 success (or dry-run)
    1 config error (missing args, unreadable log)
    2 parse error (no cumulative table found, malformed rows)
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


OUTCOME_MAP = {
    "✅": "success",
    "✅ (rescue)": "success",
    "🟡 **partial** (1/2)": "partial",
    "🟡 **partial**": "partial",
    "❌ **REJECT**": "reject",
}


ENRICHMENT: dict[int, dict[str, Any]] = {
    1:  {"tokens_sent": 1800, "tokens_received": 632,  "cost_usd": 0.0,    "commit_hash": "f087e52", "created_at": "2026-04-22T11:58:00+00:00"},
    2:  {"tokens_sent": 2200, "tokens_received": 1300, "cost_usd": 0.0,    "commit_hash": "5cb44de", "created_at": "2026-04-22T17:23:00+00:00"},
    3:  {"tokens_sent": 2300, "tokens_received": 1100, "cost_usd": 0.0,    "commit_hash": "c672e1a", "created_at": "2026-04-22T19:30:00+00:00"},
    4:  {"tokens_sent": 4900, "tokens_received": 488,  "cost_usd": 0.0033, "commit_hash": None,      "created_at": "2026-04-22T23:45:00+00:00"},
    5:  {"tokens_sent": 4200, "tokens_received": 150,  "cost_usd": 0.0026, "commit_hash": None,      "created_at": "2026-04-23T00:30:00+00:00"},
    6:  {"tokens_sent": 4300, "tokens_received": 587,  "cost_usd": 0.0030, "commit_hash": None,      "created_at": "2026-04-23T01:15:00+00:00"},
    7:  {"tokens_sent": 8600, "tokens_received": 1000, "cost_usd": 0.0059, "commit_hash": "f80ab3c", "created_at": "2026-04-23T22:00:00+00:00",
         "note_extra": "REJECT 5 constraint violations; rescue manual"},
    8:  {"tokens_sent": 3000, "tokens_received": 200,  "cost_usd": 0.0,    "commit_hash": "2dccec7", "created_at": "2026-04-23T22:15:00+00:00"},
    9:  {"tokens_sent": 7000, "tokens_received": 282,  "cost_usd": 0.0,    "commit_hash": "0fa0016", "created_at": "2026-04-24T01:45:00+00:00"},
    10: {"tokens_sent": 7000, "tokens_received": 169,  "cost_usd": 0.0,    "commit_hash": "3156edf", "created_at": "2026-04-24T02:10:00+00:00"},
    11: {"tokens_sent": 5300, "tokens_received": 656,  "cost_usd": 0.0,    "commit_hash": "3231e2e", "created_at": "2026-04-24T02:25:00+00:00"},
    12: {"tokens_sent": 9000, "tokens_received": 854,  "cost_usd": 0.0,    "commit_hash": "dce8ee4", "created_at": "2026-04-24T03:50:00+00:00",
         "note_extra": "inherited-bug-as-smell; rescue 410db7f"},
}


CONSTRAINT_COUNT: dict[int, int] = {
    1: 1, 2: 1, 3: 1, 4: 1, 5: 1,
    6: 3, 7: 5, 8: 2, 9: 2, 10: 3, 11: 1, 12: 4,
}


SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at        TEXT NOT NULL,
    task_description  TEXT NOT NULL,
    classe            TEXT NOT NULL,
    stack             TEXT NOT NULL,
    constraint_count  INTEGER NOT NULL DEFAULT 0,
    outcome           TEXT NOT NULL,
    retry_count       INTEGER NOT NULL DEFAULT 0,
    tokens_sent       INTEGER NOT NULL DEFAULT 0,
    tokens_received   INTEGER NOT NULL DEFAULT 0,
    cost_usd          REAL NOT NULL DEFAULT 0,
    commit_hash       TEXT,
    note              TEXT,
    langfuse_trace_id TEXT
);
CREATE INDEX IF NOT EXISTS idx_entries_created_at ON entries(created_at);
CREATE INDEX IF NOT EXISTS idx_entries_classe ON entries(classe);
CREATE INDEX IF NOT EXISTS idx_entries_stack ON entries(stack);
CREATE INDEX IF NOT EXISTS idx_entries_outcome ON entries(outcome);
"""


def strip_md_emphasis(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    return s.strip()


def parse_retry(s: str) -> int:
    s = strip_md_emphasis(s)
    m = re.match(r"(\d+)", s)
    return int(m.group(1)) if m else 0


def map_outcome(raw: str) -> str:
    raw = raw.strip()
    for k, v in OUTCOME_MAP.items():
        if k in raw:
            return v
    if "✅" in raw:
        return "success"
    if "🟡" in raw or "partial" in raw.lower():
        return "partial"
    if "❌" in raw or "REJECT" in raw:
        return "reject"
    return "unknown"


def normalize_stack(raw: str) -> str:
    raw = strip_md_emphasis(raw).lower()
    if "7b" in raw and "local" in raw:
        return "7B-local-whole"
    if "14b" in raw and ("q2" in raw or "q_2" in raw):
        return "14B-Q2-local-diff"
    if "groq" in raw and "70b" in raw:
        return "groq-70B-wrapper"
    if "groq" in raw:
        return "groq-70B"
    return raw.replace(" ", "-")


def normalize_classe(raw: str) -> str:
    raw = strip_md_emphasis(raw).lower().strip()
    if "cosmetic" in raw:
        return "cosmetic"
    if "behavior" in raw:
        return "behavior"
    if "strategic" in raw:
        return "strategic"
    return raw


def extract_cumulative_table(md_text: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"###\s+Cumulative Fase 6 dataset[^\n]*\n\s*\n"
        r"\|\s*#\s*\|\s*Task\s*\|\s*Classe\s*\|\s*Stack\s*\|\s*Retry\s*\|\s*Success\s*\|\s*Note\s*\|\s*\n"
        r"\|[-\s|]+\|\s*\n"
        r"((?:\|[^\n]+\|\s*\n)+)",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(md_text))
    if not matches:
        raise ValueError("No 'Cumulative Fase 6 dataset' table found in markdown")
    last = matches[-1]
    body = last.group(1)
    rows: list[dict[str, Any]] = []
    for line in body.strip().split("\n"):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            continue
        try:
            dogfood_id = int(strip_md_emphasis(cells[0]))
        except ValueError:
            continue
        rows.append({
            "id": dogfood_id,
            "task": strip_md_emphasis(cells[1]),
            "classe_raw": cells[2],
            "stack_raw": cells[3],
            "retry_raw": cells[4],
            "outcome_raw": cells[5],
            "note": strip_md_emphasis(cells[6]),
        })
    return rows


def build_entry(row: dict[str, Any]) -> dict[str, Any]:
    did = row["id"]
    enrich = ENRICHMENT.get(did, {})
    note = row["note"]
    if enrich.get("note_extra"):
        note = f"{note} | {enrich['note_extra']}"
    return {
        "created_at": enrich.get("created_at") or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "task_description": f"#{did} {row['task']}",
        "classe": normalize_classe(row["classe_raw"]),
        "stack": normalize_stack(row["stack_raw"]),
        "constraint_count": CONSTRAINT_COUNT.get(did, 0),
        "outcome": map_outcome(row["outcome_raw"]),
        "retry_count": parse_retry(row["retry_raw"]),
        "tokens_sent": enrich.get("tokens_sent", 0),
        "tokens_received": enrich.get("tokens_received", 0),
        "cost_usd": enrich.get("cost_usd", 0.0),
        "commit_hash": enrich.get("commit_hash"),
        "note": note,
        "langfuse_trace_id": None,
    }


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)


def insert_entry(conn: sqlite3.Connection, e: dict[str, Any]) -> int:
    cur = conn.execute(
        """
        INSERT INTO entries
            (created_at, task_description, classe, stack, constraint_count,
             outcome, retry_count, tokens_sent, tokens_received, cost_usd,
             commit_hash, note, langfuse_trace_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            e["created_at"], e["task_description"], e["classe"], e["stack"],
            e["constraint_count"], e["outcome"], e["retry_count"],
            e["tokens_sent"], e["tokens_received"], e["cost_usd"],
            e["commit_hash"], e["note"], e["langfuse_trace_id"],
        ),
    )
    return cur.lastrowid or 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", required=True, type=Path, help="Absolute path to dogfood.sqlite")
    parser.add_argument("--log", required=True, type=Path, help="Absolute path to aider-delegation-YYYY-MM.md")
    parser.add_argument("--dry-run", action="store_true", help="Parse + preview only, no DB write")
    parser.add_argument("--force", action="store_true", help="Insert even if duplicate detected")
    args = parser.parse_args(argv)

    if not args.log.exists():
        print(f"ERROR: log file not found: {args.log}", file=sys.stderr)
        return 1

    md = args.log.read_text(encoding="utf-8")

    try:
        rows = extract_cumulative_table(md)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    entries = [build_entry(r) for r in rows]
    print(f"Parsed {len(entries)} entries from {args.log.name}")
    for e in entries:
        print(f"  [{e['outcome']:8s}] {e['task_description'][:60]:60s} | "
              f"{e['classe']:9s} | {e['stack']:20s} | c={e['constraint_count']} | "
              f"${e['cost_usd']:.4f} | {e['commit_hash'] or '-'}")

    if args.dry_run:
        print("\n--dry-run mode: DB untouched.")
        return 0

    args.db.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(args.db, isolation_level=None) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL")
        init_db(conn)

        existing_entries = set()
        if not args.force:
            cur = conn.execute("SELECT task_description, classe, stack FROM entries")
            for row in cur:
                existing_entries.add((row["task_description"], row["classe"], row["stack"]))

        inserted = 0
        skipped = 0
        for e in entries:
            entry_key = (e["task_description"], e["classe"], e["stack"])
            if not args.force and entry_key in existing_entries:
                skipped += 1
                continue

            insert_entry(conn, e)
            if not args.force:
                existing_entries.add(entry_key)
            inserted += 1
        print(f"\nDB: {args.db}")
        print(f"Inserted: {inserted}  Skipped (duplicates): {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
