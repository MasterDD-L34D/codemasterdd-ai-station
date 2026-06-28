# Jules task -- direct unit tests for governor.parsers._first_int

Repo: MasterDD-L34D/codemasterdd-ai-station.

## Scope (single file, test-only, NO behaviour change)
Add a NEW pytest file with direct tests for the named function `_first_int` in
`apps/cross-repo-dashboard/governor/parsers.py`. This is a test-only change: do NOT modify
`parsers.py` or any production code. Read it read-only to learn the CURRENT behaviour, then
assert THAT behaviour. No logic change, no behaviour change anywhere.

## Context (read first, read-only)
- `apps/cross-repo-dashboard/governor/parsers.py`, function `_first_int(rx, text)` (around line 39).
  Pure, deterministic, no I/O. Current implementation:
      def _first_int(rx, text):
          m = rx.search(text or "")
          return int(m.group(1)) if m else 0
  `rx` is a COMPILED regex (re.Pattern) with at least one capturing group; `text` is a string or None.
- Existing sibling test for the same module:
  `apps/cross-repo-dashboard/tests/test_governor_parsers.py`. Mirror its import style:
  `from governor.parsers import _first_int` (the tests/conftest.py puts `governor` on sys.path;
  pytest runs with import-mode=importlib). Use `import re` to build the compiled patterns. Do NOT
  add any sys.path hacks of your own.

## File to modify (ONLY this one)
- NEW `apps/cross-repo-dashboard/tests/test_governor_parsers_first_int.py`

## What the tests must assert (CURRENT behaviour of the named function)
Assert exact return values; do NOT change behaviour. Cover at least:
- A match returns the captured int: `_first_int(re.compile(r"(\d+) cycles"), "5 cycles") == 5`.
- No match returns 0: `_first_int(re.compile(r"(\d+) cycles"), "no number here") == 0`.
- None text returns 0 (the `text or ""` branch): `_first_int(re.compile(r"(\d+)"), None) == 0`.
- Empty text returns 0: `_first_int(re.compile(r"(\d+)"), "") == 0`.
- The FIRST match wins when several are present: `_first_int(re.compile(r"(\d+)"), "3 then 9") == 3`.
- Leading zeros parse as int: `_first_int(re.compile(r"(\d+)"), "007 agents") == 7`.
Tests must be deterministic and hit no network and no filesystem.

## Constraints
- ASCII-only in all added code and comments (repo ADR-0021).
- Pure pytest; no new dependencies; do not touch the lockfile or any config file.
- Do NOT edit parsers.py or any non-test file. Single new test file only.
- Conventional Commit subject (lowercase), e.g.:
  test(parsers): direct tests for governor _first_int helper

## Acceptance (verify before delivering)
- The new test file passes:
  `python -m pytest -q apps/cross-repo-dashboard/tests/test_governor_parsers_first_int.py`.
- The existing governor suite stays green (no regressions, all tests pass):
  `python -m pytest -q apps/cross-repo-dashboard/tests`.
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
