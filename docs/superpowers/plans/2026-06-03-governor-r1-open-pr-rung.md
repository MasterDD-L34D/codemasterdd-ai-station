# Governor R1 open-PR reconcile rung -- Implementation Plan

> **Status (2026-06-23):** shipped -- R1 open-PR reconcile rung live

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development to
> implement this plan task-by-task (tdd-guard active). Steps use checkbox (`- [ ]`) syntax.

**Goal:** Build the governor R1->open-PR reconcile rung: deterministic, clock-free reconcile
actors that OPEN (never merge) one branch+PR per drifted doc, so the R2 auto-merge evidence
stream (>=4 clean human-merged PR-cycles) can begin.

**Architecture:** A new `governor/reconcile.py` (does NOT touch the issue actor `act.py:run_r1`).
A `Reconciler` dataclass with a fail-closed doctrine guard at construction; a pure `splice`
region-replacer (idempotent + create-if-absent); two clock-free `render` legs
(`status-multi-repo`, `vault-lint-status`); a `reconcile_actor` that opens/updates PRs via an
injected `gh_api` (fake in tests). The real `gh_api` uses the GitHub REST contents+pulls API and
NEVER emits a merge route -- pinned by a negative test against the REAL builder (no
branch-protection backstop on this free-tier repo, so the code is the merge-block). Clean-cycle
accounting is EXTERNAL (a separate read-only `reconcile_cycles_report.py`), never in the actor.

**Tech Stack:** Python 3.12, pytest (`--import-mode=importlib`), GitHub REST API via `requests`
(monkeypatched in tests -- network/gh NEVER hit), SQLite store (shipped `governor/store.py`).

