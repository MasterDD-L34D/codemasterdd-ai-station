# Governor Fase 1b -- evo URL-resolver + sot-drift adapter Implementation Plan

> **Status (2026-06-23):** shipped -- governor signal-ingestion 1b live

> **POST-IMPLEMENTATION NOTE (2026-06-01):** live ground-truth at build time found
> **evo-swarm is a PRIVATE repo** (this plan assumed public). It cannot ingest
> anonymously, so evo was DEFERRED to Fase-1c (with the vault private sources -- same
> authed-contents-fetch strategy). Fase-1b shipped with **2 active live sources**:
> `game-governance-drift` + `game-sot-drift` (both public, live smoke 2/2 errors=0).
> The evo resolver/parser/dispatch code is built + dormant (covered by a direct
> `_produce` test), reactivated in Fase-1c. Off-ramp >=2-sources requirement satisfied.

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development or superpowers:executing-plans. Steps use `- [ ]`. tdd-guard hook is ACTIVE + STRICT (one test at a time: write 1 test -> run -> fail -> implement -> pass -> next).

**Goal:** Bring a 2nd + 3rd live signal into the governor: fix the evo-swarm digest URL (dynamic dated-file resolution) and add the Game sot-drift gh-issue adapter. This lifts live sources from 1 to 3 and unblocks the off-ramp (>=2 sources live).

**Architecture:** Extends the Fase-1a `governor/` package already on main. Reuses `Signal`, `SignalStore`, `parse_evo_swarm_digest`. Adds: a JSON GitHub-REST getter (`gh_get_json`), an evo latest-URL resolver (`resolve_evo_latest_url`), a new pure parser `parse_sot_drift_issues`, and a refactor of `ingest_all` to dispatch 3 fetch styles (raw / dynamic-raw / gh-issues) via injectable deps.

**Tech Stack:** Python 3.13, sqlite3, `requests` (REST + raw), pytest + monkeypatch. Both 1b sources are PUBLIC repos (anon REST OK; token optional). Vault-authed (private) + ARCHON learnings = deferred to Fase-1c.

**Spec:** `docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md`. **Doctrine (on main):** ADR-0036 + `docs/governance/actor-activation-criteria.md`.

