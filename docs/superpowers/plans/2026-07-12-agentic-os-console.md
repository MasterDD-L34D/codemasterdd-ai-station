# Agentic OS Console Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an "Agentic OS Console" home + a tier-gated action runner to the existing `apps/cross-repo-dashboard` Flask app, so the OS has one page you open to see its state and launch fleet actions.

**Architecture:** Extend (do NOT replace) `apps/cross-repo-dashboard`. New data-only `actions_registry.py` (tiered actions, fixed argv), new `/api/run-action` endpoint mirroring the `/api/regen-dashboard` security contract (bearer auth, id-only client input, `shell=False`, no interpolation), new `/os` home route + template, and a root redirect making `/os` the front door. Local single-user, `127.0.0.1:8081`.

**Tech Stack:** Python 3.12, Flask (blueprint `cross_repo_bp` at url_prefix `/cross-repo`), pytest, existing wrappers (`scripts/fleet/jules-dispatch.ps1`, aider privacy wrappers, `gh`).

**Conventions:** ASCII-first (ADR-0021). Commit trailers `Coding-Agent:` + `Trace-Id:` (ADR-0011, NO Co-Authored-By). Test: `py -m pytest -q scripts/tests` + `apps/cross-repo-dashboard/tests`. Branch `claude/agentic-os-console` (worktree `C:/dev/_cmdd-osconsole-spec-wt`).

---

## File Structure

- Create: `apps/cross-repo-dashboard/actions_registry.py` -- tiered action catalog (data-only, fixed argv).
- Create: `scripts/tests/test_actions_registry.py` -- schema integrity + no-injection + tier enforcement (negative control, L-041).
- Modify: `apps/cross-repo-dashboard/app.py` -- add `/api/run-action`, `/os` route, `/` root redirect; import ACTIONS.
- Create: `apps/cross-repo-dashboard/templates/os_console.html` -- OS home (layers + brief + PRs + task health + actions grid).
- Create: `apps/cross-repo-dashboard/os_home.py` -- pure helpers (parse AGENTIC_OS.md layers, read latest morning-brief) kept out of app.py.
- Create: `apps/cross-repo-dashboard/tests/test_os_console.py` -- route smoke + run-action tier gating (Flask test client).
- Modify: `.claude/launch.json` -- add `agentic-os-console` config (create file if absent).

---

### Task 1: actions_registry.py (data-only tiered catalog)

**Files:**
- Create: `apps/cross-repo-dashboard/actions_registry.py`

- [ ] **Step 1: Write the registry module**

