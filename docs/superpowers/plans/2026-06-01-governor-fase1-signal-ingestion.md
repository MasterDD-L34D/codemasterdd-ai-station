# Governor Fase 1a -- Signal Ingestion (R0 observability) Implementation Plan

> **Status (2026-06-23):** shipped -- governor signal-ingestion live

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add R0 (report-only) signal ingestion to the cross-repo-dashboard: persist a normalized view of two public island signals into SQLite and render a read-only consolidated pane, with an advisory auto-observed log that is SEVERED from every autonomy gate.

**Architecture:** A new `governor/` package inside `apps/cross-repo-dashboard/`. Pure-stdlib `Signal` model + per-source parsers (no I/O, fixture-tested) feed a `SignalStore` (sqlite3, WAL). A thin fetch layer (reuses `requests`, mockable) orchestrates ingest. The Flask blueprint gains one read-only route rendering the latest signal per source. No actor, no PR, no auto-merge -- this is the rung-0 substrate + the off-ramp experiment (4 weeks -> count acted-on >= 3 before Fase 2).

**Tech Stack:** Python 3.13, Flask (blueprint, already present), sqlite3 (stdlib), pytest + monkeypatch (existing conftest mocks requests/flask at function scope), `requests` for fetch.

**Spec:** `docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md`. **Doctrine:** ADR-0036 (Accepted spine) + `docs/governance/actor-activation-criteria.md` (R0 active, all else gated).

**Scope (Fase-1a vs 1b):** This plan ships the foundation + the two PUBLIC-anon raw-fetch signals only (Game `governance_drift_report.json` JSON; evo-swarm digest markdown). Deferred to a Fase-1b plan/PR: the private-authed vault signals (gap/coherence/whats_missing -- need GH_TOKEN raw-fetch), the gh-issue-polled `sot-drift-sentinel`, and ARCHON learnings. Each Fase-1b adapter reuses the parser+store pattern established here; their exact schemas are recorded in the spec + the ground-truth map. Keeping each PR reviewable (no big-bang).

**Verified signal schemas (ground-truth 2026-06-01):**
- Game `governance_drift_report.json` (public, raw-fetchable): `{generated_at: ISO, summary: {total: int, errors: int, warnings: int}, issues: [{level, code, path, message}]}`. URL: `https://raw.githubusercontent.com/MasterDD-L34D/Game/main/reports/docs/governance_drift_report.json`.
- evo-swarm digest (public, raw-fetchable): markdown `# Evo-Swarm -> Game Repo Digest -- YYYY-MM-DD`, with a line `**Cicli inclusi**: N entry ...` and a `### Coverage gap (N entry)` header. URL: `https://raw.githubusercontent.com/MasterDD-L34D/evo-swarm/main/docs/exports/EXPORT-FOR-GAME-REPO-<date>.md` (date varies; the ingest config pins the latest known or uses a directory listing in Fase-1b -- for 1a the URL is a configured constant overridable by env).

---

## File Structure

- Create: `apps/cross-repo-dashboard/governor/__init__.py` -- package marker + public exports.
- Create: `apps/cross-repo-dashboard/governor/signals.py` -- `Signal` dataclass + `make_hash` + `severity_from_counts`. Pure, stdlib only.
- Create: `apps/cross-repo-dashboard/governor/store.py` -- `SignalStore` (sqlite3 WAL): `upsert`, `latest_per_source`, `record_acted_on`, `acted_on_count`, `add_auto_observed`, `auto_observed_recent`.
- Create: `apps/cross-repo-dashboard/governor/parsers.py` -- pure `parse_game_governance_drift(dict) -> Signal`, `parse_evo_swarm_digest(str, ref) -> Signal`.
- Create: `apps/cross-repo-dashboard/governor/ingest.py` -- `SOURCES` config, `raw_fetch(url)`, `ingest_all(store, fetcher)`, `__main__` entry.
- Modify: `apps/cross-repo-dashboard/app.py` -- add `/governor` read-only route + `GOVERNOR_DB` path constant.
- Create: `apps/cross-repo-dashboard/templates/cr_governor.html` -- read-only pane.
- Modify: `.gitignore` -- ignore `governor.db*`.
- Create tests: `tests/test_governor_signals.py`, `tests/test_governor_store.py`, `tests/test_governor_parsers.py`, `tests/test_governor_ingest.py`.
- Create fixtures: `tests/fixtures/governance_drift_report.json`, `tests/fixtures/evo_swarm_digest.md`.

