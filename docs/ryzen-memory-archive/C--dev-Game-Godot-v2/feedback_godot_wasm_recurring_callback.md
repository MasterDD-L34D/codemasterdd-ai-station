---
name: feedback-godot-wasm-recurring-callback
description: Godot 4.6 WASM single-threaded export has FUNDAMENTAL recurring-callback limitations. 6 mechanisms tested broken. Working pattern - JS-side setInterval writes window var + GDScript _process reads. Validated PR #312 2026-05-20.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7c08f071-f7f8-4cf0-a16b-fcd6aba717fa
---

Godot 4.6 export HTML5 "single-threaded, no GDExtension" lacks SharedArrayBuffer + WebWorker support. **All Godot-side recurring callback mechanisms broken** on WASM Cloudflare HTTPS path.

**6 broken mechanisms tested** (PR #307-#311):
1. `HTTPRequest.request()` first await hangs forever
2. `Timer.timeout` (autostart pre-add_child) never fires
3. `Timer.timeout` (explicit start() post-add_child) fires ONCE only
4. `get_tree().create_timer().timeout` (SceneTreeTimer) hangs
5. `JavaScriptBridge.create_callback` via setInterval — callback never invoked
6. `JavaScriptBridge.create_callback` ref-as-member (anti-GC) — same

**Working pattern** (PR #312, verified end-to-end via Chrome MCP iter 12):

JS-side native `setInterval` + `fetch` writes result to `window.__var`. GDScript `_process` reads window var every frame. Pure-data read = no Godot async involved.

```gdscript
# 1. JS-side scheduler scrive su window var
JavaScriptBridge.eval("""
    window.__my_data = null;
    window.__my_tick = function() {
        fetch('/api/...').then(r => r.text()).then(t => { window.__my_data = t; });
    };
    window.__my_tick();
    if (!window.__my_interval) {
        window.__my_interval = setInterval(window.__my_tick, %d);
    }
""" % INTERVAL_MS, true)
set_process(true)

# 2. GDScript _process legge window var (NO async, NO callback)
func _process(_delta: float) -> void:
    var raw: String = _read_window_var()
    if raw.is_empty() or raw == _last_processed:
        return
    _last_processed = raw
    # parse + apply...

func _read_window_var() -> String:
    if not OS.has_feature("web"): return ""
    var window: JavaScriptObject = JavaScriptBridge.get_interface("window")
    if window == null: return ""
    var raw_var: Variant = window.__my_data
    return String(raw_var) if raw_var != null else ""
```

**Cleanup**: store interval ID on window so re-instantiation idempotent (`if (!window.__my_interval)`). No GDScript-side cleanup needed (interval persists tab lifetime).

**Verification**: 3 reactive updates without reload via Chrome MCP autonomous loop:
- Pre-join: 0/0, vuoto
- Player1 WS-connect: 0/1, "Player1"
- Player1 off + Player2 on: 0/1, "Player2"

**Alternative future fixes** (out of scope 2026-05-20):
1. SharedArrayBuffer threading export (CORP + COEP headers, may break Cloudflare)
2. WebSocket spectator role (server push, no polling)
3. Server-Sent Events `EventSource` native browser-driven

**Anti-patterns to avoid**:
- Coroutine self-loop via SceneTreeTimer (mechanism #4 hangs)
- Timer Node any flavor (mechanisms #2 #3)
- `JavaScriptBridge.create_callback` for recurring scheduling (mechanisms #5 #6)
- HTTPRequest direct on Cloudflare HTTPS WASM path (mechanism #1) — use `WebFetchJson` JS bridge bypass

Related: [[feedback-chrome-mcp-visual-loop]] [[project-pr-284-cascade-closure]]
