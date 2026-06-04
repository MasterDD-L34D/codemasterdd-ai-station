---
name: Repo layout decision
description: Canonical paths post 2026-05-12 deep cleanup — repos under Desktop\repos\, AI artifacts in Desktop\repos\_workspace\
type: project
originSessionId: 6a6e11ce-057d-45bf-a7fa-5a63626a3f01
---
## Active repos (12)
All consolidated under `C:\Users\VGit\Desktop\repos\<name>\`:
claude-supermemory-local, codemasterdd-ai-station, compass-marketplace, evo-swarm, Game-Database, Gpt, Item-generator, LeaD, Master-DD-Pathfinder-GPT, pathfinder-1e-homebrew, synesthesia, torneo-cremesi-site.

## Canonical exceptions (do NOT move)
- **Game** → `C:\Users\VGit\Desktop\Game` (active sprint 019+)
- **Game-Godot-v2** → `C:\Users\VGit\Desktop\Game-Godot-v2`
- **vault** → `C:\Users\VGit\Vault` (Obsidian-attached, dotfile-style sync)
- **Vault-ops** → `C:\Users\VGit\Vault-ops` (runtime caches, scripts, `.venv`, *.db — referenced by scripts. Do NOT relocate.)
- **evo-tactics-refs** → `C:\Users\VGit\Documents\evo-tactics-refs` (187GB asset library)
- Dotfile dirs at $HOME (`.claude`, `.codex`, `.cursor`, `.ollama`, etc.) — app convention, do NOT move.

## AI artifacts workspace (post 2026-05-12)
All AI/IA-generated docs/zips/reports moved to `C:\Users\VGit\Desktop\repos\_workspace\`:
- `evo-tactics\` (21 files + `assets\` 19 zips, ~346MB) — design docs, concept books, bundles
- `synesthesia\` (7 files) — operative docs, SQL schema, feedback PDF
- `research-reports\` (4 files) — deep-research-reports, CAMEL/AI swarm
- `game-design\` (4 files) — GDD master, CLAUDE.md root, piano operativo
- `desktop-meta\` (3 files) — analysis/catalog/snapshot
- `archives\` (6 files, 63MB) — Archivio_Libreria zips (4 dup), drive-download, ERMES
- `operative-library\` (109 files) — unzipped Archivio_Libreria_Operativa_Progetti (02_LIBRARY → 07_CLAUDE_CODE_OPERATING_PACKAGE)
- `vault-overflow\` (4 files, 695MB) — ex `_vault_excluded\GPT-Prompts-Archivi-ZIP-moved-20260424`

## Archives (read-only)
- `C:\Users\VGit\Documents\GitHub\Game` — frozen historical
- `C:\Users\VGit\_archive\duplicates-2026-05-12\` — 3 deduped repo copies
- `C:\Users\VGit\_archive\stale-backups-2026-05-12\` — 413MB old ZIP backups
- `C:\Users\VGit\_archive\junk-2026-05-12\` — `-1.14-windows.xml`, `-1.16-windows.xml`, `AMDRM_Install.log`

## How to apply
- New AI artifact → save to `Desktop\repos\_workspace\<category>\`, NOT to Desktop root.
- Repo references → `Desktop\repos\<name>\` (not old scattered paths).
- Wiring verified clean: `Vault-ops\scripts\*.py` only reference `Desktop\Pathfinder\` (user dir, untouched). `.claude\settings.json` plugin paths intact. No broken links from this cleanup.
- Empty parents removed: `Documents\GitHub`, `Desktop\pathfinder_master_dd_repo`, `Desktop\work`, `Desktop\GPT-Projects\Master-DD-Repo-Locale`, `source\repos`, `source`, `ansel`, `Desktop\proggetto`.

## Cleanup operations summary 2026-05-12
- Cloned 4 missing repos (pathfinder-1e-homebrew, Item-generator, Gpt, LeaD).
- Archived 3 duplicate repos; pulled 3 out-of-sync (evo-swarm +74, Game-Database +1, MDPGPT +2).
- Synced Vault canonical 054cad68 → 67c3bb28.
- Consolidated 7 scattered repos into `Desktop\repos\`.
- Moved ~197 AI-generated files (~1.1GB) into `_workspace\`.
- Archived 413MB stale backups + 3 junk files.
