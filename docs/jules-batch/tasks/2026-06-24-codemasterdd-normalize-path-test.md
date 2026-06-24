# Jules task -- direct unit tests for governor.reconcile._normalize_path

Repo: MasterDD-L34D/codemasterdd-ai-station.

## Scope (single file, test-only, NO behaviour change)
Add a NEW pytest file with direct edge-case tests for the named function
`_normalize_path` in `apps/cross-repo-dashboard/governor/reconcile.py`. This is a
test-only change: do NOT modify `reconcile.py` or any production code. Read it
read-only to learn the CURRENT behaviour, then assert THAT behaviour. No logic
change, no behaviour change anywhere.

## Context (read first, read-only)
- `apps/cross-repo-dashboard/governor/reconcile.py`, function `_normalize_path(path)`
  (around line 44). Pure, deterministic, no I/O. Current implementation:
      p = (path or "").replace("\\", "/").strip()
      while p.startswith("./"): p = p[2:]
      if p.startswith("~/"): p = p[2:]
      return p.lstrip("/")
- Existing sibling test for the same module:
  `apps/cross-repo-dashboard/tests/test_governor_reconcile_doctrine.py`. Mirror its
  import style: `from governor.reconcile import _normalize_path` (the tests/conftest.py
  puts `governor` on sys.path; pytest runs with import-mode=importlib). Do NOT add any
  sys.path hacks of your own.

## File to modify (ONLY this one)
- NEW `apps/cross-repo-dashboard/tests/test_governor_reconcile_normalize_path.py`

## What the test must assert (CURRENT behaviour of the named function)
Cover, via pytest (parametrize where natural), at least these cases. Assert exact
return values; do NOT "fix" or change behaviour:
- None -> "" and "" -> "" (the `path or ""` branch).
- Backslashes become forward slashes: "a\\b\\c" -> "a/b/c".
- Surrounding whitespace stripped: "  x/y  " -> "x/y".
- Leading "./" stripped repeatedly: "./x" -> "x"; "././x" -> "x".
- A single leading "~/" stripped: "~/foo" -> "foo".
- Leading slashes stripped: "/abs/path" -> "abs/path"; "///a" -> "a".
- Order-sensitive combo (assert the ACTUAL result): "~/./x" -> "./x" (the while-loop
  runs before the "~/" strip, so the "./" left after stripping "~/" is NOT removed).
- A backslash-introduced "./" is normalized then stripped: ".\\x" -> "x".
Tests must be deterministic and hit no network and no filesystem.

## Constraints
- ASCII-only in all added code and comments (repo ADR-0021).
- Pure pytest; no new dependencies; do not touch the lockfile or any config file.
- Do NOT edit reconcile.py or any non-test file. Single new test file only.
- Conventional Commit subject (lowercase), e.g.:
  test(governor): direct edge-case tests for reconcile _normalize_path

## Acceptance (verify before delivering)
- The new test file passes:
  `python -m pytest -q apps/cross-repo-dashboard/tests/test_governor_reconcile_normalize_path.py`.
- The existing governor suite stays green (no regressions, all tests pass):
  `python -m pytest -q apps/cross-repo-dashboard/tests`.
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
