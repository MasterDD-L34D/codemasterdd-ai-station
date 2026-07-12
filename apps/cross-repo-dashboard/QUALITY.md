# QUALITY -- Agentic OS Console (feature)

Quality Gate evidence for the "Agentic OS Console" feature added to
`apps/cross-repo-dashboard` (home `/os` + `/api/run-action` + tiered
`actions_registry.py` + guarded `scripts/fleet/draft-pr.ps1`).
Scope shipped: MVP Option A (5 tier-0 + 1 tier-1). See
`docs/superpowers/specs/2026-07-12-agentic-os-console-design.md`.

Date: 2026-07-13. Machine: CODEMASTERDD (Lenovo). Agent: claude-fable-5.

## Step 1 -- Smoke (happy path green, verifiable output)

Test sweep (launcher `py`, ADR: `--import-mode=importlib`):

    py -m pytest -q scripts/tests apps/cross-repo-dashboard/tests
    -> 292 passed in ~3s

Includes a NEW hermetic happy-path (`test_run_action_happy_path_hermetic`):
injects a trivial tier-0 action with a fixed argv (`[sys.executable, "-c",
"print('ok')"]`) and asserts `/api/run-action` returns `ok:True` + output "ok".
This exercises the real exec path, not just the 4xx guards.

Plus a positive control for the P1 fix
(`test_run_action_applies_whitelisted_param_to_argv`): a valid `repo` choice
must appear in the EXECUTED argv (flag + value). Verified L-041-style that it
bites -- disabling the `steps[-1].extend(extra_args)` apply makes this test fail
(argv tail becomes `[]`), while the rest of the suite stays green.

Live server (`py -3 apps/cross-repo-dashboard/app.py`, 127.0.0.1:8081), verified
by curl:

- `GET /`               -> 302 -> `http://127.0.0.1:8081/cross-repo/os` (front door)
- `GET /cross-repo/os`  -> 200, renders "Agentic OS Console" + the working
  `repo` dropdown (4 slugs).
- `POST /api/run-action {"id":"fleet-pr-status","repo":"MasterDD-L34D/Game"}`
  -> `{"ok":true,"output":"$ gh pr list --state open --limit 50 --repo MasterDD-L34D/Game (rc=0)\n"}`

The last line is the load-bearing proof that the param is APPLIED to argv
server-side (chosen whitelist value appended as `--repo <slug>`), fixing the
"dead dropdown" P1.

## Step 2 -- Research (edge cases + unexpected behaviors)

Negative controls, verified live against the running server:

1. Param off-whitelist: `{"id":"fleet-pr-status","repo":"evil; rm -rf"}`
   -> 400, rejected BEFORE any subprocess (value never reaches argv).
2. tier-1 with no server `API_SECRET`: `{"id":"create-draft-pr"}`
   -> 403 `"tier-1 action requires API_SECRET to be set on the server"`
   (mutating action fails closed even though tier-0 stays open).
3. tier-2 excluded: `{"id":"merge-main"}` -> 403 (no runnable steps).
4. Injection-looking id: `{"id":"nope; rm -rf /"}` -> 400 (dict lookup miss;
   the id is never a command, so shell metachars are inert).
5. Wrapper guard (`scripts/fleet/draft-pr.ps1`): aborts with exit 3 if HEAD is
   not a `claude/*` branch, exit 4 if the branch is not pushed to origin; only
   then `gh pr create --draft` with `--head` pinned to the resolved branch. The
   registry test asserts `wrapper_path` RESOLVES to a real file (a dangling
   label can no longer masquerade as gated).

Unexpected behaviors flagged (and handled):

- CI (`.github/workflows/ci.yml`) `pytest` job runs ONLY `scripts/tests` with a
  pytest-only env (no Flask/requests). So the registry tests are kept
  stdlib-only, and the Flask app tests (incl. the happy-path) run locally only.
  The happy-path uses `sys.executable` (portable) rather than `cmd /c echo` so
  it is not Windows-locked if the app suite is ever added to CI.
- `fleet-pr-status` dropdown auto-selects its first option
  (codemasterdd-ai-station), so a click with no explicit choice preserves the
  prior hardcoded behavior (hub PRs).

## Step 3 -- Tuning (iteration + before/after delta)

One review-driven iteration: harsh-review found the tier-1 wiring half-baked
(dead dropdowns, bare `gh`, optional auth). Delta from 251b262 -> shipped:

| metric                        | before (251b262)                          | after                                             |
|-------------------------------|-------------------------------------------|---------------------------------------------------|
| params applied to argv        | 0 (validated, never applied)              | yes (flag+choice appended; proven live)           |
| dead dropdowns                | 2 (jules repo, aider repo)                | 0                                                 |
| tier-1 actions                | 3 (2 non-functional: jules exit-2,        | 1 (create-draft-pr, functional via wrapper)       |
|                               | aider `--version` no-op)                  |                                                   |
| create-draft-pr safety        | bare `gh` (label-only "wrapper")          | real branch-guarded wrapper (claude/* + pushed,   |
|                               |                                           | `--head` pinned)                                  |
| tier-1 auth when no secret    | ran unauthenticated                       | 403 fail-closed                                   |
| tests                         | 288                                       | 291 (+happy-path exec, +tier1-auth, +single-step; |
|                               |                                           | wrapper test strengthened to resolve-to-file)     |

Security core was already solid pre-iteration (fixed argv, shell=False, bearer
hmac, id-only client input, tier-2 -> 403) and was preserved -- no security test
was weakened to make anything pass.
