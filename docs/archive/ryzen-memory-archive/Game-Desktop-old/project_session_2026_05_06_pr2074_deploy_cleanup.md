---
name: Session 2026-05-06 PR #2074 deploy stack cleanup
description: Supersede + remove ADR-2026-04-26 hosting stack (CF Pages + Render) post Godot v2 pivot. PR shipped main + userland CF/Render dashboard cleanup via Chrome MCP.
type: project
originSessionId: 5601a2ad-e6f6-483d-a234-1fdbb8521c19
---
## PR #2074 squash merged

- **Merge SHA**: `55a8b5f3` su main
- **Title**: `chore(deploy): supersede + remove ADR-2026-04-26 hosting stack — Godot v2 pivot`
- **Diff**: 9 file, +31 -515 LOC (2 commit squashed: `c0130ad2` superseded headers + `f5788d35` remove infra)

### Files removed
- `wrangler.toml` (CF Workers/Pages config "evo")
- `render.yaml` (Render free web service backend Express+ws)
- `scripts/deploy-min.sh` (orchestrator preflight+build+deploy+smoke)
- `tests/scripts/deploy-min-bundle.test.js` (sanity test)

### Files preserved (TREE-INTACT)
- `apps/play/` source — frontend Game/ ancora attivo
- `apps/play/runtime-config.production.js` — reverse-fallback potenziale
- `package.json` `play:build` script — build target dev locale
- ADR + research + playtest + planning + checklist docs — historical records
- `ADR-2026-04-26` mark `superseded` con `superseded_by` ref a ADR-2026-04-29 + ADR-2026-05-05

## Userland cleanup eseguito (Chrome MCP)

| Target | Action | Method | Status |
|--------|--------|--------|--------|
| CF Workers project `evo` (account `7811187141724a441294a820cd6c0bd8`) | Disconnect git repo | Chrome MCP click sequence | ✅ |
| Render service `evo-tactics-backend` (`srv-d7lag5lf420s73cjmj6g`) Frankfurt | Suspend | Chrome MCP modal + user manual phrase typing | ✅ |

**NON eseguito** (lasciato dormant per reversibility):
- CF project full delete (kill `evo.eduscarpelli.workers.dev`)
- Render service full delete (kill `evo-tactics-backend.onrender.com`)

## Re-add cost se Godot cutover regredisce

- Repo files: ~20 min via `git revert 55a8b5f3` + adjust ADR
- CF dashboard: 1 click "Connetti" repo MasterDD-L34D/Game
- Render dashboard: 1 click "Resume Web Service"

## Lessons sessione

- **Bot CI Cloudflare auto-deploy**: confirmation diretta che config wired live = drain free tier ogni push. PR superseded headers non bastano, removal mandatory per killare auto-trigger.
- **Branch protection check vs CF bot fail**: CF "Workers Builds: evo" NON in required list (`paths-filter, python-tests, stack-quality, cli-checks, dataset-checks, governance`). Mergeable anche con CF fail = expected post-removal.
- **Sandbox per-action denial**: Chrome MCP destructive op su shared infra blocca anche con user "consento" generic. Richiede target naming esplicito (es. service ID + action specifica). Pattern: ask explicitly before retry.
- **Confirm phrase Render**: Suspend richiede typing literal `sudo suspend web service <name>` — user manual step (Chrome MCP type blocked).

## Trigger phrase canonical resume

> _"verify CF Workers `evo` + Render `evo-tactics-backend` ancora suspended, OR resume per Godot fallback se cutover Fase 3 regredisce"_

## Next steps

- Master-dd phone smoke retry Godot v2 (B5 + combat 5c + airplane 5d)
- Post smoke success → ADR-2026-05-05 status PROPOSED → ACCEPTED → considera full delete CF+Render
- Post smoke fail → resume Render + reconnect CF + revert PR #2074
