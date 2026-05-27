---
name: Tier 0 Deep Dive — boardgame.io + wesnoth + awesome-game-design
description: Concrete pattern extraction from 3 Tier 0 repos — 12 actionable patterns for Evo-Tactics session engine, data pipeline, balance, and GDD gaps
type: reference
---

# Tier 0 Deep Dive (2026-04-16)

## A. boardgame.io — Pattern Extraction

### Top 3 (high value)

1. **playerView (hide AI intents)** — LOW effort, HIGH value
   Strip `pending_intents` for SIS units during `round_phase === 'planning'`. ~15 lines in `sessionHelpers.js`. Increases tactical tension.

2. **enumerateLegalActions** — MEDIUM effort, HIGH value
   Extract `enumerateLegalActions(state, unitId)` listing all valid (action, target) pairs. Feed to `selectAiPolicy` instead of hardcoded `pickLowestHpEnemy`. Enables difficulty profiles (random=easy, weighted=normal, lookahead=hard).

3. **Round flow event callbacks** — MEDIUM effort, HIGH value
   Thin event layer: `emit('round:committed')`, `emit('round:resolved')`, `emit('round:ended')`. Decouples session endpoints from orchestrator. Enables VC scoring hooks, animation triggers.

### Also noted

4. **Phase config object** — LOW effort, MEDIUM value. Data-driven phase validation replacing scattered constants.
5. **maxIntentsPerUnit config** — LOW effort, LOW value. Cap from boardgame.io's `moveLimit`.
6. **Plugin system** — SKIP. Factory + DI pattern already sufficient.

### Priority matrix

| Pattern | Effort | Value | Verdict |
|---|---|---|---|
| playerView | Low | High | ADOPT |
| enumerateLegalActions | Medium | High | ADOPT |
| Event callbacks round flow | Medium | High | ADAPT |
| Phase config object | Low | Medium | ADAPT |
| maxIntentsPerUnit | Low | Low | ADOPT |
| Plugin system | High | Low | SKIP |

---

## B. wesnoth — Pattern Extraction

### Top 5 actionable

1. **Data-level test scenarios** — Add `data/test/` YAML balance fixtures resolved by rules engine. Wesnoth has `data/test/` with WML-level test scenarios. Evo-Tactics validates schema only — lacks content-level balance assertions.

2. **Species archetype layer** — Wesnoth's `movetypes.cfg` macros define reusable stat blocks (FLY_MOVE, MOUNTAIN_MOVE). Species inherit archetype + override. Apply: define 5-8 archetypes (flyer, burrower, aquatic...) between `trait_mechanics.yaml` and individual species. Reduces YAML duplication.

3. **Tagged balance tiers** — Wesnoth's `era_default` (balanced) vs `era_heroes` (not balanced). Apply: tag content in `ai_profiles.yaml` with `tier: competitive|narrative`. PT_POOL_CAP/DAMAGE_STEP_CAP enforce per-tier, not globally.

4. **Pack manifest schema** — Wesnoth's `pbl.cfg` declares pack version, compatible engine version, author. Apply: add `pack_manifest.yaml` with AJV validation for pack contracts before accepting community packs.

5. **Telemetry feedback loop** — Wesnoth has NO telemetry (balance is manual/community). Evo-Tactics is AHEAD. Gap to exploit: wire telemetry back into automated balance assertions (trait producing damage_step > cap across N sessions → flag in validation).

---

## C. awesome-game-design — GDD Gap Resources

### Gap → Best resources

| GDD Gap | Resources |
|---|---|
| **Level Design** | Fallout Tactics postmortem, Chris Taylor template (runawaystudios.com), Diablo 1 pitch (graybeardgames.com) |
| **Art Direction** | Chris Taylor template (Art Bible section) |
| **Audio Design** | Chris Taylor template (Audio section) — weakest coverage |
| **Narrative/Lore** | Hades GDC talk (gdcvault.com/play/1026975), Ink/Inky, Twine, Arcweave |
| **Screen Flow** | Generic GDD templates (Google Drive links) |
| **Target Audience** | Generic GDD templates, Nuclino methodology guide |
| **Save/Load** | Chris Taylor template, Deus Ex design doc |
| **Controls** | Generic GDD templates — no dedicated resource |

### High-value postmortems (tactical/strategy)

- **Fallout Tactics** — turn-based squad, d20-derived, AI failures, level design lessons
- **Frozen Synapse** — simultaneous-turn, AI opponent, minimal UI for complex state
- **AI War (4yr postmortem)** — asymmetric AI opponent, Co-op vs Sistema directly applicable
- **Baldur's Gate II** — d20 combat, party AI, encounter design canonical
- **Hades** — narrative integration into systems-heavy game without cutscenes

### Balance/systems tools

- **Machinations** (machinations.io) — visual economy modeling, PT pool / damage step / fairness caps
- **Game Design Patterns Wiki** (Chalmers) — academic pattern catalog for turn-based combat
- **Lost Garden** (Daniel Cook) — loops and arcs framework for session-to-campaign progression
- **Designer Notes** (Soren Johnson, Civ IV) — turn-based balance, AI, complexity management

### Notable gap in awesome list itself

No TV-first (10-foot) UI resources. For that: Google Android TV design guidelines + Valve Steam Big Picture docs.
