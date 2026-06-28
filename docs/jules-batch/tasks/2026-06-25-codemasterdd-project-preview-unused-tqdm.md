# Jules task -- remove one unused import from project-preview.py

Repo: MasterDD-L34D/codemasterdd-ai-station.

## Scope (single file, no behaviour change)
Remove ONE unused top-level import from `chatgpt-recovery/pipeline/project-preview.py`:
`from tqdm import tqdm`. The name `tqdm` is imported but never referenced in the file (dead
import). Removing an unused import is behaviour-preserving. Change ONLY that one import line;
touch nothing else in the file.

## Context (read first, read-only)
- `chatgpt-recovery/pipeline/project-preview.py`, line ~30: `from tqdm import tqdm`. The name
  `tqdm` is NEVER used anywhere else in the file (verified: it appears only on the import line).
- VERIFY before removing: grep the whole file for `tqdm`; it must appear ONLY on that import
  line. If it is actually referenced elsewhere, leave it and say so in the PR -- do NOT remove a
  used import. Keep every other import as-is.

## File to modify (ONLY this one)
- `chatgpt-recovery/pipeline/project-preview.py` -- delete the single unused `tqdm` import line only.

## Constraints
- Single file; remove exactly the one unused import line, nothing else (no reformatting, no
  reordering, no other edits). No behaviour change.
- ASCII-only (repo ADR-0021). No new dependencies; do not touch requirements.txt or any config.
- Do NOT install anything, do NOT run the full pipeline, do NOT download anything -- a static
  import removal; a syntax check is enough.
- Conventional Commit subject (lowercase), e.g.:
  refactor(project-preview): drop unused tqdm import

## Acceptance (verify before delivering)
- After the edit, grep confirms `tqdm` no longer appears in `project-preview.py`.
- The file still parses: `python -c "import ast; ast.parse(open('chatgpt-recovery/pipeline/project-preview.py').read()); print('ok')"`.
- The diff is exactly one deleted import line; no other line changed.
- Deliver as ONE branch + ONE pull request to main; do NOT merge.
