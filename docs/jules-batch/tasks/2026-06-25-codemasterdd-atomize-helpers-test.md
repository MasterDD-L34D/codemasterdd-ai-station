# Jules task -- direct unit tests for atomize.py helpers (yaml_escape + detect_language)

Repo: MasterDD-L34D/codemasterdd-ai-station.

## Scope (single file, test-only, NO behaviour change)
Add a NEW pytest file with direct tests for two named, pure functions in
`chatgpt-recovery/pipeline/atomize.py`: `yaml_escape(s)` and `detect_language(text)`.
This is a test-only change: do NOT modify `atomize.py` or any production code. Read it
read-only to learn the CURRENT behaviour, then assert THAT behaviour. No logic change,
no behaviour change anywhere.

## Context (read first, read-only)
- `chatgpt-recovery/pipeline/atomize.py` -- a standalone script (argparse main guarded by
  `if __name__ == "__main__"`; importing it has no side effects). It is NOT part of a package
  and the directory has no conftest, so import it WITHOUT a sys.path hack by loading it directly
  via importlib from its file path, e.g.:
      import importlib.util
      from pathlib import Path
      _spec = importlib.util.spec_from_file_location(
          "atomize_mod", Path(__file__).resolve().parent / "atomize.py")
      atomize_mod = importlib.util.module_from_spec(_spec)
      _spec.loader.exec_module(atomize_mod)
      yaml_escape = atomize_mod.yaml_escape
      detect_language = atomize_mod.detect_language
  atomize.py imports only stdlib (argparse, hashlib, json, re, sys, datetime, pathlib) -- do NOT
  install or download anything.
- `yaml_escape(s)` (around line 143): returns the string '""' when s is falsy (None or empty);
  otherwise returns the value wrapped in double quotes after escaping, IN THIS ORDER: backslash
  `\` -> `\\`, then double-quote `"` -> `\"`, then newline -> a single space.
- `detect_language(text)` (around line 150): counts italian-marker words vs english-marker words
  (case-insensitive, word-boundaried). Returns 'it' if it_markers > en_markers; else 'en' if
  en_markers > 3; else 'mixed'.

## File to modify (ONLY this one)
- NEW `chatgpt-recovery/pipeline/test_atomize_helpers.py`

## What the tests must assert (CURRENT behaviour; assert exact return values, do NOT "fix")
yaml_escape:
- yaml_escape(None) == '""' and yaml_escape("") == '""'.
- A plain word is wrapped in quotes: yaml_escape("plain") == '"plain"'.
- A backslash is doubled: input one backslash between a and b -> output has two backslashes
  between a and b, inside the surrounding quotes.
- An embedded double-quote is backslash-escaped inside the quotes.
- A newline in the value becomes a single space (no literal newline in the output).
detect_language (use ASCII-only marker words -- the italian markers che/della/sono/questo/come/
quindi are ASCII; do NOT put accented characters in the test file):
- Italian-dominant text (e.g. "che della sono questo come quindi") -> 'it'.
- English-dominant text with more than 3 english markers (e.g. "the and with that for this from")
  and no italian markers -> 'en'.
- Text with no markers (e.g. "xyz foo bar") -> 'mixed'.
- Text with exactly 3 english markers and no italian markers (e.g. "the and with") -> 'mixed'
  (the branch requires en_markers > 3).
Tests must be deterministic and hit no network and no filesystem.

## Constraints
- ASCII-only in all added code and comments (repo ADR-0021) -- no accented characters anywhere.
- Pure pytest; no new dependencies; do not touch the lockfile or any config file.
- Do NOT edit atomize.py or any non-test file. Single new test file only.
- Conventional Commit subject (lowercase), e.g.:
  test(atomize): direct tests for yaml_escape and detect_language helpers

## Acceptance (verify before delivering)
- The new test file passes:
  `python -m pytest -q chatgpt-recovery/pipeline/test_atomize_helpers.py`.
- No regressions elsewhere (tests pass).
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
