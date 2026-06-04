---
name: feedback-chrome-mcp-visual-loop
description: Autonomous SEE→diagnose→fix→redeploy→re-verify loop via Chrome MCP browser_batch + named tunnel. Closes feedback gap without master-dd device test in middle. Validated 5 iterations 2026-05-20.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7c08f071-f7f8-4cf0-a16b-fcd6aba717fa
---

Chrome MCP + named Cloudflare tunnel + deploy-quick.sh = autonomous visual feedback loop. Claude SEES rendered Godot HTML5 export + INTERACTS via clicks/types + READS console + diagnoses + ships code fix + redeploys + re-verifies — all without master-dd device test in middle.

**Why:** Master-dd's complaint "non noto grandi differenze" was Claude flying blind on visual surfaces. Each fix shipped → "ship and pray". Loop closes that gap. 5 iterations validated 2026-05-20 caught:
1. TV booting wrong scene (combat tutorial vs LobbyView) → PR #305 fix
2. TV portrait viewport on desktop → PR #304 fix
3. TV disconnected remote room → PR #307 Eval A
4. Quick Tunnel random URL friction → PR #307 named tunnel default
5. HTTPRequest WASM hang → PR #308 known-issue doc

**How to apply:**

1. Deploy via `deploy-quick.sh` (auto-picks named tunnel `evo-tactics.com` if token present)
2. Chrome MCP `tabs_context_mcp` to get tab IDs (create if empty)
3. `browser_batch(navigate + wait 8-10s + screenshot)` → SEE rendered surface
4. Diagnose root cause from visual evidence (NOT from code-only reasoning)
5. Code fix → local GUT + lint
6. PR + merge
7. Re-deploy + `browser_batch(reload + wait + screenshot)` to verify
8. Use `read_console_messages` for Godot `print()` debug surfaces
9. Use `javascript_tool` for DOM/window introspection (URL queries, native fetch tests)
10. For WS protocol testing: Node.js + `ws` lib from `Game/apps/backend` (already installed) — REST `/api/lobby/join` → get player_token → WS connect with `?code=X&player_id=Y&token=Z` URL

**Loop discipline:**

- Each cycle ~3-5min (build + tunnel + reload + verify)
- Time-box at 4-5 iterations per session. If root cause not clear, document as known-issue + master-dd checkpoint.
- ALWAYS verify FROM screenshot before assuming code is correct. Print()-debug to Godot console (Chrome MCP `read_console_messages`) when behavior silent.
- WASM-specific gotchas to verify: HTTPRequest first await hang, Timer.autostart pre-add_child unreliability, JavaScriptBridge as fallback.

**Tools chain (per session):**

- `mcp__Claude_in_Chrome__tabs_context_mcp` + `tabs_create_mcp`
- `mcp__Claude_in_Chrome__browser_batch` (navigate + wait + click + type + screenshot in one round-trip)
- `mcp__Claude_in_Chrome__read_console_messages` (filter by pattern)
- `mcp__Claude_in_Chrome__javascript_tool` (action: "javascript_exec")
- `Monitor` (deploy progress events)
- `Bash run_in_background` (Node WS simulation, kill leftover procs)
- Cloudflare named tunnel `evo-tactics.com` (stable URL across iterations)

**Anti-pattern callout:** Quick Tunnel random URLs FORCE master-dd to re-bookmark per session. Use `tools/deploy/named-tunnel.sh` OR `deploy-quick.sh` post-#307 (auto-detect `~/.cloudflared/evo-tactics-prod.token`).

Related: [[feedback-loc-sum-check]] [[feedback-peer-review-blocker-pattern]] [[project-pr-284-cascade-closure]]
