"""Governor R1 open-PR reconcile rung -- deterministic, clock-free doc-reconcile actors.

The rung OPENS branch+PRs (never merges) for docs whose GOVERNOR-SYNC marker region drifted
from a pure function of the governor's signal store. It does NOT touch the issue actor
(act.py:run_r1). Authority: spec docs/superpowers/specs/2026-06-03-governor-r1-open-pr-rung-design.md
(v4, merged #292); ADR-0037 dec.4; ADR-0038 (doctrine carve-out); ADR-0011 (commit trailers);
ADR-0021 (ASCII). The spec wins on any conflict.

HARD invariants: NO auto-merge (R2, future ADR); NO LLM in the diff path; NO time-derived /
clock-tick render; doctrine files are NEVER targeted (fail-closed); the write actor is
fail-closed on GOVERNOR_RECONCILE_TOKEN (no ambient fallback for writes); clean-cycle accounting
is EXTERNAL (reconcile_cycles_report.py), never in the actor.
"""
from __future__ import annotations

import base64
import json as _json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Tuple

_RECONCILE_TOKEN_ENV = "GOVERNOR_RECONCILE_TOKEN"
_API = "https://api.github.com"
# ADR-0011 policy-C agent-id for actor-generated commits (the model that authored the actor;
# overridable via env for future cron/fleet honesty). NO Co-Authored-By is ever emitted.
_CODING_AGENT_DEFAULT = "claude-opus-4-8"

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
    """A fail-closed WRITE-REFUSAL gate: True for the static subset of ADR-0038 doctrine paths
    relevant to this rung. It is a SUPERSET (over-refuses) of that static set -- NOT the canonical
    ADR-0038 classifier. Do NOT reuse it for ALLOW-decisions (e.g. a merge-eligibility call):
    ADR-0038's global `~/.claude/` rule uses a positive subpath ALLOW-list (excluding
    credentials/cache/sessions/plugins), whereas this gate treats ANY `.claude/` segment as
    doctrine. Over-refusal is harmless for a write-gate (refusing to auto-edit a path is safe; a
    doctrine path must never escape) but WRONG semantics for an allow-list. The catch-all is
    handled by a HUMAN review (below), not here.

    True for ANY of the static carve-out set: dir globs (docs/adr/**, docs/governance/**,
    Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/**), any `.claude/` segment (repo .claude/**
    AND the global ~/.claude/ governance subpaths -- home machine-junk is conservatively
    OVER-classified, which is FAIL-SAFE for a write-gate, per above), named root rule files
    (CLAUDE.md/AGENTS.md/ORCHESTRATION.md/GOALS.md/DECISIONS_LOG.md/OPEN_DECISIONS.md, any level),
    and ~/.config/aider-privacy-whitelist.txt.

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


@dataclass(frozen=True)
class Reconciler:
    """A deterministic, clock-free doc-reconciler (spec sec 3.1 / 4).

    render(store) -> the INNER marker-region body (a table), or None = "cannot compute" (the
    actor skips it, never a junk PR). render MUST be pure: reads signals from the store, no
    network, no write, NO wall-clock (spec sec 6.3).
    """
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


# C0/DEL control bytes are the contamination this gate heals: a single NUL (0x00) makes git
# treat the whole file as binary, so the governor's human-reviewable GOVERNOR-SYNC region renders
# as "Binary files differ" -- defeating the rung's entire point (vault #260; the 13 trailing NULs
# likely entered via the #258->#260 conflict-resolution, ADR-0039 Addendum 2026-06-11). The
# actor only PRESERVES whatever get_file decoded (base64 -> .decode(errors="replace") keeps 0x00
# as U+0000), so the contamination NEVER self-heals across reconcile runs. This gate strips every
# C0 control char (and DEL 0x7f) EXCEPT the three legitimate text-whitespace bytes -- tab (0x09),
# newline (0x0a), carriage-return (0x0d) -- from splice's text inputs, so a contaminated source
# self-heals on the next reconcile (the sanitized output differs from the dirty source -> drift ->
# a clean PR) instead of carrying the control bytes forward. CR is preserved to avoid an unrelated
# CRLF->LF reflow. SCOPE (deliberately narrow): this heals control-BYTE contamination only, NOT
# invalid-UTF-8 "mojibake" -- decode(errors="replace") already folds that into U+FFFD, which is
# itself valid UTF-8 (text, not binary), so it is left untouched on purpose (a different, larger
# concern). Deterministic + idempotent: clean text -> identical text (no-op), so splice's
# idempotency / no-churn contract is preserved. Source is pure ASCII (ADR-0021): \x7f is an
# ASCII-source escape, not a non-ASCII literal byte.
_CONTROL_STRIP_TABLE = {c: None for c in range(0x20) if c not in (0x09, 0x0A, 0x0D)}
_CONTROL_STRIP_TABLE[0x7F] = None


def _strip_control_bytes(text: str) -> str:
    """Strip C0 control chars + DEL (except tab/newline/CR) from `text`. Pure, deterministic,
    idempotent. Defends the reconcile region against binary contamination (NUL) propagating
    forward; a no-op on already-clean text (see _CONTROL_STRIP_TABLE rationale above)."""
    return (text or "").translate(_CONTROL_STRIP_TABLE)


def splice(doc_text, marker, new_region, anchor=None, create_header=None) -> str:
    """Pure, idempotent region-replace bounded by (begin, end) markers.

    - markers present          -> replace the BEGIN..END region in place (re.DOTALL, count=1).
    - target absent/empty       -> CREATE: `create_header` (frontmatter+heading) + the block.
    - markers absent + anchor    -> first-time injection AFTER the anchor line.
    - markers absent, no anchor   -> append the block at end (defensive; never drops prose).

    `new_region` is the INNER body (a table); splice wraps it with the markers. splice adds NO
    timestamp (idempotency: identical new_region -> identical output, spec sec 6.4). A function
    replacement is used in re.sub so backslashes in `new_region` are literal (no backref bug).

    Every text input (doc_text, new_region, create_header) is passed through
    _strip_control_bytes FIRST: the output is therefore guaranteed free of C0 control bytes
    regardless of which source (a contaminated existing doc, a junk-bearing render, or a header)
    introduced them -- so binary contamination self-heals here rather than propagating forward
    (vault #260). The markers themselves are clean literals.
    """
    begin, end = marker
    new_region = _strip_control_bytes(new_region)
    block = f"{begin}\n{new_region}\n{end}"
    text = _strip_control_bytes(doc_text)

    if begin in text and end in text:
        pattern = re.escape(begin) + r".*?" + re.escape(end)
        return re.sub(pattern, lambda _m: block, text, count=1, flags=re.DOTALL)

    if not text.strip():
        header = _strip_control_bytes(create_header).rstrip()
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


# ---------------------------------------------------------------------------
# Render legs -- pure, deterministic, CLOCK-FREE (spec sec 5 / 6.3).
# ---------------------------------------------------------------------------

_STATUS_COLS = ("source", "severity", "summary", "produced_at", "ref")

# Sources whose STORED severity is time-derived UPSTREAM of the render: ingest passes `now`
# into the parser, which folds a staleness band (info/warning/error) into severity AND
# payload_hash (parse_eng_graph_moc). Rendering that severity leaks the calendar into the
# STATUS region -- a byte-identical source could open a calendar-only PR (ADR-0039 ratify
# amendment P1 / dossier P1-1, empirically probed 2026-06-11). The STATUS render MASKS the
# severity cell for these sources; all other columns are content-derived. The staleness band
# itself keeps working for the ISSUE actor (worsened-delta reads the store, not this render).
# Pinned to the now-aware parsers by test_time_derived_severity_sources_pin_matches_parsers.
# CONTRACT with parse_eng_graph_moc (parsers.py): only `severity` and `payload_hash` may
# absorb `now`; every OTHER Signal field the STATUS render emits (source, summary,
# produced_at, ref) MUST stay content-only -- the mask is column-granular (severity), so a
# parser that leaks the calendar into summary/produced_at would reopen P1-1. Guarded by the
# parser-routed regression test_render_status_stable_across_staleness_boundary.
_TIME_DERIVED_SEVERITY_SOURCES = frozenset({"vault-eng-graph"})
# Cell text deliberately carries NO ADR citation (the footer note cites it once): the cell is
# rendered payload, so every wording change = a cosmetic drift-PR. Keep it stable.
_TIME_DERIVED_SEVERITY_MASK = "(masked: time-derived)"


def _md_cell(value) -> str:
    """Single-line markdown table cell (escape pipes/newlines). Pure."""
    s = "" if value is None else str(value)
    return s.replace("|", "\\|").replace("\n", " ").strip()


def _md_table(columns, rows_cells) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(cells) + " |" for cells in rows_cells]
    return "\n".join([header, sep] + body)


def _status_cell(row, col):
    """One STATUS cell; masks the time-derived severity of staleness-class sources so the
    rendered region stays a pure function of non-time-derived content (amendment P1)."""
    if col == "severity" and row.get("source") in _TIME_DERIVED_SEVERITY_SOURCES:
        return _md_cell(_TIME_DERIVED_SEVERITY_MASK)
    return _md_cell(row.get(col))


def render_status_multi_repo(store):
    """Deterministic, CLOCK-FREE governor signal snapshot from store.latest_per_source().

    Columns source|severity|summary|produced_at|ref, ordered by source (the store returns rows
    ORDER BY source). NO wall-clock / no time-derived value -- the change-key is signal STATE
    only (spec sec 5.1 / 6.3); the time-derived severity of staleness-class sources is MASKED
    (see _TIME_DERIVED_SEVERITY_SOURCES) so the calendar alone can never produce drift.
    produced_at is the artifact's own timestamp (from the signal), never the current time.
    Returns None when the store holds no signals (cannot compute).
    """
    rows = store.latest_per_source()
    if not rows:
        return None
    cells = [[_status_cell(r, c) for c in _STATUS_COLS] for r in rows]
    table = _md_table(_STATUS_COLS, cells)
    note = ("\n\n_Auto-synced governor signal snapshot; human prose elsewhere is "
            "authoritative. Time-derived severities are masked (ADR-0039 amendment P1)._")
    return table + note


_VAULT_LINT_SOURCES = ("vault-gap", "vault-coherence", "vault-whatsmissing")
_VAULT_LINT_COLS = ("report", "severity", "summary", "produced_at", "ref")


def render_vault_lint_status(store):
    """Deterministic, CLOCK-FREE vault lint dashboard from the three vault lint signals.

    Filters store.latest_per_source() to vault-gap / vault-coherence / vault-whatsmissing,
    iterated in fixed order (deterministic regardless of dict ordering). Columns
    report|severity|summary|produced_at|ref. Severity is CONTENT-based: parse_vault_report
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


# ---------------------------------------------------------------------------
# The actor -- the only new autonomy surface. Opens/updates PRs, NEVER merges.
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Real gh_api -- GitHub REST contents+pulls API (clone-agnostic; works for vault without a
# local clone). Tests inject a FAKE -> network/gh NEVER hit. All HTTP goes through one
# monkeypatchable chokepoint `_http`. The builder NEVER emits a merge route/flag (spec sec 6.2).
# ---------------------------------------------------------------------------

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
            f"Opened by the R1 reconcile actor; a human disposes (human-only earn window).\n\n"
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

    Idempotent at the branch level (LIVE branches; a stale branch is reset once, below): if
    the branch already carries identical content the PUT is skipped (no new commit / no new
    trace-id -> no churn). Reuses an open PR for the branch.

    Stale-branch GC (vault #258 incident 2026-06-11): the actor's contract is
    branch-exists <=> open-PR-pending. If the branch already exists (422) but NO open PR
    points at it, it is a leftover from an already-merged/closed PR (repos without
    delete-on-merge keep it): reusing it would diff against the OLD merge-base
    (add/add conflict -- #252 -> #258). So the ref is force-reset to the CURRENT base sha
    BEFORE any write; the discarded commits are the actor's own dead deterministic commits.
    A LIVE branch (open PR present) is NEVER reset -- the dedup keeps it churn-free.
    The GC assumes the `auto/governor-reconcile-*` namespace is ACTOR-EXCLUSIVE: a human
    commit pushed there without an open PR is garbage-collected by the reset (by design;
    humans own every other namespace).

    Precondition (actor contract): `content` DIFFERS from the file on `base` (the actor
    calls this only on drift), so post-reset the dedup always PUTs. A direct caller passing
    content identical to base ends fail-closed: dedup skips the PUT and the PR create on a
    zero-diff branch raises (isolated per-leg by the actor, never a junk PR).

    `content` is expected PRE-SANITIZED of control bytes: the only real caller (reconcile_actor)
    routes it through `splice` -> `_strip_control_bytes`, so the PUT never re-emits binary. This
    builder does NOT re-sanitize (single chokepoint is `splice`); a direct caller passing raw
    contaminated bytes would PUT them verbatim."""
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
    branch_existed = status == 422
    owner = repo.split("/")[0]
    status, data = _http("GET", f"{_API}/repos/{repo}/pulls?state=open&head={owner}:{branch}",
                         token=wtok)
    open_pr = data[0] if (status == 200 and isinstance(data, list) and data) else None
    # Non-200 on the PR lookup -> open_pr unknown: do NOT reset (a live PR's branch must
    # never be destroyed on a doubt); proceed as before, the per-leg isolation catches it.
    if branch_existed and status == 200 and open_pr is None:
        status, _d = _http("PATCH", f"{_API}/repos/{repo}/git/refs/heads/{branch}", token=wtok,
                           json_body={"sha": base_sha, "force": True})
        if status != 200:
            raise RuntimeError(f"force-reset stale branch {branch} -> HTTP {status}")
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
    if open_pr is not None:
        return {"number": open_pr["number"], "action": "reused",
                "url": open_pr.get("html_url", "")}
    pr_body = (f"Deterministic reconcile of the {rid} GOVERNOR-SYNC region (R1 open-PR rung). "
               f"Human-only disposition during the earn window (actor-activation-criteria sec "
               f"6); this PR is inert until a human merges it.")
    status, data = _http("POST", f"{_API}/repos/{repo}/pulls", token=wtok,
                         json_body={"title": _commit_subject(rid), "head": branch,
                                    "base": base, "body": pr_body})
    if status not in (200, 201):
        raise RuntimeError(f"create PR {branch} -> HTTP {status}")
    return {"number": data.get("number"), "action": "created", "url": data.get("html_url", "")}


# ---------------------------------------------------------------------------
# The BUILT reconciler set (spec sec 5) + real_gh_api factory + manual entrypoint.
# ---------------------------------------------------------------------------

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
> clock-free. Branch+PR only; disposition is Eduardo-only (vault sibling-peer)."""


def build_reconcilers():
    """The BUILT reconciler set (spec sec 5). Construction RAISES if any target is doctrine
    (the __post_init__ fail-closed guard).

    ADDING A LEG IS NOT A CODE-ONLY CHANGE: every new reconciler REQUIRES an explicit Eduardo
    doctrine-classification review of its target, recorded in ADR-0039 (spec sec 4.2). The
    __post_init__ `is_doctrine` guard enforces only the STATIC carve-out subset; it CANNOT catch
    ADR-0038's content-based catch-all (a new governance file at an unforeseen path). That clause
    is the human checkpoint, not this backstop -- do not add a leg without the recorded review."""
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


def main():
    """Manual entrypoint: `python -m governor.reconcile` (no cron; Fase-4 out of scope).

    Takes NO argv: the write credential is read from the env (GOVERNOR_RECONCILE_TOKEN), never a
    command-line flag (CWE-214 -- no token on the process arg list)."""
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
