# Governor Fase 1c -- private-authed sources (evo + vault) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development or executing-plans. tdd-guard ACTIVE + STRICT (one test at a time: write 1 -> run -> fail -> impl -> run -> pass).

**Goal:** Add the PRIVATE-repo signal sources to the governor: re-activate evo-swarm (deferred from 1b) and add the 3 vault lint reports (gap-scan / coherence-pass / whats_missing). All via an authed GitHub contents-API fetch (base64) using `gh auth token`. Report-only (R0).

**Architecture:** Extends the Fase-1a/1b `governor/` package on main. Adds: `_gh_token()` (env -> `gh auth token` fallback, mirrors app.py), `gh_get_file_content()` (contents-API base64 -> text, private-safe), a generic `parse_vault_report()`, and a generic `resolve_latest_in_dir()`. Wires evo + 3 vault entries into SOURCES. Game public sources unchanged.

**Tech Stack:** Python 3.13, sqlite3, requests, base64+subprocess (stdlib), pytest+monkeypatch.

**Spec:** `docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md`. **Doctrine (main):** ADR-0036 + `docs/governance/actor-activation-criteria.md`.

**Verified ground-truth (2026-06-02):**
- Authed contents API works for the PRIVATE vault: `repos/MasterDD-L34D/vault/contents/Extras/lint-reports` lists `gap-YYYY-MM-DD.md`, `coherence-YYYY-MM-DD.md`, `whatsmissing-YYYY-MM-DD.md` (newest gap = 2026-06-01). evo-swarm is also private; `repos/MasterDD-L34D/evo-swarm/contents/docs/exports` lists `EXPORT-FOR-GAME-REPO-YYYY-MM-DD.md`.
- A file's contents-API response is `{"content": "<base64>", "encoding": "base64", "download_url": ...}`.
- `gh auth token` returns a valid token on both fleet PCs.

**Privacy note:** reading vault/evo PRIVATE content here = reading Eduardo's OWN repos via his token, persisted to the LOCAL gitignored `governor.db`. No cloud egress, no LLM. Sovereign-safe (the dashboard already reads these repos' git-local state).

---

## File Structure
- Modify `governor/ingest.py`: add `_gh_token`, `gh_get_file_content`, `resolve_latest_in_dir`, vault constants; update `gh_get_json` to use `_gh_token`; refactor evo to authed-content; add 3 vault SOURCES + dispatch styles.
- Modify `governor/parsers.py`: add generic `parse_vault_report(md, source, kind, ref)`.
- Modify `governor/signals.py`: none.
- Modify tests: `test_governor_ingest.py` (token, content-fetch, dir-resolver, evo-reactivated, vault sources), `test_governor_parsers.py` (vault parser).
- Create fixtures: `tests/fixtures/vault_gap.md`, `tests/fixtures/contents_file_b64.json`.

Run: `python -m pytest apps/cross-repo-dashboard/ -v` (green). Then live smoke from `apps/cross-repo-dashboard/`: `python -m governor.ingest` -> expect `ingested: 6, errors: 0` (2 Game public + evo + 3 vault).

---

## Task 1: `_gh_token` + authed `gh_get_file_content`

**Files:** `governor/ingest.py`, `tests/test_governor_ingest.py`, `tests/fixtures/contents_file_b64.json`.

- [ ] **Step 1: fixture** `contents_file_b64.json` (a contents-API file response; `content` = base64 of `"hello vault"`):

```json
{"name": "x.md", "encoding": "base64", "content": "aGVsbG8gdmF1bHQ=\n", "download_url": "https://example/x.md"}
```

- [ ] **Step 2: ONE failing test** (append test_governor_ingest.py):

```python
def test_gh_get_file_content_decodes_base64():
    import json
    from pathlib import Path
    from governor.ingest import gh_get_file_content
    obj = json.loads((Path(__file__).resolve().parent / "fixtures" / "contents_file_b64.json").read_text())
    text = gh_get_file_content("https://api.github.com/x", getter=lambda _u: obj)
    assert text == "hello vault"
```

- [ ] **Step 3: run -> FAIL.**
- [ ] **Step 4: implement** (add to ingest.py; also add `_gh_token` now and route `gh_get_json` through it):

```python
import base64
import subprocess


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


def gh_get_file_content(api_url: str, getter=None) -> str:
    """GET a contents-API file URL -> decoded UTF-8 text (private-repo safe)."""
    getter = getter or gh_get_json
    obj = getter(api_url)
    if isinstance(obj, dict) and obj.get("encoding") == "base64":
        return base64.b64decode(obj.get("content", "")).decode("utf-8", errors="replace")
    raise ValueError("unexpected contents-API response (no base64 content)")
```