All paths relative to `apps/cross-repo-dashboard/` unless noted. Run tests from repo root: `python -m pytest apps/cross-repo-dashboard/ -v`.

---

## Task 1: Signal model (pure)

**Files:**
- Create: `apps/cross-repo-dashboard/governor/__init__.py`
- Create: `apps/cross-repo-dashboard/governor/signals.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_signals.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_governor_signals.py
def test_make_hash_stable_and_order_sensitive():
    from governor.signals import make_hash
    assert make_hash("a", "b") == make_hash("a", "b")
    assert make_hash("a", "b") != make_hash("b", "a")
    assert len(make_hash("x")) == 16

def test_severity_from_counts():
    from governor.signals import severity_from_counts
    assert severity_from_counts(0, 0) == "ok"
    assert severity_from_counts(0, 5) == "warning"
    assert severity_from_counts(2, 5) == "error"

def test_signal_is_frozen_and_has_fields():
    from governor.signals import Signal
    s = Signal(source="x", kind="drift", severity="ok", summary="fine")
    assert s.counts == {}
    assert s.produced_at is None
    import dataclasses
    assert dataclasses.is_dataclass(s)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_signals.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'governor'`

- [ ] **Step 3: Write minimal implementation**

```python
# governor/__init__.py
"""Unified fleet governor -- R0 signal ingestion (Fase 1a). Report-only."""
```

```python
# governor/signals.py
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Signal:
    """Normalized cross-island signal record (R0 -- no action attached)."""
    source: str            # stable id, e.g. "game-governance-drift"
    kind: str              # "drift" | "gap" | "coherence" | "digest" | "learning" | "sot-drift"
    severity: str          # "error" | "warning" | "info" | "ok"
    summary: str           # one-line human summary
    counts: dict[str, int] = field(default_factory=dict)
    produced_at: str | None = None   # ISO timestamp from the artifact, if any
    ref: str = ""          # url / path / issue ref
    payload_hash: str = "" # change-detect / dedup key


def make_hash(*parts: str) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update((p or "").encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()[:16]


def severity_from_counts(errors: int, warnings: int) -> str:
    if errors > 0:
        return "error"
    if warnings > 0:
        return "warning"
    return "ok"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_signals.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add apps/cross-repo-dashboard/governor/__init__.py apps/cross-repo-dashboard/governor/signals.py apps/cross-repo-dashboard/tests/test_governor_signals.py
git commit -F - <<'EOF'
feat(governor): add normalized Signal model + hash/severity helpers

Fase 1a foundation (R0). Pure stdlib, no I/O.

Coding-Agent: claude-opus-4.8
Trace-Id: <GENERATE-uuidv7>
EOF
```

(Generate the Trace-Id per `scripts/fleet/journal-land.ps1` `New-TraceId`, or any uuidv7. NO `Co-Authored-By`.)

---

## Task 2: SignalStore (SQLite, WAL)

