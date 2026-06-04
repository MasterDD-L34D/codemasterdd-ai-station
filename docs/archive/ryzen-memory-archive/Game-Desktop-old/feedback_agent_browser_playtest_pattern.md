---
name: Agent + browser MCP playtest pattern (canonical 2026-05-07)
description: Validato 2026-05-07 phone smoke session — agent-driven browser MCP + Cloudflare tunnel sostituisce master-dd manual phone-in-hand per state-machine bugs. Mobile hardware residue solo per WAN RTT / touch p95 / airplane.
type: feedback
originSessionId: a9d68ebc-909a-4239-a3fb-1bf1af777a1a
---
# Agent + browser MCP playtest = NEW DEFAULT (validato 2026-05-07)

## Rule

**Default per playtest co-op multiplayer state-machine bugs**: spawn agent + browser MCP 2-tab simulation via Cloudflare Quick Tunnel. Master-dd hands-on hardware solo per physical-only residue.

**Why**: Sessione 2026-05-07 ha catturato + fixato 3 bug runtime (B6+B7+B8) in ~3h totali end-to-end SENZA master-dd phone hands-on. Pattern legacy "ship + master-dd retest + debug + ship + retest" = 5-10x slower + error-prone (screenshot transcription, unclear state).

## How to apply

### Step 1: Identifica scope bug

| Tipo | Browser-automatable | Physical-only |
|---|:-:|:-:|
| Phase transition / state machine | ✅ | |
| Defer guards / event ordering | ✅ | |
| Broadcast handler / `[unknown_type]` toast | ✅ | |
| Host transfer / room lifecycle | ✅ | |
| WS reconnect logic | ✅ via DevTools offline | |
| Multi-client coordination | ✅ N-tab | |
| Visual regression UI | ✅ screenshot | |
| API surface (REST + WS event) | ✅ curl + JS fetch | |
| Stale build / cache invalidation | ✅ mtime+git log | |
| WAN RTT real LTE | | ✅ |
| Touch latency mobile real fingertip | | ✅ |
| Airplane hardware + mobile WS pause | | ✅ |
| Device perf (memory, thermal throttle) | | ✅ |

### Step 2: Prep tunnel + dist

