# Task: fix publishWorld trimmed payload -- add phase + actor key (Game #2733)

Repo: MasterDD-L34D/Game
Target file: apps/play/src/main.js (the lobbyBridge.publishWorld({...}) call, ~line 1342, post #2727)
Read-only reference: apps/backend/routes/sessionHelpers.js (publicSessionView, ~line 436)

FIRST: read GitHub issue #2733 in this repo -- it is the authoritative gap description
(wire-truth evidence from the Godot item-4 AI playtest, 2026-06-11).

## Scope (single-file fix, additive only)

In the trimmed payload of lobbyBridge.publishWorld in apps/play/src/main.js:

1. Add the key `phase` carrying the TV's current phase string (the same phase the web TV
   consumer already uses for its snapshot mode map; if a phase variable is not in scope at
   the call site, derive it exactly like the nearest existing consumer does -- do NOT
   invent new state).
2. Fix the actor key: the current code reads state.world.active_id which is ALWAYS
   undefined (publicSessionView exposes `active_unit`, not `active_id`), so
   JSON.stringify drops the key and phones receive NO actor key. Publish
   `active_id: state.world.active_unit` (and keep/emit `active_unit` additively if
   trivially available). The web consumer apps/play/src/ctBar.js (~line 92) already
   handles the dualism with `active_unit || active_id`.

Pattern to follow: merged PR #2727 (additive forward of overcharge_used_this_run in the
SAME payload). NO other behavior change. NO removal of existing keys. Single concern.

## Acceptance (tests must pass)

- Add or extend a unit test guarding payload parity: the published world payload MUST
  contain a defined actor key (active_id valued from active_unit) and a `phase` key,
  mirrored against a publicSessionView-shaped fixture. Follow the existing publish/forward
  guard test conventions (see the tests around #2727 if present).
- The full existing test suite passes (repo CI). CI green is required.

## Constraints

- ASCII-only in all added code, comments and strings.
- Conventional Commit subject, lowercase description, e.g.
  `fix(play): publishWorld forwards phase + active actor key (#2733)`.
- Deliver as a PR referencing issue #2733. Do NOT merge -- human gate (Eduardo) disposes.
