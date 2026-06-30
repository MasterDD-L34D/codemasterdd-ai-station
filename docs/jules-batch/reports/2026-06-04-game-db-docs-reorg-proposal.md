# Documentation Reorganization Proposal

## 1. Directory Map
* catalog/ (1 file) | Reference catalogs for taxonomy entities | merge-into-reference
* insomnia/ (1 file) | API client export files (game-database.json) | gitignore-candidate
* operativo/ (7 files) | Team processes, roadmaps, runbooks, sprint templates | merge-into-process
* research/ (11 files) | Spike logs, audit notes, edge-case scenarios | archive
* rfc/ (2 files) | Formal proposals and design specs | merge-into-adr
* superpowers/ (18 files) | Detailed execution plans and specs for subagents | keep

Note: The insomnia/ directory contains generated output that should be gitignored rather than committed.

## 2. Problems Found
* Root bloat: There are 10 loosely related markdown files at the root of docs/ with no index.
* Missing index: No top-level docs/README.md to guide developers.
* Graveyard bloat: research/ contains many dated, one-off spike logs.
* Generated files committed: insomnia/game-database.json is an export and should be gitignored.
* Naming inconsistencies and language drift: Mixed Italian (operativo) and English (research), singular/plural mixing.

## 3. Proposed Top-Level Structure
* adr/: Architecture Decision Records and formal proposals (authoritative). Folds in rfc/.
* archive/: Old research, out-of-date docs, and graveyard files. Folds in research/.
* process/: Team workflows, runbooks, roadmaps, and onboarding guides. Folds in operativo/.
* reference/: Schema documentation, catalogs, and API references. Folds in catalog/.
* superpowers/: Subagent execution plans and task specs. Retains current structure.

## 4. Migration Map
| Current Dir/File | Proposed Dir/Action |
|------------------|---------------------|
| catalog/         | reference/          |
| insomnia/        | gitignore (remove)  |
| operativo/       | process/            |
| research/        | archive/            |
| rfc/             | adr/                |
| superpowers/     | superpowers/        |
| root *.md files  | move to process/ or reference/ or archive/ based on content |

Standout files:
* insomnia/game-database.json: Must be removed from git and added to .gitignore.
* docs/README.md: Needs to be created as the main entry point (index).

## 5. No-loss Note
All documentation will be PRESERVED. Files are only grouped into logical directories or moved to archive/.
Nothing will be deleted, except for the insomnia/ export which is flagged as a gitignore candidate.