# SoT Drift Sentinel -- GGv2 (frontend) extension -- Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a sovereign fleet-side detector that flags SoT drift when a Game-Godot-v2 (frontend) `feat` PR touches an area mapped to a vault SoT doc, without touching GGv2.

**Architecture:** A Python detector (`scripts/fleet/`) polls GGv2 merged PRs read-only (`gh`), filters to `feat(...)` PRs, matches changed paths against a JSON watch-map, and opens/updates ONE Game issue (distinct label `sot-drift-candidate-ggv2`, avoiding clobber with the Game Action's label-only issue reuse). The existing verdict subagent `sot-drift-verifier` and the governor pane are reused; the governor gets one extra source to count the new label. Read-only on GGv2 + vault; the only write is the Game issue (owned repo).

**Tech Stack:** Python 3.12 stdlib only (`json`, `re`, `subprocess`, `datetime`, `argparse`) -- no new deps. pytest (`--import-mode=importlib`). `gh` CLI. PowerShell (Scheduled Task registration). ASCII-first (ADR-0021). Commit trailers ADR-0011 (`Coding-Agent` + `Trace-Id`, NO `Co-Authored-By`).

**Spec:** `docs/superpowers/specs/2026-07-13-sot-drift-ggv2-extension-design.md`

**Deviation from spec:** watch-map is `ggv2-watch-map.json` (not `.yml`) -- stdlib `json` parse, zero PyYAML dep. Same content.

---

## File structure

| File | Net | Responsibility |
|------|-----|----------------|
| `ops/sot-drift/ggv2-watch-map.json` | NEW | GGv2 path-glob -> vault SoT-ref map (human-edited, extend on demand) |
| `scripts/fleet/sot_drift_ggv2_detect.py` | NEW | Detector: pure matcher/filter/checkpoint + gh poll + idempotent Game issue |
| `scripts/tests/test_sot_drift_ggv2_detect.py` | NEW | Unit tests: matcher, feat-filter, checkpoint, poll-filter, issue body, create-vs-edit |
| `scripts/fleet/register-sot-drift-ggv2-task.ps1` | NEW | Windows Scheduled Task daily (Lenovo) |
| `apps/cross-repo-dashboard/governor/ingest.py` | MOD | +1 source (label `sot-drift-candidate-ggv2`) |
| `apps/cross-repo-dashboard/governor/parsers.py` | MOD | distinct source/ref for the frontend signal (reuse counter) |
| `apps/cross-repo-dashboard/tests/test_governor_ingest.py` | MOD | cover the new source |
| `docs/KNOWLEDGE_MAP.md` | MOD | wire the GGv2 extension into Drift automation section |

Module filename uses underscores (`sot_drift_ggv2_detect.py`) so pytest importlib can import it directly; the Scheduled Task calls it by path.

---

## Task 1: watch-map JSON config

**Files:**
- Create: `ops/sot-drift/ggv2-watch-map.json`

- [ ] **Step 1: Create the watch-map**

```json
{
  "_doc": "GGv2 (frontend) path-glob -> vault SoT-ref. Consumed by scripts/fleet/sot_drift_ggv2_detect.py. sot_ref = vault Spaces/Dev/Evo-Tactics/<ref>. Extend conservatively: only concepts with a canonical SoT doc. Globs: * = within a path segment, ** = any depth.",
  "entries": [
    { "concept": "audio direction / impl",
      "patterns": ["assets/audio/**", "default_bus_layout.tres", "scripts/audio/**"],
      "sot_ref": ["adr/ADR-2026-04-18-audio-direction-placeholder.md", "core/00F-ART_AUDIO_BUSINESS.md"] },
    { "concept": "VFX / art direction",
      "patterns": ["assets/vfx/**", "scripts/vfx/**"],
      "sot_ref": ["adr/ADR-2026-04-18-art-direction-placeholder.md", "core/41-ART-DIRECTION.md", "core/45-VISUAL-IDENTITY-CANONICAL.md"] },
    { "concept": "UI / HUD identity",
      "patterns": ["assets/ui/**", "scripts/ui/**"],
      "sot_ref": ["core/30-UI_TV_IDENTITA.md", "core/42-STYLE-GUIDE-UI.md", "core/44-HUD-LAYOUT-REFERENCES.md"] },
    { "concept": "screen flow / schermate",
      "patterns": ["scenes/**"],
      "sot_ref": ["core/17-SCREEN_FLOW.md"] },
    { "concept": "combat d20 / tattico",
      "patterns": ["scripts/combat/**"],
      "sot_ref": ["core/10-SISTEMA_TATTICO.md", "core/11-REGOLE_D20_TV.md"] },
    { "concept": "campaign loop / descent",
      "patterns": ["scripts/campaign/**"],
      "sot_ref": ["core/03-LOOP.md", "core/15-LEVEL_DESIGN.md", "core/40-ROADMAP.md"] },
    { "concept": "progression / economy",
      "patterns": ["scripts/progression/**"],
      "sot_ref": ["core/25-REGOLE_SBLOCCO_PE.md", "core/26-ECONOMY_CANONICAL.md"] },
    { "concept": "narrative / VC telemetry",
      "patterns": ["scripts/narrative/**"],
      "sot_ref": ["core/24-TELEMETRIA_VC.md"] },
    { "concept": "Nido / mating surfaces",
      "patterns": ["scripts/session/**", "scripts/phone/**"],
      "sot_ref": ["core/27-MATING_NIDO.md"] }
  ]
}
```

- [ ] **Step 2: Validate it parses**

Run: `py -c "import json; d=json.load(open('ops/sot-drift/ggv2-watch-map.json',encoding='utf-8')); print(len(d['entries']),'entries')"`
Expected: `9 entries`

- [ ] **Step 3: Commit**

```bash
git add ops/sot-drift/ggv2-watch-map.json
git commit -F- <<'MSG'
feat(sot-drift): GGv2 watch-map (frontend path-glob -> vault SoT ref)

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
MSG
```

---

## Task 2: matcher + feat-filter (pure, TDD)

**Files:**
- Create: `scripts/fleet/sot_drift_ggv2_detect.py`
- Test: `scripts/tests/test_sot_drift_ggv2_detect.py`

- [ ] **Step 1: Write the failing tests**

```python
# scripts/tests/test_sot_drift_ggv2_detect.py
import importlib.util
import pathlib

_MOD = pathlib.Path(__file__).resolve().parents[1] / "fleet" / "sot_drift_ggv2_detect.py"
_spec = importlib.util.spec_from_file_location("sot_drift_ggv2_detect", _MOD)
det = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(det)

MAP = [
    {"concept": "audio", "patterns": ["assets/audio/**", "default_bus_layout.tres"],
     "sot_ref": ["adr/audio.md"]},
    {"concept": "ui", "patterns": ["scripts/ui/**"], "sot_ref": ["core/30.md"]},
]


def test_matches_nested_glob_and_collects_files():
    m = det.match_changes(MAP, ["assets/audio/sfx/hit.wav", "README.md"])
    assert len(m) == 1
    assert m[0]["concept"] == "audio"
    assert m[0]["files"] == ["assets/audio/sfx/hit.wav"]


def test_matches_exact_file_pattern():
    m = det.match_changes(MAP, ["default_bus_layout.tres"])
    assert len(m) == 1 and m[0]["concept"] == "audio"


def test_no_match_returns_empty():
    assert det.match_changes(MAP, ["scripts/combat/x.gd", "README.md"]) == []


def test_single_star_does_not_cross_directory():
    # 'scripts/ui/**' matches any depth; a bare '*' would not cross '/'
    rx = det.glob_to_regex("data/economy*")
    assert rx.match("data/economy_x.json")
    assert not rx.match("data/economy/sub/x.json")


def test_is_feature_pr():
    assert det.is_feature_pr("feat(audio): bus layout")
    assert det.is_feature_pr("feat: something")
    assert det.is_feature_pr("feat(vfx)!: breaking")
    assert not det.is_feature_pr("fix(audio): crackle")
    assert not det.is_feature_pr("chore: bump")
    assert not det.is_feature_pr("docs: readme")
    assert not det.is_feature_pr("")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Expected: FAIL -- `module ... has no attribute 'match_changes'` (file not created yet).

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/fleet/sot_drift_ggv2_detect.py
"""SoT drift detector for Game-Godot-v2 (frontend) ships.

Polls merged GGv2 PRs (read-only, gh), keeps only feat() PRs, matches changed
paths against a JSON watch-map, and opens/updates ONE Game issue (label
sot-drift-candidate-ggv2) listing the vault SoT refs to review. Read-only on
GGv2 + vault; the only write is the Game issue (owned repo). Semantic verdict
+ vault reconcile stay with the sovereign sot-drift-verifier subagent (gated).
"""
import re

_FEAT_RE = re.compile(r"^feat(\([^)]*\))?!?:", re.IGNORECASE)


def glob_to_regex(glob):
    # Escape regex specials except '*'. Then: '**/' = any dirs (incl none),
    # '**' = anything, '*' = within one path segment.
    s = re.sub(r"([.+^${}()|\[\]\\])", r"\\\1", glob)
    s = s.replace("**/", "@@DD@@").replace("**", "@@D@@").replace("*", "[^/]*")
    s = s.replace("@@DD@@", "(?:[^/]+/)*").replace("@@D@@", ".*")
    return re.compile("^" + s + "$")


def match_changes(watch_map, changed_files):
    out = []
    for entry in watch_map:
        rxs = [glob_to_regex(p) for p in entry["patterns"]]
        files = sorted({f for f in changed_files if any(rx.match(f) for rx in rxs)})
        if files:
            out.append({"concept": entry["concept"], "sot_ref": entry["sot_ref"],
                        "patterns": entry["patterns"], "files": files})
    return out


def is_feature_pr(title):
    return bool(_FEAT_RE.match((title or "").strip()))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/fleet/sot_drift_ggv2_detect.py scripts/tests/test_sot_drift_ggv2_detect.py
git commit -F- <<'MSG'
feat(sot-drift): GGv2 detector matcher + feat-filter (TDD)

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
MSG
```

---

## Task 3: watch-map loader + checkpoint (TDD)

**Files:**
- Modify: `scripts/fleet/sot_drift_ggv2_detect.py`
- Test: `scripts/tests/test_sot_drift_ggv2_detect.py`

- [ ] **Step 1: Add failing tests**

```python
# append to scripts/tests/test_sot_drift_ggv2_detect.py
import json


def test_load_watch_map(tmp_path):
    p = tmp_path / "wm.json"
    p.write_text(json.dumps({"entries": [{"concept": "a", "patterns": ["x/**"], "sot_ref": ["y"]}]}), encoding="utf-8")
    wm = det.load_watch_map(str(p))
    assert wm == [{"concept": "a", "patterns": ["x/**"], "sot_ref": ["y"]}]


def test_checkpoint_round_trip(tmp_path):
    p = tmp_path / "sub" / "cp.json"
    det.save_checkpoint(str(p), {"last_merged_at": "2026-07-13T00:00:00Z"})
    assert det.load_checkpoint(str(p)) == {"last_merged_at": "2026-07-13T00:00:00Z"}


def test_load_checkpoint_missing_returns_empty(tmp_path):
    assert det.load_checkpoint(str(tmp_path / "nope.json")) == {}


def test_load_checkpoint_corrupt_returns_empty(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    assert det.load_checkpoint(str(p)) == {}
```

- [ ] **Step 2: Run to verify fail**

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Expected: FAIL -- `has no attribute 'load_watch_map'`.

- [ ] **Step 3: Implement**

```python
# append to scripts/fleet/sot_drift_ggv2_detect.py
import json
import os


def load_watch_map(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["entries"]


def load_checkpoint(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_checkpoint(path, data):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
```

- [ ] **Step 4: Run to verify pass**

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Expected: PASS (10 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/fleet/sot_drift_ggv2_detect.py scripts/tests/test_sot_drift_ggv2_detect.py
git commit -F- <<'MSG'
feat(sot-drift): GGv2 watch-map loader + checkpoint (TDD)

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
MSG
```

---

## Task 4: poll-filter + issue body (TDD, gh injected)

**Files:**
- Modify: `scripts/fleet/sot_drift_ggv2_detect.py`
- Test: `scripts/tests/test_sot_drift_ggv2_detect.py`

- [ ] **Step 1: Add failing tests**

```python
# append to scripts/tests/test_sot_drift_ggv2_detect.py
def test_new_prs_since_filters_and_sorts():
    prs = [
        {"number": 3, "title": "feat: c", "mergedAt": "2026-07-13T10:00:00Z"},
        {"number": 1, "title": "feat: a", "mergedAt": "2026-07-12T09:00:00Z"},
        {"number": 2, "title": "feat: b", "mergedAt": "2026-07-13T08:00:00Z"},
    ]
    fresh = det.new_prs_since(prs, {"last_merged_at": "2026-07-12T12:00:00Z"})
    assert [p["number"] for p in fresh] == [2, 3]  # PR1 too old; sorted asc


def test_new_prs_since_empty_checkpoint_uses_all():
    prs = [{"number": 1, "title": "feat: a", "mergedAt": "2026-07-13T08:00:00Z"}]
    assert len(det.new_prs_since(prs, {})) == 1


def test_build_issue_body_lists_prs_and_refs():
    per_pr = [
        {"pr": {"number": 599, "title": "feat(audio): bus"},
         "matches": [{"concept": "audio", "sot_ref": ["adr/audio.md"], "patterns": ["assets/audio/**"],
                      "files": ["assets/audio/x.wav"]}]},
    ]
    body = det.build_issue_body(per_pr)
    assert "<!-- sot-drift-ggv2 -->" in body
    assert "#599" in body
    assert "adr/audio.md" in body
    assert "sot-drift-verifier" in body
```

- [ ] **Step 2: Run to verify fail**

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Expected: FAIL -- `has no attribute 'new_prs_since'`.

- [ ] **Step 3: Implement**

```python
# append to scripts/fleet/sot_drift_ggv2_detect.py

MARKER = "<!-- sot-drift-ggv2 -->"


def new_prs_since(prs, checkpoint):
    last = checkpoint.get("last_merged_at") or ""
    fresh = [p for p in prs if (p.get("mergedAt") or "") > last]
    return sorted(fresh, key=lambda p: p.get("mergedAt") or "")


def build_issue_body(per_pr):
    lines = [
        MARKER,
        "## SoT drift candidate -- Game-Godot-v2 frontend (auto-detected)",
        "",
        "Frontend `feat` PR(s) touched areas mapped to canonical vault SoT docs.",
        "**Deterministic flag only** -- semantic verdict is gated: invoke the sovereign",
        "`sot-drift-verifier` subagent to verdict + (if stale) propose a vault branch+PR reconcile.",
        "",
    ]
    for item in per_pr:
        pr = item["pr"]
        lines.append(f"### GGv2 PR #{pr['number']} -- {pr['title']}")
        for m in item["matches"]:
            refs = ", ".join(f"`{r}`" for r in m["sot_ref"])
            lines.append(f"- **{m['concept']}** (`{'`, `'.join(m['patterns'])}`) -> review SoT: {refs}")
            for f in m["files"]:
                lines.append(f"  - changed: `{f}`")
        lines.append("")
    lines.append("_Boundary: vault reconcile = branch+PR, merge human-only. GGv2 never written._")
    return "\n".join(lines)
```

- [ ] **Step 4: Run to verify pass**

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Expected: PASS (13 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/fleet/sot_drift_ggv2_detect.py scripts/tests/test_sot_drift_ggv2_detect.py
git commit -F- <<'MSG'
feat(sot-drift): GGv2 poll-filter + issue body (TDD)

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
MSG
```

---

## Task 5: gh integration + issue open/update + main() (TDD w/ fake runner)

**Files:**
- Modify: `scripts/fleet/sot_drift_ggv2_detect.py`
- Test: `scripts/tests/test_sot_drift_ggv2_detect.py`

- [ ] **Step 1: Add failing tests (fake gh runner, no network)**

```python
# append to scripts/tests/test_sot_drift_ggv2_detect.py
class FakeGh:
    """Records gh argv; returns queued stdout per matched command prefix."""
    def __init__(self, responses):
        self.responses = responses  # list[(match_substr, stdout)]
        self.calls = []

    def __call__(self, args):
        self.calls.append(args)
        joined = " ".join(args)
        for sub, out in self.responses:
            if sub in joined:
                return out
        return ""


def test_open_or_update_creates_when_none_open():
    gh = FakeGh([("issue list", "")])  # no existing open issue
    det.open_or_update_issue(gh, "body-x", repo="OWN/Game")
    joined = [" ".join(c) for c in gh.calls]
    assert any("issue list" in j for j in joined)
    assert any("issue create" in j for j in joined)
    assert not any("issue edit" in j for j in joined)


def test_open_or_update_edits_when_open_exists():
    gh = FakeGh([("issue list", "42\n")])  # existing issue #42
    det.open_or_update_issue(gh, "body-x", repo="OWN/Game")
    joined = [" ".join(c) for c in gh.calls]
    assert any("issue edit" in j and "42" in j for j in joined)
    assert not any("issue create" in j for j in joined)
```

- [ ] **Step 2: Run to verify fail**

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Expected: FAIL -- `has no attribute 'open_or_update_issue'`.

- [ ] **Step 3: Implement gh wrapper, issue logic, main()**

```python
# append to scripts/fleet/sot_drift_ggv2_detect.py
import argparse
import datetime
import subprocess
import sys
import tempfile

GGV2_REPO = "MasterDD-L34D/Game-Godot-v2"
GAME_REPO = "MasterDD-L34D/Game"
LABEL = "sot-drift-candidate-ggv2"


def run_gh(args):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed (rc={r.returncode}): {r.stderr.strip()}")
    return r.stdout


def fetch_merged_prs(runner, repo=GGV2_REPO, limit=50):
    out = runner(["pr", "list", "--repo", repo, "--base", "main", "--state", "merged",
                  "--json", "number,title,mergedAt,files", "--limit", str(limit)])
    return json.loads(out) if out.strip() else []


def _write_tmp(body):
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(body)
    return path


def open_or_update_issue(runner, body, repo=GAME_REPO):
    existing = runner(["issue", "list", "--repo", repo, "--label", LABEL, "--state", "open",
                       "--json", "number", "--jq", ".[0].number"]).strip()
    path = _write_tmp(body)
    try:
        if existing and existing != "null":
            runner(["issue", "edit", existing, "--repo", repo, "--body-file", path])
            runner(["issue", "comment", existing, "--repo", repo,
                    "--body", "Updated: new GGv2 SoT drift candidate detected."])
            return ("edit", existing)
        num = runner(["issue", "create", "--repo", repo, "--label", LABEL,
                      "--title", "SoT drift candidate -- GGv2 frontend ahead of SoT docs",
                      "--body-file", path]).strip()
        return ("create", num)
    finally:
        os.remove(path)


def detect(runner, watch_map_path, checkpoint_path, lookback_days=7, dry_run=False):
    watch_map = load_watch_map(watch_map_path)
    checkpoint = load_checkpoint(checkpoint_path)
    if not checkpoint.get("last_merged_at"):
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=lookback_days)
        checkpoint = {"last_merged_at": cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")}
    prs = new_prs_since(fetch_merged_prs(runner), checkpoint)
    per_pr = []
    for pr in prs:
        if not is_feature_pr(pr.get("title")):
            continue
        files = [f["path"] for f in pr.get("files", [])]
        matches = match_changes(watch_map, files)
        if matches:
            per_pr.append({"pr": pr, "matches": matches})
    result = {"scanned": len(prs), "flagged": len(per_pr)}
    if per_pr and not dry_run:
        action, num = open_or_update_issue(runner, build_issue_body(per_pr))
        result["issue"] = {"action": action, "number": num}
    elif per_pr:
        result["issue"] = {"action": "dry-run"}
    # Advance checkpoint to the newest merged PR we saw (only if fetch succeeded).
    if prs:
        checkpoint["last_merged_at"] = prs[-1]["mergedAt"]
        if not dry_run:
            save_checkpoint(checkpoint_path, checkpoint)
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="SoT drift detector for Game-Godot-v2 frontend ships.")
    ap.add_argument("--watch-map", default="ops/sot-drift/ggv2-watch-map.json")
    ap.add_argument("--checkpoint", default="logs/sot-drift-ggv2-checkpoint.json")
    ap.add_argument("--lookback-days", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    res = detect(run_gh, args.watch_map, args.checkpoint,
                 lookback_days=args.lookback_days, dry_run=args.dry_run)
    print(json.dumps(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run to verify pass**

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Expected: PASS (15 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/fleet/sot_drift_ggv2_detect.py scripts/tests/test_sot_drift_ggv2_detect.py
git commit -F- <<'MSG'
feat(sot-drift): GGv2 gh integration + idempotent issue + main (TDD)

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
MSG
```

---

## Task 6: QG Step-1 smoke -- end-to-end dry-run against live GGv2 (read-only)

**Files:**
- No repo file (ephemeral run). Records result in the PR body.

- [ ] **Step 1: Dry-run with a wide lookback (read-only, opens NO issue)**

Run: `py scripts/fleet/sot_drift_ggv2_detect.py --dry-run --lookback-days 30 --checkpoint /tmp/cp-smoke.json`
Expected: JSON like `{"scanned": N, "flagged": M, "issue": {"action": "dry-run"}}`. Because #599 (feat audio) + #601 (feat vfx) merged 2026-07-12/13, a 30-day lookback should flag audio + VFX concepts. Confirm the printed run shows `flagged >= 1`.

- [ ] **Step 2: Verify the matched refs are correct**

Add a temporary debug print OR re-run with a tiny wrapper:
```bash
py -c "import json,sys; sys.path.insert(0,'scripts/fleet'); import sot_drift_ggv2_detect as d; \
r=d.detect(d.run_gh,'ops/sot-drift/ggv2-watch-map.json','/tmp/cp-smoke.json',lookback_days=30,dry_run=True); \
print(json.dumps(r,indent=2))"
```
Expected: `flagged >= 1`; the audio/VFX PRs map to the audio/art ADR refs. If `flagged == 0`, the globs miss the real GGv2 paths -> fix Task 1 patterns before proceeding.

- [ ] **Step 3: Idempotency check (logic, no write)**

Confirm by reading `open_or_update_issue`: with the distinct label `sot-drift-candidate-ggv2`, `issue list --jq '.[0].number'` returns the single GGv2 issue (label is producer-exclusive) -> edit not create on 2nd run. Document expected: no duplicate.

- [ ] **Step 4: Record smoke result**

In the codemasterdd PR body add: "QG Step-1 smoke: dry-run over 30d flagged audio+VFX (correct ADR refs); idempotent (distinct label = producer-exclusive, edit-on-2nd). No live issue opened (dry-run)."

- [ ] **Step 5: Clean up**

```bash
rm -f /tmp/cp-smoke.json
```

---

## Task 7: Game label bootstrap (one-time, maintainer)

**Files:**
- No repo file. One-time `gh` command.

- [ ] **Step 1: Create the distinct label in Game (idempotent)**

Run (once, by Eduardo / repo maintainer):
```bash
gh label create sot-drift-candidate-ggv2 --repo MasterDD-L34D/Game \
  --color 5319E7 --description "GGv2 frontend may be ahead of vault SoT docs" || true
```
Expected: label created (or already-exists no-op). Distinct color from the backend `sot-drift-candidate` label.

- [ ] **Step 2: Document in PR body**

Note: "Label `sot-drift-candidate-ggv2` created in Game (one-time). Distinct from backend `sot-drift-candidate` -> no clobber."

---

## Task 8: governor +1 source (TDD)

**Files:**
- Modify: `apps/cross-repo-dashboard/governor/ingest.py`
- Modify: `apps/cross-repo-dashboard/governor/parsers.py`
- Test: `apps/cross-repo-dashboard/tests/test_governor_ingest.py`

- [ ] **Step 1: Add a failing test**

```python
# append to apps/cross-repo-dashboard/tests/test_governor_ingest.py
def test_ggv2_sot_drift_source_is_registered_and_counts():
    from governor import ingest
    ids = [s["id"] for s in ingest.SOURCES]
    assert "game-sot-drift-ggv2" in ids

    from governor.parsers import parse_sot_drift_issues
    sig = parse_sot_drift_issues([{"updatedAt": "2026-07-13T00:00:00Z"}], "ref-ggv2")
    assert sig.counts["open"] == 1
```

- [ ] **Step 2: Run to verify fail**

Run: `py -3 -m pytest -q apps/cross-repo-dashboard/tests/test_governor_ingest.py`
(Run from `apps/cross-repo-dashboard`, matching the existing test invocation.)
Expected: FAIL -- `"game-sot-drift-ggv2"` not in ids.

- [ ] **Step 3: Implement -- add the URL const + SOURCES entry + fetch branch**

In `apps/cross-repo-dashboard/governor/ingest.py`, after `SOT_ISSUES_URL` (line ~26) add:
```python
SOT_GGV2_ISSUES_URL = "https://api.github.com/repos/MasterDD-L34D/Game/issues?labels=sot-drift-candidate-ggv2&state=open"
```
In the `SOURCES` list, after the `game-sot-drift` entry add:
```python
    {"id": "game-sot-drift-ggv2", "style": "gh-issues-ggv2"},
```
In the style dispatch (near the existing `if style == "gh-issues":` at line ~130) add:
```python
    if style == "gh-issues-ggv2":
        sig = parse_sot_drift_issues(json_getter(SOT_GGV2_ISSUES_URL), SOT_GGV2_ISSUES_URL)
        sig.source = "game-sot-drift-ggv2"
        return sig
```

In `apps/cross-repo-dashboard/governor/parsers.py`, make `parse_sot_drift_issues` label the source from the ref so the two signals are distinct. Change the `summary_text`/`source` block (line ~216-218) to:
```python
    is_ggv2 = "ggv2" in (ref or "")
    label = "frontend (GGv2)" if is_ggv2 else "backend (Game)"
    summary_text = f"{open_count} open SoT drift candidate(s) -- {label}"
    return Signal(
        source="game-sot-drift-ggv2" if is_ggv2 else "game-sot-drift",
        kind="sot-drift",
```
(Leave the rest of the Signal construction unchanged.)

- [ ] **Step 4: Run to verify pass**

Run: `py -3 -m pytest -q apps/cross-repo-dashboard/tests/test_governor_ingest.py apps/cross-repo-dashboard/tests/test_governor_parsers.py`
Expected: PASS (new test + existing parser tests still green).

- [ ] **Step 5: Commit**

```bash
git add apps/cross-repo-dashboard/governor/ingest.py apps/cross-repo-dashboard/governor/parsers.py apps/cross-repo-dashboard/tests/test_governor_ingest.py
git commit -F- <<'MSG'
feat(governor): count GGv2 SoT drift candidates as a distinct signal

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
MSG
```

---

## Task 9: Scheduled Task registration (Lenovo)

**Files:**
- Create: `scripts/fleet/register-sot-drift-ggv2-task.ps1`

- [ ] **Step 1: Create the register script (mirror register-governor-ingest-task.ps1)**

```powershell
<#
.SYNOPSIS
Registers the sot-drift-ggv2 detector Windows scheduled task (idempotent).

.DESCRIPTION
Runs `py -3 scripts/fleet/sot_drift_ggv2_detect.py` daily on the canonical host
(Lenovo). Polls Game-Godot-v2 merged PRs READ-ONLY, and on a feat() ship that
touches a watched frontend area opens/updates ONE Game issue labelled
sot-drift-candidate-ggv2. The only write is that Game issue. Mirrors
register-governor-ingest-task.ps1.

Auth: needs `gh`. Interactive (default) uses the logged-in gh auth. -Unattended
(S4U, survives logged-off; ELEVATED shell) may lack the user gh auth under the
partial profile -> pass a GitHub token via the GH_TOKEN environment variable for
the task principal, or keep Interactive.

Usage:
  powershell -NoProfile -ExecutionPolicy Bypass -File register-sot-drift-ggv2-task.ps1
  powershell -NoProfile -ExecutionPolicy Bypass -File register-sot-drift-ggv2-task.ps1 -Unattended
  powershell -NoProfile -ExecutionPolicy Bypass -File register-sot-drift-ggv2-task.ps1 -Unregister
#>
[CmdletBinding()]
param(
  [switch]$Unregister,
  [switch]$Unattended,
  [string]$At = '09:00',
  [string]$WorkDir = 'C:\dev\codemasterdd-ai-station'
)
$ErrorActionPreference = 'Stop'
$taskName = 'sot-drift-ggv2'

if ($Unregister) {
  $existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
  if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "UNREGISTERED '$taskName' on $env:COMPUTERNAME."
  } else {
    Write-Host "'$taskName' not present on $env:COMPUTERNAME (nothing to do)."
  }
  return
}

$script = Join-Path $WorkDir 'scripts\fleet\sot_drift_ggv2_detect.py'
if (-not (Test-Path $script)) { throw "detector not found: $script" }

$pyExe = (Get-Command py -ErrorAction SilentlyContinue).Source
if (-not $pyExe) { throw "py launcher not found on $env:COMPUTERNAME" }

$action    = New-ScheduledTaskAction -Execute $pyExe -Argument "-3 scripts\fleet\sot_drift_ggv2_detect.py" -WorkingDirectory $WorkDir
$trigger   = New-ScheduledTaskTrigger -Daily -At $At
$logonType = if ($Unattended) { 'S4U' } else { 'Interactive' }
$principal = New-ScheduledTaskPrincipal -UserId "$env:COMPUTERNAME\$env:USERNAME" -LogonType $logonType -RunLevel Limited
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -DontStopOnIdleEnd
$desc      = "Sovereign SoT-drift detector for Game-Godot-v2 frontend ships. READ-ONLY poll; opens one Game issue (label sot-drift-candidate-ggv2). Verdict + vault reconcile stay human-gated."

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description $desc -Force | Out-Null

$t = Get-ScheduledTask -TaskName $taskName
Write-Host "REGISTERED '$taskName' on $env:COMPUTERNAME."
Write-Host ("  Trigger  : daily @ " + (($t.Triggers | Select-Object -First 1).StartBoundary))
Write-Host ("  Action   : " + ($t.Actions | ForEach-Object { $_.Execute + ' ' + $_.Arguments }))
Write-Host "  Verify run-once: Start-ScheduledTask -TaskName '$taskName'; (Get-ScheduledTaskInfo '$taskName').LastTaskResult  # 0 = ok"
```

- [ ] **Step 2: ASCII-guard check**

Run: `py -c "[print(i) for i,l in enumerate(open('scripts/fleet/register-sot-drift-ggv2-task.ps1',encoding='utf-8'),1) if any(ord(c)>127 for c in l)] or print('ascii-clean')"`
Expected: `ascii-clean`.

- [ ] **Step 3: Commit (do NOT register here -- registration is a manual op on Lenovo)**

```bash
git add scripts/fleet/register-sot-drift-ggv2-task.ps1
git commit -F- <<'MSG'
feat(sot-drift): GGv2 detector scheduled-task registrar (Lenovo daily)

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
MSG
```

---

## Task 10: QG Step-2 (edge) + Step-3 (glob tuning) + wire docs

**Files:**
- Modify: `scripts/tests/test_sot_drift_ggv2_detect.py`
- Modify: `docs/KNOWLEDGE_MAP.md`

- [ ] **Step 1: Add edge tests (QG Step-2)**

```python
# append to scripts/tests/test_sot_drift_ggv2_detect.py
def test_detect_skips_non_feat_prs(tmp_path):
    wm = tmp_path / "wm.json"
    wm.write_text(json.dumps({"entries": [{"concept": "audio", "patterns": ["assets/audio/**"], "sot_ref": ["adr/a.md"]}]}), encoding="utf-8")
    gh = FakeGh([("pr list", json.dumps([
        {"number": 5, "title": "fix(audio): crackle", "mergedAt": "2026-07-13T10:00:00Z",
         "files": [{"path": "assets/audio/x.wav"}]},
    ]))])
    res = det.detect(gh, str(wm), str(tmp_path / "cp.json"), dry_run=True)
    assert res["flagged"] == 0  # fix() PR is not a feature ship


def test_detect_flags_feat_pr(tmp_path):
    wm = tmp_path / "wm.json"
    wm.write_text(json.dumps({"entries": [{"concept": "audio", "patterns": ["assets/audio/**"], "sot_ref": ["adr/a.md"]}]}), encoding="utf-8")
    gh = FakeGh([("pr list", json.dumps([
        {"number": 6, "title": "feat(audio): bus", "mergedAt": "2026-07-13T10:00:00Z",
         "files": [{"path": "assets/audio/bus.tres"}]},
    ]))])
    res = det.detect(gh, str(wm), str(tmp_path / "cp.json"), dry_run=True)
    assert res["flagged"] == 1


def test_detect_no_match_no_flag(tmp_path):
    wm = tmp_path / "wm.json"
    wm.write_text(json.dumps({"entries": [{"concept": "audio", "patterns": ["assets/audio/**"], "sot_ref": ["adr/a.md"]}]}), encoding="utf-8")
    gh = FakeGh([("pr list", json.dumps([
        {"number": 7, "title": "feat(net): reconnect", "mergedAt": "2026-07-13T10:00:00Z",
         "files": [{"path": "scripts/net/peer.gd"}]},
    ]))])
    res = det.detect(gh, str(wm), str(tmp_path / "cp.json"), dry_run=True)
    assert res["flagged"] == 0
```

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Expected: PASS (18 tests).

- [ ] **Step 2: QG Step-3 glob tuning (research + measure)**

Run the dry-run over the last ~60 days and inspect the flagged concepts vs. the noisy globs:
```bash
py scripts/fleet/sot_drift_ggv2_detect.py --dry-run --lookback-days 60 --checkpoint /tmp/cp-tune.json > /tmp/tune.json
py -c "import json; r=json.load(open('/tmp/tune.json')); print('scanned',r['scanned'],'flagged',r['flagged'])"
rm -f /tmp/cp-tune.json /tmp/tune.json
```
Decision rule: if `scripts/ui/**` or `scenes/**` produce mostly false-positive concepts (polish `feat(ui)` with no real SoT drift), narrow those two globs (e.g. drop `scenes/**`, or scope `scripts/ui/**` to specific subdirs) in `ops/sot-drift/ggv2-watch-map.json`. Record the before/after flagged count in the PR body (metric delta, per Quality Gate Step-3). Commit any watch-map narrowing with a `chore(sot-drift): tune GGv2 globs` message.

- [ ] **Step 3: Wire into KNOWLEDGE_MAP**

In `docs/KNOWLEDGE_MAP.md`, in the SoT Drift Sentinel / Drift automation section, append:
```markdown
- **GGv2 frontend extension (2026-07-13):** sovereign detector `scripts/fleet/sot_drift_ggv2_detect.py`
  polls Game-Godot-v2 merged `feat` PRs (read-only) vs `ops/sot-drift/ggv2-watch-map.json`, opens a
  Game issue label `sot-drift-candidate-ggv2` (distinct from backend to avoid clobber); governor counts
  it as a separate "frontend drift" signal; verdict = same `sot-drift-verifier` subagent. Daily task
  (Lenovo) `register-sot-drift-ggv2-task.ps1`. Spec `docs/superpowers/specs/2026-07-13-sot-drift-ggv2-extension-design.md`.
```

- [ ] **Step 4: Commit**

```bash
git add scripts/tests/test_sot_drift_ggv2_detect.py docs/KNOWLEDGE_MAP.md
git commit -F- <<'MSG'
test(sot-drift): GGv2 edge cases + wire KNOWLEDGE_MAP

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
MSG
```

---

## Task 11: harsh-review + full-suite gate (pre-merge, MANDATORY)

**Files:**
- No new files. Verification + PR.

- [ ] **Step 1: Run the targeted test suites**

Run: `py -m pytest -q scripts/tests/test_sot_drift_ggv2_detect.py`
Run (from `apps/cross-repo-dashboard`): `py -3 -m pytest -q tests/test_governor_ingest.py tests/test_governor_parsers.py`
Expected: all PASS. Paste the output into the PR body (Definition of Done: output shown).

- [ ] **Step 2: harsh-reviewer pass (SDMG, governance-critical infra)**

Dispatch the `harsh-reviewer` subagent on: `scripts/fleet/sot_drift_ggv2_detect.py`, `ops/sot-drift/ggv2-watch-map.json`, the governor diff, and the register script. Focus: the `feat()` heuristic (does it drop real drift shipped as non-feat?), glob false-positive rate, the checkpoint-advance-on-partial-failure path, and the read-only/boundary guarantees. Triage P1/P2/P3; fix P1 before merge.

- [ ] **Step 3: Open the codemasterdd PR (merge = Eduardo)**

```bash
git push -u origin <branch>
gh pr create --repo MasterDD-L34D/codemasterdd-ai-station --base main \
  --title "feat(sot-drift): GGv2 frontend drift sentinel extension" \
  --body-file <pr-body-with-QG-evidence-and-harsh-review-triage>
```
Do NOT merge. Eduardo reviews + merges. Label bootstrap (Task 7) + task registration (Task 9 on Lenovo) are the two manual ops noted in the PR body.

---

## Self-Review

**Spec coverage:**
- sez.3 architecture -> Tasks 2-5 (detector) + 8 (governor) + 9 (schedule).
- sez.4 detector -> Tasks 2-5; feat-filter (sez.4 step 3) -> Task 2 `is_feature_pr` + Task 10 edge tests.
- sez.5 watch-map (broad, 9 entries) -> Task 1.
- sez.6 anti-collision (distinct label) -> Task 5 `LABEL` + Task 7 bootstrap + Task 8 governor.
- sez.7 governor +1 source -> Task 8.
- sez.8 schedule (Lenovo daily, S4U/GH_TOKEN) -> Task 9.
- sez.9 verdict subagent UNCHANGED -> no task (correct).
- sez.10 data-flow/error-handling (no-match, gh-fail no-advance, lookback, idempotent) -> Task 5 `detect` (checkpoint advance only `if prs`; dry-run guard) + Task 10 edge tests.
- sez.11 QG 3-step -> Task 6 (smoke) + Task 10 (edge + tuning).
- sez.12 SDMG harsh-review -> Task 11.

**Placeholder scan:** `<uuidv7>` in commit messages = intentional (executor generates a fresh uuidv7 per commit per ADR-0011); `<branch>` / `<pr-body...>` in Task 11 = executor-supplied. No TODO/TBD in code steps.

**Type consistency:** `match_changes` returns `{concept, sot_ref, patterns, files}` -- consumed identically in `build_issue_body` (Task 4) and `detect` (Task 5). `is_feature_pr`, `new_prs_since`, `load_watch_map`, `load_checkpoint`, `save_checkpoint`, `open_or_update_issue`, `detect`, `main` names consistent across tasks + tests. Label `sot-drift-candidate-ggv2` consistent Tasks 5/7/8/9/10. `fetch_merged_prs` uses `--json ...,files`; `detect` reads `pr["files"][i]["path"]` -- matches gh pr list JSON shape.
