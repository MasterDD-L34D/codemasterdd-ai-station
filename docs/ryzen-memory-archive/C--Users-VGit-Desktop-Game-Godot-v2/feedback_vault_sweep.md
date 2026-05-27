---
name: Vault sweep workflow
description: Periodic check vault `MasterDD-L34D/vault` per contraddizioni vs CLAUDE.md + materiale nuovo → museum cards
type: feedback
originSessionId: c77e9715-286a-45d7-9987-55a73d50a206
---
Vault `MasterDD-L34D/vault` è private Obsidian + Karpathy LLM-wiki overlay. Periodicamente fai sweep per chiarezza info.

**Why**: master-dd 2026-05-11 chiarito "una cosa del genere non la ricordi" → vault è source-of-truth secondaria + design proposals + ADR cross-stack che NON vivono nel repo CLAUDE.md. Drift accumulato silently.

**How to apply**:
1. Quando master-dd dice "controlla vault" / "verifica vs vault" / "cosa c'è di nuovo in vault" → leggi via `gh api repos/MasterDD-L34D/vault/contents/<path> --jq '.content' | base64 -d` (no MCP dep needed, CLI sufficiente)
2. Tree probe rapido: `gh api repos/MasterDD-L34D/vault/contents/<folder> --jq '.[].name'`
3. Focus aree alto-valore: `Spaces/Dev/Evo-Tactics/{PILLARS_STATUS.md,adr/,design-log/}` (40+ ADR, watcher ollama output, playtest log)
4. Contraddizioni vs CLAUDE.md OR materiale nuovo → curate card sotto `docs/museum/cards/<slug>.md` per `_template-card.md` schema (Dublin Core provenance + relevance_score 1-5 + reuse_path)
5. Update `docs/museum/MUSEUM.md` index per domain + Top relevance (≥4)
6. Always include vault path in card `provenance.found_at` field

**Found 2026-05-11 sweep** (baseline):
- `Spaces/Dev/Evo-Tactics/PILLARS_STATUS.md` last rev 2026-04-17 → tutti 6 pilastri 🟡 post-playtest M1 vs CLAUDE.md sprint context P1/P2/P3/P5 🟢
- 4 ADR `proposed` 2026-05-10 (tattica-mosse-sintassi / prominence-job-abilities / pressure-tier-scaling / adjust-ai-aggressiveness) auto-gen ollama
- Playtest M1 2026-04-17 first documented session (WIN PG round 3 wipe Sistema, 4 FRICTION)
- `evo-tactics-design-watcher` agent vault `wip/agents/` (ollama deepseek-r1:14b, weekly cadence possible)

**Cadence suggested**: ogni 2-3 settimane O dopo master-dd checkpoint design call O quando CLAUDE.md sprint context cresce >50 righe nuove.

## ⚠️ Quote source carefully

`C:\Users\VGit\Desktop\CLAUDE.md` è **parent superseded** (header dice "STALE — Do NOT use", snapshot 2026-04-16 web stack v1). CLAUDE.md canonical Godot v2 è root repo `<worktree>/CLAUDE.md`. Quando citi statement CLAUDE.md, **verify quote via** `grep -n` direct vs il file canonical NON parent superseded.

**Codex P2 finding 2026-05-11 PR #219**: ho citato "P1/P2/P3/P5 🟢" preso da parent superseded → fix `48b3cbe`. Lesson: per cross-stack divergence cards, sempre verify CLAUDE.md attuale con `grep -n "pillar\|🟢\|🟡" CLAUDE.md` prima di citare.