Update `gh_get_json` to use `_gh_token()` instead of reading `os.environ["GH_TOKEN"]` directly:

```python
def gh_get_json(url: str):
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    tok = _gh_token()
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()
```

- [ ] **Step 5: run -> PASS.** Then add ONE test that `_gh_token` prefers env (monkeypatch `os.environ`), run -> may pass immediately (characterization) -> keep. Commit `feat(governor): add gh token resolver + authed base64 content fetch`.

---

## Task 2: generic vault lint parser

**Files:** `governor/parsers.py`, `tests/fixtures/vault_gap.md`, `tests/test_governor_parsers.py`.

- [ ] **Step 1: fixture** `vault_gap.md` (real gap-scan shape, trimmed):

```markdown
# Gap-scan report 2026-06-01 (OD-048 sovereign)

Scanned 2249 md.

## Summary

- G1 broken [[links]]: **0**
- G4 orphan (0 inbound, non-MOC): **1**
- G3 stale (>90d / no last_verified): **4**
- frontmatter-invalid: **0**
- title/id duplicates: **1**
```

- [ ] **Step 2: ONE failing test** (append test_governor_parsers.py):

```python
def test_parse_vault_report_gap():
    from pathlib import Path
    from governor.parsers import parse_vault_report
    md = (Path(__file__).resolve().parent / "fixtures" / "vault_gap.md").read_text(encoding="utf-8")
    sig = parse_vault_report(md, source="vault-gap", kind="gap", ref="ref")
    assert sig.source == "vault-gap"
    assert sig.kind == "gap"
    assert sig.produced_at == "2026-06-01"
    # findings present (G4=1, G3=4, dup=1 -> nonzero) -> warning
    assert sig.severity == "warning"
    assert "finding" in sig.summary.lower() or any(v > 0 for v in sig.counts.values())
    assert sig.payload_hash != ""
```

- [ ] **Step 3: run -> FAIL.**
- [ ] **Step 4: implement** (append parsers.py). Light R0 parse: pull the date from the title, count bolded numbers in the Summary, severity by total findings + a BLOCK check:

```python
_RE_VAULT_DATE = re.compile(r"(20\d{2}-\d{2}-\d{2})")
_RE_VAULT_BOLD_NUM = re.compile(r"\*\*(\d+)\*\*")


def parse_vault_report(md: str, source: str, kind: str, ref: str) -> Signal:
    text = md or ""
    m_date = _RE_VAULT_DATE.search(text)
    produced_at = m_date.group(1) if m_date else None
    nums = [int(n) for n in _RE_VAULT_BOLD_NUM.findall(text)]
    findings = sum(nums)
    has_block = ("BLOCK" in text) and any(n > 0 for n in nums)
    if has_block:
        severity = "error"
    elif findings > 0:
        severity = "warning"
    else:
        severity = "ok"
    summary_text = f"{findings} finding(s) across {len(nums)} metric(s)"
    return Signal(
        source=source,
        kind=kind,
        severity=severity,
        summary=summary_text,
        counts={"findings": findings, "metrics": len(nums)},
        produced_at=produced_at,
        ref=ref,
        payload_hash=make_hash(source, str(produced_at), str(findings)),
    )
```

- [ ] **Step 5: run -> PASS.** Add ONE test: empty/no-findings md -> severity "ok". Commit `feat(governor): add generic vault lint-report parser`.

---

## Task 3: dir-resolver + wire evo (authed) + 3 vault sources

**Files:** `governor/ingest.py`, `tests/test_governor_ingest.py`.

- [ ] **Step 1: constants + generic resolver** (add to ingest.py):

```python
VAULT_LINT_API = "https://api.github.com/repos/MasterDD-L34D/vault/contents/Extras/lint-reports"


def resolve_latest_in_dir(api_url: str, prefix: str, getter=None) -> str | None:
    """List a contents dir, return the contents-API url of the newest `prefix*.md`."""
    getter = getter or gh_get_json
    entries = getter(api_url)
    cands = sorted(
        e for e in (entries or [])
        if str(e.get("name", "")).startswith(prefix) and e.get("name", "").endswith(".md")
    , key=lambda e: e["name"])
    if not cands:
        return None
    return cands[-1].get("url")  # contents-API url of the file
```