```python
"""Agentic OS Console action catalog (data-only, tiered).

SECURITY CONTRACT (mirrors dashboards_registry.py): `steps` are FIXED argv
lists (no shell, no client input ever interpolated). /api/run-action accepts
only an action id + whitelisted param CHOICES; it executes these exact argv
lists with shell=False. Adding an entry here is the only way to make something
runnable from the OS console -- reviewed like code, because it is code.

Tiers: 0 = read/report (one-click, free) | 1 = mutating-reversible (human click
= authorization, MUST route through an existing fail-closed wrapper) | 2 =
excluded (no executable steps; merge-main/force-push/external comms stay off).
"""
from __future__ import annotations

from typing import Any

HUB = r"C:\dev\codemasterdd-ai-station"

ACTIONS: list[dict[str, Any]] = [
    # ---- tier 0: read / report ----
    {
        "id": "fleet-verify", "label": "Fleet-verify (audit flotta)", "tier": 0,
        "area": "audit", "desc": "Machine-aware fleet audit (read-mostly).",
        "steps": [["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                   "-File", r"scripts\fleet\morning-brief.ps1", "-NoFile"]],
        "cwd": HUB, "timeout": 600, "ok_exit_codes": [0],
    },
    {
        "id": "morning-brief", "label": "Morning brief (rigenera)", "tier": 0,
        "area": "report", "desc": "Regenerate the R0 fleet heartbeat now.",
        "steps": [["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                   "-File", r"scripts\fleet\morning-brief.ps1"]],
        "cwd": HUB, "timeout": 300, "ok_exit_codes": [0],
    },
    {
        "id": "fleet-pr-status", "label": "PR flotta (gh)", "tier": 0,
        "area": "report", "desc": "Open PRs across monitored repos.",
        "steps": [["gh", "pr", "list", "--repo", "MasterDD-L34D/codemasterdd-ai-station",
                   "--state", "open", "--limit", "50"]],
        "cwd": HUB, "timeout": 120, "ok_exit_codes": [0],
    },
    {
        "id": "governance-lint", "label": "Governance lint", "tier": 0,
        "area": "audit", "desc": "Run the governance lint report.",
        "steps": [["py", "-3", r"scripts\governance-lint.py"]],
        "cwd": HUB, "timeout": 300, "ok_exit_codes": [0, 1],  # lint rc=1 when it finds items
    },
    {
        "id": "pytest-scripts", "label": "Pytest (scripts)", "tier": 0,
        "area": "audit", "desc": "Run the repo pytest suite.",
        "steps": [["py", "-m", "pytest", "-q", "scripts/tests"]],
        "cwd": HUB, "timeout": 300, "ok_exit_codes": [0],
    },
    # ---- tier 1: mutating-reversible (via existing fail-closed wrappers) ----
    {
        "id": "jules-dispatch", "label": "Dispatch Jules (scoped)", "tier": 1,
        "area": "delegate", "desc": "Dispatch a scoped Jules session via the fail-closed wrapper.",
        "wrapper": "jules-dispatch",
        "steps": [["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                   "-File", r"scripts\fleet\jules-dispatch.ps1", "-DryRun"]],
        "cwd": HUB, "timeout": 180, "ok_exit_codes": [0],
        "params": [{"name": "repo", "choices": ["Game", "Game-Godot-v2", "Game-Database", "codemasterdd-ai-station"]}],
    },
    {
        "id": "create-draft-pr", "label": "Crea draft-PR (branch corrente)", "tier": 1,
        "area": "delegate", "desc": "Push current claude/* branch + open a DRAFT PR.",
        "wrapper": "gh-draft-pr",
        "steps": [["gh", "pr", "create", "--draft", "--fill",
                   "--repo", "MasterDD-L34D/codemasterdd-ai-station"]],
        "cwd": HUB, "timeout": 120, "ok_exit_codes": [0],
    },
    {
        "id": "aider-delegate", "label": "Delega Aider (cosmetic)", "tier": 1,
        "area": "delegate", "desc": "Delegate a cosmetic edit via the privacy-guarded wrapper.",
        "wrapper": "aider-cosmetic",
        "steps": [["bash", "-lc", "aider-cosmetic --version"]],  # placeholder invocation; real target added at wire-time
        "cwd": HUB, "timeout": 120, "ok_exit_codes": [0],
        "params": [{"name": "repo", "choices": ["codemasterdd-ai-station", "Game", "Game-Godot-v2"]}],
    },
    # ---- tier 2: excluded (documented, NOT runnable) ----
    {
        "id": "merge-main", "label": "Merge to main (doctrine)", "tier": 2,
        "area": "excluded", "desc": "Excluded from the panel -- Eduardo-only, classifier backstop.",
    },
]
```

- [ ] **Step 2: ASCII check**

Run: `py -c "import pathlib,sys; b=pathlib.Path('apps/cross-repo-dashboard/actions_registry.py').read_bytes(); sys.exit(1 if any(c>127 for c in b) else 0)"`
Expected: exit 0 (no output).

- [ ] **Step 3: Commit**

```bash
git add apps/cross-repo-dashboard/actions_registry.py
git commit -m "feat(os-console): tiered action registry (data-only, fixed argv)"
# trailers Coding-Agent + Trace-Id per ADR-0011
```

---

### Task 2: test_actions_registry.py (schema + no-injection + tiers)