**Verified ground-truth (2026-06-01):**
- evo exports dir `repos/MasterDD-L34D/evo-swarm/contents/docs/exports` lists `EXPORT-FOR-GAME-REPO-YYYY-MM-DD.md` (newest today: `2026-05-27`). Resolve newest -> raw-fetch it.
- Game sot-drift: `gh`/REST `repos/MasterDD-L34D/Game/issues?labels=sot-drift-candidate&state=open` -> currently 1 open (#2477, title "SoT drift candidate (runtime ahead of SoT docs)").

---

## File Structure
- Modify: `apps/cross-repo-dashboard/governor/parsers.py` -- add `parse_sot_drift_issues`.
- Modify: `apps/cross-repo-dashboard/governor/ingest.py` -- add `gh_get_json`, `resolve_evo_latest_url`, `SOT_ISSUES_URL`, refactor `ingest_all` + `SOURCES` for 3 styles.
- Modify: `apps/cross-repo-dashboard/tests/test_governor_parsers.py` -- sot-drift parser tests.
- Modify: `apps/cross-repo-dashboard/tests/test_governor_ingest.py` -- update for the resolver + json_getter injection + sot-drift source.
- Create: `apps/cross-repo-dashboard/tests/fixtures/sot_drift_issues.json` -- gh issue-list sample.

Run: `python -m pytest apps/cross-repo-dashboard/ -v` (from repo root). Must stay green (existing 55 + new).

---

## Task 1: sot-drift parser (pure, fixture-tested)

**Files:** modify `governor/parsers.py`, create `tests/fixtures/sot_drift_issues.json`, modify `tests/test_governor_parsers.py`.

- [ ] **Step 1: Create fixture** `tests/fixtures/sot_drift_issues.json` (gh issue-list shape, `--json number,title,state,updatedAt`):

```json
[
  {"number": 2477, "title": "SoT drift candidate (runtime ahead of SoT docs)", "state": "OPEN", "updatedAt": "2026-06-01T20:51:08Z"}
]
```

- [ ] **Step 2: Write ONE failing test** (append to test_governor_parsers.py):

```python
def test_parse_sot_drift_issues_open():
    import json
    from pathlib import Path
    from governor.parsers import parse_sot_drift_issues
    fix = Path(__file__).resolve().parent / "fixtures" / "sot_drift_issues.json"
    issues = json.loads(fix.read_text(encoding="utf-8"))
    sig = parse_sot_drift_issues(issues, "ref-url")
    assert sig.source == "game-sot-drift"
    assert sig.kind == "sot-drift"
    assert sig.severity == "warning"
    assert sig.counts == {"open": 1}
    assert sig.produced_at == "2026-06-01T20:51:08Z"
    assert sig.ref == "ref-url"
    assert sig.payload_hash != ""
```

- [ ] **Step 3: Run -> FAIL** (`parse_sot_drift_issues` undefined).
- [ ] **Step 4: Implement** (append to parsers.py):

```python
def parse_sot_drift_issues(issues: list, ref: str) -> Signal:
    items = issues or []
    open_count = len(items)
    updated = [i.get("updatedAt") or i.get("updated_at") or "" for i in items]
    produced_at = max(updated) if updated and any(updated) else None
    severity = "warning" if open_count > 0 else "ok"
    summary_text = f"{open_count} open SoT drift candidate(s)"
    return Signal(
        source="game-sot-drift",
        kind="sot-drift",
        severity=severity,
        summary=summary_text,
        counts={"open": open_count},
        produced_at=produced_at,
        ref=ref,
        payload_hash=make_hash("sot-drift", str(open_count), str(produced_at)),
    )
```

- [ ] **Step 5: Run -> PASS.**
- [ ] **Step 6: Write ONE failing test** (empty = ok severity):

```python
def test_parse_sot_drift_issues_empty_is_ok():
    from governor.parsers import parse_sot_drift_issues
    sig = parse_sot_drift_issues([], "ref")
    assert sig.severity == "ok"
    assert sig.counts == {"open": 0}
    assert sig.produced_at is None
```

- [ ] **Step 7: Run -> PASS** (already handled). If tdd-guard objects to a passing test with no new impl, that is fine -- it is a characterization test of the empty branch; keep it.
- [ ] **Step 8: Commit** (policy-C trailers, generate uuidv7; NO Co-Authored-By):

```
feat(governor): add sot-drift gh-issue parser (pure, fixture-tested)
```

---

## Task 2: REST JSON getter + evo latest-URL resolver

**Files:** modify `governor/ingest.py`, modify `tests/test_governor_ingest.py`.

- [ ] **Step 1: Write ONE failing test** (append to test_governor_ingest.py):

```python
def test_resolve_evo_latest_url_picks_newest():
    from governor.ingest import resolve_evo_latest_url
    listing = [
        {"name": "EXPORT-FOR-GAME-REPO-2026-04-27.md"},
        {"name": "EXPORT-FOR-GAME-REPO-2026-05-27.md"},
        {"name": "README.md"},
    ]
    url = resolve_evo_latest_url(lister=lambda _u: listing)
    assert url.endswith("/docs/exports/EXPORT-FOR-GAME-REPO-2026-05-27.md")
    assert url.startswith("https://raw.githubusercontent.com/MasterDD-L34D/evo-swarm/main/")
```

- [ ] **Step 2: Run -> FAIL.**
- [ ] **Step 3: Implement** (add to ingest.py, near the top constants):

```python
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
```

- [ ] **Step 4: Run -> PASS.**
- [ ] **Step 5: Write ONE failing test** (empty listing -> None):

```python
def test_resolve_evo_latest_url_none_when_empty():
    from governor.ingest import resolve_evo_latest_url
    assert resolve_evo_latest_url(lister=lambda _u: []) is None
```

- [ ] **Step 6: Run -> PASS. Commit:**

```
feat(governor): add REST json getter + evo latest-URL resolver
```

---

## Task 3: Refactor ingest_all for 3 fetch styles + wire sot-drift

**Files:** modify `governor/ingest.py`, modify `tests/test_governor_ingest.py`.

This refactor changes `ingest_all` to inject BOTH a raw `fetcher` and a `json_getter`, and dispatches per source. The existing 1a ingest tests pass only `fetcher=`; update them to also pass `json_getter=` (the evo source now resolves its URL via json_getter first).

- [ ] **Step 1: Update the SOURCES list + add the dispatch** (replace `SOURCES` + `_parse` + `ingest_all` in ingest.py):

```python
SOURCES = [
    {"id": "game-governance-drift", "style": "json"},
    {"id": "evo-swarm-digest", "style": "evo-dynamic"},
    {"id": "game-sot-drift", "style": "gh-issues"},
]


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
    ingested = new = errors = 0
    for src in SOURCES:
        try:
            sig = _produce(src["id"], src["style"], fetcher, json_getter)
            is_new = store.upsert(sig)
            ingested += 1
            if is_new:
                new += 1
                store.add_auto_observed(sig.source, "signal-changed", detail=sig.summary)
        except Exception as e:  # noqa: BLE001 -- one bad source must not abort the rest
            errors += 1
            store.add_auto_observed(src["id"], "ingest-error", detail=str(e)[:200])
    return {"ingested": ingested, "new": new, "errors": errors}
```

Add `from governor.parsers import parse_sot_drift_issues` to the existing parsers import line. Import `parse_game_governance_drift, parse_evo_swarm_digest, parse_sot_drift_issues`.

- [ ] **Step 2: Update the existing 1a ingest tests** that call `ingest_all(store, fetcher=...)` -- they now must also pass a `json_getter` so the evo + sot sources resolve. Replace each with a fetcher keyed by URL substring + a json_getter:

```python
def _fakes():
    drift = '{"generated_at":"2026-05-25T07:19:51+00:00","summary":{"total":2,"errors":0,"warnings":2},"issues":[]}'
    digest = "# Evo-Swarm -> Game Repo Digest -- 2026-05-27\n**Cicli inclusi**: 7 entry\n### Coverage gap (3 entry)\n"
    def fetcher(url):
        if "reports/docs/governance_drift" in url:
            return drift
        if "EXPORT-FOR-GAME-REPO" in url:
            return digest
        raise AssertionError(f"unexpected raw url {url}")
    def json_getter(url):
        if "contents/docs/exports" in url:
            return [{"name": "EXPORT-FOR-GAME-REPO-2026-05-27.md"}]
        if "labels=sot-drift-candidate" in url:
            return [{"number": 2477, "title": "x", "state": "OPEN", "updatedAt": "2026-06-01T20:51:08Z"}]
        raise AssertionError(f"unexpected json url {url}")
    return fetcher, json_getter


def test_ingest_all_three_sources_persist(tmp_path):
    from governor.store import SignalStore
    from governor.ingest import ingest_all
    store = SignalStore(tmp_path / "g.db")
    fetcher, json_getter = _fakes()
    result = ingest_all(store, fetcher=fetcher, json_getter=json_getter)
    assert result["ingested"] == 3
    assert result["new"] == 3
    sources = {r["source"] for r in store.latest_per_source()}
    assert sources == {"game-governance-drift", "evo-swarm-digest", "game-sot-drift"}
```

Rewrite the prior `test_ingest_all_*` (the 1a versions referencing only 2 sources / fetcher-only) to use `_fakes()` + the `json_getter` kwarg. Keep the advisory-on-new test + the per-source-failure-isolation test, updated for 3 sources (e.g. make `json_getter` raise for the sot URL and assert `errors == 1`, the other two still ingest).

- [ ] **Step 3: Run the full file. Iterate (tdd-guard one change at a time) until green.**
- [ ] **Step 4: Full suite green:** `python -m pytest apps/cross-repo-dashboard/ -v`
- [ ] **Step 5: Commit:**

```
feat(governor): dispatch 3 fetch styles; wire evo-dynamic + sot-drift
```

---

## Task 4: Manual smoke + PR

- [ ] **Step 1: Live smoke** (from `apps/cross-repo-dashboard/`): `python -m governor.ingest` -> expect `{'ingested': 3, ...}` (all 3 public sources live: Game drift, evo 2026-05-27, sot-drift #2477). Record the result.
- [ ] **Step 2:** Leave uncommitted work? No -- commits are per-task above. Push branch `claude/governor-fase1b-signal-ingestion`, open PR (base main, NOT auto-merged). PR body: 3 sources now live (off-ramp >=2 satisfied) + harsh-reviewer requested. Note Fase-1c = vault-authed x3 + learnings.
- [ ] **Step 3:** harsh-reviewer subagent on the diff (SDMG verification gate) before merge.

---

## Self-Review
- **Spec coverage:** evo source live (resolver) + sot-drift adapter (gh-issues style) -> 2 of the 4 remaining 1b/1c signals. Vault-authed x3 + learnings explicitly deferred to Fase-1c. Off-ramp >=2-sources requirement met (3 live).
- **Placeholder scan:** only `uuidv7`/policy-C trailer placeholders (generate per commit). No TBD.
- **Type consistency:** `parse_sot_drift_issues(issues, ref)` signature matches its test + `_produce`. `ingest_all(store, fetcher, json_getter)` matches updated tests + `main()` (which calls `ingest_all(store)` with defaults `raw_fetch` + `gh_get_json` -- both real). `resolve_evo_latest_url(lister)` matches its tests + `_produce`. `Signal` fields unchanged.
- **Risk:** `gh_get_json` hits live REST in `main()`/prod (rate-limited anon ~60/hr -- fine for a 5-min dashboard; token raises it). Tests never hit network (inject `fetcher`/`json_getter`/`lister`). `main()` defaults are real callables, so a bare `python -m governor.ingest` works live.