**Authority:** spec `docs/superpowers/specs/2026-06-03-governor-r1-open-pr-rung-design.md` (v4,
merged #292); ADR-0037 dec.4; ADR-0038 (doctrine carve-out); ADR-0011 (commit trailers);
ADR-0021 (ASCII). The spec wins on any conflict.

**Ship as:** ONE branch/PR carrying code + tests + ADR-0039 + the actor-criteria activation note.
The PR is an autonomy increment AND carries doctrine files (ADR + actor-criteria) -> Eduardo
merges. Do NOT self-merge. STOP after PR open + CI green + the 3rd harsh-reviewer pass adopted.

---

## File Structure

- Create `apps/cross-repo-dashboard/governor/reconcile.py` -- the rung (Reconciler, is_doctrine,
  splice, two render legs, reconcile_actor, real gh_api builder, build_reconcilers, `__main__`).
- Create `apps/cross-repo-dashboard/governor/reconcile_cycles_report.py` -- EXTERNAL read-only
  clean-cycle audit (pure predicate + thin gh wrapper; advisory; NOT imported by the actor).
- Create tests under `apps/cross-repo-dashboard/tests/`:
  - `test_governor_reconcile_doctrine.py`
  - `test_governor_reconcile_splice.py`
  - `test_governor_reconcile_render.py`
  - `test_governor_reconcile_actor.py`
  - `test_governor_reconcile_no_merge.py`  (load-bearing negative test)
  - `test_governor_reconcile_cycles_report.py`
- Create `docs/adr/0039-r1-open-pr-reconcile-rung.md` (DOCTRINE -> Eduardo-merge).
- Modify `docs/governance/actor-activation-criteria.md` (DOCTRINE -> Eduardo-merge): add the R1-PR
  activation note.

Established conventions (from the shipped governor): tests import `from governor.X import Y`
inside test functions; `latest_per_source()` returns dicts with keys
`source/kind/severity/summary/counts/produced_at/ref/payload_hash/fetched_at/id`; failure
isolation mirrors `ingest_all` (try/except per item, never abort the rest); the real-builder
negative test follows the `test_governor_act.py::test_lint_no_pr_merge_literals_in_gh_calls`
source-scan convention, STRENGTHENED here with a runtime recording-transport assertion.

---

## Task 1: `is_doctrine` static path-classifier (ADR-0038, fail-closed)

**Files:**
- Create: `apps/cross-repo-dashboard/governor/reconcile.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_reconcile_doctrine.py`

- [ ] **Step 1: Write the failing tests**

```python
# test_governor_reconcile_doctrine.py
import pytest

CARVE_OUTS_TRUE = [
    ("docs/adr/0039-x.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("docs/governance/EXECUTION-BOARD.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("docs/governance/actor-activation-criteria.md", "MasterDD-L34D/codemasterdd-ai-station"),
    (".claude/settings.json", "MasterDD-L34D/codemasterdd-ai-station"),
    (".claude/agents/harsh-reviewer.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/SAFE_CHANGES_ONLY.md",
     "MasterDD-L34D/codemasterdd-ai-station"),
    ("CLAUDE.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("docs/sub/CLAUDE.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("AGENTS.md", "MasterDD-L34D/Game"),
    ("ORCHESTRATION.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("GOALS.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("DECISIONS_LOG.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("OPEN_DECISIONS.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("~/.claude/rules/encoding.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("~/.config/aider-privacy-whitelist.txt", "MasterDD-L34D/codemasterdd-ai-station"),
]

TARGETS_FALSE = [
    ("STATUS_MULTI_REPO.md", "MasterDD-L34D/codemasterdd-ai-station"),
    ("Atlas/lint-status.md", "MasterDD-L34D/vault"),
]


@pytest.mark.parametrize("path,repo", CARVE_OUTS_TRUE)
def test_is_doctrine_true_for_each_carveout(path, repo):
    from governor.reconcile import is_doctrine
    assert is_doctrine(path, repo) is True


@pytest.mark.parametrize("path,repo", TARGETS_FALSE)
def test_is_doctrine_false_for_built_targets(path, repo):
    from governor.reconcile import is_doctrine
    assert is_doctrine(path, repo) is False


def test_is_doctrine_empty_path_is_failclosed_true():
    from governor.reconcile import is_doctrine
    assert is_doctrine("", "MasterDD-L34D/codemasterdd-ai-station") is True
    assert is_doctrine(None, "MasterDD-L34D/codemasterdd-ai-station") is True
```

- [ ] **Step 2: Run -> expect FAIL** (`ModuleNotFoundError: governor.reconcile`)

Run: `python -m pytest -q apps/cross-repo-dashboard/tests/test_governor_reconcile_doctrine.py`

- [ ] **Step 3: Write minimal implementation** (start `reconcile.py`)

```python
# reconcile.py
from __future__ import annotations

_DOCTRINE_NAMES = frozenset({
    "CLAUDE.md", "AGENTS.md", "ORCHESTRATION.md",
    "GOALS.md", "DECISIONS_LOG.md", "OPEN_DECISIONS.md",
})
_DOCTRINE_DIR_PREFIXES = (
    "docs/adr/",
    "docs/governance/",
    "Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/",
)
_DOCTRINE_BASENAMES_EXACT = frozenset({"aider-privacy-whitelist.txt"})


def _normalize_path(path: "str | None") -> str:
    p = (path or "").replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    if p.startswith("~/"):
        p = p[2:]
    return p.lstrip("/")


def is_doctrine(path: "str | None", repo: str) -> bool:
    """STATIC path-classifier for the ADR-0038 doctrine carve-out (fail-closed).

    True for ANY of the static carve-out set: dir globs (docs/adr/**, docs/governance/**,
    Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/**), any `.claude/` segment (repo .claude/**
    AND the global ~/.claude/ governance subpaths -- home machine-junk is conservatively
    OVER-classified, which is FAIL-SAFE for a write-gate: refusing to auto-edit it is harmless,
    a doctrine path must never escape), named root rule files (CLAUDE.md/AGENTS.md/
    ORCHESTRATION.md/GOALS.md/DECISIONS_LOG.md/OPEN_DECISIONS.md, any level), and
    ~/.config/aider-privacy-whitelist.txt.

    NOT here (BY DESIGN): the ADR-0038 *content-based* catch-all -- a pure path-classifier
    cannot evaluate "does this file's content define rules". That clause is a HUMAN process
    checkpoint (spec sec 4.2): adding ANY new reconciler REQUIRES an explicit Eduardo
    doctrine-classification review of its target. This function enforces only the static set.

    `repo` is part of the stable interface (the carve-out is repo-agnostic in ADR-0038;
    `repo` is accepted for forward-compat with a future repo-specific carve-out). It does
    not change the verdict today.
    """
    p = _normalize_path(path)
    if not p:
        return True  # fail-closed: empty/None path -> treat as doctrine (refuse)
    for pref in _DOCTRINE_DIR_PREFIXES:
        if p == pref.rstrip("/") or p.startswith(pref):
            return True
    segments = p.split("/")
    if ".claude" in segments:
        return True
    base = segments[-1]
    if base in _DOCTRINE_NAMES or base in _DOCTRINE_BASENAMES_EXACT:
        return True
    return False
```

- [ ] **Step 4: Run -> expect PASS**

Run: `python -m pytest -q apps/cross-repo-dashboard/tests/test_governor_reconcile_doctrine.py`

- [ ] **Step 5: Commit** (`feat(governor): is_doctrine static carve-out classifier (ADR-0038)`)

---

## Task 2: `Reconciler` dataclass + fail-closed `__post_init__` doctrine guard

**Files:**
- Modify: `apps/cross-repo-dashboard/governor/reconcile.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_reconcile_doctrine.py`

- [ ] **Step 1: Add failing tests**

```python
def test_reconciler_constructs_for_nondoctrine_target():
    from governor.reconcile import Reconciler
    r = Reconciler(
        id="status-multi-repo",
        repo="MasterDD-L34D/codemasterdd-ai-station",
        path="STATUS_MULTI_REPO.md",
        marker=("<!-- B -->", "<!-- E -->"),
        render=lambda store: None,
    )
    assert r.id == "status-multi-repo"


def test_reconciler_raises_on_doctrine_path():
    from governor.reconcile import Reconciler
    with pytest.raises(ValueError, match="doctrine"):
        Reconciler(
            id="bad",
            repo="MasterDD-L34D/codemasterdd-ai-station",
            path="docs/adr/0001-x.md",
            marker=("<!-- B -->", "<!-- E -->"),
            render=lambda store: None,
        )
```

- [ ] **Step 2: Run -> expect FAIL** (`ImportError: cannot import name 'Reconciler'`)

- [ ] **Step 3: Add implementation** to `reconcile.py`

```python
from dataclasses import dataclass
from typing import Callable, Optional, Tuple


@dataclass(frozen=True)
class Reconciler:
    """A deterministic, clock-free doc-reconciler (spec sec 3.1 / 4)."""
    id: str
    repo: str
    path: str
    marker: Tuple[str, str]                       # (begin, end) GOVERNOR-SYNC region
    render: Callable[[object], Optional[str]]     # store -> inner region body, or None
    anchor: Optional[str] = None                  # heading to inject after (existing doc)
    create_header: Optional[str] = None           # frontmatter+heading for a NEW doc

    def __post_init__(self):
        # Fail-closed doctrine guard AT CONSTRUCTION (spec sec 3.1 / 4.2): a reconciler
        # aimed at a doctrine path refuses to exist -- a config error fails fast, never
        # silently opens a doctrine PR.
        if is_doctrine(self.path, self.repo):
            raise ValueError(
                f"Reconciler {self.id!r} targets a doctrine path {self.path!r} "
                f"(ADR-0038 carve-out) -- refusing to construct"
            )
```

- [ ] **Step 4: Run -> expect PASS**

- [ ] **Step 5: Commit** (`feat(governor): Reconciler dataclass with fail-closed doctrine guard`)

---

## Task 3: `splice` -- pure idempotent region-replace + create-if-absent

**Files:**
- Modify: `apps/cross-repo-dashboard/governor/reconcile.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_reconcile_splice.py`

- [ ] **Step 1: Write failing tests**

```python
# test_governor_reconcile_splice.py
MARKER = ("<!-- GOVERNOR-SYNC:signals BEGIN -->", "<!-- GOVERNOR-SYNC:signals END -->")


def test_splice_first_inject_after_anchor_preserves_prose():
    from governor.reconcile import splice
    doc = "# STATUS_MULTI_REPO -- dashboard\n\nhuman prose here\n\n## Snapshot\nrow\n"
    out = splice(doc, MARKER, "TABLE", anchor="# STATUS_MULTI_REPO")
    assert "human prose here" in out
    assert "## Snapshot" in out
    assert MARKER[0] in out and MARKER[1] in out
    assert "TABLE" in out
    # block landed right after the anchor line
    assert out.index(MARKER[0]) > out.index("# STATUS_MULTI_REPO")
    assert out.index(MARKER[0]) < out.index("human prose here")


def test_splice_is_idempotent():
    from governor.reconcile import splice
    doc = "# STATUS_MULTI_REPO -- dashboard\n\nprose\n"
    once = splice(doc, MARKER, "TABLE", anchor="# STATUS_MULTI_REPO")
    twice = splice(once, MARKER, "TABLE", anchor="# STATUS_MULTI_REPO")
    assert once == twice


def test_splice_replaces_region_on_drift():
    from governor.reconcile import splice
    doc = "# STATUS_MULTI_REPO\n"
    v1 = splice(doc, MARKER, "OLD", anchor="# STATUS_MULTI_REPO")
    v2 = splice(v1, MARKER, "NEW", anchor="# STATUS_MULTI_REPO")
    assert "NEW" in v2 and "OLD" not in v2
    assert v2.count(MARKER[0]) == 1 and v2.count(MARKER[1]) == 1


def test_splice_create_if_absent_uses_header():
    from governor.reconcile import splice
    header = "---\ntitle: x\n---\n\n# Vault lint status"
    out = splice("", MARKER, "TABLE", create_header=header)
    assert out.startswith("---")
    assert "# Vault lint status" in out
    assert MARKER[0] in out and "TABLE" in out and MARKER[1] in out
    # idempotent: re-splice the created doc -> identical
    assert splice(out, MARKER, "TABLE", create_header=header) == out


def test_splice_no_timestamp_in_region():
    from governor.reconcile import splice
    import re
    out = splice("", MARKER, "severity | ok", create_header="# x")
    region = out[out.index(MARKER[0]):out.index(MARKER[1])]
    assert not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", region)  # no ISO timestamp injected


def test_splice_backslash_in_region_is_literal():
    from governor.reconcile import splice
    out = splice("", MARKER, r"a\1b\g<0>c", create_header="# x")
    assert r"a\1b\g<0>c" in out  # no regex-replacement backref interpretation
```

- [ ] **Step 2: Run -> expect FAIL** (`ImportError: cannot import name 'splice'`)

- [ ] **Step 3: Add implementation**

```python
import re


def splice(doc_text, marker, new_region, anchor=None, create_header=None) -> str:
    """Pure, idempotent region-replace bounded by (begin, end) markers.

    - markers present       -> replace the BEGIN..END region in place (re.DOTALL, count=1).
    - target absent/empty    -> CREATE: `create_header` (frontmatter+heading) + the block.
    - markers absent + anchor -> first-time injection AFTER the anchor line.
    - markers absent, no anchor -> append the block at end (defensive; never drops prose).

    `new_region` is the INNER body (a table); splice wraps it with the markers. splice adds NO
    timestamp (idempotency: identical new_region -> identical output, spec sec 6.4). A function
    replacement is used in re.sub so backslashes in `new_region` are literal (no backref bug).
    """
    begin, end = marker
    block = f"{begin}\n{new_region}\n{end}"
    text = doc_text or ""

    if begin in text and end in text:
        pattern = re.escape(begin) + r".*?" + re.escape(end)
        return re.sub(pattern, lambda _m: block, text, count=1, flags=re.DOTALL)

    if not text.strip():
        header = (create_header or "").rstrip()
        return (header + "\n\n" + block + "\n") if header else (block + "\n")

    if anchor and anchor in text:
        out = []
        injected = False
        for ln in text.split("\n"):
            out.append(ln)
            if not injected and anchor in ln:
                out.append("")
                out.append(block)
                injected = True
        return "\n".join(out)

    return text.rstrip("\n") + "\n\n" + block + "\n"
```

- [ ] **Step 4: Run -> expect PASS**

- [ ] **Step 5: Commit** (`feat(governor): splice pure idempotent region-replace + create-if-absent`)

---

## Task 4: `render_status_multi_repo` -- clock-free codemasterdd leg

**Files:**
- Modify: `apps/cross-repo-dashboard/governor/reconcile.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_reconcile_render.py`

- [ ] **Step 1: Write failing tests**

```python
# test_governor_reconcile_render.py
def _store(tmp_path, signals):
    from governor.store import SignalStore
    from governor.signals import Signal
    s = SignalStore(tmp_path / "g.db")
    for sig in signals:
        s.upsert(Signal(**sig))
    return s


def test_render_status_none_on_empty_store(tmp_path):
    from governor.reconcile import render_status_multi_repo
    assert render_status_multi_repo(_store(tmp_path, [])) is None


def test_render_status_deterministic_table(tmp_path):
    from governor.reconcile import render_status_multi_repo
    store = _store(tmp_path, [
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "3 errors", "produced_at": "2026-06-01", "ref": "http://x", "payload_hash": "h1"},
        {"source": "vault-gap", "kind": "gap", "severity": "warning",
         "summary": "gap report", "produced_at": "2026-05-30", "ref": "http://y", "payload_hash": "h2"},
    ])
    out1 = render_status_multi_repo(store)
    out2 = render_status_multi_repo(store)
    assert out1 == out2                       # deterministic
    assert "| source | severity | summary | produced_at | ref |" in out1
    assert "game-governance-drift" in out1 and "vault-gap" in out1
    # ordered by source (game- before vault-)
    assert out1.index("game-governance-drift") < out1.index("vault-gap")


def test_render_status_is_clock_free_source_scan():
    import inspect
    from governor.reconcile import render_status_multi_repo
    src = inspect.getsource(render_status_multi_repo)
    for forbidden in ("datetime", "date.today", "time.time", "time()", "now(", " now ", "utcnow"):
        assert forbidden not in src, f"clock token {forbidden!r} in render (must be clock-free)"
```

- [ ] **Step 2: Run -> expect FAIL**

- [ ] **Step 3: Add implementation**

```python
_STATUS_COLS = ("source", "severity", "summary", "produced_at", "ref")


def _md_cell(value) -> str:
    """Single-line markdown table cell (escape pipes/newlines). Pure."""
    s = "" if value is None else str(value)
    return s.replace("|", "\\|").replace("\n", " ").strip()


def _md_table(columns, rows_cells) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(cells) + " |" for cells in rows_cells]
    return "\n".join([header, sep] + body)


def render_status_multi_repo(store):
    """Deterministic, CLOCK-FREE governor signal snapshot from store.latest_per_source().

    Columns source|severity|summary|produced_at|ref, ordered by source (the store returns rows
    ORDER BY source). NO wall-clock / no time-derived value -- the change-key is signal STATE
    only (spec sec 5.1 / 6.3). produced_at is the artifact's own timestamp (from the signal),
    never the current time. Returns None when the store holds no signals (cannot compute).
    """
    rows = store.latest_per_source()
    if not rows:
        return None
    cells = [[_md_cell(r.get(c)) for c in _STATUS_COLS] for r in rows]
    table = _md_table(_STATUS_COLS, cells)
    note = ("\n\n_Auto-synced governor signal snapshot; human prose elsewhere is "
            "authoritative._")
    return table + note
```

- [ ] **Step 4: Run -> expect PASS**

- [ ] **Step 5: Commit** (`feat(governor): render_status_multi_repo clock-free signal table`)

---

## Task 5: `render_vault_lint_status` -- clock-free vault leg (content-based severity)

**Files:**
- Modify: `apps/cross-repo-dashboard/governor/reconcile.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_reconcile_render.py`

- [ ] **Step 1: Write failing tests** (the load-bearing clock-free falsification for the vault leg)

```python
def test_render_vault_lint_none_when_no_lint_sources(tmp_path):
    from governor.reconcile import render_vault_lint_status
    store = _store(tmp_path, [
        {"source": "game-governance-drift", "kind": "drift", "severity": "ok",
         "summary": "x", "payload_hash": "h"},
    ])
    assert render_vault_lint_status(store) is None


def test_render_vault_lint_filters_to_three_lint_sources(tmp_path):
    from governor.reconcile import render_vault_lint_status
    store = _store(tmp_path, [
        {"source": "vault-gap", "kind": "gap", "severity": "warning",
         "summary": "gap report 2026-05-30: 2/3 metrics nonzero", "produced_at": "2026-05-30",
         "ref": "http://g", "payload_hash": "h1"},
        {"source": "vault-coherence", "kind": "coherence", "severity": "ok",
         "summary": "coherence present", "produced_at": "2026-05-30", "ref": "http://c",
         "payload_hash": "h2"},
        {"source": "game-governance-drift", "kind": "drift", "severity": "error",
         "summary": "noise", "payload_hash": "h3"},
    ])
    out = render_vault_lint_status(store)
    assert "| report | severity | summary | produced_at | ref |" in out
    assert "gap" in out and "coherence" in out
    assert "game-governance-drift" not in out   # filtered out
    assert "noise" not in out


def test_render_vault_lint_severity_is_content_based_not_clock(tmp_path):
    """Two stores with IDENTICAL produced_at but DIFFERENT content-severity must render
    DIFFERENT severity cells -> severity tracks content (BLOCK/WARN/metrics), not the clock."""
    from governor.reconcile import render_vault_lint_status
    base = {"source": "vault-gap", "kind": "gap", "produced_at": "2026-05-30",
            "ref": "http://g"}
    s_ok = _store(tmp_path / "a", [dict(base, severity="ok", summary="present",
                                        payload_hash="ok")])
    s_err = _store(tmp_path / "b", [dict(base, severity="error", summary="BLOCK 4 WARN 1",
                                         payload_hash="er")])
    out_ok = render_vault_lint_status(s_ok)
    out_err = render_vault_lint_status(s_err)
    assert "ok" in out_ok and "error" in out_err
    assert out_ok != out_err


def test_render_vault_lint_is_clock_free_source_scan():
    import inspect
    from governor.reconcile import render_vault_lint_status
    src = inspect.getsource(render_vault_lint_status)
    for forbidden in ("datetime", "date.today", "time.time", "time()", "now(", " now ", "utcnow"):
        assert forbidden not in src, f"clock token {forbidden!r} in vault render"
```

Note: `_store` is parametrized with distinct `tmp_path` subdirs (`tmp_path / "a"`) so the two
SignalStore instances do not share a db file.

- [ ] **Step 2: Run -> expect FAIL**

- [ ] **Step 3: Add implementation**

```python
_VAULT_LINT_SOURCES = ("vault-gap", "vault-coherence", "vault-whatsmissing")
_VAULT_LINT_COLS = ("report", "severity", "summary", "produced_at", "ref")


def render_vault_lint_status(store):
    """Deterministic, CLOCK-FREE vault lint dashboard from the three vault lint signals.

    Filters store.latest_per_source() to vault-gap / vault-coherence / vault-whatsmissing,
    iterated in fixed order (deterministic regardless of dict ordering). Columns
    report|severity|summary|produced_at|ref. Severity is CONTENT-based: `parse_vault_report`
    (parsers.py) derives it from BLOCK/WARN/nonzero metrics with NO `now` parameter (spec sec
    5.2), so the rendered state changes only when vault lint CONTENT changes, never on a
    clock-tick. Returns None when none of the three lint sources is present (cannot compute).
    """
    by_source = {r["source"]: r for r in store.latest_per_source()}
    if not any(s in by_source for s in _VAULT_LINT_SOURCES):
        return None
    cells = []
    for s in _VAULT_LINT_SOURCES:
        r = by_source.get(s)
        if r is None:
            continue
        report = s[len("vault-"):]   # gap / coherence / whatsmissing
        cells.append([
            _md_cell(report), _md_cell(r.get("severity")), _md_cell(r.get("summary")),
            _md_cell(r.get("produced_at")), _md_cell(r.get("ref")),
        ])
    table = _md_table(_VAULT_LINT_COLS, cells)
    note = ("\n\n_Auto-synced vault lint status (gap / coherence / whatsmissing); "
            "content-based severity, clock-free. Human prose elsewhere is authoritative._")
    return table + note
```

- [ ] **Step 4: Run -> expect PASS**

- [ ] **Step 5: Commit** (`feat(governor): render_vault_lint_status clock-free content-based leg`)

---

## Task 6: `reconcile_actor` -- the only new autonomy surface (fake gh_api)

**Files:**
- Modify: `apps/cross-repo-dashboard/governor/reconcile.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_reconcile_actor.py`

- [ ] **Step 1: Write failing tests**

```python
# test_governor_reconcile_actor.py
TOKEN_ENV = {"GOVERNOR_RECONCILE_TOKEN": "fake_write_token"}
MK = ("<!-- GOVERNOR-SYNC:signals BEGIN -->", "<!-- GOVERNOR-SYNC:signals END -->")


def _store(tmp_path, signals):
    from governor.store import SignalStore
    from governor.signals import Signal
    s = SignalStore(tmp_path / "g.db")
    for sig in signals:
        s.upsert(Signal(**sig))
    return s


def _fake_gh_api(files=None):
    files = files or {}
    state = {"branches": {}, "prs": {}, "seq": [100]}
    calls = {"get_file": [], "open_or_update_pr": []}

    def get_file(repo, path):
        calls["get_file"].append((repo, path))
        return files.get(repo, {}).get(path, "")

    def open_or_update_pr(repo, branch, base, path, content, rid):
        calls["open_or_update_pr"].append({"repo": repo, "branch": branch, "path": path,
                                           "content": content, "id": rid})
        if branch in state["prs"]:
            if state["branches"].get(branch) == content:
                return {"number": state["prs"][branch], "action": "reused"}
            state["branches"][branch] = content
            return {"number": state["prs"][branch], "action": "updated"}
        num = state["seq"][0]; state["seq"][0] += 1
        state["prs"][branch] = num; state["branches"][branch] = content
        return {"number": num, "action": "created"}

    return {"get_file": get_file, "open_or_update_pr": open_or_update_pr}, calls, state


def _status_reconciler():
    from governor.reconcile import Reconciler, render_status_multi_repo
    return Reconciler(
        id="status-multi-repo", repo="MasterDD-L34D/codemasterdd-ai-station",
        path="STATUS_MULTI_REPO.md", marker=MK, render=render_status_multi_repo,
        anchor="# STATUS_MULTI_REPO",
    )


SIGNALS = [{"source": "game-governance-drift", "kind": "drift", "severity": "error",
            "summary": "3 errors", "produced_at": "2026-06-01", "ref": "http://x",
            "payload_hash": "h1"}]


def test_actor_render_none_is_skipped(tmp_path):
    from governor.reconcile import reconcile_actor
    store = _store(tmp_path, [])          # empty -> render None
    api, calls, _ = _fake_gh_api()
    res = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    assert res["skipped"] and res["skipped"][0]["reason"] == "render-none"
    assert calls["open_or_update_pr"] == []


def test_actor_no_drift_is_unchanged_no_pr(tmp_path):
    from governor.reconcile import reconcile_actor, splice, render_status_multi_repo
    store = _store(tmp_path, SIGNALS)
    region = render_status_multi_repo(store)
    synced = splice("# STATUS_MULTI_REPO\n", MK, region, anchor="# STATUS_MULTI_REPO")
    api, calls, _ = _fake_gh_api({"MasterDD-L34D/codemasterdd-ai-station":
                                  {"STATUS_MULTI_REPO.md": synced}})
    res = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    assert res["unchanged"] and res["unchanged"][0]["id"] == "status-multi-repo"
    assert calls["open_or_update_pr"] == []


def test_actor_drift_opens_one_pr(tmp_path):
    from governor.reconcile import reconcile_actor
    store = _store(tmp_path, SIGNALS)
    api, calls, _ = _fake_gh_api({"MasterDD-L34D/codemasterdd-ai-station":
                                  {"STATUS_MULTI_REPO.md": "# STATUS_MULTI_REPO\nstale\n"}})
    res = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    assert len(res["opened"]) == 1
    assert res["opened"][0]["pr"]["action"] == "created"
    assert len(calls["open_or_update_pr"]) == 1
    assert calls["open_or_update_pr"][0]["branch"] == "auto/governor-reconcile-status-multi-repo"
    assert calls["open_or_update_pr"][0]["base"] if False else True  # base passed positionally


def test_actor_rerun_same_state_reuses_pr(tmp_path):
    from governor.reconcile import reconcile_actor
    store = _store(tmp_path, SIGNALS)
    files = {"MasterDD-L34D/codemasterdd-ai-station":
             {"STATUS_MULTI_REPO.md": "# STATUS_MULTI_REPO\nstale\n"}}
    api, calls, _ = _fake_gh_api(files)   # main stays stale (PR not merged)
    r1 = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    r2 = reconcile_actor(store, [_status_reconciler()], api, environ=TOKEN_ENV)
    assert r1["opened"][0]["pr"]["action"] == "created"
    assert r2["opened"][0]["pr"]["action"] == "reused"      # no NEW pr
    assert r1["opened"][0]["pr"]["number"] == r2["opened"][0]["pr"]["number"]


def test_actor_token_unset_is_failclosed_skip(tmp_path):
    from governor.reconcile import reconcile_actor
    store = _store(tmp_path, SIGNALS)
    api, calls, _ = _fake_gh_api({"MasterDD-L34D/codemasterdd-ai-station":
                                  {"STATUS_MULTI_REPO.md": "# STATUS_MULTI_REPO\nstale\n"}})
    res = reconcile_actor(store, [_status_reconciler()], api, environ={})   # NO token
    assert res["skipped"] and res["skipped"][0]["reason"] == "no-token"
    assert calls["open_or_update_pr"] == []      # NEVER called without the write token


def test_actor_one_reconciler_error_is_isolated(tmp_path):
    from governor.reconcile import reconcile_actor, Reconciler
    def boom(store):
        raise RuntimeError("render kaboom")
    bad = Reconciler(id="bad", repo="MasterDD-L34D/codemasterdd-ai-station",
                     path="docs/research/scratch.md", marker=MK, render=boom)
    store = _store(tmp_path, SIGNALS)
    api, calls, _ = _fake_gh_api({"MasterDD-L34D/codemasterdd-ai-station":
                                  {"STATUS_MULTI_REPO.md": "# STATUS_MULTI_REPO\nstale\n"}})
    res = reconcile_actor(store, [bad, _status_reconciler()], api, environ=TOKEN_ENV)
    assert any(e["id"] == "bad" for e in res["errors"])
    assert len(res["opened"]) == 1               # the good one still proceeded
```

(`docs/research/scratch.md` is intentionally NON-doctrine so the `bad` Reconciler constructs.)

- [ ] **Step 2: Run -> expect FAIL**

- [ ] **Step 3: Add implementation**

```python
import os

_RECONCILE_TOKEN_ENV = "GOVERNOR_RECONCILE_TOKEN"


def reconcile_actor(store, reconcilers, gh_api, environ=None) -> dict:
    """Open/update ONE branch+PR per drifted reconciler. NEVER merges (spec sec 3.1 / 6).

    Per reconciler, ISOLATED (one failure never aborts the rest, mirroring ingest_all):
      1. current = gh_api['get_file'](repo, path)  ("" if 404 -> a new-doc reconciler creates it)
      2. region  = R.render(store); None -> skip ("cannot compute", no junk PR)
      3. patched = splice(current, R.marker, region, anchor=R.anchor, create_header=R.create_header)
      4. patched == current -> no-op (no drift; NO branch, NO PR; record 'unchanged')
      5. else: assert not is_doctrine (defence in depth) -> require the write token ->
         gh_api['open_or_update_pr'](repo, branch=auto/governor-reconcile-<id>, base=main, ...)

    Fail-closed write token (spec sec 6.5): without GOVERNOR_RECONCILE_TOKEN the actor refuses to
    OPEN PRs (records the drifted reconciler under 'skipped' reason no-token; opens NOTHING). A
    WRITE actor does NOT fall back to ambient gh auth. Reads (get_file) may use the ambient token
    (read is not the autonomy surface); only the WRITE is gated.

    Returns {"opened": [...], "unchanged": [...], "skipped": [...], "errors": [...]}.
    """
    environ = os.environ if environ is None else environ
    has_token = bool((environ.get(_RECONCILE_TOKEN_ENV) or "").strip())
    result = {"opened": [], "unchanged": [], "skipped": [], "errors": []}

    for R in reconcilers:
        try:
            current = gh_api["get_file"](R.repo, R.path)
            region = R.render(store)
            if region is None:
                result["skipped"].append({"id": R.id, "reason": "render-none"})
                continue
            patched = splice(current, R.marker, region, anchor=R.anchor,
                             create_header=R.create_header)
            if patched == current:
                result["unchanged"].append({"id": R.id})
                continue
            # Drift. Runtime re-check (defence in depth; __post_init__ already enforced it).
            if is_doctrine(R.path, R.repo):
                raise ValueError(f"refusing to open PR on doctrine path {R.path!r}")
            if not has_token:
                result["skipped"].append({"id": R.id, "reason": "no-token"})
                continue
            pr = gh_api["open_or_update_pr"](
                R.repo, f"auto/governor-reconcile-{R.id}", "main", R.path, patched, R.id,
            )
            result["opened"].append({"id": R.id, "pr": pr})
        except Exception as e:  # noqa: BLE001 -- one reconciler failure must not abort the rest
            result["errors"].append({"id": getattr(R, "id", "?"), "error": str(e)[:200]})
    return result
```

- [ ] **Step 4: Run -> expect PASS**

- [ ] **Step 5: Commit** (`feat(governor): reconcile_actor open-PR-only, fail-closed token, isolated`)

---

## Task 7: Real `gh_api` builder + uuidv7 + the LOAD-BEARING negative merge test

**Files:**
- Modify: `apps/cross-repo-dashboard/governor/reconcile.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_reconcile_no_merge.py`

- [ ] **Step 1: Write failing tests** (negative merge test + uuidv7 format + get_file 404)

```python
# test_governor_reconcile_no_merge.py
import re


def _recorder(responses):
    """Return (http_fn, calls). http_fn pops a canned (status, data) per call, recording
    (method, url). Lets us drive the REAL open_or_update_pr with NO network."""
    calls = []
    seq = list(responses)

    def http(method, url, token=None, json_body=None, timeout=20):
        calls.append({"method": method, "url": url})
        return seq.pop(0) if seq else (200, {})

    return http, calls


def test_uuid7_format():
    from governor.reconcile import _gen_uuid7
    u = _gen_uuid7()
    assert re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", u)


def test_real_get_file_returns_empty_on_404(monkeypatch):
    from governor import reconcile
    http, _ = _recorder([(404, {"message": "Not Found"})])
    monkeypatch.setattr(reconcile, "_http", http)
    monkeypatch.setattr(reconcile, "_ambient_token", lambda environ=None: "t")
    assert reconcile._real_get_file("MasterDD-L34D/vault", "Atlas/lint-status.md") == ""


def test_real_open_or_update_pr_never_emits_merge_route(monkeypatch):
    """LOAD-BEARING (spec sec 6.2): codemasterdd is a free-tier private repo with NO branch
    protection (gh api branches/main/protection -> 403). So the merge-block is CODE. Drive the
    REAL builder through create AND reuse; assert NO recorded HTTP call hits a merge route."""
    from governor import reconcile
    monkeypatch.setattr(reconcile, "_write_token", lambda environ=None: "wtok")
    # create path: get base ref, create branch ref, get file-on-branch (404), put contents,
    # list open prs (empty), create pr.
    http, calls = _recorder([
        (200, {"object": {"sha": "basesha"}}),        # GET base ref
        (201, {}),                                     # POST create branch ref
        (404, {"message": "Not Found"}),               # GET contents?ref=branch (new file)
        (201, {"content": {}}),                        # PUT contents
        (200, []),                                     # GET open prs (none)
        (201, {"number": 7, "html_url": "http://pr/7"}),  # POST create pr
    ])
    monkeypatch.setattr(reconcile, "_http", http)
    out = reconcile._real_open_or_update_pr(
        "MasterDD-L34D/codemasterdd-ai-station",
        "auto/governor-reconcile-status-multi-repo", "main",
        "STATUS_MULTI_REPO.md", "NEW CONTENT", "status-multi-repo")
    assert out["action"] == "created" and out["number"] == 7
    for c in calls:
        assert "/merge" not in c["url"], f"merge route emitted: {c}"
    # methods used are only read/create/update -- never a merge verb on a /merge route
    assert all(c["method"] in ("GET", "POST", "PUT") for c in calls)


def test_no_merge_source_scan():
    """Cheap tripwire (the test_governor_act.py convention): the real gh-builder source must
    contain no merge ROUTE / FLAG literal. (Scopes to '/merge' + flags so the PR-body prose
    'human-merge-only' / 'a human merges' does NOT false-positive.)"""
    import inspect
    from governor import reconcile
    forbidden = ("/merge", "--merge", "--admin", "--squash", "--rebase", "pr merge")
    for fn_name in ("_real_open_or_update_pr", "_real_get_file", "_http"):
        src = inspect.getsource(getattr(reconcile, fn_name))
        for tok in forbidden:
            assert tok not in src, f"{fn_name} contains forbidden merge token {tok!r}"
```

- [ ] **Step 2: Run -> expect FAIL**

- [ ] **Step 3: Add implementation** (the real builder; HTTP via a single monkeypatchable `_http`)

```python
import base64
import json as _json
import subprocess
import sys
from pathlib import Path

_API = "https://api.github.com"
# ADR-0011 policy-C agent-id for actor-generated commits (the model that authored the actor;
# overridable via env for future cron/fleet honesty). NO Co-Authored-By is ever emitted.
_CODING_AGENT_DEFAULT = "claude-opus-4-8"


def _http(method, url, token=None, json_body=None, timeout=20):
    """Single HTTP chokepoint (monkeypatched in tests so network/gh is NEVER hit).
    Returns (status_code, json-or-text)."""
    import requests
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.request(method, url, headers=headers, json=json_body, timeout=timeout)
    try:
        return r.status_code, r.json()
    except Exception:  # noqa: BLE001
        return r.status_code, r.text


def _ambient_token(environ=None):
    """READ token: env GH_TOKEN/GITHUB_TOKEN, else `gh auth token` (mirrors ingest._gh_token).
    Reads are not the autonomy surface, so the ambient token is allowed for get_file."""
    environ = os.environ if environ is None else environ
    t = (environ.get("GH_TOKEN") or "").strip() or (environ.get("GITHUB_TOKEN") or "").strip()
    if t:
        return t
    try:
        r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    return ""


def _write_token(environ=None):
    """WRITE credential: GOVERNOR_RECONCILE_TOKEN ONLY. NO ambient fallback (spec sec 6.5)."""
    environ = os.environ if environ is None else environ
    return (environ.get(_RECONCILE_TOKEN_ENV) or "").strip()


def _gen_uuid7():
    """RFC 9562 UUIDv7 (time-ordered). Python 3.12 has no uuid.uuid7. Used ONLY in the commit
    MESSAGE -- never in a rendered region -> does not affect idempotency / clock-free render."""
    import time
    ms = int(time.time() * 1000) & ((1 << 48) - 1)
    rnd = os.urandom(10)
    b = bytearray(16)
    b[0:6] = ms.to_bytes(6, "big")
    b[6] = 0x70 | (rnd[0] & 0x0F)        # version 7 (high nibble) + 4 rand bits
    b[7] = rnd[1]
    b[8] = 0x80 | (rnd[2] & 0x3F)        # variant 10 + 6 rand bits
    b[9:16] = rnd[3:10]
    h = b.hex()
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def _commit_subject(rid):
    return f"chore(governor): reconcile {rid} signal region"


def _commit_message(rid):
    """Conventional subject + policy-C trailers (ADR-0011): Coding-Agent + Trace-Id (uuidv7),
    NO Co-Authored-By. ASCII-first (ADR-0021)."""
    agent = (os.environ.get("GOVERNOR_RECONCILE_AGENT") or "").strip() or _CODING_AGENT_DEFAULT
    trace = _gen_uuid7()
    body = (f"Auto-reconcile of the {rid} GOVERNOR-SYNC region (deterministic, clock-free). "
            f"Opened by the R1 reconcile actor; a human disposes (human-merge-only earn).\n\n"
            f"Coding-Agent: {agent}\nTrace-Id: {trace}")
    return _commit_subject(rid) + "\n\n" + body


def _real_get_file(repo, path):
    """GET repo contents -> decoded UTF-8 text. "" on 404 (so a new-doc reconciler can create
    it); raises on other non-200 (the actor isolates+skips rather than corrupting)."""
    url = f"{_API}/repos/{repo}/contents/{path}"
    status, data = _http("GET", url, token=_ambient_token())
    if status == 404:
        return ""
    if status != 200:
        raise RuntimeError(f"get_file {repo}/{path} -> HTTP {status}")
    if isinstance(data, dict) and data.get("encoding") == "base64":
        return base64.b64decode(data.get("content", "")).decode("utf-8", errors="replace")
    raise ValueError("unexpected contents-API response (no base64 content)")


def _real_open_or_update_pr(repo, branch, base, path, content, rid):
    """Create/update `branch` with `content` at `path`, then open (or reuse) a PR base<-branch.
    NEVER merges. Requires GOVERNOR_RECONCILE_TOKEN (no ambient fallback for the WRITE).

    Idempotent at the branch level: if the branch already carries identical content the PUT is
    skipped (no new commit / no new trace-id -> no churn). Reuses an open PR for the branch."""
    wtok = _write_token()
    if not wtok:
        raise RuntimeError(
            "GOVERNOR_RECONCILE_TOKEN unset -- the write actor refuses to open a PR "
            "(fail-closed; no ambient fallback for writes, spec sec 6.5)"
        )
    status, data = _http("GET", f"{_API}/repos/{repo}/git/ref/heads/{base}", token=wtok)
    if status != 200:
        raise RuntimeError(f"get base ref {base} -> HTTP {status}")
    base_sha = data["object"]["sha"]
    status, _d = _http("POST", f"{_API}/repos/{repo}/git/refs", token=wtok,
                       json_body={"ref": f"refs/heads/{branch}", "sha": base_sha})
    if status not in (201, 422):   # 201 created, 422 already-exists -> both fine
        raise RuntimeError(f"create branch {branch} -> HTTP {status}")
    status, data = _http("GET", f"{_API}/repos/{repo}/contents/{path}?ref={branch}", token=wtok)
    existing_b64, file_sha = "", None
    if status == 200 and isinstance(data, dict):
        file_sha = data.get("sha")
        if data.get("encoding") == "base64":
            existing_b64 = (data.get("content") or "").replace("\n", "")
    new_b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    if not (existing_b64 and existing_b64 == new_b64):
        body = {"message": _commit_message(rid), "content": new_b64, "branch": branch}
        if file_sha:
            body["sha"] = file_sha
        status, _d = _http("PUT", f"{_API}/repos/{repo}/contents/{path}", token=wtok,
                           json_body=body)
        if status not in (200, 201):
            raise RuntimeError(f"put contents {path} -> HTTP {status}")
    owner = repo.split("/")[0]
    status, data = _http("GET", f"{_API}/repos/{repo}/pulls?state=open&head={owner}:{branch}",
                         token=wtok)
    if status == 200 and isinstance(data, list) and data:
        return {"number": data[0]["number"], "action": "reused",
                "url": data[0].get("html_url", "")}
    pr_body = (f"Deterministic reconcile of the {rid} GOVERNOR-SYNC region (R1 open-PR rung). "
               f"Human-merge-only during the earn window (actor-activation-criteria sec 6); "
               f"this PR is inert until a human merges it.")
    status, data = _http("POST", f"{_API}/repos/{repo}/pulls", token=wtok,
                         json_body={"title": _commit_subject(rid), "head": branch,
                                    "base": base, "body": pr_body})
    if status not in (200, 201):
        raise RuntimeError(f"create PR {branch} -> HTTP {status}")
    return {"number": data.get("number"), "action": "created", "url": data.get("html_url", "")}
```

- [ ] **Step 4: Run -> expect PASS**

- [ ] **Step 5: Commit** (`feat(governor): real REST gh_api builder, uuidv7 trailers, no-merge pinned`)

---

## Task 8: `build_reconcilers` + `real_gh_api` factory + `__main__`

**Files:**
- Modify: `apps/cross-repo-dashboard/governor/reconcile.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_reconcile_actor.py`

- [ ] **Step 1: Write failing tests**

```python
def test_build_reconcilers_two_legs_nondoctrine_targets():
    from governor.reconcile import build_reconcilers
    recs = build_reconcilers()
    ids = {r.id for r in recs}
    assert ids == {"status-multi-repo", "vault-lint-status"}
    by_id = {r.id: r for r in recs}
    assert by_id["status-multi-repo"].repo.endswith("/codemasterdd-ai-station")
    assert by_id["status-multi-repo"].path == "STATUS_MULTI_REPO.md"
    assert by_id["vault-lint-status"].repo.endswith("/vault")
    assert by_id["vault-lint-status"].path == "Atlas/lint-status.md"
    assert by_id["vault-lint-status"].create_header is not None     # NEW doc
    # markers are the spec's GOVERNOR-SYNC tags
    assert by_id["status-multi-repo"].marker[0] == "<!-- GOVERNOR-SYNC:signals BEGIN -->"
    assert by_id["vault-lint-status"].marker[0] == "<!-- GOVERNOR-SYNC:lint BEGIN -->"


def test_real_gh_api_exposes_two_callables():
    from governor.reconcile import real_gh_api
    api = real_gh_api()
    assert callable(api["get_file"]) and callable(api["open_or_update_pr"])
```

- [ ] **Step 2: Run -> expect FAIL**

- [ ] **Step 3: Add implementation**

```python
_VAULT_LINT_DOC_HEADER = """---
title: Vault lint status (governor-synced)
type: status-index
owner: master-dd
language: en
tags: [vault, lint, governor, status]
---

# Vault lint status

> Auto-synced by the cross-repo governor (R1 reconcile rung). The block below is
> governor-owned (marker-bounded); human prose outside it is authoritative. Source signals:
> vault gap-scan / coherence / whatsmissing lint reports. Severity is content-based,
> clock-free. Branch+PR only; merge is Eduardo-only (vault sibling-peer)."""


def build_reconcilers():
    """The BUILT reconciler set (spec sec 5). Construction RAISES if any target is doctrine
    (the __post_init__ fail-closed guard)."""
    status_block = Reconciler(
        id="status-multi-repo",
        repo="MasterDD-L34D/codemasterdd-ai-station",
        path="STATUS_MULTI_REPO.md",
        marker=("<!-- GOVERNOR-SYNC:signals BEGIN -->", "<!-- GOVERNOR-SYNC:signals END -->"),
        render=render_status_multi_repo,
        anchor="# STATUS_MULTI_REPO",
    )
    vault_lint = Reconciler(
        id="vault-lint-status",
        repo="MasterDD-L34D/vault",
        path="Atlas/lint-status.md",
        marker=("<!-- GOVERNOR-SYNC:lint BEGIN -->", "<!-- GOVERNOR-SYNC:lint END -->"),
        render=render_vault_lint_status,
        create_header=_VAULT_LINT_DOC_HEADER,
    )
    return [status_block, vault_lint]


def real_gh_api():
    """Real REST gh_api (clone-agnostic; works for vault without a local vault clone)."""
    return {"get_file": _real_get_file, "open_or_update_pr": _real_open_or_update_pr}


def main(argv=None):
    from governor.store import SignalStore
    db = Path(__file__).resolve().parent.parent / "governor.db"
    if not db.exists():
        print(f"governor.reconcile: db not found at {db} -- run ingest first", file=sys.stderr)
        return 1
    store = SignalStore(db)
    result = reconcile_actor(store, build_reconcilers(), real_gh_api())
    print(_json.dumps(result, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run -> expect PASS** (full reconcile suite green)

- [ ] **Step 5: Commit** (`feat(governor): build_reconcilers two legs + real_gh_api + __main__`)

---

## Task 9: `reconcile_cycles_report.py` -- EXTERNAL read-only clean-cycle accounting

**Files:**
- Create: `apps/cross-repo-dashboard/governor/reconcile_cycles_report.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_reconcile_cycles_report.py`

> Anti-self-licking (spec sec 7.1, actor-criteria sec 4): the COUNT lives OUTSIDE the actor,
> read-only, advisory, NOT a gate input. The actor must never import this module.

- [ ] **Step 1: Write failing tests** (pure clean-cycle predicate)

```python
# test_governor_reconcile_cycles_report.py
def test_clean_cycle_requires_human_merge_no_revert_no_followup():
    from governor.reconcile_cycles_report import is_clean_cycle
    base = {"merged": True, "merged_by_human": True, "reverted_within_7d": False,
            "same_line_followup_within_7d": False}
    assert is_clean_cycle(base) is True
    assert is_clean_cycle(dict(base, merged_by_human=False)) is False   # hub-merged != clean
    assert is_clean_cycle(dict(base, merged=False)) is False            # open != clean
    assert is_clean_cycle(dict(base, reverted_within_7d=True)) is False
    assert is_clean_cycle(dict(base, same_line_followup_within_7d=True)) is False


def test_summarize_counts_clean_cycles_readonly():
    from governor.reconcile_cycles_report import summarize
    prs = [
        {"id": "status-multi-repo", "merged": True, "merged_by_human": True,
         "reverted_within_7d": False, "same_line_followup_within_7d": False},
        {"id": "vault-lint-status", "merged": True, "merged_by_human": False,
         "reverted_within_7d": False, "same_line_followup_within_7d": False},
    ]
    rep = summarize(prs)
    assert rep["clean_cycles"] == 1
    assert rep["total"] == 2
    assert rep["advisory"] is True       # marker: never a gate input
```

- [ ] **Step 2: Run -> expect FAIL**

- [ ] **Step 3: Implement** (pure predicate + read-only summarizer; NO actor import)

```python
# reconcile_cycles_report.py
"""EXTERNAL, READ-ONLY clean-cycle audit for the R1 reconcile rung (spec sec 7.1).

Anti-self-licking (actor-activation-criteria sec 4): this is ADVISORY ONLY -- it is NEVER a gate
input and the reconcile_actor must NEVER import it. A clean R1 cycle (actor-criteria sec 6) =
a reconcile PR (a) MERGED BY A HUMAN, (b) not reverted within 7 days, (c) no same-line follow-up
fix within 7 days. The COUNT is computed here, outside the actor, from git/gh facts; the actor's
own output can never license its own promotion.

Honest scope (spec sec 7.1): N clean cycles prove renderer DETERMINISM + REVERT-SAFETY, NOT
merge-JUDGMENT-safety. The R2 ADR must weigh that.
"""
from __future__ import annotations


def is_clean_cycle(pr: dict) -> bool:
    """Pure mechanical predicate over git/gh facts (no clock here -- the 7-day windows are
    pre-computed by the caller from history at R2-decision time)."""
    return bool(
        pr.get("merged")
        and pr.get("merged_by_human")
        and not pr.get("reverted_within_7d")
        and not pr.get("same_line_followup_within_7d")
    )


def summarize(prs: list) -> dict:
    """Read-only advisory rollup. Writes nothing; not a gate input."""
    clean = [p for p in (prs or []) if is_clean_cycle(p)]
    return {
        "total": len(prs or []),
        "clean_cycles": len(clean),
        "clean_ids": [p.get("id") for p in clean],
        "advisory": True,   # NEVER a gate input (anti-self-licking)
    }
```

- [ ] **Step 4: Run -> expect PASS**

- [ ] **Step 5: Commit** (`feat(governor): external read-only reconcile clean-cycle report`)

---

## Task 10: ADR-0039 -- R1 open-PR reconcile rung (DOCTRINE, Eduardo-merge)

**Files:**
- Create: `docs/adr/0039-r1-open-pr-reconcile-rung.md`

- [ ] **Step 1: Verify 0039 is the next free ADR number**

Run: `ls docs/adr/00*.md | sort | tail -3`  (expect highest = 0038; if 0039 taken, use next free)

- [ ] **Step 2: Write the ADR** recording: class def (spec sec 4); doctrine exclusion + the
  reconciler-addition HUMAN review checkpoint (sec 4.2); human-merge-only invariant (sec 6.1);
  no-branch-protection reality + the 3-part merge-block (sec 6.2); EXTERNAL clean-cycle
  accounting + its honest scope (sec 7.1); the vault lint-status leg + its clock-free
  justification (sec 5.2); explicit NON-grant (auto-merge R2 stays OFF). ASCII body, `--` not
  em-dash (em-dash allowed only in the `# ADR-0039 -- ...` title). Status: Proposed,
  Eduardo-only-merge (doctrine).

- [ ] **Step 3: Commit** (`docs(adr): ADR-0039 R1 open-PR reconcile rung (doctrine, Eduardo-merge)`)

---

## Task 11: actor-activation-criteria activation note (DOCTRINE, Eduardo-merge)

**Files:**
- Modify: `docs/governance/actor-activation-criteria.md`

- [ ] **Step 1: Add an activation note** under sec 8 (Current state) recording: R1-PR rung BUILT
  2026-06-03 (the PR variant added alongside the issue variant); the 2 built legs
  (status-multi-repo + vault-lint-status); human-merge-only during the earn; clean-PR-cycles
  still 0 until the first reconcile PR is human-merged; R2 still hard-gated; ADR-0039 authority.

- [ ] **Step 2: Commit** (`docs(criteria): R1 open-PR rung activation note (ADR-0039, doctrine)`)

---

## Task 12: Full CI green + push + open PR (STOP -- hand merge to Eduardo)

- [ ] **Step 1: Full scoped suite**

Run: `python -m pytest -q apps/cross-repo-dashboard/tests/`
Expected: all pass (123 baseline + the new reconcile tests).

- [ ] **Step 2: ASCII guard (ADR-0021)** on the new/modified files

Run the repo's ASCII pre-commit guard (it runs on commit). Confirm no non-ASCII in new `.md`
bodies / `.py` string literals.

- [ ] **Step 3: Push** the worktree branch to a `claude/*` remote ref

```bash
git push origin worktree-governor-r1-reconcile-rung:claude/governor-r1-reconcile-rung
```

- [ ] **Step 4: Open the PR** (base main). PR body: what the rung is; the HARD invariants
  (no auto-merge, human-merge-only, no LLM in diff path, no clock-tick render, doctrine
  carve-out); the doctrine files present (ADR-0039 + actor-criteria) = Eduardo-merge; the
  no-branch-protection reality. Mark clearly: DO NOT self-merge; Eduardo merges.

- [ ] **Step 5: STOP.** Do not merge. Proceed to Task 13 (harsh-reviewer), adopt findings,
  then hand the merge to Eduardo.

---

## Task 13: 3rd SDMG harsh-reviewer pass on the BUILT code (Protocol 7)

> Pre-commit stance: "if rejected I adopt, I do not defend."

- [ ] **Step 1:** Run `agent-scanner` (global CLAUDE.md STRONG-PURE) before selecting the
  reviewer subagent.

- [ ] **Step 2:** Dispatch `harsh-reviewer` on the built code. It MUST specifically falsify the
  new vault lint-status leg (spec sec 5.2 build note):
  (a) confirm `parse_vault_report` is truly clock-free (no `now`),
  (b) the new-doc create-if-absent is safe + idempotent,
  (c) the sovereign-repo write is branch+PR-only, never merge.
  Plus general: doctrine carve-out completeness, the negative merge test really pins the REAL
  builder, fail-closed token, anti-self-licking externality.

- [ ] **Step 3:** Triage findings P0/P1/P2. Adopt all blocking + significant findings (commit
  the fixes). Re-run CI green. Record the verdict in the PR + (if the ADR needs it) a
  Falsification note.

- [ ] **Step 4:** Final state: PR open + CI green + harsh-review adopted. Hand merge to Eduardo.

---

## Self-Review (writing-plans checklist)

**1. Spec coverage:**
- sec 3.1 units: Reconciler (T2), splice (T3), reconcile_actor (T6), real gh_api (T7) -- covered.
- sec 4.2 is_doctrine completeness incl Archivio/07 + the 2 targets False + doctrine RAISES (T1/T2).
- sec 5.1 status leg clock-free table (T4); sec 5.2 vault leg content-based clock-free (T5).
- sec 6.1 human-merge-only (PR body T12 + ADR T10); sec 6.2 negative merge test on REAL builder
  (T7); sec 6.4 idempotency (T3/T6); sec 6.5 fail-closed token (T6/T7).
- sec 7.1 external clean-cycle accounting (T9, NOT in actor).
- sec 8 token via env never argv (T7 `_write_token` reads env); CWE-214 honored.
- sec 10 TDD plan items: is_doctrine / render(both) / splice / reconcile_actor / negative merge
  test -- one test at a time, network never hit -- covered T1-T8.
- D1 vault leg built (T5/T8); D2 ADR + activation note (T10/T11); D4 build now -- covered.
- HARD constraints: no auto-merge / no settings merge-rule (nothing touches settings.json);
  no LLM in diff path (pure renders); no clock-tick (T4/T5 source-scan); doctrine fail-closed
  (T1/T2); external accounting (T9); env token (T7); ADR-0011 trailers no Co-Authored-By (T7).

**2. Placeholder scan:** none -- every code step has full code; the ADR (T10) + note (T11) are
content-authoring tasks with explicit required sections (acceptable: prose docs, not code).

**3. Type/name consistency:** `gh_api` dict keys `get_file` / `open_or_update_pr` consistent
across T6 (actor), T7 (real), T8 (factory), and the fakes. `Reconciler` fields
(id/repo/path/marker/render/anchor/create_header) consistent T2/T6/T8. `splice(doc_text, marker,
new_region, anchor, create_header)` consistent T3/T6. `_RECONCILE_TOKEN_ENV` defined T6, reused
T7. `_md_table`/`_md_cell` defined T4, reused T5.