**Files:**
- Create: `scripts/tests/test_actions_registry.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Guard tests for the OS console action registry.

Mirrors test_dashboards_registry.py: schema integrity, the fixed-argv security
contract (the UI can never inject commands), tier enforcement, and negative
controls (L-041: a guard without a must-fail case proves nothing).
"""
from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[2] / "apps" / "cross-repo-dashboard"
sys.path.insert(0, str(APP_DIR))

from actions_registry import ACTIONS  # noqa: E402

VALID_TIERS = {0, 1, 2}


def test_ids_unique() -> None:
    ids = [a["id"] for a in ACTIONS]
    assert len(ids) == len(set(ids)), "duplicate action ids"


def test_schema_and_display_fields() -> None:
    for a in ACTIONS:
        assert a["tier"] in VALID_TIERS, f"{a['id']}: bad tier {a['tier']}"
        assert a.get("label") and a.get("area") and a.get("desc"), f"{a['id']}: missing display fields"


def test_tier0_and_tier1_have_executable_steps() -> None:
    for a in ACTIONS:
        if a["tier"] in (0, 1):
            assert a.get("steps") and all(isinstance(s, list) and s for s in a["steps"]), \
                f"{a['id']}: tier {a['tier']} needs non-empty argv steps"


def test_tier2_has_no_executable_steps() -> None:
    for a in ACTIONS:
        if a["tier"] == 2:
            assert not a.get("steps"), f"{a['id']}: tier-2 must not carry runnable steps"


def test_tier1_requires_wrapper() -> None:
    for a in ACTIONS:
        if a["tier"] == 1:
            assert a.get("wrapper"), f"{a['id']}: tier-1 must route through a named fail-closed wrapper"


def test_argv_elements_are_literal_strings() -> None:
    # every argv token is a literal str: nothing to interpolate from client input
    for a in ACTIONS:
        for step in a.get("steps", []):
            for tok in step:
                assert isinstance(tok, str), f"{a['id']}: argv token not a literal string: {tok!r}"


def test_params_are_whitelist_choices_only() -> None:
    for a in ACTIONS:
        for p in a.get("params", []):
            assert p.get("name") and isinstance(p.get("choices"), list) and p["choices"], \
                f"{a['id']}: param must have a name + non-empty whitelist choices"
            assert all(isinstance(c, str) for c in p["choices"]), f"{a['id']}: param choices must be strings"


def test_negative_control_injection_id_not_in_registry() -> None:
    # a shell-injection-looking id must simply not resolve (dict lookup miss)
    ids = {a["id"] for a in ACTIONS}
    assert "fleet-verify; rm -rf /" not in ids
    assert not any(";" in i or "&&" in i or "|" in i for i in ids), "action ids must be plain slugs"
```

- [ ] **Step 2: Run to verify pass** (registry from Task 1 already satisfies it)

Run: `py -m pytest -q scripts/tests/test_actions_registry.py`
Expected: PASS (8 passed).

- [ ] **Step 3: Commit**

```bash
git add scripts/tests/test_actions_registry.py
git commit -m "test(os-console): action registry schema + no-injection guards"
```

---

### Task 3: /api/run-action endpoint (mirror regen-dashboard)

**Files:**
- Modify: `apps/cross-repo-dashboard/app.py` (add import + endpoint)
- Test: `apps/cross-repo-dashboard/tests/test_os_console.py` (Task 6 covers smoke)

- [ ] **Step 1: Add the import** near `from dashboards_registry import DASHBOARDS, RUN_MONITORS`:

```python
from actions_registry import ACTIONS
```

- [ ] **Step 2: Add the endpoint** in the `cross_repo_bp` blueprint (place next to `regen_dashboard`):