**Files:**
- Create: `apps/cross-repo-dashboard/governor/store.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_store.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_governor_store.py
def test_upsert_new_returns_true_then_false_on_same_hash(tmp_path):
    from governor.store import SignalStore
    from governor.signals import Signal
    store = SignalStore(tmp_path / "g.db")
    sig = Signal(source="s1", kind="drift", severity="warning",
                 summary="297 warnings", counts={"warnings": 297},
                 produced_at="2026-05-25T07:19:51+00:00", ref="url", payload_hash="h1")
    assert store.upsert(sig) is True      # new
    assert store.upsert(sig) is False     # unchanged (same source+hash)

def test_upsert_changed_hash_returns_true_and_latest_reflects_it(tmp_path):
    from governor.store import SignalStore
    from governor.signals import Signal
    store = SignalStore(tmp_path / "g.db")
    store.upsert(Signal(source="s1", kind="drift", severity="ok", summary="old", payload_hash="h1"))
    store.upsert(Signal(source="s1", kind="drift", severity="error", summary="new", payload_hash="h2"))
    rows = store.latest_per_source()
    assert len(rows) == 1
    assert rows[0]["summary"] == "new"
    assert rows[0]["severity"] == "error"

def test_latest_per_source_one_row_per_source(tmp_path):
    from governor.store import SignalStore
    from governor.signals import Signal
    store = SignalStore(tmp_path / "g.db")
    store.upsert(Signal(source="a", kind="gap", severity="ok", summary="A", payload_hash="1"))
    store.upsert(Signal(source="b", kind="digest", severity="info", summary="B", payload_hash="2"))
    sources = {r["source"] for r in store.latest_per_source()}
    assert sources == {"a", "b"}

def test_acted_on_count(tmp_path):
    from governor.store import SignalStore
    store = SignalStore(tmp_path / "g.db")
    assert store.acted_on_count() == 0
    store.record_acted_on("s1", "h1", note="merged PR")
    store.record_acted_on("s1", "h1", note="dup ignored")  # same key, idempotent
    store.record_acted_on("s2", "h9")
    assert store.acted_on_count() == 2

def test_auto_observed_is_separate_and_listable(tmp_path):
    from governor.store import SignalStore
    store = SignalStore(tmp_path / "g.db")
    store.add_auto_observed("s1", "signal-unconsumed", detail="new drift")
    recent = store.auto_observed_recent(limit=5)
    assert len(recent) == 1
    assert recent[0]["event"] == "signal-unconsumed"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_store.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'governor.store'`

- [ ] **Step 3: Write minimal implementation**

```python
# governor/store.py
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

_SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
    source       TEXT NOT NULL,
    kind         TEXT NOT NULL,
    severity     TEXT NOT NULL,
    summary      TEXT NOT NULL,
    counts_json  TEXT NOT NULL DEFAULT '{}',
    produced_at  TEXT,
    ref          TEXT NOT NULL DEFAULT '',
    payload_hash TEXT NOT NULL,
    fetched_at   TEXT NOT NULL,
    PRIMARY KEY (source, payload_hash)
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

    def latest_per_source(self) -> list[dict]:
        """Most-recently-fetched signal per source."""
        with self._connect() as c:
            rows = c.execute(
                "SELECT s.* FROM signals s "
                "JOIN (SELECT source, MAX(fetched_at) AS mx FROM signals GROUP BY source) m "
                "ON s.source=m.source AND s.fetched_at=m.mx ORDER BY s.source"
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

    def auto_observed_recent(self, limit: int = 20) -> list[dict]:
        with self._connect() as c:
            rows = c.execute(
                "SELECT * FROM auto_observed ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_store.py -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Commit**

```bash
git add apps/cross-repo-dashboard/governor/store.py apps/cross-repo-dashboard/tests/test_governor_store.py
git commit -F - <<'EOF'
feat(governor): add SignalStore (sqlite WAL) with advisory log severed from gates

signals + acted_on + auto_observed tables. acted_on_count is the off-ramp
metric; auto_observed is advisory-only (never gates autonomy).

