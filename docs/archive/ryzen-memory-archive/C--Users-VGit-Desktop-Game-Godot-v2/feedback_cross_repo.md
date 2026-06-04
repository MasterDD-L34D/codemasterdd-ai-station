---
name: Cross-repo discipline (Game canonical, Godot v2 consumer)
description: Don't duplicate backend logic in Godot — read-only ETL from Game/ canonical
type: feedback
originSessionId: 585dba96-6d14-4988-ab48-b6cb8dcaf004
---
Game-Godot-v2 is a port consumer of `MasterDD-L34D/Game/` web stack v1.

**Why:** Single source of truth prevents drift. ADR-2026-04-19 decommissions services/rules/ Python deprecated path; Express backend on Game/ is canonical. Game-Godot-v2 must NOT re-implement Express logic — only consume via HTTPClient + WebSocketClient OR ETL canonical YAML/JSON datasets.

**How to apply:**
- Edit dataset/spec/ADR ON `Game/` (canonical), pull-sync to `Game-Godot-v2/` via ETL scripts in `tools/etl/`.
- Express backend persists on Game/ side cross-stack — Godot does not duplicate.
- Read-only references in Game-Godot-v2: `data/core/traits/active_effects.yaml` (458 entries), `data/core/species/*_lifecycle.yaml` (15), `apps/backend/services/combat/`, `apps/backend/routes/session.js` (1967 LOC), `apps/backend/services/ai/`, `apps/play/public/assets/`, `docs/skiv/CANONICAL.md`.
- ETL pattern: `tools/etl/yaml_to_json.py` (single file) + `tools/etl/lifecycle_yaml_to_json.py` (batch dir). Future ETL scripts mirror this `--in` / `--out` shape.
- Only session engine + UI logic lives in Godot. Combat/AI services are ported as scripts/combat/ scripts/ai/ following Express service module boundary.
