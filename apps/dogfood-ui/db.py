"""SQLite abstraction per dogfood-ui."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


class Database:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    def init_schema(self) -> None:
        with self.connect() as c:
            c.executescript(SCHEMA)

    def insert_entry(self, payload: dict[str, Any]) -> int:
        valid_classes = {'cosmetic', 'behavior', 'strategic'}
        if payload['classe'] not in valid_classes:
            raise ValueError(f"Invalid classe: {payload['classe']}. Must be one of {valid_classes}")

        valid_stacks = {'7B-local', '14B-Q2-local', '30B-MoE-local', 'groq-70b', 'cerebras-8b', 'gemini-flash', 'openai-mini', 'claude'}
        if payload['stack'] not in valid_stacks:
            raise ValueError(f"Invalid stack: {payload['stack']}. Must be one of {valid_stacks}")

        now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with self.connect() as c:
            cur = c.execute(
                """
                INSERT INTO entries
                    (created_at, task_description, classe, stack, constraint_count,
                     outcome, retry_count, tokens_sent, tokens_received, cost_usd,
                     commit_hash, note, langfuse_trace_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now_iso,
                    payload.get("task_description", ""),
                    payload.get("classe", ""),
                    payload.get("stack", ""),
                    int(payload.get("constraint_count", 0) or 0),
                    payload.get("outcome", ""),
                    int(payload.get("retry_count", 0) or 0),
                    int(payload.get("tokens_sent", 0) or 0),
                    int(payload.get("tokens_received", 0) or 0),
                    float(payload.get("cost_usd", 0) or 0),
                    payload.get("commit_hash", ""),
                    payload.get("note", ""),
                    payload.get("langfuse_trace_id", ""),
                ),
            )
            return cur.lastrowid or 0

    def list_entries(self, limit: int = 500) -> list[sqlite3.Row]:
        with self.connect() as c:
            cur = c.execute(
                "SELECT * FROM entries ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            return cur.fetchall()

    def delete_entry(self, entry_id: int) -> None:
        with self.connect() as c:
            c.execute("DELETE FROM entries WHERE id = ?", (entry_id,))

    def health(self) -> dict[str, Any]:
        with self.connect() as c:
            cur = c.execute("SELECT COUNT(*) AS n FROM entries")
            row = cur.fetchone()
            return {
                "path": str(self.path),
                "exists": self.path.exists(),
                "count": row["n"] if row else 0,
            }
