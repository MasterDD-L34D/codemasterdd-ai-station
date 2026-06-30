# Docs Reorganization Proposal

## 1. Directory Map

| Directory | File Count | Inferred Purpose | Verdict |
|---|---|---|---|
| adr/ | 68 | Architecture Decision Records, authoritative | keep |
| appendici/ | 7 | Additional reference materials | merge-into-archive |
| architecture/ | 10 | System architecture docs | merge-into-core |
| archive/ | 198 | Deprecated or old docs (graveyard) | keep-as-archive |
| assets/ | 4 | Images/media for docs | keep |
| audio/ | 2 | Audio guidelines/docs | merge-into-design |
| balance/ | 10 | Game balance design/tuning | merge-into-design |
| biomes/ | 4 | Environment design docs | merge-into-design |
| catalog/ | 8 | Lists of game entities | merge-into-design |
| ci/ | 1 | CI/CD notes | merge-into-ops |
| combat/ | 12 | Combat system mechanics | merge-into-design |
| config/ | 1 | Configuration guides | merge-into-ops |
| core/ | 35 | Central source of truth, GDD | keep |
| design/ | 5 | General game design docs | keep |
| editorial/ | 1 | Text/narrative guidelines | merge-into-design |
| evo-tactics/ | 15 | Specific game module docs | merge-into-design |
| evo-tactics-pack/ | 264 | Data pack info/docs | merge-into-design |
| examples/ | 4 | Code/doc examples | merge-into-guide |
| frontend/ | 22 | Client side tech docs | merge-into-core |
| generated/ | 186 | Auto-generated summaries/references | gitignore-candidate |
| governance/ | 14 | Project rules and team process | merge-into-process |
| guide/ | 20 | Tutorials and how-tos | keep |
| handoff/ | 1 | Transition notes | merge-into-archive |
| hubs/ | 8 | Entry points/indexes | keep |
| incoming/ | 3 | Triage or unorganized docs | merge-into-archive |
| integrations/ | 1 | External tool integrations | merge-into-ops |
| logs/ | 15 | Raw outputs/link checks | gitignore-candidate |
| mission-console/ | 26 | Internal tooling docs | merge-into-ops |
| museum/ | 73 | Curated graveyard for reuse | keep |
| operativo/ | 1 | Operational notes | merge-into-ops |
| ops/ | 20 | Deployment/infrastructure | keep |
| pipelines/ | 30 | Automation workflows | merge-into-ops |
| pitch/ | 3 | Game pitch materials | merge-into-archive |
| planning/ | 234 | Roadmaps and audits | keep |
| playtest/ | 249 | Playtest reports and data | merge-into-qa |
| playtests/ | 9 | Older or redundant playtest dir | merge-into-qa |
| presentations/ | 9 | Slide decks/meeting notes | merge-into-archive |
| process/ | 50 | Workflows and methodologies | keep |
| prompts/ | 1 | AI prompt templates | merge-into-process |
| public/ | 9 | External facing materials | keep |
| qa/ | 19 | Testing guidelines and results | keep |
| reports/ | 460 | Audit and status reports | merge-into-qa |
| research/ | 47 | Exploratory deep dives | keep |
| runbook/ | 1 | Incident response | merge-into-ops |
| skiv/ | 3 | Specific feature docs | merge-into-design |
| species/ | 1 | Creature documentation | merge-into-design |
| superpowers/ | 36 | Abilities design | merge-into-design |
| templates/ | 1 | Document templates | merge-into-process |
| traits/ | 16 | Trait system docs | merge-into-design |
| tutorials/ | 8 | Learning resources | merge-into-guide |

*Notes on special directories:*
- generated/: Contains build artifacts like trait-reference.md; should be gitignored, not committed.
- archive/ & museum/: Both act as graveyards. archive/ is a flat storage, museum/ is curated for reuse.
- logs/: Contains raw output (e.g., link-check.log). Logs should not be tracked in docs; likely gitignore candidates.

## 2. Problems Found