Coding-Agent: claude-opus-4.8
Trace-Id: <GENERATE-uuidv7>
EOF
```

---

## Task 3: Game governance-drift parser (pure, fixture-tested)

**Files:**
- Create: `apps/cross-repo-dashboard/governor/parsers.py`
- Create: `apps/cross-repo-dashboard/tests/fixtures/governance_drift_report.json`
- Test: `apps/cross-repo-dashboard/tests/test_governor_parsers.py`

- [ ] **Step 1: Create the fixture (real shape)**

```json
{
  "generated_at": "2026-05-25T07:19:51+00:00",
  "summary": { "total": 297, "errors": 0, "warnings": 297 },
  "issues": [
    { "level": "warning", "code": "stale_document", "path": "AGENTS.md", "message": "Documento stale" },
    { "level": "warning", "code": "frontmatter_registry_mismatch", "path": "docs/x.md", "message": "mismatch" }
  ]
}
```

- [ ] **Step 2: Write the failing test**

```python
# tests/test_governor_parsers.py
import json
from pathlib import Path

_FIX = Path(__file__).resolve().parent / "fixtures"

def test_parse_game_governance_drift():
    from governor.parsers import parse_game_governance_drift
    raw = json.loads((_FIX / "governance_drift_report.json").read_text(encoding="utf-8"))
    sig = parse_game_governance_drift(raw)
    assert sig.source == "game-governance-drift"
    assert sig.kind == "drift"
    assert sig.severity == "warning"          # 0 errors, 297 warnings
    assert sig.counts == {"total": 297, "errors": 0, "warnings": 297}
    assert sig.produced_at == "2026-05-25T07:19:51+00:00"
    assert "297" in sig.summary
    assert sig.payload_hash != ""

def test_parse_game_governance_drift_errors_make_error_severity():
    from governor.parsers import parse_game_governance_drift
    sig = parse_game_governance_drift(
        {"generated_at": "2026-01-01T00:00:00+00:00",
         "summary": {"total": 3, "errors": 3, "warnings": 0}, "issues": []})
    assert sig.severity == "error"

def test_parse_game_governance_drift_handles_missing_summary():
    from governor.parsers import parse_game_governance_drift
    sig = parse_game_governance_drift({})
    assert sig.severity == "ok"
    assert sig.counts == {"total": 0, "errors": 0, "warnings": 0}
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_parsers.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'governor.parsers'`

- [ ] **Step 4: Write minimal implementation**

```python
# governor/parsers.py
from __future__ import annotations

from governor.signals import Signal, make_hash, severity_from_counts


def parse_game_governance_drift(raw: dict) -> Signal:
    summary = (raw or {}).get("summary") or {}
    total = int(summary.get("total", 0) or 0)
    errors = int(summary.get("errors", 0) or 0)
    warnings = int(summary.get("warnings", 0) or 0)
    produced_at = (raw or {}).get("generated_at")
    severity = severity_from_counts(errors, warnings)
    summary_text = f"{errors} errors, {warnings} warnings ({total} total)"
    return Signal(
        source="game-governance-drift",
        kind="drift",
        severity=severity,
        summary=summary_text,
        counts={"total": total, "errors": errors, "warnings": warnings},
        produced_at=produced_at,
        ref="https://raw.githubusercontent.com/MasterDD-L34D/Game/main/reports/docs/governance_drift_report.json",
        payload_hash=make_hash(str(produced_at), str(total), str(errors), str(warnings)),
    )
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_parsers.py -v`
Expected: PASS (3 tests)

- [ ] **Step 6: Commit**

```bash
git add apps/cross-repo-dashboard/governor/parsers.py apps/cross-repo-dashboard/tests/fixtures/governance_drift_report.json apps/cross-repo-dashboard/tests/test_governor_parsers.py
git commit -F - <<'EOF'
feat(governor): add Game governance-drift parser (pure, fixture-tested)

Coding-Agent: claude-opus-4.8
Trace-Id: <GENERATE-uuidv7>
EOF
```

---

## Task 4: evo-swarm digest parser (pure, fixture-tested)

**Files:**
- Modify: `apps/cross-repo-dashboard/governor/parsers.py`
- Create: `apps/cross-repo-dashboard/tests/fixtures/evo_swarm_digest.md`
- Modify: `apps/cross-repo-dashboard/tests/test_governor_parsers.py`

- [ ] **Step 1: Create the fixture (real shape)**

```markdown
# Evo-Swarm -> Game Repo Digest -- 2026-05-27

