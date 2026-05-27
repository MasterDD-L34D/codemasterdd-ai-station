---
name: Phone smoke session 2026-05-07 B8 fix + functional bundle verify
description: Browser-headless 2-tab smoke retry post-#2087 harness. Bundle B6+B7+B8 RCA. PR #205 B8 fix shipped + verified runtime. Tunnel-as-service pattern lessons.
type: project
originSessionId: a9d68ebc-909a-4239-a3fb-1bf1af777a1a
---
# Phone smoke 2026-05-07 — B8 non-host transition stuck fix shipped

## Outcome

17 PR sessione (TUTTE MERGED ✅):

| Repo | PR | Squash | Topic |
|---|---|---|---|
| Game/ | [#2087](https://github.com/MasterDD-L34D/Game/pull/2087) | a1a88d7b | Phone smoke harness 17 test (Node 11 + GUT 6) |
| Godot v2 | [#202](https://github.com/MasterDD-L34D/Game-Godot-v2/pull/202) | 682a405 | Combat 5R p95 GUT integration harness |
| Godot v2 | [#203](https://github.com/MasterDD-L34D/Game-Godot-v2/pull/203) | 5d098e7 | P4 surface GAP-2 + GAP-9 wire |
| Godot v2 | [#205](https://github.com/MasterDD-L34D/Game-Godot-v2/pull/205) | d48efe1 | **B8 non-host transition stuck fix** |
| Godot v2 | [#206](https://github.com/MasterDD-L34D/Game-Godot-v2/pull/206) | 00e11c4 | **deploy-quick rebuild default invert (B6/B7 prevention)** |
| Game/ | [#2091](https://github.com/MasterDD-L34D/Game/pull/2091) | 77644e8 | **RCA doc B6+B7+B8 forensic** |
| Game/ | [#2092](https://github.com/MasterDD-L34D/Game/pull/2092) | b3667b2 | **Canonical agent-driven playtest workflow doc** |
| Game/ | [#2093](https://github.com/MasterDD-L34D/Game/pull/2093) | 4662e1c | **Playwright phone multi-context smoke (Tier 1 #1)** |
| Game/ | [#2094](https://github.com/MasterDD-L34D/Game/pull/2094) | 31b198f | **Artillery WS load smoke (Tier 1 #2)** |
| Game/ | [#2095](https://github.com/MasterDD-L34D/Game/pull/2095) | 0a6105b | **canvas-grid visual regression (Tier 1 #3)** |
| Game/ | [#2096](https://github.com/MasterDD-L34D/Game/pull/2096) | 1965b46 | **phone-smoke-bot native agent (Tier 1 #4)** |
| Game/ | [#2097](https://github.com/MasterDD-L34D/Game/pull/2097) | 6d41ebc | **Playwright WS multi-tab phase-flow (B5-B10 functional gate)** |
| Game/ | [#2098](https://github.com/MasterDD-L34D/Game/pull/2098) | 8a0ec55 | **combat → debrief → ended e2e (closes Tier 1 coverage gap)** |
| Game/ | [#2088](https://github.com/MasterDD-L34D/Game/pull/2088) | **7247656** | ✅ **ADR-2026-05-05 ACCEPTED Phase A 2026-05-07** |
| Game/ | [#2099](https://github.com/MasterDD-L34D/Game/pull/2099) | 196f606 | **Iter3 hardware-equivalent agent + browser smoke (3 items)** |
| Game/ | [#2100](https://github.com/MasterDD-L34D/Game/pull/2100) | 3935074 | **Phase A LIVE doc actions + handoff next session** |

## Bundle RCA (3 bug runtime emerged + fixed)

| Bug | Symptom | Root cause | Fix |
|---|---|---|---|
| B6 | Toast `Errore [unknown_type]: character_accepted` su player phone | Stale dist/web May 5 14:39 missing PR #197 (May 6) char_create handler | FORCE_REBUILD=1 dist + re-mount |
| B7 | Host kicked dalla room post-transition (host_id flipped a Chiara, room closed) | Stale dist/web May 5 14:39 missing PR #169 (May 5 14:44) host preserve | FORCE_REBUILD=1 dist + re-mount |
| **B8** | Player non-host stuck su STAGE_TRANSITION ("Così sarà.") indefinitely post host pick | Defer guard re-fires da `_on_onboarding_transition_complete` (view stage still transition at signal emit) → `_pending_phase_after_onboarding` re-stored → loop indefinito | PR #205: extract `_should_defer_phase_swap` + `_apply_phase_swap` helpers, bypass defer in transition_complete handler |

## B8 fix design (PR #205)

**Why**: existing `_swap_mode_for_phase` ha defer guard inline. Quando `_on_onboarding_transition_complete` chiama `_swap_mode_for_phase(target)`, defer guard fires perché view stage still STAGE_TRANSITION (signal emit doesn't reset stage). Pending phase re-stored, swap never executes.

**How**:

```gdscript
func _swap_mode_for_phase(phase: String) -> void:
    if _should_defer_phase_swap(phase):
        _pending_phase_after_onboarding = phase
        return
    _apply_phase_swap(phase)


func _should_defer_phase_swap(phase: String) -> bool:
    return (
        _current_mode == MODE_ONBOARDING
        and _current_view is PhoneOnboardingView
        and (_current_view as PhoneOnboardingView).get_current_stage() == "transition"
        and phase != "onboarding"
    )


func _apply_phase_swap(phase: String) -> void:
    match phase:
        "character_creation": _swap_mode(MODE_CHARACTER_CREATION)
        # ... other phases


func _on_onboarding_transition_complete() -> void:
    if _pending_phase_after_onboarding.is_empty():
        return
    var target: String = _pending_phase_after_onboarding
    _pending_phase_after_onboarding = ""
    _apply_phase_swap(target)  # B8 bypass defer guard
```

**Test coverage** (`tests/unit/test_phone_composer_view_nonhost_transition.gd`):
- 4 nuovi test asserts step-by-step flow
- 77/77 regression composer + onboarding suite pass

## Browser-as-phone-smoke pattern (validato 2026-05-07)

User insight: _"i phone non servono per niente, puoi testare maggior parte tramite browser"_. **Functional regression smoke = browser headless 2-tab via Cloudflare Quick Tunnel sufficient**. Mobile-only physical residual = WAN RTT LTE + touch p95 + airplane hardware.

**Workflow**:

1. Pre-flight Node + GUT harness verde (Game/ tests/api + Godot v2 tests/integration)
2. `tools/deploy/deploy-quick.sh` → Cloudflare Quick Tunnel ephemeral URL
3. Browser tab 1 host crea stanza, tab 2 player join via `?room=XXXX`
4. Drive UI via Chrome MCP `computer.left_click` + `computer.key` (NB: `computer.type` non sempre delivery — usa `key` con singoli char)
5. Verify event flow + no toast `[unknown_type]` + no host kick + phase advance entrambi tab

**Caveat**:
- Chrome RAF throttling on background tab ~1Hz → 10s timer Godot view richiede 20-30s wall-clock per accumulate. Master-dd retry phone real foreground = no throttle.
- Godot HTTPClient transient `network_error 13` on multi-tab (specially Tab 2 join). Retry funziona, intermittente. Mobile real device = no issue (single tab/single instance per phone).

## Tunnel-as-launcher pattern (Windows)

`C:\Users\VGit\Desktop\Evo-Phone-Validation.bat` — double-click → spawn Git Bash → run `deploy-quick.sh`. Pattern reusable cross-PC sessione. URL ephemeral cambia ogni run.

## Browser MCP gotchas

- `computer.type` su Godot HTML5 canvas spesso drop char. Usa `computer.key` per singoli char (più reliable).
- Click su canvas Godot UI fields: focus richiede precise coords. Field width detection via screenshot necessary.
- `computer.wait` cap 10s per call. Per >10s → multiple wait calls.
- `read_console_messages` tracks da first call → reload page per capture page-load logs.
- `read_network_requests` no requests visible per Godot HTTPClient (non passa attraverso fetch/XHR observable layer).

## Resume trigger phrase canonical (cross-PC)

> _"resume Phase A cutover post 2026-05-07, master-dd retry phone hardware (p95 + airplane), poi ADR-2026-05-05 swap PROPOSED → ACCEPTED + memory save closure"_

OR

> _"leggi memory/project_phone_smoke_2026_05_07_b8_fix.md, sessione browser smoke complete, master-dd ha eseguito phone retry hardware, drop verdict 3-item physical scope"_

## Critical path post-2026-05-07

| Item | Status | Owner |
|---|:-:|---|
| ADR-2026-05-05 swap PROPOSED → ACCEPTED Phase A | ⏸ blocked | Master-dd phone hardware retry |
| Item 2 mobile p95 (combat 5R real touch) | ⏸ deferred | Master-dd hands-on |
| Item 3 airplane hardware reconnect | ⏸ deferred | Master-dd hands-on |
| #2088 Ready for review | ⏸ pending verdict | Auto post-verdict |

**Browser scope chiuso**: B6 + B7 + B8 fix runtime verified, no other regression visible. Master-dd retry residue = solo physical-only.

## Anti-pattern emerged

- **Stale dist/web on tunnel-as-service**: `dist/web/` persists across runs. `deploy-quick.sh` skips rebuild se exists. Pattern: TUTTI smoke session = `FORCE_REBUILD=1` mandatory. Add to `tools/deploy/deploy-quick.sh` policy doc o flag default.
- **No browser-MCP automation in CI**: B8 emerged solo via 2-tab live browser smoke. Unit test 77/77 verde non lo ha catturato. Future harness candidate: Playwright-equivalent for Godot HTML5 canvas (esiste? P95 spec via Playwright canvas screenshots → assert text region presence post 10s).
