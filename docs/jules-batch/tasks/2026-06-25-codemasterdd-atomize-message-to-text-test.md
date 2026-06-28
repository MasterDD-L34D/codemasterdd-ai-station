# Jules task -- direct unit tests for atomize.py message_to_text

Repo: MasterDD-L34D/codemasterdd-ai-station.

## Scope (single file, test-only, NO behaviour change)
Add a NEW pytest file with direct tests for the named pure function `message_to_text(msg)` in
`chatgpt-recovery/pipeline/atomize.py`. This is a test-only change: do NOT modify `atomize.py` or
any production code. Read it read-only to learn the CURRENT behaviour, then assert THAT behaviour.
No logic change, no behaviour change anywhere.

## Context (read first, read-only)
- `chatgpt-recovery/pipeline/atomize.py`, function `message_to_text(msg)` (around line 101). Pure,
  deterministic, no I/O. It maps a ChatGPT message dict to a string by `content.content_type`.
  `atomize.py` is a standalone script (argparse main guarded by `if __name__ == "__main__"`) and
  imports ONLY stdlib, so import it WITHOUT a sys.path hack via importlib from its file path:
      import importlib.util
      from pathlib import Path
      _spec = importlib.util.spec_from_file_location(
          "atomize_mod", Path(__file__).resolve().parent / "atomize.py")
      atomize_mod = importlib.util.module_from_spec(_spec)
      _spec.loader.exec_module(atomize_mod)
      message_to_text = atomize_mod.message_to_text
  Do NOT install anything or download anything.
- Behaviour to assert (read the function to confirm exact strings):
  - metadata `is_visually_hidden_from_conversation` true -> '' (regardless of content).
  - content_type 'text' -> the string parts joined by newlines (non-str parts skipped).
  - content_type 'code' -> '```\n' + content['text'] + '\n```'.
  - content_type 'multimodal_text' -> string parts kept as-is; a part dict with
    content_type 'image_asset_pointer' becomes '![image: <pointer>]' where <pointer> is the
    asset_pointer with the 'sediment://' and 'file-service://' prefixes stripped; joined by newlines.
  - content_type 'thoughts' -> '<details>\n<summary>Thinking</summary>\n\n<text>\n\n</details>'
    when text is non-empty, else ''.
  - content_type 'reasoning_recap' -> '*Reasoning recap: <text>*' when non-empty, else ''.
  - content_type 'tether_browsing_display' -> '> **Browsing Result:** <text>' when non-empty, else ''.
  - content_type 'model_editable_context' -> ''.
  - an unknown content_type, or a msg with no/empty content -> ''.

## File to modify (ONLY this one)
- NEW `chatgpt-recovery/pipeline/test_atomize_message_to_text.py`

## What the tests must assert (CURRENT behaviour; assert exact return values, do NOT "fix")
Build minimal msg dicts of the shape `{"content": {"content_type": ..., "parts"/"text": ...},
"metadata": {...}}` and cover at least: text join, code fences, multimodal text + an
image_asset_pointer (assert the prefix stripping), thoughts non-empty AND empty, reasoning_recap,
tether_browsing_display, model_editable_context -> '', a visually-hidden message -> '', an unknown
content_type -> '', and an empty `{}` message -> ''. Deterministic; no network, no filesystem.

## Constraints
- ASCII-only in all added code and comments (repo ADR-0021).
- Pure pytest; no new dependencies; do not touch the lockfile or any config file.
- Do NOT edit atomize.py or any non-test file. Single new test file only.
- Conventional Commit subject (lowercase), e.g.:
  test(atomize): direct tests for message_to_text content-type branches

## Acceptance (verify before delivering)
- The new test file passes:
  `python -m pytest -q chatgpt-recovery/pipeline/test_atomize_message_to_text.py`.
- No regressions elsewhere (tests pass).
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