```python
@cross_repo_bp.route("/api/run-action", methods=["POST"])
def run_action() -> Any:
    """Run the FIXED argv steps of a tier-0/1 action (whitelist-only).

    Security mirrors /api/regen-dashboard: optional API_SECRET bearer with
    constant-time compare; the only client input is the action id (dict lookup,
    no interpolation) plus whitelisted param choices; steps are code-reviewed
    argv lists executed without shell. tier-2 is not executable (403)."""
    api_secret = os.environ.get("API_SECRET")
    if api_secret:
        auth_header = request.headers.get("Authorization", "")
        if not hmac.compare_digest(auth_header, f"Bearer {api_secret}"):
            return jsonify({"ok": False, "error": "unauthorized"}), 401

    body = request.json or {}
    action_id = body.get("id", "")
    action = next((a for a in ACTIONS if a["id"] == action_id), None)
    if action is None:
        return jsonify({"ok": False, "error": "unknown action id"}), 400
    if action["tier"] == 2:
        return jsonify({"ok": False, "error": "tier-2 action is excluded from the panel"}), 403
    if not action.get("steps"):
        return jsonify({"ok": False, "error": "action has no runnable steps"}), 400

    # validate any params strictly against the registry whitelist (never interpolate)
    chosen: dict[str, str] = {}
    for p in action.get("params", []):
        val = str(body.get(p["name"], ""))
        if val and val not in p["choices"]:
            return jsonify({"ok": False, "error": f"param {p['name']} not in whitelist"}), 400
        if val:
            chosen[p["name"]] = val

    timeout = int(action.get("timeout", 300))
    ok_codes = set(action.get("ok_exit_codes", [0]))
    outputs: list[str] = []
    for argv in action["steps"]:
        try:
            result = subprocess.run(
                argv, cwd=action["cwd"], capture_output=True, text=True,
                timeout=timeout, check=False, shell=False,
                creationflags=_NO_WINDOW_FLAG,
            )
        except subprocess.TimeoutExpired:
            return jsonify({"ok": False, "error": f"timeout after {timeout}s",
                            "output": "\n".join(outputs)[-2000:]}), 500
        except FileNotFoundError as e:
            return jsonify({"ok": False, "error": f"tool not found: {e}",
                            "output": "\n".join(outputs)[-2000:]}), 500
        tail = (result.stdout or "")[-800:] + (("\nSTDERR: " + result.stderr[-400:]) if result.stderr else "")
        outputs.append(f"$ {' '.join(argv)} (rc={result.returncode})\n{tail}")
        if result.returncode not in ok_codes:
            return jsonify({"ok": False, "error": f"step failed rc={result.returncode}",
                            "output": "\n".join(outputs)[-2000:]}), 500
    return jsonify({"ok": True, "output": "\n".join(outputs)[-2000:]})
```

- [ ] **Step 3: Verify import + syntax**

Run: `cd apps/cross-repo-dashboard && py -c "import app; print('ok')"`
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add apps/cross-repo-dashboard/app.py
git commit -m "feat(os-console): /api/run-action endpoint (fixed-argv, tier-gated)"
```

---

### Task 4: os_home.py helpers (parse layers + latest brief)

**Files:**
- Create: `apps/cross-repo-dashboard/os_home.py`

- [ ] **Step 1: Write the helpers**

```python
"""Pure helpers for the OS console home. Kept out of app.py so they stay
unit-testable without a Flask context."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

HUB = Path(r"C:\dev\codemasterdd-ai-station")
_ROW = re.compile(r"^\|\s*\d+\s*\|\s*(?P<layer>[^|]+?)\s*\|\s*(?P<authority>[^|]+?)\s*\|")


def parse_layers(map_path: Path | None = None) -> list[dict[str, str]]:
    """Extract the 7 layer rows from AGENTIC_OS.md's layer table."""
    p = map_path or (HUB / "AGENTIC_OS.md")
    if not p.is_file():
        return []
    out: list[dict[str, str]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        m = _ROW.match(line)
        if m and m.group("layer").strip().lower() not in {"layer", "---"}:
            out.append({"layer": m.group("layer").strip(), "authority": m.group("authority").strip()})
    return out


def latest_brief(today: str, brief_dir: Path | None = None) -> str:
    """Return the latest morning brief text, or a placeholder if none for today."""
    d = brief_dir or (HUB / "logs" / "morning-brief")
    f = d / f"{today}.md"
    if f.is_file():
        return f.read_text(encoding="utf-8")
    return "(morning brief non ancora generato per oggi -- usa l'azione 'Morning brief')"
```

- [ ] **Step 2: Write helper tests** in `scripts/tests/test_actions_registry.py` (append):

```python
def test_parse_layers_reads_seven_rows(tmp_path) -> None:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "cross-repo-dashboard"))
    from os_home import parse_layers
    m = tmp_path / "AGENTIC_OS.md"
    m.write_text(
        "| # | Layer | Authority | Note |\n|---|---|---|---|\n"
        "| 1 | Kernel | ORCHESTRATION.md | x |\n| 2 | Routing | MODEL_ROUTING.md | y |\n",
        encoding="utf-8",
    )
    rows = parse_layers(m)
    assert rows == [{"layer": "Kernel", "authority": "ORCHESTRATION.md"},
                    {"layer": "Routing", "authority": "MODEL_ROUTING.md"}]