(The contents-listing entries each carry a `url` = the file's contents-API endpoint -- use it for the authed content fetch.)

- [ ] **Step 2: rewrite `_produce` + `SOURCES`** for the private styles. evo now uses authed content; vault uses the generic resolver + parser:

```python
from governor.parsers import (
    parse_game_governance_drift, parse_evo_swarm_digest,
    parse_sot_drift_issues, parse_vault_report,
)

EVO_EXPORTS_API = "https://api.github.com/repos/MasterDD-L34D/evo-swarm/contents/docs/exports"

SOURCES = [
    {"id": "game-governance-drift", "style": "json"},
    {"id": "game-sot-drift", "style": "gh-issues"},
    {"id": "evo-swarm-digest", "style": "evo-private"},
    {"id": "vault-gap", "style": "vault", "prefix": "gap-", "kind": "gap"},
    {"id": "vault-coherence", "style": "vault", "prefix": "coherence-", "kind": "coherence"},
    {"id": "vault-whatsmissing", "style": "vault", "prefix": "whatsmissing-", "kind": "whatsmissing"},
]


def _produce(src: dict, fetcher, json_getter, content_getter):
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
    raise ValueError(f"unknown style {style} for {sid}")


def ingest_all(store, fetcher=raw_fetch, json_getter=gh_get_json, content_getter=gh_get_file_content) -> dict:
    ingested = new = errors = 0
    for src in SOURCES:
        try:
            sig = _produce(src, fetcher, json_getter, content_getter)
            if store.upsert(sig):
                new += 1
                store.add_auto_observed(sig.source, "signal-changed", detail=sig.summary)
            ingested += 1
        except Exception as e:  # noqa: BLE001
            errors += 1
            store.add_auto_observed(src["id"], "ingest-error", detail=str(e)[:200])
    return {"ingested": ingested, "new": new, "errors": errors}
```

Remove the now-dead 1b `resolve_evo_latest_url` (raw-URL version) + the old `evo-dynamic` branch, OR keep `resolve_evo_latest_url` if other tests use it (update them). Prefer: delete it + its tests, since `resolve_latest_in_dir` supersedes it. Update `main()` if needed (defaults now include `content_getter`).

- [ ] **Step 3: update tests** `test_governor_ingest.py`: extend `_fakes()` to also return a `content_getter` + a `json_getter` that serves the evo + vault dir listings (entries with `url`) + the file contents. Update the ingest_all tests to the 6-source contract (or assert the subset that the fakes provide). Rewrite/replace the evo `_produce` test for the new `evo-private` style. Add a vault-source ingest test. Keep per-source isolation + advisory-on-new tests (now 6 sources).

- [ ] **Step 4: full suite green.**
- [ ] **Step 5: commit** `feat(governor): wire evo (authed) + 3 vault sources via contents-API`.

---

## Task 4: live smoke + PR
- [ ] Live: `python -m governor.ingest` -> expect `{'ingested': 6, 'new': ..., 'errors': 0}` (2 Game + evo + 3 vault, all via token). PASTE the real output. If a vault file prefix has no file (e.g. coherence naming differs), record the per-source advisory + adjust the prefix.
- [ ] Push branch, open PR (base main, NOT auto-merged). PR body: 6 sources live, the authed-contents-fetch infra, the privacy note (sovereign local read), live smoke output. Note learnings (aa01) deferred.
- [ ] harsh-reviewer subagent on the diff (SDMG gate) before merge.

---

## Self-Review
- **Spec coverage:** evo (private, re-activated) + vault x3 (gap/coherence/whatsmissing) via authed contents-fetch -> the file-based private signal class complete. ARCHON learnings (aa01 repo) deferred to a follow-up (different repo + shape).
- **Token:** `_gh_token` mirrors app.py (env -> `gh auth token`). Private repos now work (the 1b harsh-reviewer SIGNIFICANT, now resolved where it is load-bearing).
- **No token leak:** never logged; only added to a header. Error advisory logs `str(e)[:200]` (url+status only, as the 1b harsh-reviewer verified for `requests`).
- **Type consistency:** `_produce(src, fetcher, json_getter, content_getter)` + `ingest_all(..., content_getter=...)` + `parse_vault_report(md, source, kind, ref)` + `resolve_latest_in_dir(api_url, prefix, getter)` -- all match across impl + tests. `gh_get_file_content(api_url, getter)` matches.
- **R0 discipline:** all new fetchers are GET (`gh_get_json`/`gh_get_file_content`/`raw_fetch`); no mutation. Still report-only.
- **Privacy:** vault/evo are sovereign-only; read locally via the user's token to a gitignored DB; no cloud, no LLM. The dashboard already reads these repos. No new exposure.
