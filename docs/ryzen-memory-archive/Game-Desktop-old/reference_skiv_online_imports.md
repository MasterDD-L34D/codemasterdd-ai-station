# Skiv online imports — reference (2026-04-25)

PC-local reference for online libraries adopted inline in Skiv-as-Monitor stack.
Cross-link with repo doc `docs/research/2026-04-25-skiv-online-imports.md` (canonical SoT).

## Quick lookup

| Source | Adopted as | LOC | ROI |
|---|---|---|:--:|
| galaxykate/tracery (Apache 2.0) | `tools/py/skiv_tracery.py` | 218 | 5/5 |
| videlais/simple-qbn (MIT) | `tools/py/skiv_qbn.py` + YAML | 100+14 | 4/5 |
| Conventional Commits spec | `parse_conventional_commit()` in `skiv_monitor.py` | 30 | 3/5 |

## Voice expansion stats

- Static palette: 131 lines × 21 categories
- Lifecycle YAML: 15 lines × 5 fasi
- Tracery effective: **662 combinatorial voices** (vs 131 atomic = +400%)
- QBN storylets: 14 (replace `WEEKLY_DIGEST_TEMPLATES`)

## Determinism guarantee

All seeded via `hash(seed + symbol + depth)`:
- `skiv_tracery.flatten(grammar, symbol, seed)` → replay-safe
- `skiv_qbn.select_storylet(qualities, state)` → tie-break alpha id
- `skiv_monitor.voice_pick()` → 50% tracery / 25% lifecycle / 25% static

## Cross-references

- Repo doc: `docs/research/2026-04-25-skiv-online-imports.md`
- LIBRARY.md section: "Online libraries shipped inline"
- Plan: `docs/planning/2026-04-25-skiv-monitor-plan.md`

## Deferred (need npm dep approval)

- @octokit/webhooks-types (typed payload)
- @octokit/webhooks (Node handler)
- OpenGameArt CC0 sprites raster (manual download required)
- LPC reptile sprites (dual-license CC-BY-SA + GPL)
