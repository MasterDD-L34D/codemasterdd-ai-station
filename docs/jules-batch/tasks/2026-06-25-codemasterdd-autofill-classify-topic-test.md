# Jules task -- direct unit tests for autofill-disposition.py classify_topic

Repo: MasterDD-L34D/codemasterdd-ai-station.

## Scope (single file, test-only, NO behaviour change)
Add a NEW pytest file with direct tests for the named pure function `classify_topic(label)` in
`chatgpt-recovery/pipeline/autofill-disposition.py`. This is a test-only change: do NOT modify
`autofill-disposition.py` or any production code. Read it read-only to learn the CURRENT
behaviour, then assert THAT behaviour. No logic change, no behaviour change anywhere.

## Context (read first, read-only)
- `chatgpt-recovery/pipeline/autofill-disposition.py`, function `classify_topic(label)` (around
  line 70). Pure, deterministic, no I/O. Returns a `(disposition, space)` tuple:
  - if `label.lower()` contains 'mixed-misc' OR 'outlier' -> the module `DEFAULT` = ('HOLD', '').
  - else the FIRST `RULES` entry whose any keyword is a substring of `label.lower()` -> its
    `(disposition, space)`.
  - else `DEFAULT` = ('HOLD', '').
- The file name has a HYPHEN and the module imports only stdlib, so import it via importlib from
  its file path (the arbitrary module name sidesteps the hyphen):
      import importlib.util
      from pathlib import Path
      _spec = importlib.util.spec_from_file_location(
          "autofill_disp", Path(__file__).resolve().parent / "autofill-disposition.py")
      mod = importlib.util.module_from_spec(_spec)
      _spec.loader.exec_module(mod)
      classify_topic = mod.classify_topic
  Do NOT install or download anything. Do NOT add a sys.path hack.
- Read the `RULES` list + `DEFAULT` in the source to get the EXACT expected tuples; assert against
  those actual values (do not guess). Use only ASCII keywords from RULES (e.g. cremesi, pathfinder,
  api, canzone, npc) -- do NOT use any non-ASCII keyword in the test.

## File to modify (ONLY this one)
- NEW `chatgpt-recovery/pipeline/test_autofill_disposition_classify_topic.py`

## What the tests must assert (CURRENT behaviour; assert exact return values, do NOT "fix")
Cover at least:
- a 'mixed-misc' label and an 'outlier' label each return DEFAULT ('HOLD', '').
- a label containing a specific ASCII keyword returns that rule's exact tuple (pick a few from
  RULES, e.g. 'cremesi', 'pathfinder', 'api', 'canzone' -- assert the EXACT (disp, space) read
  from the source).
- matching is case-insensitive (an upper-cased keyword still matches).
- a label matching NO rule returns DEFAULT ('HOLD', '').
- precedence: a label containing BOTH 'mixed-misc' AND a real keyword returns DEFAULT (the
  mixed-misc/outlier check runs before the rules).
Tests must be deterministic and hit no network and no filesystem.

## Constraints
- ASCII-only in all added code and comments (repo ADR-0021) -- including the test labels.
- Pure pytest; no new dependencies; do not touch the lockfile or any config file.
- Do NOT edit autofill-disposition.py or any non-test file. Single new test file only.
- Conventional Commit subject (lowercase), e.g.:
  test(autofill): direct tests for classify_topic disposition rules

## Acceptance (verify before delivering)
- The new test file passes:
  `python -m pytest -q chatgpt-recovery/pipeline/test_autofill_disposition_classify_topic.py`.
- No regressions elsewhere (tests pass).
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