> Source: `camel-agents/artifacts/cycle-log.md`.
**Finestra**: dal 2026-05-20 a oggi.
**Cicli inclusi**: 7 entry significative (esiti ok/idea/branch/up).

## TL;DR per Game team
qualcosa.

### Coverage gap (3 entry)
- `slug-a` (IT: ...) -- fonte: biomes_expansion.yaml
- `slug-b` -- fonte: x
- `slug-c` -- fonte: y
```

- [ ] **Step 2: Write the failing test (append to test_governor_parsers.py)**

```python
def test_parse_evo_swarm_digest():
    from governor.parsers import parse_evo_swarm_digest
    md = (_FIX / "evo_swarm_digest.md").read_text(encoding="utf-8")
    ref = "https://raw.githubusercontent.com/MasterDD-L34D/evo-swarm/main/docs/exports/EXPORT-FOR-GAME-REPO-2026-05-27.md"
    sig = parse_evo_swarm_digest(md, ref)
    assert sig.source == "evo-swarm-digest"
    assert sig.kind == "digest"
    assert sig.counts.get("cycles") == 7
    assert sig.counts.get("coverage_gaps") == 3
    assert sig.produced_at == "2026-05-27"
    assert sig.severity in {"info", "ok"}
    assert sig.ref == ref
    assert sig.payload_hash != ""

def test_parse_evo_swarm_digest_missing_numbers_safe():
    from governor.parsers import parse_evo_swarm_digest
    sig = parse_evo_swarm_digest("# Evo-Swarm -> Game Repo Digest -- 2026-06-01\nno numbers here", "r")
    assert sig.counts.get("cycles") == 0
    assert sig.counts.get("coverage_gaps") == 0
    assert sig.produced_at == "2026-06-01"
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_parsers.py -k evo_swarm -v`
Expected: FAIL with `AttributeError`/`ImportError` (parse_evo_swarm_digest not defined)

- [ ] **Step 4: Write minimal implementation (append to parsers.py)**

```python
import re

_RE_DATE = re.compile(r"Digest\s*--\s*(\d{4}-\d{2}-\d{2})")
_RE_CYCLES = re.compile(r"Cicli inclusi\**:\s*(\d+)", re.IGNORECASE)
_RE_GAPS = re.compile(r"Coverage gap\s*\((\d+)\s+entry\)", re.IGNORECASE)


def _first_int(rx: re.Pattern, text: str) -> int:
    m = rx.search(text or "")
    return int(m.group(1)) if m else 0


def parse_evo_swarm_digest(md: str, ref: str) -> Signal:
    m_date = _RE_DATE.search(md or "")
    produced_at = m_date.group(1) if m_date else None
    cycles = _first_int(_RE_CYCLES, md)
    gaps = _first_int(_RE_GAPS, md)
    severity = "info" if (cycles or gaps) else "ok"
    summary_text = f"{cycles} cycles, {gaps} coverage gaps"
    return Signal(
        source="evo-swarm-digest",
        kind="digest",
        severity=severity,
        summary=summary_text,
        counts={"cycles": cycles, "coverage_gaps": gaps},
        produced_at=produced_at,
        ref=ref,
        payload_hash=make_hash(str(produced_at), str(cycles), str(gaps)),
    )
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_parsers.py -v`
Expected: PASS (5 tests total in file)

- [ ] **Step 6: Commit**

```bash
git add apps/cross-repo-dashboard/governor/parsers.py apps/cross-repo-dashboard/tests/fixtures/evo_swarm_digest.md apps/cross-repo-dashboard/tests/test_governor_parsers.py
git commit -F - <<'EOF'
feat(governor): add evo-swarm digest parser (pure, fixture-tested)

