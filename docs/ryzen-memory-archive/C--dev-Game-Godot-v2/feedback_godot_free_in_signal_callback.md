# Godot: never immediate-free an object inside its own signal callback

**Date**: 2026-05-22 (CAMP-3c, PR #350)

## Lesson
A handler connected to a signal runs WHILE the emitter is mid-emit. Calling `obj.free()` (immediate) on the object that owns/emits that signal during the callback crashes Godot: "Object was deleted while emitting a signal". Use `obj.queue_free()` (deferred to end-of-frame) instead.

Concrete: `DebriefView.continue_pressed` → `MainDebrief.reenter(host)` frees the DebriefView. `reenter` runs inside the `continue_pressed` callback, so `view.free()` would crash. Fixed to `view.queue_free()`.

## Test consequence (load-bearing)
`queue_free()` does NOT invalidate same-frame. So `assert_false(is_instance_valid(view))` FAILS right after a queue_free. Assert `assert_true(view.is_queued_for_deletion())` instead. (Two tests failed exactly this way on resume; plan had specified `free()` + `is_instance_valid==false`, the queue_free fix flipped both.)

## Rule
- Freeing the emitter (or a node up the call stack from the emit) inside its handler → `queue_free`, never `free`.
- Immediate `free()` is only safe for a node UNRELATED to the in-flight signal (e.g. MainDebrief.mount frees a *prior* DebriefView before a fresh emit — different object, no active emit).
- Tests on queue_free paths assert `is_queued_for_deletion()`, not `not is_instance_valid()`.