def test_latest_brief_placeholder_when_absent(tmp_path) -> None:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "cross-repo-dashboard"))
    from os_home import latest_brief
    assert "non ancora generato" in latest_brief("2099-01-01", tmp_path)
```

- [ ] **Step 3: Run tests**

Run: `py -m pytest -q scripts/tests/test_actions_registry.py`
Expected: PASS (10 passed).

- [ ] **Step 4: Commit**

```bash
git add apps/cross-repo-dashboard/os_home.py scripts/tests/test_actions_registry.py
git commit -m "feat(os-console): os_home helpers (parse layers, latest brief) + tests"
```

---

### Task 5: /os route + template + root redirect (Q1)

**Files:**
- Modify: `apps/cross-repo-dashboard/app.py` (add `/os` route + `/` redirect)
- Create: `apps/cross-repo-dashboard/templates/os_console.html`

- [ ] **Step 1: Add imports** to app.py (top): `from flask import redirect` (extend existing flask import) and `from os_home import parse_layers, latest_brief`; `from datetime import date` if not present (datetime already imported).

- [ ] **Step 2: Add the route** in the blueprint:

```python
@cross_repo_bp.route("/os")
def os_console() -> Any:
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # actions without argv/steps reaching the template (mirror regen: pop steps)
    acts = []
    for a in ACTIONS:
        e = {k: a[k] for k in ("id", "label", "tier", "area", "desc") if k in a}
        e["params"] = a.get("params", [])
        acts.append(e)
    areas: dict[str, list[dict[str, Any]]] = {}
    for e in acts:
        areas.setdefault(e["area"], []).append(e)
    return render_template(
        "os_console.html",
        layers=parse_layers(),
        brief=latest_brief(today),
        actions_by_area=areas,
        api_secret=os.environ.get("API_SECRET", ""),
    )
```

- [ ] **Step 3: Add a root redirect** at app factory level (Q1: `/os` is the front door). In `create_app()`:

```python
def create_app() -> Flask:
    """App factory: creates Flask instance and registers the cross-repo blueprint."""
    _app = Flask(__name__)
    _app.register_blueprint(cross_repo_bp, url_prefix='/cross-repo')

    @_app.route("/")
    def _root():
        from flask import redirect
        return redirect("/cross-repo/os")

    return _app