Coding-Agent: claude-opus-4.8
Trace-Id: <GENERATE-uuidv7>
EOF
```

---

## Task 5: Fetch + ingest orchestration

**Files:**
- Create: `apps/cross-repo-dashboard/governor/ingest.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_ingest.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_governor_ingest.py
def test_ingest_all_uses_injected_fetcher_and_persists(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")

    fixtures = {
        "game-governance-drift": '{"generated_at":"2026-05-25T07:19:51+00:00","summary":{"total":2,"errors":0,"warnings":2},"issues":[]}',
        "evo-swarm-digest": "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n",
    }

    def fake_fetcher(url: str) -> str:
        if "Game/main/reports" in url:
            return fixtures["game-governance-drift"]
        if "evo-swarm" in url:
            return fixtures["evo-swarm-digest"]
        raise AssertionError(f"unexpected url {url}")

    result = ingest_all(store, fetcher=fake_fetcher)
    assert result["ingested"] == 2
    assert result["new"] == 2
    sources = {r["source"] for r in store.latest_per_source()}
    assert sources == {"game-governance-drift", "evo-swarm-digest"}

def test_ingest_all_records_advisory_on_new_only(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    fx = '{"generated_at":"2026-05-25T07:19:51+00:00","summary":{"total":2,"errors":0,"warnings":2},"issues":[]}'
    digest = "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n"

    def fetcher(url):
        return fx if "Game/main/reports" in url else digest

    ingest_all(store, fetcher=fetcher)             # first run -> 2 new -> 2 advisory
    ingest_all(store, fetcher=fetcher)             # second run -> unchanged -> 0 advisory
    assert len(store.auto_observed_recent(limit=50)) == 2

def test_ingest_all_one_source_failure_does_not_abort_others(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    digest = "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n"

    def fetcher(url):
        if "Game/main/reports" in url:
            raise RuntimeError("network down")
        return digest

    result = ingest_all(store, fetcher=fetcher)
    assert result["errors"] == 1
    assert result["ingested"] == 1   # evo-swarm still ingested
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_ingest.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'governor.ingest'`

- [ ] **Step 3: Write minimal implementation**

```python
# governor/ingest.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_ingest.py -v`
Expected: PASS (3 tests). Note: `requests` is mocked by conftest autouse, but tests inject `fetcher`, so the real `requests` is never called.

- [ ] **Step 5: Commit**

```bash
git add apps/cross-repo-dashboard/governor/ingest.py apps/cross-repo-dashboard/tests/test_governor_ingest.py
git commit -F - <<'EOF'
feat(governor): add fetch + ingest_all orchestration (2 public signals)

Per-source isolation (one failure does not abort others). New/changed
signals write an ADVISORY auto_observed row (severed from gates).

Coding-Agent: claude-opus-4.8
Trace-Id: <GENERATE-uuidv7>
EOF
```

---

## Task 6: Read-only pane (Flask route + template + gitignore)

**Files:**
- Modify: `apps/cross-repo-dashboard/app.py` (add route + GOVERNOR_DB constant near the other path constants, ~line 83 after `ADR_DIR`)
- Create: `apps/cross-repo-dashboard/templates/cr_governor.html`
- Modify: `.gitignore` (repo root)
- Test: `apps/cross-repo-dashboard/tests/test_governor_ingest.py` (add a route smoke test)

- [ ] **Step 1: Add gitignore entry**

Append to repo-root `.gitignore`:

```
# governor signal store (Fase 1a) -- local SQLite, not versioned
apps/cross-repo-dashboard/governor.db
apps/cross-repo-dashboard/governor.db-wal
apps/cross-repo-dashboard/governor.db-shm
```

- [ ] **Step 2: Write the failing route test (append to test_governor_ingest.py)**

```python
def test_governor_route_renders(tmp_path, monkeypatch):
    import app as appmod
    from governor.store import SignalStore
    from governor.signals import Signal
    # point the route at a temp DB with one signal
    db = tmp_path / "g.db"
    store = SignalStore(db)
    store.upsert(Signal(source="game-governance-drift", kind="drift",
                        severity="warning", summary="0 errors, 297 warnings",
                        counts={"warnings": 297}, payload_hash="h1"))
    monkeypatch.setattr(appmod, "GOVERNOR_DB", db)
    # flask is mocked; render_template is a MagicMock, so we assert it was called
    flask_app = appmod.create_app()
    client_ctx = flask_app.test_client  # MagicMock under mocked flask
    # Call the view function directly instead (mocked flask has no real client):
    resp = appmod.governor_pane()
    appmod.render_template.assert_called()
    args, kwargs = appmod.render_template.call_args
    assert args[0] == "cr_governor.html"
    assert any(s["source"] == "game-governance-drift" for s in kwargs["signals"])
    assert kwargs["acted_count"] == 0
```

Note: under the conftest mock, `flask` (and therefore `render_template`, `Blueprint`) is a `MagicMock`. The view returns the mock's return value; we assert the call + kwargs. This matches the existing test style (functions tested directly, not via a live client).

- [ ] **Step 3: Run test to verify it fails**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_ingest.py::test_governor_route_renders -v`
Expected: FAIL with `AttributeError: module 'app' has no attribute 'governor_pane'`

- [ ] **Step 4: Add the route + constant to app.py**

After the `ADR_DIR = ...` line (~line 83), add:

```python
GOVERNOR_DB = CODEMASTERDD_ROOT / "apps" / "cross-repo-dashboard" / "governor.db"
```

After the `/health` route (~line 714), add:

```python
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
```

Add `import sys`-style note: the app dir is already on `sys.path` at runtime (run from the app dir) and in tests (conftest inserts it), so `from governor.store import SignalStore` resolves. For production run, ensure the dashboard is launched from `apps/cross-repo-dashboard/` (the existing `start-dashboard.cmd` already `cd`s there).

- [ ] **Step 5: Create the template**

```html
<!-- templates/cr_governor.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Governor -- signals (R0)</title>
  <link rel="stylesheet" href="{{ url_for('cross_repo.static', filename='style.css') }}">
</head>
<body>
  <h1>Fleet governor -- consolidated signals (R0, report-only)</h1>
  <p>Acted-on signals (off-ramp metric, target &gt;= 3 over 4 weeks): <strong>{{ acted_count }}</strong></p>
  <table>
    <thead><tr><th>Source</th><th>Kind</th><th>Severity</th><th>Summary</th><th>Produced</th><th>Fetched</th></tr></thead>
    <tbody>
    {% for s in signals %}
      <tr class="sev-{{ s.severity }}">
        <td>{{ s.source }}</td><td>{{ s.kind }}</td><td>{{ s.severity }}</td>
        <td>{{ s.summary }}</td><td>{{ s.produced_at or '-' }}</td><td>{{ s.fetched_at }}</td>
      </tr>
    {% else %}
      <tr><td colspan="6">No signals yet -- run <code>python -m governor.ingest</code>.</td></tr>
    {% endfor %}
    </tbody>
  </table>
  <h2>Advisory auto-observed (NOT a gate input)</h2>
  <ul>
    {% for a in advisory %}<li>{{ a.observed_at }} -- {{ a.source }}: {{ a.event }} ({{ a.detail }})</li>{% endfor %}
  </ul>
</body>
</html>
```

- [ ] **Step 6: Run test to verify it passes**

Run: `python -m pytest apps/cross-repo-dashboard/tests/test_governor_ingest.py::test_governor_route_renders -v`
Expected: PASS

- [ ] **Step 7: Full suite + manual smoke**

Run: `python -m pytest apps/cross-repo-dashboard/ -v`
Expected: all tests PASS (existing + new governor tests).

Manual smoke (real network, optional, from app dir):
```bash
cd apps/cross-repo-dashboard
python -m governor.ingest        # expect: governor ingest: {'ingested': 2, 'new': 2, 'errors': 0}  (or errors if a URL 404s -- evo digest 'latest' URL may need a real dated file; note it)
```
If the evo digest `-latest.md` URL 404s, that is expected (Fase-1b adds directory-listing to resolve the newest dated file); the governance-drift signal still ingests. Record the observed result.

- [ ] **Step 8: Commit**

```bash
git add apps/cross-repo-dashboard/app.py apps/cross-repo-dashboard/templates/cr_governor.html .gitignore apps/cross-repo-dashboard/tests/test_governor_ingest.py
git commit -F - <<'EOF'
feat(governor): add R0 read-only signal pane + gitignore the local store

GET /cross-repo/governor renders latest signal per source + the acted-on
off-ramp metric + the advisory log (labeled NOT-a-gate). No action taken.

Coding-Agent: claude-opus-4.8
Trace-Id: <GENERATE-uuidv7>
EOF
```

---

## Task 7: Push branch + open PR (human merges -- R0 is observability, still its own reviewed PR)

- [ ] **Step 1: Branch from fresh main (after Fase-0 PR #241 has merged)**

```bash
git fetch origin --quiet
git checkout -b claude/governor-fase1a-signal-ingestion origin/main
# cherry-pick / re-apply the Fase-1a commits if they were made on a scratch branch,
# OR do Tasks 1-6 directly on this branch.
```

- [ ] **Step 2: Push + open PR (NOT auto-merged)**

```bash
git push -u origin claude/governor-fase1a-signal-ingestion
gh pr create --base main --head claude/governor-fase1a-signal-ingestion \
  --title "feat(governor): Fase 1a R0 signal ingestion (2 public signals + pane)" \
  --body "Implements docs/superpowers/plans/2026-06-01-governor-fase1-signal-ingestion.md. R0 report-only: store + 2 public ingestors + read-only pane + advisory log (severed). No autonomy. CI green. harsh-reviewer requested. Eduardo merges."
```

- [ ] **Step 3: Request harsh-reviewer (verification gate, ADR-0036 sec 4)**

Dispatch the `harsh-reviewer` subagent on the diff before merge. Adopt P0/P1 findings.

---

## Self-Review

**1. Spec coverage (spec sec 2 + sec 5 Fase-1 row):**
- ingestor adapters -> Tasks 3, 4 (2 of N; rest = Fase-1b, scoped out explicitly). COVERED (partial-by-design).
- SQLite persistence -> Task 2. COVERED.
- read-only consolidated view -> Task 6. COVERED.
- advisory auto-observed log SEVERED from gates -> Task 2 (table) + Task 5 (write on new) + Task 6 (labeled NOT-a-gate) + actor-activation-criteria sec 4. COVERED.
- acted-on off-ramp metric -> Task 2 (`acted_on_count`) + Task 6 (pane). COVERED.
- No action / no PR-from-actor / no auto-merge -> nothing in this plan opens a PR from code; the only PR is the human dev's Fase-1a PR. COVERED.
- Fase-1b deferred signals (vault authed, sot-drift gh-issue, learnings) -> explicitly scoped out in header. TRACKED.

**2. Placeholder scan:** the only `<GENERATE-uuidv7>` tokens are deliberate per-commit trace ids (the engineer generates one each, per the noted helper) -- not a content placeholder. No TBD/TODO/"handle edge cases"/"similar to Task N". Every code step has complete code.

**3. Type consistency:** `Signal` fields (source, kind, severity, summary, counts, produced_at, ref, payload_hash) are identical across signals.py (def), parsers.py (construct), store.py (`upsert` reads `sig.source/.kind/.severity/.summary/.counts/.produced_at/.ref/.payload_hash`), and tests. `SignalStore` methods (`upsert`, `latest_per_source`, `record_acted_on`, `acted_on_count`, `add_auto_observed`, `auto_observed_recent`) match across store.py, ingest.py, app.py, tests. `ingest_all(store, fetcher)` signature matches across ingest.py + tests. Consistent.

---

## Execution Handoff

(Filled in after Eduardo chooses an execution mode -- see chat.)
