# Jules task -- GDScript doc-comment batch 39 (closing duo, comment-only)

Repo: MasterDD-L34D/Game-Godot-v2.

## Scope (2 files, comment-only additions, NO logic change, no behavior change)

Add GDScript `##` doc-comments to the public API of exactly TWO files:

- `scripts/net/resume_token_manager.gd`
- `scripts/main_coop_combat_end.gd`

This is a comment-only change: ZERO deletions, zero edits to any existing line,
no rename/reformat/reorder, no other file touched. Every line to add is given
verbatim below and is pre-verified (gdformat unchanged, gdlint clean, all lines
ASCII and <= 100 chars). Copy each line byte-identical at the exact anchor.

Placement rule (load-bearing): each `##` line/block goes IMMEDIATELY above its
anchor line, with NO blank line between the `##` block and the anchor. Existing
`#` comments above the anchor stay where they are (insert the `##` lines BELOW
them, directly against the anchor line).

## Edits -- scripts/net/resume_token_manager.gd (10 lines)

Directly above the line `class_name ResumeTokenManager` insert:

```
## Client-side WS resume scaffold: version cursor, replay handlers, ledger batch dispatch.
## The reconnect query fragment comes from build_reconnect_query_fragment() ("" = fresh).
```

Directly above `func update_seen_version(version: int) -> void:` insert:

```
## Advances the version cursor when a newer state/intent version arrives.
```

Directly above `func reset() -> void:` insert:

```
## Resets the cursor to VERSION_UNKNOWN (full reconnect or new room).
```

Directly above `func register_handler(event_class: String, handler: Callable) -> void:` insert:

```
## Registers a replay handler for an event_class; empty class or invalid Callable is ignored.
```

Directly above `func unregister_handler(event_class: String) -> bool:` insert:

```
## Removes the handler for event_class; returns true when one was removed.
```

Directly above `func apply_ledger_entry(entry: LedgerEntry) -> void:` insert:

```
## Applies one ledger entry: advances the cursor, then dispatches to the matching handler.
```

Directly above `func apply_replay_batch(entries: Array) -> void:` insert:

```
## Applies a server replay batch; accepts LedgerEntry objects or wire-shape Dictionaries.
```

Directly above `func build_reconnect_query_fragment() -> String:` insert:

```
## Returns "&last_version=N" for reconnect, or "" when no version has been seen yet.
```

Directly above `func handler_count() -> int:` insert:

```
## Diagnostic: the number of registered replay handlers.
```

Do NOT touch the inner `class LedgerEntry` or its `_init` (private).

## Edits -- scripts/main_coop_combat_end.gd (3 lines)

Directly above the line `class_name MainCoopCombatEnd` insert:

```
## Main-side helper for POST /api/coop/combat/end: host-only debrief handoff to the backend.
```

Directly above `static func notify_host(` insert:

```
## Fire-and-forget POST; true when the dispatch started, false when host/auth guards reject.
```

Directly above `static func notify_host_blocking(` insert:

```
## Awaitable variant returning the response Dictionary (tests and sync paths).
```

Do NOT touch `_dispatch` or `_outcome_string` (private).

## Constraints (strict)

- ONLY the two files above; ONLY the 13 `##` lines given, byte-identical.
- ZERO deletions (git diff must show 0 removed lines), zero touched existing lines.
- ASCII-only; every added line starts with `## ` and is <= 100 characters.
- Conventional Commit subject (lowercase), e.g.:
  docs(scripts): doc-comment batch 39 -- resume_token_manager + main_coop_combat_end

## Acceptance (verify before delivering)

- `git diff --numstat` -> exactly 2 files, +10/+3 added lines, 0 deletions each.
- Every added line starts with `## ` and sits directly above its anchor with no
  blank line in between.
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