1. Graveyard Bloat: Over 270 files split between archive/ and museum/ without clear separation rules for new docs.
2. Generated Files Committed: generated/ and logs/ contain ephemeral output polluting the repo history.
3. Overlapping Domains: playtest/, playtests/, reports/, and qa/ cover similar ground. Multiple design folders.
4. Naming Inconsistencies: Singular vs. plural (playtest vs playtests), Italian vs. English (appendici, operativo).
5. Shallow Directories: Too many top-level folders with fewer than 5 files (e.g., ci, config, handoff, audio).
6. Missing Top-Level Index: There is a lack of a clear, consolidated docs/README.md top-level index file.

## 3. Proposed Top-Level Structure

- adr/ -- Authoritative Architecture Decision Records. (folds in: none)
- archive/ -- Flat storage for deprecated documents. (folds in: appendici, handoff, incoming, pitch, presentations)
- assets/ -- Static media files supporting documentation. (folds in: none)
- core/ -- System architecture and central source of truth. (folds in: architecture, frontend)
- design/ -- Mechanics, balance, biomes. (folds in: audio, balance, biomes, catalog, combat, editorial, traits, skiv)
  (also folds in: evo-tactics, evo-tactics-pack, species, superpowers)
- guide/ -- How-to guides, tutorials, and examples. (folds in: examples, tutorials)
- hubs/ -- Entry point indexes for cross-cutting themes. (folds in: none)
- museum/ -- Curated repository of reusable past ideas. (folds in: none)
- ops/ -- Tooling, pipelines, and CI. (folds in: ci, config, integrations, mission-console, operativo, pipelines)
  (also folds in: runbook)
- planning/ -- Roadmaps, milestones, and strategic audits. (folds in: none)
- process/ -- Team workflows, governance, and templates. (folds in: governance, prompts, templates)
- public/ -- External-facing communication and assets. (folds in: none)
- qa/ -- Playtest logs, reports, and quality assurance. (folds in: playtest, playtests, reports)
- research/ -- Deep dives and exploratory findings. (folds in: none)

## 4. Migration Map

| Current Directory | Proposed Action / Target Directory |
|---|---|
| adr/ | keep in adr/ |
| appendici/ | move to archive/ |
| architecture/ | merge into core/ |
| archive/ | keep in archive/ |
| assets/ | keep in assets/ |
| audio/ | merge into design/ |
| balance/ | merge into design/ |
| biomes/ | merge into design/ |
| catalog/ | merge into design/ |
| ci/ | merge into ops/ |
| combat/ | merge into design/ |
| config/ | merge into ops/ |
| core/ | keep in core/ |
| design/ | keep in design/ |
| editorial/ | merge into design/ |
| evo-tactics/ | merge into design/ |
| evo-tactics-pack/ | merge into design/ |
| examples/ | merge into guide/ |
| frontend/ | merge into core/ |
| generated/ | REMOVE from git, add to .gitignore |
| governance/ | merge into process/ |
| guide/ | keep in guide/ |
| handoff/ | move to archive/ |
| hubs/ | keep in hubs/ |
| incoming/ | move to archive/ |
| integrations/ | merge into ops/ |
| logs/ | REMOVE from git, add to .gitignore |
| mission-console/ | merge into ops/ |
| museum/ | keep in museum/ |
| operativo/ | merge into ops/ |
| ops/ | keep in ops/ |
| pipelines/ | merge into ops/ |
| pitch/ | move to archive/ |
| planning/ | keep in planning/ |
| playtest/ | merge into qa/ |
| playtests/ | merge into qa/ |
| presentations/ | move to archive/ |
| process/ | keep in process/ |
| prompts/ | merge into process/ |
| public/ | keep in public/ |
| qa/ | keep in qa/ |
| reports/ | merge into qa/ |
| research/ | keep in research/ |
| runbook/ | merge into ops/ |
| skiv/ | merge into design/ |
| species/ | merge into design/ |
| superpowers/ | merge into design/ |
| templates/ | merge into process/ |
| traits/ | merge into design/ |
| tutorials/ | merge into guide/ |

## 5. No-Loss Note

This reorganization strictly groups and archives existing documents. No historical knowledge is deleted.
Files flagged under generated/ and logs/ are considered ephemeral build outputs and are candidates for .gitignore,
rather than archival storage. Everything else will be preserved byte-for-byte in its new destination.