1. Worktree-isolated branch per fix
2. `FORCE_REBUILD=1 ./tools/web/build_web.sh --mode=phone` (post-PR #206 = default-on)
3. `cp -R dist/web/. <Game-public-phone>/`
4. Launch tunnel via `Evo-Phone-Validation.bat` desktop launcher → Cloudflare ephemeral URL

### Step 3: Browser MCP smoke

```
1. mcp__Claude_in_Chrome__tabs_context_mcp createIfEmpty=true
2. browser_batch [navigate tab1 phone URL, wait 18s splash, screenshot]
3. browser_batch [click Nome field, key 'E','d','d','y' singoli, click Crea, wait, screenshot]
4. tabs_create_mcp (Tab 2 player)
5. browser_batch [navigate tab2 ?room=XXXX deep-link, wait, fill name, click Unisciti, screenshot]
6. browser_batch [click "Inizia mondo (host)", wait 4s, screenshot tab1+tab2]
7. Verify: NO toast `[unknown_type]`, phase advance entrambi tab, host_id preserved via curl /api/lobby/list
```

### Step 4: Forensic via API curl + JS console

- `curl /api/lobby/list` → JSON state canonical (room closed, host_id, state_version)
- `mcp__Claude_in_Chrome__javascript_tool fetch('/api/...')` → bypass Godot HTTPClient se 2nd-tab quirk
- `read_console_messages` con regex pattern → Godot push_warning + browser errors
- `read_network_requests` se serve trace HTTP layer

### Step 5: Lock bug via unit test PRE-fix

Write failing test that reproduces bug at logic layer (composer state, WS handler dispatch, defer guard). Confirm test FAIL pre-fix → fix code → confirm test PASS post-fix → 4-gate DoD locked.

Pattern PR #205 esempio: `test_phone_composer_view_nonhost_transition.gd` 4 test step-by-step (chosen → transition, phase_change → deferred, transition_complete → drains, edge case immediato swap).

### Step 6: Multi-stream parallel fix

Worktree isolation per fix indipendenti:
- Fix code (script) → worktree A
- Prevention infra (deploy script) → worktree B
- RCA doc → worktree C

3 PR parallel, no merge conflict, sessione ricca senza linear bottleneck.

## Why traditional pattern was waste

1. **Master-dd serial bottleneck**: ogni round fix richiede master-dd prendere phone, eseguire 3-item checklist, screenshot, transcribe verdict. ~10min/round × 5-8 round/bug = 50-80min/bug pure manual time
2. **Screenshot ambiguity**: "vedo toast errore" senza type code preciso → ambiguous repro
3. **Single-thread iteration**: bug A ship → master-dd retest → bug B emerge → ship → retest → bug C emerge. Sequential. Agent + browser = parallel multi-bug catch in single session
4. **Hardware-as-gate fallacy**: state-machine bugs don't care about hardware. Real touch latency p95 differs but defer logic is identical mobile vs desktop
5. **Stale state contamination**: master-dd phone retains session/cache between rounds. Tab close + new tab = clean slate every time

## Mobile residue (resta master-dd hands-on)

Solo:
- **Real WAN RTT geographic** (LTE → CF edge → backend, vs localhost → CF edge)
- **Touch p95 mobile** (fingertip + capacitive sensor + iOS Safari render path differs from desktop Chrome cursor)
- **Airplane mode hardware** (mobile browser tab background pause WS = OS-level, no DevTools equivalent)
- **Device thermal/memory throttling** (sustained combat 5R+ on mid-tier phone)

Tutto altro = browser-automatable.

## Anti-pattern code-smell

- ❌ "Ship and master-dd retest" senza unit test repro pre-fix
- ❌ Screenshot upload come primary forensic
- ❌ Phone-in-hand come default validation gate per state machine bug
- ❌ "WAN richiesto per repro" senza tentare browser tunnel + DevTools network throttle
- ❌ Skip browser MCP perché "non è phone reale" — la maggior parte dei bug emerge identico
- ❌ Single-tab Chrome MCP per multiplayer bug (serve 2+ tab per repro)

## Skill candidate (future)

`/agent-playtest <scenario>` — orchestrates:
1. Worktree branch
2. FORCE_REBUILD dist
3. Tunnel up
4. N-tab browser MCP simulation
5. API curl forensic + JS console probe
6. Unit test stub pre-fix se bug emerge
7. Auto-cleanup tunnel post

Drafts via composite illuminator agents (creature-aspect-illuminator, balance-illuminator pattern). Estimate: 2-3h skill creation + smoke test gate.

## Industry patterns adoption roadmap (research 2026-05-07)

Kill-60 ranked, ordine adoption:

| # | Tool | Pattern | Effort | Wins |
|---|---|---|:-:|---|
| 1 | **Playwright multi-context** ([playwright.dev](https://playwright.dev/)) | N isolated browser contexts in single process — replace 2-tab Chrome MCP dance con `tests/e2e/phone-multi.spec.ts` 4-8 phone simultanei | low | Port existing pattern, deterministic CI gate |
| 2 | **Artillery WebSocket** ([thegreenreport.blog](https://www.thegreenreport.blog/articles/websocket-testing-essentials-strategies-and-code-for-real-time-apps/websocket-testing-essentials-strategies-and-code-for-real-time-apps.html)) | Declarative YAML WS scenarios + load test thousands clients | low | Pre-merge gate `lobbyService` host-transfer grace 90s + B5 phase_change broadcast under load |
| 3 | **PlayGodot** ([Randroids-Dojo/PlayGodot](https://github.com/Randroids-Dojo/PlayGodot)) | Playwright-style framework Godot-native via RemoteDebugger protocol | med | Eliminates HTML5 build+serve manual loop |
| 4 | **Wesnoth AI vs AI** ([wiki.wesnoth.org](https://wiki.wesnoth.org/Wesnoth_AI)) | Scripted AI head-to-head N=1000 encounters → CSV win-rate diff vs golden | med | Nightly fairness regression gate (Sprint M9 P6) |
| 5 | **GodotTestDriver** ([chickensoft-games/GodotTestDriver](https://github.com/chickensoft-games/GodotTestDriver)) | In-engine scene drivers (lobby_view, phone_composer_view), additive on GUT | low | Higher-level than GUT unit, lower than HTML5 black-box |
| 6 | **canvas-grid Playwright addon** ([dev.to/fonzi](https://dev.to/fonzi/testing-html5-canvas-with-canvasgrid-and-playwright-5h4c)) | Assert HTML5 canvas regions via grid coordinates | low | G2 echolocation pulse + Sprint G v3 visual regression |
| 7 | **gamestudio-subagents** ([pamirtuna/gamestudio-subagents](https://github.com/pamirtuna/gamestudio-subagents)) | Pre-tuned solo-dev subagent profiles QA/balance/narrative | low | Mine `phone-smoke-bot` template aligned 4-gate DoD |
| 8 | TITAN LLM agent testers ([arxiv 2509.22170](https://arxiv.org/html/2509.22170v1)) | LLM agents play game like humans + adapt UI changes | high | SKIP solo-dev — overkill, mine ideas only |

**Recommended adoption next sprint** (~6-8h totale):
- Playwright multi-context (~3h) — port 2-tab smoke as CI gate
- Artillery WS scenario (~2h) — pre-merge `LOBBY_WS_SHARED` flow
- canvas-grid hook (~1h) — visual regression Skiv echolocation pulse
- gamestudio-subagents review (~1h) — borrow QA bot template

**Sprint M9+ gating opt-in**: PlayGodot full integration + Wesnoth AI vs AI nightly. Effort med, ship dopo Phase A cutover Godot.

**SKIP indefinitely**: TITAN academic, Riot Vanguard enterprise infrastructure.

## Cross-ref

- `project_phone_smoke_2026_05_07_b8_fix.md` — sessione canonical
- `feedback_no_manual_test_when_automatable.md` — Master-dd 2026-05-06 esplicit user directive
- `feedback_smoke_test_agents_before_ready.md` — agent smoke gate policy
- Game/ `docs/playtest/2026-05-07-phone-smoke-bundle-rca.md` — forensic + lessons codified

## When to apply

✅ Multiplayer state machine bug (lobby, phases, broadcast events)
✅ Pre-merge regression check (ship a worktree, run smoke before commit)
✅ Cross-PR interaction bug (3 PR shipped consecutivi, regression possibile)
✅ "Engine LIVE Surface DEAD" check (Gate 5) — verify player VEDE feature in 60s gameplay simulato

❌ Pure backend logic (rules engine, vc scoring) — Node tests bastano
❌ Visual polish (sprite alignment, animation timing) — pixel-perfect impossibile via browser headless
❌ Audio (SFX trigger timing, mix) — agent non sente audio
❌ Pure user-feel (game balance, fun factor) — richiede umano, ma agent può scout per outliers
