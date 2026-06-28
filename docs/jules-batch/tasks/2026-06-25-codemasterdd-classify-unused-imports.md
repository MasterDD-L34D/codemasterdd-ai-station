# Jules task -- remove two unused imports from classify.py

Repo: MasterDD-L34D/codemasterdd-ai-station.

## Scope (single file, no behaviour change)
Remove TWO unused top-level imports from `chatgpt-recovery/pipeline/classify.py`. Both are
imported but never referenced anywhere in the file (dead imports). Removing an unused import is
behaviour-preserving. Change ONLY these two import lines; touch nothing else in the file.

## Context (read first, read-only)
- `chatgpt-recovery/pipeline/classify.py`:
  - line ~32: `import frontmatter` -- the name `frontmatter` is NEVER used in this file.
  - line ~36: `from sentence_transformers import SentenceTransformer` -- the name
    `SentenceTransformer` is NEVER used in this file.
- VERIFY before removing (grep the whole file): `frontmatter` and `SentenceTransformer` each
  appear ONLY on their import line. If either is actually referenced elsewhere, leave it and note
  that in the PR -- do NOT remove a used import.
- Do NOT touch any other import. In particular `from collections import defaultdict` (line ~27)
  IS used (defaultdict at line ~462) -- keep it. Keep every other import as-is.

## File to modify (ONLY this one)
- `chatgpt-recovery/pipeline/classify.py` -- delete the two named unused import lines only.

## Constraints
- Single file; remove exactly the two unused import lines, nothing else (no reformatting, no
  reordering, no other edits). No behaviour change.
- ASCII-only (repo ADR-0021). No new dependencies; do not touch requirements.txt or any config.
- Do NOT install sentence_transformers, do NOT run the full pipeline, do NOT download anything --
  this is a static import removal; a syntax check is enough.
- Conventional Commit subject (lowercase), e.g.:
  refactor(classify): drop unused frontmatter and SentenceTransformer imports

## Acceptance (verify before delivering)
- After the edit, grep confirms `frontmatter` and `SentenceTransformer` no longer appear in
  `classify.py`.
- The file still parses: `python -c "import ast,sys; ast.parse(open('chatgpt-recovery/pipeline/classify.py').read()); print('ok')"`.
- No other line in the file is changed (the diff is exactly two deleted import lines).
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
