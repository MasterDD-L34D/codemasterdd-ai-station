---
name: Phase 2 Deep Dive Results (Grid, AI, Level Design, Networking)
description: Findings from 4 parallel deep dives on external repos — patterns extracted for SoT v3 §14-§18
type: reference
---

# Phase 2 Deep Dive Results (2026-04-16)

## Grid & Pathfinding (§14)

**Best fit:** Hex grid with axial coordinates (q,r).

| Library | Type | Stars | Pathfinding | FOV/LOS | Node.js | npm |
|---|---|---|---|---|---|---|
| easystarjs | Square A* | 1.9k | ✅ async A* | ❌ | ✅ | ✅ ~7kb |
| honeycomb-grid | Hex grid | 695 | A* example | ❌ | ✅ ≥16 | ✅ |

- Red Blob Games: axial coords best for most projects. Distance = `max(|q|,|r|,|s|)/2`.
- AncientBeast: hex 16×9, multi-hex units (size 1-3), `getMovementRange()`.
- LOS: linear interpolation N+1 samples, epsilon bias for edge ambiguity.
- FOV: ray-cast from center, stop on `blocks_los` tiles.

## AI Sistema (§13.5 evolution)

**Best fit:** Utility AI (~400 LOC port).

| Pattern | Repo | Effort | Value | Verdict |
|---|---|---|---|---|
| Utility AI | UtilityAI (C#) | Low | High | **ADOPT** |
| Goal Evaluators | yuka (JS) | Medium | Medium | ADAPT if needed |
| GOAP | GOApy (Python) | High | Low | SKIP |
| BT/HTN | Behaviac (C++) | High | Low | SKIP |

Key: Brain + Action + Consideration classes. Score = Π(consideration_i). Difficulty = weight tuning.

## Level Design (§15)

**Findings:**
- AncientBeast: no encounter templates, hard-coded hex 16×9, PvP only
- wesnoth: campaign = linear scenario sequence, difficulty scaling via quantity tags
- rpg_tactical_fantasy_game: XML data-driven balance, maps hand-crafted

**Decisions:** YAML encounter templates, 7 biome arcs × 4-5 encounters = ~30-35 total. Schema AJV.

## Networking (§16)

**Best fit:** Colyseus (MIT, Node.js native, turn-based support).

- Server-authoritative, room-based, delta-compression + binary encoding
- Coexists with Express on separate port/route
- xstate FSM → room state transitions directly
- Effort: ~2-3 weeks refactor session.js → Colyseus Schema
- Alternatives: Socket.io (too low-level), Nakama (too heavy), Photon (proprietary)
