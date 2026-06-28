---
title: Museum index -- CodeMasterDD AI Station (hub / process landmarks)
maintained_by: hub session (manual curation)
last_updated: 2026-06-25
status: live
---

# MUSEUM -- CodeMasterDD AI Station

> Curated archive of hub-level landmark decisions, operational patterns, and governance
> archaeology for the codemasterdd-ai-station hub. Counterpart to the Game-family museums
> (which archive game-design/mechanics archaeology). Read this before re-deriving a governance
> stance or re-litigating a merge/Jules workflow decision.

## Scope (what belongs here)

- **Hub/process landmarks**: governance decisions (merge-autonomy, SDMG resolutions), recurring
  operational patterns (Jules cycle, delivery-miss, salvage), cross-fleet ops doctrine.
- NOT game-design archaeology -- that lives in the Game-family museums (cross-linked below).
- Recent curated records are fine here (decision archaeology), not only "buried" artifacts.

## Card index

### Top relevance (>= 4)

- [Merge-authority -- grant verbale vs doctrine SDMG-survived](cards/2026-06-25-merge-authority-grant-vs-doctrine.md)
  -- un grant reattivo NON supera ADR-0037 (deliberata + falsificata); codemasterdd auto-merge ATTIVO,
  Game-family solo via amendment+SDMG. `relevance=5`.
- [Jules delivery-miss 7/7 -- salvage obbligatorio](cards/2026-06-25-jules-delivery-miss-salvage-pattern.md)
  -- 7/7 dispatch COMPLETED senza PR; salvage-da-changeSet = fase fissa del ciclo, non eccezione.
  `relevance=5`.

## Folder layout

| Path | Purpose |
|------|---------|
| `docs/museum/MUSEUM.md` | This index (hub/process landmarks). |
| `docs/museum/cards/<slug>.md` | One Dublin-Core-style card per landmark. |

Card format mirrors the Game-family museum `_template-card.md` (type/domain/provenance/relevance +
Summary / What / Why-buried / Why-matters / Reuse / Sources / Risks).

## Cross-references (museum network)

- **Game museum**: `Game/docs/museum/MUSEUM.md` (game-design + mechanics + process archaeology,
  repo-archaeologist agent). Sibling: `MasterDD-L34D/Game`.
- **Godot-v2 museum**: `Game-Godot-v2/docs/museum/MUSEUM.md` (Godot port archaeology).
- **Vault**: `MasterDD-L34D/vault` -- personal Obsidian + Karpathy overlay; consult before research
  dives (`gh api repos/MasterDD-L34D/vault/contents/<path>`).
- **Hub doctrine**: `docs/adr/` + memory (`feedback_merge_authority`, `feedback_jules_failed_recovery`).

> TODO (follow-up, external-repo write -> Eduardo-merge): add a reciprocal link to this hub museum
> from the Game + Godot-v2 `MUSEUM.md` cross-references, so the museum network is bidirectional.