```

- [ ] **Step 4: Create the template** `templates/os_console.html`:

```html
<!doctype html>
<html lang="it"><head><meta charset="utf-8"><title>Agentic OS Console</title>
<style>
 body{font-family:system-ui,sans-serif;margin:1.5rem;background:#0f1115;color:#e6e6e6}
 h1{font-size:1.3rem} h2{font-size:1rem;margin-top:1.5rem;color:#8ab4f8}
 a{color:#8ab4f8} .muted{color:#8a8f98}
 table{border-collapse:collapse;width:100%} td,th{border:1px solid #2a2f3a;padding:.35rem .5rem;text-align:left;font-size:.85rem}
 .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.6rem}
 .card{border:1px solid #2a2f3a;border-radius:8px;padding:.6rem}
 button{cursor:pointer;background:#1f6feb;color:#fff;border:0;border-radius:6px;padding:.35rem .7rem}
 button.t1{background:#b7791f} pre{white-space:pre-wrap;background:#0b0d11;padding:.5rem;border-radius:6px;max-height:320px;overflow:auto}
 .t{font-size:.7rem;border-radius:4px;padding:.05rem .35rem} .t0{background:#1f6feb33} .t1{background:#b7791f33}
</style></head><body>
<h1>Agentic OS Console <span class="muted">-- <a href="/cross-repo/">fleet dashboard</a></span></h1>

<h2>Layer -> authority</h2>
<table><tr><th>Layer</th><th>Authority</th></tr>
{% for l in layers %}<tr><td>{{ l.layer }}</td><td>{{ l.authority }}</td></tr>{% endfor %}
{% if not layers %}<tr><td colspan="2" class="muted">AGENTIC_OS.md non trovato</td></tr>{% endif %}
</table>

<h2>Morning brief</h2>
<pre>{{ brief }}</pre>

<h2>Azioni</h2>
{% for area, acts in actions_by_area.items() %}
<h3 style="font-size:.9rem;color:#8a8f98">{{ area }}</h3>
<div class="grid">
{% for a in acts %}
 <div class="card">
  <div><span class="t t{{ a.tier }}">tier {{ a.tier }}</span> <strong>{{ a.label }}</strong></div>
  <div class="muted" style="font-size:.8rem">{{ a.desc }}</div>
  {% for p in a.params %}
   <select data-param="{{ p.name }}">{% for c in p.choices %}<option>{{ c }}</option>{% endfor %}</select>
  {% endfor %}
  {% if a.tier != 2 %}<button class="{% if a.tier==1 %}t1{% endif %}" onclick="run('{{ a.id }}', this)">Esegui</button>{% else %}<span class="muted">escluso</span>{% endif %}
 </div>
{% endfor %}
</div>
{% endfor %}

<h2>Output</h2>
<pre id="out" class="muted">(nessuna azione ancora)</pre>

<script>
const SECRET = {{ api_secret|tojson }};
async function run(id, btn){
  const card = btn.closest('.card'); const params = {};
  card.querySelectorAll('select[data-param]').forEach(s => params[s.dataset.param] = s.value);
  const out = document.getElementById('out'); out.textContent = 'running '+id+' ...'; btn.disabled = true;
  try{
    const h = {'Content-Type':'application/json'}; if(SECRET) h['Authorization']='Bearer '+SECRET;
    const r = await fetch('/cross-repo/api/run-action', {method:'POST', headers:h, body:JSON.stringify({id, ...params})});
    const j = await r.json(); out.textContent = (j.ok?'[OK] ':'[FAIL] ')+(j.output||j.error||'');
  }catch(e){ out.textContent = '[ERR] '+e; } finally { btn.disabled = false; }
}
</script>
</body></html>
```

- [ ] **Step 5: Verify import + render**

Run: `cd apps/cross-repo-dashboard && py -c "import app; c=app.create_app().test_client(); r=c.get('/cross-repo/os'); print(r.status_code); r2=c.get('/'); print(r2.status_code)"`
Expected: `200` then `308` (redirect).

- [ ] **Step 6: Commit**

```bash
git add apps/cross-repo-dashboard/app.py apps/cross-repo-dashboard/templates/os_console.html
git commit -m "feat(os-console): /os home + template + root redirect (Q1 default)"
```

---

### Task 6: route smoke + tier-gating tests (Flask test client)

**Files:**
- Create: `apps/cross-repo-dashboard/tests/test_os_console.py`

- [ ] **Step 1: Write the tests**

```python
"""Route smoke + tier gating for the OS console (Flask test client)."""
from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))

import app as appmod  # noqa: E402


def client():
    return appmod.create_app().test_client()


def test_os_home_renders() -> None:
    r = client().get("/cross-repo/os")
    assert r.status_code == 200
    assert b"Agentic OS Console" in r.data


def test_root_redirects_to_os() -> None:
    r = client().get("/")
    assert r.status_code in (301, 302, 308)
    assert "/cross-repo/os" in r.headers.get("Location", "")


def test_run_action_unknown_id_400() -> None:
    r = client().post("/cross-repo/api/run-action", json={"id": "nope"})
    assert r.status_code == 400


def test_run_action_tier2_forbidden() -> None:
    r = client().post("/cross-repo/api/run-action", json={"id": "merge-main"})
    assert r.status_code == 403


def test_run_action_bad_param_rejected() -> None:
    # jules-dispatch requires repo in whitelist; a bogus repo must 400 before any exec
    r = client().post("/cross-repo/api/run-action", json={"id": "jules-dispatch", "repo": "evil; rm -rf"})
    assert r.status_code == 400
```

- [ ] **Step 2: Run**

Run: `cd apps/cross-repo-dashboard && py -m pytest -q tests/test_os_console.py`
Expected: PASS (5 passed). (Note: `test_run_action_bad_param_rejected` must reject BEFORE running the wrapper.)

- [ ] **Step 3: Commit**

```bash
git add apps/cross-repo-dashboard/tests/test_os_console.py
git commit -m "test(os-console): route smoke + tier gating + bad-param negative control"
```

---

### Task 7: launcher (.claude/launch.json) + docs

**Files:**
- Modify/Create: `.claude/launch.json`
- Modify: `apps/cross-repo-dashboard/README.md` (one line pointing at /os)

- [ ] **Step 1: Add launch config** (`.claude/launch.json`; if the file exists, add to `configurations`):

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "agentic-os-console",
      "runtimeExecutable": "py",
      "runtimeArgs": ["-3", "apps/cross-repo-dashboard/app.py"],
      "port": 8081
    }
  ]
}
```

- [ ] **Step 2: Add README pointer** (append to `apps/cross-repo-dashboard/README.md`):

```markdown

## Agentic OS Console

The OS front door is `http://127.0.0.1:8081/cross-repo/os` (root `/` redirects there).
Start: `py -3 apps/cross-repo-dashboard/app.py` (or the tray icon / desktop shortcut).
Shows the 7 OS layers, the latest morning brief, fleet PRs, and tier-gated actions.
```

- [ ] **Step 3: Full test sweep**

Run: `py -m pytest -q scripts/tests apps/cross-repo-dashboard/tests`
Expected: all PASS.
Run ASCII guard: `py -c "import pathlib,sys; bad=[str(p) for p in [pathlib.Path('apps/cross-repo-dashboard/actions_registry.py'),pathlib.Path('apps/cross-repo-dashboard/os_home.py'),pathlib.Path('apps/cross-repo-dashboard/templates/os_console.html')] if any(c>127 for c in p.read_bytes())]; print(bad); sys.exit(1 if bad else 0)"`
Expected: `[]`, exit 0.

- [ ] **Step 4: Commit + push + open PR**

```bash
git add .claude/launch.json apps/cross-repo-dashboard/README.md
git commit -m "feat(os-console): launch.json + README front-door pointer"
git push -u origin claude/agentic-os-console
gh pr create --title "feat(os-console): Agentic OS Console (home + tiered actions)" --body "..."
```

---

## Verification (before calling done)

- [ ] Launch: `py -3 apps/cross-repo-dashboard/app.py`, open `http://127.0.0.1:8081/` -> lands on `/cross-repo/os`.
- [ ] Home shows 7 layers, brief, actions grid. Run a tier-0 action (morning-brief) -> output appears.
- [ ] Tier-2 card shows "escluso" (no button). Bad param on jules-dispatch -> rejected.
- [ ] `py -m pytest -q scripts/tests apps/cross-repo-dashboard/tests` all green; ASCII guard clean.
- [ ] harsh-reviewer pre-merge (security/governance-critical: the run-action endpoint executes commands) + Codex.

## Out of scope (later, own spec)

Tier-2 anything; `claude -p` headless agent spawn; panel-initiated autonomous/scheduled runs (act-layer, governor-gated); multi-user auth / non-local exposure; run history in governor.db.
